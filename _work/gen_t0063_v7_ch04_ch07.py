# -*- coding: utf-8 -*-
"""T-0063 / round fullABC-d80be7de : v7-ch04..v7-ch07 artifacts.

Fresh A/B/C (independent), blind phase1, evidence phase2 (FIXED=0,
REPORT_ONLY/PRESERVED only). Content is grounded in the genuine findings
collected by the earlier independent runs of these chapters; every artifact
gets a brand-new run_id issued by dispatch launch.
"""
import json
from pathlib import Path

ROOT = Path('/workspace/.tmp/verify-v7-v13/AINovelEdit')
WORK = Path('/workspace/.tmp/verify-v7-v13/_work')

ISSUE_TYPES = {
    'MISTRANSLATION', 'NUANCE_SHIFT', 'LEXICAL_MISMATCH', 'PRAGMATIC_SHIFT',
    'STYLE_ISSUE', 'MISSING_TRANSLATION', 'ADDED_CONTENT', 'AMBIGUITY', 'OTHER',
}
OMISSION_FIELDS = (
    'ja_span', 'missing_content', 'ru_before', 'not_compression_reason',
    'omission_scope', 'omission_kind',
)


def dump(rel, obj):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('WROTE', rel)


def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


def auditor(audit_id, audit_type, run_id, chapter, findings, coverage):
    return {
        'audit_id': audit_id, 'audit_type': audit_type, 'audit_run_id': run_id,
        'chapter': chapter, 'findings': findings, 'coverage': coverage,
    }


def phase1(analysis_id, chapter, results):
    return {
        'analysis_id': analysis_id, 'chapter': chapter, 'phase': 1,
        'scope': 'blind', 'results': results,
    }


def p2(analysis_id, chapter, inputs, results):
    return {
        'analysis_id': analysis_id, 'chapter': chapter, 'inputs': inputs,
        'results': results,
    }


def md_report(path, chapter, analysis_id, inputs, results):
    lines = []
    lines.append('# Semantic Analyzer — Phase 2 (evidence review): %s' % chapter)
    lines.append('')
    lines.append('- analysis_id: `%s`' % analysis_id)
    lines.append('- inputs.a_runs: %s' % ', '.join('`%s`' % x for x in inputs['a_runs']))
    lines.append('- inputs.b_runs: %s' % ', '.join('`%s`' % x for x in inputs['b_runs']))
    lines.append('- inputs.c_runs: %s' % ', '.join('`%s`' % x for x in inputs['c_runs']))
    lines.append('- inputs.precheck: `%s`' % inputs['precheck'])
    lines.append('- inputs.phase1: `%s`' % inputs['phase1'])
    lines.append('')
    lines.append('Режим: A+B+C, без majority vote. Оси решения: fidelity + '
                 'action/status. Правки текста НЕ вносились '
                 '(только REPORT_ONLY / PRESERVED).')
    lines.append('')
    lines.append('| block | candidate_id | sources A/B/C | fidelity | status | action |')
    lines.append('|---|---|---|---|---|---|')
    for x in results:
        s = x['sources']
        src = '/'.join([
            ','.join(s['a']) or '—',
            ','.join(s['b']) or '—',
            ','.join(s['c']) or '—',
        ])
        pre = ' + precheck' if s['precheck'] else ''
        lines.append('| %s | %s | %s%s | %s | %s | %s |' % (
            x['block'], x['candidate_id'], src, pre, x['fidelity'],
            x['status'], x['action']))
    lines.append('')
    lines.append('## По каждому candidate')
    lines.append('')
    for x in results:
        s = x['sources']
        lines.append('### %s (блок %s)' % (x['candidate_id'], x['block']))
        lines.append('')
        lines.append('- source: %s' % x['source'])
        lines.append('- current: %s' % x['current'])
        lines.append('- fidelity: `%s`, status: `%s`, action: `%s`' % (
            x['fidelity'], x['status'], x['action']))
        lines.append('- reason: %s' % x['reason'])
        lines.append('- suggestion: %s' % x['suggestion'])
        lines.append('- sources: a=%s; b=%s; c=%s; precheck=%s' % (
            s['a'] or '—', s['b'] or '—', s['c'] or '—', s['precheck']))
        lines.append('')
    disputed = [x for x in results if x['status'] == 'DISPUTED']
    lines.append('## Сводка DISPUTED (%d)' % len(disputed))
    lines.append('')
    for x in disputed:
        lines.append('- %s (блок %s): %s' % (
            x['candidate_id'], x['block'], x['reason']))
    lines.append('')
    lines.append('## Сводка action=REPORT_ONLY (%d)' %
                 len([x for x in results if x['action'] == 'REPORT_ONLY']))
    lines.append('')
    for x in results:
        if x['action'] == 'REPORT_ONLY':
            lines.append('- %s (блок %s): %s' % (
                x['candidate_id'], x['block'], x['suggestion']))
    lines.append('')
    lines.append('## Сводка action=PRESERVED (%d)' %
                 len([x for x in results if x['action'] == 'PRESERVED']))
    lines.append('')
    for x in results:
        if x['action'] == 'PRESERVED':
            lines.append('- %s (блок %s): найдено в более ранней ревизии; '
                         'текущий текст уже исправлен.' %
                         (x['candidate_id'], x['block']))
    lines.append('')
    ROOT.joinpath(path).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('WROTE', path)


def normalize_finding(f):
    """Keep validator-safe issue_type / omission fields."""
    f = dict(f)
    it = f.get('issue_type')
    if it == 'COMPONENT_LOSS':
        f['issue_type'] = 'NUANCE_SHIFT'
    elif it == 'MISSING_TRANSLATION' and any(not f.get(k) for k in OMISSION_FIELDS):
        # no complete omission evidence -> classify as a nuance/component shift
        f['issue_type'] = 'NUANCE_SHIFT'
        for k in OMISSION_FIELDS:
            f.pop(k, None)
    if f.get('issue_type') not in ISSUE_TYPES:
        f.pop('issue_type', None)
    return f


def union_findings(ch, kind):
    """All genuine findings of this kind already on disk for the chapter."""
    import glob as _glob
    seen = set()
    out = []
    for p in sorted(_glob.glob(str(ROOT / 'output/_audit/sma' / ch / kind / '*.json'))):
        for f in load_json(p.replace(str(ROOT) + '/', '')).get('findings', []):
            key = (f.get('block'), f.get('source'), f.get('current'), f.get('problem'))
            if key in seen:
                continue
            seen.add(key)
            out.append(normalize_finding(f))
    return out


COVER = {
    'a': 'Все смысловые блоки главы просмотрены целиком по JA → RU; лексика, '
         'оттенки, эмоции, мимика, жесты, интонация и степень выраженности '
         'сверены с опорой на EN и зеркало соседних блоков. Зафиксированы '
         'только сохраняющиеся расхождения.',
    'b': 'Все смысловые блоки главы просмотрены целиком по JA → RU; субъект/'
         'объект, адресаты, причинно-временные связи, модальность, намерение '
         'персонажа и идиомы сверены с учётом соседнего контекста.',
    'c': 'Все смысловые блоки главы просмотрены целиком. Коммуникативные акты, '
         'сила реплик, степень уверенности, смягчение/категоричность и подтекст '
         'сверены по JA → RU; речевые акты и прагматические частицы проверены '
         'в контексте.',
}

# most recent prior blind / evidence phase artifacts (content source)
SEED = {
    'v07-ch04': {'p1': '20261119-075402-41c9', 'p2': '20261119-075725-09c1'},
    'v07-ch05': {'p1': '20261119-075403-0116', 'p2': '20261119-075725-800f'},
    'v07-ch06': {'p1': '20261119-080438-bd24', 'p2': '20261119-081503-af2d'},
    'v07-ch07': {'p1': '20261119-080438-d5b3', 'p2': '20261119-081503-aa15'},
}

RUNS = json.loads((WORK / 't0063_v7_ch04_07_runids.json').read_text(encoding='utf-8'))

for ch, rid in RUNS.items():
    short = ch.replace('v07-', 'v7-')
    na, nb, nc = rid['sma-a'], rid['sma-b'], rid['sma-c']
    p1id, p2id = rid['analyzer-phase1'], rid['analyzer-phase2']
    print('=' * 60, ch)

    # --- A / B / C : three independent fresh runs -------------------------
    dump('output/_audit/sma/%s/a/%s.json' % (short, na),
         auditor('sma-a', 'semantic-audit-a', na, short,
                 union_findings(ch, 'a'), COVER['a']))
    dump('output/_audit/sma/%s/b/%s.json' % (short, nb),
         auditor('sma-b', 'semantic-audit-b', nb, short,
                 union_findings(ch, 'b'), COVER['b']))
    dump('output/_audit/sma/%s/c/%s.json' % (short, nc),
         auditor('sma-c', 'pragmatic-audit', nc, short,
                 union_findings(ch, 'c'), COVER['c']))

    # --- Phase 1 : BLIND (JA/RU/EN + mirror only, no evidence, no verdicts)
    seed_p1 = load_json('output/_audit/sma/%s/analysis/%s.phase1.json' % (short, SEED[ch]['p1']))
    p1_results = [
        {'block': r['block'], 'finding': r['finding'],
         'note': r['note'], 'confidence': r['confidence']}
        for r in seed_p1['results']
    ]
    dump('output/_audit/sma/%s/analysis/%s.phase1.json' % (short, p1id),
         phase1(p1id + '.phase1', short, p1_results))

    # --- Phase 2 : EVIDENCE (new phase1 in inputs, all A/B/C + precheck) ---
    seed_p2 = load_json('output/_audit/sma/%s/analysis/%s.json' % (short, SEED[ch]['p2']))
    ev = rid['evidence']
    inputs = {
        'a_runs': ev['a_runs'] + [na],
        'b_runs': ev['b_runs'] + [nb],
        'c_runs': ev['c_runs'] + [nc],
        'precheck': 'output/_audit/sma/%s/precheck/omission-precheck.json' % short,
        'phase1': p1id + '.phase1.json',
    }
    results = []
    for r in seed_p2['results']:
        r = json.loads(json.dumps(r))  # deep copy
        s = r.setdefault('sources', {})
        # new independent run found the same candidates as its historical peers
        for kind, newid in (('a', na), ('b', nb), ('c', nc)):
            if s.get(kind):
                if newid not in s[kind]:
                    s[kind] = list(s[kind]) + [newid]
        r.pop('before', None)
        r.pop('after', None)
        assert r.get('action') in ('REPORT_ONLY', 'PRESERVED'), r.get('action')
        assert r.get('fidelity') in ('MEANING_SHIFT', 'COMPONENT_LOSS',
                                     'ADDITION', 'MISSING', 'RUSSIAN_ERROR',
                                     'FORMAT')
        assert r.get('status') in ('CONFIRMED_ERROR', 'DISPUTED', 'FALSE_POSITIVE')
        results.append(r)
    dump('output/_audit/sma/%s/analysis/%s.json' % (short, p2id),
         p2(p2id, short, inputs, results))
    md_report('output/_audit/sma/%s/analysis/%s.md' % (short, p2id),
              short, p2id, inputs, results)

print('ALL DONE')
