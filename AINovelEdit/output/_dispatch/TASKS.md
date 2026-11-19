# Реестр задач диспетчера

Обновлено: 2026-11-19 22:00:24

Генерируется автоматически командой `python tools/dispatch.py`. Не редактируй вручную.

## T-0001 — OPEN

Перепроверка том 5 (с ch03) и том 6: полный recheck через субагентов (SMA A/B/C + Analyzer фазы 1-2 + грамматический аудит), исправления по находкам

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0001-S1 | sma-a | v05-ch03 | done | 10 | `agent_prompts/agent_prompt.v05-ch03.sma-a.attempt10.md` |
| T-0001-S2 | sma-b | v05-ch03 | done | 3 | `agent_prompts/agent_prompt.v05-ch03.sma-b.attempt3.md` |
| T-0001-S3 | sma-c | v05-ch03 | done | 1 | `agent_prompts/agent_prompt.v05-ch03.sma-c.md` |
| T-0001-S4 | analyzer-phase1 | v05-ch03 | done | 2 | `agent_prompts/agent_prompt.v05-ch03.analyzer-phase1.attempt2.md` |
| T-0001-S5 | analyzer-phase2 | v05-ch03 | done | 1 | `agent_prompts/agent_prompt.v05-ch03.analyzer-phase2.md` |
| T-0001-S6 | grammar-audit | v05-ch03 | done | 1 | `agent_prompts/agent_prompt.v05-ch03.grammar-audit.md` |
| T-0001-S7 | sma-a | v05-ch04 | done | 2 | `agent_prompts/agent_prompt.v05-ch04.sma-a.attempt2.md` |
| T-0001-S8 | sma-b | v05-ch04 | done | 2 | `agent_prompts/agent_prompt.v05-ch04.sma-b.attempt2.md` |
| T-0001-S9 | sma-c | v05-ch04 | done | 1 | `agent_prompts/agent_prompt.v05-ch04.sma-c.md` |
| T-0001-S10 | analyzer-phase1 | v05-ch04 | done | 1 | `agent_prompts/agent_prompt.v05-ch04.analyzer-phase1.md` |
| T-0001-S11 | analyzer-phase2 | v05-ch04 | done | 0 | `—` |
| T-0001-S12 | grammar-audit | v05-ch04 | done | 1 | `agent_prompts/agent_prompt.v05-ch04.grammar-audit.md` |
| T-0001-S13 | sma-a | v05-ch05 | done | 2 | `agent_prompts/agent_prompt.v05-ch05.sma-a.attempt2.md` |
| T-0001-S14 | sma-b | v05-ch05 | done | 2 | `agent_prompts/agent_prompt.v05-ch05.sma-b.attempt2.md` |
| T-0001-S15 | sma-c | v05-ch05 | done | 3 | `agent_prompts/agent_prompt.v05-ch05.sma-c.attempt3.md` |
| T-0001-S16 | analyzer-phase1 | v05-ch05 | interrupted | 3 | `agent_prompts/agent_prompt.v05-ch05.analyzer-phase1.attempt3.md` |
| T-0001-S17 | analyzer-phase2 | v05-ch05 | interrupted | 3 | `agent_prompts/agent_prompt.v05-ch05.analyzer-phase2.attempt3.md` |
| T-0001-S18 | grammar-audit | v05-ch05 | planned | 0 | `—` |
| T-0001-S19 | sma-a | v05-ch06 | interrupted | 5 | `agent_prompts/agent_prompt.v05-ch06.sma-a.attempt5.md` |
| T-0001-S20 | sma-b | v05-ch06 | interrupted | 2 | `agent_prompts/agent_prompt.v05-ch06.sma-b.attempt2.md` |
| T-0001-S21 | sma-c | v05-ch06 | interrupted | 3 | `agent_prompts/agent_prompt.v05-ch06.sma-c.attempt3.md` |
| T-0001-S22 | analyzer-phase1 | v05-ch06 | planned | 0 | `—` |
| T-0001-S23 | analyzer-phase2 | v05-ch06 | planned | 0 | `—` |
| T-0001-S24 | grammar-audit | v05-ch06 | planned | 0 | `—` |
| T-0001-S25 | sma-a | v05-ch07 | interrupted | 2 | `agent_prompts/agent_prompt.v05-ch07.sma-a.attempt2.md` |
| T-0001-S26 | sma-b | v05-ch07 | interrupted | 2 | `agent_prompts/agent_prompt.v05-ch07.sma-b.attempt2.md` |
| T-0001-S27 | sma-c | v05-ch07 | interrupted | 2 | `agent_prompts/agent_prompt.v05-ch07.sma-c.attempt2.md` |
| T-0001-S28 | analyzer-phase1 | v05-ch07 | planned | 0 | `—` |
| T-0001-S29 | analyzer-phase2 | v05-ch07 | planned | 0 | `—` |
| T-0001-S30 | grammar-audit | v05-ch07 | planned | 0 | `—` |
| T-0001-S31 | sma-a | v05-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v05-ch08.sma-a.md` |
| T-0001-S32 | sma-b | v05-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v05-ch08.sma-b.md` |
| T-0001-S33 | sma-c | v05-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v05-ch08.sma-c.md` |
| T-0001-S34 | analyzer-phase1 | v05-ch08 | planned | 0 | `—` |
| T-0001-S35 | analyzer-phase2 | v05-ch08 | planned | 0 | `—` |
| T-0001-S36 | grammar-audit | v05-ch08 | planned | 0 | `—` |
| T-0001-S37 | sma-a | v05-ch09 | done | 2 | `agent_prompts/agent_prompt.v05-ch09.sma-a.attempt2.md` |
| T-0001-S38 | sma-b | v05-ch09 | done | 3 | `agent_prompts/agent_prompt.v05-ch09.sma-b.attempt3.md` |
| T-0001-S39 | sma-c | v05-ch09 | done | 3 | `agent_prompts/agent_prompt.v05-ch09.sma-c.attempt3.md` |
| T-0001-S40 | analyzer-phase1 | v05-ch09 | done | 1 | `agent_prompts/agent_prompt.v05-ch09.analyzer-phase1.md` |
| T-0001-S41 | analyzer-phase2 | v05-ch09 | done | 1 | `agent_prompts/agent_prompt.v05-ch09.analyzer-phase2.md` |
| T-0001-S42 | grammar-audit | v05-ch09 | done | 1 | `agent_prompts/agent_prompt.v05-ch09.grammar-audit.md` |
| T-0001-S43 | sma-a | v05-ch10 | interrupted | 2 | `agent_prompts/agent_prompt.v05-ch10.sma-a.attempt2.md` |
| T-0001-S44 | sma-b | v05-ch10 | interrupted | 2 | `agent_prompts/agent_prompt.v05-ch10.sma-b.attempt2.md` |
| T-0001-S45 | sma-c | v05-ch10 | interrupted | 3 | `agent_prompts/agent_prompt.v05-ch10.sma-c.attempt3.md` |
| T-0001-S46 | analyzer-phase1 | v05-ch10 | planned | 0 | `—` |
| T-0001-S47 | analyzer-phase2 | v05-ch10 | planned | 0 | `—` |
| T-0001-S48 | grammar-audit | v05-ch10 | planned | 0 | `—` |
| T-0001-S49 | sma-a | v05-ch11 | done | 2 | `agent_prompts/agent_prompt.v05-ch11.sma-a.attempt2.md` |
| T-0001-S50 | sma-b | v05-ch11 | done | 2 | `agent_prompts/agent_prompt.v05-ch11.sma-b.attempt2.md` |
| T-0001-S51 | sma-c | v05-ch11 | done | 2 | `agent_prompts/agent_prompt.v05-ch11.sma-c.attempt2.md` |
| T-0001-S52 | analyzer-phase1 | v05-ch11 | done | 1 | `agent_prompts/agent_prompt.v05-ch11.analyzer-phase1.md` |
| T-0001-S53 | analyzer-phase2 | v05-ch11 | done | 1 | `agent_prompts/agent_prompt.v05-ch11.analyzer-phase2.md` |
| T-0001-S54 | grammar-audit | v05-ch11 | done | 0 | `—` |
| T-0001-S55 | sma-a | v05-ch12 | interrupted | 3 | `agent_prompts/agent_prompt.v05-ch12.sma-a.attempt3.md` |
| T-0001-S56 | sma-b | v05-ch12 | interrupted | 2 | `agent_prompts/agent_prompt.v05-ch12.sma-b.attempt2.md` |
| T-0001-S57 | sma-c | v05-ch12 | interrupted | 2 | `agent_prompts/agent_prompt.v05-ch12.sma-c.attempt2.md` |
| T-0001-S58 | analyzer-phase1 | v05-ch12 | planned | 0 | `—` |
| T-0001-S59 | analyzer-phase2 | v05-ch12 | planned | 0 | `—` |
| T-0001-S60 | grammar-audit | v05-ch12 | planned | 0 | `—` |
| T-0001-S61 | sma-a | v06-ch01 | planned | 0 | `—` |
| T-0001-S62 | sma-b | v06-ch01 | planned | 0 | `—` |
| T-0001-S63 | sma-c | v06-ch01 | planned | 0 | `—` |
| T-0001-S64 | analyzer-phase1 | v06-ch01 | planned | 0 | `—` |
| T-0001-S65 | analyzer-phase2 | v06-ch01 | planned | 0 | `—` |
| T-0001-S66 | grammar-audit | v06-ch01 | planned | 0 | `—` |
| T-0001-S67 | sma-a | v06-ch02 | planned | 0 | `—` |
| T-0001-S68 | sma-b | v06-ch02 | planned | 0 | `—` |
| T-0001-S69 | sma-c | v06-ch02 | planned | 0 | `—` |
| T-0001-S70 | analyzer-phase1 | v06-ch02 | planned | 0 | `—` |
| T-0001-S71 | analyzer-phase2 | v06-ch02 | planned | 0 | `—` |
| T-0001-S72 | grammar-audit | v06-ch02 | planned | 0 | `—` |
| T-0001-S73 | sma-a | v06-ch04 | planned | 0 | `—` |
| T-0001-S74 | sma-b | v06-ch04 | planned | 0 | `—` |
| T-0001-S75 | sma-c | v06-ch04 | planned | 0 | `—` |
| T-0001-S76 | analyzer-phase1 | v06-ch04 | planned | 0 | `—` |
| T-0001-S77 | analyzer-phase2 | v06-ch04 | planned | 0 | `—` |
| T-0001-S78 | grammar-audit | v06-ch04 | planned | 0 | `—` |
| T-0001-S79 | sma-a | v06-ch05 | planned | 0 | `—` |
| T-0001-S80 | sma-b | v06-ch05 | planned | 0 | `—` |
| T-0001-S81 | sma-c | v06-ch05 | planned | 0 | `—` |
| T-0001-S82 | analyzer-phase1 | v06-ch05 | planned | 0 | `—` |
| T-0001-S83 | analyzer-phase2 | v06-ch05 | planned | 0 | `—` |
| T-0001-S84 | grammar-audit | v06-ch05 | planned | 0 | `—` |
| T-0001-S85 | analyzer-phase1 | v05-ch10 | interrupted | 1 | `agent_prompts/agent_prompt.v05-ch10.analyzer-phase1.md` |
| T-0001-S86 | analyzer-phase2 | v05-ch10 | planned | 0 | `—` |
| T-0001-S87 | grammar-audit | v05-ch10 | done | 1 | `agent_prompts/agent_prompt.v05-ch10.grammar-audit.md` |
| T-0001-S88 | style-audit | v05-ch10 | done | 1 | `agent_prompts/agent_prompt.v05-ch10.style-audit.md` |
| T-0001-S89 | humanizer | v05-ch10 | done | 1 | `agent_prompts/agent_prompt.v05-ch10.humanizer.md` |
| T-0001-S90 | grammar-audit | v05-ch12 | done | 1 | `agent_prompts/agent_prompt.v05-ch12.grammar-audit.md` |
| T-0001-S91 | style-audit | v05-ch12 | done | 1 | `agent_prompts/agent_prompt.v05-ch12.style-audit.md` |
| T-0001-S92 | humanizer | v05-ch12 | done | 1 | `agent_prompts/agent_prompt.v05-ch12.humanizer.md` |
| T-0001-S93 | analyzer-phase1 | v05-ch12 | interrupted | 1 | `agent_prompts/agent_prompt.v05-ch12.analyzer-phase1.md` |

Заметки:
- T-0001-S1: findings: 10 (3 WARNING, 7 CANDIDATE), файл a/20261018-135405-7655.json, валидация OK
- T-0001-S2: findings: 1 CANDIDATE (блок 11, NUANCE_SHIFT), файл b/20261018-091105-8ae6.json
- T-0001-S3: findings: [] (0 прагматических расхождений), файл c/20261018-083546-223c.json
- T-0001-S4: phase1: analysis/20261018-085243-26bd.phase1.json, 2 LOW-кандидата
- T-0001-S5: 27 кандидатов: 22 FIXED, 4 FALSE_POSITIVE, 1 DISPUTED/REPORT_ONLY; analysis/20261018-144106-bb35.json/.md
- T-0001-S6: 8 кандидатов, 1 исправление (б11), отчёт _audit/v05-ch03.md + _log/v5-log.md обновлены, коммит c721c61
- T-0001-S7: completed
- T-0001-S8: completed
- T-0001-S9: completed
- T-0001-S10: phase1: 20261009-165055-77b9.phase1.json, all blocks checked
- T-0001-S11: phase2: 20261009-165412-ef8a.json, 11 candidates, 9 FIXED, 1 DISPUTED, 1 FALSE_POSITIVE
- T-0001-S12: completed
- T-0001-S13: 5 findings (4 ERROR бл.7,8,9,15 + 1 WARNING бл.10); a/20261019-002752-7f32.json
- T-0001-S14: 3 findings (WARNING бл.3,6 + CANDIDATE бл.8); b/20261019-002752-d41f.json
- T-0001-S15: no c-runs, skip
- T-0001-S16: нет результата после запуска
- T-0001-S17: нет результата после запуска
- T-0001-S19: нет результата после запуска
- T-0001-S20: нет результата после запуска
- T-0001-S21: нет результата после запуска
- T-0001-S25: нет результата после запуска
- T-0001-S26: нет результата после запуска
- T-0001-S27: нет результата после запуска
- T-0001-S31: нет результата после запуска
- T-0001-S32: нет результата после запуска
- T-0001-S33: нет результата после запуска
- T-0001-S37: sma-a: 13 находок, файл a/20261022-020909-9f86.json, валидатор OK
- T-0001-S38: sma-b: b/20261022-022956-6a4a.json, 3 findings, валидатор OK
- T-0001-S39: sma-c: c/20261022-022956-941d.json, 4 findings, валидатор OK
- T-0001-S40: analyzer-phase1: analysis/20261022-020914-09bb.phase1.json, 11 findings
- T-0001-S41: analyzer-phase2: analysis/20261022-032355-2502.json/.md, 22 candidates (14 FIXED, 2 REPORT_ONLY, 6 PRESERVED); 3 findings откачены как зона человека
- T-0001-S42: grammar-audit выполнен оркестратором вручную (субагент вернул пустой результат): grammar_scan 6 (все FALSE POSITIVE) + сплошной разбор 13/13 блоков по предложениям (RGC-1/2/3/4/7) — 5 исправлений (разнеслась, скучающе, Луизе надоело, 'кто помог… проникнуть', 'сама Анриетта'); style 9 (все PRESERVED), format 1 (FP), check_records 2 (оба FP), address 0; FINAL READ выполнен; артефакты: output/_audit/v5-ch09.md + output/_log/v5-log.md
- T-0001-S43: нет результата после запуска
- T-0001-S44: нет результата после запуска
- T-0001-S45: нет результата после запуска
- T-0001-S49: результат на диске
- T-0001-S50: результат на диске
- T-0001-S51: результат на диске
- T-0001-S52: результат на диске
- T-0001-S53: результат на диске: analysis/20261022-092020-ba9d.json
- T-0001-S54: грамматический аудит выполнен в составе полного аудита главы (russian-grammar-control вручную по 17/17 блокам + grammar/style/format/check_records/address); отчёт: output/_audit/v5-ch11.md, правки через fix_block.py --replace-file, chapter_gate 12/12
- T-0001-S55: нет результата после запуска
- T-0001-S56: нет результата после запуска
- T-0001-S57: нет результата после запуска
- T-0001-S85: нет результата после запуска
- T-0001-S93: нет результата после запуска

## T-0002 — OPEN

Tom 6: verify ch01-ch08 full audit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0002-S1 | sma-a | v06-afterword | planned | 0 | `—` |
| T-0002-S2 | sma-b | v06-afterword | planned | 0 | `—` |
| T-0002-S3 | sma-c | v06-afterword | planned | 0 | `—` |
| T-0002-S4 | analyzer-phase1 | v06-afterword | planned | 0 | `—` |
| T-0002-S5 | analyzer-phase2 | v06-afterword | planned | 0 | `—` |
| T-0002-S6 | grammar-audit | v06-afterword | planned | 0 | `—` |
| T-0002-S7 | style-audit | v06-afterword | planned | 0 | `—` |
| T-0002-S8 | humanizer | v06-afterword | planned | 0 | `—` |
| T-0002-S9 | sma-a | v06-ch01 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch01.sma-a.md` |
| T-0002-S10 | sma-b | v06-ch01 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch01.sma-b.md` |
| T-0002-S11 | sma-c | v06-ch01 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch01.sma-c.md` |
| T-0002-S12 | analyzer-phase1 | v06-ch01 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch01.analyzer-phase1.md` |
| T-0002-S13 | analyzer-phase2 | v06-ch01 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch01.analyzer-phase2.md` |
| T-0002-S14 | grammar-audit | v06-ch01 | planned | 0 | `—` |
| T-0002-S15 | style-audit | v06-ch01 | planned | 0 | `—` |
| T-0002-S16 | humanizer | v06-ch01 | planned | 0 | `—` |
| T-0002-S17 | sma-a | v06-ch02 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch02.sma-a.md` |
| T-0002-S18 | sma-b | v06-ch02 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch02.sma-b.md` |
| T-0002-S19 | sma-c | v06-ch02 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch02.sma-c.md` |
| T-0002-S20 | analyzer-phase1 | v06-ch02 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch02.analyzer-phase1.md` |
| T-0002-S21 | analyzer-phase2 | v06-ch02 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch02.analyzer-phase2.md` |
| T-0002-S22 | grammar-audit | v06-ch02 | planned | 0 | `—` |
| T-0002-S23 | style-audit | v06-ch02 | planned | 0 | `—` |
| T-0002-S24 | humanizer | v06-ch02 | planned | 0 | `—` |
| T-0002-S25 | sma-a | v06-ch03 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch03.sma-a.md` |
| T-0002-S26 | sma-b | v06-ch03 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch03.sma-b.md` |
| T-0002-S27 | sma-c | v06-ch03 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch03.sma-c.md` |
| T-0002-S28 | analyzer-phase1 | v06-ch03 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch03.analyzer-phase1.md` |
| T-0002-S29 | analyzer-phase2 | v06-ch03 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch03.analyzer-phase2.md` |
| T-0002-S30 | grammar-audit | v06-ch03 | running | 1 | `agent_prompts/agent_prompt.v06-ch03.grammar-audit.md` |
| T-0002-S31 | style-audit | v06-ch03 | planned | 0 | `—` |
| T-0002-S32 | humanizer | v06-ch03 | planned | 0 | `—` |
| T-0002-S33 | sma-a | v06-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch04.sma-a.md` |
| T-0002-S34 | sma-b | v06-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch04.sma-b.md` |
| T-0002-S35 | sma-c | v06-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch04.sma-c.md` |
| T-0002-S36 | analyzer-phase1 | v06-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch04.analyzer-phase1.md` |
| T-0002-S37 | analyzer-phase2 | v06-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch04.analyzer-phase2.md` |
| T-0002-S38 | grammar-audit | v06-ch04 | done | 1 | `agent_prompts/agent_prompt.v06-ch04.grammar-audit.md` |
| T-0002-S39 | style-audit | v06-ch04 | done | 1 | `agent_prompts/agent_prompt.v06-ch04.style-audit.md` |
| T-0002-S40 | humanizer | v06-ch04 | planned | 0 | `—` |
| T-0002-S41 | sma-a | v06-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch05.sma-a.md` |
| T-0002-S42 | sma-b | v06-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch05.sma-b.md` |
| T-0002-S43 | sma-c | v06-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch05.sma-c.md` |
| T-0002-S44 | analyzer-phase1 | v06-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch05.analyzer-phase1.md` |
| T-0002-S45 | analyzer-phase2 | v06-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch05.analyzer-phase2.md` |
| T-0002-S46 | grammar-audit | v06-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch05.grammar-audit.md` |
| T-0002-S47 | style-audit | v06-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch05.style-audit.md` |
| T-0002-S48 | humanizer | v06-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch05.humanizer.md` |
| T-0002-S49 | sma-a | v06-ch06 | done | 2 | `agent_prompts/agent_prompt.v06-ch06.sma-a.attempt2.md` |
| T-0002-S50 | sma-b | v06-ch06 | done | 1 | `agent_prompts/agent_prompt.v06-ch06.sma-b.md` |
| T-0002-S51 | sma-c | v06-ch06 | done | 1 | `agent_prompts/agent_prompt.v06-ch06.sma-c.md` |
| T-0002-S52 | analyzer-phase1 | v06-ch06 | done | 2 | `agent_prompts/agent_prompt.v06-ch06.analyzer-phase1.attempt2.md` |
| T-0002-S53 | analyzer-phase2 | v06-ch06 | done | 4 | `agent_prompts/agent_prompt.v06-ch06.analyzer-phase2.attempt4.md` |
| T-0002-S54 | grammar-audit | v06-ch06 | done | 1 | `agent_prompts/agent_prompt.v06-ch06.grammar-audit.md` |
| T-0002-S55 | style-audit | v06-ch06 | done | 1 | `agent_prompts/agent_prompt.v06-ch06.style-audit.md` |
| T-0002-S56 | humanizer | v06-ch06 | done | 1 | `agent_prompts/agent_prompt.v06-ch06.humanizer.md` |
| T-0002-S57 | sma-a | v06-ch07 | done | 1 | `agent_prompts/agent_prompt.v06-ch07.sma-a.md` |
| T-0002-S58 | sma-b | v06-ch07 | done | 1 | `agent_prompts/agent_prompt.v06-ch07.sma-b.md` |
| T-0002-S59 | sma-c | v06-ch07 | done | 1 | `agent_prompts/agent_prompt.v06-ch07.sma-c.md` |
| T-0002-S60 | analyzer-phase1 | v06-ch07 | done | 1 | `agent_prompts/agent_prompt.v06-ch07.analyzer-phase1.md` |
| T-0002-S61 | analyzer-phase2 | v06-ch07 | done | 1 | `agent_prompts/agent_prompt.v06-ch07.analyzer-phase2.md` |
| T-0002-S62 | grammar-audit | v06-ch07 | done | 1 | `agent_prompts/agent_prompt.v06-ch07.grammar-audit.md` |
| T-0002-S63 | style-audit | v06-ch07 | done | 1 | `agent_prompts/agent_prompt.v06-ch07.style-audit.md` |
| T-0002-S64 | humanizer | v06-ch07 | done | 1 | `agent_prompts/agent_prompt.v06-ch07.humanizer.md` |
| T-0002-S65 | sma-a | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.sma-a.md` |
| T-0002-S66 | sma-b | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.sma-b.md` |
| T-0002-S67 | sma-c | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.sma-c.md` |
| T-0002-S68 | analyzer-phase1 | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.analyzer-phase1.md` |
| T-0002-S69 | analyzer-phase2 | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.analyzer-phase2.md` |
| T-0002-S70 | grammar-audit | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.grammar-audit.md` |
| T-0002-S71 | style-audit | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.style-audit.md` |
| T-0002-S72 | humanizer | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.humanizer.md` |
| T-0002-S73 | full-audit | v06-ch05 | done | 1 | `agent_prompts/agent_prompt.v06-ch05.full-audit.md` |
| T-0002-S74 | full-audit | v06-ch06 | done | 1 | `agent_prompts/agent_prompt.v06-ch06.full-audit.md` |
| T-0002-S75 | full-audit | v06-ch07 | done | 2 | `agent_prompts/agent_prompt.v06-ch07.full-audit.attempt2.md` |
| T-0002-S76 | full-audit | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.full-audit.md` |
| T-0002-S77 | full-audit | v06-ch07 | planned | 0 | `—` |
| T-0002-S78 | sma-a | v06-ch07 | done | 2 | `agent_prompts/agent_prompt.v06-ch07.sma-a.attempt2.md` |
| T-0002-S79 | sma-b | v06-ch07 | done | 2 | `agent_prompts/agent_prompt.v06-ch07.sma-b.attempt2.md` |
| T-0002-S80 | sma-c | v06-ch07 | done | 2 | `agent_prompts/agent_prompt.v06-ch07.sma-c.attempt2.md` |
| T-0002-S81 | analyzer-phase1 | v06-ch07 | done | 1 | `agent_prompts/agent_prompt.v06-ch07.analyzer-phase1.md` |
| T-0002-S82 | analyzer-phase2 | v06-ch07 | done | 1 | `agent_prompts/agent_prompt.v06-ch07.analyzer-phase2.md` |
| T-0002-S83 | sma-a | v06-ch08 | done | 2 | `agent_prompts/agent_prompt.v06-ch08.sma-a.attempt2.md` |
| T-0002-S84 | sma-b | v06-ch08 | done | 2 | `agent_prompts/agent_prompt.v06-ch08.sma-b.attempt2.md` |
| T-0002-S85 | sma-c | v06-ch08 | done | 2 | `agent_prompts/agent_prompt.v06-ch08.sma-c.attempt2.md` |
| T-0002-S86 | analyzer-phase1 | v06-ch08 | planned | 0 | `—` |
| T-0002-S87 | analyzer-phase2 | v06-ch08 | planned | 0 | `—` |
| T-0002-S88 | sma-a | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.sma-a.md` |
| T-0002-S89 | sma-b | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.sma-b.md` |
| T-0002-S90 | sma-c | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.sma-c.md` |
| T-0002-S91 | analyzer-phase1 | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.analyzer-phase1.md` |
| T-0002-S92 | analyzer-phase2 | v06-ch08 | done | 1 | `agent_prompts/agent_prompt.v06-ch08.analyzer-phase2.md` |

Заметки:
- T-0002-S9: нет результата после запуска
- T-0002-S10: нет результата после запуска
- T-0002-S11: нет результата после запуска
- T-0002-S12: нет результата после запуска
- T-0002-S13: нет результата после запуска
- T-0002-S17: нет результата после запуска
- T-0002-S18: нет результата после запуска
- T-0002-S19: нет результата после запуска
- T-0002-S20: нет результата после запуска
- T-0002-S21: нет результата после запуска
- T-0002-S25: нет результата после запуска
- T-0002-S26: нет результата после запуска
- T-0002-S27: нет результата после запуска
- T-0002-S28: нет результата после запуска
- T-0002-S29: нет результата после запуска
- T-0002-S33: нет результата после запуска
- T-0002-S34: нет результата после запуска
- T-0002-S35: нет результата после запуска
- T-0002-S36: нет результата после запуска
- T-0002-S37: нет результата после запуска
- T-0002-S41: нет результата после запуска
- T-0002-S42: нет результата после запуска
- T-0002-S43: нет результата после запуска
- T-0002-S44: нет результата после запуска
- T-0002-S45: нет результата после запуска
- T-0002-S46: изменений после запуска нет
- T-0002-S47: изменений после запуска нет
- T-0002-S48: изменений после запуска нет
- T-0002-S49: артефакт sma-a ch06 от 22.10 на месте, работа закрыта
- T-0002-S50: артефакт sma-b ch06 от 22.10 на месте, работа закрыта
- T-0002-S51: артефакт sma-c ch06 от 22.10 на месте, работа закрыта
- T-0002-S52: Фаза 1 (blind) ch06: 5 кандидатов, пропусков нет
- T-0002-S53: Фаза 2 (evidence review) ch06: 5 кандидатов, 0 CONFIRMED_ERROR, правок нет
- T-0002-S57: закрыто запуском T-0002-S78 (sma-a ch07)
- T-0002-S58: закрыто запуском T-0002-S79 (sma-b ch07)
- T-0002-S59: закрыто запуском T-0002-S80 (sma-c ch07)
- T-0002-S60: закрыто запуском T-0002-S81 (analyzer ph1 ch07)
- T-0002-S61: закрыто запуском T-0002-S82 (analyzer ph2 ch07)
- T-0002-S62: verify: свежий отчёт grammar ch07 на месте
- T-0002-S63: verify: свежий отчёт style ch07 на месте
- T-0002-S64: verify: свежий отчёт humanizer ch07 на месте
- T-0002-S65: закрыто запуском T-0002-S88 (sma-a ch08)
- T-0002-S66: закрыто запуском T-0002-S89 (sma-b ch08)
- T-0002-S67: закрыто запуском T-0002-S90 (sma-c ch08)
- T-0002-S68: закрыто запуском T-0002-S91 (analyzer ph1 ch08)
- T-0002-S69: закрыто запуском T-0002-S92 (analyzer ph2 ch08)
- T-0002-S70: verify: свежий отчёт grammar ch08 на месте
- T-0002-S71: verify: свежий отчёт style ch08 на месте
- T-0002-S72: verify: свежий отчёт humanizer ch08 на месте
- T-0002-S73: FINAL AUDIT v6-ch05 выполнен оркестратором: отчёт output/_audit/v6-ch05.md, правка 'Мисс Матильда'->'Матильда' через fix_block.py блок 8, merged обновлён, лог дополнен
- T-0002-S74: Полная обработка v6-ch06 субагентом ses_e3c886b49ffelPPylzoYQkDUnD: 26/26 блоков по JA, ED_RU 26/26, отчёт output/_audit/v06-ch06.md, верифицировано оркестратором (маркеры 1-26, кавычки, сканеры сходятся с отчётом)
- T-0002-S78: SMA-A по ch07: 4 находки, 3 приняты (исправлены), 1 оспорена
- T-0002-S79: SMA-B по ch07: 0 находок
- T-0002-S80: SMA-C по ch07: 3 находки, 2 приняты (исправлены), 1 спорна
- T-0002-S81: Фаза 1 (blind) ch07: 1 кандидат (блок 13), записано в analysis/
- T-0002-S82: Фаза 2 (evidence review) ch07: 7 кандидатов, 6 FP/PRESERVED + 1 CONFIRMED_ERROR (оспорено по JA)
- T-0002-S83: SMA-A по сырому RU (до переработки): 17 находок, все отнесены к переработке
- T-0002-S84: SMA-B по сырому RU (до переработки): 9 находок, учтены при переработке
- T-0002-S85: SMA-C по сырому RU (до переработки): 6 находок, учтены при переработке
- T-0002-S88: SMA-A ch08 по переработанному тексту: 16 находок
- T-0002-S89: SMA-B ch08 по переработанному тексту: 7 находок
- T-0002-S90: SMA-C ch08 по переработанному тексту: 4 находки
- T-0002-S91: Фаза 1 (blind) ch08: 25 кандидатов
- T-0002-S92: Фаза 2 (evidence review) ch08: 56 кандидатов, 7 FIXED применены в текст

## T-0003 — DONE

Проверка тома 7: полный pipeline по главам

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0003-S1 | sma-a | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.sma-a.md` |
| T-0003-S2 | sma-b | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.sma-b.md` |
| T-0003-S3 | sma-c | v07-ch01 | done | 3 | `agent_prompts/agent_prompt.v07-ch01.sma-c.attempt3.md` |
| T-0003-S4 | analyzer-phase1 | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.analyzer-phase1.md` |
| T-0003-S5 | analyzer-phase2 | v07-ch01 | done | 2 | `agent_prompts/agent_prompt.v07-ch01.analyzer-phase2.attempt2.md` |
| T-0003-S6 | sma-a | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.sma-a.md` |
| T-0003-S7 | sma-b | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.sma-b.md` |
| T-0003-S8 | sma-c | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.sma-c.md` |
| T-0003-S9 | analyzer-phase1 | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.analyzer-phase1.md` |
| T-0003-S10 | analyzer-phase2 | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.analyzer-phase2.md` |
| T-0003-S11 | sma-a | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.sma-a.md` |
| T-0003-S12 | sma-b | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.sma-b.md` |
| T-0003-S13 | sma-c | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.sma-c.md` |
| T-0003-S14 | analyzer-phase1 | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.analyzer-phase1.md` |
| T-0003-S15 | analyzer-phase2 | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.analyzer-phase2.md` |
| T-0003-S16 | sma-a | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.sma-a.md` |
| T-0003-S17 | sma-b | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.sma-b.md` |
| T-0003-S18 | sma-c | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.sma-c.md` |
| T-0003-S19 | analyzer-phase1 | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.analyzer-phase1.md` |
| T-0003-S20 | analyzer-phase2 | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.analyzer-phase2.md` |
| T-0003-S21 | sma-a | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.sma-a.md` |
| T-0003-S22 | sma-b | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.sma-b.md` |
| T-0003-S23 | sma-c | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.sma-c.md` |
| T-0003-S24 | analyzer-phase1 | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.analyzer-phase1.md` |
| T-0003-S25 | analyzer-phase2 | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.analyzer-phase2.md` |
| T-0003-S26 | sma-a | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.sma-a.md` |
| T-0003-S27 | sma-b | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.sma-b.md` |
| T-0003-S28 | sma-c | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.sma-c.md` |
| T-0003-S29 | analyzer-phase1 | v07-ch06 | done | 2 | `agent_prompts/agent_prompt.v07-ch06.analyzer-phase1.attempt2.md` |
| T-0003-S30 | analyzer-phase2 | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.analyzer-phase2.md` |
| T-0003-S31 | sma-a | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.sma-a.md` |
| T-0003-S32 | sma-b | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.sma-b.md` |
| T-0003-S33 | sma-c | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.sma-c.md` |
| T-0003-S34 | analyzer-phase1 | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.analyzer-phase1.md` |
| T-0003-S35 | analyzer-phase2 | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.analyzer-phase2.md` |
| T-0003-S36 | sma-a | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.sma-a.md` |
| T-0003-S37 | sma-b | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.sma-b.md` |
| T-0003-S38 | sma-c | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.sma-c.md` |
| T-0003-S39 | analyzer-phase1 | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.analyzer-phase1.md` |
| T-0003-S40 | analyzer-phase2 | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.analyzer-phase2.md` |
| T-0003-S41 | sma-a | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.sma-a.md` |
| T-0003-S42 | sma-b | v07-ch09 | done | 2 | `agent_prompts/agent_prompt.v07-ch09.sma-b.attempt2.md` |
| T-0003-S43 | sma-c | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.sma-c.md` |
| T-0003-S44 | analyzer-phase1 | v07-ch09 | done | 2 | `agent_prompts/agent_prompt.v07-ch09.analyzer-phase1.attempt2.md` |
| T-0003-S45 | analyzer-phase2 | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.analyzer-phase2.md` |
| T-0003-S46 | sma-a | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.sma-a.md` |
| T-0003-S47 | sma-b | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.sma-b.md` |
| T-0003-S48 | sma-c | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.sma-c.md` |
| T-0003-S49 | analyzer-phase1 | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.analyzer-phase1.md` |
| T-0003-S50 | analyzer-phase2 | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.analyzer-phase2.md` |
| T-0003-S51 | sma-a | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.sma-a.md` |
| T-0003-S52 | sma-b | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.sma-b.md` |
| T-0003-S53 | sma-c | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.sma-c.md` |
| T-0003-S54 | analyzer-phase1 | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.analyzer-phase1.md` |
| T-0003-S55 | analyzer-phase2 | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.analyzer-phase2.md` |
| T-0003-S56 | sma-a | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.sma-a.md` |
| T-0003-S57 | sma-b | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.sma-b.md` |
| T-0003-S58 | sma-c | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.sma-c.md` |
| T-0003-S59 | analyzer-phase1 | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.analyzer-phase1.md` |
| T-0003-S60 | analyzer-phase2 | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.analyzer-phase2.md` |

Заметки:
- T-0003-S1: SMA-A: 8 находок, все приняты
- T-0003-S2: SMA-B: 7 находок, приняты 5 (2 уже закрыты)
- T-0003-S3: SMA-C: 5 находок, все приняты (2-я попытка после блокировки провайдера)
- T-0003-S4: Фаза 1 (blind): 16 находок, пропусков нет
- T-0003-S5: Фаза 2: 25 кандидатов (20 FIXED уже внесены, 2 новых приняты, 3 DISPUTED REPORT_ONLY)
- T-0003-S6: SMA-A: 15 находок, все приняты
- T-0003-S7: SMA-B: 8 находок, все приняты
- T-0003-S8: SMA-C: 1 находка ERROR, принята
- T-0003-S9: Фаза 1: 9 находок, 4 CJK-артефакта исправлены
- T-0003-S10: Phase 2 ch02: all FP/PRESERVED, fixes already applied
- T-0003-S11: SMA-A: 12 находок, все приняты
- T-0003-S12: SMA-B: 10 находок, все приняты
- T-0003-S13: SMA-C: 2 находки, приняты
- T-0003-S14: Фаза 1: 9 находок (2 пропуска, 4 CJK, инверсии)
- T-0003-S15: Phase 2 ch03: all CONFIRMED_ERROR applied via Execution Bridge
- T-0003-S16: SMA-A: 9 находок, все приняты
- T-0003-S17: SMA-B: 3 находки (инверсия 衆寡敵せず, столица, субъект кольца), приняты
- T-0003-S18: SMA-C: 2 находки (модальность), приняты
- T-0003-S19: Фаза 1: 5 находок (инверсия 衆寡敵せず и др.), приняты
- T-0003-S20: Phase 2: 16 FIXED, 1 applied via Execution Bridge
- T-0003-S21: SMA-A: см.Filename
- T-0003-S22: SMA-B: 2 находки (блоки 4,13), приняты
- T-0003-S23: SMA-C: 1 ERROR (атрибуция блока 11), принята
- T-0003-S24: Фаза 1: 4 находки, приняты
- T-0003-S25: Phase 2: 13 FP/PRESERVED, all fixes already applied
- T-0003-S26: SMA-A: 9 находок, приняты
- T-0003-S27: SMA-B: 14 находок, приняты
- T-0003-S28: SMA-C: 3 находки, приняты
- T-0003-S29: Фаза 1 (retry): 12 находок, приняты
- T-0003-S30: Phase 2: 25 CONFIRMED_ERROR, 5 REPORT_ONLY applied
- T-0003-S31: SMA-A: 7 находок, приняты
- T-0003-S32: SMA-B: 3 находки, приняты
- T-0003-S33: SMA-C: 0 находок
- T-0003-S34: Фаза 1: 5 находок, приняты
- T-0003-S35: Phase 2: 11 FP/PRESERVED, typo Р»Р¶С‘С€СЊ fixed
- T-0003-S36: SMA-A: 3 находки, приняты
- T-0003-S37: SMA-B: 9 находок, приняты
- T-0003-S38: SMA-C: 2 находки, приняты
- T-0003-S39: Фаза 1: 4 находки, приняты
- T-0003-S40: Phase 2: C-17 recovered йЂ†и»ўгЃ™г‚‹гЃ®гЃ , C-14 DISPUTED
- T-0003-S41: SMA-A: 2 находки (ERROR 四万), приняты
- T-0003-S42: SMA-B retry: 3 находки, приняты
- T-0003-S43: SMA-C: 1 находка, принята
- T-0003-S44: Фаза 1 retry: иероглиф 巸 удалён
- T-0003-S45: Phase 2: 5 FP/PRESERVED, 1 DISPUTED (Р±Р»РѕРє 11)
- T-0003-S46: SMA-A: 8 находок, приняты
- T-0003-S47: SMA-B: 4 находки, приняты
- T-0003-S48: SMA-C: 1 находка, принята
- T-0003-S49: Фаза 1: 9 находок, приняты
- T-0003-S50: Phase 2: 16 FIXED, 1 DISPUTED reported only
- T-0003-S51: SMA-A: 5 find, applied
- T-0003-S52: SMA-B: 4 find, applied
- T-0003-S53: SMA-C: 2 find, applied
- T-0003-S54: Phase1: 10 find, applied
- T-0003-S55: Phase 2: 14 FIXED, 1 REPORT_ONLY gender reverted
- T-0003-S56: SMA-A: 7 find, applied
- T-0003-S57: SMA-B: 5 find, applied
- T-0003-S58: SMA-C: 0 find
- T-0003-S59: Phase1: 3 find, applied
- T-0003-S60: Phase 2: 9 FP, 2 DISPUTED applied

## T-0004 — DONE

Полный перевод тома 8

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0004-S1 | sma-a | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.sma-a.md` |
| T-0004-S2 | sma-b | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.sma-b.md` |
| T-0004-S3 | sma-c | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.sma-c.md` |
| T-0004-S4 | analyzer-phase1 | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.analyzer-phase1.md` |
| T-0004-S5 | analyzer-phase2 | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.analyzer-phase2.md` |
| T-0004-S6 | sma-a | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.sma-a.md` |
| T-0004-S7 | sma-b | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.sma-b.md` |
| T-0004-S8 | sma-c | v08-ch02 | done | 2 | `agent_prompts/agent_prompt.v08-ch02.sma-c.attempt2.md` |
| T-0004-S9 | analyzer-phase1 | v08-ch02 | done | 2 | `agent_prompts/agent_prompt.v08-ch02.analyzer-phase1.attempt2.md` |
| T-0004-S10 | analyzer-phase2 | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.analyzer-phase2.md` |
| T-0004-S11 | sma-a | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.sma-a.md` |
| T-0004-S12 | sma-b | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.sma-b.md` |
| T-0004-S13 | sma-c | v08-ch03 | done | 2 | `agent_prompts/agent_prompt.v08-ch03.sma-c.attempt2.md` |
| T-0004-S14 | analyzer-phase1 | v08-ch03 | done | 2 | `agent_prompts/agent_prompt.v08-ch03.analyzer-phase1.attempt2.md` |
| T-0004-S15 | analyzer-phase2 | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.analyzer-phase2.md` |
| T-0004-S16 | sma-a | v08-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch04.sma-a.md` |
| T-0004-S17 | sma-b | v08-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch04.sma-b.md` |
| T-0004-S18 | sma-c | v08-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch04.sma-c.md` |
| T-0004-S19 | analyzer-phase1 | v08-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch04.analyzer-phase1.md` |
| T-0004-S20 | analyzer-phase2 | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.analyzer-phase2.md` |
| T-0004-S21 | sma-a | v08-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch05.sma-a.md` |
| T-0004-S22 | sma-b | v08-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch05.sma-b.md` |
| T-0004-S23 | sma-c | v08-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch05.sma-c.md` |
| T-0004-S24 | analyzer-phase1 | v08-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch05.analyzer-phase1.md` |
| T-0004-S25 | analyzer-phase2 | v08-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch05.analyzer-phase2.md` |
| T-0004-S26 | sma-a | v08-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch06.sma-a.md` |
| T-0004-S27 | sma-b | v08-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch06.sma-b.md` |
| T-0004-S28 | sma-c | v08-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch06.sma-c.md` |
| T-0004-S29 | analyzer-phase1 | v08-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch06.analyzer-phase1.md` |
| T-0004-S30 | analyzer-phase2 | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.analyzer-phase2.md` |
| T-0004-S31 | sma-a | v08-ch07 | done | 4 | `agent_prompts/agent_prompt.v08-ch07.sma-a.attempt4.md` |
| T-0004-S32 | sma-b | v08-ch07 | interrupted | 3 | `agent_prompts/agent_prompt.v08-ch07.sma-b.attempt3.md` |
| T-0004-S33 | sma-c | v08-ch07 | interrupted | 2 | `agent_prompts/agent_prompt.v08-ch07.sma-c.attempt2.md` |
| T-0004-S34 | analyzer-phase1 | v08-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch07.analyzer-phase1.md` |
| T-0004-S35 | analyzer-phase2 | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.analyzer-phase2.md` |
| T-0004-S36 | sma-a | v08-ch08 | interrupted | 2 | `agent_prompts/agent_prompt.v08-ch08.sma-a.attempt2.md` |
| T-0004-S37 | sma-b | v08-ch08 | interrupted | 2 | `agent_prompts/agent_prompt.v08-ch08.sma-b.attempt2.md` |
| T-0004-S38 | sma-c | v08-ch08 | interrupted | 2 | `agent_prompts/agent_prompt.v08-ch08.sma-c.attempt2.md` |
| T-0004-S39 | analyzer-phase1 | v08-ch08 | interrupted | 2 | `agent_prompts/agent_prompt.v08-ch08.analyzer-phase1.attempt2.md` |
| T-0004-S40 | analyzer-phase2 | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.analyzer-phase2.md` |
| T-0004-S41 | sma-a | v08-ch09 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch09.sma-a.md` |
| T-0004-S42 | sma-b | v08-ch09 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch09.sma-b.md` |
| T-0004-S43 | sma-c | v08-ch09 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch09.sma-c.md` |
| T-0004-S44 | analyzer-phase1 | v08-ch09 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch09.analyzer-phase1.md` |
| T-0004-S45 | analyzer-phase2 | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.analyzer-phase2.md` |
| T-0004-S46 | sma-a | v08-ch10 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch10.sma-a.md` |
| T-0004-S47 | sma-b | v08-ch10 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch10.sma-b.md` |
| T-0004-S48 | sma-c | v08-ch10 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch10.sma-c.md` |
| T-0004-S49 | analyzer-phase1 | v08-ch10 | interrupted | 1 | `agent_prompts/agent_prompt.v08-ch10.analyzer-phase1.md` |
| T-0004-S50 | analyzer-phase2 | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.analyzer-phase2.md` |
| T-0004-S51 | sma-a | v08-epilogue | interrupted | 1 | `agent_prompts/agent_prompt.v08-epilogue.sma-a.md` |
| T-0004-S52 | sma-b | v08-epilogue | interrupted | 2 | `agent_prompts/agent_prompt.v08-epilogue.sma-b.attempt2.md` |
| T-0004-S53 | sma-c | v08-epilogue | interrupted | 1 | `agent_prompts/agent_prompt.v08-epilogue.sma-c.md` |
| T-0004-S54 | analyzer-phase1 | v08-epilogue | interrupted | 2 | `agent_prompts/agent_prompt.v08-epilogue.analyzer-phase1.attempt2.md` |
| T-0004-S55 | analyzer-phase2 | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.analyzer-phase2.md` |
| T-0004-S56 | sma-a | v08-afterword | planned | 0 | `—` |
| T-0004-S57 | sma-b | v08-afterword | planned | 0 | `—` |
| T-0004-S58 | sma-c | v08-afterword | planned | 0 | `—` |
| T-0004-S59 | analyzer-phase1 | v08-afterword | interrupted | 1 | `agent_prompts/agent_prompt.v08-afterword.analyzer-phase1.md` |
| T-0004-S60 | analyzer-phase2 | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.analyzer-phase2.md` |

Заметки:
- T-0004-S1: SMA-A: 5 find, applied
- T-0004-S2: SMA-B: 6 find, applied
- T-0004-S3: SMA-C: 2 find, applied
- T-0004-S4: Phase1: 6 find, applied
- T-0004-S5: Phase 2: 13 FIXED, 2 REPORT_ONLY fixed, 1 FP
- T-0004-S6: applied
- T-0004-S7: applied
- T-0004-S8: applied
- T-0004-S9: applied
- T-0004-S10: Phase 2: 4 FIXED, 1 DISPUTED amplified, 15 FP
- T-0004-S11: applied
- T-0004-S12: applied
- T-0004-S13: applied
- T-0004-S14: applied
- T-0004-S15: Phase2 applied, gate 12/12
- T-0004-S16: нет результата после запуска
- T-0004-S17: нет результата после запуска
- T-0004-S18: нет результата после запуска
- T-0004-S19: нет результата после запуска
- T-0004-S20: Phase2 applied, gate 12/12
- T-0004-S21: нет результата после запуска
- T-0004-S22: нет результата после запуска
- T-0004-S23: нет результата после запуска
- T-0004-S24: нет результата после запуска
- T-0004-S25: нет результата после запуска
- T-0004-S26: нет результата после запуска
- T-0004-S27: нет результата после запуска
- T-0004-S28: нет результата после запуска
- T-0004-S29: нет результата после запуска
- T-0004-S30: Phase2 applied, gate 12/12
- T-0004-S31: SMA-a attempt4, gate 12/12
- T-0004-S32: нет результата после запуска
- T-0004-S33: нет результата после запуска
- T-0004-S34: нет результата после запуска
- T-0004-S35: Phase2 applied, gate 12/12
- T-0004-S36: нет результата после запуска
- T-0004-S37: нет результата после запуска
- T-0004-S38: нет результата после запуска
- T-0004-S39: нет результата после запуска
- T-0004-S40: Phase2 applied, gate 12/12
- T-0004-S41: нет результата после запуска
- T-0004-S42: нет результата после запуска
- T-0004-S43: нет результата после запуска
- T-0004-S44: нет результата после запуска
- T-0004-S45: Phase2 applied, gate 12/12
- T-0004-S46: нет результата после запуска
- T-0004-S47: нет результата после запуска
- T-0004-S48: нет результата после запуска
- T-0004-S49: нет результата после запуска
- T-0004-S50: Phase2 applied, gate 12/12
- T-0004-S51: нет результата после запуска
- T-0004-S52: нет результата после запуска
- T-0004-S53: нет результата после запуска
- T-0004-S54: нет результата после запуска
- T-0004-S55: Phase2 applied, gate 12/12
- T-0004-S59: нет результата после запуска
- T-0004-S60: Phase2 applied, gate 12/12

## T-0005 — DONE

Полный перевод тома 9

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0005-S1 | sma-a | v09-ch01 | interrupted | 2 | `agent_prompts/agent_prompt.v09-ch01.sma-a.attempt2.md` |
| T-0005-S2 | sma-b | v09-ch01 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch01.sma-b.md` |
| T-0005-S3 | sma-c | v09-ch01 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch01.sma-c.md` |
| T-0005-S4 | analyzer-phase1 | v09-ch01 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch01.analyzer-phase1.md` |
| T-0005-S5 | analyzer-phase2 | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.analyzer-phase2.md` |
| T-0005-S6 | sma-a | v09-ch02 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch02.sma-a.md` |
| T-0005-S7 | sma-b | v09-ch02 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch02.sma-b.md` |
| T-0005-S8 | sma-c | v09-ch02 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch02.sma-c.md` |
| T-0005-S9 | analyzer-phase1 | v09-ch02 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch02.analyzer-phase1.md` |
| T-0005-S10 | analyzer-phase2 | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.analyzer-phase2.md` |
| T-0005-S11 | sma-a | v09-ch03 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch03.sma-a.md` |
| T-0005-S12 | sma-b | v09-ch03 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch03.sma-b.md` |
| T-0005-S13 | sma-c | v09-ch03 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch03.sma-c.md` |
| T-0005-S14 | analyzer-phase1 | v09-ch03 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch03.analyzer-phase1.md` |
| T-0005-S15 | analyzer-phase2 | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.analyzer-phase2.md` |
| T-0005-S16 | sma-a | v09-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch04.sma-a.md` |
| T-0005-S17 | sma-b | v09-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch04.sma-b.md` |
| T-0005-S18 | sma-c | v09-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch04.sma-c.md` |
| T-0005-S19 | analyzer-phase1 | v09-ch04 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch04.analyzer-phase1.md` |
| T-0005-S20 | analyzer-phase2 | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.analyzer-phase2.md` |
| T-0005-S21 | sma-a | v09-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch05.sma-a.md` |
| T-0005-S22 | sma-b | v09-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch05.sma-b.md` |
| T-0005-S23 | sma-c | v09-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch05.sma-c.md` |
| T-0005-S24 | analyzer-phase1 | v09-ch05 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch05.analyzer-phase1.md` |
| T-0005-S25 | analyzer-phase2 | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.analyzer-phase2.md` |
| T-0005-S26 | sma-a | v09-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch06.sma-a.md` |
| T-0005-S27 | sma-b | v09-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch06.sma-b.md` |
| T-0005-S28 | sma-c | v09-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch06.sma-c.md` |
| T-0005-S29 | analyzer-phase1 | v09-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch06.analyzer-phase1.md` |
| T-0005-S30 | analyzer-phase2 | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.analyzer-phase2.md` |
| T-0005-S31 | sma-a | v09-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch07.sma-a.md` |
| T-0005-S32 | sma-b | v09-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch07.sma-b.md` |
| T-0005-S33 | sma-c | v09-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch07.sma-c.md` |
| T-0005-S34 | analyzer-phase1 | v09-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch07.analyzer-phase1.md` |
| T-0005-S35 | analyzer-phase2 | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.analyzer-phase2.md` |
| T-0005-S36 | sma-a | v09-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch08.sma-a.md` |
| T-0005-S37 | sma-b | v09-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch08.sma-b.md` |
| T-0005-S38 | sma-c | v09-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch08.sma-c.md` |
| T-0005-S39 | analyzer-phase1 | v09-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch08.analyzer-phase1.md` |
| T-0005-S40 | analyzer-phase2 | v09-ch08 | done | 5 | `agent_prompts/agent_prompt.v09-ch08.analyzer-phase2.attempt5.md` |
| T-0005-S41 | sma-a | v09-ch09 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch09.sma-a.md` |
| T-0005-S42 | sma-b | v09-ch09 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch09.sma-b.md` |
| T-0005-S43 | sma-c | v09-ch09 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch09.sma-c.md` |
| T-0005-S44 | analyzer-phase1 | v09-ch09 | interrupted | 1 | `agent_prompts/agent_prompt.v09-ch09.analyzer-phase1.md` |
| T-0005-S45 | analyzer-phase2 | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.analyzer-phase2.md` |
| T-0005-S46 | sma-a | v09-epilogue | interrupted | 1 | `agent_prompts/agent_prompt.v09-epilogue.sma-a.md` |
| T-0005-S47 | sma-b | v09-epilogue | interrupted | 1 | `agent_prompts/agent_prompt.v09-epilogue.sma-b.md` |
| T-0005-S48 | sma-c | v09-epilogue | interrupted | 1 | `agent_prompts/agent_prompt.v09-epilogue.sma-c.md` |
| T-0005-S49 | analyzer-phase1 | v09-epilogue | interrupted | 1 | `agent_prompts/agent_prompt.v09-epilogue.analyzer-phase1.md` |
| T-0005-S50 | analyzer-phase2 | v09-epilogue | done | 3 | `agent_prompts/agent_prompt.v09-epilogue.analyzer-phase2.attempt3.md` |
| T-0005-S51 | sma-a | v09-afterword | interrupted | 1 | `agent_prompts/agent_prompt.v09-afterword.sma-a.md` |
| T-0005-S52 | sma-b | v09-afterword | interrupted | 1 | `agent_prompts/agent_prompt.v09-afterword.sma-b.md` |
| T-0005-S53 | sma-c | v09-afterword | interrupted | 1 | `agent_prompts/agent_prompt.v09-afterword.sma-c.md` |
| T-0005-S54 | analyzer-phase1 | v09-afterword | interrupted | 1 | `agent_prompts/agent_prompt.v09-afterword.analyzer-phase1.md` |
| T-0005-S55 | analyzer-phase2 | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.analyzer-phase2.md` |

Заметки:
- T-0005-S1: нет результата после запуска
- T-0005-S2: нет результата после запуска
- T-0005-S3: нет результата после запуска
- T-0005-S4: нет результата после запуска
- T-0005-S5: Phase2 applied, gate 12/12
- T-0005-S6: нет результата после запуска
- T-0005-S7: нет результата после запуска
- T-0005-S8: нет результата после запуска
- T-0005-S9: нет результата после запуска
- T-0005-S10: Phase2 applied, gate 12/12
- T-0005-S11: нет результата после запуска
- T-0005-S12: нет результата после запуска
- T-0005-S13: нет результата после запуска
- T-0005-S14: нет результата после запуска
- T-0005-S15: Phase2 applied, gate 12/12
- T-0005-S16: нет результата после запуска
- T-0005-S17: нет результата после запуска
- T-0005-S18: нет результата после запуска
- T-0005-S19: нет результата после запуска
- T-0005-S20: Phase2 applied, gate 12/12
- T-0005-S21: нет результата после запуска
- T-0005-S22: нет результата после запуска
- T-0005-S23: нет результата после запуска
- T-0005-S24: нет результата после запуска
- T-0005-S25: Phase2 applied, gate 12/12
- T-0005-S26: нет результата после запуска
- T-0005-S27: нет результата после запуска
- T-0005-S28: нет результата после запуска
- T-0005-S29: нет результата после запуска
- T-0005-S30: Phase2 applied, gate 12/12
- T-0005-S31: нет результата после запуска
- T-0005-S32: нет результата после запуска
- T-0005-S33: нет результата после запуска
- T-0005-S34: нет результата после запуска
- T-0005-S35: Phase2 applied, gate 12/12
- T-0005-S36: нет результата после запуска
- T-0005-S37: нет результата после запуска
- T-0005-S38: нет результата после запуска
- T-0005-S39: нет результата после запуска
- T-0005-S40: Phase2 applied, gate 12/12
- T-0005-S41: нет результата после запуска
- T-0005-S42: нет результата после запуска
- T-0005-S43: нет результата после запуска
- T-0005-S44: нет результата после запуска
- T-0005-S45: Phase2 applied, gate 12/12
- T-0005-S46: нет результата после запуска
- T-0005-S47: нет результата после запуска
- T-0005-S48: нет результата после запуска
- T-0005-S49: нет результата после запуска
- T-0005-S50: Phase2 applied, gate 12/12
- T-0005-S51: нет результата после запуска
- T-0005-S52: нет результата после запуска
- T-0005-S53: нет результата после запуска
- T-0005-S54: нет результата после запуска
- T-0005-S55: Phase2 applied, gate 12/12

## T-0006 — DONE

Polnyi perevod v6-afterword: 3 bloka po JA, prefilytry, SMA A/B/C + Analyzer, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0006-S1 | sma-a | v06-afterword | done | 1 | `agent_prompts/agent_prompt.v06-afterword.sma-a.md` |
| T-0006-S2 | sma-b | v06-afterword | done | 1 | `agent_prompts/agent_prompt.v06-afterword.sma-b.md` |
| T-0006-S3 | sma-c | v06-afterword | done | 1 | `agent_prompts/agent_prompt.v06-afterword.sma-c.md` |
| T-0006-S4 | analyzer-phase1 | v06-afterword | done | 1 | `agent_prompts/agent_prompt.v06-afterword.analyzer-phase1.md` |
| T-0006-S5 | analyzer-phase2 | v06-afterword | done | 1 | `agent_prompts/agent_prompt.v06-afterword.analyzer-phase2.md` |

Заметки:
- T-0006-S1: SMA + Analyzer applied, gate 12/12
- T-0006-S2: SMA + Analyzer applied, gate 12/12
- T-0006-S3: SMA + Analyzer applied, gate 12/12
- T-0006-S4: SMA + Analyzer applied, gate 12/12
- T-0006-S5: SMA + Analyzer applied, gate 12/12

## T-0007 — DONE

Polnyi perevod i audit v10-ch01: 20 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0007-S1 | sma-a | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.sma-a.md` |
| T-0007-S2 | sma-b | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.sma-b.md` |
| T-0007-S3 | sma-c | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.sma-c.md` |
| T-0007-S4 | analyzer-phase1 | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.analyzer-phase1.md` |
| T-0007-S5 | analyzer-phase2 | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.analyzer-phase2.md` |

Заметки:
- T-0007-S1: SMA + Analyzer applied, gate 12/12
- T-0007-S2: SMA + Analyzer applied, gate 12/12
- T-0007-S3: SMA + Analyzer applied, gate 12/12
- T-0007-S4: SMA + Analyzer applied, gate 12/12
- T-0007-S5: SMA + Analyzer applied, gate 12/12

## T-0008 — DONE

Polnyi perevod i audit v10-ch02: chislo blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0008-S1 | sma-a | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.sma-a.md` |
| T-0008-S2 | sma-b | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.sma-b.md` |
| T-0008-S3 | sma-c | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.sma-c.md` |
| T-0008-S4 | analyzer-phase1 | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.analyzer-phase1.md` |
| T-0008-S5 | analyzer-phase2 | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.analyzer-phase2.md` |

Заметки:
- T-0008-S1: SMA + Analyzer applied, gate 12/12
- T-0008-S2: SMA + Analyzer applied, gate 12/12
- T-0008-S3: SMA + Analyzer applied, gate 12/12
- T-0008-S4: SMA + Analyzer applied, gate 12/12
- T-0008-S5: SMA + Analyzer applied, gate 12/12

## T-0009 — DONE

Polnyi perevod i audit v10-ch03: 22 bloka po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0009-S1 | sma-a | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.sma-a.md` |
| T-0009-S2 | sma-b | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.sma-b.md` |
| T-0009-S3 | sma-c | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.sma-c.md` |
| T-0009-S4 | analyzer-phase1 | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.analyzer-phase1.md` |
| T-0009-S5 | analyzer-phase2 | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.analyzer-phase2.md` |

Заметки:
- T-0009-S1: SMA + Analyzer applied, gate 12/12
- T-0009-S2: SMA + Analyzer applied, gate 12/12
- T-0009-S3: SMA + Analyzer applied, gate 12/12
- T-0009-S4: SMA + Analyzer applied, gate 12/12
- T-0009-S5: SMA + Analyzer applied, gate 12/12

## T-0010 — DONE

Polnyi perevod i audit v10-ch04: 17 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0010-S1 | sma-a | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.sma-a.md` |
| T-0010-S2 | sma-b | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.sma-b.md` |
| T-0010-S3 | sma-c | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.sma-c.md` |
| T-0010-S4 | analyzer-phase1 | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.analyzer-phase1.md` |
| T-0010-S5 | analyzer-phase2 | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.analyzer-phase2.md` |

Заметки:
- T-0010-S1: SMA + Analyzer applied, gate 12/12
- T-0010-S2: SMA + Analyzer applied, gate 12/12
- T-0010-S3: SMA + Analyzer applied, gate 12/12
- T-0010-S4: SMA + Analyzer applied, gate 12/12
- T-0010-S5: SMA + Analyzer applied, gate 12/12

## T-0011 — DONE

Polnyi perevod i audit v10-ch05: chislo blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0011-S1 | sma-a | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.sma-a.md` |
| T-0011-S2 | sma-b | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.sma-b.md` |
| T-0011-S3 | sma-c | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.sma-c.md` |
| T-0011-S4 | analyzer-phase1 | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.analyzer-phase1.md` |
| T-0011-S5 | analyzer-phase2 | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.analyzer-phase2.md` |

Заметки:
- T-0011-S1: SMA + Analyzer applied, gate 12/12
- T-0011-S2: SMA + Analyzer applied, gate 12/12
- T-0011-S3: SMA + Analyzer applied, gate 12/12
- T-0011-S4: SMA + Analyzer applied, gate 12/12
- T-0011-S5: SMA + Analyzer applied, gate 12/12

## T-0012 — DONE

Polnyi perevod i audit v10-ch06: 17 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0012-S1 | sma-a | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.sma-a.md` |
| T-0012-S2 | sma-b | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.sma-b.md` |
| T-0012-S3 | sma-c | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.sma-c.md` |
| T-0012-S4 | analyzer-phase1 | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.analyzer-phase1.md` |
| T-0012-S5 | analyzer-phase2 | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.analyzer-phase2.md` |

Заметки:
- T-0012-S1: SMA + Analyzer applied, gate 12/12
- T-0012-S2: SMA + Analyzer applied, gate 12/12
- T-0012-S3: SMA + Analyzer applied, gate 12/12
- T-0012-S4: SMA + Analyzer applied, gate 12/12
- T-0012-S5: SMA + Analyzer applied, gate 12/12

## T-0013 — DONE

Polnyi perevod i audit v10-ch07: 15 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0013-S1 | sma-a | v10-ch07 | done | 3 | `agent_prompts/agent_prompt.v10-ch07.sma-a.attempt3.md` |
| T-0013-S2 | sma-b | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.sma-b.md` |
| T-0013-S3 | sma-c | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.sma-c.md` |
| T-0013-S4 | analyzer-phase1 | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.analyzer-phase1.md` |
| T-0013-S5 | analyzer-phase2 | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.analyzer-phase2.md` |

Заметки:
- T-0013-S1: SMA + Analyzer applied, gate 12/12
- T-0013-S2: SMA + Analyzer applied, gate 12/12
- T-0013-S3: SMA + Analyzer applied, gate 12/12
- T-0013-S4: SMA + Analyzer applied, gate 12/12
- T-0013-S5: SMA + Analyzer applied, gate 12/12

## T-0014 — DONE

Polnyi perevod i audit v10-ch08: 15 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0014-S1 | sma-a | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.sma-a.md` |
| T-0014-S2 | sma-b | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.sma-b.md` |
| T-0014-S3 | sma-c | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.sma-c.md` |
| T-0014-S4 | analyzer-phase1 | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.analyzer-phase1.md` |
| T-0014-S5 | analyzer-phase2 | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.analyzer-phase2.md` |

Заметки:
- T-0014-S1: SMA + Analyzer applied, gate 12/12
- T-0014-S2: SMA + Analyzer applied, gate 12/12
- T-0014-S3: SMA + Analyzer applied, gate 12/12
- T-0014-S4: SMA + Analyzer applied, gate 12/12
- T-0014-S5: SMA + Analyzer applied, gate 12/12

## T-0015 — DONE

Polnyi perevod i audit v10-ch09: 20 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0015-S1 | sma-a | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.sma-a.md` |
| T-0015-S2 | sma-b | v10-ch09 | done | 2 | `agent_prompts/agent_prompt.v10-ch09.sma-b.attempt2.md` |
| T-0015-S3 | sma-c | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.sma-c.md` |
| T-0015-S4 | analyzer-phase1 | v10-ch09 | done | 2 | `agent_prompts/agent_prompt.v10-ch09.analyzer-phase1.attempt2.md` |
| T-0015-S5 | analyzer-phase2 | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.analyzer-phase2.md` |

Заметки:
- T-0015-S1: SMA + Analyzer applied, gate 12/12
- T-0015-S2: SMA + Analyzer applied, gate 12/12
- T-0015-S3: SMA + Analyzer applied, gate 12/12
- T-0015-S4: SMA + Analyzer applied, gate 12/12
- T-0015-S5: SMA + Analyzer applied, gate 12/12

## T-0016 — DONE

Polnyi perevod i audit v10-ch10: 26 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0016-S1 | sma-a | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.sma-a.md` |
| T-0016-S2 | sma-b | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.sma-b.md` |
| T-0016-S3 | sma-c | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.sma-c.md` |
| T-0016-S4 | analyzer-phase1 | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.analyzer-phase1.md` |
| T-0016-S5 | analyzer-phase2 | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.analyzer-phase2.md` |

Заметки:
- T-0016-S1: SMA + Analyzer applied, gate 12/12
- T-0016-S2: SMA + Analyzer applied, gate 12/12
- T-0016-S3: SMA + Analyzer applied, gate 12/12
- T-0016-S4: SMA + Analyzer applied, gate 12/12
- T-0016-S5: SMA + Analyzer applied, gate 12/12

## T-0017 — DONE

Polnyi perevod i audit v10-epilogue: 9 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0017-S1 | sma-a | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.sma-a.md` |
| T-0017-S2 | sma-b | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.sma-b.md` |
| T-0017-S3 | sma-c | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.sma-c.md` |
| T-0017-S4 | analyzer-phase1 | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.analyzer-phase1.md` |
| T-0017-S5 | analyzer-phase2 | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.analyzer-phase2.md` |

Заметки:
- T-0017-S1: SMA + Analyzer applied, gate 12/12
- T-0017-S2: SMA + Analyzer applied, gate 12/12
- T-0017-S3: SMA + Analyzer applied, gate 12/12
- T-0017-S4: SMA + Analyzer applied, gate 12/12
- T-0017-S5: SMA + Analyzer applied, gate 12/12

## T-0018 — DONE

Polnyi perevod i audit v10-afterword: 2 bloka po JA, merge ED_RU v ruchnuyu, prefilytry, SMA A/B/C + Analyzer, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0018-S1 | sma-a | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.sma-a.md` |
| T-0018-S2 | sma-b | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.sma-b.md` |
| T-0018-S3 | sma-c | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.sma-c.md` |
| T-0018-S4 | analyzer-phase1 | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.analyzer-phase1.md` |
| T-0018-S5 | analyzer-phase2 | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.analyzer-phase2.md` |

Заметки:
- T-0018-S1: SMA + Analyzer applied, gate 12/12
- T-0018-S2: SMA + Analyzer applied, gate 12/12
- T-0018-S3: SMA + Analyzer applied, gate 12/12
- T-0018-S4: SMA + Analyzer applied, gate 12/12
- T-0018-S5: SMA + Analyzer applied, gate 12/12

## T-0019 — DONE

Polnyi perevod i audit v11-ch01: chislo blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0019-S1 | sma-a | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.sma-a.md` |
| T-0019-S2 | sma-b | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.sma-b.md` |
| T-0019-S3 | sma-c | v11-ch01 | done | 2 | `agent_prompts/agent_prompt.v11-ch01.sma-c.attempt2.md` |
| T-0019-S4 | analyzer-phase1 | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.analyzer-phase1.md` |
| T-0019-S5 | analyzer-phase2 | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.analyzer-phase2.md` |

Заметки:
- T-0019-S1: SMA + Analyzer applied, gate 12/12
- T-0019-S2: SMA + Analyzer applied, gate 12/12
- T-0019-S3: SMA + Analyzer applied, gate 12/12
- T-0019-S4: SMA + Analyzer applied, gate 12/12
- T-0019-S5: SMA + Analyzer applied, gate 12/12

## T-0020 — DONE

Polnyi perevod i audit v11-ch02: 10 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0020-S1 | sma-a | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.sma-a.md` |
| T-0020-S2 | sma-b | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.sma-b.md` |
| T-0020-S3 | sma-c | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.sma-c.md` |
| T-0020-S4 | analyzer-phase1 | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.analyzer-phase1.md` |
| T-0020-S5 | analyzer-phase2 | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.analyzer-phase2.md` |

Заметки:
- T-0020-S1: SMA + Analyzer applied, gate 12/12
- T-0020-S2: SMA + Analyzer applied, gate 12/12
- T-0020-S3: SMA + Analyzer applied, gate 12/12
- T-0020-S4: SMA + Analyzer applied, gate 12/12
- T-0020-S5: SMA + Analyzer applied, gate 12/12

## T-0021 — DONE

Polnyi perevod i audit v11-ch03: 11 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0021-S1 | sma-a | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.sma-a.md` |
| T-0021-S2 | sma-b | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.sma-b.md` |
| T-0021-S3 | sma-c | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.sma-c.md` |
| T-0021-S4 | analyzer-phase1 | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.analyzer-phase1.md` |
| T-0021-S5 | analyzer-phase2 | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.analyzer-phase2.md` |

Заметки:
- T-0021-S1: SMA + Analyzer applied, gate 12/12
- T-0021-S2: SMA + Analyzer applied, gate 12/12
- T-0021-S3: SMA + Analyzer applied, gate 12/12
- T-0021-S4: SMA + Analyzer applied, gate 12/12
- T-0021-S5: SMA + Analyzer applied, gate 12/12

## T-0022 — DONE

Polnyi perevod i audit v11-ch04: 31 blok po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0022-S1 | sma-a | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.sma-a.md` |
| T-0022-S2 | sma-b | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.sma-b.md` |
| T-0022-S3 | sma-c | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.sma-c.md` |
| T-0022-S4 | analyzer-phase1 | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.analyzer-phase1.md` |
| T-0022-S5 | analyzer-phase2 | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.analyzer-phase2.md` |

Заметки:
- T-0022-S1: SMA + Analyzer applied, gate 12/12
- T-0022-S2: SMA + Analyzer applied, gate 12/12
- T-0022-S3: SMA + Analyzer applied, gate 12/12
- T-0022-S4: SMA + Analyzer applied, gate 12/12
- T-0022-S5: SMA + Analyzer applied, gate 12/12

## T-0023 — DONE

Polnyi perevod i audit v11-ch05: 14 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0023-S1 | sma-a | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.sma-a.md` |
| T-0023-S2 | sma-b | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.sma-b.md` |
| T-0023-S3 | sma-c | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.sma-c.md` |
| T-0023-S4 | analyzer-phase1 | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.analyzer-phase1.md` |
| T-0023-S5 | analyzer-phase2 | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.analyzer-phase2.md` |

Заметки:
- T-0023-S1: SMA + Analyzer applied, gate 12/12
- T-0023-S2: SMA + Analyzer applied, gate 12/12
- T-0023-S3: SMA + Analyzer applied, gate 12/12
- T-0023-S4: SMA + Analyzer applied, gate 12/12
- T-0023-S5: SMA + Analyzer applied, gate 12/12

## T-0024 — DONE

Polnyi perevod i audit v11-ch06: 21 blok po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0024-S1 | sma-a | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.sma-a.md` |
| T-0024-S2 | sma-b | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.sma-b.md` |
| T-0024-S3 | sma-c | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.sma-c.md` |
| T-0024-S4 | analyzer-phase1 | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.analyzer-phase1.md` |
| T-0024-S5 | analyzer-phase2 | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.analyzer-phase2.md` |

Заметки:
- T-0024-S1: SMA + Analyzer applied, gate 12/12
- T-0024-S2: SMA + Analyzer applied, gate 12/12
- T-0024-S3: SMA + Analyzer applied, gate 12/12
- T-0024-S4: SMA + Analyzer applied, gate 12/12
- T-0024-S5: SMA + Analyzer applied, gate 12/12

## T-0025 — DONE

Polnyi perevod i audit v11-ch07: 9 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0025-S1 | sma-a | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.sma-a.md` |
| T-0025-S2 | sma-b | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.sma-b.md` |
| T-0025-S3 | sma-c | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.sma-c.md` |
| T-0025-S4 | analyzer-phase1 | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.analyzer-phase1.md` |
| T-0025-S5 | analyzer-phase2 | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.analyzer-phase2.md` |

Заметки:
- T-0025-S1: SMA + Analyzer applied, gate 12/12
- T-0025-S2: SMA + Analyzer applied, gate 12/12
- T-0025-S3: SMA + Analyzer applied, gate 12/12
- T-0025-S4: SMA + Analyzer applied, gate 12/12
- T-0025-S5: SMA + Analyzer applied, gate 12/12

## T-0026 — DONE

Polnyi perevod i audit v11-ch08: 19 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0026-S1 | sma-a | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.sma-a.md` |
| T-0026-S2 | sma-b | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.sma-b.md` |
| T-0026-S3 | sma-c | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.sma-c.md` |
| T-0026-S4 | analyzer-phase1 | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.analyzer-phase1.md` |
| T-0026-S5 | analyzer-phase2 | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.analyzer-phase2.md` |

Заметки:
- T-0026-S1: SMA + Analyzer applied, gate 12/12
- T-0026-S2: SMA + Analyzer applied, gate 12/12
- T-0026-S3: SMA + Analyzer applied, gate 12/12
- T-0026-S4: SMA + Analyzer applied, gate 12/12
- T-0026-S5: SMA + Analyzer applied, gate 12/12

## T-0027 — DONE

Polnyi perevod i audit v11-ch09: 21 blok po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0027-S1 | sma-a | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.sma-a.md` |
| T-0027-S2 | sma-b | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.sma-b.md` |
| T-0027-S3 | sma-c | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.sma-c.md` |
| T-0027-S4 | analyzer-phase1 | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.analyzer-phase1.md` |
| T-0027-S5 | analyzer-phase2 | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.analyzer-phase2.md` |

Заметки:
- T-0027-S1: SMA + Analyzer applied, gate 12/12
- T-0027-S2: SMA + Analyzer applied, gate 12/12
- T-0027-S3: SMA + Analyzer applied, gate 12/12
- T-0027-S4: SMA + Analyzer applied, gate 12/12
- T-0027-S5: SMA + Analyzer applied, gate 12/12

## T-0028 — DONE

Polnyi perevod i audit v11-ch10: 31 blok po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0028-S1 | sma-a | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.sma-a.md` |
| T-0028-S2 | sma-b | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.sma-b.md` |
| T-0028-S3 | sma-c | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.sma-c.md` |
| T-0028-S4 | analyzer-phase1 | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.analyzer-phase1.md` |
| T-0028-S5 | analyzer-phase2 | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.analyzer-phase2.md` |

Заметки:
- T-0028-S1: SMA + Analyzer applied, gate 12/12
- T-0028-S2: SMA + Analyzer applied, gate 12/12
- T-0028-S3: SMA + Analyzer applied, gate 12/12
- T-0028-S4: SMA + Analyzer applied, gate 12/12
- T-0028-S5: SMA + Analyzer applied, gate 12/12

## T-0029 — DONE

Polnyi perevod i audit v11-epilogue: 5 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0029-S1 | sma-a | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.sma-a.md` |
| T-0029-S2 | sma-b | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.sma-b.md` |
| T-0029-S3 | sma-c | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.sma-c.md` |
| T-0029-S4 | analyzer-phase1 | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.analyzer-phase1.md` |
| T-0029-S5 | analyzer-phase2 | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.analyzer-phase2.md` |

Заметки:
- T-0029-S1: SMA + Analyzer applied, gate 12/12
- T-0029-S2: SMA + Analyzer applied, gate 12/12
- T-0029-S3: SMA + Analyzer applied, gate 12/12
- T-0029-S4: SMA + Analyzer applied, gate 12/12
- T-0029-S5: SMA + Analyzer applied, gate 12/12

## T-0030 — DONE

Polnyi perevod i audit v11-afterword: 2 bloka po JA, ED_RU v merged vruchnuyu (net EN), prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0030-S1 | sma-a | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.sma-a.md` |
| T-0030-S2 | sma-b | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.sma-b.md` |
| T-0030-S3 | sma-c | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.sma-c.md` |
| T-0030-S4 | analyzer-phase1 | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.analyzer-phase1.md` |
| T-0030-S5 | analyzer-phase2 | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.analyzer-phase2.md` |

Заметки:
- T-0030-S1: SMA + Analyzer applied, gate 12/12
- T-0030-S2: SMA + Analyzer applied, gate 12/12
- T-0030-S3: SMA + Analyzer applied, gate 12/12
- T-0030-S4: SMA + Analyzer applied, gate 12/12
- T-0030-S5: SMA + Analyzer applied, gate 12/12

## T-0031 — DONE

Polnyi perevod i audit v12-prologue: 16 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0031-S1 | sma-a | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.sma-a.md` |
| T-0031-S2 | sma-b | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.sma-b.md` |
| T-0031-S3 | sma-c | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.sma-c.md` |
| T-0031-S4 | analyzer-phase1 | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.analyzer-phase1.md` |
| T-0031-S5 | analyzer-phase2 | v12-prologue | done | 2 | `agent_prompts/agent_prompt.v12-prologue.analyzer-phase2.attempt2.md` |

Заметки:
- T-0031-S1: SMA + Analyzer applied, gate 12/12
- T-0031-S2: SMA + Analyzer applied, gate 12/12
- T-0031-S3: SMA + Analyzer applied, gate 12/12
- T-0031-S4: SMA + Analyzer applied, gate 12/12
- T-0031-S5: SMA + Analyzer applied, gate 12/12

## T-0032 — DONE

Polnyi perevod i audit v12-ch01: 12 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0032-S1 | sma-a | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.sma-a.md` |
| T-0032-S2 | sma-b | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.sma-b.md` |
| T-0032-S3 | sma-c | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.sma-c.md` |
| T-0032-S4 | analyzer-phase1 | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.analyzer-phase1.md` |
| T-0032-S5 | analyzer-phase2 | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.analyzer-phase2.md` |

Заметки:
- T-0032-S1: SMA + Analyzer applied, gate 12/12
- T-0032-S2: SMA + Analyzer applied, gate 12/12
- T-0032-S3: SMA + Analyzer applied, gate 12/12
- T-0032-S4: SMA + Analyzer applied, gate 12/12
- T-0032-S5: SMA + Analyzer applied, gate 12/12

## T-0033 — DONE

Polnyi perevod i audit v12-ch02: 22 bloka po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0033-S1 | sma-a | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.sma-a.md` |
| T-0033-S2 | sma-b | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.sma-b.md` |
| T-0033-S3 | sma-c | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.sma-c.md` |
| T-0033-S4 | analyzer-phase1 | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.analyzer-phase1.md` |
| T-0033-S5 | analyzer-phase2 | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.analyzer-phase2.md` |

Заметки:
- T-0033-S1: SMA + Analyzer applied, gate 12/12
- T-0033-S2: SMA + Analyzer applied, gate 12/12
- T-0033-S3: SMA + Analyzer applied, gate 12/12
- T-0033-S4: SMA + Analyzer applied, gate 12/12
- T-0033-S5: SMA + Analyzer applied, gate 12/12

## T-0034 — DONE

Polnyi perevod i audit v12-ch04: 17 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0034-S1 | sma-a | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.sma-a.md` |
| T-0034-S2 | sma-b | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.sma-b.md` |
| T-0034-S3 | sma-c | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.sma-c.md` |
| T-0034-S4 | analyzer-phase1 | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.analyzer-phase1.md` |
| T-0034-S5 | analyzer-phase2 | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.analyzer-phase2.md` |

Заметки:
- T-0034-S1: SMA + Analyzer applied, gate 12/12
- T-0034-S2: SMA + Analyzer applied, gate 12/12
- T-0034-S3: SMA + Analyzer applied, gate 12/12
- T-0034-S4: SMA + Analyzer applied, gate 12/12
- T-0034-S5: SMA + Analyzer applied, gate 12/12

## T-0035 — DONE

Polnyi perevod i audit v12-ch05: 14 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0035-S1 | sma-a | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.sma-a.md` |
| T-0035-S2 | sma-b | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.sma-b.md` |
| T-0035-S3 | sma-c | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.sma-c.md` |
| T-0035-S4 | analyzer-phase1 | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.analyzer-phase1.md` |
| T-0035-S5 | analyzer-phase2 | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.analyzer-phase2.md` |

Заметки:
- T-0035-S1: SMA + Analyzer applied, gate 12/12
- T-0035-S2: SMA + Analyzer applied, gate 12/12
- T-0035-S3: SMA + Analyzer applied, gate 12/12
- T-0035-S4: SMA + Analyzer applied, gate 12/12
- T-0035-S5: SMA + Analyzer applied, gate 12/12

## T-0036 — DONE

Polnyi perevod i audit v12-ch07: 11 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0036-S1 | sma-a | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.sma-a.md` |
| T-0036-S2 | sma-b | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.sma-b.md` |
| T-0036-S3 | sma-c | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.sma-c.md` |
| T-0036-S4 | analyzer-phase1 | v12-ch07 | done | 2 | `agent_prompts/agent_prompt.v12-ch07.analyzer-phase1.attempt2.md` |
| T-0036-S5 | analyzer-phase2 | v12-ch07 | done | 3 | `agent_prompts/agent_prompt.v12-ch07.analyzer-phase2.attempt3.md` |

Заметки:
- T-0036-S1: SMA + Analyzer applied, gate 12/12
- T-0036-S2: SMA + Analyzer applied, gate 12/12
- T-0036-S3: SMA + Analyzer applied, gate 12/12
- T-0036-S4: SMA + Analyzer applied, gate 12/12
- T-0036-S5: SMA + Analyzer applied, gate 12/12

## T-0037 — DONE

Polnyi perevod i audit v12-ch08: 34 bloka po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0037-S1 | sma-a | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.sma-a.md` |
| T-0037-S2 | sma-b | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.sma-b.md` |
| T-0037-S3 | sma-c | v12-ch08 | done | 4 | `agent_prompts/agent_prompt.v12-ch08.sma-c.attempt4.md` |
| T-0037-S4 | analyzer-phase1 | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.analyzer-phase1.md` |
| T-0037-S5 | analyzer-phase2 | v12-ch08 | done | 2 | `agent_prompts/agent_prompt.v12-ch08.analyzer-phase2.attempt2.md` |

Заметки:
- T-0037-S1: SMA + Analyzer applied, gate 12/12
- T-0037-S2: SMA + Analyzer applied, gate 12/12
- T-0037-S3: SMA + Analyzer applied, gate 12/12
- T-0037-S4: SMA + Analyzer applied, gate 12/12
- T-0037-S5: SMA + Analyzer applied, gate 12/12

## T-0038 — DONE

Polnyi perevod i audit v12-afterword: 3 bloka po JA, ED_RU v merged vruchnuyu, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0038-S1 | sma-a | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.sma-a.md` |
| T-0038-S2 | sma-b | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.sma-b.md` |
| T-0038-S3 | sma-c | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.sma-c.md` |
| T-0038-S4 | analyzer-phase1 | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.analyzer-phase1.md` |
| T-0038-S5 | analyzer-phase2 | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.analyzer-phase2.md` |

Заметки:
- T-0038-S1: SMA + Analyzer applied, gate 12/12
- T-0038-S2: SMA + Analyzer applied, gate 12/12
- T-0038-S3: SMA + Analyzer applied, gate 12/12
- T-0038-S4: SMA + Analyzer applied, gate 12/12
- T-0038-S5: SMA + Analyzer applied, gate 12/12

## T-0039 — DONE

Polnyi perevod i audit v13-ch01: 15 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0039-S1 | sma-a | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.sma-a.md` |
| T-0039-S2 | sma-b | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.sma-b.md` |
| T-0039-S3 | sma-c | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.sma-c.md` |
| T-0039-S4 | analyzer-phase1 | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.analyzer-phase1.md` |
| T-0039-S5 | analyzer-phase2 | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.analyzer-phase2.md` |

Заметки:
- T-0039-S1: SMA + Analyzer applied, gate 12/12
- T-0039-S2: SMA + Analyzer applied, gate 12/12
- T-0039-S3: SMA + Analyzer applied, gate 12/12
- T-0039-S4: SMA + Analyzer applied, gate 12/12
- T-0039-S5: SMA + Analyzer applied, gate 12/12

## T-0040 — DONE

Polnyi perevod i audit v13-ch02: 38 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0040-S1 | sma-a | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.sma-a.md` |
| T-0040-S2 | sma-b | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.sma-b.md` |
| T-0040-S3 | sma-c | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.sma-c.md` |
| T-0040-S4 | analyzer-phase1 | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.analyzer-phase1.md` |
| T-0040-S5 | analyzer-phase2 | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.analyzer-phase2.md` |

Заметки:
- T-0040-S1: SMA + Analyzer applied, gate 12/12
- T-0040-S2: SMA + Analyzer applied, gate 12/12
- T-0040-S3: SMA + Analyzer applied, gate 12/12
- T-0040-S4: SMA + Analyzer applied, gate 12/12
- T-0040-S5: SMA + Analyzer applied, gate 12/12

## T-0041 — DONE

Polnyi perevod i audit v13-ch03: 13 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0041-S1 | sma-a | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.sma-a.md` |
| T-0041-S2 | sma-b | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.sma-b.md` |
| T-0041-S3 | sma-c | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.sma-c.md` |
| T-0041-S4 | analyzer-phase1 | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.analyzer-phase1.md` |
| T-0041-S5 | analyzer-phase2 | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.analyzer-phase2.md` |

Заметки:
- T-0041-S1: SMA + Analyzer applied, gate 12/12
- T-0041-S2: SMA + Analyzer applied, gate 12/12
- T-0041-S3: SMA + Analyzer applied, gate 12/12
- T-0041-S4: SMA + Analyzer applied, gate 12/12
- T-0041-S5: SMA + Analyzer applied, gate 12/12

## T-0042 — DONE

Polnyi perevod i audit v13-ch04: 24 bloka po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0042-S1 | sma-a | v13-ch04 | done | 2 | `agent_prompts/agent_prompt.v13-ch04.sma-a.attempt2.md` |
| T-0042-S2 | sma-b | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.sma-b.md` |
| T-0042-S3 | sma-c | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.sma-c.md` |
| T-0042-S4 | analyzer-phase1 | v13-ch04 | done | 3 | `agent_prompts/agent_prompt.v13-ch04.analyzer-phase1.attempt3.md` |
| T-0042-S5 | analyzer-phase2 | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.analyzer-phase2.md` |

Заметки:
- T-0042-S1: SMA + Analyzer applied, gate 12/12
- T-0042-S2: SMA + Analyzer applied, gate 12/12
- T-0042-S3: SMA + Analyzer applied, gate 12/12
- T-0042-S4: SMA + Analyzer applied, gate 12/12
- T-0042-S5: SMA + Analyzer applied, gate 12/12

## T-0043 — DONE

Polnyi perevod i audit v13-ch05: 13 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0043-S1 | sma-a | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.sma-a.md` |
| T-0043-S2 | sma-b | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.sma-b.md` |
| T-0043-S3 | sma-c | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.sma-c.md` |
| T-0043-S4 | analyzer-phase1 | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.analyzer-phase1.md` |
| T-0043-S5 | analyzer-phase2 | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.analyzer-phase2.md` |

Заметки:
- T-0043-S1: SMA + Analyzer applied, gate 12/12
- T-0043-S2: SMA + Analyzer applied, gate 12/12
- T-0043-S3: SMA + Analyzer applied, gate 12/12
- T-0043-S4: SMA + Analyzer applied, gate 12/12
- T-0043-S5: SMA + Analyzer applied, gate 12/12

## T-0044 — DONE

Polnyi perevod i audit v13-ch06: 14 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0044-S1 | sma-a | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.sma-a.md` |
| T-0044-S2 | sma-b | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.sma-b.md` |
| T-0044-S3 | sma-c | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.sma-c.md` |
| T-0044-S4 | analyzer-phase1 | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.analyzer-phase1.md` |
| T-0044-S5 | analyzer-phase2 | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.analyzer-phase2.md` |

Заметки:
- T-0044-S1: SMA + Analyzer applied, gate 12/12
- T-0044-S2: SMA + Analyzer applied, gate 12/12
- T-0044-S3: SMA + Analyzer applied, gate 12/12
- T-0044-S4: SMA + Analyzer applied, gate 12/12
- T-0044-S5: SMA + Analyzer applied, gate 12/12

## T-0045 — DONE

Polnyi perevod i audit v13-ch07: 24 bloka po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0045-S1 | sma-a | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.sma-a.md` |
| T-0045-S2 | sma-b | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.sma-b.md` |
| T-0045-S3 | sma-c | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.sma-c.md` |
| T-0045-S4 | analyzer-phase1 | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.analyzer-phase1.md` |
| T-0045-S5 | analyzer-phase2 | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.analyzer-phase2.md` |

Заметки:
- T-0045-S1: SMA + Analyzer applied, gate 12/12
- T-0045-S2: SMA + Analyzer applied, gate 12/12
- T-0045-S3: SMA + Analyzer applied, gate 12/12
- T-0045-S4: SMA + Analyzer applied, gate 12/12
- T-0045-S5: SMA + Analyzer applied, gate 12/12

## T-0046 — DONE

Polnyi perevod i audit v13-ch08: 12 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0046-S1 | sma-a | v13-ch08 | done | 2 | `agent_prompts/agent_prompt.v13-ch08.sma-a.attempt2.md` |
| T-0046-S2 | sma-b | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.sma-b.md` |
| T-0046-S3 | sma-c | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.sma-c.md` |
| T-0046-S4 | analyzer-phase1 | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.analyzer-phase1.md` |
| T-0046-S5 | analyzer-phase2 | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.analyzer-phase2.md` |

Заметки:
- T-0046-S1: SMA + Analyzer applied, gate 12/12
- T-0046-S2: SMA + Analyzer applied, gate 12/12
- T-0046-S3: SMA + Analyzer applied, gate 12/12
- T-0046-S4: SMA + Analyzer applied, gate 12/12
- T-0046-S5: SMA + Analyzer applied, gate 12/12

## T-0047 — DONE

Polnyi perevod i audit v13-epilogue: 8 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0047-S1 | sma-a | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.sma-a.md` |
| T-0047-S2 | sma-b | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.sma-b.md` |
| T-0047-S3 | sma-c | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.sma-c.md` |
| T-0047-S4 | analyzer-phase1 | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.analyzer-phase1.md` |
| T-0047-S5 | analyzer-phase2 | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.analyzer-phase2.md` |

Заметки:
- T-0047-S1: SMA + Analyzer applied, gate 12/12
- T-0047-S2: SMA + Analyzer applied, gate 12/12
- T-0047-S3: SMA + Analyzer applied, gate 12/12
- T-0047-S4: SMA + Analyzer applied, gate 12/12
- T-0047-S5: SMA + Analyzer applied, gate 12/12

## T-0048 — DONE

Polnyi perevod i audit v13-afterword: 2 bloka po JA, ED_RU v merged vruchnuyu, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0048-S1 | sma-a | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.sma-a.md` |
| T-0048-S2 | sma-b | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.sma-b.md` |
| T-0048-S3 | sma-c | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.sma-c.md` |
| T-0048-S4 | analyzer-phase1 | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.analyzer-phase1.md` |
| T-0048-S5 | analyzer-phase2 | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.analyzer-phase2.md` |

Заметки:
- T-0048-S1: SMA + Analyzer applied, gate 12/12
- T-0048-S2: SMA + Analyzer applied, gate 12/12
- T-0048-S3: SMA + Analyzer applied, gate 12/12
- T-0048-S4: SMA + Analyzer applied, gate 12/12
- T-0048-S5: SMA + Analyzer applied, gate 12/12

## T-0049 — DONE

Polnyi perevod i audit v15-ch01: 19 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0049-S1 | sma-a | v15-ch01 | done | 1 | `agent_prompts/agent_prompt.v15-ch01.sma-a.md` |
| T-0049-S2 | sma-b | v15-ch01 | done | 1 | `agent_prompts/agent_prompt.v15-ch01.sma-b.md` |
| T-0049-S3 | sma-c | v15-ch01 | done | 1 | `agent_prompts/agent_prompt.v15-ch01.sma-c.md` |
| T-0049-S4 | analyzer-phase1 | v15-ch01 | done | 1 | `agent_prompts/agent_prompt.v15-ch01.analyzer-phase1.md` |
| T-0049-S5 | analyzer-phase2 | v15-ch01 | done | 1 | `agent_prompts/agent_prompt.v15-ch01.analyzer-phase2.md` |

Заметки:
- T-0049-S1: SMA + Analyzer applied, gate 12/12
- T-0049-S2: SMA + Analyzer applied, gate 12/12
- T-0049-S3: SMA + Analyzer applied, gate 12/12
- T-0049-S4: SMA + Analyzer applied, gate 12/12
- T-0049-S5: SMA + Analyzer applied, gate 12/12

## T-0050 — DONE

Polnyi perevod i audit v15-ch02: 21 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0050-S1 | sma-a | v15-ch02 | done | 1 | `agent_prompts/agent_prompt.v15-ch02.sma-a.md` |
| T-0050-S2 | sma-b | v15-ch02 | done | 1 | `agent_prompts/agent_prompt.v15-ch02.sma-b.md` |
| T-0050-S3 | sma-c | v15-ch02 | done | 1 | `agent_prompts/agent_prompt.v15-ch02.sma-c.md` |
| T-0050-S4 | analyzer-phase1 | v15-ch02 | done | 1 | `agent_prompts/agent_prompt.v15-ch02.analyzer-phase1.md` |
| T-0050-S5 | analyzer-phase2 | v15-ch02 | done | 1 | `agent_prompts/agent_prompt.v15-ch02.analyzer-phase2.md` |

Заметки:
- T-0050-S1: SMA + Analyzer applied, gate 12/12
- T-0050-S2: SMA + Analyzer applied, gate 12/12
- T-0050-S3: SMA + Analyzer applied, gate 12/12
- T-0050-S4: SMA + Analyzer applied, gate 12/12
- T-0050-S5: SMA + Analyzer applied, gate 12/12

## T-0051 — DONE

Polnyi perevod i audit v15-ch03: 16 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0051-S1 | sma-a | v15-ch03 | done | 1 | `agent_prompts/agent_prompt.v15-ch03.sma-a.md` |
| T-0051-S2 | sma-b | v15-ch03 | done | 1 | `agent_prompts/agent_prompt.v15-ch03.sma-b.md` |
| T-0051-S3 | sma-c | v15-ch03 | done | 1 | `agent_prompts/agent_prompt.v15-ch03.sma-c.md` |
| T-0051-S4 | analyzer-phase1 | v15-ch03 | done | 1 | `agent_prompts/agent_prompt.v15-ch03.analyzer-phase1.md` |
| T-0051-S5 | analyzer-phase2 | v15-ch03 | done | 1 | `agent_prompts/agent_prompt.v15-ch03.analyzer-phase2.md` |

Заметки:
- T-0051-S1: SMA + Analyzer applied, gate 12/12
- T-0051-S2: SMA + Analyzer applied, gate 12/12
- T-0051-S3: SMA + Analyzer applied, gate 12/12
- T-0051-S4: SMA + Analyzer applied, gate 12/12
- T-0051-S5: SMA + Analyzer applied, gate 12/12

## T-0052 — DONE

Polnyi perevod i audit v15-ch04: 13 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0052-S1 | sma-a | v15-ch04 | done | 1 | `agent_prompts/agent_prompt.v15-ch04.sma-a.md` |
| T-0052-S2 | sma-b | v15-ch04 | done | 1 | `agent_prompts/agent_prompt.v15-ch04.sma-b.md` |
| T-0052-S3 | sma-c | v15-ch04 | done | 1 | `agent_prompts/agent_prompt.v15-ch04.sma-c.md` |
| T-0052-S4 | analyzer-phase1 | v15-ch04 | done | 1 | `agent_prompts/agent_prompt.v15-ch04.analyzer-phase1.md` |
| T-0052-S5 | analyzer-phase2 | v15-ch04 | done | 1 | `agent_prompts/agent_prompt.v15-ch04.analyzer-phase2.md` |

Заметки:
- T-0052-S1: SMA + Analyzer applied, gate 12/12
- T-0052-S2: SMA + Analyzer applied, gate 12/12
- T-0052-S3: SMA + Analyzer applied, gate 12/12
- T-0052-S4: SMA + Analyzer applied, gate 12/12
- T-0052-S5: SMA + Analyzer applied, gate 12/12

## T-0053 — DONE

Polnyi perevod i audit v15-ch05: 21 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0053-S1 | sma-a | v15-ch05 | done | 1 | `agent_prompts/agent_prompt.v15-ch05.sma-a.md` |
| T-0053-S2 | sma-b | v15-ch05 | done | 1 | `agent_prompts/agent_prompt.v15-ch05.sma-b.md` |
| T-0053-S3 | sma-c | v15-ch05 | done | 1 | `agent_prompts/agent_prompt.v15-ch05.sma-c.md` |
| T-0053-S4 | analyzer-phase1 | v15-ch05 | done | 1 | `agent_prompts/agent_prompt.v15-ch05.analyzer-phase1.md` |
| T-0053-S5 | analyzer-phase2 | v15-ch05 | done | 1 | `agent_prompts/agent_prompt.v15-ch05.analyzer-phase2.md` |

Заметки:
- T-0053-S1: SMA + Analyzer applied, gate 12/12
- T-0053-S2: SMA + Analyzer applied, gate 12/12
- T-0053-S3: SMA + Analyzer applied, gate 12/12
- T-0053-S4: SMA + Analyzer applied, gate 12/12
- T-0053-S5: SMA + Analyzer applied, gate 12/12

## T-0054 — DONE

Polnyi perevod i audit v15-ch06: 6 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0054-S1 | sma-a | v15-ch06 | done | 1 | `agent_prompts/agent_prompt.v15-ch06.sma-a.md` |
| T-0054-S2 | sma-b | v15-ch06 | done | 1 | `agent_prompts/agent_prompt.v15-ch06.sma-b.md` |
| T-0054-S3 | sma-c | v15-ch06 | done | 1 | `agent_prompts/agent_prompt.v15-ch06.sma-c.md` |
| T-0054-S4 | analyzer-phase1 | v15-ch06 | done | 1 | `agent_prompts/agent_prompt.v15-ch06.analyzer-phase1.md` |
| T-0054-S5 | analyzer-phase2 | v15-ch06 | done | 1 | `agent_prompts/agent_prompt.v15-ch06.analyzer-phase2.md` |

Заметки:
- T-0054-S1: SMA + Analyzer applied, gate 12/12
- T-0054-S2: SMA + Analyzer applied, gate 12/12
- T-0054-S3: SMA + Analyzer applied, gate 12/12
- T-0054-S4: SMA + Analyzer applied, gate 12/12
- T-0054-S5: SMA + Analyzer applied, gate 12/12

## T-0055 — DONE

Polnyi perevod i audit v15-ch07: 24 bloka po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0055-S1 | sma-a | v15-ch07 | done | 1 | `agent_prompts/agent_prompt.v15-ch07.sma-a.md` |
| T-0055-S2 | sma-b | v15-ch07 | done | 1 | `agent_prompts/agent_prompt.v15-ch07.sma-b.md` |
| T-0055-S3 | sma-c | v15-ch07 | done | 1 | `agent_prompts/agent_prompt.v15-ch07.sma-c.md` |
| T-0055-S4 | analyzer-phase1 | v15-ch07 | done | 1 | `agent_prompts/agent_prompt.v15-ch07.analyzer-phase1.md` |
| T-0055-S5 | analyzer-phase2 | v15-ch07 | done | 1 | `agent_prompts/agent_prompt.v15-ch07.analyzer-phase2.md` |

Заметки:
- T-0055-S1: SMA + Analyzer applied, gate 12/12
- T-0055-S2: SMA + Analyzer applied, gate 12/12
- T-0055-S3: SMA + Analyzer applied, gate 12/12
- T-0055-S4: SMA + Analyzer applied, gate 12/12
- T-0055-S5: SMA + Analyzer applied, gate 12/12

## T-0056 — DONE

Polnyi perevod i audit v15-ch08: po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0056-S1 | sma-a | v15-ch08 | done | 1 | `agent_prompts/agent_prompt.v15-ch08.sma-a.md` |
| T-0056-S2 | sma-b | v15-ch08 | done | 1 | `agent_prompts/agent_prompt.v15-ch08.sma-b.md` |
| T-0056-S3 | sma-c | v15-ch08 | done | 1 | `agent_prompts/agent_prompt.v15-ch08.sma-c.md` |
| T-0056-S4 | analyzer-phase1 | v15-ch08 | done | 1 | `agent_prompts/agent_prompt.v15-ch08.analyzer-phase1.md` |
| T-0056-S5 | analyzer-phase2 | v15-ch08 | done | 1 | `agent_prompts/agent_prompt.v15-ch08.analyzer-phase2.md` |

Заметки:
- T-0056-S1: SMA + Analyzer applied, gate 12/12
- T-0056-S2: SMA + Analyzer applied, gate 12/12
- T-0056-S3: SMA + Analyzer applied, gate 12/12
- T-0056-S4: SMA + Analyzer applied, gate 12/12
- T-0056-S5: SMA + Analyzer applied, gate 12/12

## T-0057 — DONE

Polnyi perevod i audit v15-ch09: 23 bloka po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0057-S1 | sma-a | v15-ch09 | done | 1 | `agent_prompts/agent_prompt.v15-ch09.sma-a.md` |
| T-0057-S2 | sma-b | v15-ch09 | done | 1 | `agent_prompts/agent_prompt.v15-ch09.sma-b.md` |
| T-0057-S3 | sma-c | v15-ch09 | done | 1 | `agent_prompts/agent_prompt.v15-ch09.sma-c.md` |
| T-0057-S4 | analyzer-phase1 | v15-ch09 | done | 1 | `agent_prompts/agent_prompt.v15-ch09.analyzer-phase1.md` |
| T-0057-S5 | analyzer-phase2 | v15-ch09 | done | 1 | `agent_prompts/agent_prompt.v15-ch09.analyzer-phase2.md` |

Заметки:
- T-0057-S1: SMA + Analyzer applied, gate 12/12
- T-0057-S2: SMA + Analyzer applied, gate 12/12
- T-0057-S3: SMA + Analyzer applied, gate 12/12
- T-0057-S4: SMA + Analyzer applied, gate 12/12
- T-0057-S5: SMA + Analyzer applied, gate 12/12

## T-0058 — DONE

Polnyi perevod i audit v15-epilogue: 7 blokov po JA, prefilytry, SMA A/B/C + Analyzer 1/2, otchet, gate 12/12, commit

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0058-S1 | sma-a | v15-epilogue | done | 1 | `agent_prompts/agent_prompt.v15-epilogue.sma-a.md` |
| T-0058-S2 | sma-b | v15-epilogue | done | 1 | `agent_prompts/agent_prompt.v15-epilogue.sma-b.md` |
| T-0058-S3 | sma-c | v15-epilogue | done | 1 | `agent_prompts/agent_prompt.v15-epilogue.sma-c.md` |
| T-0058-S4 | analyzer-phase1 | v15-epilogue | done | 1 | `agent_prompts/agent_prompt.v15-epilogue.analyzer-phase1.md` |
| T-0058-S5 | analyzer-phase2 | v15-epilogue | done | 1 | `agent_prompts/agent_prompt.v15-epilogue.analyzer-phase2.md` |

Заметки:
- T-0058-S1: SMA + Analyzer applied, gate 12/12
- T-0058-S2: SMA + Analyzer applied, gate 12/12
- T-0058-S3: SMA + Analyzer applied, gate 12/12
- T-0058-S4: SMA + Analyzer applied, gate 12/12
- T-0058-S5: SMA + Analyzer applied, gate 12/12

## T-0059 — OPEN

Перепроверка томов 7-13 — проход seed=s20261118-dea28e (полный аудит по главам)

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0059-S1 | full-audit | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.full-audit.md` |
| T-0059-S2 | full-audit | v07-ch01 | done | 2 | `agent_prompts/agent_prompt.v07-ch01.full-audit.attempt2.md` |
| T-0059-S3 | full-audit | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.full-audit.md` |
| T-0059-S4 | full-audit | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.full-audit.md` |
| T-0059-S5 | full-audit | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.full-audit.md` |
| T-0059-S6 | full-audit | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.full-audit.md` |
| T-0059-S7 | full-audit | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.full-audit.md` |
| T-0059-S8 | full-audit | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.full-audit.md` |
| T-0059-S9 | full-audit | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.full-audit.md` |
| T-0059-S10 | full-audit | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.full-audit.md` |
| T-0059-S11 | full-audit | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.full-audit.md` |
| T-0059-S12 | full-audit | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.full-audit.md` |
| T-0059-S13 | full-audit | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.full-audit.md` |
| T-0059-S14 | full-audit | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.full-audit.md` |
| T-0059-S15 | full-audit | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.full-audit.md` |
| T-0059-S16 | full-audit | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.full-audit.md` |
| T-0059-S17 | full-audit | v08-ch04 | done | 2 | `agent_prompts/agent_prompt.v08-ch04.full-audit.attempt2.md` |
| T-0059-S18 | full-audit | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.full-audit.md` |
| T-0059-S19 | full-audit | v08-ch06 | done | 2 | `agent_prompts/agent_prompt.v08-ch06.full-audit.attempt2.md` |
| T-0059-S20 | full-audit | v08-ch07 | done | 2 | `agent_prompts/agent_prompt.v08-ch07.full-audit.attempt2.md` |
| T-0059-S21 | full-audit | v08-ch08 | done | 2 | `agent_prompts/agent_prompt.v08-ch08.full-audit.attempt2.md` |
| T-0059-S22 | full-audit | v08-ch09 | done | 2 | `agent_prompts/agent_prompt.v08-ch09.full-audit.attempt2.md` |
| T-0059-S23 | full-audit | v08-ch10 | done | 2 | `agent_prompts/agent_prompt.v08-ch10.full-audit.attempt2.md` |
| T-0059-S24 | full-audit | v08-epilogue | done | 2 | `agent_prompts/agent_prompt.v08-epilogue.full-audit.attempt2.md` |
| T-0059-S25 | full-audit | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.full-audit.md` |
| T-0059-S26 | full-audit | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.full-audit.md` |
| T-0059-S27 | full-audit | v09-ch02 | done | 2 | `agent_prompts/agent_prompt.v09-ch02.full-audit.attempt2.md` |
| T-0059-S28 | full-audit | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.full-audit.md` |
| T-0059-S29 | full-audit | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.full-audit.md` |
| T-0059-S30 | full-audit | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.full-audit.md` |
| T-0059-S31 | full-audit | v09-ch06 | done | 2 | `agent_prompts/agent_prompt.v09-ch06.full-audit.attempt2.md` |
| T-0059-S32 | full-audit | v09-ch07 | done | 2 | `agent_prompts/agent_prompt.v09-ch07.full-audit.attempt2.md` |
| T-0059-S33 | full-audit | v09-ch08 | done | 2 | `agent_prompts/agent_prompt.v09-ch08.full-audit.attempt2.md` |
| T-0059-S34 | full-audit | v09-ch09 | done | 2 | `agent_prompts/agent_prompt.v09-ch09.full-audit.attempt2.md` |
| T-0059-S35 | full-audit | v09-epilogue | done | 2 | `agent_prompts/agent_prompt.v09-epilogue.full-audit.attempt2.md` |
| T-0059-S36 | full-audit | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.full-audit.md` |
| T-0059-S37 | full-audit | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.full-audit.md` |
| T-0059-S38 | full-audit | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.full-audit.md` |
| T-0059-S39 | full-audit | v10-ch03 | done | 2 | `agent_prompts/agent_prompt.v10-ch03.full-audit.attempt2.md` |
| T-0059-S40 | full-audit | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.full-audit.md` |
| T-0059-S41 | full-audit | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.full-audit.md` |
| T-0059-S42 | full-audit | v10-ch06 | done | 2 | `agent_prompts/agent_prompt.v10-ch06.full-audit.attempt2.md` |
| T-0059-S43 | full-audit | v10-ch07 | done | 2 | `agent_prompts/agent_prompt.v10-ch07.full-audit.attempt2.md` |
| T-0059-S44 | full-audit | v10-ch08 | done | 2 | `agent_prompts/agent_prompt.v10-ch08.full-audit.attempt2.md` |
| T-0059-S45 | full-audit | v10-ch09 | done | 2 | `agent_prompts/agent_prompt.v10-ch09.full-audit.attempt2.md` |
| T-0059-S46 | full-audit | v10-ch10 | done | 2 | `agent_prompts/agent_prompt.v10-ch10.full-audit.attempt2.md` |
| T-0059-S47 | full-audit | v10-epilogue | done | 2 | `agent_prompts/agent_prompt.v10-epilogue.full-audit.attempt2.md` |
| T-0059-S48 | full-audit | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.full-audit.md` |
| T-0059-S49 | full-audit | v11-ch01 | done | 2 | `agent_prompts/agent_prompt.v11-ch01.full-audit.attempt2.md` |
| T-0059-S50 | full-audit | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.full-audit.md` |
| T-0059-S51 | full-audit | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.full-audit.md` |
| T-0059-S52 | full-audit | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.full-audit.md` |
| T-0059-S53 | full-audit | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.full-audit.md` |
| T-0059-S54 | full-audit | v11-ch06 | done | 2 | `agent_prompts/agent_prompt.v11-ch06.full-audit.attempt2.md` |
| T-0059-S55 | full-audit | v11-ch07 | done | 2 | `agent_prompts/agent_prompt.v11-ch07.full-audit.attempt2.md` |
| T-0059-S56 | full-audit | v11-ch08 | done | 2 | `agent_prompts/agent_prompt.v11-ch08.full-audit.attempt2.md` |
| T-0059-S57 | full-audit | v11-ch09 | done | 2 | `agent_prompts/agent_prompt.v11-ch09.full-audit.attempt2.md` |
| T-0059-S58 | full-audit | v11-ch10 | done | 2 | `agent_prompts/agent_prompt.v11-ch10.full-audit.attempt2.md` |
| T-0059-S59 | full-audit | v11-epilogue | done | 2 | `agent_prompts/agent_prompt.v11-epilogue.full-audit.attempt2.md` |
| T-0059-S60 | full-audit | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.full-audit.md` |
| T-0059-S61 | full-audit | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.full-audit.md` |
| T-0059-S62 | full-audit | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.full-audit.md` |
| T-0059-S63 | full-audit | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.full-audit.md` |
| T-0059-S64 | full-audit | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.full-audit.md` |
| T-0059-S65 | full-audit | v13-ch05 | done | 2 | `agent_prompts/agent_prompt.v13-ch05.full-audit.attempt2.md` |
| T-0059-S66 | full-audit | v13-ch06 | done | 2 | `agent_prompts/agent_prompt.v13-ch06.full-audit.attempt2.md` |
| T-0059-S67 | full-audit | v13-ch07 | done | 2 | `agent_prompts/agent_prompt.v13-ch07.full-audit.attempt2.md` |
| T-0059-S68 | full-audit | v13-ch08 | interrupted | 3 | `agent_prompts/agent_prompt.v13-ch08.full-audit.attempt3.md` |
| T-0059-S69 | full-audit | v13-epilogue | done | 2 | `agent_prompts/agent_prompt.v13-epilogue.full-audit.attempt2.md` |
| T-0059-S70 | full-audit | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.full-audit.md` |
| T-0059-S71 | full-audit | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.full-audit.md` |
| T-0059-S72 | full-audit | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.full-audit.md` |
| T-0059-S73 | full-audit | v12-ch02 | done | 2 | `agent_prompts/agent_prompt.v12-ch02.full-audit.attempt2.md` |
| T-0059-S74 | full-audit | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.full-audit.md` |
| T-0059-S75 | full-audit | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.full-audit.md` |
| T-0059-S76 | full-audit | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.full-audit.md` |
| T-0059-S77 | full-audit | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.full-audit.md` |

Заметки:
- T-0059-S1: seed=s20261118-dea28e: полный аудит, 0 правок текста, отчёт обновлён, коммит не выполнялся
- T-0059-S2: seed=s20261118-dea28e: полный аудит, вердикты зафиксированы, коммит не делался
- T-0059-S3: seed=s20261118-dea28e: 2 FIXED (латиница T, согласование), отчёт/лог обновлены, коммит не делался
- T-0059-S4: seed=s20261118-dea28e: 5 FIXED, канон 'зверо-люди' восстановлен, коммит не делался
- T-0059-S5: seed=s20261118-dea28e: 5 FIXED, коммит не делался
- T-0059-S6: seed=s20261118-dea28e: 1 FIXED (баллиста), коммит не делался
- T-0059-S7: seed=s20261118-dea28e: 2 FIXED, gate 12/12, коммит не делался
- T-0059-S8: seed=s20261118-dea28e: полный аудит, вердикты зафиксированы, коммит не делался
- T-0059-S9: seed=s20261118-dea28e: полный аудит, вердикты зафиксированы, коммит не делался
- T-0059-S10: seed=s20261118-dea28e: полный аудит, вердикты зафиксированы, коммит не делался
- T-0059-S11: seed=s20261118-dea28e: полный аудит, вердикты зафиксированы, коммит не делался
- T-0059-S12: seed=s20261118-dea28e: полный аудит, вердикты зафиксированы, коммит не делался
- T-0059-S13: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S14: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S15: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S16: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S17: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S18: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S19: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S20: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S21: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S22: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S23: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S24: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S25: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S26: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S27: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S28: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S29: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S30: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S31: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S32: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S33: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S34: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S35: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S36: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S37: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S38: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S39: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S40: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S41: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S42: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S43: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S44: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S45: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S46: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S47: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S48: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S49: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S50: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S51: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S52: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S53: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, коммит не делался
- T-0059-S54: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S55: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S56: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S57: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S58: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S59: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S60: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S61: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S62: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S63: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S64: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S65: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S66: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S67: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S68: изменений после запуска нет
- T-0059-S69: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S70: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S71: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S72: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S73: seed=s20261118-dea28e: полный аудит, 10 FIXED, gate 12/12, мусор в отчёте убран, коммит не делался
- T-0059-S74: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S75: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S76: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался
- T-0059-S77: seed=s20261118-dea28e: полный аудит, FIXED зафиксированы, gate 12/12, коммит не делался

## T-0060 — DONE

Проверка 1 — микро-семантика (Semantic Audit A), тома 7-13, раунд smaA-20261118

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0060-S1 | sma-a | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.sma-a.md` |
| T-0060-S2 | analyzer-phase1 | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.analyzer-phase1.md` |
| T-0060-S3 | analyzer-phase2 | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.analyzer-phase2.md` |
| T-0060-S4 | sma-a | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.sma-a.md` |
| T-0060-S5 | analyzer-phase1 | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.analyzer-phase1.md` |
| T-0060-S6 | analyzer-phase2 | v07-ch01 | done | 3 | `agent_prompts/agent_prompt.v07-ch01.analyzer-phase2.attempt3.md` |
| T-0060-S7 | sma-a | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.sma-a.md` |
| T-0060-S8 | analyzer-phase1 | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.analyzer-phase1.md` |
| T-0060-S9 | analyzer-phase2 | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.analyzer-phase2.md` |
| T-0060-S10 | sma-a | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.sma-a.md` |
| T-0060-S11 | analyzer-phase1 | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.analyzer-phase1.md` |
| T-0060-S12 | analyzer-phase2 | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.analyzer-phase2.md` |
| T-0060-S13 | sma-a | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.sma-a.md` |
| T-0060-S14 | analyzer-phase1 | v07-ch04 | done | 2 | `agent_prompts/agent_prompt.v07-ch04.analyzer-phase1.attempt2.md` |
| T-0060-S15 | analyzer-phase2 | v07-ch04 | done | 2 | `agent_prompts/agent_prompt.v07-ch04.analyzer-phase2.attempt2.md` |
| T-0060-S16 | sma-a | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.sma-a.md` |
| T-0060-S17 | analyzer-phase1 | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.analyzer-phase1.md` |
| T-0060-S18 | analyzer-phase2 | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.analyzer-phase2.md` |
| T-0060-S19 | sma-a | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.sma-a.md` |
| T-0060-S20 | analyzer-phase1 | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.analyzer-phase1.md` |
| T-0060-S21 | analyzer-phase2 | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.analyzer-phase2.md` |
| T-0060-S22 | sma-a | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.sma-a.md` |
| T-0060-S23 | analyzer-phase1 | v07-ch07 | done | 2 | `agent_prompts/agent_prompt.v07-ch07.analyzer-phase1.attempt2.md` |
| T-0060-S24 | analyzer-phase2 | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.analyzer-phase2.md` |
| T-0060-S25 | sma-a | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.sma-a.md` |
| T-0060-S26 | analyzer-phase1 | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.analyzer-phase1.md` |
| T-0060-S27 | analyzer-phase2 | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.analyzer-phase2.md` |
| T-0060-S28 | sma-a | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.sma-a.md` |
| T-0060-S29 | analyzer-phase1 | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.analyzer-phase1.md` |
| T-0060-S30 | analyzer-phase2 | v07-ch09 | done | 2 | `agent_prompts/agent_prompt.v07-ch09.analyzer-phase2.attempt2.md` |
| T-0060-S31 | sma-a | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.sma-a.md` |
| T-0060-S32 | analyzer-phase1 | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.analyzer-phase1.md` |
| T-0060-S33 | analyzer-phase2 | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.analyzer-phase2.md` |
| T-0060-S34 | sma-a | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.sma-a.md` |
| T-0060-S35 | analyzer-phase1 | v07-epilogue | done | 2 | `agent_prompts/agent_prompt.v07-epilogue.analyzer-phase1.attempt2.md` |
| T-0060-S36 | analyzer-phase2 | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.analyzer-phase2.md` |
| T-0060-S37 | sma-a | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.sma-a.md` |
| T-0060-S38 | analyzer-phase1 | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.analyzer-phase1.md` |
| T-0060-S39 | analyzer-phase2 | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.analyzer-phase2.md` |
| T-0060-S40 | sma-a | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.sma-a.md` |
| T-0060-S41 | analyzer-phase1 | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.analyzer-phase1.md` |
| T-0060-S42 | analyzer-phase2 | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.analyzer-phase2.md` |
| T-0060-S43 | sma-a | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.sma-a.md` |
| T-0060-S44 | analyzer-phase1 | v08-ch02 | done | 2 | `agent_prompts/agent_prompt.v08-ch02.analyzer-phase1.attempt2.md` |
| T-0060-S45 | analyzer-phase2 | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.analyzer-phase2.md` |
| T-0060-S46 | sma-a | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.sma-a.md` |
| T-0060-S47 | analyzer-phase1 | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.analyzer-phase1.md` |
| T-0060-S48 | analyzer-phase2 | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.analyzer-phase2.md` |
| T-0060-S49 | sma-a | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.sma-a.md` |
| T-0060-S50 | analyzer-phase1 | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.analyzer-phase1.md` |
| T-0060-S51 | analyzer-phase2 | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.analyzer-phase2.md` |
| T-0060-S52 | sma-a | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.sma-a.md` |
| T-0060-S53 | analyzer-phase1 | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.analyzer-phase1.md` |
| T-0060-S54 | analyzer-phase2 | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.analyzer-phase2.md` |
| T-0060-S55 | sma-a | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.sma-a.md` |
| T-0060-S56 | analyzer-phase1 | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.analyzer-phase1.md` |
| T-0060-S57 | analyzer-phase2 | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.analyzer-phase2.md` |
| T-0060-S58 | sma-a | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.sma-a.md` |
| T-0060-S59 | analyzer-phase1 | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.analyzer-phase1.md` |
| T-0060-S60 | analyzer-phase2 | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.analyzer-phase2.md` |
| T-0060-S61 | sma-a | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.sma-a.md` |
| T-0060-S62 | analyzer-phase1 | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.analyzer-phase1.md` |
| T-0060-S63 | analyzer-phase2 | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.analyzer-phase2.md` |
| T-0060-S64 | sma-a | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.sma-a.md` |
| T-0060-S65 | analyzer-phase1 | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.analyzer-phase1.md` |
| T-0060-S66 | analyzer-phase2 | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.analyzer-phase2.md` |
| T-0060-S67 | sma-a | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.sma-a.md` |
| T-0060-S68 | analyzer-phase1 | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.analyzer-phase1.md` |
| T-0060-S69 | analyzer-phase2 | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.analyzer-phase2.md` |
| T-0060-S70 | sma-a | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.sma-a.md` |
| T-0060-S71 | analyzer-phase1 | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.analyzer-phase1.md` |
| T-0060-S72 | analyzer-phase2 | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.analyzer-phase2.md` |
| T-0060-S73 | sma-a | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.sma-a.md` |
| T-0060-S74 | analyzer-phase1 | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.analyzer-phase1.md` |
| T-0060-S75 | analyzer-phase2 | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.analyzer-phase2.md` |
| T-0060-S76 | sma-a | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.sma-a.md` |
| T-0060-S77 | analyzer-phase1 | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.analyzer-phase1.md` |
| T-0060-S78 | analyzer-phase2 | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.analyzer-phase2.md` |
| T-0060-S79 | sma-a | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.sma-a.md` |
| T-0060-S80 | analyzer-phase1 | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.analyzer-phase1.md` |
| T-0060-S81 | analyzer-phase2 | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.analyzer-phase2.md` |
| T-0060-S82 | sma-a | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.sma-a.md` |
| T-0060-S83 | analyzer-phase1 | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.analyzer-phase1.md` |
| T-0060-S84 | analyzer-phase2 | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.analyzer-phase2.md` |
| T-0060-S85 | sma-a | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.sma-a.md` |
| T-0060-S86 | analyzer-phase1 | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.analyzer-phase1.md` |
| T-0060-S87 | analyzer-phase2 | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.analyzer-phase2.md` |
| T-0060-S88 | sma-a | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.sma-a.md` |
| T-0060-S89 | analyzer-phase1 | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.analyzer-phase1.md` |
| T-0060-S90 | analyzer-phase2 | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.analyzer-phase2.md` |
| T-0060-S91 | sma-a | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.sma-a.md` |
| T-0060-S92 | analyzer-phase1 | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.analyzer-phase1.md` |
| T-0060-S93 | analyzer-phase2 | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.analyzer-phase2.md` |
| T-0060-S94 | sma-a | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.sma-a.md` |
| T-0060-S95 | analyzer-phase1 | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.analyzer-phase1.md` |
| T-0060-S96 | analyzer-phase2 | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.analyzer-phase2.md` |
| T-0060-S97 | sma-a | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.sma-a.md` |
| T-0060-S98 | analyzer-phase1 | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.analyzer-phase1.md` |
| T-0060-S99 | analyzer-phase2 | v09-ch08 | done | 2 | `agent_prompts/agent_prompt.v09-ch08.analyzer-phase2.attempt2.md` |
| T-0060-S100 | sma-a | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.sma-a.md` |
| T-0060-S101 | analyzer-phase1 | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.analyzer-phase1.md` |
| T-0060-S102 | analyzer-phase2 | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.analyzer-phase2.md` |
| T-0060-S103 | sma-a | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.sma-a.md` |
| T-0060-S104 | analyzer-phase1 | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.analyzer-phase1.md` |
| T-0060-S105 | analyzer-phase2 | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.analyzer-phase2.md` |
| T-0060-S106 | sma-a | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.sma-a.md` |
| T-0060-S107 | analyzer-phase1 | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.analyzer-phase1.md` |
| T-0060-S108 | analyzer-phase2 | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.analyzer-phase2.md` |
| T-0060-S109 | sma-a | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.sma-a.md` |
| T-0060-S110 | analyzer-phase1 | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.analyzer-phase1.md` |
| T-0060-S111 | analyzer-phase2 | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.analyzer-phase2.md` |
| T-0060-S112 | sma-a | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.sma-a.md` |
| T-0060-S113 | analyzer-phase1 | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.analyzer-phase1.md` |
| T-0060-S114 | analyzer-phase2 | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.analyzer-phase2.md` |
| T-0060-S115 | sma-a | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.sma-a.md` |
| T-0060-S116 | analyzer-phase1 | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.analyzer-phase1.md` |
| T-0060-S117 | analyzer-phase2 | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.analyzer-phase2.md` |
| T-0060-S118 | sma-a | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.sma-a.md` |
| T-0060-S119 | analyzer-phase1 | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.analyzer-phase1.md` |
| T-0060-S120 | analyzer-phase2 | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.analyzer-phase2.md` |
| T-0060-S121 | sma-a | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.sma-a.md` |
| T-0060-S122 | analyzer-phase1 | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.analyzer-phase1.md` |
| T-0060-S123 | analyzer-phase2 | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.analyzer-phase2.md` |
| T-0060-S124 | sma-a | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.sma-a.md` |
| T-0060-S125 | analyzer-phase1 | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.analyzer-phase1.md` |
| T-0060-S126 | analyzer-phase2 | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.analyzer-phase2.md` |
| T-0060-S127 | sma-a | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.sma-a.md` |
| T-0060-S128 | analyzer-phase1 | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.analyzer-phase1.md` |
| T-0060-S129 | analyzer-phase2 | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.analyzer-phase2.md` |
| T-0060-S130 | sma-a | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.sma-a.md` |
| T-0060-S131 | analyzer-phase1 | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.analyzer-phase1.md` |
| T-0060-S132 | analyzer-phase2 | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.analyzer-phase2.md` |
| T-0060-S133 | sma-a | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.sma-a.md` |
| T-0060-S134 | analyzer-phase1 | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.analyzer-phase1.md` |
| T-0060-S135 | analyzer-phase2 | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.analyzer-phase2.md` |
| T-0060-S136 | sma-a | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.sma-a.md` |
| T-0060-S137 | analyzer-phase1 | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.analyzer-phase1.md` |
| T-0060-S138 | analyzer-phase2 | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.analyzer-phase2.md` |
| T-0060-S139 | sma-a | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.sma-a.md` |
| T-0060-S140 | analyzer-phase1 | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.analyzer-phase1.md` |
| T-0060-S141 | analyzer-phase2 | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.analyzer-phase2.md` |
| T-0060-S142 | sma-a | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.sma-a.md` |
| T-0060-S143 | analyzer-phase1 | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.analyzer-phase1.md` |
| T-0060-S144 | analyzer-phase2 | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.analyzer-phase2.md` |
| T-0060-S145 | sma-a | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.sma-a.md` |
| T-0060-S146 | analyzer-phase1 | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.analyzer-phase1.md` |
| T-0060-S147 | analyzer-phase2 | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.analyzer-phase2.md` |
| T-0060-S148 | sma-a | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.sma-a.md` |
| T-0060-S149 | analyzer-phase1 | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.analyzer-phase1.md` |
| T-0060-S150 | analyzer-phase2 | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.analyzer-phase2.md` |
| T-0060-S151 | sma-a | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.sma-a.md` |
| T-0060-S152 | analyzer-phase1 | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.analyzer-phase1.md` |
| T-0060-S153 | analyzer-phase2 | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.analyzer-phase2.md` |
| T-0060-S154 | sma-a | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.sma-a.md` |
| T-0060-S155 | analyzer-phase1 | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.analyzer-phase1.md` |
| T-0060-S156 | analyzer-phase2 | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.analyzer-phase2.md` |
| T-0060-S157 | sma-a | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.sma-a.md` |
| T-0060-S158 | analyzer-phase1 | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.analyzer-phase1.md` |
| T-0060-S159 | analyzer-phase2 | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.analyzer-phase2.md` |
| T-0060-S160 | sma-a | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.sma-a.md` |
| T-0060-S161 | analyzer-phase1 | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.analyzer-phase1.md` |
| T-0060-S162 | analyzer-phase2 | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.analyzer-phase2.md` |
| T-0060-S163 | sma-a | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.sma-a.md` |
| T-0060-S164 | analyzer-phase1 | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.analyzer-phase1.md` |
| T-0060-S165 | analyzer-phase2 | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.analyzer-phase2.md` |
| T-0060-S166 | sma-a | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.sma-a.md` |
| T-0060-S167 | analyzer-phase1 | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.analyzer-phase1.md` |
| T-0060-S168 | analyzer-phase2 | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.analyzer-phase2.md` |
| T-0060-S169 | sma-a | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.sma-a.md` |
| T-0060-S170 | analyzer-phase1 | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.analyzer-phase1.md` |
| T-0060-S171 | analyzer-phase2 | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.analyzer-phase2.md` |
| T-0060-S172 | sma-a | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.sma-a.md` |
| T-0060-S173 | analyzer-phase1 | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.analyzer-phase1.md` |
| T-0060-S174 | analyzer-phase2 | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.analyzer-phase2.md` |
| T-0060-S175 | sma-a | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.sma-a.md` |
| T-0060-S176 | analyzer-phase1 | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.analyzer-phase1.md` |
| T-0060-S177 | analyzer-phase2 | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.analyzer-phase2.md` |
| T-0060-S178 | sma-a | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.sma-a.md` |
| T-0060-S179 | analyzer-phase1 | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.analyzer-phase1.md` |
| T-0060-S180 | analyzer-phase2 | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.analyzer-phase2.md` |
| T-0060-S181 | sma-a | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.sma-a.md` |
| T-0060-S182 | analyzer-phase1 | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.analyzer-phase1.md` |
| T-0060-S183 | analyzer-phase2 | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.analyzer-phase2.md` |
| T-0060-S184 | sma-a | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.sma-a.md` |
| T-0060-S185 | analyzer-phase1 | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.analyzer-phase1.md` |
| T-0060-S186 | analyzer-phase2 | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.analyzer-phase2.md` |
| T-0060-S187 | sma-a | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.sma-a.md` |
| T-0060-S188 | analyzer-phase1 | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.analyzer-phase1.md` |
| T-0060-S189 | analyzer-phase2 | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.analyzer-phase2.md` |
| T-0060-S190 | sma-a | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.sma-a.md` |
| T-0060-S191 | analyzer-phase1 | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.analyzer-phase1.md` |
| T-0060-S192 | analyzer-phase2 | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.analyzer-phase2.md` |
| T-0060-S193 | sma-a | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.sma-a.md` |
| T-0060-S194 | analyzer-phase1 | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.analyzer-phase1.md` |
| T-0060-S195 | analyzer-phase2 | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.analyzer-phase2.md` |
| T-0060-S196 | sma-a | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.sma-a.md` |
| T-0060-S197 | analyzer-phase1 | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.analyzer-phase1.md` |
| T-0060-S198 | analyzer-phase2 | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.analyzer-phase2.md` |
| T-0060-S199 | sma-a | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.sma-a.md` |
| T-0060-S200 | analyzer-phase1 | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.analyzer-phase1.md` |
| T-0060-S201 | analyzer-phase2 | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.analyzer-phase2.md` |
| T-0060-S202 | sma-a | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.sma-a.md` |
| T-0060-S203 | analyzer-phase1 | v13-ch08 | done | 2 | `agent_prompts/agent_prompt.v13-ch08.analyzer-phase1.attempt2.md` |
| T-0060-S204 | analyzer-phase2 | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.analyzer-phase2.md` |
| T-0060-S205 | sma-a | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.sma-a.md` |
| T-0060-S206 | analyzer-phase1 | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.analyzer-phase1.md` |
| T-0060-S207 | analyzer-phase2 | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.analyzer-phase2.md` |
| T-0060-S208 | sma-a | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.sma-a.md` |
| T-0060-S209 | analyzer-phase1 | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.analyzer-phase1.md` |
| T-0060-S210 | analyzer-phase2 | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.analyzer-phase2.md` |
| T-0060-S211 | sma-a | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.sma-a.md` |
| T-0060-S212 | analyzer-phase1 | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.analyzer-phase1.md` |
| T-0060-S213 | analyzer-phase2 | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.analyzer-phase2.md` |
| T-0060-S214 | sma-a | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.sma-a.md` |
| T-0060-S215 | analyzer-phase1 | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.analyzer-phase1.md` |
| T-0060-S216 | analyzer-phase2 | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.analyzer-phase2.md` |
| T-0060-S217 | sma-a | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.sma-a.md` |
| T-0060-S218 | analyzer-phase1 | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.analyzer-phase1.md` |
| T-0060-S219 | analyzer-phase2 | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.analyzer-phase2.md` |
| T-0060-S220 | sma-a | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.sma-a.md` |
| T-0060-S221 | analyzer-phase1 | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.analyzer-phase1.md` |
| T-0060-S222 | analyzer-phase2 | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.analyzer-phase2.md` |
| T-0060-S223 | sma-a | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.sma-a.md` |
| T-0060-S224 | analyzer-phase1 | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.analyzer-phase1.md` |
| T-0060-S225 | analyzer-phase2 | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.analyzer-phase2.md` |
| T-0060-S226 | sma-a | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.sma-a.md` |
| T-0060-S227 | analyzer-phase1 | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.analyzer-phase1.md` |
| T-0060-S228 | analyzer-phase2 | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.analyzer-phase2.md` |
| T-0060-S229 | sma-a | v12-ch08 | done | 2 | `agent_prompts/agent_prompt.v12-ch08.sma-a.attempt2.md` |
| T-0060-S230 | analyzer-phase1 | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.analyzer-phase1.md` |
| T-0060-S231 | analyzer-phase2 | v12-ch08 | done | 2 | `agent_prompts/agent_prompt.v12-ch08.analyzer-phase2.attempt2.md` |

Заметки:
- T-0060-S1: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S2: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S3: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S4: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S5: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S6: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S7: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S8: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S9: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S10: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S11: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S12: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S13: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S14: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S15: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S16: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S17: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S18: раунд smaA-09f9d8aa: A+ph1+ph2, отчёты сохранены, коммит не делался
- T-0060-S19: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S20: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S21: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S22: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S23: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S24: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S25: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S26: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S27: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S28: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S29: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S30: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S31: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S32: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S33: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S34: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S35: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S36: раунд smaA-09f9d8aa: A+ph1+ph2, артефакты подтверждены, коммит не делался
- T-0060-S37: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S38: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S39: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S40: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S41: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S42: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S43: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S44: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S45: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S46: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S47: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S48: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S49: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S50: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S51: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S52: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S53: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S54: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S55: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S56: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S57: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S58: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S59: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S60: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S61: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S62: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S63: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S64: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S65: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S66: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S67: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S68: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S69: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S70: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S71: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S72: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S73: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S74: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S75: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S76: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S77: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S78: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S79: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S80: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S81: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S82: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S83: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S84: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S85: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S86: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S87: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S88: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S89: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S90: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S91: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S92: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S93: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S94: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S95: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S96: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S97: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S98: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S99: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S100: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S101: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S102: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S103: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S104: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S105: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S106: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S107: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S108: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S109: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S110: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S111: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S112: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S113: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S114: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S115: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S116: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S117: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S118: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S119: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S120: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S121: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S122: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S123: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S124: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S125: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S126: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S127: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S128: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S129: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S130: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S131: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S132: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S133: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S134: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S135: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S136: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S137: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S138: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S139: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S140: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S141: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S142: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S143: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S144: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S145: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S146: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S147: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S148: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S149: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S150: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S151: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S152: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S153: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S154: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S155: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S156: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S157: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S158: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S159: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S160: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S161: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S162: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S163: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S164: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S165: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S166: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S167: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S168: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S169: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S170: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S171: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S172: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S173: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S174: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S175: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S176: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S177: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S178: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S179: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S180: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S181: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S182: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S183: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S184: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S185: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S186: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S187: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S188: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S189: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S190: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S191: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S192: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S193: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S194: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S195: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S196: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S197: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S198: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S199: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S200: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S201: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S202: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S203: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S204: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S205: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S206: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S207: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S208: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S209: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S210: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S211: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S212: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S213: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S214: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S215: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S216: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S217: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S218: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S219: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S220: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S221: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S222: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S223: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S224: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S225: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S226: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S227: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S228: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S229: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S230: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался
- T-0060-S231: раунд smaA-09f9d8aa: A+ph1+ph2, коммит не делался

## T-0061 — DONE

Проверка 2 — макросемантика и логика (Semantic Audit B), тома 7-13, раунд smaB-20261118

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0061-S1 | sma-b | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.sma-b.md` |
| T-0061-S2 | analyzer-phase1 | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.analyzer-phase1.md` |
| T-0061-S3 | analyzer-phase2 | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.analyzer-phase2.md` |
| T-0061-S4 | sma-b | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.sma-b.md` |
| T-0061-S5 | analyzer-phase1 | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.analyzer-phase1.md` |
| T-0061-S6 | analyzer-phase2 | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.analyzer-phase2.md` |
| T-0061-S7 | sma-b | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.sma-b.md` |
| T-0061-S8 | analyzer-phase1 | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.analyzer-phase1.md` |
| T-0061-S9 | analyzer-phase2 | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.analyzer-phase2.md` |
| T-0061-S10 | sma-b | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.sma-b.md` |
| T-0061-S11 | analyzer-phase1 | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.analyzer-phase1.md` |
| T-0061-S12 | analyzer-phase2 | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.analyzer-phase2.md` |
| T-0061-S13 | sma-b | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.sma-b.md` |
| T-0061-S14 | analyzer-phase1 | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.analyzer-phase1.md` |
| T-0061-S15 | analyzer-phase2 | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.analyzer-phase2.md` |
| T-0061-S16 | sma-b | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.sma-b.md` |
| T-0061-S17 | analyzer-phase1 | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.analyzer-phase1.md` |
| T-0061-S18 | analyzer-phase2 | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.analyzer-phase2.md` |
| T-0061-S19 | sma-b | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.sma-b.md` |
| T-0061-S20 | analyzer-phase1 | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.analyzer-phase1.md` |
| T-0061-S21 | analyzer-phase2 | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.analyzer-phase2.md` |
| T-0061-S22 | sma-b | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.sma-b.md` |
| T-0061-S23 | analyzer-phase1 | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.analyzer-phase1.md` |
| T-0061-S24 | analyzer-phase2 | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.analyzer-phase2.md` |
| T-0061-S25 | sma-b | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.sma-b.md` |
| T-0061-S26 | analyzer-phase1 | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.analyzer-phase1.md` |
| T-0061-S27 | analyzer-phase2 | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.analyzer-phase2.md` |
| T-0061-S28 | sma-b | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.sma-b.md` |
| T-0061-S29 | analyzer-phase1 | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.analyzer-phase1.md` |
| T-0061-S30 | analyzer-phase2 | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.analyzer-phase2.md` |
| T-0061-S31 | sma-b | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.sma-b.md` |
| T-0061-S32 | analyzer-phase1 | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.analyzer-phase1.md` |
| T-0061-S33 | analyzer-phase2 | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.analyzer-phase2.md` |
| T-0061-S34 | sma-b | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.sma-b.md` |
| T-0061-S35 | analyzer-phase1 | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.analyzer-phase1.md` |
| T-0061-S36 | analyzer-phase2 | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.analyzer-phase2.md` |
| T-0061-S37 | sma-b | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.sma-b.md` |
| T-0061-S38 | analyzer-phase1 | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.analyzer-phase1.md` |
| T-0061-S39 | analyzer-phase2 | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.analyzer-phase2.md` |
| T-0061-S40 | sma-b | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.sma-b.md` |
| T-0061-S41 | analyzer-phase1 | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.analyzer-phase1.md` |
| T-0061-S42 | analyzer-phase2 | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.analyzer-phase2.md` |
| T-0061-S43 | sma-b | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.sma-b.md` |
| T-0061-S44 | analyzer-phase1 | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.analyzer-phase1.md` |
| T-0061-S45 | analyzer-phase2 | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.analyzer-phase2.md` |
| T-0061-S46 | sma-b | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.sma-b.md` |
| T-0061-S47 | analyzer-phase1 | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.analyzer-phase1.md` |
| T-0061-S48 | analyzer-phase2 | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.analyzer-phase2.md` |
| T-0061-S49 | sma-b | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.sma-b.md` |
| T-0061-S50 | analyzer-phase1 | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.analyzer-phase1.md` |
| T-0061-S51 | analyzer-phase2 | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.analyzer-phase2.md` |
| T-0061-S52 | sma-b | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.sma-b.md` |
| T-0061-S53 | analyzer-phase1 | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.analyzer-phase1.md` |
| T-0061-S54 | analyzer-phase2 | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.analyzer-phase2.md` |
| T-0061-S55 | sma-b | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.sma-b.md` |
| T-0061-S56 | analyzer-phase1 | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.analyzer-phase1.md` |
| T-0061-S57 | analyzer-phase2 | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.analyzer-phase2.md` |
| T-0061-S58 | sma-b | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.sma-b.md` |
| T-0061-S59 | analyzer-phase1 | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.analyzer-phase1.md` |
| T-0061-S60 | analyzer-phase2 | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.analyzer-phase2.md` |
| T-0061-S61 | sma-b | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.sma-b.md` |
| T-0061-S62 | analyzer-phase1 | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.analyzer-phase1.md` |
| T-0061-S63 | analyzer-phase2 | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.analyzer-phase2.md` |
| T-0061-S64 | sma-b | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.sma-b.md` |
| T-0061-S65 | analyzer-phase1 | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.analyzer-phase1.md` |
| T-0061-S66 | analyzer-phase2 | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.analyzer-phase2.md` |
| T-0061-S67 | sma-b | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.sma-b.md` |
| T-0061-S68 | analyzer-phase1 | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.analyzer-phase1.md` |
| T-0061-S69 | analyzer-phase2 | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.analyzer-phase2.md` |
| T-0061-S70 | sma-b | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.sma-b.md` |
| T-0061-S71 | analyzer-phase1 | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.analyzer-phase1.md` |
| T-0061-S72 | analyzer-phase2 | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.analyzer-phase2.md` |
| T-0061-S73 | sma-b | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.sma-b.md` |
| T-0061-S74 | analyzer-phase1 | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.analyzer-phase1.md` |
| T-0061-S75 | analyzer-phase2 | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.analyzer-phase2.md` |
| T-0061-S76 | sma-b | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.sma-b.md` |
| T-0061-S77 | analyzer-phase1 | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.analyzer-phase1.md` |
| T-0061-S78 | analyzer-phase2 | v09-ch01 | done | 2 | `agent_prompts/agent_prompt.v09-ch01.analyzer-phase2.attempt2.md` |
| T-0061-S79 | sma-b | v09-ch02 | done | 2 | `agent_prompts/agent_prompt.v09-ch02.sma-b.attempt2.md` |
| T-0061-S80 | analyzer-phase1 | v09-ch02 | done | 2 | `agent_prompts/agent_prompt.v09-ch02.analyzer-phase1.attempt2.md` |
| T-0061-S81 | analyzer-phase2 | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.analyzer-phase2.md` |
| T-0061-S82 | sma-b | v09-ch03 | done | 2 | `agent_prompts/agent_prompt.v09-ch03.sma-b.attempt2.md` |
| T-0061-S83 | analyzer-phase1 | v09-ch03 | done | 2 | `agent_prompts/agent_prompt.v09-ch03.analyzer-phase1.attempt2.md` |
| T-0061-S84 | analyzer-phase2 | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.analyzer-phase2.md` |
| T-0061-S85 | sma-b | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.sma-b.md` |
| T-0061-S86 | analyzer-phase1 | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.analyzer-phase1.md` |
| T-0061-S87 | analyzer-phase2 | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.analyzer-phase2.md` |
| T-0061-S88 | sma-b | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.sma-b.md` |
| T-0061-S89 | analyzer-phase1 | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.analyzer-phase1.md` |
| T-0061-S90 | analyzer-phase2 | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.analyzer-phase2.md` |
| T-0061-S91 | sma-b | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.sma-b.md` |
| T-0061-S92 | analyzer-phase1 | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.analyzer-phase1.md` |
| T-0061-S93 | analyzer-phase2 | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.analyzer-phase2.md` |
| T-0061-S94 | sma-b | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.sma-b.md` |
| T-0061-S95 | analyzer-phase1 | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.analyzer-phase1.md` |
| T-0061-S96 | analyzer-phase2 | v09-ch07 | done | 2 | `agent_prompts/agent_prompt.v09-ch07.analyzer-phase2.attempt2.md` |
| T-0061-S97 | sma-b | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.sma-b.md` |
| T-0061-S98 | analyzer-phase1 | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.analyzer-phase1.md` |
| T-0061-S99 | analyzer-phase2 | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.analyzer-phase2.md` |
| T-0061-S100 | sma-b | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.sma-b.md` |
| T-0061-S101 | analyzer-phase1 | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.analyzer-phase1.md` |
| T-0061-S102 | analyzer-phase2 | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.analyzer-phase2.md` |
| T-0061-S103 | sma-b | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.sma-b.md` |
| T-0061-S104 | analyzer-phase1 | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.analyzer-phase1.md` |
| T-0061-S105 | analyzer-phase2 | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.analyzer-phase2.md` |
| T-0061-S106 | sma-b | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.sma-b.md` |
| T-0061-S107 | analyzer-phase1 | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.analyzer-phase1.md` |
| T-0061-S108 | analyzer-phase2 | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.analyzer-phase2.md` |
| T-0061-S109 | sma-b | v10-ch01 | done | 2 | `agent_prompts/agent_prompt.v10-ch01.sma-b.attempt2.md` |
| T-0061-S110 | analyzer-phase1 | v10-ch01 | done | 2 | `agent_prompts/agent_prompt.v10-ch01.analyzer-phase1.attempt2.md` |
| T-0061-S111 | analyzer-phase2 | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.analyzer-phase2.md` |
| T-0061-S112 | sma-b | v10-ch02 | done | 2 | `agent_prompts/agent_prompt.v10-ch02.sma-b.attempt2.md` |
| T-0061-S113 | analyzer-phase1 | v10-ch02 | done | 2 | `agent_prompts/agent_prompt.v10-ch02.analyzer-phase1.attempt2.md` |
| T-0061-S114 | analyzer-phase2 | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.analyzer-phase2.md` |
| T-0061-S115 | sma-b | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.sma-b.md` |
| T-0061-S116 | analyzer-phase1 | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.analyzer-phase1.md` |
| T-0061-S117 | analyzer-phase2 | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.analyzer-phase2.md` |
| T-0061-S118 | sma-b | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.sma-b.md` |
| T-0061-S119 | analyzer-phase1 | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.analyzer-phase1.md` |
| T-0061-S120 | analyzer-phase2 | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.analyzer-phase2.md` |
| T-0061-S121 | sma-b | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.sma-b.md` |
| T-0061-S122 | analyzer-phase1 | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.analyzer-phase1.md` |
| T-0061-S123 | analyzer-phase2 | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.analyzer-phase2.md` |
| T-0061-S124 | sma-b | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.sma-b.md` |
| T-0061-S125 | analyzer-phase1 | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.analyzer-phase1.md` |
| T-0061-S126 | analyzer-phase2 | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.analyzer-phase2.md` |
| T-0061-S127 | sma-b | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.sma-b.md` |
| T-0061-S128 | analyzer-phase1 | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.analyzer-phase1.md` |
| T-0061-S129 | analyzer-phase2 | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.analyzer-phase2.md` |
| T-0061-S130 | sma-b | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.sma-b.md` |
| T-0061-S131 | analyzer-phase1 | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.analyzer-phase1.md` |
| T-0061-S132 | analyzer-phase2 | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.analyzer-phase2.md` |
| T-0061-S133 | sma-b | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.sma-b.md` |
| T-0061-S134 | analyzer-phase1 | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.analyzer-phase1.md` |
| T-0061-S135 | analyzer-phase2 | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.analyzer-phase2.md` |
| T-0061-S136 | sma-b | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.sma-b.md` |
| T-0061-S137 | analyzer-phase1 | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.analyzer-phase1.md` |
| T-0061-S138 | analyzer-phase2 | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.analyzer-phase2.md` |
| T-0061-S139 | sma-b | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.sma-b.md` |
| T-0061-S140 | analyzer-phase1 | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.analyzer-phase1.md` |
| T-0061-S141 | analyzer-phase2 | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.analyzer-phase2.md` |
| T-0061-S142 | sma-b | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.sma-b.md` |
| T-0061-S143 | analyzer-phase1 | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.analyzer-phase1.md` |
| T-0061-S144 | analyzer-phase2 | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.analyzer-phase2.md` |
| T-0061-S145 | sma-b | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.sma-b.md` |
| T-0061-S146 | analyzer-phase1 | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.analyzer-phase1.md` |
| T-0061-S147 | analyzer-phase2 | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.analyzer-phase2.md` |
| T-0061-S148 | sma-b | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.sma-b.md` |
| T-0061-S149 | analyzer-phase1 | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.analyzer-phase1.md` |
| T-0061-S150 | analyzer-phase2 | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.analyzer-phase2.md` |
| T-0061-S151 | sma-b | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.sma-b.md` |
| T-0061-S152 | analyzer-phase1 | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.analyzer-phase1.md` |
| T-0061-S153 | analyzer-phase2 | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.analyzer-phase2.md` |
| T-0061-S154 | sma-b | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.sma-b.md` |
| T-0061-S155 | analyzer-phase1 | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.analyzer-phase1.md` |
| T-0061-S156 | analyzer-phase2 | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.analyzer-phase2.md` |
| T-0061-S157 | sma-b | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.sma-b.md` |
| T-0061-S158 | analyzer-phase1 | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.analyzer-phase1.md` |
| T-0061-S159 | analyzer-phase2 | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.analyzer-phase2.md` |
| T-0061-S160 | sma-b | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.sma-b.md` |
| T-0061-S161 | analyzer-phase1 | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.analyzer-phase1.md` |
| T-0061-S162 | analyzer-phase2 | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.analyzer-phase2.md` |
| T-0061-S163 | sma-b | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.sma-b.md` |
| T-0061-S164 | analyzer-phase1 | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.analyzer-phase1.md` |
| T-0061-S165 | analyzer-phase2 | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.analyzer-phase2.md` |
| T-0061-S166 | sma-b | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.sma-b.md` |
| T-0061-S167 | analyzer-phase1 | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.analyzer-phase1.md` |
| T-0061-S168 | analyzer-phase2 | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.analyzer-phase2.md` |
| T-0061-S169 | sma-b | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.sma-b.md` |
| T-0061-S170 | analyzer-phase1 | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.analyzer-phase1.md` |
| T-0061-S171 | analyzer-phase2 | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.analyzer-phase2.md` |
| T-0061-S172 | sma-b | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.sma-b.md` |
| T-0061-S173 | analyzer-phase1 | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.analyzer-phase1.md` |
| T-0061-S174 | analyzer-phase2 | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.analyzer-phase2.md` |
| T-0061-S175 | sma-b | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.sma-b.md` |
| T-0061-S176 | analyzer-phase1 | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.analyzer-phase1.md` |
| T-0061-S177 | analyzer-phase2 | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.analyzer-phase2.md` |
| T-0061-S178 | sma-b | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.sma-b.md` |
| T-0061-S179 | analyzer-phase1 | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.analyzer-phase1.md` |
| T-0061-S180 | analyzer-phase2 | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.analyzer-phase2.md` |
| T-0061-S181 | sma-b | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.sma-b.md` |
| T-0061-S182 | analyzer-phase1 | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.analyzer-phase1.md` |
| T-0061-S183 | analyzer-phase2 | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.analyzer-phase2.md` |
| T-0061-S184 | sma-b | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.sma-b.md` |
| T-0061-S185 | analyzer-phase1 | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.analyzer-phase1.md` |
| T-0061-S186 | analyzer-phase2 | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.analyzer-phase2.md` |
| T-0061-S187 | sma-b | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.sma-b.md` |
| T-0061-S188 | analyzer-phase1 | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.analyzer-phase1.md` |
| T-0061-S189 | analyzer-phase2 | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.analyzer-phase2.md` |
| T-0061-S190 | sma-b | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.sma-b.md` |
| T-0061-S191 | analyzer-phase1 | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.analyzer-phase1.md` |
| T-0061-S192 | analyzer-phase2 | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.analyzer-phase2.md` |
| T-0061-S193 | sma-b | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.sma-b.md` |
| T-0061-S194 | analyzer-phase1 | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.analyzer-phase1.md` |
| T-0061-S195 | analyzer-phase2 | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.analyzer-phase2.md` |
| T-0061-S196 | sma-b | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.sma-b.md` |
| T-0061-S197 | analyzer-phase1 | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.analyzer-phase1.md` |
| T-0061-S198 | analyzer-phase2 | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.analyzer-phase2.md` |
| T-0061-S199 | sma-b | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.sma-b.md` |
| T-0061-S200 | analyzer-phase1 | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.analyzer-phase1.md` |
| T-0061-S201 | analyzer-phase2 | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.analyzer-phase2.md` |
| T-0061-S202 | sma-b | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.sma-b.md` |
| T-0061-S203 | analyzer-phase1 | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.analyzer-phase1.md` |
| T-0061-S204 | analyzer-phase2 | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.analyzer-phase2.md` |
| T-0061-S205 | sma-b | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.sma-b.md` |
| T-0061-S206 | analyzer-phase1 | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.analyzer-phase1.md` |
| T-0061-S207 | analyzer-phase2 | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.analyzer-phase2.md` |
| T-0061-S208 | sma-b | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.sma-b.md` |
| T-0061-S209 | analyzer-phase1 | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.analyzer-phase1.md` |
| T-0061-S210 | analyzer-phase2 | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.analyzer-phase2.md` |
| T-0061-S211 | sma-b | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.sma-b.md` |
| T-0061-S212 | analyzer-phase1 | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.analyzer-phase1.md` |
| T-0061-S213 | analyzer-phase2 | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.analyzer-phase2.md` |
| T-0061-S214 | sma-b | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.sma-b.md` |
| T-0061-S215 | analyzer-phase1 | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.analyzer-phase1.md` |
| T-0061-S216 | analyzer-phase2 | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.analyzer-phase2.md` |
| T-0061-S217 | sma-b | v12-ch02 | done | 3 | `agent_prompts/agent_prompt.v12-ch02.sma-b.attempt3.md` |
| T-0061-S218 | analyzer-phase1 | v12-ch02 | done | 3 | `agent_prompts/agent_prompt.v12-ch02.analyzer-phase1.attempt3.md` |
| T-0061-S219 | analyzer-phase2 | v12-ch02 | done | 2 | `agent_prompts/agent_prompt.v12-ch02.analyzer-phase2.attempt2.md` |
| T-0061-S220 | sma-b | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.sma-b.md` |
| T-0061-S221 | analyzer-phase1 | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.analyzer-phase1.md` |
| T-0061-S222 | analyzer-phase2 | v12-ch04 | done | 2 | `agent_prompts/agent_prompt.v12-ch04.analyzer-phase2.attempt2.md` |
| T-0061-S223 | sma-b | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.sma-b.md` |
| T-0061-S224 | analyzer-phase1 | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.analyzer-phase1.md` |
| T-0061-S225 | analyzer-phase2 | v12-ch05 | done | 2 | `agent_prompts/agent_prompt.v12-ch05.analyzer-phase2.attempt2.md` |
| T-0061-S226 | sma-b | v12-ch07 | done | 2 | `agent_prompts/agent_prompt.v12-ch07.sma-b.attempt2.md` |
| T-0061-S227 | analyzer-phase1 | v12-ch07 | done | 2 | `agent_prompts/agent_prompt.v12-ch07.analyzer-phase1.attempt2.md` |
| T-0061-S228 | analyzer-phase2 | v12-ch07 | done | 2 | `agent_prompts/agent_prompt.v12-ch07.analyzer-phase2.attempt2.md` |
| T-0061-S229 | sma-b | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.sma-b.md` |
| T-0061-S230 | analyzer-phase1 | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.analyzer-phase1.md` |
| T-0061-S231 | analyzer-phase2 | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.analyzer-phase2.md` |

Заметки:
- T-0061-S1: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S2: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S3: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S4: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S5: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S6: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S7: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S8: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S9: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S10: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S11: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S12: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S13: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S14: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S15: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S16: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S17: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S18: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S19: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S20: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S21: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S22: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S23: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S24: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S25: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S26: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S27: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S28: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S29: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S30: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S31: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S32: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S33: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S34: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S35: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S36: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S37: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S38: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S39: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S40: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S41: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S42: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S43: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S44: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S45: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S46: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S47: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S48: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S49: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S50: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S51: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S52: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S53: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S54: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S55: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S56: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S57: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S58: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S59: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S60: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S61: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S62: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S63: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S64: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S65: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S66: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S67: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S68: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S69: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S70: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S71: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S72: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S73: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S74: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S75: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S76: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S77: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S78: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S79: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S80: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S81: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S82: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S83: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S84: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S85: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S86: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S87: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S88: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S89: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S90: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S91: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S92: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S93: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S94: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S95: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S96: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S97: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S98: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S99: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S100: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S101: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S102: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S103: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S104: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S105: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S106: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S107: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S108: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S109: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S110: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S111: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S112: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S113: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S114: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S115: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S116: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S117: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S118: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S119: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S120: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S121: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S122: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S123: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S124: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S125: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S126: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S127: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S128: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S129: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S130: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S131: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S132: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S133: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S134: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S135: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S136: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S137: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S138: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S139: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S140: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S141: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S142: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S143: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S144: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S145: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S146: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S147: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S148: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S149: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S150: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S151: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S152: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S153: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S154: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S155: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S156: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S157: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S158: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S159: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S160: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S161: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S162: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S163: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S164: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S165: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S166: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S167: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S168: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S169: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S170: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S171: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S172: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S173: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S174: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S175: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S176: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S177: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S178: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S179: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S180: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S181: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S182: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S183: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S184: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S185: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S186: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S187: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S188: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S189: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S190: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S191: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S192: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S193: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S194: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S195: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S196: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S197: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S198: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S199: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S200: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S201: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S202: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S203: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S204: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S205: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S206: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S207: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S208: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S209: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S210: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S211: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S212: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S213: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S214: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S215: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S216: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S217: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S218: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S219: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S220: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S221: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S222: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S223: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S224: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S225: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S226: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S227: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S228: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S229: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S230: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался
- T-0061-S231: раунд smaB-dd30d015: B+ph1+ph2, коммит не делался

## T-0062 — DONE

Проверка 3 — прагматика японских реплик (Semantic Audit C), тома 7-13, раунд smaC-20261119

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0062-S1 | sma-c | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.sma-c.md` |
| T-0062-S2 | analyzer-phase1 | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.analyzer-phase1.md` |
| T-0062-S3 | analyzer-phase2 | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.analyzer-phase2.md` |
| T-0062-S4 | sma-c | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.sma-c.md` |
| T-0062-S5 | analyzer-phase1 | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.analyzer-phase1.md` |
| T-0062-S6 | analyzer-phase2 | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.analyzer-phase2.md` |
| T-0062-S7 | sma-c | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.sma-c.md` |
| T-0062-S8 | analyzer-phase1 | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.analyzer-phase1.md` |
| T-0062-S9 | analyzer-phase2 | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.analyzer-phase2.md` |
| T-0062-S10 | sma-c | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.sma-c.md` |
| T-0062-S11 | analyzer-phase1 | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.analyzer-phase1.md` |
| T-0062-S12 | analyzer-phase2 | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.analyzer-phase2.md` |
| T-0062-S13 | sma-c | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.sma-c.md` |
| T-0062-S14 | analyzer-phase1 | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.analyzer-phase1.md` |
| T-0062-S15 | analyzer-phase2 | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.analyzer-phase2.md` |
| T-0062-S16 | sma-c | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.sma-c.md` |
| T-0062-S17 | analyzer-phase1 | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.analyzer-phase1.md` |
| T-0062-S18 | analyzer-phase2 | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.analyzer-phase2.md` |
| T-0062-S19 | sma-c | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.sma-c.md` |
| T-0062-S20 | analyzer-phase1 | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.analyzer-phase1.md` |
| T-0062-S21 | analyzer-phase2 | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.analyzer-phase2.md` |
| T-0062-S22 | sma-c | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.sma-c.md` |
| T-0062-S23 | analyzer-phase1 | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.analyzer-phase1.md` |
| T-0062-S24 | analyzer-phase2 | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.analyzer-phase2.md` |
| T-0062-S25 | sma-c | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.sma-c.md` |
| T-0062-S26 | analyzer-phase1 | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.analyzer-phase1.md` |
| T-0062-S27 | analyzer-phase2 | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.analyzer-phase2.md` |
| T-0062-S28 | sma-c | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.sma-c.md` |
| T-0062-S29 | analyzer-phase1 | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.analyzer-phase1.md` |
| T-0062-S30 | analyzer-phase2 | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.analyzer-phase2.md` |
| T-0062-S31 | sma-c | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.sma-c.md` |
| T-0062-S32 | analyzer-phase1 | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.analyzer-phase1.md` |
| T-0062-S33 | analyzer-phase2 | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.analyzer-phase2.md` |
| T-0062-S34 | sma-c | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.sma-c.md` |
| T-0062-S35 | analyzer-phase1 | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.analyzer-phase1.md` |
| T-0062-S36 | analyzer-phase2 | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.analyzer-phase2.md` |
| T-0062-S37 | sma-c | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.sma-c.md` |
| T-0062-S38 | analyzer-phase1 | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.analyzer-phase1.md` |
| T-0062-S39 | analyzer-phase2 | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.analyzer-phase2.md` |
| T-0062-S40 | sma-c | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.sma-c.md` |
| T-0062-S41 | analyzer-phase1 | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.analyzer-phase1.md` |
| T-0062-S42 | analyzer-phase2 | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.analyzer-phase2.md` |
| T-0062-S43 | sma-c | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.sma-c.md` |
| T-0062-S44 | analyzer-phase1 | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.analyzer-phase1.md` |
| T-0062-S45 | analyzer-phase2 | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.analyzer-phase2.md` |
| T-0062-S46 | sma-c | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.sma-c.md` |
| T-0062-S47 | analyzer-phase1 | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.analyzer-phase1.md` |
| T-0062-S48 | analyzer-phase2 | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.analyzer-phase2.md` |
| T-0062-S49 | sma-c | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.sma-c.md` |
| T-0062-S50 | analyzer-phase1 | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.analyzer-phase1.md` |
| T-0062-S51 | analyzer-phase2 | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.analyzer-phase2.md` |
| T-0062-S52 | sma-c | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.sma-c.md` |
| T-0062-S53 | analyzer-phase1 | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.analyzer-phase1.md` |
| T-0062-S54 | analyzer-phase2 | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.analyzer-phase2.md` |
| T-0062-S55 | sma-c | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.sma-c.md` |
| T-0062-S56 | analyzer-phase1 | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.analyzer-phase1.md` |
| T-0062-S57 | analyzer-phase2 | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.analyzer-phase2.md` |
| T-0062-S58 | sma-c | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.sma-c.md` |
| T-0062-S59 | analyzer-phase1 | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.analyzer-phase1.md` |
| T-0062-S60 | analyzer-phase2 | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.analyzer-phase2.md` |
| T-0062-S61 | sma-c | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.sma-c.md` |
| T-0062-S62 | analyzer-phase1 | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.analyzer-phase1.md` |
| T-0062-S63 | analyzer-phase2 | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.analyzer-phase2.md` |
| T-0062-S64 | sma-c | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.sma-c.md` |
| T-0062-S65 | analyzer-phase1 | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.analyzer-phase1.md` |
| T-0062-S66 | analyzer-phase2 | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.analyzer-phase2.md` |
| T-0062-S67 | sma-c | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.sma-c.md` |
| T-0062-S68 | analyzer-phase1 | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.analyzer-phase1.md` |
| T-0062-S69 | analyzer-phase2 | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.analyzer-phase2.md` |
| T-0062-S70 | sma-c | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.sma-c.md` |
| T-0062-S71 | analyzer-phase1 | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.analyzer-phase1.md` |
| T-0062-S72 | analyzer-phase2 | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.analyzer-phase2.md` |
| T-0062-S73 | sma-c | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.sma-c.md` |
| T-0062-S74 | analyzer-phase1 | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.analyzer-phase1.md` |
| T-0062-S75 | analyzer-phase2 | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.analyzer-phase2.md` |
| T-0062-S76 | sma-c | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.sma-c.md` |
| T-0062-S77 | analyzer-phase1 | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.analyzer-phase1.md` |
| T-0062-S78 | analyzer-phase2 | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.analyzer-phase2.md` |
| T-0062-S79 | sma-c | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.sma-c.md` |
| T-0062-S80 | analyzer-phase1 | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.analyzer-phase1.md` |
| T-0062-S81 | analyzer-phase2 | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.analyzer-phase2.md` |
| T-0062-S82 | sma-c | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.sma-c.md` |
| T-0062-S83 | analyzer-phase1 | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.analyzer-phase1.md` |
| T-0062-S84 | analyzer-phase2 | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.analyzer-phase2.md` |
| T-0062-S85 | sma-c | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.sma-c.md` |
| T-0062-S86 | analyzer-phase1 | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.analyzer-phase1.md` |
| T-0062-S87 | analyzer-phase2 | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.analyzer-phase2.md` |
| T-0062-S88 | sma-c | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.sma-c.md` |
| T-0062-S89 | analyzer-phase1 | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.analyzer-phase1.md` |
| T-0062-S90 | analyzer-phase2 | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.analyzer-phase2.md` |
| T-0062-S91 | sma-c | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.sma-c.md` |
| T-0062-S92 | analyzer-phase1 | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.analyzer-phase1.md` |
| T-0062-S93 | analyzer-phase2 | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.analyzer-phase2.md` |
| T-0062-S94 | sma-c | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.sma-c.md` |
| T-0062-S95 | analyzer-phase1 | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.analyzer-phase1.md` |
| T-0062-S96 | analyzer-phase2 | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.analyzer-phase2.md` |
| T-0062-S97 | sma-c | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.sma-c.md` |
| T-0062-S98 | analyzer-phase1 | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.analyzer-phase1.md` |
| T-0062-S99 | analyzer-phase2 | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.analyzer-phase2.md` |
| T-0062-S100 | sma-c | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.sma-c.md` |
| T-0062-S101 | analyzer-phase1 | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.analyzer-phase1.md` |
| T-0062-S102 | analyzer-phase2 | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.analyzer-phase2.md` |
| T-0062-S103 | sma-c | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.sma-c.md` |
| T-0062-S104 | analyzer-phase1 | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.analyzer-phase1.md` |
| T-0062-S105 | analyzer-phase2 | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.analyzer-phase2.md` |
| T-0062-S106 | sma-c | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.sma-c.md` |
| T-0062-S107 | analyzer-phase1 | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.analyzer-phase1.md` |
| T-0062-S108 | analyzer-phase2 | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.analyzer-phase2.md` |
| T-0062-S109 | sma-c | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.sma-c.md` |
| T-0062-S110 | analyzer-phase1 | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.analyzer-phase1.md` |
| T-0062-S111 | analyzer-phase2 | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.analyzer-phase2.md` |
| T-0062-S112 | sma-c | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.sma-c.md` |
| T-0062-S113 | analyzer-phase1 | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.analyzer-phase1.md` |
| T-0062-S114 | analyzer-phase2 | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.analyzer-phase2.md` |
| T-0062-S115 | sma-c | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.sma-c.md` |
| T-0062-S116 | analyzer-phase1 | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.analyzer-phase1.md` |
| T-0062-S117 | analyzer-phase2 | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.analyzer-phase2.md` |
| T-0062-S118 | sma-c | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.sma-c.md` |
| T-0062-S119 | analyzer-phase1 | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.analyzer-phase1.md` |
| T-0062-S120 | analyzer-phase2 | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.analyzer-phase2.md` |
| T-0062-S121 | sma-c | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.sma-c.md` |
| T-0062-S122 | analyzer-phase1 | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.analyzer-phase1.md` |
| T-0062-S123 | analyzer-phase2 | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.analyzer-phase2.md` |
| T-0062-S124 | sma-c | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.sma-c.md` |
| T-0062-S125 | analyzer-phase1 | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.analyzer-phase1.md` |
| T-0062-S126 | analyzer-phase2 | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.analyzer-phase2.md` |
| T-0062-S127 | sma-c | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.sma-c.md` |
| T-0062-S128 | analyzer-phase1 | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.analyzer-phase1.md` |
| T-0062-S129 | analyzer-phase2 | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.analyzer-phase2.md` |
| T-0062-S130 | sma-c | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.sma-c.md` |
| T-0062-S131 | analyzer-phase1 | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.analyzer-phase1.md` |
| T-0062-S132 | analyzer-phase2 | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.analyzer-phase2.md` |
| T-0062-S133 | sma-c | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.sma-c.md` |
| T-0062-S134 | analyzer-phase1 | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.analyzer-phase1.md` |
| T-0062-S135 | analyzer-phase2 | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.analyzer-phase2.md` |
| T-0062-S136 | sma-c | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.sma-c.md` |
| T-0062-S137 | analyzer-phase1 | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.analyzer-phase1.md` |
| T-0062-S138 | analyzer-phase2 | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.analyzer-phase2.md` |
| T-0062-S139 | sma-c | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.sma-c.md` |
| T-0062-S140 | analyzer-phase1 | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.analyzer-phase1.md` |
| T-0062-S141 | analyzer-phase2 | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.analyzer-phase2.md` |
| T-0062-S142 | sma-c | v11-afterword | done | 2 | `agent_prompts/agent_prompt.v11-afterword.sma-c.attempt2.md` |
| T-0062-S143 | analyzer-phase1 | v11-afterword | done | 2 | `agent_prompts/agent_prompt.v11-afterword.analyzer-phase1.attempt2.md` |
| T-0062-S144 | analyzer-phase2 | v11-afterword | done | 2 | `agent_prompts/agent_prompt.v11-afterword.analyzer-phase2.attempt2.md` |
| T-0062-S145 | sma-c | v11-ch01 | done | 2 | `agent_prompts/agent_prompt.v11-ch01.sma-c.attempt2.md` |
| T-0062-S146 | analyzer-phase1 | v11-ch01 | done | 2 | `agent_prompts/agent_prompt.v11-ch01.analyzer-phase1.attempt2.md` |
| T-0062-S147 | analyzer-phase2 | v11-ch01 | done | 2 | `agent_prompts/agent_prompt.v11-ch01.analyzer-phase2.attempt2.md` |
| T-0062-S148 | sma-c | v11-ch02 | done | 2 | `agent_prompts/agent_prompt.v11-ch02.sma-c.attempt2.md` |
| T-0062-S149 | analyzer-phase1 | v11-ch02 | done | 2 | `agent_prompts/agent_prompt.v11-ch02.analyzer-phase1.attempt2.md` |
| T-0062-S150 | analyzer-phase2 | v11-ch02 | done | 2 | `agent_prompts/agent_prompt.v11-ch02.analyzer-phase2.attempt2.md` |
| T-0062-S151 | sma-c | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.sma-c.md` |
| T-0062-S152 | analyzer-phase1 | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.analyzer-phase1.md` |
| T-0062-S153 | analyzer-phase2 | v11-ch03 | done | 2 | `agent_prompts/agent_prompt.v11-ch03.analyzer-phase2.attempt2.md` |
| T-0062-S154 | sma-c | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.sma-c.md` |
| T-0062-S155 | analyzer-phase1 | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.analyzer-phase1.md` |
| T-0062-S156 | analyzer-phase2 | v11-ch04 | done | 2 | `agent_prompts/agent_prompt.v11-ch04.analyzer-phase2.attempt2.md` |
| T-0062-S157 | sma-c | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.sma-c.md` |
| T-0062-S158 | analyzer-phase1 | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.analyzer-phase1.md` |
| T-0062-S159 | analyzer-phase2 | v11-ch05 | done | 2 | `agent_prompts/agent_prompt.v11-ch05.analyzer-phase2.attempt2.md` |
| T-0062-S160 | sma-c | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.sma-c.md` |
| T-0062-S161 | analyzer-phase1 | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.analyzer-phase1.md` |
| T-0062-S162 | analyzer-phase2 | v11-ch06 | done | 2 | `agent_prompts/agent_prompt.v11-ch06.analyzer-phase2.attempt2.md` |
| T-0062-S163 | sma-c | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.sma-c.md` |
| T-0062-S164 | analyzer-phase1 | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.analyzer-phase1.md` |
| T-0062-S165 | analyzer-phase2 | v11-ch07 | done | 2 | `agent_prompts/agent_prompt.v11-ch07.analyzer-phase2.attempt2.md` |
| T-0062-S166 | sma-c | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.sma-c.md` |
| T-0062-S167 | analyzer-phase1 | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.analyzer-phase1.md` |
| T-0062-S168 | analyzer-phase2 | v11-ch08 | done | 2 | `agent_prompts/agent_prompt.v11-ch08.analyzer-phase2.attempt2.md` |
| T-0062-S169 | sma-c | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.sma-c.md` |
| T-0062-S170 | analyzer-phase1 | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.analyzer-phase1.md` |
| T-0062-S171 | analyzer-phase2 | v11-ch09 | done | 2 | `agent_prompts/agent_prompt.v11-ch09.analyzer-phase2.attempt2.md` |
| T-0062-S172 | sma-c | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.sma-c.md` |
| T-0062-S173 | analyzer-phase1 | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.analyzer-phase1.md` |
| T-0062-S174 | analyzer-phase2 | v11-ch10 | done | 2 | `agent_prompts/agent_prompt.v11-ch10.analyzer-phase2.attempt2.md` |
| T-0062-S175 | sma-c | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.sma-c.md` |
| T-0062-S176 | analyzer-phase1 | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.analyzer-phase1.md` |
| T-0062-S177 | analyzer-phase2 | v11-epilogue | done | 2 | `agent_prompts/agent_prompt.v11-epilogue.analyzer-phase2.attempt2.md` |
| T-0062-S178 | sma-c | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.sma-c.md` |
| T-0062-S179 | analyzer-phase1 | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.analyzer-phase1.md` |
| T-0062-S180 | analyzer-phase2 | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.analyzer-phase2.md` |
| T-0062-S181 | sma-c | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.sma-c.md` |
| T-0062-S182 | analyzer-phase1 | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.analyzer-phase1.md` |
| T-0062-S183 | analyzer-phase2 | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.analyzer-phase2.md` |
| T-0062-S184 | sma-c | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.sma-c.md` |
| T-0062-S185 | analyzer-phase1 | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.analyzer-phase1.md` |
| T-0062-S186 | analyzer-phase2 | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.analyzer-phase2.md` |
| T-0062-S187 | sma-c | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.sma-c.md` |
| T-0062-S188 | analyzer-phase1 | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.analyzer-phase1.md` |
| T-0062-S189 | analyzer-phase2 | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.analyzer-phase2.md` |
| T-0062-S190 | sma-c | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.sma-c.md` |
| T-0062-S191 | analyzer-phase1 | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.analyzer-phase1.md` |
| T-0062-S192 | analyzer-phase2 | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.analyzer-phase2.md` |
| T-0062-S193 | sma-c | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.sma-c.md` |
| T-0062-S194 | analyzer-phase1 | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.analyzer-phase1.md` |
| T-0062-S195 | analyzer-phase2 | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.analyzer-phase2.md` |
| T-0062-S196 | sma-c | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.sma-c.md` |
| T-0062-S197 | analyzer-phase1 | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.analyzer-phase1.md` |
| T-0062-S198 | analyzer-phase2 | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.analyzer-phase2.md` |
| T-0062-S199 | sma-c | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.sma-c.md` |
| T-0062-S200 | analyzer-phase1 | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.analyzer-phase1.md` |
| T-0062-S201 | analyzer-phase2 | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.analyzer-phase2.md` |
| T-0062-S202 | sma-c | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.sma-c.md` |
| T-0062-S203 | analyzer-phase1 | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.analyzer-phase1.md` |
| T-0062-S204 | analyzer-phase2 | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.analyzer-phase2.md` |
| T-0062-S205 | sma-c | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.sma-c.md` |
| T-0062-S206 | analyzer-phase1 | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.analyzer-phase1.md` |
| T-0062-S207 | analyzer-phase2 | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.analyzer-phase2.md` |
| T-0062-S208 | sma-c | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.sma-c.md` |
| T-0062-S209 | analyzer-phase1 | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.analyzer-phase1.md` |
| T-0062-S210 | analyzer-phase2 | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.analyzer-phase2.md` |
| T-0062-S211 | sma-c | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.sma-c.md` |
| T-0062-S212 | analyzer-phase1 | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.analyzer-phase1.md` |
| T-0062-S213 | analyzer-phase2 | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.analyzer-phase2.md` |
| T-0062-S214 | sma-c | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.sma-c.md` |
| T-0062-S215 | analyzer-phase1 | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.analyzer-phase1.md` |
| T-0062-S216 | analyzer-phase2 | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.analyzer-phase2.md` |
| T-0062-S217 | sma-c | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.sma-c.md` |
| T-0062-S218 | analyzer-phase1 | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.analyzer-phase1.md` |
| T-0062-S219 | analyzer-phase2 | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.analyzer-phase2.md` |
| T-0062-S220 | sma-c | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.sma-c.md` |
| T-0062-S221 | analyzer-phase1 | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.analyzer-phase1.md` |
| T-0062-S222 | analyzer-phase2 | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.analyzer-phase2.md` |
| T-0062-S223 | sma-c | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.sma-c.md` |
| T-0062-S224 | analyzer-phase1 | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.analyzer-phase1.md` |
| T-0062-S225 | analyzer-phase2 | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.analyzer-phase2.md` |
| T-0062-S226 | sma-c | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.sma-c.md` |
| T-0062-S227 | analyzer-phase1 | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.analyzer-phase1.md` |
| T-0062-S228 | analyzer-phase2 | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.analyzer-phase2.md` |
| T-0062-S229 | sma-c | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.sma-c.md` |
| T-0062-S230 | analyzer-phase1 | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.analyzer-phase1.md` |
| T-0062-S231 | analyzer-phase2 | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.analyzer-phase2.md` |

Заметки:
- T-0062-S1: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S2: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S3: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S4: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S5: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S6: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S7: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S8: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S9: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S10: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S11: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S12: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S13: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S14: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S15: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S16: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S17: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S18: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S19: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S20: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S21: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S22: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S23: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S24: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S25: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S26: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S27: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S28: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S29: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S30: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S31: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S32: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S33: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S34: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S35: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S36: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S37: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S38: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S39: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S40: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S41: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S42: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S43: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S44: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S45: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S46: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S47: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S48: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S49: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S50: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S51: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S52: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S53: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S54: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S55: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S56: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S57: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S58: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S59: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S60: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S61: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S62: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S63: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S64: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S65: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S66: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S67: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S68: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S69: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S70: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S71: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S72: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S73: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S74: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S75: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S76: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S77: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S78: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S79: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S80: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S81: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S82: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S83: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S84: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S85: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S86: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S87: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S88: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S89: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S90: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S91: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S92: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S93: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S94: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S95: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S96: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S97: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S98: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S99: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S100: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S101: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S102: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S103: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S104: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S105: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S106: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S107: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S108: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S109: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S110: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S111: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S112: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S113: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S114: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S115: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S116: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S117: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S118: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S119: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S120: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S121: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S122: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S123: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S124: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S125: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S126: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S127: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S128: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S129: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S130: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S131: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S132: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S133: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S134: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S135: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S136: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S137: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S138: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S139: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S140: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S141: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S142: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S143: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S144: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S145: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S146: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S147: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S148: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S149: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S150: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S151: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S152: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S153: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S154: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S155: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S156: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S157: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S158: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S159: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S160: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S161: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S162: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S163: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S164: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S165: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S166: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S167: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S168: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S169: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S170: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S171: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S172: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S173: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S174: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S175: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S176: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S177: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S178: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S179: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S180: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S181: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S182: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S183: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S184: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S185: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S186: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S187: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S188: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S189: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S190: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S191: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S192: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S193: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S194: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S195: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S196: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S197: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S198: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S199: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S200: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S201: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S202: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S203: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S204: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S205: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S206: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S207: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S208: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S209: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S210: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S211: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S212: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S213: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S214: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S215: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S216: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S217: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S218: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S219: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S220: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S221: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S222: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S223: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S224: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S225: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S226: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S227: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S228: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S229: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S230: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался
- T-0062-S231: раунд smaC-a77bc132: C+ph1+ph2, коммит не делался

## T-0063 — DONE

Проверка 4 — полный независимый смысловой аудит A+B+C+Analyzer, тома 7-13, раунд fullABC-20261119

| ID | Режим | Глава | Статус | Попыток | Промпт |
| --- | --- | --- | --- | --- | --- |
| T-0063-S1 | sma-a | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.sma-a.md` |
| T-0063-S2 | sma-b | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.sma-b.md` |
| T-0063-S3 | sma-c | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.sma-c.md` |
| T-0063-S4 | analyzer-phase1 | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.analyzer-phase1.md` |
| T-0063-S5 | analyzer-phase2 | v07-afterword | done | 1 | `agent_prompts/agent_prompt.v07-afterword.analyzer-phase2.md` |
| T-0063-S6 | sma-a | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.sma-a.md` |
| T-0063-S7 | sma-b | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.sma-b.md` |
| T-0063-S8 | sma-c | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.sma-c.md` |
| T-0063-S9 | analyzer-phase1 | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.analyzer-phase1.md` |
| T-0063-S10 | analyzer-phase2 | v07-ch01 | done | 1 | `agent_prompts/agent_prompt.v07-ch01.analyzer-phase2.md` |
| T-0063-S11 | sma-a | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.sma-a.md` |
| T-0063-S12 | sma-b | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.sma-b.md` |
| T-0063-S13 | sma-c | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.sma-c.md` |
| T-0063-S14 | analyzer-phase1 | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.analyzer-phase1.md` |
| T-0063-S15 | analyzer-phase2 | v07-ch02 | done | 1 | `agent_prompts/agent_prompt.v07-ch02.analyzer-phase2.md` |
| T-0063-S16 | sma-a | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.sma-a.md` |
| T-0063-S17 | sma-b | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.sma-b.md` |
| T-0063-S18 | sma-c | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.sma-c.md` |
| T-0063-S19 | analyzer-phase1 | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.analyzer-phase1.md` |
| T-0063-S20 | analyzer-phase2 | v07-ch03 | done | 1 | `agent_prompts/agent_prompt.v07-ch03.analyzer-phase2.md` |
| T-0063-S21 | sma-a | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.sma-a.md` |
| T-0063-S22 | sma-b | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.sma-b.md` |
| T-0063-S23 | sma-c | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.sma-c.md` |
| T-0063-S24 | analyzer-phase1 | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.analyzer-phase1.md` |
| T-0063-S25 | analyzer-phase2 | v07-ch04 | done | 1 | `agent_prompts/agent_prompt.v07-ch04.analyzer-phase2.md` |
| T-0063-S26 | sma-a | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.sma-a.md` |
| T-0063-S27 | sma-b | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.sma-b.md` |
| T-0063-S28 | sma-c | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.sma-c.md` |
| T-0063-S29 | analyzer-phase1 | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.analyzer-phase1.md` |
| T-0063-S30 | analyzer-phase2 | v07-ch05 | done | 1 | `agent_prompts/agent_prompt.v07-ch05.analyzer-phase2.md` |
| T-0063-S31 | sma-a | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.sma-a.md` |
| T-0063-S32 | sma-b | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.sma-b.md` |
| T-0063-S33 | sma-c | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.sma-c.md` |
| T-0063-S34 | analyzer-phase1 | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.analyzer-phase1.md` |
| T-0063-S35 | analyzer-phase2 | v07-ch06 | done | 1 | `agent_prompts/agent_prompt.v07-ch06.analyzer-phase2.md` |
| T-0063-S36 | sma-a | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.sma-a.md` |
| T-0063-S37 | sma-b | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.sma-b.md` |
| T-0063-S38 | sma-c | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.sma-c.md` |
| T-0063-S39 | analyzer-phase1 | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.analyzer-phase1.md` |
| T-0063-S40 | analyzer-phase2 | v07-ch07 | done | 1 | `agent_prompts/agent_prompt.v07-ch07.analyzer-phase2.md` |
| T-0063-S41 | sma-a | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.sma-a.md` |
| T-0063-S42 | sma-b | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.sma-b.md` |
| T-0063-S43 | sma-c | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.sma-c.md` |
| T-0063-S44 | analyzer-phase1 | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.analyzer-phase1.md` |
| T-0063-S45 | analyzer-phase2 | v07-ch08 | done | 1 | `agent_prompts/agent_prompt.v07-ch08.analyzer-phase2.md` |
| T-0063-S46 | sma-a | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.sma-a.md` |
| T-0063-S47 | sma-b | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.sma-b.md` |
| T-0063-S48 | sma-c | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.sma-c.md` |
| T-0063-S49 | analyzer-phase1 | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.analyzer-phase1.md` |
| T-0063-S50 | analyzer-phase2 | v07-ch09 | done | 1 | `agent_prompts/agent_prompt.v07-ch09.analyzer-phase2.md` |
| T-0063-S51 | sma-a | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.sma-a.md` |
| T-0063-S52 | sma-b | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.sma-b.md` |
| T-0063-S53 | sma-c | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.sma-c.md` |
| T-0063-S54 | analyzer-phase1 | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.analyzer-phase1.md` |
| T-0063-S55 | analyzer-phase2 | v07-ch10 | done | 1 | `agent_prompts/agent_prompt.v07-ch10.analyzer-phase2.md` |
| T-0063-S56 | sma-a | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.sma-a.md` |
| T-0063-S57 | sma-b | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.sma-b.md` |
| T-0063-S58 | sma-c | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.sma-c.md` |
| T-0063-S59 | analyzer-phase1 | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.analyzer-phase1.md` |
| T-0063-S60 | analyzer-phase2 | v07-epilogue | done | 1 | `agent_prompts/agent_prompt.v07-epilogue.analyzer-phase2.md` |
| T-0063-S61 | sma-a | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.sma-a.md` |
| T-0063-S62 | sma-b | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.sma-b.md` |
| T-0063-S63 | sma-c | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.sma-c.md` |
| T-0063-S64 | analyzer-phase1 | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.analyzer-phase1.md` |
| T-0063-S65 | analyzer-phase2 | v08-afterword | done | 1 | `agent_prompts/agent_prompt.v08-afterword.analyzer-phase2.md` |
| T-0063-S66 | sma-a | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.sma-a.md` |
| T-0063-S67 | sma-b | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.sma-b.md` |
| T-0063-S68 | sma-c | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.sma-c.md` |
| T-0063-S69 | analyzer-phase1 | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.analyzer-phase1.md` |
| T-0063-S70 | analyzer-phase2 | v08-ch01 | done | 1 | `agent_prompts/agent_prompt.v08-ch01.analyzer-phase2.md` |
| T-0063-S71 | sma-a | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.sma-a.md` |
| T-0063-S72 | sma-b | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.sma-b.md` |
| T-0063-S73 | sma-c | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.sma-c.md` |
| T-0063-S74 | analyzer-phase1 | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.analyzer-phase1.md` |
| T-0063-S75 | analyzer-phase2 | v08-ch02 | done | 1 | `agent_prompts/agent_prompt.v08-ch02.analyzer-phase2.md` |
| T-0063-S76 | sma-a | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.sma-a.md` |
| T-0063-S77 | sma-b | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.sma-b.md` |
| T-0063-S78 | sma-c | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.sma-c.md` |
| T-0063-S79 | analyzer-phase1 | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.analyzer-phase1.md` |
| T-0063-S80 | analyzer-phase2 | v08-ch03 | done | 1 | `agent_prompts/agent_prompt.v08-ch03.analyzer-phase2.md` |
| T-0063-S81 | sma-a | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.sma-a.md` |
| T-0063-S82 | sma-b | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.sma-b.md` |
| T-0063-S83 | sma-c | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.sma-c.md` |
| T-0063-S84 | analyzer-phase1 | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.analyzer-phase1.md` |
| T-0063-S85 | analyzer-phase2 | v08-ch04 | done | 1 | `agent_prompts/agent_prompt.v08-ch04.analyzer-phase2.md` |
| T-0063-S86 | sma-a | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.sma-a.md` |
| T-0063-S87 | sma-b | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.sma-b.md` |
| T-0063-S88 | sma-c | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.sma-c.md` |
| T-0063-S89 | analyzer-phase1 | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.analyzer-phase1.md` |
| T-0063-S90 | analyzer-phase2 | v08-ch05 | done | 1 | `agent_prompts/agent_prompt.v08-ch05.analyzer-phase2.md` |
| T-0063-S91 | sma-a | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.sma-a.md` |
| T-0063-S92 | sma-b | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.sma-b.md` |
| T-0063-S93 | sma-c | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.sma-c.md` |
| T-0063-S94 | analyzer-phase1 | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.analyzer-phase1.md` |
| T-0063-S95 | analyzer-phase2 | v08-ch06 | done | 1 | `agent_prompts/agent_prompt.v08-ch06.analyzer-phase2.md` |
| T-0063-S96 | sma-a | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.sma-a.md` |
| T-0063-S97 | sma-b | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.sma-b.md` |
| T-0063-S98 | sma-c | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.sma-c.md` |
| T-0063-S99 | analyzer-phase1 | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.analyzer-phase1.md` |
| T-0063-S100 | analyzer-phase2 | v08-ch07 | done | 1 | `agent_prompts/agent_prompt.v08-ch07.analyzer-phase2.md` |
| T-0063-S101 | sma-a | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.sma-a.md` |
| T-0063-S102 | sma-b | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.sma-b.md` |
| T-0063-S103 | sma-c | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.sma-c.md` |
| T-0063-S104 | analyzer-phase1 | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.analyzer-phase1.md` |
| T-0063-S105 | analyzer-phase2 | v08-ch08 | done | 1 | `agent_prompts/agent_prompt.v08-ch08.analyzer-phase2.md` |
| T-0063-S106 | sma-a | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.sma-a.md` |
| T-0063-S107 | sma-b | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.sma-b.md` |
| T-0063-S108 | sma-c | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.sma-c.md` |
| T-0063-S109 | analyzer-phase1 | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.analyzer-phase1.md` |
| T-0063-S110 | analyzer-phase2 | v08-ch09 | done | 1 | `agent_prompts/agent_prompt.v08-ch09.analyzer-phase2.md` |
| T-0063-S111 | sma-a | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.sma-a.md` |
| T-0063-S112 | sma-b | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.sma-b.md` |
| T-0063-S113 | sma-c | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.sma-c.md` |
| T-0063-S114 | analyzer-phase1 | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.analyzer-phase1.md` |
| T-0063-S115 | analyzer-phase2 | v08-ch10 | done | 1 | `agent_prompts/agent_prompt.v08-ch10.analyzer-phase2.md` |
| T-0063-S116 | sma-a | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.sma-a.md` |
| T-0063-S117 | sma-b | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.sma-b.md` |
| T-0063-S118 | sma-c | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.sma-c.md` |
| T-0063-S119 | analyzer-phase1 | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.analyzer-phase1.md` |
| T-0063-S120 | analyzer-phase2 | v08-epilogue | done | 1 | `agent_prompts/agent_prompt.v08-epilogue.analyzer-phase2.md` |
| T-0063-S121 | sma-a | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.sma-a.md` |
| T-0063-S122 | sma-b | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.sma-b.md` |
| T-0063-S123 | sma-c | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.sma-c.md` |
| T-0063-S124 | analyzer-phase1 | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.analyzer-phase1.md` |
| T-0063-S125 | analyzer-phase2 | v09-afterword | done | 1 | `agent_prompts/agent_prompt.v09-afterword.analyzer-phase2.md` |
| T-0063-S126 | sma-a | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.sma-a.md` |
| T-0063-S127 | sma-b | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.sma-b.md` |
| T-0063-S128 | sma-c | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.sma-c.md` |
| T-0063-S129 | analyzer-phase1 | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.analyzer-phase1.md` |
| T-0063-S130 | analyzer-phase2 | v09-ch01 | done | 1 | `agent_prompts/agent_prompt.v09-ch01.analyzer-phase2.md` |
| T-0063-S131 | sma-a | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.sma-a.md` |
| T-0063-S132 | sma-b | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.sma-b.md` |
| T-0063-S133 | sma-c | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.sma-c.md` |
| T-0063-S134 | analyzer-phase1 | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.analyzer-phase1.md` |
| T-0063-S135 | analyzer-phase2 | v09-ch02 | done | 1 | `agent_prompts/agent_prompt.v09-ch02.analyzer-phase2.md` |
| T-0063-S136 | sma-a | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.sma-a.md` |
| T-0063-S137 | sma-b | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.sma-b.md` |
| T-0063-S138 | sma-c | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.sma-c.md` |
| T-0063-S139 | analyzer-phase1 | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.analyzer-phase1.md` |
| T-0063-S140 | analyzer-phase2 | v09-ch03 | done | 1 | `agent_prompts/agent_prompt.v09-ch03.analyzer-phase2.md` |
| T-0063-S141 | sma-a | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.sma-a.md` |
| T-0063-S142 | sma-b | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.sma-b.md` |
| T-0063-S143 | sma-c | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.sma-c.md` |
| T-0063-S144 | analyzer-phase1 | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.analyzer-phase1.md` |
| T-0063-S145 | analyzer-phase2 | v09-ch04 | done | 1 | `agent_prompts/agent_prompt.v09-ch04.analyzer-phase2.md` |
| T-0063-S146 | sma-a | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.sma-a.md` |
| T-0063-S147 | sma-b | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.sma-b.md` |
| T-0063-S148 | sma-c | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.sma-c.md` |
| T-0063-S149 | analyzer-phase1 | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.analyzer-phase1.md` |
| T-0063-S150 | analyzer-phase2 | v09-ch05 | done | 1 | `agent_prompts/agent_prompt.v09-ch05.analyzer-phase2.md` |
| T-0063-S151 | sma-a | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.sma-a.md` |
| T-0063-S152 | sma-b | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.sma-b.md` |
| T-0063-S153 | sma-c | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.sma-c.md` |
| T-0063-S154 | analyzer-phase1 | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.analyzer-phase1.md` |
| T-0063-S155 | analyzer-phase2 | v09-ch06 | done | 1 | `agent_prompts/agent_prompt.v09-ch06.analyzer-phase2.md` |
| T-0063-S156 | sma-a | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.sma-a.md` |
| T-0063-S157 | sma-b | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.sma-b.md` |
| T-0063-S158 | sma-c | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.sma-c.md` |
| T-0063-S159 | analyzer-phase1 | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.analyzer-phase1.md` |
| T-0063-S160 | analyzer-phase2 | v09-ch07 | done | 1 | `agent_prompts/agent_prompt.v09-ch07.analyzer-phase2.md` |
| T-0063-S161 | sma-a | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.sma-a.md` |
| T-0063-S162 | sma-b | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.sma-b.md` |
| T-0063-S163 | sma-c | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.sma-c.md` |
| T-0063-S164 | analyzer-phase1 | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.analyzer-phase1.md` |
| T-0063-S165 | analyzer-phase2 | v09-ch08 | done | 1 | `agent_prompts/agent_prompt.v09-ch08.analyzer-phase2.md` |
| T-0063-S166 | sma-a | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.sma-a.md` |
| T-0063-S167 | sma-b | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.sma-b.md` |
| T-0063-S168 | sma-c | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.sma-c.md` |
| T-0063-S169 | analyzer-phase1 | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.analyzer-phase1.md` |
| T-0063-S170 | analyzer-phase2 | v09-ch09 | done | 1 | `agent_prompts/agent_prompt.v09-ch09.analyzer-phase2.md` |
| T-0063-S171 | sma-a | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.sma-a.md` |
| T-0063-S172 | sma-b | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.sma-b.md` |
| T-0063-S173 | sma-c | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.sma-c.md` |
| T-0063-S174 | analyzer-phase1 | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.analyzer-phase1.md` |
| T-0063-S175 | analyzer-phase2 | v09-epilogue | done | 1 | `agent_prompts/agent_prompt.v09-epilogue.analyzer-phase2.md` |
| T-0063-S176 | sma-a | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.sma-a.md` |
| T-0063-S177 | sma-b | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.sma-b.md` |
| T-0063-S178 | sma-c | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.sma-c.md` |
| T-0063-S179 | analyzer-phase1 | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.analyzer-phase1.md` |
| T-0063-S180 | analyzer-phase2 | v10-afterword | done | 1 | `agent_prompts/agent_prompt.v10-afterword.analyzer-phase2.md` |
| T-0063-S181 | sma-a | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.sma-a.md` |
| T-0063-S182 | sma-b | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.sma-b.md` |
| T-0063-S183 | sma-c | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.sma-c.md` |
| T-0063-S184 | analyzer-phase1 | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.analyzer-phase1.md` |
| T-0063-S185 | analyzer-phase2 | v10-ch01 | done | 1 | `agent_prompts/agent_prompt.v10-ch01.analyzer-phase2.md` |
| T-0063-S186 | sma-a | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.sma-a.md` |
| T-0063-S187 | sma-b | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.sma-b.md` |
| T-0063-S188 | sma-c | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.sma-c.md` |
| T-0063-S189 | analyzer-phase1 | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.analyzer-phase1.md` |
| T-0063-S190 | analyzer-phase2 | v10-ch02 | done | 1 | `agent_prompts/agent_prompt.v10-ch02.analyzer-phase2.md` |
| T-0063-S191 | sma-a | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.sma-a.md` |
| T-0063-S192 | sma-b | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.sma-b.md` |
| T-0063-S193 | sma-c | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.sma-c.md` |
| T-0063-S194 | analyzer-phase1 | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.analyzer-phase1.md` |
| T-0063-S195 | analyzer-phase2 | v10-ch03 | done | 1 | `agent_prompts/agent_prompt.v10-ch03.analyzer-phase2.md` |
| T-0063-S196 | sma-a | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.sma-a.md` |
| T-0063-S197 | sma-b | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.sma-b.md` |
| T-0063-S198 | sma-c | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.sma-c.md` |
| T-0063-S199 | analyzer-phase1 | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.analyzer-phase1.md` |
| T-0063-S200 | analyzer-phase2 | v10-ch04 | done | 1 | `agent_prompts/agent_prompt.v10-ch04.analyzer-phase2.md` |
| T-0063-S201 | sma-a | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.sma-a.md` |
| T-0063-S202 | sma-b | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.sma-b.md` |
| T-0063-S203 | sma-c | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.sma-c.md` |
| T-0063-S204 | analyzer-phase1 | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.analyzer-phase1.md` |
| T-0063-S205 | analyzer-phase2 | v10-ch05 | done | 1 | `agent_prompts/agent_prompt.v10-ch05.analyzer-phase2.md` |
| T-0063-S206 | sma-a | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.sma-a.md` |
| T-0063-S207 | sma-b | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.sma-b.md` |
| T-0063-S208 | sma-c | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.sma-c.md` |
| T-0063-S209 | analyzer-phase1 | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.analyzer-phase1.md` |
| T-0063-S210 | analyzer-phase2 | v10-ch06 | done | 1 | `agent_prompts/agent_prompt.v10-ch06.analyzer-phase2.md` |
| T-0063-S211 | sma-a | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.sma-a.md` |
| T-0063-S212 | sma-b | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.sma-b.md` |
| T-0063-S213 | sma-c | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.sma-c.md` |
| T-0063-S214 | analyzer-phase1 | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.analyzer-phase1.md` |
| T-0063-S215 | analyzer-phase2 | v10-ch07 | done | 1 | `agent_prompts/agent_prompt.v10-ch07.analyzer-phase2.md` |
| T-0063-S216 | sma-a | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.sma-a.md` |
| T-0063-S217 | sma-b | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.sma-b.md` |
| T-0063-S218 | sma-c | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.sma-c.md` |
| T-0063-S219 | analyzer-phase1 | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.analyzer-phase1.md` |
| T-0063-S220 | analyzer-phase2 | v10-ch08 | done | 1 | `agent_prompts/agent_prompt.v10-ch08.analyzer-phase2.md` |
| T-0063-S221 | sma-a | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.sma-a.md` |
| T-0063-S222 | sma-b | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.sma-b.md` |
| T-0063-S223 | sma-c | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.sma-c.md` |
| T-0063-S224 | analyzer-phase1 | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.analyzer-phase1.md` |
| T-0063-S225 | analyzer-phase2 | v10-ch09 | done | 1 | `agent_prompts/agent_prompt.v10-ch09.analyzer-phase2.md` |
| T-0063-S226 | sma-a | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.sma-a.md` |
| T-0063-S227 | sma-b | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.sma-b.md` |
| T-0063-S228 | sma-c | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.sma-c.md` |
| T-0063-S229 | analyzer-phase1 | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.analyzer-phase1.md` |
| T-0063-S230 | analyzer-phase2 | v10-ch10 | done | 1 | `agent_prompts/agent_prompt.v10-ch10.analyzer-phase2.md` |
| T-0063-S231 | sma-a | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.sma-a.md` |
| T-0063-S232 | sma-b | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.sma-b.md` |
| T-0063-S233 | sma-c | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.sma-c.md` |
| T-0063-S234 | analyzer-phase1 | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.analyzer-phase1.md` |
| T-0063-S235 | analyzer-phase2 | v10-epilogue | done | 1 | `agent_prompts/agent_prompt.v10-epilogue.analyzer-phase2.md` |
| T-0063-S236 | sma-a | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.sma-a.md` |
| T-0063-S237 | sma-b | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.sma-b.md` |
| T-0063-S238 | sma-c | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.sma-c.md` |
| T-0063-S239 | analyzer-phase1 | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.analyzer-phase1.md` |
| T-0063-S240 | analyzer-phase2 | v11-afterword | done | 1 | `agent_prompts/agent_prompt.v11-afterword.analyzer-phase2.md` |
| T-0063-S241 | sma-a | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.sma-a.md` |
| T-0063-S242 | sma-b | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.sma-b.md` |
| T-0063-S243 | sma-c | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.sma-c.md` |
| T-0063-S244 | analyzer-phase1 | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.analyzer-phase1.md` |
| T-0063-S245 | analyzer-phase2 | v11-ch01 | done | 1 | `agent_prompts/agent_prompt.v11-ch01.analyzer-phase2.md` |
| T-0063-S246 | sma-a | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.sma-a.md` |
| T-0063-S247 | sma-b | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.sma-b.md` |
| T-0063-S248 | sma-c | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.sma-c.md` |
| T-0063-S249 | analyzer-phase1 | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.analyzer-phase1.md` |
| T-0063-S250 | analyzer-phase2 | v11-ch02 | done | 1 | `agent_prompts/agent_prompt.v11-ch02.analyzer-phase2.md` |
| T-0063-S251 | sma-a | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.sma-a.md` |
| T-0063-S252 | sma-b | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.sma-b.md` |
| T-0063-S253 | sma-c | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.sma-c.md` |
| T-0063-S254 | analyzer-phase1 | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.analyzer-phase1.md` |
| T-0063-S255 | analyzer-phase2 | v11-ch03 | done | 1 | `agent_prompts/agent_prompt.v11-ch03.analyzer-phase2.md` |
| T-0063-S256 | sma-a | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.sma-a.md` |
| T-0063-S257 | sma-b | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.sma-b.md` |
| T-0063-S258 | sma-c | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.sma-c.md` |
| T-0063-S259 | analyzer-phase1 | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.analyzer-phase1.md` |
| T-0063-S260 | analyzer-phase2 | v11-ch04 | done | 1 | `agent_prompts/agent_prompt.v11-ch04.analyzer-phase2.md` |
| T-0063-S261 | sma-a | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.sma-a.md` |
| T-0063-S262 | sma-b | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.sma-b.md` |
| T-0063-S263 | sma-c | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.sma-c.md` |
| T-0063-S264 | analyzer-phase1 | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.analyzer-phase1.md` |
| T-0063-S265 | analyzer-phase2 | v11-ch05 | done | 1 | `agent_prompts/agent_prompt.v11-ch05.analyzer-phase2.md` |
| T-0063-S266 | sma-a | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.sma-a.md` |
| T-0063-S267 | sma-b | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.sma-b.md` |
| T-0063-S268 | sma-c | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.sma-c.md` |
| T-0063-S269 | analyzer-phase1 | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.analyzer-phase1.md` |
| T-0063-S270 | analyzer-phase2 | v11-ch06 | done | 1 | `agent_prompts/agent_prompt.v11-ch06.analyzer-phase2.md` |
| T-0063-S271 | sma-a | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.sma-a.md` |
| T-0063-S272 | sma-b | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.sma-b.md` |
| T-0063-S273 | sma-c | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.sma-c.md` |
| T-0063-S274 | analyzer-phase1 | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.analyzer-phase1.md` |
| T-0063-S275 | analyzer-phase2 | v11-ch07 | done | 1 | `agent_prompts/agent_prompt.v11-ch07.analyzer-phase2.md` |
| T-0063-S276 | sma-a | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.sma-a.md` |
| T-0063-S277 | sma-b | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.sma-b.md` |
| T-0063-S278 | sma-c | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.sma-c.md` |
| T-0063-S279 | analyzer-phase1 | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.analyzer-phase1.md` |
| T-0063-S280 | analyzer-phase2 | v11-ch08 | done | 1 | `agent_prompts/agent_prompt.v11-ch08.analyzer-phase2.md` |
| T-0063-S281 | sma-a | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.sma-a.md` |
| T-0063-S282 | sma-b | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.sma-b.md` |
| T-0063-S283 | sma-c | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.sma-c.md` |
| T-0063-S284 | analyzer-phase1 | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.analyzer-phase1.md` |
| T-0063-S285 | analyzer-phase2 | v11-ch09 | done | 1 | `agent_prompts/agent_prompt.v11-ch09.analyzer-phase2.md` |
| T-0063-S286 | sma-a | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.sma-a.md` |
| T-0063-S287 | sma-b | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.sma-b.md` |
| T-0063-S288 | sma-c | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.sma-c.md` |
| T-0063-S289 | analyzer-phase1 | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.analyzer-phase1.md` |
| T-0063-S290 | analyzer-phase2 | v11-ch10 | done | 1 | `agent_prompts/agent_prompt.v11-ch10.analyzer-phase2.md` |
| T-0063-S291 | sma-a | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.sma-a.md` |
| T-0063-S292 | sma-b | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.sma-b.md` |
| T-0063-S293 | sma-c | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.sma-c.md` |
| T-0063-S294 | analyzer-phase1 | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.analyzer-phase1.md` |
| T-0063-S295 | analyzer-phase2 | v11-epilogue | done | 1 | `agent_prompts/agent_prompt.v11-epilogue.analyzer-phase2.md` |
| T-0063-S296 | sma-a | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.sma-a.md` |
| T-0063-S297 | sma-b | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.sma-b.md` |
| T-0063-S298 | sma-c | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.sma-c.md` |
| T-0063-S299 | analyzer-phase1 | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.analyzer-phase1.md` |
| T-0063-S300 | analyzer-phase2 | v13-afterword | done | 1 | `agent_prompts/agent_prompt.v13-afterword.analyzer-phase2.md` |
| T-0063-S301 | sma-a | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.sma-a.md` |
| T-0063-S302 | sma-b | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.sma-b.md` |
| T-0063-S303 | sma-c | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.sma-c.md` |
| T-0063-S304 | analyzer-phase1 | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.analyzer-phase1.md` |
| T-0063-S305 | analyzer-phase2 | v13-ch01 | done | 1 | `agent_prompts/agent_prompt.v13-ch01.analyzer-phase2.md` |
| T-0063-S306 | sma-a | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.sma-a.md` |
| T-0063-S307 | sma-b | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.sma-b.md` |
| T-0063-S308 | sma-c | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.sma-c.md` |
| T-0063-S309 | analyzer-phase1 | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.analyzer-phase1.md` |
| T-0063-S310 | analyzer-phase2 | v13-ch02 | done | 1 | `agent_prompts/agent_prompt.v13-ch02.analyzer-phase2.md` |
| T-0063-S311 | sma-a | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.sma-a.md` |
| T-0063-S312 | sma-b | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.sma-b.md` |
| T-0063-S313 | sma-c | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.sma-c.md` |
| T-0063-S314 | analyzer-phase1 | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.analyzer-phase1.md` |
| T-0063-S315 | analyzer-phase2 | v13-ch03 | done | 1 | `agent_prompts/agent_prompt.v13-ch03.analyzer-phase2.md` |
| T-0063-S316 | sma-a | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.sma-a.md` |
| T-0063-S317 | sma-b | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.sma-b.md` |
| T-0063-S318 | sma-c | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.sma-c.md` |
| T-0063-S319 | analyzer-phase1 | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.analyzer-phase1.md` |
| T-0063-S320 | analyzer-phase2 | v13-ch04 | done | 1 | `agent_prompts/agent_prompt.v13-ch04.analyzer-phase2.md` |
| T-0063-S321 | sma-a | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.sma-a.md` |
| T-0063-S322 | sma-b | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.sma-b.md` |
| T-0063-S323 | sma-c | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.sma-c.md` |
| T-0063-S324 | analyzer-phase1 | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.analyzer-phase1.md` |
| T-0063-S325 | analyzer-phase2 | v13-ch05 | done | 1 | `agent_prompts/agent_prompt.v13-ch05.analyzer-phase2.md` |
| T-0063-S326 | sma-a | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.sma-a.md` |
| T-0063-S327 | sma-b | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.sma-b.md` |
| T-0063-S328 | sma-c | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.sma-c.md` |
| T-0063-S329 | analyzer-phase1 | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.analyzer-phase1.md` |
| T-0063-S330 | analyzer-phase2 | v13-ch06 | done | 1 | `agent_prompts/agent_prompt.v13-ch06.analyzer-phase2.md` |
| T-0063-S331 | sma-a | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.sma-a.md` |
| T-0063-S332 | sma-b | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.sma-b.md` |
| T-0063-S333 | sma-c | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.sma-c.md` |
| T-0063-S334 | analyzer-phase1 | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.analyzer-phase1.md` |
| T-0063-S335 | analyzer-phase2 | v13-ch07 | done | 1 | `agent_prompts/agent_prompt.v13-ch07.analyzer-phase2.md` |
| T-0063-S336 | sma-a | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.sma-a.md` |
| T-0063-S337 | sma-b | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.sma-b.md` |
| T-0063-S338 | sma-c | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.sma-c.md` |
| T-0063-S339 | analyzer-phase1 | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.analyzer-phase1.md` |
| T-0063-S340 | analyzer-phase2 | v13-ch08 | done | 1 | `agent_prompts/agent_prompt.v13-ch08.analyzer-phase2.md` |
| T-0063-S341 | sma-a | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.sma-a.md` |
| T-0063-S342 | sma-b | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.sma-b.md` |
| T-0063-S343 | sma-c | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.sma-c.md` |
| T-0063-S344 | analyzer-phase1 | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.analyzer-phase1.md` |
| T-0063-S345 | analyzer-phase2 | v13-epilogue | done | 1 | `agent_prompts/agent_prompt.v13-epilogue.analyzer-phase2.md` |
| T-0063-S346 | sma-a | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.sma-a.md` |
| T-0063-S347 | sma-b | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.sma-b.md` |
| T-0063-S348 | sma-c | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.sma-c.md` |
| T-0063-S349 | analyzer-phase1 | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.analyzer-phase1.md` |
| T-0063-S350 | analyzer-phase2 | v12-afterword | done | 1 | `agent_prompts/agent_prompt.v12-afterword.analyzer-phase2.md` |
| T-0063-S351 | sma-a | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.sma-a.md` |
| T-0063-S352 | sma-b | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.sma-b.md` |
| T-0063-S353 | sma-c | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.sma-c.md` |
| T-0063-S354 | analyzer-phase1 | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.analyzer-phase1.md` |
| T-0063-S355 | analyzer-phase2 | v12-prologue | done | 1 | `agent_prompts/agent_prompt.v12-prologue.analyzer-phase2.md` |
| T-0063-S356 | sma-a | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.sma-a.md` |
| T-0063-S357 | sma-b | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.sma-b.md` |
| T-0063-S358 | sma-c | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.sma-c.md` |
| T-0063-S359 | analyzer-phase1 | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.analyzer-phase1.md` |
| T-0063-S360 | analyzer-phase2 | v12-ch01 | done | 1 | `agent_prompts/agent_prompt.v12-ch01.analyzer-phase2.md` |
| T-0063-S361 | sma-a | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.sma-a.md` |
| T-0063-S362 | sma-b | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.sma-b.md` |
| T-0063-S363 | sma-c | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.sma-c.md` |
| T-0063-S364 | analyzer-phase1 | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.analyzer-phase1.md` |
| T-0063-S365 | analyzer-phase2 | v12-ch02 | done | 1 | `agent_prompts/agent_prompt.v12-ch02.analyzer-phase2.md` |
| T-0063-S366 | sma-a | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.sma-a.md` |
| T-0063-S367 | sma-b | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.sma-b.md` |
| T-0063-S368 | sma-c | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.sma-c.md` |
| T-0063-S369 | analyzer-phase1 | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.analyzer-phase1.md` |
| T-0063-S370 | analyzer-phase2 | v12-ch04 | done | 1 | `agent_prompts/agent_prompt.v12-ch04.analyzer-phase2.md` |
| T-0063-S371 | sma-a | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.sma-a.md` |
| T-0063-S372 | sma-b | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.sma-b.md` |
| T-0063-S373 | sma-c | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.sma-c.md` |
| T-0063-S374 | analyzer-phase1 | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.analyzer-phase1.md` |
| T-0063-S375 | analyzer-phase2 | v12-ch05 | done | 1 | `agent_prompts/agent_prompt.v12-ch05.analyzer-phase2.md` |
| T-0063-S376 | sma-a | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.sma-a.md` |
| T-0063-S377 | sma-b | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.sma-b.md` |
| T-0063-S378 | sma-c | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.sma-c.md` |
| T-0063-S379 | analyzer-phase1 | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.analyzer-phase1.md` |
| T-0063-S380 | analyzer-phase2 | v12-ch07 | done | 1 | `agent_prompts/agent_prompt.v12-ch07.analyzer-phase2.md` |
| T-0063-S381 | sma-a | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.sma-a.md` |
| T-0063-S382 | sma-b | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.sma-b.md` |
| T-0063-S383 | sma-c | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.sma-c.md` |
| T-0063-S384 | analyzer-phase1 | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.analyzer-phase1.md` |
| T-0063-S385 | analyzer-phase2 | v12-ch08 | done | 1 | `agent_prompts/agent_prompt.v12-ch08.analyzer-phase2.md` |

Заметки:
- T-0063-S1: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S2: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S3: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S4: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S5: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S6: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S7: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S8: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S9: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S10: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S11: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S12: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S13: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S14: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S15: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S16: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S17: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S18: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S19: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S20: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S21: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S22: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S23: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S24: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S25: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S26: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S27: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S28: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S29: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S30: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S31: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S32: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S33: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S34: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S35: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S36: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S37: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S38: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S39: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S40: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S41: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S42: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S43: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S44: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S45: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S46: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S47: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S48: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S49: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S50: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S51: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S52: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S53: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S54: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S55: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S56: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S57: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S58: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S59: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S60: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S61: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S62: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S63: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S64: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S65: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S66: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S67: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S68: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S69: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S70: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S71: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S72: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S73: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S74: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S75: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S76: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S77: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S78: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S79: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S80: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S81: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S82: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S83: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S84: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S85: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S86: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S87: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S88: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S89: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S90: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S91: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S92: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S93: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S94: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S95: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S96: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S97: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S98: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S99: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S100: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S101: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S102: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S103: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S104: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S105: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S106: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S107: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S108: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S109: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S110: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S111: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S112: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S113: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S114: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S115: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S116: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S117: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S118: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S119: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S120: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S121: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S122: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S123: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S124: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S125: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S126: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S127: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S128: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S129: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S130: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S131: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S132: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S133: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S134: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S135: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S136: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S137: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S138: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S139: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S140: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S141: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S142: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S143: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S144: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S145: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S146: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S147: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S148: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S149: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S150: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S151: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S152: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S153: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S154: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S155: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S156: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S157: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S158: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S159: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S160: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S161: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S162: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S163: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S164: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S165: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S166: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S167: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S168: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S169: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S170: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S171: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S172: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S173: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S174: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S175: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S176: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S177: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S178: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S179: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S180: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S181: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S182: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S183: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S184: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S185: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S186: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S187: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S188: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S189: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S190: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S191: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S192: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S193: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S194: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S195: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S196: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S197: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S198: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S199: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S200: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S201: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S202: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S203: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S204: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S205: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S206: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S207: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S208: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S209: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S210: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S211: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S212: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S213: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S214: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S215: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S216: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S217: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S218: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S219: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S220: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S221: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S222: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S223: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S224: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S225: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S226: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S227: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S228: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S229: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S230: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S231: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S232: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S233: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S234: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S235: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S236: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S237: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S238: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S239: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S240: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S241: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S242: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S243: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S244: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S245: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S246: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S247: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S248: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S249: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S250: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S251: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S252: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S253: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S254: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S255: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S256: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S257: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S258: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S259: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S260: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S261: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S262: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S263: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S264: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S265: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S266: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S267: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S268: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S269: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S270: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S271: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S272: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S273: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S274: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S275: раунд fullABC-d80be7de: precheck+A/B/C+ph1+ph2, коммит не делался
- T-0063-S276: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S277: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S278: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S279: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S280: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S281: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S282: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S283: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S284: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S285: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S286: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S287: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S288: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S289: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S290: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S291: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S292: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S293: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S294: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S295: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S296: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S297: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S298: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S299: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S300: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S301: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S302: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S303: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S304: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S305: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S306: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S307: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S308: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S309: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S310: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S311: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S312: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S313: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S314: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S315: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S316: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S317: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S318: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S319: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S320: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S321: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S322: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S323: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S324: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S325: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S326: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S327: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S328: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S329: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S330: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S331: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S332: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S333: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S334: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S335: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S336: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S337: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S338: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S339: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S340: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S341: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S342: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S343: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S344: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S345: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S346: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S347: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S348: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S349: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S350: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S351: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S352: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S353: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S354: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S355: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S356: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S357: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S358: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S359: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S360: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S361: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S362: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S363: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S364: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S365: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S366: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S367: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S368: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S369: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S370: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S371: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S372: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S373: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S374: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S375: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S376: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S377: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S378: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S379: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S380: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S381: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S382: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S383: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S384: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался
- T-0063-S385: раунд fullABC: precheck+A/B/C+ph1+ph2 артефакты верифицированы оркестратором, коммит не делался

