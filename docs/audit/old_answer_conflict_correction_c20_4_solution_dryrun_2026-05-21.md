# Old Answer Conflict Correction — C20-4 Solution/Steps Regeneration Dry-run (2026-05-21)

Solution/steps regeneration dry-run for the 4 C20-4 items that are in state
`answer_corrected_solution_pending`. For each item this document assesses the
existing `solution` / `steps` against the corrected `q.answer` (= 4 for all
4 items) and proposes an answer-locked draft or records a no-op.

This is a **dry-run document only**. It does NOT modify `app/data` and is not
an approval to apply. `solution_svg` is not modified here and is pending a
separate audit.

- Base commits: `0e6804d` (correction manifest), `c9ea03c` (C20-4 answer
  correction apply)
- Prior completed: C20-1 closed at `8f4bdf0`, C20-2 closed at `8ad2689`,
  C20-3 closed at `5f80afa`
- Manifest: `docs/audit/old_answer_conflict_correction_manifest_2026-05-21.md`
- Apply result (answer): `docs/audit/old_answer_conflict_correction_c20_4_apply_2026-05-21.md`
- Source review pack: `old_answer_manual_source_review_pack3_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Key finding — C20-4 has no no-op items

C20-3 had 4 no-op items. C20-4 is the opposite: all 4 items need some
cleanup. The defects range from stale hedges to one genuinely wrong `steps`
conclusion:

- `2016_3회_21`: `steps.변환` and `steps.계산` both conclude choice [1]
  ("전류에 비례") — the **opposite** of the corrected answer 4
  ("전압의 제곱에 반비례"). This is a genuine wrong conclusion, not a stale
  reference.
- `2016_1회_69`, `2016_1회_70`: `solution` body concludes (4)번 correctly,
  but `steps` carries a stale alternative-answer hedge.
- `2016_1회_44`: `solution` and `steps` conclude 4번, but the conclusion is
  weakened by a hedge sentence, and the reasoning body is built on an item
  enumeration that does not match the actual choice texts (a deeper weakness,
  see its risk note).

The proposed edits stay within minimal cleanup: removing stale hedges and, for
`2016_3회_21`, correcting a wrong conclusion using the derivation already
present in the same item's `solution` body. No control/power/machine theory
is newly expanded; no source or article is invented.

Per-item state summary:

| key | corrected answer | solution | steps | draft type |
| --- | ---: | --- | --- | --- |
| `2016_1회_44` | 4 | concludes 4번, weakened by a hedge sentence | concludes 4번, weak reasoning | edit (light) — remove hedge; body weakness flagged |
| `2016_1회_69` | 4 | already concludes (4)번 cleanly | `계산` carries stale "또는 … 1번 (공진치)" hedge | edit — steps hedge removal |
| `2016_1회_70` | 4 | already concludes (4)번 cleanly | `계산` carries stale "(선택지에 명시 필요)" hedge, no explicit ④ | edit (light) — steps hedge removal + explicit ④ |
| `2016_3회_21` | 4 | already concludes 4번 cleanly | `변환` + `계산` conclude choice [1] — WRONG | edit — steps wrong-conclusion fix |

## Per-item drafts

### 1. `2016_1회_44` — corrected_q_answer = 4

- source_answer: 4 / source_page: p.15 / evidence: 풀이 (전기자 반작용 영향
  4종) ends 【답】④.
- old solution issue: the `solution` concludes "정답: 4번", which matches the
  corrected `q.answer`. Two weaknesses: (a) it ends with a hedge sentence
  "다만 문제 원문이 불완전하여 정확한 오답지를 특정하기 어렵습니다." that
  contradicts the firm answer-locked conclusion — a leftover of the
  old-answer ambiguity (old stored answer was 2); (b) the `solution` body and
  `steps.계산` enumerate effects ("중성축 이동 / 주자속 감소 / 섬락 / 출력
  감소") that do NOT correspond to the actual choice texts (choice [4] is
  about EMF in brush-short-circuited coils — a commutation topic, not armature
  reaction). The conclusion is right; the reasoning body is built on a
  mismatched enumeration.
- current consistency assessment: conclusion consistent (4번); reasoning body
  weak.
- proposed solution draft: minimal cleanup only — remove the trailing hedge
  sentence "다만 문제 원문이 불완전하여 정확한 오답지를 특정하기 어렵습니다."
  so the answer-locked conclusion "정답: 4번" stands without contradiction.
  Do NOT rewrite the enumeration body (see risk note).
- proposed steps draft: minimal cleanup only — in `steps.계산`, the parenthetical
  "(불완전한 보기이지만 개념상)" is a hedge of the same kind; it may be
  removed. The conclusion "정답: 4번" is kept.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES — both `solution` and `steps`
    conclude 4번 = corrected `q.answer` = 4.
  - no figure dependency: YES — recall item, no figure.
  - no invented source/article claim: YES — the proposed change only removes
    hedges; nothing is added.
- risk note: MEDIUM. The conclusion is source-locked and the hedge removal is
  safe minimal cleanup. However, the `solution` / `steps` reasoning body
  enumerates generic armature-reaction effects that do not map to the actual
  choice texts. A correct explanation of why choice [4] is "not an armature
  reaction effect" (it is a commutation phenomenon) would require rewriting
  the reasoning — that is beyond minimal cleanup and is NOT done here, to
  avoid overexpansion and fabrication. Flagged for a deeper solution review
  with the source 풀이.

### 2. `2016_1회_69` — corrected_q_answer = 4

- source_answer: 4 / source_page: p.23 / evidence: 풀이 (고유주파수는
  안정도와 무관) ends 【답】④.
- old solution issue: the `solution` body explains that 공진치 / 위상여유 /
  이득여유 are stability measures while 고유주파수 is not, and concludes
  "정답: (4)번" — consistent with the corrected `q.answer`. The `steps.계산`
  also concludes "정답: 4번 (고유주파수 …)" but appends a stale hedge
  "또는 선택지가 공진치인 경우 **1번 (공진치)**" — a leftover
  alternative-answer hedge that contradicts the firm corrected answer.
- current consistency assessment: `solution` — consistent and clean.
  `steps.계산` — conclusion correct but carries a contradicting hedge.
- proposed solution draft: no change — already concludes (4)번 cleanly.
- proposed steps draft: in `steps.계산`, remove the trailing hedge "또는
  선택지가 공진치인 경우 **1번 (공진치)**" so the conclusion "정답: 4번
  (고유주파수)" stands alone.
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES — choice [4] 고유주파수 = 4.
  - no figure dependency: YES — concept item; `solution_svg` exists but the
    text does not depend on it.
  - no invented source/article claim: YES — only a hedge is removed.
- risk note: low. Stale-hedge removal in `steps` only.

### 3. `2016_1회_70` — corrected_q_answer = 4

- source_answer: 4 / source_page: p.23 / evidence: 풀이 (Nyquist 임계점
  -1+j0 → 0dB, ±180°) ends 【답】④.
- old solution issue: the `solution` body computes `|-1| = 1 → 0 dB` and
  phase `±180°`, reviews all choices, and concludes "정답: (4)번 0[dB],
  ±180°" — consistent with the corrected `q.answer`. The `steps.계산` reaches
  the same values but carries a stale parenthetical "(선택지에 명시 필요)" and
  ends "정답: 0[dB], ±180° (표준 정답은 일반적으로 180° 또는 -180°)" — it
  states the value but not an explicit choice ④.
- current consistency assessment: `solution` — consistent and clean.
  `steps.계산` — values correct but the conclusion is not stated as an
  explicit choice ④ and carries stale parentheticals.
- proposed solution draft: no change — already concludes (4)번 cleanly.
- proposed steps draft: in `steps.계산`, remove the stale "(선택지에 명시
  필요)" parenthetical from the choice-④ review line, and replace the final
  "**정답: 0[dB], ±180°** (표준 정답은 일반적으로 180° 또는 -180°)" with an
  explicit "**정답: ④ 0[dB], -180°**" (choice [4] text is "0[dB], -180°").
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES after fix — choice [4]
    "0[dB], -180°" = 4.
  - no figure dependency: YES — analytic item, no figure.
  - no invented source/article claim: YES — only stale parentheticals are
    removed and the conclusion made explicit; the values are unchanged.
- risk note: low. Stale-parenthetical removal + explicit choice number in
  `steps` only.

### 4. `2016_3회_21` — corrected_q_answer = 4

- source_answer: 4 / source_page: p.7 / evidence: 풀이 (전선 단면적 A ∝ 1/V²)
  ends 【답】④.
- old solution issue: the `solution` body derives the full chain — at
  constant transmitted power `I ∝ 1/V`, at constant loss `R ∝ V²`, so
  `A ∝ 1/R ∝ 1/V²` — and concludes "정답: 4번 - 전압의 제곱에 반비례한다",
  consistent with the corrected `q.answer`. The `steps`, however, are
  defective: `steps.변환` derives `A ∝ I²` and then wrongly states "전선의
  굵기는 전류에 비례한다" (misreading `I²` as `I`), and `steps.계산`
  concludes "정답: 1. 전류에 비례한다" — choice [1], the OPPOSITE of the
  corrected answer.
- current consistency assessment: `solution` — consistent (concludes 4번).
  `steps.변환` and `steps.계산` — INCONSISTENT (conclude choice [1]).
- proposed solution draft: no change — the `solution` body already derives
  `A ∝ 1/V²` and concludes 4번.
- proposed steps draft: correct the two wrong conclusions using the chain
  already present in the same item's `solution` body. `steps.변환`: keep the
  `A ∝ I²` derivation, then complete it — since `I ∝ 1/V` (from
  `P = √3·V·I·cosθ` constant), `A ∝ I² ∝ 1/V²` — and change the closing
  sentence from "전선의 굵기는 전류에 비례한다" to "전선의 굵기는 전압의
  제곱에 반비례한다". `steps.계산`: change the final "∴ **정답: 1. 전류에
  비례한다** (전선의 굵기 A는 전류 I에 정확히 비례)" to a conclusion that
  combines `A ∝ I²` with `I ∝ 1/V` to give `A ∝ 1/V²`, ending "**정답: ④
  전압의 제곱에 반비례한다**".
- answer-lock checks:
  - conclusion matches corrected_q_answer: YES after fix — `A ∝ 1/V²` =
    choice [4] = 4.
  - no figure dependency: YES — analytic item, no figure.
  - no invented source/article claim: YES — the fix uses the derivation
    (`I ∝ 1/V`, `A ∝ I²`) already present in the `solution` body and the
    `steps` themselves; the missing link `A ∝ I² ∝ 1/V²` connects existing
    pieces. Nothing is invented.
- risk note: MEDIUM-HIGH. `steps.변환` and `steps.계산` had a genuinely wrong
  conclusion (choice [1], opposite of source). The fix is grounded (the
  solution body holds the correct full derivation), but it rewrites the
  concluding statements of both `steps` sub-fields. Recommend the apply quote
  the exact text to be replaced and keep the correction to the conclusion
  chain only (no expansion of the surrounding theory).

## Aggregate

- Items needing a real solution/steps edit at apply time: 4 (all of C20-4).
  - `2016_1회_44` — solution + steps hedge removal (light); body weakness
    flagged, not fixed.
  - `2016_1회_69` — steps stale-hedge removal.
  - `2016_1회_70` — steps stale-parenthetical removal + explicit ④.
  - `2016_3회_21` — steps wrong-conclusion fix (변환 + 계산).
- No-op items: 0.
- No item requires a full from-scratch solution regeneration. For
  `2016_3회_21` the corrected derivation is already in the `solution` body.

## Status

- This is a dry-run. No `app/data` modification. Not an approval to apply.
- `solution_svg` is not modified here; it is pending a separate audit
  (SVG-AUDIT track).
- Q2 bulk apply remains BLOCKED.
- C20-1 closed (`8f4bdf0`), C20-2 closed (`8ad2689`), C20-3 closed
  (`5f80afa`). DQ-1 sealed.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No additional answer correction.
- No `solution` / `steps` apply.
- No `choices` modification.
- No `solution_svg` modification.
- No C20-1 / C20-2 / C20-3 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
