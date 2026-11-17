# Реестр задач диспетчера

Обновлено: 2026-11-17 16:19:06

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

