# Выгрузка предфильтра (грамматика, кандидаты): v19-ch09.md

Кандидатов на разбор: **9** (agreement 1, passive-ru 2, possessive 2, voice 4).

Скрипт — не истина: каждый пункт либо исправляется по скиллу
russian-grammar-control, либо отклоняется с обоснованием в отчёте
аудита (ложное срабатывание).

## Блок 1 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: проснулись)

- **EN:** They were awakened by the sound of the opening door.
- **ED_RU:** Сайто и Тиффания проснулись от звука открывающейся двери.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 2 — Согласование: местоимение ед. ч. + глагол мн. ч. (RGC: заклинание … смогли)

- **EN:** She said it very seriously. Saito though about it a bit, then nodded.
"Ok. I promise."
"I returned your weapon but you can never kill an elf. You have to promise me."
"I promise."
"Then we should hurry."
Tiffania and Saito raised the hoods of the robes and followed Luctiana. Outside was a corridor with plastered walls that looked like concrete. There were plenty of doors similar to one they came from.
"Here."
Luctiana went forward walking with dignity.
They turned at the corner and saw five elves in official looking clothes. Few guards accompanied them. Tiffania and Saito tensed but Luctiana stopped and said to them in a low voice.
- **ED_RU:** Послышалось короткое заклинание — и они снова смогли двигаться.
- **Подсказка:** RGC-3: сказуемое согласуется с подлежащим в числе — и у местоимения («он лишились»), и у существительного подлежащего («сидение … запарили» → «… разморило», manual-fix v3-ch03 c25). Сверь, кто здесь подлежащее: если оно мн. ч. («гости ушли») — ложное срабатывание.

## Блок 3 — RU пассив «был + причастие»: проверь агента (RGC: отделан)

- **EN:** "
And they went away toward the room where the prisoners were held.
- **ED_RU:** Весь он был отделан штукатуркой, похожей на бетон, — и вдоль него тянулись двери, такие же, как в комнате, где они сидели.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 3 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: нравится)

- **EN:** "
And they went away toward the room where the prisoners were held.
- **ED_RU:** К тому же мне не нравится, как поступил Совет.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 5 — RU пассив «был + причастие»: проверь агента (RGC: поражён)

- **EN:** The street had sidewalks and roadways. In the roadways dragons pulled cars along the street.
Glass-walled stores distracted Saito. It was a strange fusion of a modern world and Earth's Middle Ages.
"The city of the Elves..."
Nobody paid any attention to Saito and Tiffania in elvish robes with their heads fully covered by hoods.
"Where are you taking us?"
"My old friend's place."
Luctiana went to stairs which led to a canal on one side of the street. There was a strong smell of the seashore.
"It's slippery, be careful."
Seaweed grew along the way to the canal, so Tiffania grasped Saito's hand. She slipped a few times, but Saito didn't let her fall. Her impressive breasts brushed his hand occasionally but he had no problem with that.
- **ED_RU:** Сверху он тоже был поражён, но теперь, когда город предстал перед ним вблизи, его красота была вне всякого сравнения.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 7 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: раздался)

- **EN:** To be abused like that by a selfish Luctiana...
- **ED_RU:** В этот момент с другого берега канала, примерно в пятнадцати метрах от них, раздался голос:
— Лодку?
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 9 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: пришлось)

- **EN:** Ali was a good swordsman, but the elf warrior was overwhelmed by the speed of Gandálfr.
- **ED_RU:** Тогда ему пришлось несладко из-за «Отражения».
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 10 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: Saito's position was)

- **EN:** It was difficult to jump into the middle of this sword fight, Tiffania hesitated.
"Oh, this is bad" said worried Luctiana.
"Huh?"
"It looks like Ali is using a 'sleep' spell."
Ali was casting a spell. After a small finishing gesture he pointed his hand at Saito, and Saito's eyes became muddled.
Tiffania remembered the strong drowsiness she felt during their kidnapping and trembled. Saito's position was desperate already and Ali continued to chant, reinforcing the spell.
At this rate, Saito would fall asleep.
- **ED_RU:** Если бы они атаковали прямолинейно, как стрелы, беды бы не было — но клинки Алия были не такими. Будто у них была своя воля, они наносили самые разные, неожиданные удары. Казалось, он дерётся сразу с пятью опытными воинами — и у этих воинов не было тела.
Иными словами, противник был почти непобедим.
Глядя на то, как тяжело приходится Сайто, Лукшана сказала с тревогой:
— Ой… похоже, против «мечей воли» Алия у него нет шансов.
— Не время тут спокойно рассуждать! Помоги Сайто!
Тиффания сказала это — и Лукшана покачала головой.
— Не могу. Сейчас вся сила духов в этих краях перешла к Алию. Он очень сильный «носитель» — мне некуда вмешаться.
Сайто отчаянно дрался одной левой рукой. Тиффания чуть не плакала. Неужели она ничего не может сделать?
Что-нибудь… но единственное заклинание, которым она владела, — «Забвение». Нужно подойти ближе. Но… можно ли подойти?
У неё не хватило духа броситься в эту схватку, и Тиффания медлила.
— Ох, плохо…
Лукшана произнесла это озабоченным голосом.
— А?
— Алий собрался применить «Сон».
Алий начал читать заклинание. Он сделал небольшой жест рукой, потом вытянул ладонь к Сайто — и глаза Сайто стали затуманиваться.
Похоже, он навёл усыпляющее заклинание. Наверное, когда их схватили, их тоже усыпили этим же.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 15 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: вырвавшейся)

- **EN:** The sword seemed to be embarrassed by his yell.
- **ED_RU:** Удар струи, вырвавшейся из пасти, был словно столкновение с самосвалом.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

