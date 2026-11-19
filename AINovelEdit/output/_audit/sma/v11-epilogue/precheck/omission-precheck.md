# Omission pre-check (Common Omission Pre-check): v11-epilogue.md

- **check_type:** `omission-precheck`
- **Глава:** v11-epilogue.md
- **Проверено отредактированных блоков (ED_RU):** 5
- **Candidates:** 1
- **Уровень:** `severity=CANDIDATE` — pre-check не принимает решений; статус (CONFIRMED_ERROR / DISPUTED / FALSE_POSITIVE / OPTIONAL) выносит Analyzer по сверке JA → RU.
- **Сигналы:** S1 обрыв хвоста, S2 пустой RU, S3 числовой якорь.
- **Защита от FP:** сравнение длины JA/RU не используется; слияние абзацев без потери реплик не считается пропуском.

MISSING_TRANSLATION — BLOCK 2
Scope: DIALOGUE_FRAGMENT
Kind: PARTIAL
Severity: CANDIDATE

JA:
するとルイズは、ぽろっと言った。

「わたしも、飲んでみたいな。サイトの国のスープ」

RU (before):
— Я тоже хочу попробовать. Суп из твоей страны, Сайто.

RU (after):
Щёки Сайто покраснели сильнее, чем во время поцелуя.

Missing:
Непокрытые JA-звенья (15…16 из 16):
するとルイズは、ぽろっと言った。

「わたしも、飲んでみたいな。サイトの国のスープ」

Reason:
Это обрыв, а не компрессия: в RU 14 абзацев против 16 в JA и 11 реплик-маркеров против 12 в JA — реплики и абзацы JA начиная с позиции 15…16 из 16 не покрыты вовсе. Допустимое сжатие и слияние (один RU-абзац вместо нескольких JA) сохраняют число реплик и все звенья; здесь же хвост JA отсутствует. Сравнение длины текста JA/RU в проверке НЕ использовалось. Решение принимает Analyzer.

Confidence: MEDIUM | Signal: S1-tail-truncation
---

