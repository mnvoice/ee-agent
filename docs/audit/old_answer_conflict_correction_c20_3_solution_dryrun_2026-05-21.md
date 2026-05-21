# Old Answer Conflict Correction — C20-3 Solution/Steps Regeneration Dry-run (2026-05-21)

Solution/steps regeneration dry-run for the 5 C20-3 items that are in state
`answer_corrected_solution_pending`. For each item this document assesses the
existing `solution` / `steps` against the corrected `q.answer` and proposes
an answer-locked draft or records a no-op.

This is a **dry-run document only**. It does NOT modify `app/data` and is not
an approval to apply. `solution_svg` is not modified here and is pending a
separate audit.

- Base commits: `0e6804d` (correction manifest), `8a6a961` (C20-3 answer
  correction apply)
- Prior completed: C20-1 closed at `8f4bdf0`, C20-2 closed at `8ad2689`
- Manifest: `docs/audit/old_answer_conflict_correction_manifest_2026-05-21.md`
- Apply result (answer): `docs/audit/old_answer_conflict_correction_c20_3_apply_2026-05-21.md`
- Source review pack: `old_answer_manual_source_review_pack3_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Key finding

Of the 5 C20-3 items, 4 already have `solution` / `steps` whose conclusion
matches the corrected `q.answer` — no edit is needed. 1 item (`2015_2회_23`)
has a genuine defect in `steps.계산`: the string is truncated mid-sentence,
never states an explicit choice-④ conclusion, and carries a stale "참고
풀이에 오류" reference. The proposed fix is bounded and source-grounded — the
correct formula is already derived in the same item's `solution` body and in
`steps.변환`.

Separately, `2015_3회_25` carries a `choices`-field OCR defect (choice [4]
stored text is page-footer residue). Per the apply instruction, `choices` is
NOT modified; the defect is recorded as a choice-OCR recovery flag only.

Per-item state summary:

| key | corrected answer | existing solution | existing steps | draft type |
| --- | ---: | --- | --- | --- |
| `2015_1회_87` | 2 | already concludes 2번 (300V) | already concludes 2번 (300V) | no-op |
| `2015_2회_23` | 4 | already concludes (4)번 | `계산` truncated mid-sentence, no explicit ④ conclusion, stale ref | edit — steps defect fix |
| `2015_2회_29` | 2 | already concludes 2번 (피뢰기) | already concludes 2번 (피뢰기) | no-op |
| `2015_3회_22` | 1 | already concludes 1번 (△결선) | already concludes 1번 (△결선) | no-op |
| `2015_3회_25` | 4 | already concludes 4번 (반한시-정한시) | already concludes 4번 (반한시-정한시) | no-op + choice-OCR flag |

## Per-item drafts

### 1. `2015_1회_87` — corrected_q_answer = 2

- source_answer: 2 / source_page: p.29 / evidence: 풀이 (231.6 옥내전로
  대지전압 300V 이하) ends 【답】②.
- old solution issue: none. The `solution` states the indoor-circuit ground
  voltage limit for incandescent / discharge lamps is 300 V or less and
  concludes "정답: 2번 (300[V])". The `steps.계산` reviews all choices
  (250/300/350/400) and concludes "정답: 2번 (300[V])". Both match the
  corrected `q.answer` = 2.
- current consistency assessment: consistent — solution and steps both
  conclude choice [2].
- proposed solution draft: no change.
- proposed steps draft: no change.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES.
  - no figure dependency: YES — recall item, no figure.
  - no invented source/article claim: YES — the article reference
    "전기설비기술기준 231.6" already exists in the stored `solution` / `steps`;
    it is not added, modified, or fabricated here.
- risk note: low. No-op; listed for completeness.

### 2. `2015_2회_23` — corrected_q_answer = 4

- source_answer: 4 / source_page: p.9 / evidence: 풀이 (π형 회로 I_s 보정항)
  ends 【답】④.
- old solution issue: the `solution` body derives the π-circuit sending-end
  current `I_s = Y(1+ZY/4)E_r + (1+ZY/2)I_r` (via the ABCD matrix) and
  concludes "정답: (4)번" — consistent with the corrected `q.answer`. The
  `steps.계산` block, however, is defective: it reviews 선택지 1/2/3 only,
  carries the stale phrase "정답의 참고 풀이에 오류가 있으며" (a reference to
  the old-answer state), prints the correct boxed `I_s` formula, and then
  **ends truncated mid-sentence** at "(선택지 중 정확한 답이". It never states
  an explicit choice-④ conclusion.
- current consistency assessment: `solution` body — consistent (concludes
  (4)번). `steps.계산` — DEFECTIVE (truncated, no explicit conclusion).
- proposed solution draft: no change — the solution body already concludes
  (4)번 correctly.
- proposed steps draft: in `steps.계산`, keep the 선택지 1/2/3 review
  unchanged. Replace the tail starting at "정답의 참고 풀이에 오류가
  있으며 …" — through the truncated "(선택지 중 정확한 답이" fragment — with:
  a 선택지 4 review line stating that choice ④
  `(1+ZY/2)I_r + Y(1+ZY/4)E_r` matches the π-circuit sending-end current
  formula; the boxed `I_s = Y(1+ZY/4)E_r + (1+ZY/2)I_r` (already present);
  and an explicit "정답: ④". The boxed formula is the value already derived
  in `steps.변환` and in the solution body — nothing new is introduced.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES after fix — `I_s` formula =
    choice [4] = corrected `q.answer` = 4.
  - no figure dependency: YES — analytic ABCD-matrix derivation;
    `solution_svg` exists but the text does not depend on it.
  - no invented source/article claim: YES — the fix completes a truncated
    review using the formula already derived in the same item; no source or
    article is invented.
- risk note: MEDIUM. The `steps.계산` defect (truncation + missing
  conclusion) is genuine, not a stale reference alone. The fix is grounded
  (solution body + `steps.변환` both give the same formula). Recommend the
  apply quote the exact tail text to be replaced.

### 3. `2015_2회_29` — corrected_q_answer = 2

- source_answer: 2 / source_page: p.10 / evidence: 풀이 (② 피뢰기=이상전압
  파고치 저감) ends 【답】②.
- old solution issue: none. The `solution` evaluates all four devices and
  concludes "정답: 2번 (피뢰기)" — 피뢰기 reduces the peak of an overvoltage
  to protect equipment. The `steps.계산` table likewise concludes "정답: 2번
  (피뢰기)". Both match the corrected `q.answer` = 2.
- current consistency assessment: consistent — solution and steps both
  conclude choice [2].
- proposed solution draft: no change.
- proposed steps draft: no change.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES.
  - no figure dependency: YES — recall item, no figure.
  - no invented source/article claim: YES.
- risk note: low. No-op. Note: the stored `text` carries trailing OCR residue
  ("[답] 15년도 2회 / 439 / …"); that is a `text`-field issue, out of scope
  for this solution dry-run, and `text` is not modified.

### 4. `2015_3회_22` — corrected_q_answer = 1

- source_answer: 1 / source_page: p.9 / evidence: 풀이 (제3고조파 제거=변압기
  △결선) ends 【답】①.
- old solution issue: none. The `solution` explains that 3rd-harmonic
  (zero-sequence) components circulate and cancel within a △ connection and
  concludes "정답: 1번 (변압기 △ 결선)". The `steps.계산` performs the
  symmetrical-component analysis and concludes "정답: 1번 (변압기 △ 결선)".
  Both match the corrected `q.answer` = 1.
- current consistency assessment: consistent — solution and steps both
  conclude choice [1].
- proposed solution draft: no change.
- proposed steps draft: no change.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES.
  - no figure dependency: YES — concept item; `solution_svg` exists but the
    text does not depend on it.
  - no invented source/article claim: YES.
- risk note: low. No-op. Note: the stored choice [4] `text` carries trailing
  OCR residue ("D-60 전기기사"); that is a `choices`-field issue, out of scope,
  and `choices` is not modified.

### 5. `2015_3회_25` — corrected_q_answer = 4

- source_answer: 4 / source_page: p.9 / evidence: 풀이 (④ 반한시-정한시
  특성) ends 【답】④.
- old solution issue: none in the `solution` / `steps` substance. The
  `solution` defines 반한시 / 순한시 / 정한시 / 반한시-정한시 characteristics
  and concludes "정답: 4번 (반한시-정한시 특성)". The `steps.계산` likewise
  concludes "정답: 4번 (반한시-정한시 특성)". Both match the corrected
  `q.answer` = 4 and both name the choice meaning correctly.
- current consistency assessment: `solution` / `steps` — consistent
  (conclude 4번, 반한시-정한시 특성).
- proposed solution draft: no change.
- proposed steps draft: no change.
- choice-OCR flag: the DB-stored `choices` field for this item is corrupt —
  choice [4] holds page-footer residue ("15년도 3회 / 473 / 전기기사 펄기
  D-60 시리즈") instead of the choice text "반한시-정한시 특성", and choices
  [1]-[3] carry a stray leading "：". Per the apply instruction, `choices`
  is NOT modified by this track. The defect is recorded here as a choice-OCR
  recovery flag. The `solution` / `steps` already state the intended choice
  ④ meaning ("반한시-정한시 특성") correctly, so no `solution` / `steps` edit
  is needed.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES — `solution` / `steps` conclude
    4번 = corrected `q.answer` = 4.
  - no figure dependency: YES — recall item, no figure.
  - no invented source/article claim: YES.
- risk note: MEDIUM (data-side, not solution-side). The `solution` / `steps`
  are consistent and need no edit, but the `choices` field is OCR-corrupt.
  Flagged for the choice-OCR recovery track. `choices` not modified here.

## Aggregate

- Items needing a real solution/steps edit at apply time: 1
  - `2015_2회_23` — `steps.계산` defect fix (complete the truncated tail,
    add explicit ④ conclusion).
- Items already consistent (no change, confirm only): 4
  (`2015_1회_87`, `2015_2회_29`, `2015_3회_22`, `2015_3회_25`).
- Choice-OCR recovery flag: `2015_3회_25` (choice [4] DB text corrupt;
  `choices` not modified).
- No item requires a full from-scratch solution regeneration.

## Status

- This is a dry-run. No `app/data` modification. Not an approval to apply.
- `solution_svg` is not modified here; it is pending a separate audit
  (SVG-AUDIT track).
- Q2 bulk apply remains BLOCKED.
- C20-1 closed (`8f4bdf0`), C20-2 closed (`8ad2689`). C20-4 untouched.
  DQ-1 sealed.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No additional answer correction.
- No `solution` / `steps` apply.
- No `choices` modification (incl. `2015_3회_25` choice-OCR).
- No `solution_svg` modification.
- No C20-1 / C20-2 / C20-4 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
