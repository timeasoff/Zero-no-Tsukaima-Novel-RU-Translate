#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merged_io.py — общий разбор трёхъязычного merged-файла (единица — смысловой
блок) и блок-файлов `translates/{ja,en,ru}` / `output/`.

Формат merged (генерируется tools/normalize.py и scripts/update_merged.py):

    ## Блок 7

    **JA:**
    <абзац 1>
    <абзац 2>

    **EN:**
    <абзац 1>

    **RU:**
    …

    **ED_RU:**
    …

Значение поля может занимать несколько строк; поля разделяются заголовком
следующего поля или следующим `## Блок`.

Формат блок-файлов: `# Заголовок`, затем блоки, разделённые маркером
`<!-- block: N -->`, внутри блока — абзацы, разделённые пустой строкой.
"""
from __future__ import annotations

import re
from pathlib import Path

HEADER_RE = re.compile(r"^##\s*Блок\s+(\d+)\s*$", re.M)
FIELD_RE = re.compile(
    r"^\*\*(JA|EN|RU|ED_RU):\*\*[ \t]*(.*?)"
    r"(?=^\*\*(?:JA|EN|RU|ED_RU):\*\*|^##\s|\Z)",
    re.M | re.S)
BLOCK_MARK_RE = re.compile(r"^<!--\s*block:\s*(\d+)\s*-->\s*$")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def clean(text):
    """Убирает HTML-комментарии и лишние пробелы."""
    return COMMENT_RE.sub(" ", text or "").strip()


def has_block_markers(path):
    """True, если файл размечен смысловыми блоками (`<!-- block: N -->`)."""
    try:
        return BLOCK_MARK_RE.search(Path(path).read_text(encoding="utf-8")) is not None
    except OSError:
        return False


def read_merged(path):
    """Возвращает список (номер_блока, {поле: текст}) из merged-файла."""
    text = Path(path).read_text(encoding="utf-8")
    marks = list(HEADER_RE.finditer(text))
    items = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        fields = {"JA": "", "EN": "", "RU": "", "ED_RU": ""}
        for key, val in FIELD_RE.findall(text[m.end():end]):
            fields[key] = val.strip()
        items.append((int(m.group(1)), fields))
    return items


def read_source_blocks(path):
    """Читает блок-файл (translates/* или output/*) → [(номер_блока, [абзацы])].

    Возвращает пустой список, если файла нет или он не размечен блоками
    (такие тома считаются завершёнными/неподдерживаемыми, см. completed.md).
    """
    p = Path(path)
    if not p.exists():
        return []
    blocks = []
    cur_num, cur = None, []
    for line in p.read_text(encoding="utf-8").splitlines():
        m = BLOCK_MARK_RE.match(line.strip())
        if m:
            if cur_num is not None:
                blocks.append((cur_num, cur))
            cur_num, cur = int(m.group(1)), []
        elif line.strip() == "" or line.startswith("# ") or line.strip().startswith("<!--"):
            continue
        else:
            cur.append(line.strip())
    if cur_num is not None:
        blocks.append((cur_num, cur))
    return blocks
