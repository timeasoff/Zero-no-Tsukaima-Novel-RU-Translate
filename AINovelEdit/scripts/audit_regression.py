#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_regression.py — регрессия по КЛАССАМ дефектов manual-fix v5-ch03.

Корпус: ручные правки коммита 133ff7e (`_work/qa_corpus/`, фикстура
`scripts/fixtures/manual-fixes/v5-ch03.json`). Тестируются КЛАССЫ дефектов,
а не точные фразы: инструкции обязаны содержать закреплённые правила,
сканеры — ловить подтверждённые дефекты и молчать на контрольных местах,
фикстура — быть приземлённой в реальные ревизии и корпус.

Три группы:

  G1  инструкции — якоря правил присутствуют в скиллах/промптах/шлюзе,
      отменённые формулировки отсутствуют (документ ≠ доказательство
      качества, но его отсутствие — доказательство незакрытого пробела);
  G2  сканеры — класс RU_ONLY ловит дефекты ДОфиксовой версии и молчит
      на пост-версии и на контролах (что НЕ является дефектом);
  G3  фикстура — before/after приземлены в prefix/postfix.text, ханки
      принадлежат корпусу, вердикты в словаре policy, ja_ref совпадает
      с JA-строкой, summary консистентно.

Использование:
    python scripts/audit_regression.py --selftest
"""

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # AINovelEdit/scripts
ROOT = HERE.parent                              # AINovelEdit/
REPO = ROOT.parent                              # корень репозитория
SKILLS = ROOT / ".agents" / "skills"
FIXTURE = HERE / "fixtures" / "manual-fixes" / "v5-ch03.json"
CORPUS = ROOT / "_work" / "qa_corpus"

sys.path.insert(0, str(HERE))
try:
    import style_scan  # noqa: E402
except Exception as exc:                        # pragma: no cover
    style_scan = None
    STYLE_SCAN_IMPORT_ERROR = repr(exc)
else:
    STYLE_SCAN_IMPORT_ERROR = ""

# ---------------------------------------------------------------------------
# G1. Якоря инструкций
# ---------------------------------------------------------------------------

# (файл относительно .agents/skills/, обязательные подстроки)
G1_ANCHORS = [
    ("russian-style-audit/SKILL.md", [
        "19.1. RU-only проход",
        "не закрывает русскую проблему",
    ]),
    ("russian-grammar-control/SKILL.md", ["RGC-9"]),
    ("russian-grammar-control/references/grammar-traps.md", ["RGC-9"]),
    ("novel-editor/SKILL.md", [
        "FINAL READ — обязательный независимый перечит главы",
        "## FINAL READ",
    ]),
    ("translation-audit/SKILL.md", [
        "переносимост",              # тест переносимости образа
        "фрейм/голос",               # ошибки атрибуции фрейма
        "Контроль после правки",     # RECHECK после fix_block
        "полярность",                # оценка まあまあ
        "Контроль — НЕ дефект",      # контроли: правка ≠ эталон
    ]),
    ("pragmatic-audit/SKILL.md", ["Оценка: полярность и степень"]),
    ("semantic-audit-a/SKILL.md", ["полярность"]),
    ("semantic-audit-b/SKILL.md", ["звень"]),
    ("self-review/SKILL.md", ["Фрейм и голос"]),
]

# (путь к файлу, обязательные подстроки) — инструменты вне скиллов
G1_EXTERNAL = [
    (REPO / "tools" / "agent_workflow.py", ["FINAL READ", "RU-only"]),
    (HERE / "chapter_gate.py", ["FINAL READ"]),
    (HERE / "style_scan.py", ["RU_ONLY"]),
]

# отменённые/ложные формулировки, обязанные отсутствовать
G1_FORBIDDEN = [
    ("translation-audit/SKILL.md", "а не «личико-то так себе»"),
    ("translation-audit/SKILL.md", "загговорили"),
    ("translation-audit/SKILL.md", "やutt"),
    ("translation-audit/SKILL.md", "叙述者"),
]

# ---------------------------------------------------------------------------
# G2. Контрольные строки сканера
# ---------------------------------------------------------------------------

# Контроли: формы, сохранённые человеком / корректные до-версии.
# Сканер обязан молчать (иначе он канонизирует правку человека или
# ловит работящий образ).
G2_EXPLICIT_CONTROLS = [
    "Видимо, то, что не выходило ртом, норовило высказаться подошвой.",
    "Луиза следила за тем, чтобы ноги не летели.",
    "Луиза невольно поблагодарила гадателя ногой.",
    "Ну, личико-то так себе…",
]


class Checker:
    """Счётчик проверок с накоплением падений."""

    def __init__(self):
        self.checks = 0
        self.failed = []

    def check(self, cond, msg):
        self.checks += 1
        if cond:
            print("  OK   %s" % msg)
        else:
            self.failed.append(msg)
            print("  FAIL %s" % msg)

    def fail(self, msg):
        self.check(False, msg)


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# G1
# ---------------------------------------------------------------------------

def g1_instructions(c):
    print("G1. Якоря инструкций")
    for rel, needles in G1_ANCHORS:
        path = SKILLS / rel
        if not path.exists():
            c.fail("%s: файл отсутствует" % rel)
            continue
        text = read_text(path)
        for needle in needles:
            c.check(needle in text, "%s: есть якорь %r" % (rel, needle))

    for path, needles in G1_EXTERNAL:
        rel = str(path.relative_to(REPO))
        if not path.exists():
            c.fail("%s: файл отсутствует" % rel)
            continue
        text = read_text(path)
        for needle in needles:
            c.check(needle in text, "%s: есть якорь %r" % (rel, needle))

    for rel, forbidden in G1_FORBIDDEN:
        path = SKILLS / rel
        if not path.exists():
            c.fail("%s: файл отсутствует" % rel)
            continue
        c.check(forbidden not in read_text(path),
                "%s: нет отменённого %r" % (rel, forbidden))


# ---------------------------------------------------------------------------
# G2
# ---------------------------------------------------------------------------

def ru_only_hits(text):
    """Число вхождений правил класса RU_ONLY в тексте."""
    if style_scan is None:
        return None
    return sum(1 for regex, _ in style_scan.RU_ONLY_PATTERNS
               if regex.search(text))


def ru_only_categories(paragraph):
    """Категории находок style_scan по абзацу (для сканирования строк)."""
    if style_scan is None:
        return None
    return [cat for _, cat, _ in style_scan.scan_paragraph(1, paragraph)]


def g2_scanners(c):
    print("G2. Сканеры: класс RU_ONLY (ловит дефекты / молчит на контролах)")
    c.check(style_scan is not None,
            "style_scan импортируется (%s)" % (STYLE_SCAN_IMPORT_ERROR or "OK"))
    if style_scan is None:
        return

    pre_path = CORPUS / "revisions" / "v5-ch03" / "prefix.text"
    post_path = CORPUS / "revisions" / "v5-ch03" / "postfix.text"
    for p in (pre_path, post_path):
        c.check(p.exists(), "ревизия существует: %s" % p.relative_to(ROOT))
    if not (pre_path.exists() and post_path.exists()):
        return
    pre_text = read_text(pre_path)
    post_text = read_text(post_path)

    # 2.1 Правила, подтверждённые ЭТОЙ главой (помечены в msg), обязаны
    #     срабатывать на до-тексте: иначе правило — мёртвое/не приземлённое.
    tagged = [(rx, msg) for rx, msg in style_scan.RU_ONLY_PATTERNS
              if "v5-ch03" in msg]
    c.check(len(tagged) >= 7,
            "правил RU_ONLY с меткой v5-ch03: %d (≥ 7)" % len(tagged))
    misses = [msg for rx, msg in tagged if not rx.search(pre_text)]
    c.check(not misses,
            "все %d правил v5-ch03 срабатывают на до-тексте"
            " (нет: %s)" % (len(tagged), "; ".join(misses) or "—"))

    # 2.2 На исправленном тексте класс обязан молчать.
    post_hits = ru_only_hits(post_text)
    c.check(post_hits == 0,
            "на пост-версии RU_ONLY: %s (ожидается 0)" % post_hits)

    # 2.3 Каждый кейс, чей ожидаемый владелец — style_scan:RU_ONLY,
    #     обязан ловиться по своему before (класс механизован).
    fx = json.loads(read_text(FIXTURE))
    mech = [case for case in fx["cases"]
            if str(case.get("expected_owner", "")).startswith("style_scan:RU_ONLY")]
    c.check(bool(mech), "кейсов с owner style_scan:RU_ONLY: %d" % len(mech))
    for case in mech:
        hits = ru_only_hits(case["before"])
        c.check(hits and hits > 0,
                "%s: RU_ONLY ловит before (%s)" % (case["id"], hits))

    # 2.4 Контроли фикстуры и явные контроли — тишина.
    control_ids = fx.get("summary", {}).get("controls_do_not_flag", [])
    controls = [case for case in fx["cases"] if case["id"] in control_ids]
    c.check(len(controls) == len(control_ids),
            "контроли фикстуры найдены: %d/%d"
            % (len(controls), len(control_ids)))
    for case in controls:
        cats = ru_only_categories(case["before"])
        c.check(cats == [],
                "%s: контроль молчит (%s)" % (case["id"], cats))
    for text in G2_EXPLICIT_CONTROLS:
        cats = ru_only_categories(text)
        c.check(cats == [], "контроль молчит: %r → %s" % (text[:40], cats))

    # 2.5 Контроли обязаны НЕ считаться ошибкой по policy.
    for case in controls:
        c.check(case.get("counts_as_error") is False,
                "%s: counts_as_error = false" % case["id"])


# ---------------------------------------------------------------------------
# G3
# ---------------------------------------------------------------------------

def g3_fixture(c):
    print("G3. Фикстура корпуса (приземление в ревизии)")
    c.check(FIXTURE.exists(), "фикстура существует: %s"
            % FIXTURE.relative_to(ROOT))
    if not FIXTURE.exists():
        return
    try:
        fx = json.loads(read_text(FIXTURE))
    except Exception as exc:
        c.fail("фикстура разбирается как JSON: %r" % exc)
        return
    c.check(fx.get("schema") == "manual-fix-corpus/1",
            "schema = %s" % fx.get("schema"))
    c.check(fx.get("chapter") == "v5-ch03",
            "chapter = %s" % fx.get("chapter"))

    # файлы ревизий
    texts = {}
    for key in ("pre_text", "post_text"):
        rel = fx.get("revisions", {}).get(key)
        path = ROOT / str(rel).replace("AINovelEdit/", "", 1)
        if rel and path.exists():
            c.check(True, "ревизия существует: %s" % key)
            texts[key] = read_text(path)
        else:
            c.fail("ревизия отсутствует: %s → %s" % (key, rel))
    if not ("pre_text" in texts and "post_text" in texts):
        return
    pre_text, post_text = texts["pre_text"], texts["post_text"]

    # источники
    for key in ("ja", "en"):
        rel = fx.get("sources", {}).get(key)
        path = REPO / str(rel)
        c.check(bool(rel) and path.exists(), "источник %s: %s" % (key, rel))

    # hunk_source == статистика собранного корпуса
    hunks_json = CORPUS / "v5-ch03.hunks.json"
    c.check(hunks_json.exists(), "корпус ханков существует")
    if not hunks_json.exists():
        return
    corpus = json.loads(read_text(hunks_json))
    stats = corpus["stats"]
    src = fx["hunk_source"]
    for field in ("hunks", "changed_lines_removed", "changed_lines_added"):
        c.check(src.get(field) == stats.get(field),
                "hunk_source.%s = %s == stats.%s"
                % (field, src.get(field), stats.get(field)))
    corpus_ids = {h["id"] for h in corpus["hunks"]}

    policy = set(fx["policy"]["counted_as_error"]) | \
        set(fx["policy"]["not_counted_as_error"])
    case_ids = [case["id"] for case in fx["cases"]]
    c.check(len(case_ids) == len(set(case_ids)), "id кейсов уникальны")
    c.check(len(fx["cases"]) >= 21,
            "кейсов: %d (≥ 21)" % len(fx["cases"]))

    ja_path = REPO / str(fx["sources"]["ja"])
    ja_lines = read_text(ja_path).splitlines() if ja_path.exists() else []

    for case in fx["cases"]:
        cid = case["id"]
        # приземление текста
        c.check(case["before"] in pre_text, "%s: before ∈ prefix.text" % cid)
        c.check(case["after"] in post_text, "%s: after ∈ postfix.text" % cid)
        # ханки из корпуса
        c.check(all(h in corpus_ids for h in case["hunks"]),
                "%s: ханки %s ∈ корпус" % (cid, case["hunks"]))
        # вердикт и политика
        verdict = case.get("verdict")
        c.check(verdict in policy, "%s: verdict %s ∈ policy" % (cid, verdict))
        counted = verdict in set(fx["policy"]["counted_as_error"])
        c.check(case.get("counts_as_error") is counted,
                "%s: counts_as_error %s согласован с policy"
                % (cid, case.get("counts_as_error")))
        # словари полей
        c.check(case.get("expected_detection") in ("MECHANICAL", "LLM", "MANUAL"),
                "%s: expected_detection = %s" % (cid, case.get("expected_detection")))
        c.check(case.get("actual", {}).get("detection") in ("HIT", "MISS"),
                "%s: detection = %s"
                % (cid, case.get("actual", {}).get("detection")))
        c.check(case.get("actual", {}).get("gate")
                in ("NOT_DETECTED", "LOST_AT_DECISION", "LOST_AT_EXECUTION"),
                "%s: gate = %s" % (cid, case.get("actual", {}).get("gate")))
        # JA-опора
        m = re.match(r"L(\d+)", str(case.get("ja_ref", "")))
        if m and ja_lines:
            n = int(m.group(1))
            ok = 1 <= n <= len(ja_lines) and case["ja"].strip() in ja_lines[n - 1]
            c.check(ok, "%s: ja_ref %s содержит ja" % (cid, case["ja_ref"]))
        else:
            c.fail("%s: ja_ref не разобран: %r" % (cid, case.get("ja_ref")))

    # summary
    summary = fx.get("summary", {})
    counted = set(summary.get("counted_errors", []))
    not_counted = set(summary.get("not_counted", []))
    c.check(counted | not_counted == set(case_ids),
            "summary покрывает все кейсы (%d + %d = %d)"
            % (len(counted), len(not_counted), len(case_ids)))
    c.check(not (counted & not_counted), "summary без пересечений")
    for cid in counted:
        case = next(x for x in fx["cases"] if x["id"] == cid)
        c.check(case.get("counts_as_error") is True,
                "%s ∈ counted_errors и counts_as_error=true" % cid)

    by_id = {case["id"]: case for case in fx["cases"]}
    gates = {}
    for case in fx["cases"]:
        g = case["actual"]["gate"]
        gates[g] = gates.get(g, 0) + 1
    c.check(gates == summary.get("gate"),
            "summary.gate %s == фактические %s"
            % (summary.get("gate"), gates))
    for cid in summary.get("lost_at_decision_ids", []):
        c.check(by_id[cid]["actual"]["gate"] == "LOST_AT_DECISION",
                "%s ∈ lost_at_decision_ids" % cid)
    for cid in summary.get("lost_at_execution_ids", []):
        c.check(by_id[cid]["actual"]["gate"] == "LOST_AT_EXECUTION",
                "%s ∈ lost_at_execution_ids" % cid)

    controls = set(summary.get("controls_do_not_flag", []))
    c.check(controls <= set(case_ids), "controls ⊆ case ids")
    for cid in controls:
        c.check(by_id[cid].get("counts_as_error") is False,
                "контроль %s не считается ошибкой" % cid)
    human = set(summary.get("human_not_gold", []))
    c.check(human <= not_counted, "human_not_gold ⊆ not_counted")
    c.check({"v5ch03-c13", "v5ch03-c19", "v5ch03-c21"} <= controls,
            "ключевые контроли (ногой / так себе / ноги летели) на месте")


# ---------------------------------------------------------------------------

def run_selftest():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    c = Checker()
    g1_instructions(c)
    g2_scanners(c)
    g3_fixture(c)
    print()
    if c.failed:
        print("[regression] ПРОВАЛЕНО: %d проверок из %d"
              % (len(c.failed), c.checks))
        for msg in c.failed:
            print("   → %s" % msg)
        return 1
    print("[regression] OK: все %d проверок пройдены" % c.checks)
    return 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(
        description="Регрессия по классам дефектов manual-fix v5-ch03")
    ap.add_argument("--selftest", action="store_true",
                    help="прогнать группы G1/G2/G3")
    args = ap.parse_args()
    if not args.selftest:
        ap.error("нужен --selftest")
        return 1
    return run_selftest()


if __name__ == "__main__":
    sys.exit(main())