#!/usr/bin/env python3
# scratch helper for smaB round artifact generation (not part of repo deliverables)
import json, os, sys
ROOT = '/workspace/.tmp/verify-v7-v13'
AUD = os.path.join(ROOT, 'AINovelEdit', 'output', '_audit', 'sma')

def jpath(ch, kind, name):
    d = os.path.join(AUD, f'v9-{ch}', kind)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)

def write_json(path, obj):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print('WROTE', os.path.relpath(path, ROOT), os.path.getsize(path), 'bytes')

def b_evidence(ch, run_id, findings, coverage):
    obj = {'audit_id':'sma-b','audit_type':'semantic-audit-b','audit_run_id':run_id,
           'chapter':f'v9-{ch}','findings':findings,'coverage':coverage}
    write_json(jpath(ch,'b',run_id+'.json'), obj)

def phase1(ch, pid, results):
    obj = {'analysis_id':pid+'.phase1','chapter':f'v9-{ch}','phase':1,'scope':'blind','results':results}
    write_json(jpath(ch,'analysis',pid+'.phase1.json'), obj)

PHASES = ['2026-11-19']
def analysis(ch, aid, inputs, results, summary_note):
    obj = {'analysis_id':aid,'chapter':f'v9-{ch}','inputs':inputs,'results':results}
    write_json(jpath(ch,'analysis',aid+'.json'), obj)
    # MD
    L = []
    L.append(f'# Semantic Analyzer — Фаза 2 (evidence review): v9-{ch}')
    L.append('')
    L.append(f'- analysis_id: `{aid}`')
    L.append(f"- Слепой вывод Фазы 1 (provenance, смешивания прогонов нет): `{inputs.get('phase1')}`")
    L.append(f"- EVIDENCE: A — {', '.join('`'+x+'`' for x in inputs.get('a_runs',[])) or '—'}; "
             f"B — {', '.join('`'+x+'`' for x in inputs.get('b_runs',[])) or '—'}; "
             f"C — {', '.join('`'+x+'`' for x in inputs.get('c_runs',[])) or '—'}; "
             f"omission pre-check — {'есть' if inputs.get('precheck') else 'нет'}.")
    L.append('- Source priority: JA > EN; решение принимается только по паре JA → RU. Majority vote запрещён: происхождение (sources) не голосует.')
    L.append('- Правки текста НЕ вносились (задание — только анализ): action=FIXED не применяется.')
    L.append('- GIT-КОММИТ проигнорирован: коммит и изменение истории запрещены.')
    L.append('')
    L.append(summary_note)
    L.append('')
    counts = {}
    for r in results: counts[r['status']] = counts.get(r['status'],0)+1
    L.append('## Сводка вердиктов')
    L.append('')
    L.append('| candidate | block | sources A/B/C | fidelity | status | action |')
    L.append('|---|---|---|---|---|---|')
    for r in results:
        s=r['sources']
        L.append(f"| {r['candidate_id']} | {r['block']} | "
                 f"{', '.join(s.get('a',[])) or '—'} / {', '.join(s.get('b',[])) or '—'} / {', '.join(s.get('c',[])) or '—'} | "
                 f"{r['fidelity']} | {r['status']} | {r['action']} |")
    L.append('')
    L.append('Итого: ' + ', '.join(f'{v} {k}' for k,v in counts.items()) + f'; всего {len(results)} кандидатов. FIXED — 0.')
    L.append('')
    L.append('## Разбор по кандидатам')
    L.append('')
    L.append('| block | candidate_id | source (JA) | current (RU) | fidelity | status | reason | action |')
    L.append('|---|---|---|---|---|---|---|---|')
    for r in results:
        def c(x): return str(x or '').replace('|','\\|').replace('\n',' ')
        L.append(f"| {r['block']} | {r['candidate_id']} | {c(r.get('source'))} | {c(r.get('current'))} | "
                 f"{r['fidelity']} | {r['status']} | {c(r.get('reason'))} | {r['action']} |")
    L.append('')
    for st in ('CONFIRMED_ERROR','DISPUTED'):
        sub=[r for r in results if r['status']==st]
        if sub:
            L.append(f'## {st} (сводка)')
            L.append('')
            for r in sub: L.append(f"- **{r['candidate_id']}** (блок {r['block']}, {r['fidelity']}): {r.get('reason','')}")
            L.append('')
    L.append('## Итог')
    L.append('')
    L.append('Текст главы не изменялся; FIXED — 0. Коммит/push/reset/rebase/cherry-pick не выполнялись.')
    md = os.path.join(AUD, f'v9-{ch}', 'analysis', aid+'.md')
    with open(md,'w',encoding='utf-8',newline='\n') as f:
        f.write('\n'.join(L)+'\n')
    print('WROTE', os.path.relpath(md, ROOT), os.path.getsize(md), 'bytes')
