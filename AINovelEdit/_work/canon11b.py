# -*- coding: utf-8 -*-
"""Канон: 股間 / シューター / ガチで / 余さず в завершённых томах."""
import io
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
base = "D:/skills/NovelEdit/noverl/AINovelEdit/"

print("===== JA 股間 → контексты =====")
for p in sorted(glob.glob(base + "translates/ja/v1-ch*.md")) + \
        sorted(glob.glob(base + "translates/ja/v2-ch*.md")) + \
        sorted(glob.glob(base + "translates/ja/v3-ch*.md")) + \
        sorted(glob.glob(base + "translates/ja/v4-ch*.md")):
    t = io.open(p, encoding="utf-8").read()
    i = 0
    while True:
        i = t.find("股間", i)
        if i < 0:
            break
        print(os.path.basename(p), "|", t[max(0, i - 50):i + 50].replace("\n", " / "))
        i += 1

print("===== RU: как передано место удара (пах/промежность) в output =====")
for p in sorted(glob.glob(base + "output/v1-ch*.md")) + \
        sorted(glob.glob(base + "output/v2-ch*.md")) + \
        sorted(glob.glob(base + "output/v3-ch*.md")) + \
        sorted(glob.glob(base + "output/v4-ch*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["в пах", "по паху", "промежност", "между ног", "под дых"]:
        i = 0
        while True:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 70):i + 70].replace("\n", " / "))
            i += 1

print("===== JA 叔父 / 夜逃げ =====")
for p in sorted(glob.glob(base + "translates/ja/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    i = t.find("夜逃げ")
    if i >= 0:
        print(os.path.basename(p), "|", t[max(0, i - 60):i + 60].replace("\n", " / "))
