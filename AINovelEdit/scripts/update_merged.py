#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_merged.py — обновление merged-файлов (JA/EN/RU/ED_RU).

Агент вызывает этот скрипт ПОСЛЕ сохранения блока — merged-файлы руками
не редактировать. ED_RU берётся из output/<имя>.md (отредактированный
перевод); для ещё не отредактированных абзацев ставится «—».

ВАЖНО: translates/{ja,en,ru} — ИСХОДНИКИ, скрипт читает их и НИКОГДА не
пишет в них (пишет только в translates/_report/merged/). RU-колонка строится
НЕ позиционно (RU-абзацев меньше, чем EN — позиционность давала рассинхрон),
а выравниванием по длине (DP, копия логики tools/normalize.py). Абзацы RU
распределяются по EN-строкам БЕЗ ПОТЕРЬ: если RU-абзацев в группе больше,
чем EN-строк, остаток присоединяется к последней строке группы через « / ».

Использование:
    python scripts/update_merged.py --file v14-ch01.md
    python scripts/update_merged.py            # все главы тома
"""
import argparse
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent
TR = BASE / "translates"
OUT = BASE / "output"
MERGED = TR / "_report" / "merged"

# плейсхолдеры «нет пары» в исходниках; при показе в merged — «—»
NO_PAIR = ("<!-- нет пары в JA -->", "<!-- нет пары в RU -->")


def read_paras(path):
    text = path.read_text(encoding="utf-8")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    # маркеры прогресса — не абзацы
    blocks = [b for b in blocks if not b.startswith("<!-- block:")]
    # первый блок-заголовок (# ...) — это название главы, не абзац
    title = ""
    if blocks and blocks[0].startswith("#"):
        title = blocks.pop(0).lstrip("#").strip()
    return title, blocks


# ---------- выравнивание EN ↔ RU (общая логика с tools/normalize.py) ---------
# Логика выравнивания ЕДИНА: импортируем из tools/normalize.py (якорное
# посиднеечное выравнивание: длина + числа + транслитерированные имена).
# Раньше здесь была копия чисто длиностного DP — из-за этого RU-абзацы,
# покрывавшие соседние EN-абзацы, «съезжали» в merged (пример: RU-контент
# EN-38 оказывался в строке 39, а строка 38 оставалась пустой).

sys.path.insert(0, str(BASE.parent / "tools"))
from normalize import ru_en_sentence_map  # noqa: E402

# проверка соответствия строк (съезд ED_RU ↔ EN-якорь) выполняется сразу
# после генерации merged — проблема всплывает здесь, а не при аудите
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import check_alignment as ca  # noqa: E402
except Exception:
    ca = None


def ru_column(en, ru):
    """Распределяет RU-абзацы по EN-строкам БЕЗ ПОТЕРЬ. Возвращает список
    длины len(en). Склеенный RU-абзац разрезается по предложениям по якорям,
    а не поровну."""
    mapping = ru_en_sentence_map(ru, en)
    return [mapping.get(i, "") for i in range(len(en))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=None, help="напр. v14-ch01.md; иначе — все главы")
    ap.add_argument("--aligned-out", default=None, metavar="DIR",
                    help="дополнительно собрать выровненные копии в папку DIR: "
                         "ED_RU пересаживаются на свои EN-строки по "
                         "DP-выравниванию (для аналитики и итоговой склейки). "
                         "merged/ всегда остаётся зеркалом output/, output/ не "
                         "меняется; без этого флага дубликаты не создаются")
    args = ap.parse_args()

    names = ([args.file] if args.file
             else sorted(p.name for p in (TR / "en").glob("v*.md")))
    for name in names:
        ja_t, ja = read_paras(TR / "ja" / name)
        en_t, en = read_paras(TR / "en" / name)
        _, ru = read_paras(TR / "ru" / name)
        ja = ["" if b in NO_PAIR else b for b in ja]
        ru_col = ["" if b in NO_PAIR else b for b in ru_column(en, ru)]
        out_path = OUT / name
        ed = read_paras(out_path)[1] if out_path.exists() else []
        n = len(en)
        note = ""
        if len(ja) != n:
            note += " (!) JA %d != EN %d" % (len(ja), n)
            ja = (ja + [""] * n)[:n]
        if ed and len(ed) != n:
            note += " (!) ED_RU %d != EN %d — лишние строки отброшены, недостающие — «—»" % (len(ed), n)
            ed = (ed + [""] * n)[:n]
        # --aligned-out DIR: выровненные копии для аналитики. Сам merged/ —
        # всегда зеркало output/ (по нему правят через fix_block.py), поэтому
        # выровненный вариант пишется ТОЛЬКО по явному запросу и в указанную
        # папку (в репозитории дубликатов нет).
        aligned_ed = None
        if args.aligned_out and ca is not None and ed and any(ed):
            plan = ca.align(en, ed, ca.load_names())
            if plan:
                old_ed = list(ed)
                new_ed = [""] * len(ed)
                for ed_idx, row in sorted(plan.items()):
                    txt = ed[ed_idx]
                    if not txt:
                        continue
                    if not new_ed[row]:
                        new_ed[row] = txt
                    elif txt not in new_ed[row]:
                        # две ED-строки на одной EN-строке — склейка через « / »
                        # (тот же принцип, что в ru_column): текст не теряется
                        new_ed[row] = new_ed[row] + " / " + txt
                # абзацы, не попавшие в план (пропуск ED в DP), остаются на своих
                # строках; если строка занята — приклеиваем через « / »
                for i, txt in enumerate(ed):
                    if not txt or i in plan:
                        continue
                    if not new_ed[i]:
                        new_ed[i] = txt
                    elif txt not in new_ed[i]:
                        new_ed[i] = new_ed[i] + " / " + txt
                # гарантия: ни один исходный абзац не потерян
                missing = [t for t in ed if t and not any(t in x for x in new_ed)]
                if missing:
                    note += " (!) выравнивание отменено: потеряно абзацев %d" % len(missing)
                else:
                    moved = sum(1 for a, b in zip(ed, new_ed) if a != b)
                    aligned_ed = new_ed
                    note += " (!) выровненная копия: пересажено %d абзацев" % moved

        def build(ed_list):
            out = []
            for i in range(n):
                out.append("## Абзац %d\n\n**JA:** %s\n\n**EN:** %s\n\n**RU:** %s\n\n**ED_RU:** %s" % (
                    i + 1,
                    ja[i] if i < len(ja) and ja[i] else "—",
                    en[i],
                    ru_col[i] if i < len(ru_col) and ru_col[i] else "—",
                    ed_list[i] if i < len(ed_list) and ed_list[i] else "—"))
            return "# %s\n\n%s\n" % (en_t or name, "\n\n".join(out))

        MERGED.mkdir(parents=True, exist_ok=True)
        (MERGED / name).write_text(build(ed), encoding="utf-8")
        if aligned_ed is not None:
            out_dir = Path(args.aligned_out)
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / name).write_text(build(aligned_ed), encoding="utf-8")
        done = sum(1 for e in ed if e) if ed else 0
        print("OK: %s | абзацев %d | ED_RU заполнено %d%s" % (
            name, n, done, note))
        if ca is not None and done:
            try:
                _signals, _stats = ca.check(MERGED / name, ca.load_names())
                if _stats["strong"] or _stats["near_miss"]:
                    _first = next((s for s in _signals
                                   if s["weight"] == "strong"), None)
                    print(" (!) построчная сверка: строгих %d, съезд %d%s"
                          % (_stats["strong"], _stats["near_miss"],
                             ("; первый: абзац %d (%s) — план пересадки: "
                              "python scripts/check_alignment.py --file %s "
                              "--propose --report"
                              % (_first["para"], _first["kind"], name))
                             if _first else ""))
            except Exception as exc:  # сверка не должна ломать генерацию
                print(" (!) построчная сверка не выполнена: %s" % exc,
                      file=sys.stderr)


if __name__ == "__main__":
    main()
