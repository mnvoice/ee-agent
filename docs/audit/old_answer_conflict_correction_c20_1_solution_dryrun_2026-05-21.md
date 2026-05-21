# Old Answer Conflict Correction — C20-1 Solution/Steps Regeneration Dry-run (2026-05-21)

Solution/steps regeneration dry-run for the 5 C20-1 items that are in state
`answer_corrected_solution_pending`. For each item this document records the
state of the existing `solution` / `steps` against the corrected `q.answer`
and proposes an answer-locked draft.

This is a **dry-run document only**. It does NOT modify `app/data` and is not
an approval to apply. `solution_svg` is not modified here and is pending a
separate audit.

- Base commits: `0e6804d` (correction manifest), `13036de` (C20-1 answer
  correction apply)
- Manifest: `docs/audit/old_answer_conflict_correction_manifest_2026-05-21.md`
- Apply result: `docs/audit/old_answer_conflict_correction_c20_1_apply_2026-05-21.md`
- Source review pack: `old_answer_manual_source_review_pack_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Key finding before the per-item drafts

The 20 conflict items came from the C1 pilot's `conclusion_mismatch` set —
items where the existing `solution` already concluded one choice while the
**stored** `q.answer` named a different one. After the C20-1 answer
correction, the stored `q.answer` now equals the value the solution body was
already arguing toward.

Consequence: for these 5 items, full solution regeneration is NOT required.
The real pending work is **cleanup of stale references to the old answer**
(parentheticals, "주의" notes that argue against the now-removed old answer,
and one steps choice-number typo). One item (`2001_3회_43`) has a genuine
reasoning gap that is bounded by an OCR-damaged stored choice text.

Per-item state summary:

| key | corrected answer | existing solution body | existing steps | draft type |
| --- | ---: | --- | --- | --- |
| `1998_4회_10` | 4 | already concludes choice 4 | concludes 4, but carries a stale "주의" note vs old answer ① | stale-reference cleanup |
| `2001_1회_68` | 3 | already concludes choice 3 | choice-number typo: says ④ for 가속도 (which is ③) | steps typo fix |
| `2001_3회_41` | 4 | already concludes choice 4 | already concludes 4 | already consistent — no change |
| `2001_3회_43` | 2 | concludes choice 2 but reasoning is hollow ("기존 풀이에 따르면") | concludes 2, same hollow basis | risk-flagged; bounded by OCR-damaged choice |
| `2002_3회_4` | 4 | already concludes choice 4 | already concludes 4 | already consistent — no change |

## Per-item drafts

### 1. `1998_4회_10` — corrected_q_answer = 4

- source_answer: 4 / source_page: p.2 / evidence: 문제 10 풀이 box ends 【답】④.
- old solution issue: the solution body correctly derives
  `B₂ = μ₀(4a_x − 8a_y + 8a_z)` = choice [4] and already prints "정답: 4번".
  Two stale fragments reference the old answer state: (a) solution ends with
  "정답: 4번 **(선택지 미제시)**" — but choices [1]-[4] do exist, so the
  parenthetical is wrong; (b) the `steps.계산` block ends with a "주의" note
  arguing that "제시된 정답 ①은 수식적으로 성립하지 않는다" — that note exists
  only because the stored answer used to be 1. With `q.answer` now 4, that
  note is obsolete.
- proposed solution draft: keep the full derivation unchanged; in the final
  line replace "**정답: 4번** (선택지 미제시)" with "**정답: 4번** — 선택지 ④
  `B₂ = μ₀(4a_x − 8a_y + 8a_z)`".
- proposed steps draft: keep `인식` / `변환` / `계산` derivation unchanged;
  remove the trailing "> **주의:** 제시된 정답 ①..." paragraph from `계산`
  (it argues against an answer value that no longer exists).
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES — derivation result is choice
    [4], which equals corrected `q.answer` = 4.
  - no figure dependency: YES — pure boundary-condition vector computation;
    no figure is referenced. (`solution_svg` exists but the solution text does
    not depend on it.)
  - no invented source/article claim: YES — no statute or external source is
    cited; the derivation is self-contained.
- risk note: low. The change is deletion of stale text; the derivation itself
  is untouched and already source-consistent.

### 2. `2001_1회_68` — corrected_q_answer = 3

- source_answer: 3 / source_page: p.6 / evidence: 풀이 (가속도편차상수 Kₐ)
  ends 【답】③.
- old solution issue: the solution body is correct and prints "정답: 3번
  (가속도 오차 상수)". The `steps.계산` block, however, ends with "**정답: ④
  가속도 오차 상수**" — a choice-number typo. 가속도 오차 상수 is choice [3],
  not [4]. The label ④ is inconsistent with both the choices and the
  corrected `q.answer`.
- proposed solution draft: no change — the solution body already concludes
  choice 3 correctly.
- proposed steps draft: in `steps.계산`, change "**정답: ④ 가속도 오차 상수**
  (또는 선택지에 따라 위치/속도/가속도 중 포물선에 해당하는 답 선택)" to
  "**정답: ③ 가속도 오차 상수**". The trailing "(또는 선택지에 따라...)"
  hedge is removed as the choice is now fixed.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES after the typo fix — 가속도
    오차 상수 = choice [3] = corrected `q.answer` = 3.
  - no figure dependency: YES — definition-recall item, no figure.
  - no invented source/article claim: YES — standard control-theory
    definitions only.
- risk note: low. Single choice-number correction in `steps`; the conceptual
  content is already correct.

### 3. `2001_3회_41` — corrected_q_answer = 4

- source_answer: 4 / source_page: p.3 / evidence: 풀이 (철손은 무부하손)
  ends 【답】④.
- old solution issue: none. Both `solution` and `steps` already evaluate all
  four choices and conclude "(4)번" — 철손이 증가한다 is the incorrect
  statement, because 철손 is a no-load loss independent of load. This matches
  corrected `q.answer` = 4.
- proposed solution draft: no change — already answer-locked to choice 4.
- proposed steps draft: no change — already answer-locked to choice 4.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES.
  - no figure dependency: YES — concept item, no figure.
  - no invented source/article claim: YES.
- risk note: low. Item is already consistent; listed for completeness. No
  apply needed for this item beyond confirming no change.

### 4. `2001_3회_43` — corrected_q_answer = 2

- source_answer: 2 / source_page: p.4 / evidence: 풀이 box ends 【답】②;
  the source PDF choices are readable, but the DB-stored choice text is
  OCR-damaged (a separate DB-side issue).
- old solution issue: the solution concludes "정답: (2)번", which matches the
  corrected `q.answer`. But the reasoning is hollow: it states "(2)번 보기가
  불완전하게 제시되었으나, 기존 풀이에 따르면 (2)번이 정답" — it does not
  explain why choice [2] is the incorrect statement. The DB-stored choice [2]
  text ("3자 권선을 설치하여 1자 권선과 조정권선을 회전자에, 2자 권선을
  고정자에 설치하였다") is OCR-damaged, so the wrong statement cannot be
  reliably analysed from the stored text alone.
- proposed solution draft: keep the conclusion locked to choice [2]
  (source 【답】②). Do NOT fabricate a reason for why choice [2] is wrong —
  the source 풀이 detail and a clean choice text are both unavailable. Minimal
  proposed body: state the four choices describe the structure of a commutator
  frequency converter; the source 풀이 marks choice ② as the incorrect
  statement; a full explanation of the error in choice ② is deferred because
  the stored choice ② text is OCR-damaged.
- proposed steps draft: keep `인식` / `변환` unchanged; in `계산`, keep the
  (1)/(3)/(4) checks, and for (2) replace "문제에서 제시된 보기가 불완전함 /
  제시된 선택지 중 완전하지 않은 보기가 정답으로 지정됨" with a factual note:
  "source 풀이가 ②를 틀린 설명으로 표시 (【답】②); 저장된 ② 선택지 텍스트는
  OCR 손상 상태로, 오류 내용의 정밀 분석은 choice-OCR 복구 후로 보류."
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES — locked to choice [2] = 2.
  - no figure dependency: YES — concept item, no figure.
  - no invented source/article claim: YES — explicitly avoids inventing the
    reason; defers it instead.
- risk note: MEDIUM. The conclusion is source-locked and safe, but the
  solution cannot be made fully explanatory while choice [2] is OCR-damaged.
  This item should additionally be flagged for the choice-OCR recovery track.
  Recommendation: apply only a minimal, conclusion-locked solution; do not
  attempt a detailed wrong-statement analysis until the choice text is
  recovered.

### 5. `2002_3회_4` — corrected_q_answer = 4

- source_answer: 4 / source_page: p.2 / evidence: 풀이 (potential-form
  surface integral) ends 【답】④.
- old solution issue: none in substance. Both `solution` and `steps` derive
  `U = (1/4πε)∬(ρ_s/r)dS` and conclude "④번", matching corrected `q.answer`.
  Minor: the `steps.계산` block carries a parenthetical "(참고: 참고 풀이의
  정답 표기 오류 - 실제 정답은 ④번...)" — this referenced the old stored
  answer. With `q.answer` now 4, the parenthetical is optional cleanup, not a
  correctness issue.
- proposed solution draft: no change — already answer-locked to choice 4.
- proposed steps draft: optional minor cleanup — the "(참고: 참고 풀이의 정답
  표기 오류...)" parenthetical in `계산` may be removed since the stored
  answer is now consistent. Not required for correctness.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES.
  - no figure dependency: YES — the derivation is analytic; `solution_svg`
    exists but the text does not depend on it.
  - no invented source/article claim: YES.
- risk note: low. Item is already consistent. Note the stored choice [4] text
  carries trailing OCR residue ("2-286 D-60 전기기사"); that is a choice-text
  issue, out of scope for this answer/solution dry-run.

## Aggregate

- Items needing a real solution/steps edit at apply time: 3
  (`1998_4회_10` stale-note cleanup, `2001_1회_68` steps choice-number fix,
  `2001_3회_43` hollow-reasoning replacement — conclusion-locked, minimal).
- Items already consistent (no change, confirm only): 2
  (`2001_3회_41`, `2002_3회_4` — `2002_3회_4` has an optional parenthetical
  cleanup only).
- No item requires a full from-scratch solution regeneration. The conflict
  set was `conclusion_mismatch`: the solution bodies were already arguing the
  source-correct answer.

## Status

- This is a dry-run. No `app/data` modification. Not an approval to apply.
- `solution_svg` is not modified here; it is pending a separate audit
  (SVG-AUDIT track).
- Q2 bulk apply remains BLOCKED.
- `2001_3회_43` is additionally flagged for the choice-OCR recovery track.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No additional answer correction.
- No `solution` / `steps` apply.
- No `solution_svg` modification.
- No C20-2 / C20-3 / C20-4 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
