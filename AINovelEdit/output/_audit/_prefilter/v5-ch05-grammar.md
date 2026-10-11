# Выгрузка предфильтра (грамматика, кандидаты): v5-ch05.md

Кандидатов на разбор: **4** (agreement 1, passive-ru 3).

Скрипт — не истина: каждый пункт либо исправляется по скиллу
russian-grammar-control, либо отклоняется с обоснованием в отчёте
аудита (ложное срабатывание).

## Блок 1 — RU пассив «был + причастие»: проверь агента (RGC: поглощена)

- **EN:** "
As expected, there was some ice mixed in the wind.
- **ED_RU:** Несмотря на жар, та не выступила ни капелькой пота и целиком была поглощена книгой.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 8 — RU пассив «был + причастие»: проверь агента (RGC: мерзковат)

- **EN:** But because Guiche, who had been backed up by Kirche, started to skip away, Montmorency had no choice but to follow.
- **ED_RU:** Хозяин был мерзковат, но раз Монморанси похвалили, её настроение переменилось.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 11 — Согласование: местоимение ед. ч. + глагол мн. ч. (RGC: нынешние … проходили)

- **EN:** It seemed Kirche was used to these kinds of things and continued drinking wine calmly, but Guiche was feeling uneasy.
- **ED_RU:** В нынешние смутные времена, видно, дни их проходили в военных учениях.
- **Подсказка:** RGC-3: сказуемое согласуется с подлежащим в числе — и у местоимения («он лишились»), и у существительного подлежащего («сидение … запарили» → «… разморило», manual-fix v3-ch03 c25). Сверь, кто здесь подлежащее: если оно мн. ч. («гости ушли») — ложное срабатывание.

## Блок 16 — RU пассив «был + причастие»: проверь агента (RGC: сделано)

- **EN:** "Do any of you gentlemen have the Chevalier title?"
The officers twisted their necks in disbelief.
"Then she should prove to be more than a match."
As Kirche finished speaking, she sat down on a chair as though her job was over. The officers, who couldn't back down, followed Tabitha to the outside of the bar.
"Is she gonna be ok?"
Asked Guiche. Kirche was just drinking her wine elegantly.
"That girl never forgets this kind of old fashioned promises."
Kirche muttered happily.
- **ED_RU:** Сказав это, Кирхе села — будто её дело было сделано.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

