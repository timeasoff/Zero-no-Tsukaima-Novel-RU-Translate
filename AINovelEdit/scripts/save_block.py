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
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

OUT_DIR = Path(__file__).resolve().parent.parent / "output"
EN_DIR = Path(__file__).resolve().parent.parent / "translates" / "en"

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import check_alignment as ca  # noqa: E402
except Exception:
    ca = None


def paragraphs(path):
    """Абзацы файла (первый блок-заголовок '# ...' — не абзац)."""
    text = path.read_text(encoding="utf-8")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    blocks = [b for b in blocks if not b.startswith("<!-- block:")]
    if blocks and blocks[0].startswith("#"):
        blocks.pop(0)
    return blocks


def position_check(path):
    """Профилактика съезда: сверка результата с исходником.

    Блочный формат (новые тома): сверяются НОМЕРА смысловых блоков —
    блок N output/ обязан существовать в translates/en (блоки выровнены
    при нормализации, абзацных сравнений не требуется).

    Абзацный формат (старые тома): сравнить позиции абзацев результата
    с EN-якорем и предупредить о съезде.
    """
    if ca is None:
        return
    en_path = EN_DIR / path.name
    if not en_path.exists():
        return
    try:
        en_text = en_path.read_text(encoding="utf-8")
        if "<!-- block:" in en_text:
            en_ids = {int(m) for m in
                      re.findall(r"<!--\s*block:\s*(\d+)\s*-->", en_text)}
            out_text = path.read_text(encoding="utf-8")
            out_ids = [int(m) for m in
                       re.findall(r"<!--\s*block:\s*(\d+)\s*-->", out_text)]
            unknown = sorted({n for n in out_ids if n not in en_ids})
            if unknown:
                print(" (!) блоки %s отсутствуют в EN-исходнике — проверь "
                      "номер смыслового блока (блоки выровнены normalize.py)"
                      % unknown)
            return
        en = paragraphs(en_path)
        ed = paragraphs(path)
        if not en or not ed:
            return
        mapping = ca.align(en, ed, ca.load_names())
        off = [(i + 1, row + 1) for i, row in sorted(mapping.items())
               if row != i]
        if len(off) >= 3 and len(off) * 2 >= len(mapping):
            first = off[0]
            print(" (!) позиции: %d абзацев ближе к соседней EN-строке, чем к "
                  "своей (первый: абзац %d → строка %d). Разбиение блока не "
                  "следует EN — поправь блок и прогони "
                  "scripts/check_alignment.py --file %s"
                  % (len(off), first[0], first[1], path.name))
    except Exception as exc:  # профилактика не должна мешать записи
        print(" (!) позиционная сверка не выполнена: %s" % exc, file=sys.stderr)


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
    position_check(path)


if __name__ == "__main__":
    main()
