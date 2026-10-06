#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§11 RC-1 demo: runtime regression guard (НЕ format_scan:typo).

validated text (canon) → pipeline вносит опечатку → drift_scan --strict
→ BLOCKING (exit 1). Формы слова собираются программно (визуально
неразличимы). Файлы создаются только во временном каталоге; репозиторий
и regression corpus не изменяются."""
from __future__ import annotations
import subprocess
import sys
import tempfile
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]        # noverl/
SCRIPTS = ROOT / "AINovelEdit" / "scripts"

canon = "заговорила"                              # validated text
wrong = canon[:3] + "г" + canon[3:]               # внесённая опечатка
assert "гг" not in canon and "гг" in wrong, (canon, wrong)
assert len(wrong) == len(canon) + 1

validated = "<!-- block: 1 -->\nСуетливо %s Сиеста. Рядом с ней лежал поднос.\n" % canon
tampered = "<!-- block: 1 -->\nСуетливо %s Сиеста. Рядом с ней лежал поднос.\n" % wrong

tmp = Path(tempfile.mkdtemp(prefix="drift_guard_"))
base_f = tmp / "baseline.md"
cur_f = tmp / "current.md"
exp_f = tmp / "explained.json"
base_f.write_text(validated, encoding="utf-8")
cur_f.write_text(tampered, encoding="utf-8")

import json as _json
exp_f.write_text(_json.dumps({
    "results": [{
        "status": "CONFIRMED_ERROR",
        "action": "FIXED",
        "before": validated.split("\n", 1)[1],
        "after": tampered.split("\n", 1)[1],
    }]
}, ensure_ascii=False), encoding="utf-8")


def run(args):
    p = subprocess.run([sys.executable] + [str(a) for a in args],
                       cwd=str(ROOT / "AINovelEdit"), capture_output=True)
    return p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace")


print("== RC-1 pipeline-regression guard (temp: %s) ==" % tmp)

rc, out = run([SCRIPTS / "drift_scan.py", "--file", cur_f,
               "--against-file", base_f, "--strict"])
print("[1] drift --strict (unexplained WEAK): exit=%d (ожидание 1)" % rc)
assert rc == 1, out[-800:]

rc, out = run([SCRIPTS / "drift_scan.py", "--file", cur_f,
               "--against-file", base_f, "--strict", "--explain", exp_f])
print("[2] drift --strict --explain (пара before/after): exit=%d (ожидание 0)" % rc)
assert rc == 0, out[-800:]

rc, out = run([SCRIPTS / "format_scan.py", "--file", cur_f, "--only", "typo"])
hit = "typo 1" in out
print("[3] format_scan --only typo: exit=%d, typo-находка=%s (ожидание 0/True)"
      % (rc, hit))
assert rc == 0 and hit, out[-800:]

rc, out = run([SCRIPTS / "format_scan.py", "--file", base_f, "--only", "typo"])
print("[4] format_scan по validated-text: exit=%d, 0 находок=%s (ожидание 0/True)"
      % (rc, "Кандидатов на разбор: **0**" in out))
assert rc == 0 and "Кандидатов на разбор: **0**" in out, out[-800:]

print("\nOK: drift ловит ИЗМЕНЕНИЕ проверенного текста (WEAK, blocking);")
print("format_scan ловит КОНКРЕТНУЮ опечатку независимо от baseline;")
print("слои не смешиваются. Временные файлы: %s" % tmp)
