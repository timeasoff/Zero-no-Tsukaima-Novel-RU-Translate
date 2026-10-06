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
  agreement  — согласование числа подлежащего и сказуемого: (а) местоимение
               ед. ч. + глагол мн. ч. вплотную («он лишились»); (б) существительное
               ед. ч. (им./вин. на -ние/-тие/-енье/-ство) + глагол прош. мн. ч.
               в том же предложении («долгое сидение … запарили» — manual-fix
               v3-ch03, c25, RUSSIAN_ERROR); запятая с одной стороной (граница
               придаточного со своим подлежащим) гасит кандидат.
  numbers    — цифры 1–9 в ED_RU (правило russian-prose-rules: словами).

Использование:
    python scripts/grammar_scan.py --file v14-ch04.md
    python scripts/grammar_scan.py --file v14-ch04.md --report
    python scripts/grammar_scan.py --file v14-ch04.md --only voice,possessive
    python scripts/grammar_scan.py --file v14-ch04.md --strict
    python scripts/grammar_scan.py --selftest
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
# 4б. существительное ед. ч. как подлежащее + глагол прош. мн. ч. в том же
#     предложении (кейс c25 «долгое сидение … окончательно запарили»):
#     маркер ед. ч. — именительный/винительный на -ние/-тие/-енье/-ство
#     (родительный «сидения» оканчивается на -ия и не матчится), затем без
#     границы предложения (.:;!?…) глагол на -ли/-ши. Запятая с одной стороной
#     в промежутке = граница придаточного со своим подлежащим — кандидат гасим.
RU_AGREEMENT_NOUN_RE = re.compile(
    r"\b([а-яё]{3,}(?:ние|тие|енье|ство))\b"
    r"([^.!?…:;]{0,60}?)"
    r"\b([а-яё]{2,}(?:ли|ши))\b", re.I)
# подлежащее мн. ч./союз непосредственно перед «глаголом на -ли» — сам глагол
# согласован верно, а матчится существительное раньше в предложении
# (встречено на v3-ch10: «посторонние звуки более не долетали»)
AGREEMENT_NOUN_GUARD_RE = re.compile(
    r"(?:\b(?:все|они|мы|вы|гости|люди|ребята|девушки|мальчики|друзья"
    r"|и|а|но|или)\s*[—-]?\s*|не\s*[—-]?\s*|[а-яё]{2,}[иы]\s*[—-]?\s*)$",
    re.I)
# не глаголы/не сказуемые: наречия, союзы и существительные на -ли/-ши
# (встречены на v2-ch09/v3-ch10: «положение до боли», «расстояние … воли»,
# «мгновение … свинцовые пули»)
AGREEMENT_STOP = {"вдали", "издали", "коли", "ежели", "дотоли", "доли",
                  "ноши", "уши", "боли", "воли", "пули", "земли", "крови",
                  "голуби", "дубли", "рубли", "кули", "тесни"}
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
    "agreement": "RGC-3: сказуемое согласуется с подлежащим в числе — и у "
                 "местоимения («он лишились»), и у существительного "
                 "подлежащего («сидение … запарили» → «… разморило», "
                 "manual-fix v3-ch03 c25). Сверь, кто здесь подлежащее: "
                 "если оно мн. ч. («гости ушли») — ложное срабатывание.",
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

        # 4. согласование числа: (а) местоимение ед. ч. + глагол мн. ч.;
        #    (б) существительное ед. ч. + глагол прош. мн. ч. (кейс c25
        #    «долгое сидение … запарили»): запятая с одной стороной — граница
        #    придаточного со своим подлежащим, союз/местоимение мн. ч. перед
        #    глаголом — подлежащее названо после, такой кандидат гасим
        if "agreement" in only:
            for s in ed_sents:
                m = RU_AGREEMENT_RE.search(s)
                if m and m.group(2).lower() not in AGREEMENT_STOP:
                    findings.append({"para": num, "kind": "agreement",
                                     "ru": s, "en": en_sent,
                                     "word": "%s %s" % (m.group(1), m.group(2))})
                    break
                m = RU_AGREEMENT_NOUN_RE.search(s)
                if (m and m.group(3).lower() not in AGREEMENT_STOP
                        and m.group(2).count(",") % 2 == 0
                        and not AGREEMENT_NOUN_GUARD_RE.search(m.group(2))):
                    findings.append({"para": num, "kind": "agreement",
                                     "ru": s, "en": en_sent,
                                     "word": "%s … %s" % (m.group(1),
                                                          m.group(3))})
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


# ---- selftest: регрессия классов кандидатов (каждый случай — merged-подобный
# файл во временном каталоге; scan_path не зависит от каталога проекта) ----
SELFTEST_CASES = [
    # (имя случая, EN, ED_RU, ожидаемые kind-ы)
    ("pronoun: местоимение ед. ч. + глагол мн. ч.",
     "He lost the wand.",
     "Он лишились жезла.",
     {"agreement"}),
    ("noun c25: «сидение … запарили» (manual-fix v3-ch03)",
     "She stayed in the hot water for a long time.",
     "и долгое сидение в горячей воде окончательно запарили Сайто",
     {"agreement"}),
    ("noun c25 neg: то же с глаголом ед. ч. — нет кандидата",
     "She stayed in the hot water for a long time.",
     "А долгое сидение в горячей воде окончательно разморило Сайто",
     set()),
    ("noun neg: подлежащее мн. ч. после запятой (граница придаточного)",
     "The guests left at last.",
     "Долгое ожидание кончилось, и все гости наконец ушли.",
     set()),
    ("noun neg: подлежащее мн. ч. вплотную — guard-слово перед глаголом",
     "They all endured the silence.",
     "Молчание наконец все перетерпели.",
     set()),
    ("voice: EN пассив с деятелем + RU -ся",
     "The wand was stolen by the thief.",
     "Жезл у вора пропался без вести.",
     {"voice"}),
    ("passive-ru: «был украден» — проверь агента",
     "The thief stole the wand.",
     "Жезл был украден у Маликорна.",
     {"passive-ru"}),
    ("numbers: цифра 7 в ED_RU",
     "He counted seven coins.",
     "Он насчитал 7 монет.",
     {"numbers"}),
    ("clean: согласованное предложение — нет находок",
     "The guests left at last.",
     "Долгое сидение окончательно разморило Сайто, и все ушли.",
     set()),
]


def run_selftest() -> int:
    """Проверка на синтетических merged-файлах (не трогает merged/ проекта)."""
    import tempfile
    failed = 0
    with tempfile.TemporaryDirectory(prefix="grammar_scan_st_") as td:
        path = Path(td) / "chapter.md"
        for name, en, ed, want in SELFTEST_CASES:
            path.write_text(
                "## Блок 1\n\n**JA:**\n（テスト）\n\n**EN:**\n%s\n\n"
                "**RU:**\n%s\n\n**ED_RU:**\n%s\n" % (en, ed, ed),
                encoding="utf-8", newline="\n")
            got = {f["kind"] for f in scan_path(path, set(CHECKS))}
            ok = got == want
            if not ok:
                failed += 1
            print("  %s %s -> %s (want %s)" % (
                "OK  " if ok else "FAIL", name,
                sorted(got) or "нет", sorted(want) or "нет"))
    if failed:
        print("\n[selftest] ПРОВАЛЕНО: %d из %d" % (failed, len(SELFTEST_CASES)))
        return 1
    print("\n[selftest] OK: все %d контрольных кейсов пройдены"
          % len(SELFTEST_CASES))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="напр. v14-ch04.md")
    ap.add_argument("--only", default=",".join(CHECKS),
                    help="проверки через запятую (по умолчанию все: %s)"
                         % ", ".join(CHECKS))
    ap.add_argument("--report", action="store_true",
                    help="записать выгрузку предфильтра в output/_audit/_prefilter/<глава>-grammar.md")
    ap.add_argument("--strict", action="store_true",
                    help="вернуть код 1, если найдены кандидаты")
    ap.add_argument("--selftest", action="store_true",
                    help="прогнать регрессию на синтетических merged-кейсах")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(run_selftest())
    if not args.file:
        print("ОШИБКА: нужен --file (или --selftest)", file=sys.stderr)
        sys.exit(2)

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
