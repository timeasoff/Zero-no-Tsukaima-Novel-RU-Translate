#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""style_scan.py — механический предфильтр лексико-стилистических проблем
(скилл russian-style-audit).

Не LLM: находит только ПОДОЗРИТЕЛЬНЫЕ места и печатает их как кандидатов.
Каждый кандидат обязан получить вердикт человека/агента:
ИСПРАВЛЕНО / ОТКЛОНЕНО / CANDIDATE (см. SKILL.md скилла).

Принцип консервативного расширения (обязателен при правке словарей):
новое правило добавляется ТОЛЬКО после реальной подтверждённой ошибки
из корпуса проекта + POSITIVE_CASE + зелёного --selftest. Расширение
«на будущее» («иногда бывает ошибкой», «на всякий случай») запрещено:
ложное срабатывание опаснее пропуска сомнительного кандидата.

Отсутствие кандидатов НЕ означает отсутствие стилистических проблем.

Использование:
    python scripts/style_scan.py --file output/v14-ch01.md
    python scripts/style_scan.py --file output/v14-ch01.md --report
"""

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Словари
# ---------------------------------------------------------------------------

# Тавтология / семантическая избыточность: пары "элемент1 элемент2".
# Совпадение ищется в пределах WINDOW слов друг от друга.
# Совпадение — кандидат, не ошибка: разговорные усиления бывают намеренными.
TAUTOLOGY_PAIRS = [
    ("вправду", "правда"), ("действительно", "правда"),
    ("главный", "суть"), ("главный", "основной"), ("основной", "суть"),
    ("свободная", "вакансия"), ("свободный", "вакансия"),
    ("памятный", "сувенир"), ("сувенир", "на память"),
    ("снова", "повторить"), ("повторить", "ещё раз"), ("повторить", "повторно"),
    ("продолжать", "дальше"), ("продолжить", "дальше"),
    ("вернуться", "обратно"), ("возвращаться", "обратно"),
    ("спуститься", "вниз"), ("спускаться", "вниз"),
    ("подняться", "вверх"), ("подниматься", "вверх"),
    ("заранее", "предупредить"), ("предупредить", "заранее"),
    ("совместное", "сотрудничество"), ("совместный", "сотрудничество"),
    ("предварительно", "планировать"), ("полностью", "завершить"),
    ("лично", "сам"), ("минута", "времени"),
    ("месяц", "времени"), ("период", "времени"),
    ("решить", "решение"),
]

# Избыточные усилители (два интенсификатора рядом).
INTENSIFIERS = [
    ("совершенно", "абсолютно"), ("абсолютно", "совершенно"),
    ("действительно", "на самом деле"), ("вполне", "полностью"),
    ("крайне", "сильно"), ("абсолютно", "точно"), ("полностью", "полностью"),
]

# Глагольные номинализации: слабый глагол + отглагольное существительное.
# Регэкспы вместо точных фраз: «осуществили/осуществляют/осуществить …».
NOMINALIZATION_PATTERNS = [
    r"осуществ\w*\s+проверк\w+", r"производ\w*\s+проверк\w+",
    r"осуществ\w*\s+осмотр\w*", r"производ\w*\s+осмотр\w*",
    r"осуществ\w*\s+перемещени\w*", r"осуществ\w*\s+попытк\w+",
    r"производ\w*\s+попытк\w+", r"оказ\w*\s+содействи\w*",
    r"производ\w*\s+поиск\w*", r"осуществ\w*\s+поиск\w*",
    r"производ\w*\s+действи\w*", r"дать\s+определение", r"иметь\s+наличие",
]

# Тяжёлые канцелярские связки в художественном тексте (кандидаты на коллокации).
BUREAUCRATIC = [
    "в связи с тем", "в рамках", "в целях", "осуществляет",
    "данный", "имеет место", "с точки зрения",
]

# Служебные слова, повторы которых не считаем.
STOPWORDS = {
    "и", "а", "но", "да", "или", "либо", "что", "чтобы", "как", "же", "ли",
    "бы", "б", "в", "во", "с", "со", "к", "ко", "у", "о", "об", "от", "до",
    "по", "за", "на", "из", "не", "ни", "ну", "вот", "это", "этот", "эта",
    "эти", "тот", "та", "те", "он", "она", "они", "оно", "его", "её", "их",
    "мой", "моя", "твой", "твоя", "свой", "своя", "наш", "ваш", "всё", "все",
    "весь", "вся", "уже", "ещё", "тоже", "также", "так", "там", "тут", "здесь",
    "когда", "если", "потом", "затем", "теперь", "только", "даже",
}

SUFFIX_RE = re.compile(
    r"(?:иями|ями|ами|ого|его|ому|ему|ыми|ими|ая|яя|ое|ее|ые|ие|ой|ей|ий|ый|"
    r"ом|ем|ым|ах|ях|ую|юю|ья|ье|ьи|ов|ев|ам|ям|ть|ла|ло|ли|ся|сь|ние|нье|"
    r"у|ю|а|я|о|е|ы|и|й|ь|л)$"
)

WINDOW = 3  # в пределах скольких слов ищем пару


def stem(word: str) -> str:
    w = word.lower()
    for _ in range(2):
        w2 = SUFFIX_RE.sub("", w)
        if len(w2) >= 4:
            w = w2
        else:
            break
    return w


def same_root(a: str, b: str) -> bool:
    sa, sb = stem(a), stem(b)
    if min(len(sa), len(sb)) < 4:
        return False
    common = 0
    for x, y in zip(sa, sb):
        if x != y:
            break
        common += 1
    return common >= 4


def tokenize(text: str):
    return re.findall(r"[а-яёА-ЯЁa-zA-Z]+(?:-[а-яёА-ЯЁa-zA-Z]+)?", text)


def word_matches(token: str, pattern_word: str) -> bool:
    """Точное совпадение, либо префиксное (после отбрасывания -ть/-ся/-сь),
    либо совпадение грубых стемов — чтобы ловить «вернулся» по «вернуться»,
    «повторила» по «повторить», «решил» по «решить»."""
    if token == pattern_word:
        return True
    base = re.sub(r"(?:ть|ся|сь)$", "", pattern_word)
    if len(base) >= 5 and token.startswith(base[:5]):
        return True
    return stem(token) == stem(pattern_word)


def find_pairs(tokens, pairs, cat):
    """Ищем пару (w1, w2) в пределах WINDOW слов (с морфологической допусккой)."""
    low = [t.lower() for t in tokens]
    for w1, w2 in pairs:
        for i, t in enumerate(low):
            if word_matches(t, w1) or word_matches(t, w2):
                other = w2 if word_matches(t, w1) else w1
                for j in range(i + 1, min(i + 1 + WINDOW, len(low))):
                    if word_matches(low[j], other):
                        yield (cat, w1, w2, i)
                        break


def scan_paragraph(idx, text):
    findings = []
    tokens = tokenize(text)

    # 1. Тавтологические пары
    for cat, a, b, pos in find_pairs(tokens, TAUTOLOGY_PAIRS, "TAUTOLOGY"):
        findings.append((idx, cat, f"«{a} … {b}» — тавтологическое/избыточное сочетание"))

    # 2. Усилители
    for cat, a, b, pos in find_pairs(tokens, INTENSIFIERS, "REDUNDANCY"):
        findings.append((idx, cat, f"«{a} … {b}» — двойной усилитель"))

    # 3. Номинализации и канцелярит (подстрока)
    low_text = text.lower()
    for pattern in NOMINALIZATION_PATTERNS:
        if re.search(pattern, low_text):
            findings.append((idx, "NOMINALIZATION",
                             f"«{pattern}» — отглагольная конструкция"))
    for phrase in BUREAUCRATIC:
        if phrase in low_text:
            findings.append((idx, "COLLOCATION", f"«{phrase}» — канцелярская связка"))

    # 4. Повтор одного значимого слова в абзаце
    counts = {}
    for t in tokens:
        lw = t.lower()
        if lw in STOPWORDS or len(lw) <= 3:
            continue
        counts[lw] = counts.get(lw, 0) + 1
    for w, n in counts.items():
        if n >= 3:
            findings.append((idx, "REPETITION", f"«{w}» повторяется {n} раза в абзаце"))
        elif n == 2 and len(w) >= 6:
            findings.append((idx, "REPETITION", f"«{w}» повторяется 2 раза в абзаце (проверить функцию)"))

    # 5. Однокоренные повторы рядом (окно 5 слов)
    low = [t.lower() for t in tokens]
    reported = set()
    for i, t in enumerate(low):
        if t in STOPWORDS or len(t) <= 4:
            continue
        for j in range(i + 2, min(i + 6, len(low))):
            u = low[j]
            if u in STOPWORDS or u == t or (i, u) in reported:
                continue
            if same_root(t, u):
                reported.add((i, u))
                findings.append((idx, "ROOT_REPETITION",
                                 f"«{t} … {u}» — однокоренные слова рядом"))
                break

    # 6. Прямые кавычки из машинного перевода
    if '"' in text:
        findings.append((idx, "OTHER", "прямая кавычка \" — заменить на «ёлочки» (prose-rules)"))

    return findings


def parse_blocks(path: Path):
    """Разбивает файл на абзацы (разделитель — пустая строка)."""
    text = path.read_text(encoding="utf-8")
    paragraphs, cur = [], []
    for line in text.splitlines():
        if line.strip() == "":
            if cur:
                paragraphs.append("\n".join(cur))
                cur = []
        else:
            if line.startswith("# ") or line.strip().startswith("<!--"):
                continue          # заголовок и маркеры <!-- block: N -->
            cur.append(line)
    if cur:
        paragraphs.append("\n".join(cur))
    return paragraphs


# ---------------------------------------------------------------------------
# Selftest: положительные (должны ловиться) и отрицательные (не должны)
# ---------------------------------------------------------------------------

POSITIVE_CASES = [
    "Неужели… Это и вправду правда?",
    "Он решил принять решение после долгого размышления.",
    "Она посмотрела на него. Его взгляд встретился с её взглядом.",
    "Он быстро подошёл к двери и быстрым движением открыл её.",
    "Мы осуществили проверку документов.",
    "Он вернулся обратно к дому.",
]

NEGATIVE_CASES = [
    "Он думал, что думал об этом слишком долго.",
    "Он медленно открыл дверь и вошёл в кабинет. В углу стоял книжный шкаф.",
    "Она очень сильно устала за этот день.",
    "Он принял решение утром. К вечеру сомнения в правильности выбранного пути рассеялись.",
]


def run_selftest() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    failed = []
    for text in POSITIVE_CASES:
        found = scan_paragraph(1, text)
        if not found:
            failed.append(("FIND", text))
            print(f"  FAIL FIND (не обнаружено): {text}")
        else:
            print(f"  OK   FIND: {text}")
    for text in NEGATIVE_CASES:
        found = scan_paragraph(1, text)
        if found:
            msgs = "; ".join(m for _, _, m in found)
            failed.append(("PASS", text))
            print(f"  FAIL PASS (сработало: {msgs}): {text}")
        else:
            print(f"  OK   PASS: {text}")
    if failed:
        print(f"\n[selftest] ПРОВАЛЕНО: {len(failed)} из "
              f"{len(POSITIVE_CASES) + len(NEGATIVE_CASES)}")
        return 1
    print(f"\n[selftest] OK: все {len(POSITIVE_CASES) + len(NEGATIVE_CASES)} "
          "контрольных кейсов пройдены")
    return 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Механический стилевой предфильтр (russian-style-audit)")
    ap.add_argument("--file", help="путь к RU-файлу главы")
    ap.add_argument("--selftest", action="store_true",
                    help="прогнать контрольные тесты (положительные и отрицательные)")
    ap.add_argument("--report", action="store_true",
                    help="сохранить выгрузку в output/_audit/_prefilter/")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()

    if not args.file:
        ap.error("нужен --file или --selftest")
        return 1
    path = Path(args.file)
    if not path.exists():
        print(f"[style_scan] файл не найден: {path}", file=sys.stderr)
        return 1

    paragraphs = parse_blocks(path)
    all_findings = []
    for i, p in enumerate(paragraphs, start=1):
        all_findings.extend(scan_paragraph(i, p))

    print(f"[style_scan] {path.name}: {len(paragraphs)} абзацев, "
          f"{len(all_findings)} кандидатов\n")
    if not all_findings:
        print("Кандидатов не найдено. Напоминаю: это НЕ означает отсутствие "
              "стилистических проблем — требуется полный аудит по чек-листу.")
        return 0

    for idx, cat, msg in all_findings:
        print(f"[{cat}] абзац {idx}: {msg}")

    if args.report:
        out_dir = path.parent / "_audit" / "_prefilter"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / (path.stem + "-style.md")
        with out.open("w", encoding="utf-8") as f:
            f.write(f"# Style prefilter: {path.name}\n\n")
            for idx, cat, msg in all_findings:
                f.write(f"- [{cat}] абзац {idx}: {msg}\n")
        print(f"\n[style_scan] отчёт: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
