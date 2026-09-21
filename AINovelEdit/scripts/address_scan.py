#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
address_scan.py — механический предфильтр проверки обращений
(скилл forms-of-address).

Скрипт НИЧЕГО не правит и не выносит вердиктов: он сужает зону поиска,
превращая «проверить всю главу на обращения» в список конкретных КАНДИДАТОВ
(единицы-десятки мест на главу). Каждый кандидат агент обязан разобрать
по скиллу forms-of-address и либо исправить, либо записать в отчёт
обоснованный отказ (ложное срабатывание).

ED_RU и EN берутся из translates/_report/merged/<file> (обязательный
update_merged.py после правок), поэтому проверка идёт по смысловым блокам:
единица — блок (`## Блок N`), в котором JA/EN/RU/ED_RU уже выровнены.

Проверка:
  address — после ключевых слов «мисс», «мистер», «господин», «госпожа»
            (и «госпож» без окончания) следующее слово начинается с заглавной
            буквы (предположительно имя собственное). Такие места помечаются
            как требующие ручной проверки: возможно, обращение должно быть
            заменено на культурно-корректное (мадемуазель/месье/мадам) или
            удалено вовсе если его нет в оригинале.

Использование:
    python scripts/address_scan.py --file v14-ch04.md
    python scripts/address_scan.py --file v14-ch04.md --report
    python scripts/address_scan.py --file v14-ch04.md --strict
"""
import argparse
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import merged_io  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
MERGED = BASE / "translates" / "_report" / "merged"
AUDIT = BASE / "output" / "_audit" / "_prefilter"

SENT_RE = re.compile(r"[^.!?…]+[.!?…]*")

# Ключевые слова обращений (проверка без окончания "госпож" для "госпожа")
ADDRESS_PREFIXES = ["мисс", "мистер", "господин", "госпожа", "госпож"]

# Регэксп для поиска обращений: ключевое слово + пробелы + слово с заглавной буквы
# Слово с заглавной буквы — предполагаемое имя собственное
ADDRESS_RE = re.compile(
    r"\b(" + "|".join(ADDRESS_PREFIXES) + r")\s+([А-ЯЁ][а-яё]+)",
    re.IGNORECASE
)

KIND_TITLES = {
    "address": "Обращения: мисс/мистер/господин/госпожа + имя собственное",
}
KIND_HINT = {
    "address": "FA-1: Проверь по addresses.md: 1) есть ли обращение в JA/EN; "
               "2) культурная норма говорящего (Тристейн → мадемуазель/месье); "
               "3) не добавлено ли обращение «из воздуха». "
               "Если JA/EN не содержат Miss/Mister/Lord/Lady и т.п. — удалить. "
               "Если содержат — заменить на форму по королевству говорящего.",
}
CHECKS = ("address",)


# ---------------------------------------------------------------------------
# Selftest: положительные (должны ловиться) и отрицательные (не должны)
# ---------------------------------------------------------------------------

POSITIVE_CASES = [
    "Мисс Вальер пришла в комнату.",
    "Мистер Осман был здесь вчера.",
    "Господин де ла Рош поклонился.",
    "Госпожа Вальер сказала ему.",
    "Госпож Вальер не было на месте.",
]

NEGATIVE_CASES = [
    "Мадемуазель Вальер улыбнулась.",
    "Месье Смит вошёл в зал.",
    "мадемуазель Вальер села за стол.",
    "Луиза Вальер была здесь.",
    "Она обратилась к нему по имени.",
]


def run_selftest() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    failed = []
    for text in POSITIVE_CASES:
        candidates = find_address_candidates(text)
        if not candidates:
            failed.append(("FIND", text))
            print(f"  FAIL FIND (не обнаружено): {text}")
        else:
            print(f"  OK   FIND: {text}")
    for text in NEGATIVE_CASES:
        candidates = find_address_candidates(text)
        if candidates:
            found_str = ", ".join(f"{c['prefix']} {c['name']}" for c in candidates)
            failed.append(("PASS", text))
            print(f"  FAIL PASS (сработало: {found_str}): {text}")
        else:
            print(f"  OK   PASS: {text}")
    if failed:
        print(f"\n[selftest] ПРОВАЛЕНО: {len(failed)} из "
              f"{len(POSITIVE_CASES) + len(NEGATIVE_CASES)}")
        return 1
    print(f"\n[selftest] OK: все {len(POSITIVE_CASES) + len(NEGATIVE_CASES)} "
          "контрольных кейсов пройдены")
    return 0


def read_paras(path):
    """Возвращает список (номер блока, {поле: текст}) из merged-файла.

    Разбор выполняет общий модуль merged_io (единица — смысловой блок).
    """
    return merged_io.read_merged(path)


def clean(text):
    return merged_io.clean(text)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if s.strip()]


def find_address_candidates(ed_ru):
    """Находит все кандидаты с обращениями в тексте ED_RU."""
    candidates = []
    for match in ADDRESS_RE.finditer(ed_ru):
        prefix = match.group(1).lower()
        name_word = match.group(2)
        # Нормализуем префикс для отображения
        if prefix == "госпож":
            # Проверяем полное слово в тексте
            full_word = match.group(0).split()[0]
            prefix = full_word.lower()
        candidates.append({
            "prefix": prefix,
            "name": name_word,
            "span": match.span(),
            "context": ed_ru[max(0, match.start() - 30):min(len(ed_ru), match.end() + 30)],
        })
    return candidates


def scan_path(path, only):
    """Ядро проверки: работает с любым merged-подобным файлом (нужен для тестов)."""
    findings = []
    for num, f in read_paras(path):
        ed = clean(f.get("ED_RU", ""))
        en = clean(f.get("EN", ""))
        if not ed or ed == "—":
            continue

        if "address" in only:
            candidates = find_address_candidates(ed)
            for c in candidates:
                # Находим предложение, содержащее кандидат
                ed_sents = sentences(ed)
                for s in ed_sents:
                    if c["prefix"] in s.lower() and c["name"] in s:
                        findings.append({
                            "para": num,
                            "kind": "address",
                            "ru": s,
                            "en": next((x for x in sentences(en) if c["name"] in x), ""),
                            "prefix": c["prefix"],
                            "name": c["name"],
                        })
                        break

    findings.sort(key=lambda x: x["para"])
    return findings


def scan_file(name, only):
    """Проверка главы из translates/_report/merged/."""
    path = MERGED / name
    if not path.exists():
        print("ОШИБКА: нет merged-файла %s — сначала прогони:\n"
              "  python scripts/update_merged.py --file %s" % (path, name),
              file=sys.stderr)
        sys.exit(2)
    return scan_path(path, only)


def render(name, findings):
    kinds = {}
    for f in findings:
        kinds[f["kind"]] = kinds.get(f["kind"], 0) + 1
    lines = ["# Выгрузка предфильтра (обращения, кандидаты): %s" % name, ""]
    lines.append("Кандидатов на разбор: **%d** (%s)." % (
        len(findings),
        ", ".join("%s %d" % (k, kinds[k]) for k in sorted(kinds)) or "нет"))
    lines += ["", "Скрипт — не истина: каждый пункт либо исправляется по скиллу",
              "forms-of-address, либо отклоняется с обоснованием в отчёте",
              "аудита (ложное срабатывание).", ""]
    for f in findings:
        lines.append("## Блок %d — %s («%s %s»)" % (
            f["para"], KIND_TITLES[f["kind"]], f["prefix"], f["name"]))
        lines.append("")
        if f["en"]:
            lines.append("- **EN:** %s" % f["en"])
        lines.append("- **ED_RU:** %s" % f["ru"])
        lines.append("- **Подсказка:** %s" % KIND_HINT[f["kind"]])
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="напр. v14-ch04.md")
    ap.add_argument("--selftest", action="store_true",
                    help="прогнать контрольные тесты (положительные и отрицательные)")
    ap.add_argument("--only", default=",".join(CHECKS),
                    help="проверки через запятую (по умолчанию все: %s)"
                         % ", ".join(CHECKS))
    ap.add_argument("--report", action="store_true",
                    help="записать выгрузку предфильтра в output/_audit/_prefilter/<глава>-address.md")
    ap.add_argument("--strict", action="store_true",
                    help="вернуть код 1, если найдены кандидаты")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()

    if not args.file:
        ap.error("нужен --file или --selftest")
        return 1

    only = {x.strip() for x in args.only.split(",") if x.strip()}
    unknown = sorted(only - set(CHECKS))
    if unknown or not only:
        print("ОШИБКА: неизвестная проверка %s. Доступны: %s"
              % (", ".join(unknown) or "(пусто)", ", ".join(CHECKS)),
              file=sys.stderr)
        sys.exit(2)
    findings = scan_file(args.file, only)
    report = render(args.file, findings)

    if args.report:
        AUDIT.mkdir(parents=True, exist_ok=True)
        dst = AUDIT / ("%s-address.md" % Path(args.file).stem)
        dst.write_text(report, encoding="utf-8", newline="\n")
        print("OK: выгрузка → output/_audit/_prefilter/%s | кандидатов %d"
              % (dst.name, len(findings)))
    else:
        sys.stdout.write(report)
        print("Итого кандидатов: %d" % len(findings))

    if args.strict and findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
