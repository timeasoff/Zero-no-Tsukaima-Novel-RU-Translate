#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_block.py — точечная замена текста блока в файле output/ без перезаписи
всего файла. Используется скиллом translation-audit для исправления ошибок,
найденных в уже сохранённых блоках.

Использование (рекомендуемый режим для агента — декларативные замены):
    # правки «было → стало» внутри блока, без ручного payload-файла:
    python scripts/fix_block.py --file v4-ch05.md --block 16 \
        --replace-file fixes_b16.json
    # то же, но только показать план (файл НЕ меняется):
    python scripts/fix_block.py --file v4-ch05.md --block 16 \
        --replace-file fixes_b16.json --dry-run

    # безопасный способ передать весь текст блока (кириллица НЕ проходит
    # через командную строку):
    python scripts/fix_block.py --file v14-ch01.md --block 2 --text-file new_block.txt
    # только для ASCII-текста; аргументы shell с кириллицей искажаются:
    python scripts/fix_block.py --file v14-ch01.md --block 2 --text "new text"

ФОРМАТ --replace-file (UTF-8 JSON; кириллица в файле, командная строка ASCII):

    [["старый фрагмент", "новый фрагмент"],
     {"old": "другой фрагмент", "new": "его замена", "count": 1}]

    или {"replacements": [ ... те же элементы ... ]}

    * "old"  — точная подстрока в текущем блоке (обязательна, непустая);
    * "new"  — замена (строка; пустая допускается только с
               "allow_empty": true — тогда это осознанное удаление);
    * "count" — ожидаемое число вхождений (если задано и не совпало —
                правки НЕ применяются);
    * пустой список замен = перезапись блока без изменений (нормализация
      разделителей и пустой строки перед следующим маркером).

КАНАЛ ПЕРЕДАЧИ ТЕКСТА. Аргумент --text (и конвейер stdin через shell)
с не-ASCII текстом может искажаться на стороне командной оболочки (подмены
букв, порча кодировки). Для больших правок пишите текст в UTF-8 файл и
передавайте скрипту только ПУТЬ (--text-file); для точечных замен —
--replace-file (тогда payload собирает сам скрипт).

После записи скрипт сам проверяет результат (UTF-8, уникальность и порядок
маркеров, совпадение записанного блока с заданным текстом) и при расхождении
откатывает файл к исходному состоянию.
"""
import argparse
import json
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


def brief(text, limit=60):
    """Короткое представление фрагмента для вывода в консоль."""
    flat = text.replace("\n", "\\n")
    return flat if len(flat) <= limit else flat[:limit] + "…"


def load_replacements(path_str):
    """Читает декларативный список замен из UTF-8 JSON.

    Форматы: [[old, new], …] | [{"old":…, "new":…, "count":…}, …] |
    {"replacements": [...]}. Пустой список = перезапись блока без изменений.
    """
    src = Path(path_str)
    if not src.exists():
        fail("файл замен не найден: %s" % src)
    try:
        raw = src.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail("%s не декодируется как UTF-8 (%s); файл НЕ изменён"
             % (src, exc))
    if "\ufffd" in raw:
        fail("в %s найдены признаки порчи кодировки (\\ufffd); "
             "файл НЕ изменён" % src)
    try:
        data = json.loads(raw)
    except ValueError as exc:
        fail("%s не разбирается как JSON (%s); файл НЕ изменён" % (src, exc))
    if isinstance(data, dict):
        data = data.get("replacements")
    if not isinstance(data, list):
        fail('%s: ожидался список замен или {"replacements": [...]}' % src)

    items = []
    for i, entry in enumerate(data, 1):
        if isinstance(entry, (list, tuple)) and len(entry) == 2:
            old, new = entry
            count, allow_empty = None, False
        elif isinstance(entry, dict):
            old, new = entry.get("old"), entry.get("new")
            count = entry.get("count")
            allow_empty = bool(entry.get("allow_empty", False))
        else:
            fail("%s: элемент %d не распознан (нужна пара [old, new] "
                 "или объект)" % (src, i))
        if not isinstance(old, str) or not old.strip():
            fail('%s: элемент %d — пустое/нестроковое поле "old"' % (src, i))
        if not isinstance(new, str):
            fail('%s: элемент %d — поле "new" должно быть строкой' % (src, i))
        if old == new:
            fail('%s: элемент %d — "new" совпадает с "old" (замена без '
                 'изменений)' % (src, i))
        if new == "" and not allow_empty:
            fail('%s: элемент %d — пустая замена запрещена; для осознанного '
                 'удаления добавьте "allow_empty": true' % (src, i))
        if count is not None and (not isinstance(count, int) or count < 0):
            fail('%s: элемент %d — "count" должен быть целым >= 0'
                 % (src, i))
        items.append({"old": old, "new": new, "count": count})
    return items


def find_segment(content, block_no):
    """Границы текста блока: от его маркера до следующего маркера (/конца)."""
    marker = "<!-- block: %d -->" % block_no
    idx = content.find(marker)
    if idx == -1:
        fail("маркер блока %d не найден" % block_no)
    start = idx + len(marker)
    m = re.search(r"<!-- block: \d+ -->", content[start:])
    end = start + m.start() if m else len(content)
    return start, end


def apply_replacements(seg_text, items):
    """Применяет замены к тексту блока; при любой несходимости — отказ.

    Возвращает (новый текст, список строк-отчёта по каждой паре).
    """
    report = []
    new_text = seg_text
    for item in items:
        old, new = item["old"], item["new"]
        found = new_text.count(old)
        if found == 0:
            fail("фрагмент не найден в блоке: «%s» — правки НЕ применены"
                 % brief(old))
        expected = item["count"]
        if expected is not None and found != expected:
            fail("«%s»: найдено %d вхождений, ожидалось %d — "
                 "правки НЕ применены" % (brief(old), found, expected))
        new_text = new_text.replace(old, new)
        report.append("  • «%s» → «%s» (%d×)" % (brief(old), brief(new), found))
    return new_text, report


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
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument("--replace-file", default=None,
                       help="UTF-8 JSON со списком замен [[old, new], …] — "
                            "рекомендуемый режим точечных правок")
    modes.add_argument("--text", default=None,
                       help="новый текст блока целиком (только ASCII; для "
                            "кириллицы используйте --text-file)")
    modes.add_argument("--text-file", default=None,
                       help="UTF-8 файл с новым текстом блока — безопасный "
                            "канал для не-ASCII (путь передаётся вместо текста)")
    ap.add_argument("--dry-run", action="store_true",
                    help="только показать план замен (--replace-file), "
                         "файл НЕ изменять")
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

    if args.replace_file is not None:
        content = path.read_text(encoding="utf-8")
        start, end = find_segment(content, args.block)
        items = load_replacements(args.replace_file)
        text, report = apply_replacements(content[start:end].strip("\n"),
                                          items)
        if not items:
            report = ["  • замен нет: нормализация разделителей блока"]
        if args.dry_run:
            print("DRY-RUN: %s | блок %d | файл НЕ изменён"
                  % (path.name, args.block))
            print("  план правок (%d):" % len(report))
            for line in report:
                print(line)
            return
        print("%s | блок %d | применено пар: %d"
              % (path.name, args.block, len(items)))
        for line in report:
            print(line)
    else:
        if args.dry_run:
            fail("--dry-run поддерживается только вместе с --replace-file")
        text = read_payload(args)
        content = path.read_text(encoding="utf-8")
        start, end = find_segment(content, args.block)

    if not text.strip():
        print("ОШИБКА: пустой текст блока", file=sys.stderr)
        sys.exit(1)
    if BLOCK_MARK_RE.search(text):
        fail("текст блока содержит маркер <!-- block: N --> — так можно "
             "задвоить маркеры; текст НЕ записан")

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
