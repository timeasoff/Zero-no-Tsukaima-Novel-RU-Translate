#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_records.py — контроль оформления прямой речи внутри записи ED_RU.

Правило (russian-prose-rules, «Наррация и реплика в одной записи ED_RU»):
если наррация и реплика попали в один абзац результата (внутри смыслового
блока), реплика начинается с НОВОЙ СТРОКИ внутри записи; слитная запись
«наррация. — Реплика» запрещена.

Скрипт ищет внутри одной визуальной строки конструкции
    <текст, оканчивающийся . ! ? … » > + пробел + «— » + слово с заглавной
и различает:
  * ЛОЖНЫЕ срабатывания (не нарушения):
      - атрибуция ПОСЛЕ реплики: «— Реплика, — сказал он» / «— Реплика! — Жозеф
        расхохотался» (перед тире — реплика, а не наррация);
      - вводящие слова автора с двоеточием: «…проговорил: — Реплика»;
      - продолжение реплики после авторских слов: «… — …Второе предложение».
  * КАНДИДАТЫ (требуют проверки): наррация. — Реплика / две реплики в строке.

Обнаружение ≠ правка: кандидат разбирается по JA/EN (скилл russian-prose-rules),
при подтверждении — fix_block.py с переносом строки перед тире.

Использование:
    python scripts/check_records.py                 # все главы output/
    python scripts/check_records.py --file v14-ch08.md
    python scripts/check_records.py --strict        # код 1 при кандидатах
"""
import argparse
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

OUT = Path(__file__).resolve().parent.parent / "output"

# «. — Слово» / «? — Слово» / «… — Слово» / «» — Слово» внутри строки
PAT = re.compile(r"([.!?…»])([ \t]+)—([ \t]+)([А-ЯЁA-Z][а-яёa-z\-]+)")

# глаголы речи/мысли/жеста: если в ближайших словах после тире есть такой
# глагол, скорее всего это атрибуция после реплики — не нарушение
ATTR = re.compile(r"^(?:сказал|сказала|проговорил|проговорила|пробормотал|"
                  r"пробормотала|промолвил|произнёс|произнесла|спросил|"
                  r"спросила|ответил|ответила|воскликнул|воскликнула|крикнул|"
                  r"крикнула|вскричал|шепнул|прошептал|отозвался|отозвалась|"
                  r"добавил|добавила|продолжил|продолжила|заметил|заметила|"
                  r"повторил|повторила|возразил|возразила|усмехнулся|"
                  r"усмехнулась|улыбнулся|улыбнулась|вздохнул|вздохнула|"
                  r"кивнул|кивнула|подумал|подумала|буркнул|буркнула|рявкнул|"
                  r"гаркнул|протянул|протянула|пропел|фыркнул|хмыкнул|"
                  r"расхохотался|расхохоталась|опечалился|опечалилась|"
                  r"рванулся|рванулась|развёл|развела|достал|достала|"
                  r"побледнел|побледнела|стиснул|стиснула|стукнул|стукнула|"
                  r"покачал|покачала|замер|замерла|встал|встала|сел|села|"
                  r"уселся|уселась|придвинулся|придвинулась|отвернулся|"
                  r"отвернулась|обернулся|обернулась|посмотрел|посмотрела|"
                  r"взглянул|взглянула|уставился|уставилась|помрачнел|"
                  r"помрачнела|ухмыльнулся|ухмыльнулась|заулыбался|заулыбалась|"
                  r"охнул|охнула|вздрогнул|вздрогнула|спустился|спустилась|"
                  r"поднялся|поднялась|опустился|опустилась|взял|взяла|"
                  r"вспомнив|сказав|услышав|улыбнувшись|усмехнувшись|глядя|"
                  r"обернувшись|кивнув|вздохнув|помолчав|подумав|сжав|"
                  r"подняв|опустив|распахнув|приподняв|заглянув)", re.I)

WORD = re.compile(r"[А-Яа-яЁёA-Za-z][А-Яа-яЁёA-Za-z'’\-]*")


def paragraphs(path):
    text = path.read_text(encoding="utf-8")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    return [b for b in blocks if not b.startswith("<!-- block:")]


def check(path):
    """Возвращает список (абзац, строка, фрагмент) для кандидатов."""
    found = []
    for i, p in enumerate(paragraphs(path), start=1):
        if p.startswith("#"):
            continue
        for li, line in enumerate(p.split("\n"), start=1):
            for m in PAT.finditer(line):
                # окно из 4 слов после тире: глагол речи/жеста → атрибуция
                tail = WORD.findall(line[m.end(3):])[:4]
                if any(ATTR.match(w) for w in tail):
                    continue          # атрибуция после реплики — норма
                found.append((i, li, line[max(0, m.start() - 45):m.end() + 20]))
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", help="напр. v14-ch08.md (иначе — все главы)")
    ap.add_argument("--strict", action="store_true",
                    help="вернуть код 1, если есть кандидаты")
    args = ap.parse_args()

    files = ([OUT / args.file] if args.file
             else sorted(OUT.glob("v14-*.md")))
    total = 0
    for path in files:
        if not path.exists():
            print("ОШИБКА: файл не найден: %s" % path, file=sys.stderr)
            return 1
        found = check(path)
        if found:
            print("[%s] кандидатов: %d" % (path.name, len(found)))
            for i, li, frag in found:
                print("   абз. %d, стр. %d: …%s…" % (i, li, frag))
        total += len(found)
    print("\nИтого кандидатов: %d (обнаружение ≠ правка: разбор по JA/EN)"
          % total)
    return 1 if (args.strict and total) else 0


if __name__ == "__main__":
    sys.exit(main())
