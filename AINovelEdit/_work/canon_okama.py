# -*- coding: utf-8 -*-
"""Канон オカマ / トレビアн / Скаррон / Гиш."""
import io
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
base = "D:/skills/NovelEdit/noverl/AINovelEdit/"

print("===== JA オカマ / トレビアン =====")
for p in sorted(glob.glob(base + "translates/ja/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["オカマ", "トレビアン", "おかま"]:
        i = 0
        while True:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 70):i + 70].replace("\n", " / "))
            i += 1

print()
print("===== RU: Скаррон / Очаровательная Фея =====")
for p in sorted(glob.glob(base + "output/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["Скаррон", "Очаровательная Фея", "Очаровательной Феи"]:
        i = 0
        cnt = 0
        while cnt < 2:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 70):i + 70].replace("\n", " / "))
            i += 1
            cnt += 1

print()
print("===== RU: как передано オカマ/трансвеститы ('гей', 'педик', 'тетушка') =====")
for p in sorted(glob.glob(base + "output/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["гей", "педик", "тетушк", "трансвест", "женоподоб", "жемани"]:
        i = 0
        cnt = 0
        while cnt < 3:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 60):i + 60].replace("\n", " / "))
            i += 1
            cnt += 1

print()
print("===== RU: Гиш (как форма имени) =====")
for p in sorted(glob.glob(base + "output/v1-ch*.md"))[:3]:
    t = io.open(p, encoding="utf-8").read()
    i = t.find("Гиш")
    if i >= 0:
        print(os.path.basename(p), "|", t[max(0, i - 60):i + 60].replace("\n", " / "))
