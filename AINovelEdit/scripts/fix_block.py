#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_block.py — точечная замена текста блока в файле output/ без перезаписи
всего файла. Используется скиллом translation-audit для исправления ошибок,
найденных в уже сохранённых блоках.

Использование:
    python scripts/fix_block.py --file v14-ch01.md --block 2 --text "новый текст"
"""
import argparse
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

OUT_DIR = Path(__file__).resolve().parent.parent / "output"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="имя файла в output/")
    ap.add_argument("--block", type=int, required=True, help="номер блока")
    ap.add_argument("--text", default=None, help="новый текст блока; иначе stdin")
    args = ap.parse_args()

    path = (OUT_DIR / args.file).resolve()
    if path.parent != OUT_DIR or not path.exists():
        print("ОШИБКА: файл не найден в output/", file=sys.stderr)
        sys.exit(1)

    text = args.text if args.text is not None else sys.stdin.read()
    if not text.strip():
        print("ОШИБКА: пустой текст блока", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    marker = "<!-- block: %d -->" % args.block
    idx = content.find(marker)
    if idx == -1:
        print("ОШИБКА: маркер блока %d не найден" % args.block, file=sys.stderr)
        sys.exit(1)
    start = idx + len(marker)
    m = re.search(r"<!-- block: \d+ -->", content[start:])
    end = start + m.start() if m else len(content)

    seg = "\n\n" + text.strip("\n") + "\n\n"
    path.write_text(content[:start] + seg + content[end:],
                    encoding="utf-8", newline="\n")
    print("OK: %s | блок %d заменён | файл %d байт" % (
        path.name, args.block, path.stat().st_size))


if __name__ == "__main__":
    main()
