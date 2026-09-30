import sys, re
sys.path.insert(0, 'scripts')
import check_alignment as ca, merged_io

pairs = ca.load_names()
items = merged_io.read_merged('translates/_report/merged/v5-ch01.md')
idx = int(sys.argv[1]) if len(sys.argv) > 1 else 1
ed = merged_io.clean(items[idx][1].get('ED_RU', ''))
toks = [re.sub(r'[^а-яё]', '', w.lower().replace('ё', 'е'))
        for w in re.findall(r'[А-Яа-яЁё][А-Яа-яЁё\-]+', ed)]
print('--- RU-side matches in ED_RU block %d:' % (idx + 1))
for p in pairs:
    for t in toks:
        if t.startswith(p[1]):
            print('  token=%s -> ru=%s base=%s en_forms=%s' % (
                t.encode('unicode_escape').decode(),
                p[2].encode('unicode_escape').decode(), p[1],
                sorted(p[0])))
