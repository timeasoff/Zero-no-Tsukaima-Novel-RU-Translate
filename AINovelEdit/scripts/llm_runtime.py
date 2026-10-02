#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
llm_runtime.py — минимальный runtime adapter для запуска LLM из Python.

Отделяет семантику (verify_findings.py, run_semantic_audit.py) от способа
запуска модели. Реализованы два адаптера с ОДНИМ контрактом:

    adapter = get_adapter(kind, model=..., provider=...)
    outcome = adapter.run(prompt, cwd, timeout, data_dir=None, kill_grace=60)
    -> RunOutcome (alias RuntimeResult)

RunOutcome / RuntimeResult:
    status, text, provider, model, duration, usage, session_id, error (+detail).

Адаптер Cline:

* передаёт промпт в argv процесса (CreateProcessW / UTF-16, без shell);
* работает в пустом cwd и с изолированным data-dir — глобальный
  `~/.cline/data/settings/providers.json` не изменяется;
* `-m` / `-P` НЕ передаются: модель задаётся записью в КОПИЮ providers.json
  изолированного data-dir;
* классифицирует исход: OK / TIMEOUT / MODEL_ERROR / PROCESS_ERROR.

Адаптер OpenCode (OpenCode → OmniRoute → model):

* поднимает СОБСТВЕННЫЙ headless-сервер `opencode-cli serve` на свободном
  порту (или подключается к заданному server_url) — глобальный
  `~/.config/opencode/opencode.json` НЕ изменяется;
* каждый вызов `run()` = НОВАЯ session OpenCode с location = пустой cwd;
  session между запусками не переиспользуются (A, B и verifier — разные
  sessions), история разговора не переносится;
* модель передаётся в конкретную session (`model: {providerID, id}`),
  формат model ID не изобретается: либо `provider/model-id` (OpenCode-стиль),
  либо `model-id` с явным provider / провайдером по умолчанию;
* промпт уходит по HTTP (нет лимита длины argv);
* классифицирует исход: OK / TIMEOUT / MODEL_ERROR / HTTP_ERROR /
  AUTH_ERROR / INVALID_RESPONSE / RUNTIME_ERROR — исходная причина
  сохраняется в `detail`.

Runtime adapter НЕ знает ничего о semantic-audit: только
prompt / cwd / model / timeout → response.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

OK = None
TIMEOUT = "TIMEOUT"
MODEL_ERROR = "MODEL_ERROR"
PROCESS_ERROR = "PROCESS_ERROR"
HTTP_ERROR = "HTTP_ERROR"
AUTH_ERROR = "AUTH_ERROR"
INVALID_RESPONSE = "INVALID_RESPONSE"
RUNTIME_ERROR = "RUNTIME_ERROR"

COMPLETED = "completed"

DEFAULT_OPENCODE_PROVIDER = "omniroute"
OPENCODE_SPAWN_TIMEOUT = 60.0
OPENCODE_WAIT_CHUNK = 5.0           # сек на один вызов session/wait

GLOBAL_DATA_DIR = Path.home() / ".cline" / "data"

# Системный прокси (на машине включён) НЕ используется: все запросы идут
# напрямую на 127.0.0.1, поэтому локальные вызовы не уходят наружу.
_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


@dataclass
class RunOutcome:
    """Результат одного вызова LLM (RuntimeResult)."""
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
    status: str = ""                  # "completed" | код ошибки
    provider: str = ""
    session_id: str = ""

    @property
    def ok(self) -> bool:
        return self.error is None


RuntimeResult = RunOutcome


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


# ---------------------------------------------------------------------------
# OpenCode: OpenCode → OmniRoute → модель
# ---------------------------------------------------------------------------
def resolve_opencode() -> str | None:
    """→ путь к opencode-cli (desktop CLI) или None.

    npm-пакет `opencode` НЕ используется: его `serve` отдаёт проксированный
    HTML вместо API. Ищем только desktop CLI (`opencode-cli.exe`).
    """
    candidates: list[Path] = []
    override = os.environ.get("OPENCODE_CLI")
    if override:
        candidates.append(Path(override))
    appdata = os.environ.get("APPDATA")
    if appdata:
        cli_root = Path(appdata) / "ai.opencode.desktop" / "cli"
        if cli_root.is_dir():
            def _ver(p: Path) -> tuple:
                return tuple(int(x) for x in p.name.split(".") if x.isdigit()) or (0,)
            for child in sorted(cli_root.iterdir(), key=_ver, reverse=True):
                exe = child / "opencode-cli.exe"
                if exe.is_file():
                    candidates.append(exe)
    for cand in candidates:
        if cand.is_file():
            return str(cand)
    which = shutil.which("opencode-cli")
    return which


def split_model_ref(model: str, provider: str | None = None,
                    known_providers: set[str] | None = None) -> tuple[str, str]:
    """→ (providerID, model_id) без выдумывания ID.

    * явный provider приоритетен; префикс `provider/` из model срезается;
    * `provider/model` резолвится по первому `/` только если первый сегмент —
      известный provider (GET /api/model) либо `omniroute`;
    * иначе provider = `omniroute`, id = вся строка как есть.
    """
    model = (model or "").strip()
    if not model:
        raise ValueError("model не задан")
    if provider:
        pref = provider + "/"
        if model.startswith(pref):
            model = model[len(pref):]
        if not model:
            raise ValueError(f"после среза префикса {provider!r} model пуста")
        return provider, model
    head, sep, tail = model.partition("/")
    known = known_providers or set()
    if sep and tail and (head in known or head == DEFAULT_OPENCODE_PROVIDER):
        return head, tail
    return DEFAULT_OPENCODE_PROVIDER, model


def classify_opencode_error(err_type: str = "", message: str = "",
                            http_status: int | None = None,
                            local_timeout: bool = False,
                            text: str = "",
                            outcome: str | None = None) -> tuple[str, str]:
    """→ (код_ошибки, detail). Исходная причина сохраняется в detail."""
    bits = []
    if err_type:
        bits.append(err_type)
    if message:
        bits.append(message)
    if http_status not in (None, 200):
        bits.append(f"HTTP {http_status}")
    detail = ": ".join(bits)
    low = f"{err_type} {message}".lower()
    if local_timeout:
        return TIMEOUT, (detail + "; " if detail else "") + \
            "локальный дедлайн исчерпан, сессия прервана"
    if http_status in (401, 403) or "unauthorized" in low \
            or "api key" in low or "apikey" in low:
        return AUTH_ERROR, detail or "нет доступа к API"
    if (err_type.startswith("provider.")
            or "model unavailable" in low or "no route" in low
            or "rate limit" in low or "ratelimit" in low
            or "quota" in low or "model_not_found" in low
            or http_status == 429):
        return MODEL_ERROR, detail or "модель недоступна"
    if http_status == -1:
        return RUNTIME_ERROR, detail or "сетевая ошибка HTTP"
    if http_status is not None and 400 <= http_status <= 599:
        return HTTP_ERROR, detail
    if outcome == "succeeded":
        if not text.strip():
            return INVALID_RESPONSE, "сессия завершилась успешно, но текст ответа пуст"
        return OK, ""
    if outcome == "failed":
        return RUNTIME_ERROR, detail or "session outcome=failed, причина неизвестна"
    if outcome == "interrupted":
        return RUNTIME_ERROR, detail or "session interrupted не нами"
    return RUNTIME_ERROR, detail or "неизвестный исход"


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _basic_auth(password: str) -> str:
    raw = base64.b64encode(f"opencode:{password}".encode("utf-8")).decode("ascii")
    return "Basic " + raw


def _service_password() -> str:
    """Пароль фонового сервиса OpenCode (read-only чтение, ничего не меняется)."""
    try:
        data = json.loads((Path.home() / ".config" / "opencode" / "service.json")
                          .read_text(encoding="utf-8"))
        return str(data.get("password") or "")
    except (OSError, ValueError):
        return ""


def _short(obj, limit: int = 300) -> str:
    if obj is None:
        return ""
    text = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)
    return text[:limit]


class _SseTap:
    """Одно SSE-подключение /api/event: ловит session.execution.failed.

    Единственный источник причины ошибки сессии (в message-логе её нет).
    """

    def __init__(self, base: str, auth: str):
        self.base = base
        self.auth = auth
        self.error: dict | None = None       # data.error {type, message}
        self.connected = False
        self.connect_detail = ""
        self._resp = None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self, sid: str) -> None:
        self._thread = threading.Thread(target=self._loop, args=(sid,),
                                        daemon=True, name=f"sse-{sid[-6:]}")
        self._thread.start()

    def _loop(self, sid: str) -> None:
        req = urllib.request.Request(self.base + "/api/event")
        req.add_header("Authorization", self.auth)
        try:
            resp = _opener.open(req)          # без таймаута: остановка через close()
        except Exception as exc:              # noqa: BLE001
            self.connect_detail = f"{type(exc).__name__}: {exc}"
            return
        self._resp = resp
        self.connected = True
        buf = ""
        try:
            while not self._stop.is_set():
                chunk = resp.read(1)
                if not chunk:
                    break
                buf += chunk.decode("utf-8", "replace")
                if "\n\n" not in buf:
                    continue
                block, buf = buf.split("\n\n", 1)
                for line in block.splitlines():
                    if not line.startswith("data:"):
                        continue
                    try:
                        ev = json.loads(line[5:].strip())
                    except json.JSONDecodeError:
                        continue
                    if ev.get("type") != "session.execution.failed":
                        continue
                    data = ev.get("data") or {}
                    if data.get("sessionID") != sid:
                        continue
                    self.error = data.get("error") or {
                        "type": "unknown",
                        "message": "session.execution.failed без error"}
        except Exception:                     # noqa: BLE001 — закрытие из stop()
            pass
        finally:
            try:
                resp.close()
            except Exception:                 # noqa: BLE001
                pass

    def stop(self) -> None:
        self._stop.set()
        if self._resp is not None:
            try:
                self._resp.close()
            except Exception:                 # noqa: BLE001
                pass
        if self._thread is not None:
            self._thread.join(timeout=2.0)


class OpenCodeAdapter:
    """Один промпт через HTTP API headless-сервера OpenCode.

    Изоляция:
      * сервер — собственный `opencode-cli serve` на свободном порту
        (или подключение к заданному server_url); глобальный
        `~/.config/opencode/opencode.json` только читается, не меняется;
      * каждый run() = НОВАЯ session OpenCode (A, B и verifier — разные
        sessions, история не переносится), location = пустой cwd;
      * запись файлов заблокирована: session не-interactive, адаптер НИКОГДА
        не подтверждает permission-запросы → действия, требующие разрешения,
        отклоняются автоматически (проверено: попытка записи файла в пустой
        cwd не создаёт файлов). Явные deny-all rules в create НЕ передаются:
        сервер помечает такие sessions как внешние, и free tier отвечает
        403 FreeTierError («free tier can only be used from within
        OpenCode»); опция permissions_deny=True оставлена для моделей без
        этого ограничения;
      * модель передаётся в session (`model: {providerID, id}`), формат
        model ID не изобретается (см. split_model_ref).
    """

    name = "opencode"

    def __init__(self, model: str, provider: str | None = None,
                 server_url: str | None = None, server_password: str | None = None,
                 cli: str | None = None, work_dir: str | Path | None = None,
                 agent: str | None = None, user_agent: str | None = None,
                 permissions_deny: bool = False):
        if not (model or "").strip():
            raise ValueError("OpenCodeAdapter: нужен model")
        self.model = model.strip()
        self._provider = provider or None
        self.server_url = (server_url or "").rstrip("/") or None
        self.server_password = server_password or None
        self.cli = cli or resolve_opencode()
        self.work_dir = Path(work_dir) if work_dir else None
        self.agent = agent
        self.user_agent = user_agent          # None → заголовок не ставится
        self.permissions_deny = permissions_deny  # False: см. докстринг (free tier)
        if not self.server_url and not self.cli:
            raise RuntimeError("opencode-cli не найден (OPENCODE_CLI или установка "
                               "OpenCode desktop); npm-пакет `opencode` не поддерживается")
        self.base: str | None = None
        self.auth = ""
        self._proc: subprocess.Popen | None = None
        self._lock = threading.Lock()
        self._providers: set[str] | None = None
        self._seq = 0
        self._server_log: deque = deque(maxlen=400)

    # -- provider ---------------------------------------------------------
    @property
    def provider(self) -> str:
        return self._provider or DEFAULT_OPENCODE_PROVIDER

    # -- сервер -----------------------------------------------------------
    def ensure_server(self) -> None:
        """Поднимает (однократно, потокобезопасно) или подключается к серверу."""
        with self._lock:
            if self.base:
                return
            if self.server_url:
                self.base = self.server_url
                pw = (self.server_password
                      or os.environ.get("OPENCODE_SERVER_PASSWORD")
                      or _service_password())
                self.auth = _basic_auth(pw)
            else:
                self._spawn_server()
            self._check_server()

    def _spawn_server(self) -> None:
        if self.work_dir is None:
            self.work_dir = (Path(tempfile.gettempdir()) / "ainoveledit-opencode"
                             / f"server-{os.getpid()}-{time.strftime('%H%M%S')}")
        self.work_dir.mkdir(parents=True, exist_ok=True)
        port = _free_port()
        cmd = [self.cli, "serve", "--hostname", "127.0.0.1", "--port", str(port)]
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    cwd=str(self.work_dir),
                                    creationflags=_NO_WINDOW)
        except OSError as exc:
            raise RuntimeError(f"не удалось запустить {self.cli}: {exc}") from exc
        self._proc = proc
        state: dict = {}
        ready = threading.Event()

        def pump() -> None:
            assert proc.stdout is not None
            for raw in iter(proc.stdout.readline, b""):
                line = raw.decode("utf-8", "replace").rstrip("\r\n")
                self._server_log.append(line)
                if not state.get("url") and line.startswith("server listening on "):
                    state["url"] = line[len("server listening on "):].strip()
                if not state.get("pw") and line.startswith("server password "):
                    state["pw"] = line[len("server password "):].strip()
                if state.get("url") and state.get("pw"):
                    ready.set()
            ready.set()                       # процесс умер — не ждём дальше
            try:
                proc.stdout.close()
            except OSError:
                pass

        threading.Thread(target=pump, daemon=True, name="oc-serve-pump").start()
        if not ready.wait(OPENCODE_SPAWN_TIMEOUT) or not state.get("url"):
            tail = " | ".join(list(self._server_log)[-8:])
            try:
                proc.kill()
            except OSError:
                pass
            raise RuntimeError(
                f"opencode serve не поднялся за {OPENCODE_SPAWN_TIMEOUT:.0f}s: {tail}")
        self.base = str(state["url"]).rstrip("/")
        self.auth = _basic_auth(str(state.get("pw") or ""))

    def _check_server(self) -> None:
        st, body = self._http("GET", "/api/info", timeout=15)
        if st == 200 and isinstance(body, dict) and body.get("version"):
            return
        detail = _short(body)
        if self._proc is not None:
            try:
                self._proc.kill()
            except OSError:
                pass
        if st == 401:
            raise RuntimeError("сервер OpenCode отклонил авторизацию (401): "
                               "проверьте server_password")
        raise RuntimeError(f"сервер OpenCode не отвечает по API "
                           f"(HTTP {st}, /api/info): {detail}")

    def _http(self, method: str, path: str, body: dict | None = None,
              timeout: float = 30.0) -> tuple[int, object]:
        url = (self.base or "") + path
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", self.auth)
        if self.user_agent:
            req.add_header("User-Agent", self.user_agent)
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with _opener.open(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", "replace")
                if not raw.strip():
                    return resp.status, None
                try:
                    return resp.status, json.loads(raw)
                except json.JSONDecodeError:
                    return resp.status, raw
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            try:
                return exc.code, json.loads(raw)
            except json.JSONDecodeError:
                return exc.code, raw
        except Exception as exc:              # noqa: BLE001 — таймаут/сеть
            return -1, f"{type(exc).__name__}: {exc}"

    def _known_providers(self) -> set[str]:
        with self._lock:
            if self._providers is not None:
                return self._providers
        provs: set[str] = set()
        for attempt in range(2):          # models подгружаются асинхронно:
            if attempt:                   # первый ответ может быть пустым
                time.sleep(1.5)
            st, body = self._http("GET", "/api/model", timeout=30)
            if st == 200 and isinstance(body, dict):
                for item in body.get("data") or []:
                    pid = item.get("providerID")
                    if pid:
                        provs.add(pid)
            if provs:
                break
        with self._lock:
            if provs:                      # пустой список НЕ кэшируем
                self._providers = provs
        return provs

    # -- основной вызов ----------------------------------------------------
    def run(self, prompt: str, cwd: Path, timeout: int,
            data_dir: Path | None = None, kill_grace: int = 60,
            model: str | None = None) -> RunOutcome:
        """Один вызов LLM. `data_dir` не используется (OpenCode не нужен).

        `model` — разовый override (для самопроверки адаптера).
        """
        cwd = Path(cwd)
        cwd.mkdir(parents=True, exist_ok=True)
        started = time.time()
        deadline = started + max(int(timeout), 1)
        with self._lock:
            self._seq += 1
            seq = self._seq

        def fail(error: str, detail: str, session_id: str = "",
                 text: str = "", usage: dict | None = None,
                 model_ref: str = "", finish: str | None = None) -> RunOutcome:
            return RunOutcome(text=text, duration=round(time.time() - started, 2),
                              error=error, detail=detail,
                              finish_reason=finish,
                              model=model_ref or (model or self.model),
                              usage=usage or {}, status=error or COMPLETED,
                              provider=self.provider, session_id=session_id)

        try:
            self.ensure_server()
        except Exception as exc:              # noqa: BLE001
            return fail(RUNTIME_ERROR, f"сервер OpenCode недоступен: {exc}")

        try:
            pid, mid = split_model_ref(model or self.model, self._provider,
                                       self._known_providers())
        except ValueError as exc:
            return fail(RUNTIME_ERROR, str(exc))
        model_ref = f"{pid}/{mid}"

        # --- новая session на каждый run() --------------------------------
        payload: dict = {
            "title": f"ainoveledit-{seq}-{time.strftime('%H%M%S')}",
            "model": {"providerID": pid, "id": mid},
            "location": {"directory": str(cwd)},
        }
        if self.permissions_deny:
            # ВНИМАНИЕ: deny-all rules помечают session как внешнюю — free
            # tier (provider opencode) в этом случае даёт 403 FreeTierError.
            payload["permissions"] = [
                {"action": "*", "resource": "*", "effect": "deny"}]
        if self.agent:
            payload["agent"] = self.agent
        st, body = self._http("POST", "/api/session", payload, timeout=30)
        if st != 200:
            err, detail = classify_opencode_error(
                http_status=st, message=_short(body))
            return fail(err, f"создание session: {detail}", model_ref=model_ref)
        sid = ((body or {}).get("data") or {}).get("id") or ""
        if not sid:
            return fail(RUNTIME_ERROR, f"создание session: нет id в ответе: "
                                       f"{_short(body)}", model_ref=model_ref)

        tap = _SseTap(self.base or "", self.auth)
        tap.start(sid)
        try:
            return self._drive(sid, prompt, cwd, tap, deadline, started,
                               kill_grace, model_ref, seq)
        finally:
            tap.stop()

    def _drive(self, sid: str, prompt: str, cwd: Path, tap: _SseTap,
               deadline: float, started: float, kill_grace: int,
               model_ref: str, seq: int) -> RunOutcome:
        def fail(error: str, detail: str, text: str = "", usage: dict | None = None,
                 finish: str | None = None) -> RunOutcome:
            return RunOutcome(text=text, duration=round(time.time() - started, 2),
                              error=error, detail=detail, finish_reason=finish,
                              model=model_ref, usage=usage or {},
                              status=error or COMPLETED, provider=self.provider,
                              session_id=sid,
                              stdout_tail="\n".join(list(self._server_log)[-20:]))

        # --- prompt --------------------------------------------------------
        st, body = self._http("POST", f"/api/session/{sid}/prompt",
                              {"text": prompt}, timeout=30)
        if st != 200:
            err, detail = classify_opencode_error(http_status=st,
                                                  message=_short(body))
            return fail(err, f"prompt не принят: {detail}")
        prompt_created = ((body or {}).get("data") or {}).get("time", {}) \
                         .get("created", 0) or 0

        # --- ожидание idle --------------------------------------------------
        idle: dict | None = None
        timed_out = False
        net_fails = 0
        while True:
            if time.time() >= deadline:
                timed_out = True
                break
            self._http("POST", f"/api/experimental/session/{sid}/wait",
                       timeout=min(OPENCODE_WAIT_CHUNK,
                                   max(0.5, deadline - time.time())))
            st, msgs = self._http("GET",
                                  f"/api/session/{sid}/message?order=asc&limit=200",
                                  timeout=20)
            if st == -1:
                net_fails += 1
                if net_fails >= 3:
                    return fail(RUNTIME_ERROR,
                                f"сервер перестал отвечать во время ожидания: "
                                f"{_short(msgs)}")
            else:
                net_fails = 0
                for m in (msgs or {}).get("data") or []:
                    if m.get("type") == "idle" and \
                            (m.get("time") or {}).get("created", 0) >= prompt_created:
                        idle = m
                        break
            if idle is not None:
                break
            if time.time() >= deadline:
                timed_out = True
                break
            time.sleep(0.2)

        # --- чтение сообщений ------------------------------------------------
        st, msgs = self._http("GET",
                              f"/api/session/{sid}/message?order=asc&limit=200",
                              timeout=20)
        data = (msgs or {}).get("data") if st == 200 else None
        parts: list[str] = []
        finish, usage, aerr = None, {}, None
        for m in data or []:
            if m.get("type") != "assistant":
                continue
            if (m.get("time") or {}).get("created", 0) < prompt_created:
                continue
            for c in m.get("content") or []:
                if c.get("type") == "text" and c.get("text"):
                    parts.append(c["text"])
            finish = m.get("finish") or finish
            if m.get("tokens"):
                usage = m["tokens"]
            if m.get("error"):
                aerr = m["error"]
        text = "\n".join(p for p in parts if p)

        st_s, ses = self._http("GET", f"/api/session/{sid}", timeout=15)
        if st_s == 200 and isinstance(ses, dict):
            tokens = (ses.get("data") or {}).get("tokens") or {}
            if tokens.get("input") or tokens.get("output"):
                usage = tokens

        # --- таймаут: прерываем ---------------------------------------------
        if timed_out:
            self._http("POST", f"/api/session/{sid}/interrupt", timeout=10)
            grace_end = time.time() + min(max(kill_grace, 0), 15)
            while time.time() < grace_end:
                st_i, m_i = self._http(
                    "GET", f"/api/session/{sid}/message?order=asc&limit=200",
                    timeout=10)
                if st_i == 200 and any(
                        m.get("type") == "idle"
                        and (m.get("time") or {}).get("created", 0) >= prompt_created
                        for m in (m_i or {}).get("data") or []):
                    break
                time.sleep(0.5)
            detail = (f"локальный дедлайн {int(deadline - started)}s исчерпан; "
                      f"session прервана (interrupt)")
            if tap.error:
                detail += f"; причина до прерывания: {tap.error}"
            return fail(TIMEOUT, detail, text=text, usage=usage, finish=finish)

        outcome = (idle or {}).get("outcome")
        cause = aerr or tap.error or {}
        err, detail = classify_opencode_error(
            err_type=str(cause.get("type") or ""),
            message=str(cause.get("message") or ""),
            http_status=cause.get("status"),
            text=text, outcome=outcome)
        if outcome == "failed" and not cause and not tap.connected:
            detail += f"; SSE не подключён ({tap.connect_detail})"
        return fail(err, detail, text=text, usage=usage, finish=finish)

    # -- завершение ---------------------------------------------------------
    def close(self) -> None:
        proc, self._proc = self._proc, None
        if proc is not None and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except (OSError, subprocess.TimeoutExpired):
                try:
                    proc.kill()
                except OSError:
                    pass

    def __enter__(self) -> "OpenCodeAdapter":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


def get_adapter(kind: str = "cline", **kwargs):
    """Фабрика runtime adapters: `cline` | `opencode`."""
    key = (kind or "cline").strip().lower().replace("-", "_")
    if key == "cline":
        return ClineAdapter(**kwargs)
    if key == "opencode":
        return OpenCodeAdapter(**kwargs)
    raise ValueError(f"неизвестный runtime adapter: {kind!r}")


# ---------------------------------------------------------------------------
# CLI self-test адаптера OpenCode (без semantic-audit)
# ---------------------------------------------------------------------------
SELF_TEST_PROMPT = "Return exactly: OPEN_CODE_RUNTIME_OK"


def opencode_self_test(model: str, provider: str | None = None,
                       timeout: int = 120, kill_grace: int = 10,
                       server_url: str | None = None,
                       server_password: str | None = None,
                       fake_model: str = "omniroute/__ainoveledit_missing__",
                       fake_timeout: int = 2) -> int:
    """Проверки адаптера: OK / session-isolation / filesystem-isolation /
    MODEL_ERROR / TIMEOUT. Возвращает код выхода (0 = всё сошлось)."""
    checks: list[tuple[str, bool, str]] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, bool(ok), detail))

    root = (Path(tempfile.gettempdir()) / "ainoveledit-opencode"
            / f"selftest-{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}")
    root.mkdir(parents=True, exist_ok=True)
    print(f"self-test OpenCodeAdapter: model={provider + '/' if provider else ''}"
          f"{model}\ncwd-корень: {root}\n")

    adapter = OpenCodeAdapter(model=model, provider=provider,
                              server_url=server_url,
                              server_password=server_password)
    try:
        # 1. базовый вызов
        cwd1 = root / "run1"
        out1 = adapter.run(SELF_TEST_PROMPT, cwd1, timeout,
                           kill_grace=kill_grace)
        add("self-test: статус completed", out1.status == COMPLETED,
            f"{out1.status}: {out1.detail}")
        add("self-test: в ответе OPEN_CODE_RUNTIME_OK",
            "OPEN_CODE_RUNTIME_OK" in out1.text, repr(out1.text[:200]))
        add("self-test: session_id получен", bool(out1.session_id),
            out1.session_id)
        add("self-test: cwd остался пустым",
            not any(cwd1.iterdir()) if cwd1.is_dir() else False,
            str(list(cwd1.iterdir())) if cwd1.is_dir() else "нет cwd")
        print(f"  session #1: {out1.session_id} "
              f"({out1.duration}s, model={out1.model})")

        # 2. второй вызов — новая session
        cwd2 = root / "run2"
        out2 = adapter.run(SELF_TEST_PROMPT, cwd2, timeout,
                           kill_grace=kill_grace)
        add("run#2: статус completed", out2.status == COMPLETED,
            f"{out2.status}: {out2.detail}")
        add("run#2: новая session (изоляция history)",
            bool(out1.session_id) and out2.session_id != out1.session_id,
            f"{out1.session_id} == {out2.session_id}")
        print(f"  session #2: {out2.session_id} ({out2.duration}s)")

        # 3. заведомо несуществующая модель → MODEL_ERROR
        cwd3 = root / "run3"
        out3 = adapter.run(SELF_TEST_PROMPT, cwd3, min(timeout, 60),
                           kill_grace=kill_grace, model=fake_model)
        add("fake model → MODEL_ERROR", out3.error == MODEL_ERROR,
            f"{out3.error}: {out3.detail}")
        add("fake model: причина сохранена в detail", bool(out3.detail),
            out3.detail)

        # 4. малый локальный дедлайн → TIMEOUT
        cwd4 = root / "run4"
        out4 = adapter.run(SELF_TEST_PROMPT, cwd4, fake_timeout,
                           kill_grace=kill_grace)
        add(f"timeout={fake_timeout}s → TIMEOUT", out4.error == TIMEOUT,
            f"{out4.error}: {out4.detail}")
        add("TIMEOUT: session прервана (прерывание в detail)",
            "прервана" in out4.detail, out4.detail)
    finally:
        adapter.close()
        print(f"\nсервер остановлен; временные каталоги: {root}")

    print("\n=== SELF-TEST OpenCodeAdapter ===")
    for name, ok, detail in checks:
        print(f"  [{'OK  ' if ok else 'FAIL'}] {name}" +
              (f"\n         {detail}" if detail and not ok else ""))
    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"\nИтог: {passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Runtime adapters (cline/opencode)")
    ap.add_argument("--opencode-self-test", action="store_true",
                    help="самопроверка адаптера OpenCode без semantic-audit")
    ap.add_argument("--model", help="model ID (обязателен для self-test)")
    ap.add_argument("--provider", default=None,
                    help="явный provider (по умолчанию определяется по model)")
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--kill-grace", type=int, default=10)
    ap.add_argument("--server-url", default=None,
                    help="подключиться к уже запущенному серверу вместо spawn")
    ap.add_argument("--server-password", default=None)
    ap.add_argument("--fake-model", default="omniroute/__ainoveledit_missing__",
                    help="несуществующая модель для проверки MODEL_ERROR")
    args = ap.parse_args(argv)

    if not args.opencode_self_test:
        ap.error("нужен --opencode-self-test")
    if not args.model:
        print("ОШИБКА: model ID не задан. Укажите --model \"<provider>/<id>\" "
              "или --model \"<id>\" (provider возьмётся из явного --provider "
              f"либо = {DEFAULT_OPENCODE_PROVIDER!r}). Выдумывать ID нельзя.")
        return 2
    try:
        return opencode_self_test(args.model, args.provider, args.timeout,
                                  args.kill_grace, args.server_url,
                                  args.server_password, args.fake_model)
    except (RuntimeError, ValueError) as exc:
        print(f"ОШИБКА: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
