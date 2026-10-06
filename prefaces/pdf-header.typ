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
// ЗАГОЛОВКИ ГЛАВ.
// Каждый заголовок уровня 1 оборачивается в прозрачный блок с padding,
// а блок декорируется уголками из header_border_trim.webp — той же картинкой,
// что и рамка страницы, но только ДВА угла: правый верхний (как есть —
// картинка уже нарисована как правый верхний уголок) и левый нижний
// (поворот на 180 градусов).
// Отступы: перед заголовком 3em, после 1.5em — главы не сливаются с текстом.
// Заголовок «Глава первая. Название» делится на две строки (после точки) —
// сам перенос вставляет tools/merge_volume.py в typst-копию Markdown
// (см. _typst_break_input), здесь ничего делать не нужно.
// ─────────────────────────────────────────────────────────────────────────────

#let header_corner = image("border_header.webp", width: 1.7cm)

#show heading.where(level: 1): it => block(
  above: 3em,
  below: 1.5em,
  width: 100%,
  {
    place(top + right, header_corner)
    place(bottom + left, rotate(180deg, header_corner))
    box(
      width: 100%,
      inset: (top: 1.6em, bottom: 1.6em, left: 2.2em, right: 2.2em),
      align(center, {
        show par: set par(leading: 0.3em)
        it
      }),
    )
  },
)

// Размер уголка и отступы блока подбираются так же, как у рамки страницы:
// width: 1.7cm → 1.2cm → 0.9cm; inset управляет «воздухом» вокруг заголовка.


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

#let quote-paper = rgb("#f8f2e4")   // «бумага» отрывка (лист внутри книги)
#let quote-frame = rgb("#c6b89f")   // цвет двойной рамки
#let quote-ink = rgb("#33291f")     // «чернила» отрывка (тёплый чёрный)
#let quote-accent = rgb("#8a6a3d")  // рубрики и жирного внутри отрывка

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
