#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semantic_findings.py — схема и проверка смысловых findings Semantic Audit
(A / B / C + Analyzer) с явным сквозным классом пропуска перевода.

Назначение
----------
Единый детерминированный источник правды (код, не промпт) для полей смысловых
находок и для нового сквозного класса:

    issue_type: MISSING_TRANSLATION

Первичное обнаружение пропусков выполняет отдельный общий слой —
`scripts/omission_precheck.py` (Common Omission Pre-check), запускаемый ДО
аудиторских сессий A/B/C. Этот файл задаёт схему, по которой оформляются его
candidates и findings аудиторов, и проверяет их валидность.

MISSING_TRANSLATION — это НЕ «передано иначе». Это случай, когда в текущем
русском переводе ОТСУТСТВУЕТ содержательный фрагмент японского оригинала,
который был переведён, но исчез (полностью или частично). Такой случай должен
быть явно распознаваемым классом finding, а не частным semantic mismatch.
Типичный пример-регрессия: v3-ch04, блок 15 (см. fixtures/).

Отличие от прочих классов
-------------------------
    MISTRANSLATION / NUANCE_SHIFT / LEXICAL_MISMATCH / PRAGMATIC_SHIFT
        — содержание ЕСТЬ, но передано иначе (слово, оттенок, речевой акт);
    MISSING_TRANSLATION
        — содержания НЕТ (фрагмент JA не покрыт русским текстом).

Явное различие масштаба пропуска — поле omission_scope
------------------------------------------------------
    PHRASE < SENTENCE < DIALOGUE_FRAGMENT < MULTI_SENTENCE
        < BLOCK_PART < FULL_BLOCK < MULTI_BLOCK

Защита от ложного срабатывания (JA длиннее RU ≠ пропуск)
--------------------------------------------------------
Само по себе «JA длиннее RU» НЕ является пропуском: русский текст законно
сжимает японскую формулировку. Поэтому finding типа MISSING_TRANSLATION
обязан назвать, ЧТО именно исчезло (missing_content) и почему это потеря
содержания, а не компрессия (not_compression_reason). Finding с пустым
missing_content отклоняется валидатором — длина сама по себе доказательством
не считается.

Использование:
    python scripts/semantic_findings.py --selftest
    python scripts/semantic_findings.py --validate <file.json>
    python scripts/semantic_findings.py --render <file.json>
    python scripts/semantic_findings.py --apply-fixed <analysis.json> <output.md>
    python scripts/semantic_findings.py --apply-fixed <analysis.json> <output.md> --dry-run

Execution Bridge (--apply-fixed) применяет к output-файлу ТОЛЬКО findings с
action=FIXED; REPORT_ONLY и PRESERVED никогда не применяются автоматически.
Semantic taxonomy (FIXED / REPORT_ONLY / PRESERVED) мост не меняет: после
исполнения записывается ОТДЕЛЬНЫЙ execution-статус (SUCCESS / FAILED /
SKIPPED) в execution-audit.

Обнаружение ≠ вердикт: скрипт лишь проверяет структуру finding и рисует
человекочитаемый отчёт. Решение (CONFIRMED_ERROR / DISPUTED) принимает
Analyzer по сверке JA → RU.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "semantic_findings"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import completed  # noqa: E402  — реестр завершённых томов (канон completed.md)

OUTPUT = BASE / "output"
SCRIPTS = Path(__file__).resolve().parent
FIX_BLOCK = SCRIPTS / "fix_block.py"
BLOCK_MARK_RE = re.compile(r"<!--\s*block:\s*(\d+)\s*-->")

# --- канонические словари полей -------------------------------------------

ISSUE_TYPES = (
    "MISTRANSLATION",     # содержание передано неверно
    "NUANCE_SHIFT",       # оттенок/эмоция/интонация смещены
    "LEXICAL_MISMATCH",   # лексическое несоответствие
    "PRAGMATIC_SHIFT",    # изменён речевой акт / сила реплики / подтекст
    "STYLE_ISSUE",        # стилистика, не смысл
    "MISSING_TRANSLATION",  # СКВОЗНОЙ КЛАСС: фрагмент JA отсутствует в RU
    "ADDED_CONTENT",      # в RU добавлено то, чего нет в JA
    "AMBIGUITY",          # неоднозначность принадлежит JA (не ошибка перевода)
    "OTHER",
)

OMISSION_SCOPES = (
    "PHRASE",             # слово/фраза внутри предложения
    "SENTENCE",           # одно предложение
    "DIALOGUE_FRAGMENT",  # выпавшая реплика / реплики диалога
    "MULTI_SENTENCE",     # несколько соседних предложений нарратива
    "BLOCK_PART",         # связная часть блока (не реплика целиком)
    "FULL_BLOCK",         # весь смысловой блок
    "MULTI_BLOCK",        # несколько блоков
)

OMISSION_KINDS = ("FULL", "PARTIAL")   # совсем нет ↔ RU обрывается раньше конца JA
SEVERITIES = ("ERROR", "WARNING", "CANDIDATE")
CONFIDENCES = ("HIGH", "MEDIUM", "LOW")

ANALYZER_STATUSES = ("CONFIRMED_ERROR", "DISPUTED", "FALSE_POSITIVE", "OPTIONAL")
ANALYZER_ACTIONS = ("FIXED", "REPORT_ONLY", "PRESERVED")

# обязательные непустые поля finding-а типа MISSING_TRANSLATION
OMISSION_REQUIRED_NONEMPTY = (
    "ja_span",               # точный JA-фрагмент пропуска
    "missing_content",       # что именно отсутствует (защита от «JA длиннее»)
    "ru_before",             # RU-текст непосредственно до пропуска
    "not_compression_reason",  # почему это потеря содержания, а не компрессия
)


def _nonempty(value):
    """Непустая (после strip) строка."""
    return isinstance(value, str) and value.strip() != ""


def validate_finding(finding, *, allow_legacy=True):
    """Проверить структуру одного смыслового finding → список ошибок.

    Пустой список = корректно. `issue_type` НЕобязателен (обратная
    совместимость со старыми A/B/C-записями, где его не было). Но если
    finding объявлен как MISSING_TRANSLATION — обязателен полный набор
    omission-полей (см. OMISSION_REQUIRED_NONEMPTY + omission_scope/kind).
    """
    if not isinstance(finding, dict):
        return ["finding должен быть объектом JSON"]

    errors = []
    issue_type = finding.get("issue_type")
    scope = finding.get("omission_scope")

    if issue_type is not None and issue_type not in ISSUE_TYPES:
        errors.append("issue_type: недопустимое значение %r" % (issue_type,))
    if scope is not None and scope not in OMISSION_SCOPES:
        errors.append("omission_scope: недопустимое значение %r" % (scope,))
    severity = finding.get("severity")
    if severity is not None and severity not in SEVERITIES:
        errors.append("severity: недопустимое значение %r" % (severity,))
    confidence = finding.get("confidence")
    if confidence is not None and confidence not in CONFIDENCES:
        errors.append("confidence: недопустимое значение %r" % (confidence,))

    if issue_type == "MISSING_TRANSLATION":
        if scope not in OMISSION_SCOPES:
            errors.append(
                "MISSING_TRANSLATION: omission_scope обязателен и должен быть "
                "одним из %s" % (", ".join(OMISSION_SCOPES),))
        kind = finding.get("omission_kind")
        if kind not in OMISSION_KINDS:
            errors.append(
                "MISSING_TRANSLATION: omission_kind обязателен (FULL|PARTIAL)")
        for field in OMISSION_REQUIRED_NONEMPTY:
            if not _nonempty(finding.get(field)):
                if field == "missing_content":
                    errors.append(
                        "MISSING_TRANSLATION: missing_content обязателен — "
                        "сама длина JA>RU пропуском не является (защита от "
                        "ложного срабатывания на естественной компрессии)")
                elif field == "not_compression_reason":
                    errors.append(
                        "MISSING_TRANSLATION: not_compression_reason обязателен — "
                        "почему это потеря содержания, а не компрессия/адаптация")
                else:
                    errors.append("MISSING_TRANSLATION: %s обязателен" % field)
    elif scope is not None or finding.get("omission_kind") is not None:
        errors.append(
            "omission_scope/omission_kind допустимы только для "
            "issue_type=MISSING_TRANSLATION")

    if not allow_legacy and issue_type is None:
        errors.append("issue_type обязателен (allow_legacy=False)")

    return errors


def validate_analysis_result(result):
    """Проверить один result из analysis/<id>.json → список ошибок.

    Кодифицирует правила Analyzer: status/action из канонических наборов,
    FIXED — только для CONFIRMED_ERROR и только с before/after.
    """
    if not isinstance(result, dict):
        return ["result должен быть объектом JSON"]

    errors = []
    status = result.get("status")
    action = result.get("action")
    if status not in ANALYZER_STATUSES:
        errors.append("status: недопустимое значение %r" % (status,))
    if action not in ANALYZER_ACTIONS:
        errors.append("action: недопустимое значение %r" % (action,))
    if action == "FIXED" and status != "CONFIRMED_ERROR":
        errors.append("action=FIXED допустим только при status=CONFIRMED_ERROR")
    if action == "FIXED":
        for field in ("before", "after"):
            if not _nonempty(result.get(field)):
                errors.append("action=FIXED требует непустое поле %s" % field)
    errors += validate_finding(result)   # omission-поля, если есть
    return errors


def classify_omission_scope(*, missing_units, unit_kind, blocks_spanned=1,
                            full_block=False, block_part=False):
    """Детерминированно вывести omission_scope из структурного описания.

    Параметры:
      missing_units — число содержательных единиц JA без соответствия в RU;
      unit_kind     — "phrase" | "sentence" | "dialogue" (доминирующая единица);
      blocks_spanned — сколько блоков задевает пропуск (>=1);
      full_block    — пропущен весь блок;
      block_part    — пропущена связная НЕдиалоговая часть блока.

    Приоритет: MULTI_BLOCK > FULL_BLOCK > BLOCK_PART > диалог/предложения.
    """
    if blocks_spanned > 1:
        return "MULTI_BLOCK"
    if full_block:
        return "FULL_BLOCK"
    if block_part:
        return "BLOCK_PART"
    if unit_kind == "dialogue":
        return "DIALOGUE_FRAGMENT"
    if unit_kind == "sentence":
        return "SENTENCE" if missing_units <= 1 else "MULTI_SENTENCE"
    if unit_kind == "phrase":
        return "PHRASE" if missing_units <= 1 else "MULTI_SENTENCE"
    raise ValueError("unit_kind должен быть phrase|sentence|dialogue")


def find_omission_findings(findings):
    """Отобрать findings класса MISSING_TRANSLATION (сквозной фильтр A/B/C)."""
    return [f for f in findings
            if isinstance(f, dict) and f.get("issue_type") == "MISSING_TRANSLATION"]


def render_omission_report(finding, *, block=None):
    """Человекочитаемый блок отчёта для MISSING_TRANSLATION (см. скилл)."""
    bid = block if block is not None else finding.get("block")
    scope = finding.get("omission_scope", "?")
    kind = finding.get("omission_kind", "?")
    severity = finding.get("severity") or "WARNING"
    ru_after = finding.get("ru_after")
    after_txt = ru_after if _nonempty(ru_after) else "— (конец блока/файла)"
    lines = [
        "MISSING_TRANSLATION — BLOCK %s" % bid,
        "Scope: %s" % scope,
        "Kind: %s" % kind,
        "Severity: %s" % severity,
        "",
        "JA:",
        finding.get("ja_span", ""),
        "",
        "RU (before):",
        finding.get("ru_before", ""),
        "",
        "RU (after):",
        after_txt,
        "",
        "Missing:",
        finding.get("missing_content", ""),
        "",
        "Reason:",
        finding.get("not_compression_reason", ""),
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Execution Bridge: Phase 2 analysis → pre-flight → fix_block.py → verification
# ---------------------------------------------------------------------------
# Мост применяет к output-файлу ТОЛЬКО findings с action=FIXED (см.
# ANALYZER_ACTIONS). REPORT_ONLY и PRESERVED никогда не применяются
# автоматически. Semantic taxonomy не меняется: после исполнения записывается
# ОТДЕЛЬНЫЙ execution-статус (SUCCESS / FAILED / SKIPPED) в execution-audit
# output/_audit/sma/<глава>/execution/<analysis_id>.execution.json.

EXECUTION_STATES = ("SUCCESS", "FAILED", "SKIPPED")


def _find_block_bounds(content, block_no):
    """(start, end) текста блока в content или None — маркер не найден.

    Границы те же, что у fix_block.py::find_segment: от маркера блока до
    следующего маркера (или конца файла).
    """
    marker = "<!-- block: %d -->" % block_no
    idx = content.find(marker)
    if idx == -1:
        return None
    start = idx + len(marker)
    m = BLOCK_MARK_RE.search(content[start:])
    end = start + m.start() if m else len(content)
    return start, end


def _tail(text, limit=200):
    """Хвост вывода инструмента для reason в audit."""
    text = (text or "").strip()
    return text[-limit:] if text else "(нет вывода)"


def _run_fix_block(out_name, block_no, before, after, *, dry_run):
    """Один последовательный запуск СУЩЕСТВУЮЩЕГО fix_block.py.

    Текст правки идёт через временный UTF-8 --replace-file (не через argv);
    count=1 дублирует pre-flight «ровно одно вхождение» на стороне редактора.
    --dry-run fix_block используется как предварительная проверка плана.
    """
    with tempfile.TemporaryDirectory(prefix="exec_bridge_") as td:
        rep = Path(td) / "replace.json"
        rep.write_text(
            json.dumps([{"old": before, "new": after, "count": 1}],
                       ensure_ascii=False),
            encoding="utf-8")
        cmd = [sys.executable, str(FIX_BLOCK), "--file", out_name,
               "--block", str(block_no), "--replace-file", str(rep)]
        if dry_run:
            cmd.append("--dry-run")
        proc = subprocess.run(cmd, capture_output=True, cwd=str(BASE))
    out = (proc.stdout + proc.stderr).decode("utf-8", "replace")
    return proc.returncode == 0, out


def _run_tool(argv_tail):
    """Запуск существующего инструмента пайплайна; (returncode, output)."""
    proc = subprocess.run([sys.executable] + list(argv_tail),
                          capture_output=True, cwd=str(BASE))
    out = (proc.stdout + proc.stderr).decode("utf-8", "replace")
    return proc.returncode, out


def _verify_chapter(out_name):
    """update_merged → check_alignment → drift_scan (не блокирующие).

    grammar_scan/style_scan намеренно НЕ запускаются (не blocking по схеме
    Execution Bridge). Падение проверки НЕ откатывает удачные правки:
    execution=SUCCESS и verification=FAIL разделяются.
    """
    ver = {}
    rc, out = _run_tool([str(SCRIPTS / "update_merged.py"), "--file", out_name])
    ver["update_merged"] = "PASS" if rc == 0 else "FAIL"

    rc, out = _run_tool([str(SCRIPTS / "check_alignment.py"), "--file", out_name])
    ver["alignment"] = "PASS" if rc == 0 else "FAIL"
    m = re.search(r"Сигналов:\s*строгих\s+(\d+)", out)
    if m:
        ver["alignment_strong"] = int(m.group(1))

    rc, out = _run_tool([str(SCRIPTS / "drift_scan.py"), "--file", out_name])
    if rc != 0:
        ver["drift"] = "FAIL"
    elif "сравнивать не с чем" in out:
        ver["drift"] = "NO_BASELINE"
    else:
        m = re.search(r"Кандидатов: \*\*(\d+)\*\* \(([^)]*)\)", out)
        n = int(m.group(1)) if m else 0
        kinds = m.group(2) if m else ""
        ver["drift_candidates"] = n
        if n == 0:
            ver["drift"] = "CLEAN"
        elif "STRONG" in kinds:
            ver["drift"] = "STRONG"
        elif "WEAK" in kinds:
            ver["drift"] = "WEAK"
        elif "INFO" in kinds:
            ver["drift"] = "INFO"
        else:
            ver["drift"] = "UNKNOWN"
    return ver


def _norm_chapter(value):
    """'v3-ch07.md' / 'v3-ch07' → 'v3-ch07'; None/пусто → None."""
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip()
    return value[:-3] if value.endswith(".md") else value


def apply_fixed_findings(analysis_json_path, output_md_path, *,
                         verify=True, dry_run=False, write_audit=True,
                         verbose=True):
    """Execution Bridge: применить findings Phase 2 с action=FIXED.

    1. Читает analysis JSON (Phase 2) и обрабатывает ТОЛЬКО action=FIXED;
       REPORT_ONLY/PRESERVED получают execution=SKIPPED и никогда не
       применяются автоматически.
    2. Детерминированный pre-flight по каждому FIXED (без LLM): глава
       совпадает с файлом; блок существует; before непустой и встречается в
       блоке ровно один раз; after непустой и ещё НЕ присутствует в блоке;
       канон completed.md (замороженный том) → SKIPPED.
    3. Последовательное применение через СУЩЕСТВУЮЩИЙ fix_block.py
       (--replace-file; его --dry-run как предварительная проверка). После
       SUCCESS конфликтующая правка того же блока → SKIPPED.
    4. Если применилась хотя бы одна правка: update_merged → check_alignment
       → drift_scan (проверки не блокируют execution и не делают rollback).
    5. Пишет execution-audit (отдельный слой от semantic status).

    Возвращает (audit-dict, exit-code): 1 — есть хотя бы один FAILED,
    иначе 0.
    """
    analysis = json.loads(Path(analysis_json_path).read_text(encoding="utf-8"))
    results = analysis.get("results")
    if not isinstance(results, list):
        raise ValueError("analysis JSON: нет списка results")

    # путь к output-файлу: абсолютный | output/<имя> | <имя>
    cand = Path(output_md_path)
    out_path = next((p for p in (cand, OUTPUT / cand.name, BASE / cand)
                     if p.exists()), OUTPUT / cand.name)
    if out_path.resolve().parent != OUTPUT:
        raise ValueError("fix_block.py работает только с файлами внутри "
                         "output/: %s" % out_path)
    out_name = out_path.name
    stem = out_path.stem
    analysis_id = str(analysis.get("analysis_id")
                      or Path(analysis_json_path).stem)
    chapter_cur = _norm_chapter(stem)
    chapter_claim = _norm_chapter(analysis.get("chapter"))

    # канон: завершённые (замороженные) тома не правятся — см. completed.md
    vol = completed.volume_of(out_name)
    canon_reason = None
    if completed.is_frozen(vol):
        canon_reason = ("канон: том %s завершён (completed.md) — правка "
                        "запрещена" % vol)

    records = []
    fixed_seen = 0
    success_blocks = set()
    sim_content = None  # dry_run: правок на диске нет, состояние симулируется

    for i, res in enumerate(results):
        if not isinstance(res, dict):
            records.append({"finding_id": "result-%d" % (i + 1),
                            "execution": "FAILED",
                            "reason": "result не объект JSON"})
            continue

        action = res.get("action")
        fid = (res.get("candidate_id") or res.get("finding_id")
               or ("result-%d" % (i + 1)))
        rec = {"finding_id": fid, "block": res.get("block")}
        prov = {"action": action, "status": res.get("status")}
        for key in ("sources", "routed_observation", "owner_hint"):
            if res.get(key) is not None:
                prov[key] = res[key]
        rec["provenance"] = prov

        if action != "FIXED":
            # REPORT_ONLY / PRESERVED: автоматически не применяются
            rec["execution"] = "SKIPPED"
            rec["reason"] = ("action=%s — автоматически не применяется"
                             % action)
            records.append(rec)
            continue

        fixed_seen += 1
        before = res.get("before")
        after = res.get("after")
        block = res.get("block")
        rec["before"] = before if isinstance(before, str) else None
        rec["after"] = after if isinstance(after, str) else None

        def mark(execution, reason):
            rec["execution"] = execution
            if reason:
                rec["reason"] = reason

        # --- pre-flight (детерминированный, без LLM) ---
        claim = _norm_chapter(res.get("chapter")) or chapter_claim
        if canon_reason:
            mark("SKIPPED", canon_reason)
        elif claim and claim != chapter_cur:
            mark("FAILED", "finding относится к главе %s, а файл — %s"
                 % (claim, chapter_cur))
        elif not isinstance(block, int):
            mark("FAILED", "нет номера блока")
        elif not isinstance(after, str) or not after.strip():
            mark("FAILED", "after пустой")
        elif not isinstance(before, str) or not before.strip():
            mark("FAILED", "before пустой")
        else:
            try:
                if dry_run:
                    if sim_content is None:
                        sim_content = out_path.read_text(encoding="utf-8")
                    content = sim_content
                else:
                    content = out_path.read_text(encoding="utf-8")
            except OSError as exc:
                mark("FAILED", "файл не читается: %s" % exc)
            else:
                bounds = _find_block_bounds(content, block)
                if bounds is None:
                    mark("FAILED", "маркер блока %d не найден" % block)
                else:
                    start, end = bounds
                    seg = content[start:end]
                    if after in seg:
                        mark("FAILED",
                             "after уже присутствует в блоке %d (правка уже "
                             "применена) — текст не изменён" % block)
                    elif seg.count(before) == 0:
                        if block in success_blocks:
                            mark("SKIPPED",
                                 "конфликт: before изменён предыдущей правкой "
                                 "блока %d" % block)
                        else:
                            mark("FAILED",
                                 "before не найден в блоке %d (текст изменился "
                                 "с момента Phase 2)" % block)
                    elif seg.count(before) > 1:
                        mark("FAILED",
                             "before встречается в блоке %d %d раз (нужно "
                             "ровно 1)" % (block, seg.count(before)))
                    else:
                        ok, tool_out = _run_fix_block(out_name, block,
                                                      before, after,
                                                      dry_run=True)
                        if not ok:
                            mark("FAILED", "fix_block --dry-run отказал: %s"
                                 % _tail(tool_out))
                        elif dry_run:
                            mark("SUCCESS", None)
                            rec["dry_run"] = True
                            success_blocks.add(block)
                            sim_content = (content[:start]
                                           + seg.replace(before, after, 1)
                                           + content[end:])
                        else:
                            ok, tool_out = _run_fix_block(out_name, block,
                                                          before, after,
                                                          dry_run=False)
                            if ok:
                                mark("SUCCESS", None)
                                success_blocks.add(block)
                            else:
                                mark("FAILED", "fix_block отказал: %s"
                                     % _tail(tool_out))
        records.append(rec)

    counts = {state: sum(1 for r in records if r.get("execution") == state)
              for state in EXECUTION_STATES}

    if verbose:
        print("Execution Bridge: %s → %s" % (analysis_id, out_name))
        for rec in records:
            reason = rec.get("reason") or (
                "применено" if rec.get("execution") == "SUCCESS" else "")
            print("  [%s] %s (блок %s) %s"
                  % (rec.get("execution"), rec["finding_id"],
                     rec.get("block"), reason))
        print("Итог: SUCCESS %d | FAILED %d | SKIPPED %d "
              "(action=FIXED в analysis: %d)"
              % (counts["SUCCESS"], counts["FAILED"], counts["SKIPPED"],
                 fixed_seen))

    # --- verification: после применения всех успешных правок ---
    verification = None
    if verify and not dry_run and counts["SUCCESS"]:
        verification = _verify_chapter(out_name)
        if verbose:
            print("Verification: update_merged=%s | alignment=%s (строгих %s) "
                  "| drift=%s"
                  % (verification["update_merged"], verification["alignment"],
                     verification.get("alignment_strong", "?"),
                     verification["drift"]))
        vfind = {"alignment": verification["alignment"],
                 "drift": verification["drift"]}
        for rec in records:
            if rec.get("execution") == "SUCCESS":
                rec["verification"] = dict(vfind)

    audit = {
        "analysis_id": analysis_id,
        "analysis": str(analysis_json_path),
        "chapter": chapter_claim or chapter_cur,
        "output": out_name,
        "dry_run": bool(dry_run),
        "semantic_actions": list(ANALYZER_ACTIONS),
        "execution_states": list(EXECUTION_STATES),
        "counts": dict(counts, fixed=fixed_seen),
        "verification": verification,
        "results": records,
    }
    if write_audit and not dry_run:
        dst_dir = OUTPUT / "_audit" / "sma" / stem / "execution"
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / ("%s.execution.json" % analysis_id)
        dst.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
        audit["audit_path"] = str(dst)
        if verbose:
            print("Audit: %s" % dst)

    return audit, (1 if counts["FAILED"] else 0)


# ---------------------------------------------------------------------------
# Selftest: regression-кейсы класса MISSING_TRANSLATION + границы
# ---------------------------------------------------------------------------

SCOPE_CASES = [
    # v3-ch04 / block 15: несколько выпавших реплик диалога внутри блока
    (dict(missing_units=6, unit_kind="dialogue"), "DIALOGUE_FRAGMENT"),
    (dict(missing_units=1, unit_kind="phrase"), "PHRASE"),
    (dict(missing_units=1, unit_kind="sentence"), "SENTENCE"),
    (dict(missing_units=3, unit_kind="sentence"), "MULTI_SENTENCE"),
    (dict(missing_units=2, unit_kind="sentence", block_part=True), "BLOCK_PART"),
    (dict(missing_units=4, unit_kind="dialogue", full_block=True), "FULL_BLOCK"),
    (dict(missing_units=4, unit_kind="sentence", blocks_spanned=2), "MULTI_BLOCK"),
]

VALID_CASES = [
    # обычный finding без issue_type — обратная совместимость A/B/C
    ("legacy-no-issue-type",
     {"block": 4, "source": "独占欲が強い…", "current": "Ревность…",
      "problem": "Лексический оттенок", "reason": "…", "severity": "WARNING"}),
    # обычный finding с issue_type, но без omission-полей
    ("ordinary-issue-type",
     {"block": 4, "issue_type": "NUANCE_SHIFT", "severity": "CANDIDATE"}),
]

INVALID_CASES = [
    ("unknown-issue-type",
     {"issue_type": "TYPO", "source": "x"}, "issue_type"),
    ("omission-scope-without-type",
     {"issue_type": "NUANCE_SHIFT", "omission_scope": "PHRASE"},
     "omission_scope"),
    # защита от ложного срабатывания: заявлен пропуск, но НЕ сказано, что исчезло
    ("omission-missing-content",
     {"issue_type": "MISSING_TRANSLATION", "omission_scope": "PHRASE",
      "omission_kind": "FULL", "ja_span": "x", "missing_content": "   ",
      "ru_before": "y", "not_compression_reason": "z"}, "missing_content"),
    ("omission-no-kind",
     {"issue_type": "MISSING_TRANSLATION", "omission_scope": "SENTENCE",
      "ja_span": "x", "missing_content": "y", "ru_before": "z",
      "not_compression_reason": "w"}, "omission_kind"),
]

ANALYZER_CASES = [
    ("fixed-ok",
     {"status": "CONFIRMED_ERROR", "action": "FIXED",
      "before": "A", "after": "B"}, True),
    ("fixed-without-before",
     {"status": "CONFIRMED_ERROR", "action": "FIXED", "after": "B"}, False),
    ("fixed-non-error",
     {"status": "OPTIONAL", "action": "FIXED",
      "before": "A", "after": "B"}, False),
    ("report-only-ok",
     {"status": "DISPUTED", "action": "REPORT_ONLY"}, True),
]


def bridge_selftest(check):
    """Контрольные кейсы Execution Bridge (реальные запуски fix_block.py).

    Файл-мишень создаётся в output/ и удаляется после кейсов; audit в selftest
    не пишется (write_audit=False), merged не обновляется (verify=False).
    """
    import shutil
    out_name = "_selftest_bridge.md"
    out_path = OUTPUT / out_name
    base_content = (
        "<!-- block: 1 -->\n\nТекст для правки в первом блоке.\n\n"
        "<!-- block: 2 -->\n\nВторой блок: повтор и снова повтор.\n")
    tmpd = Path(tempfile.mkdtemp(prefix="semantic_findings_bridge_"))
    seq = [0]

    def run_case(results, chapter="_selftest_bridge"):
        seq[0] += 1
        out_path.write_text(base_content, encoding="utf-8")
        analysis = {"analysis_id": "selftest-bridge", "chapter": chapter,
                    "results": results}
        aj = tmpd / ("analysis-%d.json" % seq[0])
        aj.write_text(json.dumps(analysis, ensure_ascii=False),
                      encoding="utf-8")
        audit, rc = apply_fixed_findings(aj, out_path, verify=False,
                                         write_audit=False, verbose=False)
        return audit, rc, out_path.read_text(encoding="utf-8")

    def fixed(**kw):
        r = {"block": 1, "status": "CONFIRMED_ERROR", "action": "FIXED",
             "before": "Текст для правки", "after": "Текст после правки"}
        r.update(kw)
        return r

    try:
        # 1. FIXED + валидный before → SUCCESS, правка применена
        audit, rc, txt = run_case([fixed(candidate_id="F-1")])
        rec = audit["results"][0]
        check(rec["execution"] == "SUCCESS" and rc == 0,
              "bridge: FIXED + валидный before -> SUCCESS")
        check("Текст после правки" in txt and "Текст для правки" not in txt,
              "bridge: файл изменён (before -> after)")
        check(rec.get("before") == "Текст для правки"
              and rec.get("after") == "Текст после правки",
              "bridge: audit-запись содержит before/after")

        # 2. FIXED + before отсутствует → FAILED, без правки
        audit, rc, txt = run_case([fixed(candidate_id="F-2",
                                         before="этого текста в файле нет")])
        check(audit["results"][0]["execution"] == "FAILED"
              and rc == 1 and txt == base_content,
              "bridge: FIXED + before missing -> FAILED (без правки)")

        # 3. FIXED + before встречается дважды → FAILED, без правки
        audit, rc, txt = run_case([fixed(candidate_id="F-3", block=2,
                                         before="повтор",
                                         after="исправление")])
        check(audit["results"][0]["execution"] == "FAILED"
              and txt == base_content,
              "bridge: FIXED + duplicate before -> FAILED (без правки)")

        # 4. REPORT_ONLY → не применяется
        audit, rc, txt = run_case([{"block": 1, "candidate_id": "R-1",
                                    "status": "DISPUTED",
                                    "action": "REPORT_ONLY",
                                    "before": "Текст для правки",
                                    "after": "Текст после правки"}])
        check(audit["results"][0]["execution"] == "SKIPPED"
              and txt == base_content,
              "bridge: REPORT_ONLY -> SKIPPED (файл не изменён)")

        # 5. PRESERVED → не применяется
        audit, rc, txt = run_case([{"block": 1, "candidate_id": "P-1",
                                    "status": "FALSE_POSITIVE",
                                    "action": "PRESERVED",
                                    "before": "Текст для правки",
                                    "after": "Текст после правки"}])
        check(audit["results"][0]["execution"] == "SKIPPED"
              and txt == base_content,
              "bridge: PRESERVED -> SKIPPED (файл не изменён)")

        # 6. два конфликтующих FIXED → первый SUCCESS, второй SKIPPED
        audit, rc, txt = run_case([
            fixed(candidate_id="X-1", after="Первая правка"),
            fixed(candidate_id="X-2", after="Вторая правка")])
        e1 = audit["results"][0]["execution"]
        e2 = audit["results"][1]["execution"]
        check(e1 == "SUCCESS" and e2 == "SKIPPED",
              "bridge: конфликт двух FIXED -> SUCCESS + SKIPPED")
        check("Первая правка" in txt and "Вторая правка" not in txt,
              "bridge: применена только первая правка")

        # 7. routed_observation + FIXED → обычный execution path
        audit, rc, txt = run_case([fixed(candidate_id="Routed-1",
                                         routed_observation=True,
                                         owner_hint="spelling")])
        rec = audit["results"][0]
        check(rec["execution"] == "SUCCESS"
              and rec["provenance"].get("routed_observation") is True
              and rec["provenance"].get("owner_hint") == "spelling",
              "bridge: routed_observation + FIXED -> обычный SUCCESS "
              "(owner_hint сохранён в provenance)")

        # 8. глава analysis не совпадает с файлом → FAILED, без правки
        audit, rc, txt = run_case([fixed(candidate_id="C-1")],
                                  chapter="v0-ch00")
        check(audit["results"][0]["execution"] == "FAILED"
              and txt == base_content,
              "bridge: chapter mismatch -> FAILED (без правки)")

        # 9. маркер блока отсутствует → FAILED, без правки
        audit, rc, txt = run_case([fixed(candidate_id="B-1", block=99)])
        check(audit["results"][0]["execution"] == "FAILED"
              and txt == base_content,
              "bridge: маркер блока отсутствует -> FAILED (без правки)")

        # 10. after уже присутствует (правка уже применена) → FAILED, без правки
        audit, rc, txt = run_case([
            fixed(candidate_id="A-1",
                  after="Текст для правки в первом блоке.")])
        check(audit["results"][0]["execution"] == "FAILED"
              and txt == base_content,
              "bridge: after уже в блоке -> FAILED (без двойного применения)")
    finally:
        try:
            out_path.unlink()
        except OSError:
            pass
        shutil.rmtree(tmpd, ignore_errors=True)


def run_selftest():
    failed = 0
    total = 0

    def check(ok, label):
        nonlocal failed, total
        total += 1
        print(("  OK   " if ok else "  FAIL ") + label)
        if not ok:
            failed += 1

    print("== classify_omission_scope ==")
    for ev, want in SCOPE_CASES:
        got = classify_omission_scope(**ev)
        check(got == want, "%s -> %s (want %s)" % (ev, got, want))

    print("== validate_finding: valid ==")
    for name, f in VALID_CASES:
        errs = validate_finding(f)
        check(not errs, "%s%s" % (name, "" if not errs else " :: %s" % errs))

    print("== validate_finding: invalid ==")
    for name, f, needle in INVALID_CASES:
        errs = validate_finding(f)
        check(bool(errs) and any(needle in e for e in errs),
              "%s (need %r)" % (name, needle))

    print("== validate_analysis_result ==")
    for name, res, want_ok in ANALYZER_CASES:
        errs = validate_analysis_result(res)
        check((not errs) == want_ok,
              "%s%s" % (name, "" if (not errs) == want_ok else " :: %s" % errs))

    print("== coverage-attestation (top-level findings) ==")
    errs = validate_coverage_attestation({"findings": []})
    check(bool(errs) and "coverage" in errs[0],
          "findings: [] без coverage -> ошибка%s"
          % ("" if errs else " (нет ошибки!)"))
    check(not validate_coverage_attestation(
        {"findings": [], "coverage": "блоки 1–29 проверены целиком"}),
        "findings: [] с coverage -> OK")
    check(not validate_coverage_attestation(
        {"findings": [VALID_CASES[0][1]]}),
        "непустой findings без coverage -> OK (обратная совместимость)")
    check(not validate_coverage_attestation(
        {"findings": [{"bad": 1}], "coverage": " "}),
        "непустой findings -> правило coverage не применяется")

    print("== execution bridge (apply_fixed_findings) ==")
    bridge_selftest(check)

    print("== fixtures (regression) ==")
    fixtures = sorted(FIXTURES.glob("*.json"))
    if not fixtures:
        check(False, "нет fixtures в %s" % FIXTURES)
    for path in fixtures:
        doc = json.loads(path.read_text(encoding="utf-8"))
        name = doc.get("case", path.name)
        finding = doc.get("finding", {})
        errs = validate_finding(finding)
        if doc.get("expect", "VALID") == "VALID":
            check(not errs, "fixture %s (VALID)%s" % (
                name, "" if not errs else " :: %s" % errs))
            for key, field in (("expect_issue_type", "issue_type"),
                               ("expect_scope", "omission_scope"),
                               ("expect_kind", "omission_kind")):
                if key in doc:
                    got = finding.get(field)
                    check(got == doc[key],
                          "fixture %s: %s=%s (want %s)" % (
                              name, field, got, doc[key]))
        else:
            needle = doc.get("expect_error", "")
            ok = bool(errs) and (not needle or any(needle in e for e in errs))
            check(ok, "fixture %s (INVALID, need %r)%s" % (
                name, needle, "" if ok else " :: %s" % errs))

    if failed:
        print("\n[selftest] ПРОВАЛЕНО: %d из %d" % (failed, total))
        return 1
    print("\n[selftest] OK: все %d контрольных кейсов пройдены" % total)
    return 0


# --- CLI -------------------------------------------------------------------

def validate_coverage_attestation(doc):
    """Coverage-attestation: top-level «findings» требует объём проверки.

    Пустой массив находок без ``coverage`` — недоказанный «чистый» прогон:
    аудитор обязан перечислить просмотренные блоки и объём проверки, иначе
    «findings: []» неотличим от непроверенной главы (дыра класса D:
    обратная связь не замыкается). Правило применяется ТОЛЬКО к top-level
    объекту с полем findings и только когда он пуст: непустой findings без
    coverage валидатор не роняет (обратная совместимость со старыми
    запусками), fixture-обёртки и analysis-результаты не затрагиваются.
    Возвращает список ошибок ([] — ок).
    """
    findings = doc.get("findings")
    if not isinstance(findings, list) or findings:
        return []
    coverage = doc.get("coverage")
    if isinstance(coverage, str) and coverage.strip():
        return []
    return ['coverage: обязателен при "findings": [] — attestation покрытия '
            "(какие блоки просмотрены и в каком объёме); без него пустой "
            "массив не доказывает чистоту главы"]


def cmd_validate(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = []
    if isinstance(doc, dict) and "finding" in doc:
        # fixture-обёртка: {"case": …, "expect": …, "finding": {…}}
        errors = ["finding: %s" % e for e in validate_finding(doc["finding"])]
    elif isinstance(doc, dict) and "findings" in doc:
        for i, f in enumerate(doc["findings"]):
            errors += ["findings[%d]: %s" % (i, e) for e in validate_finding(f)]
        errors += validate_coverage_attestation(doc)
    elif isinstance(doc, dict) and "results" in doc:
        for i, r in enumerate(doc["results"]):
            errors += ["results[%d]: %s" % (i, e)
                       for e in validate_analysis_result(r)]
    elif isinstance(doc, list):
        for i, f in enumerate(doc):
            errors += ["[%d]: %s" % (i, e) for e in validate_finding(f)]
    else:
        errors = validate_finding(doc)
    if errors:
        for e in errors:
            print("ОШИБКА: %s" % e)
        return 1
    print("OK: структура корректна")
    return 0


def cmd_render(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    finding = doc.get("finding", doc) if isinstance(doc, dict) else doc
    sys.stdout.write(render_omission_report(finding) + "\n")
    return 0


def cmd_apply_fixed(analysis_path, output_path, dry_run=False):
    """CLI Execution Bridge: --apply-fixed <analysis.json> <output.md>."""
    _audit, rc = apply_fixed_findings(analysis_path, output_path,
                                      dry_run=dry_run)
    return rc


def main():
    ap = argparse.ArgumentParser(
        description="Схема/проверка смысловых findings Semantic Audit "
                    "(issue_type, MISSING_TRANSLATION, omission_scope)")
    ap.add_argument("--selftest", action="store_true",
                    help="прогнать контрольные кейсы")
    ap.add_argument("--validate", default=None, metavar="FILE",
                    help="проверить finding/findings/analysis-результат")
    ap.add_argument("--render", default=None, metavar="FILE",
                    help="нарисовать human-readable блок для omission-finding")
    ap.add_argument("--apply-fixed", nargs=2, metavar=("ANALYSIS", "OUTPUT"),
                    help="Execution Bridge: применить findings action=FIXED "
                         "из Phase 2 analysis JSON к файлу output/ "
                         "(REPORT_ONLY/PRESERVED не применяются)")
    ap.add_argument("--dry-run", action="store_true",
                    help="только с --apply-fixed: pre-flight + fix_block "
                         "--dry-run, файл НЕ меняется")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()
    if args.validate:
        return cmd_validate(args.validate)
    if args.render:
        return cmd_render(args.render)
    if args.apply_fixed:
        return cmd_apply_fixed(args.apply_fixed[0], args.apply_fixed[1],
                               dry_run=args.dry_run)
    if args.dry_run:
        ap.error("--dry-run применим только вместе с --apply-fixed")
    ap.error("укажи --selftest | --validate <file> | --render <file> | "
             "--apply-fixed <analysis.json> <output.md>")


if __name__ == "__main__":
    sys.exit(main())




