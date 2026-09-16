#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
images.py — извлечение иллюстраций из EN-PDF тома и разметка их позиций
между EN-абзацами (нумерация абзацев та же, что в translates/en и merged).

Запускается пользователем вручную (агент с изображениями не работает):
    python tools/images.py --volume 14

Выход:
    images/vNN/            — файлы иллюстраций
    images/vNN/images.md   — таблица: файл, страница PDF, глава,
                             между какими EN-абзацами стоит изображение
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pymupdf
from normalize import extract_en  # noqa: E402


def scan_pages(doc, sections):
    """Для каждой страницы: (slug, first_para_global, last_para_global)."""
    infos = []
    sec_i, cur_slug = 0, "(before-ch1)"
    g = 0
    for pno in range(doc.page_count):
        first = None
        last = None
        for b in sorted(doc[pno].get_text("blocks"), key=lambda x: (x[1], x[0])):
            text = b[4].strip()
            if not text or text.isdigit():
                continue
            if sec_i < len(sections) and text.replace("\n", " ").startswith(
                    sections[sec_i].title[:20]):
                cur_slug = sections[sec_i].slug
                sec_i += 1
                continue
            if cur_slug != "(before-ch1)":
                g += 1
                if first is None:
                    first = g
                last = g
        infos.append({"pno": pno, "slug": cur_slug, "first": first, "last": last})
    return infos


def next_para(infos, pno):
    """Первый текстовый абзац на страницах ПОСЛЕ pno: (global_idx, slug)."""
    for j in range(pno + 1, len(infos)):
        if infos[j]["first"] is not None:
            return infos[j]["first"], infos[j]["slug"]
    return None, None


def para_text(slug, idx, sections):
    for s in sections:
        if s.slug == slug:
            return s.paras[idx - 1] if 0 < idx <= len(s.paras) else ""
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volume", type=int, required=True)
    ap.add_argument("--origs", default="origs")
    ap.add_argument("--out", default="images")
    args = ap.parse_args()

    pdf = Path(args.origs) / ("%d-en.pdf" % args.volume)
    out_dir = Path(args.out) / ("v%d" % args.volume)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf)
    sections = extract_en(pdf)
    infos = scan_pages(doc, sections)

    rows = ["# Изображения — том %d" % args.volume, "",
            "Позиция привязана к EN-абзацам (нумерация как в merged/EN-файле):",
            "вставлять ПОСЛЕ указанного абзаца (или ПЕРЕД абзацем из последней",
            "колонки, если в колонке «После» стоит —).", "",
            "| Файл | Стр. PDF | Глава | После EN-абзаца | Следующий абзац (начало) |",
            "|---|---|---|---|---|"]
    saved = 0
    for info in infos:
        pno = info["pno"]
        page = doc[pno]
        if page.get_text().strip():
            continue  # текстовая страница — не иллюстрация
        nxt_idx, nxt_slug = next_para(infos, pno)
        after = None if nxt_idx in (None, 1) else nxt_idx - 1
        nxt_text = para_text(nxt_slug, nxt_idx, sections) if nxt_idx else ""
        for k, im in enumerate(page.get_images(full=True)):
            w, h = im[2], im[3]
            if w < 200 or h < 200:
                continue
            f = doc.extract_image(im[0])
            fname = "p%03d-%d.%s" % (pno + 1, k + 1, f["ext"])
            (out_dir / fname).write_bytes(f["image"])
            saved += 1
            rows.append("| %s | %d | %s | %s | [%s] %s |" % (
                fname, pno + 1, info["slug"],
                ("№%d" % after) if after else "—",
                nxt_slug if nxt_slug else "—",
                (nxt_text[:60] + "…") if nxt_text else "—"))

    (out_dir / "images.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("Извлечено изображений: %d -> %s" % (saved, out_dir))


if __name__ == "__main__":
    main()
