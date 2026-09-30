# -*- coding: utf-8 -*-
"""Диагностика names-info сигналов check_alignment для блока 10."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/skills/NovelEdit/noverl/AINovelEdit/scripts")
import check_alignment as ca  # noqa: E402

names = ca.load_names()

t = io.open("D:/skills/NovelEdit/noverl/AINovelEdit/output/v5-ch01.md",
            encoding="utf-8").read()
start = t.find("<!-- block: 10 -->")
end = t.find("<!-- block: 11 -->")
ed = t[start:(end if end > 0 else len(t))].lower()

targets = ["разумный меч", "чёрный лес", "придворная дама"]
for entry in names:
    forms, base = entry[0], entry[1]
    disp = entry[-1]
    if disp.lower() in targets:
        print("NAME:", disp, "| forms:", forms, "| base:", base)
        for f in list(forms) + [base]:
            if f and f.lower() in ed:
                i = ed.find(f.lower())
                print("   MATCH form/base:", repr(f),
                      "| ctx:", ed[max(0, i - 60):i + 60].replace("\n", " / "))
