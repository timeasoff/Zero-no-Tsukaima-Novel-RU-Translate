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
