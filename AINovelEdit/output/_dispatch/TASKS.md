# Реестр задач диспетчера

Обновлено: 2026-10-25 03:23:19

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
| T-0002-S49 | sma-a | v06-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch06.sma-a.md` |
| T-0002-S50 | sma-b | v06-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch06.sma-b.md` |
| T-0002-S51 | sma-c | v06-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch06.sma-c.md` |
| T-0002-S52 | analyzer-phase1 | v06-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch06.analyzer-phase1.md` |
| T-0002-S53 | analyzer-phase2 | v06-ch06 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch06.analyzer-phase2.md` |
| T-0002-S54 | grammar-audit | v06-ch06 | running | 1 | `agent_prompts/agent_prompt.v06-ch06.grammar-audit.md` |
| T-0002-S55 | style-audit | v06-ch06 | running | 1 | `agent_prompts/agent_prompt.v06-ch06.style-audit.md` |
| T-0002-S56 | humanizer | v06-ch06 | running | 1 | `agent_prompts/agent_prompt.v06-ch06.humanizer.md` |
| T-0002-S57 | sma-a | v06-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch07.sma-a.md` |
| T-0002-S58 | sma-b | v06-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch07.sma-b.md` |
| T-0002-S59 | sma-c | v06-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch07.sma-c.md` |
| T-0002-S60 | analyzer-phase1 | v06-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch07.analyzer-phase1.md` |
| T-0002-S61 | analyzer-phase2 | v06-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch07.analyzer-phase2.md` |
| T-0002-S62 | grammar-audit | v06-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch07.grammar-audit.md` |
| T-0002-S63 | style-audit | v06-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch07.style-audit.md` |
| T-0002-S64 | humanizer | v06-ch07 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch07.humanizer.md` |
| T-0002-S65 | sma-a | v06-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch08.sma-a.md` |
| T-0002-S66 | sma-b | v06-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch08.sma-b.md` |
| T-0002-S67 | sma-c | v06-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch08.sma-c.md` |
| T-0002-S68 | analyzer-phase1 | v06-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch08.analyzer-phase1.md` |
| T-0002-S69 | analyzer-phase2 | v06-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch08.analyzer-phase2.md` |
| T-0002-S70 | grammar-audit | v06-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch08.grammar-audit.md` |
| T-0002-S71 | style-audit | v06-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch08.style-audit.md` |
| T-0002-S72 | humanizer | v06-ch08 | interrupted | 1 | `agent_prompts/agent_prompt.v06-ch08.humanizer.md` |

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
- T-0002-S49: нет результата после запуска
- T-0002-S50: нет результата после запуска
- T-0002-S51: нет результата после запуска
- T-0002-S52: нет результата после запуска
- T-0002-S53: нет результата после запуска
- T-0002-S57: нет результата после запуска
- T-0002-S58: нет результата после запуска
- T-0002-S59: нет результата после запуска
- T-0002-S60: нет результата после запуска
- T-0002-S61: нет результата после запуска
- T-0002-S62: изменений после запуска нет
- T-0002-S63: изменений после запуска нет
- T-0002-S64: изменений после запуска нет
- T-0002-S65: нет результата после запуска
- T-0002-S66: нет результата после запуска
- T-0002-S67: нет результата после запуска
- T-0002-S68: нет результата после запуска
- T-0002-S69: нет результата после запуска
- T-0002-S70: изменений после запуска нет
- T-0002-S71: изменений после запуска нет
- T-0002-S72: изменений после запуска нет

