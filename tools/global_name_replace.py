#!/usr/bin/env python3
"""Replace a character name and its Russian inflected forms in output files.

The replacement is deliberately conservative: a line that already contains the
new (canonical) form is left untouched. Such lines are discussions of the name
choice («Генриетта или Анриетта?», «"Анриетта" — уже коверкание имени»), not
usages of the old form — rewriting them would destroy the very question the
answering paragraph explains.

Line endings of the processed file are preserved.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FORMS = {
    "Анриетта": "Генриетта", "Анриетты": "Генриетты",
    "Анриетте": "Генриетте", "Анриетту": "Генриетту",
    "Анриеттой": "Генриеттой", "Анриеттою": "Генриеттою",
    "анриетта": "генриетта", "анриетты": "генриетты",
    "анриетте": "генриетте", "анриетту": "генриетту",
    "анриеттой": "генриеттой", "анриеттою": "генриеттою",
}
PATTERN = re.compile(
    r"(?<![А-Яа-яЁё])(?:" + "|".join(map(re.escape, sorted(FORMS, key=len, reverse=True))) + r")(?![А-Яа-яЁё])"
)
NEW_FORMS = tuple(sorted(set(FORMS.values()), key=len, reverse=True))


def completed_volumes(path: Path) -> set[int]:
    result: set[int] = set()
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"\|\s*(\d+)\s*\|\s*завершён", line, re.IGNORECASE)
            if match:
                result.add(int(match.group(1)))
    return result


def volume_number(path: Path) -> int | None:
    match = re.fullmatch(r"v(\d+)-.+\.md", path.name)
    return int(match.group(1)) if match else None


def replace_text(text: str) -> tuple[str, int]:
    """Заменить старые формы построчно; строки с новой формой не трогать."""
    count = 0
    result: list[str] = []

    def replacement(match: re.Match[str]) -> str:
        return FORMS[match.group(0)]

    for line in text.splitlines(keepends=True):
        if any(form in line for form in NEW_FORMS):
            # строка обсуждает выбор формы (уже содержит каноническое имя)
            result.append(line)
            continue
        updated, n = PATTERN.subn(replacement, line)
        count += n
        result.append(updated)
    return "".join(result), count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--include-completed", action="store_true",
                        help="allow replacement in completed volumes")
    parser.add_argument("--dry-run", action="store_true",
                        help="report changes without writing files")
    args = parser.parse_args()

    root = args.root.resolve()
    output = root / "AINovelEdit" / "output" / "chapters"
    completed = completed_volumes(root / "AINovelEdit" / "completed.md")
    if not output.is_dir():
        print(f"output directory not found: {output}", file=sys.stderr)
        return 2

    total = files = 0
    skipped: list[str] = []
    for path in sorted(output.glob("v*.md")):
        volume = volume_number(path)
        if volume in completed and not args.include_completed:
            skipped.append(path.name)
            continue
        original = path.read_text(encoding="utf-8", newline="")
        updated, count = replace_text(original)
        if not count:
            continue
        files += 1
        total += count
        action = "would update" if args.dry_run else "updated"
        print(f"{action}: {path.relative_to(root)} ({count})")
        if not args.dry_run:
            path.write_text(updated, encoding="utf-8", newline="")

    print(f"replacements: {total} in {files} files")
    if skipped:
        print("skipped completed volumes: " + ", ".join(skipped), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
