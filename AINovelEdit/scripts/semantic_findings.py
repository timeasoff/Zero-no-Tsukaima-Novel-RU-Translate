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

Обнаружение ≠ вердикт: скрипт лишь проверяет структуру finding и рисует
человекочитаемый отчёт. Решение (CONFIRMED_ERROR / DISPUTED) принимает
Analyzer по сверке JA → RU.
"""
import argparse
import json
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "semantic_findings"

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

def cmd_validate(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = []
    if isinstance(doc, dict) and "finding" in doc:
        # fixture-обёртка: {"case": …, "expect": …, "finding": {…}}
        errors = ["finding: %s" % e for e in validate_finding(doc["finding"])]
    elif isinstance(doc, dict) and "findings" in doc:
        for i, f in enumerate(doc["findings"]):
            errors += ["findings[%d]: %s" % (i, e) for e in validate_finding(f)]
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
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()
    if args.validate:
        return cmd_validate(args.validate)
    if args.render:
        return cmd_render(args.render)
    ap.error("укажи --selftest | --validate <file> | --render <file>")


if __name__ == "__main__":
    sys.exit(main())




