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
| 11 | `2006_2회_27` | 3 | 전력공학 | `data/문제_2006_2회_20260316.pdf` | 27 | `needs_source_answer_check` | q.answer conflict: 제수문 is for intake-flow control/cutoff (choice 4); sand removal is a 침사지 function. Worked result points to choice 4, while q.answer=3. | 4 | 4 | 문제 27 풀이 (제수문은 취수량 조절·물 유입 단절용) ends with 【답】④; differs from q.answer=3. | `source_answer_conflict` |
| 12 | `2007_1회_9` | 4 | 전기자기학 | `data/문제_2007_1회_20260316.pdf` | 9 | `needs_source_answer_check` | q.answer conflict: perpendicularity A·B = 1+3a = 0 gives a = -1/3 (choice 2), while q.answer=4. | 2 | 2 | 문제 9 풀이 (A·B = 1+3a = 0 → a = -1/3) ends with 【답】②; differs from q.answer=4. | `source_answer_conflict` |
| 13 | `2007_2회_64` | 2 | 회로이론 | `data/문제_2007_2회_20260316.pdf` | 64 | `needs_source_answer_check` | q.answer conflict: Routh first column all positive means stable (choice 1), while q.answer=2 (unstable). | 1 | 6 | 문제 64 풀이 (Hurwitz/Routh first column all positive → stable) ends with 【답】①; differs from q.answer=2. | `source_answer_conflict` |
| 14 | `2014_2회_50` | 3 | 전기기기 | `data/문제_2014_2회_20260316.pdf` | 50 | `needs_source_answer_check` | q.answer conflict: V-curve relates field current to armature current at constant output; q.answer=3 (constant field current) contradicts the V-curve definition. | 1, 2 | 17 | 문제 50 풀이 (V곡선 정의: 단자전압·부하 일정, 여자전류 변화) ends with a double marker 【답】①,②; q.answer=3 is in neither. | `source_answer_conflict` |
| 15 | `2014_3회_62` | 4 | 회로이론 | `data/문제_2014_3회_20260316.pdf` | 62 | `needs_source_answer_check` | q.answer conflict: unit-step Laplace transform is 1/s (choice 1); q.answer=4 is suspect and the choice z-transform text may be OCR-damaged. | 전항정답 | 19 | 문제 62 풀이 table gives F(s)=1/s, F(z)=z/(z-1); no single choice matches that pair, so the source marks 【답】전항정답 (all-choice / defective question). No single source answer exists. | `defer` |
| 16 | `2015_1회_13` | 1 | 전기자기학 | `data/문제_2015_1회_20260316.pdf` | 13 | `proposed_solution_written` | q.answer matches standard theory; old solution concluded choice 2 (cos-squared form) while the worked Poynting-vector result is choice 1 (sin-squared form). | 1 | 5 | 문제 13 풀이 (Poynting vector P = 6.63×10⁻⁶ sin²ω(x-vt)) ends with 【답】①; equals q.answer=1. | `source_answer_verified` |
| 17 | `2015_1회_22` | 1 | 전력공학 | `data/문제_2015_1회_20260316.pdf` | 22 | `proposed_solution_written` | q.answer matches standard theory; old solution concluded choice 4 while the worked result (series-reactance increase is not a stability-improvement method) is choice 1. | 1 | 8 | 문제 22 풀이 (stability-improvement measures) ends with 【답】①; equals q.answer=1. | `source_answer_verified` |
| 18 | `2015_1회_71` | 4 | 전기자기학 | `data/문제_2015_1회_20260316.pdf` | 71 | `needs_source_answer_check` | q.answer conflict: L=Nφ/I=12H and τ=L/R=1s point to choice 1, while q.answer=4 (0.001). | 1 | 24 | 문제 71 풀이 (L = Nφ/I = 12[H], τ = L/R = 12/12 = 1[sec]) ends with 【답】①; differs from q.answer=4. | `source_answer_conflict` |
| 19 | `2015_1회_87` | 3 | 전기설비기술기준 | `data/문제_2015_1회_20260316.pdf` | 87 | `needs_source_answer_check` | q.answer conflict: indoor-circuit ground voltage for incandescent/discharge lamps is 300V or less (choice 2), while q.answer=3 (350). | 2 | 29 | 문제 87 풀이 (231.6 옥내전로 대지전압 제한: 백열전등·방전등 옥내전로 대지전압 300[V] 이하) ends with 【답】②; differs from q.answer=3. | `source_answer_conflict` |
| 20 | `2015_2회_23` | 3 | 전력공학 | `data/문제 _2015_2회_20260316.pdf` | 23 | `needs_source_answer_check` | q.answer conflict: π-circuit sending-end current I_s = Y(1+ZY/4)E_r + (1+ZY/2)I_r (choice 4), while q.answer=3 (missing correction term). | 4 | 9 | 문제 23 풀이 (π형 회로: I_s = Y(1+ZY/4)E_r + (1+ZY/2)I_r) ends with 【답】④; differs from q.answer=3. | `source_answer_conflict` |

## Routing after manual review

- `source_answer_verified` -> answer-locked regeneration candidate.
- `source_answer_conflict` -> answer correction track.
- `source_choice_ocr_corrupt` -> choice recovery track.
- `needs_better_scan` / `defer` -> hold.

## Status

- The reviewer fields (`source_answer`, `source_page`, `evidence_note`,
  `verdict`) for all 10 items are now filled from manual multimodal reading of
  the source PDF 【답】 markers. Verdict tally: 2 `source_answer_verified`,
  7 `source_answer_conflict`, 1 `defer`.
- Item 15 (`2014_3회_62`) carries `defer`: the source 풀이 table gives
  F(s)=1/s and F(z)=z/(z-1), which no single choice matches, so the official
  marker is 【답】전항정답 (defective question, all choices accepted). There is
  no single source answer to lock against.
- Item 14 (`2014_2회_50`) source carries a double marker 【답】①,②; q.answer=3
  matches neither, so it is recorded as `source_answer_conflict`.
- No answer, choice, solution, or `solution_svg` was changed here. This pack
  records source answers and verdicts only; routing is the next step.
- Q2 full apply remains BLOCKED. The earlier Q2-B apply (`fec4bbc`) was a limited
  exception for the 4 `source_answer_verified` items only and does not extend to
  this batch.
- The 6 `source_answer_conflict` items from pack 1 remain sealed until the
  answer correction track; they are not touched here.
