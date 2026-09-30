# -*- coding: utf-8 -*-
"""Диагностика names-weak сигналов блока 10: какие формы словаря есть в EN-10."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/skills/NovelEdit/noverl/AINovelEdit/scripts")
import check_alignment as ca  # noqa: E402

names = ca.load_names()

e_t = io.open("D:/skills/NovelEdit/noverl/AINovelEdit/translates/en/v5-ch01.md",
              encoding="utf-8").read()
s = e_t.find("<!-- block: 10 -->")
e = e_t.find("<!-- block: 11 -->")
en = e_t[s:e].lower()

t = io.open("D:/skills/NovelEdit/noverl/AINovelEdit/output/v5-ch01.md",
            encoding="utf-8").read()
s2 = t.find("<!-- block: 10 -->")
e2 = t.find("<!-- block: 11 -->")
ed = t[s2:e2].lower()

for entry in names:
    forms, base, disp = entry[0], entry[1], entry[-1]
    in_en = [f for f in list(forms) + [base] if f and f.lower() in en]
    in_ed = [f for f in list(forms) + [base] if f and f.lower() in ed]
    if in_en and not in_ed:
        print("WEAK:", disp, "| forms in EN:", in_en)
        f = in_en[0].lower()
        i = en.find(f)
        print("   EN ctx:", en[max(0, i - 70):i + 70].replace("\n", " / "))
