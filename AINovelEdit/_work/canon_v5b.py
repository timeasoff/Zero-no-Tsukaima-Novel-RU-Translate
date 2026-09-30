# -*- coding: utf-8 -*-
"""Канон терминов для блоков 11-19 v5-ch01."""
import io
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
base = "D:/skills/NovelEdit/noverl/AINovelEdit/"

print("===== RU: Васра / узы / усмиряющие ===== ")
for p in sorted(glob.glob(base + "output/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["Васра", "Васру", "васра", "усмиряющ", "смиряющ", "путы"]:
        i = 0
        while True:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 60):i + 60].replace("\n", " / "))
            i += 1

print()
print("===== JA: ヴァスラ / 拘束具 =====")
for p in sorted(glob.glob(base + "translates/ja/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["ヴァスラ", "拘束具"]:
        i = 0
        while True:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 60):i + 60].replace("\n", " / "))
            i += 1

print()
print("===== RU: Дерфлингер / разумный меч =====")
for p in sorted(glob.glob(base + "output/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["Дерфлингер", "разумный меч", "Разумный меч"]:
        i = 0
        cnt = 0
        while cnt < 2:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 50):i + 50].replace("\n", " / "))
            i += 1
            cnt += 1

print()
print("===== RU: тре бьен / Скаррон =====")
for p in sorted(glob.glob(base + "output/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["тре бьен", "Тре бьен", "Скаррон"]:
        i = 0
        cnt = 0
        while cnt < 3:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 50):i + 50].replace("\n", " / "))
            i += 1
            cnt += 1

print()
print("===== RU: Пустота / Нулевая =====")
for p in sorted(glob.glob(base + "output/v*.md")):
    t = io.open(p, encoding="utf-8").read()
    for kw in ["Пустоты", "Пустота", "Нулевая"]:
        i = 0
        cnt = 0
        while cnt < 2:
            i = t.find(kw, i)
            if i < 0:
                break
            print(os.path.basename(p), "|", kw, "|",
                  t[max(0, i - 50):i + 50].replace("\n", " / "))
            i += 1
            cnt += 1
