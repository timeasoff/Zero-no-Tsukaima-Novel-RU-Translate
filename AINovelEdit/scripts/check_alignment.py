#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_alignment.py — механическая проверка соответствия строк в merged
(JA / EN / RU / ED_RU). Ищет «съезд»: случай, когда ED_RU написан не на ту
строку, на которую указывает EN-якорь (перевод сдвинут на соседний абзац).

Эталон соответствия — EN: разбиение абзацев проекта следует EN-файлу
(JA выравнивается приблизительно и может быть сдвинут на ±1–2 абзаца —
такие случаи помечаются отдельно как `ja-shift`, это известное свойство
нормализации, а не ошибка текста).

Сигналы (по абзацу):
  no-translation — ED_RU пуст («—»): строка ещё не отредактирована.
  count          — число абзацев ED_RU не равно EN.
  speech         — EN-реплика (начинается с кавычки), а ED_RU не реплика
                   (или наоборот): сильный признак съезда.
  marks          — расхождение знаков «?» / «!» с EN.
  negation       — расхождение отрицания (EN not/no/never ↔ RU не/ни/без/нет).
  numbers        — числа EN не подтверждаются в ED_RU (цифрой или словом).
  names          — имена из dictionary.md: есть в EN и нет в ED_RU (или наоборот).
  shift          — ED_RU ближе по признакам к соседнему EN-абзацу (i±1),
                   чем к своему: кандидат «перевод уехал на строку i±1».
  ja-shift       — JA-абзац расходится с ED_RU по типу (реплика/наррация),
                   при том что ED_RU с EN согласован: сдвиг выравнивания JA.

Использование:
    python scripts/check_alignment.py --file v14-ch04.md
    python scripts/check_alignment.py --file v14-ch04.md --report
    python scripts/check_alignment.py --all
    python scripts/check_alignment.py --file v14-ch04.md --strict
"""
import argparse
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent
MERGED = BASE / "translates" / "_report" / "merged"
AUDIT = BASE / "output" / "_audit" / "_prefilter"
DICT = BASE / "dictionary.md"

PARA_RE = re.compile(r"^##\s*Абзац\s+(\d+)\s*$", re.M)
FIELD_RE = re.compile(r"^\*\*(JA|EN|RU|ED_RU):\*\*\s*(.*)$", re.M)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
EN_OPEN_QUOTE_RE = re.compile(r'^[\s"]*"')
RU_SPEECH_RE = re.compile(r"^\s*(?:<!--.*?-->\s*)*—")
DIGIT_RE = re.compile(r"(?<![\d,.\-–—])\d[\d\s]*")
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


def is_speech_en(en):
    return bool(EN_OPEN_QUOTE_RE.match(en))


def is_speech_ru(ru):
    return bool(RU_SPEECH_RE.match(ru))


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


def score(en, ed, pairs):
    """Совпадение ED_RU с EN-абзацем: признаки + имена + числа."""
    s = 0
    s += 3 if is_speech_en(en) == is_speech_ru(ed) else -3
    s += 1 if ("?" in en) == ("?" in ed) else -1
    s += 1 if ("!" in en) == ("!" in ed) else -1
    s += 1 if bool(EN_NEG_RE.search(en)) == bool(RU_NEG_RE.search(ed)) else -1
    en_n, ed_n = numbers_in(en), numbers_in(ed)
    if en_n or ed_n:
        s += 2 if en_n == ed_n else -2
    en_names = names_in(en, pairs, "en")
    ed_names = names_in(ed, pairs, "ru")
    s += 3 * len(en_names & ed_names)
    s -= 3 * len(en_names ^ ed_names)
    return s, en_n, ed_n, en_names, ed_names


def read_paras(path):
    text = path.read_text(encoding="utf-8")
    marks = list(PARA_RE.finditer(text))
    items = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        fields = {k: v.strip() for k, v in FIELD_RE.findall(text[m.end():end])}
        items.append((int(m.group(1)), fields))
    return items


def clean(s):
    return HTML_COMMENT_RE.sub(" ", s).strip()


def check(path, pairs):
    """Возвращает (сигналы, статистику)."""
    items = read_paras(path)
    en_list = [clean(f.get("EN", "")) for _, f in items]
    ed_list = [clean(f.get("ED_RU", "")) for _, f in items]
    ja_list = [clean(f.get("JA", "")) for _, f in items]
    signals = []
    stats = {"paragraphs": len(items), "translated": 0, "strong": 0, "weak": 0,
             "info": 0, "ja_shift": 0, "near_miss": 0, "kinds": {}}

    for idx, (num, _f) in enumerate(items):
        en, ed, ja = en_list[idx], ed_list[idx], ja_list[idx]
        if not ed or ed == "—":
            continue
        stats["translated"] += 1
        if not en or en == "—":
            continue

        s_own, en_n, ed_n, en_names, ed_names = score(en, ed, pairs)
        kind, detail, weight = None, "", "weak"
        if is_speech_en(en) != is_speech_ru(ed):
            kind, weight = "speech", "strong"
            detail = "EN — %s, ED_RU — %s" % (
                "реплика" if is_speech_en(en) else "наррация",
                "реплика" if is_speech_ru(ed) else "наррация")
        elif ("?" in en) != ("?" in ed):
            kind = "marks"
            detail = "вопрос «?» только в %s" % ("EN" if "?" in en else "ED_RU")
        elif RU_NEG_RE.search(ed) and not EN_NEG_RE.search(en):
            kind = "negation"
            detail = "лишнее отрицание в ED_RU (в EN его нет)"
        elif EN_NEG_RE.search(en) and not RU_NEG_RE.search(ed):
            kind = "negation"
            weight = "info"
            detail = "отрицание EN не передано явно (часто норма при идиоме)"
        else:
            missing = [n for n in sorted(en_n) if not number_confirmed(n, ed)]
            only_en = sorted(en_names - ed_names)
            # имя «только в ED_RU» — сигнал съезда лишь если оно есть в EN
            # соседних абзацев (±2), иначе это JA-момент, а не смещение
            near_names = set()
            for step in (-2, -1, 1, 2):
                j = idx + step
                if 0 <= j < len(items):
                    near_names |= names_in(en_list[j], pairs, "en")
            only_ru = sorted((ed_names - en_names) & near_names)
            if missing:
                kind, detail = "numbers", "числа EN не подтверждены: %s" % missing
            elif only_en or only_ru:
                kind = "names"
                detail = "; ".join(x for x in [
                    "есть в EN, нет в ED_RU: %s" % ", ".join(only_en) if only_en else "",
                    "есть в ED_RU, нет в EN: %s" % ", ".join(only_ru) if only_ru else ""] if x)

        if kind:
            stats[weight] += 1
            stats.setdefault("kinds", {})
            stats["kinds"][kind] = stats["kinds"].get(kind, 0) + 1
            signals.append({"para": num, "kind": kind, "weight": weight,
                            "detail": detail, "en": en, "ed": ed,
                            "score": s_own})

        # съезд: ED_RU ближе к соседнему EN-абзацу, чем к своему
        near = []
        for step in (-1, 1):
            j = idx + step
            if 0 <= j < len(items):
                s_near, *_ = score(en_list[j], ed, pairs)
                if s_near >= 5 and s_near > s_own + 2:
                    near.append((step, s_near))
        if near:
            step, s_near = max(near, key=lambda x: x[1])
            stats["near_miss"] += 1
            signals.append({
                "para": num, "kind": "shift", "weight": "strong",
                "detail": "ED_RU ближе к EN %+d (score %d против %d у своей строки)"
                          % (step, s_near, s_own),
                "en": en_list[idx + step], "ed": ed, "score": s_near})

        # JA-сдвиг: с EN согласовано, но JA-абзац другого типа
        if (ja and ja != "—" and not kind
                and is_speech_ru(ed) != is_speech_en(ja)):
            stats["ja_shift"] += 1
            signals.append({
                "para": num, "kind": "ja-shift", "weight": "info",
                "detail": "JA (%s) и ED_RU (%s) разного типа — сдвиг выравнивания "
                          "JA (эталон — EN)" % (
                              "реплика" if is_speech_en(ja) else "наррация",
                              "реплика" if is_speech_ru(ed) else "наррация"),
                "en": en, "ed": ed, "score": s_own})

    return signals, stats


def render(name, signals, stats, proposal=None):
    lines = ["# Выгрузка предфильтра (соответствие строк merged): %s" % name, ""]
    lines.append("Абзацев %d, переведено %d. Сигналов: строгих %d, прочих %d, "
                 "инфо %d, «съезд» %d, JA-сдвигов %d." % (
                     stats["paragraphs"], stats["translated"], stats["strong"],
                     stats["weak"], stats["info"], stats["near_miss"],
                     stats["ja_shift"]))
    kinds = stats.get("kinds", {})
    if kinds:
        lines.append("")
        lines.append("По типам: " + ", ".join(
            "%s %d" % (k, kinds[k]) for k in sorted(kinds)))
    lines += ["", "Эталон соответствия — EN. `ja-shift` — не ошибка текста: "
                  "JA выровнен приблизительно (±1–2 абзаца).", ""]

    strong = [s for s in signals if s["weight"] == "strong"]
    weak = [s for s in signals if s["weight"] == "weak"]
    info = [s for s in signals if s["weight"] == "info"]

    def dump(title, group):
        if not group:
            return
        lines.append("## %s" % title)
        lines.append("")
        for s in group:
            lines.append("### Абзац %d — %s" % (s["para"], s["kind"]))
            lines.append("")
            lines.append("- %s" % s["detail"])
            en = s["en"] if len(s["en"]) <= 300 else s["en"][:300] + "…"
            ed = s["ed"] if len(s["ed"]) <= 300 else s["ed"][:300] + "…"
            lines.append("- **EN (эталон):** %s" % en)
            lines.append("- **ED_RU:** %s" % ed)
            lines.append("")

    dump("Строгие сигналы (проверить обязательно)", strong)
    dump("Слабые сигналы (проверить по смыслу)", weak)
    dump("JA-сдвиги (известное свойство выравнивания)", info)

    if proposal:
        moves = [p for p in proposal if p[1] != p[2]]
        if moves:
            lines.append("## Предложение по пересадке (DP-выравнивание)")
            lines.append("")
            lines.append("Куда, по признакам, должен лечь каждый съехавший "
                         "ED_RU-абзац. Это ПЛАН, а не правка: первые строки "
                         "зоны проверить глазами, применять через fix_block.py.")
            lines.append("")
            for para, own, row, sc in moves:
                lines.append("- ED_RU %d → строка %d (score %d)" % (para, row, sc))
            lines.append("")
    return "\n".join(lines) + "\n"


def align(en_list, ed_list, pairs, window=3, skip=6):
    """DP-выравнивание ED_RU-абзацев на EN-строки.

    Возвращает {индекс ED-абзаца: индекс EN-строки} для всех совмещённых
    абзацев. Совпадение даёт score пары, пропуск строки/абзаца — штраф skip.
    """
    ed_idx = [i for i, ed in enumerate(ed_list) if ed and ed != "—"]
    en_n, m = len(en_list), len(ed_idx)
    if not m or not en_n:
        return {}

    NEG = float("-inf")
    # dp[i][j]: лучший счёт, совместив первые i ED и первые j EN
    dp = [[NEG] * (en_n + 1) for _ in range(m + 1)]
    bt = [[None] * (en_n + 1) for _ in range(m + 1)]
    dp[0][0] = 0
    for i in range(m + 1):
        for j in range(en_n + 1):
            cur = dp[i][j]
            if cur == NEG:
                continue
            # матч (i, j): абзац ed_idx[i] ↔ строка en_list[j]
            if i < m and j < en_n and abs(ed_idx[i] - j) <= window:
                s, *_ = score(en_list[j], ed_list[ed_idx[i]], pairs)
                v = cur + s
                if v > dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = v
                    bt[i + 1][j + 1] = ("m", i, j)
            # пропуск EN-строки
            if j < en_n:
                v = cur - skip
                if v > dp[i][j + 1]:
                    dp[i][j + 1] = v
                    bt[i][j + 1] = ("sj", i, j)
            # пропуск ED-абзаца
            if i < m:
                v = cur - skip
                if v > dp[i + 1][j]:
                    dp[i + 1][j] = v
                    bt[i + 1][j] = ("si", i, j)

    # восстановление пути из лучшей ячейки последнего ряда
    best_j = max(range(en_n + 1), key=lambda j: dp[m][j])
    mapping = {}
    i, j = m, best_j
    while i > 0 or j > 0:
        move = bt[i][j]
        if move is None:
            break
        kind, pi, pj = move
        if kind == "m":
            mapping[ed_idx[i - 1]] = j - 1
            i, j = i - 1, j - 1
        elif kind == "sj":
            j -= 1
        else:
            i -= 1
    return mapping


def propose(en_list, ed_list, pairs, window=3, skip=6, margin=3):
    """План пересадки съехавших ED_RU-абзацев.

    Возвращает список (номер ED_RU, своя строка, предложенная строка, score)
    только для абзацев, которым выравнивание предложило чужую строку и
    выигрыш заметен (больше margin по score). Это ПЛАН для проверки глазами;
    автоприменение — `update_merged.py --realign`.
    """
    mapping = align(en_list, ed_list, pairs, window, skip)
    out = []
    for ed_pos, row in sorted(mapping.items()):
        s, *_ = score(en_list[row], ed_list[ed_pos], pairs)
        s_own, *_ = score(en_list[ed_pos], ed_list[ed_pos], pairs)
        if row != ed_pos and s > s_own + margin:
            out.append((ed_pos + 1, ed_pos + 1, row + 1, s))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=None, help="напр. v14-ch04.md")
    ap.add_argument("--all", action="store_true",
                    help="проверить все главы тома (по merged)")
    ap.add_argument("--report", action="store_true",
                    help="записать выгрузку предфильтра в output/_audit/_prefilter/<глава>-alignment.md")
    ap.add_argument("--propose", action="store_true",
                    help="добавить в отчёт план пересадки съехавших ED_RU "
                         "(DP-выравнивание: ED_RU абзац → строка EN)")
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
            print("ОШИБКА: нет merged-файла %s — прогони update_merged.py"
                  % path, file=sys.stderr)
            sys.exit(2)
        items = read_paras(path)
        en_list = [clean(f.get("EN", "")) for _, f in items]
        ed_list = [clean(f.get("ED_RU", "")) for _, f in items]
        signals, stats = check(path, pairs)
        proposal = (propose(en_list, ed_list, pairs)
                    if args.propose else None)
        if not stats["translated"]:
            print("OK: %s | ED_RU пуст — проверять нечего" % name)
            continue
        total_strong += stats["strong"]
        report = render(name, signals, stats, proposal)
        if args.report:
            AUDIT.mkdir(parents=True, exist_ok=True)
            dst = AUDIT / ("%s-alignment.md" % Path(name).stem)
            dst.write_text(report, encoding="utf-8", newline="\n")
            print("OK: выгрузка → output/_audit/_prefilter/%s | строгих %d, "
                  "прочих %d, съезд %d, JA-сдвигов %d%s" % (
                      dst.name, stats["strong"], stats["weak"],
                      stats["near_miss"], stats["ja_shift"],
                      (", пересадка: %d" % len([p for p in proposal
                                                if p[1] != p[2]]))
                      if proposal is not None else ""))
        else:
            sys.stdout.write(report)

    if args.strict and total_strong:
        sys.exit(1)


if __name__ == "__main__":
    main()