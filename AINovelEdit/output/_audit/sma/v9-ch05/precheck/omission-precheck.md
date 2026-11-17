# Omission pre-check (Common Omission Pre-check): v9-ch05.md

- **check_type:** `omission-precheck`
- **Глава:** v9-ch05.md
- **Проверено отредактированных блоков (ED_RU):** 31
- **Candidates:** 1
- **Уровень:** `severity=CANDIDATE` — pre-check не принимает решений; статус (CONFIRMED_ERROR / DISPUTED / FALSE_POSITIVE / OPTIONAL) выносит Analyzer по сверке JA → RU.
- **Сигналы:** S1 обрыв хвоста, S2 пустой RU, S3 числовой якорь.
- **Защита от FP:** сравнение длины JA/RU не используется; слияние абзацев без потери реплик не считается пропуском.

MISSING_TRANSLATION — BLOCK 20
Scope: DIALOGUE_FRAGMENT
Kind: PARTIAL
Severity: CANDIDATE

JA:
「こんな清楚で可愛いわたしを見たら、あの虫けらはひれ伏すしかないわね」

「さよか」

RU (before):
— Угу.

RU (after):
— Фу-фу. Фу-фу-фу-фу-фу… — захихикала Луиза.

Missing:
Непокрытые JA-звенья (15…16 из 16):
「こんな清楚で可愛いわたしを見たら、あの虫けらはひれ伏すしかないわね」

「さよか」

Reason:
Это обрыв, а не компрессия: в RU 13 абзацев против 16 в JA и 12 реплик-маркеров против 14 в JA — реплики и абзацы JA начиная с позиции 15…16 из 16 не покрыты вовсе. Допустимое сжатие и слияние (один RU-абзац вместо нескольких JA) сохраняют число реплик и все звенья; здесь же хвост JA отсутствует. Сравнение длины текста JA/RU в проверке НЕ использовалось. Решение принимает Analyzer.

Confidence: MEDIUM | Signal: S1-tail-truncation
---

