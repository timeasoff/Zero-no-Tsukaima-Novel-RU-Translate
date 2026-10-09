# Выгрузка предфильтра (грамматика, кандидаты): v5-ch04.md

Кандидатов на разбор: **5** (agreement 1, passive-ru 2, possessive 1, voice 1).

Скрипт — не истина: каждый пункт либо исправляется по скиллу
russian-grammar-control, либо отклоняется с обоснованием в отчёте
аудита (ложное срабатывание).

## Блок 3 — Согласование: местоимение ед. ч. + глагол мн. ч. (RGC: сражение … выиграли)

- **EN:** But the customer himself seemed to be used to that level of flattery.
- **ED_RU:** — И то сражение при Тарбе, считай, случайно выиграли!
- **Подсказка:** RGC-3: сказуемое согласуется с подлежащим в числе — и у местоимения («он лишились»), и у существительного подлежащего («сидение … запарили» → «… разморило», manual-fix v3-ch03 c25). Сверь, кто здесь подлежащее: если оно мн. ч. («гости ушли») — ложное срабатывание.

## Блок 3 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: улыбнулась)

- **EN:** But the customer himself seemed to be used to that level of flattery.
- **ED_RU:** Луиза приветливо улыбнулась.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 10 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: who's shoulders were)

- **EN:** Without moving, Louise held her camisole and bowed. That was all she could do.
"Now, go away, go away. I have no need for children. Off with you."
Saito saw Louise's temple twitch. It seemed she was angry. Saito prayed. Louise, don't snap! That guy's too dangerous!
"Oh, looking closer, you're not a kid... just a girl with small breasts."
Louise's face went pale. Her legs started to tremble slowly. Chulenne's face twisted with lust.
And then... extended his hands out towards Louise's small breasts.
"Now, how about this Chulenne-sama checks and see just how big they are."
At that moment...
The sole of a foot exploded onto Chulenne's face.
Toppling the chair, Chulenne rolled backwards.
"Wha, why you!"
The surrounding nobles pulled out their wands all at once.
In the front... was the silhouette of a boy who's shoulders were shaking with anger.
"Saito..."
Louise looked at the back of Saito, who had stood up to protect her. While looking at that back.... something hot filled her chest that had been shaking with anger.
As expected, Saito couldn't endure it anymore. Louise is trying her best, isn't she? My master doesn't have breasts, but she's cute, right? That Louise tried hard to compliment you, and what do you do? Just complain!
Well, complaining is fine. I say some at times too. It's Louise, so there's no helping that.
But... But...
There is one thing I can't forgive.
"Hey, old man, cut it out already."
"Da-damn you... To a noble's face, you..."
"Whether they're a noble, a prince, or a god... I definitely won't allow them to do it. It's my own special privilege. Who cares about nobles?! The only one that can touch Louise is me!"
Saito shouted.
- **ED_RU:** Луиза, не дрогнув, придержала камизоль и поклонилась. Другой любезности она не знала.
— Ну, иди-иди! Дети мне ни к чему. Ступай!
Сайто заметил, как у Луизы задёргался висок. Она, похоже, злится. Сайто взмолился. Луиза, не выходи из себя! Этот тип опасный!
— Хм, а приглядеться — так и не ребёнок… Просто девица с маленькой грудью.
Лицо Луизы побледнело. Ноги начали мелко дрожать. Лицо Тюренна похотливо искривилось.
А потом… он потянулся к её плоской груди.
— А ну-ка, сам Тюренн проверит её размер!
В тот же миг…
Подошва врезалась Тюренну в лицо.
Опрокинув стул, Тюренн покатился назад.
— Ах ты, мерзавец!
Разом все окрестные аристократы выхватили палочки.
Перед ними… стоял юноша, чьи плечи дрожали от гнева.
— Сайто…
Луиза смотрела в спину Сайто, вставшего, чтобы заслонить её. Глядя в эту спину… в груди, дрожавшей от гнева, разливалось что-то горячее.
Сайто и впрямь больше не мог терпеть.
_Луиза ведь старается. Пусть у моей госпожи и груди нет — зато она милая. И такая Луиза изо всех сил любезничает, а ты что? Знай себе придирается!_
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 17 — RU пассив «был + причастие»: проверь агента (RGC: собран)

- **EN:** Scarron said after looking at the wallets Chulenne and his men left on the ground.
- **ED_RU:** Сваленный хлам был собран в одном месте, и комнате придали вид, в котором кое-как можно жить.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 18 — RU пассив «был + причастие»: проверь агента (RGC: влюблён)

- **EN:** a large amount of money was stuffed there.
- **ED_RU:** Оттого ли, что он и без того был влюблён в Луизу, или то была «магия Очарования», наложенная на бюстье, — Сайто не понимал, но одно было верно.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

