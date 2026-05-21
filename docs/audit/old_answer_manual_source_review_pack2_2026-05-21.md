# Old Answer Manual Source Review Pack 2 (2026-05-21)

Second manual source review pack. Covers pilot items 11-20 of the 30-item C1
pilot — the items not yet manually source-reviewed. This is a review-prep sheet:
no answer, choice, or solution is changed here, and the reviewer source fields
are left blank. They are filled in the next round.

- Pilot source (30-item list): `docs/audit/old_solution_quality_pilot_2026-05-21.md`
- Q2-A dry-run: `docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md`
- First pack (items 1-10): `docs/audit/old_answer_manual_source_review_pack_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Reference commits

- `4317aea` — docs: fill source answers for first 10 review-pack items
- `33c8fcf` — docs: record first source review routing
- `bce99f6` — docs: draft q2b verified source-answer solutions
- `fec4bbc` — docs/apply: apply q2b verified source-answer solutions

## Context

The automatic `mapping.json` answer-key crop+OCR path is blocked for this batch
(see `DR-T35-V2A-AK-MAPPING-BLOCKED-001`). The pilot items therefore move to
manual source review. The first pack handled items 1-10; this pack handles the
next 10 (items 11-20).

The 문제 PDFs from this period contain inline 【답】 markers in each solution box;
manual multimodal reading of those markers is the verification method.

## Verdict definitions

- `source_answer_verified` — source answer found in the PDF and it equals `q.answer`.
- `source_answer_conflict` — source answer found and it differs from `q.answer`.
- `source_choice_ocr_corrupt` — source choices are too OCR-damaged to map an answer.
- `needs_better_scan` — source page is unreadable; a better scan is required.
- `defer` — source is ambiguous, missing, or structurally unclear; hold.

## Review instructions

For each item, open the source PDF, locate `q_no`, inspect the source answer
marker (【답】) or answer table if present, and fill the reviewer fields. Do not
modify `app/data/questions.json`, `app/data/questions.v2.json`, answers, choices,
solutions, or `solution_svg` from this pack.

Path note: item 20's source PDF filename contains a space after `문제`
(`문제 _2015_2회_...`), unlike every other file (`문제_YYYY_...`). The path is
recorded verbatim as it exists on disk.

## Second 10 manual review table (pilot items 11-20)

| # | key | current_q_answer | subject | source PDF path | q_no | dry-run status | suspected issue | source_answer | source_page | evidence_note | verdict |
| ---: | --- | ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| 11 | `2006_2회_27` | 3 | 전력공학 | `data/문제_2006_2회_20260316.pdf` | 27 | `needs_source_answer_check` | q.answer conflict: 제수문 is for intake-flow control/cutoff (choice 4); sand removal is a 침사지 function. Worked result points to choice 4, while q.answer=3. |  |  |  |  |
| 12 | `2007_1회_9` | 4 | 전기자기학 | `data/문제_2007_1회_20260316.pdf` | 9 | `needs_source_answer_check` | q.answer conflict: perpendicularity A·B = 1+3a = 0 gives a = -1/3 (choice 2), while q.answer=4. |  |  |  |  |
| 13 | `2007_2회_64` | 2 | 회로이론 | `data/문제_2007_2회_20260316.pdf` | 64 | `needs_source_answer_check` | q.answer conflict: Routh first column all positive means stable (choice 1), while q.answer=2 (unstable). |  |  |  |  |
| 14 | `2014_2회_50` | 3 | 전기기기 | `data/문제_2014_2회_20260316.pdf` | 50 | `needs_source_answer_check` | q.answer conflict: V-curve relates field current to armature current at constant output; q.answer=3 (constant field current) contradicts the V-curve definition. |  |  |  |  |
| 15 | `2014_3회_62` | 4 | 회로이론 | `data/문제_2014_3회_20260316.pdf` | 62 | `needs_source_answer_check` | q.answer conflict: unit-step Laplace transform is 1/s (choice 1); q.answer=4 is suspect and the choice z-transform text may be OCR-damaged. |  |  |  |  |
| 16 | `2015_1회_13` | 1 | 전기자기학 | `data/문제_2015_1회_20260316.pdf` | 13 | `proposed_solution_written` | q.answer matches standard theory; old solution concluded choice 2 (cos-squared form) while the worked Poynting-vector result is choice 1 (sin-squared form). |  |  |  |  |
| 17 | `2015_1회_22` | 1 | 전력공학 | `data/문제_2015_1회_20260316.pdf` | 22 | `proposed_solution_written` | q.answer matches standard theory; old solution concluded choice 4 while the worked result (series-reactance increase is not a stability-improvement method) is choice 1. |  |  |  |  |
| 18 | `2015_1회_71` | 4 | 전기자기학 | `data/문제_2015_1회_20260316.pdf` | 71 | `needs_source_answer_check` | q.answer conflict: L=Nφ/I=12H and τ=L/R=1s point to choice 1, while q.answer=4 (0.001). |  |  |  |  |
| 19 | `2015_1회_87` | 3 | 전기설비기술기준 | `data/문제_2015_1회_20260316.pdf` | 87 | `needs_source_answer_check` | q.answer conflict: indoor-circuit ground voltage for incandescent/discharge lamps is 300V or less (choice 2), while q.answer=3 (350). |  |  |  |  |
| 20 | `2015_2회_23` | 3 | 전력공학 | `data/문제 _2015_2회_20260316.pdf` | 23 | `needs_source_answer_check` | q.answer conflict: π-circuit sending-end current I_s = Y(1+ZY/4)E_r + (1+ZY/2)I_r (choice 4), while q.answer=3 (missing correction term). |  |  |  |  |

## Routing after manual review

- `source_answer_verified` -> answer-locked regeneration candidate.
- `source_answer_conflict` -> answer correction track.
- `source_choice_ocr_corrupt` -> choice recovery track.
- `needs_better_scan` / `defer` -> hold.

## Status

- This document is a review-prep sheet. `source_answer` and the other reviewer
  fields are intentionally left blank; they are filled in the next round.
- Q2 full apply remains BLOCKED. The earlier Q2-B apply (`fec4bbc`) was a limited
  exception for the 4 `source_answer_verified` items only and does not extend to
  this batch.
- The 6 `source_answer_conflict` items from pack 1 remain sealed until the
  answer correction track; they are not touched here.
