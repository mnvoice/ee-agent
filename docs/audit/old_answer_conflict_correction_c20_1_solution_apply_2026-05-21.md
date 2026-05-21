# Old Answer Conflict Correction — C20-1 Solution/Steps Apply Result (2026-05-21)

Apply-result log for the C20-1 solution/steps cleanup. The dry-run identified
3 of the 5 C20-1 items as needing a real `solution` / `steps` edit; this step
applied those 3 edits to `app/data/questions.json` and
`app/data/questions.v2.json`. The other 2 items were already consistent with
the corrected `q.answer` and were left unchanged.

This is an apply-result record. No `answer` field was modified here — the
C20-1 answer correction was already applied in `13036de`.

- Base commits: `13036de` (C20-1 answer correction apply), `f2c50d8`
  (C20-1 corrected-answer solution dry-run)
- Dry-run: `docs/audit/old_answer_conflict_correction_c20_1_solution_dryrun_2026-05-21.md`
- Apply result (answer): `docs/audit/old_answer_conflict_correction_c20_1_apply_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Edited items (3)

| key | corrected answer | change summary |
| --- | ---: | --- |
| `1998_4회_10` | 4 | `solution`: final line "정답: 4번 (선택지 미제시)" replaced with "정답: 4번 — 선택지 ④ B₂=μ₀(4a_x−8a_y+8a_z)". `steps.계산`: trailing "주의" paragraph (which argued against the now-removed old answer ①) removed. |
| `2001_1회_68` | 3 | `steps.계산`: choice-number typo fixed — "정답: ④ 가속도 오차 상수 (또는 …)" replaced with "정답: ③ 가속도 오차 상수". `solution` unchanged (already concluded 3). |
| `2001_3회_43` | 2 | `solution`: hollow final paragraph ("기존 풀이에 따르면 …") replaced with a source-locked, non-fabricated statement (source 풀이 marks ②; choice-② error detail deferred due to OCR damage). `steps.계산`: "(2번)" block likewise replaced with the source-locked, OCR-deferral note. |

For all 3 items the derivation/reasoning bodies were preserved; only the
stale old-answer references and one choice-number typo were corrected. The
conclusions remain locked to the corrected `q.answer`.

## No-op items (2)

| key | corrected answer | reason for no change |
| --- | ---: | --- |
| `2001_3회_41` | 4 | `solution` and `steps` already evaluate all choices and conclude (4)번 — consistent with corrected `q.answer`. No `app/data` change. |
| `2002_3회_4` | 4 | `solution` and `steps` already derive U=(1/4πε)∬(ρ_s/r)dS and conclude ④번 — consistent with corrected `q.answer`. The optional parenthetical cleanup noted in the dry-run was not required for correctness and was not applied. No `app/data` change. |

## `2001_3회_43` — choice-OCR recovery flag

The DB-stored choice [2] text of `2001_3회_43`
("3자 권선을 설치하여 1자 권선과 조정권선을 회전자에, 2자 권선을 고정자에
설치하였다") is OCR-damaged. The source review pack recorded that the source
PDF choices are readable but the DB-stored choice text is corrupt. The applied
`solution` / `steps` therefore lock the conclusion to choice ② (source 【답】②)
without fabricating the reason the statement is wrong.

- Flag: `2001_3회_43` choice [2] requires choice-OCR recovery.
- Scope: this flag is recorded in audit only. The `choices` field in
  `app/data` was NOT modified.
- Follow-up: once the choice text is recovered, the `solution` / `steps` for
  this item can be expanded with the specific wrong-statement analysis.

## Changed files

- `app/data/questions.json` — `solution` / `steps` of 3 items updated.
- `app/data/questions.v2.json` — `solution` / `steps` of 3 items updated.

`solution` / `steps` content strings are identical between the two files; the
files differ only in provenance metadata (`*_source`) and `solution_svg`
representation, neither of which was touched.

## Changed fields

- `1998_4회_10`: `solution`, `steps`.
- `2001_1회_68`: `steps`.
- `2001_3회_43`: `solution`, `steps`.
- No other field changed for any item. `answer`, `choices`, `text`,
  metadata, `*_source`, and `solution_svg` are unchanged.

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- Exactly 3 items changed in each file; each change is confined to
  `solution` / `steps` only.
- C20-1 answers unchanged: `1998_4회_10`=4, `2001_1회_68`=3, `2001_3회_41`=4,
  `2001_3회_43`=2, `2002_3회_4`=4.
- No-op items (`2001_3회_41`, `2002_3회_4`) byte-identical to pre-state.
- Edited items: all non-`solution`/`steps` fields unchanged.
- `choices` / `text` / metadata / `solution_svg` unchanged for all items.
- DQ-1 items (`2014_2회_50`, `2014_3회_62`) and C20-2 / C20-3 / C20-4 items
  (16 keys) unchanged.
- `git diff --check` — no whitespace errors.
- Serialization preserved — diff confined to the edited string lines; no mass
  reformatting.

## Downstream status

- C20-1 `answer_corrected_solution_pending` state is RESOLVED for all 5 items:
  3 had their `solution` / `steps` cleaned to match the corrected `q.answer`;
  2 were already consistent.
- `solution_svg` is still pending the SVG-AUDIT track (not modified here).
- `2001_3회_43` carries a choice-OCR recovery flag (above).

## Status

- Q2 bulk apply remains BLOCKED.
- This step covered C20-1 only. C20-2 / C20-3 / C20-4 are not applied and
  require separate per-batch approval.
- DQ-1 items remain sealed pending the defective / multi-answer policy.

## Not done in this step

- No `answer` modification.
- No `choices` / question text / metadata modification.
- No `solution_svg` modification.
- No modification of the 2 no-op items.
- No C20-2 / C20-3 / C20-4 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
