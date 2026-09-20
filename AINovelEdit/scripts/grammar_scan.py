#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
grammar_scan.py — механический предфильтр грамматического контроля
(скилл russian-grammar-control).

Скрипт НИЧЕГО не правит и не выносит вердиктов: он сужает зону поиска,
превращая «проверить всю главу на морфологию и управление» (вся глава)
в список конкретных КАНДИДАТОВ (единицы-десяток мест на главу). Каждый
кандидат агент обязан разобрать по скиллу russian-grammar-control и либо
исправить, либо записать в отчёт обоснованный отказ (ложное срабатывание).

ED_RU и EN берутся из translates/_report/merged/<file> (обязательный
update_merged.py после правок), поэтому проверка идёт по смысловым блокам:
единица — блок (`## Блок N`), в котором JA/EN/RU/ED_RU уже выровнены.

Проверки:
  voice      — в EN пассив (was/were/been + причастие, «by the …»), а в
               ED_RU возвратный глагол (-ся/-сь): вероятна подмена
               подлежащего (канонический случай: EN "Malicorne's wand was
               stolen" → «Маликорна лишились жезла» вместо «лишили жезла»).
  possessive — в EN «X's Y was …ed»: подлежащее RU обязано быть Y (жезл)
               или безличное мн. ч. (лишили/отобрали), но не X (Маликорн).
  passive-ru — в ED_RU «был/была/было/были + краткое причастие»: проверить,
               назван ли в EN деятель и не потерян ли он в русском (EN-пассив
               здесь только усилитель сигнала, условием не является).
  agreement  — местоимение ед. ч. + глагол мн. ч. вплотную («он лишились»).
  numbers    — цифры 1–9 в ED_RU (правило russian-prose-rules: словами).

Использование:
    python scripts/grammar_scan.py --file v14-ch04.md
    python scripts/grammar_scan.py --file v14-ch04.md --report
    python scripts/grammar_scan.py --file v14-ch04.md --only voice,possessive
    python scripts/grammar_scan.py --file v14-ch04.md --strict
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

# ---------- RU: возвратные глаголы ----------
# слова, оканчивающиеся на -ся/-сь, но глаголами не являющиеся
REFLEXIVE_STOP = {
    "здесь", "ось", "авось", "небось", "вкось", "подкось", "накось",
    "вся", "весь", "вася", "люся", "муся", "ася", "тося", "веся",
    # не глаголы, а вводные/модальные слова с окончанием -ся
    "разумеется", "кажется", "казалось", "полагается", "признаться",
}
REFLEXIVE_RE = re.compile(r"\b([а-яё]{5,}(?:ся|сь))\b", re.I)
REFLEXIVE_END_RE = re.compile(
    r"(?:ться|тся|лся|лась|лось|лись|ешься|ется|ются|ится|ишься"
    r"|имся|итесь|ятся|йтесь|йся|усь|юсь|ёмся|емся|етесь|улся|улась"
    r"|улось|улись|аюсь|аешься|ается|аемся|аетесь|аются|еся|ись)$", re.I)

# ---------- EN: пассив ----------
IRREGULAR_PART = (
    "known|taken|stolen|given|made|seen|told|thrown|beaten|broken|brought"
    "|caught|held|left|lost|paid|put|sent|shown|spent|torn|written|eaten"
    "|driven|sold|struck|worn|kept|found|fed|felt|dealt|built|hung|shot"
    "|hit|cut|read|run|swept|drawn|forgotten|hidden|chosen"
)
EN_PASSIVE_RE = re.compile(
    r"\b(?:was|were|is|are|am|been|being|be|got|gets)\s+"
    r"(?:\w+\s+){0,2}?(?:\w+ed|" + IRREGULAR_PART + r")\b", re.I)
EN_AGENT_RE = re.compile(r"\bby\s+(?:the|his|her|their|its|a|an)\b", re.I)
EN_POSS_SS_RE = re.compile(r"\b\w+'s\s+\w+\s+(?:was|were)\b", re.I)

# ---------- RU: пассив и согласование ----------
RU_PASSIVE_RE = re.compile(
    r"\b(?:был|была|было|были)\s+([а-яё]{4,}(?:(?:ан|ян|ен|ён)(?:а|о|ы)"
    r"|(?:ан|ян|ен|ён|ат|ит|ут)))\b", re.I)
RU_AGREEMENT_RE = re.compile(
    r"\b(он|она|оно|я|ты)\s+([а-яё]{3,}(?:ли|лись))\b", re.I)
# не глаголы/не сказуемые: наречия и союзы на -ли
AGREEMENT_STOP = {"вдали", "издали", "коли", "ежели", "дотоли"}
# однозначное число цифрой; исключаются даты, дроби, проценты и разрядные
# группы («9 000», «1941») — правило russian-prose-rules их разрешает
RU_DIGIT_RE = re.compile(
    r"(?<![\d,.\-–—])(?<!\d\s)\d(?![\d,.\-–—%]|\s*%|\s*\d)")

KIND_TITLES = {
    "voice": "Залог/актанты: EN пассив ↔ RU возвратный глагол",
    "possessive": "Актанты: EN «X's Y was …» (субъект RU — не X)",
    "passive-ru": "RU пассив «был + причастие»: проверь агента",
    "agreement": "Согласование: местоимение ед. ч. + глагол мн. ч.",
    "numbers": "Числа: однозначные — словами (russian-prose-rules)",
}
KIND_HINT = {
    "voice": "RGC-1: в JA 受身/EN пассив подлежащее — то, ЧТО претерпело "
             "действие. Возвратный глагол делает подлежащим того, КТО "
             "действует. Проверь схему: кто → что делает → кого/чего.",
    "possessive": "RGC-1: «X's Y was stolen» ≠ «X лишился Y». Правильно: "
                  "«X лишили Y» / «у X отобрали Y» / «Y у X отобрали».",
    "passive-ru": "RGC-1: RU-пассив без деятеля («был схвачен») там, где в EN "
                  "деятель назван, — сигнал потери актанта. Проверь, не должен "
                  "ли русский быть активом или неопределённо-личным.",
    "agreement": "RGC-3: сказуемое согласуется с подлежащим в числе.",
    "numbers": "russian-prose-rules: однозначные числа и порядковые — словами.",
}
CHECKS = ("voice", "possessive", "passive-ru", "agreement", "numbers")


def read_paras(path):
    """Возвращает список (номер блока, {поле: текст}) из merged-файла.

    Разбор выполняет общий модуль merged_io (единица — смысловой блок).
    """
    return merged_io.read_merged(path)


def clean(s):
    return merged_io.clean(s)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if s.strip()]


def is_reflexive_verb(word):
    lw = word.lower()
    if lw in REFLEXIVE_STOP:
        return False
    return bool(REFLEXIVE_END_RE.search(lw))


def scan_path(path, only):
    """Ядро проверки: работает с любым merged-подобным файлом (нужен для тестов)."""
    findings = []
    for num, f in read_paras(path):
        en = clean(f.get("EN", ""))
        ed = clean(f.get("ED_RU", ""))
        if not ed or ed == "—" or not en or en == "—":
            continue

        en_sents = sentences(en)
        en_pass = EN_PASSIVE_RE.search(en)
        en_agent = EN_AGENT_RE.search(en)
        en_poss = EN_POSS_SS_RE.search(en)
        en_sent = next((x for x in en_sents if EN_PASSIVE_RE.search(x)), en)
        ed_sents = sentences(ed)

        # 1. залог/актанты: EN пассив (с агентом или «X's Y was») + RU -ся
        if "voice" in only and en_pass and (en_agent or en_poss):
            for s in ed_sents:
                hit = next((w for w in REFLEXIVE_RE.findall(s)
                            if is_reflexive_verb(w)), None)
                if not hit:
                    continue
                kind = "possessive" if en_poss else "voice"
                if kind not in only:
                    break
                findings.append({"para": num, "kind": kind, "ru": s,
                                 "en": en_sent, "word": hit})
                break

        # 2. «X's Y was …» даже без возвратного глагола в RU
        if "possessive" in only and en_poss:
            if not any(x["para"] == num and x["kind"] == "possessive"
                       for x in findings):
                findings.append({"para": num, "kind": "possessive", "ru": ed,
                                 "en": en_sent, "word": en_poss.group(0)})

        # 3. RU пассив «был + краткое причастие»: проверь, назван ли деятель
        #    в EN и не потерян ли он в русском (EN-пассив — усилитель сигнала,
        #    а не условие: важнее как раз случай «EN актив, RU без агента»)
        if "passive-ru" in only:
            m = RU_PASSIVE_RE.search(ed)
            if m:
                findings.append({
                    "para": num, "kind": "passive-ru", "word": m.group(1),
                    "ru": next((s for s in ed_sents if RU_PASSIVE_RE.search(s)), ed),
                    "en": en_sent if en_pass else en})

        # 4. согласование: местоимение ед. ч. + глагол мн. ч.
        if "agreement" in only:
            for s in ed_sents:
                m = RU_AGREEMENT_RE.search(s)
                if m and m.group(2).lower() not in AGREEMENT_STOP:
                    findings.append({"para": num, "kind": "agreement",
                                     "ru": s, "en": en_sent,
                                     "word": "%s %s" % (m.group(1), m.group(2))})
                    break

        # 5. однозначные числа цифрами
        if "numbers" in only:
            for s in ed_sents:
                m = RU_DIGIT_RE.search(s)
                if m:
                    findings.append({"para": num, "kind": "numbers", "ru": s,
                                     "en": "", "word": m.group(0)})
                    break

    findings.sort(key=lambda x: (x["para"], x["kind"]))
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
    lines = ["# Выгрузка предфильтра (грамматика, кандидаты): %s" % name, ""]
    lines.append("Кандидатов на разбор: **%d** (%s)." % (
        len(findings),
        ", ".join("%s %d" % (k, kinds[k]) for k in sorted(kinds)) or "нет"))
    lines += ["", "Скрипт — не истина: каждый пункт либо исправляется по скиллу",
              "russian-grammar-control, либо отклоняется с обоснованием в отчёте",
              "аудита (ложное срабатывание).", ""]
    for f in findings:
        lines.append("## Блок %d — %s (RGC: %s)" % (
            f["para"], KIND_TITLES[f["kind"]], f["word"]))
        lines.append("")
        if f["en"]:
            lines.append("- **EN:** %s" % f["en"])
        lines.append("- **ED_RU:** %s" % f["ru"])
        lines.append("- **Подсказка:** %s" % KIND_HINT[f["kind"]])
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="напр. v14-ch04.md")
    ap.add_argument("--only", default=",".join(CHECKS),
                    help="проверки через запятую (по умолчанию все: %s)"
                         % ", ".join(CHECKS))
    ap.add_argument("--report", action="store_true",
                    help="записать выгрузку предфильтра в output/_audit/_prefilter/<глава>-grammar.md")
    ap.add_argument("--strict", action="store_true",
                    help="вернуть код 1, если найдены кандидаты")
    args = ap.parse_args()

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
        dst = AUDIT / ("%s-grammar.md" % Path(args.file).stem)
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
