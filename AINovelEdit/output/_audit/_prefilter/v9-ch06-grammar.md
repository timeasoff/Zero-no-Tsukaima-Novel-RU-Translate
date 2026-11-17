# Выгрузка предфильтра (грамматика, кандидаты): v9-ch06.md

Кандидатов на разбор: **7** (agreement 1, passive-ru 1, possessive 4, voice 1).

Скрипт — не истина: каждый пункт либо исправляется по скиллу
russian-grammar-control, либо отклоняется с обоснованием в отчёте
аудита (ложное срабатывание).

## Блок 3 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: кончилась)

- **EN:** Even my kind heart had to be used as a tool to rule over the people...
- **ED_RU:** А когда война кончилась…
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 5 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: послышался)

- **EN:** Almost all the people knew about the evacuating allied forces and how they got rescued by Gallia's army which had suddenly participated in the war.
- **ED_RU:** В толпе послышался насмешливый смех.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 6 — RU пассив «был + причастие»: проверь агента (RGC: распущен)

- **EN:** A smile which was rarely seen lately was displayed, and Henrietta tightly embraced the visitor who was waiting for her since some time ago.
- **ED_RU:** По прибытии во дворец отряд охраны, кроме дежурной части, был распущен.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 8 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: случилось)

- **EN:** At Albion, we were attacked by a 'familiar of Void,' and we met another 'Bearer of Void.
- **ED_RU:** Что случилось с «Рубином Ветра»?
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 9 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: растерялась)

- **EN:** Because it is something filled with memories, I will never sell such a valuable thing.
- **ED_RU:** Генриетта растерялась.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 12 — Согласование: местоимение ед. ч. + глагол мн. ч. (RGC: расписание … недели)

- **EN:** One of these days, my sleeping time would be scraped off as well, she muttered in her heart.
- **ED_RU:** — Я хотела сверить ваше расписание на ближайшие две недели…
- **Подсказка:** RGC-3: сказуемое согласуется с подлежащим в числе — и у местоимения («он лишились»), и у существительного подлежащего («сидение … запарили» → «… разморило», manual-fix v3-ch03 c25). Сверь, кто здесь подлежащее: если оно мн. ч. («гости ушли») — ложное срабатывание.

## Блок 14 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: откинулась)

- **EN:** "The Academy of Magic is the place where the younger generation of nobles who carry the future of the country is educated...
- **ED_RU:** Генриетта снова откинулась на спинку стула и облокотилась.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

