# Выгрузка предфильтра (грамматика, кандидаты): v18-ch06.md

Кандидатов на разбор: **17** (agreement 2, passive-ru 1, possessive 6, voice 8).

Скрипт — не истина: каждый пункт либо исправляется по скиллу
russian-grammar-control, либо отклоняется с обоснованием в отчёте
аудита (ложное срабатывание).

## Блок 1 — Согласование: местоимение ед. ч. + глагол мн. ч. (RGC: соседние … жители)

- **EN:** Their arrival was somewhat delayed.
- **ED_RU:** Вокруг полно народу — соседние жители пришли посмотреть на Папу.
- **Подсказка:** RGC-3: сказуемое согласуется с подлежащим в числе — и у местоимения («он лишились»), и у существительного подлежащего («сидение … запарили» → «… разморило», manual-fix v3-ch03 c25). Сверь, кто здесь подлежащее: если оно мн. ч. («гости ушли») — ложное срабатывание.

## Блок 1 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: двигался)

- **EN:** Their arrival was somewhat delayed.
- **ED_RU:** Экипаж Папы двигался к Ромалии — не слишком быстро, не слишком медленно.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 6 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: приблизиться)

- **EN:** The group assigned to lead the Pope's caravan was none other than the Order of Arieste Knights of the Church, which was commanded by Carlo Trobontino.
- **ED_RU:** Не успеем приблизиться к карете, как нас изрешетят заклинаниями.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 7 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: сорвутся)

- **EN:** He imagined those hated elves burning by his sacred magic until they were reduced to ashes.
- **ED_RU:** _
Конечно, если переговоры сорвутся — начнётся война.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 9 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: остановились)

- **EN:** Saito was nervous while he was being gazed at directly by Pope Vittorio.
- **ED_RU:** Трое всадников остановились в двадцати милях от него, прямо на виду.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 10 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: оставалось)

- **EN:** Everyone was surrounded by the intense light.
- **ED_RU:** Оно выглядело как настоящее, но оставалось миражом.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 12 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: обратился)

- **EN:** You cannot even be considered heretics, you're just animals!
- **ED_RU:** Сайто обратился к онемевшей Табите:
— Я пришёл спасти тебя!
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 14 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: собралась)

- **EN:** On the ground, Castlemont and company as well as the Templar Knights were still stunned seeing the spectacle in the sky, but...
- **ED_RU:** В ту же секунду, когда она уже собралась взлетать, на спину вскочила Луиза, а за ней — Кирхе.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 15 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: Saito's heart was)

- **EN:** "Saito! Tabitha is...!" Louise issued a desperate cry. Performing a maneuver like a somersault, Azuro swooped at full speed and once again captured Tabitha in its mouth. Without changing direction, Azuro continued rotating reaching an astonishing rate of descent.
"They did it on purpose, they just wanted to hurt Tabitha!" Kirche said desperately. Upon hearing those words Saito's heart was set on fire. If they continued with that she could fall and hit the ground... and yet they were playing with her small body as if it was a rag doll.
There was still a chance, an opportunity obtained by putting his life in danger, he would never allow them to escape.
"Come on! Sylphid!"
"Understood!" Sylphid quickly began to close the distance. Azuro tried to escape, but his speed didn't increase.
"Attack them, Sylphid!"
"Kyuikyui!" Sylphid prepared to attack with everything she had. However Azuro swiftly dodged them. At that moment, Saito jumped while drawing his sword.
With his left hand, he was able to hang on to a claw of Azuro. Then following Azuro's movements, he began to climb up and reach the dragon's back.
Having faster reaction time than Julio, Saito took him by the neck and pointed his sword.
"Get us down!"
Despite the situation, Julio kept his calm face.
"You're just in time. Come, I want to show you something."
"You've got to be kidding me!" Saito screamed furiously. "Oh God!... you're always acting like this, at least listen for once to what people have to say."
"Do you expect me to listen to a selfish person like you? Always talking about the Crusade, always clinging to that foolishness. Just GET us down!"
As Julio shook his head "As you wish.", was when he finally decided to land Azuro.
Upon reaching the ground, Saito immediately ran to where Tabitha was.
"Tabitha!"
"I'm... fine."
- **ED_RU:** В ту же секунду, когда показались Горы Огненного Дракона, случилось страшное: из пасти Адзуро выпала Табита — Сайто увидел это собственными глазами.
— Сайто! Табита! — вскричала Луиза.
Адзуро развернулся и пикировал, снова подхватив Табиту. Резкий разворот стоил ему скорости.
— Она нарочно вывернулась, чтобы упасть, — прошептала Кирхе.
Сердце Сайто загорелось. Ещё миг — и она разбилась бы о землю... Но Табита вместо этого бросилась вверх, в небо.
Нельзя упускать шанс, который Табита добыла ценой собственной жизни.
— Вперёд, Сильфида!
— Поняла-а!
Сильфида стала быстро сокращать расстояние. Адзуро пытался уйти, но скорость не прибавлялась.
— Сильфида! Тарань их!
— Есть!
Сильфида уже готовилась ударить что есть силы — но Адзуро ловко увернулся. И в этот миг Сайто, выхватывая меч, прыгнул.
Левой рукой он ухватился за коготь Адзуро, разворот дракона вынес его вверх — и он оказался у него на спине.
Быстрее, чем Джулио успел среагировать, Сайто схватил его за шею и приставил меч.
— Приземляйся!
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 17 — Согласование: местоимение ед. ч. + глагол мн. ч. (RGC: прежние … были)

- **EN:** Do you think that justifies all the blood that has been spilled so far?
- **ED_RU:** — Все прежние «священные войны» были такими же.
- **Подсказка:** RGC-3: сказуемое согласуется с подлежащим в числе — и у местоимения («он лишились»), и у существительного подлежащего («сидение … запарили» → «… разморило», manual-fix v3-ch03 c25). Сверь, кто здесь подлежащее: если оно мн. ч. («гости ушли») — ложное срабатывание.

## Блок 17 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: проваливается)

- **EN:** Do you think that justifies all the blood that has been spilled so far?
- **ED_RU:** Тогда Джулио посмотрел на него, как смотрят на приятеля, который вечно проваливается и которого надо подтянуть.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 18 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: уставился)

- **EN:** "
Saito was outraged by the hostile tone of Julio and began to respond.
- **ED_RU:** Сайто с ненавистью уставился на него.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 19 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: изменились)

- **EN:** But anyway, Saito had never faced an opponent before who was unarmed.
- **ED_RU:** Глаза Джулио изменились — привычная насмешка исчезла бесследно.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 20 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: тренировался)

- **EN:** Finally, both Saito and Julio were exhausted.
- **ED_RU:** Он и раньше тренировался драться, и не раз бывал в настоящих схватках.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 23 — RU пассив «был + причастие»: проверь агента (RGC: выброшен)

- **EN:** It was a spectacle that could be described in one word: 'Majestic'.
- **ED_RU:** Кастельмор был выброшен из седла.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 25 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: поднимается)

- **EN:** "
"So, what you're trying to say is that we will be left without a place to live?
- **ED_RU:** Впервые вижу, как поднимается гора.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 30 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: согласился)

- **EN:** "I was excited.
- **ED_RU:** Только не подумай, что я уже согласился сотрудничать.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

