#!/usr/bin/env python3
"""
Диспетчер крупных задач проекта AINovelEdit (оркестрация субагентов).

НАЗНАЧЕНИЕ
==========
Агент-оркестратор получает СВОБОДНУЮ задачу («проверь том 3 целиком»,
«продолжи перевод с последней завершённой главы», «что не переведено»),
сам разбивает её на субзадачи, генерирует готовые промпты (через
tools/agent_workflow.py) и запускает субагентов. Этот скрипт — внешняя
ПАМЯТЬ оркестратора: он детерминированно фиксирует, что запущено, что
завершено, что оборвалось, и переживает компактизацию контекста агента.

Почему внешняя память: сессии субагентов могут обрываться (обрыв коннекта,
падение, компактизация). Оркестратор не должен полагаться на свою память о
запущенном — только на реестр. Обрыв субагента — НЕ ошибка работы: скрипт
помечает субзадачу как INTERRUPTED, а команда `resume` генерирует промпт
ПРОДОЛЖЕНИЯ (не перезапуска с нуля): субагент сначала проверяет, что уже
сделано, и доделывает недостающее.

РЕЕСТР (источник истины)
========================
AINovelEdit/output/_dispatch/ledger.json  — машиночитаемый реестр задач и
  субзадач с историей попыток; создаётся/обновляется только этим скриптом.
AINovelEdit/output/_dispatch/TASKS.md     — человекочитаемая сводка,
  перезаписывается при каждом изменении реестра.

КОМАНДЫ (все недетерминированные, без input())
==============================================
  status [--volume N] [--json]   состояние глав проекта (что переведено,
                                 что не переведено, где продолжать);
                                 без субагентов, чистое сканирование файлов
  list                           список задач и субзадач реестра
  new "текст задачи"             создать задачу (возвращает TASK-ID)
  plan TASK --kind SLUG[,SLUG] --volume N --chapter CH[,CH] | --all
                                 поставить субзадачи (cartesian: kinds × chapters)
  launch SUB [SUB ...]           сгенерировать промпт и пометить запуск;
                                 печатает файл промпта для субагента
  done SUB [--note ...]          субагент вернулся, работа подтверждена
  fail SUB --note ...            субагент вернулся с ошибкой
  close TASK [--status done|cancelled] [--force]
                                 закрыть задачу целиком
  verify [TASK] [--json] [--mark]
                                 сверить реестр с файлами проекта:
                                 DONE / PROGRESS / INTERRUPTED; --mark
                                 переводит running→done/interrupted
  resume SUB [SUB ...]           прерванная/упавшая субзадача: новая попытка
                                 с промптом «продолжи с места обрыва»
  recover                        verify --mark + сводка незавершённого;
                                 ОБЯЗАТЕЛЬНЫЙ первый запуск в каждой сессии
                                 оркестратора (в т.ч. после компактизации)
  pending                        короткая сводка «что не завершено»
  show TASK                      детали задачи
  kinds                          справочник промпт-режимов (slugs)
  self-test                      самопроверка логики (во временной папке)

ЗАПУСК
======
Из корня проекта:  python tools/dispatch.py <команда>
Режим оркестратора описан в AINovelEdit/.agents/skills/dispatcher/SKILL.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AINOVELEDIT = os.path.join(ROOT, "AINovelEdit")

# Реестр диспетчера. Отдельная папка output/_dispatch/: реестр — служебные
# данные оркестрации, а не результат перевода. Переопределяется переменной
# окружения DISPATCH_DIR (используется self-test, чтобы не трогать реестр).
DISPATCH_DIR_ENV = "DISPATCH_DIR"
LEDGER_NAME = "ledger.json"
TASKS_MD_NAME = "TASKS.md"

# Группы промпт-режимов (slugs из tools/agent_workflow.py PROMPTS).
# Тип определяет, КАК проверяется завершение субзадачи (см. verify_subtask).
SMA_SLUGS = {"sma-a", "sma-b", "sma-c", "analyzer-phase1", "analyzer-phase2"}
WORK_SLUGS = {"first-launch", "continue", "one-block", "resolve-decisions",
              "encoding"}
AUDIT_SLUGS = {"full-audit", "quick-audit", "grammar-audit", "style-audit",
               "humanizer", "alignment"}

# Пути результатов смыслового аудита внутри промпта (OUTPUT FILE).
SMA_PATH_RE = re.compile(r"output/_audit/sma/[A-Za-z0-9._\-/]+\.(?:json|md)")

# Статусы субзадач.
ST_PLANNED = "planned"          # поставлена, промпт ещё не сгенерирован
ST_RUNNING = "running"          # промпт сгенерирован, запуск зарегистрирован
ST_DONE = "done"                # подтверждено (orchestrator или verify --mark)
ST_FAILED = "failed"            # субагент вернулся с ошибкой
ST_INTERRUPTED = "interrupted"  # запуск оборвался: нужен resume

# Статусы задач.
T_OPEN = "open"
T_DONE = "done"
T_CANCELLED = "cancelled"

# ============================================================================
# УТИЛИТЫ
# ============================================================================
def now_iso() -> str:
    """Локальное время в формате реестра: YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def parse_iso(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return None

def mtime_of(path: str) -> float:
    """mtime файла или 0.0, если файла нет."""
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0

def exists(path: str) -> bool:
    return os.path.exists(path)

def rel_to_root(path: str) -> str:
    """Путь относительно корня проекта с прямыми слэшами (для реестра)."""
    try:
        return os.path.relpath(path, ROOT).replace(os.sep, "/")
    except ValueError:
        return path.replace(os.sep, "/")

def atomic_write(path: str, text: str) -> None:
    """Атомарная запись UTF-8: временный файл + os.replace."""
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".tmp-", suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            with contextlib_suppress():
                os.remove(tmp)

import contextlib

@contextlib.contextmanager
def contextlib_suppress():
    try:
        yield
    except OSError:
        pass

def load_workflow():
    """Ленивый импорт tools/agent_workflow.py (генераторы промптов)."""
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    import agent_workflow  # type: ignore
    return agent_workflow

def workflow_slug_map() -> dict[str, object]:
    """slug → PromptInfo из tools/agent_workflow.py."""
    aw = load_workflow()
    return {info.slug: info for info in aw.PROMPTS if getattr(info, "slug", "")}

def make_chapter(volume: int, chapter_raw: str):
    """Глава в формате agent_workflow.Chapter (принимает «5», «ch05», «epilogue»)."""
    aw = load_workflow()
    raw = str(chapter_raw).strip()
    if raw.lower().endswith(".md"):
        raw = raw[:-3]
    match = re.match(r"^v\d+-(.*)$", raw, re.IGNORECASE)
    if match:
        raw = match.group(1)
    if raw.lower().startswith("ch") and raw[2:].isdigit():
        raw = raw[2:]
    return aw.Chapter(volume=int(volume), chapter_raw=raw)

# ============================================================================
# РЕЕСТР
# ============================================================================
def dispatch_dir() -> str:
    override = os.environ.get(DISPATCH_DIR_ENV)
    if override:
        return os.path.abspath(override)
    return os.path.join(AINOVELEDIT, "output", "_dispatch")

def ledger_path() -> str:
    return os.path.join(dispatch_dir(), LEDGER_NAME)

def tasks_md_path() -> str:
    return os.path.join(dispatch_dir(), TASKS_MD_NAME)

def empty_ledger() -> dict:
    return {"version": 1, "created": now_iso(), "tasks": []}

def load_ledger() -> dict:
    path = ledger_path()
    if not os.path.isfile(path):
        return empty_ledger()
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ОШИБКА: реестр повреждён ({rel_to_root(path)}): {exc}")
        print("Исправь файл вручную или удали его (задачи будут потеряны).")
        raise SystemExit(2)
    if not isinstance(data, dict) or "tasks" not in data:
        raise SystemExit(f"ОШИБКА: неожиданная структура реестра {rel_to_root(path)}")
    return data

def save_ledger(ledger: dict) -> None:
    path = ledger_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = json.dumps(ledger, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".tmp-",
                               suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            with contextlib_suppress():
                os.remove(tmp)
    write_tasks_md(ledger)

def write_tasks_md(ledger: dict) -> None:
    """Человекочитаемая сводка реестра (перезаписывается целиком)."""
    lines = ["# Реестр задач диспетчера", "",
             f"Обновлено: {now_iso()}", "",
             "Генерируется автоматически командой `python tools/dispatch.py`. "
             "Не редактируй вручную.", ""]
    if not ledger["tasks"]:
        lines += ["_Задач нет._", ""]
    for task in ledger["tasks"]:
        lines += [f"## {task['id']} — {task['status'].upper()}", "",
                  task.get("text", ""), ""]
        subtasks = task.get("subtasks", [])
        if not subtasks:
            lines += ["_Субзадач нет._", ""]
            continue
        lines += ["| ID | Режим | Глава | Статус | Попыток | Промпт |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for sub in subtasks:
            chapter = sub.get("chapter_id", "?")
            lines.append(
                f"| {sub['id']} | {sub.get('kind', '?')} | {chapter} | "
                f"{sub['status']} | {len(sub.get('attempts', []))} | "
                f"`{sub.get('prompt_file') or '—'}` |")
        lines.append("")
        notes = [f"- {sub['id']}: {sub['note']}"
                 for sub in subtasks if sub.get("note")]
        if notes:
            lines += ["Заметки:"] + notes + [""]
    atomic_write(tasks_md_path(), "\n".join(lines) + "\n")

# ----------------------------------------------------------------------------
# Доступ к записям
# ----------------------------------------------------------------------------
def find_task(ledger: dict, task_id: str) -> dict:
    wanted = task_id.strip().upper()
    for task in ledger["tasks"]:
        if task["id"].upper() == wanted:
            return task
    raise SystemExit(f"ОШИБКА: задача {task_id} не найдена. См. `list`.")

def all_subtasks(ledger: dict) -> list[tuple[dict, dict]]:
    result = []
    for task in ledger["tasks"]:
        for sub in task.get("subtasks", []):
            result.append((task, sub))
    return result

def find_subtask(ledger: dict, sub_id: str) -> tuple[dict, dict]:
    wanted = sub_id.strip().upper()
    for task, sub in all_subtasks(ledger):
        if sub["id"].upper() == wanted:
            return task, sub
    raise SystemExit(f"ОШИБКА: субзадача {sub_id} не найдена. См. `list`.")

def next_task_id(ledger: dict) -> str:
    numbers = [int(m.group(1)) for task in ledger["tasks"]
               if (m := re.match(r"^T-(\d+)$", task["id"])) ]
    return f"T-{(max(numbers) + 1 if numbers else 1):04d}"

def next_subtask_id(task: dict) -> str:
    numbers = [int(m.group(1)) for sub in task.get("subtasks", [])
               if (m := re.match(r"^.+-S(\d+)$", sub["id"]))]
    return f"{task['id']}-S{(max(numbers) + 1 if numbers else 1)}"

# ============================================================================
# СТАТУС ПРОЕКТА (что переведено / не переведено / где продолжать)
# ============================================================================
FILE_RE = re.compile(r"^v(\d+)-(.+)\.md$")

def volume_chapters(volume: int) -> list[str]:
    """Главы тома: объединение translates/ja и output (без ведущих нулей тома).

    Порядок: числовые главы по номеру, затем именованные (prologue,
    epilogue, afterword) по алфавиту. Пустой список — том не найден.
    """
    found: dict[str, None] = {}
    for folder in (os.path.join(AINOVELEDIT, "translates", "ja"),
                   os.path.join(AINOVELEDIT, "output")):
        if not os.path.isdir(folder):
            continue
        for name in sorted(os.listdir(folder)):
            match = FILE_RE.match(name)
            if not match or int(match.group(1)) != volume:
                continue
            found.setdefault(match.group(2), None)

    def sort_key(chapter: str) -> tuple[int, int | str]:
        return (0, int(chapter)) if chapter.isdigit() else (1, chapter)

    return sorted(found, key=sort_key)

def known_volumes() -> list[int]:
    volumes: set[int] = set()
    for folder in (os.path.join(AINOVELEDIT, "translates", "ja"),
                   os.path.join(AINOVELEDIT, "output")):
        if not os.path.isdir(folder):
            continue
        for name in os.listdir(folder):
            match = FILE_RE.match(name)
            if match:
                volumes.add(int(match.group(1)))
    return sorted(volumes)

def completed_volumes() -> set[int]:
    """Тома из completed.md (таблица «Завершённые тома»; источник истины)."""
    path = os.path.join(AINOVELEDIT, "completed.md")
    if not os.path.isfile(path):
        return set()
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return set()
    volumes: set[int] = set()
    for line in text.splitlines():
        match = re.match(r"^\|\s*(\d{1,2})\s*\|", line)
        if match:
            volumes.add(int(match.group(1)))
    return volumes

def sma_runs(chapter_id: str) -> dict[str, int]:
    """Число запусков SMA по типам для главы (по файлам .json на диске)."""
    base = os.path.join(AINOVELEDIT, "output", "_audit", "sma", chapter_id)
    counts: dict[str, int] = {}
    for kind in ("a", "b", "c", "analysis"):
        folder = os.path.join(base, kind)
        if not os.path.isdir(folder):
            counts[kind] = 0
            continue
        counts[kind] = len([n for n in os.listdir(folder)
                            if n.lower().endswith(".json")
                            and not n.lower().endswith(".phase1.json")])
    analysis_dir = os.path.join(base, "analysis")
    phase1 = 0
    if os.path.isdir(analysis_dir):
        phase1 = len([n for n in os.listdir(analysis_dir)
                      if n.lower().endswith(".phase1.json")])
    counts["phase1"] = phase1
    counts["precheck"] = 1 if os.path.isfile(os.path.join(
        base, "precheck", "omission-precheck.json")) else 0
    return counts

def chapter_report(volume: int, chapter: str) -> dict:
    """Срез состояния одной главы по файлам проекта (без изменения ничего)."""
    aw = load_workflow()
    ch = aw.Chapter(volume=volume, chapter_raw=chapter)
    audit_plain = os.path.join(AINOVELEDIT, "output", "_audit",
                               f"v{volume}-{ch.chapter_id}.md")
    audit_padded = os.path.join(AINOVELEDIT, "output", "_audit",
                                f"{ch.volume_id}-{ch.chapter_id}.md")
    audit_path = audit_padded if exists(audit_padded) else audit_plain
    runs = sma_runs(f"{ch.volume_file_id}-{ch.chapter_id}")
    state = "NOT_TRANSLATED"
    if exists(ch.output_path):
        state = "TRANSLATED"
        if exists(audit_path) or any(runs[k] for k in
                                     ("a", "b", "c", "analysis", "phase1")):
            state = "AUDITED"
    return {
        "chapter_id": ch.chapter_id_full,
        "file_name": ch.file_name,
        "ja": exists(ch.ja_path),
        "en": exists(ch.en_path),
        "ru_source": exists(ch.ru_path),
        "output": exists(ch.output_path),
        "merged": exists(ch.merged_path),
        "audit": exists(audit_path),
        "log": exists(ch.log_path),
        "sma": runs,
        "state": state,
        "output_mtime": datetime.fromtimestamp(
            mtime_of(ch.output_path)).strftime("%Y-%m-%d %H:%M") if exists(
            ch.output_path) else "",
    }

def project_status(volume: int | None = None) -> list[dict]:
    volumes = [volume] if volume else known_volumes()
    report = []
    completed = completed_volumes()
    for vol in volumes:
        chapters = volume_chapters(vol)
        report.append({
            "volume": vol,
            "completed": vol in completed,
            "chapters": [chapter_report(vol, chapter) for chapter in chapters],
        })
    return report

def print_status(volume: int | None = None) -> None:
    report = project_status(volume)
    completed = completed_volumes()
    print("СОСТОЯНИЕ ПРОЕКТА (по файлам; ничего не изменено)")
    print("=" * 78)
    for block in report:
        vol = block["volume"]
        mark = " [COMPLETED]" if vol in completed else ""
        print(f"\nТом v{vol}{mark}")
        if not block["chapters"]:
            print("  (глав не найдено)")
            continue
        print(f"  {'Глава':<14}{'JA':<4}{'EN':<4}{'RU':<4}{'OUT':<5}"
              f"{'MERGE':<7}{'AUDIT':<7}{'SMA a/b/c/ana/ph1':<19}Состояние")
        untranslated = []
        last_translated = None
        for ch in block["chapters"]:
            runs = ch["sma"]
            sma = (f"{runs['a']}/{runs['b']}/{runs['c']}/"
                   f"{runs['analysis']}/{runs['phase1']}")
            flag = {"NOT_TRANSLATED": "не переведено",
                    "TRANSLATED": "переведено, без аудита",
                    "AUDITED": "переведено, аудит есть"}[ch["state"]]
            print(f"  {ch['chapter_id']:<14}"
                  f"{'✓' if ch['ja'] else '—':<4}"
                  f"{'✓' if ch['en'] else '—':<4}"
                  f"{'✓' if ch['ru_source'] else '—':<4}"
                  f"{'✓' if ch['output'] else '—':<5}"
                  f"{'✓' if ch['merged'] else '—':<7}"
                  f"{'✓' if ch['audit'] else '—':<7}"
                  f"{sma:<19}{flag}")
            if ch["output"]:
                last_translated = ch["chapter_id"]
            elif ch["ja"]:
                untranslated.append(ch["chapter_id"])
        if untranslated:
            print(f"  → не переведено: {', '.join(untranslated)}")
        if last_translated:
            print(f"  → последняя глава с результатом: {last_translated}")
    print("\nПодсказки: «продолжить перевод» — с первой не переведённой главы "
          "первого незавершённого тома;\nзавершённые тома (completed.md) не "
          "трогаются (read-only).")

# ============================================================================
# ПЛАН И ГЕНЕРАЦИЯ ПРОМПТОВ
# ============================================================================
def prompt_file_for(ch, slug: str, attempt: int) -> str:
    """Путь файла промпта (та же конвенция, что у agent_workflow).

    Попытка 1 — как в agent_workflow: agent_prompt.<chapter>.<slug>.md.
    Повторные попытки получают суффикс .attemptN и НЕ затирают прежний файл
    (прежний промпт остаётся для разбора обрыва).
    """
    aw = load_workflow()
    directory = os.path.join(ROOT, aw.PROMPT_DIR_NAME)
    name = f"{aw.PROMPT_FILE_PREFIX}.{ch.chapter_id_full}.{slug}.md"
    if attempt > 1:
        name = name[:-3] + f".attempt{attempt}.md"
    return os.path.join(directory, name)

def extract_expected_from_prompt(text: str) -> list[str]:
    """Ожидаемые артефакты SMA-промпта: OUTPUT FILE из текста задания.

    Слепые файлы Фазы 1 (``*.phase1.json``) — ВХОД Фазы 2, а не её результат,
    поэтому из ожидаемых исключаются.
    """
    found = []
    for match in SMA_PATH_RE.finditer(text):
        path = match.group(0)
        if path.endswith(".phase1.json"):
            continue
        if path not in found:
            found.append(path)
    return expected_for_subtask_paths(found)

def expected_for_subtask(kind: str, ch) -> list[str]:
    """Ожидаемые артефакты (пути относительно корня) для режима и главы."""
    if kind in SMA_SLUGS:
        return []  # заполняется при launch из текста промпта (там run_id)
    if kind in AUDIT_SLUGS:
        paths = [ch.audit_path, ch.output_path, ch.log_path]
    else:  # WORK_SLUGS и всё незнакомое — работа с текстом главы
        paths = [ch.output_path, ch.log_path, ch.merged_path]
    return expected_for_subtask_paths([rel_to_root(p) for p in paths])

def expected_for_subtask_paths(paths: list[str]) -> list[str]:
    seen: list[str] = []
    for path in paths:
        if path not in seen:
            seen.append(path)
    return seen

def resume_header(sub: dict, attempt: int) -> str:
    """Блок ПРОДОЛЖЕНИЯ, добавляемый в промпт при resume (не перезапуск!)."""
    previous = sub["attempts"][-1] if sub.get("attempts") else {}
    started = previous.get("started", "время неизвестно")
    sma_note = ""
    if sub.get("kind") in SMA_SLUGS:
        sma_note = (
            "\nУ этого задания НОВЫЙ OUTPUT FILE (новый audit_run_id): результат "
            "пиши только в него. Прежний неполный файл результата (если остался "
            "от оборвавшейся попытки) не доделывай, не перезаписывай и не "
            "используй как основание — это был другой запуск."
        )
    return f"""ПРОДОЛЖЕНИЕ ПОСЛЕ ОБРЫВА (попытка {attempt} из серии субзадачи {sub['id']})

Предыдущая попытка этого задания была зарегистрирована {started} и НЕ была
завершена: работа субагента оборвалась (обрыв соединения/сессии). Это норма —
твоя задача сейчас не начинать с нуля, а ПРОДОЛЖИТЬ.
Порядок:
1. Сначала проверь, что уже сделано: созданные/изменённые файлы, текущее
   состояние output/, лога, merged и результата по OUTPUT FILE из задания ниже.
2. Уже готовое не переделывай и не перезаписывай. Найденное partial-состояние
   — точка продолжения, а не повод начинать заново.
3. Доделай недостающее с места обрыва и заверши задание целиком.
4. Если результат уже полностью готов — просто подтверди это коротко и завершай.
Если по ходу выяснится, что прежняя попытка успела испортить файлы — не
откатывай их, а сообщи об этом в ответе.{sma_note}

--- НИЖЕ ИСХОДНОЕ ЗАДАНИЕ ЭТОЙ СУБЗАДАЧИ ---

"""

def generate_prompt(sub: dict, attempt: int) -> tuple[str, list[str]]:
    """Генерирует текст промпта субзадачи и ожидаемые артефакты.

    Для attempt > 1 перед результатом добавляется блок ПРОДОЛЖЕНИЯ.
    """
    slug_map = workflow_slug_map()
    kind = sub["kind"]
    if kind not in slug_map:
        raise SystemExit(
            f"ОШИБКА: неизвестный режим промпта «{kind}». См. `kinds`.")
    info = slug_map[kind]
    if info.generator is None:
        raise SystemExit(
            f"ОШИБКА: режим «{kind}» без генератора промпта "
            "(interactive-режим меню); выбери другой slug.")
    ch = make_chapter(sub["volume"], sub["chapter"])
    text = info.generator(ch)
    expected = extract_expected_from_prompt(text) if kind in SMA_SLUGS \
        else expected_for_subtask(kind, ch)
    if attempt > 1:
        text = resume_header(sub, attempt) + text
    return text, expected

# ============================================================================
# КОМАНДЫ
# ============================================================================
def cmd_new(args: argparse.Namespace) -> int:
    ledger = load_ledger()
    task = {
        "id": next_task_id(ledger),
        "text": args.text,
        "created": now_iso(),
        "status": T_OPEN,
        "note": args.note or "",
        "subtasks": [],
    }
    ledger["tasks"].append(task)
    save_ledger(ledger)
    print(f"Создана задача {task['id']}: {task['text']}")
    print("Следующие шаги: `plan "
          f"{task['id']} --kind <slug> --volume N --chapter CH|--all`")
    return 0

def cmd_plan(args: argparse.Namespace) -> int:
    ledger = load_ledger()
    task = find_task(ledger, args.task)
    if task["status"] != T_OPEN:
        raise SystemExit(f"ОШИБКА: задача {task['id']} в статусе "
                         f"{task['status']} — планировать нельзя.")
    kinds = [k.strip() for k in args.kind.split(",") if k.strip()]
    slug_map = workflow_slug_map()
    unknown = [k for k in kinds if k not in slug_map]
    if unknown:
        raise SystemExit(f"ОШИБКА: неизвестные режимы: {', '.join(unknown)}. "
                         "См. `kinds`.")
    if args.all_chapters:
        chapters = volume_chapters(args.volume)
        if not chapters:
            raise SystemExit(f"ОШИБКА: в томе v{args.volume} глав не найдено.")
    else:
        chapters = [c.strip() for c in (args.chapter or "").split(",")
                    if c.strip()]
        if not chapters:
            raise SystemExit("ОШИБКА: укажи --chapter CH[,CH] или --all.")
    created = []
    for chapter in chapters:
        for kind in kinds:
            ch = make_chapter(args.volume, chapter)
            sub = {
                "id": next_subtask_id(task),
                "kind": kind,
                "volume": args.volume,
                "chapter": ch.chapter_raw,
                "chapter_id": ch.chapter_id_full,
                "status": ST_PLANNED,
                "prompt_file": "",
                "expected": expected_for_subtask(kind, ch),
                "attempts": [],
                "note": "",
            }
            task["subtasks"].append(sub)
            created.append(sub)
    save_ledger(ledger)
    print(f"Задача {task['id']}: добавлено субзадач — {len(created)}")
    for sub in created:
        expected = ", ".join(sub["expected"]) or "(по тексту промпта при launch)"
        print(f"  {sub['id']:<12} {sub['kind']:<18} {sub['chapter_id']:<10} "
              f"ожидается: {expected}")
    print("Дальше: `launch "
          f"{created[0]['id']}` … (можно несколько ID разом)")
    return 0

def cmd_launch(args: argparse.Namespace) -> int:
    ledger = load_ledger()
    for sub_id in args.subtasks:
        _, sub = find_subtask(ledger, sub_id)
        if sub["status"] == ST_DONE:
            print(f"  {sub['id']}: уже done — пропущено")
            continue
        attempt = len(sub["attempts"]) + 1
        text, expected = generate_prompt(sub, attempt)
        ch = make_chapter(sub["volume"], sub["chapter"])
        path = prompt_file_for(ch, sub["kind"], attempt)
        atomic_write(path, text)
        sub["prompt_file"] = rel_to_root(path)
        if not sub["expected"]:
            sub["expected"] = expected
        sub["attempts"].append({
            "n": attempt,
            "started": now_iso(),
            "prompt": sub["prompt_file"],
            "finished": "",
            "result": "",
            "note": "",
        })
        sub["status"] = ST_RUNNING
        print(f"  {sub['id']} [{sub['kind']} {sub['chapter_id']}] "
              f"попытка {attempt}: промпт → {sub['prompt_file']}")
        print(f"    ЗАПУСТИ СУБАГЕНТА с заданием: прочитай файл "
              f"{sub['prompt_file']} и выполни его дословно.")
    save_ledger(ledger)
    print("\nПосле возврата субагента отметь итог: `done <ID>` или "
          "`fail <ID> --note ...`.\nЕсли сессия субагента оборвалась — не "
      "угадывай: `recover` определит это по файлам, `resume <ID>` продолжит.")
    return 0

def cmd_done(args: argparse.Namespace) -> int:
    ledger = load_ledger()
    _, sub = find_subtask(ledger, args.subtask)
    if sub["attempts"]:
        sub["attempts"][-1]["finished"] = now_iso()
        sub["attempts"][-1]["result"] = ST_DONE
        sub["attempts"][-1]["note"] = args.note or ""
    sub["status"] = ST_DONE
    if args.note:
        sub["note"] = args.note
    save_ledger(ledger)
    print(f"  {sub['id']}: done" + (f" ({args.note})" if args.note else ""))
    return 0

def cmd_fail(args: argparse.Namespace) -> int:
    if not args.note:
        raise SystemExit("ОШИБКА: для fail обязателен --note (почему упало).")
    ledger = load_ledger()
    _, sub = find_subtask(ledger, args.subtask)
    if sub["attempts"]:
        sub["attempts"][-1]["finished"] = now_iso()
        sub["attempts"][-1]["result"] = ST_FAILED
        sub["attempts"][-1]["note"] = args.note
    sub["status"] = ST_FAILED
    sub["note"] = args.note
    save_ledger(ledger)
    print(f"  {sub['id']}: failed — {args.note}")
    print("  Причина рабочая (не обрыв) — разбери её и `launch`/`resume` "
          "заново; обрыв — просто `resume`.")
    return 0

# ----------------------------------------------------------------------------
# verify / recover / pending
# ----------------------------------------------------------------------------
def verify_subtask(sub: dict) -> dict:
    """Сверка одной субзадачи с файлами проекта.

    Возвращает вердикт: DONE (артефакты на месте и свежие), PROGRESS (что-то
    изменилось после запуска — вероятно, живая работа), INTERRUPTED (нет
    ни артефактов, ни изменений — обрыв), NO_ATTEMPTS (промпт не сгенерирован).
    """
    kind = sub["kind"]
    if not sub.get("attempts"):
        return {"verdict": "NO_ATTEMPTS", "detail": "промпт не сгенерирован"}
    last = sub["attempts"][-1]
    started = parse_iso(last.get("started", "")) or datetime(1970, 1, 1)
    started_ts = started.timestamp()
    expected = sub.get("expected") or []
    absolute = [p if os.path.isabs(p) else os.path.join(ROOT, p)
                for p in expected]
    fresh = [p for p in absolute if mtime_of(p) >= started_ts]
    stale = [p for p in absolute if exists(p) and p not in fresh]
    progress = [p for p in _progress_paths(sub) if mtime_of(p) >= started_ts]

    if kind in SMA_SLUGS:
        if fresh:
            return {"verdict": "DONE", "detail": "артефакт результата свежий",
                    "fresh": [rel_to_root(p) for p in fresh]}
        detail = "нет результата после запуска"
        if stale:
            detail += f" (есть старые файлы: {', '.join(rel_to_root(p) for p in stale)})"
        return {"verdict": "INTERRUPTED", "detail": detail, "fresh": []}
    # WORK / AUDIT: единичный «свежий артефакт» не равен завершению работы,
    # но свежие изменения — признак живой работы; нет ничего — обрыв.
    if kind in AUDIT_SLUGS and any(mtime_of(p) >= started_ts
                                   for p in absolute[:1]):
        return {"verdict": "DONE", "detail": "свежий отчёт аудита",
                "fresh": [rel_to_root(absolute[0])]}
    if progress:
        return {"verdict": "PROGRESS", "detail": "файлы менялись после запуска",
                "fresh": [rel_to_root(p) for p in progress]}
    return {"verdict": "INTERRUPTED", "detail": "изменений после запуска нет",
            "fresh": []}

def _progress_paths(sub: dict) -> list[str]:
    ch = make_chapter(sub["volume"], sub["chapter"])
    paths = [ch.output_path, ch.log_path, ch.merged_path, ch.audit_path]
    base = os.path.join(AINOVELEDIT, "output", "_audit", "sma",
                        f"{ch.volume_file_id}-{ch.chapter_id}")
    for kind in ("a", "b", "c", "analysis", "precheck"):
        folder = os.path.join(base, kind)
        if os.path.isdir(folder):
            for name in os.listdir(folder):
                paths.append(os.path.join(folder, name))
    return paths

def apply_verdicts(ledger: dict, mark: bool, task_filter: str | None
                   ) -> list[dict]:
    """Прогоняет verify по субзадачам; при mark — меняет статусы.

    Правила --mark: DONE → done; INTERRUPTED → interrupted; PROGRESS и
    NO_ATTEMPTS статус НЕ меняют (живую работу не трогаем, незапущенную
    надо launch'ить заново).
    """
    rows = []
    for task, sub in all_subtasks(ledger):
        if task_filter and task["id"].upper() != task_filter.upper():
            continue
        result = verify_subtask(sub)
        row = {"task": task["id"], "sub": sub["id"], "kind": sub["kind"],
               "chapter": sub.get("chapter_id", "?"), "status": sub["status"],
               **result}
        if mark and sub["status"] == ST_RUNNING:
            if result["verdict"] == "DONE":
                sub["status"] = ST_DONE
                if sub["attempts"]:
                    sub["attempts"][-1]["finished"] = now_iso()
                    sub["attempts"][-1]["result"] = ST_DONE
                    sub["attempts"][-1]["note"] = "verify --mark"
                row["status"] = ST_DONE
            elif result["verdict"] == "INTERRUPTED":
                sub["status"] = ST_INTERRUPTED
                sub["note"] = result["detail"]
                row["status"] = ST_INTERRUPTED
        rows.append(row)
    if mark:
        save_ledger(ledger)
    return rows

def print_verdicts(rows: list[dict]) -> None:
    if not rows:
        print("Субзадач нет.")
        return
    print(f"{'Субзадача':<14}{'Режим':<18}{'Глава':<11}{'Статус':<13}"
          f"{'Вердикт':<14}Детали")
    icons = {"DONE": "✓", "PROGRESS": "…", "INTERRUPTED": "✗", "NO_ATTEMPTS": "-"}
    for row in rows:
        print(f"{row['sub']:<14}{row['kind']:<18}{row['chapter']:<11}"
              f"{row['status']:<13}"
              f"{icons.get(row['verdict'], '?') + ' ' + row['verdict']:<14}"
              f"{row['detail']}")
    needs = [r for r in rows if r["verdict"] in ("INTERRUPTED", "NO_ATTEMPTS")
             and r["status"] in (ST_INTERRUPTED, ST_FAILED, ST_RUNNING)]
    if needs:
        print("\nТребуют действия (resume продолжит с места обрыва):")
        print("  python tools/dispatch.py resume " +
              " ".join(r["sub"] for r in needs))
        if any(r["status"] == ST_RUNNING for r in needs):
            print("Внимание: субзадачи в статусе running с вердиктом "
                  "INTERRUPTED — это норма, если субагент СЕЙЧАС работает: "
                  "вердикт\nпроверяй только после возврата субагента или "
                  "после подозрения на обрыв.")

def cmd_verify(args: argparse.Namespace) -> int:
    ledger = load_ledger()
    rows = apply_verdicts(ledger, mark=args.mark, task_filter=args.task)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print_verdicts(rows)
    return 0

def cmd_recover(args: argparse.Namespace) -> int:
    """Точка входа каждой сессии оркестратора (в т.ч. после компактизации)."""
    ledger = load_ledger()
    rows = apply_verdicts(ledger, mark=True, task_filter=None)
    open_tasks = [t for t in ledger["tasks"] if t["status"] == T_OPEN]
    print("ВОССТАНОВЛЕНИЕ ПОСЛЕ ОБРЫВА/КОМПАКТИЗАЦИИ")
    print("=" * 78)
    if rows:
        print_verdicts(rows)
    else:
        print("Реестр пуст: задач ещё не было.")
    print()
    if not open_tasks:
        print("Открытых задач нет. Можно начинать новую: "
              "`new \"<текст задачи>\"`.")
        return 0
    print(f"Открытых задач: {len(open_tasks)}")
    for task in open_tasks:
        subs = task.get("subtasks", [])
        counts: dict[str, int] = {}
        for sub in subs:
            counts[sub["status"]] = counts.get(sub["status"], 0) + 1
        summary = ", ".join(f"{v}× {k}" for k, v in sorted(counts.items())) \
            or "субзадач нет"
        print(f"  {task['id']}: {task['text'][:60]}")
        print(f"    субзадачи: {summary}")
    todo = [r for r in rows if r["status"] in (ST_INTERRUPTED, ST_FAILED)]
    if todo:
        print("\nПрерванное восстанови командой resume (промпт «продолжи с "
              "места обрыва»):")
        for row in todo:
            print(f"  python tools/dispatch.py resume {row['sub']}"
                  f"   # {row['kind']} {row['chapter']}")
    print("\nПолная картина: `python tools/dispatch.py pending`.")
    return 0

def cmd_pending(args: argparse.Namespace) -> int:
    ledger = load_ledger()
    rows = apply_verdicts(ledger, mark=False, task_filter=None)
    by_sub = {row["sub"]: row for row in rows}
    print("НЕЗАВЕРШЁННО (по реестру, ничего не изменено)")
    print("=" * 78)
    anything = False
    for task in ledger["tasks"]:
        if task["status"] != T_OPEN:
            continue
        anything = True
        print(f"\n{task['id']} [{task['status']}] {task['text']}")
        for sub in task.get("subtasks", []):
            row = by_sub.get(sub["id"], {})
            verdict = row.get("verdict", "?")
            detail = row.get("detail", "")
            print(f"  {sub['id']:<12}{sub['kind']:<18}"
                  f"{sub.get('chapter_id', '?'):<11}{sub['status']:<13}"
                  f"{verdict:<13}{detail}")
            if sub.get("prompt_file") and sub["status"] in (ST_RUNNING,
                                                            ST_INTERRUPTED):
                print(f"    промпт: {sub['prompt_file']}")
    if not anything:
        print("Открытых задач нет.")
    return 0

def cmd_close(args: argparse.Namespace) -> int:
    """Закрыть задачу: done (всё выполнено) или cancelled (отменена)."""
    ledger = load_ledger()
    task = find_task(ledger, args.task)
    if args.status == T_CANCELLED:
        task["status"] = T_CANCELLED
    else:
        leftovers = [sub for sub in task.get("subtasks", [])
                     if sub["status"] not in (ST_DONE,)]
        if leftovers and not args.force:
            ids = ", ".join(f"{s['id']}({s['status']})" for s in leftovers)
            raise SystemExit(
                f"ОШИБКА: незавершённые субзадачи: {ids}. Заверши/отмени их "
                "или повтори с --force.")
        task["status"] = T_DONE
    if args.note:
        task["note"] = args.note
    save_ledger(ledger)
    print(f"Задача {task['id']}: {task['status']}"
          + (f" — {args.note}" if args.note else ""))
    return 0

def cmd_list(args: argparse.Namespace) -> int:
    ledger = load_ledger()
    if not ledger["tasks"]:
        print("Реестр пуст.")
        return 0
    for task in ledger["tasks"]:
        subs = task.get("subtasks", [])
        counts: dict[str, int] = {}
        for sub in subs:
            counts[sub["status"]] = counts.get(sub["status"], 0) + 1
        summary = ", ".join(f"{v}×{k}" for k, v in sorted(counts.items())) or "—"
        print(f"{task['id']} [{task['status']}] {task['text'][:64]}")
        print(f"  создана {task['created']} | субзадач: {len(subs)} ({summary})")
    return 0

def cmd_show(args: argparse.Namespace) -> int:
    ledger = load_ledger()
    task = find_task(ledger, args.task)
    print(json.dumps(task, ensure_ascii=False, indent=2))
    return 0

def cmd_kinds(args: argparse.Namespace) -> int:
    slug_map = workflow_slug_map()
    print("РЕЖИМЫ ПРОМПТОВ (slugs для plan --kind)")
    print("=" * 78)
    for slug, info in sorted(slug_map.items()):
        group = ("SMA" if slug in SMA_SLUGS else
                 "AUDIT" if slug in AUDIT_SLUGS else "WORK")
        generator = "да" if getattr(info, "generator", None) else "нет"
        print(f"  {slug:<20}{group:<8}генератор: {generator:<4}{info.title}")
    print("\nSMA  — изолированные смысловые аудиты (ожидаемый файл результата "
          "берётся из промпта).")
    print("AUDIT — аудиты главы (ожидается свежий отчёт output/_audit/).")
    print("WORK — работа с текстом главы (ориентир — свежие output/ и лог).")
    return 0

# ----------------------------------------------------------------------------
# self-test
# ----------------------------------------------------------------------------
def cmd_self_test(args: argparse.Namespace) -> int:
    """Проверка логики реестра и вердиктов во временной папке (без записи
    в боевой реестр и без генерации LLM-промптов агент- workflow не трогаем:
    проверяются чистые функции + round-trip реестра)."""
    import shutil
    tmp = tempfile.mkdtemp(prefix="dispatch-selftest-")
    os.environ[DISPATCH_DIR_ENV] = tmp
    checks: list[tuple[str, bool]] = []
    try:
        ledger = load_ledger()
        task = {"id": next_task_id(ledger), "text": "тест", "created": now_iso(),
                "status": T_OPEN, "note": "", "subtasks": []}
        ledger["tasks"].append(task)
        sub = {"id": next_subtask_id(task), "kind": "sma-a", "volume": 3,
               "chapter": "5", "chapter_id": "v3-ch05", "status": ST_RUNNING,
               "prompt_file": "", "expected": [], "attempts": [], "note": ""}
        task["subtasks"].append(sub)
        checks.append(("next ids", task["id"] == "T-0001"
                       and sub["id"] == "T-0001-S1"))
        save_ledger(ledger)
        reloaded = load_ledger()
        checks.append(("round-trip", reloaded["tasks"][0]["subtasks"][0]["id"]
                       == "T-0001-S1"))
        # Вердикт INTERRUPTED: попытка есть, артефактов нет.
        sub2 = reloaded["tasks"][0]["subtasks"][0]
        sub2["attempts"] = [{"n": 1, "started": now_iso(), "prompt": "",
                             "finished": "", "result": "", "note": ""}]
        sub2["expected"] = [os.path.join(tmp, "no-such-artifact.json")]
        verdict = verify_subtask(sub2)
        checks.append(("interrupted без артефакта",
                       verdict["verdict"] == "INTERRUPTED"))
        # Вердикт DONE: свежий артефакт.
        artifact = os.path.join(tmp, "artifact.json")
        with open(artifact, "w", encoding="utf-8") as handle:
            handle.write("{}")
        sub2["expected"] = [artifact]
        checks.append(("done со свежим артефактом",
                       verify_subtask(sub2)["verdict"] == "DONE"))
        # apply_verdicts --mark переводит running → interrupted.
        sub2["expected"] = [os.path.join(tmp, "gone.json")]
        rows = apply_verdicts(reloaded, mark=True, task_filter=None)
        checks.append(("mark → interrupted",
                       rows[0]["status"] == ST_INTERRUPTED
                       and reloaded["tasks"][0]["subtasks"][0]["status"]
                       == ST_INTERRUPTED))
        # SMA-ожидания: phase1-файл не должен стать артефактом Фазы 2.
        text = ("OUTPUT FILES\nJSON: output/_audit/sma/v3-ch05/analysis/"
                "X.json\nMD: output/_audit/sma/v3-ch05/analysis/X.md\n"
                "phase1: output/_audit/sma/v3-ch05/analysis/Y.phase1.json")
        expected = extract_expected_from_prompt(text)
        checks.append(("phase1 исключён из артефактов Фазы 2",
                       expected == ["output/_audit/sma/v3-ch05/analysis/X.json",
                                    "output/_audit/sma/v3-ch05/analysis/X.md"]))
        # Обход глав тома.
        chapters = volume_chapters(1)
        checks.append(("обход глав v1", bool(chapters) and "ch01" in chapters))
        checks.append(("completed.md читается", isinstance(completed_volumes(),
                                                           set)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        os.environ.pop(DISPATCH_DIR_ENV, None)
    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"  [{'OK' if ok else 'FAIL'}] {name}")
    if failed:
        print(f"\nSELF-TEST: ПРОВАЛЕНО {len(failed)} из {len(checks)}")
        return 1
    print(f"\nSELF-TEST: все {len(checks)} проверок пройдены.")
    return 0

# ============================================================================
# CLI
# ============================================================================
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dispatch.py",
        description="Диспетчер крупных задач: реестр субагентов, "
                    "проверка завершённости, продолжение после обрывов.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("new", help="создать задачу")
    p.add_argument("text", help="текст задачи свободной формулировкой")
    p.add_argument("--note", default="", help="необязательная заметка")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("plan", help="поставить субзадачи")
    p.add_argument("task", help="TASK-ID (см. list)")
    p.add_argument("--kind", required=True,
                   help="slug режима(ов), через запятую (см. kinds)")
    p.add_argument("--volume", type=int, required=True, help="номер тома")
    p.add_argument("--chapter", default="",
                   help="главы через запятую: 5,ch07,epilogue")
    p.add_argument("--all", dest="all_chapters", action="store_true",
                   help="все главы тома (по translates/ja и output)")
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("launch", help="сгенерировать промпт и зарегистрировать "
                                      "запуск субагента")
    p.add_argument("subtasks", nargs="+", help="SUB-ID …")
    p.set_defaults(func=cmd_launch)

    p = sub.add_parser("done", help="подтвердить завершение субзадачи")
    p.add_argument("subtask")
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("fail", help="зафиксировать ошибку субзадачи")
    p.add_argument("subtask")
    p.add_argument("--note", required=True)
    p.set_defaults(func=cmd_fail)

    p = sub.add_parser("verify", help="сверить реестр с файлами проекта")
    p.add_argument("task", nargs="?", default=None)
    p.add_argument("--mark", action="store_true",
                   help="перевести running → done/interrupted по вердиктам")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("resume", help="продолжить прерванную/упавшую субзадачу")
    p.add_argument("subtasks", nargs="+")
    p.set_defaults(func=lambda a: cmd_launch(a))

    p = sub.add_parser("recover", help="восстановление после обрыва/компактизации"
                                       " (первый запуск в сессии)")
    p.set_defaults(func=cmd_recover)

    p = sub.add_parser("pending", help="сводка незавершённого (без изменений)")
    p.set_defaults(func=cmd_pending)

    p = sub.add_parser("close", help="закрыть задачу (done | cancelled)")
    p.add_argument("task")
    p.add_argument("--status", choices=[T_DONE, T_CANCELLED], default=T_DONE)
    p.add_argument("--note", default="")
    p.add_argument("--force", action="store_true",
                   help="закрыть, даже если есть незавершённые субзадачи")
    p.set_defaults(func=cmd_close)

    p = sub.add_parser("list", help="список задач")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="показать задачу целиком (JSON)")
    p.add_argument("task")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("status", help="состояние глав проекта")
    p.add_argument("--volume", type=int, default=None)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("kinds", help="справочник режимов промптов")
    p.set_defaults(func=cmd_kinds)

    p = sub.add_parser("self-test", help="самопроверка логики")
    p.set_defaults(func=cmd_self_test)
    return parser

def cmd_status(args: argparse.Namespace) -> int:
    if args.json:
        print(json.dumps(project_status(args.volume), ensure_ascii=False,
                         indent=2))
    else:
        print_status(args.volume)
    return 0

def main() -> int:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
