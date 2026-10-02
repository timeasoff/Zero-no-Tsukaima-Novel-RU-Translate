#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LEGACY / NOT IMPLEMENTED — автоматический semantic audit.

Статус: НЕ РЕАЛИЗОВАН / НЕ ПОДДЕРЖИВАЕТСЯ. Не использовать в текущем
pipeline. Сохранён только как задел/история для возможной будущей
реализации. Подробности: legacy/semantic-audit-auto/LEGACY.md.

Текущий рабочий pipeline: Semantic Audit A → Semantic Audit B →
Semantic Analyzer A+B (output/_audit/sma/<chapter>/{a,b,analysis}/);
запуск — через tools/agent_workflow.py.

run_semantic_audit.py — оркестратор ДВОЙНОГО независимого смыслового аудита (A + B).

Запускает два НЕЗАВИСИМЫх процесса Cline (CLI 3.0.62) ПАРАЛЛЕЛЬНО:

    оркестратор (этот скрипт)
        ├── %TEMP%\\ainoveledit-sma\\<run-id>\\A   → Cline A  (cwd = A)
        └── %TEMP%\\ainoveledit-sma\\<run-id>\\B   → Cline B  (cwd = B)

Изоляция (по результатам проведённого эксперимента с Cline 3.0.62)
------------------------------------------------------------------
* SESSION / CONVERSATION — есть. У каждого запуска своя sessionId и свой
  каталог ~/.cline/data/sessions/<id>; свежий запуск не видит контекста
  прошлых запусков (проверено: запрос о «секретном слове» → NONE).
* FILESYSTEM — разделения НЕТ. Агент с cwd в пустом временном каталоге
  физически способен читать абсолютные пути проекта (проверено: чтение
  файла из чужого каталога успешно). Поэтому каталоги A/B намеренно ПУСТЫ,
  а весь вход (JA, RU, контекст, текст скилла) передаётся ТЕКСТОМ в
  промпте — путей к проекту в промпте нет, агенту читать нечего.
* TOOLS — селективных запретов в 3.0.62 нет; --auto-approve false ломает
  ВСЕ tool-call'ы (включая чтение внутри своего workspace) и поэтому не
  используется. Режим plan (поведение по умолчанию) запрещает агенту
  создавать/изменять файлы: результат возвращается через stdout (NDJSON).
* PARALLEL — два процесса запускаются одновременно (Popen + общий wait),
  что экспериментально подтверждено (в отличие от OpenCode free tier).
* -m / -P НЕ передаются: эти флаги мутируют глобальный providers.json
  (lastUsedProvider / settings.model) и ломают последующие запуски.

Поток
-----
JA (translates/ja/<file>) + текущий RU-результат (output/<file>) читаются по
смысловым блокам через merged_io.read_source_blocks → строятся prompt A и
prompt B (скилл A/B inline + material) → запускаются A‖B → оба результата
валидируются → ТОЛЬКО ПОСЛЕ УСПЕХА ОБОИХ пишутся
output/_audit/<ch>-sma-a.json и <ch>-sma-b.json → вызывается
merge_findings.py → <ch>-sma-merged.{json,md} → временные каталоги удаляются.

Коды выхода: 0 — ок; 1 — ошибка входа/аргументов; 2 — упал A; 3 — упал B;
4 — невалидный результат (JSON/схема); 5 — ошибка merge; 6 — runtime не найден
(Cline или opencode-cli).

Runtime (--runtime, по умолчанию cline)
---------------------------------------
* `cline` — два процесса Cline, история сессий из ~/.cline (как раньше);
* `opencode` — OpenCode → OmniRoute → модель из --model: у каждого запуска
  СВОЯ session OpenCode (A, B — разные sessions), сервер поднимает адаптер,
  глобальный ~/.config/opencode/opencode.json не меняется. Проверки
  sessionId/параллельности берутся из результатов адаптера, а не из
  истории Cline. Семантика A/B, prompts и SKILL.md не меняются.

Кодировка: промпт передаётся в аргументах процесса через CreateProcessW
(UTF-16) БЕЗ shell — каналы PowerShell и `|` не используются, поэтому
не-ASCII текст не искажается (правило AGENTS.md о порче символов в shell).

Использование (LEGACY — не в текущем pipeline)
---------------------------------------------
    python legacy/semantic-audit-auto/run_semantic_audit.py --file v5-ch02.md --blocks 5-7
    python legacy/semantic-audit-auto/run_semantic_audit.py --file v5-ch02.md --blocks 6 --self-test
    python legacy/semantic-audit-auto/run_semantic_audit.py --file v5-ch02.md --dry-run
    python legacy/semantic-audit-auto/run_semantic_audit.py --file v5-ch02.md            # вся глава
    python legacy/semantic-audit-auto/run_semantic_audit.py --file v5-ch02.md --runtime opencode \
        --model "<MODEL_ID>"                                          # OpenCode
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# ПУТИ И ИМПОРТЫ ПРОЕКТА
# ---------------------------------------------------------------------------
# LEGACY relocation shim: файл вынесен в legacy/semantic-audit-auto/.
# Это НЕ переписывание под новую архитектуру sma/<chapter>/..., а только
# пересчёт путей после переноса. Общие модули (merged_io, llm_runtime)
# остаются в AINovelEdit/scripts/, а agent_workflow — в tools/.
LEGACY_DIR = Path(__file__).resolve().parent
AINOVELEDIT = LEGACY_DIR.parent.parent          # AINovelEdit/
SCRIPTS_DIR = AINOVELEDIT / "scripts"           # общие модули проекта
TOOLS_DIR = AINOVELEDIT.parent / "tools"        # agent_workflow.py

for _p in (str(LEGACY_DIR), str(SCRIPTS_DIR), str(TOOLS_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import merged_io                      # noqa: E402  (общий разбор блок-файлов)
import llm_runtime as rt              # noqa: E402  (runtime adapters)
from agent_workflow import Chapter  # noqa: E402  (пути главы без дублирования)

OUT_DIR = AINOVELEDIT / "output" / "_audit"
SKILL_DIR = AINOVELEDIT / ".agents" / "skills"
RUN_ROOT = Path(tempfile.gettempdir()) / "ainoveledit-sma"

# Ограничение длины промпта (предел командной строки Windows ~32767 символов).
PROMPT_CHAR_LIMIT = 26000

AUDITORS = {
    "a": {
        "audit_id": "sma-a",
        "audit_type": "semantic-audit-a",
        "skill": "semantic-audit-a",
        "role": "Semantic Auditor A (лексическая точность, оттенки, эмоции, мимика, жесты)",
    },
    "b": {
        "audit_id": "sma-b",
        "audit_type": "semantic-audit-b",
        "skill": "semantic-audit-b",
        "role": "Semantic Auditor B (субъект/объект, причинно-следственные связи, идиомы, контекст)",
    },
}

SEVERITIES = {"ERROR", "WARNING", "CANDIDATE"}

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUN_A = 2
EXIT_RUN_B = 3
EXIT_VALIDATE = 4
EXIT_MERGE = 5
EXIT_NO_RUNTIME = 6
EXIT_NO_CLINE = EXIT_NO_RUNTIME   # старое имя (совместимость)

RUNTIMES = ("cline", "opencode")


# ---------------------------------------------------------------------------
# КОДИРОВКА КОНСОЛИ
# ---------------------------------------------------------------------------
def setup_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


# ---------------------------------------------------------------------------
# КОМАНДА CLINE
# ---------------------------------------------------------------------------
def resolve_cline() -> tuple[str, str] | tuple[None, None]:
    """Возвращает (node, cline_bin) без использования флагов -m / -P."""
    override = os.environ.get("CLINE_BIN")
    candidates = []
    if override:
        candidates.append(Path(override))
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(Path(appdata) / "npm" / "node_modules" / "cline" / "bin" / "cline")
    for cand in candidates:
        if cand.exists():
            node = shutil.which("node") or "node"
            return node, str(cand)
    which = shutil.which("cline")
    if which:
        node = shutil.which("node")
        if node:
            return node, which
    return None, None


def base_cmd(node: str, cline_bin: str) -> list[str]:
    """Базовый argv без промпта: никогда не содержит -m / -P."""
    if cline_bin.lower().endswith((".cmd", ".bat")):
        return ["cmd", "/c", cline_bin]
    if node and cline_bin.endswith("cline") and os.sep + "bin" + os.sep in cline_bin:
        return [node, cline_bin]
    return [cline_bin]


def cline_history(node: str, cline_bin: str, limit: int = 20) -> list[dict]:
    """Снимок истории Cline (после завершения запусков)."""
    cmd = base_cmd(node, cline_bin) + ["history", "--json", "--limit", str(limit)]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"  предупреждение: история Cline недоступна: {exc}", file=sys.stderr)
        return []
    try:
        data = json.loads(proc.stdout.decode("utf-8", "replace"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


# ---------------------------------------------------------------------------
# ВХОД: ГЛАВА И БЛОКИ
# ---------------------------------------------------------------------------
def parse_chapter_arg(raw: str, volume_arg: int | None) -> Chapter:
    """v5-ch02 / v05-ch02 / v5-ch02.md / ch02 (+ --volume) → Chapter."""
    text = raw.strip()
    if text.lower().endswith(".md"):
        text = text[:-3].strip()
    m = re.match(r"^v?(\d+)-(.+)$", text, re.IGNORECASE)
    if m:
        volume = int(m.group(1))
        chapter_raw = m.group(2).strip()
    elif volume_arg is not None:
        chapter_raw = text
        volume = volume_arg
    else:
        raise ValueError(
            f"не удалось разобрать главу {raw!r}: ожидается форма v5-ch02 "
            f"или chNN с ключом --volume"
        )
    if not chapter_raw:
        raise ValueError("пустой идентификатор главы")
    return Chapter(volume=volume, chapter_raw=chapter_raw)


def parse_blocks(spec: str | None) -> list[int] | None:
    """'5-7,9,12-13' → [5,6,7,9,12,13]; None → все блоки главы."""
    if spec is None:
        return None
    out: list[int] = []
    for piece in spec.split(","):
        piece = piece.strip()
        if not piece:
            continue
        m = re.match(r"^(\d+)-(\d+)$", piece)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            if lo > hi:
                raise ValueError(f"неверный диапазон блоков: {piece}")
            out.extend(range(lo, hi + 1))
        elif piece.isdigit():
            out.append(int(piece))
        else:
            raise ValueError(f"не удалось разобрать блок: {piece!r}")
    if not out:
        raise ValueError("пустой список блоков")
    return sorted(dict.fromkeys(out))


def load_chapter_blocks(ch: Chapter) -> tuple[dict[int, list[str]], dict[int, list[str]]]:
    """Читает JA (translates/ja) и текущий RU-результат (output/)."""
    ja_path = Path(ch.ja_path)
    ru_path = Path(ch.output_path)
    if not ja_path.exists():
        raise FileNotFoundError(f"нет JA-файла: {ja_path}")
    if not ru_path.exists():
        raise FileNotFoundError(
            f"нет текущего результата: {ru_path} — SMA сравнивает JA с "
            f"финальным переводом output/, а не с машинным translates/ru"
        )
    ja_blocks = dict(merged_io.read_source_blocks(ja_path))
    ru_blocks = dict(merged_io.read_source_blocks(ru_path))
    if not ja_blocks:
        raise ValueError(f"JA-файл не размечен блоками <!-- block: N -->: {ja_path}")
    if not ru_blocks:
        raise ValueError(f"RU-файл не размечен блоками <!-- block: N -->: {ru_path}")
    return ja_blocks, ru_blocks


def load_skill(kind: str) -> str:
    path = SKILL_DIR / AUDITORS[kind]["skill"] / "SKILL.md"
    if not path.exists():
        raise FileNotFoundError(f"нет скилла: {path}")
    return path.read_text(encoding="utf-8").strip()


# ---------------------------------------------------------------------------
# ФОРМИРОВАНИЕ PROMPT
# ---------------------------------------------------------------------------
def _block_text(store: dict[int, list[str]], num: int) -> str:
    paras = store.get(num)
    if paras is None:
        return "(блок отсутствует в этом файле)"
    return "\n\n".join(p for p in paras if p.strip()).strip() or "(пусто)"


def build_material(
    ch: Chapter,
    targets: list[int],
    ja_blocks: dict[int, list[str]],
    ru_blocks: dict[int, list[str]],
) -> str:
    """MATERIAL: TARGET-блоки + соседний контекст (контекст не аудируется)."""
    first, last = targets[0], targets[-1]
    lines = [
        f"CHAPTER: {ch.chapter_id_full}",
        f"AUDITED BLOCKS: {', '.join(str(b) for b in targets)}",
        "",
        "Соседние блоки даны ТОЛЬКО как контекст. Находки должны относиться "
        "исключительно к блокам из AUDITED BLOCKS.",
        "",
    ]
    for num in targets:
        lines += [
            f"=== TARGET BLOCK {num} ===",
            "JA:",
            _block_text(ja_blocks, num),
            "",
            "RU (текущий результат):",
            _block_text(ru_blocks, num),
            "",
        ]
    prev_num = first - 1
    if prev_num >= 1:
        lines += [
            f"=== CONTEXT PREVIOUS (блок {prev_num}, контекст) ===",
            "JA:",
            _block_text(ja_blocks, prev_num),
            "",
            "RU (текущий результат):",
            _block_text(ru_blocks, prev_num),
            "",
        ]
    else:
        lines += ["=== CONTEXT PREVIOUS ===", "(нет: это первый блок главы)", ""]
    next_num = last + 1
    if next_num in ja_blocks:
        lines += [
            f"=== CONTEXT NEXT (блок {next_num}, контекст) ===",
            "JA:",
            _block_text(ja_blocks, next_num),
            "",
            "RU (текущий результат):",
            _block_text(ru_blocks, next_num),
            "",
        ]
    else:
        lines += ["=== CONTEXT NEXT ===", "(нет: это последний блок главы)", ""]
    return "\n".join(lines).rstrip()


def build_format(kind: str, ch: Chapter, targets: list[int]) -> str:
    meta = AUDITORS[kind]
    return f"""--- FORMAT-BEGIN ---
Ответь СТРОГО одним JSON-объектом. Без markdown, без ```json, без текста до и после.

{{
  "audit_id": "{meta['audit_id']}",
  "audit_type": "{meta['audit_type']}",
  "chapter": "{ch.chapter_id_full}",
  "blocks": [{', '.join(str(b) for b in targets)}],
  "findings": [
    {{
      "block": {targets[0]},
      "source": "точный фрагмент JA",
      "current": "точный фрагмент RU",
      "problem": "тип проблемы (коротко)",
      "reason": "почему JA и RU расходятся",
      "suggestion": "предложенный вариант или null",
      "severity": "ERROR | WARNING | CANDIDATE"
    }}
  ]
}}

Правила формата:
- findings может содержать находки ТОЛЬКО по блокам из "blocks"; у каждой
  находки обязателен свой целочисленный "block".
- Если проблем нет — "findings": [] (пустой массив, объект всё равно обязателен).
- source и current — точные цитаты из раздела MATERIAL, без пересказа.
- Ты только фиксируешь находки: не изменяй и не создавай файлы.
--- FORMAT-END ---"""


def build_prompt(kind: str, ch: Chapter, targets: list[int], material: str,
                 skill_text: str) -> str:
    meta = AUDITORS[kind]
    return f"""ЗАДАЧА: независимый смысловой аудит перевода JA → RU ({meta['role']}).

Ты работаешь ИЗОЛИРОВАННО: не видишь результатов другого аудитора, не знаешь
их находок и не имеешь к ним доступа. Результат второго аудитора тебе не
передавался и не будет передан.

ВАЖНО:
У тебя нет необходимости читать файлы проекта — все необходимые данные уже
предоставлены ниже. Не используй filesystem/tool calls для поиска
дополнительных сведений: аудитируй ТОЛЬКО предоставленный материал.
Ты не должен создавать, изменять или удалять файлы — ответ возвращается
единственным JSON-объектом в текстовом ответе.

--- SKILL-BEGIN ---
{skill_text}
--- SKILL-END ---

--- MATERIAL-BEGIN ---
{material}
--- MATERIAL-END ---
{build_format(kind, ch, targets)}"""


# ---------------------------------------------------------------------------
# ЗАПУСК CLINE (параллельно A и B)
# ---------------------------------------------------------------------------
def start_run(node: str, cline_bin: str, cwd: Path, prompt: str,
              timeout: int) -> subprocess.Popen:
    cmd = base_cmd(node, cline_bin) + [
        "-c", str(cwd), "--json", "-t", str(timeout), prompt,
    ]
    return subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def collect_run(proc: subprocess.Popen, label: str, timeout: int,
                started_at: float) -> dict:
    """Дожидается процесса и разбирает stdout как NDJSON."""
    try:
        out_b, err_b = proc.communicate(timeout=timeout + 60)
    except subprocess.TimeoutExpired:
        proc.kill()
        out_b, err_b = proc.communicate()
        return {
            "label": label, "exit": None, "finish": None, "text": "",
            "events": 0, "error_events": [], "stdout": "",
            "stderr": (err_b or b"").decode("utf-8", "replace")[:1000],
            "duration": round(time.time() - started_at, 1),
            "failure": "процесс не завершился за отведённое время и был убит",
        }
    stdout = (out_b or b"").decode("utf-8", "replace")
    stderr = (err_b or b"").decode("utf-8", "replace")
    result, events, error_events = None, 0, []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        events += 1
        if ev.get("type") == "run_result":
            result = ev
        elif ev.get("type") == "error":
            error_events.append(str(ev.get("message", ""))[:300])
    text = (result or {}).get("text", "") or ""
    failure = None
    if proc.returncode not in (0,):
        failure = f"код выхода {proc.returncode}"
    if result is None:
        failure = failure or "run_result не получен (возможен crash процесса)"
    elif result.get("finishReason") != "completed":
        failure = failure or (
            f"finishReason={result.get('finishReason')!r}"
            + (f", текст={text[:120]!r}" if text else "")
        )
    elif not text.strip():
        failure = "пустой результат"
    return {
        "label": label,
        "exit": proc.returncode,
        "finish": (result or {}).get("finishReason"),
        "text": text,
        "events": events,
        "error_events": error_events,
        "stdout": stdout,
        "stderr": stderr[:1000],
        "duration": round(time.time() - started_at, 1),
        "failure": failure,
    }


# ---------------------------------------------------------------------------
# РАЗБОР И ВАЛИДАЦИЯ РЕЗУЛЬТАТА
# ---------------------------------------------------------------------------
def extract_json(text: str) -> tuple[dict | None, str | None]:
    """Строгой разбор, затем безопасный fallback (удаление markdown-обёртки)."""
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data, None
        return None, "результат — не JSON-объект"
    except json.JSONDecodeError as first:
        stripped = text.strip()
        m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", stripped, re.S)
        candidate = m.group(1) if m else None
        if candidate is None:
            start, end = stripped.find("{"), stripped.rfind("}")
            if 0 <= start < end:
                candidate = stripped[start:end + 1]
        if candidate:
            try:
                data = json.loads(candidate)
                if isinstance(data, dict):
                    return data, "JSON извлечён из markdown-обёртки/пояснений"
                return None, "извлечённое значение — не JSON-объект"
            except json.JSONDecodeError as second:
                return None, f"не удалось разобрать JSON: {second.msg}"
        return None, f"не удалось разобрать JSON: {first.msg}"


def validate_payload(kind: str, ch: Chapter, targets: list[int],
                     raw_text: str) -> tuple[dict | None, list[str], str | None]:
    """→ (payload, список ошибок, предупреждение)."""
    meta = AUDITORS[kind]
    payload, note = extract_json(raw_text)
    if payload is None:
        return None, [note or "не удалось разобрать JSON"], None

    errors: list[str] = []
    got_id = payload.get("audit_id")
    if got_id != meta["audit_id"]:
        errors.append(f"audit_id={got_id!r}, ожидалось {meta['audit_id']!r}")
    chapter = payload.get("chapter")
    allowed = {ch.chapter_id_full, f"v{ch.volume}-{ch.chapter_raw}"}
    if chapter not in allowed:
        errors.append(f"chapter={chapter!r}, ожидалось одно из {sorted(allowed)}")
    findings = payload.get("findings")
    if not isinstance(findings, list):
        errors.append("findings отсутствует или не массив")
        findings = []
    allowed_blocks = set(targets)
    for i, item in enumerate(findings):
        where = f"findings[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: не объект")
            continue
        block = item.get("block")
        if not isinstance(block, int) or block not in allowed_blocks:
            errors.append(f"{where}: block={block!r} вне аудируемых {sorted(allowed_blocks)}")
            continue
        for key in ("source", "current", "problem", "reason"):
            if not isinstance(item.get(key), str) or not item.get(key, "").strip():
                errors.append(f"{where}: пустое поле {key!r}")
        sev = str(item.get("severity", "")).strip().upper()
        if sev not in SEVERITIES:
            errors.append(f"{where}: severity={item.get('severity')!r} вне {sorted(SEVERITIES)}")
        suggestion = item.get("suggestion", None)
        if suggestion is not None and not isinstance(suggestion, str):
            errors.append(f"{where}: suggestion должен быть строкой или null")
    if errors:
        return None, errors, note
    return payload, [], note


# ---------------------------------------------------------------------------
# ЗАПИСЬ РЕЗУЛЬТАТОВ (только после успеха обоих)
# ---------------------------------------------------------------------------
def write_outputs(ch: Chapter, payload_a: dict, payload_b: dict) -> tuple[Path, Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path_a = OUT_DIR / f"{ch.chapter_id_full}-sma-a.json"
    path_b = OUT_DIR / f"{ch.chapter_id_full}-sma-b.json"
    path_a.write_text(json.dumps(payload_a, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    path_b.write_text(json.dumps(payload_b, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    return path_a, path_b


def run_merge(node: str, cline_bin: str, ch: Chapter,
              path_a: Path, path_b: Path) -> tuple[Path, Path] | tuple[None, None]:
    """merge_findings.py (существующий скрипт) вызывается как есть."""
    out_json = OUT_DIR / f"{ch.chapter_id_full}-sma-merged.json"
    out_md = OUT_DIR / f"{ch.chapter_id_full}-sma-merged.md"
    cmd = [sys.executable, str(LEGACY_DIR / "merge_findings.py"),
           "--a", str(path_a), "--b", str(path_b),
           "--output", str(out_json), "--report", str(out_md)]
    proc = subprocess.run(cmd, capture_output=True, encoding="utf-8")
    if proc.returncode != 0 or not out_json.exists():
        sys.stderr.write(proc.stdout or "")
        sys.stderr.write(proc.stderr or "")
        return None, None
    print(proc.stdout.strip())
    return out_json, out_md


# ---------------------------------------------------------------------------
# ГРУППИРОВКА БЛОКОВ ПО РАЗМЕРУ ПРОМПТА
# ---------------------------------------------------------------------------
def chunk_blocks(targets: list[int], ja_blocks: dict[int, list[str]],
                 ru_blocks: dict[int, list[str]], skill_text: str) -> list[list[int]]:
    """Делит диапазон на партии так, чтобы промпт укладывался в лимит."""
    chunks: list[list[int]] = []
    current: list[int] = []
    base_overhead = len(skill_text) + 3000  # скилл + заголовки + формат
    for num in targets:
        size = (len(_block_text(ja_blocks, num)) + len(_block_text(ru_blocks, num)) + 200)
        if current and base_overhead + size + sum(
            len(_block_text(ja_blocks, b)) + len(_block_text(ru_blocks, b)) + 200
            for b in current
        ) > PROMPT_CHAR_LIMIT:
            chunks.append(current)
            current = []
        current.append(num)
    if current:
        chunks.append(current)
    return chunks


# ---------------------------------------------------------------------------
# ПАРАЛЛЕЛЬНЫЙ ПРОГОН ОДНОЙ ПАРТИИ (A ‖ B)
# ---------------------------------------------------------------------------
def run_batch(node: str, cline_bin: str, base: Path, kind: str, prompt: str,
              timeout: int) -> dict:
    cwd = base / kind.upper()
    cwd.mkdir(parents=True, exist_ok=True)
    started = time.time()
    proc = start_run(node, cline_bin, cwd, prompt, timeout)
    return {"kind": kind, "cwd": cwd, "proc": proc, "started": started,
            "prompt": prompt}


def history_sessions(entries: list[dict], base: Path) -> list[dict]:
    prefix = str(base).lower()
    found = []
    for e in entries:
        if str(e.get("cwd", "")).lower().startswith(prefix):
            found.append(e)
    return found


def overlaps(a: dict, b: dict) -> bool:
    try:
        s_a = a.get("startedAt") or ""
        e_a = a.get("endedAt") or "9999"
        s_b = b.get("startedAt") or ""
        e_b = b.get("endedAt") or "9999"
    except Exception:
        return False
    return s_a <= e_b and s_b <= e_a


def _iso(ts: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(ts))


# ---------------------------------------------------------------------------
# RUNTIME BACKEND (wrapper поверх start_run/collect_run — семантика A/B та же)
# ---------------------------------------------------------------------------
class ClineRunner:
    """Два процесса Cline; sessionId/перекрытие — из истории Cline."""

    name = "cline"

    def __init__(self, node: str, cline_bin: str):
        self.node, self.cline_bin = node, cline_bin

    def start(self, base: Path, kind: str, prompt: str, timeout: int) -> dict:
        return run_batch(self.node, self.cline_bin, base, kind, prompt, timeout)

    def alive(self, run: dict) -> bool:
        return run["proc"].poll() is None

    def handles(self, runs: list[dict]) -> str:
        return "PIDs: " + ", ".join(str(r["proc"].pid) for r in runs)

    def collect(self, run: dict, timeout: int, kill_grace: int) -> dict:
        res = collect_run(run["proc"], run["kind"].upper(), timeout, run["started"])
        res["cwd"] = str(run["cwd"])
        res["pid"] = run["proc"].pid
        res["prompt"] = run["prompt"]
        res["session_id"] = ""
        return res

    def session_report(self, base: Path) -> list[dict]:
        entries = cline_history(self.node, self.cline_bin, limit=30)
        return history_sessions(entries, base)

    def close(self) -> None:          # процессы уже завершены collect_run
        pass


class OpenCodeRunner:
    """A и B — два потока на один adapter OpenCode: у каждого запуска СВОЯ
    session (adapter.run создаёт новую), sessionId берём из результата."""

    name = "opencode"

    def __init__(self, adapter):
        self.adapter = adapter
        self.records: list[dict] = []

    def start(self, base: Path, kind: str, prompt: str, timeout: int) -> dict:
        cwd = base / kind.upper()
        cwd.mkdir(parents=True, exist_ok=True)
        run = {"kind": kind, "cwd": cwd, "prompt": prompt, "timeout": timeout,
               "started": time.time(), "box": {}, "thread": None}

        def worker() -> None:
            run["box"]["outcome"] = self.adapter.run(
                prompt, cwd, timeout, None,
                kill_grace=int(os.environ.get("AINOVELEDIT_KILL_GRACE", "60")))

        thread = threading.Thread(target=worker, daemon=True, name=f"oc-{kind}")
        run["thread"] = thread
        thread.start()
        return run

    def alive(self, run: dict) -> bool:
        return run["thread"].is_alive()

    def handles(self, runs: list[dict]) -> str:
        return "threads: " + ", ".join(str(r["thread"].ident) for r in runs)

    def collect(self, run: dict, timeout: int, kill_grace: int) -> dict:
        run["thread"].join(timeout + max(kill_grace, 0) + 60)
        ended = time.time()
        outcome = run["box"].get("outcome")
        if outcome is None:
            failure, text, finish, session_id = \
                "поток не завершился в отведённое время", "", None, ""
        else:
            failure = None if outcome.ok else f"{outcome.error}: {outcome.detail}"
            if not failure and not outcome.text.strip():
                failure = "пустой результат"
            text, finish, session_id = outcome.text, outcome.finish_reason, \
                outcome.session_id
        self.records.append({
            "sessionId": session_id or None, "pid": None,
            "startedAt": _iso(run["started"]), "endedAt": _iso(ended),
            "cwd": str(run["cwd"]),
        })
        return {"label": run["kind"].upper(), "exit": None, "finish": finish,
                "text": text, "events": 0,
                "error_events": [failure] if failure else [],
                "stdout": "", "stderr": "", "duration": round(ended - run["started"], 1),
                "failure": failure, "cwd": str(run["cwd"]), "pid": None,
                "prompt": run["prompt"], "session_id": session_id}

    def session_report(self, base: Path) -> list[dict]:
        prefix = str(base).lower()
        return [s for s in self.records
                if str(s.get("cwd", "")).lower().startswith(prefix)]

    def close(self) -> None:
        self.adapter.close()


# ---------------------------------------------------------------------------
# ОСНОВНОЙ ПРОГОН
# ---------------------------------------------------------------------------
def audit(chapter_arg: str, volume: int | None, blocks_spec: str | None,
          timeout: int, batch_size: int, self_test: bool, dry_run: bool,
          keep_temp: bool, no_merge: bool, force: bool, retries: int,
          runtime: str = "cline", model: str | None = None,
          provider: str | None = None, server_url: str | None = None,
          server_password: str | None = None) -> int:
    if runtime not in RUNTIMES:
        print(f"ОШИБКА: неизвестный runtime {runtime!r} "
              f"(доступны: {', '.join(RUNTIMES)})")
        return EXIT_USAGE

    node, cline_bin = None, None
    if runtime == "cline":
        node, cline_bin = resolve_cline()
        if not node or not cline_bin:
            print("ОШИБКА: Cline не найден (задайте CLINE_BIN или установите cline).")
            return EXIT_NO_RUNTIME
        runner: ClineRunner | OpenCodeRunner = ClineRunner(node, cline_bin)
    else:
        # opencode: модель НЕ выдумывается — только из --model.
        if not (model or "").strip():
            print("ОШИБКА: для --runtime opencode укажите --model \"<MODEL_ID>\" "
                  "(провайдер — опциональный --provider); выдумывать ID нельзя")
            return EXIT_NO_RUNTIME
        try:
            adapter = rt.OpenCodeAdapter(
                model=model.strip(), provider=(provider or None),
                server_url=server_url, server_password=server_password)
        except (RuntimeError, ValueError) as exc:
            print(f"ОШИБКА: {exc}")
            return EXIT_NO_RUNTIME
        runner = OpenCodeRunner(adapter)

    try:
        ch = parse_chapter_arg(chapter_arg, volume)
        ja_blocks, ru_blocks = load_chapter_blocks(ch)
    except (ValueError, FileNotFoundError) as exc:
        print(f"ОШИБКА: {exc}")
        return EXIT_USAGE

    all_blocks = sorted(set(ja_blocks) & set(ru_blocks))
    if not all_blocks:
        print("ОШИБКА: не найдено ни одного блока, доступного и в JA, и в RU.")
        return EXIT_USAGE
    targets = parse_blocks(blocks_spec) or all_blocks
    missing = [b for b in targets if b not in ja_blocks or b not in ru_blocks]
    if missing:
        print(f"ОШИБКА: блоки отсутствуют в JA или RU: {missing}")
        print(f"  доступные блоки: {all_blocks[0]}–{all_blocks[-1]}")
        return EXIT_USAGE
    if batch_size:
        limited = [targets[i:i + batch_size] for i in range(0, len(targets), batch_size)]
        # batch_size задаёт верхнюю границу; общий лимит длины учитывает chunk_blocks
    else:
        limited = None

    skills = {}
    try:
        for kind in ("a", "b"):
            skills[kind] = load_skill(kind)
    except FileNotFoundError as exc:
        print(f"ОШИБКА: {exc}")
        return EXIT_USAGE

    # Один material на партию — A и B получают ИДЕНТИЧНЫЕ данные.
    chunks = []
    for group in (limited or [targets]):
        for sub in chunk_blocks(group, ja_blocks, ru_blocks, skills["a"]):
            chunks.append(sub)

    print(f"Глава {ch.chapter_id_full} ({ch.file_name})")
    print(f"  JA: {ch.ja_path}")
    print(f"  RU: {ch.output_path}")
    print(f"  блоки аудита: {', '.join(str(b) for b in targets)}")
    print(f"  партий (A‖B): {len(chunks)}")
    if runtime == "cline":
        print(f"  Cline: {cline_bin}")
    else:
        print(f"  runtime: opencode, model={model}"
              + (f" (provider={provider})" if provider else " (provider: по model)")
              + (f", server={server_url}" if server_url else ""))

    # Существующие результаты мешают правилу «файлы появляются только после
    # успешного завершения обоих аудиторов» — убираем их ДО запуска.
    if not self_test and not dry_run:
        existing = [
            OUT_DIR / f"{ch.chapter_id_full}-sma-{k}.json" for k in ("a", "b")
        ]
        existing = [p for p in existing if p.exists()]
        if existing and not force:
            print("ОШИБКА: файлы аудита уже существуют: "
                  + ", ".join(p.name for p in existing))
            print("  Удалите их или запустите с --force.")
            return EXIT_USAGE
        for path in existing:
            path.unlink()
        if existing:
            print("OK: удалены существующие файлы (--force): "
                  + ", ".join(p.name for p in existing))

    run_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}"
    base = RUN_ROOT / run_id

    # --- статические проверки (всегда, до запусков) --------------------------
    materials = [build_material(ch, g, ja_blocks, ru_blocks) for g in chunks]
    prompts = {
        kind: [build_prompt(kind, ch, g, m, skills[kind])
               for g, m in zip(chunks, materials)]
        for kind in ("a", "b")
    }
    static_checks: list[tuple[str, bool, str]] = []
    static_checks.append((
        "MATERIAL у A и B идентичен",
        all(
            _extract(prompts["a"][i], "MATERIAL") == _extract(prompts["b"][i], "MATERIAL")
            for i in range(len(chunks))
        ),
        "раздел MATERIAL полностью совпадает у обоих агентов",
    ))
    static_checks.append((
        "промпт не содержит идентификаторов другого аудитора (без скилла)",
        all(
            AUDITORS["b"]["audit_id"] not in _strip_skill(prompts["a"][i])
            and AUDITORS["b"]["audit_type"] not in _strip_skill(prompts["a"][i])
            and AUDITORS["a"]["audit_id"] not in _strip_skill(prompts["b"][i])
            and AUDITORS["a"]["audit_type"] not in _strip_skill(prompts["b"][i])
            for i in range(len(chunks))
        ),
        "вне секции SKILL промпт A не ссылается на sma-b/semantic-audit-b "
        "и наоборот (в самих скиллах друг упоминается только как исключение)",
    ))
    static_checks.append((
        "в промпте нет путей к проекту (output/_audit и др.)",
        all(str(AINOVELEDIT) not in p and str(OUT_DIR) not in p
            for kind in ("a", "b") for p in prompts[kind]),
        "пути к файлам проекта в prompt не попадают",
    ))

    if dry_run:
        print("\nDRY RUN: процессы не запускаются.")
        for i, group in enumerate(chunks):
            print(f"  партия {i + 1}: блоки {group}")
            print(f"    prompt A: {len(prompts['a'][i])} симв., "
                  f"prompt B: {len(prompts['b'][i])} симв.")
        for name, ok, detail in static_checks:
            print(f"  [{'OK' if ok else 'FAIL'}] {name} — {detail}")
        return EXIT_OK if all(ok for _, ok, _ in static_checks) else EXIT_VALIDATE

    try:
        base.mkdir(parents=True, exist_ok=True)
        workspace_a = base / "A"
        workspace_b = base / "B"
        workspace_a.mkdir(parents=True, exist_ok=True)
        workspace_b.mkdir(parents=True, exist_ok=True)

        # Проверка №6: output/_audit не внутри cwd агентов.
        audit_inside = any(
            str(OUT_DIR).lower().startswith(str(w).lower())
            for w in (workspace_a, workspace_b)
        )
        static_checks.append((
            "output/_audit проекта не находится внутри cwd",
            not audit_inside and OUT_DIR.resolve() != workspace_a.resolve()
            and OUT_DIR.resolve() != workspace_b.resolve(),
            f"cwd A={workspace_a}, cwd B={workspace_b}",
        ))
        static_checks.append((
            "cwd A и cwd B различаются, оба пусты",
            workspace_a.resolve() != workspace_b.resolve()
            and not any(workspace_a.iterdir()) and not any(workspace_b.iterdir()),
            "временные workspace созданы и пусты",
        ))

        results: dict[str, dict] = {}
        payloads: dict[str, dict] = {}
        timing: dict[str, float] = {}
        alive_flags: list[bool] = []
        wrote_after_both = True
        written_at: float | None = None
        files_before = _audit_snapshot(ch)
        kill_grace = int(os.environ.get("AINOVELEDIT_KILL_GRACE", "60"))

        for i, group in enumerate(chunks):
            print(f"\nпартия {i + 1}/{len(chunks)}: блоки {group} — запуск A ‖ B")
            batch_ok = False
            finished: dict[str, dict] = {}
            payloads_ok: dict[str, dict] = {}
            last_errors: list[str] = []

            for attempt in range(1, retries + 2):
                runs = [
                    runner.start(base, kind, prompts[kind][i], timeout)
                    for kind in ("a", "b")
                ]
                time.sleep(1.0)
                both_alive = len(runs) == 2 and all(runner.alive(r) for r in runs)
                alive_flags.append(both_alive)
                print(f"  запуски одновременно активны: {'да' if both_alive else 'нет'} "
                      f"({runner.handles(runs)})")

                finished = {}
                for r in runs:
                    res = runner.collect(r, timeout, kill_grace)
                    finished[r["kind"]] = res
                    timing[r["kind"]] = time.time()
                    status = "OK" if not res["failure"] else f"FAIL ({res['failure']})"
                    ident = ("session=" + res["session_id"]
                             if res.get("session_id")
                             else f"exit={res['exit']}")
                    print(f"  {r['kind'].upper()}: {ident} "
                          f"finish={res['finish']} {res['duration']}с — {status}")

                last_errors = []
                payloads_ok = {}
                for kind in ("a", "b"):
                    res = finished[kind]
                    if res["failure"]:
                        last_errors.append(f"{kind.upper()}: {res['failure']}")
                        continue
                    payload, errors, note = validate_payload(kind, ch, group, res["text"])
                    if errors:
                        last_errors.append(f"{kind.upper()}: " + "; ".join(errors))
                        continue
                    if note:
                        print(f"  {kind.upper()}: предупреждение — {note}")
                    payloads_ok[kind] = payload

                if not last_errors:
                    batch_ok = True
                    break
                if attempt <= retries:
                    print(f"  повтор {attempt}/{retries}: {'; '.join(last_errors)}")

            if not batch_ok:
                print(f"\nОШИБКА: партия {i + 1} не выполнена:")
                for err in last_errors:
                    print(f"  - {err}")
                for kind in ("a", "b"):
                    res = finished.get(kind, {})
                    if not res.get("failure"):
                        if any(e.startswith(kind.upper() + ":") for e in last_errors):
                            print(f"  {kind.upper()} сырой ответ: {res['text'][:600]}")
                        continue
                    print(f"  {kind.upper()}: "
                          + (f"session={res.get('session_id')} "
                             if res.get("session_id")
                             else f"exit={res.get('exit')} ")
                          + f"finish={res.get('finish')}")
                    if res.get("error_events"):
                        print(f"    события ошибок: {res['error_events']}")
                    if (res.get("stderr") or "").strip():
                        print(f"    stderr: {res['stderr'].strip()[:400]}")
                    if not (res.get("text") or "").strip():
                        print(f"    stdout: {res['stdout'][:400]}")
                _cleanup(base, keep_temp, runner)
                run_failed = [k for k in ("a", "b") if finished.get(k, {}).get("failure")]
                if run_failed:
                    return EXIT_RUN_A if run_failed[0] == "a" else EXIT_RUN_B
                return EXIT_VALIDATE

            for kind in ("a", "b"):
                res = finished[kind]
                payload = payloads_ok[kind]
                results[kind] = res
                payloads.setdefault(kind, {"findings": []})
                payloads[kind].setdefault("audit_id", AUDITORS[kind]["audit_id"])
                payloads[kind].setdefault("audit_type", AUDITORS[kind]["audit_type"])
                payloads[kind].setdefault("chapter", ch.chapter_id_full)
                payloads[kind].setdefault("blocks", [])
                payloads[kind]["blocks"] = sorted(
                    set(payloads[kind]["blocks"]) | set(group)
                )
                payloads[kind]["findings"].extend(payload.get("findings", []))

            if self_test:
                # Проверка №7: во время прогонов файлы результатов не меняются
                # (снимок берётся до старта партий — уже существующие файлы
                # предыдущих запусков не считаются нарушением).
                wrote_after_both = wrote_after_both and (
                    _audit_snapshot(ch) == files_before
                )
        # --- конец партий -------------------------------------------------

        if self_test:
            written_at = None
        else:
            # Правило 13: запись ТОЛЬКО после успеха обоих агентов (всех партий).
            time_a = timing.get("a", 0.0)
            time_b = timing.get("b", 0.0)
            path_a, path_b = write_outputs(ch, payloads["a"], payloads["b"])
            written_at = time.time()
            wrote_after_both = written_at >= max(time_a, time_b)
            print(f"\nOK: записаны {path_a.name} и {path_b.name} "
                  f"(после завершения обоих: {'да' if wrote_after_both else 'НЕТ'})")
            if no_merge:
                _cleanup(base, keep_temp, runner)
                return EXIT_OK
            out_json, out_md = run_merge(node, cline_bin, ch, path_a, path_b)
            if out_json is None:
                print("ОШИБКА: merge_findings.py не выполнился.")
                _cleanup(base, keep_temp, runner)
                return EXIT_MERGE
            print(f"OK: merged → {out_json.name}, отчёт → {out_md.name}")

        # --- история: sessionId, перекрытие интервалов ---------------------
        sessions = runner.session_report(base)
        session_ids = [s.get("sessionId") for s in sessions]
        distinct = (len(session_ids) >= 2 and all(session_ids)
                    and len(set(session_ids)) == len(session_ids))
        overlap_ok = any(
            overlaps(sessions[i], sessions[j])
            for i in range(len(sessions))
            for j in range(i + 1, len(sessions))
        )
        session_detail = "; ".join(
            f"{s.get('sessionId')} pid={s.get('pid')} "
            f"{s.get('startedAt')} → {s.get('endedAt')}"
            for s in sessions
        ) or "сессии в истории не найдены"

        # Текст одного аудитора не должен присутствовать в промпте другого.
        leak = False
        for i in range(len(chunks)):
            text_a = results.get("a", {}).get("text", "").strip()
            text_b = results.get("b", {}).get("text", "").strip()
            if text_a and text_a in prompts["b"][i]:
                leak = True
            if text_b and text_b in prompts["a"][i]:
                leak = True

        parallel_started = bool(alive_flags) and all(alive_flags)
        ident = {k: (results[k].get("pid") or results[k].get("session_id"))
                 for k in ("a", "b") if k in results}
        par_label = (
            "процессы запускались одновременно (poll обеих Popen)"
            if runtime == "cline" else
            "запуски шли одновременно (обе нити адаптера активны)"
        )
        hist_label = ("история Cline" if runtime == "cline"
                      else "записи адаптера OpenCode")
        dynamic_checks: list[tuple[str, bool, str]] = [
            ("A и B имеют разные sessionId",
             distinct,
             session_detail + f" | PID/session (факт): {ident}"),
            (par_label,
             parallel_started,
             f"параллельных запусков проверено: {len(alive_flags)}; "
             f"PID/session из запусков: {ident}"),
            (f"интервалы сессий пересекаются ({hist_label})",
             overlap_ok,
             session_detail),
            ("файлы результатов появились только после завершения обоих",
             wrote_after_both,
             "запись выполнена после сбора результатов обоих запусков"
             if written_at else
             "self-test: во время прогонов файлы output/_audit не изменялись"),
            ("текст одного агента отсутствует в промпте другого",
             not leak,
             "prompt A и prompt B построены до запусков и не содержат чужих ответов"),
        ]

        print("\n=== ПРОВЕРКИ ИЗОЛЯЦИИ ===")
        all_checks = static_checks + dynamic_checks
        for name, ok, detail in all_checks:
            print(f"  [{'OK  ' if ok else 'FAIL'}] {name}")
            print(f"         {detail}")
        passed = sum(1 for _, ok, _ in all_checks if ok)
        print(f"\nИтог: {passed}/{len(all_checks)} проверок пройдено")

        _cleanup(base, keep_temp, runner)
        if not ok_of(all_checks):
            return EXIT_VALIDATE
        return EXIT_OK
    except Exception as exc:  # noqa: BLE001 — единая точка очистки temp
        _cleanup(base, keep_temp, runner)
        print(f"ОШИБКА: {type(exc).__name__}: {exc}")
        return EXIT_USAGE


def _extract(prompt: str, marker: str) -> str:
    m = re.search(rf"--- {marker}-BEGIN ---(.*?)--- {marker}-END ---",
                  prompt, re.S)
    return m.group(1).strip() if m else ""


def _strip_skill(prompt: str) -> str:
    """Промпт без секции SKILL: там второй аудитор упоминается по правилу
    «не твоя зона» — это не утечка, а ограничение задачи."""
    return re.sub(r"--- SKILL-BEGIN ---.*?--- SKILL-END ---", "", prompt, flags=re.S)


def _audit_snapshot(ch: Chapter) -> dict[str, tuple[int, int]]:
    """(размер, mtime_ns) файлов sma-* главы — для проверки «не записывали
    во время прогонов»."""
    snap: dict[str, tuple[int, int]] = {}
    if not OUT_DIR.exists():
        return snap
    for path in OUT_DIR.glob(f"{ch.chapter_id_full}-sma-*"):
        st = path.stat()
        snap[path.name] = (st.st_size, st.st_mtime_ns)
    return snap


def _cleanup(base: Path, keep: bool, runner=None) -> None:
    if runner is not None:
        try:
            runner.close()          # opencode: остановить свой serve-процесс
        except Exception as exc:    # noqa: BLE001 — очистка не должна падать
            print(f"  предупреждение: runtime не закрылся: {exc}", file=sys.stderr)
    if keep:
        print(f"  временные каталоги сохранены: {base}")
        return
    shutil.rmtree(base, ignore_errors=True)


def ok_of(checks: list[tuple[str, bool, str]]) -> bool:
    return all(ok for _, ok, _ in checks)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> int:
    setup_encoding()
    ap = argparse.ArgumentParser(
        description="Оркестратор двойного независимого смыслового аудита "
                    "(A + B; runtime: cline | opencode)"
    )
    ap.add_argument("--file", required=True,
                    help="глава: v5-ch02.md / v5-ch02 / v05-ch02")
    ap.add_argument("--volume", type=int, default=None,
                    help="том, если глава указана без префикса vN-")
    ap.add_argument("--blocks", default=None,
                    help="диапазон блоков, напр. 5-7 или 6,8-9 (по умолчанию все)")
    ap.add_argument("--runtime", choices=list(RUNTIMES), default="cline",
                    help="бэкенд запуска A/B: cline (по умолчанию) или opencode "
                         "(OpenCode → OmniRoute → модель из --model)")
    ap.add_argument("--model", default=None,
                    help="model ID для --runtime opencode (ОБЯЗАТЕЛЕН для opencode): "
                         "<MODEL_ID> или <provider>/<MODEL_ID>; не выдумывается")
    ap.add_argument("--provider", default=None,
                    help="providerID для --runtime opencode "
                         "(по умолчанию определяется по model/списку сервера)")
    ap.add_argument("--server-url", default=None,
                    help="подключиться к уже запущенному opencode serve "
                         "вместо запуска своего")
    ap.add_argument("--server-password", default=None,
                    help="пароль opencode serve (иначе OPENCODE_SERVER_PASSWORD "
                         "или ~/.config/opencode/service.json)")
    ap.add_argument("--timeout", type=int, default=300,
                    help="таймаут одного запуска (Cline/OpenCode), сек "
                         "(по умолчанию 300)")
    ap.add_argument("--batch-size", type=int, default=0,
                    help="максимум блоков в одном прогоне (0 = автоподбор по длине)")
    ap.add_argument("--self-test", action="store_true",
                    help="инфраструктурный тест изоляции; файлы не записываются")
    ap.add_argument("--dry-run", action="store_true",
                    help="только построить промпты и проверить их, без запуска")
    ap.add_argument("--keep-temp", action="store_true",
                    help="не удалять временные каталоги A/B")
    ap.add_argument("--force", action="store_true",
                    help="удалить уже существующие sma-a.json / sma-b.json")
    ap.add_argument("--no-merge", action="store_true",
                    help="не запускать merge_findings.py")
    ap.add_argument("--retries", type=int, default=0,
                    help="число повторных прогонов партии при сбое runtime "
                         "или невалидном ответе (по умолчанию 0)")
    args = ap.parse_args()

    return audit(
        chapter_arg=args.file,
        volume=args.volume,
        blocks_spec=args.blocks,
        timeout=args.timeout,
        batch_size=args.batch_size,
        self_test=args.self_test,
        dry_run=args.dry_run,
        keep_temp=args.keep_temp,
        no_merge=args.no_merge,
        force=args.force,
        retries=args.retries,
        runtime=args.runtime,
        model=args.model,
        provider=args.provider,
        server_url=args.server_url,
        server_password=args.server_password,
    )


if __name__ == "__main__":
    sys.exit(main())
