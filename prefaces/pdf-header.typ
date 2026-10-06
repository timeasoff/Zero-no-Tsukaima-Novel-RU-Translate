// Стили PDF для Typst.
//
// Файл: prefaces/pdf-header.typ — заполняется вручную; скрипт его не меняет.
// Подключается к сборке PDF автоматически (движок typst), либо явно:
//   python tools/merge_volume.py --volume 14 --pdf-header prefaces/pdf-header.typ
//
// ВАЖНО ПРО ПУТИ. Typst собирает документ в песочнице с корнем = корень
// проекта, поэтому картинку указывайте ОТ КОРНЯ проекта:
//   image("images/border.webp")     — верно
//   image("D:/.../border.webp")     — ошибка: абсолютные пути запрещены
//   image("../../images/…")         — ошибка: выход за пределы корня
//
// ВАЖНО ПРО КОДИРОВКУ. Файл должен быть в UTF-8 (кириллица в комментариях).
//
// Цвет ссылок задаётся автоматически (--pdf-link-color, по умолчанию #1f4e79).
// Переопределить можно раскомментировав строку ниже:
// #show link: set text(fill: rgb("#b3372f"))

// ─────────────────────────────────────────────────────────────────────────────
// РАМКА: уголки на четырёх углах каждой страницы
// border.webp — уголковый орнамент (левый верхний угол), поэтому остальные
// углы получаются поворотом на 90/180/270 градусов.
// ─────────────────────────────────────────────────────────────────────────────

#let corner = image("border.webp", width: 5cm)
#set page(background: {
  place(top + left, corner)
  place(top + right, rotate(90deg, corner))
  place(bottom + right, rotate(180deg, corner))
  place(bottom + left, rotate(270deg, corner))
})

// Размер уголка подбирается шириной: width: 5cm → 3.5cm → 2.5cm.
// Если рамку нужно отключить — закомментируйте блок выше.


// ─────────────────────────────────────────────────────────────────────────────
// ПАЛИТРА «КНИЖНОЙ» ВЁРСТКИ (общая для заголовков и отрывков)
// ─────────────────────────────────────────────────────────────────────────────

#let quote-paper = rgb("#f8f2e4")   // «бумага» блоков (лист внутри книги)
#let quote-frame = rgb("#c6b89f")   // цвет двойной рамки
#let quote-ink = rgb("#33291f")     // «чернила» (тёплый чёрный)
#let quote-accent = rgb("#8a6a3d")  // рубрики, акценты, орнамент-линии

// ─────────────────────────────────────────────────────────────────────────────
// ОРНАМЕНТ-ЛИНИЯ (резервный вариант).
// separator.webp, повторённый мелкими плитками во всю ширину колонки.
// Сейчас НЕ используется (ряд во всю длину оказался не очень) — лежит на
// случай, если захотите вернуть: ornament-line() в заголовке или разделителе.
//
// tile-w — ширина одной плитки: 20pt (мелкий узор), 28pt, 40pt (крупнее).
// ─────────────────────────────────────────────────────────────────────────────

#let ornament-line(tile-w: 28pt) = layout(size => {
  let n = calc.max(1, calc.floor(size.width / tile-w))

  stack(
    dir: ltr,
    spacing: 0pt,
    ..range(n).map(_ => box(
      width: tile-w,
      image("separator.webp", width: 100%),
    )),
  )
})

// Одиночный орнамент (для боковин заголовка и разделителя)
#let ornament(w: 1.5cm) = image("separator.webp", width: w)

// Тонкая линия цвета quote-frame — «волосок» книжной вёрстки
#let hairline = 0.6pt + quote-frame

// Декоративный разделитель сцены «---»: классическая связка
// «линия — орнамент — линия» по центру (перекрывает правило из
// tools/merge_volume.py — pdf-header подключается последним).
// Альтернативы (раскомментируйте одну строку вместо block ниже):
//   align(center, image("separator.webp", width: 2cm))   — один крупный орнамент
//   block(width: 100%, ornament-line())                  — ряд во всю ширину
#let horizontalrule = block(
  above: 1.6em,
  below: 1.6em,
  width: 100%,
  grid(
    columns: (1fr, auto, 1fr),
    column-gutter: 0.9em,
    align: horizon,
    line(length: 100%, stroke: hairline),
    ornament(w: 1.6cm),
    line(length: 100%, stroke: hairline),
  ),
)


// ─────────────────────────────────────────────────────────────────────────────
// ЗАГОЛОВКИ ГЛАВ.
// Каждый заголовок уровня 1 — «лист внутри книги» в той же рамке, что и
// отрывки-цитаты (та же палитра, двойная линия), ВМЕСТО уголков
// border_header.webp (картинка больше не используется):
//
//   ┌────────────────────────────────────────────────┐
//   │              ГЛАВА ПЕРВАЯ.                     │
//   │                Название главы                 │
//   └────────────────────────────────────────────────┘
//
// Без орнамента (вариант А): только двойная рамка, бумага и текст по центру.
// Отклонённые варианты (боковые виньетки с поворотом 90°, орнамент над
// текстом, связка «линия — орнамент — линия», волоски по бокам, флёр ❦)
// смотрелись на пробной странице хуже — ветка не кода, а решение.
//
// «Глава первая. Название» делится на строку-надзаголовок (капитель с
// разрядкой, акцентный цвет) и название (крупно, тёплые чернила) — сам
// перенос вставляет tools/merge_volume.py в typst-копию Markdown
// (см. _typst_break_input), здесь ничего делать не нужно.
// Отступы: перед заголовком 2.6em, после 1.6em — главы не слипаются с текстом.
//
// Настройка: inset внутреннего блока — «воздух» внутри рамки;
// sizes/kicker tracking — крупность и разрядка строк заголовка.
// ─────────────────────────────────────────────────────────────────────────────

// Заголовок без переноса → (none, заголовок); «Глава первая. ⏎ Название» →
// (строка-надзаголовок, название).
#let heading-parts(body) = {
  let kids = if body.has("children") { body.children } else { (body,) }
  let idx = kids.position(k => k.func() == linebreak)

  if idx == none or idx == 0 {
    (none, body)
  } else {
    (kids.slice(0, idx).join(), kids.slice(idx + 1).join())
  }
}

#show heading.where(level: 1): it => {
  let (kicker, title) = heading-parts(it.body)

  block(
    above: 2.6em,
    below: 1.6em,
    width: 100%,
    fill: quote-paper,
    stroke: 0.9pt + quote-frame,
    inset: 0.5em,
    block(
      width: 100%,
      stroke: 0.5pt + quote-frame,
      inset: (x: 1em, y: 1.1em),
      align(center, {
        show par: set par(leading: 0.35em, justify: false)

        if kicker != none {
          text(
            fill: quote-accent,
            weight: "bold",
            size: 0.92em,
            tracking: 0.28em,
            kicker,
          )
          linebreak()
          v(0.5em, weak: true)
        }

        text(fill: quote-ink, weight: "bold", size: 1.5em, title)
      }),
    ),
  )
}

// Рамка заголовка — та же конструкция, что у отрывков (см. ниже): внешняя
// линия 0.9pt → зазор 0.5em → внутренняя линия 0.5pt. Цвета — quote-frame.


// ─────────────────────────────────────────────────────────────────────────────
// ОТРЫВКИ, КОТОРЫЕ ПЕРСОНАЖИ ЧИТАЮТ (цитаты Markdown «>» → #quote).
//
// pandoc превращает абзацы «> …» в #quote(block: true)[…] — страницы
// «Молитвенника Основателя», указы, записки. Чтобы читатель сразу видел:
// это текст ВНУТРИ текста, — отрывок оформляется как «лист внутри книги»:
//
//   * тёплая бумага (quote-paper) и двойная тонкая рамка (quote-frame);
//   * текст чуть мельче, выключен по ширине, чернила тёплые (quote-ink);
//   * абзац целиком жирный (**Вступление**) — рубрика: по центру, с разрядкой
//     и акцентным цветом; если рубрика — первая, над ней ставится орнамент
//     separator.webp (та же картинка, что у разделителей «---»);
//   * прочее жирное внутри отрывка (**Издатель:** …) — акцентным цветом.
//
// Настройка «по-красивому»: quote-paper/quote-frame/quote-accent — цвета;
// inset внутреннего блока — воздух внутри листа; width орнамента — 1.4cm
// (0 → убрать, 2cm → крупнее); tracking у рубрики — плотность разрядки.
// ─────────────────────────────────────────────────────────────────────────────

// Палитра (quote-paper / quote-frame / quote-ink / quote-accent) — в начале
// файла, раздел «ПАЛИТРА «КНИЖНОЙ» ВЁРСТКИ».

// Абзац, целиком набранный жирным (**Вступление**) — рубрика отрывка.
// Допускается только пробелы и завершающая пунктуация
// (**Бримир Ру Румиру Юру Вири Ве Варутори**.).
#let quote-rubric(group) = {
  let strong-seen = false

  for child in group {
    let f = child.func()

    if f == strong {
      strong-seen = true
    } else if repr(f) == "space" {
      // пробелы между элементами строки
    } else if f == text and child.text.match(regex("^[\\s\\p{P}]*$")) != none {
      // только знаки препинания
    } else {
      return false
    }
  }

  strong-seen
}

// Содержимое цитаты → список абзацев (группы элементов между parbreak).
#let quote-paragraphs(body) = {
  let kids = if body.has("children") { body.children } else { (body,) }
  let groups = ()
  let current = ()

  for child in kids {
    if child.func() == parbreak {
      if current.len() > 0 {
        groups.push(current)
        current = ()
      }
    } else {
      current.push(child)
    }
  }

  if current.len() > 0 {
    groups.push(current)
  }

  // пустые группы (лишние пробелы) не нужны
  groups.filter(g => g.any(c => repr(c.func()) != "space"))
}

#show quote.where(block: true): it => {
  set text(fill: quote-ink, size: 0.95em)
  set par(justify: true, leading: 0.42em, spacing: 0.6em)
  show strong: s => text(fill: quote-accent, weight: "bold", s.body)

  let items = ()

  for (index, group) in quote-paragraphs(it.body).enumerate() {

    if quote-rubric(group) {

      let label = align(center,
        text(weight: "bold", tracking: 0.1em, fill: quote-accent, group.join()),
      )

      if index == 0 {
        // рубрика-заголовок в начале отрывка — над ней орнамент
        //items.push(block(width: 100%, above: 0em, below: 1.2em, {
         // align(center, image("separator.webp", width: 1.4cm))
         // v(0.8em)
         // label
        //}))

        items.push(block(width: 100%, above: 1em, below: 1.2em, label))
      } else {
        // промежуточная рубрика («Издан в Тристейне.»)
        items.push(block(width: 100%, above: 1.2em, below: 1.2em, label))
      }

    } else {
      items.push(group.join())
    }
  }

  if it.attribution != none {
    items.push(align(right,
      text(style: "italic", fill: quote-accent, it.attribution),
    ))
  }

  // «лист внутри книги»: внешняя линия → зазор → внутренняя линия → текст
  block(
    width: 100%,
    above: 1.7em,
    below: 1.7em,
    fill: quote-paper,
    stroke: 0.9pt + quote-frame,
    inset: 0.5em,
    block(
      width: 100%,
      stroke: 0.5pt + quote-frame,
      inset: (x: 1.6em, y: 1.4em),
      items.join(parbreak()),
    ),
  )
}


// ─────────────────────────────────────────────────────────────────────────────
// ИЛЛЮСТРАЦИИ.
// pandoc вставляет image() без явной ширины — typst берёт «натуральный» размер
// из DPI-метаданных файла (после пересохранения jpeg→jpg картинки становятся
// миниатюрными). Явно задаём: ширина = 100% ширины ТЕКСТОВОГО БЛОКА
// (то есть строго внутри полей страницы и внутри рамки-уголков),
// высота — по пропорциям (height не задаём, typst сохраняет aspect ratio).
// Центрируем. Уголки рамки не задеваются: они рисуются фоном страницы,
// а контент (и картинки) живёт в контентном боксе внутри полей 2cm.
// Явные width в image(...) (уголки выше) имеют приоритет над set-правилом.
// ─────────────────────────────────────────────────────────────────────────────

#set image(width: 100%)
#show image: it => align(center, it)


// ─────────────────────────────────────────────────────────────────────────────
// РАМКА без картинки: уголки линиями
// ─────────────────────────────────────────────────────────────────────────────
//
// #let corner-line(angle, len: 1.4cm, w: 0.8pt) = place(angle, box(
//   width: len, height: len,
//   stroke: (top: w, left: w, right: none, bottom: none),
// ))
// #set page(background: {
//   place(top + left, corner-line(top + left))
//   place(top + right, corner-line(top + right))
//   place(bottom + left, corner-line(bottom + left))
//   place(bottom + right, corner-line(bottom + right))
// })

// ─────────────────────────────────────────────────────────────────────────────
// СНОСКИ (ПРИМЕЧАНИЯ ПЕРЕВОДЧИКА)
// Сноски со звёздочкой (*), гармонирующие с виньетками и полями страницы
// ─────────────────────────────────────────────────────────────────────────────

#set footnote(numbering: "*")

#set footnote.entry(
  // Разделительная линия над сносками цвета #c6b89f
  separator: line(length: 30%, stroke: 0.5pt + rgb("#838383")),
  // Расстояние от основного текста до разделителя
  clearance: 1.5em,
  // Расстояние между несколькими сносками на одной странице
  gap: 0.7em,
  indent: 0pt,
)

// Значок сноски в основном тексте — полужирная увеличенная звёздочка
#show footnote: it => super(baseline: -0.15em)[#text(size: 1.5em, weight: "bold")[\*]]

// Шрифт сноски чуть меньше основного и с плотным межстрочным интервалом,
// а значок сноски внизу страницы также выделен полужирным
#show footnote.entry: it => {
  set text(size: 8.5pt)
  set par(leading: 0.45em)
  show super: s => text(size: 1.3em, weight: "bold")[\*]
  it
}
