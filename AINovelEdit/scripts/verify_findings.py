#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_findings.py — независимый Verifier для двойного смыслового аудита.

Pipeline (этап 5):

    A ─┐
       ├── merge_findings → candidates ── verify_findings → verdict.json / .md
    B ─┘

Ответственности:

* merge_findings.py (НЕ изменяется) — объединяет находки A и B в candidates;
* verify_findings.py — собирает verifier input (candidates + JA/RU/context),
  строит промпт, запускает LLM через runtime adapter, валидирует ответ,
  пишет только вердикты;
* llm_runtime.py — способ запуска модели (сейчас Cline; семантика от него
  не зависит).

Verifier:

* не голосует между A и B, не доверяет severity, не считает ONLY_A / ONLY_B
  разными по надёжности, не читает старые audit reports и не лезет в
  filesystem проекта — весь вход инлайном;
* работает в пустом cwd `%TEMP%\\ainoveledit-sma\\<run-id>\\verifier`;
* не меняет перевод: не вызывает fix_block.py, не трогает output/*.md.

Коды выхода:
    0 — ок
    1 — ошибка входа/аргументов
    2 — MODEL_ERROR
    3 — TIMEOUT
    4 — INVALID_JSON
    5 — INVALID_RESULT (неизвестный/пропущенный candidate, плохие поля)
    6 — PROCESS_ERROR
    7 — частичный результат (часть блоков не верифицирована)

Использование:
    python scripts/verify_findings.py --file v5-ch02.md --blocks 6
    python scripts/verify_findings.py --case test.json --output out.json
    python scripts/verify_findings.py --file v5-ch02.md --dry-run
    python scripts/verify_findings.py --self-test
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
AINOVELEDIT = SCRIPTS_DIR.parent
TOOLS_DIR = AINOVELEDIT.parent / "tools"
for _p in (str(SCRIPTS_DIR), str(TOOLS_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import merged_io                                     # noqa: E402
import llm_runtime as rt                             # noqa: E402
from run_semantic_audit import parse_chapter_arg     # noqa: E402
from run_semantic_audit import parse_blocks          # noqa: E402

OUT_DIR = AINOVELEDIT / "output" / "_audit"
SKILL_PATH = AINOVELEDIT / ".agents" / "skills" / "verifier" / "SKILL.md"
RUN_ROOT = Path(tempfile.gettempdir()) / "ainoveledit-sma"

DEFAULT_MODEL = "cline-free/deepseek-v4.1-flash"
DEFAULT_PROVIDER = "cline"
PROMPT_CHAR_LIMIT = 30000

VERDICTS = ("ERROR", "QUESTIONABLE", "ACCEPT")
CONFIDENCES = ("HIGH", "MEDIUM", "LOW")
REQUIRED_RESULT_FIELDS = ("block", "candidate_id", "source", "current",
                          "verdict", "reason", "confidence")

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_MODEL = 2
EXIT_TIMEOUT = 3
EXIT_INVALID_JSON = 4
EXIT_INVALID_RESULT = 5
EXIT_PROCESS = 6
EXIT_PARTIAL = 7

RT_ERROR_EXIT = {
    rt.MODEL_ERROR: EXIT_MODEL,
    rt.TIMEOUT: EXIT_TIMEOUT,
    rt.PROCESS_ERROR: EXIT_PROCESS,
}

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# ВХОД: candidates из merged + текст блоков
# ---------------------------------------------------------------------------
def load_skill() -> str:
    if not SKILL_PATH.exists():
        raise FileNotFoundError(f"нет скилла верификатора: {SKILL_PATH}")
    return SKILL_PATH.read_text(encoding="utf-8").strip()


def load_merged(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"нет merged-файла: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: ожидался JSON-объект")
    return data


def candidates_from_merged(merged: dict, block: int) -> list[dict]:
    """→ список candidates с стабильными id.

    Происхождение сохраняется:
        ONLY_A     → id A-<block>-<n>, sources ["A"], status ONLY_A
        ONLY_B     → id B-<block>-<n>, sources ["B"], status ONLY_B
        BOTH_FOUND → id A-<block>-<n>, sources ["A","B"], status BOTH_FOUND
                     (основная находка берётся у A, у B — второй reason)
    """
    items = []
    for entry in merged.get("blocks", []):
        if entry.get("block") != block:
            continue
        for finding in entry.get("findings", []):
            status = finding.get("status")
            fa = finding.get("finding_a") or {}
            fb = finding.get("finding_b") or {}
            if status == "ONLY_A":
                origin, base, extra_reason = "A", fa, None
            elif status == "ONLY_B":
                origin, base, extra_reason = "B", fb, None
            elif status == "BOTH_FOUND":
                origin, base, extra_reason = "A", fa, fb.get("reason")
            else:
                raise ValueError(f"неизвестный статус finding: {status!r}")
            items.append({"_origin": origin, "_base": base,
                          "_extra_reason": extra_reason, "status": status})
    counters: dict[str, int] = {}
    out = []
    for it in items:
        origin = it["_origin"]
        counters[origin] = counters.get(origin, 0) + 1
        base = it["_base"]
        candidate_id = f"{origin}-{block}-{counters[origin]}"
        sources = ["A", "B"] if it["status"] == "BOTH_FOUND" else [origin]
        reason = base.get("reason", "")
        if it["_extra_reason"]:
            reason = f"{reason}\n[Reason B]: {it['_extra_reason']}"
        out.append({
            "candidate_id": candidate_id,
            "sources": sources,
            "status": it["status"],
            "source": base.get("source", ""),
            "current": base.get("current", ""),
            "problem": base.get("problem", ""),
            "reason": reason,
            "suggestion": base.get("suggestion") or "",
            "severity": base.get("severity", ""),
        })
    return out


def _blocks_dict(path: str) -> dict[int, str]:
    return {num: "\n\n".join(p for p in paras if p.strip())
            for num, paras in merged_io.read_source_blocks(path)}


def build_case(chapter: str, block: int, merged: dict,
               ja_path: str, ru_path: str) -> dict:
    ja = _blocks_dict(ja_path)
    ru = _blocks_dict(ru_path)
    if block not in ja or block not in ru:
        raise ValueError(f"блок {block} отсутствует в JA или RU "
                         f"(JA: {sorted(ja)}, RU: {sorted(ru)})")
    nums = sorted(set(ja) & set(ru))
    prev_b = max((n for n in nums if n < block), default=None)
    next_b = min((n for n in nums if n > block), default=None)
    return {
        "chapter": chapter,
        "block": block,
        "ja": ja[block],
        "ru": ru[block],
        "prev_ja": ja.get(prev_b, "") if prev_b else "",
        "prev_ru": ru.get(prev_b, "") if prev_b else "",
        "next_ja": ja.get(next_b, "") if next_b else "",
        "next_ru": ru.get(next_b, "") if next_b else "",
        "candidates": candidates_from_merged(merged, block),
    }


def load_case_file(path: Path) -> dict:
    case = json.loads(path.read_text(encoding="utf-8"))
    for key in ("chapter", "block", "ja", "ru", "candidates"):
        if key not in case:
            raise ValueError(f"{path}: нет поля {key!r}")
    if not isinstance(case["candidates"], list) or not case["candidates"]:
        raise ValueError(f"{path}: candidates должны быть непустым массивом")
    for i, c in enumerate(case["candidates"]):
        for key in ("candidate_id", "source", "current", "problem", "reason"):
            if not str(c.get(key, "")).strip():
                raise ValueError(f"{path}: candidates[{i}] нет поля {key!r}")
        c.setdefault("sources", ["A"] if c["candidate_id"].startswith("A") else ["B"])
        c.setdefault("status", "ONLY_A" if c["candidate_id"].startswith("A") else "ONLY_B")
        c.setdefault("suggestion", "")
    for key in ("prev_ja", "prev_ru", "next_ja", "next_ru"):
        case.setdefault(key, "")
    return case


# ---------------------------------------------------------------------------
# ПРОМПТ
# ---------------------------------------------------------------------------
def _section(title: str, text: str, empty: str = "(нет)") -> str:
    return f"{title}:\n{(text or '').strip() or empty}"


def build_prompt(case: dict, skill_text: str) -> str:
    cands = case["candidates"]
    blocks = [
        "ЗАДАЧА: независимый семантический верификатор перевода JA → RU.",
        "",
        "Ты работаешь ИЗОЛИРОВАННО: не читаешь файлы, не обращаешься к "
        "файловой системе, не ищешь старые отчёты. Весь материал — ниже, "
        "больше ничего дано не будет.",
        "",
        "СНАЧАЛА выполни ФАЗУ 1 (самостоятельная оценка JA → RU), И только "
        "потом ФАЗУ 2 (проверка candidates). Finding аудитора — гипотеза, а не "
        "доказательство ошибки. Не голосуй между аудиторами, severity "
        "аудиторов игнорируй.",
        "",
        "--- SKILL-BEGIN ---",
        skill_text,
        "--- SKILL-END ---",
        "",
        "--- MATERIAL-BEGIN ---",
        _section("CHAPTER", case["chapter"]),
        "",
        "TARGET BLOCK:",
        str(case["block"]),
        "",
        _section("JA", case["ja"]),
        "",
        _section("RU", case["ru"]),
        "",
        "PREVIOUS CONTEXT (не верифицируется, только контекст):",
        _section("JA", case["prev_ja"]),
        _section("RU", case["prev_ru"]),
        "",
        "NEXT CONTEXT (не верифицируется, только контекст):",
        _section("JA", case["next_ja"]),
        _section("RU", case["next_ru"]),
        "",
        "CANDIDATES:",
    ]
    for c in cands:
        origin = "+".join(c["sources"])
        blocks += [
            "",
            f"[{origin}]",
            f"candidate_id: {c['candidate_id']}",
            f"sources: {','.join(c['sources'])}",
            f"status: {c['status']}",
            _section("source", c["source"]),
            _section("current", c["current"]),
            _section("problem", c["problem"]),
            _section("reason", c["reason"]),
            _section("suggestion", c["suggestion"], empty="(нет)"),
        ]
    blocks += [
        "",
        "--- MATERIAL-END ---",
        "",
        "--- FORMAT-BEGIN ---",
        "Верни ТОЛЬКО валидный JSON (без markdown и пояснений):",
        json.dumps({
            "chapter": case["chapter"],
            "results": [{
                "block": case["block"],
                "candidate_id": cands[0]["candidate_id"],
                "source": cands[0]["source"],
                "current": cands[0]["current"],
                "verdict": "ERROR | QUESTIONABLE | ACCEPT",
                "reason": "…",
                "confidence": "HIGH | MEDIUM | LOW",
                "suggestion": "… (опционально)",
            }],
        }, ensure_ascii=False, indent=2),
        "",
        "Обязательные поля: block, candidate_id, source, current, verdict, "
        "reason, confidence. suggestion — опционально.",
        f"Вернি ровно {len(cands)} результат(ов): по одному на каждый "
        "candidate_id из CANDIDATES, дословно. Неизвестные id запрещены.",
        "verdict — только ERROR / QUESTIONABLE / ACCEPT; "
        "confidence — только HIGH / MEDIUM / LOW.",
        "--- FORMAT-END ---",
    ]
    return "\n".join(blocks)


# ---------------------------------------------------------------------------
# РАЗБОР И ВАЛИДАЦИЯ ОТВЕТА
# ---------------------------------------------------------------------------
def extract_json(text: str) -> tuple[dict | None, str | None]:
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data, None
        return None, "ответ не является JSON-объектом"
    except json.JSONDecodeError as first:
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "",
                         text.strip(), flags=re.M | re.S)
        try:
            data = json.loads(cleaned)
            if isinstance(data, dict):
                return data, None
        except json.JSONDecodeError:
            pass
        start, end = text.find("{"), text.rfind("}")
        if 0 <= start < end:
            try:
                data = json.loads(text[start:end + 1])
                if isinstance(data, dict):
                    return data, None
            except json.JSONDecodeError:
                pass
        return None, f"не удалось разобрать JSON: {first.msg}"


def validate_results(payload: dict | None, case: dict) -> tuple[list | None, str | None]:
    """→ (нормализованные результаты | None, ошибка | None).

    Любое отклонение → INVALID_RESULT: частичный результат не принимается.
    """
    if payload is None:
        return None, "нет разобранного JSON"
    known = {c["candidate_id"]: c for c in case["candidates"]}
    results = payload.get("results")
    if not isinstance(results, list) or not results:
        return None, "results отсутствует или не массив"
    chapter = payload.get("chapter")
    if chapter is not None and chapter != case["chapter"]:
        return None, f"chapter={chapter!r}, ожидался {case['chapter']!r}"

    seen: set[str] = set()
    normalized = []
    for i, item in enumerate(results):
        where = f"results[{i}]"
        if not isinstance(item, dict):
            return None, f"{where}: не объект"
        cid = item.get("candidate_id")
        if not isinstance(cid, str) or cid not in known:
            return None, (f"INVALID_RESULT: {where} candidate_id={cid!r} "
                          f"отсутствует во входных candidates")
        if cid in seen:
            return None, f"INVALID_RESULT: дубликат candidate_id={cid!r}"
        seen.add(cid)
        block = item.get("block")
        if isinstance(block, str) and block.strip().isdigit():
            block = int(block)
        if block != case["block"]:
            return None, f"{where}: block={block!r}, ожидался {case['block']!r}"
        verdict = str(item.get("verdict", "")).strip().upper()
        if verdict not in VERDICTS:
            return None, f"{where}: verdict={item.get('verdict')!r} вне {VERDICTS}"
        confidence = str(item.get("confidence", "")).strip().upper()
        if confidence not in CONFIDENCES:
            return None, (f"{where}: confidence={item.get('confidence')!r} "
                          f"вне {CONFIDENCES}")
        for field in ("source", "current", "reason"):
            if not isinstance(item.get(field), str) or not item.get(field, "").strip():
                return None, f"{where}: пустое обязательное поле {field!r}"
        cand = known[cid]
        suggestion = item.get("suggestion")
        if suggestion is not None and not isinstance(suggestion, str):
            return None, f"{where}: suggestion должен быть строкой или null"
        normalized.append({
            "block": case["block"],
            "candidate_id": cid,
            "sources": cand["sources"],
            "status": cand["status"],
            "source": cand["source"],
            "current": cand["current"],
            "problem": cand.get("problem", ""),
            "verdict": verdict,
            "reason": item["reason"].strip(),
            "confidence": confidence,
            "suggestion": (suggestion or "").strip() if isinstance(suggestion, str) else "",
        })
    missing = [cid for cid in known if cid not in seen]
    if missing:
        return None, (f"INVALID_RESULT: верификатор не ответил по candidates: "
                      f"{missing} (частичный результат не принимается)")
    return normalized, None


# ---------------------------------------------------------------------------
# ЗАПИСЬ
# ---------------------------------------------------------------------------
def write_outputs(out_json: Path, payload: dict, write_md: bool) -> list[Path]:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    written = [out_json]
    if write_md:
        out_md = out_json.with_suffix(".md")
        out_md.write_text(render_md(payload), encoding="utf-8")
        written.append(out_md)
    return written


def render_md(payload: dict) -> str:
    lines = [
        f"# Вердикты верификатора: {payload.get('chapter', '')}",
        "",
        f"Runtime: {payload.get('runtime', {}).get('provider', '?')} / "
        f"{payload.get('runtime', {}).get('model', '?')}",
        f"Дата: {payload.get('generated_at', '')}",
        "",
    ]
    for res in payload.get("results", []):
        sug = res.get("suggestion") or "—"
        lines += [
            f"## Блок {res['block']} — {res['candidate_id']} "
            f"({'+'.join(res.get('sources', []))}, {res.get('status', '')})",
            "",
            f"- **Verdict:** {res['verdict']} "
            f"(`confidence: {res['confidence']}`)",
            f"- **JA:** {res['source']}",
            f"- **RU:** {res['current']}",
            f"- **Problem (аудитор):** {res.get('problem', '')}",
            f"- **Reason (верификатор):** {res['reason']}",
            f"- **Suggestion:** {sug}",
            "",
        ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# ЗАПУСК ОДНОГО КЕЙСА
# ---------------------------------------------------------------------------
def run_case(case: dict, skill_text: str, adapter, data_dir: Path,
             cwd: Path, timeout: int, retries: int, kill_grace: int = 60
             ) -> tuple[dict | None, str | None, int]:
    """→ (payload | None, ошибка | None, код_выхода)."""
    prompt = build_prompt(case, skill_text)
    if len(prompt) > PROMPT_CHAR_LIMIT:
        return None, f"промпт {len(prompt)} симв. превышает лимит {PROMPT_CHAR_LIMIT}", EXIT_USAGE

    last_error, exit_code = None, EXIT_MODEL
    for attempt in range(1, retries + 2):
        outcome = adapter.run(prompt, cwd, timeout, data_dir,
                              kill_grace=kill_grace)
        if outcome.error is not None:
            last_error = f"{outcome.error}: {outcome.detail}"
            exit_code = RT_ERROR_EXIT.get(outcome.error, EXIT_PROCESS)
            print(f"  попытка {attempt}/{retries + 1}: {last_error}")
            continue
        payload, note = extract_json(outcome.text)
        if payload is None:
            last_error, exit_code = f"INVALID_JSON: {note}", EXIT_INVALID_JSON
            print(f"  попытка {attempt}/{retries + 1}: {last_error}; "
                  f"ответ: {outcome.text[:200]!r}")
            continue
        results, invalid = validate_results(payload, case)
        if invalid is not None:
            last_error, exit_code = invalid, EXIT_INVALID_RESULT
            print(f"  попытка {attempt}/{retries + 1}: {last_error}")
            continue
        return {"chapter": case["chapter"],
                "block": case["block"],
                "runtime": {"provider": adapter.provider, "model": outcome.model,
                            "adapter": adapter.name},
                "usage": outcome.usage,
                "duration": outcome.duration,
                "results": results}, None, EXIT_OK
    return None, last_error, exit_code


# ---------------------------------------------------------------------------
# SELF-TEST (детерминированные проверки, без LLM)
# ---------------------------------------------------------------------------
def _synthetic_merged() -> dict:
    def f(block, problem, source, current, reason, severity="WARNING"):
        return {"block": block, "problem": problem, "source": source,
                "current": current, "reason": reason, "severity": severity}
    return {
        "chapter": "v05-ch02",
        "blocks": [
            {"block": 75, "findings": [
                {"status": "ONLY_A", "finding_a": f(75, "Эмоциональный оттенок",
                                                    "ひきつった笑顔", "кривую улыбку",
                                                    "оттенок улыбки изменён")},
                {"status": "BOTH_FOUND",
                 "finding_a": f(75, "Субъект", "彼は", "она", "сдвиг субъекта"),
                 "finding_b": f(75, "Субъект", "彼は", "она", "B: тот же сдвиг")},
            ]},
            {"block": 76, "findings": [
                {"status": "ONLY_B",
                 "finding_b": f(76, "Объект", "本を", "книгу", "объект потерян")},
            ]},
        ],
    }


def _synthetic_case(merged: dict, block: int) -> dict:
    return {
        "chapter": merged["chapter"], "block": block,
        "ja": "ひきつった笑顔を浮かべるとルイズは一礼した。",
        "ru": "Луиза надела кривую улыбку и поклонилась.",
        "prev_ja": "前後の文脈。", "prev_ru": "Соседний контекст.",
        "next_ja": "次の文脈。", "next_ru": "Следующий контекст.",
        "candidates": candidates_from_merged(merged, block),
    }


def self_test() -> int:
    checks: list[tuple[str, bool, str]] = []

    def add(name: str, ok: bool, detail: str = ""):
        checks.append((name, bool(ok), detail))

    merged = _synthetic_merged()

    # 1. ONLY_A / BOTH / ONLY_B — идентичность и происхождение
    c75 = candidates_from_merged(merged, 75)
    ids75 = [c["candidate_id"] for c in c75]
    add("ONLY_A получает id A-75-1", ids75 == ["A-75-1", "A-75-2"], str(ids75))
    both = c75[1]
    add("BOTH_FOUND сохраняет sources=['A','B'] и status",
        both["sources"] == ["A", "B"] and both["status"] == "BOTH_FOUND",
        f"{both['candidate_id']} {both['sources']} {both['status']}")
    add("BOTH_FOUND несёт оба reason",
        "[Reason B]" in both["reason"], both["reason"][:80])
    c76 = candidates_from_merged(merged, 76)
    add("ONLY_B получает id B-76-1",
        [c["candidate_id"] for c in c76] == ["B-76-1"], str(c76))

    skill = load_skill()

    def sub_merged(block: int, *findings: dict) -> dict:
        return {"chapter": "v05-ch02",
                "blocks": [{"block": block, "findings": list(findings)}]}

    block75 = merged["blocks"][0]["findings"]
    block76 = merged["blocks"][1]["findings"]

    # 2. Формирование prompt для ONLY_A / ONLY_B / BOTH / multiple
    cases = {
        "ONLY_A": _synthetic_case(sub_merged(75, block75[0]), 75),
        "ONLY_B": _synthetic_case(sub_merged(76, block76[0]), 76),
        "BOTH_FOUND": _synthetic_case(sub_merged(75, block75[1]), 75),
        "multiple": _synthetic_case(merged, 75),
    }
    expect_ids = {
        "ONLY_A": ["A-75-1"],
        "ONLY_B": ["B-76-1"],
        "BOTH_FOUND": ["A-75-1"],
        "multiple": ["A-75-1", "A-75-2"],
    }
    for name, case in cases.items():
        prompt = build_prompt(case, skill)
        ids = [c["candidate_id"] for c in case["candidates"]]
        add(f"[{name}] prompt содержит все candidate_id",
            all(cid in prompt for cid in ids) and ids == expect_ids[name],
            f"id={ids}")
        add(f"[{name}] prompt содержит JA/RU/контекст/candidates",
            all(m in prompt for m in ("CHAPTER:", "TARGET BLOCK:", "JA:", "RU:",
                                      "PREVIOUS CONTEXT", "NEXT CONTEXT",
                                      "CANDIDATES:", "SKILL-BEGIN")),
            f"{len(prompt)} симв.")
        add(f"[{name}] в prompt нет путей проекта",
            all(p not in prompt for p in (str(AINOVELEDIT), str(OUT_DIR),
                                          str(SCRIPTS_DIR), ".git", "output/")),
            "")
        add(f"[{name}] длина prompt в лимите", len(prompt) < PROMPT_CHAR_LIMIT,
            f"{len(prompt)}")

    # 3. multiple: каждый id встречается ровно в своём блоке candidates
    prompt_m = build_prompt(cases["multiple"], skill)
    add("[multiple] 2 candidates объявлены, формат требует 2 результата",
        prompt_m.count("candidate_id:") == 2 and "ровно 2 результат" in prompt_m,
        "")

    # 4. Валидация ответа
    case_m = cases["multiple"]
    good = {"chapter": "v05-ch02", "results": [
        {"block": 75, "candidate_id": cid, "source": c["source"],
         "current": c["current"], "verdict": "ERROR", "reason": "ok",
         "confidence": "HIGH"}
        for cid, c in zip([c["candidate_id"] for c in case_m["candidates"]],
                          case_m["candidates"])]}
    res, err = validate_results(good, case_m)
    add("валидный полный ответ принят", err is None and len(res) == 2, str(err))

    bad = json.loads(json.dumps(good))
    bad["results"][0]["candidate_id"] = "Z-75-9"
    _, err = validate_results(bad, case_m)
    add("неизвестный candidate_id → INVALID_RESULT",
        err is not None and "INVALID_RESULT" in err, str(err))

    bad = json.loads(json.dumps(good))
    bad["results"].pop()
    _, err = validate_results(bad, case_m)
    add("частичный результат → INVALID_RESULT",
        err is not None and "INVALID_RESULT" in err, str(err))

    bad = json.loads(json.dumps(good))
    bad["results"][0]["verdict"] = "MAYBE"
    _, err = validate_results(bad, case_m)
    add("недопустимый verdict → INVALID_RESULT", err is not None, str(err))

    bad = json.loads(json.dumps(good))
    bad["results"][0]["confidence"] = "0.9"
    _, err = validate_results(bad, case_m)
    add("score-подобный confidence → INVALID_RESULT", err is not None, str(err))

    bad = json.loads(json.dumps(good))
    del bad["results"][1]["reason"]
    _, err = validate_results(bad, case_m)
    add("отсутствие обязательного поля → INVALID_RESULT", err is not None, str(err))

    bad = json.loads(json.dumps(good))
    bad["results"][0]["block"] = 76
    _, err = validate_results(bad, case_m)
    add("block не совпал → INVALID_RESULT", err is not None, str(err))

    # 5. Классификация ошибок runtime
    add("aborted → TIMEOUT",
        rt._classify(1, "aborted", "", True, False)[0] == rt.TIMEOUT)
    add("finishReason=error → MODEL_ERROR",
        rt._classify(1, "error", "model not found", True, False)[0] == rt.MODEL_ERROR)
    add("нет run_result → PROCESS_ERROR",
        rt._classify(0, None, "", False, False)[0] == rt.PROCESS_ERROR)
    add("пустой ответ → MODEL_ERROR",
        rt._classify(0, "completed", "   ", True, False)[0] == rt.MODEL_ERROR)
    add("локальный таймаут → TIMEOUT",
        rt._classify(None, None, "", False, True)[0] == rt.TIMEOUT)
    add("нормальный ответ → OK",
        rt._classify(0, "completed", '{"ok":1}', True, False)[0] is None)

    # 6. extract_json
    add("JSON в markdown-обёртке разбирается",
        extract_json('```json\n{"chapter":"x","results":[]}\n```')[0] is not None)
    add("мусор → ошибка", extract_json("нет JSON")[0] is None)

    print("=== SELF-TEST verifier input/валидации (без LLM) ===")
    for name, ok, detail in checks:
        print(f"  [{'OK  ' if ok else 'FAIL'}] {name}" +
              (f"\n         {detail}" if detail and not ok else ""))
    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"\nИтог: {passed}/{len(checks)}")
    return EXIT_OK if passed == len(checks) else EXIT_INVALID_RESULT


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(
        description="Независимый verifier для двойного смыслового аудита (A+B)")
    ap.add_argument("--file", help="глава: v5-ch02.md / v5-ch02")
    ap.add_argument("--volume", type=int, default=None)
    ap.add_argument("--blocks", help="номера блоков: 6 или 6,8 (по умолчанию все с candidates)")
    ap.add_argument("--merged", help="путь к merged-candidates (по умолчанию output/_audit/<ch>-sma-merged.json)")
    ap.add_argument("--ja-file", help="переопределение JA-файла (фикстуры тестов)")
    ap.add_argument("--ru-file", help="переопределение RU-файла (фикстуры тестов)")
    ap.add_argument("--case", action="append", default=[],
                    help="готовый verifier input (JSON); можно несколько")
    ap.add_argument("--output", help="путь verdict.json (обязателен для --case)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--provider", default=DEFAULT_PROVIDER)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--retries", type=int, default=1)
    ap.add_argument("--self-test", action="store_true",
                    help="детерминированные проверки входа/валидации без LLM")
    ap.add_argument("--dry-run", action="store_true",
                    help="построить промпты и проверить их, не запуская LLM")
    ap.add_argument("--keep-temp", action="store_true")
    ap.add_argument("--no-md", action="store_true", help="не писать .md")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    try:
        skill_text = load_skill()
    except (OSError, ValueError) as exc:
        print(f"ОШИБКА: {exc}")
        return EXIT_USAGE

    # --- сборка кейсов -----------------------------------------------------
    cases: list[dict] = []
    outputs: list[Path] = []
    try:
        if args.case:
            if not args.output:
                print("ОШИБКА: для --case укажите --output")
                return EXIT_USAGE
            for path in args.case:
                cases.append(load_case_file(Path(path)))
            outputs = [Path(args.output)] if len(cases) == 1 else [
                Path(args.output).with_name(
                    f"{Path(args.output).stem}-{i + 1}{Path(args.output).suffix}")
                for i in range(len(cases))]
        else:
            if not args.file:
                print("ОШИБКА: нужен --file или --case")
                return EXIT_USAGE
            ch = parse_chapter_arg(args.file, args.volume)
            ja_file = args.ja_file or ch.ja_path
            ru_file = args.ru_file or ch.output_path
            merged_path = Path(args.merged) if args.merged else (
                OUT_DIR / f"{ch.chapter_id_full}-sma-merged.json")
            merged = load_merged(merged_path)
            available = sorted({b.get("block") for b in merged.get("blocks", [])})
            try:
                wanted = parse_blocks(args.blocks) or available
            except ValueError as exc:
                print(f"ОШИБКА: {exc}")
                return EXIT_USAGE
            missing = [b for b in wanted if b not in available]
            if missing:
                print(f"ОШИБКА: в {merged_path} нет блоков: {missing}; "
                      f"доступны: {available}")
                return EXIT_USAGE
            if not wanted:
                print(f"ОШИБКА: в {merged_path} нет candidates")
                return EXIT_USAGE
            for block in wanted:
                cases.append(build_case(ch.chapter_id_full, block, merged,
                                        ja_file, ru_file))
            out = Path(args.output) if args.output else (
                OUT_DIR / f"{ch.chapter_id_full}-sma-verdict.json")
            outputs = [out]
            if len(cases) > 1:
                outputs = [out.with_name(f"{out.stem}-b{c['block']}{out.suffix}")
                           for c in cases]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ОШИБКА: {exc}")
        return EXIT_USAGE

    print(f"Кейсов к верификации: {len(cases)}")
    for case, out in zip(cases, outputs):
        print(f"  блок {case['block']} ({case['chapter']}): "
              f"{len(case['candidates'])} candidate(s) → {out}")

    prompts = [build_prompt(case, skill_text) for case in cases]
    for case, prompt in zip(cases, prompts):
        status = "OK" if len(prompt) < PROMPT_CHAR_LIMIT else "FAIL"
        print(f"  блок {case['block']}: prompt {len(prompt)} симв. [{status}]")
        if len(prompt) >= PROMPT_CHAR_LIMIT:
            return EXIT_USAGE
        if args.dry_run:
            print("-" * 60)
            print(prompt)
            print("-" * 60)
    if args.dry_run:
        return EXIT_OK

    # --- запуск ------------------------------------------------------------
    try:
        adapter = rt.get_adapter("cline", model=args.model, provider=args.provider)
    except (RuntimeError, ValueError) as exc:
        print(f"ОШИБКА: {exc}")
        return EXIT_PROCESS

    run_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}"
    base = RUN_ROOT / run_id
    cwd = base / "verifier"
    data_dir = base / "cline-data"
    cwd.mkdir(parents=True, exist_ok=True)
    try:
        rt.prepare_data_dir(data_dir, args.model, args.provider)
    except (OSError, ValueError) as exc:
        print(f"ОШИБКА: не удалось подготовить изолированный data-dir: {exc}")
        return EXIT_PROCESS

    print(f"\nRuntime: provider={args.provider} model={args.model}")
    print(f"cwd: {cwd} (пустой)\ndata-dir: {data_dir} (изолирован)")

    failures = 0
    code = EXIT_MODEL
    kill_grace = int(os.environ.get("AINOVELEDIT_KILL_GRACE", "60"))
    for case, out in zip(cases, outputs):
        print(f"\nблок {case['block']}: {len(case['candidates'])} candidate(s)")
        payload, error, code = run_case(
            case, skill_text, adapter, data_dir, cwd,
            args.timeout, args.retries, kill_grace)
        if payload is None:
            print(f"  ОШИБКА: {error}")
            failures += 1
            continue
        written = write_outputs(out, payload, not args.no_md)
        print(f"  OK: {', '.join(p.name for p in written)}")
        for res in payload["results"]:
            print(f"    {res['candidate_id']} "
                  f"[{'+'.join(res['sources'])}/{res['status']}] → "
                  f"{res['verdict']} ({res['confidence']})")

    if args.keep_temp:
        print(f"\n  временные каталоги сохранены: {base}")
    else:
        shutil.rmtree(base, ignore_errors=True)

    if failures:
        return EXIT_PARTIAL if failures < len(cases) else code
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
