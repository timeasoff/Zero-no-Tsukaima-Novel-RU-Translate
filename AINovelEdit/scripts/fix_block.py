#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_block.py — точечная замена текста блока в файле output/ без перезаписи
всего файла. Используется скиллом translation-audit для исправления ошибок,
найденных в уже сохранённых блоках.

Использование:
    # безопасный способ (кириллица НЕ проходит через командную строку):
    python scripts/fix_block.py --file v14-ch01.md --block 2 --text-file new_block.txt
    # только для ASCII-текста; аргументы shell с кириллицей искажаются:
    python scripts/fix_block.py --file v14-ch01.md --block 2 --text "new text"

КАНАЛ ПЕРЕДАЧИ ТЕКСТА. Аргумент --text (и конвейер stdin через shell)
с не-ASCII текстом может искажаться на стороне командной оболочки (подмены
букв, порча кодировки). Пишите текст правки в UTF-8 файл инструментом
редактирования и передавайте скрипту только ПУТЬ (--text-file): Python
читает файл напрямую, командная строка остаётся ASCII.

После записи скрипт сам проверяет результат (UTF-8, уникальность и порядок
маркеров, совпадение записанного блока с заданным текстом) и при расхождении
откатывает файл к исходному состоянию.
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

MARKER_RE = re.compile(r"<!-- block: (\d+) -->")
BLOCK_MARK_RE = re.compile(r"<!--\s*block:\s*\d+\s*-->")


def fail(msg):
    print("ОШИБКА: %s" % msg, file=sys.stderr)
    sys.exit(1)


def read_payload(args):
    """Текст блока: --text-file (безопасно) | --text (ASCII) | stdin."""
    if args.text_file is not None:
        src = Path(args.text_file)
        if not src.exists():
            fail("файл с текстом не найден: %s" % src)
        try:
            text = src.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            fail("%s не декодируется как UTF-8 (%s); файл НЕ изменён"
                 % (src, exc))
        if "\ufffd" in text:
            fail("в %s найдены признаки порчи кодировки (\\ufffd); "
                 "файл НЕ изменён" % src)
        return text
    if args.text is not None:
        return args.text
    try:
        return sys.stdin.read()
    except UnicodeDecodeError as exc:
        print("ОШИБКА: stdin не декодируется как UTF-8 (%s); файл НЕ "
              "изменён. Запишите текст в файл и подавайте через "
              "--text-file." % exc, file=sys.stderr)
        sys.exit(1)


def verify_written(path, before_bytes, expected_text, block_no):
    """Контроль после записи: при расхождении — откат к before_bytes."""
    problems = []
    try:
        written = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        problems.append("записанный файл не читается как UTF-8: %s" % exc)
        written = None
    if written is not None:
        if "\ufffd" in written or "\x00" in written:
            problems.append("в записи найдены признаки порчи (\\ufffd/\\x00)")
        nums = [int(x) for x in MARKER_RE.findall(written)]
        if len(nums) != len(set(nums)) or nums != sorted(nums):
            problems.append("маркеры блоков повреждены (дубли/порядок): %s"
                            % nums)
        marker = "<!-- block: %d -->" % block_no
        idx = written.find(marker)
        if idx == -1:
            problems.append("маркер блока %d пропал" % block_no)
        else:
            start = idx + len(marker)
            m = re.search(r"<!-- block: \d+ -->", written[start:])
            end = start + m.start() if m else len(written)
            if written[start:end].strip("\n") != expected_text.strip("\n"):
                problems.append("записанный блок %d не совпал с заданным "
                                "текстом" % block_no)
    if problems:
        path.write_bytes(before_bytes)
        print("ОШИБКА: проверка после записи провалена — файл ОТКАЧЕН "
              "к исходному состоянию:", file=sys.stderr)
        for p in problems:
            print("  - %s" % p, file=sys.stderr)
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="имя файла в output/")
    ap.add_argument("--block", type=int, required=True, help="номер блока")
    ap.add_argument("--text", default=None,
                    help="новый текст блока (только ASCII; для кириллицы "
                         "используйте --text-file)")
    ap.add_argument("--text-file", default=None,
                    help="UTF-8 файл с новым текстом блока — безопасный "
                         "канал для не-ASCII (путь передаётся вместо текста)")
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

    text = read_payload(args)
    if not text.strip():
        print("ОШИБКА: пустой текст блока", file=sys.stderr)
        sys.exit(1)
    if BLOCK_MARK_RE.search(text):
        fail("текст блока содержит маркер <!-- block: N --> — так можно "
             "задвоить маркеры; текст НЕ записан")

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
              "неправильной кодировке — запишите текст в файл и подайте "
              "через --text-file." % exc, file=sys.stderr)
        sys.exit(1)
    if "\x00" in new_content or "\ufffd" in new_content:
        print("ОШИБКА: в новом тексте блока найдены знаки подстановки/нуля; "
              "файл НЕ изменён (вероятно, порча кодировки при передаче).",
              file=sys.stderr)
        sys.exit(1)

    before_bytes = path.read_bytes()
    tmp_path = path.with_name(path.name + ".tmp")
    tmp_path.write_bytes(payload)
    os.replace(tmp_path, path)
    verify_written(path, before_bytes, text, args.block)
    print("OK: %s | блок %d заменён | файл %d байт | проверка после записи: "
          "пройдена" % (path.name, args.block, path.stat().st_size))


if __name__ == "__main__":
    main()
