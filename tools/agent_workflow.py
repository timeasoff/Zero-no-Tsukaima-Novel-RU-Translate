#!/usr/bin/env python3
"""
Оркестратор рабочего процесса AI-агента проекта AINovelEdit.

Внутри два независимых раздела:
PROMPTS — LLM-промпты (PromptInfo): генерация готового задания агенту,
  копирование в буфер и сохранение в папку agent_prompts/;
ACTIONS — технические действия оркестратора (ActionInfo): запускают
  детерминированные скрипты проекта и НЕ создают LLM-промптов.

Основные возможности:
- выбор режима через числовой ввод в консоли;
- главное меню сгруппировано по темам («Работа с главой», «Аудиты текста»);
- отдельное МЕНЮ СМЫСЛОВОГО АУДИТА с фиксированным порядком фаз:
  Omission Pre-check → Auditor A → Auditor B → Pragmatic Auditor C →
  Фаза 1 (blind) → Фаза 2 (evidence review); любой этап можно открыть
  напрямую, но при отсутствии обязательных входов (файл Фазы 1, запуски
  A/B/C) выводится предупреждение;
- кнопка «Следующий промпт (фаза)» / «Следующий этап»: переход к следующей
  фазе пайплайна с показом экрана подтверждения;
- отслеживание идентификаторов фаз: audit_run_id печатается сразу при
  генерации, в экране подтверждения перечисляются идентификаторы прошлых
  запусков этапа, а в пунктах аудит-меню — сколько запусков каждой фазы
  уже сделано;
- выбор тома и главы (поддержка числовых и строковых идентификаторов);
- быстрая навигация между главами (следующая / предыдущая);
- автоматические идентификаторы vNN / chYY или кастомные названия;
- централизованный контекст проекта;
- поддержка отдельных режимов аудита и обработки;
- режим обработки одного блока;
- режим поиска пропущенных отрывков (GAP-аудит) — LEGACY/DEPRECATED,
  из активного меню убран (см. prompt_gap_audit); поиск пропусков выполняет
  AINovelEdit/scripts/omission_precheck.py;
- разбор решений пользователя (OPEN / DEFERRED, PROVISIONAL);
- подробное описание режима перед подтверждением;
- независимый смысловой аудит (SMA): отдельные режимы Auditor A, Auditor B,
  Pragmatic Auditor C (прагматика / подтекст) и Analyzer в двух НЕЗАВИСИМЫХ
  фазах — «Фаза 1 (blind)» (только JA + RU + контекст, без evidence) и
  «Фаза 2 (evidence review)» (A/B/C + omission pre-check) — (уникальный
  audit_run_id на каждый запуск, изоляция запусков, результаты внутри
  output/_audit/sma/<chapter>/<a|b|c|analysis|precheck>/); Фаза 2 адресует
  слепой вывод Фазы 1 конкретным файлом (при нескольких прогонах — самый
  свежий) и фиксирует выбранный файл в inputs.phase1 результата;
- автоматическое копирование готового промпта в буфер обмена;
- сохранение готового промпта в markdown-файл
  `agent_prompts/agent_prompt.<chapter>.<slug>.md` (отдельная папка в корне
  проекта, чтобы корень не засорялся), на который можно сослаться в задаче
  агенту (папка в .gitignore, файлы перезаписываются при каждой генерации;
  имя содержит главу и режим, поэтому параллельные запуски в нескольких
  терминалах не затирают друг другу — общий agent_prompt.md отменён);
  запись атомарная (tmp + os.replace), прерывание не оставляет
  обрезанный файл;
- ACTIONS оркестратора: Omission Pre-check — детерминированная проверка
  пропусков перед A/B/C (запускает AINovelEdit/scripts/omission_precheck.py;
  не является LLM-аудитом и не изменяет перевод).
Запускать из корня проекта:
python tools/agent_workflow.py
"""
from __future__ import annotations

import base64
import contextlib
import io
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

# ============================================================================
# КОНСТАНТЫ
# ============================================================================
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AINOVELEDIT = os.path.join(ROOT, "AINovelEdit")
TERMINAL_WIDTH = 78
# Готовые промпт-инструкции складываются в отдельную папку
# <PROJECT_ROOT>/agent_prompts/, а не в корень проекта: файлов много
# (глава × режим), корень ими быстро засоряется.
# Внутри: agent_prompt.<chapter>.<slug>.md (паттерн в .gitignore:
# /agent_prompts/). Имя содержит главу и режим, поэтому параллельные
# запуски генератора в разных терминалах пишут в РАЗНЫЕ файлы и не
# затирают друг друга. Запись атомарная: временный файл + os.replace
# (прерывание не оставляет обрезанный промпт).
PROMPT_FILE_PREFIX = "agent_prompt"
PROMPT_DIR_NAME = "agent_prompts"

# Разделы главного меню (порядок вывода).
GROUP_CHAPTER = "Работа с главой"
GROUP_AUDITS = "Аудиты текста"
GROUP_SMA = "Смысловой аудит"
GROUP_ORDER = (GROUP_CHAPTER, GROUP_AUDITS, GROUP_SMA)

# ============================================================================
# УТИЛИТЫ ВЫВОДА
# ============================================================================
def clear_screen() -> None:
    """Очистить экран."""
    if sys.platform == "win32":
        os.system("cls")
    else:
        print("\033[2J\033[H", end="")

def separator(char: str = "-", width: int = TERMINAL_WIDTH) -> None:
    """Вывести разделитель."""
    print(char * width)

def print_wrapped(
    text: str,
    width: int = TERMINAL_WIDTH,
    indent: str = "",
) -> None:
    """Вывести текст с автоматическим переносом строк."""
    if not text:
        print()
        return
    for line in text.splitlines():
        if not line.strip():
            print()
            continue
        wrapped = textwrap.wrap(
            line,
            width=max(20, width - len(indent)),
            break_long_words=False,
            break_on_hyphens=False,
        )
        if not wrapped:
            print()
            continue
        for part in wrapped:
            print(indent + part)

# ============================================================================
# ДАННЫЕ ГЛАВЫ
# ============================================================================
@dataclass
class Chapter:
    volume: int
    chapter_raw: str  # Может быть числом ("2") или строкой ("afterword", "ch00")

    @property
    def is_numeric(self) -> bool:
        """Проверяет, является ли сырой ввод числом."""
        return self.chapter_raw.isdigit()

    @property
    def chapter_num(self) -> int | None:
        """Возвращает номер главы как int, если это числовая глава."""
        return int(self.chapter_raw) if self.is_numeric else None

    @property
    def volume_id(self) -> str:
        return f"v{self.volume:02d}"

    @property
    def chapter_id(self) -> str:
        if self.is_numeric:
            return f"ch{int(self.chapter_raw):02d}"
        return self.chapter_raw

    @property
    def chapter_id_full(self) -> str:
        return f"{self.volume_id}-{self.chapter_id}"

    @property
    def volume_file_id(self) -> str:
        """Идентификатор тома для имён ФАЙЛОВ: без ведущего нуля (v1, v2, v14)."""
        return f"v{self.volume}"

    @property
    def file_name(self) -> str:
        # Файлы глав в проекте — без ведущего нуля (v2-ch06.md): translates/,
        # output/, merged/, _prefilter/. «v02» остаётся идентификатором тома
        # в заголовках и в отчётах полного аудита.
        return f"{self.volume_file_id}-{self.chapter_id}.md"

    @property
    def output_path(self) -> str:
        return os.path.join(AINOVELEDIT, "output", self.file_name)

    @property
    def log_path(self) -> str:
        return os.path.join(AINOVELEDIT, "output", "_log",
                            f"{self.volume_file_id}-log.md")

    @property
    def audit_path(self) -> str:
        # Отчёты аудита: том 2 ведётся как v02-chYY.md (шаблон AGENTS.md
        # «vXX-chYY»), том 1 — как v1-chYY.md. Если существует вариант без
        # ведущего нуля (и vNN-варианта нет) — берём его; новый файл — по vNN.
        padded = os.path.join(AINOVELEDIT, "output", "_audit",
                              f"{self.volume_id}-{self.chapter_id}.md")
        plain = os.path.join(AINOVELEDIT, "output", "_audit",
                             f"{self.volume_file_id}-{self.chapter_id}.md")
        if os.path.exists(plain) and not os.path.exists(padded):
            return plain
        return padded

    @property
    def ja_path(self) -> str:
        return os.path.join(AINOVELEDIT, "translates", "ja", self.file_name)

    @property
    def en_path(self) -> str:
        return os.path.join(AINOVELEDIT, "translates", "en", self.file_name)

    @property
    def merged_path(self) -> str:
        return os.path.join(AINOVELEDIT, "translates", "_report", "merged", self.file_name)

    @property
    def ru_path(self) -> str:
        return os.path.join(AINOVELEDIT, "translates", "ru", self.file_name)

# ============================================================================
# ВВОД И НАВИГАЦИЯ
# ============================================================================
def clean_chapter_input(raw: str) -> str:
    """Очищает ввод главы: убирает .md и префикс тома, если он есть."""
    raw = raw.strip()
    if raw.lower().endswith(".md"):
        raw = raw[:-3]
    # Если ввели полностью, например v01-ch02, оставляем только ch02
    match = re.match(r"^v\d+-(.*)$", raw, re.IGNORECASE)
    if match:
        raw = match.group(1)
    return raw

def ask_int(prompt: str, minimum: int = 1) -> int:
    """Запросить положительное целое число."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value < minimum:
                raise ValueError
            return value
        except ValueError:
            print(f"  Введите целое число не меньше {minimum}.")

def ask_chapter() -> Chapter:
    """Выбрать том и главу."""
    print()
    print("Выбор главы")
    separator()
    print()
    volume = ask_int("Номер тома: ")
    print()
    while True:
        chapter_raw = input("Номер или название главы (например, 2, 0, afterword): ").strip()
        chapter_raw = clean_chapter_input(chapter_raw)
        if chapter_raw:
            break
        print("  Название не может быть пустым.")
    return Chapter(volume=volume, chapter_raw=chapter_raw)

def ask_custom_chapter(current_volume: int, prompt_text: str) -> Chapter | None:
    """Запросить кастомное название главы или номер. Возвращает None при отмене."""
    raw = input(prompt_text).strip()
    if not raw:
        return None
    raw = clean_chapter_input(raw)
    if not raw:
        return None
    return Chapter(volume=current_volume, chapter_raw=raw)

def navigate_next(ch: Chapter) -> Chapter | None:
    """Переход к следующей главе."""
    if ch.is_numeric:
        return Chapter(ch.volume, str(ch.chapter_num + 1))
    return ask_custom_chapter(ch.volume, "Введите название следующей главы или номер (Enter — отмена): ")

def navigate_prev(ch: Chapter) -> Chapter | None:
    """Переход к предыдущей главе."""
    if ch.is_numeric:
        if ch.chapter_num > 1:
            return Chapter(ch.volume, str(ch.chapter_num - 1))
        return ask_custom_chapter(ch.volume, "Это первая числовая глава. Введите название (например, afterword) или номер (Enter — отмена): ")
    return ask_custom_chapter(ch.volume, "Введите название предыдущей главы или номер (Enter — отмена): ")

def ask_block_number() -> int:
    """Запросить номер блока."""
    return ask_int("Номер блока: ")

# ============================================================================
# КОНТЕКСТ ПРОЕКТА
# ============================================================================
def project_context(ch: Chapter) -> str:
    """
    Общий контекст, который добавляется в каждый промпт.
    """
    return f"""
КОНТЕКСТ ПРОЕКТА
Проект: AINovelEdit
Том: {ch.volume_id}
Глава: {ch.chapter_id}
Идентификатор главы: {ch.chapter_id_full}
Корень проекта:
{AINOVELEDIT}
Основные инструкции агента:
{os.path.join(AINOVELEDIT, "AGENTS.md")}
Японский оригинал:
{ch.ja_path}
Английский текст:
{ch.en_path}
Русский текст:
{ch.ru_path}
Трёхъязычное зеркало (JA/EN/RU/ED_RU по смысловым блокам):
{ch.merged_path}
Словарь терминов:
{os.path.join(AINOVELEDIT, "dictionary.md")}
Справочник обращений:
{os.path.join(AINOVELEDIT, "addresses.md")}
Завершённые тома (источник истины при расхождениях, read-only):
{os.path.join(AINOVELEDIT, "completed.md")}
Текущий результат:
{ch.output_path}
Лог:
{ch.log_path}
Аудит:
{ch.audit_path}
ВАЖНО
Японский текст является основным источником смысла.
Английский текст используется как вспомогательный источник для сверки.
Не следует автоматически считать английскую формулировку более правильной,
если она расходится с японским оригиналом.
Перед изменением текста необходимо учитывать AGENTS.md,
словарь терминов и существующие правила проекта.
Единица работы — смысловой блок (`<!-- block: N -->`); границу блока
не переносить, абзацы внутри блока можно перестраивать.
Завершённые тома (completed.md) — источник истины при расхождениях
терминов/имён/названий/обращений; их текст не редактируется. Расхождение
фиксируй в отчёте аудита, решение — в пользу формы из завершённого тома
(исключение — ручная правка пользователем в dictionary.md/addresses.md).
""".strip()

# ============================================================================
# SMA (НЕЗАВИСИМЫЙ СМЫСЛОВОЙ АУДИТ): ID, ПУТИ, КОНТЕКСТ
# ============================================================================
# Новая архитектура смыслового аудита:
#   один текущий RU → Auditor A (своя сессия) ‖ Auditor B (своя сессия)
#   ‖ Pragmatic Auditor C (своя сессия) → Analyzer (своя сессия)
#   → правка только ясных ошибок, спорное — в отчёт.
# Каждый запуск A/B/C — самостоятельный эксперимент: у него свой audit_run_id,
# свой выходной файл и НЕТ доступа к результатам других запусков.
# C НЕ является третьим универсальным semantic auditor: A закрывает
# микро-семантику, B — макро-семантику и логику, C — только прагматику
# (коммуникативный акт, подтекст, коммуникативную силу реплики).
SMA_AUDIT_DIR = "_audit"                  # output/_audit/
SMA_DIR_NAME = "sma"                      # output/_audit/sma/
SMA_REL_ROOT = f"output/{SMA_AUDIT_DIR}/{SMA_DIR_NAME}"
# Каноническая раскладка каталогов главы (storage):
#   a/        evidence Auditor A
#   b/        evidence Auditor B
#   c/        evidence Auditor C
#   precheck/ детерминированное omission-evidence (НЕ аудитор, НЕ run kind)
#   analysis/ финальные результаты Analyzer + слепые выводы Фазы 1
#             (<id>.phase1.json — не обычные final-запуски)
#             Фаза 2 адресует Фазу 1 конкретным файлом (при нескольких
#             прогонах — самый свежий по mtime, см. sma_phase1_files) и
#             фиксирует выбранный файл в inputs.phase1 результата
SMA_KINDS = ("a", "b", "c", "analysis")   # типы результатов внутри главы
# Общий Omission Pre-check (scripts/omission_precheck.py) кладёт evidence в
# отдельный каталог главы; это НЕ каталог аудитора, НЕ run_id-результат и
# НЕ член SMA_KINDS (kind="precheck" существует только как путь).
SMA_PRECHECK_KIND = "precheck"
SMA_PRECHECK_FILE = "omission-precheck.json"
_SMA_ISSUED_IDS: set[str] = set()         # гарантия уникальности в процессе

# Формулировки изоляции (используются и в промптах, и в self-test).
SMA_AUTONOMY_NOTE = (
    "РАБОТАЙ АВТОНОМНО. Все данные для аудита приведены в этом задании. "
    "Не перечисляй содержимое каталогов и не открывай никакие файлы, кроме "
    "перечисленных в задании; единственное исключение — OWN SKILL, если он "
    "явно указан в задании (это инструкции самого аудитора, а не чужие "
    "результаты)."
)
SMA_OWN_FILE_NOTE = (
    "Единственный файл, который ты создаёшь, — результат этого запуска "
    "(см. OUTPUT FILE). Любые другие файлы в папке результата в задание не "
    "входят: не читай их, не сравнивай с ними свой результат и не делай "
    "выводов из их наличия или отсутствия."
)
# Чего A/B/C по-прежнему НЕ видят (собственный skill разрешён, всё остальное
# закрыто). Проверяется self-test вместе со SMA_AUTONOMY_NOTE / OWN SKILL.
SMA_FORBIDDEN_INPUTS_NOTE = (
    "ЗАПРЕЩЁННЫЕ ВХОДЫ (не читай и не используй, даже если попадутся): "
    "чужие skill-файлы, AGENTS.md, dictionary.md, addresses.md, "
    "результаты/evidence других запусков и других этапов, старые отчёты "
    "аудита. Если такой материал оказался в задании — не используй его "
    "и сообщи об ошибке генерации."
)

# Иерархия источников для промптов Analyzer ОБЕИХ фаз:
# JA = источник истины, RU = проверяемый перевод, EN = только справочный
# материал. Проверяется self-test по реальному сгенерированному prompt
# (см. self_test_semantic_prompts), а не только по тексту skill-файла.
SMA_SOURCE_HIERARCHY_NOTE = (
    "ИЕРАРХИЯ ИСТОЧНИКОВ (SOURCE PRIORITY)\n"
    "JA — authoritative source of truth (авторитетный источник истины).\n"
    "RU — text under review (проверяемый перевод).\n"
    "EN — reference only (только справочный материал), не источник смысла.\n"
    "Основная проверка — JA → RU. Не EN → RU и не JA → EN → RU: EN не является\n"
    "промежуточным эталоном перевода.\n"
    "JA has priority over EN (JA > EN) при любом конфликте: конфликтующую с JA\n"
    "интерпретацию EN игнорируй.\n"
    "EN must not be treated as authority.\n"
    "Совпадение RU с EN само по себе не является доказательством правильности\n"
    "перевода.\n"
    "Конфликтный случай JA = X, EN = Y, RU = Y: вывод «RU корректен, потому что\n"
    "совпадает с EN» запрещён — оценивай соответствие RU японскому оригиналу\n"
    "(JA → RU)."
)

def sma_chapter_id(ch: Chapter) -> str:
    """Идентификатор главы для каталогов SMA: как в именах файлов output/.

    ``v3`` + ``ch03`` → ``v3-ch03`` (ведущий ноль тома не используется:
    так же назван файл output/v3-ch03.md).
    """
    return f"{ch.volume_file_id}-{ch.chapter_id}"

def sma_chapter_dir(ch: Chapter, kind: str) -> str:
    """Абсолютный путь каталога результатов одного типа для этой главы."""
    return os.path.join(AINOVELEDIT, "output", SMA_AUDIT_DIR, SMA_DIR_NAME,
                        sma_chapter_id(ch), kind)

def sma_result_rel_path(ch: Chapter, kind: str, run_id: str, ext: str = "json") -> str:
    """Путь результата относительно корня AINovelEdit (прямые слэши)."""
    return f"{SMA_REL_ROOT}/{sma_chapter_id(ch)}/{kind}/{run_id}.{ext}"

def sma_result_abs_path(ch: Chapter, kind: str, run_id: str, ext: str = "json") -> str:
    """Абсолютный путь файла результата (kind: a / b / c / analysis)."""
    return os.path.join(sma_chapter_dir(ch, kind), f"{run_id}.{ext}")

def _sma_run_id_taken(ch: Chapter, run_id: str) -> bool:
    """True, если идентификатор запуска уже занят файлом результата."""
    for kind in SMA_KINDS:
        folder = sma_chapter_dir(ch, kind)
        for ext in ("json", "md"):
            if os.path.exists(os.path.join(folder, f"{run_id}.{ext}")):
                return True
    return False

def new_audit_run_id(ch: Chapter | None = None) -> str:
    """Уникальный идентификатор запуска аудита: ``YYYYMMDD-HHMMSS-xxxx``.

    Генерируется при создании prompt, поэтому повторные запуски A/B не
    перезаписывают предыдущие результаты: каждый запуск пишет свой файл.
    Номер вручную увеличивать не нужно.
    """
    while True:
        run_id = f"{datetime.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:4]}"
        if run_id in _SMA_ISSUED_IDS:
            continue
        if ch is not None and _sma_run_id_taken(ch, run_id):
            continue
        _SMA_ISSUED_IDS.add(run_id)
        return run_id

def sma_existing_runs(ch: Chapter, kind: str) -> list[str]:
    """Уже существующие run_id результатов A/B/C/final-Analyzer этой главы.

    Используется Analyzer'ом: он учитывает ВСЕ существующие запуски (механизма
    ручного выбора отдельных run_id нет), а не только последний. Слепые выводы
    Фазы 1 (``<id>.phase1.json``) сюда НЕ попадают — это не финальные
    analysis-результаты; для них есть ``sma_existing_phase1_runs``.
    Ничего не создаёт и не изменяет.
    """
    folder = sma_chapter_dir(ch, kind)
    if not os.path.isdir(folder):
        return []
    ids = [os.path.splitext(name)[0] for name in os.listdir(folder)
           if name.lower().endswith(".json")
           and not name.lower().endswith(".phase1.json")]
    return sorted(ids)

def sma_existing_phase1_runs(ch: Chapter) -> list[str]:
    """Существующие слепые выводы Фазы 1 (``analysis/<id>.phase1.json``).

    Отдельный helper: phase1-файлы лежат в том же каталоге ``analysis/``, но
    семантически НЕ являются обычными финальными analysis-запусками и не
    должны путаться с ними. Ничего не создаёт и не изменяет.
    """
    folder = sma_chapter_dir(ch, "analysis")
    if not os.path.isdir(folder):
        return []
    return sorted(os.path.splitext(name)[0] for name in os.listdir(folder)
                  if name.lower().endswith(".phase1.json"))

def _sma_phase1_file_name(value: str) -> str:
    """Привести значение к имени файла Фазы 1 (``<id>.phase1.json``).

    Принимает имя файла, ``<id>.phase1`` или голый ``<id>``: нужно и при
    чтении каталога, и для симуляции в self-test.
    """
    name = os.path.basename(str(value).strip())
    if name.endswith(".json"):
        return name
    if name.endswith(".phase1"):
        return f"{name}.json"
    return f"{name}.phase1.json"

def _sma_phase1_sort(found: list[tuple[float, str]]) -> list[str]:
    """Имена файлов Фазы 1 в порядке «самый свежий — первым».

    ``found`` — пары (mtime, имя файла); при равном mtime порядок по имени.
    Чистая функция: вызывается и при чтении каталога, и в self-test.
    """
    return [name for _, name in
            sorted((-mtime, name) for mtime, name in found)]

def sma_phase1_files(ch: Chapter) -> list[str]:
    """Файлы слепых выводов Фазы 1 этой главы, самый свежий — первым.

    Имена — с расширением (``<run_id>.phase1.json``); порядок по времени
    изменения файла (mtime), при равенстве — по имени. Пустой список
    означает, что Фаза 1 для главы ещё не выполнялась: Фаза 2 в этом случае
    работать не может. Ничего не создаёт и не изменяет.
    """
    folder = sma_chapter_dir(ch, "analysis")
    if not os.path.isdir(folder):
        return []
    found: list[tuple[float, str]] = []
    for name in os.listdir(folder):
        if not name.lower().endswith(".phase1.json"):
            continue
        try:
            mtime = os.path.getmtime(os.path.join(folder, name))
        except OSError:
            mtime = 0.0
        found.append((mtime, name))
    return _sma_phase1_sort(found)

def _sma_phase1_files_for(ch: Chapter,
                          runs: dict[str, list[str]] | None) -> list[str]:
    """Файлы Фазы 1 для промпта Фазы 2 (с диска или из симуляции self-test).

    ``runs["phase1"]`` (только self-test) задаёт список в порядке «самый
    свежий — первым»; в рабочем режиме порядок берётся из ``sma_phase1_files``.
    """
    if runs is not None and "phase1" in runs:
        return [_sma_phase1_file_name(v) for v in runs["phase1"]]
    return sma_phase1_files(ch)

def _sma_phase1_order_selftest() -> bool:
    """Проверка порядка файлов Фазы 1 (без записи на диск).

    Самый свежий mtime — первым; при равном mtime порядок по имени.
    """
    found = [(100.0, "b.phase1.json"), (300.0, "a.phase1.json"),
             (200.0, "c.phase1.json"), (300.0, "z.phase1.json")]
    return _sma_phase1_sort(found) == ["a.phase1.json", "z.phase1.json",
                                       "c.phase1.json", "b.phase1.json"]

def sma_precheck_rel_path(ch: Chapter) -> str:
    """Путь evidence Omission Pre-check относительно корня AINovelEdit."""
    return (f"{SMA_REL_ROOT}/{sma_chapter_id(ch)}/{SMA_PRECHECK_KIND}/"
            f"{SMA_PRECHECK_FILE}")

def sma_precheck_abs_path(ch: Chapter) -> str:
    """Абсолютный путь evidence Omission Pre-check."""
    return os.path.join(sma_chapter_dir(ch, SMA_PRECHECK_KIND),
                        SMA_PRECHECK_FILE)

def sma_precheck_exists(ch: Chapter) -> bool:
    """True, если для этой главы уже прогнан Omission Pre-check."""
    return os.path.isfile(sma_precheck_abs_path(ch))

def sma_phase1_rel_path(ch: Chapter, phase1_id: str) -> str:
    """Путь слепого вывода Фазы 1 (её собственный результат, не evidence)."""
    return sma_result_rel_path(ch, "analysis", f"{phase1_id}.phase1", "json")


def _load_merged_io():
    """Ленивый импорт scripts/merged_io.py (общий разбор блок-файлов)."""
    scripts_dir = os.path.join(AINOVELEDIT, "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        import merged_io  # type: ignore
    except Exception:
        return None
    return merged_io

def sma_block_inventory(ch: Chapter) -> tuple[list[int], list[int]]:
    """Номера смысловых блоков JA и текущего RU (пустые — если разбор недоступен).

    Переиспользует существующий scripts/merged_io.py вместо собственного
    разбора маркеров ``<!-- block: N -->``.
    """
    merged_io = _load_merged_io()
    if merged_io is None:
        return [], []

    def numbers(path: str) -> list[int]:
        try:
            return sorted(num for num, _ in merged_io.read_source_blocks(path))
        except Exception:
            return []

    return numbers(ch.ja_path), numbers(ch.output_path)

def semantic_audit_context(ch: Chapter) -> str:
    """Минимальный контекст для Auditor A / Auditor B / Pragmatic Auditor C.

    Отличие от ``project_context``: НЕ раскрываются audit-отчёты, лог,
    словарь, AGENTS.md и прочие пути проекта. Аудитору нужны только JA,
    текущий RU, EN (вспомогательная опора) и зеркало блоков для соседнего
    контекста. Сведения о путях старых результатов отсутствуют намеренно —
    архитектурно аудитору не нужен доступ к каталогу output/_audit/sma/.
    """
    ja_blocks, ru_blocks = sma_block_inventory(ch)
    if ja_blocks:
        block_info = (
            f"Блоков в JA: {len(ja_blocks)} (номера {ja_blocks[0]}–{ja_blocks[-1]}).\n"
            f"Блоков в текущем RU: {len(ru_blocks)}."
        )
    else:
        block_info = "Нумерация блоков — по маркерам <!-- block: N --> в файлах."
    return f"""КОНТЕКСТ СМЫСЛОВОГО АУДИТА
Проект: AINovelEdit
Глава: {sma_chapter_id(ch)}
Японский оригинал (JA — основной смысловой источник):
{ch.ja_path}
Текущий русский результат (RU — предмет аудита):
{ch.output_path}
Английский перевод (EN — вспомогательная опора, не истина):
{ch.en_path}
Трёхъязычное зеркало по смысловым блокам (JA/EN/RU, соседний контекст):
{ch.merged_path}
{block_info}
Единица аудита — смысловой блок <!-- block: N -->. Блоки берутся из JA;
RU выровнен по тем же маркерам (границы могут слегка сдвигаться на соседние
сцены). Соседние блоки нужны ТОЛЬКО как контекст: находка относится к тому
блоку, в котором находится расхождение.
Материал аудита ограничен: JA, текущий RU, EN (опора) и соседний контекст
блоков. Никакие другие материалы в задание не входят."""

# ============================================================================
# ПРОМПТЫ
# ============================================================================
@dataclass
class PromptInfo:
    title: str
    description: str
    guide: str
    generator: Callable[[Chapter], str] | None = None
    # Раздел главного меню (см. GROUP_*): порядок вывода и граница действия
    # кнопки «Следующий промпт (фаза)».
    group: str = ""
    # Слаг режима для имени файла промпта:
    # agent_prompts/agent_prompt.<chapter>.<slug>.md
    slug: str = ""

@dataclass
class ActionInfo:
    """Техническое действие оркестратора (НЕ LLM-промпт).

    В отличие от PromptInfo действие не генерирует задание для агента, а
    выполняет детерминированный технический шаг проекта: ``execute``
    получает текущую главу и возвращает код завершения процесса (0 — успех).

    ActionInfo НЕ наследуется от PromptInfo и НЕ входит в PROMPTS.
    """
    name: str
    description: str
    execute: Callable[[Chapter], int]

def prompt_first_launch(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: ПЕРВЫЙ ЗАПУСК
Подготовь рабочую среду для главы {ch.chapter_id_full} и сразу начни работу.
Пользователь уже поручил обработать эту главу — это разрешение на
выполнение; отдельного подтверждения не требуется.
Не начинай художественную редактуру вслепую, но и не превращай проверку
в остановку: первичная проверка — подготовительный этап, а не отдельная
фаза работы.
Подготовительный этап (выполни и сразу переходи к исполнению):
1. Прочитай AGENTS.md.
2. Изучи структуру AINovelEdit.
3. Проверь существующие skills.
4. Изучи словарь терминов.
5. Проверь исходные JA / EN / RU файлы главы.
6. Определи текущее состояние обработки.
7. Не перезаписывай существующий хороший результат без необходимости.
Обнаруженные новые термины и локальные неоднозначности (например,
непереведённое название дороги, титула или местности) НЕ являются поводом
останавливать работу и спрашивать пользователя: выбери наиболее
обоснованную рабочую (provisional) форму, зафиксируй её в журнале
с пометкой PROVISIONAL и продолжай без ожидания подтверждения
(AGENTS.md, «Неопределённость: non-blocking и blocking»; UNCERTAINTY ≠
STOP, PROVISIONAL ≠ CANONICAL, PROVISIONAL ≠ WAIT). Новый
PROVISIONAL-термин обязательно укажи в итоговом отчёте блока/главы.
Запрос пользователю — только для по-настоящему блокирующей
неопределённости.
После успешной проверки НЕ останавливайся и НЕ проси разрешения начать.
В том же запуске перейди:
ANALYSIS → CLASSIFICATION → PROVISIONAL RESOLUTION → EXECUTION
и сразу начни первый блок главы: создай файл результата через
`scripts/save_block.py --new --block 1` и выполни полный pipeline
(см. `.agents/skills/novel-editor/SKILL.md`). В pipeline каждого блока
входят механические предфильтры: после сохранения — `grammar_scan.py`,
`format_scan.py` (оформление: регистр, титулы, мысли, атрибуции,
слипшиеся абзацы) и `style_scan.py`, каждый кандидат получает
classification и disposition; `format_scan.py` запускается по
output-файлу, `grammar_scan.py` — по merged (нужен `update_merged.py`).
Краткий план — это рабочий
ориентир внутри исполнения, а не повод завершить ответ.
Запрещено в этом режиме: спрашивать «начинать ли / продолжать ли»,
возвращать только план, завершать ответ после подготовки, ждать
следующего сообщения пользователя.
Исключение — только действительно блокирующая неопределённость
(AGENTS.md, «Неопределённость: non-blocking и blocking»): тогда
останови минимально достаточный участок и задай один конкретный вопрос.
""".strip()

def prompt_continue(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: ПРОДОЛЖЕНИЕ РАБОТЫ
Продолжи работу над главой {ch.chapter_id_full}
с текущего состояния.
Сначала проверь:
- AGENTS.md;
- текущий русский результат;
- существующий лог;
- существующие аудиты;
- словарь терминов;
- состояние предыдущей обработки.
Не повторяй уже выполненную работу без причины.
Определи следующий необходимый этап и выполни его.
После завершения зафиксируй результат в соответствии
с правилами проекта.
""".strip()

def prompt_full_audit(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: ПОЛНЫЙ АУДИТ
Проведи полный аудит главы {ch.chapter_id_full}.
Порядок:
1. translation-audit (JA — арбитр при конфликте EN ↔ RU)
2. novel-editor
3. self-review (перед сохранением)
4. russian-humanizer
5. russian-prose-rules
6. grammar_scan.py + russian-grammar-control
(grammar_scan.py — шаг 0 предфильтра, затем разбор по схемам RGC)
7. style_scan.py + russian-style-audit
8. format_scan.py — механический предфильтр оформления
(регистр предложений/титулов, мысли в кавычках, строки-атрибуции,
слипшиеся абзацы, незакрытый курсив, маркеры блоков, согласование рода
звательных форм; разбор — по russian-prose-rules)
9. drift_scan.py — ОПЦИОНАЛЬНЫЙ инструмент: используется только при необходимости
сравнить две ветки или ревизии (например, `python scripts/drift_scan.py --file vXX-chYY.md
--against <SHA/branch>`). Для первичного пайплайна главы НЕ обязателен.
10. FINAL AUDIT (сводные итоги: GRAMMAR, STYLE, FORMAT; при сравнении веток — также DRIFT)
Проверяй не только наличие проблем, но и контекст.
Не исправляй текст автоматически только потому,
что механический сканер отметил подозрительное место.
Перед правкой оформления (тире, разбиение абзацев, курсив) определи
функцию абзаца относительно соседних (реплика / атрибуция / наррация) —
по JA/EN, а не по внешнему виду. Абзацную структуру RU внутри смыслового
блока (`<!-- block: N -->`) выбираешь сам; границу блока не переносить,
число блоков не менять. Курсив — только *…*.
Грамматически допустимую конструкцию не меняй ради более частотного
или «более естественного» варианта: сначала установи синтаксическую
структуру (подлежащее, сказуемое, вставка); если сказуемое согласовано
с подлежащим выбранной структуры — правка запрещена.
Все изменения должны соответствовать смыслу оригинала,
терминологии проекта и стилю русской художественной прозы.
Правки сохранённого текста — только через fix_block.py, после каждой
правки — повторный грамматический контроль блока и update_merged.py.
Каждый кандидат получает classification (ERROR / WARNING / CANDIDATE / PASS)
и disposition по модели AGENTS.md (FIXED / FALSE POSITIVE /
PRESERVED — ... / USER DECISION / ???); обнаружение сигнала — повод для
проверки, а не разрешение на правку. Ноль правок — допустимый итог.
Перед запуском сканеров обнови merged (scripts/update_merged.py). Прогони
также check_records.py, address_scan.py и format_scan.py (format_scan читает
output-файл напрямую); при необходимости сравнить ревизии — drift_scan.py;
при подозрении на пропуски прогони детерминированный pre-check
scripts/omission_precheck.py (его evidence для Analyzer —
output/_audit/sma/<chapter>/precheck/); старый режим «GAP-аудит»
— LEGACY и в меню недоступен.
В конце сформируй итоговый отчёт в output/_audit/vXX-chYY.md:
GRAMMAR, STYLE, FORMAT (и DRIFT при сравнении веток) — с судьбой каждого кандидата
format_scan.py (FIXED / FALSE POSITIVE / PRESERVED — … / USER DECISION / ???).
""".strip()

def prompt_quick_audit(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: БЫСТРЫЙ АУДИТ
Проведи быстрый контроль текущего русского текста главы.
Проверь прежде всего:
- явные ошибки;
- пропуски;
- грубые смысловые расхождения;
- терминологию;
- очевидную машинность;
- явные грамматические проблемы;
- очевидные повторы.
Не проводи глубокую художественную переработку,
если для этого нет необходимости.
Выдай список найденных проблем и исправь только действительно
обоснованные случаи.
""".strip()

def prompt_grammar_audit(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: ГРАММАТИЧЕСКИЙ АУДИТ
Проведи отдельный грамматический аудит главы.
Используй скилл russian-grammar-control.
Порядок:
1. Механический предфильтр:
python scripts/grammar_scan.py --file vXX-chYY.md --report
(читает merged — сначала свежий update_merged.py).
2. Разбор по предложениям: схема «кто → что делает → кого/чего»,
голос (RGC-1), управление (RGC-2), согласование (RGC-3),
референция (RGC-4/RGC-7).
Проверь:
- залог и актанты (возвратный глагол там, где в JA/EN пассив —
сигнал проверки RGC-1, а не автоматически ошибка: сначала установи
синтаксическую структуру и сверись с JA/EN — пассив ≠ ошибка,
возвратный глагол ≠ ошибка, инверсия ≠ ошибка);
- управление глаголов;
- согласование;
- падежи;
- местоименные связи;
- пунктуацию там, где она связана с грамматикой.
Каждый кандидат предфильтра обязан получить вердикт: ИСПРАВЛЕНО
(disposition FIXED, fix_block.py), ОТКЛОНЕНО (disposition FALSE POSITIVE)
с обоснованием или ??? (недостаточно данных — решение пользователя).
«Звучит по-русски» — не аргумент, разбор схемы и падежей обязателен.
Ноль исправлений — допустимый итог аудита.
Правки — только через fix_block.py, после каждой правки повтори
грамматический контроль изменённого блока и update_merged.py.
Не переписывай художественный текст без необходимости.
Сохраняй авторский стиль и смысл.
""".strip()

def prompt_style_audit(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: СТИЛЕВОЙ АУДИТ
Проведи глубокий стилевой аудит русского текста.
Используй:
- style_scan.py — механический предфильтр кандидатов;
- russian-style-audit — разбор каждого кандидата и всего текста.
Проверь:
- тавтологию;
- повторы и повтор однокоренных слов;
- семантическую избыточность;
- неудачные коллокации;
- кальки;
- избыточные номинализации;
- неестественный порядок слов;
- монотонность эпитетов (трек MONOTONY: один описательный эпитет —
  «исполинский», «гигантский» и т.п. — повторяется в главе слишком часто,
  синонимы не применяются; слово не запрещено, но нужны синонимы:
  огромный / громадный / большой / гигантский; кандидат — chapter-level).
Не дублируй проверки других скиллов: смысл и соответствие JA/EN —
translation-audit; залог и актанты — russian-grammar-control;
оформление речи и мыслей — russian-prose-rules; канцелярит и
AI-штампы — russian-humanizer.
Не исправляй нормальную авторскую повторность,
если она выполняет художественную функцию.
Не превращай текст в стерильный литературный пересказ.
Предпочтение редактора не является доказательством ошибки: нельзя менять
корректный текст ради варианта «красивее / литературнее / естественнее /
без повтора / привычнее» (AGENTS.md, «Жизненный цикл любого сигнала»).
Ноль правок — допустимый итог аудита.
Каждому кандидату style_scan.py дай classification (ERROR / WARNING /
CANDIDATE) и disposition по модели AGENTS.md: FIXED / FALSE POSITIVE /
PRESERVED — FUNCTIONAL / PRESERVED — JA/EN / PRESERVED — CHARACTER VOICE /
ACCEPTABLE ADAPTATION / USER DECISION / ???. Формулировка
«все кандидаты разобраны» без судьбы каждого кандидата запрещена.
Отчёт — в output/_audit/vXX-chYY.md, раздел «## Стилевой контроль»,
плюс сводка STYLE AUDIT в финальном аудите главы.
""".strip()

def prompt_humanizer(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: HUMANIZER / MACHINE-LIKE
Проведи проверку русского текста на признаки машинного перевода
и искусственной генерации.
Используй russian-humanizer (каталоги references/patterns.md,
translationese.md, kantselyarit-dict.md; защита от переисправления —
references/false-positives.md).
Ищи:
- кальки с английского (основной источник машинности в этом проекте);
- канцелярит;
- шаблонные конструкции;
- неестественный порядок слов;
- чрезмерно книжные связки;
- повторяющиеся синтаксические шаблоны;
- формулировки, которые формально правильны,
но не звучат естественно по-русски.
Ограничения этого проекта (перекрывают каталог скилла):
- курсив `_…_` и blockquote `>` — НЕ «следы Markdown», это разметка
по russian-prose-rules; устаревший вариант курсива `*…*` (главы v3/v4)
в новом и правимом тексте заменяется на `_…_`;
- реплики персонажей — голос персонажа: характер речи не улучшать;
- модальные слова («возможно», «кажется») править только после
сверки с JA;
- цвет/уровень риска маркера (🔴/🟡/🟢) — сигнал риска, а не разрешение
на правку: автоматически — только однозначный низкорисковый мусор
(опечатки, технические артефакты, нарушение обязательного
форматирования); всё рискованное — предложить, а не навязать;
- рискованные правки не вноси молча — фиксируй в отчёте аудита
как предложение пользователю.
После каждой внесённой правки — повторный контроль: смысл (self-review),
JA/EN, терминология, грамматика, оформление. Humanizer не должен
создавать stylistic churn; ноль правок — допустимый итог.
Важно:
Не делай текст просто «красивее».
Не меняй смысл.
Не удаляй намеренную стилистику персонажей.
Не исправляй нормальную разговорную речь только потому,
что она отличается от нейтральной литературной нормы.
""".strip()

def prompt_alignment(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: JA / EN ALIGNMENT
Проведи сверку русского текста с японским оригиналом
и английским переводом.
Приоритет при сверке по смысловым блокам (по скиллу translation-audit):
JA → основной смысловой источник, арбитр при конфликте EN ↔ RU
EN → структурная опора выходного текста (по нему построены merged
и смысловые блоки) и вспомогательный источник смысла
EN — фанатский перевод и не абсолютная истина: если EN и JA расходятся,
не выбирай молча одну версию и не удаляй расхождение молча. По умолчанию
сохраняй близкий к EN смысл, помечай `<!-- ??? -->` и заноси СОМНЕНИЕ
в журнал. Каждый кандидат получает classification и disposition —
обнаружение сигнала не является разрешением на правку (AGENTS.md,
«Жизненный цикл любого сигнала»).
Проверь:
- пропуски;
- добавления;
- смысловые сдвиги;
- неверные обращения (по addresses.md, скилл forms-of-address);
- имена;
- термины;
- местоимения;
- пол персонажей;
- время и аспект;
- отрицания;
- эмоциональные оттенки;
- действия персонажей;
- соответствие строк: ED_RU каждой строки обязан соответствовать
JA/EN той же строки (скрипт scripts/check_alignment.py).
Если JA и EN расходятся, отдельно укажи это.
""".strip()

def prompt_encoding(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: ПРОВЕРКА КОДИРОВКИ
Проверь файлы главы на проблемы кодировки.
Особое внимание:
- UTF-8;
- битые символы;
- mojibake;
- японские символы;
- русские символы;
- кавычки;
- тире;
- многоточия;
- специальные символы;
- управляющие символы.
Не меняй содержание текста без необходимости.
Если обнаружены проблемы, перечисли их отдельно
и только после этого исправляй.
""".strip()

def prompt_one_block(
    ch: Chapter,
    block_number: int,
) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: ОБРАБОТКА ОДНОГО БЛОКА
Номер блока: {block_number}
Работай только с блоком {block_number}.
Используй полный pipeline (по скиллам):
1. translation-audit — сверка смысла с JA/EN
2. novel-editor — художественная редактура
3. self-review — проверка на галлюцинации (перед сохранением)
4. russian-humanizer — канцелярит, кальки, AI-штампы
5. russian-prose-rules — оформление речи, мыслей, курсива
(fix/проверка оформления — подсказки format_scan.py)
6. russian-grammar-control — grammar_scan.py (шаг 0) + разбор схем
7. save-progress — сохранение через save_block.py
+ update_merged.py + check_alignment.py
8. style_scan.py + russian-style-audit
9. format_scan.py — предфильтр оформления output-блока (регистр, мысли,
атрибуции, слипшиеся абзацы)
10. FINAL AUDIT
Сначала проверь смысл относительно JA / EN.
Затем выполни редактуру.
Не меняй соседние блоки без крайней необходимости.
Не нарушай существующие решения по терминологии,
именам, обращениям и стилю персонажей.
Единица обработки — смысловой блок (`<!-- block: N -->`): границу блока
не переносить, число блоков не менять. Абзацы внутри блока дели и
объединяй свободно по законам русской прозы, сохраняя смысл JA.
После обработки покажи итоговую версию блока.
""".strip()

def prompt_resolve_decisions(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: РЕШЕНИЯ ПОЛЬЗОВАТЕЛЯ — OPEN (DEFERRED) И PROVISIONAL
Пользователь даёт решения по ранее отложенным вопросам (реестр
«Отложенные вопросы (OPEN / DEFERRED)» в output/_audit/) и/или по
временным значениям словаря (записи PROVISIONAL в dictionary.md и
журнале). Нужно не переписать вопрос, а применить решение: в одном
проходе найти ВСЕ места, где встречается затронутое сомнение или
форма, и привести их в соответствие.
Основания: AGENTS.md «Жизненный цикл любого сигнала»,
«OPEN / DEFERRED — отложенные пользователем вопросы»,
«PROVISIONAL ≠ CANONICAL» (PROVISIONAL → USER CONFIRMED → CANONICAL;
PROVISIONAL → REJECTED → REPLACE ALL AFFECTED OCCURRENCES).
1. РАЗОБРАТЬ РЕШЕНИЯ ПОЛЬЗОВАТЕЛЯ
- Прочитай сообщение пользователя и выпиши каждый пункт решения
отдельно: что разрешено, что запрещено, к чему относится
(одна глава / правило проекта / термин словаря).
- Сверь пункты с реестрами OPEN / DEFERRED и списками PROVISIONAL
в output/_audit/ и output/_log/.
- Решение должно быть однозначным. Если формулировку можно понять
двояко — задай один конкретный вопрос и до ответа текст не меняй.
2. СОСТАВИТЬ ПОЛНЫЙ СПИСОК ЗАТРОНУТЫХ МЕСТ
Решение по правилу или термину почти всегда шире одной главы.
Проверь весь том, а не только текущий файл:
- output/*.md — все главы тома;
- dictionary.md, addresses.md;
- output/_audit/*.md и output/_log/vNN-log.md — реестры и записи;
- translates/ru и translates/_report/merged — для обновления зеркала.
Перечисли найденные файлы и номера блоков ДО правки: решение
применяется ко всем местам сразу, а не к одному.
3. ПРИМЕНИТЬ
- Правки текста результата — только через scripts/fix_block.py,
после каждой правки — scripts/update_merged.py.
- Замена формы — REPLACE ALL AFFECTED OCCURRENCES: единая новая
форма во всех найденных местах, без частичных и «пилотных» правок.
- Граница смыслового блока (`<!-- block: N -->`) — alignment-инвариант,
её не переносить; абзацы внутри блока можно перестраивать, сохраняя
смысл JA. Сверка — scripts/check_alignment.py.
- Расхождения терминов/имён/обращений с завершёнными томами
(AINovelEdit/completed.md) фиксируй в отчёте, но решай в пользу формы
из завершённого тома; исключение — ручная правка пользователем в
dictionary.md.
- Если решение подтверждает текущий текст («оставить как есть») —
текст не менять вообще.
4. ОБНОВИТЬ СТАТУСЫ И ЗАПИСИ
- Реестр OPEN (DEFERRED): RESOLVED (решение внесено правкой) либо
CLOSED (оставлено как есть, но решение пользователя явное).
Формулировку вопроса и «текущее состояние» привести к решению.
- dictionary.md: при подтверждении — PROVISIONAL → канон (снять
пометку, дописать «решение пользователя»); при отклонении —
форму заменить во всех местах, запись привести к новой.
- Журнал (output/_log/vNN-log.md): отдельная запись на каждый
пункт — решение, затронутые файлы, блоки, что именно изменено.
- Если решение касается правила, а не отдельного текста, — отметь,
нужно ли обновить AGENTS.md, скиллы или dictionary.md.
5. ПОВТОРНЫЙ КОНТРОЛЬ (RECHECK)
- Правка = новый непроверенный текст: после изменений — self-review,
сверка JA/EN, терминология, грамматика, оформление.
- Для каждой изменённой главы — update_merged.py + check_alignment.py.
- Убедись, что ни одно место с той же формой не пропущено и что
неизменённый текст не пострадал.
Запрещено:
- закрывать OPEN / DEFERRED без явного решения пользователя;
- менять текст «заодно» или по своей инициативе;
- применять решение только к текущей главе, если оно относится
ко всем файлам;
- записывать неподтверждённую форму как канон словаря;
- считать вопрос закрытым по факту правки без записи в реестре
и журнале.
Отчёт: обновлённые реестры в output/_audit/ и запись в журнале;
при распространении решения на другие главы перечислить их отдельно.
""".strip()

def prompt_gap_audit(ch: Chapter) -> str:
    # LEGACY / DEPRECATED / NOT USED IN CURRENT PIPELINE.
    #
    # Этот prompt относится к СТАРОЙ архитектуре поиска пропусков и НЕ должен
    # использоваться как рабочий способ поиска omission. Сейчас пропуски
    # ищет общий детерминированный слой:
    #
    #     JA + RU → Common Omission Pre-check (AINovelEdit/scripts/omission_precheck.py)
    #                 → candidate evidence (severity=CANDIDATE)
    #                 → A + B + C (независимые аудиторы, пропуски НЕ ищут
    #                               систематически)
    #                 → Analyzer (Phase 1 BLIND, Phase 2 EVIDENCE) — решает сам
    #
    # prompt_gap_audit убран из активного меню PROMPTS (как prompt_dual_
    # semantic_audit), функция сохранена только как legacy-задел: здесь есть
    # полезные эвристики, которые могут быть перенесены в omission_precheck.py
    # как будущие сигналы (проверка сдвига границ блоков, повторная сверка
    # несколькими ключами, выборочная проверка середины, поиск фрагмента в
    # другом блоке, сцено-чек-лист). НЕ переписывать под новую архитектуру,
    # НЕ интегрировать в Analyzer, НЕ превращать в ещё одного аудитора.
    # См. также: legacy/semantic-audit-auto/ — тот же статус легаси.
    #
    # Само тело prompt ниже — исторический текст (старый LLM-workflow:
    # собственная классификация, FIXED, fix_block.py, update_merged.py,
    # отчёт в output/_audit/vXX-chYY.md + _log). Оставлено без изменений.
    return f"""
{project_context(ch)}
РЕЖИМ: ПОИСК ПРОПУЩЕННЫХ ОТРЫВКОВ (GAP-АУДИТ)
Цель: найти в output/ целые микросцены, реплики или абзацы
JA-оригинала, отсутствующие в русском результате, — пропуски, которые
обычный смысловой аудит пропускает, потому что остаток текста выглядит
связным. Пропущенный фрагмент не оставляет видимой «дыры»: соседние
абзацы просто смыкаются. JA — полный инвентарь содержания; связность
RU ничего не доказывает.
Не доверяйся утверждениям предыдущих отчётов о полноте («сцена
восстановлена», «удалять было нечего»): каждое такое утверждение
проверяй механически.
Имена файлов уточняй по фактическому списку (Get-ChildItem): в проекте
используется v2-chYY.md без ведущего нуля, отчёты аудита —
v02-chYY.md.
Порядок работы:
1. ПОБЛОЧНАЯ СВЕРКА ИНВЕНТАРЯ. Для каждого блока N возьми JA из
translates/ja/ и ED_RU из output/ с одинаковым маркером
`<!-- block: N -->`. EN/RU из merged НЕ используй как меру полноты:
их границы сдвинуты на 1–3 блока (AGENTS.md).
2. СЧЁТ РЕПЛИК И АБЗАЦЕВ. В JA блока — реплики 「…」 и абзацы;
в ED_RU — реплики «— …» и абзацы. Красный флажок: JA-реплик или
JA-абзацев существенно больше при внешне нормальном тексте. Сравни
долю покрытия с соседними блоками.
3. ЯКОРНЫЕ КЛЮЧИ. Для каждой JA-строки выбери 1–2 характерных ключа
(имя собственное, редкое существительное, число, действие) и найди
их в output/ (учитывай UTF-8: Get-Content -Raw -Encoding UTF8 /
Select-String). Ключ с «0 вхождений» при наличии в JA — кандидат.
4. СЦЕНОВОЙ ЧЕК-ЛИСТ. Перечисли микросцены JA (смена собеседника,
смена места, появление персонажа) и укажи абзац output, где каждая
есть. Сцена «без адреса» — пропуск.
5. СВИДЕТЕЛЬСТВА EN/RU. Сцена есть в EN или сыром RU, но отсутствует
в output, — подтверждение пропуска (доказательство наличия материала,
а не смысла).
6. ВЫБОРКА ИЗ СЕРЕДИНЫ. Возьми несколько случайных JA-абзацев из
середины блоков и найди их в output — ловит пропуски, которые
пропустили счётчики.
Верификация кандидата (обязательна):
- подтверди отсутствие повторным поиском 2–3 разных ключей фрагмента;
- восстанови точный JA-текст (не пересказ, не «по памяти»);
- проверь, нет ли фрагмента в другом блоке output (сдвиг границ);
- блок восстановления = номер JA-блока; границу блока не переносить,
число блоков не менять.
Классификация и disposition (по AGENTS.md):
- целая сцена или абзацы пропущены → ERROR, disposition FIXED
(восстановление), запись ПРОПУСК в журнал с перечнем JA-строк;
- микропропуск (атрибуция, деталь) → WARNING, FIXED;
- фрагмент найден в другом месте output → FALSE POSITIVE (сдвиг).
Правки: только fix_block.py полным текстом блока (существующие
абзацы + восстановленные), затем update_merged.py и RECHECK:
check_records, grammar_scan, style_scan, format_scan, check_alignment.
Восстановленный текст — живая русская проза по russian-prose-rules;
досочинять запрещено: только JA-содержимое (EN/RU — вспомогательная
сверка формы). Самопроверка (self-review) каждого восстановленного
абзаца по JA: полнота, отсутствие добавлений, неизменность модальности.
Отчёт: output/_audit/vXX-chYY.md — раздел «Поиск пропусков» с
таблицей «блок / JA-строки / ключи (0 → N) / disposition» + запись в
output/_log/vNN-log.md. Ноль находок допустим, но каждый блок должен
получить подпись «покрытие полное» по итогам счёта реплик.
""".strip()

def prompt_rules_recheck(ch: Chapter) -> str:
    return f"""
{project_context(ch)}
РЕЖИМ: РЕКОНТРОЛЬ ГОТОВОЙ ГЛАВЫ ПО НОВЫМ ПРАВИЛАМ
Контекст: глава уже полностью переведена и прошла полный аудит ДО того,
как в проект были введены новые правила (согласование рода в обращениях,
каталог калькированных реплик, отбивка разделителей сцен). Текст
менять без причины НЕЛЬЗЯ — режим ищет только классы ошибок, которые
предыдущий аудит не проверял. Повторный полный смысловой аудит НЕ нужен:
JA/EN сверяй ТОЛЬКО там, где кандидат требует решения по смыслу.
Порядок работы:
1. МЕХАНИЧЕСКИЕ ПРЕДФИЛЬТРЫ (по output-файлу напрямую):
   python scripts/format_scan.py --file output/vXX-chYY.md
   python scripts/style_scan.py --file output/vXX-chYY.md
   Каждый кандидат получает classification (ERROR / WARNING / CANDIDATE)
   и disposition (FIXED / FALSE POSITIVE / PRESERVED — … / USER DECISION
   / ???) в отчёте; «все кандидаты разобраны» без судьбы каждого
   кандидата — нарушение.
2. РОД В ОБРАЩЕНИЯХ (новая проверка gender_vocative): прогони по тексту
   классы «понял, Луиза?» / «слышала, Сайто?» / «Луиза, ты … видел» /
   «Сайто, ты … пришла?» / «в тебе, дуре» о Сайто. Ловится сканером,
   но при разборе проверь руками: женский род адресата обязателен
   (Луиза, Кирхе, Табита, Сиеста, Генриетта, мадемуазель), мужской —
   у Сайто, Гиша, Варда, Уэльса, Кольбера, Османа. Брань и ласковые
   формы — того же рода, что и адресат.
3. КАЛЬКИ И ИДИОМЫ (новая проверка CALQUE): сверка с контрастивной
   таблицей эталонных правок в скиллах russian-humanizer и
   translation-audit. Механически ловятся: «не пойму ты», «полегчайте»,
   «за ржавчину», «им не по дороге», «руки-ноги сделались бесполезны»,
   «громила-особа». Ручной проход по смыслу: калька может быть и
   нестандартной (переводчики ломают фразеологизмы по-новому) — если
   фраза дословно воспроизводит EN/JA-конструкцию и по-русски звучит
   чужо, пометь `<!-- ??? -->` и предложи золотой вариант из таблицы.
4. ТИТУЛЫ В ПРЯМОЙ РЕЧИ (проверка регистр-в-реплике): прямое обращение →
   «Ваше Высочество» / «Её Величество» с заглавных; в наррации (косвенное
   упоминание) — строчная; в ПРЯМОЙ РЕЧИ косвенное упоминание титула —
   контекстное решение: почтительная заглавная допустима и не только в
   обращении (russian-prose-rules, «Титулы: регистр»). Спорное —
   CANDIDATE, регистр не править механически ни в одну сторону.
5. РАЗДЕЛИТЕЛИ СЦЕН (`---`): необязательный композиционный инструмент.
   Отсутствие `---` само по себе НЕ является ошибкой и НЕ создаёт
   WARNING: обязательного разделителя нет, механического правила
   «каждая смена сцены должна получить ---» в проекте нет. Ставить или
   не ставить `---` — решение по контексту: агент может его поставить
   при подтверждённой смене локации/времени/ракурса (смысл границы — по
   JA); если разделитель композиционно действительно нужен, вставляй его
   осознанно и обосновывай по контексту, а не по правилу. format_scan
   (kind=paragraph) проверяет только отбивку УЖЕ существующих
   разделителей (пустая строка до и после), но не их наличие.
   Сомнение → `<!-- ??? -->`.
6. ФОРМАТ МЫСЛЕЙ: внутренняя речь — курсив _…_ без кавычек; мысль
   в «…», — подумал он → кандидат (kind=thought). Проверь также, что
   после курсива есть пустая строка перед следующим абзацем и что
   реплики не слиплись (kind=paragraph).
7. НОВЫЕ ПРОВЕРКИ (blockgap / quotespeech / thoughtinline / namespell):
   * blockgap — маркеры `<!-- block: N -->` и `<!-- img_ … -->` обязаны
     отделяться пустой строкой от текста с обеих сторон;
   * quotespeech — абзац целиком в «…» без тире: речь вслух по JA/EN →
     реплика «— …»; цитата/название остаются в кавычках;
   * thoughtinline — мысль курсивом слита с нарративом в одном абзаце
     («Вард задумался. _Так не пойдет._») → вынести мысль отдельным
     абзацем; атрибуция («_…_, — подумал он.») и вставка мысли в реплику —
     не нарушение;
   * namespell — искажение имени по словарю NAME_TYPOS («Дельф» → «Дерф»,
     «Реконкисте» в кавычках → «Реконкиста»): исправляй всегда, канон —
     dictionary.md. Сигнал check_alignment (names) в больших главах тонет
     среди слабых — ему не доверяй единственно.
8. ПАДЕЖ ГЕОНАЗВАНИЙ: конструкции «сам(о/ой/им/ом) + государство мужского
   рода» — «до самого Тристейна», не «до самой Тристейна» (и т.п. по
   контексту). Класс из ручных правок v2-ch09, механически не покрыт —
   ручной проход по именам собственным из dictionary.md.
Чего НЕ делать: не переписывай уже выверенные абзацы «на лучше»,
не повторяй смысловой аудит JA/EN целиком, не трогай terminology
и обращения из addresses.md (они прошли проверку). Ноль правок —
допустимый итог: режим закрывается, если предфильтры дали только
FALSE POSITIVE / PRESERVED.
Правки — только fix_block.py с обновлением merged (update_merged.py)
и RECHECK: format_scan + style_scan по изменённому блоку.
Отчёт: output/_audit/vXX-chYY.md — раздел «Реконтроль по новым
правилам»: итоги format_scan/style_scan (число кандидатов по kind),
таблица disposition каждого кандидата + запись в output/_log/vNN-log.md.
""".strip()


def prompt_dual_semantic_audit(ch: Chapter) -> str:
    # LEGACY / DEPRECATED: единый режим A+B больше НЕ используется как рабочий
    # prompt (см. prompt_semantic_a / prompt_semantic_b /
    # prompt_semantic_analyzer). Из списка PROMPTS удалён, функция сохранена
    # только для истории. Не подключать повторно: она смешивает A и B в одном
    # задании, что противоречит архитектуре изолированных запусков.
    return f"""
{project_context(ch)}
РЕЖИМ: ДВОЙНОЙ СМЫСЛОВОЙ АУДИТ (A + B)

Этот режим генерирует два НЕЗАВИСИМЫХ задания для смыслового аудита.

ВАЖНО: Аудиторы A и B работают в ИЗОЛЯЦИИ.
- Аудитор A не видит результаты B
- Аудитор B не видит результаты A
- Каждый аудитор получает только: JA, RU, контекст соседних блоков

ЗАДАНИЕ A: Semantic Auditor A
- Фокус: лексическая точность, оттенки значения, эмоции, мимика, жесты
- Скилл: .agents/skills/semantic-audit-a/SKILL.md
- Результат: output/_audit/{ch.chapter_id_full}-sma-a.json

ЗАДАНИЕ B: Semantic Auditor B
- Фокус: субъект/объект, действия, причинно-следственные связи, идиомы
- Скилл: .agents/skills/semantic-audit-b/SKILL.md
- Результат: output/_audit/{ch.chapter_id_full}-sma-b.json

ФОРМАТ РЕЗУЛЬТАТА (JSON):
{{
  "audit_id": "sma-a",
  "audit_type": "semantic-audit-a",
  "chapter": "{ch.chapter_id_full}",
  "block": 75,
  "findings": [
    {{
      "block": 75,
      "source": "JA-фрагмент",
      "current": "RU-фрагмент",
      "problem": "Тип проблемы",
      "reason": "Обоснование",
      "suggestion": "Предложенный вариант",
      "severity": "WARNING"
    }}
  ]
}}

ПРОЦЕДУРА:
1. Прочитай скилл соответствующего аудитора
2. Для каждого блока главы:
   - Прочитай JA-блок и RU-блок
   - Прочитай соседние блоки для контекста
   - Проверь соответствие JA → RU
   - Зафиксируй находки в JSON-формате
3. Сохрани результат в output/_audit/{ch.chapter_id_full}-sma-{a|b}.json

ВАЖНО:
- Не проводи грамматический аудит (это russian-grammar-control)
- Не проводи стилевой аудит (это russian-style-audit)
- Не исправляй текст — только фиксируй находки
- Если проблем нет — верни пустой массив findings
""".strip()

def prompt_semantic_a(ch: Chapter) -> str:
    """Prompt ТОЛЬКО для Auditor A (лексическая точность и оттенки смысла).

    Полностью изолирован: в тексте нет ссылок на второго аудитора, на его
    результаты, на старые отчёты аудита и на поиск в каталоге
    output/_audit/sma/. Аудитор получает свой уникальный audit_run_id и
    единственный выходной файл внутри output/_audit/sma/<chapter>/a/.
    """
    run_id = new_audit_run_id(ch)
    out_rel = sma_result_rel_path(ch, "a", run_id, "json")
    out_abs = sma_result_abs_path(ch, "a", run_id, "json")
    return f"""ЗАДАЧА: независимый смысловой аудит перевода JA → RU. Ты — Semantic Auditor A.

{SMA_AUTONOMY_NOTE}

OWN SKILL (единственный разрешённый файл за пределами задания):
AINovelEdit/.agents/skills/semantic-audit-a/SKILL.md
{SMA_FORBIDDEN_INPUTS_NOTE}

{semantic_audit_context(ch)}

{SMA_SOURCE_HIERARCHY_NOTE}

ФОКУС AUDITOR A — лексическая точность и оттенки смысла:
- точность выбора русского слова для японского (лексическая точность);
- оттенки значения, тонкие различия близких японских слов;
- эмоции и эмоциональная окраска;
- мимика (выражение лица, улыбки, взгляды);
- жесты и язык тела;
- интонация и стилистические особенности речи;
- степень выраженности (сила эмоции, интенсивность действия);
- потеря небольшого смыслового компонента (пропал оттенок или деталь);
- добавление небольшого смыслового компонента, которого нет в JA.

НАПРАВЛЕНИЕ ПРОВЕРКИ: JA → RU. Сначала установи смысл японского фрагмента,
затем сверь, как этот смысл передан в текущем русском результате.

ЧТО НЕ ВХОДИТ В ЗАДАЧУ (не проверяй и не фиксируй):
- грамматика (согласование, управление, падежи) — это russian-grammar-control;
- стиль (тавтология, повторы, кальки) — это russian-style-audit;
- оформление текста (кавычки, тире, курсив) — это russian-prose-rules;
- общее «очеловечивание» текста — это russian-humanizer;
- автоматические исправления: ты НИЧЕГО не исправляешь и ничего не пишешь
  в output/.

ПРОЦЕДУРА:
1. Прочитай скилл .agents/skills/semantic-audit-a/SKILL.md.
2. Для каждого смыслового блока <!-- block: N --> главы:
   - прочитай JA-блок и соответствующий RU-блок;
   - прочитай соседние блоки ТОЛЬКО как контекст;
   - сверь лексику, оттенки, эмоции, мимику, жесты, интонацию (JA → RU);
   - зафиксируй расхождения.
3. Находку относи только к тому блоку, где находится расхождение.

ФОРМАТ РЕЗУЛЬТАТА (ровно один JSON-объект, без markdown-обёртки):
{{
  "audit_id": "sma-a",
  "audit_type": "semantic-audit-a",
  "audit_run_id": "{run_id}",
  "chapter": "{sma_chapter_id(ch)}",
  "findings": [
    {{
      "block": 75,
      "source": "JA-фрагмент",
      "current": "RU-фрагмент",
      "problem": "Тип проблемы",
      "reason": "Обоснование",
      "suggestion": "Предложенный вариант",
      "severity": "ERROR"
    }}
  ],
  "coverage": "Просмотренные блоки и объём проверки (см. правила)"
}}

ПРАВИЛА:
- severity: только ERROR / WARNING / CANDIDATE.
- Если проблем нет — "findings": [] (пустой массив, объект всё равно обязателен).
- "coverage" (attestation покрытия) обязателен ВСЕГДА: какие блоки
  просмотрены и в каком объёме (напр. «блоки 1–29 целиком, соседние
  контексты проверены»). При "findings": [] coverage обязателен тем более:
  пустой массив без него — недоказанный «чистый» прогон, и валидатор
  (semantic_findings --validate) отклонит результат.
- source и current — точные цитаты, без пересказа.
- Литературное предпочтение — не ошибка: вариант «красивее» находкой не является.
- Не выдумывай: нет уверенности — не включай находку.

{SMA_OWN_FILE_NOTE}

OUTPUT FILE (единственный файл этого запуска):
{out_rel}
(абсолютный путь: {out_abs})
Запиши результат строго в описанном JSON-формате. Ничего больше не создавай
и не изменяй."""

def prompt_semantic_b(ch: Chapter) -> str:
    """Prompt ТОЛЬКО для Auditor B (смысловые связи и контекст).

    Полностью изолирован: в тексте нет ссылок на первого аудитора, на его
    результаты, на старые отчёты аудита и на поиск в каталоге
    output/_audit/sma/. Аудитор получает свой уникальный audit_run_id и
    единственный выходной файл внутри output/_audit/sma/<chapter>/b/.
    """
    run_id = new_audit_run_id(ch)
    out_rel = sma_result_rel_path(ch, "b", run_id, "json")
    out_abs = sma_result_abs_path(ch, "b", run_id, "json")
    return f"""ЗАДАЧА: независимый смысловой аудит перевода JA → RU. Ты — Semantic Auditor B.

{SMA_AUTONOMY_NOTE}

OWN SKILL (единственный разрешённый файл за пределами задания):
AINovelEdit/.agents/skills/semantic-audit-b/SKILL.md
{SMA_FORBIDDEN_INPUTS_NOTE}

{semantic_audit_context(ch)}

{SMA_SOURCE_HIERARCHY_NOTE}

ФОКУС AUDITOR B — смысловые связи, логика и контекст:
- субъект и объект (кто выполняет действие, на кого оно направлено);
- действие (тип, характер, направленность);
- состояние и его изменения;
- причинно-следственные связи (почему, зачем, следствие);
- временные отношения (последовательность, одновременность, длительность);
- логические связи между частями высказывания;
- местоименные связи (к чему/к кому относится местоимение);
- модальность (возможность, необходимость, вероятность, сомнение);
- идиомы и устойчивые выражения;
- метафоры и переносные значения;
- контекст, раскрывающий смысл из соседних блоков;
- неоднозначные конструкции, допускающие несколько прочтений;
- намерение/цель персонажа как часть содержания ситуации (что он хочет
  сделать и почему это вытекает из событий), связи событий и логика
  происходящего — НЕ прагматика самой реплики (речевой акт, сила,
  подтекст — это слой прагматики, вне твоей компетенции).

НАПРАВЛЕНИЕ ПРОВЕРКИ: JA → RU. Сначала установи смысл японского фрагмента
(с учётом контекста), затем сверь, как этот смысл передан в текущем русском
результате.

ЧТО НЕ ВХОДИТ В ЗАДАЧУ (не проверяй и не фиксируй):
- грамматика (согласование, управление, падежи) — это russian-grammar-control;
- стиль (тавтология, повторы, кальки) — это russian-style-audit;
- оформление текста (кавычки, тире, курсив) — это russian-prose-rules;
- общее «очеловечивание» текста — это russian-humanizer;
- коммуникативная функция самой реплики — речевой акт, прагматическая сила,
  подтекст, implied meaning: это прагматический слой, не макро-семантика;
- автоматические исправления: ты НИЧЕГО не исправляешь и ничего не пишешь
  в output/.

ПРОЦЕДУРА:
1. Прочитай скилл .agents/skills/semantic-audit-b/SKILL.md.
2. Для каждого смыслового блока <!-- block: N --> главы:
   - прочитай JA-блок и соответствующий RU-блок;
   - прочитай соседние блоки как контекст (они проясняют связи);
   - проверь субъект/объект, связи, время, модальность, идиомы, метафоры,
     неоднозначные конструкции (JA → RU);
   - зафиксируй расхождения.
3. Находку относи только к тому блоку, где находится расхождение.

ФОРМАТ РЕЗУЛЬТАТА (ровно один JSON-объект, без markdown-обёртки):
{{
  "audit_id": "sma-b",
  "audit_type": "semantic-audit-b",
  "audit_run_id": "{run_id}",
  "chapter": "{sma_chapter_id(ch)}",
  "findings": [
    {{
      "block": 75,
      "source": "JA-фрагмент",
      "current": "RU-фрагмент",
      "problem": "Тип проблемы",
      "reason": "Обоснование",
      "suggestion": "Предложенный вариант",
      "severity": "WARNING"
    }}
  ],
  "coverage": "Просмотренные блоки и объём проверки (см. правила)"
}}

ПРАВИЛА:
- severity: только ERROR / WARNING / CANDIDATE.
- Если проблем нет — "findings": [] (пустой массив, объект всё равно обязателен).
- "coverage" (attestation покрытия) обязателен ВСЕГДА: какие блоки
  просмотрены и в каком объёме (напр. «блоки 1–29 целиком, соседние
  контексты проверены»). При "findings": [] coverage обязателен тем более:
  пустой массив без него — недоказанный «чистый» прогон, и валидатор
  (semantic_findings --validate) отклонит результат.
- source и current — точные цитаты, без пересказа.
- Литературное предпочтение — не ошибка: вариант «красивее» находкой не является.
- Если JA допускает несколько прочтений — укажи это как неоднозначность,
  а не как ошибку.
- Не выдумывай: нет уверенности — не включай находку.

{SMA_OWN_FILE_NOTE}

OUTPUT FILE (единственный файл этого запуска):
{out_rel}
(абсолютный путь: {out_abs})
Запиши результат строго в описанном JSON-формате. Ничего больше не создавай
и не изменяй."""

def prompt_pragmatic_c(ch: Chapter) -> str:
    """Prompt ТОЛЬКО для Pragmatic Auditor C (прагматика, речевые акты, подтекст).

    C — НЕ третий универсальный смысловой аудитор: он закрывает отдельный слой
    смысла — коммуникативный смысл высказывания (что говорящий делает репликой,
    намёк, недосказанность, степень уверенности, сила реплики, скрытое
    отношение) — и не дублирует ни микро-семантику, ни макро-семантику/логику.

    Полностью изолирован: в тексте нет ссылок на других аудиторов, на их
    результаты, на Analyzer, на старые отчёты аудита и на поиск в каталоге
    output/_audit/sma/. Аудитор получает свой уникальный audit_run_id и
    единственный выходной файл внутри output/_audit/sma/<chapter>/c/.
    """
    run_id = new_audit_run_id(ch)
    out_rel = sma_result_rel_path(ch, "c", run_id, "json")
    out_abs = sma_result_abs_path(ch, "c", run_id, "json")
    return f"""ЗАДАЧА: независимый прагматический аудит перевода JA → RU. Ты — Pragmatic Auditor C.

{SMA_AUTONOMY_NOTE}

OWN SKILL (единственный разрешённый файл за пределами задания):
AINovelEdit/.agents/skills/pragmatic-audit/SKILL.md
{SMA_FORBIDDEN_INPUTS_NOTE}

{semantic_audit_context(ch)}

{SMA_SOURCE_HIERARCHY_NOTE}

ФОКУС AUDITOR C — коммуникативный смысл (прагматика) высказывания:
- что говорящий фактически делает своей репликой (речевой акт): сообщает,
  спрашивает, просит, требует, обещает, предупреждает, разрешает, приказывает,
  отказывает, уклоняется от ответа;
- сохранился ли намёк и сохранилась ли недосказанность: подразумеваемое не
  должно превращаться в прямо сказанное (и наоборот — явное не должно
  становиться только подразумеваемым);
- степень уверенности / неуверенности: предположение vs утверждение,
  сомнение vs уверенность, вероятность vs факт;
- форма и сила реплики: просьба vs требование, мягкий отказ vs прямой отказ,
  уклонение vs прямой ответ, разрешение vs приказ, обещание vs намерение,
  предупреждение vs обычное сообщение;
- установка говорящего: удивление, недоверие, сомнение, ирония, сарказм,
  скрытое отношение говорящего (скрытое недовольство, насмешка, неловкость);
- смягчение или усиление высказывания; изменение коммуникативной силы
  реплики и степени её категоричности;
- потеря implied meaning и появление подразумеваемого смысла, которого
  в JA нет.

ОСОБОЕ ВНИМАНИЕ — японским прагматическим конструкциям, частицам и формам,
где словарное содержание может быть передано правильно, но меняется функция
высказывания: ね / よ / かな / かも / さ / な / でしょう / んです / なんて /
まさか / 別に / ちょっと… и подобные.
НО не своди аудит к списку частиц: главное — их влияние на коммуникативный
смысл в конкретном контексте реплики (кто говорит, кому, зачем, после чего
и с какой интонацией).

ГЛАВНЫЙ ВОПРОС ПРОВЕРКИ:
«Сохранился ли в русском тот же коммуникативный акт и тот же подтекст,
который был в японском?»
Именно такие изменения — приоритетные кандидаты:
намёк → прямое утверждение; сомнение → уверенность; мягкая просьба →
требование; уклонение → прямой ответ; ирония → буквальность; скрытое
недовольство → нейтральная реплика; смягчённый отказ → категоричный отказ.

НАПРАВЛЕНИЕ ПРОВЕРКИ: JA → RU. Сначала установи, что говорящий делает своей
репликой в японском оригинале (и чего он сознательно не договаривает), затем
сверь, сохраняет ли текущий русский тот же речевой акт, ту же степень
уверенности, ту же силу реплики и тот же подтекст.

ЧТО НЕ ВХОДИТ В ЗАДАЧУ (не проверяй и не фиксируй):
- неправильные слова и обычные лексические переводческие ошибки, точность
  выбора русского слова, оттенки значения, эмоции, мимика, жесты, интонация —
  это слой микро-семантики, не прагматика;
- субъект/объект, обычные причинно-следственные и временные отношения,
  местоименные связи, обычная логика событий, намерение/цель персонажа
  как часть содержания ситуации, идиомы, метафоры — это слой
  макро-семантики и логики, не прагматика;
- грамматика (согласование, управление, падежи) — это russian-grammar-control;
- стиль (тавтология, повторы, кальки) — это russian-style-audit;
- оформление текста (кавычки, тире, курсив) — это russian-prose-rules;
- орфография и стилистические улучшения русского («можно сказать красивее»)
  — это вообще не находка;
- автоматические исправления: ты НИЧЕГО не исправляешь и ничего не пишешь
  в output/.

ПРОЦЕДУРА:
1. Прочитай скилл .agents/skills/pragmatic-audit/SKILL.md.
2. Для каждого смыслового блока <!-- block: N --> главы:
   - прочитай JA-блок и соответствующий RU-блок;
   - прочитай соседние блоки ТОЛЬКО как контекст (разговорный контекст и
     отношение говорящего часто раскрывают именно прагматику);
   - установи коммуникативный акт JA-реплики, её силу, степень уверенности
     и подтекст;
   - сверь с речевым актом, силой, категоричностью и подтекстом RU-реплики;
   - зафиксируй расхождения.
3. Находку относи только к тому блоку, где находится расхождение.

ФОРМАТ РЕЗУЛЬТАТА (ровно один JSON-объект, без markdown-обёртки):
{{
  "audit_id": "sma-c",
  "audit_type": "pragmatic-audit",
  "audit_run_id": "{run_id}",
  "chapter": "{sma_chapter_id(ch)}",
  "findings": [
    {{
      "block": 75,
      "source": "JA-фрагмент",
      "current": "RU-фрагмент",
      "aspect": "Смягчённая просьба → требование",
      "problem": "Тип проблемы",
      "reason": "Объяснение расхождения",
      "pragmatic_reason": "Почему это именно прагматическая проблема, а не литературное предпочтение",
      "confidence": "HIGH",
      "suggestion": "Предложенный вариант",
      "severity": "WARNING"
    }}
  ],
  "coverage": "Просмотренные блоки и объём проверки (см. правила)"
}}

ПРАВИЛА:
- severity: только ERROR / WARNING / CANDIDATE.
- confidence: только HIGH / MEDIUM / LOW. Расхождение должно быть реальным:
  нет уверенности — не включай находку; LOW допустим только при severity
  CANDIDATE.
- aspect — конкретный аспект прагматического расхождения: что именно
  изменилось (речевой акт, степень уверенности, сила/категоричность,
  намёк/недосказанность, скрытое отношение).
- reason — объяснение расхождения по JA → RU; pragmatic_reason — почему это
  именно прагматическая проблема (изменён коммуникативный смысл реплики),
  а не литературное предпочтение. Без pragmatic_reason находка недействительна.
- Если проблем нет — "findings": [] (пустой массив, объект всё равно обязателен).
- "coverage" (attestation покрытия) обязателен ВСЕГДА: какие блоки
  просмотрены и в каком объёме (напр. «блоки 1–29 целиком, соседние
  контексты проверены»). При "findings": [] coverage обязателен тем более:
  пустой массив без него — недоказанный «чистый» прогон, и валидатор
  (semantic_findings --validate) отклонит результат.
- source и current — точные цитаты, без пересказа.
- Литературное предпочтение — не ошибка: вариант «красивее» находкой не является.
- Не выдумывай: нет уверенности — не включай находку.

{SMA_OWN_FILE_NOTE}

OUTPUT FILE (единственный файл этого запуска):
{out_rel}
(абсолютный путь: {out_abs})
Запиши результат строго в описанном JSON-формате. Ничего больше не создавай
и не изменяй."""

# ---------------------------------------------------------------------------
# ANALYZER (A+B+C): prompt собирается из трёх частей, чтобы держать функции
# компактными: head (роль и входы) + rules (порядок и политика правок) +
# format (формат JSON/MD и пути результата).
# ---------------------------------------------------------------------------
def prompt_semantic_analyzer_phase1(ch: Chapter) -> str:
    """ФАЗА Analyzer 1 — ПОЛНОСТЬЮ BLIND (только JA + RU + контекст).

    В этот промпт физически НЕ передаются: findings A/B/C, evidence Omission
    Pre-check, provenance (sources), списки запусков и результаты прежних
    анализов. Изоляция проверяется self-test по итоговому тексту промпта
    (см. ``self_test_semantic_prompts``), а не только по формулировкам.

    Роль: независимая оценка JA → RU. Никакого отдельного алгоритма поиска
    пропусков здесь не запускается — просто самостоятельное сравнение
    перевода целиком.
    """
    phase1_id = new_audit_run_id(ch)
    return "\n\n".join([
        _sma_analyzer_p1_head(ch, phase1_id),
        _sma_analyzer_p1_rules(),
        _sma_analyzer_p1_format(ch, phase1_id),
    ])

def _sma_analyzer_p1_head(ch: Chapter, phase1_id: str) -> str:
    chap = sma_chapter_id(ch)
    p1_out = sma_phase1_rel_path(ch, phase1_id)
    return f"""ЗАДАЧА: смысловой анализатор (Analyzer), ФАЗА 1 — СЛЕПАЯ ПРОВЕРКА.
Глава: {chap}. Запуск фазы: {phase1_id}.

РОЛЬ
Ты — СМЫСЛОВОЙ АНАЛИЗАТОР, но в Фазе 1 ты работаешь как чистая независимая
сверка JA → RU. Ты ещё не видел ничьих находок и ничьих выводов — и не должен
их видеть. Фаза 1 обязана быть настоящей независимой оценкой, а не повтором
чужого мнения.

ВХОДНЫЕ ДАННЫЕ ЭТОЙ ФАЗЫ (и БОЛЬШЕ НИЧЕГО)
JA — authoritative source of truth (источник смысла): {ch.ja_path}
RU — text under review (текущий результат): {ch.output_path}
EN — reference only (только справочный материал): {ch.en_path}
Зеркало блоков (соседний контекст): {ch.merged_path}
Куда записать свой вывод Фазы 1: {p1_out}

{SMA_SOURCE_HIERARCHY_NOTE}

{SMA_AUTONOMY_NOTE}

ОГРАНИЧЕНИЕ ФАЗЫ 1
Это задание содержит только перечисленные выше файлы. Никакие другие
каталоги, файлы результатов, списки запусков и прошлые выводы в него не
входят и открываться не должны. Если тебе передали что-то сверх списка выше —
не используй это и сообщи о ошибке генерации задания.

После Фазы 1 будет отдельное задание Фазы 2, куда тебе передадут
результаты независимых проверок для сопоставления с твоим первоначальным
выводом. Сейчас об этом не думай: сделай самостоятельную оценку."""

def _sma_analyzer_p1_rules() -> str:
    return """ПОРЯДОК РАБОТЫ ФАЗЫ 1 (слепо, по каждому смысловому блоку)
  1) прочитай JA-блок;
  2) прочитай текущий RU-блок;
  3) прочитай соседние блоки для контекста;
  4) самостоятельно установи смысл JA;
  5) самостоятельно установи смысл RU;
  6) ответь на вопросы по существу:
     - есть ли semantic mismatch и в чём именно;
     - есть ли OMISSION — содержательный фрагмент JA, которому в RU нет
       никакого соответствия (полный обрыв, частичный обрыв, выпавшая
       реплика или событие);
     - есть ли ДОБАВЛЕННЫЙ смысл — в RU есть то, чего в JA нет;
     - есть ли другие существенные ошибки.

О МЕТОДЕ ПРОВЕРКИ ПОЛНОТЫ
Отдельный алгоритм поиска пропусков в Фазе 1 НЕ запускается. Ты просто
самостоятельно сравниваешь JA и RU как перевод в целом: если русский текст
заканчивается раньше японского, последовательность реплик или событий не
покрыта, либо фрагмент явно отсутствует — зафиксируй это как кандидата
omission. «JA длиннее RU» само по себе пропуском не является: сжатие,
слияние абзацев и убранный повтор — норма, если содержание сохранено.

ЗАПРЕЩЕНО В ФАЗЕ 1
- ссылаться на находки, оценки, статусы или вердикты других этапов:
  ты их не видел и не должен о них знать;
- подбирать заключение под чужие мнения: этих данных в Фазу 1 не передают
  и передавать не будут;
- править текст: правки вносятся только в Фазе 2 после сверки с
  переданным evidence;
- останавливаться и спрашивать разрешения: нулевое число находок —
  допустимый итог Фазы 1."""

def _sma_analyzer_p1_format(ch: Chapter, phase1_id: str) -> str:
    chap = sma_chapter_id(ch)
    p1_out = sma_phase1_rel_path(ch, phase1_id)
    return f"""ФОРМАТ ВЫВОДА ФАЗЫ 1 (ровно один JSON-объект, сохранить в {p1_out}):
{{
  "analysis_id": "{phase1_id}.phase1",
  "chapter": "{chap}",
  "phase": 1,
  "scope": "blind",
  "results": [
    {{
      "block": 15,
      "finding": "MISSING_TRANSLATION",
      "note": "Кратко: что именно отсутствует и почему это не компрессия",
      "confidence": "HIGH"
    }}
  ]
}}

Значения finding: MISTRANSLATION / NUANCE_SHIFT / LEXICAL_MISMATCH /
PRAGMATIC_SHIFT / ADDED_CONTENT / AMBIGUITY / MISSING_TRANSLATION / OTHER /
NONE.
- NONE — блок проверен, существенных ошибок нет.
- confidence: HIGH / MEDIUM / LOW.
- Это ПРЕДВАРИТЕЛЬНОЕ заключение слепой проверки, а не финальный вердикт:
  никакие финальные статусы и действия ЗДЕСЬ не выносятся — они появляются
  только в Фазе 2 после сверки с переданным evidence.
- Пустой список results = «существенных ошибок не найдено»; это допустимый
  итог, не повод останавливаться.
- Ничего, кроме этого JSON, в файл не пиши и никакие другие файлы не создавай."""

def prompt_semantic_analyzer(ch: Chapter, runs: dict[str, list[str]] | None = None) -> str:
    """ФАЗА Analyzer 2 — EVIDENCE REVIEW (после слепой Фазы 1).

    Analyzer — единственный агент, которому сознательно разрешено читать
    результаты независимых аудитов A/B/C (все существующие запуски ЭТОЙ
    главы; механизма ручного выбора run_id нет). Он
    самостоятельно сверяет candidates с JA/RU, исправляет только
    CONFIRMED_ERROR и записывает спорные случаи в отчёт analysis/.

    Два режима, логика одного и того же:
    - A+B — если запусков C ещё нет (старые главы / C не запускался);
    - A+B+C — если запуски C существуют.
    Наличие C не обязательно; majority vote запрещён в обоих режимах.

    Фаза 1 адресуется КОНКРЕТНЫМ файлом, а не маской: в задание попадает
    реальный путь ``analysis/<phase1_id>.phase1.json`` (при нескольких слепых
    прогонах — самый свежий, он же по умолчанию), а имя использованного файла
    обязательно фиксируется в ``inputs.phase1`` результата. Если файлов Фазы 1
    нет, задание прямо сообщает об этом и требует STOP.

    ``runs`` — только для self-test (симуляция содержимого каталогов a/b/c и
    списка файлов Фазы 1 через ключ ``"phase1"``); в рабочем режиме запуски и
    файлы Фазы 1 читаются с диска.
    """
    analysis_id = new_audit_run_id(ch)
    return "\n\n".join([
        _sma_analyzer_head(ch, analysis_id, runs),
        _sma_analyzer_rules(),
        _sma_analyzer_format(ch, analysis_id, runs),
    ])

def _sma_analyzer_head(ch: Chapter, analysis_id: str,
                       runs: dict[str, list[str]] | None = None) -> str:
    chap = sma_chapter_id(ch)
    a_dir = f"{SMA_REL_ROOT}/{chap}/a/"
    b_dir = f"{SMA_REL_ROOT}/{chap}/b/"
    c_dir = f"{SMA_REL_ROOT}/{chap}/c/"
    an_dir = f"{SMA_REL_ROOT}/{chap}/analysis/"
    run_map = (runs if runs is not None
               else {k: sma_existing_runs(ch, k) for k in ("a", "b", "c")})
    a_runs = run_map.get("a", [])
    b_runs = run_map.get("b", [])
    c_runs = run_map.get("c", [])
    a_list = ", ".join(a_runs) if a_runs else "(пока нет ни одного запуска A)"
    b_list = ", ".join(b_runs) if b_runs else "(пока нет ни одного запуска B)"
    c_list = ", ".join(c_runs) if c_runs else "(пока нет ни одного запуска C)"
    mode = "A + B + C" if c_runs else "A + B"
    pc_path = sma_precheck_rel_path(ch)
    pc_note = (f"{pc_path} (есть — учти как evidence)" if sma_precheck_exists(ch)
               else f"{pc_path} (не найден — работай без него, это норма)")
    p1_files = _sma_phase1_files_for(ch, runs)
    if not p1_files:
        p1_note = (
            f"ФАЙЛА ФАЗЫ 1 НЕТ: в {an_dir} нет ни одного <id>.phase1.json.\n"
            "Слепого заключения для этой главы не существует, поэтому эта\n"
            "схема работать не может. Сначала ОТДЕЛЬНОЕ задание «Смысловой\n"
            "анализатор — Фаза 1 (blind)», после него — заново сгенерированная\n"
            "Фаза 2."
        )
    elif len(p1_files) == 1:
        p1_note = (f"{an_dir}{p1_files[0]}\n"
                   "(единственный слепой вывод Фазы 1 этой главы —\n"
                   "работай ровно с ним)")
    else:
        listed = "\n".join(f"  {i}) {an_dir}{name}"
                           for i, name in enumerate(p1_files, 1))
        p1_note = (
            f"ВНИМАНИЕ: в {an_dir} НЕСКОЛЬКО слепых выводов Фазы 1 (самый\n"
            f"свежий — первым):\n{listed}\n"
            f"  По умолчанию используй САМЫЙ СВЕЖИЙ: {an_dir}{p1_files[0]}\n"
            "  Не смешивай выводы разных слепых прогонов (они не голоса и не\n"
            "  дополняют друг друга). Выбранный файл обязательно зафиксируй\n"
            "  в inputs.phase1."
        )
    return f"""ЗАДАЧА: смысловой анализатор (Analyzer) независимых аудитов A, B и прагматического аудита C.
Глава: {chap}. Запуск анализа: {analysis_id}.

РОЛЬ
Ты НЕ независимый аудитор: ты получаешь результаты уже выполненных
независимых аудитов A, B и C и выносишь итоговое решение по каждому
кандидату. Доступ к результатам A/B/C — сознательное исключение именно
для Analyzer.

ВХОДНЫЕ ДАННЫЕ ЭТОЙ ГЛАВЫ
JA — authoritative source of truth (источник смысла): {ch.ja_path}
RU — text under review (текущий результат): {ch.output_path}
EN — reference only (только справочный материал): {ch.en_path}
Зеркало блоков (JA/EN/RU, соседний контекст): {ch.merged_path}
Слепой вывод Фазы 1 (твоё собственное ПЕРВОНАЧАЛЬНОЕ заключение, сделано
БЕЗ evidence) — конкретный файл этого запуска:
  {p1_note}
Результаты Auditor A (читай ТОЛЬКО этот каталог): {a_dir}
Результаты Auditor B (читай ТОЛЬКО этот каталог): {b_dir}
Результаты Pragmatic Auditor C (читай ТОЛЬКО этот каталог): {c_dir}
Evidence общего Omission Pre-check (детерминированный pre-check, НЕ аудитор):
  {pc_path}
Каталог результатов Analyzer (куда писать): {an_dir}

{SMA_SOURCE_HIERARCHY_NOTE}

НАБОР EVIDENCE (inputs этой главы)
a_runs: {a_list}
b_runs: {b_list}
c_runs: {c_list}
precheck: {pc_note}
phase1: {p1_files[0] if p1_files else "(нет файла Фазы 1 — работать нельзя)"}

РЕЖИМ ЭТОГО ЗАПУСКА: {mode}
- Режим A + B — если в c/ нет ни одного <run_id>.json: работай только с
  findings A и B. Отсутствие запусков C — норма (C ещё не запускался),
  это не повод останавливаться.
- Режим A + B + C — если запуски C существуют: подключи их findings наравне
  с findings A и B (тот же порядок работы, тот же статус, тот же разбор).
Наличие C НЕ обязательно: анализ главы, где C не запускался, выполняется
в прежнем объёме A+B.
Наличие pre-check НЕ обязательно: если его файла нет — работай без него и не
останавливайся.

ПРАВИЛА EVIDENCE:
- Учитывай ВСЕ существующие запуски этой главы, а не только последний:
  если в a/, b/ или c/ появились другие <run_id>.json — включи их все
  (ручного выбора отдельных запусков нет).
- Результаты ДРУГИХ глав не используй: анализируй только эту главу.
- Если в a/, b/ и c/ нет ни одного <run_id>.json — сообщи, что сначала нужно
  выполнить аудит, и остановись (правки не вноси)."""

def _sma_analyzer_rules() -> str:
    return """ШАГ 0 — УБЕДИСЬ, ЧТО ФАЗА 1 УЖЕ ВЫПОЛНЕНА (слепо, без evidence)
Фаза 1 выполнялась ОТДЕЛЬНЫМ заданием, куда не передавалось НИКАКОГО
evidence: ни findings A/B/C, ни данных детерминированного pre-check, ни
происхождения находок, ни прежних analysis-результатов. Её вывод лежит в
analysis/<phase1_id>.phase1.json — это твоё СОБСТВЕННОЕ ПЕРВОНАЧАЛЬНОЕ
заключение по чистой сверке JA → RU: есть ли mismatch, есть ли OMISSION,
есть ли добавленный смысл, есть ли другие существенные ошибки.
- В задании назван КОНКРЕТНЫЙ файл Фазы 1 (см. блок «конкретный файл этого
  запуска» и строку phase1 в наборе evidence) — работай ровно с ним, а не с
  «каким-нибудь» файлом из каталога analysis/.
- Если задание перечислило НЕСКОЛЬКО слепых выводов Фазы 1 (повторный
  прогон слепой фазы — норма), бери САМЫЙ СВЕЖИЙ: он указан первым и назван
  «по умолчанию». Слепые выводы разных прогонов НЕ смешивай: они не голоса и
  не дополняют друг друга — это два независимых первоначальных заключения.
- inputs.phase1 результата — обязательный provenance слепой фазы, такой же,
  как sources.a/b/c для аудиторов: запиши туда имя фактически использованного
  файла. Без него нельзя проверить, с каким слепым выводом сверялся анализ.
- Если файла Фазы 1 нет (задание прямо говорит «ФАЙЛА ФАЗЫ 1 НЕТ», а
  inputs.phase1 = null) — STOP: Фазу 1 выполнять в этом задании НЕЛЬЗЯ.
  Это задание уже содержит evidence, поэтому слепая проверка внутри него
  невозможна (blindness утрачена). НЕ пытайся выполнить Фазу 1 в рамках
  Фазы 2: сначала запусти ОТДЕЛЬНОЕ задание «Смысловой анализатор —
  Фаза 1 (blind)», сохрани его вывод в analysis/<id>.phase1.json, и только
  после завершения Фазы 1 выполняй Фазу 2.
- Вывод Фазы 1 — входные данные, а НЕ evidence и не чужое мнение: он не
  голосует и не является основанием для правки.

ШАГ 1 — СБОР EVIDENCE (Фаза 2 начинается здесь)
Собери ВСЕ findings из всех существующих запусков A, B и C ЭТОЙ главы плюс
evidence детерминированного omission pre-check. Логически совпадающие
candidates сгруппируй и сохрани происхождение: какие A-запуски, какие
B-запуски и какие C-запуски нашли этот candidate (sources.a / sources.b /
sources.c) и отмечен ли он pre-check'ом (precheck).

ФАЗА 2 — EVIDENCE REVIEW (ТОЛЬКО после завершённой Фазы 1)
  1) воспроизведи своё заключение Фазы 1 — каким оно было ДО evidence;
  2) посмотри findings A;
  3) посмотри findings B;
  4) посмотри findings C;
  5) посмотри evidence omission pre-check;
  6) сопоставь всё со своим первоначальным выводом;
  7) реши по каждому candidate: подтвердить, отвергнуть или создать нового;
  8) реши, достаточно ли оснований для правки.

ДОПУСТИМЫЕ ИСХОДЫ (все перечисленные — норма, не ошибка процесса)
- pre-check нашёл пропуск, Фаза 1 его не заметила → после сверки с JA → RU
  можно CONFIRMED_ERROR (и FIXED, если правка разрешена).
- Фаза 1 считает перевод корректным, а pre-check подозревает пропуск → после
  проверки DISPUTED (границы/допустимость неясны) либо FALSE_POSITIVE
  (компрессия допустима).
- pre-check и аудиторы молчат, а Фаза 1 нашла ошибку → candidate создаёшь ты.
- pre-check отсутствует → работай с A/B/C в прежнем объёме.
- Фаза 1 сама не заметила то, что подтвердилось в Фазе 2 — это не порок
  слепой проверки: именно поэтому фазы разделены.

ЗАПРЕЩЕНО:
- majority vote; «A + B + C → ошибка»; «BOTH_FOUND → ERROR автоматически»;
- считать, что согласие всех аудиторов подтверждает ошибку, а находка только
  одного (в том числе только C) — автоматически ложный positive;
- считать количество обнаружений доказательством: это только evidence;
- принимать решение вместо проверки JA → RU;
- считать EN источником истины или опираться на совпадение RU с EN:
  если evidence аудитора или EN противоречит JA, ориентируйся на JA
  (JA > EN); совпадение RU с EN само по себе не доказывает корректности
  RU — решение принимается только по паре JA → RU.

ПРОИСХОЖДЕНИЕ (sources) НЕ ГОЛОСУЕТ
- sources.a / sources.b / sources.c — это отметка о том, кто заметил место,
  а не голос за статус.
- finding C не имеет приоритета над A/B и не отменяется отсутствием находок
  в A/B (и наоборот): каждый candidate рассматривается сам по себе.
- Режим A+B (запусков C нет) и режим A+B+C обрабатываются одинаково:
  меняется только набор evidence, но не порядок работы и не статусы.

ДВЕ ОСИ РЕШЕНИЯ (каждому candidate обязательны ОБЕ)
Ось достоверности fidelity (что именно не так):
- MEANING_SHIFT — смысл искажён: JA говорит X, RU говорит Y.
- COMPONENT_LOSS — ядро смысла передано, но потерян компонент (оттенок,
  модальность, эмоциональная составляющая, деталь, регистр).
- ADDITION — в RU есть содержание, которого нет в JA.
- MISSING — фрагмент JA отсутствует в RU (omission-candidate).
- RUSSIAN_ERROR — смысл в порядке, ошибочен сам русский (грамматика,
  орфография, коллокация).
- FORMAT — формат/оформление: разметка, кавычки, курсив, абзацы.
Ось действия action (что делать):
- FIXED — правка внесена через fix_block.py (обязательны before/after).
- REPORT_ONLY — в отчёт, перевод не менять (крупная или спорная правка).
- PRESERVED — finding отклонён, текст сохранён.
Исход status (каждому candidate обязателен один):
- CONFIRMED_ERROR — подтверждённая по сверке JA → RU ошибка; правка разрешена.
- DISPUTED — расхождение мнений аудиторов, неоднозначность JA или
  неподтверждённое предложение → НЕ исправлять.
- FALSE_POSITIVE — finding не подтверждается → НЕ исправлять.
- OPTIONAL упразднён: «допустимое улучшение» не является классом потери;
  если потери нет — FALSE_POSITIVE + PRESERVED, если компонент потерян —
  fidelity COMPONENT_LOSS и решение по политике ниже.
ПОЛИТИКА ДЕЙСТВИЯ (по fidelity и размеру правки):
- FIXED — всегда при MEANING_SHIFT / MISSING / ADDITION / RUSSIAN_ERROR / FORMAT.
- при COMPONENT_LOSS: правка минимальна (одна лексема/форма либо ≤ 120
  символов в пределах одного предложения) и обоснована JA → FIXED;
  правка крупнее (переписывание предложения или абзаца) → REPORT_ONLY.
- PRESERVED — только когда finding отклонён (FALSE_POSITIVE).
- FIXED допустим ТОЛЬКО со status CONFIRMED_ERROR; для него обязательны
  before и after (так же проверяет scripts/semantic_findings.py).

ПРАВКА (только текущая глава)
- WARNING / CANDIDATE сами по себе НЕ разрешают правку; исправляй ТОЛЬКО
  CONFIRMED_ERROR.
- Перед правкой зафиксируй исходное состояние блока: сохрани RU-блок «before»
  и подготовь «after».
- Правку вноси ТОЛЬКО через scripts/fix_block.py (текст блока — через
  --text-file или --replace-file). НЕ перезаписывай output/vXX-chYY.md вручную.
- После каждой правки: scripts/update_merged.py, затем повторная проверка
  изменённого блока (grammar/style/format — по текущему pipeline) и сверка с JA.
- Ничего не меняй «заодно»; соседние блоки без необходимости не редактируй.
- После исправления одного блока следующие candidates проверяй по АКТУАЛЬНОМУ
  RU (а findings A/B/C остаются историческими).
- НЕ делай цикл A → B → C → Analyzer → правка → A → B → C → … : после Analyzer
  цикл заканчивается; повторный аудит — отдельный ручной запуск.

НЕИЗМЕНЯЕМОСТЬ EVIDENCE
- findings A/B/C — исторические результаты: НЕ редактируй, не удаляй и не
  переписывай файлы в a/, b/ и c/. Даже исправленный finding остаётся в истории.
- Старые отчёты output/_audit/vXX-chYY.md не являются источником истины и не
  подменяют A/B/C.
- Результаты Analyzer пишутся только в каталог analysis/ этой главы."""

def _sma_analyzer_format(ch: Chapter, analysis_id: str,
                         runs: dict[str, list[str]] | None = None) -> str:
    chap = sma_chapter_id(ch)
    run_map = (runs if runs is not None
               else {k: sma_existing_runs(ch, k) for k in ("a", "b", "c")})
    a_json = ", ".join(f'"{r}"' for r in run_map.get("a", []))
    b_json = ", ".join(f'"{r}"' for r in run_map.get("b", []))
    c_json = ", ".join(f'"{r}"' for r in run_map.get("c", []))
    out_rel = sma_result_rel_path(ch, "analysis", analysis_id, "json")
    out_md_rel = sma_result_rel_path(ch, "analysis", analysis_id, "md")
    out_abs = sma_result_abs_path(ch, "analysis", analysis_id, "json")
    out_md_abs = sma_result_abs_path(ch, "analysis", analysis_id, "md")
    # inputs.precheck: путь к evidence pre-check или null (pre-check не гонялся)
    pc_input = (f'"{sma_precheck_rel_path(ch)}"' if sma_precheck_exists(ch)
                else "null")
    # inputs.phase1: имя файла слепого вывода Фазы 1 (по умолчанию — самый
    # свежий) или null, если Фазы 1 для главы не было.
    p1_files = _sma_phase1_files_for(ch, runs)
    p1_input = f'"{p1_files[0]}"' if p1_files else "null"
    return f"""ФОРМАТ РЕЗУЛЬТАТА (ровно один JSON-объект, без markdown-обёртки):
{{
  "analysis_id": "{analysis_id}",
  "chapter": "{chap}",
  "inputs": {{
    "a_runs": [{a_json}],
    "b_runs": [{b_json}],
    "c_runs": [{c_json}],
    "precheck": {pc_input},
    "phase1": {p1_input}
  }},
  "results": [
    {{
      "block": 11,
      "candidate_id": "C-11-01",
      "sources": {{ "a": ["<run_id>"], "b": ["<run_id>"], "c": ["<run_id>"], "precheck": false }},
      "source": "JA fragment",
      "current": "RU fragment",
      "fidelity": "MEANING_SHIFT",
      "status": "CONFIRMED_ERROR",
      "reason": "Обоснование Analyzer",
      "suggestion": "Исправленный вариант",
      "action": "FIXED",
      "before": "RU-блок до правки (обязательно для FIXED)",
      "after": "RU-блок после правки (обязательно для FIXED)"
    }}
  ]
}}

fidelity обязателен для каждого result: MEANING_SHIFT / COMPONENT_LOSS /
ADDITION / MISSING / RUSSIAN_ERROR / FORMAT (оси решения см. выше).
Разрешённые status: CONFIRMED_ERROR / DISPUTED / FALSE_POSITIVE
(OPTIONAL упразднён; в старых analysis-JSON остаётся как легаси).
Разрешённые action: FIXED / REPORT_ONLY / PRESERVED.
- FIXED — только для CONFIRMED_ERROR и только когда политика размера
  правки даёт «внести» (правка внесена через fix_block.py).
- REPORT_ONLY — DISPUTED, а также COMPONENT_LOSS с крупной правкой
  (в отчёт, перевод не менять).
- PRESERVED — FALSE_POSITIVE (оставлено как есть).
Для каждого FIXED обязательны before и after.
- inputs.a_runs / inputs.b_runs / inputs.c_runs — все существующие запуски
  этой главы на момент анализа (в режиме A+B поле c_runs пустое).
- inputs.precheck — путь к evidence детерминированного omission pre-check
  либо null, если pre-check для главы не прогонялся (это норма).
- inputs.phase1 — имя файла слепого вывода Фазы 1, с которым сверялся этот
  результат (по умолчанию — самый свежий, см. задание); provenance слепой
  фазы, такой же обязательный, как sources.a/b/c. Если файла Фазы 1 не было,
  там null — это признак того, что анализ выполнен без слепой фазы (STOP, а
  не валидный результат).
- sources каждого candidate — из каких запусков A/B/C он собран; пустой
  список означает, что этот аудит находку не находил.
- sources.precheck — маркер того, что candidate пришёл от omission pre-check:
  это evidence, а не голос (как и sources.a/b/c).

OUTPUT FILES (этой главы, запуск {analysis_id})
JSON: {out_rel}
MD:   {out_md_rel}
(абсолютные пути: {out_abs} и {out_md_abs})
JSON — машинный результат; MD — человекочитаемый отчёт с таблицей по каждому
candidate (block, candidate_id, sources A/B/C, fidelity, status, reason,
action, before/after для FIXED; отдельно сводка по DISPUTED и по всем
candidate с action REPORT_ONLY).
Пиши только в каталог analysis/ этой главы; другие файлы не создавай и не
изменяй."""

# ============================================================================
# СПИСОК ПРОМПТОВ
# ============================================================================
PROMPTS: list[PromptInfo] = [
    PromptInfo(
        "Первый запуск",
        "Подготовка и сразу начало работы",
        """
Проверяет, что проект правильно подготовлен к работе с этой главой,
и в том же запуске начинает обработку.
Агент изучит текущие инструкции, словарь терминов, исходные тексты
и уже существующие результаты, определит, на каком этапе находится
работа, и проверит, нет ли проблем, которые могут помешать дальнейшей
обработке. После успешной проверки агент НЕ останавливается и не просит
разрешения: он переходит к первому блоку и выполняет обычный pipeline.
Локальные неопределённости решаются как PROVISIONAL и не блокируют
работу; остановка — только при действительно блокирующей
неопределённости.
Использовать при начале работы с новой главой или после существенного
изменения структуры проекта.
""".strip(),
        prompt_first_launch,
        group=GROUP_CHAPTER,
        slug="first-launch",
    ),
    PromptInfo(
        "Продолжение",
        "Продолжить работу с текущего состояния",
        """
Продолжает работу с того места, где глава была оставлена.
Агент сначала определит текущее состояние главы и уже выполненную
работу, чтобы не повторять предыдущие этапы без необходимости.
Сохраняет существующие переводческие и редакторские решения
и продолжает обработку с подходящего следующего этапа.
Использовать для обычного продолжения незавершённой работы.
""".strip(),
        prompt_continue,
        group=GROUP_CHAPTER,
        slug="continue",
    ),
    PromptInfo(
        "Полный аудит",
        "Полная последовательная проверка главы",
        """
Проводит максимально полную проверку готового или почти готового
текста главы.
Проверяется соответствие оригиналу, качество русского текста,
естественность речи, грамматика, стиль, терминология и возможные
следы машинного перевода.
Проверка проходит от смысла к художественной форме, поэтому сначала
выявляются серьёзные смысловые проблемы, а затем менее критичные
языковые и стилистические недостатки.
Японский оригинал используется как основной источник смысла,
английский перевод — как дополнительная опора.
Использовать, когда нужно получить максимально тщательно проверенную
версию главы перед завершением работы.
""".strip(),
        prompt_full_audit,
        group=GROUP_AUDITS,
        slug="full-audit",
    ),
    PromptInfo(
        "Быстрый аудит",
        "Быстрая проверка текущего результата",
        """
Быстро проверяет текущий русский текст на наиболее заметные проблемы.
В первую очередь ищет пропуски, очевидные смысловые ошибки,
неправильные имена и термины, грубые грамматические ошибки,
явную машинность и бросающиеся в глаза стилистические проблемы.
Не предназначен для глубокой литературной переработки всей главы.
Использовать для промежуточной проверки или когда нужно быстро
понять, есть ли в текущем результате серьёзные проблемы.
""".strip(),
        prompt_quick_audit,
        group=GROUP_AUDITS,
        slug="quick-audit",
    ),
    PromptInfo(
        "Грамматический аудит",
        "Грамматика, управление, падежи и синтаксис",
        """
Проверяет русский текст именно с точки зрения грамматики.
Особое внимание уделяется согласованию, управлению, падежам,
связям между словами, формам глаголов, местоимениям и синтаксису.
Задача режима — исправлять реальные грамматические ошибки,
не переписывая текст только ради изменения формулировки.
Авторская интонация, разговорная речь и индивидуальный стиль
персонажей должны сохраняться, если они не нарушают грамматическую
норму намеренно.
Использовать, когда смысл и стиль текста уже в целом устраивают,
но требуется отдельная проверка русского языка.
""".strip(),
        prompt_grammar_audit,
        group=GROUP_AUDITS,
        slug="grammar-audit",
    ),
    PromptInfo(
        "Стилевой аудит",
        "Повторы, тавтология, кальки и неудачные формулировки",
        """
Проверяет, насколько естественно и цельно звучит русский текст.
Ищет ненужные повторы, тавтологию, неудачные сочетания слов,
кальки, тяжёлые конструкции, избыточные формулировки и другие
стилистические проблемы.
При этом намеренные повторы, характерная речь персонажей и другие
художественные приёмы не должны автоматически считаться ошибками.
Цель — сделать текст естественнее, не стирая его индивидуальность
и не превращая его в безликую литературную переработку.
Использовать после смысловой и грамматической проверки.
""".strip(),
        prompt_style_audit,
        group=GROUP_AUDITS,
        slug="style-audit",
    ),
    PromptInfo(
        "Humanizer / machine-like",
        "Поиск признаков машинного перевода и искусственной речи",
        """
Ищет места, которые формально выглядят правильными, но звучат
неестественно для живого русского текста.
Проверяются кальки, необычный порядок слов, шаблонные конструкции,
чрезмерно книжные обороты, повторяющиеся синтаксические схемы
и другие признаки машинной или искусственно сгенерированной речи.
Режим не должен просто делать текст более красивым или литературным.
Его задача — убрать ощущение машинности, сохранив исходный смысл,
тон и индивидуальную речь персонажей.
Использовать, когда перевод уже смыслово корректен,
но отдельные фразы всё ещё звучат как перевод.
""".strip(),
        prompt_humanizer,
        group=GROUP_AUDITS,
        slug="humanizer",
    ),
    PromptInfo(
        "JA / EN alignment",
        "Сверка японского и английского источников",
        """
Проверяет русский перевод одновременно по японскому оригиналу
и английской версии.
Основная задача — обнаружить места, где при переводе могли появиться
пропуски, добавления или смысловые смещения.
Отдельно проверяются имена, обращения, термины, местоимения,
отрицания, действия персонажей, эмоциональные оттенки и другие
детали, которые могли измениться при переводе.
Японский текст имеет приоритет как исходник. Английский текст
используется для дополнительного сопоставления и может помочь
понять неоднозначные места.
Использовать, когда есть сомнения в точности перевода
или необходимо проверить уже готовый русский текст по источникам.
""".strip(),
        prompt_alignment,
        group=GROUP_AUDITS,
        slug="alignment",
    ),
    PromptInfo(
        "Обработка одного блока",
        "Обработать только выбранный блок",
        """
Полностью обработать один конкретный блок текста, не затрагивая
остальную главу.
Сначала проверяется соответствие оригиналу, затем русский текст
редактируется и проверяется на естественность, грамматику и стиль.
Все изменения ограничиваются выбранным блоком, кроме случаев,
когда для понимания необходимо посмотреть соседний контекст.
Использовать для точечной работы, проверки спорного места
или постепенной обработки большой главы по частям.
""".strip(),
        None,
        group=GROUP_CHAPTER,
        slug="one-block",
    ),
    PromptInfo(
        "Проверка кодировки",
        "Проверка UTF-8 и повреждённых символов",
        """
Проверяет файлы на технические проблемы с текстовой кодировкой.
Ищет повреждённые символы, mojibake, проблемы с UTF-8,
некорректные кавычки, тире, многоточия и другие символы,
которые могли испортиться при преобразовании файлов.
Содержание текста при этом не редактируется.
Использовать, если после конвертации файлов, переноса текста
или работы с разными редакторами появились подозрительные символы.
""".strip(),
        prompt_encoding,
        group=GROUP_CHAPTER,
        slug="encoding",
    ),
    PromptInfo(
        "Решения пользователя (OPEN / DEFERRED / PROVISIONAL)",
        "Применить решения по отложенным вопросам и временным значениям словаря",
        """
Разбирает решения пользователя по вопросам со статусом OPEN / DEFERRED
и по временным (PROVISIONAL) значениям словаря, после чего применяет
их в одном проходе.
Агент выписывает каждый пункт решения, находит все места, где
встречается затронутое сомнение или форма, и приводит их в
соответствие — не только в текущей главе, но во всех файлах тома,
если решение относится к правилу или термину.
Отложенные вопросы закрываются со статусом RESOLVED (правка внесена)
или CLOSED (оставлено как есть), временные записи словаря переходят
в канон либо заменяются во всех местах. Решение фиксируется в реестре
аудита и в журнале, после правок выполняется повторный контроль.
Использовать после того, как пользователь дал решения по реестру
«Отложенные вопросы (OPEN / DEFERRED)» или по PROVISIONAL-терминам.
""".strip(),
        prompt_resolve_decisions,
        group=GROUP_CHAPTER,
        slug="resolve-decisions",
    ),
    # GAP-аудит (prompt_gap_audit) УДАЛЁН из активного меню: это LEGACY.
    # Поиск пропусков выполняет общий Omission Pre-check
    # (AINovelEdit/scripts/omission_precheck.py) → evidence для Analyzer.
    # Функция prompt_gap_audit сохранена ниже как исторический задел и из
    # меню недоступна (аналогично prompt_dual_semantic_audit).
    # «Реконтроль готовой главы (новые правила)» УДАЛЁН из активного меню:
    # главы-первоисточники закрыты, новые правила уже влиты в AGENTS.md и
    # скиллы, отдельный режим больше не нужен. Функция prompt_rules_recheck
    # сохранена ниже как исторический задел (аналогично prompt_gap_audit и
    # prompt_dual_semantic_audit) — не удалять и не подключать без задачи.
    PromptInfo(
        "Смысловой аудит A",
        "Изолированный аудит A: лексика, оттенки, эмоции (независимый запуск)",
        """
        Генерирует задание для ОДНОГО независимого смыслового аудитора A.
        Фокус A: лексическая точность, оттенки значения, эмоции, мимика,
        жесты, интонация, степень выраженности, потеря/добавление небольшого
        смыслового компонента; направление проверки JA → RU.

        Задание изолировано: в нём нет ни малейшей ссылки на второго
        аудитора, на его результаты, на старые отчёты аудита и на каталог
        output/_audit/sma/. Аудитор получает уникальный audit_run_id и ровно
        один выходной файл:
        output/_audit/sma/<chapter>/a/<audit_run_id>.json

        Каждый запуск — самостоятельный эксперимент: повторный вызов даёт
        новый audit_run_id и не перезаписывает предыдущий результат.

        Грамматика, стиль и оформление в задачу НЕ входят; текст аудитор не
        исправляет — только фиксирует находки.
        """.strip(),
        prompt_semantic_a,
        group=GROUP_SMA,
        slug="sma-a",
    ),
    PromptInfo(
        "Смысловой аудит B",
        "Изолированный аудит B: связи, логика, контекст (независимый запуск)",
        """
        Генерирует задание для ОДНОГО независимого смыслового аудитора B.
        Фокус B: субъект/объект, действие, состояние, причинно-следственные
        и временные связи, логика, местоименные связи, модальность, идиомы,
        метафоры, контекст, неоднозначные конструкции, намерение персонажа.

        Задание изолировано: в нём нет ни малейшей ссылки на первого
        аудитора, на его результаты, на старые отчёты аудита и на каталог
        output/_audit/sma/. Аудитор получает уникальный audit_run_id и ровно
        один выходной файл:
        output/_audit/sma/<chapter>/b/<audit_run_id>.json

        Каждый запуск — самостоятельный эксперимент: повторный вызов даёт
        новый audit_run_id и не перезаписывает предыдущий результат.

        Грамматика, стиль и оформление в задачу НЕ входят; текст аудитор не
        исправляет — только фиксирует находки.
        """.strip(),
        prompt_semantic_b,
        group=GROUP_SMA,
        slug="sma-b",
    ),
    PromptInfo(
        "Прагматический аудит C",
        "Изолированный Pragmatic Audit C: речевой акт, подтекст, сила реплики (независимый запуск)",
        """
        Генерирует задание для ОДНОГО независимого прагматического аудитора C
        (Pragmatic Audit C / pragmatic-audit).

        C — НЕ третий универсальный смысловой аудитор: он закрывает отдельный
        слой смысла — коммуникативный смысл высказывания. Фокус C:
        что говорящий фактически делает своей репликой; сохранились ли намёк
        и недосказанность; степень уверенности/неуверенности (предположение vs
        утверждение, сомнение vs уверенность); просьба vs требование, мягкий
        отказ vs прямой, уклонение vs прямой ответ, разрешение vs приказ,
        обещание vs намерение, предупреждение vs сообщение; удивление,
        недоверие, ирония, сарказм, скрытое отношение; смягчение/усиление,
        коммуникативная сила и категоричность; потеря или появление implied
        meaning. Особое внимание — японским прагматическим частицам и формам
        (ね, よ, かな, かも, さ, な, でしょう, んです, なんて, まさか, 別に,
        ちょっと…), но проверка не сводится к списку частиц: важен их эффект
        на коммуникативный смысл в конкретном контексте.

        Главный вопрос C: «Сохранился ли в русском тот же коммуникативный акт
        и тот же подтекст, который был в японском?»

        Задание изолировано: в нём нет ни малейшей ссылки на других аудиторов,
        на их результаты, на Analyzer, на старые отчёты аудита и на каталог
        output/_audit/sma/. Аудитор получает уникальный audit_run_id и ровно
        один выходной файл:
        output/_audit/sma/<chapter>/c/<audit_run_id>.json

        Каждый запуск — самостоятельный эксперимент: повторный вызов даёт
        новый audit_run_id и не перезаписывает предыдущий результат.

        Лексика, макро-смысл/логика, грамматика, стиль и оформление в задачу
        НЕ входят; текст аудитор не исправляет — только фиксирует находки.
        """.strip(),
        prompt_pragmatic_c,
        group=GROUP_SMA,
        slug="sma-c",
    ),
    PromptInfo(
        "Смысловой анализатор — Фаза 1 (blind)",
        "Analyzer: слепая самостоятельная сверка JA → RU, БЕЗ какого-либо evidence",
        """
        Первая из двух НЕЗАВИСИМЫХ фаз работы Analyzer.

        Задание содержит ТОЛЬКО: JA, текущий RU, EN и зеркало блоков
        (соседний контекст). Физически не передаются и не должны передаваться:
        findings A/B/C, evidence omission pre-check, происхождение находок
        (sources), списки запусков и результаты прежних анализов.

        Analyzer сам отвечает: есть ли semantic mismatch, есть ли OMISSION
        (содержательный фрагмент JA без соответствия в RU), есть ли
        добавленный смысл, есть ли другие существенные ошибки. Отдельный
        алгоритм поиска пропусков здесь НЕ запускается — просто
        самостоятельное сравнение перевода целиком.

        Никаких вердиктов (CONFIRMED_ERROR / DISPUTED / ...) Фаза 1 не
        выносит — только предварительное заключение в
        output/_audit/sma/<chapter>/analysis/<id>.phase1.json.

        Запускать ПЕРЕД «Смысловой анализатор — Фаза 2».
        Изоляция проверяется self-test (tools/agent_workflow.py
        --self-test-sma).
        """,
        prompt_semantic_analyzer_phase1,
        group=GROUP_SMA,
        slug="analyzer-phase1",
    ),
    PromptInfo(
        "Смысловой анализатор — Фаза 2 (evidence review)",
        "Analyzer: сверяет свой слепой вывод Фазы 1 с A/B/C + omission pre-check",
        """
        Вторая фаза: сюда сознательно передаются ВСЕ evidence — findings A,
        B и C, а также evidence детерминированного omission pre-check
        (scripts/omission_precheck.py) — и собственное слепое заключение
        Фазы 1: в задании указывается КОНКРЕТНЫЙ файл
        (analysis/<phase1_id>.phase1.json; при нескольких прогонах слепой
        фазы — самый свежий, он же по умолчанию), а имя использованного
        файла обязательно фиксируется в inputs.phase1 результата.
        Если файлов Фазы 1 для главы нет, задание требует STOP: сначала
        отдельный запуск Фазы 1, затем заново сгенерированная Фаза 2.

        Analyzer сопоставляет evidence со своим первоначальным выводом:
        он может подтвердить finding, отвергнуть его, создать нового или
        принять кандидат pre-check, которого сам в Фазе 1 не заметил.

        Pre-check — evidence, а не голос и не Auditor D; A/B/C — тоже
        evidence. Majority vote запрещён: «A+B+C согласны → ошибка» и
        «только C нашёл → false positive» одинаково недопустимы.

        Два режима сохранены: A + B (C не запускался) и A + B + C;
        отсутствие pre-check не мешает работе. Две оси решения: fidelity
        (MEANING_SHIFT / COMPONENT_LOSS / ADDITION / MISSING / RUSSIAN_ERROR /
        FORMAT) + action (FIXED / REPORT_ONLY / PRESERVED) при исходе status
        CONFIRMED_ERROR / DISPUTED / FALSE_POSITIVE (OPTIONAL упразднён);
        правка только через
        fix_block.py. Результат: output/_audit/sma/<chapter>/analysis/.

        Запускать ПОСЛЕ «Смысловой анализатор — Фаза 1».
        """,
        prompt_semantic_analyzer,
        group=GROUP_SMA,
        slug="analyzer-phase2",
    ),
]

# ============================================================================
# ACTIONS (технические действия оркестратора; НЕ LLM-промпты)
# ============================================================================
def action_omission_precheck(ch: Chapter) -> int:
    """Детерминированная проверка пропусков перед A/B/C.

    Техническое действие оркестратора: запускает
    AINovelEdit/scripts/omission_precheck.py и показывает stdout/stderr и
    код завершения. Не создаёт LLM-промпт, не является LLM-аудитом и не
    меняет перевод. Evidence складывается в
    output/_audit/sma/<chapter>/precheck/omission-precheck.json.
    """
    script = "scripts/omission_precheck.py"
    file_name = ch.file_name
    result_rel = sma_precheck_rel_path(ch)
    command_display = f"python {script} --file {file_name} --json"
    print()
    separator("=")
    print(f"  Глава: {ch.chapter_id_full}")
    print()
    print("  Действие:")
    print("  Omission Pre-check")
    print()
    print("  Команда:")
    print(f"  {command_display}")
    print()
    print("  Назначение:")
    print("  детерминированная проверка пропусков.")
    print("  Не является LLM-аудитом.")
    print("  Не изменяет перевод.")
    print()
    print("  Результат:")
    print(f"  {result_rel}")
    separator("=")
    print()

    command = [sys.executable, script, "--file", file_name, "--json"]
    try:
        process = subprocess.run(
            command,
            cwd=AINOVELEDIT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        print(f"  Не удалось запустить omission_precheck.py: {exc}")
        return 1

    print("  --- stdout ---")
    print((process.stdout or "").rstrip())
    if process.stderr:
        print("  --- stderr ---")
        print(process.stderr.rstrip())
    print()
    print(f"  Код завершения: {process.returncode}")
    print()
    return process.returncode

# ---------------------------------------------------------------------------
# ДЕЙСТВИЯ ПОЛНОГО ПРОГОНА: ПРЕДФИЛЬТРЫ И ГЕЙТ ГЛАВЫ
# ---------------------------------------------------------------------------
PREFILTER_ACTION_NAME = "Предфильтры (прогнать сканеры)"
GATE_ACTION_NAME = "Гейт готовности главы"
# Отчёты обязательных предфильтров: <stem>-<kind>.md в _prefilter/.
# check_records --report не умеет, drift_scan опционален — в набор не входят.
PREFILTER_KINDS = ("grammar", "style", "format", "address", "alignment")

def prefilter_report_paths(ch: Chapter) -> dict[str, str]:
    """Пути отчётов предфильтров главы (ключ — kind, см. PREFILTER_KINDS)."""
    stem = os.path.splitext(ch.file_name)[0]
    folder = os.path.join(AINOVELEDIT, "output", "_audit", "_prefilter")
    return {kind: os.path.join(folder, f"{stem}-{kind}.md")
            for kind in PREFILTER_KINDS}

def gate_report_path(ch: Chapter) -> str:
    """Путь отчёта гейта главы: _prefilter/<stem>-gate.md."""
    stem = os.path.splitext(ch.file_name)[0]
    return os.path.join(AINOVELEDIT, "output", "_audit", "_prefilter",
                        f"{stem}-gate.md")

def _run_project_command(command: list[str]) -> int:
    """Запустить одну команду в AINovelEdit, показать вывод и код."""
    display = "python " + " ".join(command[1:])
    print(f"  $ {display}")
    try:
        process = subprocess.run(
            command,
            cwd=AINOVELEDIT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        print(f"  Не удалось запустить {command[1]}: {exc}")
        return 1
    stdout = (process.stdout or "").rstrip()
    if stdout:
        print("  --- stdout ---")
        for line in stdout.splitlines():
            print(f"  {line}")
    stderr = (process.stderr or "").rstrip()
    if stderr:
        print("  --- stderr ---")
        for line in stderr.splitlines():
            print(f"  {line}")
    print(f"  Код завершения: {process.returncode}")
    print()
    return process.returncode

def action_prefilter_run(ch: Chapter) -> int:
    """Прогнать механические предфильтры главы и сохранить отчёты.

    Техническое действие оркестратора: обновляет merged-зеркало и
    последовательно запускает сканеры с ``--report``. Отчёты кладутся в
    ``output/_audit/_prefilter/<глава>-{grammar,style,format,address,
    alignment}.md`` и служат эвиденсом фазы в меню полного прогона.
    Не создаёт LLM-промпт и не меняет текст главы (кроме merged-зеркала).
    """
    file_name = ch.file_name
    out_rel = f"output/{file_name}"
    commands = [
        [sys.executable, "scripts/update_merged.py", "--file", file_name],
        [sys.executable, "scripts/grammar_scan.py",
         "--file", file_name, "--report"],
        [sys.executable, "scripts/style_scan.py",
         "--file", out_rel, "--report"],
        [sys.executable, "scripts/format_scan.py",
         "--file", out_rel, "--report"],
        [sys.executable, "scripts/address_scan.py",
         "--file", file_name, "--report"],
        [sys.executable, "scripts/check_alignment.py",
         "--file", file_name, "--report"],
        [sys.executable, "scripts/check_records.py", "--file", file_name],
    ]
    print()
    separator("=")
    print(f"  Глава: {ch.chapter_id_full}")
    print()
    print("  Действие:")
    print(f"  {PREFILTER_ACTION_NAME}")
    print()
    print("  Команды (по порядку):")
    for command in commands:
        print(f"  $ python {' '.join(command[1:])}")
    print()
    print("  Назначение:")
    print("  прогнать механические предфильтры и сохранить отчёты.")
    print("  Не является LLM-аудитом; текст главы не меняется.")
    print()
    print("  Результат (файлы-эвиденсы):")
    for path in prefilter_report_paths(ch).values():
        print(f"  {os.path.relpath(path, ROOT)}")
    separator("=")
    print()

    codes = [_run_project_command(command) for command in commands]
    failed = sum(1 for code in codes if code != 0)
    print(f"  Итог: команд {len(codes)}, с ненулевым кодом: {failed}.")
    print()
    return 0 if failed == 0 else 1

def action_chapter_gate(ch: Chapter) -> int:
    """Гейт готовности главы: сверить обязательные входы по файлам-эвиденсам.

    Техническое действие оркестратора: запускает
    AINovelEdit/scripts/chapter_gate.py (блоки RU/JA, свежие предфильтры,
    смысловой аудит, отчёт аудита, открытые ``<!-- ??? -->``), печатает
    чек-лист и пишет отчёт в ``_prefilter/<глава>-gate.md``. Код 0 — глава
    готова; 1 — есть незакрытые пункты. LLM-промпт не создаётся.
    """
    script = "scripts/chapter_gate.py"
    command = [sys.executable, script, "--file", ch.file_name, "--report"]
    display = f"python {script} --file {ch.file_name} --report"
    print()
    separator("=")
    print(f"  Глава: {ch.chapter_id_full}")
    print()
    print("  Действие:")
    print(f"  {GATE_ACTION_NAME}")
    print()
    print("  Команда:")
    print(f"  {display}")
    print()
    print("  Назначение:")
    print("  сверить обязательные входы главы по файлам-эвиденсам.")
    print("  Код 0 — глава готова, 1 — есть незакрытые пункты.")
    print("  Не является LLM-аудитом; текст главы не меняется.")
    print()
    print("  Результат:")
    print(f"  {os.path.relpath(gate_report_path(ch), ROOT)}")
    separator("=")
    print()
    return _run_project_command(command)

# Действия показываются ТОЛЬКО в меню полного прогона главы (см.
# fullrun_pipeline); в главное меню и в меню смыслового аудита они не
# выводятся. Новое действие без пункта в fullrun_pipeline окажется
# недоступным — добавлять его туда же.
ACTIONS: list[ActionInfo] = [
    ActionInfo(
        "Omission Pre-check",
        "Детерминированная проверка пропусков перед A/B/C",
        action_omission_precheck,
    ),
    ActionInfo(
        PREFILTER_ACTION_NAME,
        "Обновить merged и прогнать предфильтры с сохранением отчётов",
        action_prefilter_run,
    ),
    ActionInfo(
        GATE_ACTION_NAME,
        "Чек-лист готовности главы по файлам-эвиденсам",
        action_chapter_gate,
    ),
]

# ============================================================================
# МЕНЮ (числовой ввод)
# ============================================================================
def visible_prompt_indices() -> list[int]:
    """Индексы PROMPTS в порядке вывода в ГЛАВНОМ меню.

    Разделы сортируются по GROUP_ORDER, внутри раздела сохраняется
    исходный порядок списка. Раздел «Смысловой аудит» в главное меню не
    выводится: его пункты живут в отдельном меню фаз (choose_audit_menu),
    где идут фиксированным пайплайном вместе с Omission Pre-check.
    """
    ordered = sorted(
        (i for i, p in enumerate(PROMPTS) if p.group in GROUP_ORDER),
        key=lambda i: (GROUP_ORDER.index(PROMPTS[i].group), i),
    )
    return [i for i in ordered if PROMPTS[i].group != GROUP_SMA]

def print_menu(ch: Chapter) -> None:
    """Вывести главное меню: разделы тем, разделы, навигация."""
    visible = visible_prompt_indices()
    print()
    print("AINovelEdit — оркестратор промптов")
    separator()
    print(f"  Текущая глава: {ch.chapter_id_full}")
    separator()
    number = 1
    for group in GROUP_ORDER:
        indices = [i for i in visible if PROMPTS[i].group == group]
        if not indices:
            continue
        print()
        print(f"=== {group} ===")
        print()
        for index in indices:
            prompt = PROMPTS[index]
            print(f"  {number:2d}. {prompt.title}")
            print(f"      {prompt.description}")
            print()
            number += 1
    print()
    print("=== Разделы ===")
    print()
    print(f"  {number:2d}. Смысловой аудит — меню фаз")
    print("      Pre-check → A → B → C → Фаза 1 → Фаза 2 (фиксированный порядок)")
    print()
    number += 1
    print(f"  {number:2d}. Полный прогон главы — меню фаз")
    print("      Перевод → предфильтры → смысловой аудит → аудиты → "
          "FINAL AUDIT → гейт")
    print()
    number += 1
    print("=== Навигация ===")
    print()
    print(f"  {number:2d}. Следующая глава")
    print(f"  {number + 1:2d}. Предыдущая глава")
    print(f"  {number + 2:2d}. Изменить том / главу")
    print(f"  {number + 3:2d}. Выход")
    print()

def choose_prompt(ch: Chapter) -> tuple[str, int] | str:
    """
    Запросить выбор пункта главного меню числом.

    Возвращает:
    ("prompt", i) — индекс i в PROMPTS (от 0)
    "audit"       — открыть меню смыслового аудита
    "fullrun"     — открыть меню полного прогона главы
    "next"        — следующая глава
    "prev"        — предыдущая глава
    "change"      — сменить главу
    "quit"        — выход
    """
    while True:
        print_menu(ch)
        raw = input("Введите номер: ").strip().lower()
        if raw in ("q", "quit", "exit", "выход"):
            return "quit"
        try:
            number = int(raw)
        except ValueError:
            print("  Введите число.")
            print()
            input("  Нажмите Enter...")
            continue

        visible = visible_prompt_indices()
        n_visible = len(visible)
        if 1 <= number <= n_visible:
            return ("prompt", visible[number - 1])
        if number == n_visible + 1:
            return "audit"
        if number == n_visible + 2:
            return "fullrun"
        base = n_visible + 2  # последний номер блока «Разделы»
        if number == base + 1:
            return "next"
        if number == base + 2:
            return "prev"
        if number == base + 3:
            return "change"
        if number == base + 4:
            return "quit"

        print(f"  Введите число от 1 до {base + 4}.")
        print()
        input("  Нажмите Enter...")

# ---------------------------------------------------------------------------
# МЕНЮ СМЫСЛОВОГО АУДИТА (отдельный режим: фиксированный порядок фаз)
# ---------------------------------------------------------------------------
def audit_pipeline() -> list[tuple[str, int]]:
    """Фиксированный порядок этапов смыслового аудита.

    Возвращает пары ("action" | "prompt", индекс в ACTIONS / PROMPTS):
    Omission Pre-check → Auditor A → Auditor B → Pragmatic Auditor C →
    Фаза 1 (blind) → Фаза 2 (evidence review).
    """
    steps: list[tuple[str, int]] = []
    for index, action in enumerate(ACTIONS):
        if action.name == "Omission Pre-check":
            steps.append(("action", index))
    for generator in (prompt_semantic_a, prompt_semantic_b, prompt_pragmatic_c,
                      prompt_semantic_analyzer_phase1, prompt_semantic_analyzer):
        for index, prompt in enumerate(PROMPTS):
            if prompt.generator is generator:
                steps.append(("prompt", index))
                break
    return steps

def audit_stage_index(kind: str, index: int) -> int | None:
    """Номер этапа в audit_pipeline() для пары (kind, index); None — вне пайплайна."""
    for stage, (step_kind, step_index) in enumerate(audit_pipeline()):
        if step_kind == kind and step_index == index:
            return stage
    return None

def next_prompt_index(current: int) -> int | None:
    """Индекс следующего промпта в рамках того же раздела; None — конец раздела."""
    group = PROMPTS[current].group
    for index in range(current + 1, len(PROMPTS)):
        if PROMPTS[index].group == group:
            return index
    return None

def _audit_stage_status(kind: str, index: int, ch: Chapter) -> str:
    """Статус этапа в меню: сколько запусков этой фазы уже сделано."""
    if kind == "action":
        return "evidence: есть" if sma_precheck_exists(ch) else "evidence: нет"
    generator = PROMPTS[index].generator
    if generator is prompt_semantic_a:
        return f"запусков: {len(sma_existing_runs(ch, 'a'))}"
    if generator is prompt_semantic_b:
        return f"запусков: {len(sma_existing_runs(ch, 'b'))}"
    if generator is prompt_pragmatic_c:
        return f"запусков: {len(sma_existing_runs(ch, 'c'))}"
    if generator is prompt_semantic_analyzer_phase1:
        return f"файлов Фазы 1: {len(sma_existing_phase1_runs(ch))}"
    if generator is prompt_semantic_analyzer:
        return f"результатов Фазы 2: {len(sma_existing_runs(ch, 'analysis'))}"
    return ""

def print_audit_menu(ch: Chapter, stage: int) -> int:
    """Вывести меню смыслового аудита; вернуть число пунктов-этапов."""
    steps = audit_pipeline()
    print()
    print("AINovelEdit — смысловой аудит (фиксированный порядок фаз)")
    separator()
    print(f"  Текущая глава: {ch.chapter_id_full}")
    if 0 <= stage < len(steps):
        kind, index = steps[stage]
        title = ACTIONS[index].name if kind == "action" else PROMPTS[index].title
        print(f"  Текущий этап: {title}")
    separator()
    print()
    for position, (kind, index) in enumerate(steps, start=1):
        title = ACTIONS[index].name if kind == "action" else PROMPTS[index].title
        marker = "->" if position - 1 == stage else "  "
        print(f"  {marker} {position:2d}. {title}")
        print(f"           {_audit_stage_status(kind, index, ch)}")
    count = len(steps)
    print()
    print(f"  {count + 1:2d}. Следующий этап")
    print(f"  {count + 2:2d}. Следующая глава")
    print(f"  {count + 3:2d}. Предыдущая глава")
    print(f"  {count + 4:2d}. Изменить том / главу")
    print(f"  {count + 5:2d}. Назад в главное меню")
    print()
    return count

def choose_audit_menu(ch: Chapter, stage: int) -> tuple[str, int] | str:
    """
    Меню смыслового аудита: этапы идут фиксированным пайплайном.

    Возвращает:
    ("prompt", i) / ("action", i) — выбранный напрямую этап;
    ("stage", n)                  — «Следующий этап» (n — новый номер);
    "next" / "prev" / "change"    — навигация по главам;
    "back"                        — назад в главное меню.

    Прямой выбор любого этапа разрешён: при отсутствии обязательных входов
    (файл Фазы 1, запуски A/B/C) перед подтверждением выводится
    предупреждение (audit_prereq_warning), но переход не блокируется.
    """
    steps = audit_pipeline()
    while True:
        count = print_audit_menu(ch, stage)
        raw = input("Введите номер: ").strip().lower()
        if raw in ("q", "quit", "exit", "выход"):
            return "back"
        try:
            number = int(raw)
        except ValueError:
            print("  Введите число.")
            print()
            input("  Нажмите Enter...")
            continue

        if 1 <= number <= count:
            return steps[number - 1]
        if number == count + 1:
            if stage + 1 >= len(steps):
                print("  Это последний этап пайплайна.")
                print()
                input("  Нажмите Enter...")
                continue
            return ("stage", stage + 1)
        if number == count + 2:
            return "next"
        if number == count + 3:
            return "prev"
        if number == count + 4:
            return "change"
        if number == count + 5:
            return "back"

        print(f"  Введите число от 1 до {count + 5}.")
        print()
        input("  Нажмите Enter...")

# ---------------------------------------------------------------------------
# МЕНЮ ПОЛНОГО ПРОГОНА ГЛАВЫ (пофазовый порядок «от перевода до проверки»)
# ---------------------------------------------------------------------------
# Образец поведения — меню смыслового аудита (выше): фиксированный порядок
# фаз, статусы по файлам-эвиденсам ([x]/[ ]), prereq-предупреждения при
# переходе к фазе без обязательных входов.

_AUDIT_SECTION_PATTERNS = {
    # Заголовки секций в output/_audit/vXX-chYY.md встречаются в разных
    # формулировках («## 5. Грамматический контроль», «## Грамматика»,
    # «### Итог GRAMMAR: ЧИСТО») — матчер толерантный, но без re.I по
    # латинице, чтобы «grammar_scan» в тексте заголовка не считался секцией.
    prompt_grammar_audit: re.compile(
        r"^#{2,4}[^\n]*(?:Граммати|ГРАММАТИ|\bGRAMMAR\b)", re.MULTILINE),
    prompt_style_audit: re.compile(
        r"^#{2,4}[^\n]*(?:Стил|\bSTYLE\b)", re.MULTILINE),
    prompt_humanizer: re.compile(
        r"^#{2,4}[^\n]*(?:[Hh]umanizer|[Мм]ашинност)", re.MULTILINE),
}

def fullrun_pipeline() -> list[tuple[str, int]]:
    """Фиксированный порядок полного прогона главы «от перевода до проверки».

    Возвращает пары ("action" | "prompt", индекс в ACTIONS / PROMPTS):
    Первый запуск → Продолжение (заполнение/перевод) → предфильтры →
    смысловой аудит целиком (audit_pipeline: Pre-check → A → B → C →
    Фаза 1 → Фаза 2) → грамматический → стилевой → humanizer →
    FINAL AUDIT → гейт готовности главы.
    """
    steps: list[tuple[str, int]] = []

    def add_prompt(generator) -> None:
        for index, prompt in enumerate(PROMPTS):
            if prompt.generator is generator:
                steps.append(("prompt", index))
                return
        raise AssertionError(f"нет промпта-пункта для {generator!r}")

    def add_action(name: str) -> None:
        for index, action in enumerate(ACTIONS):
            if action.name == name:
                steps.append(("action", index))
                return
        raise AssertionError(f"нет действия {name!r}")

    add_prompt(prompt_first_launch)
    add_prompt(prompt_continue)
    add_action(PREFILTER_ACTION_NAME)
    steps.extend(audit_pipeline())
    add_prompt(prompt_grammar_audit)
    add_prompt(prompt_style_audit)
    add_prompt(prompt_humanizer)
    add_prompt(prompt_full_audit)
    add_action(GATE_ACTION_NAME)
    return steps

def fullrun_stage_index(kind: str, index: int) -> int | None:
    """Номер фазы в fullrun_pipeline() для пары (kind, index); None — вне."""
    for stage, (step_kind, step_index) in enumerate(fullrun_pipeline()):
        if step_kind == kind and step_index == index:
            return stage
    return None

def fullrun_next_step(kind: str, index: int) -> tuple[str, int] | None:
    """Следующая фаза полного прогона; None — текущая фаза последняя."""
    steps = fullrun_pipeline()
    stage = fullrun_stage_index(kind, index)
    if stage is None or stage + 1 >= len(steps):
        return None
    return steps[stage + 1]

# --- файлы-эвиденсы фаз ----------------------------------------------------
def _mtime(path: str) -> float | None:
    try:
        return os.path.getmtime(path)
    except OSError:
        return None

def _is_fresh(report: str, source: str) -> bool:
    """Отчёт не старее источника (оба файла существуют, report >= source)."""
    report_mtime = _mtime(report)
    source_mtime = _mtime(source)
    return (report_mtime is not None
            and source_mtime is not None
            and report_mtime >= source_mtime)

def _stamp(path: str) -> str:
    mtime = _mtime(path)
    if mtime is None:
        return "—"
    return datetime.fromtimestamp(mtime).strftime("%d.%m %H:%M")

def _fill_evidence(ch: Chapter) -> tuple[bool, str]:
    """Заполнение/перевод: output-файл и покрытие JA-блоков RU-блоками."""
    if not os.path.isfile(ch.output_path):
        return False, "нет output-файла (глава не начата)"
    ja_blocks, ru_blocks = sma_block_inventory(ch)
    if not ja_blocks:
        return True, "output-файл есть (нумерация блоков недоступна)"
    done = set(ru_blocks) >= set(ja_blocks)
    return done, f"блоков RU/JA: {len(ru_blocks)}/{len(ja_blocks)}"

def _prefilter_evidence(ch: Chapter) -> tuple[bool, str]:
    """Предфильтры: отчёты 5 сканеров существуют и не старее текста."""
    paths = prefilter_report_paths(ch)
    if not os.path.isfile(ch.output_path):
        return False, "нет output-файла"
    existing = [kind for kind, path in paths.items() if os.path.isfile(path)]
    fresh = [kind for kind in existing
             if _is_fresh(paths[kind], ch.output_path)]
    done = len(existing) == len(paths) and len(fresh) == len(paths)
    return done, (f"отчётов: {len(existing)}/{len(paths)}, "
                  f"свежих: {len(fresh)}")

def _audit_text(ch: Chapter) -> str | None:
    try:
        with open(ch.audit_path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None

def _audit_section_evidence(ch: Chapter, generator) -> tuple[bool, str]:
    """Секция фазы (грамматика/стиль/humanizer) в отчёте аудита, свежая."""
    text = _audit_text(ch)
    if text is None:
        return False, "отчёта аудита нет"
    if not _AUDIT_SECTION_PATTERNS[generator].search(text):
        return False, "секции фазы нет в отчёте аудита"
    if not _is_fresh(ch.audit_path, ch.output_path):
        return False, (f"секция есть, отчёт УСТАРЕЛ "
                       f"({_stamp(ch.audit_path)}) — текст правился позже")
    return True, f"секция в отчёте есть (отчёт {_stamp(ch.audit_path)})"

def _final_audit_evidence(ch: Chapter) -> tuple[bool, str]:
    """FINAL AUDIT: отчёт аудита существует и не старее текста главы."""
    if not os.path.isfile(ch.audit_path):
        return False, "отчёта аудита нет"
    if not _is_fresh(ch.audit_path, ch.output_path):
        return False, (f"отчёт УСТАРЕЛ ({_stamp(ch.audit_path)}) — "
                       "текст правился после аудита")
    return True, f"отчёт свежий ({_stamp(ch.audit_path)})"

def _gate_evidence(ch: Chapter) -> tuple[bool, str]:
    """Гейт: отчёт гейта существует и не старее текста главы."""
    report = gate_report_path(ch)
    if not os.path.isfile(report):
        return False, "гейт не запускался"
    if not _is_fresh(report, ch.output_path):
        return False, (f"гейт-отчёт УСТАРЕЛ ({_stamp(report)}) — "
                       "текст правился после гейта")
    return True, f"гейт-отчёт свежий ({_stamp(report)})"

def fullrun_stage_evidence(kind: str, index: int, ch: Chapter) -> tuple[bool, str]:
    """Факт выполнения фазы полного прогона: (выполнено, описание эвиденса).

    Статусы считаются только по файлам-эвиденсам (отчёты предфильтров,
    run-файлы SMA, отчёт аудита, гейт-отчёт), а не по пометкам пользователя.
    """
    if kind == "action":
        name = ACTIONS[index].name
        if name == "Omission Pre-check":
            exists = sma_precheck_exists(ch)
            return exists, "evidence pre-check: " + ("есть" if exists else "нет")
        if name == PREFILTER_ACTION_NAME:
            return _prefilter_evidence(ch)
        if name == GATE_ACTION_NAME:
            return _gate_evidence(ch)
        return False, "эвиденс фазы не задан"

    generator = PROMPTS[index].generator
    if generator is prompt_first_launch:
        exists = os.path.isfile(ch.output_path)
        return exists, ("output-файл есть (глава начата)" if exists
                        else "нет output-файла (глава не начата)")
    if generator is prompt_continue:
        return _fill_evidence(ch)
    if generator is prompt_semantic_a:
        count = len(sma_existing_runs(ch, "a"))
        return count > 0, f"запусков A: {count}"
    if generator is prompt_semantic_b:
        count = len(sma_existing_runs(ch, "b"))
        return count > 0, f"запусков B: {count}"
    if generator is prompt_pragmatic_c:
        count = len(sma_existing_runs(ch, "c"))
        return count > 0, f"запусков C: {count}"
    if generator is prompt_semantic_analyzer_phase1:
        count = len(sma_existing_phase1_runs(ch))
        return count > 0, f"файлов Фазы 1: {count}"
    if generator is prompt_semantic_analyzer:
        count = len(sma_existing_runs(ch, "analysis"))
        return count > 0, f"результатов Фазы 2: {count}"
    if generator in _AUDIT_SECTION_PATTERNS:
        return _audit_section_evidence(ch, generator)
    if generator is prompt_full_audit:
        return _final_audit_evidence(ch)
    return False, "эвиденс фазы не задан"

def fullrun_stage_status(kind: str, index: int, ch: Chapter) -> str:
    """Строка статуса фазы: галочка выполнения + описание эвиденса."""
    done, detail = fullrun_stage_evidence(kind, index, ch)
    return f"[{'x' if done else ' '}] {detail}"

def fullrun_prereq_warnings(item: PromptInfo | ActionInfo,
                            ch: Chapter) -> list[str]:
    """Обязательные входы фаз полного прогона (для экрана подтверждения).

    Дополняет audit_prereq_warning (он проверяет только Фазы 1/2): текст
    главы для предфильтров, аудитов и гейта; свежие предфильтры и результаты
    смыслового аудита — для FINAL AUDIT. Пустой список — входы в порядке.
    """
    warnings: list[str] = []
    output_exists = os.path.isfile(ch.output_path)

    if isinstance(item, ActionInfo):
        if item.name in (PREFILTER_ACTION_NAME, GATE_ACTION_NAME) \
                and not output_exists:
            warnings.append(
                "НЕТ OUTPUT-ФАЙЛА: нечего сканировать и проверять — сначала "
                "переведи и сохрани хотя бы один блок (save_block.py).")
        return warnings

    audit_gens = (prompt_grammar_audit, prompt_style_audit,
                  prompt_humanizer, prompt_full_audit)
    if item.generator in audit_gens and not output_exists:
        warnings.append(
            "НЕТ OUTPUT-ФАЙЛА: аудит работает по сохранённому тексту — "
            "сначала заполни главу (фазы «Первый запуск» / «Продолжение»).")
    if item.generator is prompt_full_audit and output_exists:
        stale = [kind for kind, path in prefilter_report_paths(ch).items()
                 if not _is_fresh(path, ch.output_path)]
        if stale:
            warnings.append(
                f"ПРЕДФИЛЬТРЫ НЕ СВЕЖИ ({len(stale)}/{len(PREFILTER_KINDS)}: "
                + ", ".join(stale) + "): прогони фазу «"
                + PREFILTER_ACTION_NAME + "» — иначе финальный аудит "
                "опирается на устаревшие выгрузки.")
        if not sma_existing_runs(ch, "analysis"):
            warnings.append(
                "СМЫСЛОВОЙ АУДИТ НЕ ЗАВЕРШЁН: в analysis/ нет ни одного "
                "результата Фазы 2 — финальный аудит пойдёт без смыслового "
                "слоя (сначала фазы меню смыслового аудита).")
    return warnings

def fullrun_evidence_note(item: PromptInfo | ActionInfo,
                          ch: Chapter) -> str | None:
    """Описание файлов-эвиденсов выбранной фазы — для подтверждения запуска."""
    for kind, index in fullrun_pipeline():
        if (kind == "action" and ACTIONS[index] is item) \
                or (kind == "prompt" and PROMPTS[index] is item):
            _done, detail = fullrun_stage_evidence(kind, index, ch)
            return f"Эвиденс фазы: {detail}"
    return None

def print_fullrun_menu(ch: Chapter, stage: int) -> int:
    """Вывести меню полного прогона главы; вернуть число пунктов-фаз."""
    steps = fullrun_pipeline()
    print()
    print("AINovelEdit — полный прогон главы (от перевода до проверки)")
    separator()
    print(f"  Текущая глава: {ch.chapter_id_full}")
    if 0 <= stage < len(steps):
        kind, index = steps[stage]
        title = ACTIONS[index].name if kind == "action" else PROMPTS[index].title
        print(f"  Текущая фаза: {title}")
    separator()
    print()
    for position, (kind, index) in enumerate(steps, start=1):
        title = ACTIONS[index].name if kind == "action" else PROMPTS[index].title
        marker = "->" if position - 1 == stage else "  "
        print(f"  {marker} {position:2d}. {title}")
        print(f"           {fullrun_stage_status(kind, index, ch)}")
    count = len(steps)
    print()
    print(f"  {count + 1:2d}. Следующая фаза")
    print(f"  {count + 2:2d}. Следующая глава")
    print(f"  {count + 3:2d}. Предыдущая глава")
    print(f"  {count + 4:2d}. Изменить том / главу")
    print(f"  {count + 5:2d}. Назад в главное меню")
    print()
    return count

def choose_fullrun_menu(ch: Chapter, stage: int) -> tuple[str, int] | str:
    """
    Меню полного прогона главы: фазы идут фиксированным пайплайном.

    Возвращает:
    ("prompt", i) / ("action", i) — выбранная напрямую фаза;
    ("stage", n)                  — «Следующая фаза» (n — новый номер);
    "next" / "prev" / "change"    — навигация по главам;
    "back"                        — назад в главное меню.

    Прямой выбор любой фазы разрешён: при отсутствии обязательных входов
    (output-файл, свежие предфильтры, результаты Фазы 2) перед
    подтверждением выводится предупреждение (fullrun_prereq_warnings), но
    переход не блокируется.
    """
    steps = fullrun_pipeline()
    while True:
        count = print_fullrun_menu(ch, stage)
        raw = input("Введите номер: ").strip().lower()
        if raw in ("q", "quit", "exit", "выход"):
            return "back"
        try:
            number = int(raw)
        except ValueError:
            print("  Введите число.")
            print()
            input("  Нажмите Enter...")
            continue

        if 1 <= number <= count:
            return steps[number - 1]
        if number == count + 1:
            if stage + 1 >= len(steps):
                print("  Это последняя фаза пайплайна.")
                print()
                input("  Нажмите Enter...")
                continue
            return ("stage", stage + 1)
        if number == count + 2:
            return "next"
        if number == count + 3:
            return "prev"
        if number == count + 4:
            return "change"
        if number == count + 5:
            return "back"

        print(f"  Введите число от 1 до {count + 5}.")
        print()
        input("  Нажмите Enter...")

# ============================================================================
# DISPATCH: PROMPT vs ACTION
# ============================================================================
def run_action(action: ActionInfo, ch: Chapter) -> int:
    """Выполнить техническое действие оркестратора; вернуть код завершения."""
    return action.execute(ch)

def dispatch_selection(selection, ch: Chapter):
    """Разделить выбор меню на prompt и action.

    Возвращает:
    ("prompt", PromptInfo) | ("action", ActionInfo) | None.

    None — выбор не относится к PROMPTS/ACTIONS (навигация
    обрабатывается вызывающим кодом до этого вызова).
    """
    if not (isinstance(selection, tuple) and len(selection) == 2):
        return None
    kind, index = selection
    if kind == "prompt":
        return ("prompt", PROMPTS[index])
    if kind == "action":
        return ("action", ACTIONS[index])
    return None

# ============================================================================
# ПОДТВЕРЖДЕНИЕ
# ============================================================================
def audit_prereq_warning(item: PromptInfo | ActionInfo, ch: Chapter) -> str | None:
    """Предупреждение при переходе напрямую к этапу без обязательных входов.

    Возвращает текст предупреждения или None. Проверяются только реально
    обязательные входы: Фазе 2 нужен файл слепой Фазы 1 и хоть один запуск
    A/B/C; Фазе 1 ничего не нужно (blind), но наличие прошлых слепых выводов
    стоит показать — при нескольких прогонах Фаза 2 возьмёт самый свежий.
    """
    if not isinstance(item, PromptInfo):
        return None
    if item.generator is prompt_semantic_analyzer:
        phase1_files = sma_phase1_files(ch)
        if not phase1_files:
            return (
                "ФАЗА 1 НЕ ВЫПОЛНЯЛАСЬ: в "
                f"{SMA_REL_ROOT}/{sma_chapter_id(ch)}/analysis/ нет ни одного "
                "<id>.phase1.json — задание Фазы 2 потребует STOP и работать "
                "не будет. Сначала «Фаза 1 (blind)», после неё — заново "
                "сгенерированная Фаза 2."
            )
        if not any(sma_existing_runs(ch, kind) for kind in ("a", "b", "c")):
            return (
                "НЕТ НИ ОДНОГО ЗАПУСКА A / B / C: задание Фазы 2 остановится "
                "с сообщением «в a/, b/ и c/ нет ни одного <run_id>.json». "
                "Сначала Omission Pre-check и аудиторы A / B (/ C)."
            )
    if item.generator is prompt_semantic_analyzer_phase1:
        existing = sma_phase1_files(ch)
        if existing:
            return (
                f"УЖЕ ЕСТЬ {len(existing)} слепых вывод(а) Фазы 1: этот запуск "
                "добавит ещё один, и Фаза 2 по умолчанию возьмёт самый свежий "
                "файл (см. inputs.phase1)."
            )
    return None

def audit_existing_runs_note(item: PromptInfo | ActionInfo, ch: Chapter) -> str | None:
    """Идентификаторы прошлых запусков этапа — для отслеживания фаз.

    Показывается в экране подтверждения: какие run_id уже есть у этой фазы
    и сколько их. None — если этап не относится к смысловому аудиту.
    """
    if not isinstance(item, PromptInfo):
        return None
    if item.generator is prompt_semantic_a:
        ids, label = sma_existing_runs(ch, "a"), "Auditor A"
    elif item.generator is prompt_semantic_b:
        ids, label = sma_existing_runs(ch, "b"), "Auditor B"
    elif item.generator is prompt_pragmatic_c:
        ids, label = sma_existing_runs(ch, "c"), "Pragmatic Auditor C"
    elif item.generator is prompt_semantic_analyzer_phase1:
        ids, label = sma_existing_phase1_runs(ch), "Фаза 1 (blind)"
    elif item.generator is prompt_semantic_analyzer:
        ids, label = sma_existing_runs(ch, "analysis"), "Фаза 2 (analysis)"
    else:
        return None
    if not ids:
        return f"Прошлые запуски ({label}): нет"
    shown = ", ".join(ids[-8:])
    more = "" if len(ids) <= 8 else f" … (+{len(ids) - 8} ранее)"
    return f"Прошлые запуски ({label}), всего {len(ids)}: {shown}{more}"

def ask_confirmation(
    item: PromptInfo | ActionInfo,
    ch: Chapter,
    notes: list[str] | None = None,
) -> bool | str:
    """
    Показать описание режима (PromptInfo) или действия (ActionInfo) и спросить
    подтверждение — одинаковый диалог для обоих случаев.
    ``notes`` — предупреждения (пропущенные входы фазы, идентификаторы
    прошлых запусков); печатаются перед разделителем.
    Возвращает True (да), False (нет), "next" (следующая), "prev" (предыдущая).
    """
    is_action = isinstance(item, ActionInfo)
    title = item.name if is_action else item.title
    print()
    print("Подтверждение запуска")
    separator()
    print()
    print(f"  {'Действие' if is_action else 'Режим'}: {title}")
    print(f"  Глава: {ch.chapter_id_full}")
    print()
    print("  Кратко:")
    print_wrapped(item.description, indent="    ")
    if not is_action:
        print()
        print("  Что делает этот режим:")
        print_wrapped(item.guide, indent="    ")
    if notes:
        print()
        print("  Предупреждения:")
        for note in notes:
            print_wrapped(note, indent="    ")
            print()
    print()
    separator()
    print()
    while True:
        raw = input(
            f'Запустить "{title}" для {ch.chapter_id_full}? '
            "(1 — да, 2 — нет, 3 — след. глава, 4 — пред. глава): "
        ).strip()
        if raw == "1":
            return True
        if raw in ("2", "q", "n", "нет"):
            return False
        if raw == "3":
            return "next"
        if raw == "4":
            return "prev"
        print("  Введите 1, 2, 3 или 4.")

# ============================================================================
# ГЕНЕРАЦИЯ ПРОМПТА
# ============================================================================
def generate_prompt(
    prompt_index: int,
    ch: Chapter,
) -> str | None:
    """Сгенерировать выбранный промпт."""
    prompt = PROMPTS[prompt_index]
    if prompt.generator is not None:
        return prompt.generator(ch)

    # Промпт без собственного генератора: «Обработка одного блока».
    # Раньше здесь был хардкод prompt_index == 8 — он ломался при любом
    # добавлении/удалении пунктов меню.
    print()
    print(prompt.title)
    separator()
    print()
    print(f"  Том:   {ch.volume_id}")
    print(f"  Глава: {ch.chapter_id}")
    print()
    block_number = ask_block_number()
    return prompt_one_block(ch, block_number)

# ============================================================================
# ПОКАЗ ГОТОВОГО ПРОМПТА
# ============================================================================
def show_generated_prompt(
    prompt_text: str,
    prompt: PromptInfo,
    ch: Chapter,
) -> None:
    """Показать полностью сгенерированный промпт."""
    print()
    separator("=")
    print()
    print(f"  Режим: {prompt.title}")
    print(f"  Глава: {ch.chapter_id_full}")
    print()
    separator("=")
    print()
    print(prompt_text)
    print()
    separator("=")
    print()
    input("  Нажмите Enter для возврата...")

# ============================================================================
# КОПИРОВАНИЕ
# ============================================================================
def copy_to_clipboard(text: str) -> bool:
    """
    Копирует Unicode-текст в буфер обмена Windows.
    Использует PowerShell и .NET напрямую, без передачи
    русского текста через кодировку консоли.
    """
    if sys.platform != "win32":
        return False
    try:
        encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
        command = (
            "$bytes = [Convert]::FromBase64String('"
            + encoded
            + "'); "
            "$text = [System.Text.Encoding]::UTF8.GetString($bytes); "
            "Set-Clipboard -Value $text"
        )
        process = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                command,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return process.returncode == 0
    except Exception:
        return False

# ============================================================================
# СОХРАНЕНИЕ В ФАЙЛ
# ============================================================================
def prompt_file_name(ch: Chapter, prompt: PromptInfo) -> str:
    """Путь к файлу промпта относительно корня проекта.

    ``agent_prompts/agent_prompt.<глава>.<слаг режима>.md`` — отдельная
    папка, чтобы корень проекта не засорялся файлами (глава × режим).
    Общий agent_prompt.md затирался при параллельной работе нескольких
    терминалов (в том числе на середине записи), поэтому у каждого режима
    и главы своё имя. Слаг берётся из PromptInfo.slug.
    """
    return (f"{PROMPT_DIR_NAME}/{PROMPT_FILE_PREFIX}."
            f"{sma_chapter_id(ch)}.{prompt.slug}.md")

def prompt_file_path(ch: Chapter, prompt: PromptInfo) -> str:
    """Абсолютный путь файла промпта (папка создаётся при записи)."""
    return os.path.join(ROOT, *prompt_file_name(ch, prompt).split("/"))

def prompt_run_id(prompt_text: str) -> str | None:
    """Достать audit_run_id (или analysis_id) из сгенерированного промпта.

    Возвращает run_id без суффикса .phase1, либо None, если промпт
    смыслового аудита такого идентификатора не содержит. Суффикс
    .phase1 отрезается: в самой фазе у Фазы 2 свой analysis_id, а
    отслеживать нужно тот, что упомянут в задании.
    """
    match = re.search(r'"(?:audit_run_id|analysis_id)"\s*:\s*"([^"]+)"', prompt_text)
    if not match:
        return None
    value = match.group(1)
    return value[: -len(".phase1")] if value.endswith(".phase1") else value

def save_prompt_to_file(
    prompt_text: str,
    prompt: PromptInfo,
    ch: Chapter,
) -> str | None:
    """
    Сохранить готовый промпт в markdown-файл в папке agent_prompts/.

    Имя файла: agent_prompts/agent_prompt.<глава>.<слаг>.md (см.
    prompt_file_name) — так параллельные терминалы и разные режимы не
    затирают чужие задания, а корень проекта остаётся чистым.
    Папка создаётся автоматически. Запись атомарная: сначала временный
    файл рядом с целью, затем os.replace — читатель не увидит
    полузаписанный файл, а Ctrl+C не оставит обрезанный промпт.
    Возвращает путь к файлу (относительно корня) либо None при ошибке.
    """
    path = prompt_file_path(ch, prompt)
    header = (
        "# Промпт-инструкция для агента\n"
        "\n"
        f"- Режим: {prompt.title}\n"
        f"- Глава: {ch.chapter_id_full}\n"
        f"- Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        "- Источник: tools/agent_workflow.py\n"
        "\n"
        "---\n"
        "\n"
    )
    tmp_name = f"{path}.{os.getpid()}.tmp"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(tmp_name, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(header + prompt_text + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, path)
    except OSError:
        try:
            if os.path.exists(tmp_name):
                os.remove(tmp_name)
        except OSError:
            pass
        return None
    return prompt_file_name(ch, prompt)

def print_generation_summary(
    prompt_text: str,
    prompt: PromptInfo,
    ch: Chapter,
) -> str | None:
    """
    Печать итогов генерации: режим, глава, буфер обмена, файл, audit_run_id.

    audit_run_id печатается всегда, когда он есть в тексте — без этого
    идентификатор запуска терялся (он был только внутри промпта), и фазы
    аудита невозможно было отслеживать после генерации.
    Возвращает имя файла (None — не сохранено).
    """
    print()
    separator()
    print()
    print(f"  Режим: {prompt.title}")
    print(f"  Глава: {ch.chapter_id_full}")
    print()
    if copy_to_clipboard(prompt_text):
        print("  Промпт скопирован в буфер обмена.")
        print("  Внимание: буфер обмена один на все терминалы — параллельные")
        print("  копирования затирают друг друга.")
    else:
        print("  Не удалось скопировать промпт автоматически.")
    file_name = save_prompt_to_file(prompt_text, prompt, ch)
    if file_name:
        print(f"  Промпт сохранён в файл: {file_name}")
        print(f"  На него можно сослаться в задаче агенту: {file_name}")
    else:
        print(f"  Не удалось сохранить промпт в {prompt_file_name(ch, prompt)}.")
    run_id = prompt_run_id(prompt_text)
    if run_id:
        print(f"  audit_run_id: {run_id}")
    print()
    separator()
    return file_name

# ============================================================================
# SELF-TEST SMA (dry-run: ничего не пишет на диск, перевод не меняет)
# ============================================================================
# Запрещённые подстроки: сигнализируют об утечке чужого контекста в prompt A/B/C.
_SMA_FORBIDDEN_A = (
    "semantic-audit-b", "sma-b", "-sma-b", "/b/", "\\b\\", "analysis/",
    "Auditor B", "аудитор B", "результаты B", "результат B", "B findings",
    "B report", "-sma-a.json", "-sma-b.json", "sma-merged", "manual-sma",
    "_audit/v",
)
_SMA_FORBIDDEN_B = (
    "semantic-audit-a", "sma-a", "-sma-a", "/a/", "\\a\\", "analysis/",
    "Auditor A", "аудитор A", "результаты A", "результат A", "A findings",
    "A report", "-sma-a.json", "-sma-b.json", "sma-merged", "manual-sma",
    "_audit/v",
)
# Pragmatic Auditor C изолирован от A, B и Analyzer: в его задании не должно
# быть ни имён/путей других аудиторов, ни их результатов, ни Analyzer.
_SMA_FORBIDDEN_C = (
    "semantic-audit-a", "semantic-audit-b",
    "sma-a", "sma-b", "-sma-a", "-sma-b",
    "/a/", "/b/", "\\a\\", "\\b\\", "analysis/",
    "Auditor A", "Auditor B", "аудитор A", "аудитор B",
    "результаты A", "результаты B", "результат A", "результат B",
    "A findings", "B findings", "A report", "B report",
    "a_runs", "b_runs", "sources.a", "sources.b",
    "Analyzer", "анализатор",
    "-sma-a.json", "-sma-b.json", "sma-merged", "manual-sma", "_audit/v",
)
# Инструменты обхода каталогов — в задании A/B/C их быть не должно.
_SMA_SEARCH_TOOLS = ("Get-ChildItem", "os.listdir", "Select-String", "grep ")
# Путь вида .../_audit/sma/<chapter>/<kind>/...
_SMA_PATH_RE = re.compile(r"_audit[\\/]+sma[\\/]+[^\\/\s\"']+[\\/]+([a-z]+)[\\/]")
# Имя подпапки/файла сразу после output/_audit/
_SMA_AUDIT_CHILD_RE = re.compile(r"_audit[\\/]+([A-Za-z0-9_.-]+)")

def _sma_path_kinds(prompt: str) -> set[str]:
    """Множество типов (<a|b|c|analysis>) в путях output/_audit/sma/ промпта."""
    return set(_SMA_PATH_RE.findall(prompt))

def _sma_audit_children(prompt: str) -> set[str]:
    """Что упомянуто сразу после output/_audit/ (для проверки утечек)."""
    return set(_SMA_AUDIT_CHILD_RE.findall(prompt))

def _sma_hits(prompt: str, needles) -> list[str]:
    """Подстроки из needles, найденные в prompt (для отчёта self-test)."""
    return [n for n in needles if n in prompt]

def _sma_json_field(prompt: str, field: str) -> str:
    """Значение строкового поля в JSON-шаблоне промпта (для self-test)."""
    match = re.search(rf'"{re.escape(field)}":\s*"([^"]+)"', prompt)
    return match.group(1) if match else ""

def _sma_checks_a(ch: Chapter, pa1: str, pa2: str) -> list[tuple[str, bool, str]]:
    """Проверки изоляции prompt Auditor A (пары имя/ok/деталь)."""
    chap = sma_chapter_id(ch)
    run_id_1 = _sma_json_field(pa1, "audit_run_id")
    run_id_2 = _sma_json_field(pa2, "audit_run_id")
    own_path = f"{SMA_REL_ROOT}/{chap}/a/{run_id_1}.json"
    old_name = re.compile(rf"{re.escape(chap)}-sma-[ab]")
    leak = _sma_hits(pa1, _SMA_FORBIDDEN_A)
    kinds = _sma_path_kinds(pa1)
    children = _sma_audit_children(pa1)
    return [
        ("A: mentions B — NO",
         not leak,
         f"утечки: {leak}" if leak else "упоминаний второго аудитора нет"),
        ("A: mentions B results — NO",
         not _sma_hits(pa1, ("результаты B", "результат B", "B findings", "B report")),
         ""),
        ("A: mentions old audit results — NO",
         not (old_name.search(pa1) or _sma_hits(
             pa1, ("-sma-a.json", "-sma-b.json", "sma-merged", "manual-sma"))),
         ""),
        ("A: mentions output/_audit old reports — NO",
         children == {"sma"},
         f"под output/_audit/: {sorted(children)}"),
        ("A: has own output path — YES",
         own_path in pa1,
         own_path),
        ("A: has unique audit_run_id — YES",
         bool(run_id_1) and run_id_1 != run_id_2 and pa1 != pa2,
         f"{run_id_1} / повторный запуск: {run_id_2}"),
        ("A: own output path ведёт только в папку a/ — YES",
         kinds == {"a"},
         f"типы путей в промпте: {sorted(kinds)}"),
        ("A: автономность и единственность файла зафиксированы — YES",
         SMA_AUTONOMY_NOTE in pa1 and SMA_OWN_FILE_NOTE in pa1,
         ""),
        ("A: OWN SKILL разрешён (противоречие с autonomy снято) — YES",
         "OWN SKILL" in pa1
         and "AINovelEdit/.agents/skills/semantic-audit-a/SKILL.md" in pa1
         and SMA_FORBIDDEN_INPUTS_NOTE in pa1,
         ""),
        ("A: иерархия JA authoritative / RU under review / EN reference only / JA > EN — YES",
         all(s in pa1 for s in ("JA — authoritative source of truth",
                                "RU — text under review",
                                "EN — reference only",
                                "JA has priority over EN",
                                "EN must not be treated as authority")),
         ""),
        ("A: не просит перечислять каталоги — YES",
         not _sma_hits(pa1, _SMA_SEARCH_TOOLS),
         ""),
    ]

def _sma_checks_b(ch: Chapter, pb: str) -> list[tuple[str, bool, str]]:
    """Проверки изоляции prompt Auditor B (пары имя/ok/деталь)."""
    chap = sma_chapter_id(ch)
    run_id = _sma_json_field(pb, "audit_run_id")
    own_path = f"{SMA_REL_ROOT}/{chap}/b/{run_id}.json"
    old_name = re.compile(rf"{re.escape(chap)}-sma-[ab]")
    leak = _sma_hits(pb, _SMA_FORBIDDEN_B)
    kinds = _sma_path_kinds(pb)
    children = _sma_audit_children(pb)
    return [
        ("B: mentions A — NO",
         not leak,
         f"утечки: {leak}" if leak else "упоминаний первого аудитора нет"),
        ("B: mentions A results — NO",
         not _sma_hits(pb, ("результаты A", "результат A", "A findings", "A report")),
         ""),
        ("B: mentions old audit results — NO",
         not (old_name.search(pb) or _sma_hits(
             pb, ("-sma-a.json", "-sma-b.json", "sma-merged", "manual-sma"))),
         ""),
        ("B: mentions output/_audit old reports — NO",
         children == {"sma"},
         f"под output/_audit/: {sorted(children)}"),
        ("B: has own output path — YES",
         own_path in pb,
         own_path),
        ("B: has unique audit_run_id — YES",
         bool(run_id),
         run_id),
        ("B: own output path ведёт только в папку b/ — YES",
         kinds == {"b"},
         f"типы путей в промпте: {sorted(kinds)}"),
        ("B: автономность и единственность файла зафиксированы — YES",
         SMA_AUTONOMY_NOTE in pb and SMA_OWN_FILE_NOTE in pb,
         ""),
        ("B: OWN SKILL разрешён (противоречие с autonomy снято) — YES",
         "OWN SKILL" in pb
         and "AINovelEdit/.agents/skills/semantic-audit-b/SKILL.md" in pb
         and SMA_FORBIDDEN_INPUTS_NOTE in pb,
         ""),
        ("B: иерархия JA authoritative / RU under review / EN reference only / JA > EN — YES",
         all(s in pb for s in ("JA — authoritative source of truth",
                               "RU — text under review",
                               "EN — reference only",
                               "JA has priority over EN",
                               "EN must not be treated as authority")),
         ""),
        ("B: не просит перечислять каталоги — YES",
         not _sma_hits(pb, _SMA_SEARCH_TOOLS),
         ""),
    ]

def _sma_checks_c(ch: Chapter, pc1: str, pc2: str) -> list[tuple[str, bool, str]]:
    """Проверки изоляции prompt Pragmatic Auditor C (пары имя/ok/деталь)."""
    chap = sma_chapter_id(ch)
    run_id_1 = _sma_json_field(pc1, "audit_run_id")
    run_id_2 = _sma_json_field(pc2, "audit_run_id")
    own_path = f"{SMA_REL_ROOT}/{chap}/c/{run_id_1}.json"
    own_abs_1 = sma_result_abs_path(ch, "c", run_id_1, "json")
    own_abs_2 = sma_result_abs_path(ch, "c", run_id_2, "json")
    old_name = re.compile(rf"{re.escape(chap)}-sma-[ab]")
    leak = _sma_hits(pc1, _SMA_FORBIDDEN_C)
    kinds = _sma_path_kinds(pc1)
    children = _sma_audit_children(pc1)
    return [
        ("C: mentions A/B/Analyzer — NO",
         not leak,
         f"утечки: {leak}" if leak else "упоминаний других аудиторов и Analyzer нет"),
        ("C: mentions A/B results — NO",
         not _sma_hits(pc1, ("результаты A", "результаты B", "результат A",
                             "результат B", "A findings", "B findings",
                             "a_runs", "b_runs", "sources.a", "sources.b")),
         ""),
        ("C: mentions old audit results — NO",
         not (old_name.search(pc1) or _sma_hits(
             pc1, ("-sma-a.json", "-sma-b.json", "sma-merged", "manual-sma"))),
         ""),
        ("C: mentions output/_audit old reports — NO",
         children == {"sma"},
         f"под output/_audit/: {sorted(children)}"),
        ("C: has own output path — YES",
         own_path in pc1,
         own_path),
        ("C: has unique audit_run_id — YES",
         bool(run_id_1) and run_id_1 != run_id_2 and pc1 != pc2,
         f"{run_id_1} / повторный запуск: {run_id_2}"),
        ("C: два запуска подряд не перезаписывают друг друга — YES",
         bool(run_id_1) and own_abs_1 != own_abs_2
         and not os.path.exists(own_abs_1) and not os.path.exists(own_abs_2)
         and "c" in SMA_KINDS,
         f"{own_abs_1} | {own_abs_2}"),
        ("C: own output path ведёт только в папку c/ — YES",
         kinds == {"c"},
         f"типы путей в промпте: {sorted(kinds)}"),
        ("C: автономность и единственность файла зафиксированы — YES",
         SMA_AUTONOMY_NOTE in pc1 and SMA_OWN_FILE_NOTE in pc1,
         ""),
        ("C: OWN SKILL разрешён (противоречие с autonomy снято) — YES",
         "OWN SKILL" in pc1
         and "AINovelEdit/.agents/skills/pragmatic-audit/SKILL.md" in pc1
         and SMA_FORBIDDEN_INPUTS_NOTE in pc1,
         ""),
        ("C: иерархия JA authoritative / RU under review / EN reference only / JA > EN — YES",
         all(s in pc1 for s in ("JA — authoritative source of truth",
                                "RU — text under review",
                                "EN — reference only",
                                "JA has priority over EN",
                                "EN must not be treated as authority")),
         ""),
        ("C: не просит перечислять каталоги — YES",
         not _sma_hits(pc1, _SMA_SEARCH_TOOLS),
         ""),
        ("C: фокус — коммуникативный акт, подтекст, сила реплики — YES",
         all(key in pc1 for key in ("коммуникативный акт", "подтекст",
                                    "коммуникативной силы", "категоричности")),
         ""),
        ("C: формат: aspect / reason / pragmatic_reason / confidence — YES",
         all(f'"{field}"' in pc1 for field in
             ("aspect", "reason", "pragmatic_reason", "confidence")),
         ""),
        ("C: японские прагматические частицы упомянуты — YES",
         all(p in pc1 for p in ("ね", "かな", "かも", "でしょう", "んです",
                                "まさか", "別に", "ちょっと")),
         ""),
        ("C: проверка не сведена к списку частиц — YES",
         "своди аудит к списку частиц" in pc1, ""),
        ("C: дублирование A/B исключено (лексика / логика / грамматика / стиль) — YES",
         all(s in pc1 for s in ("russian-grammar-control", "russian-style-audit",
                                "russian-prose-rules", "микро-семантики",
                                "макро-семантики")),
         ""),
    ]

def _sma_phase1_inputs_match_doc(doc: str, pan1: str) -> bool:
    """Оба текста описывают один вход Фазы 1: JA + RU + EN (reference) + зеркало."""
    return ("зеркало блоков" in doc.lower()
            and "EN — reference only" in doc
            and "Зеркало блоков (соседний контекст)" in pan1)

def _sma_phase1_doc_sync(pan1: str) -> list[tuple[str, bool, str]]:
    """Сверка документации Phase 1 (AGENTS.md) с generated prompt.

    Гарантия, что описание входа Фазы 1 в AGENTS.md и в реально сгенерированном
    prompt — одно и то же: JA authoritative / RU text under review /
    EN reference only / JA > EN, а EN в Фазе 1 явно справочный, не evidence
    A/B/C и не источник истины. Ничего не пишет на диск.
    """
    agents_path = os.path.join(AINOVELEDIT, "AGENTS.md")
    try:
        with open(agents_path, encoding="utf-8") as fh:
            agents = fh.read()
    except OSError as exc:
        return [("Фаза 1: AGENTS.md доступен для сверки документации — YES",
                 False, f"{agents_path}: {exc}")]
    start = agents.find("**Phase 1 — BLIND**")
    end = (agents.find("**Phase 2 — EVIDENCE REVIEW**", start + 1)
           if start >= 0 else -1)
    doc = agents[start:end] if start >= 0 and end > start else ""
    shared = ("JA — authoritative source of truth", "RU — text under review",
              "EN — reference only", "JA > EN")
    return [
        ("Фаза 1: вход AGENTS.md = вход prompt (JA/RU/EN/зеркало) — YES",
         bool(doc) and all(p in doc for p in shared)
         and all(p in pan1 for p in shared)
         and _sma_phase1_inputs_match_doc(doc, pan1),
         f"AGENTS: {agents_path}"),
        ("Фаза 1: EN в AGENTS.md — справка, не evidence и не истина — YES",
         all(s in doc for s in ("EN — reference only",
                                "не является evidence A/B/C",
                                "не является источником истины",
                                "JA > EN")),
         ""),
    ]

# Старое имя модуля собирается из частей, чтобы проверка «нет зависимостей
# от старого имени» не находила саму себя в исходнике.
_OLD_MODULE_NAME = "generate_" + "agent_prompt"

def _dispatch_action_selftest() -> bool:
    """Проверить dispatch action без запуска внешних скриптов (dry-run)."""
    calls = {"n": 0}

    def _stub(ch: Chapter) -> int:
        calls["n"] += 1
        return 42

    probe = ActionInfo("probe", "selftest", _stub)
    code = run_action(probe, Chapter(3, "3"))
    if code != 42 or calls["n"] != 1:
        return False
    dispatched = dispatch_selection(("action", 0), Chapter(3, "3"))
    return (dispatched is not None and dispatched[0] == "action"
            and dispatched[1] is ACTIONS[0])

def _no_old_module_deps() -> bool:
    """Нет импортов старого модуля в .py-файлах проекта (исторические
    отчёты/логи не являются кодом и здесь не проверяются)."""
    skip_dirs = {".git", "__pycache__", "output", "translates", "origs"}
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for name in files:
            if not name.endswith(".py"):
                continue
            try:
                with open(os.path.join(root, name), encoding="utf-8") as fh:
                    text = fh.read()
            except OSError:
                continue
            if (f"import {_OLD_MODULE_NAME}" in text
                    or f"from {_OLD_MODULE_NAME} import" in text):
                return False
    return True

# ============================================================================
# SELF-TEST: РЕГРЕСС-СТРАЖИ СКИЛЛОВ
# ============================================================================
# Формулировки, которые уже один раз расходились с каноном и потому
# проверяются механически (dry-run, только чтение файлов скиллов).
SKILLS_REL_ROOT = os.path.join("AINovelEdit", ".agents", "skills")
_SKILL_FORBIDDEN_PATTERNS = (
    (re.compile(r'--text\s+"\.\.\."'),
     'шаблон `--text "..."`: не-ASCII текст в аргументах CLI запрещён '
     "(AGENTS.md, «Канал передачи текста правок»; нужен --text-file/"
     "--replace-file)"),
    (re.compile(r"\|\s*python\s+scripts/(?:save_block|fix_block)\.py"),
     "передача текста через конвейер PowerShell (запрещено AGENTS.md)"),
    (re.compile(r"--file\s+v14-"),
     "пример команды на замороженном томе v14 (completed.md; скрипты "
     "откажутся работать)"),
)


def _iter_skill_files() -> list[str]:
    """Все .md-файлы скиллов (SKILL.md и references/)."""
    root = os.path.join(ROOT, SKILLS_REL_ROOT)
    files: list[str] = []
    for dirpath, _dirs, names in os.walk(root):
        for name in sorted(names):
            if name.lower().endswith(".md"):
                files.append(os.path.join(dirpath, name))
    return files


def _read_text_or_empty(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def _skills_regression_selftest() -> list[tuple[str, bool, str]]:
    """Регресс-стражи формулировок скиллов (dry-run, ничего не пишется).

    Проверяются только реально найденные ранее расхождения: запрещённый
    канал передачи не-ASCII текста, примеры команд на замороженном томе,
    взаимные упоминания изолированных аудиторов A/B.
    """
    files = _iter_skill_files()
    hits: list[str] = []
    for path in files:
        text = _read_text_or_empty(path)
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        for pattern, why in _SKILL_FORBIDDEN_PATTERNS:
            if pattern.search(text):
                hits.append(f"{rel}: {why}")
    cross: list[str] = []
    for folder, needle in (("semantic-audit-a", "semantic-audit-b"),
                           ("semantic-audit-b", "semantic-audit-a")):
        path = os.path.join(ROOT, SKILLS_REL_ROOT, folder, "SKILL.md")
        text = _read_text_or_empty(path)
        if not text:
            cross.append(f"{folder}/SKILL.md: не читается")
        elif needle in text:
            cross.append(f"{folder} упоминает {needle}")
    return [
        ("Скиллы: канал --text/пайп и примеры на замороженном томе — NO",
         bool(files) and not hits,
         "; ".join(hits) if hits else f"проверено файлов: {len(files)}"),
        ("Скиллы: A/B не упоминают скилл друг друга (изоляция) — NO",
         not cross, "; ".join(cross) if cross else ""),
    ]


def _fullrun_pipeline_selftest() -> tuple[bool, str]:
    """Пайплайн полного прогона: структура, порядок и корректность индексов."""
    steps = fullrun_pipeline()
    audit_steps = audit_pipeline()
    problems = []

    def prompt_index(generator):
        return next((i for i, p in enumerate(PROMPTS)
                     if p.generator is generator), None)

    def action_index(name):
        return next((i for i, a in enumerate(ACTIONS) if a.name == name), None)

    for kind, index in steps:
        pool = PROMPTS if kind == "prompt" else ACTIONS if kind == "action" else []
        if not pool or not (0 <= index < len(pool)):
            problems.append(f"битый индекс {kind}:{index}")
    if steps[:3] != [("prompt", prompt_index(prompt_first_launch)),
                     ("prompt", prompt_index(prompt_continue)),
                     ("action", action_index(PREFILTER_ACTION_NAME))]:
        problems.append("нет фаз заполнения/предфильтров в начале")
    audit_start = 3
    if steps[audit_start:audit_start + len(audit_steps)] != audit_steps:
        problems.append("смысловой аудит идёт не целиком после предфильтров")
    tail = steps[audit_start + len(audit_steps):]
    expected_tail = [("prompt", prompt_index(g)) for g in
                     (prompt_grammar_audit, prompt_style_audit,
                      prompt_humanizer, prompt_full_audit)]
    expected_tail.append(("action", action_index(GATE_ACTION_NAME)))
    if tail != expected_tail:
        problems.append("нет финальных аудит-фаз или гейта в конце")
    if fullrun_stage_index(*steps[0]) != 0:
        problems.append("первая фаза не имеет номера 0")
    if fullrun_next_step(*steps[-1]) is not None:
        problems.append("последняя фаза возвращает следующую")
    detail = "; ".join(problems) or f"фаз: {len(steps)}"
    return not problems, detail

def _fullrun_status_selftest() -> tuple[bool, str]:
    """Статусы фаз на главе без файлов: везде [ ] и непустое описание."""
    empty = Chapter(997, "97")
    problems = []
    for kind, index in fullrun_pipeline():
        status = fullrun_stage_status(kind, index, empty)
        if not status.startswith("[ ]"):
            problems.append(f"ожидался [ ], получено {status!r}")
        if len(status) < len("[ ] ") + 3:
            problems.append(f"пустое описание эвиденса: {status!r}")
    detail = "; ".join(problems) or "все фазы показывают [ ] без эвиденса"
    return not problems, detail

def _fullrun_menu_visible_selftest(ch: Chapter) -> tuple[bool, str]:
    """Главное меню: пункт прогона идёт после «Смысловой аудит», нумерация верна."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        print_menu(ch)
    text = buffer.getvalue()
    problems = []
    match_audit = re.search(r"^\s*(\d+)\. Смысловой аудит — меню фаз$",
                            text, re.MULTILINE)
    match_run = re.search(r"^\s*(\d+)\. Полный прогон главы — меню фаз$",
                          text, re.MULTILINE)
    match_next = re.search(r"^\s*(\d+)\. Следующая глава$", text, re.MULTILINE)
    if not (match_audit and match_run and match_next):
        problems.append("пункты «Разделы»/«Навигация» не найдены в меню")
    else:
        audit_no = int(match_audit.group(1))
        run_no = int(match_run.group(1))
        next_no = int(match_next.group(1))
        if run_no != audit_no + 1:
            problems.append(f"прогон под номером {run_no}, ожидался "
                            f"{audit_no + 1} (сразу после аудита)")
        if next_no != run_no + 1:
            problems.append(f"навигация под номером {next_no}, ожидался "
                            f"{run_no + 1}")
    detail = "; ".join(problems) or "нумерация меню корректна"
    return not problems, detail

def _fullrun_prereq_selftest() -> tuple[bool, str]:
    """Prereq-предупреждения фаз полного прогона на главе без файлов."""
    empty = Chapter(997, "97")
    problems = []

    def prompt_for(generator):
        return next(p for p in PROMPTS if p.generator is generator)

    def action_for(name):
        return next(a for a in ACTIONS if a.name == name)

    if fullrun_prereq_warnings(prompt_for(prompt_continue), empty):
        problems.append("«Продолжение» предупреждает без причины")
    for generator in (prompt_grammar_audit, prompt_full_audit):
        warns = fullrun_prereq_warnings(prompt_for(generator), empty)
        if not any("OUTPUT" in w for w in warns):
            problems.append(f"{generator.__name__}: нет предупреждения о "
                            "output-файле")
    for name in (PREFILTER_ACTION_NAME, GATE_ACTION_NAME):
        warns = fullrun_prereq_warnings(action_for(name), empty)
        if not any("OUTPUT" in w for w in warns):
            problems.append(f"{name}: нет предупреждения об output-файле")
    if fullrun_prereq_warnings(action_for("Omission Pre-check"), empty):
        problems.append("Omission Pre-check: лишнее предупреждение")
    # На живой главе с output: финальный аудит требует свежих предфильтров
    # и результатов смыслового аудита — проверяется только структура текста.
    warns = fullrun_prereq_warnings(prompt_for(prompt_full_audit),
                                    Chapter(3, "3"))
    if any("ПРЕДФИЛЬТРЫ НЕ СВЕЖИ" in w and PREFILTER_ACTION_NAME not in w
           for w in warns):
        problems.append("предупреждение о предфильтрах не ссылается на фазу")
    detail = "; ".join(problems) or "предупреждения корректны"
    return not problems, detail

def _freshness_selftest() -> tuple[bool, str]:
    """_is_fresh: отчёт старее источника — устаревший; новее — свежий."""
    problems = []
    with tempfile.TemporaryDirectory() as tmp:
        report = os.path.join(tmp, "report.md")
        source = os.path.join(tmp, "source.md")
        missing = os.path.join(tmp, "missing.md")
        with open(report, "w", encoding="utf-8") as fh:
            fh.write("r")
        with open(source, "w", encoding="utf-8") as fh:
            fh.write("s")
        os.utime(report, (1000, 1000))
        os.utime(source, (2000, 2000))
        if _is_fresh(report, source):
            problems.append("старый отчёт посчитан свежим")
        os.utime(report, (3000, 3000))
        if not _is_fresh(report, source):
            problems.append("свежий отчёт посчитан устаревшим")
        if _is_fresh(report, missing):
            problems.append("отчёт без источника посчитан свежим")
        if _is_fresh(missing, source):
            problems.append("отсутствующий отчёт посчитан свежим")
    detail = "; ".join(problems) or "свежесть считается корректно"
    return not problems, detail

def _audit_section_pattern_selftest() -> tuple[bool, str]:
    """Толерантные матчеры секций отчёта аудита (грамматика/стиль/humanizer)."""
    samples = {
        prompt_grammar_audit: (
            "## 5. Грамматический контроль (grammar_scan.py)",
            "## Грамматика",
            "### Итог GRAMMAR: ЧИСТО",
        ),
        prompt_style_audit: (
            "## 6. Стилевой контроль (style_scan.py)",
            "## Стиль",
            "## 10. Стилевой контроль (STYLE AUDIT)",
        ),
        prompt_humanizer: (
            "## 3. russian-humanizer (машинность)",
            "## Машинность (`russian-humanizer`)",
            "## 7. Машинность (russian-humanizer)",
        ),
    }
    problems = []
    for generator, headings in samples.items():
        pattern = _AUDIT_SECTION_PATTERNS[generator]
        for heading in headings:
            if not pattern.search(heading):
                problems.append(f"{generator.__name__}: не ловит {heading!r}")
    if _AUDIT_SECTION_PATTERNS[prompt_grammar_audit].search(
            "## Замечания по grammar_scan"):
        problems.append("«grammar_scan» в заголовке считается секцией")
    if _AUDIT_SECTION_PATTERNS[prompt_style_audit].search(
            "## Замечания по style_scan"):
        problems.append("«style_scan» в заголовке считается секцией")
    detail = "; ".join(problems) or "матчеры секций работают"
    return not problems, detail

def _prompt_format_selftest(pa: str, pb: str, pc: str,
                            ph: str) -> list[tuple[str, bool, str]]:
    """Инварианты формата промптов A/B/C и разметки в промпте humanizer."""
    prompts = (pa, pb, pc)
    return [
        ("A/B/C: один JSON-объект на запуск с audit_run_id — YES",
         all('"audit_run_id"' in p for p in prompts)
         and all("выводи JSON-массив находок" not in p for p in prompts),
         ""),
        ("Humanizer: канон курсива `_…_`, `*…*` не объявлен нормой — YES",
         "курсив `_…_`" in ph and "курсив `*…*`" not in ph, ""),
        ("A/B/C: coverage-attestation в формате и правилах — YES",
         all('"coverage": "Просмотренные блоки' in p for p in prompts)
         and all("coverage обязателен тем более" in p for p in prompts),
         ""),
        ("A/B/C: при findings [] coverage обязателен, валидатор отклонит — YES",
         all("semantic_findings --validate" in p for p in prompts),
         ""),
    ]

def self_test_semantic_prompts(
    ch: Chapter,
) -> tuple[list[tuple[str, bool, str]], dict[str, str]]:
    """Dry-run проверка prompt A / B / C / Analyzer.

    Ничего не пишет на диск и не меняет перевод: только генерирует промпты в
    память и проверяет изоляцию, пути и формат. Возвращает пары
    (проверки, промпты) — промпты нужны для опционального показа (--show-sma).

    Analyzer проверяется в трёх видах:
    - ``pan``  — реальное состояние каталогов главы (A+B или A+B+C);
    - ``pan_abc`` — симуляция: запуски A, B и C уже существуют;
    - ``pan_ab``  — симуляция: запусков C нет (режим A+B для старых A/B).
    Плюс три симуляции адресации Фазы 1 из Фазы 2 (``pan_p1`` — один файл
    Фазы 1, ``pan_p1_many`` — несколько, ``pan_p1_none`` — ни одного).
    """
    pa1 = prompt_semantic_a(ch)
    pa2 = prompt_semantic_a(ch)
    pb = prompt_semantic_b(ch)
    pc1 = prompt_pragmatic_c(ch)
    pc2 = prompt_pragmatic_c(ch)
    pan = prompt_semantic_analyzer(ch)
    pan_abc = prompt_semantic_analyzer(ch, runs={
        "a": ["sim-a-run-1", "sim-a-run-2"],
        "b": ["sim-b-run-1", "sim-b-run-2"],
        "c": ["sim-c-run-1", "sim-c-run-2"],
        "phase1": ["sim-p1-1"],
    })
    pan_ab = prompt_semantic_analyzer(ch, runs={
        "a": sma_existing_runs(ch, "a"),
        "b": sma_existing_runs(ch, "b"),
        "c": [],
        "phase1": ["sim-p1-1"],
    })
    # симуляции адресации Фазы 1: один файл / несколько / ни одного
    pan_p1 = prompt_semantic_analyzer(ch, runs={
        "a": ["sim-a-run-1"], "b": ["sim-b-run-1"], "c": [],
        "phase1": ["sim-p1-1"]})
    pan_p1_many = prompt_semantic_analyzer(ch, runs={
        "a": ["sim-a-run-1"], "b": ["sim-b-run-1"], "c": [],
        "phase1": ["sim-p1-1", "sim-p1-2"]})
    pan_p1_none = prompt_semantic_analyzer(ch, runs={
        "a": ["sim-a-run-1"], "b": ["sim-b-run-1"], "c": [],
        "phase1": []})
    pan1 = prompt_semantic_analyzer_phase1(ch)
    rr = prompt_rules_recheck(ch)
    ph = prompt_humanizer(ch)
    # глава без pre-check: проверка, что его отсутствие не ломает Фазу 2
    ch_nopc = Chapter(99, "99")
    pan_nopc = prompt_semantic_analyzer(ch_nopc, runs={
        "a": ["sim-x"], "b": ["sim-x"], "c": [], "phase1": ["sim-p1-1"]})
    # глава, у которой точно нет audit-файлов, — для проверки
    # audit_prereq_warning (Фаза 2 без входов должна предупреждать)
    _empty_ch = Chapter(997, "97")
    chap = sma_chapter_id(ch)
    a_dir = f"{SMA_REL_ROOT}/{chap}/a/"
    b_dir = f"{SMA_REL_ROOT}/{chap}/b/"
    c_dir = f"{SMA_REL_ROOT}/{chap}/c/"
    an_dir = f"{SMA_REL_ROOT}/{chap}/analysis/"
    analysis_id = _sma_json_field(pan, "analysis_id")
    kinds = _sma_path_kinds(pan)
    checks = _sma_checks_a(ch, pa1, pa2)
    checks += _sma_checks_b(ch, pb)
    checks += _sma_checks_c(ch, pc1, pc2)
    checks += [
        ("Analyzer: reads ALL existing A results — YES",
         a_dir in pan, a_dir),
        ("Analyzer: reads ALL existing B results — YES",
         b_dir in pan, b_dir),
        ("Analyzer: reads ALL existing C results — YES",
         c_dir in pan, c_dir),
        ("Analyzer: пишет только в analysis/ — YES",
         an_dir in pan and kinds == {"a", "b", "c", "analysis", "precheck"},
         f"типы путей в промпте: {sorted(kinds)}"),
        ("Analyzer: has unique analysis_id и путь результата — YES",
         bool(analysis_id) and f"{an_dir}{analysis_id}.json" in pan,
         analysis_id),
        ("Analyzer: может править output через fix_block.py — YES",
         "fix_block.py" in pan and "update_merged.py" in pan,
         ""),
        ("Analyzer: запрещено менять evidence A/B/C — YES",
         "НЕ редактируй, не удаляй и не" in pan and "a/, b/ и c/" in pan,
         ""),
        ("Analyzer: запрет majority vote — YES",
         "majority vote" in pan and "только evidence" in pan,
         ""),
        ("Analyzer: «A+B+C согласны» ≠ ошибка, «только C» ≠ false positive — YES",
         "«A + B + C → ошибка»" in pan and "только C" in pan
         and "автоматически ложный positive" in pan, ""),
        ("Analyzer: происхождение sources не голосует — YES",
         "ПРОИСХОЖДЕНИЕ (sources) НЕ ГОЛОСУЕТ" in pan, ""),
        ("Analyzer: не берёт результаты другой главы — YES",
         "Результаты ДРУГИХ глав не используй" in pan,
         ""),
        ("Analyzer: фиксирует before/after для FIXED — YES",
         '"before"' in pan and '"after"' in pan,
         ""),
        ("Analyzer: две оси решения (fidelity + action) — YES",
         all(s in pan for s in ("CONFIRMED_ERROR", "DISPUTED",
                                "FALSE_POSITIVE", "fidelity",
                                "MEANING_SHIFT", "COMPONENT_LOSS")),
         ""),
        ("Analyzer: действия сохранены — YES",
         all(a in pan for a in ("FIXED", "REPORT_ONLY", "PRESERVED")),
         ""),
        ("Analyzer: фаза 1 (самостоятельная JA → RU) раньше фазы 2 — YES",
         "ФАЗА 1" in pan and "ФАЗА 2" in pan
         and "ТОЛЬКО после завершённой Фазы 1" in pan
         and pan.find("ФАЗА 1") < pan.find("ФАЗА 2"),
         ""),
        ("Analyzer: режим A+B+C видит несколько запусков A/B/C — YES",
         '"a_runs": ["sim-a-run-1", "sim-a-run-2"]' in pan_abc
         and '"b_runs": ["sim-b-run-1", "sim-b-run-2"]' in pan_abc
         and '"c_runs": ["sim-c-run-1", "sim-c-run-2"]' in pan_abc,
         ""),
        ("Analyzer: sources.a / sources.b / sources.c в формате — YES",
         '"sources": { "a": ["<run_id>"], "b": ["<run_id>"], "c": ["<run_id>"], "precheck": false }'
         in pan_abc, ""),
        ("Analyzer: режим A+B+C объявлен в prompt — YES",
         "РЕЖИМ ЭТОГО ЗАПУСКА: A + B + C" in pan_abc, ""),
        ("Analyzer: работает без C (режим A+B) — YES",
         '"c_runs": []' in pan_ab
         and "(пока нет ни одного запуска C)" in pan_ab
         and "РЕЖИМ ЭТОГО ЗАПУСКА: A + B\n" in pan_ab
         and "Наличие C НЕ обязательно" in pan_ab,
         ""),
        ("Analyzer: C необязателен для старых запусков A/B — YES",
         "Отсутствие запусков C — норма" in pan_ab
         and "прежнем объёме A+B" in pan_ab,
         ""),
        # ---- ФАЗА 1: фактическая (не декларативная) изоляция промпта ----
        ("Фаза 1: в промпте НЕТ каталогов A/B/C — YES",
         not _sma_hits(pan1, (a_dir, b_dir, c_dir)),
         ""),
        ("Фаза 1: в промпте НЕТ путей в a/, b/, c/ — YES",
         not _sma_hits(pan1, (f"/{chap}/a/", f"/{chap}/b/", f"/{chap}/c/")),
         ""),
        ("Фаза 1: в промпте НЕТ evidence omission pre-check — YES",
         not _sma_hits(pan1, (sma_precheck_rel_path(ch),
                              f"/{chap}/{SMA_PRECHECK_KIND}/",
                              SMA_PRECHECK_FILE)),
         ""),
        ("Фаза 1: в промпте НЕТ списков запусков (a_runs/b_runs/c_runs) — YES",
         not _sma_hits(pan1, ('"a_runs"', '"b_runs"', '"c_runs"')),
         ""),
        ("Фаза 1: в промпте НЕТ provenance (sources) — YES",
         not _sma_hits(pan1, ('"sources"', 'sources.a', 'sources.b',
                              'sources.c')),
         ""),
        ("Фаза 1: в промпте НЕТ прежних analysis-результатов (final + phase1) — YES",
         not _sma_hits(pan1, [f"{chap}/analysis/{r}." for r in
                              sma_existing_runs(ch, "analysis")
                              + sma_existing_phase1_runs(ch)]),
         ""),
        ("Фаза 1: в промпте НЕТ findings A/B/C и их аудиторов — YES",
         not _sma_hits(pan1, ("Auditor A", "Auditor B", "Pragmatic Auditor C",
                              "findings A", "findings B", "findings C",
                              "НАБОР EVIDENCE")),
         ""),
        ("Фаза 1: в промпте НЕТ вердиктов/статусов — YES",
         not _sma_hits(pan1, ("CONFIRMED_ERROR", "DISPUTED", "FALSE_POSITIVE",
                              "REPORT_ONLY", "majority vote")),
         ""),
        ("Фаза 1: путь только в analysis (собственный вывод) — YES",
         _sma_path_kinds(pan1) <= {"analysis"},
         f"типы путей: {sorted(_sma_path_kinds(pan1))}"),
        ("Фаза 1: содержит JA + RU + EN + контекст и вывод phase1 — YES",
         ch.ja_path in pan1 and ch.output_path in pan1
         and ch.en_path in pan1
         and ch.merged_path in pan1 and ".phase1.json" in pan1,
         ""),
        # ---- ДОКУМЕНТАЦИЯ ↔ PROMPT: описание входа Фазы 1 в AGENTS.md
        # совпадает с фактическим generated prompt ----
        *_sma_phase1_doc_sync(pan1),
        # ---- ФАЗА 2: evidence приходит только сюда ----
        ("Фаза 2: содержит каталог A — YES", a_dir in pan, ""),
        ("Фаза 2: содержит каталог B — YES", b_dir in pan, ""),
        ("Фаза 2: содержит каталог C — YES", c_dir in pan, ""),
        ("Фаза 2: содержит evidence omission pre-check — YES",
         sma_precheck_rel_path(ch) in pan
         and f"/{chap}/{SMA_PRECHECK_KIND}/" in pan, ""),
        ("Фаза 2: провенанс (sources) присутствует — YES",
         '"sources"' in pan and "ПРОИСХОЖДЕНИЕ (sources) НЕ ГОЛОСУЕТ" in pan,
         ""),
        # ---- ФАЗА 2 ↔ ФАЗА 1: конкретный ФАЙЛ, а не маска *.phase1.json ----
        ("Фаза 2: один файл Фазы 1 → конкретный путь (без glob) — YES",
         f"{an_dir}sim-p1-1.phase1.json" in pan_p1
         and "*.phase1.json" not in pan_p1
         and "ПЕРВОНАЧАЛЬНОЕ" in pan_p1,
         "sim-p1-1.phase1.json"),
        ("Фаза 2: выбранный файл Фазы 1 записан в inputs.phase1 — YES",
         '"phase1": "sim-p1-1.phase1.json"' in pan_p1
         and "inputs.phase1" in pan_p1,
         ""),
        ("Фаза 2: несколько файлов Фазы 1 → перечислены, по умолчанию свежий — YES",
         f"{an_dir}sim-p1-1.phase1.json" in pan_p1_many
         and f"{an_dir}sim-p1-2.phase1.json" in pan_p1_many
         and "НЕСКОЛЬКО слепых выводов Фазы 1" in pan_p1_many
         and "САМЫЙ СВЕЖИЙ" in pan_p1_many
         and '"phase1": "sim-p1-1.phase1.json"' in pan_p1_many,
         ""),
        ("Фаза 2: слепые прогоны не смешиваются и не голосуют — YES",
         "Не смешивай выводы разных слепых прогонов" in pan_p1_many
         and "они не голоса" in pan_p1_many, ""),
        ("Фаза 2: нет файла Фазы 1 → inputs.phase1 = null и отказ — YES",
         "ФАЙЛА ФАЗЫ 1 НЕТ" in pan_p1_none
         and '"phase1": null' in pan_p1_none
         and "нет файла Фазы 1 — работать нельзя" in pan_p1_none, ""),
        ("Фаза 2: порядок файлов Фазы 1 — по mtime (свежий первым) — YES",
         _sma_phase1_order_selftest(), ""),
        # ---- ФАЗА 2 БЕЗ phase1: STOP + отдельный запуск Фазы 1 ----
        # (внутри evidence-review задания Фазу 1 выполнять НЕЛЬЗЯ: blindness
        # утрачен — проверяется по тексту сгенерированного prompt)
        ("Фаза 2: phase1 отсутствует → STOP, сначала отдельный Фаза 1 — YES",
         "STOP: Фазу 1 выполнять в этом задании НЕЛЬЗЯ" in pan
         and "ОТДЕЛЬНОЕ задание «Смысловой анализатор —" in pan
         and "после завершения Фазы 1 выполняй Фазу 2" in pan,
         ""),
        ("Фаза 2: НЕ инструктирует выполнить Фазу 1 внутри себя — YES",
         "сначала выполни Фазу 1" not in pan
         and "и лишь после этого возвращайся к Фазе 2" not in pan,
         ""),
        ("Фаза 2: pre-check — evidence, а не голос — YES",
         "НЕ аудитор" in pan and "Наличие pre-check НЕ обязательно" in pan, ""),
        ("Фаза 2: без pre-check работает (chapter без файла) — YES",
         sma_precheck_rel_path(ch_nopc) in pan_nopc
         and "работай без него" in pan_nopc
         and '"precheck": null' in pan_nopc, ""),
        # ---- ИЕРАРХИЯ ИСТОЧНИКОВ (JA > EN): проверяется СГЕНЕРИРОВАННЫЙ
        # prompt обеих фаз, а не текст skill-файла ----
        ("Фаза 1: JA — authoritative source of truth — YES",
         "JA — authoritative source of truth" in pan1, ""),
        ("Фаза 1: RU — text under review — YES",
         "RU — text under review" in pan1, ""),
        ("Фаза 1: EN — reference only — YES",
         "EN — reference only" in pan1, ""),
        ("Фаза 1: JA has priority over EN (JA > EN) — YES",
         "JA has priority over EN" in pan1 and "JA > EN" in pan1, ""),
        ("Фаза 1: EN must not be treated as authority — YES",
         "EN must not be treated as authority" in pan1, ""),
        ("Фаза 1: EN не объявлен источником смысла — YES",
         not _sma_hits(pan1, ("EN — источник истины",
                              "EN (источник смысла",
                              "EN — основной смысловой")), ""),
        ("Фаза 1: конфликт JA/EN (JA=X, EN=Y, RU=Y) оценивается по JA → RU — YES",
         "JA = X, EN = Y, RU = Y" in pan1
         and "совпадает с EN» запрещён" in pan1
         and "Основная проверка — JA → RU" in pan1, ""),
        ("Фаза 2: JA — authoritative source of truth — YES",
         "JA — authoritative source of truth" in pan, ""),
        ("Фаза 2: RU — text under review — YES",
         "RU — text under review" in pan, ""),
        ("Фаза 2: EN — reference only — YES",
         "EN — reference only" in pan, ""),
        ("Фаза 2: JA has priority over EN (JA > EN) — YES",
         "JA has priority over EN" in pan and "JA > EN" in pan, ""),
        ("Фаза 2: EN must not be treated as authority — YES",
         "EN must not be treated as authority" in pan, ""),
        ("Фаза 2: EN не объявлен источником смысла — YES",
         not _sma_hits(pan, ("EN — источник истины",
                             "EN (источник смысла",
                             "EN — основной смысловой")), ""),
        ("Фаза 2: конфликт JA/EN (JA=X, EN=Y, RU=Y) оценивается по JA → RU — YES",
         "JA = X, EN = Y, RU = Y" in pan
         and "совпадает с EN» запрещён" in pan
         and "Основная проверка — JA → RU" in pan, ""),
        ("Фаза 2: evidence/EN против JA → ориентир JA, совпадение с EN ≠ доказательство — YES",
         "если evidence аудитора или EN противоречит JA, ориентируйся на JA" in pan
         and "не доказывает корректности" in pan, ""),
        # ---- РЕКОНТРОЛЬ: разделитель сцены необязателен (как в AGENTS.md) ----
        ("prompt_rules_recheck: --- необязателен, отсутствие не WARNING — YES",
         "необязательный композиционный инструмент" in rr
         and "Отсутствие `---` само по себе НЕ является ошибкой" in rr
         and "Отсутствие `---` при явной смене сцены — WARNING" not in rr
         and "обязательные разделители сцен" not in rr,
         ""),
        # ---- ФОРМАТ ПРОМПТОВ A/B/C И РАЗМЕТКА HUMANIZER ----
        *_prompt_format_selftest(pa1, pb, pc1, ph),
        # ---- РЕГРЕСС-СТРАЖИ СКИЛЛОВ (канал текста, изоляция A/B) ----
        *_skills_regression_selftest(),
        # ---- LEGACY: GAP-аудит не активен, функция сохранена ----
        ("prompt_gap_audit: больше не в активном меню PROMPTS — YES",
         not any(getattr(p, "generator", None) is prompt_gap_audit
                 for p in PROMPTS)
         and not any("GAP" in p.title for p in PROMPTS),
         f"пунктов меню: {len(PROMPTS)}"),
        ("prompt_gap_audit: функция сохранена (legacy-задел) — YES",
         callable(prompt_gap_audit), ""),
        # ---- МЕНЮ: группировка, слаги, отдельное меню смыслового аудита ----
        ("Меню: «Реконтроль готовой главы» убран, функция сохранена — YES",
         not any(getattr(p, "generator", None) is prompt_rules_recheck
                 for p in PROMPTS)
         and callable(prompt_rules_recheck),
         f"пунктов меню: {len(PROMPTS)}"),
        ("Меню: у каждого пункта задан group и slug — YES",
         all(p.group in GROUP_ORDER and p.slug for p in PROMPTS),
         "; ".join(f"{p.title}: group={p.group or '—'} slug={p.slug or '—'}"
                   for p in PROMPTS
                   if p.group not in GROUP_ORDER or not p.slug) or ""),
        ("Меню: слаги уникальны — YES",
         len({p.slug for p in PROMPTS}) == len(PROMPTS),
         f"слаги: {[p.slug for p in PROMPTS]}"),
        ("Меню: раздел «Смысловой аудит» скрыт из главного меню — YES",
         bool(visible_prompt_indices())
         and all(PROMPTS[i].group != GROUP_SMA for i in visible_prompt_indices()),
         f"видно пунктов: {len(visible_prompt_indices())} из {len(PROMPTS)}"),
        ("Меню: главные разделы идут в порядке GROUP_ORDER — YES",
         [PROMPTS[i].group for i in visible_prompt_indices()]
         == sorted((PROMPTS[i].group for i in visible_prompt_indices()),
                   key=GROUP_ORDER.index),
         f"порядок: {[PROMPTS[i].group for i in visible_prompt_indices()]}"),
        ("Меню: пайплайн аудита фиксированный (Pre-check → A → B → C → Ф1 → Ф2) — YES",
         [PROMPTS[i].generator if kind == "prompt" else "pre-check"
          for kind, i in audit_pipeline()]
         == ["pre-check", prompt_semantic_a, prompt_semantic_b,
             prompt_pragmatic_c, prompt_semantic_analyzer_phase1,
             prompt_semantic_analyzer]
         and all(audit_stage_index(kind, i) == stage
                 for stage, (kind, i) in enumerate(audit_pipeline())),
         f"этапов: {len(audit_pipeline())}"),
        ("Меню: «Следующий промпт» остаётся в пределах раздела — YES",
         all(
             (nxt := next_prompt_index(i)) is None
             or PROMPTS[nxt].group == PROMPTS[i].group
             for i in range(len(PROMPTS))
         ) and next_prompt_index(
             max(i for i in range(len(PROMPTS))
                 if PROMPTS[i].group == GROUP_SMA)) is None,
         ""),
        ("Меню: промпт пишется в папку agent_prompts/ (имя содержит главу и слаг) — YES",
         prompt_file_name(ch, PROMPTS[0])
         == f"{PROMPT_DIR_NAME}/{PROMPT_FILE_PREFIX}."
            f"{sma_chapter_id(ch)}.{PROMPTS[0].slug}.md",
         prompt_file_name(ch, PROMPTS[0])),
        ("Меню: prompt_run_id достаёт audit_run_id и режет .phase1 — YES",
         prompt_run_id('{"audit_run_id": "abc-123.phase1"}') == "abc-123"
         and prompt_run_id('{"analysis_id": "xyz"}') == "xyz"
         and prompt_run_id("без идентификатора") is None,
         ""),
        ("Меню: предупреждения о пропущенных входах фазы — YES",
         audit_prereq_warning(
             next(p for p in PROMPTS
                  if p.generator is prompt_semantic_analyzer), _empty_ch) is not None
         and audit_prereq_warning(
             next(p for p in PROMPTS
                  if p.generator is prompt_semantic_analyzer_phase1),
             _empty_ch) is None
         and audit_prereq_warning(
             next(p for p in PROMPTS if p.generator is prompt_semantic_a),
             _empty_ch) is None,
         "глава без audit-файлов: Фаза 2 предупреждает, Фаза 1 / A — нет"),
        ("Меню: пункт «Обработка одного блока» остался на индексе 8 — YES",
         len(PROMPTS) > 8 and PROMPTS[8].title == "Обработка одного блока",
         f"PROMPTS[8] = {PROMPTS[8].title if len(PROMPTS) > 8 else '(нет)'}"),
        ("Меню: обе фазы Analyzer присутствуют — YES",
         any(p.generator is prompt_semantic_analyzer_phase1 for p in PROMPTS)
         and any(p.generator is prompt_semantic_analyzer for p in PROMPTS),
         ""),
        # ---- МЕНЮ ПОЛНОГО ПРОГОНА ГЛАВЫ (пофазовый прогон, эвиденсы) ----
        ("Полный прогон: пайплайн от перевода до гейта (аудит внутри) — YES",
         _fullrun_pipeline_selftest(), ""),
        ("Полный прогон: статусы фаз по файлам-эвиденсам ([x]/[ ]) — YES",
         _fullrun_status_selftest(), ""),
        ("Полный прогон: пункт в главном меню сразу после «Смысловой аудит» — YES",
         _fullrun_menu_visible_selftest(ch), ""),
        ("Полный прогон: prereq-предупреждения входов фаз — YES",
         _fullrun_prereq_selftest(), ""),
        ("Полный прогон: свежесть отчётов (report >= source) — YES",
         _freshness_selftest(), ""),
        ("Полный прогон: матчеры секций отчёта аудита толерантны — YES",
         _audit_section_pattern_selftest(), ""),
        # ---- ORCHESTRATOR: PROMPTS vs ACTIONS ----
        ("Orchestrator: PROMPTS непусты — YES",
         len(PROMPTS) > 0, f"промптов: {len(PROMPTS)}"),
        ("Orchestrator: ACTIONS непусты — YES",
         len(ACTIONS) > 0, f"actions: {len(ACTIONS)}"),
        ("Orchestrator: Omission Pre-check — это Action, а не Prompt — YES",
         any(a.name == "Omission Pre-check" for a in ACTIONS)
         and not any("Omission Pre-check" in p.title for p in PROMPTS),
         f"actions: {[a.name for a in ACTIONS]}"),
        ("Orchestrator: ActionInfo не наследуется от PromptInfo — YES",
         not issubclass(ActionInfo, PromptInfo), ""),
        ("Orchestrator: dispatch action (execute -> int) — YES",
         _dispatch_action_selftest(), ""),
        ("Orchestrator: новое имя файла agent_workflow.py — YES",
         os.path.basename(os.path.abspath(__file__)) == "agent_workflow.py",
         os.path.basename(os.path.abspath(__file__))),
        ("Orchestrator: нет зависимостей от старого имени модуля — YES",
         _no_old_module_deps(), f"старое имя: {_OLD_MODULE_NAME}"),
    ]
    prompts = {"A": pa1, "B": pb, "C": pc1,
               "Analyzer Phase 1": pan1, "Analyzer Phase 2": pan}
    return checks, prompts

def _parse_selftest_chapter(argv: list[str]) -> Chapter | None:
    """Разобрать --self-test-sma <volume> <chapter> | <vN-chYY>."""
    if "--self-test-sma" not in argv:
        return None
    index = argv.index("--self-test-sma")
    rest = [arg for arg in argv[index + 1:] if not arg.startswith("--")]
    if not rest:
        return None
    match = re.match(r"^v?(\d+)-ch(\d+)$", rest[0], re.IGNORECASE)
    if match:
        return Chapter(int(match.group(1)), str(int(match.group(2))))
    if len(rest) >= 2:
        try:
            volume = int(rest[0])
        except ValueError:
            return None
        return Chapter(volume, clean_chapter_input(rest[1]))
    return None

def run_sma_self_test(argv: list[str]) -> int:
    """CLI dry-run: печатает self-test A / B / C / Analyzer. Ничего не пишет."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ch = _parse_selftest_chapter(argv)
    if ch is None:
        print("Использование: python tools/agent_workflow.py "
              "--self-test-sma <volume> <chapter>")
        print("  например: --self-test-sma 3 3   или   --self-test-sma v3-ch03")
        print("  опция --show-sma — дополнительно напечатать промпты A/B/C/Analyzer")
        return 2
    checks, prompts = self_test_semantic_prompts(ch)
    separator("=")
    print(f"SMA self-test (dry-run) — глава {sma_chapter_id(ch)}")
    separator("=")
    for name, ok, detail in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        if detail:
            print(f"         {detail}")
    separator("=")
    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"  Итог: {passed}/{len(checks)} проверок пройдено.")
    print("  Файлы не создавались, перевод не изменялся (dry-run).")
    if "--show-sma" in argv:
        for title in prompts:
            print()
            separator("=")
            print(f"  PROMPT {title}")
            separator("=")
            print(prompts[title])
    return 0 if passed == len(checks) else 1

# ============================================================================
# ОСНОВНОЙ ЦИКЛ
# ============================================================================
def main() -> None:
    """Главный цикл программы."""
    print()
    print("AINovelEdit — генератор промптов")
    separator()
    ch = ask_chapter()

    prompt_index: int | None = None
    prompt_obj: PromptInfo | None = None
    prompt_text: str | None = None
    action_obj: ActionInfo | None = None
    in_audit_menu = False   # мы внутри меню смыслового аудита
    audit_stage = 0         # позиция в audit_pipeline() (для метки ->)
    in_fullrun_menu = False # мы внутри меню полного прогона главы
    fullrun_stage = 0       # позиция в fullrun_pipeline() (для метки ->)
    needs_confirm = True    # подтвердить перед следующей генерацией

    while True:
        # --- 1. Выбор пункта меню (главного, смыслового аудита, прогона) ---
        if prompt_index is None and action_obj is None:
            if in_fullrun_menu:
                result = choose_fullrun_menu(ch, fullrun_stage)
            elif in_audit_menu:
                result = choose_audit_menu(ch, audit_stage)
            else:
                result = choose_prompt(ch)

            if result == "quit":
                print()
                print("Выход.")
                return

            if result == "back":
                in_audit_menu = False
                in_fullrun_menu = False
                continue

            if result == "change":
                ch = ask_chapter()
                continue

            if result in ("next", "prev"):
                new_ch = navigate_next(ch) if result == "next" else navigate_prev(ch)
                if new_ch:
                    ch = new_ch
                    print(f"  Переключено на: {ch.chapter_id_full}")
                else:
                    print("  Отменено.")
                continue

            if result == "audit":
                in_audit_menu = True
                in_fullrun_menu = False
                audit_stage = 0
                continue

            if result == "fullrun":
                in_fullrun_menu = True
                in_audit_menu = False
                fullrun_stage = 0
                continue

            if isinstance(result, tuple) and result[0] == "stage":
                # «Следующий этап/фаза» из меню аудита или прогона: переходим
                # и показываем подтверждение нового этапа.
                if in_fullrun_menu:
                    fullrun_stage = result[1]
                    step_kind, step_index = fullrun_pipeline()[fullrun_stage]
                else:
                    audit_stage = result[1]
                    step_kind, step_index = audit_pipeline()[audit_stage]
                result = (step_kind, step_index)

            dispatched = dispatch_selection(result, ch)
            if dispatched is None:
                continue
            if dispatched[0] == "action":
                action_obj = dispatched[1]
            else:
                prompt_index = result[1]
                prompt_obj = PROMPTS[prompt_index]
            needs_confirm = True

        # --- 2. Подтверждение выбранного этапа/режима ---
        if prompt_index is not None:
            stage = audit_stage_index("prompt", prompt_index)
            if stage is not None:
                audit_stage = stage
            stage = fullrun_stage_index("prompt", prompt_index)
            if stage is not None:
                fullrun_stage = stage
            if needs_confirm:
                notes = []
                warning = audit_prereq_warning(prompt_obj, ch)
                if warning:
                    notes.append(warning)
                if in_fullrun_menu:
                    notes.extend(fullrun_prereq_warnings(prompt_obj, ch))
                note = audit_existing_runs_note(prompt_obj, ch)
                if note:
                    notes.append(note)
                elif in_fullrun_menu:
                    note = fullrun_evidence_note(prompt_obj, ch)
                    if note:
                        notes.append(note)
                conf = ask_confirmation(prompt_obj, ch, notes)
                if conf == "next":
                    new_ch = navigate_next(ch)
                    if new_ch:
                        ch = new_ch
                        print(f"  Переключено на: {ch.chapter_id_full}")
                    needs_confirm = False
                    continue
                if conf == "prev":
                    new_ch = navigate_prev(ch)
                    if new_ch:
                        ch = new_ch
                        print(f"  Переключено на: {ch.chapter_id_full}")
                    needs_confirm = False
                    continue
                if not conf:
                    prompt_index = None  # Сбрасываем, чтобы вернуться в меню
                    continue
                needs_confirm = False

        elif action_obj is not None:
            if needs_confirm:
                notes = []
                if in_fullrun_menu:
                    notes.extend(fullrun_prereq_warnings(action_obj, ch))
                    note = fullrun_evidence_note(action_obj, ch)
                    if note:
                        notes.append(note)
                conf = ask_confirmation(action_obj, ch, notes or None)
                if conf in ("next", "prev"):
                    new_ch = navigate_next(ch) if conf == "next" else navigate_prev(ch)
                    if new_ch:
                        ch = new_ch
                        print(f"  Переключено на: {ch.chapter_id_full}")
                    action_obj = None
                    continue
                if not conf:
                    action_obj = None
                    continue
                needs_confirm = False
            # Действие запускается только после подтверждения и не создаёт
            # LLM-промпт; после запуска возвращаемся в текущее меню.
            run_action(action_obj, ch)
            action_obj = None
            input("  Нажмите Enter для возврата в меню...")
            continue

        else:
            # Навигация уже обработана выше.
            continue

        # --- 3. Генерация промпта ---
        prompt_text = generate_prompt(prompt_index, ch)
        if not prompt_text:
            prompt_index = None
            continue

        print_generation_summary(prompt_text, prompt_obj, ch)

        # --- 4. Меню после генерации ---
        while True:
            print()
            print("  1. Показать полный промпт")
            print()
            print("  2. Скопировать повторно")
            print()
            print("  3. Сгенерировать для следующей главы")
            print()
            print("  4. Сгенерировать для предыдущей главы")
            print()
            print("  5. Следующий промпт (фаза)")
            print()
            print("  6. Вернуться в меню")
            print()
            raw = input("  Выберите (1-6): ").strip()

            if raw == "1":
                show_generated_prompt(prompt_text, prompt_obj, ch)
            elif raw == "2":
                if copy_to_clipboard(prompt_text):
                    print("  Промпт повторно скопирован в буфер обмена.")
                else:
                    print("  Не удалось скопировать промпт автоматически.")
            elif raw in ("3", "4"):
                new_ch = navigate_next(ch) if raw == "3" else navigate_prev(ch)
                if not new_ch:
                    print("  Отменено.")
                    continue
                ch = new_ch
                new_text = generate_prompt(prompt_index, ch)
                if not new_text:
                    print("  Ошибка генерации.")
                    prompt_index = None
                    break
                prompt_text = new_text
                print_generation_summary(prompt_text, prompt_obj, ch)
            elif raw == "5":
                if in_fullrun_menu:
                    step = fullrun_next_step("prompt", prompt_index)
                    if step is None:
                        print("  Это последняя фаза полного прогона главы.")
                        print("  Вернитесь в меню (пункт 6).")
                        continue
                    if step[0] == "action":
                        print("  Следующая фаза — техническое действие "
                              f"«{ACTIONS[step[1]].name}».")
                        print("  Вернитесь в меню (пункт 6) и выберите её.")
                        continue
                    nxt = step[1]
                else:
                    nxt = next_prompt_index(prompt_index)
                    if nxt is None:
                        print(f"  Это последний промпт раздела «{PROMPTS[prompt_index].group}».")
                        print("  Вернитесь в меню (пункт 6).")
                        continue
                # Переход к следующей фазе/промпту: показываем подтверждение.
                prompt_index = nxt
                prompt_obj = PROMPTS[nxt]
                needs_confirm = True
                break
            elif raw in ("6", "q", ""):
                prompt_index = None  # Сбрасываем, чтобы вернуться в меню
                needs_confirm = True
                break
            else:
                print("  Введите число от 1 до 6.")

# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Dry-run SMA: печатает self-test A / B / Analyzer и выходит, ничего не
    # создавая (перевод и audit-файлы не затрагиваются).
    if "--self-test-sma" in sys.argv:
        sys.exit(run_sma_self_test(sys.argv))
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Выход.")
    except Exception as exc:
        print()
        print("Произошла ошибка:")
        print()
        print(f"  {type(exc).__name__}: {exc}")
        print()
        input("Нажмите Enter для выхода...")