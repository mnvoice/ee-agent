# Answer-Selection Pedagogy — Residual-2 Closeout Review (2026-05-21)

Closeout review of the 2 residual expansion items not yet applied:
`2006_1회_7` (`hold-Type-S`) and `2001_3회_43` (`hold-source`). It judges
whether each can be closed, without applying anything.

This is a **read-only review / decision document**. It does NOT modify
`app/data`. No `solution`/`steps` apply; no `text`/`choices`/`answer` change.

- Base commit: `8f6d4c6` (origin-synced; 23 pedagogy items applied so far)
- Inputs: `app/data/questions.json`; `data/mathpix_기출_{2006_1회,2001_3회}.json`;
  `docs/audit/answer_selection_pedagogy_cleanup_dependency_{dryrun,cl2_review}_2026-05-21.md`;
  `docs/audit/old_answer_manual_source_review_pack_2026-05-21.md`

---

## 1. `2006_1회_7` — Type S correction review

### Current `app/data` state

- `subject` 전기자기학, `q_type` 계산형, `answer` 2.
- `text`: `전계 \(E=i 2 e^{3 x} \sin 5 y-j e^{3 x} \cos 5 y+k 3 Z e^{\overline{4 z}}\) 일 때 … 발산은？`
- `choices`: [1] 0 / [2] 3 / [3] 6 / [4] 10.
- `solution`/`steps`: still the pre-pedagogy auto-generated version (the v2.1
  pedagogy draft exists in the expansion dry-run, item #8, but was held).

### Source re-check — text region vs 풀이 region

`data/mathpix_기출_2006_1회.json`, 문제 07:

- **text region** (the question stem OCR): `…+k 3 Z e^{\overline{4 z}}` —
  carries the **same artifact** as `app/data` (capital `Z`; a spurious
  `\overline` over the exponent). `app/data` faithfully copied this artifacted
  stem OCR.
- **풀이 region** (the solution OCR): explicitly writes
  `\frac{\partial}{\partial z}\left(3 z e^{4 z}\right)`, then
  `3\left(e^{4 z}+4 z e^{4 z}\right)`, then `3(1+4 z) e^{4 z}`, and concludes
  `점 (0,0,0) 대입 div E = 3`, `【답】(2)`.

So the source PDF's stem region is corrupted, but the **same PDF's 풀이
region** OCR unambiguously gives the intended z-component `3 z e^{4 z}`
(lowercase `z`, no overline).

### Is the `3 z e^{4 z}` restoration sufficiently justified?

YES — and on repo-internal evidence:

- The 풀이 region (repo-internal, `data/mathpix_기출_2006_1회.json`) restates
  the z-component as `3 z e^{4 z}` and computes `div E = 3`.
- The stored `answer` = 2, `choices[2]` = `3`; `div E` at the origin equals 3
  **only** if the z-component is `3z·e^{4z}`. `3 Z e^{\overline{4 z}}` as
  literally written is not evaluable / not valid notation — `\overline` over
  an exponent has no meaning here, and a capital `Z` where the coordinate
  `z` is needed is an OCR misread.
- This is not an external guess: the correct form is present in the source
  PDF's own solution box.

### Correction candidates

- (a) **`text` stem correction** — z-component `k 3 Z e^{\overline{4 z}}` →
  `k 3 z e^{4 z}` (capital `Z`→`z`, remove the spurious `\overline`; spacing
  kept in `app/data` style, consistent with the other components
  `i 2 e^{3 x}`, `j e^{3 x}`). `answer` and `choices` unchanged.
- (b) **pedagogy `solution`/`steps` apply** — the v2.1 draft (expansion
  dry-run item #8) is reviewed and uses the clean `3z·e^{4z}` form. Applying
  it together with (a) keeps the displayed stem and the solution consistent
  (the same cleanup-before/with-pedagogy rule the 6 cleanup-dependency items
  followed).

### Classification: `apply-ready-Type-S`

The stem correction is justified by repo-internal source (the 풀이 region)
plus answer consistency — not insufficient, not a defective question. It is
classified `apply-ready-Type-S` because it modifies the question stem and
must therefore go through a separate Type-S apply approval. This document
serves as the Type-S correction dry-run/review; **no apply is performed
here** (per the supervisor instruction — Type S edits are forbidden before a
separate apply approval).

Recommended next step (separate approval): a paired Type-S apply — (a) the
`text` stem correction + (b) the pedagogy `solution`/`steps` apply for
`2006_1회_7` — then a PA-V-style verification.

## 2. `2001_3회_43` — hold-source review

### Current `app/data` state

- `subject` 전기기기, `q_type` 개념형, `answer` 2.
- `text`: `정류자형 주파수 변환기의 설명 중 틀린 것은？`
- `choices`: [1] 전기각 2π/3 간격 3조 브러시 / [2] 3차 권선 설치, 1차·조정권선
  을 회전자에·2차 권선을 고정자에 / [3] 3개 슬립링 = 회전자 권선 3등분점 접속
  / [4] 대용량기 보상권선·보극권선을 고정자에.
- `solution`/`steps`: pre-pedagogy auto-generated version (held).

### Source re-check

`data/mathpix_기출_2001_3회.json`, 문제 43 풀이:

> 정류자형 주파수 변환기는 유도전동기의 2차 여자를 행하기 위한 교류여자기로서
> 사용된다. 구조는 3상 회전변류기의 전기자와 거의 같은 구조를 갖고 정류자와
> 3개의 슬립링을 갖추고 있다. 정류자상에는 한 쌍의 자극마다 전기각 2π/3의
> 간격으로 3조의 브러시가 있고 3개의 슬립링은 회전자 권선을 3등분한 점에 각각
> 접속된다. 용량이 큰 것에서는 정류작용을 좋게 하기 위하여 보상 권선, 보극
> 그리고 보극권선 등을 설치한 고정자도 있다. 【답】(2)

`old_answer_manual_source_review_pack_2026-05-21.md` (pack1): records only
"문제 43 풀이 box ends with 【답】②".

### Can the error in choice [2] be confirmed?

NO — from repo-internal source. The 풀이 box confirms:

- the answer is ② (`【답】(2)`),
- choices (1) [브러시 2π/3 3조], (3) [슬립링 = 회전자 권선 3등분점], (4)
  [보상권선·보극권선 = 고정자] are correct (the 풀이 restates each).

But the 풀이 box says **nothing** about where the 1차 / 2차 / 조정 권선 are
placed — it does not address choice [2]'s claim at all. So the specific error
mechanism in [2] (is it the 회전자/고정자 placement that is reversed? the
"3차 권선" count? the winding naming?) is **not confirmed** by the source.

Repo search for other coverage of 정류자형 주파수 변환기 winding arrangement:
only the question itself (duplicated across `data/questions_기출_*` files) and
unrelated 제어공학 hits — no 전기기기 textbook / study material in-repo
describes the machine's winding placement. Per the supervisor instruction,
no estimation is made beyond the available source.

### Classification: `hold-source-external-textbook-needed`

The answer ② is source-verified, but a pedagogy `보기 판단` for choice [2]
requires stating *why* [2] is wrong, and that error mechanism cannot be
established from any repo-internal source. It is not a defective question
(so not `hold-DQ`) — it is a sound question whose wrong-choice rationale
needs an **external 전기기기 textbook** to confirm. `2001_3회_43` stays
`hold-source`; it is excluded from apply until that external source is
obtained.

## 3. Summary

| key | classification | close in this track? | reason |
| --- | --- | --- | --- |
| `2006_1회_7` | `apply-ready-Type-S` | yes — pending a separate Type-S apply approval | stem `3 z e^{4 z}` restoration justified by the source 풀이 region + answer; pedagogy draft ready |
| `2001_3회_43` | `hold-source-external-textbook-needed` | no | choice [2] error mechanism not confirmable from any repo-internal source; needs an external 전기기기 textbook |

- `2006_1회_7` is **closeable** via a separate Type-S apply (text stem
  correction + pedagogy apply, paired). No apply done here — review only.
- `2001_3회_43` **cannot be closed** in this track. It remains held; closing
  it requires an external textbook source for the choice-[2] error, which is
  outside the repo. Recommend recording it as a deferred item rather than
  forcing an apply.

## Not done in this step

- No `app/data/questions.json` / `questions.v2.json` modification.
- No `text` / `choices` / `answer` / `solution` / `steps` modification.
- No apply of either item (review/decision only).
- No commit; no push; no local server; no paid API call.

## Status

- Residual-2 closeout review complete.
- `2006_1회_7` → `apply-ready-Type-S`: the stem correction
  `3 Z e^{\overline{4 z}}` → `3 z e^{4 z}` is justified by the source 풀이
  region and answer consistency; ready for a separate Type-S apply (stem
  correction + pedagogy apply).
- `2001_3회_43` → `hold-source-external-textbook-needed`: stays held; the
  choice-[2] error mechanism is not confirmable from repo-internal source.
- Next (separate approval): the `2006_1회_7` Type-S apply; for `2001_3회_43`,
  obtain an external 전기기기 textbook source or record it as a deferred item.
