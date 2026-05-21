# Answer-Selection Pedagogy Pilot — Apply Result (2026-05-21)

Apply-result log for the answer-selection pedagogy pilot. The `solution` /
`steps` of the 7 pilot items were replaced with the pedagogy drafts from the
pilot dry-run, in both `app/data/questions.json` and
`app/data/questions.v2.json`.

This is an apply-result record. No `answer`, `choices`, question text,
metadata, or `solution_svg` was modified.

- Base commits: `0ff1f31` (pedagogy track design), `4d0262d` (pilot dry-run),
  `35f422e` (pilot choice cleanup)
- Pilot dry-run: `docs/audit/answer_selection_pedagogy_pilot_dryrun_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Applied items (7)

| key | subject | answer | source provenance |
| --- | --- | ---: | --- |
| `2007_1회_9` | 전기자기학 | 2 | C20-2 corrected |
| `2007_2회_64` | 회로이론 | 1 | C20-2 corrected |
| `2001_3회_41` | 전기기기 | 4 | C20-1 corrected; choices cleaned `35f422e` |
| `2006_2회_27` | 전력공학 | 4 | C20-2 corrected; choices cleaned `35f422e` |
| `2016_1회_70` | 제어공학 | 4 | C20-4 corrected |
| `2016_3회_21` | 전력공학 | 4 | C20-4 corrected; choices cleaned `35f422e` |
| `2015_3회_22` | 전력공학 | 1 | C20-3 corrected; choices cleaned `35f422e` |

For each item, `solution` was replaced with the pedagogy markdown (8
elements; `2006_2회_27` has 7 — the 다른 과목 연결 element was omitted as
the dry-run found no genuinely strong cross-subject link), and `steps` was
replaced with the `인식` / `변환` / `계산` draft.

## Choice-mapping recheck (the 4 cleaned items)

Before apply, the per-choice text in the drafts was rechecked against the
`choices` cleaned in `35f422e`:

- `2001_3회_41` choice [3] now `온도가 상승한다.` — draft says "[3] 온도는
  손실 증가로 상승". Consistent.
- `2006_2회_27` choices [2]/[3] now `홍수위…` / `모래를 배제하기…` — draft
  says "[2] 홍수위 조절은 방수로의 역할" / "[3] 모래 배제는 침사지…".
  Consistent.
- `2016_3회_21` choice [4] now `전압의 제곱에 반비례한다．` (residue
  removed) — draft references it. Consistent.
- `2015_3회_22` choice [4] now `전력용 콘덴서를 설치한다.` (residue
  removed) — draft says "[4] 전력용 콘덴서: 역률 개선용". Consistent.

All per-choice explanations map to the current (cleaned) `choices`.

## Correction during apply — `2016_3회_21` steps typo

The dry-run draft of `2016_3회_21` `steps.변환` contained a typo:
`A=ρl/A 관계에서` (the letter A on both sides — not a valid relation). The
standard resistance formula is `R=ρl/A`, and the same item's `solution`
body correctly uses `A = ρl/R`. Applying the typo verbatim would violate the
quality gate ("no contradiction"). The applied `steps.변환` therefore uses
`A=ρl/R 관계에서` — consistent with the `solution` body and the standard
formula. This is the only deviation from the dry-run text, and it corrects a
draft typo rather than introducing new content.

## Changed files / fields

- `app/data/questions.json` — `solution` / `steps` of 7 items replaced.
- `app/data/questions.v2.json` — `solution` / `steps` of 7 items replaced.
- Changed fields: `solution`, `steps`.

## Unchanged

- `answer` — `2007_1회_9`=2, `2007_2회_64`=1, `2001_3회_41`=4,
  `2006_2회_27`=4, `2016_1회_70`=4, `2016_3회_21`=4, `2015_3회_22`=1.
- `choices` (all 7 items).
- question `text`.
- metadata (`subject`, `q_no`, `q_type`, `difficulty`, `quality`, `tag`,
  `year`, `session`, `*_source`).
- `solution_svg`.

## Quality checks

For all 7 items:

- answer matches q.answer: YES.
- every choice explanation maps to the current `choices`: YES (rechecked
  above for the 4 cleaned items; the other 3 had intact choices).
- no invented source / article / statute: YES (no statute numbers; standard
  theory only — the pilot deliberately excluded 전기설비기술기준 items).
- no unsupported cross-subject claim: YES (cross-subject elements only where
  genuinely standard — 회로↔제어 Hurwitz, Nyquist↔Bode, 전력↔기기 변압기
  결선; `2006_2회_27` omits the element).
- no contradiction with the source answer: YES.
- concise enough for UI: YES (each element a short paragraph).

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` / `questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- Exactly 7 items changed in each file; each change confined to
  `solution` / `steps`.
- All 7: `answer` unchanged; `choices` unchanged; non-`solution`/`steps`
  fields unchanged.
- `steps` keys remain `['인식', '변환', '계산']` for all 7.
- `solution` of all 7 ends with a `최종 정답` element.
- `2016_3회_21` `steps.변환` uses `A=ρl/R` (the typo `A=ρl/A` is absent).
- No other record changed.
- `git diff --check` — no whitespace errors. Serialization preserved.

## Final status

`pedagogy_pilot_applied`

The 7 pilot items now carry the answer-selection pedagogy `solution` /
`steps`. `answer` and `choices` are unchanged and source-clean.

## Follow-up

- Pilot review after a browser / reading inspection — confirm the pedagogy
  solution renders well in the app UI and reads clearly.
- Template refinement based on that review (which elements help, the right
  length) before expanding to a larger batch.
- No bulk apply — expansion stays small-batch with dry-run → review →
  limited apply → closeout.

## Not done in this step

- No `answer` modification.
- No `choices` modification.
- No question text / metadata modification.
- No `solution_svg` modification.
- No modification of any other record.
- No paid API call.
- No push.
