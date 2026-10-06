#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chapter_gate.py — гейт готовности главы по файлам-эвиденсам.

Финальная проверка перед сдачей главы: сверяет, что все обязательные входы
полного прогона (перевод → предфильтры → смысловой аудит → аудиты →
FINAL AUDIT) реально закрыты — только по файлам на диске, без LLM.

Проверки:
  1. output-файл существует.
  2. Блоки: каждый JA-блок <!-- block: N --> есть в output (RU).
  3. Предфильтры: отчёты 5 сканеров (grammar/style/format/address/
     alignment) существуют и не старее output-файла.
  4. Смысловой аудит: pre-check, запуски A и B (C — информационно),
     файл Фазы 1, результат Фазы 2 в output/_audit/sma/<глава>/.
  5. Отчёт аудита output/_audit/vXX-chYY.md существует и не старее
     output-файла.
  6. В output нет неразобранных маркеров <!-- ??? -->.

Детекция ≠ решение: гейт не правит текст и не выносит суждений о качестве —
он только констатирует, какие фазы не оставили файлов-эвиденсов.

Коды возврата: 0 — все пункты закрыты; 1 — есть незакрытые пункты;
2 — ошибка входных данных (нет файла, неизвестная проверка).

Примеры:
    python scripts/chapter_gate.py --file v3-ch10.md
    python scripts/chapter_gate.py --file v3-ch10.md --report
    python scripts/chapter_gate.py --selftest
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import merged_io  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
AUDIT = OUT / "_audit"
PREFILTER = AUDIT / "_prefilter"
JA_DIR = BASE / "translates" / "ja"
SMA = AUDIT / "sma"

# Те же 5 отчётов, что считает меню полного прогона в
# tools/agent_workflow.py (PREFILTER_KINDS): check_records --report не
# умеет, drift_scan опционален — они гейтом не проверяются.
PREFILTER_KINDS = ("grammar", "style", "format", "address", "alignment")
OPEN_MARKER = "<!-- ??? -->"


def _rel(path: Path) -> str:
    """Путь относительно AINovelEdit в posix-вида (для отчёта и консоли)."""
    try:
        return path.relative_to(BASE).as_posix()
    except ValueError:
        return str(path)


def _mtime(path: Path) -> float | None:
    try:
        return path.stat().st_mtime
    except OSError:
        return None


def _is_fresh(report: Path, source: Path) -> bool:
    """Отчёт не старее источника (оба файла существуют, report >= source)."""
    report_mtime = _mtime(report)
    source_mtime = _mtime(source)
    return (report_mtime is not None
            and source_mtime is not None
            and report_mtime >= source_mtime)


def _stamp(path: Path) -> str:
    mtime = _mtime(path)
    if mtime is None:
        return "—"
    return datetime.fromtimestamp(mtime).strftime("%d.%m %H:%M")


def build_paths(file_name: str) -> dict:
    """Раскладка файлов-эвиденсов главы (file_name — вида v3-ch10.md)."""
    stem = Path(file_name).stem
    padded = AUDIT / f"v{int(stem[1:stem.index('-')]):02d}-{stem[stem.index('-') + 1:]}.md"
    plain = AUDIT / f"{stem}.md"
    # Как и Chapter.audit_path оркестратора: вариант без ведущего нуля
    # берётся, только если padded-варианта нет; новый отчёт — по padded.
    audit = plain if (plain.is_file() and not padded.is_file()) else padded
    sma_dir = SMA / stem
    return {
        "file_name": file_name,
        "stem": stem,
        "output": OUT / file_name,
        "ja": JA_DIR / file_name,
        "audit": audit,
        "prefilter": {kind: PREFILTER / f"{stem}-{kind}.md"
                      for kind in PREFILTER_KINDS},
        "sma": {
            "precheck": sma_dir / "precheck" / "omission-precheck.json",
            "a": sma_dir / "a",
            "b": sma_dir / "b",
            "c": sma_dir / "c",
            "analysis": sma_dir / "analysis",
        },
        "gate_report": PREFILTER / f"{stem}-gate.md",
    }


def _block_numbers(path: Path) -> list[int]:
    """Номера смысловых блоков файла (пусто — файла нет или маркеров нет)."""
    try:
        return sorted(num for num, _ in merged_io.read_source_blocks(str(path)))
    except Exception:
        return []


def _json_runs(folder: Path, *, phase1: bool | None = None) -> int:
    """Число run-файлов в каталоге SMA.

    phase1=None — все <run_id>.json; True — только <run_id>.phase1.json;
    False — только обычные результаты (без .phase1.json).
    """
    if not folder.is_dir():
        return 0
    count = 0
    for entry in folder.iterdir():
        if not entry.is_file() or not entry.name.endswith(".json"):
            continue
        is_phase1 = entry.name.endswith(".phase1.json")
        if phase1 is True and not is_phase1:
            continue
        if phase1 is False and is_phase1:
            continue
        count += 1
    return count


def gate_checks(paths: dict) -> list[tuple[str, bool, str]]:
    """Чек-лист гейта: [(пункт, закрыт, деталь)]. Ничего не пишет."""
    checks: list[tuple[str, bool, str]] = []
    output = paths["output"]
    has_output = output.is_file()
    checks.append((
        "output-файл существует",
        has_output,
        _rel(output) if has_output else f"нет {_rel(output)}",
    ))

    # 2. Блоки: RU покрывает JA (тот же разбор маркеров, что у оркестратора).
    if not paths["ja"].is_file():
        checks.append(("Блоки: RU покрывает JA", False,
                       f"нет JA-файла {_rel(paths['ja'])}"))
    else:
        ja_blocks = _block_numbers(paths["ja"])
        if not ja_blocks:
            checks.append(("Блоки: RU покрывает JA", False,
                           "в JA нет маркеров <!-- block: N -->"))
        elif not has_output:
            checks.append(("Блоки: RU покрывает JA", False,
                           "нет output-файла"))
        else:
            ru_blocks = set(_block_numbers(output))
            missing = [n for n in ja_blocks if n not in ru_blocks]
            detail = (f"блоков RU/JA: {len(ru_blocks)}/{len(ja_blocks)}"
                      + (f"; нет в RU: {missing[:10]}" if missing else ""))
            checks.append(("Блоки: RU покрывает JA", not missing, detail))

    # 3. Предфильтры: 5 отчётов существуют и не старее текста.
    problems = []
    for kind, report in paths["prefilter"].items():
        if not report.is_file():
            problems.append(f"{kind}: нет отчёта")
        elif not has_output:
            problems.append(f"{kind}: нет output-файла для сверки")
        elif not _is_fresh(report, output):
            problems.append(f"{kind}: устарел ({_stamp(report)})")
    checks.append((
        "Предфильтры: отчёты 5 сканеров свежие",
        not problems,
        "все 5 свежие" if not problems else "; ".join(problems),
    ))

    # 4. Смысловой аудит: pre-check, A+B (C — информационно), Ф1, Ф2.
    sma = paths["sma"]
    precheck_ok = sma["precheck"].is_file()
    checks.append((
        "SMA: Omission Pre-check (evidence)",
        precheck_ok,
        _rel(sma["precheck"]) if precheck_ok else "нет evidence pre-check",
    ))
    runs_a = _json_runs(sma["a"])
    runs_b = _json_runs(sma["b"])
    runs_c = _json_runs(sma["c"])
    checks.append((
        "SMA: запуски A и B (C опционален)",
        runs_a > 0 and runs_b > 0,
        f"A: {runs_a}, B: {runs_b}, C: {runs_c}",
    ))
    phase1 = _json_runs(sma["analysis"], phase1=True)
    checks.append(("SMA: Фаза 1 (blind)", phase1 > 0, f"файлов: {phase1}"))
    phase2 = _json_runs(sma["analysis"], phase1=False)
    checks.append(("SMA: Фаза 2 (результаты)", phase2 > 0,
                   f"результатов: {phase2}"))

    # 5. Отчёт аудита: существует и не старее текста.
    audit = paths["audit"]
    if not audit.is_file():
        checks.append(("Отчёт аудита свежий", False, f"нет {_rel(audit)}"))
    elif not has_output:
        checks.append(("Отчёт аудита свежий", False, "нет output-файла"))
    elif not _is_fresh(audit, output):
        checks.append(("Отчёт аудита свежий", False,
                       f"устарел ({_stamp(audit)}) — текст правился позже"))
    else:
        checks.append(("Отчёт аудита свежий", True,
                       f"{_rel(audit)} ({_stamp(audit)})"))

    # 6. Открытые решения: <!-- ??? --> не должны дожить до сдачи главы.
    if not has_output:
        checks.append(("Решения закрыты (нет <!-- ??? -->)", False,
                       "нет output-файла"))
    else:
        try:
            text = output.read_text(encoding="utf-8")
        except OSError:
            text = ""
        open_count = text.count(OPEN_MARKER)
        checks.append((
            "Решения закрыты (нет <!-- ??? -->)",
            open_count == 0,
            f"открытых маркеров: {open_count}",
        ))
    return checks


def render_report(paths: dict, checks: list[tuple[str, bool, str]]) -> str:
    """Markdown-отчёт гейта (тот же текст, что печатается в консоль)."""
    closed = sum(1 for _, ok, _ in checks if ok)
    ready = closed == len(checks)
    lines = [
        f"# Гейт готовности главы: {paths['file_name']}",
        "",
        f"Запуск: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Команда: python scripts/chapter_gate.py --file {paths['file_name']}"
        " --report",
        "",
    ]
    for label, ok, detail in checks:
        lines.append(f"- [{'x' if ok else ' '}] {label}: {detail}")
    lines += [
        "",
        f"Итог: {closed}/{len(checks)} пунктов закрыто — "
        f"{'ГОТОВА' if ready else 'НЕ ГОТОВА'}",
        "",
        "Гейт не правит текст: каждый незакрытый пункт закрывается своей",
        "фазой полного прогона (перевод → предфильтры → смысловой аудит →",
        "аудиты → FINAL AUDIT), затем гейт запускается повторно.",
        "",
    ]
    return "\n".join(lines)


def run_selftest() -> int:
    """Дерево-фиксатура во временном каталоге; ничего в проекте не пишется."""
    failed = 0

    def check(ok: bool, label: str) -> None:
        nonlocal failed
        print(("  OK   " if ok else "  FAIL ") + label)
        if not ok:
            failed += 1

    def write(path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        file_name = "v9-ch9.md"
        stem = "v9-ch9"
        blocks = ("<!-- block: 1 -->\n\nТекст первого блока.\n\n"
                  "<!-- block: 2 -->\n\nТекст второго блока.\n")
        paths = {
            "file_name": file_name,
            "stem": stem,
            "output": root / "output" / file_name,
            "ja": root / "translates" / "ja" / file_name,
            "audit": root / "output" / "_audit" / "v09-ch9.md",
            "prefilter": {kind: root / "output" / "_audit" / "_prefilter"
                          / f"{stem}-{kind}.md"
                          for kind in PREFILTER_KINDS},
            "sma": {
                "precheck": root / "output" / "_audit" / "sma" / stem
                            / "precheck" / "omission-precheck.json",
                "a": root / "output" / "_audit" / "sma" / stem / "a",
                "b": root / "output" / "_audit" / "sma" / stem / "b",
                "c": root / "output" / "_audit" / "sma" / stem / "c",
                "analysis": root / "output" / "_audit" / "sma" / stem
                            / "analysis",
            },
            "gate_report": root / "output" / "_audit" / "_prefilter"
                           / f"{stem}-gate.md",
        }

        def fill_all() -> None:
            write(paths["output"], blocks)
            write(paths["ja"], blocks)
            for report in paths["prefilter"].values():
                write(report, "# отчёт\n")
            write(paths["sma"]["precheck"], "{}")
            for kind in ("a", "b", "c"):
                write(paths["sma"][kind] / "20260101-0000-abcd.json", "{}")
            analysis = paths["sma"]["analysis"]
            write(analysis / "20260101-0000-aaaa.phase1.json", "{}")
            write(analysis / "20260101-0000-bbbb.json", "{}")
            write(paths["audit"], "## Итог\n")
            # Свежесть: текст главы старше отчётов и отчёта аудита.
            base = 2_000_000_000
            for path in [paths["output"], paths["ja"]]:
                os.utime(path, (base - 100, base - 100))
            for path in list(paths["prefilter"].values()) + [paths["audit"]]:
                os.utime(path, (base, base))

        fill_all()
        checks = gate_checks(paths)
        results = {label: ok for label, ok, _ in checks}
        check(all(ok for _, ok, _ in checks),
              "полное дерево: все пункты закрыты")
        check(len(checks) == 9,
              f"чек-лист из 9 пунктов (получено {len(checks)})")

        # 1) RU потерял блок → блочный пункт падает.
        write(paths["output"], "<!-- block: 1 -->\n\nТекст первого блока.\n")
        os.utime(paths["output"], (3_000_000_000, 3_000_000_000))
        results = {label: ok for label, ok, _ in gate_checks(paths)}
        check(not results.get("Блоки: RU покрывает JA", True),
              "потерянный RU-блок закрывает гейт")

        fill_all()
        # 2) удалён отчёт предфильтра → предфильтры падают.
        paths["prefilter"]["style"].unlink()
        results = {label: ok for label, ok, _ in gate_checks(paths)}
        check(not results.get("Предфильтры: отчёты 5 сканеров свежие", True),
              "удалённый отчёт предфильтра закрывает гейт")

        fill_all()
        # 3) нет результатов Фазы 2 → пункт Фазы 2 падает.
        for entry in paths["sma"]["analysis"].iterdir():
            if entry.name.endswith(".json") \
                    and not entry.name.endswith(".phase1.json"):
                entry.unlink()
        results = {label: ok for label, ok, _ in gate_checks(paths)}
        check(not results.get("SMA: Фаза 2 (результаты)", True),
              "отсутствие Фазы 2 закрывает гейт")

        fill_all()
        # 4) маркер <!-- ??? --> → пункт решений падает.
        write(paths["output"], blocks + "\n" + OPEN_MARKER + "\n")
        os.utime(paths["output"], (3_000_000_000, 3_000_000_000))
        results = {label: ok for label, ok, _ in gate_checks(paths)}
        check(not results.get("Решения закрыты (нет <!-- ??? -->)", True),
              "открытый ??? закрывает гейт")

        fill_all()
        # 5) отчёт аудита старше текста → пункт аудита падает.
        os.utime(paths["audit"], (1_000_000_000, 1_000_000_000))
        results = {label: ok for label, ok, _ in gate_checks(paths)}
        check(not results.get("Отчёт аудита свежий", True),
              "устаревший отчёт аудита закрывает гейт")

        fill_all()
        # 6) отчёт гейта рендерится и содержит вердикт.
        report = render_report(paths, gate_checks(paths))
        check("Итог: 9/9 пунктов закрыто — ГОТОВА" in report,
              "render_report: вердикт ГОТОВА на полном дереве")

    print()
    if failed:
        print("[selftest] ПРОВАЛЕНО: %d проверок" % failed)
        return 1
    print("[selftest] OK: все проверки гейта пройдены")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(
        description="Гейт готовности главы по файлам-эвиденсам")
    ap.add_argument("--file", help="напр. v3-ch10.md")
    ap.add_argument("--report", action="store_true",
                    help="записать чек-лист в output/_audit/_prefilter/"
                         "<глава>-gate.md")
    ap.add_argument("--selftest", action="store_true",
                    help="прогнать контрольные тесты (временное дерево)")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()

    if not args.file:
        ap.error("нужен --file или --selftest")
    file_name = Path(args.file).name
    paths = build_paths(file_name)
    if not paths["output"].is_file() and not paths["ja"].is_file():
        print(f"ОШИБКА: нет ни output-, ни JA-файла {file_name}",
              file=sys.stderr)
        return 2

    checks = gate_checks(paths)
    report = render_report(paths, checks)
    print(report)

    if args.report:
        PREFILTER.mkdir(parents=True, exist_ok=True)
        paths["gate_report"].write_text(report, encoding="utf-8",
                                        newline="\n")
        print(f"Отчёт: {_rel(paths['gate_report'])}")

    return 0 if all(ok for _, ok, _ in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
