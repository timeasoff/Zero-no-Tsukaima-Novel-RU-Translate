# -*- coding: utf-8 -*-
"""Поиск канона 必勝法 и форм «выигрышный метод» в завершённых томах."""
import io
import re
import sys
import glob

sys.stdout.reconfigure(encoding="utf-8")
root = r"D:\skills\NovelEdit\noverl\AINovelEdit"

print("== JA 必勝 ==")
for p in glob.glob(root + r"\translates\ja\*.md"):
    t = io.open(p, encoding="utf-8").read()
    for m in re.finditer("必勝", t):
        print(p.split("\\")[-1], m.start(),
              t[max(0, m.start() - 60):m.start() + 60].replace("\n", " / "))

print("== RU-формы в output ==")
pat = re.compile("выигрышн\\w+ (?:метод|стратеги)|гарантированн\\w+ способ|"
                 "безотказн\\w+ (?:метод|способ)|верный способ")
for p in glob.glob(root + r"\output\*.md"):
    t = io.open(p, encoding="utf-8").read()
    for m in pat.finditer(t):
        print(p.split("\\")[-1], m.group(0))
