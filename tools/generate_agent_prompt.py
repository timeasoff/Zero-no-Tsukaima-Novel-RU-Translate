#!/usr/bin/env python3
"""
Генератор промптов для AI-агента проекта AINovelEdit.
Основные возможности:
- выбор режима через числовой ввод в консоли;
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
  output/_audit/sma/<chapter>/<a|b|c|analysis|precheck>/);
- автоматическое копирование готового промпта в буфер обмена;
- сохранение готового промпта в markdown-файл `agent_prompt.md`
  в корне проекта, на который можно сослаться в задаче агенту
  (файл в .gitignore, перезаписывается при каждой генерации).
Запускать из корня проекта:
python tools/generate_agent_prompt.py
"""
from __future__ import annotations

import base64
import os
import re
import subprocess
import sys
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
# Готовый промпт-инструкция сохраняется в корне проекта под этим именем
# (md-файл добавлен в .gitignore, перезаписывается при каждой генерации).
PROMPT_FILE_NAME = "agent_prompt.md"
PROMPT_FILE = os.path.join(ROOT, PROMPT_FILE_NAME)

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
SMA_KINDS = ("a", "b", "c", "analysis")   # типы результатов внутри главы
# Общий Omission Pre-check (scripts/omission_precheck.py) кладёт evidence в
# отдельный каталог главы; это НЕ каталог аудитора и НЕ run_id-результат.
SMA_PRECHECK_KIND = "precheck"
SMA_PRECHECK_FILE = "omission-precheck.json"
_SMA_ISSUED_IDS: set[str] = set()         # гарантия уникальности в процессе

# Формулировки изоляции (используются и в промптах, и в self-test).
SMA_AUTONOMY_NOTE = (
    "РАБОТАЙ АВТОНОМНО. Все данные для аудита приведены в этом задании. "
    "Не перечисляй содержимое каталогов и не открывай никакие файлы, кроме "
    "перечисленных в задании."
)
SMA_OWN_FILE_NOTE = (
    "Единственный файл, который ты создаёшь, — результат этого запуска "
    "(см. OUTPUT FILE). Любые другие файлы в папке результата в задание не "
    "входят: не читай их, не сравнивай с ними свой результат и не делай "
    "выводов из их наличия или отсутствия."
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
    """Уже существующие run_id результатов A/B/C/Analyzer для этой главы.

    Используется Analyzer'ом: он учитывает ВСЕ выбранные запуски, а не
    только последний. Ничего не создаёт и не изменяет.
    """
    folder = sma_chapter_dir(ch, kind)
    if not os.path.isdir(folder):
        return []
    ids = [os.path.splitext(name)[0] for name in os.listdir(folder)
           if name.lower().endswith(".json")]
    return sorted(ids)

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
- курсив `*…*` и blockquote `>` — НЕ «следы Markdown», это разметка
по russian-prose-rules;
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
каталог калькированных реплик, обязательные разделители сцен). Текст
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
5. РАЗДЕЛИТЕЛИ СЦЕН: сверись с JA/RU-translates: каждая смена
   локации/времени/ракурса, отмеченная в оригинале, должна получить
   `---` в output (пустая строка до и после — проверяется format_scan,
   kind=paragraph). Отсутствие `---` при явной смене сцены — WARNING,
   FIX: вставить разделитель через fix_block.py. Точный смысл границы
   — по JA; сомнение → `<!-- ??? -->`.
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

{semantic_audit_context(ch)}

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
  ]
}}

ПРАВИЛА:
- severity: только ERROR / WARNING / CANDIDATE.
- Если проблем нет — "findings": [] (пустой массив, объект всё равно обязателен).
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

{semantic_audit_context(ch)}

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
- намерение персонажа, стоящее за действием или репликой.

НАПРАВЛЕНИЕ ПРОВЕРКИ: JA → RU. Сначала установи смысл японского фрагмента
(с учётом контекста), затем сверь, как этот смысл передан в текущем русском
результате.

ЧТО НЕ ВХОДИТ В ЗАДАЧУ (не проверяй и не фиксируй):
- грамматика (согласование, управление, падежи) — это russian-grammar-control;
- стиль (тавтология, повторы, кальки) — это russian-style-audit;
- оформление текста (кавычки, тире, курсив) — это russian-prose-rules;
- общее «очеловечивание» текста — это russian-humanizer;
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
  ]
}}

ПРАВИЛА:
- severity: только ERROR / WARNING / CANDIDATE.
- Если проблем нет — "findings": [] (пустой массив, объект всё равно обязателен).
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

{semantic_audit_context(ch)}

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
  местоименные связи, обычная логика событий, идиомы, метафоры — это слой
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
  ]
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
    результаты независимых аудитов A/B/C (выбранные запуски ЭТОЙ главы). Он
    самостоятельно сверяет candidates с JA/RU, исправляет только
    CONFIRMED_ERROR и записывает спорные случаи в отчёт analysis/.

    Два режима, логика одного и того же:
    - A+B — если запусков C ещё нет (старые главы / C не запускался);
    - A+B+C — если запуски C существуют.
    Наличие C не обязательно; majority vote запрещён в обоих режимах.

    ``runs`` — только для self-test (симуляция содержимого каталогов a/b/c);
    в рабочем режиме список запусков читается с диска.
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
Слепой вывод Фазы 1 (твоё собственное ПЕРВОНАЧАЛЬНОЕ заключение, файл
{an_dir}*.phase1.json — сделано БЕЗ evidence):
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
- Учитывай ВСЕ выбранные запуски, а не только последний. Если в a/, b/ или c/
  появились другие <run_id>.json — включи их как выбранные запуски.
- Результаты ДРУГИХ глав не используй: анализируй только эту главу.
- Если в a/, b/ и c/ нет ни одного <run_id>.json — сообщи, что сначала нужно
  выполнить аудит, и остановись (правки не вноси)."""

def _sma_analyzer_rules() -> str:
    return """ШАГ 0 — УБЕДИСЬ, ЧТО ФАЗА 1 УЖЕ ВЫПОЛНЕНА (слепо, без evidence)
Фаза 1 выполнялась ОТДЕЛЬНЫМ заданием, куда не передавалось НИКАКОГО
evidence: ни findings A/B/C, ни данных детерминированного pre-check, ни
происхождения находок, ни прежних analysis-результатов. Её вывод лежит в
analysis/*.phase1.json — это твоё СОБСТВЕННОЕ ПЕРВОНАЧАЛЬНОЕ заключение
по чистой сверке JA → RU: есть ли mismatch, есть ли OMISSION, есть ли
добавленный смысл, есть ли другие существенные ошибки.
- Если такого файла нет — сначала выполни Фазу 1 (только JA + RU + контекст)
  и лишь после этого возвращайся к Фазе 2.
- Вывод Фазы 1 — входные данные, а НЕ evidence и не чужое мнение: он не
  голосует и не является основанием для правки.

ШАГ 1 — СБОР EVIDENCE (Фаза 2 начинается здесь)
Собери ВСЕ findings из всех выбранных запусков A, B и C ЭТОЙ главы плюс
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

СТАТУСЫ (каждому candidate обязателен один)
- CONFIRMED_ERROR — ясная смысловая ошибка: JA однозначен, RU передаёт другой
  смысл, исправление формулируется однозначно → МОЖНО исправлять.
- DISPUTED — расхождение мнений аудиторов или неоднозначность JA → НЕ исправлять.
- FALSE_POSITIVE — finding не подтверждается → НЕ исправлять.
- OPTIONAL — допустимое улучшение, текущий перевод правилен → НЕ исправлять.

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
    return f"""ФОРМАТ РЕЗУЛЬТАТА (ровно один JSON-объект, без markdown-обёртки):
{{
  "analysis_id": "{analysis_id}",
  "chapter": "{chap}",
  "inputs": {{
    "a_runs": [{a_json}],
    "b_runs": [{b_json}],
    "c_runs": [{c_json}],
    "precheck": {pc_input}
  }},
  "results": [
    {{
      "block": 11,
      "candidate_id": "C-11-01",
      "sources": {{ "a": ["<run_id>"], "b": ["<run_id>"], "c": ["<run_id>"], "precheck": false }},
      "source": "JA fragment",
      "current": "RU fragment",
      "status": "CONFIRMED_ERROR",
      "reason": "Обоснование Analyzer",
      "suggestion": "Исправленный вариант",
      "action": "FIXED",
      "before": "RU-блок до правки (обязательно для FIXED)",
      "after": "RU-блок после правки (обязательно для FIXED)"
    }}
  ]
}}

Разрешённые status: CONFIRMED_ERROR / DISPUTED / FALSE_POSITIVE / OPTIONAL.
Разрешённые action: FIXED / REPORT_ONLY / PRESERVED.
- FIXED — только для CONFIRMED_ERROR (правка внесена через fix_block.py).
- REPORT_ONLY — DISPUTED / OPTIONAL (в отчёт, перевод не менять).
- PRESERVED — FALSE_POSITIVE (оставлено как есть).
Для каждого FIXED обязательны before и after.
- inputs.a_runs / inputs.b_runs / inputs.c_runs — все выбранные запуски этого
  запуска анализа (в режиме A+B поле c_runs пустое).
- inputs.precheck — путь к evidence детерминированного omission pre-check
  либо null, если pre-check для главы не прогонялся (это норма).
- sources каждого candidate — из каких запусков A/B/C он собран; пустой
  список означает, что этот аудит находку не находил.
- sources.precheck — маркер того, что candidate пришёл от omission pre-check:
  это evidence, а не голос (как и sources.a/b/c).

OUTPUT FILES (этой главы, запуск {analysis_id})
JSON: {out_rel}
MD:   {out_md_rel}
(абсолютные пути: {out_abs} и {out_md_abs})
JSON — машинный результат; MD — человекочитаемый отчёт с таблицей по каждому
candidate (block, candidate_id, sources A/B/C, status, reason, action,
before/after для FIXED; отдельно сводка по DISPUTED и OPTIONAL).
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
    ),
    PromptInfo(
        "Решения пользователя (OPEN / PROVISIONAL)",
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
    ),
    # GAP-аудит (prompt_gap_audit) УДАЛЁН из активного меню: это LEGACY.
    # Поиск пропусков выполняет общий Omission Pre-check
    # (AINovelEdit/scripts/omission_precheck.py) → evidence для Analyzer.
    # Функция prompt_gap_audit сохранена ниже как исторический задел и из
    # меню недоступна (аналогично prompt_dual_semantic_audit).
    PromptInfo(
        "Реконтроль готовой главы (новые правила)",
        "Проверка уже переведённой и прошедшей аудит главы по новым правилам",
        """
        Проверяет главу, которая уже полностью переведена и прошла полный
        аудит, но делала это ДО введения новых правил проекта: согласования
        рода в обращениях («понял, Луиза?»), каталога машинных кальк
        («полегчайте не смогу», «им не по дороге»), регистра титулов в прямой
        речи («ваше высочество» → «Ваше Высочество»), обязательных разделителей
        сцен `---`, курсива внутренней речи, отбивки маркеров блоков
        (blockgap), реплик в кавычках вместо тире (quotespeech), мыслей,
        слитых с нарративом (thoughtinline), искажений имён (namespell) и
        падежа геоназваний («до самого Тристейна»).
        Это НЕ повторный полный аудит: текст переписывается только там, где
        новые проверки дают подтверждённого кандидата. Смысловая сверка с JA/EN
        ведётся точечно — только для кандидатов, требующих решения по смыслу.
        Сначала запускаются механические предфильтры (format_scan, style_scan),
        затем ручной разбор их кандидатов и проход по контрастивной таблице
        эталонных правок. Каждый кандидат получает disposition в отчёте;
        ноль правок — допустимый итог.
        Использовать для ранее завершённых глав, чтобы прогнать их через
        правила, появившиеся после их закрытия.
        """.strip(),
        prompt_rules_recheck,
    ),
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
        Изоляция проверяется self-test (tools/generate_agent_prompt.py
        --self-test-sma).
        """,
        prompt_semantic_analyzer_phase1,
    ),
    PromptInfo(
        "Смысловой анализатор — Фаза 2 (evidence review)",
        "Analyzer: сверяет свой слепой вывод Фазы 1 с A/B/C + omission pre-check",
        """
        Вторая фаза: сюда сознательно передаются ВСЕ evidence — findings A,
        B и C, а также evidence детерминированного omission pre-check
        (scripts/omission_precheck.py) — и собственное слепое заключение
        Фазы 1 (analysis/*.phase1.json).

        Analyzer сопоставляет evidence со своим первоначальным выводом:
        он может подтвердить finding, отвергнуть его, создать нового или
        принять кандидат pre-check, которого сам в Фазе 1 не заметил.

        Pre-check — evidence, а не голос и не Auditor D; A/B/C — тоже
        evidence. Majority vote запрещён: «A+B+C согласны → ошибка» и
        «только C нашёл → false positive» одинаково недопустимы.

        Два режима сохранены: A + B (C не запускался) и A + B + C;
        отсутствие pre-check не мешает работе. Статусы CONFIRMED_ERROR /
        DISPUTED / FALSE_POSITIVE / OPTIONAL; правка только через
        fix_block.py. Результат: output/_audit/sma/<chapter>/analysis/.

        Запускать ПОСЛЕ «Смысловой анализатор — Фаза 1».
        """,
        prompt_semantic_analyzer,
    ),
]

# ============================================================================
# МЕНЮ (числовой ввод)
# ============================================================================
def print_menu(ch: Chapter) -> None:
    """Вывести главное меню."""
    print()
    print("AINovelEdit — генератор промптов")
    separator()
    print(f"  Текущая глава: {ch.chapter_id_full}")
    separator()
    print()
    for i, p in enumerate(PROMPTS, start=1):
        print(f"  {i:2d}. {p.title}")
        print(f"      {p.description}")
        print()  # <-- Возвращаем отступ между пунктами
        
    extra_start = len(PROMPTS) + 1
    print(f"  {extra_start}. Следующая глава")
    print(f"  {extra_start + 1}. Предыдущая глава")
    print(f"  {extra_start + 2}. Изменить том / главу")
    print(f"  {extra_start + 3}. Выход")
    print()

def choose_prompt(ch: Chapter) -> int | str:
    """
    Запросить выбор режима числом.
    Возвращает:
    int      — индекс в PROMPTS (от 0)
    "next"   — следующая глава
    "prev"   — предыдущая глава
    "change" — сменить главу
    "quit"   — выход
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

        if 1 <= number <= len(PROMPTS):
            return number - 1
        if number == len(PROMPTS) + 1:
            return "next"
        if number == len(PROMPTS) + 2:
            return "prev"
        if number == len(PROMPTS) + 3:
            return "change"
        if number == len(PROMPTS) + 4:
            return "quit"

        print(f"  Введите число от 1 до {len(PROMPTS) + 4}.")
        print()
        input("  Нажмите Enter...")

# ============================================================================
# ПОДТВЕРЖДЕНИЕ
# ============================================================================
def ask_confirmation(prompt: PromptInfo, ch: Chapter) -> bool | str:
    """
    Показать описание режима и спросить подтверждение.
    Возвращает True (да), False (нет), "next" (следующая), "prev" (предыдущая).
    """
    print()
    print("Подтверждение запуска")
    separator()
    print()
    print(f"  Режим: {prompt.title}")
    print(f"  Глава: {ch.chapter_id_full}")
    print()
    print("  Кратко:")
    print_wrapped(prompt.description, indent="    ")
    print()
    print("  Что делает этот режим:")
    print_wrapped(prompt.guide, indent="    ")
    print()
    separator()
    print()
    while True:
        raw = input(
            f'Запустить "{prompt.title}" для {ch.chapter_id_full}? '
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

    # Обработка одного блока (индекс 8).
    if prompt_index == 8:
        print()
        print("Обработка одного блока")
        separator()
        print()
        print(f"  Том:   {ch.volume_id}")
        print(f"  Глава: {ch.chapter_id}")
        print()
        block_number = ask_block_number()
        return prompt_one_block(ch, block_number)

    return None

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
def save_prompt_to_file(
    prompt_text: str,
    prompt: PromptInfo,
    ch: Chapter,
) -> str | None:
    """
    Сохранить готовый промпт в markdown-файл в корне проекта.

    Файл перезаписывается при каждой генерации, чтобы на него можно
    было сослаться в задаче агенту («см. agent_prompt.md»).
    Возвращает путь к файлу либо None при ошибке записи.
    """
    header = (
        "# Промпт-инструкция для агента\n"
        "\n"
        f"- Режим: {prompt.title}\n"
        f"- Глава: {ch.chapter_id_full}\n"
        f"- Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        "- Источник: tools/generate_agent_prompt.py\n"
        "\n"
        "---\n"
        "\n"
    )
    try:
        with open(PROMPT_FILE, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(header + prompt_text + "\n")
    except OSError:
        return None
    return PROMPT_FILE

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
    })
    pan_ab = prompt_semantic_analyzer(ch, runs={
        "a": sma_existing_runs(ch, "a"),
        "b": sma_existing_runs(ch, "b"),
        "c": [],
    })
    pan1 = prompt_semantic_analyzer_phase1(ch)
    # глава без pre-check: проверка, что его отсутствие не ломает Фазу 2
    ch_nopc = Chapter(99, "99")
    pan_nopc = prompt_semantic_analyzer(ch_nopc, runs={
        "a": ["sim-x"], "b": ["sim-x"], "c": []})
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
        ("Analyzer: reads selected A results — YES",
         a_dir in pan, a_dir),
        ("Analyzer: reads selected B results — YES",
         b_dir in pan, b_dir),
        ("Analyzer: reads selected C results — YES",
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
        ("Analyzer: статусы сохранены — YES",
         all(s in pan for s in ("CONFIRMED_ERROR", "DISPUTED",
                                "FALSE_POSITIVE", "OPTIONAL")),
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
        ("Фаза 1: в промпте НЕТ прежних analysis-результатов — YES",
         not _sma_hits(pan1, [f"{chap}/analysis/{r}." for r in
                              sma_existing_runs(ch, "analysis")]),
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
        ("Фаза 1: содержит JA + RU + контекст и вывод phase1 — YES",
         ch.ja_path in pan1 and ch.output_path in pan1
         and ch.merged_path in pan1 and ".phase1.json" in pan1,
         ""),
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
        ("Фаза 2: ссылка на слепой вывод Фазы 1 — YES",
         "*.phase1.json" in pan and "ПЕРВОНАЧАЛЬНОЕ" in pan, ""),
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
        # ---- LEGACY: GAP-аудит не активен, функция сохранена ----
        ("prompt_gap_audit: больше не в активном меню PROMPTS — YES",
         not any(getattr(p, "generator", None) is prompt_gap_audit
                 for p in PROMPTS)
         and not any("GAP" in p.title for p in PROMPTS),
         f"пунктов меню: {len(PROMPTS)}"),
        ("prompt_gap_audit: функция сохранена (legacy-задел) — YES",
         callable(prompt_gap_audit), ""),
        ("Меню: пункт «Обработка одного блока» остался на индексе 8 — YES",
         len(PROMPTS) > 8 and PROMPTS[8].title == "Обработка одного блока",
         f"PROMPTS[8] = {PROMPTS[8].title if len(PROMPTS) > 8 else '(нет)'}"),
        ("Меню: обе фазы Analyzer присутствуют — YES",
         any(p.generator is prompt_semantic_analyzer_phase1 for p in PROMPTS)
         and any(p.generator is prompt_semantic_analyzer for p in PROMPTS),
         ""),
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
        print("Использование: python tools/generate_agent_prompt.py "
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
    
    prompt_index = None
    prompt_obj = None
    prompt_text = None

    while True:
        # Если промпт не выбран или сброшен — показываем главное меню
        if prompt_index is None:
            result = choose_prompt(ch)

            if result == "quit":
                print()
                print("Выход.")
                return

            if result == "change":
                ch = ask_chapter()
                continue

            if result == "next":
                new_ch = navigate_next(ch)
                if new_ch:
                    ch = new_ch
                    print(f"  Переключено на: {ch.chapter_id_full}")
                else:
                    print("  Отменено.")
                continue

            if result == "prev":
                new_ch = navigate_prev(ch)
                if new_ch:
                    ch = new_ch
                    print(f"  Переключено на: {ch.chapter_id_full}")
                else:
                    print("  Отменено.")
                continue

            prompt_index = result
            prompt_obj = PROMPTS[prompt_index]

            # Подтверждение
            conf = ask_confirmation(prompt_obj, ch)
            if conf == "next":
                new_ch = navigate_next(ch)
                if new_ch:
                    ch = new_ch
                    print(f"  Переключено на: {ch.chapter_id_full}")
                continue
            if conf == "prev":
                new_ch = navigate_prev(ch)
                if new_ch:
                    ch = new_ch
                    print(f"  Переключено на: {ch.chapter_id_full}")
                continue
            if not conf:
                prompt_index = None  # Сбрасываем, чтобы вернуться в меню
                continue

        # Генерация промпта
        prompt_text = generate_prompt(prompt_index, ch)
        if not prompt_text:
            prompt_index = None
            continue

        # Копирование в буфер
        print()
        separator()
        print()
        print(f"  Режим: {prompt_obj.title}")
        print(f"  Глава: {ch.chapter_id_full}")
        print()
        
        if copy_to_clipboard(prompt_text):
            print("  Промпт скопирован в буфер обмена.")
        else:
            print("  Не удалось скопировать промпт автоматически.")
        if save_prompt_to_file(prompt_text, prompt_obj, ch):
            print(f"  Промпт сохранён в файл: {PROMPT_FILE}")
            print(f"  На него можно сослаться: {PROMPT_FILE_NAME}")
        else:
            print(f"  Не удалось сохранить промпт в {PROMPT_FILE_NAME}.")
        print()
        separator()

        # Меню после генерации
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
            print("  5. Вернуться в меню")
            print()
            raw = input("  Выберите (1-5): ").strip()

            if raw == "1":
                show_generated_prompt(prompt_text, prompt_obj, ch)
            elif raw == "2":
                if copy_to_clipboard(prompt_text):
                    print("  Промпт повторно скопирован в буфер обмена.")
                else:
                    print("  Не удалось скопировать промпт автоматически.")
            elif raw == "3":
                new_ch = navigate_next(ch)
                if new_ch:
                    ch = new_ch
                    prompt_text = generate_prompt(prompt_index, ch)
                    if prompt_text:
                        copy_to_clipboard(prompt_text)
                        save_prompt_to_file(prompt_text, prompt_obj, ch)
                        print(f"\n  Сгенерировано для {ch.chapter_id_full}: промпт скопирован и сохранён в {PROMPT_FILE_NAME}")
                    else:
                        print("  Ошибка генерации.")
                        prompt_index = None
                        break
                else:
                    print("  Отменено.")
            elif raw == "4":
                new_ch = navigate_prev(ch)
                if new_ch:
                    ch = new_ch
                    prompt_text = generate_prompt(prompt_index, ch)
                    if prompt_text:
                        copy_to_clipboard(prompt_text)
                        save_prompt_to_file(prompt_text, prompt_obj, ch)
                        print(f"\n  Сгенерировано для {ch.chapter_id_full}: промпт скопирован и сохранён в {PROMPT_FILE_NAME}")
                    else:
                        print("  Ошибка генерации.")
                        prompt_index = None
                        break
                else:
                    print("  Отменено.")
            elif raw in ("5", "q", ""):
                prompt_index = None  # Сбрасываем, чтобы вернуться в главное меню
                break
            else:
                print("  Введите число от 1 до 5.")

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