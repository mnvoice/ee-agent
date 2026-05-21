# Answer-Selection Pedagogy — Pilot Choice Cleanup Apply Result (2026-05-21)

Apply-result log for the pedagogy pilot choice cleanup. The `choices` field
of the 4 pilot items with minor OCR residue / typos was corrected to the
source PDF text, in both `app/data/questions.json` and
`app/data/questions.v2.json`. Only the damaged choices were changed.

This is an apply-result record. No `answer`, `solution`, `steps`, question
text, metadata, or `solution_svg` was modified.

- Base commit: `9d14e94` (docs: draft pedagogy pilot choice cleanup)
- Cleanup dry-run: `docs/audit/answer_selection_pedagogy_choice_cleanup_dryrun_2026-05-21.md`
- Pilot dry-run: `docs/audit/answer_selection_pedagogy_pilot_dryrun_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Applied items (4)

### `2001_3회_41` (answer 4)

- choice [3]: `운도가 상승한다.` → `온도가 상승한다.`
- Source evidence: `data/문제_2001_3회_20260316.pdf`, 문제 41 — the source
  PDF prints "③ 온도가 상승한다." plainly.

### `2006_2회_27` (answer 4)

- choice [2]: `충수위를 낮추기 위하여` → `홍수위를 낮추기 위하여`
- choice [3]: `모래를 베제하기 위하여` → `모래를 배제하기 위하여`
- Source evidence: `data/문제_2006_2회_20260316.pdf`, 문제 27, PDF p.5 —
  the source PDF prints "② 홍수위를 낮추기 위하여" and "③ 모래를 배제하기
  위하여" plainly.

### `2016_3회_21` (answer 4)

- choice [4]: `전압의 제곱에 반비례한다． \begin{table}\captionsetup{labelformat=empty}\caption{`
  → `전압의 제곱에 반비례한다．` (trailing LaTeX/table residue removed)
- Source evidence: `data/문제_2016_3회_20260316.pdf`, 문제 21, PDF p.7 —
  the source PDF prints "④ 전압의 제곱에 반비례한다." with no table markup.
  The fullwidth period "．" is kept to match siblings [1]-[3].

### `2015_3회_22` (answer 1)

- choice [4]: `전력용 콘덴서를 설치한다. D-60 전기기사`
  → `전력용 콘덴서를 설치한다.` (trailing page-footer residue removed)
- Source evidence: `data/문제 _2015_3회_20260316.pdf`, 문제 22 — the source
  PDF prints "④ 전력용 콘덴서를 설치한다."; "D-60 전기기사" is the running
  page footer.

## Changed files

- `app/data/questions.json` — `choices` of 4 items updated.
- `app/data/questions.v2.json` — `choices` of 4 items updated.

## Changed field

- `choices` only. For each changed item the field-level diff is exactly
  `['choices']`. Within `choices`, only the damaged elements were replaced
  (`2001_3회_41` [3]; `2006_2회_27` [2] and [3]; `2016_3회_21` [4];
  `2015_3회_22` [4]); the other choices were left unchanged.

## Unchanged

- `answer` — `2001_3회_41`=4, `2006_2회_27`=4, `2016_3회_21`=4,
  `2015_3회_22`=1 (not modified).
- `solution`, `steps`.
- question `text`.
- metadata (`subject`, `q_no`, `q_type`, `difficulty`, `quality`, `tag`,
  `year`, `session`, `*_source`).
- `solution_svg`.

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- All 4 targets exist exactly once in both files.
- All 4 targets: `choices` == the source-corrected choices.
- All 4 targets: `answer` unchanged (4 / 4 / 4 / 1).
- Exactly 4 items changed in each file; each change is confined to
  `choices`.
- Edited items: all non-`choices` fields (`answer`, `solution`, `steps`,
  `text`, metadata, `solution_svg`) unchanged.
- No other record changed.
- `git diff --check` — no whitespace errors.
- Serialization preserved — diff confined to the changed choice strings; no
  mass reformatting.

## Final status

`pedagogy_pilot_choices_cleaned`

The 4 pilot items' `choices` are now clean of OCR residue / typos. With all
7 pilot items now on clean `choices`, `answer`, `solution`, and `steps`, the
pedagogy `solution` apply can proceed.

## Status

- Pedagogy pilot choice cleanup complete for the 4 items.
- The 7 pilot items (`2007_1회_9`, `2007_2회_64`, `2001_3회_41`,
  `2006_2회_27`, `2016_1회_70`, `2016_3회_21`, `2015_3회_22`) are now all
  source-clean.
- Q2 bulk apply remains BLOCKED.

## Not done in this step

- No `answer` modification.
- No `solution` / `steps` modification.
- No question text / metadata modification.
- No `solution_svg` modification.
- No modification of any other record.
- No paid API call.
- No push.
