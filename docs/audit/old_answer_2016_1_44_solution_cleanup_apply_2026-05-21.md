# Old Answer — `2016_1회_44` Solution/Steps Cleanup Apply Result (2026-05-21)

Apply-result log for the `2016_1회_44` solution/steps cleanup. The reasoning
review (`fb3bb91`) verdict was `needs_solution_cleanup`; the cleanup dry-run
(`9536ae6`) drafted a corrected, choice-matched `solution` / `steps`. This
step applied that draft to `app/data/questions.json` and
`app/data/questions.v2.json`.

This is an apply-result record. No `answer` field was modified — `q.answer`
remains 4 (corrected earlier in `c9ea03c`).

- Base commits: `fb3bb91` (`2016_1회_44` reasoning review), `9536ae6`
  (`2016_1회_44` solution cleanup dry-run)
- Reasoning review: `docs/audit/old_answer_2016_1_44_reasoning_review_2026-05-21.md`
- Dry-run: `docs/audit/old_answer_2016_1_44_solution_cleanup_dryrun_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Changed record

- `2016_1회_44` (전기기기, 암기형).

## Change summary

The `solution` and `steps` (`인식` / `변환` / `계산`) were replaced with the
dry-run draft. The previous reasoning body enumerated a generic
armature-reaction effect list (중성축 이동 / 주자속 감소 / 섬락 / 출력감소)
mapped to the wrong choice numbers and never addressed the actual content of
choice [4]. The new reasoning analyses the actual choice texts:

- [1] 자속 감소 → 유기기전력 감소 — demagnetization, an armature-reaction
  effect (true statement).
- [2] 발전기 회전 방향 중성축 이동 — armature-reaction effect (true).
- [3] 전동기 회전 방향과 반대 중성축 이동 — armature-reaction effect (true).
- [4] 브러시 단락 코일 기전력 → 브러시 사이 유기기전력 증가 — a commutation
  (정류) reactance-voltage phenomenon, NOT an armature-reaction effect; and
  armature reaction decreases (not increases) the EMF. → the answer.

The conclusion remains "정답: 4번", consistent with `q.answer` = 4.

The wording nuance noted in the dry-run (choices [2]/[3] say "기하학적
중성축" where standard theory shifts the "전기적 중성축") is handled in the
`solution` by phrasing the effect as "중성축 이동" without contradicting or
rewriting the stored choice text. `choices` were not modified.

## Changed files

- `app/data/questions.json` — `solution` / `steps` of `2016_1회_44` replaced.
- `app/data/questions.v2.json` — `solution` / `steps` of `2016_1회_44`
  replaced.

`solution` / `steps` content strings are identical between the two files; the
files differ only in provenance metadata (`*_source`) and `solution_svg`
representation, neither of which was touched. (This item has no
`solution_svg`.)

## Changed fields

- `2016_1회_44`: `solution`, `steps`.

## Unchanged

- `answer` = 4 (not modified).
- `choices` (intact, including the [2]/[3] "기하학적 중성축" wording).
- question `text`.
- metadata (`subject`, `q_no`, `q_type`, `difficulty`, `quality`, `tag`,
  `year`, `session`, `*_source`).
- `solution_svg` (this item has none).

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- Exactly 1 item changed in each file; the change is confined to
  `solution` / `steps`.
- `2016_1회_44` `answer` remains 4.
- `2016_1회_44` non-`solution`/`steps` fields unchanged; `choices`, `text`,
  and `solution_svg` byte-identical to pre-state.
- `steps` keys remain `['인식', '변환', '계산']`.
- `solution` and `steps.계산` both conclude "정답: 4번".
- No other record changed.
- `git diff --check` — no whitespace errors.
- Serialization preserved — diff confined to the changed strings; no mass
  reformatting.

## Final verdict

`reasoning_cleanup_closed`

`2016_1회_44` is closed: `q.answer` (4) correct, `choices` intact, and the
`solution` / `steps` reasoning now matches the actual choice texts and
correctly explains why choice [4] is the answer.

## Downstream

- `solution_svg`: this item has none — no action (consistent with the SVG
  consistency audit, which recorded `2016_1회_44` as `no_svg`).
- DQ-1 (`2014_2회_50`, `2014_3회_62`) and the choice-OCR recovery items
  (`2001_3회_43`, `2015_3회_25`) remain separate, unaffected by this step.

## Status

- `2016_1회_44` reasoning cleanup closed.
- Q2 bulk apply remains BLOCKED.
- DQ-1 items remain `defer`; choice-OCR recovery remains a separate track.

## Not done in this step

- No `answer` modification.
- No `choices` / question text / metadata modification.
- No `solution_svg` modification.
- No modification of any other record.
- No paid API call.
- No push.
