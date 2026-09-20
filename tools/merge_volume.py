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

Предисловие переводчика (ручной файл prefaces/v<N>.md, например
prefaces/v14.md) добавляется в начало тома как отдельный блок.
Файл заполняется вручную и скриптом никогда не изменяется.

PDF собирается автоматически:
    * есть typst/xelatex/lualatex/pdflatex → pandoc --pdf-engine=<движок>;
    * иначе (без LaTeX) → pandoc → HTML → headless Chrome/Edge
      (кириллица и изображения обрабатываются браузером);
    * движок можно задать явно: --pdf-engine browser|typst|xelatex|
      lualatex|pdflatex|none (none — только Markdown без PDF).

Оформление PDF:
    * цвет ссылок — --pdf-link-color (по умолчанию #1f4e79); в Typst он
      задаётся правилом `#show link` (через -V linkcolor нельзя: значение
      попадает в разметку, где «#» начинает код);
    * рамка и прочие стили — ручной файл prefaces/pdf-header.typ
      (--pdf-header <файл>). Пути к картинкам в Typst — от корня проекта
      (`image("border.webp")`); абсолютные и выходящие за корень запрещены.

Запуск:

    cd /d/skills/NovelEdit/noverl

    python tools/merge_volume.py --volume 14                    # авто (сейчас — Chrome)
    python tools/merge_volume.py --volume 14 --pdf-engine browser   # принудительно браузер
    python tools/merge_volume.py --volume 14 --pdf-engine none      # только Markdown
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Консоль Windows по умолчанию не в UTF-8: символы «✓»/«✗» в отчёте
# (и кириллица при перенаправлении вывода) вызывали UnicodeEncodeError
# ДО создания PDF. Принудительно включаем UTF-8.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ============================================================
# Пути проекта
# ============================================================

# Папка noverl/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# AINovelEdit/output/
MARKDOWN_DIR = PROJECT_ROOT / "AINovelEdit" / "output"

MERGE_DIR = MARKDOWN_DIR / "merge"

# images/
IMAGES_ROOT = PROJECT_ROOT / "images"

# Папка с предисловиями переводчика (заполняются вручную).
# Файл тома N: prefaces/vN.md — добавляется в начало смерженного тома
# как отдельный блок. Скрипт его никогда не изменяет.
PREFACES_ROOT = PROJECT_ROOT / "prefaces"

# Цвет ссылок в PDF (работает и для typst, и для браузерной печати)
PDF_LINK_COLOR = "#1f4e79"


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
# Предисловие переводчика
# ============================================================

PREFACE_SEPARATOR = "<!-- PREFACE_END -->"


def find_preface(volume):
    """
    Возвращает путь к предисловию тома или None.

    Ищется файл prefaces/v<N>.md (например, prefaces/v14.md).
    Файл заполняется вручную и скриптом не изменяется.
    """

    candidates = [
        PREFACES_ROOT / f"v{volume}.md",
        PREFACES_ROOT / f"v{volume}-preface.md",
    ]

    for path in candidates:

        if path.is_file():
            return path

    return None


def extract_volume_title(preface_path):
    """
    Извлекает название тома из файла prefaces/v<N>.md.

    Ожидаемый формат:

        **Название тома:** Святая Аквилеи

    Возвращает название без пробелов по краям.
    Если строка не найдена — возвращает None.
    """

    if preface_path is None or not preface_path.is_file():
        return None

    text = preface_path.read_text(encoding="utf-8")

    match = re.search(
        r"^\s*\*\*Название тома:\*\*\s*(.+?)\s*$",
        text,
        re.MULTILINE,
    )

    if not match:
        return None

    title = match.group(1).strip()

    return title or None


def load_preface(
    volume,
    markdown_output,
):
    """
    Читает предисловие тома и обрабатывает его как обычный Markdown
    (block-маркеры удаляются, img-маркеры заменяются изображениями).

    Возвращает (text, missing). text = None, если предисловия нет
    или оно пустое.
    """

    path = find_preface(volume)

    if path is None:

        print()
        print(
            "Предисловие не найдено "
            f"({PREFACES_ROOT / f'v{volume}.md'}) — пропускаю."
        )

        return (
            None,
            [],
        )

    print()
    print(
        "Предисловие:"
    )
    print(
        f"  {path}"
    )

    text = path.read_text(
        encoding="utf-8",
    )

    (text, _found, missing) = process_markdown(
        text,
        markdown_output,
    )

    text = text.strip()

    if not text:

        print()
        print(
            "Предисловие пустое, пропускаю."
        )

        return (
            None,
            missing,
        )

    return (
        text,
        missing,
    )


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
    preface=None,
):
    chunks = []

    inserted = []
    missing = []

    # --------------------------------------------------------
    # Предисловие переводчика — отдельный блок в начале тома
    # --------------------------------------------------------

    if preface:

        chunks.append(
            preface.strip() + "\n\n" + PREFACE_SEPARATOR
        )

        print(
            "  Предисловие добавлено в начало тома"
        )

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

# ============================================================
# Движки PDF
# ============================================================

# порядок предпочтения: typst, затем LaTeX (xelatex/lualatex умеют кириллицу)
PANDOC_PDF_ENGINES = ("typst", "xelatex", "lualatex", "pdflatex")
LATEX_ENGINES = ("xelatex", "lualatex", "pdflatex")

BROWSER_CANDIDATES = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
)

# Стиль для браузерной печати (A4, поля, кириллица, абзацный отступ).
# Цвет ссылок подставляется из --pdf-link-color.
PDF_CSS_TEMPLATE = """\
@page { size: A4; margin: 2cm; }
body { font-family: "PT Serif", Georgia, "Times New Roman", serif;
       font-size: 11.5pt; line-height: 1.5; text-align: justify;
       hyphens: auto; }
h1 { page-break-before: always; text-align: center; }
h1:first-of-type { page-break-before: avoid; }
p { margin: 0 0 0.6em 0; text-indent: 1.4em; }
img { max-width: 100%; height: auto; display: block; margin: 0.6em auto; }
hr { border: none; border-top: 1px solid #999; margin: 1.2em 0;
     break-after: page; }
a { color: %(link)s; }
code, pre { font-family: Consolas, "Courier New", monospace; }
"""


def pdf_css(link_color):
    """
    CSS для браузерной печати с заданным цветом ссылок.
    """

    return PDF_CSS_TEMPLATE % {"link": link_color}


def find_pandoc_pdf_engine():
    """
    Первый доступный движок pandoc (typst/LaTeX) или None.
    """

    for engine in PANDOC_PDF_ENGINES:

        if shutil.which(engine):
            return engine

    return None


def find_browser():
    """
    Путь к Chrome/Edge/Chromium (для печати HTML → PDF) или None.
    """

    for name in ("chrome", "msedge", "chromium", "chromium-browser"):

        found = shutil.which(name)

        if found:
            return found

    for candidate in BROWSER_CANDIDATES:

        if Path(candidate).is_file():
            return candidate

    return None


def _run(command, cwd=None):
    """
    Запускает внешнюю команду. Возвращает (returncode, stdout, stderr).
    """

    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=cwd,
    )

    return (
        result.returncode,
        result.stdout or "",
        result.stderr or "",
    )


def _link_color_typ_file(pdf_file, link_color):
    """
    Пишет временный Typst-файл с правилом цвета ссылок.

    ВАЖНО: через `-V linkcolor=...` цвет не передать — в шаблоне pandoc
    значение попадает в разметку `[...]`, где `#1f4e79` парсится как код
    («invalid number suffix»). Поэтому правило задаётся явным `#show link`.
    """

    path = pdf_file.with_suffix(".link-color.typ")
    path.write_text(
        '#show link: set text(fill: rgb("{}"))\n'.format(link_color),
        encoding="utf-8",
    )
    return path


def _resource_path(markdown_file):
    """
    resource-path для pandoc: папка Markdown + корень images
    (чтобы разрешались ссылки вида ../../images/v14/14-1.jpeg).
    """

    return os.pathsep.join(
        [
            str(
                markdown_file.parent.resolve()
            ),
            str(
                IMAGES_ROOT.resolve()
            ),
        ]
    )


def find_pdf_header():
    """
    Ручной Typst-файл для тонкой настройки PDF (рамки, стили):
    prefaces/pdf-header.typ. Подключается только для движка typst.
    """

    candidates = [
        PREFACES_ROOT / "pdf-header.typ",
        PREFACES_ROOT / "pdf-header.typ.txt",
    ]

    for candidate in candidates:

        if Path(candidate).is_file():
            return candidate

    return None


def _typst_break_input(markdown_file, out_file):
    """
    Готовит копию Markdown с явными разрывами страниц (typst):

    * после предисловия (после разделителя «***») — чтобы иллюстрации и
      первая глава не шли на странице предисловия;
    * перед каждым заголовком уровня 1, КРОМЕ первого (предисловия) —
      чтобы каждая глава начиналась с новой страницы и не появлялось
      пустой первой страницы.

    Возвращает число вставленных разрывов.
    """

    lines = markdown_file.read_text(encoding="utf-8").splitlines()
    out = []
    seen_h1 = 0
    seen_sep = False
    in_fence = False
    breaks = 0

    # «Глава первая. Название» → после точки явный перенос строки,
    # чтобы номер главы и название главы были отдельными «абзацами»
    # внутри одного заголовка (и внутри одного блока с уголками).
    # Raw inline `{=typst}` вставляется pandoc'ом напрямую в Typst-разметку.
    chapter_split = re.compile(r"^(#\s+Глава\s+[^.]*\.)\s+(.+)$")

    for line in lines:

        if line.startswith("```"):
            in_fence = not in_fence

        # разрыв перед каждой главой (кроме первой — предисловия)
        if (not in_fence and line.startswith("# ")
                and not line.startswith("## ")):

            seen_h1 += 1

            if seen_h1 > 1:
                out += ["```{=typst}", "#pagebreak()", "```", ""]
                breaks += 1

        # «Глава первая. Название» → разрыв строки после точки
        if not in_fence and chapter_split.match(line):
            line = chapter_split.sub(
                r"\1 `#linebreak() #v(0.5em, weak: true)`{=typst} \2",
                line,
            )

        out.append(line)

        # разрыв после предисловия (после разделителя ***), чтобы
        # следующие за ним иллюстрации не попадали на страницу предисловия
        if (not in_fence and not seen_sep
                and line.strip() == PREFACE_SEPARATOR):

            seen_sep = True
            out += ["", "```{=typst}", "#pagebreak()", "```", ""]
            breaks += 1

    out_file.write_text(
        "\n".join(out) + "\n",
        encoding="utf-8",
    )

    return breaks


def _create_pdf_pandoc(
    markdown_file,
    pdf_file,
    engine,
    link_color,
    typst_header=None,
):
    """
    PDF через pandoc --pdf-engine=<engine> (LaTeX/Typst).
    """

    command = [
        "pandoc",
        str(markdown_file),
        "-o",
        str(pdf_file),
        f"--pdf-engine={engine}",
        f"--resource-path={_resource_path(markdown_file)}",
    ]

    if engine in LATEX_ENGINES:

        command += [
            "-V",
            "geometry:margin=2cm",
        ]

    link_file = None
    break_file = None

    if engine == "typst":

        # цвет ссылок — отдельным подключаемым файлом (см. _link_color_typ_file)
        link_file = _link_color_typ_file(pdf_file, link_color)
        command += [
            "--include-in-header",
            str(link_file),
        ]

        # каждая глава — с новой страницы (pandoc сам разрывов не делает):
        # собираем копию Markdown с явными #pagebreak() перед главами
        break_file = pdf_file.with_suffix(".typst.md")
        n_breaks = _typst_break_input(markdown_file, break_file)
        command[1] = str(break_file)

        if n_breaks:
            print(
                "Разрывы страниц (предисловие и главы): %d" % n_breaks
            )

        # ручной файл стилей (рамки и пр.) — prefaces/pdf-header.typ
        if typst_header is None:
            typst_header = find_pdf_header()

        if typst_header:
            command += [
                "--include-in-header",
                str(typst_header),
            ]
            print(
                f"Typst-стили: {typst_header}"
            )

    (returncode, out, err) = _run(command, cwd=str(PROJECT_ROOT))

    if returncode == 0:

        # временные файлы сборки больше не нужны (при ошибке остаются)
        for tmp_file in (link_file, break_file):

            if tmp_file is not None:
                tmp_file.unlink(missing_ok=True)

    if returncode == 0:
        return True

    print()
    print(
        f"ОШИБКА pandoc (движок {engine}):"
    )

    if out:
        print(out)

    if err:
        print(err)

    return False


def _create_pdf_browser(
    markdown_file,
    pdf_file,
    link_color,
):
    """
    PDF без LaTeX: pandoc → HTML (встроенные ресурсы) → печать headless
    Chrome/Edge. Кириллица и картинки обрабатываются браузером.
    """

    browser = find_browser()

    if browser is None:

        print()
        print(
            "ОШИБКА: не найден ни LaTeX/Typst-движок, ни Chrome/Edge."
        )
        print(
            "Установите Chrome (или MiKTeX для pdflatex) — тогда PDF соберётся."
        )

        return False

    html_file = pdf_file.with_suffix(".html")
    css_file = pdf_file.with_suffix(".css")

    css_file.write_text(
        pdf_css(link_color),
        encoding="utf-8",
    )

    command = [
        "pandoc",
        str(markdown_file),
        "-o",
        str(html_file),
        "--standalone",
        "--embed-resources",
        f"--resource-path={_resource_path(markdown_file)}",
        f"--css={css_file}",
        "--metadata",
        f"title={pdf_file.stem}",
    ]

    (returncode, out, err) = _run(command)

    if returncode != 0:

        print()
        print(
            "ОШИБКА pandoc (Markdown → HTML):"
        )

        if out:
            print(out)

        if err:
            print(err)

        return False

    profile = pdf_file.parent / ".chrome-profile"

    command = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--user-data-dir={profile}",
        f"--print-to-pdf={pdf_file}",
        html_file.resolve().as_uri(),
    ]

    (returncode, out, err) = _run(command)

    shutil.rmtree(
        profile,
        ignore_errors=True,
    )

    if returncode == 0 and pdf_file.exists():

        # промежуточные HTML/CSS больше не нужны (при ошибке — остаются
        # для разбора причины)
        for tmp_file in (html_file, css_file):

            try:
                tmp_file.unlink()
            except OSError:
                pass

        return True

    print()
    print(
        "ОШИБКА печати PDF через браузер:"
    )

    if out:
        print(out)

    if err:
        print(err)

    return False


def create_pdf(
    markdown_file,
    pdf_file,
    engine="auto",
    link_color=PDF_LINK_COLOR,
    typst_header=None,
):
    """
    Создаёт PDF из склеенного Markdown.

    engine:
        auto     — движок pandoc (typst/LaTeX), иначе headless Chrome/Edge;
        typst | xelatex | lualatex | pdflatex — конкретный движок pandoc;
        browser  — принудительно pandoc → HTML → Chrome/Edge (без LaTeX);
        none     — PDF не создаётся.

    link_color — цвет ссылок; typst_header — ручной Typst-файл стилей
    (prefaces/pdf-header.typ): рамки, фоны и прочие show/set-правила.
    """

    print()
    print(
        "Создание PDF..."
    )

    if engine == "none":

        print(
            "PDF пропущен (engine=none)."
        )

        return False

    choice = engine

    if choice == "auto":

        choice = find_pandoc_pdf_engine() or "browser"

    try:

        if choice == "browser":

            print(
                "Движок PDF: headless Chrome/Edge (LaTeX/Typst не найден)."
            )

            return _create_pdf_browser(
                markdown_file,
                pdf_file,
                link_color,
            )

        print(
            f"Движок PDF: pandoc --pdf-engine={choice}"
        )

        return _create_pdf_pandoc(
            markdown_file,
            pdf_file,
            choice,
            link_color,
            typst_header,
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

    parser.add_argument(
        "--pdf-engine",
        default="auto",
        choices=(
            "auto",
            "browser",
            "typst",
            "xelatex",
            "lualatex",
            "pdflatex",
            "none",
        ),
        help=(
            "Движок PDF: auto — pandoc (typst/LaTeX), иначе headless "
            "Chrome/Edge; browser — принудительно через браузер; "
            "none — PDF не создавать"
        ),
    )

    parser.add_argument(
        "--pdf-link-color",
        default=PDF_LINK_COLOR,
        metavar="COLOR",
        help=f"цвет ссылок в PDF (по умолчанию {PDF_LINK_COLOR})",
    )

    parser.add_argument(
        "--pdf-header",
        default=None,
        metavar="FILE",
        help=(
            "Typst-файл стилей PDF (рамки, фоны; только для движка typst). "
            "По умолчанию используется prefaces/pdf-header.typ, если есть"
        ),
    )

    args = parser.parse_args()

    volume = str(
        args.volume
    )

    # --------------------------------------------------------
    # Название тома из prefaces/v<N>.md
    # --------------------------------------------------------

    preface_path = find_preface(volume)

    if preface_path is None:
        print()
        print(
            "ОШИБКА: файл предисловия не найден:"
        )
        print(
            f"  {PREFACES_ROOT / f'v{volume}.md'}"
        )
        return 1

    volume_title = extract_volume_title(preface_path)

    if not volume_title:
        print()
        print(
            "ОШИБКА: в предисловии не найдено название тома:"
        )
        print(
            "  **Название тома:** ..."
        )
        print(
            f"  Файл: {preface_path}"
        )
        return 1

    print()
    print(
        f"Название тома: {volume_title}"
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
        MERGE_DIR
        / f"Том {volume} — {volume_title}.md"
    )

    pdf_output = (
        MERGE_DIR
        / f"Том {volume} — {volume_title}.pdf"
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

    # --------------------------------------------------------
    # Предисловие переводчика (ручной файл)
    # --------------------------------------------------------

    (preface, preface_missing) = load_preface(
        volume,
        md_output,
    )

    (
        merged,
        inserted,
        missing,
    ) = merge_markdown_files(
        files,
        md_output,
        preface,
    )

    md_output.write_text(
        merged,
        encoding="utf-8",
    )

    # не найденные изображения из предисловия учитываются в общей статистике
    missing.extend(preface_missing)

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
        args.pdf_engine,
        args.pdf_link_color,
        args.pdf_header,
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