# Omission pre-check (Common Omission Pre-check): v20-ch04.md

- **check_type:** `omission-precheck`
- **Глава:** v20-ch04.md
- **Проверено отредактированных блоков (ED_RU):** 17
- **Candidates:** 1
- **Уровень:** `severity=CANDIDATE` — pre-check не принимает решений; статус (CONFIRMED_ERROR / DISPUTED / FALSE_POSITIVE / OPTIONAL) выносит Analyzer по сверке JA → RU.
- **Сигналы:** S1 обрыв хвоста, S2 пустой RU, S3 числовой якорь.
- **Защита от FP:** сравнение длины JA/RU не используется; слияние абзацев без потери реплик не считается пропуском.

MISSING_TRANSLATION — BLOCK 8
Scope: DIALOGUE_FRAGMENT
Kind: PARTIAL
Severity: CANDIDATE

JA:
ビダーシャルは立ち止まると、

「きみはルクシャナを愛しているかね？」

RU (before):
— Ты любишь Лукшану? — спросил он.

RU (after):
Али посмотрел вдаль.

Missing:
Непокрытые JA-звенья (15…16 из 16):
ビダーシャルは立ち止まると、

「きみはルクシャナを愛しているかね？」

Reason:
Это обрыв, а не компрессия: в RU 15 абзацев против 16 в JA и 12 реплик-маркеров против 13 в JA — реплики и абзацы JA начиная с позиции 15…16 из 16 не покрыты вовсе. Допустимое сжатие и слияние (один RU-абзац вместо нескольких JA) сохраняют число реплик и все звенья; здесь же хвост JA отсутствует. Сравнение длины текста JA/RU в проверке НЕ использовалось. Решение принимает Analyzer.

Confidence: MEDIUM | Signal: S1-tail-truncation
---

