# -*- coding: utf-8 -*-
"""Убрать литеральный маркер блока из приложения журнала (его отвергает save_block)."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")

p = "D:/skills/NovelEdit/noverl/AINovelEdit/_work/log_append_v5.txt"
t = io.open(p, encoding="utf-8").read()
i = t.find("<!--")
while i >= 0:
    j = t.find("-->", i)
    print("marker at", i, ":", repr(t[i:j + 3]))
    i = t.find("<!--", i + 1)
# замена: упоминание маркера блока 10 переформулировать
old1 = "`<!-- block: 10 -->`"
new1 = "маркера блока 10"
old2 = "<!-- block: 10 -->"
if old1 in t:
    t = t.replace(old1, new1)
elif old2 in t:
    t = t.replace(old2, new1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("after: contains <!-- :", "<!--" in t, "| len:", len(t))
