# Old Answer Conflict Correction — C20-2 Solution/Steps Apply Result (2026-05-21)

Apply-result log for the C20-2 solution/steps cleanup. The dry-run identified
3 of the 5 C20-2 items as needing a real `solution` / `steps` edit; this step
applied those 3 edits to `app/data/questions.json` and
`app/data/questions.v2.json`. The other 2 items were already consistent with
the corrected `q.answer` and were left unchanged.

This is an apply-result record. No `answer` field was modified here — the
C20-2 answer correction was already applied in `c7390e4`.

- Base commits: `c7390e4` (C20-2 answer correction apply), `11fcced`
  (C20-2 corrected-answer solution dry-run)
- Dry-run: `docs/audit/old_answer_conflict_correction_c20_2_solution_dryrun_2026-05-21.md`
- Apply result (answer): `docs/audit/old_answer_conflict_correction_c20_2_apply_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Edited items (3)

| key | corrected answer | change summary |
| --- | ---: | --- |
| `2006_1회_6` | 3 | `steps.계산`: erroneous Step 4 (a spurious "0.24 → 4.2" re-conversion that wrongly concluded ①) removed; conclusion replaced with "정답: ③ 0.24×CV²t/(ερ)". `solution`: stale "(보기 표시 누락되었으나 위 식)" parenthetical replaced with an explicit choice-③ reference. |
| `2006_2회_27` | 4 | `solution`: "정답: (4)번 (제시되지 않은 옵션)" — the false "option not present" framing — replaced with an explicit choice-④ reference. `steps.계산`: the fabricated "(4) 정답 불명시 … 정답: 제시된 선택지 중 올바른 답 없음" block replaced with a factual choice-④ evaluation and conclusion. |
| `2015_1회_71` | 1 | `solution`: stale OCR parenthetical "(정정 주의: OCR에서 \"0번\"이라 표기되어 있으나 정답은 1번)" removed; conclusion kept at 1번 with an explicit choice-① reference. `steps` unchanged (already concluded ① 1). |

For all 3 items the conclusions are locked to the corrected `q.answer`.

## No-op items (2)

| key | corrected answer | reason for no change |
| --- | ---: | --- |
| `2007_1회_9` | 2 | `solution` derives `A·B = 1+3a = 0 → a = -1/3` and `steps` both conclude choice [2] — already consistent. No `app/data` change. |
| `2007_2회_64` | 1 | `solution` computes all Hurwitz determinants positive → 안정, and `steps` both conclude choice [1] — already consistent. No `app/data` change. |

## Risk note — `2006_1회_6` and `2006_2회_27` were genuine defect fixes

Unlike C20-1 (all stale-reference cleanups), 2 of these 3 edits corrected a
real defect in the existing content. The fixes are source-grounded:

- `2006_1회_6` — the removed Step 4 was mathematically wrong: `steps.계산`
  Step 3 already derives `Q = 0.24·CV²t/(ερ)` (the source-correct value), and
  Step 4 spuriously multiplied by 4.2 to conclude ①. The corrected conclusion
  ③ `0.24·CV²t/(ερ)` is the value Step 3 derived and the value the `solution`
  body independently derives. Verification basis: Step 3 of the same item +
  the solution body + source 【답】③ (pack1, p.2). Nothing was invented; an
  erroneous step was removed and the conclusion aligned to the existing
  correct derivation.
- `2006_2회_27` — the existing `solution` / `steps` falsely claimed the
  correct answer was absent from the choices. Choice [4] "유량을 조정하기
  위하여" is exactly the 제수문 주목적 (취수량 조절). Verification basis: the
  stored `choices` list (choice [4] text) + source 【답】④ (pack2, p.4). The
  fix removed a fabricated "no valid answer" claim and pointed to the existing
  choice text; nothing was invented.

`2015_1회_71` was a simple stale-parenthetical removal (low risk).

## Changed files

- `app/data/questions.json` — `solution` / `steps` of 3 items updated.
- `app/data/questions.v2.json` — `solution` / `steps` of 3 items updated.

`solution` / `steps` content strings are identical between the two files; the
files differ only in provenance metadata (`*_source`) and `solution_svg`
representation, neither of which was touched.

## Changed fields

- `2006_1회_6`: `solution`, `steps`.
- `2006_2회_27`: `solution`, `steps`.
- `2015_1회_71`: `solution`.
- No other field changed for any item. `answer`, `choices`, `text`,
  metadata, `*_source`, and `solution_svg` are unchanged.

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- Exactly 3 items changed in each file; each change is confined to
  `solution` / `steps` only.
- C20-2 answers unchanged: `2006_1회_6`=3, `2006_2회_27`=4, `2007_1회_9`=2,
  `2007_2회_64`=1, `2015_1회_71`=1.
- No-op items (`2007_1회_9`, `2007_2회_64`) byte-identical to pre-state.
- Edited items: all non-`solution`/`steps` fields unchanged.
- `choices` / `text` / metadata / `solution_svg` unchanged for all items.
- C20-1 items (5 keys), C20-3 / C20-4 items (9 keys), and DQ-1 items
  (`2014_2회_50`, `2014_3회_62`) unchanged.
- `git diff --check` — no whitespace errors.
- Serialization preserved — diff confined to the edited string lines; no mass
  reformatting.

## Downstream status

- C20-2 `answer_corrected_solution_pending` state is RESOLVED for all 5 items:
  3 had their `solution` / `steps` corrected to match the corrected `q.answer`;
  2 were already consistent.
- `solution_svg` is still pending the SVG-AUDIT track (not modified here).

## Status

- Q2 bulk apply remains BLOCKED.
- This step covered C20-2 only. C20-3 / C20-4 are not applied and require
  separate per-batch approval.
- C20-1 is closed (`13036de` + `8f4bdf0`). C20-2 is now closed
  (`c7390e4` + this step).
- DQ-1 items remain sealed pending the defective / multi-answer policy.

## Not done in this step

- No `answer` modification.
- No `choices` / question text / metadata modification.
- No `solution_svg` modification.
- No modification of the 2 no-op items.
- No C20-1 / C20-3 / C20-4 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
