#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semantic_blocks.py — построение смысловых блоков (микросцен) и кросс-языковых
якорей для нормализации томов (используется tools/normalize.py).

Единица обработки — СМЫСЛОВОЙ БЛОК, а не абзац. Блок = кластер соседних
абзацев одного языка, объединённых одним действием/говорящим (реплика +
атрибуция, диалоговая пара, короткая наррация вокруг реплики). Блоки
нумеруются и переносятся во все языки: JA, EN и RU сравниваются по блокам,
поэтому расхождение абзацной разбивки между языками перестаёт «съезжать»
на всю главу (именно этот дефект давала прежняя EN-якорная абзацная сетка).

Модуль не зависит от normalize.py: только стандартная библиотека и re.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Маркеры речи и завершённости (JA)
# ---------------------------------------------------------------------------

_JA_OPEN = "「『"        # японские кавычки прямой речи
_JA_CLOSE = "」』"
_TERMINALS = "。！？!?…"


def is_speech(text):
    """Абзац открывается японской кавычкой прямой речи (с учётом пробелов)."""
    s = text.lstrip()
    return bool(s) and s[0] in _JA_OPEN


def closes_speech(text):
    """Абзац завершается закрывающей кавычкой речи (возможно с точкой)."""
    s = text.rstrip()
    while s and s[-1] in _TERMINALS:
        s = s[:-1].rstrip()
    return bool(s) and s[-1] in _JA_CLOSE


def ends_terminal(text):
    """Абзац завершён знаком конца предложения или закрытой речью."""
    s = text.rstrip()
    if not s:
        return True
    if s[-1] in _TERMINALS or s[-1] in _JA_CLOSE:
        return True
    return False


def _soft_boundary(prev, nxt, narr_max):
    """Мягкая ли граница между соседними абзацами (=> объединять в блок)."""
    if not prev or not nxt:
        return False
    # 1) незавершённая мысль: абзац не закончился — продолжение
    if not ends_terminal(prev):
        return True
    # 2) диалоговый ряд / ответная реплика
    if is_speech(prev) and (is_speech(nxt) or len(nxt) <= narr_max):
        return True
    # 3) наррация-атрибуция перед репликой
    if is_speech(nxt) and len(prev) <= narr_max:
        return True
    return False


DEFAULT_PARAMS = {
    "narr_max": 90,      # порог «короткой» наррации для склейки с репликой
    "max_paras": 8,      # максимум абзацев в одном блоке
    "max_chars": 700,    # максимум символов в одном блоке
}


def cluster_blocks(paras, narr_max=None, max_paras=None, max_chars=None):
    """Кластеризует абзацы одного языка в смысловые блоки (микросцены).

    Возвращает список блоков, каждый блок — список индексов абзацев
    (индексы возрастают, блоки покрывают все абзацы без потерь).
    """
    p = dict(DEFAULT_PARAMS)
    if narr_max is not None:
        p["narr_max"] = narr_max
    if max_paras is not None:
        p["max_paras"] = max_paras
    if max_chars is not None:
        p["max_chars"] = max_chars

    blocks = []
    cur = []
    cur_chars = 0
    for i, para in enumerate(paras):
        cur.append(i)
        cur_chars += len(para)
        if i + 1 >= len(paras):
            break
        cont = _soft_boundary(para, paras[i + 1], p["narr_max"])
        if (not cont or len(cur) >= p["max_paras"]
                or cur_chars >= p["max_chars"]):
            blocks.append(cur)
            cur = []
            cur_chars = 0
    if cur:
        blocks.append(cur)
    return blocks


# ---------------------------------------------------------------------------
# Трёхъязычные якоря из dictionary.md
# ---------------------------------------------------------------------------
# Столбцы словаря: Японский | Английский | Русский (канон) | Примечание.
# Один и тот же термин в трёх языках получает ОДИН общий токен-якорь
# (g:<JA>), поэтому он «зацепляет» соответствие JA↔EN↔RU напрямую, в отличие
# от прежних якорей только по длине и числам.

_DICT_HEADER = {"японский", "日本語", "english", "английский", "русский"}


def load_glossary(path):
    """Читает dictionary.md → список {'ja','en','ru','key'}.

    Строки-заголовки и разделители пропускаются; «—» в русской колонке
    трактуется как отсутствие формы.
    """
    entries = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return entries
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        ja, en, ru = cells[0], cells[1], cells[2]
        if not ja or set(ja) <= set("- :"):
            continue                       # строка-разделитель
        if ja.lower() in _DICT_HEADER:
            continue                       # заголовок таблицы
        if len(ja.strip()) < 2:
            continue                       # односложный термин даёт ложные якоря
        if ru in ("—", "-", ""):
            ru = ""
        entries.append({"ja": ja, "en": en, "ru": ru, "key": "g:" + ja})
    return entries


_WORD_LAT = r"[A-Za-zА-Яа-яЁё]"


def _has_lat(text, term):
    pat = r"(?<!%s)%s(?!%s)" % (_WORD_LAT, re.escape(term), _WORD_LAT)
    return re.search(pat, text, re.I) is not None


# --- числа как кросс-языковой якорь -----------------------------------------
# EN/RU пишут «10,000», JA — «一万»: без нормализации числа не совпадают,
# и в плотных диалогах (обычно именно про числа и меры) выравнивание уплывает.
_NUM_RE = re.compile(r"\d[\d,\.\s]*\d|\d")
_JA_NUM_CHARS = "〇一二三四五六七八九十百千万億"
_JA_DIG = {"〇": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
           "六": 6, "七": 7, "八": 8, "九": 9}


def ja_to_int(s):
    """Японское числительное (一万, 七万, 千, 十, 一万二千) → int."""
    if not s:
        return None
    total, section, num = 0, 0, 0
    for ch in s:
        if ch in _JA_DIG:
            num = _JA_DIG[ch]
        elif ch == "十":
            section += (num or 1) * 10
            num = 0
        elif ch == "百":
            section += (num or 1) * 100
            num = 0
        elif ch == "千":
            section += (num or 1) * 1000
            num = 0
        elif ch == "万":
            total += (section + num or 1) * 10000
            section, num = 0, 0
        elif ch == "億":
            total += (section + num or 1) * 100000000
            section, num = 0, 0
    return total + section + num or None


def number_anchors(text, lang):
    """Числовые якоря: арабские цифры (с ,/пробелами) + японские числительные."""
    out = set()
    if not text:
        return out
    for m in _NUM_RE.findall(text):
        digits = re.sub(r"[,\s\.]", "", m)
        if digits.isdigit():
            out.add("\0" + str(int(digits)))
    if lang == "ja":
        for m in re.findall("[%s]+" % _JA_NUM_CHARS, text):
            n = ja_to_int(m)
            if n:
                out.add("\0" + str(n))
    return out


def glossary_anchors(text, entries, lang):
    """Множество токенов-якорей для текста на языке lang ∈ {ja, en, ru}.

    Словарные термины (общий ключ g:<JA> во всех языках) + числа
    (арабские и японские, приведённые к одному виду).
    """
    out = number_anchors(text, lang)
    if not text:
        return out
    for e in entries:
        term = e.get(lang) or ""
        if not term:
            continue
        if lang == "ja":
            if term in text:
                out.add(e["key"])
        elif _has_lat(text, term):
            out.add(e["key"])
    return out


def anchors_for(text, entries, lang):
    """Якоря текста: словарные (трилингвальные) + числа."""
    return glossary_anchors(text, entries, lang)