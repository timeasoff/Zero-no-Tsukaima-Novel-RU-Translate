# -*- coding: utf-8 -*-
"""Восстановление v5-log.md + вынос приложения в UTF-8 файл для save_block."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")

p = "D:/skills/NovelEdit/noverl/AINovelEdit/output/_log/v5-log.md"
t = io.open(p, encoding="utf-8").read()
marker = "### ВАЖНО: повторная нормализация тома"
i = t.find(marker)
assert i > 0, "marker not found"
appendix = t[i:]
original = t[:i]
io.open(p, "w", encoding="utf-8", newline="\n").write(original)
io.open("D:/skills/NovelEdit/noverl/AINovelEdit/_work/log_append_v5.txt", "w",
        encoding="utf-8", newline="\n").write(appendix)
print("restored len:", len(original), "| appendix len:", len(appendix))
print("restored tail:", repr(original[-80:]))
