# Old Answer Manual Source Review Pack (2026-05-21)

Review sheet for a human to verify source answers for the first 10 items from
the 30-item C1 pilot. This is not an answer-correction or solution-apply step:
no answer, choice, or solution is changed here. The reviewer only fills the
blank source fields and assigns a verdict.

- Pilot source: `docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md`
- Source verification track: `docs/audit/old_question_answer_source_verification_track.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## V2-A automatic crop+OCR blocker

The automatic `mapping.json` answer-key crop+OCR path is blocked for this batch.

- `data/batch_answer_key/mapping.json` `ak` pages do not contain a per-question
  answer index for the pilot questions.
- Pilot `q_no` header discovery on mapped `ak` pages was 0/30.
- Old PDFs, especially the 1998-2007 scans, have low OCR quality.
- Circled answer markers are not reliable under local OCR.

Therefore the 30 pilot items move to manual source review. To control scope,
this first pack contains only 10 items.

## Verdict definitions

- `source_answer_verified` — source answer found in the PDF and it equals `q.answer`.
- `source_answer_conflict` — source answer found and it differs from `q.answer`.
- `source_choice_ocr_corrupt` — source choices are too OCR-damaged to map an answer.
- `needs_better_scan` — source page is unreadable; a better scan is required.
- `defer` — source is ambiguous, missing, or structurally unclear; hold.

## Review instructions

For each item, open the source PDF, locate `q_no`, inspect the source answer
marker or answer table if present, and fill the reviewer fields. Do not modify
`app/data/questions.json`, `app/data/questions.v2.json`, answers, choices, or
solutions from this pack.

## First 10 manual review table

| # | key | current_q_answer | subject | source PDF path | q_no | dry-run status | suspected issue | source_answer | source_page | evidence_note | verdict |
| ---: | --- | ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| 1 | `1998_4회_10` | 1 | 전기자기학 | `data/문제_1998_4회_20260316.pdf` | 10 | `needs_source_answer_check` | q.answer conflict: boundary-condition calculation points to choice 4, while q.answer=1. | 4 | 2 | 문제 10 풀이 box ends with 【답】④; differs from q.answer=1. | `source_answer_conflict` |
| 2 | `2001_1회_21` | 2 | 전력공학 | `data/문제_2001_1회_20260316.pdf` | 21 | `proposed_solution_written` | q.answer matches standard theory; old solution appears to have wrong choice-number conclusion. | 2 | 2 | 문제 21 풀이 box ends with 【답】②; equals q.answer=2. | `source_answer_verified` |
| 3 | `2001_1회_68` | 1 | 제어공학 | `data/문제_2001_1회_20260316.pdf` | 68 | `needs_source_answer_check` | q.answer conflict: parabolic-input error constant points to choice 3, while q.answer=1. | 3 | 6 | 문제 68 풀이 (가속도편차상수 Kₐ) ends with 【답】③; differs from q.answer=1. | `source_answer_conflict` |
| 4 | `2001_3회_41` | 2 | 전기기기 | `data/문제_2001_3회_20260316.pdf` | 41 | `needs_source_answer_check` | q.answer conflict: "incorrect" item appears to be iron-loss increase choice 4, while q.answer=2. | 4 | 3 | 문제 41 풀이 (철손은 무부하손) ends with 【답】④; differs from q.answer=2. | `source_answer_conflict` |
| 5 | `2001_3회_43` | 1 | 전기기기 | `data/문제_2001_3회_20260316.pdf` | 43 | `needs_source_answer_check` | source choice OCR likely corrupt; stored choices include damaged text. | 2 | 4 | 문제 43 풀이 box ends with 【답】②; differs from q.answer=1. PDF source choices are readable; DB-stored choice OCR damage is a separate DB-side issue. | `source_answer_conflict` |
| 6 | `2002_1회_32` | 1 | 전력공학 | `data/문제_2002_1회_20260316.pdf` | 32 | `needs_source_answer_check` | source choice OCR likely corrupt; choice 1 has table/OCR residue. | 1 | 3-4 | 문제 32 on PDF p.3; 풀이 (고장별 대칭분 table) on PDF p.4 ends with 【답】①; equals q.answer=1. PDF source choices are readable. | `source_answer_verified` |
| 7 | `2002_3회_4` | 2 | 전기자기학 | `data/문제_2002_3회_20260316.pdf` | 4 | `needs_source_answer_check` | q.answer conflict: dimensional check suggests potential-form choice 4, while q.answer=2. | 4 | 2 | 문제 4 풀이 (potential-form surface integral) ends with 【답】④; differs from q.answer=2. | `source_answer_conflict` |
| 8 | `2005_3회_83` | 4 | 전기설비기술기준 | `data/문제_2005_3회_20260316.pdf` | 83 | `proposed_solution_written` | q.answer matches standard theory; old solution conclusion is internally inconsistent. | 4 | 8 | 문제 83 풀이 (232.12 금속관공사 부싱) ends with 【답】④; equals q.answer=4. | `source_answer_verified` |
| 9 | `2006_1회_6` | 4 | 전기자기학 | `data/문제_2006_1회_20260316.pdf` | 6 | `needs_source_answer_check` | q.answer conflict: dielectric heating formula points to choice 3, while q.answer=4. | 3 | 2 | 문제 06 풀이 (Q=0.24·CV²t/(ερ)) ends with 【답】③; differs from q.answer=4. | `source_answer_conflict` |
| 10 | `2006_1회_7` | 2 | 전기자기학 | `data/문제_2006_1회_20260316.pdf` | 7 | `proposed_solution_written` | q.answer matches standard theory; old solution confused computed value 3 with choice number 3. | 2 | 2 | 문제 07 풀이 (div E=3 at origin) ends with 【답】②; equals q.answer=2. | `source_answer_verified` |

## Routing after manual review

- `source_answer_verified` -> answer-locked regeneration candidate.
- `source_answer_conflict` -> answer correction track.
- `source_choice_ocr_corrupt` -> choice recovery track.
- `needs_better_scan` / `defer` -> hold.

Q2 apply remains blocked until source answers are reviewed and routed.
