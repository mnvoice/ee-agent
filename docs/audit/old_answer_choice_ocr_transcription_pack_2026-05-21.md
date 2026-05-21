# Old Answer — Choice-OCR Source Transcription Pack (R0) (2026-05-21)

R0 review pack for the choice-OCR recovery track. This is the
transcription-prep sheet for a human to transcribe choices [1]-[4] directly
from the source PDF for the 2 OCR-damaged items. The reviewer source fields
are left blank — they are filled in the next round (R1).

This is an **R0 prep document only**. It does NOT modify `app/data`, does NOT
modify `choices`, and the source choice fields are NOT filled here.

- Base commit: `c13510b` (docs: design old answer choice ocr recovery)
- Design parent: `docs/audit/old_answer_choice_ocr_recovery_design_2026-05-21.md`
- Source review packs: `old_answer_manual_source_review_pack{,3}_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Purpose

- A review pack for a human to transcribe choices [1]-[4] directly from the
  source PDF for the 2 items whose DB-stored `choices` text is OCR-damaged.
- The `answer` for both items is already corrected and source-locked; this
  work is `choices` text recovery preparation only. It does not touch
  `answer`, `solution`, or `steps`.

## Verdict definitions

- `transcription_ready` — all four choices were legibly transcribed from the
  source PDF; the item is ready for the R3 choices-only apply.
- `needs_better_scan` — the source PDF page is too damaged to read one or
  more choices; a better scan is required.
- `defer` — the source is ambiguous, missing, or structurally unclear; hold.

## Transcription rules

- Transcribe the choice text exactly as it appears in the source PDF.
- For formulas / symbols, preserve the source meaning as faithfully as
  possible.
- Do NOT guess illegible characters — mark them in `evidence_note` instead.
- Set `transcription_ready` ONLY when all four choices are confidently read.
- Do NOT use an automated OCR result as the sole basis — the scanned old
  PDFs have low OCR quality (`DR-T35-V2A-AK-MAPPING-BLOCKED-001`).
- Do not modify `app/data/questions.json`, `app/data/questions.v2.json`,
  `choices`, `answer`, `solution`, `steps`, or `solution_svg` from this pack.

## Item 1 — `2001_3회_43`

- key: `2001_3회_43`
- current_answer: 2
- source_answer: 2
- source PDF path: `data/문제_2001_3회_20260316.pdf`
- source_page: q_no 43, p.4 (per source review pack 1)
- subject: 전기기기 / text: "정류자형 주파수 변환기의 설명 중 틀린 것은?"

current `choices` snapshot (DB, OCR-damaged):

- [1] `정류자 위에는 한 개의 자극마다 전기자 2π/3 간격으로 3조의 브러시가 있다.`
- [2] `3자 권선을 설치하여 1자 권선과 조정권선을 회전자에, 2자 권선을 고정자에 설치하였다.`
- [3] `3개의 승압콘은 회전자 권선을 3도분만 젬에 각각 접속되어 있다.`
- [4] `용량이 큰 것은 정류자용을 줄게 하기 위해 보상 권선과 보극권선을 고정자에 설치한다.`

suspected damaged choices: [2] and [3] are visibly garbled ("3자 권선" /
"1자 권선" likely "3차 / 1차 권선"; "승압콘", "3도분만 젬에" are non-words).
[1] and [4] are mostly readable but may carry minor OCR noise.

reviewer fields (blank — fill in R1):

```
source_choice_1:
source_choice_2:
source_choice_3:
source_choice_4:
source_page_confirmed:
evidence_note:
transcription_confidence:
verdict:
```

## Item 2 — `2015_3회_25`

- key: `2015_3회_25`
- current_answer: 4
- source_answer: 4
- source PDF path: `data/문제 _2015_3회_20260316.pdf` (note the space after
  `문제`)
- source_page: q_no 25, p.9 (per source review pack 3)
- subject: 전력공학 / text: "보호 계전기의 반한시•정한시 특성은?"

current `choices` snapshot (DB, OCR-damaged):

- [1] `：반한시 특성`
- [2] `：순한시 특성`
- [3] `：정한시 특성`
- [4] `15년도 3회` / `473` / `전기기사 펄기 D-60 시리즈` (newline-separated
  page-footer residue)

suspected damaged choices: [4] is entirely page-footer residue — the actual
choice [4] text is missing. [1]-[3] carry a stray leading "：" punctuation.

reviewer fields (blank — fill in R1):

```
source_choice_1:
source_choice_2:
source_choice_3:
source_choice_4:
source_page_confirmed:
evidence_note:
transcription_confidence:
verdict:
```

## Routing after transcription (R1/R2)

- `transcription_ready` → R3 choices-only apply (separate approval).
- `needs_better_scan` → hold; obtain a better scan.
- `defer` → hold.

## Status

- This is the R0 prep document. The source choice fields are NOT filled here.
- No `app/data` modification.
- Both items remain `choice_ocr_recovery_candidate`, not applied.
- `answer` for both items is already corrected and source-locked; this track
  recovers `choices` text only.
- Q2 bulk apply remains BLOCKED.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `choices` modification.
- No `answer` modification.
- No `solution` / `steps` modification.
- No `solution_svg` modification.
- No source choice transcription (deferred to R1).
- No paid API call.
- No push.
