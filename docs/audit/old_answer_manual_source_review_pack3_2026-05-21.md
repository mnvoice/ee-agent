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
| 21 | `2015_2회_29` | 1 | 전력공학 | `data/문제 _2015_2회_20260316.pdf` | 29 | `needs_source_answer_check` | q.answer conflict: a surge arrester (피뢰기) reduces the peak of an overvoltage to protect equipment — choice 2 (choice 2 names 피뢰기). q.answer=1 (series reactor) conflicts. | 2 | 10 | 문제 29 풀이 (① 직렬 리액터=제5고조파 제거 / ② 피뢰기=이상전압 파고치 저감·기기 보호 / ③ 아킹 호온 / ④ 아모 로드) ends with 【답】②; differs from q.answer=1. | `source_answer_conflict` |
| 22 | `2015_3회_22` | 4 | 전력공학 | `data/문제 _2015_3회_20260316.pdf` | 22 | `needs_source_answer_check` | q.answer conflict: transformer 3rd-harmonic elimination is done by a △ (delta) connection — choice 1. q.answer=4 (power capacitor) conflicts. | 1 | 9 | 문제 22 풀이 (제3고조파 제거 = 변압기 △결선; 제5고조파 제거 = 직렬 리액터) ends with 【답】①; differs from q.answer=4. | `source_answer_conflict` |
| 23 | `2015_3회_25` | 1 | 전력공학 | `data/문제 _2015_3회_20260316.pdf` | 25 | `needs_source_answer_check` | choice OCR likely corrupt: the protective-relay 반한시-정한시 characteristic question; old solution concludes choice 4 (반한시-정한시) while q.answer=1 (반한시 단독). Choice text may be OCR-damaged. | 4 | 9 | 문제 25 풀이 (① 반한시 / ② 순한시 / ③ 정한시 / ④ 반한시-정한시 특성) ends with 【답】④; differs from q.answer=1. The source PDF choices are readable; any DB-stored choice OCR damage is a separate DB-side issue. | `source_answer_conflict` |
| 24 | `2015_3회_27` | 3 | 전력공학 | `data/문제 _2015_3회_20260316.pdf` | 27 | `proposed_solution_written` | q.answer matches standard theory; old solution concluded choice 4 while the worked result (raising generator/transformer reactance is not a stability-improvement method) is choice 3. | 3 | 10 | 문제 27 풀이 (안정도 향상 대책 4종; raising generator/transformer reactance is not among them) ends with 【답】③; equals q.answer=3. | `source_answer_verified` |
| 25 | `2016_1회_44` | 2 | 전기기기 | `data/문제_2016_1회_20260316.pdf` | 44 | `needs_source_answer_check` | q.answer conflict / choice ambiguity: choices use OCR-blurred wording around 전기적/기하학적 중성축; old solution concludes choice 4 while q.answer=2. Reliable mapping is difficult. | 4 | 15 | 문제 44 풀이 (전기자 반작용의 영향 4종, 마지막 항목이 발전기 출력 감소) ends with 【답】④; differs from q.answer=2. The source PDF choices are readable. | `source_answer_conflict` |
| 26 | `2016_1회_69` | 1 | 전력공학 | `data/문제_2016_1회_20260316.pdf` | 69 | `needs_source_answer_check` | q.answer conflict: phase margin and gain margin are direct stability measures; the item least related to stability is natural frequency — choice 4. q.answer=1 (resonance peak) conflicts. | 4 | 23 | 문제 69 풀이 (안정도 척도 = 공진치·위상여유·이득여유; 고유주파수는 안정도와 무관) ends with 【답】④; differs from q.answer=1. | `source_answer_conflict` |
| 27 | `2016_1회_70` | 2 | 제어공학 | `data/문제_2016_1회_20260316.pdf` | 70 | `needs_source_answer_check` | q.answer conflict: the Nyquist critical point -1+j0 maps to 0[dB], ±180° — choice 4. q.answer=2 (0[dB], -90°) conflicts. | 4 | 23 | 문제 70 풀이 (Nyquist 임계점 -1+j0 → 이득 20log1=0[dB], 위상 ±180°) ends with 【답】④; differs from q.answer=2. | `source_answer_conflict` |
| 28 | `2016_1회_71` | 3 | 제어공학 | `data/문제_2016_1회_20260316.pdf` | 71 | `proposed_solution_written` | q.answer matches standard theory; old solution worked E_l = E_p (Δ connection) correctly but mislabeled the conclusion as choice 1, while E_l = E_p is choice 3. | 3 | 23 | 문제 71 풀이 (△결선: 선간전압 E_l = E_p; Y결선: E_l = √3 E_p) ends with 【답】③; equals q.answer=3. | `source_answer_verified` |
| 29 | `2016_3회_21` | 1 | 전력공학 | `data/문제_2016_3회_20260316.pdf` | 21 | `needs_source_answer_check` | q.answer conflict: at constant loss rate the conductor cross-section A ∝ 1/V² (inverse square of voltage) — choice 4. q.answer=1 (proportional to current) conflicts. | 4 | 7 | 문제 21 풀이 (전선 단면적 A는 전압 자승에 반비례, ∝ 1/V²) ends with 【답】④; differs from q.answer=1. | `source_answer_conflict` |
| 30 | `2016_3회_44` | 4 | 전기기기 | `data/문제_2016_3회_20260316.pdf` | 44 | `proposed_solution_written` | q.answer matches standard theory; old solution worked 무부하시험 (open-circuit test) correctly but mislabeled the conclusion as choice 1, while 무부하시험 is choice 4. | 4 | 15 | 문제 44 풀이 (개방회로/무부하 시험으로 철손 측정; 단락시험은 동손) ends with 【답】④; equals q.answer=4. | `source_answer_verified` |

## Routing after manual review

- `source_answer_verified` -> answer-locked regeneration candidate.
- `source_answer_conflict` -> answer correction track.
- `source_choice_ocr_corrupt` -> choice recovery track.
- `needs_better_scan` / `defer` -> hold.

## Status

- The reviewer fields (`source_answer`, `source_page`, `evidence_note`,
  `verdict`) for all 10 items are now filled from manual multimodal reading of
  the source PDF 【답】 markers. Verdict tally: 3 `source_answer_verified`,
  7 `source_answer_conflict`, 0 `source_choice_ocr_corrupt`, 0 `needs_better_scan`,
  0 `defer`.
- The 3 `proposed_solution_written` items (24 `2015_3회_27`, 28 `2016_1회_71`,
  30 `2016_3회_44`) are all verified — the source 【답】 marker equals `q.answer`.
- The 7 `needs_source_answer_check` items are all `source_answer_conflict`.
- Items 23 (`2015_3회_25`) and 25 (`2016_1회_44`) were flagged as possible
  choice-OCR concerns in the prep sheet, but the source PDF choices are
  readable; both resolve to `source_answer_conflict`, not
  `source_choice_ocr_corrupt`.
- No answer, choice, solution, or `solution_svg` was changed here. This pack
  records source answers and verdicts only; routing is the next step.
- Q2 full apply remains BLOCKED. The Q2-B apply (`fec4bbc`) and Q2-C apply
  (`fbeffef`) were limited exceptions for the 6 `source_answer_verified` items
  only and do not extend to this batch.
- The 13 `source_answer_conflict` items from packs 1-2 remain sealed until the
  answer correction track; they are not touched here.
- The 1 `defer` item (`2014_3회_62`) remains sealed until a defective-question
  policy is defined; it is not touched here.
