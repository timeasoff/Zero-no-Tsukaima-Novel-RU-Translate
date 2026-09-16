#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize.py — нормализация сырых исходников тома (JA epub / EN pdf / RU docx)
в выровненные по абзацам markdown-файлы для проекта AINovelEdit.

Использование (из папки, где лежат origs/ и AINovelEdit/):
    python tools/normalize.py --volume 14
"""
import argparse
import re
import zipfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

import pymupdf
import docx

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
    r"^(Chapter\s+(\d+)\s*[:.]\s*.+|Prologue|Epilogue|Afterword|Interlude)(\s*[:.].*)?$")


def _ends_sentence(s):
    return bool(re.search(r'[.!?…:;]["»\'”’)]?\s*$', s))


def extract_en(path):
    sections = []
    cur = None
    carry = ""   # незавершённый абзац, продолжающийся на следующей странице
    doc = pymupdf.open(path)
    for page in doc:
        blocks = sorted(page.get_text("blocks"), key=lambda b: (b[1], b[0]))
        for b in blocks:
            raw = re.sub(r"(\w)-\n(\w)", r"\1\2", b[4])
            text = clean_ws(raw)
            if not text or re.fullmatch(r"\d{1,3}", text):
                continue
            if carry:
                text = carry + " " + text
                carry = ""
            head_text = text.replace("\n", " ")
            m = EN_HEAD_RE.match(head_text)
            if m and len(head_text) < 120:
                if m.group(2):
                    kind, num = "chapter", int(m.group(2))
                else:
                    kind = head_text.split(":")[0].strip().lower()
                    num = None
                cur = Section(kind, num, head_text)
                sections.append(cur)
                continue
            if cur is not None:
                cur.paras.append(text)
        # абзац оборван на границе страниц — переносим на следующую
        if cur is not None and cur.paras and not _ends_sentence(cur.paras[-1]):
            carry = cur.paras.pop()
    return sections


# ----------------------------- RU (docx) -----------------------------------

def extract_ru(path):
    sections = []
    cur = None
    stopped = False
    d = docx.Document(path)
    for p in d.paragraphs:
        if stopped:
            break
        style = p.style.name or ""
        text = clean_ws(p.text)
        if not text:
            continue
        if style.startswith("Heading"):
            if re.search(r"[Пп]римечани", text):
                stopped = True
                continue
            m = re.match(r"^(Глава|Пролог|Эпилог|Послесловие)\s*(\d+)?\s*[:.]?\s*(.*)$", text)
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
        if re.fullmatch(r"\d{1,3}", text):
            continue
        if cur is not None:
            cur.paras.append(text)
    return sections

# --------------------------- Выравнивание ----------------------------------

def dp_align(a, b, gap=1.0):
    """Выравнивание двух списков абзацев по относительной длине.
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


def build_groups(ops):
    """Из операций DP — список групп {'a': [idx...], 'b': [idx...]}."""
    groups = []
    pend_a, pend_b = [], []
    for i, j in ops:
        if i is not None and j is not None:
            groups.append({"a": [i] + pend_a, "b": [j] + pend_b})
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


_SENT_SPLIT_RE = re.compile(r"(?<=[.!?…])\s+(?=[А-ЯЁA-Z«\"\-–—])")


def split_into(text, n):
    """Разрезает абзац на n частей по границам предложений.
    Если предложений меньше n — возвращает текст как есть."""
    sents = [s for s in _SENT_SPLIT_RE.split(text) if s.strip()]
    if len(sents) < n:
        return [text]
    buckets = [[] for _ in range(n)]
    for i, s in enumerate(sents):
        buckets[min(i * n // len(sents), n - 1)].append(s)
    return [" ".join(b) for b in buckets]


def _split_ja_sentences(text):
    parts = re.findall(r"[^。！？」』]+[。！？」』]+|[^。！？」』]+$", text)
    return [p for p in parts if p.strip()]


def _split_en_sentences(text):
    parts = re.split(r"(?<=[.!?…])\s+", text)
    return [p for p in parts if p.strip()]


def ja_en_sentence_map(ja, en):
    """Сопоставляет JA-абзацы EN-абзацам на уровне предложений.

    Возвращает dict: индекс EN-абзаца -> текст JA (конкатенация предложений,
    привязавшихся к этому EN-абзацу). JA-абзац, чьи предложения распределились
    по нескольким EN-абзацам, автоматически «разрезается»."""
    ja_s, en_s = [] , []     # (индекс абзаца, текст предложения)
    for pi, p in enumerate(ja):
        for s in _split_ja_sentences(p):
            ja_s.append((pi, s))
    for pi, p in enumerate(en):
        for s in _split_en_sentences(p):
            en_s.append((pi, s))

    ops = dp_align([t for _, t in ja_s], [t for _, t in en_s])
    buckets = {}             # en_para -> список (ja_para, текст предложения)
    ii = jj = 0
    first_ja = []            # JA-предложения до первого совпадения
    for i, j in ops:
        if i is not None and j is not None:
            buckets.setdefault(en_s[jj][0], []).append((ja_s[ii][0], ja_s[ii][1]))
            ii += 1; jj += 1
        elif i is not None:
            # JA-предложение без пары: если бинкеты уже есть — в последний,
            # иначе ждём первого совпадения
            if buckets:
                buckets[max(buckets)].append((ja_s[ii][0], ja_s[ii][1]))
            else:
                first_ja.append((ja_s[ii][0], ja_s[ii][1]))
            ii += 1
        else:
            jj += 1          # EN-предложение без JA-пары — строка без JA
    if first_ja:
        if buckets:
            key = min(buckets)
            buckets[key] = first_ja + buckets[key]
        else:
            buckets[0] = first_ja

    # Пустые EN-строки: JA-предложение могло прилипнуть к соседнему бакету.
    # 1) «Хвост» из более позднего JA-абзаца в бакете предыдущей строки ->
    #    переливаем в пустую строку. 2) «Голова» из более раннего JA-абзаца
    #    в бакете следующей строки -> тоже переливаем. Проверяем монотонность
    #    номеров JA-абзацев, чтобы не разрушить порядок.
    def runs(lst):
        out = []
        for item in lst:
            if out and out[-1][0][0] == item[0]:
                out[-1].append(item)
            else:
                out.append([item])
        return out

    for e in range(len(en)):
        if e in buckets:
            continue
        prev = [k for k in buckets if k < e]
        nxt = [k for k in buckets if k > e]
        # --- вариант 1: хвост предыдущего бакета
        if prev:
            q = max(prev)
            rs = runs(buckets[q])
            if len(rs) >= 2 and rs[-1][0][0] > rs[0][0][0]:
                tail = rs[-1]
                ok = True
                if nxt:
                    if tail[0][0] >= buckets[min(nxt)][0][0]:
                        ok = False
                if ok:
                    buckets[e] = list(tail)
                    buckets[q] = buckets[q][:len(buckets[q]) - len(tail)]
                    continue
        # --- вариант 2: голова следующего бакета
        if nxt:
            q = min(nxt)
            rs = runs(buckets[q])
            if len(rs) >= 2:
                head = rs[0]
                ok = True
                if prev:
                    plast = runs(buckets[max(prev)])[-1][0][0]
                    if head[0][0] <= plast:
                        ok = False
                if ok:
                    buckets[e] = list(head)
                    buckets[q] = buckets[q][len(head):]

    # Финальная подгонка: границы JA-предложений по границам EN-строк.
    # Локальный поиск одиночных сдвигов, минимизирующий отклонение длины
    # JA-строки от пропорциональной длины EN-строки (JA короче EN по знакам).
    rows = {e: list(v) for e, v in buckets.items()}
    ja_total = sum(len(t) for v in rows.values() for _, t in v)
    en_total = sum(len(en[e]) for e in rows) or 1
    ratio = ja_total / en_total

    def rlen(e):
        return sum(len(t) for _, t in rows.get(e, []))

    def pair_cost(e):
        return (abs(rlen(e) - ratio * len(en[e]))
                + abs(rlen(e + 1) - ratio * len(en[e + 1])))

    for _ in range(40):
        improved = False
        for e in range(len(en) - 1):
            a, b = rows.get(e, []), rows.get(e + 1, [])
            before = pair_cost(e)
            if len(a) >= 2:                      # сдвиг вниз: последнее -> вправо
                na, nb = a[:-1], [a[-1]] + b
                rows[e], rows[e + 1] = na, nb
                if pair_cost(e) + 1e-9 < before:
                    improved = True
                    continue
                rows[e], rows[e + 1] = a, b
            if len(b) >= 2:                      # сдвиг вверх: первое -> влево
                na, nb = a + [b[0]], b[1:]
                rows[e], rows[e + 1] = na, nb
                if pair_cost(e) + 1e-9 < before:
                    improved = True
                    continue
                rows[e], rows[e + 1] = a, b
        if not improved:
            break

    return {e: "".join(t[1] for t in v) for e, v in sorted(rows.items()) if v}


def align_triple(ja, en, ru, warnings):
    """Возвращает список строк-триплетов (ja_text, en_text, ru_text)."""
    ops = dp_align(en, ru)
    g_en_ru = build_groups(ops)
    ja_for_en = ja_en_sentence_map(ja, en)
    matched = sum(len(v) for v in ja_for_en.values())
    total = sum(len(p) for p in ja)
    if matched < total * 0.9:
        warnings.append("часть JA не привязалась (%d%%)" %
                        int(100 * matched / max(total, 1)))

    lines = []
    stats = {"empty_ja": 0, "ru_split": 0}
    for g in g_en_ru:
        en_idx, ru_idx = g["a"], g["b"]
        en_texts = [en[e] for e in en_idx]
        ru_texts = [ru[r] for r in ru_idx]
        # RU склеен (EN-абзацев больше): пробуем разрезать по предложениям
        if len(ru_texts) == 1 and len(en_texts) > 1:
            parts = split_into(ru_texts[0], len(en_texts))
            if len(parts) == len(en_texts):
                ru_texts = parts
                stats["ru_split"] += 1
        for k, e in enumerate(en_idx):
            t_ja = ja_for_en.get(e, "")
            t_en = en_texts[k]
            t_ru = ru_texts[k] if k < len(ru_texts) else ""
            if not t_ja:
                stats["empty_ja"] += 1
            lines.append((t_ja, t_en, t_ru))
    return lines, stats


def match_sections(all_langs):
    base = all_langs["en"]
    result = []
    used = {"ja": set(), "ru": set()}
    for sec in base:
        trio = {"en": sec}
        for lang in ("ja", "ru"):
            found = None
            for idx, s in enumerate(all_langs[lang]):
                if idx in used[lang]:
                    continue
                if s.kind == sec.kind and (s.number == sec.number or s.number is None):
                    found = idx
                    break
            if found is None:
                for idx, s in enumerate(all_langs[lang]):
                    if idx not in used[lang] and s.kind == sec.kind:
                        found = idx
                        break
            if found is not None:
                used[lang].add(found)
                trio[lang] = all_langs[lang][found]
            else:
                trio[lang] = None
        result.append(trio)
    return result

# ----------------------------- RU (markdown) -------------------------------

RU_HEAD_RE = re.compile(r"^(Глава|Пролог|Эпилог|Послесловие)\s*(\d+)?\s*[:.]?\s*(.*)$")


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
        res.append(Section(s.kind, s.number, s.title, paras[pos:target]))
        pos = target
    all_langs["ru"] = res
    print("[ru] заголовков глав не найдено — абзацы распределены по главам EN "
          "пропорционально объёму (границы глав приблизительны!)")

# --------------------------------- main ------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volume", type=int, required=True)
    ap.add_argument("--origs", default="origs")
    ap.add_argument("--project", default="AINovelEdit")
    args = ap.parse_args()

    origs = Path(args.origs)
    project = Path(args.project)
    out_base = project / "translates"
    vol = args.volume

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
    trios = match_sections(all_langs)
    report = ["# Отчёт выравнивания — том %d" % vol, ""]
    report.append("| Секция | JA абз. | EN абз. | RU абз. | Строк | Пустых JA | RU разрезано |")
    report.append("|---|---|---|---|---|---|---|")

    for trio in trios:
        sec = trio["en"]
        slug = "v%d-%s" % (vol, sec.slug)
        warnings = []
        ja_p = trio["ja"].paras if trio["ja"] else []
        ru_p = trio["ru"].paras if trio["ru"] else []
        lines, stats = align_triple(ja_p, sec.paras, ru_p, warnings)

        ja_lines = [l[0] if l[0].strip() else "<!-- нет пары в JA -->" for l in lines]
        for lang, sec_lang, content in (
            ("ja", trio["ja"], ja_lines),
            ("en", sec, [l[1] for l in lines]),
            ("ru", trio["ru"], [l[2] for l in lines]),
        ):
            d = out_base / lang
            d.mkdir(parents=True, exist_ok=True)
            title = sec_lang.title if sec_lang else sec.title
            text = "# %s\n\n%s\n" % (title, "\n\n".join(content))
            (d / (slug + ".md")).write_text(text, encoding="utf-8")

        # merged-копия для визуальной свечки человеком (не для агента)
        merged_dir = out_base / "_report" / "merged"
        merged_dir.mkdir(parents=True, exist_ok=True)
        parts = ["## Абзац %d\n\n**JA:** %s\n\n**EN:** %s\n\n**RU:** %s" % (
            i, l[0] or "—", l[1] or "—", l[2] or "—")
            for i, l in enumerate(lines, 1)]
        (merged_dir / (slug + ".md")).write_text("\n\n".join(parts) + "\n", encoding="utf-8")

        report.append("| %s | %d | %d | %d | %d | %d | %d |" % (
            slug, len(ja_p), len(sec.paras), len(ru_p),
            len(lines), stats["empty_ja"], stats["ru_split"]))
        for w in warnings:
            report.append("  - WARNING %s: %s" % (slug, w))

    rep_dir = out_base / "_report"
    rep_dir.mkdir(parents=True, exist_ok=True)
    (rep_dir / ("v%d-alignment.md" % vol)).write_text("\n".join(report) + "\n", encoding="utf-8")
    print("Готово. Секций: %d. Отчёт: %s" % (len(trios), rep_dir / ("v%d-alignment.md" % vol)))


if __name__ == "__main__":
    main()



