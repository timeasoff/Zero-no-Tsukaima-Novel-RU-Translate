# -*- coding: utf-8 -*-
"""Аудиторский драйвер правок v04-ch01: применяет пары old->new по смысловым
блокам через scripts/fix_block.py (текст уходит в stdin, без shell-канала).

Использование:  python output/_audit/_fix/apply_fixes.py [--verify-only]
"""
import re
import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "output" / "v4-ch01.md"
FIX = BASE / "scripts" / "fix_block.py"

FIXES = [
    (2,  [("что стоял поблизости.", "что стоял поблизости:")]),
    (5,  [("Но впоследствии оказалось, что это вовсе",
           "Но впоследствии выяснилось, что это вовсе")]),
    (6,  [("чуть позже третьего дня.", "чуть позже трёх пополудни.")]),
    (8,  [("А тут ещё вещь, связанная руками:", "А тут ещё ручная работа:"),
          ("Сайто, пасуя, перебирал", "Сайто, робея, перебирал")]),
    (9,  [("Луиза заставила вырыть яму крота Гиша,",
           "Луиза заставила крота Гиша вырыть яму,")]),
    (10, [("Дерфлингер спросил ровным, притворно-невинным голосом.",
           "Дерфлингер сказал ровным, притворно-невинным голосом:")]),
    (12, [("Недавний взрыв магического света…",
           "Недавний магический свет «Взрыв»…")]),
    (13, [("служанкой в баню ходили", "служанкой в ванну ходили"),
          ("вместе в баню заходили", "вместе в ванну заходили")]),
    (14, [("— Следующий будет он, милый мой.", "— Следующий будет он.")]),
    (17, [("включается нагнетённый электрический",
           "включается накопленный электрический")]),
]

MARK_RE = re.compile(r"<!-- block: \d+ -->")


def segment(text, n):
    marks = [(m.start(), m.group(0)) for m in MARK_RE.finditer(text)]
    for i, (pos, tag) in enumerate(marks):
        if tag == "<!-- block: %d -->" % n:
            start = pos + len(tag)
            end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
            return start, end
    raise SystemExit("FAIL: marker %d not found" % n)


def apply_all():
    fails = []
    for n, pairs in FIXES:
        text = OUT.read_text(encoding="utf-8")
        start, end = segment(text, n)
        seg = text[start:end]
        new = seg
        for old, newstr in pairs:
            if old not in new:
                fails.append("b%d: OLD not found: %s" % (n, old))
                continue
            new = new.replace(old, newstr)
        if new == seg:
            fails.append("b%d: no change" % n)
            continue
        # payload в файл (--text-file): кириллица не проходит через shell
        payload = Path(__file__).resolve().parent / "_payload.txt"
        with payload.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(new)
        r = subprocess.run(
            [sys.executable, str(FIX), "--file", "v4-ch01.md",
             "--block", str(n), "--text-file", str(payload)],
            capture_output=True, text=True, encoding="utf-8",
            cwd=str(BASE))
        if r.returncode != 0:
            fails.append("b%d: fix_block rc=%s out=%s err=%s"
                         % (n, r.returncode, r.stdout.strip(), r.stderr.strip()))
            continue
    return fails


def verify():
    fails = []
    text = OUT.read_text(encoding="utf-8")
    marks = MARK_RE.findall(text)
    if len(marks) != 17:
        fails.append("marker count %d != 17" % len(marks))
    for n, pairs in FIXES:
        for old, newstr in pairs:
            if newstr not in text:
                fails.append("b%d: missing NEW: %s" % (n, newstr))
            if old in text:
                fails.append("b%d: leftover OLD: %s" % (n, old))
    lost = ["породили тот свет", "Действительно холодно с открытым",
            "мычала: «У-у-у-у!»", "мог ведь и вправду погибнуть",
            "бесподобно плоской", "приняв солидный вид, заговорил:",
            "— А? На пол?", "ещё лет сто рано"]
    for s in lost:
        if s not in text:
            fails.append("lost paragraph tail missing: %s" % s)
    # контроль порчи: подозрительные «тто/уто/отлиуие» быть не должно
    for bad in ["тто ", "уто ", "отлиуие", "ууть", "потесал", "ответал, раскативая"]:
        if bad in text:
            fails.append("corruption marker present: %s" % bad)
    return fails


def main():
    if "--verify-only" in sys.argv:
        fails = verify()
    else:
        fails = apply_all() + verify()
    if fails:
        print("FAIL count: %d" % len(fails))
        for f in fails:
            print("FAIL:", f)
        return 1
    print("OK: all %d fix groups applied and verified; markers=17" % len(FIXES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
