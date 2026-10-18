# Реестр задач диспетчера

Обновлено: 2026-10-19 01:08:26

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
| T-0001-S16 | analyzer-phase1 | v05-ch05 | running | 3 | `agent_prompts/agent_prompt.v05-ch05.analyzer-phase1.attempt3.md` |
| T-0001-S17 | analyzer-phase2 | v05-ch05 | running | 3 | `agent_prompts/agent_prompt.v05-ch05.analyzer-phase2.attempt3.md` |
| T-0001-S18 | grammar-audit | v05-ch05 | planned | 0 | `—` |
| T-0001-S19 | sma-a | v05-ch06 | running | 5 | `agent_prompts/agent_prompt.v05-ch06.sma-a.attempt5.md` |
| T-0001-S20 | sma-b | v05-ch06 | running | 2 | `agent_prompts/agent_prompt.v05-ch06.sma-b.attempt2.md` |
| T-0001-S21 | sma-c | v05-ch06 | running | 3 | `agent_prompts/agent_prompt.v05-ch06.sma-c.attempt3.md` |
| T-0001-S22 | analyzer-phase1 | v05-ch06 | planned | 0 | `—` |
| T-0001-S23 | analyzer-phase2 | v05-ch06 | planned | 0 | `—` |
| T-0001-S24 | grammar-audit | v05-ch06 | planned | 0 | `—` |
| T-0001-S25 | sma-a | v05-ch07 | running | 2 | `agent_prompts/agent_prompt.v05-ch07.sma-a.attempt2.md` |
| T-0001-S26 | sma-b | v05-ch07 | running | 2 | `agent_prompts/agent_prompt.v05-ch07.sma-b.attempt2.md` |
| T-0001-S27 | sma-c | v05-ch07 | running | 2 | `agent_prompts/agent_prompt.v05-ch07.sma-c.attempt2.md` |
| T-0001-S28 | analyzer-phase1 | v05-ch07 | planned | 0 | `—` |
| T-0001-S29 | analyzer-phase2 | v05-ch07 | planned | 0 | `—` |
| T-0001-S30 | grammar-audit | v05-ch07 | planned | 0 | `—` |
| T-0001-S31 | sma-a | v05-ch08 | running | 1 | `agent_prompts/agent_prompt.v05-ch08.sma-a.md` |
| T-0001-S32 | sma-b | v05-ch08 | running | 1 | `agent_prompts/agent_prompt.v05-ch08.sma-b.md` |
| T-0001-S33 | sma-c | v05-ch08 | running | 1 | `agent_prompts/agent_prompt.v05-ch08.sma-c.md` |
| T-0001-S34 | analyzer-phase1 | v05-ch08 | planned | 0 | `—` |
| T-0001-S35 | analyzer-phase2 | v05-ch08 | planned | 0 | `—` |
| T-0001-S36 | grammar-audit | v05-ch08 | planned | 0 | `—` |
| T-0001-S37 | sma-a | v05-ch09 | running | 1 | `agent_prompts/agent_prompt.v05-ch09.sma-a.md` |
| T-0001-S38 | sma-b | v05-ch09 | running | 1 | `agent_prompts/agent_prompt.v05-ch09.sma-b.md` |
| T-0001-S39 | sma-c | v05-ch09 | running | 1 | `agent_prompts/agent_prompt.v05-ch09.sma-c.md` |
| T-0001-S40 | analyzer-phase1 | v05-ch09 | planned | 0 | `—` |
| T-0001-S41 | analyzer-phase2 | v05-ch09 | planned | 0 | `—` |
| T-0001-S42 | grammar-audit | v05-ch09 | planned | 0 | `—` |
| T-0001-S43 | sma-a | v05-ch10 | running | 1 | `agent_prompts/agent_prompt.v05-ch10.sma-a.md` |
| T-0001-S44 | sma-b | v05-ch10 | running | 1 | `agent_prompts/agent_prompt.v05-ch10.sma-b.md` |
| T-0001-S45 | sma-c | v05-ch10 | running | 1 | `agent_prompts/agent_prompt.v05-ch10.sma-c.md` |
| T-0001-S46 | analyzer-phase1 | v05-ch10 | planned | 0 | `—` |
| T-0001-S47 | analyzer-phase2 | v05-ch10 | planned | 0 | `—` |
| T-0001-S48 | grammar-audit | v05-ch10 | planned | 0 | `—` |
| T-0001-S49 | sma-a | v05-ch11 | running | 1 | `agent_prompts/agent_prompt.v05-ch11.sma-a.md` |
| T-0001-S50 | sma-b | v05-ch11 | running | 1 | `agent_prompts/agent_prompt.v05-ch11.sma-b.md` |
| T-0001-S51 | sma-c | v05-ch11 | running | 1 | `agent_prompts/agent_prompt.v05-ch11.sma-c.md` |
| T-0001-S52 | analyzer-phase1 | v05-ch11 | planned | 0 | `—` |
| T-0001-S53 | analyzer-phase2 | v05-ch11 | planned | 0 | `—` |
| T-0001-S54 | grammar-audit | v05-ch11 | planned | 0 | `—` |
| T-0001-S55 | sma-a | v05-ch12 | running | 1 | `agent_prompts/agent_prompt.v05-ch12.sma-a.md` |
| T-0001-S56 | sma-b | v05-ch12 | running | 1 | `agent_prompts/agent_prompt.v05-ch12.sma-b.md` |
| T-0001-S57 | sma-c | v05-ch12 | running | 1 | `agent_prompts/agent_prompt.v05-ch12.sma-c.md` |
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

