#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
completed.py — реестр завершённых (замороженных) томов.

Завершённые тома — источник истины при расхождениях терминов/имён/обращений.
Их текст не редактируется и не нормализуется повторно. Список ведётся
в `AINovelEdit/completed.md` (машиночитаемые строки таблицы: `| NN | …`).

Использование:
    from completed import is_frozen, frozen_volumes
"""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
REGISTRY = BASE / "completed.md"

_ROW = re.compile(r"^\|\s*(\d{1,3})\s*\|")


def frozen_volumes(path=None):
    """Множество номеров замороженных томов из реестра."""
    p = Path(path) if path else REGISTRY
    try:
        text = p.read_text(encoding="utf-8")
    except OSError:
        return set()
    out = set()
    for line in text.splitlines():
        m = _ROW.match(line.strip())
        if m:
            out.add(int(m.group(1)))
    return out


def is_frozen(vol, path=None):
    """True, если том завершён (заморожен) и не подлежит обработке."""
    try:
        return int(vol) in frozen_volumes(path)
    except (TypeError, ValueError):
        return False


def volume_of(name):
    """Номер тома из имени файла ('v14-ch01.md' → 14) или None."""
    m = re.match(r"v(\d{1,3})-", str(name))
    return int(m.group(1)) if m else None