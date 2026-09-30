# -*- coding: utf-8 -*-
"""Проверка состояния output/v5-ch01.md вокруг блоков 14-16."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")
p = "D:/skills/NovelEdit/noverl/AINovelEdit/output/v5-ch01.md"
t = io.open(p, encoding="utf-8").read()
i = t.find("<!-- block: 14 -->")
j = t.find("<!-- block: 16 -->")
print(repr(t[i:j]))
