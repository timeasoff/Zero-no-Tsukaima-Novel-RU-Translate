#!/usr/bin/env python3
"""Extract JA/RU per block from merged chapter file for pragmatic audit review."""
import re, sys

path = sys.argv[1]
text = open(path, encoding='utf-8').read()
# split on ## Блок N
parts = re.split(r'^## Блок (\d+)\s*$', text, flags=re.M)
for i in range(1, len(parts), 2):
    n = parts[i]
    body = parts[i+1]
    def grab(tag):
        m = re.search(r'\*\*' + tag + r':\*\*\s*\n(.*?)(?=\n\*\*[A-Z_]+:\*\*|\Z)', body, flags=re.S)
        return m.group(1).strip() if m else ''
    ja = grab('JA')
    ru = grab('RU')
    print(f'========== BLOCK {n} ==========')
    print('[JA]', ja)
    print('[RU]', ru)
    print()
