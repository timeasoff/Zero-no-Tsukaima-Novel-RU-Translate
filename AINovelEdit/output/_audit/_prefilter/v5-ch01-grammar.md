# Выгрузка предфильтра (грамматика, кандидаты): v5-ch01.md

Кандидатов на разбор: **9** (agreement 1, passive-ru 2, possessive 2, voice 4).

Скрипт — не истина: каждый пункт либо исправляется по скиллу
russian-grammar-control, либо отклоняется с обоснованием в отчёте
аудита (ложное срабатывание).

## Блок 1 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: начинаются)

- **EN:** As always, Saito was being stepped on by Louise, and he, once again had to explain his reason for why he was being stepped on by Louise.
- **ED_RU:** — Что ж, с завтрашнего дня начинаются летние каникулы, — объявила Луиза, глядя сверху вниз на фамильяра.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 2 — Согласование: местоимение ед. ч. + глагол мн. ч. (RGC: благородство … щели)

- **EN:** Like a flower blooming in the wild, lots of charm poured out from there. Amazing when undressed, the chasm of the two hills flew into her eyes. Louise gave a "Ha-!" and looked at Saito's face. Underneath her foot, the familiar was desperately leering at the gap of Siesta's exposed shirt. Louise was about to snap but endured it.
Like I'll lose! That's right, I'm a noble. Even if I remain silent, nobility will pour out from the gaps of my shirt.
Louise followed suit. She murmurs "Fuuh, it's hot." and loosened her shirt's buttons. And then she wiped her sweat with a handkerchief. But... what was there was not a chasm, but a refreshing plain that spread out everywhere.
Saito seemed to prefer the terrain with highs and lows and did not move his glance.
- **ED_RU:** Молчи я хоть весь день — благородство само польётся из щели в моей рубашке!
- **Подсказка:** RGC-3: сказуемое согласуется с подлежащим в числе — и у местоимения («он лишились»), и у существительного подлежащего («сидение … запарили» → «… разморило», manual-fix v3-ch03 c25). Сверь, кто здесь подлежащее: если оно мн. ч. («гости ушли») — ложное срабатывание.

## Блок 4 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: подняться)

- **EN:** Then Louise said, "Going back home is halted.
- **ED_RU:** Луиза сделала серьёзный вид и подала знак Сайто подняться.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 5 — RU пассив «был + причастие»: проверь агента (RGC: написано)

- **EN:** Louise and Saito walked on the road under the scorching sun, heading towards Tristania. It takes two days to get there.
Looking reproachfully at the sun, Saito whispered,
"Damn... even though I should be at Siesta's house drinking cold water right now..."
"Don't complain! Come on! Walk!"
- **ED_RU:** Луиза объяснила, что было написано в письме.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

## Блок 7 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: disk's circumference was)

- **EN:** Without caring about Louise narrowing her eyebrows at them, Saito gazed at the gambling.
"What are you looking at?"
"Well, I was just thinking about earning money with this. How about it?"
"Isn't that gambling? What a thing!"
"Now, just watch me. I've done it a lot of times before in games."
Saito exchanged chips for thirty new gold coins... twenty écus and headed towards the table with the spinning disk. The disk's circumference was split into thirty-seven parts, each having their own number and colored red or black.
An iron ball spun around inside the disk. And near the disk, there were men and women with changed eye colors staring at this intently.
It was roulette.
Saito looked at the placing guests. First, I'll test my luck. Copying the winning guests, Saito placed a chip worth about ten écus on red.
The ball entered a red pocket.
"See, look. I earned some! I'm amazing!"
Saito was somewhat stingy, so he placed cautiously and earned about thirty écus worth of chips.
"See, look! The money we have for completing the mission increased! Geez, it's a big difference compared to a certain someone who only complains!"
- **ED_RU:** — Не хватает.
— Чего?
— Этих денег на расходы. С четырёхсот экю лошадь купишь — и ничего не останется.
— Лошадь-то зачем? Там же написано: скрывать положение, верно? Значит, притворись простолюдинкой. Пешком ходи. Ноги есть же.
— Притворяться простолюдинкой или нет — без лошади нормально поработать не выйдет!
— Лошадь подешевле сойдёт. Смирись.
— Такая лошадь в нужный момент бесполезна! И сбруя^[Сбруя — ремни и другие принадлежности для запряжки или седлания лошади.] тоже нужна. А ещё…. В дурных гостиницах я не остановлюсь. На эти деньги хватит всего на два с половиной месяца — и конец!
_Какая же это гостиница, где шестьсот золотых улетучиваются за мгновение?_
— Сойдёт и дешёвая гостиница.
— Нет! В дешёвом номере нормально не выспишься!
_Ну и аристократка. На задании среди простолюдинов — а ночевать собирается в дорогой гостинице._
_О чём она только думает?_ — подумал Сайто.
— У меня тоже есть. Могу одолжить.
— …Всё равно не хватит. Обслуживание ведь денег стоит.
— И что же делать?
— Нет ли способа их приумножить?
После долгих споров о том, как добыть деньги и не снять ли подешевле, они вошли в таверну — и Сайто обнаружил в углу устроенное казино.
Споря о том, как раздобыть деньги и где остановиться, они вошли в таверну — и Сайто обнаружил в углу устроенный зал для игры. Там пьяные мужчины и женщины сомнительного вида рубились на фишки: то отбирали чужие, то теряли свои. Сайто, не считаясь с тем, как хмурилась Луиза, уставился на игру.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 9 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: промахнулась)

- **EN:** "
"Until now, I've been betting on red or black, right?
- **ED_RU:** промахнулась.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 12 — Залог/актанты: EN пассив ↔ RU возвратный глагол (RGC: останется)

- **EN:** Saito was slightly relieved.
- **ED_RU:** Эти деньги нельзя было пускать в игру — тогда и сам Сайто останется без гроша.
- **Подсказка:** RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело действие. Возвратный глагол делает подлежащим того, КТО действует. Проверь схему: кто → что делает → кого/чего.

## Блок 17 — Актанты: EN «X's Y was …» (субъект RU — не X) (RGC: Guiche's clothes were)

- **EN:** "Haah? State yourself! You know, I, amazingly enough, am from a Duke's family..."
When she tried to say that, Saito stood up and covered Louise's mouth.
"Duke's family?"
"It-it's nothing! Yes! Her brain's just a bit like that. Yes."
Muffled, Louise thrashed around, but Saito ignored that and continued to cover her mouth. If they stood out anymore, it wouldn't be a secret mission anymore.
The man looked very interestedly at Saito and Louise. He was wearing rather showy clothes. Guiche's clothes were showy too, but the vector was strangely different. Black hair covered in oil, a sparkling, violet satin-earth shirt opened up at the chest with disheveled chest hair poking out, under his nose was a magnificent split chin and had a stylish mustache. A strong scent of perfume reached Saito's nose.
"Then why are you sleeping on the ground?"
"Well, we don't have a place to sleep or eat..."
"But we're not beggars."
Louise said bluntly. The man looked deeply at Louise's face.
"I see. Well then, come to my place. My name is Scarron. I run an inn. I'll prepare a room."
The man said that smiling. The way he talked and dressed was gross, but he seemed like a generous person. Saito's face glittered.
"Really?!"
"Yep, but there's one condition."
"I'll do anything."
"I'm managing a store on the first floor. This girl will help. That is the condition. Okay?"
- **ED_RU:** — Значит так: чеши шею ногой. Ну же!
Сайто указал на неё подбородком — и тут же получил подошвой Луизы прямо в лицо. Он рухнул на землю.
— Ты о чём вообще думаешь?! С-с-сказал мне изображать зверя?!
Сайто вскочил, схватил Лузу за руку и накричал.
— А как же без выступления-то! Есть другой способ подзаработать?! А-а-а!?
Луиза растрепала волосы и вцепилась в Сайто. Зрители странно так удовлетворенно кивали: «И правда волчица!»
Но просто смотреть, как они дерутся, зрителям быстро наскучило, и они разошлись. Ни копейки. Сайто обессилел и повалился на землю. Луиза тоже устала и вскоре выбилась из сил, после чего уселась ему на спину.
— Есть хочу…
— Я тоже…
Пока они так сидели, кто-то бросил им медную монету — «дзынь!». Сайто тут же подскочил и подхватил её. Луиза возмущённо вскочила.
— Кто это?! Выходи!
Из толпы вышел мужчина странного вида.
— Ох…… я ведь думала — вы попрошайки……
Он говорил как-то по-женски.
— А? А ну-ка поклонись мне! Я тебе не кто-нибудь! Перед тобой — герцогский дом…
Но, прежде чем она договорила, Сайто вскочил и закрыл ей рот.
- **Подсказка:** RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: «X лишили Y» / «у X отобрали Y» / «Y у X отобрали».

## Блок 18 — RU пассив «был + причастие»: проверь агента (RGC: зализаны)

- **EN:** Louise looked reluctant, but she obediently nodded when Saito stared at her.
"Très bien."
Scarron grouped his hands together and rest them on his cheek, and narrowing his lips, smiled. He acted like a gay. Actually, he couldn't be anything but a gay. Gross. There are gays in other worlds too... And there's that "très bien"... Saito became strangely depressed.
"Then it's decided. Follow me."
The man started walking, swinging his hips as if to a rhythm. Saito reluctantly took Louise's hand and followed.
"I kind of don't want to. He's weird."
- **ED_RU:** Чёрные волосы мужчины были зализаны назад и блестели от масла.
- **Подсказка:** RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN деятель назван, — сигнал потери актанта. Проверь, не должен ли русский быть активом или неопределённо-личным.

