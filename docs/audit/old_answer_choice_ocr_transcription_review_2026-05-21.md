# Old Answer — Choice-OCR Transcription Review (R2) (2026-05-21)

R2 review of the source-choice transcriptions filled at R1. This document
reviews and confirms the transcribed choices for the 2 OCR-damaged items and
判定s whether they are ready for the R3 choices-only apply.

This is an **R2 review document only**. It does NOT modify `app/data`, does
NOT modify `choices`, and is not an approval to apply.

- Base commits: `c13510b` (choice-OCR recovery design), `2532058` (R0
  transcription pack), `09c2240` (R1 transcription filled)
- Design parent: `docs/audit/old_answer_choice_ocr_recovery_design_2026-05-21.md`
- Transcription pack (R0/R1): `docs/audit/old_answer_choice_ocr_transcription_pack_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Review verdict definition

- `ready_for_choices_only_apply` — all four source choices were transcribed
  with high confidence, the answer index is consistent with the transcribed
  choice numbering, and the item is ready for the R3 choices-only apply.

## Item 1 — `2001_3회_43`

- key: `2001_3회_43`
- current_answer: 2 / source_answer: 2
- transcription verdict (R1): `transcription_ready`
- source PDF / page: `data/문제_2001_3회_20260316.pdf`, 문제 43, PDF p.4
  (book page 2-316)

source choices [1]-[4] (transcribed from the source PDF):

- [1] 정류자 위에는 한 개의 자극마다 전기각 2π/3 간격으로 3조의 브러시가 있다.
- [2] 3차 권선을 설치하여 1차 권선과 조정권선을 회전자에, 2차 권선을 고정자에 설치하였다.
- [3] 3개의 슬립링은 회전자 권선을 3등분한 점에 각각 접속되어 있다.
- [4] 용량이 큰 것은 정류작용을 좋게 하기 위해 보상 권선과 보극권선을 고정자에 설치한다.

DB current choices damage summary:

- [1] `전기자 2π/3` — should be `전기각 2π/3` (전기자 → 전기각).
- [2] `3자/1자/2자 권선` — systematic 차→자 OCR error (→ 3차/1차/2차).
- [3] `3개의 승압콘은 회전자 권선을 3도분만 젬에 …` — heavily garbled
  (승압콘 → 슬립링, 3도분만 젬에 → 3등분한 점에).
- [4] `정류자용을 줄게` — should be `정류작용을 좋게`.

answer / source-choice numbering consistency check:

- `q.answer` = 2, `source_answer` = 2. The 풀이 marks 【답】② and confirms
  choices [1]/[3]/[4] describe the correct structure of a commutator
  frequency converter, so choice [2] is the wrong statement. The transcribed
  choice [2] occupies position 2. The answer index 2 points to the
  transcribed choice [2] — CONSISTENT.

review verdict: `ready_for_choices_only_apply`.

## Item 2 — `2015_3회_25`

- key: `2015_3회_25`
- current_answer: 4 / source_answer: 4
- transcription verdict (R1): `transcription_ready`
- source PDF / page: `data/문제 _2015_3회_20260316.pdf` (note the space
  after `문제`), 문제 25, PDF p.9 (book page 473)

source choices [1]-[4] (transcribed from the source PDF):

- [1] 동작 전류가 커질수록 동작 시간이 짧게 되는 특성
- [2] 최소 동작전류 이상의 전류가 흐르면 즉시 동작하는 특성
- [3] 동작전류의 크기에 관계없이 일정한 시간에 동작하는 특성
- [4] 동작전류가 적은 동안에는 동작전류가 커질수록 동작시간이 짧아지고 어떤 전류 이상이 되면 동작전류의 크기에 관계없이 일정한 시간에서 동작하는 특성

DB current choices damage summary:

- [1]-[3] hold the 풀이(solution) answer-key labels ("①: 반한시 특성",
  "②: 순한시 특성", "③: 정한시 특성") with a stray leading "：" — these are
  not the actual choice texts.
- [4] holds page-footer residue ("15년도 3회 / 473 / 전기기사 펄기 D-60
  시리즈") — the actual choice [4] text is entirely missing.
- The DB `choices` for this item are wholly wrong (the answer-key labels were
  captured instead of the choice sentences).

answer / source-choice numbering consistency check:

- `q.answer` = 4, `source_answer` = 4. The 풀이 maps ①반한시 / ②순한시 /
  ③정한시 / ④반한시-정한시 and marks 【답】④. The question asks for the
  반한시·정한시(combined) characteristic; the transcribed choice [4]
  describes exactly that combined characteristic ("…커질수록 짧아지고…어떤
  전류 이상이 되면…일정한 시간에서 동작"). The answer index 4 points to the
  transcribed choice [4] — CONSISTENT.

review verdict: `ready_for_choices_only_apply`.

## Overall

| key | transcription verdict | review verdict |
| --- | --- | --- |
| `2001_3회_43` | `transcription_ready` | `ready_for_choices_only_apply` |
| `2015_3회_25` | `transcription_ready` | `ready_for_choices_only_apply` |

2 / 2 `ready_for_choices_only_apply`. No item routed to `needs_better_scan`
or `defer`.

## Proposed apply scope (R3 — not executed here)

- In `app/data/questions.json` and `app/data/questions.v2.json`, replace ONLY
  the `choices` field of the 2 target items with the transcribed source
  choices [1]-[4].
- `answer`, `solution`, `steps`, metadata, and `solution_svg` remain
  unchanged.
- `answer` indices (2 and 4) are confirmed consistent with the transcribed
  choice numbering, so no `answer` change is needed.
- R3 requires separate approval; R4 post-apply verification follows.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `choices` apply.
- No `answer` modification.
- No `solution` / `steps` modification.
- No `solution_svg` modification.
- No paid API call.
- No push.

## Status

- R2 complete. Both items: `ready_for_choices_only_apply`.
- No `app/data` modification.
- Q2 bulk apply remains BLOCKED.
- Next: R3 choices-only apply (separate approval), then R4 verification.
