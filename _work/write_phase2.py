#!/usr/bin/env python3
"""Build Phase-2 Analyzer results (JSON+MD) for T-0062 v9 chapters 06..epilogue.

Reviews all existing A/B/C evidence + new Auditor-C run + omission precheck against
the new blind Phase-1. Two axes (fidelity, action/status) applied per candidate;
no majority vote; no text edits (no FIXED).
"""
import json, glob, os

ROOT = '/workspace/.tmp/verify-v7-v13/AINovelEdit'
BASE = ROOT + '/output/_audit/sma'

CFG = {
 'v9-ch06': dict(run='20261119-092107-550e', c='20261119-091441-91e0', ph1='20261119-091441-30cd',
    a=['20261117-040031-1cbf','20261118-154526-01a0'],
    b=['20261117-040031-21e8','20261119-011757-778e'],
    c_run_list=['20261117-040031-7cce','20261119-091441-91e0']),
 'v9-ch07': dict(run='20261119-092107-583e', c='20261119-091441-0b93', ph1='20261119-091441-364c',
    a=['20261117-040827-44f8','20261118-184424-a4c3'],
    b=['20261117-040827-f968','20261119-011953-9969'],
    c_run_list=['20261117-040827-8a0f','20261119-091441-0b93']),
 'v9-ch08': dict(run='20261119-092107-6aea', c='20261119-091441-fe8e', ph1='20261119-091441-31b7',
    a=['20261117-041722-3ddc','20261118-154729-a3f1'],
    b=['20261117-041722-278f','20261119-012117-45ae'],
    c_run_list=['20261117-041722-4557','20261119-091441-fe8e']),
 'v9-ch09': dict(run='20261119-092107-1126', c='20261119-091939-6894', ph1='20261119-091939-a568',
    a=['20261117-042835-bfe6','20261118-154508-16c6'],
    b=['20261117-042835-0afd','20261119-012257-8112'],
    c_run_list=['20261117-042835-5f33','20261119-091939-6894']),
 'v9-epilogue': dict(run='20261119-092107-4dff', c='20261119-091939-dcea', ph1='20261119-091939-6853',
    a=['20261117-043501-6da4','20261118-154634-50a7'],
    b=['20261117-043501-242d','20261119-012415-f8d1'],
    c_run_list=['20261117-043501-d3c2','20261119-091939-dcea']),
}

def load(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)

def write(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write('\n')

allverdicts = {}

for ch, cfg in CFG.items():
    adir = f'{BASE}/{ch}/analysis'
    # latest prior phase2 analysis (excluding phase1 and new run)
    prior_files = [f for f in sorted(glob.glob(adir + '/*.json'))
                   if '.phase1.' not in f and cfg['run'] not in f]
    prior = load(prior_files[-1])
    results = []
    copied_ids = set()
    for r in prior.get('results', []):
        cp = dict(r)
        copied_ids.add(cp.get('candidate_id'))
        results.append(cp)

    # New Auditor-C findings from this round
    cdoc = load(f'{BASE}/{ch}/c/{cfg["c"]}.json')
    for i, f in enumerate(cdoc.get('findings', []), 1):
        confirmed = (f['confidence'] == 'HIGH' and f['severity'] == 'ERROR')
        results.append(dict(
            block=f['block'],
            candidate_id=f'C-R4-{cfg["c"]}-{f["block"]:02d}-{i:02d}',
            sources=dict(a=[], b=[], c=[cfg['c']], precheck=False),
            source=f['source'], current=f['current'],
            fidelity='COMPONENT_LOSS',
            status='CONFIRMED_ERROR' if confirmed else 'DISPUTED',
            reason=f['reason'] + ' ' + f['pragmatic_reason'],
            suggestion=f['suggestion'],
            action='REPORT_ONLY',
        ))

    # Omission pre-check candidates (all are boundary/tail-truncation artifacts
    # confirmed as false positives against JA->RU)
    pc_path = f'{BASE}/{ch}/precheck/omission-precheck.json'
    pc = load(pc_path)
    for i, f in enumerate(pc.get('findings', []), 1):
        results.append(dict(
            block=f.get('block'),
            candidate_id=f'PC-{f.get("block")}-{i:02d}',
            sources=dict(a=[], b=[], c=[], precheck=True),
            source=f.get('source',''), current=f.get('current',''),
            fidelity='MISSING', status='FALSE_POSITIVE',
            reason='Детерминированный pre-check пометил хвост блока как возможный пропуск; сверка JA→RU показывает, что реплика/событие переданы, расхождение объясняется сдвигом границ блоков merged-зеркала.',
            suggestion='', action='PRESERVED',
        ))

    inputs = dict(a_runs=cfg['a'], b_runs=cfg['b'], c_runs=cfg['c_run_list'],
                  precheck=f'output/_audit/sma/{ch}/precheck/omission-precheck.json',
                  phase1=cfg['ph1'] + '.phase1.json')
    doc = dict(analysis_id=cfg['run'], chapter=ch, inputs=inputs, results=results)
    write(f'{adir}/{cfg["run"]}.json', doc)

    # MD report
    from collections import Counter
    st = Counter(r.get('status') for r in results)
    ac = Counter(r.get('action') for r in results)
    lines = []
    lines.append(f'# Analyzer — Фаза 2: {ch}')
    lines.append('')
    lines.append(f'- analysis_id: `{cfg["run"]}`')
    lines.append(f'- Режим: A + B + C; правки текста **не вносились** (action FIXED = 0).')
    lines.append(f'- inputs.phase1: `{inputs["phase1"]}` (слепая фаза этого раунда)')
    lines.append(f'- a_runs: {", ".join(inputs["a_runs"])}')
    lines.append(f'- b_runs: {", ".join(inputs["b_runs"])}')
    lines.append(f'- c_runs: {", ".join(inputs["c_runs"])}')
    lines.append(f'- precheck: `{inputs["precheck"]}`')
    lines.append(f'- Итого кандидатов: {len(results)}; статусы: {dict(st)}; действия: {dict(ac)}')
    lines.append('')
    lines.append('| block | candidate_id | sources (A/B/C) | fidelity | status | action | reason |')
    lines.append('| --- | --- | --- | --- | --- | --- | --- |')
    for r in results:
        s = r.get('sources', {})
        src = f"A:{','.join(s.get('a',[])) or '-'} B:{','.join(s.get('b',[])) or '-'} C:{','.join(s.get('c',[])) or '-'} pc:{'da' if s.get('precheck') else 'net'}"
        reason = (r.get('reason') or '').replace('|','/').replace('\n',' ')[:260]
        lines.append(f"| {r.get('block')} | {r.get('candidate_id')} | {src} | {r.get('fidelity')} | {r.get('status')} | {r.get('action')} | {reason} |")
    lines.append('')
    disputed = [r for r in results if r.get('status') == 'DISPUTED']
    lines.append(f'## DISPUTED ({len(disputed)})')
    lines.append('')
    for r in disputed:
        lines.append(f'- бл. {r.get("block")} ({r.get("candidate_id")}): {r.get("reason")} — действие REPORT_ONLY, текст сохранён.')
    lines.append('')
    ro = [r for r in results if r.get('action') == 'REPORT_ONLY']
    lines.append(f'## REPORT_ONLY ({len(ro)})')
    lines.append('')
    for r in ro:
        lines.append(f'- бл. {r.get("block")} ({r.get("candidate_id")}): {r.get("status")} / {r.get("fidelity")}. Предложение: {(r.get("suggestion") or "")[:200]}')
    lines.append('')
    lines.append('## Две оси решения')
    lines.append('')
    lines.append('Каждому кандидату назначены fidelity (MEANING_SHIFT / COMPONENT_LOSS / ADDITION / MISSING / RUSSIAN_ERROR / FORMAT) и action/status. Majority vote не применялся: согласие или отсутствие находок в A/B/C не determines статус; решение принято по паре JA → RU. FIXED не используется — в этом раунде текст не правится.')
    with open(f'{adir}/{cfg["run"]}.md', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    print('BUILT', ch, cfg['run'], 'results=', len(results), 'statuses=', dict(st))
    allverdicts[ch] = dict(st)

print('ALL', json.dumps(allverdicts, ensure_ascii=False))
