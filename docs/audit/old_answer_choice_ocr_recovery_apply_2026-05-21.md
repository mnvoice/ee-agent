# Old Answer — Choice-OCR Recovery Apply Result (R3) (2026-05-21)

Apply-result log for the choice-OCR recovery (R3). The `choices` field of the
2 OCR-damaged items was replaced with the source choices transcribed at R1
and confirmed at R2, in both `app/data/questions.json` and
`app/data/questions.v2.json`. Only the `choices` field was changed.

This is an apply-result record. The apply was authorized for the 2
`ready_for_choices_only_apply` items only.

- Base commits: `c13510b` (choice-OCR recovery design), `09c2240` (R1
  transcription filled), `288048e` (R2 transcription review)
- Transcription pack (R0/R1): `docs/audit/old_answer_choice_ocr_transcription_pack_2026-05-21.md`
- Transcription review (R2): `docs/audit/old_answer_choice_ocr_transcription_review_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Applied items (2)

| key | answer | source PDF / page |
| --- | ---: | --- |
| `2001_3회_43` | 2 | `data/문제_2001_3회_20260316.pdf`, 문제 43, PDF p.4 |
| `2015_3회_25` | 4 | `data/문제 _2015_3회_20260316.pdf`, 문제 25, PDF p.9 |

### `2001_3회_43`

old `choices` damage summary:

- [1] `전기자 2π/3` → should be `전기각 2π/3`.
- [2] `3자/1자/2자 권선` → systematic 차→자 OCR error.
- [3] `3개의 승압콘은 회전자 권선을 3도분만 젬에 …` → heavily garbled.
- [4] `정류자용을 줄게` → should be `정류작용을 좋게`.

new `choices` (transcribed from the source PDF):

- [1] 정류자 위에는 한 개의 자극마다 전기각 2π/3 간격으로 3조의 브러시가 있다.
- [2] 3차 권선을 설치하여 1차 권선과 조정권선을 회전자에, 2차 권선을 고정자에 설치하였다.
- [3] 3개의 슬립링은 회전자 권선을 3등분한 점에 각각 접속되어 있다.
- [4] 용량이 큰 것은 정류작용을 좋게 하기 위해 보상 권선과 보극권선을 고정자에 설치한다.

### `2015_3회_25`

old `choices` damage summary:

- [1]-[3] held the 풀이(solution) answer-key labels ("①: 반한시 특성",
  "②: 순한시 특성", "③: 정한시 특성") with a stray leading "：" — not the
  actual choice texts.
- [4] held page-footer residue ("15년도 3회 / 473 / 전기기사 펄기 D-60
  시리즈") — the actual choice [4] text was entirely missing.

new `choices` (transcribed from the source PDF):

- [1] 동작 전류가 커질수록 동작 시간이 짧게 되는 특성
- [2] 최소 동작전류 이상의 전류가 흐르면 즉시 동작하는 특성
- [3] 동작전류의 크기에 관계없이 일정한 시간에 동작하는 특성
- [4] 동작전류가 적은 동안에는 동작전류가 커질수록 동작시간이 짧아지고 어떤 전류 이상이 되면 동작전류의 크기에 관계없이 일정한 시간에서 동작하는 특성

## Changed files

- `app/data/questions.json` — `choices` of 2 items replaced.
- `app/data/questions.v2.json` — `choices` of 2 items replaced.

## Changed field

- `choices` only. For each changed item the field-level diff is exactly
  `['choices']`.

## Unchanged

- `answer` — `2001_3회_43` = 2, `2015_3회_25` = 4 (not modified; the answer
  indices were confirmed consistent with the transcribed choice numbering at
  R2).
- `solution`, `steps`.
- question `text`.
- metadata (`subject`, `q_no`, `q_type`, `difficulty`, `quality`, `tag`,
  `year`, `session`, `*_source`).
- `solution_svg` (neither item has one).

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- Both targets exist exactly once in both files.
- Both targets: `choices` == the transcribed source choices (4 each).
- Both targets: `answer` retained — `2001_3회_43` = 2, `2015_3회_25` = 4.
- Exactly 2 items changed in each file; each change is confined to `choices`.
- Edited items: all non-`choices` fields (`answer`, `solution`, `steps`,
  `text`, metadata, `solution_svg`) unchanged.
- No other record changed.
- `git diff --check` — no whitespace errors.
- Serialization preserved — diff confined to the `choices` strings; no mass
  reformatting.

## Final status

`choice_ocr_recovered`

Both items' `choices` text is recovered from the source PDF. The `answer`,
`solution`, and `steps` were already closed; the `choices` text the learner
reads now matches the source.

## Downstream

- `2001_3회_43`: the C20-1 solution dry-run had deferred the detailed
  wrong-statement analysis of choice [2] because the stored choice text was
  OCR-damaged. With `choices` now recovered, that detail could optionally be
  revisited, but it is not required — the `solution` already locks the
  conclusion to ②. Recorded as an optional follow-up, not opened here.
- `2015_3회_25`: `solution` / `steps` already named the choice ④ meaning
  ("반한시-정한시 특성") correctly; no `solution` follow-up needed.

## Status

- Choice-OCR recovery track complete for both items (`choice_ocr_recovered`).
- Q2 bulk apply remains BLOCKED.
- DQ-1 items (`2014_2회_50`, `2014_3회_62`) remain `defer` pending the DQ
  migration (separate large track).

## Not done in this step

- No `answer` modification.
- No `solution` / `steps` modification.
- No question text / metadata modification.
- No `solution_svg` modification.
- No modification of any other record.
- No paid API call.
- No push.
