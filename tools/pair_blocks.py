#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pair_blocks.py — один файл «output ↔ японский оригинал» для стороннего ИИ.

НАЗНАЧЕНИЕ
==========
Инструмент складывает в ОДИН отдельный файл (в отдельную папку) две составляющие
одной главы:

  * то, что получилось в `AINovelEdit/output/<слаг>.md` (RU, результат работы),
  * японский оригинал из `AINovelEdit/translates/ja/<слаг>.md` (JA).

Файл собран блоками (`<!-- block: N -->`): внутри блока сначала JA-оригинал,
сразу под ним — то, что получилось в output. Такой файл можно целиком отдать
стороннему ИИ, а можно скопировать один блок (от `<!-- block: N -->` до
`===== КОНЕЦ БЛОКА N =====`) — метки внутри однозначно разделяют части.

Ничего в исходных файлах не меняется: инструмент только читает и пишет
один свой файл.

ИСПОЛЬЗОВАНИЕ (из корня репозитория)
====================================
    python tools/pair_blocks.py v6-ch03            # -> pairs/v6-ch03.md
    python tools/pair_blocks.py 6-ch03              # ведущая v необязательна
    python tools/pair_blocks.py v6-ch03 --out /tmp/one.md   # свой путь
    python tools/pair_blocks.py --list              # какие главы доступны
    python tools/pair_blocks.py --self-test         # самопроверка

    # опции: --project AINovelEdit  --out-dir pairs  --quiet

СОПОСТАВЛЕНИЕ БЛОКОВ
====================
* Обычный случай: в обоих файлах есть `<!-- block: N -->` — пары идут по номеру
  блока; блок, которого нет на одной из сторон, попадает в файл с пометкой.
* JA-файл без маркеров блоков (старые тома, например v14-*): JA-абзацы
  распределяются по блокам output ПРИБЛИЗИТЕЛЬНО — пропорционально объёму
  текста. Это явно помечается и в файле, и в консоли: JA-текст при этом
  не режется и не переписывается, меняется только группировка абзацев.
* JA-файл отсутствует (например, `v*-ch00` — служебные страницы): ошибка
  с кодом 2 и подсказка доступных слагов.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BLOCK_RE = re.compile(r"<!--\s*block:\s*(\d+)\s*-->")

LABEL_JA = "JA (японский оригинал)"
LABEL_OUT = "OUTPUT (то, что получилось в output)"


# ---------------------------------------------------------------------------
# Разбор главы
# ---------------------------------------------------------------------------

def _clean(text: str) -> str:
    """Убрать пустые строки по краям и схлопнуть серии пустых строк до одной."""
    lines = [ln.rstrip() for ln in text.splitlines()]
    i, j = 0, len(lines)
    while i < j and not lines[i].strip():
        i += 1
    while j > i and not lines[j - 1].strip():
        j -= 1
    out, blank = [], False
    for ln in lines[i:j]:
        if ln.strip():
            out.append(ln)
            blank = False
        elif not blank:
            out.append("")
            blank = True
    return "\n".join(out)


def parse_chapter(path: Path):
    """-> (заголовок главы без `#` или "", OrderedDict[номер -> текст], есть_ли_маркеры)."""
    text = path.read_text(encoding="utf-8")
    parts = BLOCK_RE.split(text)
    head = ""
    for ln in parts[0].splitlines():
        if ln.strip():
            head = ln.strip()
            break
    title = head.lstrip("#").strip() if head.startswith("#") else ""
    blocks = OrderedDict()
    for i in range(1, len(parts) - 1, 2):
        num = int(parts[i])
        content = _clean(parts[i + 1])
        if num in blocks and blocks[num] and content:
            blocks[num] = blocks[num] + "\n\n" + content   # дубликат номера
        else:
            blocks[num] = content
    return title, blocks, bool(BLOCK_RE.search(text))


def paragraphs(text: str):
    """Абзацы JA-файла без маркеров (пустые строки — границы абзацев)."""
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _body(text: str) -> str:
    """Текст без строки заголовка главы (заголовок учитывается отдельно)."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].lstrip().startswith("#"):
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
    return "\n".join(lines[i:]).strip()


# ---------------------------------------------------------------------------
# Сопоставление
# ---------------------------------------------------------------------------

def approximate_ja_blocks(ja_paras, ru_sizes):
    """JA без маркеров: раздать абзацы по блокам RU пропорционально объёму.

    Возвращает список списков абзацев той же длины, что и ru_sizes.
    """
    if not ru_sizes:
        return [[]]
    total_ru = sum(ru_sizes) or 1
    total_ja = sum(len(p) for p in ja_paras)
    result = [[] for _ in ru_sizes]
    acc_ru, acc_ja, idx = 0, 0, 0
    last = len(ru_sizes) - 1
    for i, size in enumerate(ru_sizes):
        acc_ru += size
        limit = total_ja * acc_ru / total_ru
        while idx < len(ja_paras) and acc_ja < limit and i != last:
            acc_ja += len(ja_paras[idx])
            result[i].append(ja_paras[idx])
            idx += 1
    for para in ja_paras[idx:]:          # остаток — в последний блок
        result[last].append(para)
    return result


def build_pairs(ru_blocks, ja_body, ja_blocks, ja_has_markers):
    """-> (пары [(номер, JA-текст, RU-текст, флаг_приблизительности)], заметки)."""
    notes = []
    if ja_has_markers:
        pairs = []
        for num in sorted(set(ru_blocks) | set(ja_blocks)):
            pairs.append((num, ja_blocks.get(num, ""), ru_blocks.get(num, ""), False))
        if set(ru_blocks) != set(ja_blocks):
            only_ru = sorted(set(ru_blocks) - set(ja_blocks))
            only_ja = sorted(set(ja_blocks) - set(ru_blocks))
            if only_ru:
                notes.append("Блоки только в output (JA-стороны нет): %s"
                             % ", ".join(map(str, only_ru)))
            if only_ja:
                notes.append("Блоки только в JA (нет в output): %s"
                             % ", ".join(map(str, only_ja)))
        return pairs, notes

    # JA без маркеров блоков — приблизительное выравнивание по объёму текста
    notes.append("JA-файл не разбит на блоки: JA-абзацы распределены по блокам "
                 "output ПРИБЛИЗИТЕЛЬНО (пропорционально объёму текста).")
    paras = paragraphs(ja_body)
    ru_list = list(ru_blocks.items()) or [(1, "")]
    sizes = [len(t) for _, t in ru_list]
    groups = approximate_ja_blocks(paras, sizes)
    pairs = []
    for (num, ru_text), group in zip(ru_list, groups):
        pairs.append((num, "\n\n".join(group), ru_text, True))
    return pairs, notes


# ---------------------------------------------------------------------------
# Рендер
# ---------------------------------------------------------------------------

def render(slug, ru_path, ru_title, ja_path, ja_title, pairs, notes):
    lines = []
    lines.append("# %s — output ↔ японский оригинал" % slug)
    lines.append("")
    lines.append("Файл собран `tools/pair_blocks.py` для передачи стороннему ИИ. "
                 "Единица — блок: сначала японский оригинал, затем то, что "
                 "получилось в output. Копировать можно один блок — от "
                 "`<!-- block: N -->` до `===== КОНЕЦ БЛОКА N =====`.")
    lines.append("")
    lines.append("- JA (оригинал): `%s` — %s" % (ja_path, ja_title or "(без заголовка)"))
    lines.append("- OUTPUT (RU):   `%s` — %s" % (ru_path, ru_title or "(без заголовка)"))
    approx = sum(1 for *_x, a in pairs if a)
    lines.append("- Блоков: %d%s%s"
                 % (len(pairs),
                    "; приблизительное выравнивание JA — в блоках: %d" % approx
                    if approx else "",
                    "; заметки: %d" % len(notes) if notes else ""))
    for note in notes:
        lines.append("- ⚠ %s" % note)
    lines.append("")
    lines.append("---")
    lines.append("")

    for num, ja_text, ru_text, _approx in pairs:
        lines.append("<!-- block: %d -->" % num)
        lines.append("")
        lines.append("===== %s =====" % LABEL_JA)
        lines.append(ja_text if ja_text.strip() else "(нет текста на стороне JA)")
        lines.append("")
        lines.append("===== %s =====" % LABEL_OUT)
        lines.append(ru_text if ru_text.strip() else "(нет текста на стороне output)")
        lines.append("")
        lines.append("===== КОНЕЦ БЛОКА %d =====" % num)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Слаг и каталоги
# ---------------------------------------------------------------------------

def norm_slug(raw: str) -> str:
    """`6-ch03` / `v6-ch03` / `v06-ch03` -> `v6-ch03`."""
    s = raw.strip().removesuffix(".md")
    m = re.fullmatch(r"v?0*(\d+)-(.+)", s)
    return "v%s-%s" % (m.group(1), m.group(2)) if m else s


def available_slugs(project: Path):
    out = {p.stem for p in (project / "output").glob("*.md")}
    ja = {p.stem for p in (project / "translates" / "ja").glob("*.md")}
    return sorted(out | ja), sorted(out & ja)


# ---------------------------------------------------------------------------
# Основной сценарий
# ---------------------------------------------------------------------------

def pair_chapter(slug, project: Path):
    """Собрать пары главы. -> (файл-текст, список заметок) или ValueError."""
    ru_path = project / "output" / (slug + ".md")
    ja_path = project / "translates" / "ja" / (slug + ".md")
    if not ru_path.exists():
        raise ValueError("нет файла output: %s" % ru_path)
    if not ja_path.exists():
        raise ValueError("нет японского оригинала: %s (см. --list)" % ja_path)

    ru_title, ru_blocks, _ru_mk = parse_chapter(ru_path)
    ja_title, ja_blocks, ja_mk = parse_chapter(ja_path)
    ja_body = _body(ja_path.read_text(encoding="utf-8"))
    notes_head = []

    if not ru_blocks:
        # output без маркеров блоков (например, послесловие): весь текст — блок 1
        ru_body = _body(ru_path.read_text(encoding="utf-8"))
        if not ru_body:
            raise ValueError("пустой файл output: %s" % ru_path)
        ru_blocks = OrderedDict([(1, ru_body)])
        notes_head.append("Файл output не разбит на <!-- block: N --> — "
                          "весь текст собран в блок 1.")
    if not ja_body:
        notes_head.append("JA-файл содержит только заголовок — японской "
                          "стороны нет.")

    pairs, notes = build_pairs(ru_blocks, ja_body, ja_blocks, ja_mk)
    notes = notes_head + notes
    text = render(slug,
                  os.path.relpath(ru_path, ROOT), ru_title,
                  os.path.relpath(ja_path, ROOT), ja_title,
                  pairs, notes)
    return text, notes, len(pairs)


def cmd_pair(args) -> int:
    project = Path(args.project)
    if args.list_mode:
        all_slugs, both = available_slugs(project)
        for slug in all_slugs:
            mark = "OK " if slug in both else "-- "
            print("%s%s" % (mark, slug))
        return 0

    if not args.slug:
        print("Укажи слаг главы: python tools/pair_blocks.py v6-ch03 "
              "(или --list)", file=sys.stderr)
        return 2
    slug = norm_slug(args.slug)
    try:
        text, notes, n_blocks = pair_chapter(slug, project)
    except ValueError as exc:
        print("ОШИБКА: %s" % exc, file=sys.stderr)
        return 2

    if args.out:
        out_path = Path(args.out)
    else:
        out_path = Path(args.out_dir) / ("%s.md" % slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")

    if not args.quiet:
        print("Готово: %s (блоков: %d)" % (out_path, n_blocks))
        for note in notes:
            print("  ⚠ %s" % note)
    return 0


# ---------------------------------------------------------------------------
# Самопроверка
# ---------------------------------------------------------------------------

def cmd_self_test(_args) -> int:
    checks = []

    def check(name, ok):
        checks.append((name, bool(ok)))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        project = root / "proj"
        (project / "output").mkdir(parents=True)
        (project / "translates" / "ja").mkdir(parents=True)

        ru = ("# Глава 1: тест\n\n"
              "<!-- block: 1 -->\n\nРеплика номер один.\n\nВторой абзац.\n\n"
              "<!-- block: 2 -->\n\nВторой блок RU.\n")
        ja = ("# 第一章 テスト\n\n"
              "<!-- block: 1 -->\n\n一番目の発言。\n\n二番目の段落。\n\n"
              "<!-- block: 2 -->\n\n二番目のブロック。\n")
        (project / "output" / "v9-ch01.md").write_text(ru, encoding="utf-8")
        (project / "translates" / "ja" / "v9-ch01.md").write_text(ja,
                                                                   encoding="utf-8")

        text, notes, n = pair_chapter("v9-ch01", project)
        check("пары по блокам: 2", n == 2)
        check("JA в паре 1", "一番目の発言。" in text)
        check("OUTPUT в паре 1", "Реплика номер один." in text)
        check("JA идёт раньше OUTPUT", text.index("一番目の発言。")
              < text.index("Реплика номер один."))
        check("закрывающая метка блока", "===== КОНЕЦ БЛОКА 2 =====" in text)
        check("нет ложных заметок", not notes)
        check("заголовок главы в файле", "第一章 テスト" in text
              and "Глава 1: тест" in text)
        check("заголовки не дублируются в блоках",
              text.count("第一章 テスト") == 1
              and text.count("Глава 1: тест") == 1)
        check("нормализация слага", norm_slug("09-ch01") == "v9-ch01"
              and norm_slug("v9-ch01.md") == "v9-ch01")

        # JA без маркеров блоков -> приблизительное выравнивание
        ja_plain = "# 第二章\n\n%s\n" % "\n\n".join(
            "日本の段落%d。" % i for i in range(1, 21))
        (project / "translates" / "ja" / "v9-ch02.md").write_text(ja_plain,
                                                                   encoding="utf-8")
        ru2 = ("# Глава 2\n\n<!-- block: 1 -->\n\n%s\n\n"
               "<!-- block: 2 -->\n\n%s\n" % ("A" * 100, "B" * 100))
        (project / "output" / "v9-ch02.md").write_text(ru2, encoding="utf-8")
        text2, notes2, n2 = pair_chapter("v9-ch02", project)
        check("JA без маркеров: те же 2 блока", n2 == 2)
        check("JA без маркеров: заметка выдана", any("ПРИБЛИЗИТЕЛЬНО" in x
                                                     for x in notes2))
        check("JA без маркеров: все абзацы попали в файл",
              sum(1 for i in range(1, 21) if ("日本の段落%d。" % i) in text2) == 20)
        check("заголовок JA не дублируется в блоках",
              text2.count("第二章") == 1)

        # блок только на одной стороне
        ru3 = ("# Глава 3\n\n<!-- block: 1 -->\n\nТолько RU.\n\n"
               "<!-- block: 2 -->\n\nЕщё RU.\n")
        ja3 = "# 第三章\n\n<!-- block: 1 -->\n\nJAだけ。\n"
        (project / "output" / "v9-ch03.md").write_text(ru3, encoding="utf-8")
        (project / "translates" / "ja" / "v9-ch03.md").write_text(ja3,
                                                                   encoding="utf-8")
        text3, notes3, n3 = pair_chapter("v9-ch03", project)
        check("односторонний блок сохранён", n3 == 2)
        check("односторонний блок помечен",
              "(нет текста на стороне JA)" in text3)
        check("заметка о блоке без JA", any("только в output" in x for x in notes3))

        # отсутствующий JA -> ValueError
        (project / "output" / "v9-ch04.md").write_text(
            "# X\n\n<!-- block: 1 -->\n\nТекст.\n", encoding="utf-8")
        try:
            pair_chapter("v9-ch04", project)
            check("нет JA -> ошибка", False)
        except ValueError:
            check("нет JA -> ошибка", True)

        # output без маркеров блоков + JA только с заголовком
        (project / "output" / "v9-ch05.md").write_text(
            "# Послесловие\n\nАбзац один.\n\nАбзац два.\n", encoding="utf-8")
        (project / "translates" / "ja" / "v9-ch05.md").write_text(
            "# あとがき\n", encoding="utf-8")
        text5, notes5, n5 = pair_chapter("v9-ch05", project)
        check("output без маркеров: один блок", n5 == 1)
        check("output без маркеров: заметка", any("собран в блок 1" in x
                                                  for x in notes5))
        check("пустой JA: заметка", any("только заголовок" in x for x in notes5))
        check("пустой JA: текст на стороне output цел",
              "Абзац один." in text5 and "Абзац два." in text5)

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print("  [%s] %s" % ("OK" if ok else "FAIL", name))
    if failed:
        print("\nSELF-TEST: ПРОВАЛЕНО %d из %d" % (len(failed), len(checks)))
        return 1
    print("\nSELF-TEST: все %d проверок пройдены." % len(checks))
    return 0


# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="pair_blocks.py",
        description="Один файл «output ↔ японский оригинал» по блокам — "
                    "для передачи стороннему ИИ.")
    ap.add_argument("slug", nargs="?", default=None,
                    help="слаг главы, например v6-ch03")
    ap.add_argument("--list", dest="list_mode", action="store_true",
                    help="показать доступные слаги и выйти")
    ap.add_argument("--project", default=str(ROOT / "AINovelEdit"),
                    help="каталог проекта (по умолчанию AINovelEdit)")
    ap.add_argument("--out-dir", default=str(ROOT / "pairs"),
                    help="куда писать файл, если не задан --out "
                         "(по умолчанию <корень>/pairs)")
    ap.add_argument("--out", default=None, help="путь итогового файла")
    ap.add_argument("--quiet", action="store_true", help="без вывода в консоль")
    ap.add_argument("--self-test", action="store_true",
                    help="самопроверка на временных файлах")
    return ap


def main(argv=None) -> int:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    if args.self_test:
        return cmd_self_test(args)
    return cmd_pair(args)


if __name__ == "__main__":
    raise SystemExit(main())
