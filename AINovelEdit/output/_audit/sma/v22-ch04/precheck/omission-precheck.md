# Omission pre-check (Common Omission Pre-check): v22-ch04.md

- **check_type:** `omission-precheck`
- **Глава:** v22-ch04.md
- **Проверено отредактированных блоков (ED_RU):** 12
- **Candidates:** 1
- **Уровень:** `severity=CANDIDATE` — pre-check не принимает решений; статус (CONFIRMED_ERROR / DISPUTED / FALSE_POSITIVE / OPTIONAL) выносит Analyzer по сверке JA → RU.
- **Сигналы:** S1 обрыв хвоста, S2 пустой RU, S3 числовой якорь.
- **Защита от FP:** сравнение длины JA/RU не используется; слияние абзацев без потери реплик не считается пропуском.

MISSING_TRANSLATION — BLOCK 4
Scope: DIALOGUE_FRAGMENT
Kind: PARTIAL
Severity: CANDIDATE

JA:
「やっぱり、怒ってる？」

才人が尋ねると、

RU (before):
Спросил Сайто.

RU (after):
— Да нет, будь он хоть человеком из другого мира — Сайто всё равно Сайто.

Missing:
Непокрытые JA-звенья (15…16 из 16):
「やっぱり、怒ってる？」

才人が尋ねると、

Reason:
Это обрыв, а не компрессия: в RU 15 абзацев против 16 в JA и 7 реплик-маркеров против 8 в JA — реплики и абзацы JA начиная с позиции 15…16 из 16 не покрыты вовсе. Допустимое сжатие и слияние (один RU-абзац вместо нескольких JA) сохраняют число реплик и все звенья; здесь же хвост JA отсутствует. Сравнение длины текста JA/RU в проверке НЕ использовалось. Решение принимает Analyzer.

Confidence: MEDIUM | Signal: S1-tail-truncation
---

