# Аудит: v08-afterword («Послесловие»)

Проверено 2 смысловых блока. JA (`translates/ja/v8-afterword.md`) — источник
смысла; EN-зеркало отсутствует, RU-сырец отсутствует — перевод написан прямо
по JA. `translates/ja` не изменялся. Гейт до обработки — 0/12.

## Переработка

2/2 блока по JA, заголовок «Послесловие» (あとがき) внутри блока 1.
EN/RU-зеркала нет: вручную заполнены ED_RU в
`translates/_report/merged/v8-afterword.md`; создан alignment-отчёт
`output/_audit/_prefilter/v8-afterword-alignment.md`.
Имена: ヤマグチノボル → «Ямагути Нобору», 兎塚エイジ → «Усуцка Эйдзи».
Языковые вкрапления устранены: rivalry, 她的, 2**, из:nameко.

## Грамматика / стиль / оформление

- `grammar_scan.py`: 0. `style_scan.py`: 15 — FP/PRESERVED — JA.
- `format_scan.py`: 2 — 1 FIXED (blockgap), 1 FP (регистр названия);
  `address_scan.py`: 0. `check_records.py`: 0.
- `omission_precheck.py`: 0. `check_alignment.py`: строгих 0, прочих 5, инфо 2.

## FINAL READ

2 блока. Автор (@Ямагути Нобору) благодарит читателей: восьмой том как
«пункт с водой на марафоне» сериала, тема — «родина» и романтика; упоминает
анимацию, мангу и игру (медиамикс) (1). Биографические справки автора и
иллюстратора Усуцки Эйдзи (2). Реплики, кавычки, маркеры в порядке.

## Итоги (FINAL AUDIT)

- GRAMMAR: 0. STYLE: 15 → FP/PRESERVED — JA.
- FORMAT: 1 FIXED (blockgap), 1 FP. DRIFT: не выполнялся.
- Смысловой слой: SMA A — 3 (ERROR: 予感て → «предчувствие» (не «Четверых!»),
  捨てる, ラブコме → «ромком»), B — 0, C — 2 (でしょう/と思います —
  смягчение). Фаза 1 — NONE по обоим блокам. Фаза 2
  (`20261117-030653-89f9.json`): 5 кандидатов — все FALSE_POSITIVE/PRESERVED
  (находки уже исправлены в актуальном RU), 0 FIXED, 0 DISPUTED.
- `omission_precheck.py`: 0; `check_alignment.py`: строгих 0.

## Контроль

- `output/chapters/v8-afterword.md`: 2 блока, маркеры по порядку, 2/2 ED_RU.
