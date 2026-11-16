# Выгрузка предфильтра (грамматика, кандидаты): v7-ch05.md

Кандидатов на разбор: **14** (agreement 1, passive-ru 5, possessive 3, voice 5).

Скрипт — не истина: каждый пункт либо исправляется по скиллу
russian-grammar-control, либо отклоняется с обоснованием в отчёте
аудита (ложное срабатывание).

## Блок 1 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: началось)

- **EN:** According to the reports in the past few days, the enemy's cannons have all been destroyed by our fleet's bombardment, and they've only deployed demi-humans to guard the streets.
- **ED_RU:** Прошло пятнадцать дней с высадки — и сегодня наступление наконец началось.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 3 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: обращаются)

- **EN:** The metallic lights shot towards the approaching golems one after another, felling many of them as they were struck by its fire.
- **ED_RU:** — Наверное, с ней обращаются орки-демоны.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 4 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: прибавляются)

- **EN:** Finally arriving at the foot of the collapsed wall, which had been turned into rubble by the cannon fire earlier, the mud golems began clearing away the rubble.
- **ED_RU:** Ни храбрость, ни подвиг от этого не прибавляются.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 5 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: рванулся)

- **EN:** The other orcs at the forefront were felled onto the ground as well, blocking the advance of the group behind them.
- **ED_RU:** Гиш рванулся вперёд, но Николя удержал его.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 6 — RU пассив «был + причастие»: проверь агента (RGC: построен)

- **EN:** To find out why Louise was running back and forth through the maze of alleyways within Saxe-Gotha, we would have to begin from the mission that they had accepted.
In the simplest sense, their objective coincided with that of the assaulting main force: Infiltrate the city from the opposite side. Their original purpose was to use "Illusion" to create a phantom army, thus plunging the enemy into disarray…
"Why did you have to suddenly yell out like that?! Hey!" shouted Louise as she ran.
Three hours ago, they had snuck into the city under the cover of darkness.
"Didn't I already tell you? No matter what you see, don't act surprised! Hey!"
"B-but... It's too big! That troll thing! That ogre or something!"
- **ED_RU:** Сити оф Саусгота был построен на невысоком холме.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 8 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: выпрямился)

- **EN:** How am I supposed to know things like this?
- **ED_RU:** _Он меня раскусил_, — подумал Сайто и выпрямился.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 9 — RU пассив «был + причастие»: проверь агента (RGC: отброшен)

- **EN:** They were completely trapped.
- **ED_RU:** »
Сайто попытался принять удар — и был отброшен троллем-великаном.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 10 — Согласование: местоимение ед. ч. + глагол мн. ч. (RGC: передние … вспыхнули)

- **EN:** Louise, feeling relieved, pated her chest, and said thanks to Julio.
"Thank you. We survived."
"Don't thank us yet."
Discouraged Louise's shoulders dropped.
"We… failed the mission. No good…"
Julio pointed to the ground.
"Indeed. There doesn't seem to be that much of a change in the general situation."
- **ED_RU:** И тут передние орки-демоны вдруг вспыхнули пламенем.
- **Подсказка:** RGC-3: сказуемое согласуется с подлежащим в числе — и у местоимения («он лишились»), и у существительного подлежащего («сидение … запарили» → «… разморило», manual-fix v3-ch03 c25). Сверь, кто здесь подлежащее: если оно мн. ч. («гости ушли») — ложное срабатывание.

## Блок 12 — RU пассив «был + причастие»: проверь агента (RGC: провозглашена)

- **EN:** Huge demi-humans were not capable of moving well in the urban area suited for humans, and were defeated in even one-on-one battles.
- **ED_RU:** И в конце года, в четвёртой неделе месяца Винн, в срединный день Инга, на центральной площади Сити оф Саусгота была провозглашена «освобождённая» жизнь города.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 12 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: пожаловаться)

- **EN:** Huge demi-humans were not capable of moving well in the urban area suited for humans, and were defeated in even one-on-one battles.
- **ED_RU:** Может, стоит пожаловаться?
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 15 — RU пассив «был + причастие»: проверь агента (RGC: обращён)

- **EN:** There wasn't a girl who would not be attracted to him.
- **ED_RU:** Взгляд её был обращён к Джулио.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 15 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: отказывается)

- **EN:** There wasn't a girl who would not be attracted to him.
- **ED_RU:** сердце отказывается признать причину.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 16 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: улыбнулся)

- **EN:** That stupid Guiche is rewarded?
- **ED_RU:** Джулио улыбнулся.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 17 — RU пассив «был + причастие»: проверь агента (RGC: завиден)

- **EN:** Though Louise military achievements were much bigger than Guiche's, things like this could not be done publicly.
However, once this war ended… when the peace comes… she will tell her family about her large military achievements and loyalty to the mother-country.
Maybe then they will change their opinion about her. But for now, she cannot stumble and take even the slightest credit for her own achievements.
When thinking she remembered Saito's mistakes. The feint mission sneaking into the town failed thanks to Saito. She watched him, while throwing occasional side glances.
The user of legendary power. A mistake in using them and they got themselves in a pinch yesterday. Saito should be more prudent, Louise thought.
- **ED_RU:** Как же ей был завиден такой Гиш.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

