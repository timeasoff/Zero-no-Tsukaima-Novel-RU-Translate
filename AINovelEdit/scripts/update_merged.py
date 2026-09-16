#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_merged.py — обновление merged-файлов (JA/EN/RU/ED_RU).

Агент вызывает этот скрипт ПОСЛЕ сохранения блока — merged-файлы руками
не редактировать. ED_RU берётся из output/<имя>.md (отредактированный
перевод); для ещё не отредактированных абзацев ставится «—».

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=None, help="напр. v14-ch01.md; иначе — все главы")
    args = ap.parse_args()

    names = ([args.file] if args.file
             else sorted(p.name for p in (TR / "en").glob("v*.md")))
    for name in names:
        ja_t, ja = read_paras(TR / "ja" / name)
        en_t, en = read_paras(TR / "en" / name)
        _, ru = read_paras(TR / "ru" / name)
        out_path = OUT / name
        ed = read_paras(out_path)[1] if out_path.exists() else []
        n = len(en)
        note = ""
        if ed and len(ed) != n:
            note = " (!) ED_RU %d != EN %d — лишние строки отброшены, недостающие — «—»" % (len(ed), n)
            ed = (ed + [""] * n)[:n]
        parts = []
        for i in range(n):
            parts.append("## Абзац %d\n\n**JA:** %s\n\n**EN:** %s\n\n**RU:** %s\n\n**ED_RU:** %s" % (
                i + 1,
                ja[i] if i < len(ja) else "—",
                en[i],
                ru[i] if i < len(ru) else "—",
                ed[i] if i < len(ed) and ed[i] else "—"))
        MERGED.mkdir(parents=True, exist_ok=True)
        (MERGED / name).write_text(
            "# %s\n\n%s\n" % (en_t or name, "\n\n".join(parts)), encoding="utf-8")
        done = sum(1 for e in ed if e) if ed else 0
        print("OK: %s | абзацев %d | ED_RU заполнено %d%s" % (name, n, done, note))


if __name__ == "__main__":
    main()
