#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merged_io.py — общий парсер трёхъязычного merged-файла.

Поддерживает ДВА формата (для совместимости со старыми томами):

  * новый (блочный):  `## Блок N` + многострочные поля
        ## Блок 7
        **JA:**
        <абзац 1>
        <абзац 2>
  * старый (абзацный): `## Абзац N` + однострочные поля
        ## Абзац 7
        **JA:** текст

Единица чтения — блок/абзац с полями JA / EN / RU / ED_RU. Значение поля
может занимать несколько строк (новый формат); поля разделяются заголовком
следующего поля или следующим `## Блок/Абзац`.
"""
from __future__ import annotations

import re
from pathlib import Path

HEADER_RE = re.compile(r"^##\s*(?:Блок|Абзац)\s+(\d+)\s*$", re.M)
FIELD_RE = re.compile(
    r"^\*\*(JA|EN|RU|ED_RU):\*\*[ \t]*(.*?)"
    r"(?=^\*\*(?:JA|EN|RU|ED_RU):\*\*|^##\s|\Z)",
    re.M | re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def clean(text):
    """Убирает HTML-комментарии и лишние пробелы."""
    return COMMENT_RE.sub(" ", text or "").strip()


def read_merged(path):
    """Возвращает список (номер_блока, {поле: текст}) из merged-файла."""
    text = Path(path).read_text(encoding="utf-8")
    marks = list(HEADER_RE.finditer(text))
    items = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        chunk = text[m.end():end]
        fields = {"JA": "", "EN": "", "RU": "", "ED_RU": ""}
        for key, val in FIELD_RE.findall(chunk):
            fields[key] = val.strip()
        items.append((int(m.group(1)), fields))
    return items


def is_block_format(path):
    """True, если merged-файл в новом (блочном) формате."""
    text = Path(path).read_text(encoding="utf-8")
    return re.search(r"^##\s*Блок\s+\d+\s*$", text, re.M) is not None


def read_source_blocks(path):
    """Читает блоки исходного файла translates/{ja,en,ru} или output/.

    Возвращает список (номер_блока, [абзацы]). Если маркеров нет —
    возвращает (None, [все абзацы]) как единый список.
    """
    text = Path(path).read_text(encoding="utf-8")
    if "<!-- block:" not in text:
        paras = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
        paras = [p for p in paras if not p.startswith("# ")]
        return None, paras
    blocks = []
    cur_num = None
    cur = []
    for line in text.splitlines():
        m = re.match(r"^<!--\s*block:\s*(\d+)\s*-->\s*$", line.strip())
        if m:
            if cur_num is not None:
                blocks.append((cur_num, cur))
            cur_num = int(m.group(1))
            cur = []
        elif line.strip() == "":
            continue
        elif line.startswith("# "):
            continue
        elif line.strip().startswith("<!--"):
            continue
        else:
            cur.append(line.strip())
    if cur_num is not None:
        blocks.append((cur_num, cur))
    return blocks, None