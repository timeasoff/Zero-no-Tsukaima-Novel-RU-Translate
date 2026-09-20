#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_alignment.py — механическая сверка merged по СМЫСЛОВЫМ БЛОКАМ
(JA / EN / RU / ED_RU).

Единица — смысловой блок (`## Блок N`). Блоки JA/EN/RU/ED_RU уже выровнены
при нормализации (`tools/normalize.py`), поэтому «съезд» строк здесь
невозможен по построению: блок N — одна и та же микросцена во всех колонках.

Сигналы (по блоку) — структурные подозрения ВНУТРИ блока:
  no-translation — ED_RU не заполнен («—»).
  speech         — наличие реплик расходится: EN и ED_RU.
  marks          — расхождение знаков «?» / «!» с EN.
  negation       — расхождение отрицания (EN not/no/never ↔ RU не/ни/без/нет).
  numbers        — числа EN не подтверждаются в ED_RU (цифрой или словом).
  names          — имена из dictionary.md: есть в EN и нет в ED_RU (или наоборот).

Обнаружение ≠ вердикт: сигнал разбирается по скиллу translation-audit.
Расхождения терминов с завершёнными томами фиксируются там же
(см. AINovelEdit/completed.md).

Использование:
    python scripts/check_alignment.py --file v15-ch04.md
    python scripts/check_alignment.py --file v15-ch04.md --report
    python scripts/check_alignment.py --all
    python scripts/check_alignment.py --file v15-ch04.md --strict
"""
import argparse
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import merged_io  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
MERGED = BASE / "translates" / "_report" / "merged"
AUDIT = BASE / "output" / "_audit" / "_prefilter"
DICT = BASE / "dictionary.md"
EN_NEG_RE = re.compile(r"\b(?:not|no|never|none|nothing|without|n't|nor)\b", re.I)
RU_NEG_RE = re.compile(r"\b(?:не|ни|нет|без|никогда|ничего|никто)\b", re.I)
WORD_RE = re.compile(r"[А-Яа-яЁёA-Za-z][А-Яа-яЁёA-Za-z'’\-]+", re.U)

# числительные 1–10 по корню (проект: однозначные — словами)
RU_NUM = {
    1: ("один", "одн", "перв"), 2: ("два", "две", "двух", "втор"),
    3: ("три", "трёх", "трех", "трет"), 4: ("четыр", "четвёрт", "четверт"),
    5: ("пят", "пяти"), 6: ("шест", "шест"), 7: ("сем", "седьм"),
    8: ("восем", "восьм"), 9: ("девят", "девят"), 10: ("десят", "десят"),
}
# частые EN-слова из словарных колонок: дают ложные «имена» (Ancient magic,
# Order of …, Academy …) — как признаки имени не используются
EN_NAME_STOP = {
    "ancient", "magic", "magical", "order", "holy", "water", "spirit",
    "spirits", "knights", "knight", "academy", "church", "sword", "swords",
    "saint", "spell", "spells", "flame", "lily", "rose", "cross", "wand",
    "wands", "people", "guard", "guards", "crown", "royal", "lady", "lord",
}


def load_names():
    """Пары EN → RU из dictionary.md: (набор EN-форм, RU-основа, RU-канон).

    Берутся только слова EN-колонки с заглавной буквы (имена и названия);
    общие слова — по стоп-листу. Так «Ancient magic» не срабатывает на
    любое слово magic в тексте.
    """
    if not DICT.exists():
        return []
    pairs = []
    for line in DICT.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        en, ru = cells[1], cells[2]
        if en.startswith("---") or ru.startswith("---"):
            continue
        en_forms = {w.lower() for w in re.findall(r"\b[A-Z][A-Za-z'\-]{4,}", en)
                    if w.lower() not in EN_NAME_STOP}
        ru_words = re.findall(r"[А-Яа-яЁё]+", ru)
        ru_base = ru_words[0].lower().replace("ё", "е")[:4] if ru_words else ""
        if en_forms and len(ru_base) == 4 and len(ru_words[0]) >= 4:
            pairs.append((en_forms, ru_base, ru))
    return pairs


NUM_GROUP_RE = re.compile(r"(?<=\d)[,\u00a0 ](?=\d{3}\b)")
ANY_DIGITS_RE = re.compile(r"\d+")


def norm_numbers(s):
    """«10,000» / «9 000» → «10000» / «9000» (разрядные группы)."""
    return NUM_GROUP_RE.sub("", s)


def numbers_in(text):
    return {int(x) for x in ANY_DIGITS_RE.findall(norm_numbers(text))}


def number_confirmed(num, ru_text):
    low = ru_text.lower().replace("ё", "е")
    if num in numbers_in(ru_text):
        return True
    if any(r in low for r in RU_NUM.get(num, ())):
        return True
    # крупные числа проекта пишутся словами: «десять тысяч», «семьдесят тысяч»
    if num >= 10:
        if num % 1000 == 0 and "тысяч" in low:
            return True
        if num % 100 == 0 and ("сот" in low or "сто" in low):
            return True
        if num % 1000000 == 0 and "миллион" in low:
            return True
    return False


def names_in(text, pairs, side):
    found = set()
    if side == "en":
        # «Aquileia's» → «aquileia»: притяжательный апостроф не должен мешать
        words = {w.split("'")[0].split("’")[0].lower()
                 for w in re.findall(r"[A-Za-z][A-Za-z'’\-]+", text)}
        for en_forms, ru_base, ru in pairs:
            if en_forms & words:
                found.add(ru)
    else:
        tokens = [re.sub(r"[^а-яё]", "", w.lower().replace("ё", "е"))
                  for w in re.findall(r"[А-Яа-яЁё][А-Яа-яЁё\-]+", text)]
        for en_forms, ru_base, ru in pairs:
            if any(t.startswith(ru_base) for t in tokens):
                found.add(ru)
    return found
def check(path, pairs):
    """Сверка merged по смысловым блокам → (сигналы, статистика).

    Блоки JA/EN/RU/ED_RU выровнены при нормализации, поэтому проверка
    «съезда» не нужна: сигналы фиксируют расхождения внутри блока.
    """
    items = merged_io.read_merged(path)
    en_list = [merged_io.clean(f.get("EN", "")) for _, f in items]
    ed_list = [merged_io.clean(f.get("ED_RU", "")) for _, f in items]
    signals = []
    stats = {"blocks": len(items), "translated": 0, "strong": 0, "weak": 0,
             "info": 0, "kinds": {}}

    def add(num, kind, weight, detail, en="", ed=""):
        signals.append({"para": num, "kind": kind, "weight": weight,
                        "detail": detail, "en": en, "ed": ed})
        stats[weight] += 1
        stats["kinds"][kind] = stats["kinds"].get(kind, 0) + 1

    for idx, (num, _fields) in enumerate(items):
        en, ed = en_list[idx], ed_list[idx]
        if not ed or ed == "—":
            add(num, "no-translation", "info", "ED_RU не заполнен")
            continue
        stats["translated"] += 1

        en_sp = '"' in en
        ed_sp = ("—" in ed) or ("«" in ed)
        if en_sp != ed_sp:
            add(num, "speech", "weak",
                "наличие реплик: EN — %s, ED_RU — %s" % (
                    "есть" if en_sp else "нет", "есть" if ed_sp else "нет"),
                en, ed)

        if ("?" in en) != ("?" in ed):
            add(num, "marks", "weak",
                "вопросительный знак: EN и ED_RU расходятся", en, ed)

        if bool(EN_NEG_RE.search(en)) != bool(RU_NEG_RE.search(ed)):
            add(num, "negation", "weak",
                "отрицание: EN и ED_RU расходятся", en, ed)

        en_n, ed_n = numbers_in(en), numbers_in(ed)
        missing = {n for n in en_n if not number_confirmed(n, ed)}
        if missing:
            add(num, "numbers", "weak",
                "числа EN не подтверждены в ED_RU: %s"
                % ", ".join(str(n) for n in sorted(missing)), en, ed)

        en_names = names_in(en, pairs, "en")
        ed_names = names_in(ed, pairs, "ru")
        lost = en_names - ed_names
        if lost:
            add(num, "names", "weak",
                "имена словаря: есть в EN, нет в ED_RU: %s"
                % ", ".join(sorted(lost)), en, ed)
        extra = ed_names - en_names
        if extra:
            add(num, "names", "info",
                "имена словаря: есть в ED_RU, нет в EN (проверить): %s"
                % ", ".join(sorted(extra)), en, ed)

    signals.sort(key=lambda s: (s["para"], s["kind"]))
    return signals, stats


def one_line(text, limit=160):
    """Текст поля одной строкой для отчёта."""
    s = " / ".join(t.strip() for t in text.splitlines() if t.strip())
    return s if len(s) <= limit else s[:limit] + "…"


def render(name, signals, stats):
    kinds = stats.get("kinds", {})
    lines = ["# Выгрузка предфильтра (сверка смысловых блоков): %s" % name, ""]
    lines.append("Блоков %d, переведено %d. Сигналов: строгих %d, прочих %d, "
                 "инфо %d." % (stats["blocks"], stats["translated"],
                               stats["strong"], stats["weak"], stats["info"]))
    if kinds:
        lines.append("")
        lines.append("По типам: " + ", ".join(
            "%s %d" % (k, kinds[k]) for k in sorted(kinds)))
    lines += ["",
              "Единица — смысловой блок: блоки JA/EN/RU/ED_RU выровнены при "
              "нормализации, «съезда» нет. Сигнал — обнаружение, не вердикт: "
              "разбор по скиллу translation-audit.", ""]
    if signals:
        lines += ["## Сигналы", ""]
        for s in signals:
            lines.append("### Блок %d — %s (%s)" % (
                s["para"], s["kind"], s["weight"]))
            lines.append("")
            lines.append("- %s" % s["detail"])
            if s["en"]:
                lines.append("- **EN:** %s" % one_line(s["en"]))
            if s["ed"]:
                lines.append("- **ED_RU:** %s" % one_line(s["ed"]))
            lines.append("")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=None, help="напр. v15-ch04.md")
    ap.add_argument("--all", action="store_true",
                    help="проверить все главы тома (по merged)")
    ap.add_argument("--report", action="store_true",
                    help="записать выгрузку в "
                         "output/_audit/_prefilter/<глава>-alignment.md")
    ap.add_argument("--strict", action="store_true",
                    help="вернуть код 1, если есть строгие сигналы")
    args = ap.parse_args()

    if not args.file and not args.all:
        ap.error("укажи --file vXX-chYY.md либо --all")

    names = ([args.file] if args.file
             else sorted(p.name for p in MERGED.glob("v*.md")))
    pairs = load_names()
    total_strong = 0

    for name in names:
        path = MERGED / name
        if not path.exists():
            print("ОШИБКА: нет merged-файла %s — прогони "
                  "scripts/update_merged.py" % path, file=sys.stderr)
            sys.exit(2)
        signals, stats = check(path, pairs)
        if not stats["translated"]:
            print("OK: %s | ED_RU пуст — проверять нечего" % name)
            continue
        total_strong += stats["strong"]
        report = render(name, signals, stats)
        if args.report:
            AUDIT.mkdir(parents=True, exist_ok=True)
            dst = AUDIT / ("%s-alignment.md" % Path(name).stem)
            dst.write_text(report, encoding="utf-8", newline="\n")
            print("OK: выгрузка → output/_audit/_prefilter/%s | строгих %d, "
                  "прочих %d, инфо %d" % (dst.name, stats["strong"],
                                          stats["weak"], stats["info"]))
        else:
            sys.stdout.write(report)

    if args.strict and total_strong:
        sys.exit(1)


if __name__ == "__main__":
    main()
