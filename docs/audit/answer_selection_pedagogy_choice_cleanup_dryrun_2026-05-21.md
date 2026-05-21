# Answer-Selection Pedagogy — Pilot Choice Cleanup Dry-run (2026-05-21)

Choice-cleanup dry-run for the 4 pilot items whose `choices` carry minor OCR
residue / typos (surfaced in the pedagogy pilot dry-run `4d0262d`). It
records, per item, the source-correct choice text read from the source PDF
and judges whether the item is ready for a choices-only apply.

This is a **dry-run document only**. It does NOT modify `app/data`, does NOT
modify `choices`, and is not an approval to apply.

- Base commit: `4d0262d` (docs: draft answer selection pedagogy pilot)
- Pilot dry-run: `docs/audit/answer_selection_pedagogy_pilot_dryrun_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Cleanup verdict definition

- `ready_for_choices_only_apply` — the source-correct choice text was read
  with confidence from the source PDF; the item is ready for a choices-only
  apply.
- `needs_source_check` — the source could not be confirmed; a further check
  is required.
- `defer` — the source is ambiguous; hold.

## Method

- Two items (`2001_3회_41`, `2015_3회_22`) were confirmed from source PDF
  reads already performed earlier this session.
- Two items (`2016_3회_21`, `2006_2회_27`) were confirmed from a direct
  read of the source PDF in this step.
- Choice text is transcribed from the source PDF, not reconstructed from
  theory. The damage in all 4 cases is a minor OCR typo or trailing residue;
  the answer-relevant content was already legible.

## Item 1 — `2001_3회_41`

- key: `2001_3회_41`
- current_answer: 4
- current choices snapshot (DB):
  - [1] `동손이 증가한다.`
  - [2] `여자 전류는 변함없다.`
  - [3] `운도가 상승한다.`
  - [4] `철손이 증가한다.`
- suspected OCR issue: choice [3] `운도` should be `온도`.
- source PDF / page: `data/문제_2001_3회_20260316.pdf`, 문제 41, "3과목
  전기기기" section (book page 2-317 area).
- proposed source-correct choice text:
  - [1] `동손이 증가한다.` (unchanged)
  - [2] `여자 전류는 변함없다.` (unchanged)
  - [3] `온도가 상승한다.` ← corrected from `운도가 상승한다.`
  - [4] `철손이 증가한다.` (unchanged)
- evidence note: the source PDF prints "③ 온도가 상승한다." plainly.
  Choices [1]/[2]/[4] match the DB; only [3] carries the 운→온 typo.
- cleanup verdict: `ready_for_choices_only_apply` (only [3] changes).
- risk note: low. Single-character typo fix; meaning unchanged; `answer` (4)
  unaffected.

## Item 2 — `2006_2회_27`

- key: `2006_2회_27`
- current_answer: 4
- current choices snapshot (DB):
  - [1] `낙차를 높이기 위하여`
  - [2] `충수위를 낮추기 위하여`
  - [3] `모래를 베제하기 위하여`
  - [4] `유량을 조정하기 위하여`
- suspected OCR issue: choice [2] `충수위` should be `홍수위`; choice [3]
  `베제` should be `배제`.
- source PDF / page: `data/문제_2006_2회_20260316.pdf`, 문제 27, PDF p.5
  (book page 2-170).
- proposed source-correct choice text:
  - [1] `낙차를 높이기 위하여` (unchanged)
  - [2] `홍수위를 낮추기 위하여` ← corrected from `충수위를 낮추기 위하여`
  - [3] `모래를 배제하기 위하여` ← corrected from `모래를 베제하기 위하여`
  - [4] `유량을 조정하기 위하여` (unchanged)
- evidence note: the source PDF prints "② 홍수위를 낮추기 위하여" and
  "③ 모래를 배제하기 위하여" plainly. Choices [1]/[4] match the DB.
- cleanup verdict: `ready_for_choices_only_apply` (only [2] and [3] change).
- risk note: low. Two single-character typo fixes; meaning unchanged;
  `answer` (4) unaffected.

## Item 3 — `2016_3회_21`

- key: `2016_3회_21`
- current_answer: 4
- current choices snapshot (DB):
  - [1] `전류에 비례한다．`
  - [2] `전류에 반비례한다．`
  - [3] `전압의 제곱에 비례한다．`
  - [4] `전압의 제곱에 반비례한다． \begin{table}\captionsetup{labelformat=empty}\caption{`
- suspected OCR issue: choice [4] carries trailing LaTeX residue after the
  sentence.
- source PDF / page: `data/문제_2016_3회_20260316.pdf`, 문제 21, PDF p.7
  (book page 2-169).
- proposed source-correct choice text:
  - [1] `전류에 비례한다．` (unchanged)
  - [2] `전류에 반비례한다．` (unchanged)
  - [3] `전압의 제곱에 비례한다．` (unchanged)
  - [4] `전압의 제곱에 반비례한다．` ← trailing LaTeX residue removed
- evidence note: the source PDF prints "④ 전압의 제곱에 반비례한다." plainly,
  with no table markup. The proposed [4] keeps the fullwidth period "．" to
  match the sibling choices [1]-[3]. Choices [1]-[3] match the DB.
- cleanup verdict: `ready_for_choices_only_apply` (only [4] changes —
  residue removal).
- risk note: low. Trailing-residue removal only; the choice sentence itself
  is intact; `answer` (4) unaffected.

## Item 4 — `2015_3회_22`

- key: `2015_3회_22`
- current_answer: 1
- current choices snapshot (DB):
  - [1] `변압기를 \(\triangle\) 결선한다.`
  - [2] `동기조상기를 설치한다.`
  - [3] `직렬 리액터를 설치한다.`
  - [4] `전력용 콘덴서를 설치한다. D-60 전기기사`
- suspected OCR issue: choice [4] carries trailing page-footer residue
  (`D-60 전기기사`).
- source PDF / page: `data/문제 _2015_3회_20260316.pdf` (note the space
  after `문제`), 문제 22, PDF p.9 area (read earlier this session).
- proposed source-correct choice text:
  - [1] `변압기를 \(\triangle\) 결선한다.` (unchanged — `\(\triangle\)` is a
    LaTeX rendering of the △ symbol, not OCR damage)
  - [2] `동기조상기를 설치한다.` (unchanged)
  - [3] `직렬 리액터를 설치한다.` (unchanged)
  - [4] `전력용 콘덴서를 설치한다.` ← trailing footer residue `D-60 전기기사`
    removed
- evidence note: the source PDF prints "④ 전력용 콘덴서를 설치한다." plainly;
  "D-60 전기기사" is the running page footer, not part of the choice.
  Choices [1]-[3] match the DB ([1] uses `\(\triangle\)` for △ — kept as-is).
- cleanup verdict: `ready_for_choices_only_apply` (only [4] changes —
  residue removal).
- risk note: low. Trailing-residue removal only; the choice sentence itself
  is intact; `answer` (1) unaffected.

## Overall recommendation

| key | cleanup verdict | choices to change |
| --- | --- | --- |
| `2001_3회_41` | `ready_for_choices_only_apply` | [3] only |
| `2006_2회_27` | `ready_for_choices_only_apply` | [2], [3] |
| `2016_3회_21` | `ready_for_choices_only_apply` | [4] only |
| `2015_3회_22` | `ready_for_choices_only_apply` | [4] only |

- 4 / 4 `ready_for_choices_only_apply`. No item routed to
  `needs_source_check` or `defer`.
- All four are minor fixes (single-character typos or trailing-residue
  removal); each was confirmed against the source PDF.
- Proposed next step (separate approval): a choices-only apply for the 4
  items — replace ONLY the listed damaged choices, leaving `answer`,
  `solution`, `steps`, question text, metadata, and `solution_svg`
  unchanged. Then the pedagogy `solution` apply can proceed on clean
  `choices`.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `choices` apply.
- No `answer` modification.
- No `solution` / `steps` modification.
- No `solution_svg` modification.
- No app code or schema modification.
- No paid API call.
- No push.

## Status

- Choice-cleanup dry-run complete. 4 / 4 `ready_for_choices_only_apply`.
- No `app/data` modification.
- Next (separate approval): a choices-only apply for the 4 items, then the
  pedagogy `solution` / `steps` apply.
