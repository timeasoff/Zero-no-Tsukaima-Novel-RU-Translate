# -*- coding: utf-8 -*-
"""Поиск канонических форм для блока 11."""
import io
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
base = "D:/skills/NovelEdit/noverl/AINovelEdit/"

pairs = [
    ("valiere", ["Вальер", "Вальер", "Вальер"]),
    ("hazel", ["鳶色", "кари", "орехов", "медово", "рыжеват"]),
    ("groin ja", ["股間"]),
    ("groin ru", ["пах", "промежност", "между ног"]),
    ("valliere ru", ["Ла Вальер", "ла Вальер", "де Вальер"]),
]

print("===== RU-формы Ла Вальер в output =====")
for p in sorted(glob.glob(base + "output/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["Ла Вальер", "ла Вальер"]:
        i = 0
        while True:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", t[max(0, i - 60):i + 60].replace("\n", " / "))
            i += 1

print("===== JA 鳶色 → какие RU соответствия (по контексту v1/v3/v4) =====")
for p in sorted(glob.glob(base + "translates/ja/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    i = 0
    while True:
        i = t.find("鳶色", i)
        if i < 0:
            break
        print(os.path.basename(p), "|", t[max(0, i - 40):i + 40].replace("\n", " / "))
        i += 1

print("===== RU-описания глаз в output (кари/орехов/медов) =====")
for p in sorted(glob.glob(base + "output/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["карие", "карих", "орехов", "медов", "рыжеват", "янтарн"]:
        i = 0
        while True:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 60):i + 60].replace("\n", " / "))
            i += 1
