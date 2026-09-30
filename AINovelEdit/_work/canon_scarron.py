# -*- coding: utf-8 -*-
"""Канон: Скаррон / «Очаровательная Фея» / オカマ в завершённых томах."""
import io
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
base = "D:/skills/NovelEdit/noverl/AINovelEdit/"

print("== RU: Скаррон / Очаровательная Фея / okama-передачи ==")
kws = ["Скаррон", "Очаровательная Фея", "Очаровательной Феи",
       "мужик в юбке", "гомо", "педик", "женоподоб"]
for p in sorted(glob.glob(base + "output/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in kws:
        i = 0
        c = 0
        while c < 2:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 80):i + 80].replace("\n", " / "))
            i += 1
            c += 1

print()
print("== JA: スカロン / オカマ ==")
for p in sorted(glob.glob(base + "translates/ja/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["スカロン", "オカマ"]:
        i = 0
        c = 0
        while c < 2:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 90):i + 90].replace("\n", " / "))
            i += 1
            c += 1

print()
print("== dictionary/addresses: Скаррон ==")
for f in ["dictionary.md", "addresses.md"]:
    t = io.open(base + f, encoding="utf-8").read()
    for kw in ["Скаррон", "スカロン"]:
        i = 0
        while True:
            i = t.find(kw, i)
            if i < 0:
                break
            print(f, "|", t[max(0, i - 120):i + 120].replace("\n", " / "))
            i += 1
