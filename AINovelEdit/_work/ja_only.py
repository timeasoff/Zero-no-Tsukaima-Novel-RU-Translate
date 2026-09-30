# -*- coding: utf-8 -*-
"""Компактная печать JA-блоков v5-ch01 (только JA) для перевода."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")
p = "D:/skills/NovelEdit/noverl/AINovelEdit/translates/ja/v5-ch01.md"
t = io.open(p, encoding="utf-8").read()
out, cur = {}, None
for para in t.split("\n\n"):
    s = para.strip()
    if not s:
        continue
    if s.startswith("<!-- block:") and s.endswith("-->"):
        cur = int(s.split(":")[1].replace("-->", "").strip())
        out[cur] = []
    elif cur is not None and not s.startswith("# "):
        out[cur].append(s)

for n in [int(x) for x in sys.argv[1:]] or sorted(out):
    print("### JA-%d (%d абз.)" % (n, len(out[n])))
    for k, para in enumerate(out[n], 1):
        print("%d. %s" % (k, para))
    print()
