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