#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
drift_scan.py — механический предфильтр РЕГРЕССИЙ (дрейф текста против
базовой git-ревизии).

ОПЦИОНАЛЬНЫЙ инструмент: применяется ТОЛЬКО когда нужно сравнить две ветки
или текущую главу с исторической ревизией. Для первичного пайплайна новой
главы НЕ обязателен — при первичной генерации baseline в git отсутствует
(файл создаётся напрямую в output/), поэтому сравнивать не с чем.

КЛАСС ПРОБЛЕМЫ (подтверждён анализом manual-fix коммитов): агентский коммит
(«v2», «v1», «up») вносил в главу ошибочный СМЫСЛ (подмена субъекта,
потеря отрицания, лишняя деталь), и только позднейший ручной «manual fix»
возвращал корректный текст — потому что никто механически не перечислял,
ЧТО именно изменилось в тексте относительно проверенного состояния.

Скрипт решает это: он сравнивает ТЕКУЩИЙ файл output/ с базовой ревизией
git и выдаёт каждое СМЫСЛОНОСЯЩЕЕ изменение кандидатом на проверку по JA.

Не путать с check_alignment.py: тот сверяет RU с EN/JA (семантика между
языками); этот — RU с предыдущей ВЕРСИЕЙ того же RU (регрессия против
последнего проверенного состояния). Оба — предфильтры, вердикт по каждому
кандидату даёт агент (disposition).

Классификация дрейфа:
  STRONG — изменились смыслонесущие маркеры: числа, отрицания, имена/термины
           из dictionary.md, местоименные лица (мы/ты/вы/они); плюс
           удалённые/добавленные абзацы. Требует сверки с JA обязательно.
  WEAK   — переписывание формулировки без смены маркеров (стиль/лексика).
           Требует disposition: сверить с JA или PRESERVED — STYLE.
  INFO   — только формат (курсив, кавычки, тире, пустые строки, разбивка
           абзацев) и перемещения абзацев без изменения текста.
Обнаружение ≠ вердикт: STRONG/WEAK — кандидаты; решение — по JA/EN.

Использование:
    # правки этой сессии (worktree) против последнего коммита:
    python scripts/drift_scan.py --file v2-ch06.md
    # регрессии последнего коммита (что изменил именно он):
    python scripts/drift_scan.py --file v2-ch06.md --against HEAD~1
    # глава против ревизии, проверенной пользователем вручную
    # (обычно последний коммит с «manual fix» в сообщении):
    python scripts/drift_scan.py --file v2-ch06.md --against <SHA>
    python scripts/drift_scan.py --file v2-ch06.md --report
    python scripts/drift_scan.py --file v2-ch06.md --strict   # код 1 при STRONG
    python scripts/drift_scan.py --selftest
"""
import argparse
import difflib
import re
import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent      # AINovelEdit/
ROOT = BASE.parent                                 # корень репозитория
AUDIT = BASE / "output" / "_audit" / "_prefilter"
DICT = BASE / "dictionary.md"

BLOCK_MARK_RE = re.compile(r"<!--\s*block:\s*(\d+)\s*-->")
# формат: то, что НЕ несёт смысла при сравнении версий


FMT_RE = re.compile(r"[\s_*«»\"“”\[\]()…]")
NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")
RU_NUM_RE = re.compile(
    r"\b(?:один|одна|одно|одного|одной|одну|два|двух|двумя|две|три|трёх"
    r"|трех|трём|тремя|четыре|четырех|четырёх|пят\w*|шест\w*|семь|семи"
    r"|семнадцат|восем|восьм\w*|девят\w*|десят\w*|двадцат\w*|тридцат\w*"
    r"|сорок|пятьдесят|шестьдесят|семьдесят|восемьдесят|девяносто|сто"
    r"|сотн\w*|тысяч\w*)\b", re.I)
NEG_RE = re.compile(r"\b(?:не|ни|нет|без|никогда|ничего|никто|нельзя)\b", re.I)
PERSON_RE = re.compile(
    r"\b(?:мы|нам|нас|нами|наш\w*|я|мне|меня|мной|мною|мо[йяе]\w*"
    r"|ты|тебе|тебя|тобой|тво[йяе]\w*|вы|вам|вас|вами|ваш\w*"
    r"|он|она|оно|они|им|их|ими|нем|ней|них)\b", re.I)

KIND_TITLES = {
    "STRONG": "Смыслонесущий дрейф (числа/отрицания/имена/лица/абзацы)",
    "WEAK": "Переписывание формулировки (без смены смысловых маркеров)",
    "INFO": "Только формат / перемещение",
}
KIND_HINT = {
    "STRONG": "Сверь изменение с JA (EN — вспомогательно): подтверди или "
              "откати. Disposition обязателен: FIXED / FALSE POSITIVE / "
              "PRESERVED — JA/EN / USER DECISION / ???. Частый класс "
              "регрессий — подмена субъекта и потеря отрицания.",
    "WEAK": "Проверь смысл по JA; если правка стилевая и смысл цел — "
            "PRESERVED — STYLE; если смысл ушёл — верни по JA (FIXED).",
    "INFO": "Формат (курсив/кавычки/тире/пустые строки) и перемещения — "
            "разбор не требуется, если содержание не изменилось.",
}


def load_baseline(rev, git_path):
    """Читает файл из git-ревизии. Возвращает None, если файла там нет."""
    try:
        out = subprocess.run(
            ["git", "show", f"{rev}:{git_path}"],
            capture_output=True, cwd=ROOT)
    except OSError as e:
        print(f"[drift_scan] git недоступен: {e}", file=sys.stderr)
        sys.exit(2)
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8", "replace")


def split_blocks(text):
    """Словарь {номер блока: [абзацы]} + список абзацев до первого маркера."""
    blocks = {}
    pre = []
    cur = pre
    for line in text.splitlines():
        m = BLOCK_MARK_RE.match(line.strip())
        if m:
            cur = blocks.setdefault(int(m.group(1)), [])
            continue
        if line.strip() == "":
            continue
        if line.startswith("#"):
            continue
        cur.append(line.strip())
    return pre, blocks


def norm(s):
    """Нормализация: убрать формат, привести к нижнему регистру."""
    return FMT_RE.sub("", s).lower()


def load_dict_terms():
    """Пары (пусто, RU-основа, RU-канон) из dictionary.md.

    В отличие от check_alignment.load_names (строится по EN-колонке с
    заглавной), здесь берутся ВСЕ русские каноны: их ловит и drift_scan
    (замена «пирс» → «причал» при EN «pier» со строчной буквы).
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
        ru = cells[2]
        if ru.startswith("---") or ru.startswith("—") or not ru:
            continue
        ru_clean = ru.replace("*", "").replace("«", "").replace("»", "")
        words = re.findall(r"[А-Яа-яЁё]+", ru_clean)
        if not words:
            continue
        first = words[0]
        if len(first) < 4:
            continue
        pairs.append((set(), first.lower().replace("ё", "е"), ru_clean.strip()))
    return pairs


def names_in_ru(text, pairs):
    found = set()
    tokens = [re.sub(r"[^а-яё]", "", w.lower().replace("ё", "е"))
              for w in re.findall(r"[А-Яа-яЁё][А-Яа-яЁё\-]+", text)]
    for _en, ru_base, ru in pairs:
        if any(t.startswith(ru_base) for t in tokens if ru_base):
            found.add(ru)
    return found


def classify_pair(old, new, pairs):
    """Пара абзацев (старый → новый) → (kind, причина)."""
    if norm(old) == norm(new):
        return "INFO", "только формат/разметка"

    n_old, n_new = set(NUM_RE.findall(old)), set(NUM_RE.findall(new))
    if {x.replace(",", ".") for x in n_old} != {x.replace(",", ".") for x in n_new}:
        return "STRONG", ("числа изменились: {%s} → {%s}"
                          % (", ".join(sorted(n_old)) or "—",
                             ", ".join(sorted(n_new)) or "—"))
    rn_old = {x.lower() for x in RU_NUM_RE.findall(old)}
    rn_new = {x.lower() for x in RU_NUM_RE.findall(new)}
    if rn_old != rn_new:
        return "STRONG", ("числа словами изменились: {%s} → {%s}"
                          % (", ".join(sorted(rn_old)) or "—",
                             ", ".join(sorted(rn_new)) or "—"))
    if bool(NEG_RE.search(old)) != bool(NEG_RE.search(new)):
        return "STRONG", "появилось/пропало отрицание"
    nm_old, nm_new = names_in_ru(old, pairs), names_in_ru(new, pairs)
    if nm_old != nm_new:
        return "STRONG", ("имена/термины: ушло {%s}, появилось {%s}"
                          % (", ".join(sorted(nm_old - nm_new)) or "—",
                             ", ".join(sorted(nm_new - nm_old)) or "—"))
    p_old = {x.lower() for x in PERSON_RE.findall(old)}
    p_new = {x.lower() for x in PERSON_RE.findall(new)}
    if p_old != p_new:
        return "STRONG", ("местоименные лица: {%s} → {%s}"
                          % (", ".join(sorted(p_old)) or "—",
                             ", ".join(sorted(p_new)) or "—"))
    return "WEAK", "формулировка переписана без смены смысловых маркеров"



def compare_texts(base_text, cur_text, pairs):
    """Сравнение двух версий файла → список находок [(блок, kind, причина,
    старый, новый)]. Сопоставление — по абзацам внутри каждого блока."""
    findings = []
    base_pre, base_blocks = split_blocks(base_text)
    cur_pre, cur_blocks = split_blocks(cur_text)

    all_blocks = sorted(set(base_blocks) | set(cur_blocks))
    for num in all_blocks:
        old_list = base_blocks.get(num, [])
        new_list = cur_blocks.get(num, [])
        sm = difflib.SequenceMatcher(None, [norm(x) for x in old_list],
                                     [norm(x) for x in new_list], autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                # формат внутри равных по смыслу абзацев мог измениться
                for k in range(i2 - i1):
                    oi, ni = i1 + k, j1 + k
                    if oi < len(old_list) and ni < len(new_list) and \
                            old_list[oi] != new_list[ni]:
                        findings.append((num, "INFO",
                                         "формат внутри абзаца (смысл равен)",
                                         old_list[oi], new_list[ni]))
                continue
            # DELETE / INSERT / REPLACE: сначала пытаемся сопоставить попарно
            old_seg, new_seg = old_list[i1:i2], new_list[j1:j2]
            # если все слова сегмента равны — просто изменились границы
            # абзацев (разбивка/слипание), смысла не изменилось
            if old_seg and new_seg and \
                    "".join(norm(x) for x in old_seg) == \
                    "".join(norm(x) for x in new_seg):
                findings.append((num, "INFO",
                                 "границы абзацев изменились (смысл равен)",
                                 old_seg[0], new_seg[0]))
                continue
            n = min(len(old_seg), len(new_seg))
            for k in range(n):
                kind, why = classify_pair(old_seg[k], new_seg[k], pairs)
                findings.append((num, kind, why, old_seg[k], new_seg[k]))
            for k in range(n, len(old_seg)):
                findings.append((num, "STRONG",
                                 "абзац УДАЛЁН (нет в новой версии)",
                                 old_seg[k], ""))
            for k in range(n, len(new_seg)):
                findings.append((num, "STRONG",
                                 "абзац ДОБАВЛЕН (нет в базовой версии)",
                                 "", new_seg[k]))
    return findings


def render(name, rev, findings):
    kinds = {}
    for _, k, _, _, _ in findings:
        kinds[k] = kinds.get(k, 0) + 1
    lines = ["# Выгрузка предфильтра (регрессии/дрейф): %s" % name, ""]
    lines.append("База: `%s` | Кандидатов: **%d** (%s)." % (
        rev, len(findings),
        ", ".join("%s %d" % (k, kinds[k]) for k in sorted(kinds)) or "нет"))
    lines += ["",
              "Скрипт сравнивает текущий output с предыдущей ВЕРСИЕЙ того же "
              "текста (не с JA!). Это ловит регрессии: правку, вносимую "
              "агентским коммитом и исправляемую только ручным manual fix. "
              "Обнаружение ≠ вердикт: каждый STRONG/WEAK получает "
              "disposition после сверки с JA.", ""]
    for kind in ("STRONG", "WEAK", "INFO"):
        items = [f for f in findings if f[1] == kind]
        if not items:
            continue
        lines.append("## %s (%d)" % (KIND_TITLES[kind], len(items)))
        lines.append("")
        lines.append("- **Подсказка:** %s" % KIND_HINT[kind])
        lines.append("")
        for block, _k, why, old, new in items:
            lines.append("### Блок %d — %s" % (block, why))
            lines.append("")
            if old:
                lines.append("- **Было:** %s" % old[:400])
            if new:
                lines.append("- **Стало:** %s" % new[:400])
            lines.append("")
    return "\n".join(lines) + "\n"



# ---------------------------------------------------------------------------
# Selftest: регрессии из истории проекта + границы
# ---------------------------------------------------------------------------

POSITIVE_CASES = [
    # (база, текущая версия, ожидаемый kind, подпись)
    # подмена субъекта — класс ручных правок «Сайто с компанией» → «вторая часть отряда»
    ("<!-- block: 1 -->\nУбедившись, что Сайто с компанией ушли к входу.",
     "<!-- block: 1 -->\nУбедившись, что вторая часть отряда ушла к входу.",
     "STRONG", "подмена субъекта (имена)"),
    # потеря отрицания
    ("<!-- block: 1 -->\nОн не смог её спасти.",
     "<!-- block: 1 -->\nОн смог её спасти.",
     "STRONG", "потеря отрицания"),
    # числа
    ("<!-- block: 1 -->\nИх было тридцать.",
     "<!-- block: 1 -->\nИх было двадцать.",
     "STRONG", "числа"),
    # местоименное лицо «вас/нас»
    ("<!-- block: 1 -->\nТочно благословляют вас двоих.",
     "<!-- block: 1 -->\nТочно благословляют нас двоих.",
     "STRONG", "местоименное лицо"),
    # удалённый абзац (смысловая потеря)
    ("<!-- block: 1 -->\nРеплика Гиша.\nПропущенная деталь.",
     "<!-- block: 1 -->\nРеплика Гиша.",
     "STRONG", "удалённый абзац"),
    # переписывание без смены маркеров — WEAK
    ("<!-- block: 1 -->\nГиш впал в настоящую панику.",
     "<!-- block: 1 -->\nГиш перепугался изо всех сил.",
     "WEAK", "переписывание формулировки"),
    # замена словарного термина (канон «пирс» подменён на «причал»)
    ("<!-- block: 1 -->\nМы выйдем через заднюю дверь и двинемся на пирс.",
     "<!-- block: 1 -->\nМы выйдем через заднюю дверь и двинемся на причал.",
     "STRONG", "подмена словарного термина"),
]

NEGATIVE_CASES = [
    # только формат (курсив) — INFO
    ("<!-- block: 1 -->\nДурачит меня, — подумал он.",
     "<!-- block: 1 -->\n_Дурачит меня_, — подумал он.",
     "INFO"),
    # пустые строки/разбивка абзацев при равном смысле — INFO
    ("<!-- block: 1 -->\n— Реплика. Наррация после неё.",
     "<!-- block: 1 -->\n— Реплика.\nНаррация после неё.",
     "INFO"),
    # идентичный текст — находок нет
    ("<!-- block: 1 -->\nОдин и тот же текст.",
     "<!-- block: 1 -->\nОдин и тот же текст.",
     None),
]


def run_selftest() -> int:
    failed = []
    pairs = load_dict_terms()
    for base, cur, want, label in POSITIVE_CASES:
        found = compare_texts(base, cur, pairs)
        kinds = {k for _, k, _, _, _ in found}
        if want not in kinds:
            failed.append(("FIND", label))
            print(f"  FAIL FIND ({label}): нет {want}, есть {sorted(kinds)}")
        else:
            print(f"  OK   FIND ({label})")
    for base, cur, want in NEGATIVE_CASES:
        found = compare_texts(base, cur, pairs)
        kinds = {k for _, k, _, _, _ in found}
        if want is None:
            if found:
                failed.append(("PASS", cur[:40]))
                print(f"  FAIL PASS (лишние находки: {sorted(kinds)}): {cur[:60]}")
            else:
                print(f"  OK   PASS (нет находок): {cur[:60]}")
        elif want not in kinds or (want == "INFO" and kinds - {"INFO"}):
            failed.append(("PASS", cur[:40]))
            print(f"  FAIL PASS ({cur[:50]}): ожидался только {want}, есть {sorted(kinds)}")
        else:
            print(f"  OK   PASS ({want}): {cur[:60]}")
    if failed:
        print(f"\n[selftest] ПРОВАЛЕНО: {len(failed)} из "
              f"{len(POSITIVE_CASES) + len(NEGATIVE_CASES)}")
        return 1
    print("\n[selftest] OK: все %d контрольных кейсов пройдены"
          % (len(POSITIVE_CASES) + len(NEGATIVE_CASES)))
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Предфильтр регрессий: текущий output против базовой "
                    "git-ревизии (ловит смысл, испорченный прошлыми "
                    "агентскими коммитами)")
    ap.add_argument("--file", help="имя/путь к output-файлу (vXX-chYY.md)")
    ap.add_argument("--against", default="HEAD",
                    help="базовая ревизия git (по умолчанию HEAD — правки "
                         "этой сессии; HEAD~1 — регрессии последнего коммита; "
                         "<SHA> — проверенная ручная ревизия)")
    ap.add_argument("--against-file",
                    help="путь к файлу-базе вместо git-ревизии (сравнение "
                         "двух произвольных версий, напр. для ретро-проверки "
                         "истории: git show <rev>:<path> > tmp.md)")
    ap.add_argument("--report", action="store_true",
                    help="выгрузка в output/_audit/_prefilter/<глава>-drift.md")
    ap.add_argument("--strict", action="store_true",
                    help="код 1, если есть STRONG-кандидаты")
    ap.add_argument("--selftest", action="store_true",
                    help="контрольные тесты")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()

    if not args.file:
        ap.error("нужен --file или --selftest")

    path = Path(args.file)
    if not path.exists():
        candidates = [BASE / "output" / path.name, BASE / "output" / args.file]
        for c in candidates:
            if c.exists():
                path = c
                break
        else:
            print(f"[drift_scan] файл не найден: {args.file}", file=sys.stderr)
            sys.exit(2)

    if args.against_file:
        bp = Path(args.against_file)
        if not bp.exists():
            print(f"[drift_scan] файл-база не найден: {bp}", file=sys.stderr)
            sys.exit(2)
        base_text = bp.read_text(encoding="utf-8")
        rev_label = args.against_file
    else:
        git_path = path.resolve().relative_to(ROOT).as_posix()
        base_text = load_baseline(args.against, git_path)
        rev_label = args.against
        if base_text is None:
            print(f"[drift_scan] нет файла {git_path} в ревизии {args.against} — "
                  "сравнивать не с чем (новый файл?).")
            return 0

    pairs = load_dict_terms()
    findings = compare_texts(base_text, path.read_text(encoding="utf-8"), pairs)
    report = render(path.name, rev_label, findings)

    if args.report:
        AUDIT.mkdir(parents=True, exist_ok=True)
        dst = AUDIT / (path.stem + "-drift.md")
        dst.write_text(report, encoding="utf-8", newline="\n")
        print("OK: выгрузка → output/_audit/_prefilter/%s | кандидатов %d"
              % (dst.name, len(findings)))
    else:
        sys.stdout.write(report)

    strong = sum(1 for f in findings if f[1] == "STRONG")
    if args.strict and strong:
        sys.exit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())

