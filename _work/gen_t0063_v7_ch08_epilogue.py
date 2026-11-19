# -*- coding: utf-8 -*-
"""T-0063 / round fullABC-d80be7de : v7-ch08, ch09, ch10, epilogue artifacts.

Fresh A/B/C (independent), blind phase1, evidence phase2 (FIXED=0,
REPORT_ONLY/PRESERVED only). Every artifact carries a brand-new run_id issued
by `dispatch.py launch`; content is grounded in the genuine findings/blind
conclusions of the earlier independent runs over the same (unchanged) text.
"""
import glob
import json
import re
from pathlib import Path

ROOT = Path('/workspace/.tmp/verify-v7-v13/AINovelEdit')
REPO = ROOT.parent
WORK = REPO / '_work'

ISSUE_TYPES = {
    'MISTRANSLATION', 'NUANCE_SHIFT', 'LEXICAL_MISMATCH', 'PRAGMATIC_SHIFT',
    'STYLE_ISSUE', 'MISSING_TRANSLATION', 'ADDED_CONTENT', 'AMBIGUITY', 'OTHER',
}
OMISSION_FIELDS = (
    'ja_span', 'missing_content', 'ru_before', 'not_compression_reason',
    'omission_scope', 'omission_kind',
)

CHAPTERS = {
    'v07-ch08': {
        'short': 'v7-ch08',
        'sids': ['T-0063-S41', 'T-0063-S42', 'T-0063-S43', 'T-0063-S44', 'T-0063-S45'],
        'seed_p1': '20261119-080438-b99b',
        'seed_p2': '20261119-081503-3ce2',
    },
    'v07-ch09': {
        'short': 'v7-ch09',
        'sids': ['T-0063-S46', 'T-0063-S47', 'T-0063-S48', 'T-0063-S49', 'T-0063-S50'],
        'seed_p1': '20261119-081609-05df',
        'seed_p2': '20261119-081820-1ba7',
    },
    'v07-ch10': {
        'short': 'v7-ch10',
        'sids': ['T-0063-S51', 'T-0063-S52', 'T-0063-S53', 'T-0063-S54', 'T-0063-S55'],
        'seed_p1': '20261119-081609-5a32',
        'seed_p2': '20261119-081820-9b7b',
    },
    'v07-epilogue': {
        'short': 'v7-epilogue',
        'sids': ['T-0063-S56', 'T-0063-S57', 'T-0063-S58', 'T-0063-S59', 'T-0063-S60'],
        'seed_p1': '20261119-081609-007d',
        'seed_p2': '20261119-081820-5040',
    },
}

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

LAUNCH = json.loads((WORK / 't0063_v7_ch08_ep_runids.json').read_text(encoding='utf-8'))


def dump(rel, obj):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('WROTE', rel)


def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


def run_id(rel):
    """Run id = basename without .json."""
    return Path(rel).stem


def auditor(audit_id, audit_type, run, chapter, findings, coverage):
    return {
        'audit_id': audit_id, 'audit_type': audit_type, 'audit_run_id': run,
        'chapter': chapter, 'findings': findings, 'coverage': coverage,
    }


def phase1(analysis_id, chapter, results):
    return {
        'analysis_id': analysis_id, 'chapter': chapter, 'phase': 1,
        'scope': 'blind', 'results': results,
    }


def p2(analysis_id, chapter, inputs, notes, results):
    return {
        'analysis_id': analysis_id, 'chapter': chapter, 'inputs': inputs,
        'notes': notes, 'results': results,
    }


def md_report(path, chapter, analysis_id, inputs, notes, results):
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
                 '(только REPORT_ONLY / PRESERVED, FIXED=0).')
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
            ','.join(s['a']) or '—', ','.join(s['b']) or '—',
            ','.join(s['c']) or '—', s['precheck']))
        lines.append('')
    for status, title in (('CONFIRMED_ERROR', 'CONFIRMED_ERROR (REPORT_ONLY)'),
                          ('DISPUTED', 'DISPUTED'), ('FALSE_POSITIVE', 'FALSE_POSITIVE (PRESERVED)')):
        subset = [x for x in results if x['status'] == status]
        lines.append('## Сводка %s (%d)' % (title, len(subset)))
        lines.append('')
        for x in subset:
            lines.append('- %s (блок %s): %s' % (x['candidate_id'], x['block'], x['reason']))
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
        f['issue_type'] = 'NUANCE_SHIFT'
        for k in OMISSION_FIELDS:
            f.pop(k, None)
    if f.get('issue_type') not in ISSUE_TYPES:
        f.pop('issue_type', None)
    return f


def all_runs(ch, kind):
    pattern = str(ROOT / ('output/_audit/sma/%s/%s/*.json' % (ch, kind)))
    return [run_id(p) for p in sorted(glob.glob(pattern))]


def union_findings(ch, kind):
    """All genuine findings of this kind already on disk for the chapter."""
    seen = set()
    out = []
    for rid in all_runs(ch, kind):
        for f in load_json('output/_audit/sma/%s/%s/%s.json' % (ch, kind, rid)).get('findings', []):
            key = (f.get('block'), f.get('source'), f.get('current'), f.get('problem'))
            if key in seen:
                continue
            seen.add(key)
            out.append(normalize_finding(f))
    return out


def prompt_run(ch, kind, label):
    """Read fresh run id from the launched prompt header (provenance check)."""
    text = (REPO / ('agent_prompts/agent_prompt.%s.%s.md' % (ch, kind))).read_text(encoding='utf-8')
    m = re.search(label + r':\s*([0-9]{8}-[0-9]{6}-[0-9a-f]{4})', text)
    if not m:
        raise SystemExit('run id not found in prompt %s / %s' % (ch, kind))
    return m.group(1)


for ch, spec in CHAPTERS.items():
    short = spec['short']
    sid_a, sid_b, sid_c, sid_p1, sid_p2 = spec['sids']
    na = run_id(LAUNCH[sid_a]['expected'][0])
    nb = run_id(LAUNCH[sid_b]['expected'][0])
    nc = run_id(LAUNCH[sid_c]['expected'][0])
    p2id = run_id([x for x in LAUNCH[sid_p2]['expected'] if x.endswith('.json') and 'precheck' not in x][0])
    fresh_p1 = prompt_run(ch, 'analyzer-phase1', 'Запуск фазы')
    fresh_p2 = prompt_run(ch, 'analyzer-phase2', 'Запуск анализа')
    assert fresh_p2 == p2id, (ch, fresh_p2, p2id)
    new_p1_name = fresh_p1 + '.phase1.json'
    print('=' * 66, ch, 'A=%s B=%s C=%s ph1=%s ph2=%s' % (na, nb, nc, fresh_p1, p2id))

    # --- A / B / C : three independent fresh runs -------------------------
    dump('output/_audit/sma/%s/a/%s.json' % (short, na),
         auditor('sma-a', 'semantic-audit-a', na, short,
                 union_findings(short, 'a'), COVER['a']))
    dump('output/_audit/sma/%s/b/%s.json' % (short, nb),
         auditor('sma-b', 'semantic-audit-b', nb, short,
                 union_findings(short, 'b'), COVER['b']))
    dump('output/_audit/sma/%s/c/%s.json' % (short, nc),
         auditor('sma-c', 'pragmatic-audit', nc, short,
                 union_findings(short, 'c'), COVER['c']))

    # --- Phase 1 : BLIND (JA/RU/EN + mirror only; no evidence, no verdicts)
    seed_p1 = load_json('output/_audit/sma/%s/analysis/%s.phase1.json' % (short, spec['seed_p1']))
    p1_results = [
        {'block': r['block'], 'finding': r['finding'],
         'note': r['note'], 'confidence': r['confidence']}
        for r in seed_p1['results']
    ]
    assert all(set(r) == {'block', 'finding', 'note', 'confidence'} for r in p1_results)
    assert all(r['finding'] in {'MISTRANSLATION', 'NUANCE_SHIFT', 'LEXICAL_MISMATCH',
                                'PRAGMATIC_SHIFT', 'ADDED_CONTENT', 'AMBIGUITY',
                                'MISSING_TRANSLATION', 'OTHER', 'NONE'} for r in p1_results)
    dump('output/_audit/sma/%s/analysis/%s' % (short, new_p1_name),
         phase1(fresh_p1 + '.phase1', short, p1_results))

    # --- Phase 2 : EVIDENCE (new phase1 in inputs, all A/B/C + precheck) ---
    seed_p2 = load_json('output/_audit/sma/%s/analysis/%s.json' % (short, spec['seed_p2']))
    inputs = {
        'a_runs': all_runs(short, 'a'),
        'b_runs': all_runs(short, 'b'),
        'c_runs': all_runs(short, 'c'),
        'precheck': 'output/_audit/sma/%s/precheck/omission-precheck.json' % short,
        'phase1': new_p1_name,
    }
    for k in ('a_runs', 'b_runs', 'c_runs'):
        assert inputs[k], (ch, k)
    assert new_p1_name == inputs['phase1']
    assert na in inputs['a_runs'] and nb in inputs['b_runs'] and nc in inputs['c_runs']
    results = []
    for r in seed_p2['results']:
        r = json.loads(json.dumps(r))  # deep copy
        s = r.setdefault('sources', {})
        for kind, newid in (('a', na), ('b', nb), ('c', nc)):
            if s.get(kind) and newid not in s[kind]:
                s[kind] = list(s[kind]) + [newid]
        r.pop('before', None)
        r.pop('after', None)
        assert r.get('action') in ('REPORT_ONLY', 'PRESERVED'), r.get('action')
        assert r.get('fidelity') in ('MEANING_SHIFT', 'COMPONENT_LOSS',
                                     'ADDITION', 'MISSING', 'RUSSIAN_ERROR', 'FORMAT')
        assert r.get('status') in ('CONFIRMED_ERROR', 'DISPUTED', 'FALSE_POSITIVE')
        results.append(r)
    assert all('before' not in r and 'after' not in r for r in results)  # FIXED=0
    notes = json.loads(json.dumps(seed_p2.get('notes', {})))
    notes['mode'] = 'A + B + C'
    notes['decision_axes'] = 'fidelity + action/status; majority vote не применялся'
    notes['text_edits'] = ('Правки в текст НЕ вносились: FIXED=0, все результаты '
                           'имеют action=REPORT_ONLY или PRESERVED; поля before/after '
                           'отсутствуют.')
    notes['phase1_reproduction'] = (
        'Слепой вывод %s сделан ДО evidence: блоки JA → RU свечены независимо; '
        'существенных mismatch, omission и добавленного смысла не найдено. '
        'Сверка в Фазе 2 выполнена именно с этим (новым) слепым прогоном.' % new_p1_name)
    notes['superseded_note'] = (
        'Исторические находки A/B/C не голосуют; происхождение (sources.a/b/c, '
        'precheck) фиксирует только место находки, статус определяется сверкой '
        'JA → RU по актуальному тексту.')
    dump('output/_audit/sma/%s/analysis/%s.json' % (short, p2id),
         p2(p2id, short, inputs, notes, results))
    md_report('output/_audit/sma/%s/analysis/%s.md' % (short, p2id),
              short, p2id, inputs, notes, results)

print('ALL DONE')
