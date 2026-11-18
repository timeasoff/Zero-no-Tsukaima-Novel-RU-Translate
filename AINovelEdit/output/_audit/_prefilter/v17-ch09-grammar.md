# Выгрузка предфильтра (грамматика, кандидаты): v17-ch09.md

Кандидатов на разбор: **6** (agreement 1, passive-ru 3, possessive 1, voice 1).

Скрипт — не истина: каждый пункт либо исправляется по скиллу
russian-grammar-control, либо отклоняется с обоснованием в отчёте
аудита (ложное срабатывание).

## Блок 1 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: опуститься)

- **EN:** The reception party, party seats, dinner menu, and even the schedule of the one week long party and ball was so flawlessly orchestrated by his own hand that even the Gallian nobles who were picky about details were unable to find fault with it.
- **ED_RU:** Уже готова была опуститься на величественный дворец завеса сумерок — и всё же дворец, сложенный из синего камня, символа королевского дома, являл собой свежую, яркую красоту.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 3 — Согласование: местоимение ед. ч. + глагол мн. ч. (RGC: последние … недели)

- **EN:** "
I will protect this mother and daughter—Every time she was touched by such a heart warming scene during dinner, Isabella would swear in her heart.
- **ED_RU:** За последние недели Изабелла полюбила её как мать.
- **Подсказка:** RGC-3: сказуемое согласуется с подлежащим в числе — и у местоимения («он лишились»), и у существительного подлежащего («сидение … запарили» → «… разморило», manual-fix v3-ch03 c25). Сверь, кто здесь подлежащее: если оно мн. ч. («гости ушли») — ложное срабатывание.

## Блок 4 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: наелась)

- **EN:** Made by professional tailors of the country, the beautiful gown, made out for the queen was waiting to be worn.
- **ED_RU:** — Фух, я наелась.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 7 — RU пассив «был + причастие»: проверь агента (RGC: улажено)

- **EN:** Her inner clothing were exposed through the minuscule holes.
- **ED_RU:** Она вспомнила младшего лейтенанта Вилера, который, бывало, махал ей с палубы после того, как дело было улажено, и загорелое лицо командующего.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 9 — RU пассив «был + причастие»: проверь агента (RGC: пропитана)

- **EN:** Thinking about this, Tabitha smiled softly.
"Now, I should be.......very happy."
Even though her position as the queen made her uneasy, but the Gallian nobles were capable and powerful, so even though there was an exchange in power, the country has not dissolved into ruin. Also, living here with her family made her feel safe and warm. Tabitha felt that the happy feelings of home were starting to return.
- **ED_RU:** Ткань была пропитана «снотворным».
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 10 — RU пассив «был + причастие»: проверь агента (RGC: наложено)

- **EN:** Romania was still an unknown variable, but currently they have made no obvious moves.
Also, she was going to meet her sweetheart, Saito, in a few days time.
She might even get to dance with him.
- **ED_RU:** — На тебя было наложено заклинание, меняющее лицо, — сказал Джулио.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

