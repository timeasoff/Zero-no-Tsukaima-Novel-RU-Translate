#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LEGACY / NOT IMPLEMENTED — автоматический semantic audit (merge A+B).

Статус: НЕ РЕАЛИЗОВАН / НЕ ПОДДЕРЖИВАЕТСЯ. Не использовать в текущем
pipeline. Сохранён только как задел/история. Подробности:
legacy/semantic-audit-auto/LEGACY.md.

merge_findings.py — объединение находок двух независимых смысловых аудитов.

Работает на уровне отдельных findings, а не только блоков.
Поддерживает: BOTH_FOUND, ONLY_A, ONLY_B, DIFFERENT_FINDINGS.

Использование (LEGACY — не в текущем pipeline):
    python legacy/semantic-audit-auto/merge_findings.py --a vXX-chYY-sma-a.json --b vXX-chYY-sma-b.json --output vXX-chYY-sma-merged.json
"""
import argparse
import json
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def load_findings(path: Path) -> dict:
    """Загружает JSON-файл с находками."""
    if not path.exists():
        return {"findings": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data
    except (json.JSONDecodeError, OSError) as exc:
        print(f"ОШИБКА: не удалось загрузить {path}: {exc}", file=sys.stderr)
        return {"findings": []}


def normalize_text(text: str) -> str:
    """Нормализует текст для сравнения (нижний регистр, без пробелов)."""
    return "".join(text.lower().split())


def findings_match(finding_a: dict, finding_b: dict) -> bool:
    """
    Определяет, относятся ли две находки к одной проблеме.

    Консервативный подход: считаем находки совпадающими, если:
    1. Совпадает номер блока
    2. Совпадает тип проблемы (problem)
    3. Совпадает source (или очень близок)

    Если хотя бы один критерий не совпадает — находки разные.
    """
    # Проверяем номер блока
    if finding_a.get("block") != finding_b.get("block"):
        return False

    # Проверяем тип проблемы
    problem_a = finding_a.get("problem", "").lower()
    problem_b = finding_b.get("problem", "").lower()
    if problem_a != problem_b:
        return False

    # Проверяем source (нормализованный)
    source_a = normalize_text(finding_a.get("source", ""))
    source_b = normalize_text(finding_b.get("source", ""))
    if source_a != source_b:
        return False

    return True


def merge_findings(data_a: dict, data_b: dict) -> dict:
    """
    Объединяет находки двух аудиторов.

    Возвращает структуру:
    {
        "chapter": "vXX-chYY",
        "blocks": [
            {
                "block": 75,
                "findings": [
                    {
                        "status": "BOTH_FOUND",
                        "finding_a": {...},
                        "finding_b": {...}
                    },
                    {
                        "status": "ONLY_A",
                        "finding_a": {...}
                    },
                    {
                        "status": "ONLY_B",
                        "finding_b": {...}
                    }
                ]
            }
        ]
    }
    """
    findings_a = data_a.get("findings", [])
    findings_b = data_b.get("findings", [])

    # Группируем по блокам
    blocks_a = {}
    for f in findings_a:
        block = f.get("block")
        if block is not None:
            blocks_a.setdefault(block, []).append(f)

    blocks_b = {}
    for f in findings_b:
        block = f.get("block")
        if block is not None:
            blocks_b.setdefault(block, []).append(f)

    all_blocks = sorted(set(blocks_a.keys()) | set(blocks_b.keys()))

    merged_blocks = []
    for block in all_blocks:
        a_list = blocks_a.get(block, [])
        b_list = blocks_b.get(block, [])

        merged_findings = []
        used_b = set()

        # Для каждой находки A ищем совпадение в B
        for finding_a in a_list:
            found_match = False
            for idx_b, finding_b in enumerate(b_list):
                if idx_b in used_b:
                    continue
                if findings_match(finding_a, finding_b):
                    merged_findings.append({
                        "status": "BOTH_FOUND",
                        "finding_a": finding_a,
                        "finding_b": finding_b
                    })
                    used_b.add(idx_b)
                    found_match = True
                    break

            if not found_match:
                merged_findings.append({
                    "status": "ONLY_A",
                    "finding_a": finding_a
                })

        # Добавляем оставшиеся находки B
        for idx_b, finding_b in enumerate(b_list):
            if idx_b not in used_b:
                merged_findings.append({
                    "status": "ONLY_B",
                    "finding_b": finding_b
                })

        merged_blocks.append({
            "block": block,
            "findings": merged_findings
        })

    return {
        "chapter": data_a.get("chapter", ""),
        "blocks": merged_blocks
    }


def render_report(merged: dict) -> str:
    """Создаёт человекочитаемый отчёт."""
    lines = [
        f"# Объединённый отчёт смыслового аудита: {merged.get('chapter', '')}",
        "",
        f"Блоков с находками: {len(merged.get('blocks', []))}",
        ""
    ]

    for block_data in merged.get("blocks", []):
        block = block_data.get("block")
        findings = block_data.get("findings", [])

        lines.append(f"## Блок {block}")
        lines.append("")

        for finding in findings:
            status = finding.get("status")

            if status == "BOTH_FOUND":
                fa = finding.get("finding_a", {})
                fb = finding.get("finding_b", {})
                lines.append(f"### BOTH_FOUND")
                lines.append(f"- **Проблема:** {fa.get('problem', '')}")
                lines.append(f"- **Source:** {fa.get('source', '')}")
                lines.append(f"- **Current:** {fa.get('current', '')}")
                lines.append(f"- **Reason (A):** {fa.get('reason', '')}")
                lines.append(f"- **Reason (B):** {fb.get('reason', '')}")
                lines.append(f"- **Severity:** {fa.get('severity', '')}")
                lines.append("")

            elif status == "ONLY_A":
                fa = finding.get("finding_a", {})
                lines.append(f"### ONLY_A")
                lines.append(f"- **Проблема:** {fa.get('problem', '')}")
                lines.append(f"- **Source:** {fa.get('source', '')}")
                lines.append(f"- **Current:** {fa.get('current', '')}")
                lines.append(f"- **Reason:** {fa.get('reason', '')}")
                lines.append(f"- **Severity:** {fa.get('severity', '')}")
                lines.append("")

            elif status == "ONLY_B":
                fb = finding.get("finding_b", {})
                lines.append(f"### ONLY_B")
                lines.append(f"- **Проблема:** {fb.get('problem', '')}")
                lines.append(f"- **Source:** {fb.get('source', '')}")
                lines.append(f"- **Current:** {fb.get('current', '')}")
                lines.append(f"- **Reason:** {fb.get('reason', '')}")
                lines.append(f"- **Severity:** {fb.get('severity', '')}")
                lines.append("")

    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(
        description="Объединение находок двух независимых смысловых аудитов"
    )
    ap.add_argument("--a", required=True, help="JSON-файл аудитора A")
    ap.add_argument("--b", required=True, help="JSON-файл аудитора B")
    ap.add_argument("--output", default=None, help="Выходной JSON-файл")
    ap.add_argument("--report", default=None, help="Выходной отчёт (markdown)")
    args = ap.parse_args()

    path_a = Path(args.a)
    path_b = Path(args.b)

    data_a = load_findings(path_a)
    data_b = load_findings(path_b)

    merged = merge_findings(data_a, data_b)

    # Сохраняем JSON
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(merged, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"OK: объединённый JSON сохранён в {output_path}")

    # Сохраняем отчёт
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_report(merged), encoding="utf-8")
        print(f"OK: отчёт сохранён в {report_path}")

    # Выводим статистику
    total_findings = 0
    both_found = 0
    only_a = 0
    only_b = 0

    for block_data in merged.get("blocks", []):
        for finding in block_data.get("findings", []):
            total_findings += 1
            status = finding.get("status")
            if status == "BOTH_FOUND":
                both_found += 1
            elif status == "ONLY_A":
                only_a += 1
            elif status == "ONLY_B":
                only_b += 1

    print(f"\nСтатистика:")
    print(f"  Всего находок: {total_findings}")
    print(f"  BOTH_FOUND: {both_found}")
    print(f"  ONLY_A: {only_a}")
    print(f"  ONLY_B: {only_b}")


if __name__ == "__main__":
    main()
