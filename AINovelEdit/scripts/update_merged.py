#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_merged.py — обновление merged-файлов (JA/EN/RU/ED_RU) по СМЫСЛОВЫМ БЛОКАМ.

Агент вызывает скрипт ПОСЛЕ сохранения блока — merged-файлы руками не
редактировать. ED_RU берётся из output/<имя>.md (отредактированный перевод);
для ещё не отредактированных блоков ставится «—».

Блоки уже выровнены при нормализации (`<!-- block: N -->` одинаков во всех
`translates/{ja,en,ru}`), поэтому merged строится напрямую: блок N исходников
и блок N `output/` — одна и та же микросцена.

Завершённые тома (AINovelEdit/completed.md) не обрабатываются: их текст
заморожен и служит источником истины при расхождениях.

ВАЖНО: translates/{ja,en,ru} — ИСХОДНИКИ, скрипт их только читает и НИКОГДА
не пишет (пишет только в translates/_report/merged/).

Использование:
    python scripts/update_merged.py --file v15-ch01.md
    python scripts/update_merged.py            # все главы тома
"""
import argparse
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent
TR = BASE / "translates"
OUT = BASE / "output"
MERGED = TR / "_report" / "merged"
REGISTRY = BASE / "completed.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import merged_io      # noqa: E402
import completed      # noqa: E402
try:
    import check_alignment as ca  # noqa: E402
except Exception:
    ca = None


def read_title(path):
    """Заголовок главы (первая строка '# ...')."""
    try:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return ""


def update_block_file(name):
    """Строит merged/<name> по смысловым блокам. Возвращает (блоков, заполнено)."""
    ja_by = {n: "\n".join(ps) for n, ps in
             merged_io.read_source_blocks(TR / "ja" / name)}
    en_by = {n: "\n".join(ps) for n, ps in
             merged_io.read_source_blocks(TR / "en" / name)}
    ru_by = {n: "\n".join(ps) for n, ps in
             merged_io.read_source_blocks(TR / "ru" / name)}
    ed_by = {n: "\n".join(ps) for n, ps in
             merged_io.read_source_blocks(OUT / name)}

    ids = sorted(set(ja_by) | set(en_by) | set(ru_by) | set(ed_by))
    parts = []
    for bid in ids:
        parts.append(
            "## Блок %d\n\n**JA:**\n%s\n\n**EN:**\n%s\n\n**RU:**\n%s\n\n"
            "**ED_RU:**\n%s\n" % (
                bid,
                ja_by.get(bid) or "—",
                en_by.get(bid) or "—",
                ru_by.get(bid) or "—",
                ed_by.get(bid) or "—"))
    MERGED.mkdir(parents=True, exist_ok=True)
    (MERGED / name).write_text(
        "# %s\n\n%s\n" % (read_title(TR / "en" / name) or name,
                          "\n".join(parts)), encoding="utf-8")

    done = sum(1 for bid in ids if ed_by.get(bid))
    print("OK: %s | блоков %d | ED_RU заполнено %d" % (name, len(ids), done))
    if ca is not None and done:
        try:
            _s, _st = ca.check(MERGED / name, ca.load_names())
            print("   сверка блоков: строгих %d, прочих %d, инфо %d" % (
                _st["strong"], _st["weak"], _st["info"]))
        except Exception as exc:  # сверка не должна ломать генерацию
            print("   сверка не выполнена: %s" % exc, file=sys.stderr)
    return len(ids), done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=None,
                    help="напр. v15-ch01.md; иначе — все главы тома")
    args = ap.parse_args()

    names = ([args.file] if args.file
             else sorted(p.name for p in (TR / "en").glob("v*.md")))
    frozen = completed.frozen_volumes(REGISTRY)
    skipped = []
    for name in names:
        vol = completed.volume_of(name)
        if vol in frozen:
            skipped.append(name)
            continue
        if not merged_io.has_block_markers(TR / "en" / name):
            print(" (!) %s: нет маркеров смысловых блоков — пропущено "
                  "(том не нормализован текущим tools/normalize.py)" % name,
                  file=sys.stderr)
            continue
        update_block_file(name)
    if skipped:
        print("Завершённые (замороженные) тома не обновляются: %s"
              % ", ".join(sorted(set(skipped))))


if __name__ == "__main__":
    main()

