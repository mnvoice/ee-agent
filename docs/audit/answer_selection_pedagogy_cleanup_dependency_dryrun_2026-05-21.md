# Answer-Selection Pedagogy — Cleanup-Dependency CL-1 Dry-run (2026-05-21)

CL-1 of the cleanup-dependency batch: the `choices` / `text` cleanup dry-run.
For each of the 7 items it records the current stored value, the source
basis (mathpix OCR of the source PDF), the proposed corrected value, the
answer impact, the pedagogy `보기 판단` mapping impact, and the apply risk.

This is a **dry-run document only**. It does NOT modify `app/data`. No
`choices` / `text` is corrected here; no pedagogy `solution` / `steps` is
applied.

- Base commit: `6772786`
- Batch design: `docs/audit/answer_selection_pedagogy_cleanup_dependency_batch_design_2026-05-21.md`
- Source material: `data/mathpix_기출_{2015_1회,2015_2회,2015_3회,2002_3회,2016_1회,2006_1회}.json`
- Current `choices`/`text` read directly from `app/data/questions.json` (commit `6772786`)

## Cleanup-type legend

- Type R — residue deletion (choice/text sentence intact; trailing junk removed)
- Type L — LaTeX artifact fix
- Type W — word-level change (a content word substituted/removed)
- Type S — stem `text` fix (the question stem — the most sensitive surface)

---

## Item 1 — `2015_2회_29` choice [4] · Type R

- 현재 값: `아모 로드(Armour rod) : 전선의 진동에 의한 전선의 단선 방지\n[답] 15년도 2회\n439\n전기기사 펄기 D－60 시리즈`
- source 근거: 2015_2회 mathpix, 풀이 (4): `아모 로드(Armour rod) : 전선의 진동에 의한 전선의 단선 방지` — followed by `[답]` then the page footer `15년도 2회 / 439 / 전기기사 펄기 D－60 시리즈` then `문제 30`. The footer is page residue, not part of the choice.
- 제안 값: `아모 로드(Armour rod) : 전선의 진동에 의한 전선의 단선 방지` (delete the trailing `\n[답] 15년도 2회\n439\n전기기사 펄기 D－60 시리즈`)
- answer/정답 영향: none. `answer`=2; choice [4] is a non-answer choice and only trailing residue is removed.
- pedagogy 보기 판단 매핑 영향: none. The solution's `보기 판단` [4] ("아모 로드는 전선 진동에 의한 단선을 막는 보강재") maps to the cleaned sentence.
- apply risk: low.
- **Observation (out of scope for this cleanup):** the source's *question*
  choices for 문제 29 are bare device names (`(1) 리액터 / (2) 피뢰기 /
  (3) 아킹 호온 / (4) 아모 로드`). The `app/data` `choices` array instead
  holds the *풀이* lines (`설비 : 기능` format). This is a pre-existing
  structural choice — the pedagogy `solution` was written for the `설비:기능`
  format and is consistent with it. The Type R fix keeps that format; whether
  the `choices` should be re-sourced to the bare question choices is a
  separate data-quality question, NOT part of this OCR cleanup.

## Item 2 — `2002_3회_4` choice [4] · Type R

- 현재 값: `\(U=\frac{1}{4 \pi \epsilon} \iint \frac{\rho_{s}}{r} d s\) 2-286\nD-60 전기기사`
- source 근거: 2002_3회 mathpix, 문제 04 choice (4): `\(U=\frac{1}{4 \pi \epsilon} \iint \frac{\rho_{s}}{r} d s\)` — followed by the page footer `2-286 / D-60 전기기사` then `풀이`. Footer is page residue.
- 제안 값: `\(U=\frac{1}{4 \pi \epsilon} \iint \frac{\rho_{s}}{r} d s\)` (delete the trailing ` 2-286\nD-60 전기기사`)
- answer/정답 영향: none. `answer`=4 — choice [4] is the answer choice, but only trailing residue is removed; the formula is byte-identical to the source.
- pedagogy 보기 판단 매핑 영향: none. `보기 판단` [4] ("U=(1/4πε)∬ρs/r dS") maps to the cleaned formula.
- apply risk: low.

## Item 3 — `2016_1회_71` choice [4] · Type L

- 현재 값: `\(E_l = ` + `<FF>` + `rac{1}{\sqrt{3}}E_p\)` — the choice contains a literal form-feed control character (U+000C) followed by `rac`; i.e. the `\f` of `\frac` was corrupted into a form-feed byte.
- source 근거: 2016_1회 mathpix, 문제 71 choice (4): `\(E_{l}=\frac{1}{\sqrt{3}} E_{p}\)`. The intended command is `\frac`.
- 제안 값: `\(E_l = \frac{1}{\sqrt{3}}E_p\)` (replace the form-feed + `rac` with `\frac`; the surrounding `E_l`/`E_p` style is left as the app/data's existing convention, matching choices [1]-[3])
- answer/정답 영향: none. `answer`=3; choice [4] is a non-answer choice.
- pedagogy 보기 판단 매핑 영향: none. `보기 판단` [4] ("1/√3배는 Y 관계의 역수") maps to `\frac{1}{\sqrt{3}}`.
- apply risk: low. (Also removes a control character from the data — a hygiene improvement.)

## Item 4 — `2015_1회_22` choice [2] · Type W

- 현재 값: `전압변동을 직접 한다.`
- source 근거: 2015_1회 mathpix, 문제 22 choice (2): `전압변동을 적게 한다.` — and the 풀이 lists "전압 변동률을 적게 한다" as an 안정도 향상 대책. `직접` is an OCR misread of `적게`.
- 제안 값: `전압변동을 적게 한다.`
- answer/정답 영향: none. `answer`=1; choice [2] is a non-answer choice.
- pedagogy 보기 판단 매핑 영향: none / improves. `보기 판단` [2] ("전압 변동을 줄이면 운전점이 안정 → 향상책") describes the evident meaning; the corrected choice "적게 한다" matches it directly.
- apply risk: low — source-confirmed word substitution.

## Item 5 — `2015_3회_27` choice [4] · Type W

- 현재 값: `고장전류를 줄이고 고속도 자단방식을 채용한다.`
- source 근거: 2015_3회 mathpix, 문제 27 choice (4): `고장전류를 줄이고 고속도 차단방식을 채용한다.` `자단` is an OCR misread of `차단`.
- 제안 값: `고장전류를 줄이고 고속도 차단방식을 채용한다.`
- answer/정답 영향: none. `answer`=3; choice [4] is a non-answer choice.
- pedagogy 보기 판단 매핑 영향: none. `보기 판단` [4] ("고장전류 저감·고속 차단은 증진") maps to the corrected choice.
- apply risk: low — source-confirmed word substitution.

## Item 6 — `2016_1회_44` choices [2] and [3] · Type W

- 현재 값: [2] `발전기의 굽은 회전방향으로 기하학적 중성축이 형성된다.` / [3] `전동기의 굽은 회전방향과 반대방향으로 기하학적 중성축이 형성된다.`
- source 근거: 2016_1회 mathpix, 문제 44 choices: (2) `발전기의 경우 회전방향으로 기하학적 중성축이 형성된다.` / (3) `전동기의 경우 회전방향과 반대방향으로 기하학적 중성축이 형성된다.` `굽은` is an OCR misread of `경우` — **not** a spurious word (the batch design assumed a deletion; the source shows a substitution).
- 제안 값: [2] `발전기의 경우 회전방향으로 기하학적 중성축이 형성된다.` / [3] `전동기의 경우 회전방향과 반대방향으로 기하학적 중성축이 형성된다.`
- answer/정답 영향: none. `answer`=4; choices [2]/[3] are non-answer choices.
- pedagogy 보기 판단 매핑 영향: none. `보기 판단` describes "[2] 발전기는 회전 방향으로, [3] 전동기는 그 반대 방향으로 중성축 이동" — consistent with the corrected choices.
- apply risk: low — source-confirmed word substitution (`굽은` → `경우`, both [2] and [3]).

## Item 7 — `2006_1회_7` `text` (z-component) · Type S

- 현재 값: `…+k 3 Z e^{\overline{4 z}}\)` (within the question `text`)
- source 근거: 2006_1회 mathpix — the source PDF's **text region** OCR for 문제 07 carries the *same* artifact: `+k 3 Z e^{\overline{4 z}}`. However, the source PDF's **풀이 region** OCR computes the z-component cleanly: `\frac{\partial}{\partial z}\left(3 z e^{4 z}\right)` and `3\left(e^{4 z}+4 z e^{4 z}\right)`. Answer consistency also requires it — `div E` at the origin = 3 only if the z-component is `3z·e^{4z}` (`answer`=2, value 3).
- 제안 값: z-component `k 3 Z e^{\overline{4 z}}` → `k 3 z e^{4 z}` (capital `Z`→`z`, remove the spurious `\overline`)
- answer/정답 영향: none. `answer`=2 (value 3); the correction does not change the computed divergence — it makes the stem consistent with the verified answer.
- pedagogy 보기 판단 매핑 영향: none / improves. The pedagogy `근거/계산` already writes `∂(3z·e^{4z})/∂z`; correcting the stem makes the displayed `text` match the solution.
- apply risk: **medium** — Type S (question-stem modification). Unlike items
  1-6, the source PDF's text region is NOT clean: it carries the same
  artifact as `app/data`, so the correction makes the stem *deviate from the
  literal source text region* toward the source 풀이 region's clean form.
  The deviation is well-justified (source 풀이 + answer consistency + the
  pedagogy solution already uses the clean form), but a stem change on a
  judgment basis warrants supervisor review before apply.

---

## Summary

| # | key | field | type | proposed correction | answer impact | pedagogy impact | risk | classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `2015_2회_29` | choice [4] | R | delete trailing footer residue | none | none | low | pass |
| 2 | `2002_3회_4` | choice [4] | R | delete trailing footer residue | none | none | low | pass |
| 3 | `2016_1회_71` | choice [4] | L | form-feed+`rac` → `\frac` | none | none | low | pass |
| 4 | `2015_1회_22` | choice [2] | W | `직접` → `적게` | none | none/improves | low | pass |
| 5 | `2015_3회_27` | choice [4] | W | `자단` → `차단` | none | none | low | pass |
| 6 | `2016_1회_44` | choices [2],[3] | W | `굽은` → `경우` | none | none | low | pass |
| 7 | `2006_1회_7` | `text` | S | `3 Z e^{\overline{4 z}}` → `3 z e^{4 z}` | none | none/improves | medium | needs-review |

Classification tally: **pass 6**, **needs-review 1** (`2006_1회_7`),
**hold-DQ 0**.

- All 7 corrections are source-grounded; none changes any `answer`; none
  harms a pedagogy `보기 판단` mapping (items 4 and 7 improve consistency).
- Items 1-6 (pass) make `app/data` *match* the source — straightforward
  cleanup. Per the batch design they map to CL-3a (R+L: items 1, 2, 3) and
  CL-3b (W: items 4, 5, 6).
- Item 7 (`2006_1회_7`, needs-review) is the CL-3c step (Type S, `text`).
  The correction is well-justified but deviates from the source text
  region's literal OCR; a supervisor decision is needed — (a) correct the
  stem to `3 z e^{4 z}`, or (b) leave the stem as-is (the pedagogy solution
  already explains the z-component correctly). Recommendation: (a) — the
  source 풀이, the answer, and the pedagogy solution all agree on
  `3z·e^{4z}`.
- Two batch-design assumptions are corrected by this source comparison:
  `2016_1회_44`'s `굽은` is a substitution (`→경우`), not a deletion; and the
  `2016_1회_71` choice [4] defect is a form-feed control character, not a
  plain missing backslash.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `choices` / `text` correction applied.
- No pedagogy `solution` / `steps` apply.
- No `answer` modification.
- No `2001_3회_43` change (out of scope — `hold-source`).
- No commit; no push; no local server; no paid API call.

## Status

- CL-1 cleanup dry-run complete: 7 items compared against the mathpix source,
  correction candidates drafted with per-item source basis, answer impact,
  pedagogy mapping impact, and apply risk.
- Classification: pass 6, needs-review 1 (`2006_1회_7`, Type S), hold-DQ 0.
- Next (separate approval): CL-2 review of this dry-run, then CL-3a/CL-3b
  (pass items) and a supervisor decision on CL-3c (`2006_1회_7`).
