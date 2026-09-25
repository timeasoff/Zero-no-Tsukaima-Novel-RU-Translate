#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
save_block.py — безопасное дозаписывание (append) блока перевода в output/.

Использование:
    # безопасный способ (кириллица НЕ проходит через командную строку):
    python scripts/save_block.py --file v14-ch01.md --new --block 1 --text-file block.txt
    python scripts/save_block.py --file v14-ch01.md --block 2 --text-file block.txt
    # только для ASCII-текста:
    python scripts/save_block.py --file v14-ch01.md --block 2 --text "..."

Агент Agent-IDE вызывает этот скрипт вместо прямой записи файлов:
  * без --new  — текст ДОПИСЫВАЕТСЯ в конец (перезапись невозможна);
  * с --new    — файл создаётся заново (только для первого блока главы);
  * --block N  — добавляет маркер <!-- block: N --> для отслеживания прогресса;
  * --text-file — UTF-8 файл с текстом блока: безопасный канал для не-ASCII
    (командная строка остаётся ASCII, Python читает файл напрямую);
  * без --text/--text-file — текст читается из stdin (предпочтительно из
    Python-драйвера; конвейер через shell для кириллицы ненадёжен).

После записи скрипт проверяет результат (UTF-8, уникальность и порядок
маркеров, наличие текста) и откатывает файл при расхождении.
"""
import argparse
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
if not sys.stdin.isatty():
    try:
        sys.stdin.reconfigure(encoding="utf-8", errors="strict")
    except (AttributeError, ValueError):
        pass

OUT_DIR = Path(__file__).resolve().parent.parent / "output"
EN_DIR = Path(__file__).resolve().parent.parent / "translates" / "en"
REGISTRY = Path(__file__).resolve().parent.parent / "completed.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import completed  # noqa: E402

MARKER_RE = re.compile(r"<!-- block: (\d+) -->")
BLOCK_MARK_RE = re.compile(r"<!--\s*block:\s*\d+\s*-->")


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
                    help="текст блока (только ASCII; для кириллицы — "
                         "--text-file); если не задан — stdin")
    ap.add_argument("--text-file", default=None,
                    help="UTF-8 файл с текстом блока — безопасный канал "
                         "для не-ASCII (по пути читает Python)")
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

    # --- чтение payload: --text-file (безопасно) | --text (ASCII) | stdin ---
    if args.text_file is not None:
        src = Path(args.text_file)
        if not src.exists():
            print("ОШИБКА: файл с текстом не найден: %s" % src, file=sys.stderr)
            sys.exit(1)
        try:
            text = src.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            print("ОШИБКА: %s не декодируется как UTF-8 (%s); файл НЕ "
                  "изменён." % (src, exc), file=sys.stderr)
            sys.exit(1)
        if "\ufffd" in text:
            print("ОШИБКА: в %s признаки порчи кодировки (\\ufffd); файл НЕ "
                  "изменён." % src, file=sys.stderr)
            sys.exit(1)
    elif args.text is not None:
        text = args.text
    else:
        try:
            text = sys.stdin.read()
        except UnicodeDecodeError as exc:
            print("ОШИБКА: stdin не декодируется как UTF-8 (%s); файл НЕ "
                  "изменён. Запишите текст в файл и подавайте через "
                  "--text-file." % exc, file=sys.stderr)
            sys.exit(1)
    if not text.strip():
        print("ОШИБКА: пустой текст блока", file=sys.stderr)
        sys.exit(1)
    if BLOCK_MARK_RE.search(text):
        print("ОШИБКА: текст содержит маркер <!-- block: N --> — скрипт "
              "добавляет маркер сам, возможен дубль; текст НЕ записан.",
              file=sys.stderr)
        sys.exit(1)

    existed = path.exists()
    before_bytes = path.read_bytes() if existed else None
    if existed and not args.new and args.block is not None:
        nums = [int(x) for x in
                MARKER_RE.findall(path.read_text(encoding="utf-8"))]
        if args.block in nums:
            print("ОШИБКА: маркер блока %d уже есть в %s — дубль; текст НЕ "
                  "записан." % (args.block, path.name), file=sys.stderr)
            sys.exit(1)

    mode = "w" if args.new else "a"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open(mode, encoding="utf-8", newline="\n") as f:
        if args.block is not None:
            f.write("<!-- block: %d -->\n\n" % args.block)
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")

    # --- контроль после записи: при расхождении откат к before_bytes ---
    problems = []
    try:
        written = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        problems.append("записанный файл не читается как UTF-8: %s" % exc)
        written = None
    if written is not None:
        if "\ufffd" in written or "\x00" in written:
            problems.append("признаки порчи кодировки (\\ufffd/\\x00)")
        nums = [int(x) for x in MARKER_RE.findall(written)]
        if len(nums) != len(set(nums)) or nums != sorted(nums):
            problems.append("маркеры блоков повреждены (дубли/порядок): %s"
                            % nums)
        if text.strip() not in written:
            problems.append("записанный текст не найден в файле")
    if problems:
        if before_bytes is None:
            try:
                path.unlink()
            except OSError:
                pass
        else:
            path.write_bytes(before_bytes)
        print("ОШИБКА: проверка после записи провалена — файл ОТКАЧЕН "
              "(созданный — удалён):", file=sys.stderr)
        for p in problems:
            print("  - %s" % p, file=sys.stderr)
        sys.exit(1)

    size = path.stat().st_size
    print("OK: %s | режим=%s | блок=%s | %d символов | файл %d байт | "
          "проверка после записи: пройдена"
          % (path.name, mode, args.block, len(text), size))
    position_check(path)


if __name__ == "__main__":
    main()
