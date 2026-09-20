#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
from pathlib import Path

import pymupdf


def main():
    parser = argparse.ArgumentParser(
        description="Извлечь изображения из PDF и последовательно пронумеровать их."
    )

    parser.add_argument(
        "pdf",
        help="PDF-файл, например 14-en.pdf",
    )

    parser.add_argument(
        "--out",
        default="images",
        help="Папка для изображений (по умолчанию: images)",
    )

    args = parser.parse_args()

    pdf_path = Path(args.pdf)

    if not pdf_path.exists():
        print(f"Ошибка: файл не найден: {pdf_path}")
        return 1

    # Берём номер из имени файла:
    # 14-en.pdf -> 14
    match = re.match(r"(\d+)-en$", pdf_path.stem, re.IGNORECASE)

    if not match:
        print(
            f"Ошибка: имя PDF должно иметь формат N-en.pdf, "
            f"например 14-en.pdf"
        )
        return 1

    volume = match.group(1)

    out_dir = Path(args.out) / volume
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"PDF: {pdf_path}")
    print(f"Том: {volume}")
    print(f"Выход: {out_dir}")

    doc = pymupdf.open(pdf_path)

    image_number = 0

    try:
        for page_number in range(doc.page_count):
            page = doc[page_number]

            for image in page.get_images(full=True):
                xref = image[0]

                try:
                    extracted = doc.extract_image(xref)
                except Exception as exc:
                    print(
                        f"Ошибка: страница {page_number + 1}, "
                        f"image {xref}: {exc}"
                    )
                    continue

                image_number += 1

                ext = extracted["ext"]

                filename = f"{volume}-{image_number}.{ext}"
                output_path = out_dir / filename

                output_path.write_bytes(extracted["image"])

                print(
                    f"{image_number:3d}: "
                    f"PDF стр. {page_number + 1:3d} -> {filename}"
                )

    finally:
        doc.close()

    print()
    print(f"Готово. Извлечено изображений: {image_number}")
    print(f"Папка: {out_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())