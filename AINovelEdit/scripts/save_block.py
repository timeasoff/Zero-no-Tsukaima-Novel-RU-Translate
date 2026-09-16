#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
save_block.py — безопасное дозаписывание (append) блока перевода в output/.

Использование:
    python scripts/save_block.py --file v14-ch01.md --new --block 1 --text "..."
    python scripts/save_block.py --file v14-ch01.md --block 2 --text "..."

Агент Cline вызывает этот скрипт вместо прямой записи файлов:
  * без --new  — текст ДОПИСЫВАЕТСЯ в конец (перезапись невозможна);
  * с --new    — файл создаётся заново (только для первого блока главы);
  * --block N  — добавляет маркер <!-- block: N --> для отслеживания прогресса;
  * без --text — текст читается из stdin (можно передать через here-string).
"""
import argparse
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

OUT_DIR = Path(__file__).resolve().parent.parent / "output"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True,
                    help="имя файла в output/, напр. v14-ch01.md")
    ap.add_argument("--new", action="store_true",
                    help="создать файл заново (только для первого блока)")
    ap.add_argument("--block", type=int, default=None,
                    help="номер блока (маркер прогресса)")
    ap.add_argument("--text", default=None,
                    help="текст блока; если не задан — читается из stdin")
    args = ap.parse_args()

    OUT_DIR.mkdir(exist_ok=True)
    path = (OUT_DIR / args.file).resolve()
    if OUT_DIR not in path.parents:
        print("ОШИБКА: файл должен лежать внутри output/", file=sys.stderr)
        sys.exit(1)
    if not path.name.endswith(".md"):
        print("ОШИБКА: разрешены только .md файлы", file=sys.stderr)
        sys.exit(1)

    text = args.text if args.text is not None else sys.stdin.read()
    if not text.strip():
        print("ОШИБКА: пустой текст блока", file=sys.stderr)
        sys.exit(1)

    mode = "w" if args.new else "a"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open(mode, encoding="utf-8", newline="\n") as f:
        if args.block is not None:
            f.write("<!-- block: %d -->\n\n" % args.block)
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")

    size = path.stat().st_size
    print("OK: %s | режим=%s | блок=%s | %d символов | файл %d байт" % (
        path.name, mode, args.block, len(text), size))


if __name__ == "__main__":
    main()
