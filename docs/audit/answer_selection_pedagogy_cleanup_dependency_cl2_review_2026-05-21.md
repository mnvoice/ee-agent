# Answer-Selection Pedagogy — Cleanup-Dependency CL-2 Review (2026-05-21)

CL-2 of the cleanup-dependency batch: review of the CL-1 cleanup dry-run. It
re-confirms the 6 `pass` corrections against the source, checks the answer
and pedagogy invariants, and rules separately on `2006_1회_7`.

This is a **read-only review document**. It does NOT modify `app/data`. No
`choices` / `text` is corrected; no pedagogy `solution` / `steps` is applied.

- Base commit: `6772786`
- Reviewed: `docs/audit/answer_selection_pedagogy_cleanup_dependency_dryrun_2026-05-21.md` (CL-1)
- Batch design: `docs/audit/answer_selection_pedagogy_cleanup_dependency_batch_design_2026-05-21.md`
- Source: `data/mathpix_기출_*.json`; current values from `app/data/questions.json` (`6772786`)

## 0. Review independence note

CL-1 and this CL-2 were produced by the same instance (not a separated
builder/auditor). The independent re-checks performed: a mechanical
re-verification script that (a) re-extracts the source mathpix text and
confirms it contains the proposed corrected content, (b) confirms each
proposed value carries no residue marker and no control character, (c)
confirms the corrections edit `choices`/`text` strings only and never the
`answer` field. Those checks are code-based, not assertions.

## 1. pass 6 — source re-confirmation

Re-verified by script (re-extract source, compare):

| key | choice | correction | source contains proposed content | residue markers in proposed | control chars in proposed |
| --- | --- | --- | --- | --- | --- |
| `2015_2회_29` | [4] | delete trailing footer residue | YES | none | none |
| `2002_3회_4` | [4] | delete trailing footer residue | YES | none | none |
| `2016_1회_71` | [4] | form-feed(U+000C)+`rac` → `\frac` | YES | none | none (was `0x0c`) |
| `2015_1회_22` | [2] | `직접` → `적게` | YES | none | none |
| `2015_3회_27` | [4] | `자단` → `차단` | YES | none | none |
| `2016_1회_44` | [2] | `굽은` → `경우` | YES | none | none |
| `2016_1회_44` | [3] | `굽은` → `경우` | YES | none | none |

- Every proposed corrected value's content is present verbatim in the
  source mathpix — the corrections are source-confirmed.
- All residue markers (`[답]`, `2-286`, `D-60`, `시리즈`) are absent from the
  proposed values — the residue is fully removed for the two Type R items.
- `2016_1회_71` choice [4] currently carries a `U+000C` form-feed control
  character; the proposed value removes it (also a data-hygiene fix).

Precision note on "matches source exactly": the corrections are defect-only
edits. For `2016_1회_71` and `2016_1회_44` the proposed string fixes the
defect but preserves `app/data`'s existing local convention for the
unchanged parts — `E_l`/`E_p` subscript style (consistent with the same
item's choices [1]-[3]) and ASCII punctuation — which differs from the
source mathpix's `E_{l}` / fullwidth punctuation. This is intentional: the
cleanup fixes the OCR defect and does NOT re-transcribe punctuation/symbol
style (a wholesale reformat would be scope creep and would make the choice
inconsistent with its siblings). The corrected *content* matches source; the
*style* of unchanged segments stays as `app/data` had it.

## 2. answer unchanged

The 6 corrections edit `choices` strings only (`2006_1회_7` would edit
`text`; it is held — Section 4). None writes the `answer` field. Confirmed
`answer` values, unchanged by any correction:

`2015_2회_29`=2, `2002_3회_4`=4, `2016_1회_71`=3, `2015_1회_22`=1,
`2015_3회_27`=3, `2016_1회_44`=4.

Note `2002_3회_4` choice [4] *is* the answer choice (`answer`=4) — but the
correction removes only trailing page-footer residue; the formula
`\(U=\frac{1}{4πε}\iint\frac{ρs}{r}ds\)` is byte-identical before and after,
so the answer choice's meaning is untouched.

## 3. pedagogy `보기 판단` — no conflict

Each item's applied-batch pedagogy `solution` `보기 판단` was checked against
the proposed corrected choice:

| key | `보기 판단` reference | corrected choice | consistent |
| --- | --- | --- | --- |
| `2015_2회_29` | [4] 아모 로드 = 진동 단선 방지 보강재 | 아모 로드(Armour rod) : 전선의 진동에 의한 전선의 단선 방지 | YES |
| `2002_3회_4` | [4] U=(1/4πε)∬ρs/r dS | `\(U=\frac{1}{4πε}\iint\frac{ρs}{r}ds\)` | YES |
| `2016_1회_71` | [4] 1/√3배 = Y 관계의 역수 | `\frac{1}{\sqrt{3}}` (= 1/√3) | YES |
| `2015_1회_22` | [2] 전압 변동을 줄이면 → 향상책 | 전압변동을 적게 한다 | YES (improves) |
| `2015_3회_27` | [4] 고장전류 저감·고속 차단 → 증진 | …고속도 차단방식… | YES |
| `2016_1회_44` | [2]/[3] 발전기/전동기 중성축 이동 | 발전기의 경우 …/전동기의 경우 … | YES |

No correction conflicts with a pedagogy `보기 판단`; `2015_1회_22` and
`2006_1회_7` (held) improve the text↔solution consistency. The 6 corrections
do not alter any answer-relevant reasoning.

## 4. `2006_1회_7` — separate ruling

`2006_1회_7` (Type S, question `text` z-component
`3 Z e^{\overline{4 z}}` → `3 z e^{4 z}`) is ruled **`hold-Type-S`**, not
`hold-DQ`.

Rationale:

- It is NOT a defective question — it has a single valid, source-verified
  answer (`answer`=2, div E = 3). `hold-DQ` is reserved for genuine question
  defects (multi-answer / 전항정답, e.g. the `2014_2회_50` class). Classifying
  a sound question as `hold-DQ` would mislabel it.
- The issue is a stem-`text` OCR artifact whose correction rests on the
  source 풀이 region + answer consistency, not on the source `text` region
  (which carries the same artifact). That is a Type S correction-review
  matter — exactly the `hold-Type-S` bucket.
- Per the supervisor instruction it is excluded from the CL-3a/CL-3b pass
  cleanup and not mixed in.

Recommendation for the separate Type S review: correct the stem to
`3 z e^{4 z}` — the source 풀이 (`∂/∂z(3z·e^{4z})`), the verified answer, and
the already-applied pedagogy `근거/계산` all agree on `3z·e^{4z}`. Apply risk:
medium (stem modification on a 풀이/answer basis). This is the CL-3c step.

## 5. CL-2 classification

| bucket | count | items |
| --- | ---: | --- |
| pass-apply-ready | 6 | `2015_2회_29` [4], `2002_3회_4` [4], `2016_1회_71` [4], `2015_1회_22` [2], `2015_3회_27` [4], `2016_1회_44` [2]+[3] |
| hold-Type-S | 1 | `2006_1회_7` `text` |
| hold-DQ | 0 | — |

Per-correction apply risk:

| key / choice | type | apply risk | note |
| --- | --- | --- | --- |
| `2015_2회_29` [4] | R | low | residue deletion; content & answer untouched |
| `2002_3회_4` [4] | R | low | residue deletion; answer choice formula byte-identical |
| `2016_1회_71` [4] | L | low | `\frac` fix + removes a U+000C control char |
| `2015_1회_22` [2] | W | low | single-word substitution, source-confirmed |
| `2015_3회_27` [4] | W | low | single-word substitution, source-confirmed |
| `2016_1회_44` [2],[3] | W | low | single-word substitution ×2, source-confirmed |
| `2006_1회_7` `text` | S | medium | held — Section 4; CL-3c separate review |

All 6 `pass-apply-ready` corrections are source-confirmed, answer-invariant,
pedagogy-consistent, and low apply risk. They map to the batch design's
CL-3a (R+L: `2015_2회_29`, `2002_3회_4`, `2016_1회_71`) and CL-3b (W:
`2015_1회_22`, `2015_3회_27`, `2016_1회_44`).

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `choices` / `text` correction applied.
- No pedagogy `solution` / `steps` apply.
- No `answer` modification.
- No commit; no push.

## Status

- CL-2 review complete. 6 corrections re-confirmed against source (script
  re-verification), answer-invariant, pedagogy-consistent.
- Classification: pass-apply-ready 6, hold-Type-S 1 (`2006_1회_7`), hold-DQ 0.
- Next (separate approval): CL-3a (`2015_2회_29`, `2002_3회_4`,
  `2016_1회_71`) and CL-3b (`2015_1회_22`, `2015_3회_27`, `2016_1회_44`) —
  the choices cleanup apply; and a separate Type S correction review for
  `2006_1회_7` (CL-3c).
