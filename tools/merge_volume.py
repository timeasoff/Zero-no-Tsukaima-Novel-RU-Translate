#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
merge_volume.py

Склеивает Markdown-файлы тома, удаляет block-маркеры,
вставляет изображения по img-маркерам и создаёт PDF.

Структура проекта:

    noverl/
    ├── tools/
    │   └── merge_volume.py
    │
    ├── images/
    │   ├── v14/
    │   │   ├── 14-1.jpeg
    │   │   ├── 14-2.jpeg
    │   │   └── ...
    │   ├── v15/
    │   │   └── ...
    │   └── v16/
    │       └── ...
    │
    └── AINovelEdit/
        └── output/
            ├── v14-ch01.md
            ├── v14-ch02.md
            ├── ...
            ├── v14-ch09.md
            └── v14-epilogue.md


Markdown-маркеры:

    <!-- block: 1 -->
    <!-- block: 2 -->

Удаляются полностью.

Изображения:

    <!-- img_14-1 -->
    <!-- img_14-9 -->
    <!-- img_15-1 -->
    <!-- img_16-27 -->

Изображение ищется по ПОЛНОМУ ID:

    img_14-9  -> images/v14/14-9.jpeg
    img_15-1  -> images/v15/15-1.jpeg
    img_16-27 -> images/v16/16-27.jpeg


Результат:

    AINovelEdit/output/14-merged.md
    AINovelEdit/output/14-merged.pdf


Запуск:

    cd /d/skills/NovelEdit/noverl
    python tools/merge_volume.py --volume 14
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


# ============================================================
# Пути проекта
# ============================================================

# Папка noverl/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# AINovelEdit/output/
MARKDOWN_DIR = PROJECT_ROOT / "AINovelEdit" / "output"

# images/
IMAGES_ROOT = PROJECT_ROOT / "images"


# ============================================================
# Регулярные выражения
# ============================================================

IMAGE_MARKER_RE = re.compile(
    r"<!--\s*img_([0-9]+-[0-9]+)\s*-->",
    re.IGNORECASE,
)

BLOCK_MARKER_RE = re.compile(
    r"<!--\s*block\s*:\s*[0-9]+\s*-->",
    re.IGNORECASE,
)


# ============================================================
# Сортировка Markdown
# ============================================================

def markdown_sort_key(path):
    """
    Порядок:

        v14-ch01.md
        v14-ch02.md
        ...
        v14-ch09.md
        v14-epilogue.md
    """

    name = path.stem.lower()

    match = re.search(
        r"-ch([0-9]+)$",
        name,
    )

    if match:
        chapter_number = int(match.group(1))

        return (
            0,
            chapter_number,
        )

    if name.endswith("-epilogue"):
        return (
            1,
            0,
        )

    return (
        2,
        name,
    )


# ============================================================
# Поиск Markdown-файлов
# ============================================================

def collect_markdown_files(volume):
    """
    Находит только Markdown-файлы нужного тома.

    Для volume=14:

        v14-ch01.md
        v14-ch02.md
        ...
        v14-ch09.md
        v14-epilogue.md
    """

    files = []

    chapter_pattern = re.compile(
        rf"v{volume}-ch[0-9]+\.md",
        re.IGNORECASE,
    )

    epilogue_name = (
        f"v{volume}-epilogue.md"
    ).lower()

    for path in MARKDOWN_DIR.glob("*.md"):

        name = path.name

        if chapter_pattern.fullmatch(name):
            files.append(path)
            continue

        if name.lower() == epilogue_name:
            files.append(path)
            continue

    files.sort(
        key=markdown_sort_key
    )

    return files


# ============================================================
# Поиск изображения
# ============================================================

def find_image(image_name):
    """
    image_name:

        14-1
        15-3
        16-27

    Изображение ищется в папке соответствующего тома:

        images/v14/14-1.jpeg
        images/v15/15-3.jpeg
        images/v16/16-27.jpeg
    """

    match = re.fullmatch(
        r"([0-9]+)-([0-9]+)",
        image_name,
    )

    if not match:
        return None

    image_volume = match.group(1)

    image_dir = (
        IMAGES_ROOT
        / f"v{image_volume}"
    )

    extensions = (
        ".jpeg",
        ".jpg",
        ".png",
        ".webp",
    )

    for extension in extensions:

        path = (
            image_dir
            / f"{image_name}{extension}"
        )

        if path.exists():
            return path

    return None


# ============================================================
# Относительный путь к изображению
# ============================================================

def image_markdown_path(
    image_path,
    markdown_output,
):
    """
    Возвращает относительный путь
    от папки merged Markdown до изображения.

    Например:

        Markdown:
        AINovelEdit/output/14-merged.md

        Image:
        images/v14/14-9.jpeg

    Получится:

        ../../images/v14/14-9.jpeg
    """

    return Path(
        os.path.relpath(
            image_path.resolve(),
            markdown_output.parent.resolve(),
        )
    ).as_posix()


# ============================================================
# Обработка одного Markdown
# ============================================================

def process_markdown(
    text,
    markdown_output,
):
    """
    1. Удаляет block-маркеры.
    2. Заменяет img-маркеры изображениями.
    """

    # --------------------------------------------------------
    # Удаляем block-маркеры
    # --------------------------------------------------------

    text = BLOCK_MARKER_RE.sub(
        "",
        text,
    )

    inserted = []
    missing = []

    # --------------------------------------------------------
    # Обрабатываем изображения
    # --------------------------------------------------------

    def replace_image(match):

        image_name = match.group(1)

        image_path = find_image(
            image_name
        )

        if image_path is None:

            missing.append(
                image_name
            )

            # Оставляем исходный маркер,
            # чтобы было видно ошибку.
            return match.group(0)

        inserted.append(
            image_name
        )

        relative_path = (
            image_markdown_path(
                image_path,
                markdown_output,
            )
        )

        return (
            f"![]({relative_path})"
        )

    text = IMAGE_MARKER_RE.sub(
        replace_image,
        text,
    )

    return (
        text,
        inserted,
        missing,
    )


# ============================================================
# Склейка Markdown
# ============================================================

def merge_markdown_files(
    files,
    markdown_output,
):
    chunks = []

    inserted = []
    missing = []

    for path in files:

        print(
            f"  Обработка: {path.name}"
        )

        text = path.read_text(
            encoding="utf-8",
        )

        (
            text,
            found,
            not_found,
        ) = process_markdown(
            text,
            markdown_output,
        )

        text = text.strip()

        if text:
            chunks.append(text)

        inserted.extend(
            found
        )

        missing.extend(
            not_found
        )

    result = "\n\n\n".join(
        chunks
    )

    result = result.rstrip() + "\n"

    return (
        result,
        inserted,
        missing,
    )


# ============================================================
# Создание PDF
# ============================================================

def create_pdf(
    markdown_file,
    pdf_file,
):
    """
    Создаёт PDF через:

        Pandoc
        XeLaTeX
    """

    # В resource-path добавляем:
    #
    # 1. папку Markdown
    # 2. корень images
    #
    # Благодаря этому Pandoc сможет
    # разрешить ../../images/v14/14-1.jpeg

    resource_paths = os.pathsep.join(
        [
            str(
                markdown_file.parent.resolve()
            ),
            str(
                IMAGES_ROOT.resolve()
            ),
        ]
    )

    command = [
        "pandoc",
        str(markdown_file),
        "-o",
        str(pdf_file),
        "--pdf-engine=pdflatex",
        f"--resource-path={resource_paths}",
        "-V",
        "geometry:margin=2cm",
    ]

    print()
    print(
        "Создание PDF..."
    )

    try:

        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    except FileNotFoundError:

        print()
        print(
            "ОШИБКА: команда 'pandoc' не найдена."
        )
        print()
        print(
            "Проверьте установку Pandoc."
        )

        return False

    if result.returncode == 0:
        return True

    print()
    print(
        "ОШИБКА при создании PDF:"
    )

    if result.stdout:
        print(
            result.stdout
        )

    if result.stderr:
        print(
            result.stderr
        )

    return False


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Склейка Markdown тома + "
            "вставка изображений + PDF"
        )
    )

    parser.add_argument(
        "--volume",
        type=int,
        required=True,
        help=(
            "Номер тома. "
            "Например: 14"
        ),
    )

    args = parser.parse_args()

    volume = str(
        args.volume
    )

    # --------------------------------------------------------
    # Проверяем структуру
    # --------------------------------------------------------

    print()
    print(
        "Корень проекта:"
    )
    print(
        f"  {PROJECT_ROOT}"
    )

    print()
    print(
        "Markdown:"
    )
    print(
        f"  {MARKDOWN_DIR}"
    )

    print()
    print(
        "Изображения:"
    )
    print(
        f"  {IMAGES_ROOT}"
    )

    if not MARKDOWN_DIR.exists():

        print()
        print(
            "ОШИБКА: папка Markdown не найдена:"
        )
        print(
            f"  {MARKDOWN_DIR}"
        )

        return 1

    if not IMAGES_ROOT.exists():

        print()
        print(
            "ОШИБКА: папка изображений не найдена:"
        )
        print(
            f"  {IMAGES_ROOT}"
        )

        return 1

    # --------------------------------------------------------
    # Пути результата
    # --------------------------------------------------------

    md_output = (
        MARKDOWN_DIR
        / f"{volume}-merged.md"
    )

    pdf_output = (
        MARKDOWN_DIR
        / f"{volume}-merged.pdf"
    )

    # --------------------------------------------------------
    # Находим Markdown
    # --------------------------------------------------------

    files = collect_markdown_files(
        volume
    )

    if not files:

        print()
        print(
            "ОШИБКА: Markdown-файлы не найдены."
        )

        print()
        print(
            "Ожидались файлы:"
        )

        print(
            f"  v{volume}-ch01.md"
        )

        print(
            f"  v{volume}-ch02.md"
        )

        print(
            "  ..."
        )

        print(
            f"  v{volume}-epilogue.md"
        )

        return 1

    # --------------------------------------------------------
    # Показываем порядок
    # --------------------------------------------------------

    print()
    print(
        "Файлы в порядке склейки:"
    )

    for number, path in enumerate(
        files,
        start=1,
    ):

        print(
            f"  {number:02d}. "
            f"{path.name}"
        )

    # --------------------------------------------------------
    # Склеиваем
    # --------------------------------------------------------

    print()
    print(
        "Обработка Markdown:"
    )

    (
        merged,
        inserted,
        missing,
    ) = merge_markdown_files(
        files,
        md_output,
    )

    md_output.write_text(
        merged,
        encoding="utf-8",
    )

    print()
    print(
        "Markdown создан:"
    )

    print(
        f"  {md_output}"
    )

    # --------------------------------------------------------
    # Статистика изображений
    # --------------------------------------------------------

    unique_inserted = list(
        dict.fromkeys(
            inserted
        )
    )

    unique_missing = list(
        dict.fromkeys(
            missing
        )
    )

    print()
    print(
        f"Вставлено изображений: "
        f"{len(inserted)}"
    )

    print(
        f"Уникальных изображений: "
        f"{len(unique_inserted)}"
    )

    if unique_inserted:

        print()
        print(
            "Вставленные изображения:"
        )

        for name in unique_inserted:

            print(
                f"  ✓ {name}"
            )

    if unique_missing:

        print()
        print(
            "ОТСУТСТВУЮЩИЕ ИЗОБРАЖЕНИЯ:"
        )

        for name in unique_missing:

            print(
                f"  ✗ {name}"
            )

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    pdf_success = create_pdf(
        md_output,
        pdf_output,
    )

    if pdf_success:

        print()
        print(
            "PDF создан:"
        )

        print(
            f"  {pdf_output}"
        )

    else:

        print()
        print(
            "PDF не создан."
        )

    # --------------------------------------------------------
    # Итог
    # --------------------------------------------------------

    print()
    print(
        "Готово."
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )