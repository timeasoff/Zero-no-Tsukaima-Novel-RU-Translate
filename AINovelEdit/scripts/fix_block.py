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
import os
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
REGISTRY = Path(__file__).resolve().parent.parent / "completed.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import completed  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="имя файла в output/")
    ap.add_argument("--block", type=int, required=True, help="номер блока")
    ap.add_argument("--text", default=None, help="новый текст блока; иначе stdin")
    args = ap.parse_args()

    path = (OUT_DIR / args.file).resolve()

    vol = completed.volume_of(path.name)
    if completed.is_frozen(vol, REGISTRY):
        print("ОШИБКА: том %s завершён и заморожен (completed.md) — "
              "редактировать его текст запрещено." % vol, file=sys.stderr)
        sys.exit(1)

    if path.parent != OUT_DIR or not path.exists():
        print("ОШИБКА: файл не найден в output/", file=sys.stderr)
        sys.exit(1)

    text = args.text
    if text is None:
        try:
            text = sys.stdin.read()
        except UnicodeDecodeError as exc:
            print("ОШИБКА: stdin не декодируется как UTF-8 (%s); файл НЕ "
                  "изменён. Запишите текст в файл и подавайте его через "
                  "перенаправление при PYTHONUTF8=1." % exc, file=sys.stderr)
            sys.exit(1)
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
    new_content = content[:start] + seg + content[end:]

    # Защита от инцидента с обнулённым файлом: сначала полностью готовим и
    # кодируем новый контекст во временный файл, только затем атомарно
    # подменяем оригинал. Если кодировка сломана (мусор из конвейера,
    # суррогаты) — выходим с ошибкой, НЕ трогая исходный файл.
    try:
        payload = new_content.encode("utf-8")
    except UnicodeEncodeError as exc:
        print("ОШИБКА: новый текст блока содержит не-UTF-8 мусора (%s); "
              "файл НЕ изменён. Скорее всего, текст пришёл по конвейеру в "
              "неправильной кодировке — запишите текст в файл и подайте его "
              "через stdin с PYTHONUTF8=1." % exc, file=sys.stderr)
        sys.exit(1)
    if "\x00" in new_content or "\ufffd" in new_content:
        print("ОШИБКА: в новом тексте блока найдены знаки подстановки/нуля; "
              "файл НЕ изменён (вероятно, порча кодировки при передаче).",
              file=sys.stderr)
        sys.exit(1)

    tmp_path = path.with_name(path.name + ".tmp")
    tmp_path.write_bytes(payload)
    os.replace(tmp_path, path)
    print("OK: %s | блок %d заменён | файл %d байт" % (
        path.name, args.block, path.stat().st_size))


if __name__ == "__main__":
    main()
