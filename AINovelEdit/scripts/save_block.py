#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
save_block.py — безопасное дозаписывание (append) блока перевода в output/.

Использование:
    python scripts/save_block.py --file v14-ch01.md --new --block 1 --text "..."
    python scripts/save_block.py --file v14-ch01.md --block 2 --text "..."

Агент Agent-IDE вызывает этот скрипт вместо прямой записи файлов:
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
REGISTRY = Path(__file__).resolve().parent.parent / "completed.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import completed  # noqa: E402


def position_check(path):
    """Сверка результата с исходником по смысловым блокам.

    Проверяет, что каждый номер блока в `output/` существует в
    `translates/en/<глава>` (блоки выровнены при нормализации), — то есть
    агент не создал «лишний» блок и не сдвинул нумерацию.
    """
    en_path = EN_DIR / path.name
    if not en_path.exists():
        return
    try:
        en_text = en_path.read_text(encoding="utf-8")
        if "<!-- block:" not in en_text:
            print(" (!) %s: нет маркеров смысловых блоков — том не "
                  "нормализован текущим tools/normalize.py" % path.name,
                  file=sys.stderr)
            return
        en_ids = {int(m) for m in
                  re.findall(r"<!--\s*block:\s*(\d+)\s*-->", en_text)}
        out_text = path.read_text(encoding="utf-8")
        out_ids = [int(m) for m in
                   re.findall(r"<!--\s*block:\s*(\d+)\s*-->", out_text)]
        unknown = sorted({n for n in out_ids if n not in en_ids})
        if unknown:
            print(" (!) блоки %s отсутствуют в EN-исходнике — проверь номер "
                  "смыслового блока (нумерация выровнена normalize.py)"
                  % unknown)
        n_en, n_out = len(en_ids), len(set(out_ids))
        if n_out > n_en:
            print(" (!) в результате %d блоков, в EN-исходнике %d — лишние "
                  "блоки/номер пропущен" % (n_out, n_en))
    except Exception as exc:  # профилактика не должна мешать записи
        print(" (!) блочная сверка не выполнена: %s" % exc, file=sys.stderr)


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

    vol = completed.volume_of(path.name)
    if completed.is_frozen(vol, REGISTRY):
        print("ОШИБКА: том %s завершён и заморожен (completed.md) — "
              "редактировать его текст запрещено. Правки терминов вносятся "
              "в dictionary.md вручную." % vol, file=sys.stderr)
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
