# Old Answer Conflict Correction — C20-2 Solution/Steps Regeneration Dry-run (2026-05-21)

Solution/steps regeneration dry-run for the 5 C20-2 items that are in state
`answer_corrected_solution_pending`. For each item this document assesses the
existing `solution` / `steps` against the corrected `q.answer` and proposes
an answer-locked draft or records a no-op.

This is a **dry-run document only**. It does NOT modify `app/data` and is not
an approval to apply. `solution_svg` is not modified here and is pending a
separate audit.

- Base commits: `0e6804d` (correction manifest), `c7390e4` (C20-2 answer
  correction apply)
- Prior completed: C20-1 answer + solution closed at `8f4bdf0`
- Manifest: `docs/audit/old_answer_conflict_correction_manifest_2026-05-21.md`
- Apply result (answer): `docs/audit/old_answer_conflict_correction_c20_2_apply_2026-05-21.md`
- Source review packs: `old_answer_manual_source_review_pack{,2}_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Key finding — C20-2 differs from C20-1

C20-1's 5 items were all clean `conclusion_mismatch` cases: the solution body
already concluded the source-correct answer, and only stale old-answer
references needed cleanup. C20-2 is not uniform:

- 2 items (`2007_1회_9`, `2007_2회_64`) are clean — solution and steps already
  conclude the corrected answer. No-op.
- 1 item (`2015_1회_71`) needs light cleanup — solution body concludes the
  corrected answer but carries a stale OCR parenthetical.
- 2 items (`2006_1회_6`, `2006_2회_27`) have a **genuine defect** in the
  existing `solution` / `steps`, not merely a stale reference:
  - `2006_1회_6`: `steps.계산` contains an erroneous extra step (a spurious
    "0.24 → 4.2" re-conversion) and concludes choice ① — internally
    contradicting its own Step 3 and the solution body.
  - `2006_2회_27`: both `solution` and `steps` falsely assert that the correct
    answer is "not among the choices", when choice [4] "유량을 조정하기
    위하여" is exactly the 제수문 주목적.

The proposed fixes for these 2 items are bounded, source-grounded corrections
(the correct value is already derived elsewhere in the same item), NOT a
from-scratch regeneration. No physics or source claim is invented.

Per-item state summary:

| key | corrected answer | existing solution | existing steps | draft type |
| --- | ---: | --- | --- | --- |
| `2006_1회_6` | 3 | concludes (3)번; stale "(보기 표시 누락)" parenthetical | `계산` has erroneous Step 4 → wrongly concludes ① | edit — fix steps defect + solution parenthetical |
| `2006_2회_27` | 4 | concludes (4)번 but framed as "제시되지 않은 옵션" | concludes "선택지 중 올바른 답 없음" — false | edit — remove fabricated "no valid answer" claim |
| `2007_1회_9` | 2 | already concludes (2)번 a=-1/3 | already concludes 2번 | no-op |
| `2007_2회_64` | 1 | already concludes (1)번 안정 | already concludes ① 안정 | no-op |
| `2015_1회_71` | 1 | concludes 1번; stale OCR "(정정 주의… 0번…)" parenthetical | already concludes ① 1 | edit — solution parenthetical cleanup only |

## Per-item drafts

### 1. `2006_1회_6` — corrected_q_answer = 3

- source_answer: 3 / source_page: p.2 / evidence: 풀이 (Q=0.24·CV²t/(ερ))
  ends 【답】③.
- old solution issue: the `solution` body correctly derives
  `Q = 0.24·CV²t/(ρε)` and concludes "정답: (3)번", which matches the corrected
  `q.answer`. The `steps.계산` block, however, derives the same correct result
  in Step 3 (`Q = 0.24·CV²t/(ερ)`) and then adds an **erroneous Step 4** that
  "re-converts" J to cal a second time, replacing 0.24 with 4.2, and concludes
  "정답: ① 4.2·CV²t/(ρε)". Step 4 is mathematically wrong (the result is
  already in cal after Step 3; 0.24 cal/J is the conversion, not 4.2) and its
  conclusion ① contradicts both Step 3 and the solution body.
- current consistency assessment: `solution` body — consistent with corrected
  answer 3. `steps.계산` — INCONSISTENT (concludes ①).
- proposed solution draft: keep the full derivation; replace the final line
  "**정답: (3)번** (보기 표시 누락되었으나 위 식)" with "**정답: (3)번** —
  선택지 ③ `0.24 × CV²t/(ρε)`" (choices [1]-[4] are present).
- proposed steps draft: in `steps.계산`, keep Step 1-3 unchanged; remove the
  erroneous Step 4 block; replace the conclusion with "**정답: ③
  `0.24 × CV²t/(ρε)`**". The corrected conclusion is the value Step 3 already
  derived — no new derivation is introduced.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES after fix — Step 3 result
    `0.24·CV²t/(ρε)` = choice [3] = corrected `q.answer` = 3.
  - no figure dependency: YES — analytic derivation; `solution_svg` exists but
    the text does not depend on it.
  - no invented source/article claim: YES — the fix uses the value already
    present in Step 3 and in the solution body; nothing is invented.
- risk note: MEDIUM. The `steps.계산` defect is a genuine math error, not a
  stale reference. The fix is well-grounded (Step 3 + solution body both give
  the source-correct value), but it removes an existing step rather than only
  deleting stale text. Recommend the apply quote the exact Step 4 text to be
  removed.

### 2. `2006_2회_27` — corrected_q_answer = 4

- source_answer: 4 / source_page: p.4 / evidence: 풀이 (제수문=취수량
  조절·물 유입 단절) ends 【답】④.
- old solution issue: choice [4] is "유량을 조정하기 위하여", which is exactly
  the 제수문 주목적 (취수량 조절). The `solution` concludes "정답: (4)번" but
  appends "(제시되지 않은 옵션)" and frames the whole 오답분석 as if the correct
  purpose were absent from the choices. The `steps.계산` is worse: its
  conclusion is "정답: 제시된 선택지 중 올바른 답 없음" — a false claim, since
  choice [4] is the answer.
- current consistency assessment: `solution` — conclusion (4) matches, but the
  framing falsely says the option is missing. `steps` — INCONSISTENT (concludes
  "no valid answer").
- proposed solution draft: replace "**정답: (4)번** (제시되지 않은 옵션)" with
  "**정답: (4)번** — 선택지 ④ \"유량을 조정하기 위하여\" (제수문은 취수량을
  조절). 오답 분석의 (1)(2)(3)은 그대로 유효." The ✓주목적 block and the
  (1)/(2)/(3) 오답 분석 are kept.
- proposed steps draft: in `steps.계산`, replace the "(4) 정답 불명시 …" line
  and the final "정답: 제시된 선택지 중 올바른 답 없음 …" line with:
  "(4) 유량을 조정하기 위하여: 제수문의 주목적인 취수량 조절·유입 제어에
  해당. ✓" and "**정답: ④ 유량을 조정하기 위하여**".
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES after fix — choice [4] = 4.
  - no figure dependency: YES — concept item, no figure.
  - no invented source/article claim: YES — the fix removes a fabricated
    "no valid answer" claim and points to the choice text that already exists;
    nothing is invented.
- risk note: MEDIUM. The defect is a fabricated claim, not a stale reference.
  The fix is grounded (choice [4] text + source 【답】④), but it rewrites the
  conclusion of both `solution` and `steps`. Recommend the apply quote the
  exact text to be replaced.

### 3. `2007_1회_9` — corrected_q_answer = 2

- source_answer: 2 / source_page: p.2 / evidence: 풀이 (A·B=1+3a=0 → a=-1/3)
  ends 【답】②.
- old solution issue: none. The `solution` derives `A·B = 1+3a = 0 → a = -1/3`
  and concludes "정답: (2)번 a=-1/3". The `steps.계산` concludes "정답: 2번
  -1/3". Both match the corrected `q.answer` = 2.
- current consistency assessment: consistent — solution and steps both
  conclude choice [2].
- proposed solution draft: no change.
- proposed steps draft: no change.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES.
  - no figure dependency: YES — analytic; `solution_svg` exists but text does
    not depend on it.
  - no invented source/article claim: YES.
- risk note: low. No-op; listed for completeness.

### 4. `2007_2회_64` — corrected_q_answer = 1

- source_answer: 1 / source_page: p.6 / evidence: 풀이 (Routh first column all
  positive → stable) ends 【답】①.
- old solution issue: none. The `solution` computes all Hurwitz determinants
  (`D₁=2, D₂=6, D₃=16, D₄=32`, all positive) and concludes "정답: (1번) 안정".
  The `steps.계산` concludes "정답: ① 안정". Both match the corrected
  `q.answer` = 1.
- current consistency assessment: consistent — solution and steps both
  conclude choice [1].
- proposed solution draft: no change.
- proposed steps draft: no change.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES.
  - no figure dependency: YES — analytic; `solution_svg` exists but text does
    not depend on it.
  - no invented source/article claim: YES.
- risk note: low. No-op; listed for completeness.

### 5. `2015_1회_71` — corrected_q_answer = 1

- source_answer: 1 / source_page: p.24 / evidence: 풀이 (L=Nφ/I=12H,
  τ=L/R=1s) ends 【답】①.
- old solution issue: the `solution` derives `L = Nφ/I = 12 H` and
  `τ = L/R = 12/12 = 1 sec` and concludes "정답: 1번", matching the corrected
  `q.answer`. It carries a stale parenthetical "(정정 주의: OCR에서 \"0번\"이라
  표기되어 있으나 정답은 1번)" — an artifact referencing an old answer-state
  inconsistency. The `steps.계산` already concludes "정답: ① 1" cleanly.
- current consistency assessment: `solution` — conclusion correct, stale
  parenthetical only. `steps` — already clean.
- proposed solution draft: replace "**정답: 1번 (정정 주의: OCR에서 \"0번\"이라
  표기되어 있으나 정답은 1번)**" with "**정답: 1번** — 선택지 ① `τ = 1` [sec]".
- proposed steps draft: no change — already concludes ① 1.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES — τ = 1 sec = choice [1] = 1.
  - no figure dependency: YES — analytic; `solution_svg` exists but text does
    not depend on it.
  - no invented source/article claim: YES.
- risk note: low. Solution-only stale-parenthetical removal.

## Aggregate

- Items needing a real solution/steps edit at apply time: 3
  - `2006_1회_6` — steps defect fix (remove erroneous Step 4) + solution
    parenthetical.
  - `2006_2회_27` — remove fabricated "no valid answer" claim in solution and
    steps.
  - `2015_1회_71` — solution stale-parenthetical removal only.
- Items already consistent (no change, confirm only): 2
  (`2007_1회_9`, `2007_2회_64`).
- No item requires a full from-scratch solution regeneration. For
  `2006_1회_6` and `2006_2회_27` the source-correct answer is already derived
  within the item; the fix is bounded.

## Status

- This is a dry-run. No `app/data` modification. Not an approval to apply.
- `solution_svg` is not modified here; it is pending a separate audit
  (SVG-AUDIT track).
- Q2 bulk apply remains BLOCKED.
- C20-1 is closed (`8f4bdf0`). C20-3 / C20-4 are untouched. DQ-1 sealed.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No additional answer correction.
- No `solution` / `steps` apply.
- No `solution_svg` modification.
- No C20-1 / C20-3 / C20-4 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
