#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
llm_runtime.py — минимальный runtime adapter для запуска LLM из Python.

Отделяет семантику (verify_findings.py, run_semantic_audit.py) от способа
запуска модели. Сегодня реализован только адаптер Cline; новые runtime
(Opencode, OpenAI-compatible HTTP и т.п.) добавляются новым классом с тем же
интерфейсом `run(prompt, cwd, timeout) -> RunOutcome`.

Адаптер Cline:

* передаёт промпт в argv процесса (CreateProcessW / UTF-16, без shell);
* работает в пустом cwd и с изолированным data-dir — глобальный
  `~/.cline/data/settings/providers.json` не изменяется;
* `-m` / `-P` НЕ передаются: модель задаётся записью в КОПИЮ providers.json
  изолированного data-dir;
* классифицирует исход: OK / TIMEOUT / MODEL_ERROR / PROCESS_ERROR.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

OK = None
TIMEOUT = "TIMEOUT"
MODEL_ERROR = "MODEL_ERROR"
PROCESS_ERROR = "PROCESS_ERROR"

GLOBAL_DATA_DIR = Path.home() / ".cline" / "data"


@dataclass
class RunOutcome:
    """Результат одного вызова LLM."""
    text: str = ""
    exit_code: int | None = None
    finish_reason: str | None = None
    duration: float = 0.0
    error: str | None = OK            # None == OK
    detail: str = ""                  # пояснение ошибки
    stderr: str = ""
    stdout_tail: str = ""
    model: str = ""
    usage: dict = field(default_factory=dict)


def resolve_cline() -> tuple[str, str] | tuple[None, None]:
    """→ (node, cline_bin) или (None, None). Без -m / -P."""
    candidates = []
    override = os.environ.get("CLINE_BIN")
    if override:
        candidates.append(Path(override))
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(Path(appdata) / "npm" / "node_modules" / "cline"
                          / "bin" / "cline")
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


def prepare_data_dir(dest: Path, model: str, provider: str = "cline") -> Path:
    """Копия пользовательского data-dir с подменённой моделью.

    Глобальный providers.json не читается обратно и не изменяется: пишется
    только копия внутри `dest`.
    """
    src_dir = GLOBAL_DATA_DIR / "settings"
    dst_dir = dest / "settings"
    dst_dir.mkdir(parents=True, exist_ok=True)
    src = src_dir / "providers.json"
    if not src.exists():
        raise FileNotFoundError(f"нет {src} — нечем авторизовать runtime")
    data = json.loads(src.read_text(encoding="utf-8"))
    data["lastUsedProvider"] = provider
    prov = data.setdefault("providers", {}).setdefault(provider, {})
    settings = prov.setdefault("settings", {})
    settings["provider"] = provider
    settings["model"] = model
    prov["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    (dst_dir / "providers.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


def _classify(exit_code: int | None, finish: str | None, text: str,
              run_result_seen: bool, local_timeout: bool) -> tuple[str | None, str]:
    if local_timeout:
        return TIMEOUT, "процесс не завершился за отведённое время и был убит"
    if not run_result_seen:
        return PROCESS_ERROR, "run_result не получен (crash процесса или сбой шины)"
    if finish == "aborted":
        return TIMEOUT, "Cline прервал запуск (finishReason=aborted)"
    if finish == "error" or exit_code not in (0,):
        return MODEL_ERROR, f"finishReason={finish!r}, exit={exit_code}, text={text[:200]!r}"
    if not text.strip():
        return MODEL_ERROR, "модель вернула пустой ответ"
    return OK, ""


class ClineAdapter:
    """Запуск одного промпта через Cline CLI (plan mode, --json)."""

    name = "cline"

    def __init__(self, model: str, provider: str = "cline",
                 node: str | None = None, cline_bin: str | None = None,
                 extra_args: list[str] | None = None):
        if node is None or cline_bin is None:
            node, cline_bin = resolve_cline()
        if not node or not cline_bin:
            raise RuntimeError("Cline не найден (CLINE_BIN или установка cline)")
        self.model = model
        self.provider = provider
        self.node = node
        self.cline_bin = cline_bin
        self.extra_args = list(extra_args or [])

    def run(self, prompt: str, cwd: Path, timeout: int,
            data_dir: Path, kill_grace: int = 60) -> RunOutcome:
        """Один вызов LLM. `kill_grace` — сколько секунд ждать после
        `timeout` до жёсткого kill (тестовые прогоны задают 1–2)."""
        cwd = Path(cwd)
        cwd.mkdir(parents=True, exist_ok=True)
        cmd = base_cmd(self.node, self.cline_bin) + [
            "-c", str(cwd),
            "--json",
            "-p",                      # plan mode: инструменты недоступны
            "--data-dir", str(data_dir),
            "-t", str(timeout),
            *self.extra_args,
            prompt,
        ]
        started = time.time()
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, cwd=str(cwd))
        except OSError as exc:
            return RunOutcome(error=PROCESS_ERROR, detail=f"не удалось запустить процесс: {exc}",
                              duration=round(time.time() - started, 2))
        local_timeout = False
        try:
            out_b, err_b = proc.communicate(timeout=timeout + max(kill_grace, 0))
        except subprocess.TimeoutExpired:
            local_timeout = True
            proc.kill()
            out_b, err_b = proc.communicate()
        duration = round(time.time() - started, 2)
        stdout = (out_b or b"").decode("utf-8", "replace")
        stderr = (err_b or b"").decode("utf-8", "replace")

        result, usage, model_id = None, {}, ""
        for line in stdout.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "run_result":
                result = ev
        if result:
            usage = result.get("usage") or {}
            model_id = ((result.get("model") or {}).get("id")) or ""
        text = (result or {}).get("text", "") or ""
        error, detail = _classify(proc.returncode,
                                  (result or {}).get("finishReason"),
                                  text, result is not None, local_timeout)
        if error == PROCESS_ERROR:
            detail = (f"{detail}; stderr: {stderr.strip()[-300:] or '(пусто)'}; "
                      f"stdout: {stdout.strip()[-300:] or '(пусто)'}")
        elif error == MODEL_ERROR and not detail:
            detail = (stderr.strip()[-300:]
                      or stdout.strip()[-300:]
                      or f"exit={proc.returncode}")
        return RunOutcome(
            text=text,
            exit_code=proc.returncode,
            finish_reason=(result or {}).get("finishReason"),
            duration=duration,
            error=error,
            detail=detail,
            stderr=stderr[-1000:],
            stdout_tail=stdout[-1000:],
            model=model_id or self.model,
            usage=usage,
        )


def get_adapter(kind: str = "cline", **kwargs):
    """Фабрика runtime adapters (сейчас только cline)."""
    if kind == "cline":
        return ClineAdapter(**kwargs)
    raise ValueError(f"неизвестный runtime adapter: {kind!r}")
