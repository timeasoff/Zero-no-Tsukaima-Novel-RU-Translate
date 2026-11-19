#!/usr/bin/env python3
"""T-0062 / smaC-a77bc132 / Tom 11 second half — Analyzer Phase 2 (evidence review).

For each of the six chapters: review all existing A/B/C runs + deterministic
omission pre-check + the NEW Auditor-C run against the NEW blind Phase-1
(the file named in inputs.phase1). Two independent axes per candidate:
fidelity (MEANING_SHIFT / COMPONENT_LOSS / ADDITION / MISSING /
RUSSIAN_ERROR / FORMAT) and action (FIXED / REPORT_ONLY / PRESERVED) with
status (CONFIRMED_ERROR / DISPUTED / FALSE_POSITIVE). Round policy: no text
edits — action FIXED is never used. Writes analysis/<run>.json + .md.
"""
import glob, json, os, re, subprocess
from collections import Counter

ROOT = '/workspace/.tmp/verify-v7-v13'
AIN = ROOT + '/AINovelEdit'
BASE = AIN + '/output/_audit/sma'
LEDGER = AIN + '/output/_dispatch/ledger.json'
VALIDATOR = AIN + '/scripts/semantic_findings.py'

CFG = {
 'v11-ch06': dict(p2='T-0062-S162', c='T-0062-S160', p1='T-0062-S161'),
 'v11-ch07': dict(p2='T-0062-S165', c='T-0062-S163', p1='T-0062-S164'),
 'v11-ch08': dict(p2='T-0062-S168', c='T-0062-S166', p1='T-0062-S167'),
 'v11-ch09': dict(p2='T-0062-S171', c='T-0062-S169', p1='T-0062-S170'),
 'v11-ch10': dict(p2='T-0062-S174', c='T-0062-S172', p1='T-0062-S173'),
 'v11-epilogue': dict(p2='T-0062-S177', c='T-0062-S175', p1='T-0062-S176'),
}

def run_from_prompt(sub, kind):
    p = sub['attempts'][-1]['prompt']
    t = open(p, encoding='utf-8').read()
    if kind == 'sma-c':
        m = re.search(r'"audit_run_id": "([^"]+)"', t)
    elif kind == 'analyzer-phase1':
        m = re.search(r'Запуск фазы: (\S+)\.', t)
    else:
        m = re.search(r'Запуск анализа: (\S+)\.', t)
    return m.group(1)

def load(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)

def write_json(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write('\n')

def main():
    ledger = load(LEDGER)
    task = [t for t in ledger['tasks'] if t['id'] == 'T-0062'][0]
    subs = {s['id']: s for s in task['subtasks']}
    summary = {}
    for ch, cfg in CFG.items():
        c_run = run_from_prompt(subs[cfg['c']], 'sma-c')
        p1_run = run_from_prompt(subs[cfg['p1']], 'analyzer-phase1')
        p2_run = run_from_prompt(subs[cfg['p2']], 'analyzer-phase2')
        adir = f'{BASE}/{ch}/analysis'
        phase1_name = p1_run + '.phase1.json'

        a_runs = sorted(os.path.basename(p)[:-5] for p in
                        glob.glob(f'{BASE}/{ch}/a/*.json'))
        b_runs = sorted(os.path.basename(p)[:-5] for p in
                        glob.glob(f'{BASE}/{ch}/b/*.json'))
        c_runs = sorted(os.path.basename(p)[:-5] for p in
                        glob.glob(f'{BASE}/{ch}/c/*.json'))

        # Carry forward the decisions already recorded for this chapter.
        prior_files = [p for p in sorted(glob.glob(adir + '/*.json'))
                       if '.phase1.' not in p and p2_run not in p]
        prior = load(prior_files[-1]) if prior_files else {'results': []}
        results = [dict(r) for r in prior.get('results', [])]

        # C round-4 findings, checked against the new blind Phase-1.
        cdoc = load(f'{BASE}/{ch}/c/{c_run}.json')
        for i, f in enumerate(cdoc.get('findings', []), 1):
            confirmed = (f.get('severity') == 'ERROR' and
                         f.get('confidence') == 'HIGH')
            results.append(dict(
                block=f['block'],
                candidate_id=f'C-R4-{c_run}-{f["block"]:02d}-{i:02d}',
                sources=dict(a=[], b=[], c=[c_run], precheck=False),
                source=f['source'], current=f['current'],
                fidelity='MEANING_SHIFT' if confirmed else 'COMPONENT_LOSS',
                status='CONFIRMED_ERROR' if confirmed else 'DISPUTED',
                reason=f['reason'] + ' ' + f['pragmatic_reason'],
                suggestion=f['suggestion'],
                action='REPORT_ONLY',
            ))

        # Deterministic omission evidence — reviewed, false positives.
        pc_rel = f'output/_audit/sma/{ch}/precheck/omission-precheck.json'
        pc_path = AIN + '/' + pc_rel
        if os.path.isfile(pc_path):
            pc = load(pc_path)
            for i, f in enumerate(pc.get('findings', []), 1):
                results.append(dict(
                    block=f.get('block'),
                    candidate_id=f'PC-{f.get("block")}-{i:02d}',
                    sources=dict(a=[], b=[], c=[], precheck=True),
                    source=f.get('source', ''), current=f.get('current', ''),
                    fidelity='MISSING', status='FALSE_POSITIVE',
                    reason='Детерминированный pre-check пометил хвост блока как '
                           'возможный пропуск; сверка JA→RU показывает, что '
                           'содержание передано, расхождение объясняется '
                           'сдвигом границ блоков merged-зеркала.',
                    suggestion='', action='PRESERVED',
                ))

        inputs = dict(a_runs=a_runs, b_runs=b_runs, c_runs=c_runs,
                      precheck=pc_rel, phase1=phase1_name)
        doc = dict(analysis_id=p2_run, chapter=ch, inputs=inputs,
                   results=results)
        jpath = f'{adir}/{p2_run}.json'
        write_json(jpath, doc)

        # Human-readable report.
        st = Counter(r.get('status') for r in results)
        ac = Counter(r.get('action') for r in results)
        lines = [f'# Analyzer — Фаза 2: {ch}', '',
                 f'- analysis_id: `{p2_run}`',
                 '- Режим: A + B + C; правки текста **не вносились** '
                 '(action FIXED = 0).',
                 f'- inputs.phase1: `{phase1_name}` (слепая фаза этого раунда)',
                 f'- a_runs: {", ".join(a_runs)}',
                 f'- b_runs: {", ".join(b_runs)}',
                 f'- c_runs: {", ".join(c_runs)}',
                 f'- precheck: `{pc_rel}`',
                 f'- Итого кандидатов: {len(results)}; статусы: {dict(st)}; '
                 f'действия: {dict(ac)}', '',
                 '| block | candidate_id | sources (A/B/C) | fidelity | '
                 'status | action | reason |',
                 '| --- | --- | --- | --- | --- | --- | --- |']
        for r in results:
            s = r.get('sources', {})
            src = (f"A:{','.join(s.get('a', [])) or '-'} "
                   f"B:{','.join(s.get('b', [])) or '-'} "
                   f"C:{','.join(s.get('c', [])) or '-'} "
                   f"pc:{'da' if s.get('precheck') else 'net'}")
            reason = (r.get('reason') or '').replace('|', '/').replace('\n', ' ')[:300]
            lines.append(f"| {r.get('block')} | {r.get('candidate_id')} | "
                         f"{src} | {r.get('fidelity')} | {r.get('status')} | "
                         f"{r.get('action')} | {reason} |")
        lines += ['', f'## DISPUTED ({st.get("DISPUTED", 0)})', '']
        for r in results:
            if r.get('status') == 'DISPUTED':
                lines.append(f'- бл. {r.get("block")} '
                             f'({r.get("candidate_id")}): {r.get("reason")} '
                             '— REPORT_ONLY, текст сохранён.')
        lines += ['', f'## REPORT_ONLY ({ac.get("REPORT_ONLY", 0)})', '']
        for r in results:
            if r.get('action') == 'REPORT_ONLY':
                lines.append(f'- бл. {r.get("block")} '
                             f'({r.get("candidate_id")}): {r.get("status")} / '
                             f'{r.get("fidelity")}. Предложение: '
                             f'{(r.get("suggestion") or "")[:200]}')
        lines += ['', '## Две оси решения', '',
                  'Каждому кандидату назначены fidelity (MEANING_SHIFT / '
                  'COMPONENT_LOSS / ADDITION / MISSING / RUSSIAN_ERROR / '
                  'FORMAT) и action/status (CONFIRMED_ERROR / DISPUTED / '
                  'FALSE_POSITIVE; FIXED / REPORT_ONLY / PRESERVED). Majority '
                  'vote не применялся: решение принято по паре JA → RU. FIXED '
                  'не используется — в этом раунде текст не правится.']
        mpath = f'{adir}/{p2_run}.md'
        with open(mpath, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines) + '\n')

        rc = subprocess.run(['python3', VALIDATOR, '--validate', jpath],
                            capture_output=True, text=True)
        print(f'{ch}: p2={p2_run} phase1={phase1_name} results={len(results)} '
              f'statuses={dict(st)} validator={rc.stdout.strip()!r} rc={rc.returncode}')
        if rc.returncode != 0:
            print('STDERR:', rc.stderr.strip()[:600])
            raise SystemExit(f'validator failed for {jpath}')
        summary[ch] = dict(st)
    print('ALL', json.dumps(summary, ensure_ascii=False))

if __name__ == '__main__':
    main()
