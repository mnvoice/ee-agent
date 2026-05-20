# T3.5 Regeneration Decision Log

Date: 2026-05-20
Branch: `feat/phase-b-migration`

## Context

The project is migrating from answer-mismatch detection toward answer-locked solution regeneration.

Core finding:

- `q.answer` is the answer SoT.
- For 2025-2026, PDF `[정답]` answer tables were extracted and matched `q.answer` 400/400.
- Latest P1 answer mismatch cases were not answer errors. They were LLM-generated solution conclusion errors.
- Therefore the LLM should not choose the answer. It should explain the already-fixed answer.

## Gate Roles

Use different levels of strictness by gate:

| Gate | Role | Strictness |
| --- | --- | --- |
| G3 source answer check | Verify `q.answer` against PDF/source answer | precise |
| G1 automatic validation | Check conclusion number, answer choice text, PUA/FFFD, output shape | precise |
| G2 human QA | Spot check generated explanations for obvious quality problems | coarse |

G2 is not answer verification.

Human reviewers should not solve the problem again and should not compare every item against the textbook. G2 only asks whether the explanation is embarrassing or unsafe to show to a beginner.

## T3.5-F2 Decision

Proposed:

- Regenerate the 22-item QA review sheet with a simpler 4-item spot-check rubric.

Decision:

- Skip T3.5-F2 for the current batch.

Reason:

- Claude already evaluated the existing 22-item QA sheet.
- The result is actionable enough for this batch.
- Rebuilding the review sheet now would not change the decision materially.
- The simplified rubric should be used for the next batch, not retroactively for this one.

Carry forward:

- Add the simplified G2 policy to future review sheets.

## G2 Result Interpreted

Claude G2 review result:

- PASS: 21
- RETRY: 0
- FAIL: 1
- Automatic fail criteria: 0

Failed item:

- `2025_3회_79`
- Category: concept
- Cause: figure/block-diagram dependent problem.
- The generated explanation was too generic because figure-derived analysis is intentionally not available.

Interpretation:

- This is not a q.answer problem.
- This is not an answer-locked regeneration policy failure.
- This is a figure-dependent input limitation.

## Next Track

Run T3.5-G:

1. Hold `2025_3회_79` as `hold_figure_dependent`.
2. Sweep all 77 regenerated items for figure-dependent cases.
3. Split staging into:
   - apply candidates
   - hold candidates
4. Recompute G2 after hold exclusions.
5. Do not modify `questions.json`, `questions.v2.json`, `app/index.html`, or `data/pdf_pages` during this audit.

## T3.5-G Outcome

T3.5-G completed as a read-only audit.

Result:

- Apply candidates: 74
- Hold candidates: 3
- Data changes: 0

Hold candidates:

| Key | Reason |
| --- | --- |
| `2025_2회_60` | Figure-dependent DC machine winding identification. The regenerated explanation inferred the winding structure from `q.answer`. |
| `2025_3회_79` | Block-diagram comparison problem. This was the Claude G2 FAIL item. |
| `2026_1회_67` | Gate-circuit diagram identification. The regenerated explanation inferred the circuit structure from `q.answer`. |

One additional figure-keyword candidate, `2025_2회_45`, remains apply-eligible because the text states enough information without the figure (`가극성 변압기`) for the calculation to stand.

Updated G2 interpretation:

- Effective sample after hold exclusion: 21
- Effective sample PASS: 21/21
- Category effective pass rates:
  - calculation: 5/5
  - regulation: 5/5
  - concept: 11/11

Decision:

- Do not apply all 77 regenerated solutions.
- Treat the 3 figure-dependent cases as hold items for a separate figure/crop-backed track.
- The 74 apply candidates may proceed to G4 patch staging and user approval.

Policy carry-forward:

- Figure-dependent problems must be detected before answer-locked regeneration is applied.
- If the explanation only works by reverse-engineering `q.answer` without access to the figure, hold it.
- Regulation items should not invent KEC/article numbers. Missing article numbers are not a hard failure by themselves; invented article numbers are a failure.

## T3.5-H Dry-Run Outcome

T3.5-H completed as a read-only dry-run.

Result:

- Apply candidates: 74
- Missing keys in `questions.json`: 0
- Missing keys in `questions.v2.json`: 0
- Old hash drift: 0
- File changes made: 0

Dry-run change plan:

| File | Fields |
| --- | --- |
| `app/data/questions.json` | `solution`, `steps` |
| `app/data/questions.v2.json` | `solution`, `steps`, `solution_source`, `steps_source` |

Change count:

- `solution`: 74
- `steps`: 74
- `questions.v2.json` source metadata: 74 `solution_source` + 74 `steps_source`

Recommended v2 source metadata policy:

- Keep `source: "llm_synthesized"` because the regenerated explanation is still LLM-authored.
- Set `tool_name: "answer-locked-regen-T3.5"` to distinguish these from earlier free-form LLM solutions.
- Set `verified_at` to the apply timestamp because the batch passed source-answer locking, automatic validation, and G2 sampling QA.

Recommended apply procedure:

1. Re-run `/tmp/patch_apply_drift_check.py`.
2. Apply all 74 candidates to both JSON files in one operation.
3. Keep the 3 figure-dependent cases excluded.
4. Update `/tmp` staging only if needed for bookkeeping; repo data remains the actual patch target.
5. Run G5 app verification at `http://localhost:8001/`.

Decision pending:

- User approval for T3.5-I actual apply.
- Whether to use the recommended v2 source metadata policy above.

## Future G2 Rubric

Use a coarse 4-item spot check:

1. Does the explanation make sense?
2. Is the calculation or logic flow natural?
3. Does it avoid inventing evidence, law articles, or source facts?
4. Is it understandable for a beginner?

Per item:

- `OK`
- `suspicious`
- `NG`

Final item verdict:

- `PASS`: no `NG`, at most one `suspicious`
- `RETRY`: no `NG`, two or more `suspicious`
- `FAIL`: one or more `NG`

Batch pass guideline:

- FAIL: 0
- RETRY: 2 or fewer
- PASS: at least 20 of 22
- Category pass rates:
  - calculation: at least 4 of 5
  - regulation: at least 4 of 5
  - concept: at least 10 of 12

Important: G2 is a smell test, not expert answer verification.

## T3.5-I Apply Outcome

T3.5-I applied the 74 apply candidates to both data files after user approval.

Result:

- Drift check (`patch_apply_drift_check.py`): exit 0, 0 drift, 0 missing keys.
- Applied: 74/74 to `app/data/questions.json` and `app/data/questions.v2.json`.
- Post-apply hash verification: 0 mismatch on both files.
- `answer_mismatch` recheck on the 74 applied items: 0 remaining on both files.
- Hold items (`2025_2회_60`, `2025_3회_79`, `2026_1회_67`): unchanged, not applied.
- Apply timestamp: `2026-05-20T13:09:55+09:00`.

Format-preservation catch:

- The first apply pass wrote `questions.v2.json` with `json.dump(indent=2)`, but the
  original file is compact single-line. This reformatted the whole file (~294k line diff).
- Corrected: restored the original via `git show HEAD`, then re-applied the 74 items
  with compact serialization (`separators=(',',':')`), preserving the original format.
- `questions.json` was unaffected because its original format is already indent=2.

v2 source metadata applied:

- `solution_source` / `steps_source` for the 74 items set to
  `{source: "llm_synthesized", tool_name: "answer-locked-regen-T3.5", verified_at: <apply timestamp>}`.
- Hold items keep their previous `tool_name` (unchanged).

Final diff:

- `app/data/questions.json`: 535 line change (74 items, indent=2 preserved).
- `app/data/questions.v2.json`: compact single-line file (line-level diff not meaningful).

Gate status:

- G4 (data apply): complete.
- G5 (post-apply app verification): complete (see T3.5-J).

## T3.5-J G5 Verification Outcome

T3.5-J completed G5 as a read-only verification. No data changes.

Static verification (all 74 applied items, 9 checks, each 74/74):

- Key present in both `questions.json` and `questions.v2.json`.
- `solution` / `steps` SHA1[:12] hash matches staging `new_solution_hash` / `new_steps_hash`
  in `questions.json` and `questions.v2.json`.
- `answer == staging q_answer == new_conclusion` (answer-locked invariant holds).
- `getSolutionRenderState(q) == 'meaningful'` for all 74 — the app render-gating logic
  (replicated from `app/index.html`) classifies every regenerated solution as visible,
  so none fall back to the placeholder/empty pending box.
- No PUA (U+E000..U+F8FF) and no U+FFFD in `solution` + `steps`.

Browser spot-check at `http://localhost:8001/` (6 representative items — concept x3,
calculation x2, regulation x1, spanning 2025 1/2/3회 and 2026 1회):

| Item | Category | Result indicator | Pending box | Conclusion |
| --- | --- | --- | --- | --- |
| 2025_1회_14 | concept | 정답입니다 | none | 정답: 2번 (가우스의 정리) |
| 2025_1회_36 | calculation | 정답입니다 | none | 정답: 2번 (60,820) |
| 2025_1회_81 | regulation | 정답입니다 | none | 정답: 1번 (300) |
| 2025_2회_16 | concept | 정답입니다 | none | 정답: 1번 (주파수에 비례한다.) |
| 2025_3회_26 | concept | 정답입니다 | none | 정답: 1번 (서지 흡수기) |
| 2026_1회_2 | calculation | 정답입니다 | none | 정답: 3번 (11) |

- All 6 render question/choices/answer highlight/solution toggle correctly.
- Pending gating box: 0. Step blocks: 2-3 each. Replacement-char badge: 0.
- LaTeX renders via KaTeX (no MathJax). Console errors: 0.
- `solution_svg` items (2025_2회_16, 2026_1회_2) show the "AI 풀이 그림 (원문 아님)" label.

Conclusion: the 74 answer-locked regenerated solutions are correct at the data, render-gating,
and live-display layers. Hold items (`2025_2회_60`, `2025_3회_79`, `2026_1회_67`) remain
out of scope for this gate.

Environmental note — display cache vs data (two separate problems):

- A separate in-app browser (OpenAI Codex) showed the pre-regeneration solutions for
  some items. This is a service-worker / HTTP cache staleness issue in that browser
  context — NOT a data or render defect.
- Evidence it is a cache issue, not data: (1) the app ships a service worker (`app/sw.js`);
  (2) static hash checks confirm `app/data/questions.json` and `questions.v2.json` hold
  the regenerated content (74/74); (3) the gstack verification used a clean Chrome
  context with no prior cache and rendered the new solutions correctly.
- Remedy for a stale browser: hard-reload or unregister the service worker. No data
  or code change is warranted by the stale display.
- Hold item `2025_3회_79` correctly retains its OLD solution because it was never
  applied — this is expected, not a cache artifact.

### T3.5-J Batch 1 — 2025_1회 clean-Chrome G5 verification

Continuation of G5: full browser verification of the 2025_1회 regenerated items.
The 6 items in the spot-check table above plus the 3 hold items are excluded; Batch 1
covers the remaining 19 regenerated items of 2025_1회.

Scope (19 items):
`Q23 Q28 Q29 Q33 Q39 Q43 Q44 Q45 Q46 Q58 Q84 Q85 Q87 Q90 Q91 Q92 Q93 Q94 Q100`

Method:
- Reference environment fixed to clean Chrome via gstack headless browser.
- Before verification: service worker `unregister()` + `caches` keys all deleted + reload,
  to eliminate stale-cache influence.
- Per item: jump to question code, click the `q_answer` choice, expand the solution toggle,
  read the result indicator, pending box, conclusion line, step blocks, replacement-char
  badge, KaTeX element count, and `.katex-error` count.
- Codex in-app browser results are excluded from the verdict basis (possible stale cache;
  reference-only). clean Chrome / gstack is the fixed final basis.

Result — 19/19 PASS, 0 FAIL:

| Item | Category | Conclusion | Item | Category | Conclusion |
| --- | --- | --- | --- | --- | --- |
| Q23 | concept | 2번 (적산 유량 곡선) | Q85 | regulation | 1번 (1) |
| Q28 | concept | 2번 (탑각 접지저항의 감소) | Q87 | concept | 3번 (합성수지관공사) |
| Q29 | concept | 1번 (특별한 보호장치가 필요 없다) | Q90 | regulation | 1번 (50) |
| Q33 | concept | 1번 (유도뢰) | Q91 | calculation | 3번 (6) |
| Q39 | calculation | 3번 (80) | Q92 | calculation | 2번 (2.6) |
| Q43 | concept | 3번 (교차 자화작용) | Q93 | concept | 2번 (태양전지 개폐기) |
| Q44 | concept | 1번 (브흐홀쯔 계전기) | Q94 | calculation | 3번 (5.78) |
| Q45 | concept | 3번 (기동 토크의 발생) | Q100 | regulation | 3번 (20) |
| Q46 | concept | 1번 (기전력의 용량이 같을 것) | Q58 | calculation | 2번 (0.19) |
| Q84 | regulation | 3번 (1) | | | |

Verification facts:
- All 19: result indicator `정답입니다`, pending box `none`, step blocks 2-3.
- Conclusion answer number matches `questions.json.answer == questions.v2.json.answer
  == staging q_answer == new_conclusion` for all 19 (4-way agreement; static cross-check 19/19).
- Console errors: 0 across the whole batch.
- `.katex-error`: 0. Q58 renders 5 KaTeX elements correctly; other items use plain-text
  math notation (0 KaTeX elements) — a notation choice of the regenerated solution,
  not a render failure.
- Replacement-char badge: 0 on all 19.
- Hold items (`2025_2회_60`, `2025_3회_79`, `2026_1회_67`) are 2025_2회/3회/2026_1회;
  none belong to 2025_1회, so no hold item is present in Batch 1.

Independent judgment:
- Claude CLI execution verification: 19/19 PASS.
- Web Claude independent judgment: 19/19 PASS.
- Supervisor approval: Batch 1 fixed as final PASS on the clean Chrome / gstack basis.

Batch 1 verdict: PASS — 19/19. No data, solution-content, or render-code changes were made.

### T3.5-J Batch 2 — 2025_2회 clean-Chrome G5 verification

Continuation of G5: full browser verification of the 2025_2회 regenerated items.

Scope (21 items):
`Q18 Q23 Q24 Q25 Q28 Q31 Q42 Q45 Q47 Q49 Q51 Q56 Q58 Q66 Q81 Q83 Q92 Q93 Q94 Q96 Q100`

Method:
- Reference environment fixed to clean Chrome via gstack headless browser.
- Before verification: service worker `unregister()` + `caches` keys all deleted + reload,
  to eliminate stale-cache influence.
- Per item: jump to question code, click the `q_answer` choice, expand the solution toggle,
  read the result indicator, pending box, conclusion line, step blocks, replacement-char
  badge, KaTeX element count, and `.katex-error` count.
- Codex in-app browser results are excluded from the verdict basis (possible stale cache;
  reference-only). clean Chrome / gstack is the fixed final basis.

Result — 21/21 PASS, 0 FAIL:

| Item | Category | Conclusion |
| --- | --- | --- |
| Q18 | concept | 1번 (경계면 전계·전속밀도 불변 = 틀림) |
| Q23 | calculation | 1번 (339) |
| Q24 | calculation | 1번 (550) |
| Q25 | concept | 1번 (선택접지 계전기) |
| Q28 | concept | 2번 (역률개선용 콘덴서 개방) |
| Q31 | concept | 2번 (발전기의 조속기) |
| Q42 | calculation | 2번 (1200) |
| Q45 | calculation | 3번 (300) |
| Q47 | concept | 3번 (교류를 직류로 변환) |
| Q49 | concept | 1번 (점도가 높을 것 = 틀림) |
| Q51 | concept | 1번 (전절권 = 틀림) |
| Q56 | calculation | 1번 (12) |
| Q58 | concept | 2번 (감자작용) |
| Q66 | concept | 1번 (정K형 전역) |
| Q81 | concept | 2번 (3상 정류기용 변압기) |
| Q83 | regulation | 1번 (15) |
| Q92 | regulation | 2번 (10) |
| Q93 | calculation | 2번 (150) |
| Q94 | concept | 1번 (케이블트레이공사) |
| Q96 | concept | 2번 (콤바인덕트 케이블) |
| Q100 | concept | 3번 (소선 5가닥 이상 = 틀림) |

Verification facts:
- All 21: result indicator `정답입니다`, pending gating box 0/21 (every item rendered
  as `meaningful`), step blocks 2-3; solution displayed correctly after the answer
  choice was selected (21/21).
- Data 5-layer agreement for all 21: `questions.json.answer` == `questions.v2.json.answer`
  == staging `q_answer` == `new_conclusion` == browser conclusion `정답: N번`.
- Console errors: 0 across the whole batch.
- `.katex-error`: 0. KaTeX rendered correctly on Q23 (2), Q42 (3), Q56 (1); other items
  use plain-text math notation (0 KaTeX elements) — a notation choice, not a render failure.
- Replacement-char badge: 0 on all 21.
- AI figure labels render correctly: Q45 ("AI 보조 그림 (원문 아님)"), Q66 ("AI 풀이 그림 (원문 아님)").
- Hold item `2025_2회_60` confirmed excluded from the Batch 2 scope (not present).

Independent judgment:
- Claude CLI execution verification: 21/21 PASS.
- Web Claude independent judgment: 21/21 PASS.
- Supervisor approval: Batch 2 fixed as final PASS on the clean Chrome / gstack basis.

Batch 2 verdict: PASS — 21/21. No data, solution-content, or render-code changes were made.

### T3.5-J Batch 3 — 2025_3회 clean-Chrome G5 verification

Continuation of G5: full browser verification of the 2025_3회 regenerated items.

Scope (15 items):
`Q39 Q41 Q43 Q45 Q49 Q55 Q56 Q57 Q58 Q85 Q86 Q87 Q89 Q91 Q96`

Method: identical to Batch 2 (clean Chrome via gstack; service worker `unregister()` +
`caches` deleted + reload before verification; Codex in-app browser excluded from the
verdict basis).

Result — 15/15 PASS, 0 FAIL:

| Item | Category | Conclusion |
| --- | --- | --- |
| Q39 | concept | 1번 (증기를 가열한다) |
| Q41 | calculation | 1번 (48.81°) |
| Q43 | concept | 3번 (게이트-에미터 입력 임피던스 낮음 = 틀림) |
| Q45 | concept | 1번 (극수가 증가한 경우) |
| Q49 | concept | 1번 (크레인) |
| Q55 | calculation | 3번 (50) |
| Q56 | concept | 2번 (감소한다) |
| Q57 | concept | 2번 (폐로권·고상권·이층권) |
| Q58 | concept | 3번 (절연저항이 같을 것 = 틀림) |
| Q85 | regulation | 1번 (50) |
| Q86 | regulation | 1번 (1) |
| Q87 | concept | 2번 (154[kV] 분산전원형 발전소) |
| Q89 | regulation | 2번 (2.5[㎜²] 경동선 = 틀림) |
| Q91 | regulation | 2번 (10) |
| Q96 | concept | 2번 (3상 정류기용 변압기) |

Verification facts:
- All 15: result indicator `정답입니다`, pending gating box 0/15 (every item rendered
  as `meaningful`), step blocks 2-3; solution displayed correctly after the answer
  choice was selected (15/15).
- Data 5-layer agreement for all 15: `questions.json.answer` == `questions.v2.json.answer`
  == staging `q_answer` == `new_conclusion` == browser conclusion `정답: N번`.
- Console errors: 0 across the whole batch.
- `.katex-error`: 0. KaTeX rendered correctly on Q41 (3), Q55 (2), Q56 (3); other items
  use plain-text math notation (0 KaTeX elements) — a notation choice, not a render failure.
- Replacement-char badge: 0 on all 15.
- Hold item `2025_3회_79` confirmed excluded from the Batch 3 scope (not present).

Independent judgment:
- Claude CLI execution verification: 15/15 PASS.
- Web Claude independent judgment: 15/15 PASS.
- Supervisor approval: Batch 3 fixed as final PASS on the clean Chrome / gstack basis.

Batch 3 verdict: PASS — 15/15. No data, solution-content, or render-code changes were made.

### T3.5-J Batch 2/3 combined summary

- Batch 2 + Batch 3 combined: 36/36 PASS, 0 FAIL, 0 held.
- Hold items `2025_2회_60`, `2025_3회_79`, `2026_1회_67` were not touched (`2026_1회_67`
  belongs to 2026_1회, outside both batch scopes).
- No paid Claude / OpenAI API calls were made; verification used local static checks
  plus clean Chrome / gstack browser automation only.
- No data, solution-content, or render-code changes were made.

Process note — from the next batch (Batch 4, 2026_1회) onward, an explicit
PUA (U+E000..U+F8FF) / U+FFFD 0-count check is added as a per-batch reporting item.
For Batch 2/3 this property was already covered by the T3.5-J static verification
(no PUA / no U+FFFD across all 74 applied items) and by the replacement-char badge
count of 0 in every browser check.
