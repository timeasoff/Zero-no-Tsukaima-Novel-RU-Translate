# LEGACY: автоматический semantic audit

**Статус: НЕ РЕАЛИЗОВАН / НЕ ПОДДЕРЖИВАЕТСЯ.**

> Не использовать в текущем pipeline. Сохранён только как задел/история для
> возможной будущей реализации. Никакие задачи текущего проекта не должны
> опираться на этот контур.

## Текущий рабочий pipeline

```text
Semantic Audit A  →  Semantic Audit B  →  Semantic Analyzer A+B
```

- Запуск промптов: `python tools/generate_agent_prompt.py`
  (режимы «Смысловой аудит A», «Смысловой аудит B», «Смысловой анализатор A+B»).
- Структура результатов:

```text
output/_audit/sma/<chapter>/
    a/
    b/
    analysis/
```

- Скиллы: `.agents/skills/semantic-audit-a/`, `semantic-audit-b/`,
  `semantic-analyzer/`.
- Каждый новый запуск A/B получает уникальный `audit_run_id`; результаты не
  перезаписываются. Analyzer — единственный агент, который сознательно читает
  выбранные результаты A/B и работает поверх них.

## Legacy-компоненты

Расположены в этой директории (`AINovelEdit/legacy/semantic-audit-auto/`):

| Компонент | Роль в legacy-контуре |
| --- | --- |
| `run_semantic_audit.py` | оркестратор автоматического double-audit A‖B (параллельные процессы Cline/OpenCode) |
| `merge_findings.py` | объединение находок A и B в candidates (`BOTH_FOUND` / `ONLY_A` / `ONLY_B`) |
| `verify_findings.py` | «верификатор»/resolver: вердикты `ERROR` / `QUESTIONABLE` / `ACCEPT` |
| `.agents/skills/verifier/SKILL.md` | legacy-скилл верификатора (помечен `LEGACY`, оставлен на месте) |

Общие модули, которые legacy-скрипты **используют, но не владеют** (остаются
в рабочей части проекта и могут развиваться отдельно):

- `AINovelEdit/scripts/llm_runtime.py` — runtime-адаптеры (`cline`/`opencode`);
- `AINovelEdit/scripts/merged_io.py` — общий разбор блок-файлов;
- `tools/generate_agent_prompt.py` — источник класса `Chapter` (пути главы).

## Причина вывода из pipeline

Legacy-контур использует **отдельную flat-раскладку результатов** и другой
resolver, несовместимые с новой архитектурой:

- legacy пишет один фиксированный файл на главу:
  `output/_audit/<chapter>-sma-a.json`, `<chapter>-sma-b.json`, затем
  `<chapter>-sma-merged.{json,md}` и `<chapter>-sma-verdict.{json,md}`;
- новая архитектура пишет независимые запуски в
  `output/_audit/sma/<chapter>/{a,b}/<audit_run_id>.json` и решение — в
  `output/_audit/sma/<chapter>/analysis/<analysis_id>.{json,md}`;
- legacy-verifier выносит `ERROR / QUESTIONABLE / ACCEPT` и **не имеет**
  статусов/действий Analyzer (`CONFIRMED_ERROR` / `DISPUTED` /
  `FALSE_POSITIVE` / `OPTIONAL`; `FIXED` / `REPORT_ONLY` / `PRESERVED`), т.е.
  не реализует правило «править только `CONFIRMED_ERROR`»;
- автоматический запуск A/B через runtime (OpenCode/Cline) для нового контура
  не реализован — новый контур запускается вручную через генератор промптов.

Итого: автоматический semantic audit **не доведён до рабочего состояния** и
развиваться на текущем этапе не будет. Решено вынести его в изолированный
black box, чтобы наличие этих скриптов не выглядело как часть рабочего
pipeline.

## Что было изменено при выносе

- Три скрипта перемещены из `AINovelEdit/scripts/` в
  `AINovelEdit/legacy/semantic-audit-auto/` (без переписывания логики).
- В каждом добавлена шапка `LEGACY / NOT IMPLEMENTED`.
- Единственная правка кода — **relocation shim** (пересчёт путей после
  переноса: `AINOVELEDIT`, `SCRIPTS_DIR`, `TOOLS_DIR`, путь к
  `merge_findings.py`). Логика аудита/merge/verifier не менялась.
- Скилл `verifier` оставлен физически на месте (его путь зашит в
  `verify_findings.py`), но помечен `LEGACY` в шапке.

## Что НЕ делалось (отдельная будущая задача)

- legacy-контур **не** переносился на `sma/<chapter>/...`;
- схемы JSON, resolver-механизмы и модели запуска не переписывались;
- автоматический запуск нового контура не реализовывался.

## Legacy-артефакты в `output/_audit/`

Сохраняются как история; новым pipeline не используются и не генерируются:

- `output/_audit/v05-ch02-sma-merged.md`
- `output/_audit/v05-ch02-sma-verdict.md`

Ручные legacy-отчёты A/B перенесены в новую структуру как evidence-история:

- `output/_audit/sma/v3-ch03/a/legacy-manual-a.md`
- `output/_audit/sma/v3-ch03/b/legacy-manual-b.md`

## Проверка после переноса

Перенесённые скрипты по-прежнему запускаются (для истории), но это не делает
их частью pipeline:

```text
python AINovelEdit/legacy/semantic-audit-auto/run_semantic_audit.py --file vX-chYY.md --dry-run
python AINovelEdit/legacy/semantic-audit-auto/verify_findings.py --self-test
```