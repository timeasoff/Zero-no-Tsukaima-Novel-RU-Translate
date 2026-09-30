import sys, re
sys.path.insert(0, 'scripts')
import check_alignment as ca, merged_io

pairs = ca.load_names()
for p in pairs:
    if p[2].encode('unicode_escape').decode().startswith('\\u0412\\u0430\\u043b'):  # 'Вал...'
        print('PAIR:', p[0], '| base:', p[1], '| ru:', p[2].encode('unicode_escape').decode())

items = merged_io.read_merged('translates/_report/merged/v5-ch01.md')
ed = merged_io.clean(items[1][1].get('ED_RU', ''))
toks = [re.sub(r'[^а-яё]', '', w.lower().replace('ё', 'е'))
        for w in re.findall(r'[А-Яа-яЁё][А-Яа-яЁё\-]+', ed)]
for p in pairs:
    for t in toks:
        if t.startswith(p[1]):
            print('MATCH token=%s -> ru=%s' % (t.encode('unicode_escape').decode(),
                                               p[2].encode('unicode_escape').decode()))
