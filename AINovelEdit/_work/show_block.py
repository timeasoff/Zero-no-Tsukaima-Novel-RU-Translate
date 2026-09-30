# -*- coding: utf-8 -*-
"""Печать смыслового блока N из JA/EN/RU/ED_RU (v5-ch01)."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")

base = "D:/skills/NovelEdit/noverl/AINovelEdit/"
paths = {
    "JA": base + "translates/ja/v5-ch01.md",
    "EN": base + "translates/en/v5-ch01.md",
    "RU": base + "translates/ru/v5-ch01.md",
    "ED_RU": base + "output/v5-ch01.md",
}


def blocks(path):
    t = io.open(path, encoding="utf-8").read()
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
    return out


nums = [int(x) for x in sys.argv[1:]] or [11]
for n in nums:
    for lang, p in paths.items():
        bs = blocks(p)
        ps = bs.get(n, [])
        print("==== %s block %d (%d paras) ====" % (lang, n, len(ps)))
        for k, para in enumerate(ps, 1):
            print("  [%d] %s" % (k, para))
        print()
