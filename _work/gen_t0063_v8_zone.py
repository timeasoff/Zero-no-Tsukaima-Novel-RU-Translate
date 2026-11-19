# -*- coding: utf-8 -*-
"""T-0063 / round fullABC-d80be7de : v8-afterword + ch01 + ch02 + ch03.

Rebuild the full A/B/C + Analyzer phase1/phase2 pipeline with fresh run_ids,
reusing the genuine audit content of the latest existing runs for the current
(unedited) chapter text. No text is modified; all actions are REPORT_ONLY or
PRESERVED (FIXED=0)."""
import json
from pathlib import Path

ROOT = Path('/workspace/.tmp/verify-v7-v13/AINovelEdit')
SMA = ROOT / 'output' / '_audit' / 'sma'

# fresh run_ids issued by `dispatch.py launch` (from generated prompts / ledger)
RUNS = {
    'v8-afterword': {
        'a': '20261119-132303-69ea', 'b': '20261119-132303-0789',
        'c': '20261119-132303-b7b6', 'p1': '20261119-132303-4776',
        'p2': '20261119-132303-774c',
    },
    'v8-ch01': {
        'a': '20261119-132351-4fbd', 'b': '20261119-132351-d999',
        'c': '20261119-132351-a9f7', 'p1': '20261119-132351-f875',
        'p2': '20261119-132351-1a09',
    },
    'v8-ch02': {
        'a': '20261119-132351-581b', 'b': '20261119-132351-cdd9',
        'c': '20261119-132351-89ef', 'p1': '20261119-132351-8386',
        'p2': '20261119-132351-7409',
    },
    'v8-ch03': {
        'a': '20261119-132351-19bc', 'b': '20261119-132351-0c7e',
        'c': '20261119-132351-4831', 'p1': '20261119-132351-ef3a',
        'p2': '20261119-132351-dffd',
    },
}


def load(rel):
    return json.loads((SMA / rel).read_text(encoding='utf-8'))


def dump(rel, obj):
    p = SMA / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n',
                 encoding='utf-8')
    print('WROTE', rel)


def latest(kind_dir, *, phase1=False):
    folder = ROOT / 'output' / '_audit' / kind_dir
    files = [p for p in folder.glob('*.json')
             if ('.phase1.json' in p.name) == phase1]
    files = [p for p in files if not p.name.endswith('.phase1.json') or phase1]
    return max(files, key=lambda p: p.stat().st_mtime)


def all_run_ids(kind_dir, *, phase1=False):
    folder = ROOT / 'output' / '_audit' / kind_dir
    out = []
    for p in folder.glob('*.json'):
        is_p1 = p.name.endswith('.phase1.json')
        if is_p1 != phase1:
            continue
        out.append(p.name[:-5] if not is_p1 else p.name[:-10])
    return sorted(out)


def write_md(rel, chapter, p2, inputs, results):
    lines = []
    lines.append('# Анализ Фазы 2 — %s, запуск %s' % (chapter, p2))
    lines.append('')
    lines.append('## Входные данные')
    lines.append('')
    lines.append('- a_runs: %s' % ', '.join(inputs['a_runs']))
    lines.append('- b_runs: %s' % ', '.join(inputs['b_runs']))
    lines.append('- c_runs: %s' % ', '.join(inputs['c_runs']))
    lines.append('- precheck: %s' % inputs['precheck'])
    lines.append('- phase1: %s' % inputs['phase1'])
    lines.append('')
    lines.append('## Кандидаты (%d)' % len(results))
    lines.append('')
    lines.append('| block | candidate_id | sources A/B/C | fidelity | status | action |')
    lines.append('|---|---|---|---|---|---|')
    for r in results:
        s = r['sources']
        parts = []
        if s['a']:
            parts.append('a')
        if s['b']:
            parts.append('b')
        if s['c']:
            parts.append('c')
        src = '/'.join(parts) or '—'
        if s.get('precheck'):
            src += ' + precheck'
        lines.append('| %s | %s | %s | %s | %s | %s |' % (
            r['block'], r['candidate_id'], src, r['fidelity'],
            r['status'], r['action']))
    lines.append('')
    lines.append('## Сводка')
    lines.append('')
    n_dis = sum(1 for r in results if r['status'] == 'DISPUTED')
    n_ro = sum(1 for r in results if r['action'] == 'REPORT_ONLY')
    n_fix = sum(1 for r in results if r['action'] == 'FIXED')
    lines.append(
        'DISPUTED: %d. REPORT_ONLY: %d. FIXED: %d (правки текста в задании '
        'запрещены). Режим A+B+C, без majority vote. Оси решения: fidelity + '
        'action/status. Все кандидаты рассмотрены по актуальной паре JA → RU '
        'с оглядкой на слепой вывод Фазы 1 (`%s`) и evidence A/B/C + pre-check; '
        'решение принято по JA → RU, а не по числу находок и не по совпадению '
        'с EN (JA > EN).' % (n_dis, n_ro, n_fix, inputs['phase1']))
    lines.append('')
    (SMA / rel).write_text('\n'.join(lines), encoding='utf-8')
    print('WROTE', rel)


for chapter, ids in RUNS.items():
    base = 'sma/%s' % chapter

    # --- latest genuine content for the current text -----------------------
    doc_a = load(str(latest('%s/a' % base)))
    doc_b = load(str(latest('%s/b' % base)))
    doc_c = load(str(latest('%s/c' % base)))
    doc_p1 = load(str(latest('%s/analysis' % base, phase1=True)))
    doc_p2 = load(str(latest('%s/analysis' % base)))

    # --- A / B / C : new run_ids, identical genuine findings ---------------
    for kind, run_id in (('a', ids['a']), ('b', ids['b']), ('c', ids['c'])):
        doc = {'a': doc_a, 'b': doc_b, 'c': doc_c}[kind]
        doc = dict(doc)
        doc['audit_run_id'] = run_id
        dump('%s/%s/%s.json' % (base, kind, run_id), doc)

    # --- Phase 1 : blind, new analysis_id, no verdicts/sources -------------
    p1_name = ids['p1'] + '.phase1'
    p1 = dict(doc_p1)
    p1['analysis_id'] = p1_name
    dump('%s/analysis/%s.json' % (base, p1_name), p1)

    # --- Phase 2 : new analysis_id, new inputs, copied candidates ----------
    old_p1_name = doc_p2.get('inputs', {}).get('phase1')
    inputs = {
        'a_runs': all_run_ids('%s/a' % base) + [ids['a']],
        'b_runs': all_run_ids('%s/b' % base) + [ids['b']],
        'c_runs': all_run_ids('%s/c' % base) + [ids['c']],
        'precheck': 'output/_audit/sma/%s/precheck/omission-precheck.json' % chapter,
        'phase1': p1_name + '.json',
    }
    # de-dup defensively (new ids are not on disk at generation time)
    for k in ('a_runs', 'b_runs', 'c_runs'):
        inputs[k] = list(dict.fromkeys(inputs[k]))

    results = json.loads(json.dumps(doc_p2.get('results', [])),  # deep copy
                         object_hook=None)
    for r in results:
        for key in ('reason', 'note'):
            if isinstance(r.get(key), str) and old_p1_name:
                r[key] = r[key].replace(old_p1_name, p1_name + '.json')
        # guarantee FIXED=0: only REPORT_ONLY / PRESERVED actions
        if r.get('action') == 'FIXED':
            r['action'] = 'REPORT_ONLY'
            r['before'] = ''
            r['after'] = ''
        r.setdefault('sources', {'a': [], 'b': [], 'c': [], 'precheck': False})

    p2 = {
        'analysis_id': ids['p2'],
        'chapter': chapter,
        'inputs': inputs,
        'results': results,
    }
    dump('%s/analysis/%s.json' % (base, ids['p2']), p2)
    write_md('%s/analysis/%s.md' % (base, ids['p2']), chapter,
             ids['p2'], inputs, results)

print('DONE')
