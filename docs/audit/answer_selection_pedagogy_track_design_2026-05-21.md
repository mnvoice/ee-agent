# Answer-Selection Pedagogy Track — Design (2026-05-21)

Design for the answer-selection pedagogy track. The goal is to structure the
`solution` so a learner builds the skill of reasoning toward the answer from
the question — not just reading a stored answer key. Accuracy, source
safety, and verifiability come first.

This is a **design document only**. It does NOT modify `app/data`, does NOT
apply any `solution` / `steps`, and is not an approval to apply. This step
goes only as far as the design and the pilot candidate selection.

- Old-answer reflection: `3d06543`
  (`docs/audit/supervisor_reflection_old_answer_track_2026-05-21.md`)
- Old-answer final closeout: `b4a8dad`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## 1. Background

The old-answer verification / correction track established a source-verified
data base to build on:

- `source_answer_verified` and applied — 9 items.
- single-answer `source_answer_conflict` corrected (answer + solution
  cleanup) — 19 items.
- DQ defer — 2 items (`2014_2회_50`, `2014_3회_62`).
- choice-OCR recovery — 2 items (`2001_3회_43`, `2015_3회_25`).
- `solution_svg` consistency audit — `stale_svg` 0.
- Reflection recorded at `3d06543`.

With data integrity established, the goal is now to design a "reason-toward-
the-answer" solution on top of that verified data.

## 2. Core principles

- Only source-clean items are eligible for the pilot.
- Items whose `answer` / `choices` / source are uncertain are excluded.
- The LLM must NOT invent new facts, statute articles, or numeric values.
- Per-choice judgment MUST match the current stored `choices` exactly
  (the `2016_1회_44` lesson — reasoning was written against a generic list,
  not the actual choices).
- Statute / numeric questions are handled conservatively.
- Every change goes through a dry-run and supervisor review before apply.
- No bulk apply.

## 3. Proposed solution structure

Each pilot solution is designed to be able to carry these elements (concise,
not every element is mandatory for every item):

| element | purpose |
| --- | --- |
| 핵심 개념 | the single concept the question tests |
| 문제에서 봐야 할 단서 | the textual clue(s) in the stem that point to the concept |
| 보기 판단 / 오답 제거 | per-choice: why each wrong choice is wrong, why the answer is right |
| 정식 근거 또는 계산 | the formal derivation / computation, or the rule it rests on |
| 흔한 함정 | the common trap (the plausible-but-wrong reasoning) |
| 다른 과목 연결 | a cross-subject link, only when genuinely supported |
| 시험장 빠른 판별법 | how to discriminate under exam time pressure |
| 최종 정답 | the answer, stated explicitly, matching `q.answer` |

Constraint: the per-choice section MUST reference the actual stored
`choices`; the 다른 과목 연결 element is included only when it is genuinely
supported, never as a forced or invented link.

## 4. Fit with the current app/data structure

- `solution` is a markdown string; `steps` is a dict
  (`인식` / `변환` / `계산`). Both already exist on every item.
- Recommendation: hold the pedagogy elements (Section 3) in the existing
  `solution` markdown string, using short section headers. Keep the `steps`
  dict (`인식` / `변환` / `계산`) as the derivation skeleton — it already
  maps closely to 단서(인식) / 근거·계산(변환·계산).
- Do NOT add new schema fields for the pilot. The DQ-2 schema probe
  (`3894a38`) established that schema changes are sensitive and touch
  scattered app logic; a new field is out of scope for a pilot.
- UI / learning-flow concern: an over-long `solution` can hurt the learning
  flow. Each element should be concise (a few lines), so the whole solution
  stays scannable. If the pilot shows the markdown is too long for the UI,
  that is feedback for the expansion step — not a reason to add a field now.

## 5. Pilot selection criteria

An item is pilot-eligible only if all hold:

- `source_answer` verified or corrected (and closed).
- `choices` intact or recovered.
- Not a DQ / defer item.
- Not figure-dependent — the question stem must be answerable from text
  alone. (Items with a `solution_svg` are acceptable IF the SVG is only an
  illustrative derivation diagram and the stem is text-only; the SVG audit
  `10d8901` confirmed the audited SVGs are illustrative, not stem-required.)
- Statute-article items (전기설비기술기준) are LOW priority — high risk of
  article-number fabrication; deferred to a later statute-specific template.
- 5-10 items spanning several subjects.

## 6. Pilot candidates

7 candidates proposed, from the source-clean old-answer pool, spanning 5
subjects. All are `source_answer` corrected/closed; none is figure-dependent.

| key | subject | why safe | why pedagogically useful | risk | recommend |
| --- | --- | --- | --- | --- | --- |
| `2007_1회_9` | 전기자기학 | corrected (4→2), closed; stem is text-only; `solution_svg` is an illustrative vector diagram | clean concept (내적=0 ⇔ 수직); clear single clue ("수직"); cross-link to 제어공학 orthogonality | low | include |
| `2007_2회_64` | 회로이론 | corrected (2→1), closed; `steps.계산` was fixed in C20-3; stem text-only | Hurwitz determinant method; strong cross-subject link 회로이론↔제어공학 안정도 | low | include |
| `2001_3회_41` | 전기기기 | corrected (2→4), closed; no `solution_svg`; "옳지 않은 것" elimination question | concept 동손(부하손) vs 철손(무부하손); clean wrong-answer elimination | low | include |
| `2006_2회_27` | 전력공학 | corrected (3→4), closed; no `solution_svg`; pure 암기형; C20-2 removed a fabricated claim | strong wrong-answer-elimination teaching (제수문 vs 방수로 vs 모래제거기) | low | include |
| `2016_1회_70` | 제어공학 | corrected (2→4), closed; no `solution_svg`; analytic | Nyquist 임계점 ↔ Bode 변환; clear derivation (|−1|=1→0dB, ∠=±180°) | low | include |
| `2016_3회_21` | 전력공학 | corrected (1→4), closed; no `solution_svg` | multi-step derivation under "조건 일정" — good "reason toward the answer" item | low-medium | include |
| `2015_3회_22` | 전력공학 | corrected (4→1), closed; `solution_svg` is an illustrative △-connection diagram; stem text-only | 영상분 / △결선 3고조파 제거; cross-link to 전기기기 변압기 결선 | low | include |

Excluded / deferred from the pilot:

- `2005_3회_83`, `2015_1회_87` — 전기설비기술기준 (statute-article items);
  deferred to a statute-specific template (article-fabrication risk).
- `2001_3회_43`, `2015_3회_25` — `choices` were just recovered (`fac4b8d`);
  let the recovered data settle before using them in the pilot.
- `2016_1회_44` — `solution`/`steps` reasoning was just rewritten
  (`4fbc820`); let it settle.
- DQ-1 (`2014_2회_50`, `2014_3회_62`) — deferred, not source-clean.

Secondary pool (available if more breadth is wanted): the 9
`source_answer_verified` items, e.g. `2015_1회_13` (전기자기학, Poynting
vector), `2006_1회_7` (전기자기학, divergence) — verified provenance, usable
in a later batch.

## 7. Quality gate

### Dry-run stage (per item)

- The solution's stated answer matches `q.answer`.
- Every choice explanation maps to an actual stored choice.
- No invented source / article / statute number.
- No unsupported cross-subject claim.
- No contradiction with the source answer.
- Concise enough for the UI (each element a few lines; total scannable).

### Before apply

- Supervisor approval.
- Target-only diff (only the pilot items differ).
- `solution` / `steps` only — `answer` and `choices` unchanged.
- `git diff --check` clean; serialization preserved (no mass reformatting).

## 8. Expansion strategy

- pilot 7 items → review → a 20-item batch → subject-specific templates.
- Use the pilot feedback to refine the template (which elements help, which
  are noise, the right length).
- Statute / numeric / figure-bearing questions get separate templates
  (statute: article-citation discipline; numeric: derivation discipline;
  figure: figure-coordination).
- No bulk apply at any stage — small-batch, dry-run → review → limited
  apply → closeout.

## 9. Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `solution` / `steps` apply.
- No `answer` / `choices` modification.
- No app code or schema modification.
- No bulk prompt generation.
- No pilot solution draft (this step is design + candidate selection only).
- No paid API call.
- No push.

## 10. Status

- Design and pilot candidate selection complete: 7 candidates proposed.
- No `app/data` modification. No pilot solution drafted yet.
- Next step (separate approval): a pilot solution dry-run for the 7
  candidates, following dry-run → review → limited apply → closeout.
