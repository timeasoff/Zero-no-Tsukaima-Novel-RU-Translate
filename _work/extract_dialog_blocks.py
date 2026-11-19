import re, sys
path = sys.argv[1]
text = open(path, encoding='utf-8').read()
parts = re.split(r'(?m)^## Блок (\d+)\s*$', text)
# parts[0] preamble, then pairs (num, body)
for i in range(1, len(parts), 2):
    num = parts[i]; body = parts[i+1]
    ja = re.search(r'\*\*JA:\*\*\n(.*?)(?=\n\*\*EN:\*\*)', body, re.S)
    ru = re.search(r'\*\*ED_RU:\*\*\n(.*)', body, re.S)
    ja_t = ja.group(1).strip() if ja else ''
    ru_t = ru.group(1).strip() if ru else ''
    if '「' in ja_t or '」' in ja_t or '『' in ja_t:
        print(f'===== БЛОК {num} =====')
        print('[JA]', ja_t)
        print('[RU]', ru_t)
        print()
