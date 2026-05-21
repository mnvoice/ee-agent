# Old Answer Manual Source Review Pack 3 (2026-05-21)

Third manual source review pack. Covers pilot items 21-30 of the 30-item C1
pilot — the last items not yet manually source-reviewed. This is a review-prep
sheet: no answer, choice, or solution is changed here, and the reviewer source
fields are left blank. They are filled in the next round.

- Pilot source (30-item list): `docs/audit/old_solution_quality_pilot_2026-05-21.md`
- Q2-A dry-run: `docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md`
- First pack (items 1-10): `docs/audit/old_answer_manual_source_review_pack_2026-05-21.md`
- Second pack (items 11-20): `docs/audit/old_answer_manual_source_review_pack2_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Reference commits

- `4317aea` — docs: fill source answers for first 10 review-pack items
- `33c8fcf` — docs: record first source review routing
- `fec4bbc` — docs/apply: apply q2b verified source-answer solutions
- `041b83f` — docs: fill source answers for second review-pack items
- `cff0e6d` — docs: record second source review routing
- `fbeffef` — docs/apply: apply q2c verified source-answer solutions

## Current cumulative state

- verified apply: 6 items (Q2-B 4 items in `fec4bbc` + Q2-C 2 items in `fbeffef`)
- conflict: 13 items (pack 1: 6 items + pack 2: 7 items) — sealed until the
  answer correction track
- defer: 1 item (pack 2: `2014_3회_62`) — sealed until a defective-question
  ("전항정답") policy is defined

## Context

The automatic `mapping.json` answer-key crop+OCR path is blocked for this batch
(see `DR-T35-V2A-AK-MAPPING-BLOCKED-001`). The pilot items therefore move to
manual source review. The first pack handled items 1-10, the second pack items
11-20; this pack handles the last 10 (items 21-30).

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

Path note: items 21-24's source PDF filenames contain a space after `문제`
(`문제 _2015_2회_...`, `문제 _2015_3회_...`), unlike the 2016 files
(`문제_2016_...`). Each path is recorded verbatim as it exists on disk.

## Third 10 manual review table (pilot items 21-30)

| # | key | current_q_answer | subject | source PDF path | q_no | dry-run status | suspected issue | source_answer | source_page | evidence_note | verdict |
| ---: | --- | ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| 21 | `2015_2회_29` | 1 | 전력공학 | `data/문제 _2015_2회_20260316.pdf` | 29 | `needs_source_answer_check` | q.answer conflict: a surge arrester (피뢰기) reduces the peak of an overvoltage to protect equipment — choice 2 (choice 2 names 피뢰기). q.answer=1 (series reactor) conflicts. |  |  |  |  |
| 22 | `2015_3회_22` | 4 | 전력공학 | `data/문제 _2015_3회_20260316.pdf` | 22 | `needs_source_answer_check` | q.answer conflict: transformer 3rd-harmonic elimination is done by a △ (delta) connection — choice 1. q.answer=4 (power capacitor) conflicts. |  |  |  |  |
| 23 | `2015_3회_25` | 1 | 전력공학 | `data/문제 _2015_3회_20260316.pdf` | 25 | `needs_source_answer_check` | choice OCR likely corrupt: the protective-relay 반한시-정한시 characteristic question; old solution concludes choice 4 (반한시-정한시) while q.answer=1 (반한시 단독). Choice text may be OCR-damaged. |  |  |  |  |
| 24 | `2015_3회_27` | 3 | 전력공학 | `data/문제 _2015_3회_20260316.pdf` | 27 | `proposed_solution_written` | q.answer matches standard theory; old solution concluded choice 4 while the worked result (raising generator/transformer reactance is not a stability-improvement method) is choice 3. |  |  |  |  |
| 25 | `2016_1회_44` | 2 | 전기기기 | `data/문제_2016_1회_20260316.pdf` | 44 | `needs_source_answer_check` | q.answer conflict / choice ambiguity: choices use OCR-blurred wording around 전기적/기하학적 중성축; old solution concludes choice 4 while q.answer=2. Reliable mapping is difficult. |  |  |  |  |
| 26 | `2016_1회_69` | 1 | 전력공학 | `data/문제_2016_1회_20260316.pdf` | 69 | `needs_source_answer_check` | q.answer conflict: phase margin and gain margin are direct stability measures; the item least related to stability is natural frequency — choice 4. q.answer=1 (resonance peak) conflicts. |  |  |  |  |
| 27 | `2016_1회_70` | 2 | 제어공학 | `data/문제_2016_1회_20260316.pdf` | 70 | `needs_source_answer_check` | q.answer conflict: the Nyquist critical point -1+j0 maps to 0[dB], ±180° — choice 4. q.answer=2 (0[dB], -90°) conflicts. |  |  |  |  |
| 28 | `2016_1회_71` | 3 | 제어공학 | `data/문제_2016_1회_20260316.pdf` | 71 | `proposed_solution_written` | q.answer matches standard theory; old solution worked E_l = E_p (Δ connection) correctly but mislabeled the conclusion as choice 1, while E_l = E_p is choice 3. |  |  |  |  |
| 29 | `2016_3회_21` | 1 | 전력공학 | `data/문제_2016_3회_20260316.pdf` | 21 | `needs_source_answer_check` | q.answer conflict: at constant loss rate the conductor cross-section A ∝ 1/V² (inverse square of voltage) — choice 4. q.answer=1 (proportional to current) conflicts. |  |  |  |  |
| 30 | `2016_3회_44` | 4 | 전기기기 | `data/문제_2016_3회_20260316.pdf` | 44 | `proposed_solution_written` | q.answer matches standard theory; old solution worked 무부하시험 (open-circuit test) correctly but mislabeled the conclusion as choice 1, while 무부하시험 is choice 4. |  |  |  |  |

## Routing after manual review

- `source_answer_verified` -> answer-locked regeneration candidate.
- `source_answer_conflict` -> answer correction track.
- `source_choice_ocr_corrupt` -> choice recovery track.
- `needs_better_scan` / `defer` -> hold.

## Status

- This document is a review-prep sheet. `source_answer` and the other reviewer
  fields are intentionally left blank; they are filled in the next round.
- Q2 full apply remains BLOCKED. The Q2-B apply (`fec4bbc`) and Q2-C apply
  (`fbeffef`) were limited exceptions for the 6 `source_answer_verified` items
  only and do not extend to this batch.
- The 13 `source_answer_conflict` items from packs 1-2 remain sealed until the
  answer correction track; they are not touched here.
- The 1 `defer` item (`2014_3회_62`) remains sealed until a defective-question
  policy is defined; it is not touched here.
