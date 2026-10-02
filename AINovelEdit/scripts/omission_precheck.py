#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
omission_precheck.py — Common Omission Pre-check: общий детерминированный слой
поиска потенциально непокрытых содержательных JA-фрагментов.

Архитектура
-----------
    JA + RU + context
            ↓
    Common Omission Pre-check      ← ЭТОТ скрипт (технический слой, НЕ аудитор)
            ↓
    Audit A   Audit B   Audit C     (независимые LLM-сессии)
            ↓
    Analyzer                        (принимает окончательное решение)

Pre-check выполняется ДО независимых аудиторских сессий. Он НЕ является
отдельным LLM-аудитором («Auditor D»), НЕ меняет специализации A/B/C и НЕ
принимает вердиктов: он создаёт evidence/candidates уровня `severity=CANDIDATE`.
Финальное решение (CONFIRMED_ERROR / DISPUTED / FALSE_POSITIVE / OPTIONAL)
принимает Analyzer по сверке JA → RU.

Сигналы (все детерминированные, по merged: JA ↔ ED_RU, иначе RU)
-----------------------------------------------------------------
S1  Обрыв хвоста (truncation): RU покрывает только префикс JA-реплик —
    реплик-маркеров в RU меньше, чем реплик в JA, и абзацев в RU меньше,
    чем в JA. Непокрытыми считаются JA-звенья ПОСЛЕ последней покрытой реплики.
S2  Пустой / почти пустой RU при содержательном JA (FULL omission).
S3  Числовой якорь: в JA-звенье есть число, которого нет нигде в RU, —
    число редко сжимается, сигнал локализует ПРОПУСК ВНУТРИ БЛОКА.

Защита от ложных срабатываний (обязательна)
--------------------------------------------
* «JA длиннее RU» само по себе НЕ сигнал: сравнение идёт по числу абзацев и
  реплик, а не по длине текста.
* Слияние (один RU-абзац покрывает несколько JA-абзацев) НЕ считается
  пропуском: если число реплик в RU не меньше, чем в JA, хвост считается
  покрытым — блок с слиянием не порождает candidate (см. selftest).
* Если сигналов недостаточно — finding не создаётся.
* Pre-check никогда не ставит `severity=ERROR`: только `CANDIDATE`
  (+ `confidence` HIGH/MEDIUM/LOW).

Использование:
    python scripts/omission_precheck.py --file v3-ch04.md
    python scripts/omission_precheck.py --file v3-ch04.md --block 15
    python scripts/omission_precheck.py --file v3-ch04.md --report --json
    python scripts/omission_precheck.py --selftest

Куда пишется:
    output/_audit/sma/<chapter>/precheck/omission-precheck.json   (evidence)
    output/_audit/sma/<chapter>/precheck/omission-precheck.md     (human-readable)

Раскладка каталогов главы: a/ — evidence Auditor A, b/ — evidence Auditor B,
c/ — evidence Auditor C, precheck/ — ЭТОТ детерминированный слой (не аудитор,
не run kind, не входит в SMA_KINDS), analysis/ — финальные результаты
Analyzer и слепые выводы Фазы 1 (<id>.phase1.json).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import merged_io  # noqa: E402
from semantic_findings import (  # noqa: E402
    OMISSION_SCOPES, classify_omission_scope, validate_analysis_result,
    validate_finding,
)

BASE = Path(__file__).resolve().parent.parent
MERGED = BASE / "translates" / "_report" / "merged"

# --- пороги (откалиброваны на корпусе: ~2.5% edited-блоков дают candidate) ---
MIN_UNCOVERED = 2      # минимум непокрытых JA-звеньев
MIN_UNIT_DEFICIT = 1   # абзацев RU должно быть МЕНЬШЕ, чем JA (нет — нет пропуска)
HIGH_UNCOVERED = 4     # порог HIGH-уверенности (вместе с MIN_UNIT_DEFICIT)
HIGH_DEFICIT = 3

SPEECH_START = ("—", "-", "«", "\"", "»")
NUM_RE = re.compile(r"[0-9]+")
CHECK_TYPE = "omission-precheck"


# --------------------------------------------------------------------------- #
# Разбор текста
# --------------------------------------------------------------------------- #

def split_units(text):
    """Абзацы блока (пустые строки/комментарии отброшены); «—» = пусто."""
    text = (text or "").strip()
    if not text or text == "—":
        return []
    return [l.strip() for l in text.splitlines() if l.strip()]


def is_speech(line):
    return line.startswith(SPEECH_START)


def has_speech_marker(line):
    return line.startswith(SPEECH_START) or "«" in line




# --------------------------------------------------------------------------- #
# Анализ одного блока
# --------------------------------------------------------------------------- #

def anchor_numbers(text):
    """Числовые якоря: только 2+-значные (однозначные часто пишутся словом)."""
    return {t for t in NUM_RE.findall(text or "") if len(t) >= 2}


def analyze_block(ja_text, ru_text):
    """Детерминированные сигналы одного блока → словарь (без вердиктов)."""
    ja_units = split_units(ja_text)
    ru_units = split_units(ru_text)
    ja_turn_units = [i for i, u in enumerate(ja_units) if "「" in u]
    n_ja_turns = sum(u.count("「") for u in ja_units)
    n_ru_turns = sum(1 for u in ru_units if is_speech(u))
    unit_deficit = len(ja_units) - len(ru_units)

    # --- S1/S2: обрыв хвоста (непокрытые JA-звенья) ---
    uncovered_idx = []
    if ja_units and not ru_units:                       # S2: RU пуст
        uncovered_idx = list(range(len(ja_units)))
    elif n_ja_turns > n_ru_turns and ja_turn_units:
        if n_ru_turns == 0:                             # реплик в RU нет
            uncovered_idx = list(range(len(ja_units)))
        else:
            last = ja_turn_units[n_ru_turns - 1]        # RU покрывает префикс
            uncovered_idx = list(range(last + 1, len(ja_units)))

    # --- S3: числовые якоря (локализация внутри блока) ---
    ru_anchor = anchor_numbers(ru_text)
    num_idx = [i for i, u in enumerate(ja_units)
               if anchor_numbers(u) - ru_anchor]

    return {
        "ja_units": ja_units, "ru_units": ru_units,
        "n_ja": len(ja_units), "n_ru": len(ru_units),
        "unit_deficit": unit_deficit,
        "n_ja_turns": n_ja_turns, "n_ru_turns": n_ru_turns,
        "turn_deficit": n_ja_turns - n_ru_turns,
        "uncovered_idx": uncovered_idx, "num_idx": num_idx,
    }


def _scope_for(units_text, n):
    """Масштаб по содержанию непокрытых JA-звеньев (классификатор схемы)."""
    has_dialogue = any("「" in u for u in units_text)
    if has_dialogue:
        return classify_omission_scope(missing_units=n, unit_kind="dialogue")
    if n <= 1:
        return classify_omission_scope(missing_units=n, unit_kind="sentence")
    if n <= 3:
        return classify_omission_scope(missing_units=n, unit_kind="sentence")
    return classify_omission_scope(missing_units=n, unit_kind="sentence",
                                   block_part=True)


def decide(a):
    """→ (найден?, начало_непокрытых_индексов, omission_kind, scope, confidence,
    доминирующий_сигнал) либо None, если сигналов недостаточно."""
    ja_units, ru_units = a["ja_units"], a["ru_units"]
    if not ja_units:
        return None

    # S2 — пустой / почти пустой RU при содержательном JA
    if not ru_units or (a["n_ru"] <= 2 and a["n_ja"] >= 8):
        idx = list(range(len(ja_units)))
        scope = "FULL_BLOCK"
        return idx, "FULL", scope, "HIGH", "S2-empty-ru"

    # S1 — обрыв хвоста; обязательна коррекция «абзацев в RU меньше, чем в JA»
    if (len(a["uncovered_idx"]) >= MIN_UNCOVERED
            and a["unit_deficit"] >= MIN_UNIT_DEFICIT):
        idx = a["uncovered_idx"]
        scope = _scope_for([ja_units[i] for i in idx], len(idx))
        kind = "PARTIAL" if a["n_ru_turns"] > 0 else "FULL"
        conf = ("HIGH" if (len(idx) >= HIGH_UNCOVERED
                           and a["unit_deficit"] >= HIGH_DEFICIT)
                else "MEDIUM")
        return idx, kind, scope, conf, "S1-tail-truncation"

    # S3 — числовой якорь: локальный пропуск внутри блока
    if a["num_idx"]:
        idx = a["num_idx"]
        scope = _scope_for([ja_units[i] for i in idx], len(idx))
        return idx, "FULL", scope, "HIGH", "S3-number-anchor"

    return None


# --------------------------------------------------------------------------- #
# Сборка evidence (формат pre-check, не формат A/B/C)
# --------------------------------------------------------------------------- #

def build_finding(block, a, decision, ru_before="", ru_after=""):
    """→ omission-finding уровня CANDIDATE (никогда не ERROR).

    `ru_before`/`ru_after` — текст соседних блоков; используются, когда сам
    блок не содержит RU (S2) или обрыв уходит за границу блока.
    """
    idx, kind, scope, conf, signal = decision
    ja_units, ru_units = a["ja_units"], a["ru_units"]
    ja_span = "\n\n".join(ja_units[i] for i in idx)
    if ru_units:
        ru_before = ru_units[-1]
    elif not ru_before:
        ru_before = "(отредактированный RU в блоке отсутствует)"
    present = set()
    for i in idx:
        present |= anchor_numbers(ja_units[i])
    missing_nums = sorted(present - anchor_numbers("\n".join(ru_units)))
    pos = "%d…%d из %d" % (idx[0] + 1, idx[-1] + 1, len(ja_units))

    not_compression = (
        "Это обрыв, а не компрессия: в RU {n_ru} абзацев против {n_ja} в JA и "
        "{n_ru_turns} реплик-маркеров против {n_ja_turns} в JA — реплики и "
        "абзацы JA начиная с позиции {pos} не покрыты вовсе. Допустимое сжатие "
        "и слияние (один RU-абзац вместо нескольких JA) сохраняют число реплик "
        "и все звенья; здесь же хвост JA отсутствует. Сравнение длины текста "
        "JA/RU в проверке НЕ использовалось. Решение принимает Analyzer."
    ).format(n_ru=a["n_ru"], n_ja=a["n_ja"], n_ru_turns=a["n_ru_turns"],
             n_ja_turns=a["n_ja_turns"], pos=pos)

    evidence = (
        "signal={sig}; unit_deficit={ud}; turn_deficit={td}; uncovered={un}; "
        "n_ja={nj}; n_ru={nr}; ja_turns={jt}; ru_turns={rt}; "
        "missing_numbers={nums}; positions={pos}"
    ).format(sig=signal, ud=a["unit_deficit"], td=a["turn_deficit"],
             un=len(idx), nj=a["n_ja"], nr=a["n_ru"],
             jt=a["n_ja_turns"], rt=a["n_ru_turns"],
             nums=",".join(missing_nums) or "-", pos=pos)

    reason = (
        "JA содержит {un} содержательных звеньев (позиции {pos}) без "
        "соответствия в RU{tail}. Это кандидат уровня CANDIDATE, а не "
        "подтверждённая ошибка."
    ).format(un=len(idx), pos=pos,
             tail=", хвост RU обрывается раньше конца JA"
             if signal == "S1-tail-truncation" else "")

    return {
        "block": block,
        "issue_type": "MISSING_TRANSLATION",
        "omission_scope": scope,
        "omission_kind": kind,
        "severity": "CANDIDATE",
        "confidence": conf,
        "precheck_signal": signal,
        "source": ja_span,
        "current": ru_before,
        "ja_span": ja_span,
        "ru_before": ru_before,
        "ru_after": ru_after,
        "missing_content": "Непокрытые JA-звенья (%s):\n%s" % (pos, ja_span),
        "not_compression_reason": not_compression,
        "evidence": evidence,
        "reason": reason,
    }


def precheck_chapter(chapter, only=None):
    """→ (findings, число_проверенных_отредактированных_блоков).

    Сверяются JA ↔ ED_RU (текущий отредактированный русский текст). Блоки без
    ED_RU пропускаются — они уже покрыты сигналом `no-translation`
    (scripts/check_alignment.py).
    """
    path = MERGED / chapter
    if not path.exists():
        raise SystemExit("ОШИБКА: нет merged-файла %s — прогони "
                         "scripts/update_merged.py" % path)
    items = merged_io.read_merged(path)
    findings, edited = [], 0
    prev_ru_last = ""
    for i, (num, fields) in enumerate(items):
        if only and num not in only:
            continue
        ed = (fields.get("ED_RU") or "").strip()
        if not ed or ed == "—":
            continue
        edited += 1
        a = analyze_block(fields.get("JA", ""), ed)
        decision = decide(a)
        if not decision:
            if a["ru_units"]:
                prev_ru_last = a["ru_units"][-1]
            continue
        ru_after = ""
        if i + 1 < len(items):
            nxt = split_units((items[i + 1][1].get("ED_RU") or ""))
            if nxt:
                ru_after = nxt[0]
        findings.append(build_finding(num, a, decision,
                                      ru_before=prev_ru_last,
                                      ru_after=ru_after))
        if a["ru_units"]:
            prev_ru_last = a["ru_units"][-1]

    # обрыв, переходящий через границу блока → MULTI_BLOCK
    # (громоздятся только S1/S2-обрывы: S3 — локальный числовой пропуск)
    run = []
    for fnd in [f for f in findings
                if f["precheck_signal"].startswith(("S1", "S2"))] + [None]:
        if fnd is not None and run and fnd["block"] == run[-1]["block"] + 1:
            run.append(fnd)
            continue
        if len(run) >= 2:
            for r in run:
                r["omission_scope"] = "MULTI_BLOCK"
                r["evidence"] += "; adjacent_run=%d" % len(run)
        run = [fnd] if fnd is not None else []
    return findings, edited


# --------------------------------------------------------------------------- #
# Вывод
# --------------------------------------------------------------------------- #

def render_evidence(chapter, findings):
    """JSON-evidence для Analyzer (отдельная модель, не формат A/B/C)."""
    return {"check_type": CHECK_TYPE, "chapter": chapter,
            "findings": findings}


def render_report(chapter, findings, edited):
    from semantic_findings import render_omission_report
    lines = [
        "# Omission pre-check (Common Omission Pre-check): %s" % chapter,
        "",
        "- **check_type:** `%s`" % CHECK_TYPE,
        "- **Глава:** %s" % chapter,
        "- **Проверено отредактированных блоков (ED_RU):** %d" % edited,
        "- **Candidates:** %d" % len(findings),
        "- **Уровень:** `severity=CANDIDATE` — pre-check не принимает решений; "
        "статус (CONFIRMED_ERROR / DISPUTED / FALSE_POSITIVE / OPTIONAL) "
        "выносит Analyzer по сверке JA → RU.",
        "- **Сигналы:** S1 обрыв хвоста, S2 пустой RU, S3 числовой якорь.",
        "- **Защита от FP:** сравнение длины JA/RU не используется; слияние "
        "абзацев без потери реплик не считается пропуском.",
        "",
    ]
    if not findings:
        lines += ["Кандидатов не обнаружено.", ""]
    for f in findings:
        lines += [render_omission_report(f, block=f["block"]), "",
                  "Confidence: %s | Signal: %s" % (f["confidence"],
                                                   f["precheck_signal"]),
                  "---", ""]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# Selftest: фикстуры (детерминированные, реальный перевод не изменяется)
# --------------------------------------------------------------------------- #

FULL_JA = "\n".join([
    "「行くぞ！」", "彼は扉を開けた。", "「待て！」",
    "少女が叫んだ。", "「わかった」", "彼は頷いた。",
])

PRE_FIX_BLOCK15_RU = "\n".join([
    "— Чем это ты занимаешься?",
    "— Не то. Это, не то. Луиза, это не то, что ты думаешь.",
    "— Чем ты занимался на чужой кровати?",
    "— Это долгая история. Сиеста, ну, принесла мне чай в баню…",
    "— Оправдания не нужны. Вообще-то фамильяр, вытворяющий такое на кровати "
    "своей госпожи, — этого я никак не могу простить.",
    "— Да говору же, не то! Я не собирался…",
    "— На этот раз я по-настоящему разозлилась.",
    "Из глаз Луизы покатилась слеза.",
    "Сайто поднялся и схватил Луизу за плечи.",
    "— Да выслушай ты меня. Это недоразумение.",
])

NUMBER_JA = "\n".join([
    "彼は1975年の本を読んだ。", "「それは奇妙だ」",
    "彼はうなずいた。", "「もう一度見よう」",
])
NUMBER_RU = "\n".join([
    "— Это странно.", "Он кивнул.", "— Посмотрим ещё раз.",
])

# JA существенно длиннее RU при ПОЛНОМ покрытии всех реплик → пропуска НЕТ
COMPRESS_JA = "\n".join([
    "「行くぞ！」",
    "Он медленно, очень медленно и с большим сомнением открыл тяжёлую дверь, "
    "оборачиваясь несколько раз на звук шагов позади.",
    "「待て！」",
    "Девочка крикнула так громко, что эхо разнеслось по всему коридору и "
    "снова вернулось к ним.",
    "「わかった」",
    "Он кивнул и продолжал стоять, не делая ни одного шага вперёд.",
])
COMPRESS_RU = "\n".join(["— Пойдём!", "— Жди!", "— Ладно."])


def _real_ja(block):
    return dict(merged_io.read_merged(MERGED / "v3-ch04.md"))[block]["JA"]


def _finding(ja, ru, block=1, ru_before="", ru_after=""):
    a = analyze_block(ja, ru)
    d = decide(a)
    return (build_finding(block, a, d, ru_before=ru_before,
                          ru_after=ru_after) if d else None), a, d


def run_selftest():
    failed, total = [], [0]

    def check(ok, label):
        total[0] += 1
        print(("  OK   " if ok else "  FAIL ") + label)
        if not ok:
            failed.append(label)

    print("== 1. полный omission (S2: RU пуст) ==")
    f, a, d = _finding(FULL_JA, "", ru_before="— Он молчал.")
    check(f is not None, "находка создана")
    if f:
        check(f["omission_kind"] == "FULL",
              "kind=FULL (got %s)" % f["omission_kind"])
        check(f["omission_scope"] == "FULL_BLOCK",
              "scope=FULL_BLOCK (got %s)" % f["omission_scope"])
        check(f["confidence"] == "HIGH",
              "confidence=HIGH (got %s)" % f["confidence"])
        check(f["precheck_signal"] == "S2-empty-ru", "signal=S2-empty-ru")

    print("== 2. partial omission (S1: RU обрывается раньше конца JA) ==")
    f, a, d = _finding(FULL_JA, "— Пойдём!\nОн открыл дверь.")
    check(f is not None, "находка создана")
    if f:
        check(f["omission_kind"] == "PARTIAL",
              "kind=PARTIAL (got %s)" % f["omission_kind"])
        check(f["omission_scope"] == "DIALOGUE_FRAGMENT",
              "scope=DIALOGUE_FRAGMENT (got %s)" % f["omission_scope"])
        check(bool(f["ja_span"]), "ja_span непустой")
        check(f["ru_before"] == "Он открыл дверь.",
              "ru_before = последний абзац RU")

    print("== 3. omission внутри блока (S3: числовой якорь) ==")
    f, a, d = _finding(NUMBER_JA, NUMBER_RU)
    check(f is not None, "находка создана")
    if f:
        check(f["precheck_signal"] == "S3-number-anchor", "signal=S3")
        check(f["omission_kind"] == "FULL", "kind=FULL (got %s)" % f["omission_kind"])
        check(f["omission_scope"] in OMISSION_SCOPES,
              "scope в схеме (%s)" % f["omission_scope"])
        check("1975" in f["ja_span"],
              "локализация: пропущено именно JA-звенье с числом")

    print("== 4. multi-segment: один finding на несколько связанных звеньев ==")
    f, a, d = _finding(_real_ja(15), PRE_FIX_BLOCK15_RU, block=15)
    check(f is not None, "находка создана")
    if f:
        check(f["omission_scope"] == "DIALOGUE_FRAGMENT",
              "scope=DIALOGUE_FRAGMENT (got %s)" % f["omission_scope"])
        check(f["omission_kind"] == "PARTIAL",
              "kind=PARTIAL (got %s)" % f["omission_kind"])
        check(f["confidence"] == "HIGH",
              "confidence=HIGH (got %s)" % f["confidence"])
        check(len(a["uncovered_idx"]) == 6,
              "ровно 6 непокрытых звеньев (got %d)" % len(a["uncovered_idx"]))

    print("== 5/6. JA длиннее RU / допустимая компрессия — omission НЕТ ==")
    merged_ru = ("— Пойдём!\n— Жди!\nОн открыл дверь, а она крикнула, и эхо "
                 "разнеслось по коридору.\n— Ладно.")
    check(_finding(FULL_JA, merged_ru)[0] is None,
          "слияние абзацев (3 JA-нарратива → 1 RU) при полном покрытии "
          "реплик → тихо")
    check(len(COMPRESS_JA) > len(COMPRESS_RU),
          "предпосылка: JA действительно длиннее RU (%d > %d)"
          % (len(COMPRESS_JA), len(COMPRESS_RU)))
    check(_finding(COMPRESS_JA, COMPRESS_RU)[0] is None,
          "русская компрессия (все реплики покрыты) → тихо")

    print("== 7. regression: v3-ch04 / блок 15 ==")
    cur, edited = precheck_chapter("v3-ch04.md", only={15})
    check(cur == [],
          "текущий (исправленный) блок 15 → 0 candidates (got %d)" % len(cur))
    check(edited == 1, "проверен 1 отредактированный блок (got %d)" % edited)
    f8, a8, _ = _finding(_real_ja(15), PRE_FIX_BLOCK15_RU, block=15)
    check(f8 is not None, "ДОфиксовое состояние → candidate найден")
    if f8:
        check(f8["block"] == 15, "block=15")
        check(f8["issue_type"] == "MISSING_TRANSLATION", "issue_type")
        check(f8["severity"] == "CANDIDATE",
              "pre-check не ставит ERROR (got %s)" % f8["severity"])

    print("== 8. формат pre-check evidence корректен ==")
    f8, _, _ = _finding(_real_ja(15), PRE_FIX_BLOCK15_RU, block=15)
    ev = render_evidence("v3-ch04.md", [f8] if f8 else [])
    check(ev.get("check_type") == "omission-precheck", "check_type")
    check(ev.get("chapter") == "v3-ch04.md", "chapter")
    check(isinstance(ev.get("findings"), list), "findings — список")
    errs = validate_finding(f8) if f8 else ["no finding"]
    check(not errs, "finding проходит semantic_findings.validate_finding%s"
          % ("" if not errs else " :: %s" % errs))
    check(all(x.get("severity") == "CANDIDATE" for x in ev["findings"]),
          "все findings — CANDIDATE (не вердикт)")

    print("== 9. Analyzer работает в разных режимах ==")
    check(not validate_analysis_result(
        {"status": "DISPUTED", "action": "REPORT_ONLY"}),
        "result без omission-полей (обычный candidate)")
    om = {"status": "CONFIRMED_ERROR", "action": "FIXED",
          "before": "A", "after": "B"}
    if f8:
        om.update({k: f8[k] for k in
                   ("issue_type", "omission_scope", "omission_kind",
                    "ja_span", "ru_before", "ru_after", "missing_content",
                    "not_compression_reason")})
    check(not validate_analysis_result(om),
          "result с omission-полями из pre-check")
    base = {"status": "OPTIONAL", "action": "REPORT_ONLY"}
    check(not validate_analysis_result(dict(base, inputs={"c_runs": []})),
          "режим A+B (c_runs пуст) валиден")
    check(not validate_analysis_result(
        dict(base, inputs={"c_runs": ["20261002-054143-0ee8"]})),
        "режим A+B+C валиден")

    if failed:
        print("\n[selftest] ПРОВАЛЕНО: %d из %d" % (len(failed), total[0]))
        return 1
    print("\n[selftest] OK: все %d контрольных кейсов пройдены" % total[0])
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _parse_blocks(spec):
    """'15' | '15-17' | '3,5' → set[int] (None — все блоки)."""
    if not spec:
        return None
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            out.update(range(int(lo), int(hi) + 1))
        else:
            out.add(int(part))
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Common Omission Pre-check: детерминированный слой поиска "
                    "непокрытых JA-фрагментов (до аудитов A/B/C)")
    ap.add_argument("--file", default=None, metavar="vXX-chYY.md",
                    help="глава (merged-файл)")
    ap.add_argument("--block", default=None, metavar="SPEC",
                    help="только блоки: 15 | 15-17 | 3,5")
    ap.add_argument("--report", action="store_true",
                    help="записать MD в output/_audit/sma/<ch>/precheck/")
    ap.add_argument("--json", action="store_true",
                    help="записать JSON-evidence туда же")
    ap.add_argument("--selftest", action="store_true",
                    help="прогнать контрольные кейсы")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()
    if not args.file:
        ap.error("укажи --file vXX-chYY.md либо --selftest")

    chapter = Path(args.file).name
    findings, edited = precheck_chapter(chapter, only=_parse_blocks(args.block))
    print("Omission pre-check: %s | отредактированных блоков %d | "
          "candidates %d" % (chapter, edited, len(findings)))
    for f in findings:
        print("  блок %s [%s] %s/%s conf=%s" % (
            f["block"], f["precheck_signal"], f["omission_scope"],
            f["omission_kind"], f["confidence"]))

    stem = Path(chapter).stem
    out_dir = BASE / "output" / "_audit" / "sma" / stem / "precheck"
    if args.report or args.json:
        out_dir.mkdir(parents=True, exist_ok=True)
    if args.report:
        p = out_dir / "omission-precheck.md"
        p.write_text(render_report(chapter, findings, edited),
                     encoding="utf-8", newline="\n")
        print("  report → %s" % p)
    if args.json:
        p = out_dir / "omission-precheck.json"
        p.write_text(json.dumps(render_evidence(chapter, findings),
                                ensure_ascii=False, indent=2),
                     encoding="utf-8", newline="\n")
        print("  evidence → %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())







