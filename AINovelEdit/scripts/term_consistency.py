#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""term_consistency.py — межблочная сверка терминов главы.

ЧТО ДЕЛАЕТ:
  1) Словарный режим (по умолчанию): собирает RU-каноны из dictionary.md
     (та же разметка, что и в drift_scan.load_dict_terms) и перечисляет
     ВСЕ их вхождения по блокам главы с кратким контекстом. Это ИНВЕНТАРЬ
     повторов: его читает агент и решает, согласована ли терминология.
     Скрипт НЕ выносит вердиктов: один JA-термин не всегда требует
     единственной RU-формы (см. SKILL terminology-dictionary).
  2) Режим --variants "форма1, форма2, ...": исследует заданный список
     КОНКУРИРУЮЩИХ RU-форм одного (гипотетически) JA-термина. Показывает
     распределение по блокам и выдаёт КАНДИДАТА на сверку с JA (не ошибку!),
     когда:
       - два разных варианта встречаются в ОДНОМ блоке, или
       - разные варианты встречаются в блоках, отстоящих не дальше чем
         --gap позиций друг от друга (по умолчанию 1 — соседние блоки).
     При контекстной вариативности (цель — собеседник, стиль, цитата)
     агент правомочен вынести PRESERVED — STYLE.

ОБНАРУЖЕНИЕ ≠ ВЕРДИКТ: любые предупреждения этого скрипта — кандидаты
на разбор. Текст главы скрипт не правит.

ИСПОЛЬЗОВАНИЕ:
  python scripts/term_consistency.py --file v5-ch09.md
  python scripts/term_consistency.py --file v5-ch09.md \\
         --variants "свидание, встретиться" --gap 1
  python scripts/term_consistency.py --file v5-ch09.md --report
  python scripts/term_consistency.py --selftest
"""
import argparse
import re
import sys
from pathlib import Path
from collections import Counter

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent       # AINovelEdit/
ROOT = BASE.parent                                   # корень репозитория
DICT = BASE / "dictionary.md"
AUDIT = BASE / "output" / "_audit" / "_prefilter"

BLOCK_MARK_RE = re.compile(r"<!--\s*block:\s*(\d+)\s*-->")


def split_blocks(text):
    """{номер блока: [абзацы]} + абзацы до первого маркера (как в drift_scan)."""
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


def load_dict_terms(dict_path=None):
    """Пары (стем, RU-канон) из dictionary.md.

    Стем = первые N-2 символа первого слова канона (не меньше 4), где N —
    длина слова: покрывает падежные формы («сильфида» → «сильфид...»),
    но не прыгает на другие корни («сильный» ≠ «сильфид...»).
    """
    path = Path(dict_path) if dict_path else DICT
    if not path.exists():
        return []
    pairs = []
    seen = set()
    for line in path.read_text(encoding="utf-8").splitlines():
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
        key = first.lower()[:max(4, len(first) - 2)]
        if key in seen:
            continue
        seen.add(key)
        pairs.append((key, ru_clean.strip()))
    return pairs


def find_occurrences(blocks, stem):
    """[(блок, форма, фрагмент)] для всех слов, начинающихся со стема."""
    rx = re.compile(r"\b%s[А-Яа-яЁё\-]*" % re.escape(stem), re.IGNORECASE)
    out = []
    for bnum in sorted(blocks):
        for para in blocks[bnum]:
            m = rx.search(para)
            if not m:
                continue
            full = m.group(0)
            # контекст: вокруг найденной формы до 60 символов
            a, b = max(0, m.start() - 20), min(len(para), m.end() + 40)
            ctx = para[a:b]
            out.append((bnum, full, ctx))
    return out


def inventory_report(blocks, pairs):
    """Строки отчёта: для каждого словарного канона — вхождения по блокам."""
    lines = []
    any_term = False
    for stem, canon in pairs:
        occ = find_occurrences(blocks, stem)
        if not occ:
            continue
        any_term = True
        forms = Counter(full for _, full, _ in occ)
        bnum_list = ", ".join(str(b) for b, _, _ in occ)
        lines.append("### %s" % canon)
        lines.append("- Вхождения: %s" % bnum_list)
        lines.append("- Формы: %s" % ", ".join(
            "%s ×%d" % (f, c) for f, c in forms.most_common()))
        _, _, first_ctx = occ[0]
        lines.append("- Контекст (первое): «%s»" % first_ctx)
        lines.append("")
    if not any_term:
        lines.append("(словарные каноны в этой главе не встречаются)")
        lines.append("")
    return lines


def variants_report(blocks, variants, gap=1):
    """Строки отчёта для заданных конкурирующих форм.

    variants — список RU-форм (строки). Кандидат на сверку, если
    две разные формы встречаются в одном блоке или в блоках,
    отстоящих друг от друга не более чем на gap позиций (в проекции
    списка присутствующих блоков).
    """
    lines = []
    block_nums = sorted(blocks)
    pos_of_block = {b: i for i, b in enumerate(block_nums)}
    hits = {}
    for v in variants:
        rx = re.compile(re.escape(v), re.I)
        occ = []
        for bnum in sorted(blocks):
            for para in blocks[bnum]:
                for m in rx.finditer(para):
                    a, b = max(0, m.start() - 20), min(len(para), m.end() + 40)
                    occ.append((bnum, para[a:b]))
        hits[v] = occ

    lines.append("### Заданные конкурирующие формы")
    for v in variants:
        occ = hits[v]
        if not occ:
            lines.append("- «%s»: не встречается" % v)
            continue
        per_block = Counter(b for b, _ in occ)
        dist = ", ".join("б.%d ×%d" % (b, c) for b, c in sorted(per_block.items()))
        lines.append("- «%s»: %s" % (v, dist))
        lines.append("  - Контекст (первое): «%s»" % occ[0][1])
    lines.append("")

    present = [(v, b) for v in variants for (b, _) in hits[v]]
    candidates = []
    for i in range(len(present)):
        vi, bi = present[i]
        for j in range(i + 1, len(present)):
            vj, bj = present[j]
            if vi == vj:
                continue
            if bi == bj:
                candidates.append((vi, vj, bi, "в одном блоке б.%d" % bi))
            elif abs(pos_of_block[bi] - pos_of_block[bj]) <= gap:
                candidates.append((vi, vj, bi,
                                   "близко: б.%d и б.%d" % (bi, bj)))
    if candidates:
        lines.append("## Кандидаты на сверку (не вердикты)")
        for vi, vj, bi, why in candidates:
            lines.append("- «%s» ↔ «%s» — %s" % (vi, vj, why))
        lines.append("")
        lines.append("Разбор по JA: если формы взаимозаменяемы в контексте —")
        lines.append("PRESERVED — STYLE; если JA-термин требует унификации — FIXED.")
        lines.append("Один JA-термин может допускать контекстную вариативность RU.")
        lines.append("")
    else:
        lines.append("(конкуренция форм в близких блоках не найдена — сценарий ожидаемый)")
        lines.append("")
    return lines


def render(name, lines):
    out = ["# Терминологическая сверка: %s" % name, ""]
    out.extend(lines)
    return "\n".join(out) + "\n"


POSITIVE_CASES = [
    # (текст, варианты, gap, подпись) — ожидается кандидат на сверку
    ("<!-- block: 2 -->\nОн назначил свидание.",
     "<!-- block: 3 -->\nОни решили встретиться.",
     ["свидание", "встретиться"], 1,
     "варианты в соседних блоках → кандидат"),
    ("<!-- block: 2 -->\nСвидание состоялось; о встретиться с нами.",
     "<!-- block: 3 -->\nТут же встретиться.",
     ["свидание", "встретиться"], 1,
     "варианты в одном блоке → кандидат"),
]

NEGATIVE_CASES = [
    # (текст, варианты, gap, подпись) — кандидата быть не должно
    ("<!-- block: 1 -->\nОн назначил свидание.",
     "<!-- block: 2 -->\nСвидание состоялось.",
     ["свидание", "встретиться"], 1,
     "одна форма — без кандидата"),
    ("<!-- block: 1 -->\nСвидание состоялось.",
     "<!-- block: 2 -->\nОн ушёл.\n\n<!-- block: 3 -->\nОн снова ушёл.\n"
     "\n<!-- block: 4 -->\nОн опять ушёл.\n\n<!-- block: 5 -->\nОн опять ушёл.\n"
     "\n<!-- block: 6 -->\nОн опять ушёл.\n\n<!-- block: 7 -->\nОн опять ушёл.\n"
     "\n<!-- block: 8 -->\nДалеко потом встретиться.",
     ["свидание", "встретиться"], 1,
     "варианты в далёких блоках (1 и 8) → без кандидата"),
    ("<!-- block: 1 -->\nСвидание состоялось.",
     "<!-- block: 2 -->\nОн ушёл.\n\n<!-- block: 3 -->\nОн снова ушёл.\n"
     "\n<!-- block: 4 -->\nОн опять ушёл.\n\n<!-- block: 5 -->\nОн опять ушёл.\n"
     "\n<!-- block: 6 -->\nОн опять ушёл.\n\n<!-- block: 7 -->\nОн опять ушёл.\n"
     "\n<!-- block: 8 -->\nДалеко потом встретиться.",
     ["свидание", "встретиться"], 2,
     "при gap=2 всё ещё без кандидата (расстояние 7)"),
]


def run_selftest() -> int:
    failed = []
    print("[selftest] POSITIVE (ожидается кандидат):")
    for i, (a, b, variants, gap, label) in enumerate(POSITIVE_CASES, 1):
        text = "%s\n\n%s" % (a, b)
        _, blocks = split_blocks(text)
        lines = variants_report(blocks, variants, gap)
        ok = "Кандидаты на сверку" in ("\n".join(lines))
        if not ok:
            failed.append(("POS", label))
            print("  FAIL POS (%s): кандидат не выписан" % label)
        else:
            print("  OK   POS (%s)" % label)

    print("[selftest] NEGATIVE (кандидата быть не должно):")
    for i, (a, b, variants, gap, label) in enumerate(NEGATIVE_CASES, 1):
        text = "%s\n\n%s" % (a, b)
        _, blocks = split_blocks(text)
        lines = variants_report(blocks, variants, gap)
        ok = "Кандидаты на сверку" not in ("\n".join(lines))
        if not ok:
            failed.append(("NEG", label))
            print("  FAIL NEG (%s): кандидат выписан, а shouldn't" % label)
        else:
            print("  OK   NEG (%s)" % label)

    if failed:
        print("\n[selftest] FAIL: %d из %d" % (len(failed),
              len(POSITIVE_CASES) + len(NEGATIVE_CASES)))
        return 1
    print("\n[selftest] OK: все %d контрольных кейсов пройдены"
          % (len(POSITIVE_CASES) + len(NEGATIVE_CASES)))
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Межблочная сверка терминов: инвентарь словарных канонов "
                    "и распределение заданных конкурирующих форм по блокам")
    ap.add_argument("--file", help="имя/путь к output-файлу (vXX-chYY.md)")
    ap.add_argument("--variants", help='конкурирующие формы через запятую, '
                    'напр. "свидание, встретиться"')
    ap.add_argument("--gap", type=int, default=1,
                    help="максимальное блочное расстояние для кандидата (1)")
    ap.add_argument("--report", action="store_true",
                    help="выгрузка в output/_audit/_prefilter/<глава>-terms.md")
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
            print(f"[term_consistency] файл не найден: {args.file}", file=sys.stderr)
            sys.exit(2)

    text = path.read_text(encoding="utf-8")
    _, blocks = split_blocks(text)

    if args.variants:
        variants = [v.strip() for v in args.variants.split(",") if v.strip()]
        if not variants:
            ap.error("--variants пуст")
        lines = variants_report(blocks, variants, args.gap)
    else:
        pairs = load_dict_terms()
        lines = inventory_report(blocks, pairs)

    report = render(path.name, lines)

    if args.report:
        AUDIT.mkdir(parents=True, exist_ok=True)
        dst = AUDIT / (path.stem + "-terms.md")
        dst.write_text(report, encoding="utf-8", newline="\n")
        print("OK: выгрузка → output/_audit/_prefilter/%s" % dst.name)
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
