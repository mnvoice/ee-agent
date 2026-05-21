# Answer-Selection Pedagogy — Expansion Pre-apply Correction Pass (2026-05-21)

Pre-apply correction pass for the 18-item expansion dry-run. It records the
`2016_1회_44` length trim, the `2001_3회_43` source spot-check result, the
OCR-flag cleanup decision (deferred), and the final 4-bucket classification.

This is a **correction-record document**. It does NOT modify `app/data`, does
NOT apply any `solution` / `steps`, and is not an approval to apply.

- Base commit: `f09b97e`
- Dry-run: `docs/audit/answer_selection_pedagogy_expansion_dryrun_2026-05-21.md`
  (`2016_1회_44` candidate edited in place by this pass)
- Review: `docs/audit/answer_selection_pedagogy_expansion_dryrun_review_2026-05-21.md`
- Source pool: `docs/audit/old_answer_conflict_correction_manifest_2026-05-21.md`,
  `docs/audit/old_answer_manual_source_review_pack_2026-05-21.md` (pack1)

## 1. `2016_1회_44` — light trim (548 → 491)

The dry-run draft was 548 chars, over the v2.1 350-500 target. Trimmed to
**491 chars** (re-measured). The `정답` / `보기 판단` / `근거/계산` structure is
preserved; all 4 choices remain explicitly referenced.

What changed:

- `근거/계산` — the second sentence ("단락 코일의 리액턴스 전압은 정류 자체의
  현상이다") was removed; it restated what `보기 판단` [4] already says. The
  rule kept in `근거/계산` is the 3대 영향 list.
- `보기 판단` — choices [2] and [3] (발전기/전동기 중성축 이동) were merged
  into one clause; **both [2] and [3] are still explicitly referenced**.
- `함정` / `시험장 판별` — each compressed to one short sentence (the point
  overlapped across 4 elements; one statement per element kept).
- `핵심 단서` / `정답` — unchanged in substance.

Post-trim self-check: length 491 (within 350-500); 6 v2.1 labels present in
order; `정답:` is the last line; choices [1]-[4] all mapped; answer 4 matches
`q.answer`. The `steps` dict (145 chars) is unchanged.

The dry-run document's item-16 candidate was edited in place to the 491-char
version (with a `보정 2026-05-21` note). `app/data` is NOT modified.

## 2. `2001_3회_43` — source spot-check result

### What was checked

The dry-run flagged that the *reason* choice [2] is wrong was an inference
(derived by negating the answer), not a sourced fact. Two (a) sources were
read directly:

- `old_answer_manual_source_review_pack_2026-05-21.md` (pack1, line 48):
  records only "문제 43 풀이 box ends with 【답】②" — confirms the answer,
  not the reason.
- `data/mathpix_기출_2001_3회.json` — the mathpix OCR of the source PDF,
  including the 풀이 (solution) box for 문제 43.

### The source 풀이 box (verbatim, from the mathpix OCR)

> 정류자형 주파수 변환기는 유도전동기의 2차 여자를 행하기 위한 교류여자기로서
> 사용된다. 구조는 3상 회전변류기의 전기자와 거의 같은 구조를 갖고 정류자와
> 3개의 슬립링을 갖추고 있다. 정류자상에는 한 쌍의 자극마다 전기각 2π/3의
> 간격으로 3조의 브러시가 있고 3개의 슬립링은 회전자 권선을 3등분한 점에 각각
> 접속된다. 용량이 큰 것에서는 정류작용을 좋게 하기 위하여 보상 권선, 보극
> 그리고 보극권선 등을 설치한 고정자도 있다. 【답】(2)

### What the source confirms / does NOT confirm

- CONFIRMS (a): the answer is ② (`【답】(2)`), and the 풀이's machine
  description matches choices **(1)** (한 쌍의 자극마다 전기각 2π/3 간격 3조
  브러시), **(3)** (3개 슬립링 = 회전자 권선 3등분점 접속), and **(4)**
  (대용량기 보상권선·보극권선 = 고정자) — all three are correct statements.
- Does NOT confirm: **the specific error in choice [2]**. The 풀이 box
  describes the machine for the three correct choices but says nothing about
  where the 1차 / 2차 / 조정 권선 are placed. It does not state the correct
  winding arrangement, so it does not establish whether [2]'s error is the
  rotor/stator swap (the dry-run's inference) or something else (e.g. the
  "3차 권선" claim, or the winding naming).

### Conclusion

The source check was performed; it confirms the answer ② but does NOT
confirm the [2] error mechanism. Per the supervisor instruction
("source 확인이 안 되면 이번 limited apply 후보에서 제외"), `2001_3회_43` is
**held from this limited apply round** — classification `hold-source`.

The dry-run's `2001_3회_43` draft is NOT re-drafted (re-drafting needs the
confirmed error mechanism, which is not available). To clear the hold: a
전기기기 textbook (not the 기출 해설, which lacks it) must confirm the actual
error in choice [2]; then the `보기 판단` / `근거/계산` are re-drafted on that
source and the 530-char length trimmed in the same pass.

## 3. OCR flags — `choices` / `text` cleanup (separate decision, deferred)

The expansion has displayed-text mismatch in 7 items (the dry-run's 6
formally-flagged + 1 latent found in review):

| key | location | OCR issue |
| --- | --- | --- |
| `2015_1회_22` | choice [2] | `직접` → `적게` |
| `2015_3회_27` | choice [4] | `자단` → `차단` |
| `2015_2회_29` | choice [4] | trailing page-footer residue |
| `2002_3회_4` | choice [4] | trailing page-footer residue |
| `2016_1회_71` | choice [4] | LaTeX residue `rac{` → `\frac{` |
| `2006_1회_7` | `text` (z항) | OCR residue `\overline`; `3 Z` → `3z` |
| `2016_1회_44` | choice [2]/[3] | `굽은 회전방향` (latent; standard wording = `회전방향`) |

These do NOT block the `solution` / `steps` apply (the apply touches
`solution`/`steps` only). But the displayed `choices`/`text` would mismatch
the pedagogy `보기 판단`. The pilot precedent ran a choice-cleanup pass
(`35f422e`) before the pedagogy apply (`2aadbe5`).

This pass does NOT decide the cleanup — `choices` / `text` modification
needs separate approval. Recorded as a **pending separate decision**: run a
`choices`/`text` cleanup pass (선행 or 동반) for these 7 before/with the
pedagogy apply of the 7 cleanup-dependency items. Until that decision, the 7
items are apply-ready in their `solution`/`steps` but carry the dependency.

## 4. Final classification (18)

| # | key | bucket | note |
| --- | --- | --- | --- |
| 1 | `2001_1회_21` | apply-ready | — |
| 2 | `2015_1회_22` | apply-ready-with-cleanup-dependency | choice [2] OCR |
| 3 | `2015_3회_27` | apply-ready-with-cleanup-dependency | choice [4] OCR |
| 4 | `2015_2회_23` | apply-ready | — |
| 5 | `2015_2회_29` | apply-ready-with-cleanup-dependency | choice [4] residue |
| 6 | `2015_3회_25` | apply-ready | choices recovered `fac4b8d`, clean |
| 7 | `2016_1회_69` | apply-ready | — |
| 8 | `2006_1회_7` | apply-ready-with-cleanup-dependency | text (z항) OCR |
| 9 | `2015_1회_13` | apply-ready | — |
| 10 | `1998_4회_10` | apply-ready | — |
| 11 | `2002_3회_4` | apply-ready-with-cleanup-dependency | choice [4] residue |
| 12 | `2006_1회_6` | apply-ready | — |
| 13 | `2015_1회_71` | apply-ready | — |
| 14 | `2016_3회_44` | apply-ready | — |
| 15 | `2001_3회_43` | hold-source | [2] 오류 사유 source 미확인 (Section 2) |
| 16 | `2016_1회_44` | apply-ready-with-cleanup-dependency | trimmed 548→491; choice [2]/[3] latent OCR |
| 17 | `2016_1회_71` | apply-ready-with-cleanup-dependency | choice [4] LaTeX residue |
| 18 | `2001_1회_68` | apply-ready | — |

Tally:

| bucket | count | keys |
| --- | ---: | --- |
| apply-ready | 10 | `2001_1회_21`, `2015_2회_23`, `2015_3회_25`, `2016_1회_69`, `2015_1회_13`, `1998_4회_10`, `2006_1회_6`, `2015_1회_71`, `2016_3회_44`, `2001_1회_68` |
| apply-ready-with-cleanup-dependency | 7 | `2015_1회_22`, `2015_3회_27`, `2015_2회_29`, `2006_1회_7`, `2002_3회_4`, `2016_1회_44`, `2016_1회_71` |
| hold-source | 1 | `2001_3회_43` |
| hold-DQ | 0 | — |

`hold-DQ` is empty among the 18 — the DQ item (`2002_1회_32`, corrupted
answer choice) and the 2 statute items were already excluded before the
18-item set (dry-run Section 1) and never were expansion candidates.

After this pass: `2016_1회_44` moved needs-trim → cleanup-dependency (trim
done; the remaining dependency is the latent choice OCR). `2001_3회_43`
moved needs-source-check → hold-source (source checked, error mechanism not
confirmed).

## 5. Recommended sequencing

- **10 apply-ready** — `solution`/`steps` drafts ready for a limited apply,
  behind supervisor approval and the iPad/browser viewport gate. No
  dependency.
- **7 apply-ready-with-cleanup-dependency** — `solution`/`steps` ready, but
  sequence the Section 3 `choices`/`text` cleanup decision before or bundled
  with their apply, so displayed text matches the `보기 판단`.
- **1 hold-source** (`2001_3회_43`) — excluded from this limited apply round;
  re-enters after a textbook source confirms the [2] error mechanism, then
  re-draft + trim 530→≤500.
- **0 hold-DQ**.
- No bulk apply at any stage. dry-run → review → correction → limited apply
  → closeout.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `solution` / `steps` apply.
- No `answer` / `choices` / `text` modification (the OCR cleanup is deferred
  to a separate decision).
- No `2001_3회_43` re-draft (held — source not confirmed).
- No app code or schema modification.
- No local server run.
- No paid API call.
- No commit; no push.

## Status

- Correction pass complete. `2016_1회_44` trimmed 548→491 (within target);
  the dry-run document's item-16 candidate updated in place.
- `2001_3회_43` source spot-check done: source confirms answer ② and choices
  (1)(3)(4), does NOT confirm the [2] error mechanism → `hold-source`,
  excluded from this limited apply round.
- Final classification: apply-ready 10, apply-ready-with-cleanup-dependency
  7, hold-source 1, hold-DQ 0.
- Next (separate approval): the `choices`/`text` cleanup decision for the 7
  dependency items, a textbook source check for `2001_3회_43`, then a limited
  pedagogy apply of the apply-ready set behind the iPad viewport gate.
