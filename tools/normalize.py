#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize.py — нормализация сырых исходников тома (JA epub / EN pdf / RU docx)
в markdown-файлы проекта AINovelEdit, выровненные по СМЫСЛОВЫМ БЛОКАМ.

Смысловой блок (микросцена) — кластер соседних абзацев, объединённых одним
действием/говорящим (реплика + атрибуция, диалоговая пара). Блоки нумеруются
маркером `<!-- block: N -->` и одинаковы во всех языках: перевод и сравнение
идут по блокам, а не по «абзац №N». Именно блочная единица даёт устойчивое
соответствие JA/EN/RU: одна и та же микросцена, а не «строка N».

Внутри блока абзацы языка могут не совпадать по числу и границам — это норма.

Завершённые тома (см. AINovelEdit/completed.md) не нормализуются повторно.

Использование (из корня репозитория, где лежат origs/ и AINovelEdit/):
    python tools/normalize.py --volume 15
    python tools/normalize.py --volume 15 --out tmp_test   # не трогать проект
"""
import argparse
import os
import re
import sys
import zipfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import semantic_blocks as sb  # noqa: E402

KANJI_DIGITS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
                "六": 6, "七": 7, "八": 8, "九": 9}


def kanji_to_int(s):
    s = s.strip()
    if s.isdigit():
        return int(s)
    if "百" in s or "千" in s:
        return None
    m = re.fullmatch(r"([一二三四五六七八九]?)十([一二三四五六七八九])?", s)
    if m:
        tens = KANJI_DIGITS.get(m.group(1), 1) if m.group(1) else 1
        ones = KANJI_DIGITS.get(m.group(2), 0) if m.group(2) else 0
        return tens * 10 + ones
    return KANJI_DIGITS.get(s)


def clean_ws(s):
    s = s.replace("\u00a0", " ").replace("\u2007", " ").replace("\u3000", " ")
    return re.sub(r"\s+", " ", s).strip()


@dataclass
class Section:
    kind: str           # chapter / prologue / epilogue / afterword
    number: object      # int | None
    title: str
    paras: list = field(default_factory=list)
    story: object = None   # № рассказа в сборнике (EN «Story N» / RU «История N»)

    @property
    def slug(self):
        if self.kind == "chapter" and self.number:
            return "ch%02d" % self.number
        return {"prologue": "prologue", "epilogue": "epilogue",
                "afterword": "afterword"}.get(self.kind, "other")


# ----------------------------- JA (epub) -----------------------------------

JA_HEADING_RE = re.compile(
    r"^(第\s*([0-9一二三四五六七八九十百]+)\s*[章話]|(プロローグ|エピローグ|まえがき|あとがき|後書き))")
JA_STOP_RE = re.compile(r"^(奥付|発行|CREDIT)")


class JaParagraphs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.paras = []      # (text, classes)
        self._buf = None
        self._cls = ""
        self._skip = 0       # внутри <rt>/<rp>

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self._buf = []
            self._cls = dict(attrs).get("class", "")
        elif tag in ("rt", "rp") and self._buf is not None:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("rt", "rp"):
            self._skip = max(0, self._skip - 1)
        elif tag == "p" and self._buf is not None:
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            self.paras.append((text, self._cls))
            self._buf = None

    def handle_data(self, data):
        if self._buf is not None and self._skip == 0:
            self._buf.append(data)


def extract_ja(path):
    sections = []
    cur = None
    with zipfile.ZipFile(path) as z:
        opf = z.read("item/standard.opf").decode("utf-8")
        manifest = dict(re.findall(
            r'<item[^>]*id="([^"]+)"[^>]*href="([^"]+)"', opf))
        spine = re.findall(r'idref="([^"]+)"',
                           re.search(r"<spine[^>]*>(.*?)</spine>", opf, re.S).group(1))
        for item_id in spine:
            href = manifest.get(item_id, "")
            if not href.endswith(".xhtml"):
                continue
            fname = href.split("/")[-1]
            if re.search(r"titlepage|credit|cover|bookwalker|colophon", fname):
                continue
            x = z.read("item/" + href).decode("utf-8")
            x = re.sub(r"<rt[^>]*>.*?</rt>", "", x, flags=re.S)
            x = re.sub(r"<rp[^>]*>.*?</rp>", "", x, flags=re.S)
            p = JaParagraphs()
            p.feed(x)
            stop_file = False
            for text, cls in p.paras:
                if not text:
                    continue
                if cls and re.search(r"mfont|bold", cls) and JA_HEADING_RE.match(text):
                    m = JA_HEADING_RE.match(text)
                    num = kanji_to_int(m.group(2)) if m.group(2) else None
                    kind = ("chapter" if num else
                            {"プロローグ": "prologue", "エピローグ": "epilogue",
                             "あとがき": "afterword", "後書き": "afterword",
                             "まえがき": "prologue"}.get(m.group(3), "other"))
                    if kind == "other" and JA_STOP_RE.match(text):
                        cur = None
                        stop_file = True
                        break
                    cur = Section(kind, num, text)
                    sections.append(cur)
                    continue
                if re.fullmatch(r"\d{1,3}", text):
                    continue
                if cur is not None:
                    cur.paras.append(text)
            if stop_file:
                break
    return sections

# ----------------------------- EN (pdf) ------------------------------------

EN_HEAD_RE = re.compile(
    r"^(?:Chapter\s+(?P<num>\d+|[Oo]ne|[Tt]wo|[Tt]hree|[Ff]our|[Ff]ive|[Ss]ix|"
    r"[Ss]even|[Ee]ight|[Nn]ine|[Tt]en|[Ee]leven|[Tt]welve|[Tt]hirteen|"
    r"[Ff]ourteen|[Ff]ifteen|[Ss]ixteen|[Ss]eventeen|[Ee]ighteen|[Nn]ineteen|"
    r"[Tt]wenty)\s*[:.]?\s*|(?P<word>Prologue|Epilogue|Afterword|Interlude))"
    r"(?P<rest>.*)$")

EN_WORD_NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20,
}

# Сборники (том 5, 12): «Story 1: …» — граница рассказа, главы внутри него
# нумеруются заново. Заголовок может переноситься на следующую строку.
EN_STORY_RE = re.compile(r"^Story\s*(\d+)\s*[:.]", re.I)


def _ends_sentence(s):
    return bool(re.search(r'[.!?…:;]["»\'”’)]?\s*$', s))


def extract_en(path):
    sections = []
    cur = None
    carry = ""   # незавершённый абзац, продолжающийся на следующей странице
    cur_story = None      # текущий рассказ сборника («Story N»)
    story_title = False   # продолжение заголовка «Story N: …»
    doc = pymupdf.open(path)
    for page in doc:
        blocks = sorted(page.get_text("blocks"), key=lambda b: (b[1], b[0]))
        for b in blocks:
            raw = re.sub(r"(\w)-\n(\w)", r"\1\2", b[4])
            lines = []
            for line in raw.splitlines():
                line = clean_ws(line)
                if not line or re.fullmatch(r"\d{1,3}", line):
                    continue
                lines.append(line)
            if not lines:
                continue
            buf = []
            for line in lines:
                m = EN_HEAD_RE.match(line)
                if m and len(line) < 120:
                    # заголовок главы: сбрасываем накопленный текст
                    story_title = False
                    if buf:
                        if cur is not None:
                            cur.paras.append(" ".join(buf))
                        buf = []
                    num = m.group("num")
                    if num is not None:
                        kind = "chapter"
                        num = (int(num) if num.isdigit()
                               else EN_WORD_NUM[num.lower()])
                    else:
                        kind = m.group("word").lower()
                        num = None
                    cur = Section(kind, num, line, story=cur_story)
                    sections.append(cur)
                    continue
                ms = EN_STORY_RE.match(line)
                if ms and len(line) < 120:
                    # граница рассказа: заголовок не текст главы
                    cur_story = int(ms.group(1))
                    story_title = True
                    continue
                if story_title:
                    continue      # вторая строка перенесённого «Story N: …»
                buf.append(line)
            if not buf:
                continue
            text = " ".join(buf)
            if carry:
                text = carry + " " + text
                carry = ""
            if cur is not None:
                cur.paras.append(text)
        # абзац оборван на границе страниц — переносим на следующую
        if cur is not None and cur.paras and not _ends_sentence(cur.paras[-1]):
            carry = cur.paras.pop()
    return sections


# ----------------------------- RU (docx) -----------------------------------

RU_HEAD_RE = re.compile(r"^(Глава|Пролог|Эпилог|Послесловие)\s*(\d+)?\s*[:.]?\s*(.*)$")
# «Глава первая: Фон Цербст» (том 11) — номер главы словом
RU_WORD_NUM = {"первая": 1, "вторая": 2, "третья": 3, "четвертая": 4,
               "четвёртая": 4, "пятая": 5, "шестая": 6, "седьмая": 7,
               "восьмая": 8, "девятая": 9, "десятая": 10, "одиннадцатая": 11,
               "двенадцатая": 12, "тринадцатая": 13, "четырнадцатая": 14,
               "пятнадцатая": 15, "шестнадцатая": 16, "семнадцатая": 17,
               "восемнадцатая": 18, "девятнадцатая": 19, "двадцатая": 20}
# Сборники без «Глава N» (том 5): «История N: …» / «Часть M».
RU_PART_RE = re.compile(r"^Часть\s*(\d+)\b", re.I)
RU_STORY_RE = re.compile(r"^История\s*(\d+)\s*[:：]", re.I)
# приложение/примечания — словарные приложения, в текст глав не входят
RU_STOP_RE = re.compile(r"[Пп]римечани|[Пп]риложени")


def _ru_chapter_number(text):
    """Номер главы из заголовка: цифра, иначе порядковое слово («первая»)."""
    m = re.match(r"^Глава\s*(\d+)", text)
    if m:
        return int(m.group(1))
    m = re.match(r"^Глава\s*([^\s:.\d]+)", text)
    if m:
        return RU_WORD_NUM.get(m.group(1).lower())
    return None


def _docx_read(z, name):
    """Чтение части docx, терпимое к битым CRC (в исходниках повреждены
    картинки word/media/*.jpeg — python-docx роняет весь разбор на них,
    хотя текст лежит в word/document.xml и цел)."""
    try:
        with z.open(name) as f:
            return f.read()
    except (zipfile.BadZipFile, zipfile.LargeZipFile, OSError) as e:
        raise SystemExit("docx: не удалось прочитать %s — %s" % (name, e))


def _docx_paragraphs(path):
    """Абзацы docx как (текст, имя стиля) — без загрузки медиафайлов.

    Эквивалент `Document(path).paragraphs` (только абзацы верхнего уровня
    body), но читает OOXML напрямую: не зависит от целостности картинок и
    от того, как python-docx регистрирует встроенные имена стилей."""
    import xml.etree.ElementTree as ET

    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(path) as z:
        styles_xml = _docx_read(z, "word/styles.xml")
        doc_xml = _docx_read(z, "word/document.xml")
    id2name = {}
    for st in ET.fromstring(styles_xml).iter(W + "style"):
        sid = st.get(W + "styleId")
        nm = st.find(W + "name")
        id2name[sid] = nm.get(W + "val") if nm is not None else sid
    body = ET.fromstring(doc_xml).find(W + "body")
    out = []
    if body is None:
        return out
    for child in body:
        if child.tag != W + "p":
            continue
        sid = None
        pPr = child.find(W + "pPr")
        if pPr is not None:
            ps = pPr.find(W + "pStyle")
            if ps is not None:
                sid = ps.get(W + "val")
        parts = []
        for el in child.iter():
            if el.tag == W + "t":
                parts.append(el.text or "")
            elif el.tag == W + "tab":
                parts.append("\t")
            elif el.tag in (W + "br", W + "cr"):
                parts.append("\n")
        out.append(("".join(parts), id2name.get(sid, sid) or ""))
    return out


def _is_heading(style):
    """Заголовок секции. В OOXML встроенные стили называются «heading 1»
    (в нижнем регистре), в отдельных шаблонах — «Heading 1»; python-docx
    дополнительно нормализует регистр. Сравниваем без учёта регистра."""
    return style.lower().startswith("heading")


def extract_ru(path):
    """RU-абзацы по секциям. Секции — заголовки `Глава N`/`Пролог`/…;
    в сборниках, где глав нет, — заголовки `Часть M` внутри `История N`
    (номер главы — сквозной внутри рассказа, как в EN). Всё до первого
    заголовка секции не принадлежит главе (обложка, описание героев)."""
    sections = []
    cur = None
    stopped = False
    cur_story = None   # № рассказа сборника
    part_seq = 0       # № главы внутри рассказа
    for raw_text, style in _docx_paragraphs(path):
        if stopped:
            break
        text = clean_ws(raw_text)
        if not text:
            continue
        if _is_heading(style):
            if RU_STOP_RE.search(text):
                stopped = True
                continue
            m = RU_HEAD_RE.match(text)
            if m:
                if m.group(1) == "Глава":
                    kind, num = "chapter", _ru_chapter_number(text)
                    if num is None:
                        print("[ru] не распознан номер главы: %r — "
                              "сопоставление пойдёт по порядку" % text)
                    part_seq = num or part_seq
                else:
                    kind = {"Пролог": "prologue", "Эпилог": "epilogue",
                            "Послесловие": "afterword"}[m.group(1)]
                    num = None
                cur = Section(kind, num, text, story=cur_story)
                sections.append(cur)
                continue
            ms = RU_STORY_RE.match(text)
            if ms:
                # граница рассказа: текст до «Часть M» главой не является
                cur_story, part_seq = int(ms.group(1)), 0
                cur = None
                continue
            pm = RU_PART_RE.match(text)
            if pm:
                part_seq += 1
                cur = Section("chapter", part_seq, text, story=cur_story)
                sections.append(cur)
                continue
        if re.fullmatch(r"\d{1,3}", text):
            continue
        if cur is not None:
            cur.paras.append(text)
    return sections

# --------------------------- якорное выравнивание ---------------------------
# Единицы (JA-блоки) сопоставляются с абзацами другого языка DP-выравниванием.
# Якоря (числа и словарные термины) задаются вызывающим кодом (semantic_blocks):
# это множества токенов, где один и тот же термин в разных языках имеет общий
# ключ, поэтому совпадение якорей — точное пересечение множеств.


def _anchor_overlap(a_set, b_set):
    """Число общих токенов-якорей (числа + словарные термины)."""
    if not a_set or not b_set:
        return 0
    return len(a_set & b_set)


def dp_align(a, b, gap=1.0, anchors_a=None, anchors_b=None, anchor_w=1.2):
    """Выравнивание двух списков абзацев по относительной длине.
    Если переданы якоря (списки множеств той же длины, что a и b),
    диагональная стоимость уменьшается на anchor_w * число совпавших якорей.
    Возвращает список операций (i|None, j|None)."""
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return [(i, None) for i in range(n)] + [(None, j) for j in range(m)]
    ma = sum(len(x) for x in a) / n or 1
    mb = sum(len(x) for x in b) / m or 1
    na = [len(x) / ma for x in a]
    nb = [len(x) / mb for x in b]

    INF = float("inf")
    d = [[INF] * (m + 1) for _ in range(n + 1)]
    bt = [[0] * (m + 1) for _ in range(n + 1)]  # 1=diag 2=up 3=left
    d[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 and j == 0:
                continue
            best, move = INF, 0
            if i > 0 and j > 0:
                c = d[i - 1][j - 1] + abs(na[i - 1] - nb[j - 1]) * 1.5
                if anchors_a is not None and anchors_b is not None:
                    c -= anchor_w * _anchor_overlap(anchors_a[i - 1],
                                                    anchors_b[j - 1])
                    c = max(0.0, c)
                if c < best:
                    best, move = c, 1
            if i > 0:
                c = d[i - 1][j] + gap
                if c < best:
                    best, move = c, 2
            if j > 0:
                c = d[i][j - 1] + gap
                if c < best:
                    best, move = c, 3
            d[i][j], bt[i][j] = best, move

    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        mv = bt[i][j]
        if mv == 1:
            ops.append((i - 1, j - 1))
            i, j = i - 1, j - 1
        elif mv == 2:
            ops.append((i - 1, None))
            i -= 1
        else:
            ops.append((None, j - 1))
            j -= 1
    ops.reverse()
    return ops


# --------------------------- Выравнивание ----------------------------------

def build_groups(ops):
    """Из операций DP — список групп {'a': [idx...], 'b': [idx...]}."""
    groups = []
    pend_a, pend_b = [], []
    for i, j in ops:
        if i is not None and j is not None:
            groups.append({"a": pend_a + [i], "b": pend_b + [j]})
            pend_a, pend_b = [], []
        elif i is not None:
            if groups:
                groups[-1]["a"].append(i)
            else:
                pend_a.append(i)
        else:
            if groups:
                groups[-1]["b"].append(j)
            else:
                pend_b.append(j)
    if groups and (pend_a or pend_b):
        groups[-1]["a"] += pend_a
        groups[-1]["b"] += pend_b
    return groups


def _find_section(sections, used, sec):
    """Секция языка, отвечающая секции EN: сначала по номеру, иначе — по порядку."""
    for idx, s in enumerate(sections):
        if idx in used:
            continue
        if s.kind == sec.kind and (s.number == sec.number or s.number is None):
            return idx
    for idx, s in enumerate(sections):
        if idx not in used and s.kind == sec.kind:
            return idx
    return None


def _story_groups(sections):
    """Индексы секций, сгруппированные по рассказу (EN «Story N» / RU «История N»).
    Если истории не размечены — одна группа, поведение прежнее."""
    groups, cur = [], None
    for i, s in enumerate(sections):
        if not groups or (s.story is not None and s.story != cur):
            groups.append([])
            cur = s.story
        groups[-1].append(i)
    return groups


def _split_proportional(n, weights):
    """Индексы 0..n-1, разделённые по весам (пропорционально объёму)."""
    total = sum(weights) or 1
    parts, pos = [], 0
    for w in weights:
        nxt = min(n, pos + int(round(n * w / total)))
        parts.append(list(range(pos, nxt)))
        pos = nxt
    if pos < n:
        parts[-1].extend(range(pos, n))
    return parts


def _split_story(ja_sec, en_secs, glossary, params):
    """Делит JA-секцию (рассказ целиком) на части по главам EN.

    Абзацы JA выравниваются с абзацами всех глав рассказа (DP + якоря),
    границы глав EN становятся границами частей. Возвращает столько секций,
    сколько глав, с kind/number/title главы EN."""
    ja = ja_sec.paras
    en_all = [p for s in en_secs for p in s.paras]
    parts = None
    if ja and en_all:
        anc_ja = ([sb.anchors_for(p, glossary, "ja") for p in ja]
                  if glossary else None)
        anc_en = ([sb.anchors_for(p, glossary, "en") for p in en_all]
                  if glossary else None)
        ops = dp_align(ja, en_all, anchors_a=anc_ja, anchors_b=anc_en,
                       anchor_w=params["anchor_w"])
        ch_of = []
        for k, s in enumerate(en_secs):
            ch_of.extend([k] * len(s.paras))
        parts, cur = [[] for _ in en_secs], 0
        for i, j in ops:
            if j is not None:
                cur = min(ch_of[j], len(parts) - 1)
            if i is not None:
                parts[cur].append(i)
        if any(not p for p in parts):
            parts = None      # не удалось развести — делим пропорционально
    if parts is None:
        parts = (_split_proportional(len(ja), [len(s.paras) for s in en_secs])
                 if ja else [[] for _ in en_secs])
    return [Section(s.kind, s.number, s.title, [ja[i] for i in sorted(p)],
                    s.story)
            for s, p in zip(en_secs, parts)]


def match_sections(all_langs, glossary=None, params=None):
    """Сопоставляет секции EN (база) с JA и RU.

    В сборниках (том 5) EN размечен по рассказам «Story N», а JA-эпизод —
    это весь рассказ сразу, без глав. Если JA содержит ровно столько же
    секций-рассказов, сколько историй в EN, каждая JA-секция режется по
    главам её рассказа — и JA/EN/RU сходятся по главе.
    """
    base = all_langs["en"]
    result = []
    used = {"ja": set(), "ru": set()}
    groups = _story_groups(base)
    ja_chaps = [i for i, s in enumerate(all_langs["ja"]) if s.kind == "chapter"]
    # одна JA-секция на весь рассказ → режем её по главам EN
    ja_by_story = (ja_chaps if len(groups) > 1 and len(ja_chaps) == len(groups)
                   else None)

    for gi, gidx in enumerate(groups):
        en_secs = [base[i] for i in gidx]
        ja_single = ja_by_story[gi] if ja_by_story is not None else None
        if ja_single is not None:
            used["ja"].add(ja_single)
        slices = (_split_story(all_langs["ja"][ja_single], en_secs,
                               glossary, params)
                  if ja_single is not None and len(en_secs) > 1 else None)
        for pos, sec in enumerate(en_secs):
            trio = {"en": sec}
            if slices is not None:
                trio["ja"] = slices[pos]
            elif ja_single is not None:
                trio["ja"] = all_langs["ja"][ja_single]
            else:
                found = _find_section(all_langs["ja"], used["ja"], sec)
                if found is not None:
                    used["ja"].add(found)
                trio["ja"] = (all_langs["ja"][found] if found is not None
                              else None)
            found = _find_section(all_langs["ru"], used["ru"], sec)
            if found is not None:
                used["ru"].add(found)
            trio["ru"] = all_langs["ru"][found] if found is not None else None
            result.append(trio)

    # Секции, которых нет в EN (например, послесловие только в JA/RU):
    # всё равно нормализуем, опираясь на JA или RU.
    for lang, other in (("ja", "ru"), ("ru", "ja")):
        for idx, s in enumerate(all_langs[lang]):
            if idx in used[lang]:
                continue
            trio = {"en": None, lang: s}
            trio[other] = None
            for jdx, t in enumerate(all_langs[other]):
                if jdx not in used[other] and t.kind == s.kind:
                    used[other].add(jdx)
                    trio[other] = t
                    break
            used[lang].add(idx)
            result.append(trio)
    return result

# ----------------------------- RU (markdown) -------------------------------
# RU_HEAD_RE общий с extract_ru (см. раздел RU docx).


def extract_ru_md(path):
    """RU-перевод в markdown. Абзацы разделяются пустой строкой, главы —
    заголовками вида '# Глава N: ...'. Переносы строк внутри абзаца склеиваются.
    Если заголовков глав нет, весь текст становится одной секцией
    (потом распределяется по главам EN пропорционально объёму)."""
    sections = []
    cur = None
    pre = []
    raw = path.read_text(encoding="utf-8")
    blocks = [b for b in re.split(r"\n\s*\n", raw) if b.strip()]
    for block in blocks:
        block = re.sub(r"\s*\n\s*", " ", block).strip()
        if not block or re.fullmatch(r"\d{1,3}", block):
            continue
        if block.startswith("#"):
            text = block.lstrip("#").strip()
            if re.search(r"[Пп]римечани", text):
                break
            m = RU_HEAD_RE.match(text)
            if m:
                if m.group(1) == "Глава":
                    kind, num = "chapter", int(m.group(2))
                else:
                    kind = {"Пролог": "prologue", "Эпилог": "epilogue",
                            "Послесловие": "afterword"}[m.group(1)]
                    num = None
                cur = Section(kind, num, text)
                sections.append(cur)
                continue
        if cur is None:
            pre.append(block)
        else:
            cur.paras.append(block)
    if not sections:
        sections = [Section("other", None, "", pre)]
    return sections


def distribute_ru_sections(all_langs):
    """Если RU пришёл одной секцией без глав — распределяем его абзацы
    по секциям EN пропорционально объёму текста."""
    en_secs = all_langs["en"]
    ru_secs = all_langs["ru"]
    if not (len(ru_secs) == 1 and ru_secs[0].kind == "other" and len(en_secs) > 1):
        return
    paras = ru_secs[0].paras
    chars = [sum(len(p) for p in s.paras) or 1 for s in en_secs]
    total = float(sum(chars))
    res, pos, acc = [], 0, 0.0
    for s, c in zip(en_secs, chars):
        acc += c
        target = min(max(int(round(len(paras) * acc / total)), pos), len(paras))
        res.append(Section(s.kind, s.number, s.title, paras[pos:target], s.story))
        pos = target
    all_langs["ru"] = res
    print("[ru] заголовков глав не найдено — абзацы распределены по главам EN "
          "пропорционально объёму (границы глав приблизительны!)")

# ---------------------- смысловые блоки (микросцены) -----------------------

def build_blocks(ja, en, ru, glossary, params):
    """Строит смысловые блоки: кластеры базового языка + привязка остальных.

    База — JA; если JA нет (например, послесловие есть только в RU) — EN,
    если нет и EN — RU. Возвращает список {'ja': [...], 'en': [...],
    'ru': [...]} — индексы абзацев каждого языка (0-based).
    """
    if not (ja or en or ru):
        return []
    if ja:
        base, base_lang = ja, "ja"
    elif en:
        base, base_lang = en, "en"
    else:
        base, base_lang = ru, "ru"

    base_blocks = sb.cluster_blocks(base, params["narr_max"],
                                    params["max_paras"], params["max_chars"])
    unit_texts = ["".join(base[i] for i in b) for b in base_blocks]
    unit_anc = [sb.anchors_for(t, glossary, base_lang) for t in unit_texts]

    def map_paras(other, lang):
        out = [[] for _ in base_blocks]
        if not other or not unit_texts:
            return out
        anc_b = [sb.anchors_for(p, glossary, lang) for p in other]
        ops = dp_align(unit_texts, other, anchors_a=unit_anc, anchors_b=anc_b,
                       anchor_w=params["anchor_w"])
        last = 0
        for gr in build_groups(ops):
            if gr["a"]:
                last = gr["a"][0]        # блок-приёмник; для «только b» — прежний
            if gr["b"]:
                out[last].extend(gr["b"])
        return out

    own = [list(b) for b in base_blocks]
    by = {"ja": [], "en": [], "ru": []}
    by[base_lang] = own
    for lang in ("ja", "en", "ru"):
        if lang == base_lang:
            continue
        by[lang] = map_paras({"ja": ja, "en": en, "ru": ru}[lang], lang)

    # Если база не RU, а EN есть: RU — машинный перевод EN, поэтому RU-абзацы
    # привязываем через EN (точнее, чем напрямую к JA).
    if base_lang != "ru" and en:
        ru_per_en = map_paras_ru(en, ru, glossary, params["anchor_w"])
        en_to_block = {}
        for k, idxs in enumerate(by["en"]):
            for j in idxs:
                en_to_block[j] = k
        ru_by = [[] for _ in base_blocks]
        last = 0
        for j, ru_idxs in enumerate(ru_per_en):
            if j in en_to_block:
                last = en_to_block[j]
            ru_by[last].extend(ru_idxs)
        by["ru"] = ru_by

    blocks = [{"ja": sorted(by["ja"][k]), "en": sorted(by["en"][k]),
               "ru": sorted(by["ru"][k])} for k in range(len(base_blocks))]
    for key in ("ja", "en", "ru"):
        _fill_empty(blocks, key)
    return blocks


def map_paras_ru(en, ru, glossary, anchor_w):
    """Привязка RU-абзацев к EN-абзацам (список длины len(en)).

    RU — машинный перевод EN: структура предложений и имена ближе к EN, чем
    к JA, поэтому соответствие ищется EN ↔ RU, а не JA ↔ RU.
    """
    out = [[] for _ in en]
    if not en or not ru:
        return out
    anc_en = [sb.anchors_for(p, glossary, "en") for p in en]
    anc_ru = [sb.anchors_for(p, glossary, "ru") for p in ru]
    ops = dp_align(en, ru, anchors_a=anc_en, anchors_b=anc_ru,
                   anchor_w=anchor_w)
    last = 0
    for gr in build_groups(ops):
        if gr["a"]:
            last = gr["a"][0]
        if gr["b"]:
            out[last].extend(gr["b"])
    return out


def _fill_empty(blocks, key):
    """Гарантирует каждому блоку хотя бы один абзац языка key.

    Границы микросцен размыты: если выравнивание оставило блок без абзацев
    другого языка, забираем ближайший абзац у соседа с избытком — иначе блок
    теряет опору (нечего сравнивать) и в merged остаётся «—».
    """
    changed = True
    while changed:
        changed = False
        for k in range(len(blocks)):
            if blocks[k][key]:
                continue
            for cand in (k - 1, k + 1):
                if 0 <= cand < len(blocks) and len(blocks[cand][key]) >= 2:
                    idx = (blocks[cand][key][-1] if cand < k
                           else blocks[cand][key][0])
                    blocks[cand][key].remove(idx)
                    blocks[k][key] = sorted(blocks[k][key] + [idx])
                    changed = True
                    break
    return blocks


def write_block_file(path, title, paras, blocks, lang):
    """Markdown языка: блоки разделены маркером `<!-- block: N -->`."""
    lines = ["# %s" % title, ""]
    for bid, b in enumerate(blocks, 1):
        idxs = b.get(lang) or []
        if not idxs:
            continue
        lines.append("<!-- block: %d -->" % bid)
        lines.append("")
        for i in idxs:
            t = paras[i].strip()
            if t:
                lines.append(t)
                lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _col(paras, idxs):
    txt = "\n".join(paras[i].strip() for i in idxs
                    if i < len(paras) and paras[i].strip())
    return txt or "—"


def read_ed_ru(path):
    """ED_RU из `output/<имя>.md`: {номер блока: текст}.

    Нужен, чтобы повторная нормализация не затирала отредактированный
    перевод в `translates/_report/merged/` (merged — зеркало output/;
    формат блок-файла — см. `scripts/merged_io.read_source_blocks`).
    Если файла нет (глава ещё не обработана) — пусто, поле будет «—»."""
    p = Path(path)
    if not p.exists():
        return {}
    blocks, num, cur = {}, None, []
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        m = re.match(r"^<!--\s*block:\s*(\d+)\s*-->$", s)
        if m:
            if num is not None:
                blocks[num] = "\n".join(cur)
            num, cur = int(m.group(1)), []
        elif not s or line.startswith("# ") or s.startswith("<!--"):
            continue
        else:
            cur.append(s)
    if num is not None:
        blocks[num] = "\n".join(cur)
    return {k: v for k, v in blocks.items() if v}


def write_merged(path, title, ja, en, ru, blocks, ed=None):
    """Трёхъязычный merged: единица — блок (`## Блок N`), поля многострочные.

    `ed` — ED_RU из output/; без него поле пишется как «—»."""
    ed = ed or {}
    parts = []
    for bid, b in enumerate(blocks, 1):
        parts.append("## Блок %d\n\n**JA:**\n%s\n\n**EN:**\n%s\n\n**RU:**\n%s\n\n"
                     "**ED_RU:**\n%s\n"
                     % (bid, _col(ja, b["ja"]), _col(en, b["en"]),
                        _col(ru, b["ru"]), ed.get(bid) or "—"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# %s\n\n%s\n" % (title, "\n".join(parts)), encoding="utf-8")


def write_blocks_json(path, slug, ja, en, ru, glossary, blocks):
    """Карта соответствия Block_ID -> [JA_indices], [EN_indices], [RU_indices]."""
    import json

    def anc(paras, idxs, lang):
        s = set()
        for i in idxs:
            if i < len(paras):
                s |= sb.anchors_for(paras[i], glossary, lang)
        return sorted(s)

    data = {"file": slug + ".md", "n_blocks": len(blocks), "blocks": []}
    for bid, b in enumerate(blocks, 1):
        data["blocks"].append({
            "id": bid,
            "ja_paras": [i + 1 for i in b["ja"]],
            "en_paras": [i + 1 for i in b["en"]],
            "ru_paras": [i + 1 for i in b["ru"]],
            "anchors": {"ja": anc(ja, b["ja"], "ja"),
                        "en": anc(en, b["en"], "en"),
                        "ru": anc(ru, b["ru"], "ru")},
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                    encoding="utf-8")


# --------------------------------- main ------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volume", type=int, required=True)
    ap.add_argument("--origs", default="origs")
    ap.add_argument("--project", default="AINovelEdit")
    ap.add_argument("--out", default=None,
                    help="куда писать translates/ (по умолчанию <project>/translates)")
    ap.add_argument("--glossary", default=None,
                    help="путь к dictionary.md (по умолчанию <project>/dictionary.md)")
    ap.add_argument("--narr-max", type=int, default=150,
                    help="порог «короткой» наррации для склейки с репликой")
    ap.add_argument("--max-paras", type=int, default=16,
                    help="максимум абзацев в одном смысловом блоке")
    ap.add_argument("--max-chars", type=int, default=1600,
                    help="максимум символов в одном смысловом блоке")
    ap.add_argument("--anchor-w", type=float, default=4.0,
                    help="вес словарных/числовых якорей при выравнивании блоков")
    args = ap.parse_args()

    origs = Path(args.origs)
    project = Path(args.project)
    out_base = Path(args.out) if args.out else project / "translates"
    glossary_path = (Path(args.glossary) if args.glossary
                     else project / "dictionary.md")
    glossary = sb.load_glossary(glossary_path)
    vol = args.volume
    params = {"narr_max": args.narr_max, "max_paras": args.max_paras,
              "max_chars": args.max_chars, "anchor_w": args.anchor_w}

    # завершённые тома не нормализуются повторно (источник истины, заморожены)
    sys.path.insert(0, str(project / "scripts"))
    try:
        import completed
        if completed.is_frozen(vol, project / "completed.md"):
            raise SystemExit(
                "Том %d завершён и заморожен (см. %s/completed.md) — "
                "повторная нормализация запрещена." % (vol, project))
    except ImportError:
        pass

    ru_docx = origs / ("%d-ru.docx" % vol)
    ru_md = origs / ("%d-ru.md" % vol)
    if ru_docx.exists():
        ru_src = (ru_docx, extract_ru)
    elif ru_md.exists():
        ru_src = (ru_md, extract_ru_md)
    else:
        raise SystemExit("Не найден RU-файл: %s (docx) или %s (md)" % (ru_docx, ru_md))
    sources = {
        "ja": (origs / ("%d-ja.epub" % vol), extract_ja),
        "en": (origs / ("%d-en.pdf" % vol), extract_en),
        "ru": ru_src,
    }
    all_langs = {}
    for lang, (path, fn) in sources.items():
        if not path.exists():
            raise SystemExit("Не найден файл: %s" % path)
        all_langs[lang] = fn(path)
        total = sum(len(s.paras) for s in all_langs[lang])
        print("[%s] %s: секций %d, абзацев %d" % (lang, path.name, len(all_langs[lang]), total))

    distribute_ru_sections(all_langs)
    trios = match_sections(all_langs, glossary, params)

    # В одном томе может быть несколько книг со сквозной нумерацией глав
    # («Глава 1» начинается заново). Если номера дублируются — перенумеровываем
    # главы EN последовательно, иначе slug'и (vXX-chNN) перезапишут друг друга.
    _en_nums = [s.number for s in all_langs["en"] if s.kind == "chapter"]
    if len(_en_nums) != len(set(_en_nums)):
        _counter = 0
        for _sec in all_langs["en"]:
            if _sec.kind == "chapter":
                _counter += 1
                _sec.number = _counter

    print("Режим смысловых блоков; словарь: %d терминов" % len(glossary))
    report = ["# Отчёт смысловых блоков — том %d" % vol, ""]
    report.append("Единица — смысловой блок (микросцена). translates/* и merged/ "
                  "разбиты по блокам (`<!-- block: N -->` / `## Блок N`); "
                  "абзацы внутри блока могут не совпадать по числу и границам.")
    report.append("")
    report.append("| Секция | JA абз. | EN абз. | RU абз. | Блоков | Пустых JA |")
    report.append("|---|---|---|---|---|---|")

    for trio in trios:
        sec = trio["en"] or trio["ja"] or trio["ru"]
        slug = "v%d-%s" % (vol, sec.slug)
        ja_p = trio["ja"].paras if trio["ja"] else []
        ru_p = trio["ru"].paras if trio["ru"] else []
        en_p = trio["en"].paras if trio["en"] else []
        blocks = build_blocks(ja_p, en_p, ru_p, glossary, params)

        titles = {}
        for lang, sec_lang in (("ja", trio["ja"]), ("en", trio["en"]),
                               ("ru", trio["ru"])):
            titles[lang] = sec_lang.title if sec_lang else sec.title
        write_block_file(out_base / "ja" / (slug + ".md"),
                         titles["ja"], ja_p, blocks, "ja")
        write_block_file(out_base / "en" / (slug + ".md"),
                         titles["en"], en_p, blocks, "en")
        write_block_file(out_base / "ru" / (slug + ".md"),
                         titles["ru"], ru_p, blocks, "ru")
        write_merged(out_base / "_report" / "merged" / (slug + ".md"),
                     titles["en"], ja_p, en_p, ru_p, blocks,
                     read_ed_ru(project / "output" / (slug + ".md")))
        write_blocks_json(out_base / "_report" / "blocks" / (slug + ".json"),
                          slug, ja_p, en_p, ru_p, glossary, blocks)

        empty_ja = sum(1 for b in blocks if not b["ja"])
        report.append("| %s | %d | %d | %d | %d | %d |" % (
            slug, len(ja_p), len(en_p), len(ru_p), len(blocks), empty_ja))

    rep_dir = out_base / "_report"
    rep_dir.mkdir(parents=True, exist_ok=True)
    (rep_dir / ("v%d-alignment.md" % vol)).write_text(
        "\n".join(report) + "\n", encoding="utf-8")
    print("Готово. Секций: %d. Блоки: %s/{ja,en,ru}, %s/blocks/*.json; отчёт: %s"
          % (len(trios), out_base, rep_dir, rep_dir / ("v%d-alignment.md" % vol)))


if __name__ == "__main__":
    main()



