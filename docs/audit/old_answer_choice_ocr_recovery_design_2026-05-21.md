# Old Answer — Choice-OCR Recovery Track Design (2026-05-21)

Design document for the choice-OCR recovery track. The source answer
correction track closed the `answer` and `solution` / `steps` for the
1998-2016 old pilot conflict items, but two items carry a remaining flag:
their DB-stored `choices` text is OCR-damaged. This document designs how to
recover those `choices` fields.

This is a **design document only**. It does NOT modify `app/data`, does NOT
modify `choices`, and is not an approval to apply.

- Reasoning review / SVG audit: `fb3bb91`, `10d8901`
- C20 closeout: `5277967`
- Source review packs: `old_answer_manual_source_review_pack{,3}_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## 1. Background

- The C20 answer correction track corrected `q.answer` and reconciled
  `solution` / `steps` for the 19 single-answer conflict items, and
  `2016_1회_44`'s reasoning cleanup is closed.
- Two of those items additionally carry a `choices`-field OCR-damage flag,
  raised during the C20-1 / C20-3 solution dry-runs and the SVG audit:
  `2001_3회_43` and `2015_3회_25`.
- `choices` modification is more sensitive than `answer` / `solution`
  modification: the `choices` text is what the learner reads and selects
  against, and the `answer` index points into it. A damaged choice text must
  be recovered from the source PDF, not reconstructed from theory. This
  warrants a separate, dedicated design.

## 2. Target items (2)

`route` = `choice_ocr_recovery_candidate` for both. `current status` =
answer + solution closed; `choices` OCR-damaged.

### `2001_3회_43`

- `current_answer` / `source_answer`: 2
- subject: 전기기기 / text: "정류자형 주파수 변환기의 설명 중 틀린 것은?"
- current `choices` snapshot:
  - [1] `정류자 위에는 한 개의 자극마다 전기자 2π/3 간격으로 3조의 브러시가 있다.`
  - [2] `3자 권선을 설치하여 1자 권선과 조정권선을 회전자에, 2자 권선을 고정자에 설치하였다.`
  - [3] `3개의 승압콘은 회전자 권선을 3도분만 젬에 각각 접속되어 있다.`
  - [4] `용량이 큰 것은 정류자용을 줄게 하기 위해 보상 권선과 보극권선을 고정자에 설치한다.`
- suspected damaged choices: [2] and [3] are visibly garbled
  ("3자 권선" / "1자 권선" — likely "3차/1차 권선"; "승압콘" / "3도분만 젬에"
  are non-words). [1] and [4] are mostly readable but may also carry minor
  OCR noise.
- source PDF path / page: `data/문제_2001_3회_20260316.pdf`, q_no 43, p.4
  (per source review pack 1).
- current status: `answer`=2 corrected, `solution` / `steps` closed
  (source-locked to ②, error detail deferred due to this OCR damage).

### `2015_3회_25`

- `current_answer` / `source_answer`: 4
- subject: 전력공학 / text: "보호 계전기의 반한시•정한시 특성은?"
- current `choices` snapshot:
  - [1] `：반한시 특성`
  - [2] `：순한시 특성`
  - [3] `：정한시 특성`
  - [4] `15년도 3회\n473\n전기기사 펄기 D-60 시리즈`
- suspected damaged choices: [4] is entirely page-footer residue
  ("15년도 3회 / 473 / 전기기사 펄기 D-60 시리즈") — the actual choice [4]
  text is missing. [1]-[3] carry a stray leading "：" punctuation.
- source PDF path / page: `data/문제 _2015_3회_20260316.pdf` (note the space
  after `문제`), q_no 25, p.9 (per source review pack 3).
- current status: `answer`=4 corrected, `solution` / `steps` consistent
  (already name choice ④ as "반한시-정한시 특성").

## 3. Policy boundary

### Allowed (after separate per-item approval)

- Recover the `choices` field text from the source PDF choice text.
- Modify `app/data/questions.json` and `app/data/questions.v2.json` together.
- Write a choice recovery audit document.

### Prohibited

- Modifying `choices` before the source PDF choice text is confirmed.
- Modifying `answer`.
- Modifying `solution` / `steps`.
- Modifying `solution_svg`.
- Reconstructing a choice sentence from theory instead of the source text.
- Filling only part of a choice by guessing the rest.
- Forcing a recovery through when the OCR / source read is uncertain.

## 4. Recovery procedure (proposed)

| step | description |
| --- | --- |
| R0 | Write a read-only source-choice transcription pack: per item, the source PDF path / page, the current DB `choices`, and blank reviewer fields for the source choice text. No `app/data` change. |
| R1 | A human transcribes choices [1]-[4] directly from the source PDF into the pack. Transcription, not OCR inference. |
| R2 | Transcription review — confirm all 4 choices are legible and transcribed; record any choice that cannot be read. |
| R3 | Choices-only apply, after separate approval — replace the `choices` field of the target item in both JSON files. |
| R4 | Post-apply verification (Section 5). |

If any choice cannot be read confidently from the source at R1/R2, that item
is set to `defer` rather than applied.

## 5. Verification gate

### Before apply

- The source PDF page and the source choice text (evidence) exist.
- All four choices [1]-[4] are legible / transcribed from the source.
- The difference between the current DB `choices` and the source `choices`
  is recorded explicitly per choice.
- The `answer` / `source_answer` index is consistent with the recovered
  choice numbering (e.g. `2001_3회_43` answer 2 must point to the recovered
  choice [2]; `2015_3회_25` answer 4 must point to the recovered choice [4]).

### After apply

- `app/data/questions.json` and `app/data/questions.v2.json` both parse as
  valid JSON.
- Only the 2 target items differ in `git diff` (or fewer, if applied
  per-item).
- Only the `choices` field changed for each target.
- `answer`, `solution`, `steps`, metadata, and `solution_svg` unchanged.
- The `choices` change is reflected identically in both JSON files.
- Browser / render spot check — optional.

## 6. Recommendation

- This step is design only. No `app/data` modification.
- The next step is to write the R0 source-choice transcription pack.
- Use manual transcription from the source PDF as the primary method, not
  automated OCR — the source review packs already established that the
  scanned old PDFs have low OCR quality (`DR-T35-V2A-AK-MAPPING-BLOCKED-001`).
- If a choice cannot be read confidently from the source, defer that item
  rather than apply a partial or guessed recovery.
- Note: `answer` for both items is already correct and source-locked; this
  track only repairs the `choices` text the learner reads. It is a
  data-quality fix, not a scoring fix — so it is lower urgency than the
  answer correction track was, and `defer` is an acceptable resting state if
  the source read is uncertain.

## 7. Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `choices` modification.
- No `answer` modification.
- No `solution` / `steps` modification.
- No `solution_svg` modification.
- No app code or schema modification.
- No paid API call.
- No push.

## 8. Status

- 2 items (`2001_3회_43`, `2015_3회_25`) are `choice_ocr_recovery_candidate`,
  not applied.
- Q2 bulk apply remains BLOCKED.
- Next: R0 source-choice transcription pack.
