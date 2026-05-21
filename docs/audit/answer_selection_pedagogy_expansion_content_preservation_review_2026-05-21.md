# Answer-Selection Pedagogy — Content-Preservation Sanity Review (2026-05-21)

A content-preservation sanity review of the 3 PA-applied items with the
largest `solution` length reduction. It checks whether the v2.1 pedagogy
rewrite dropped any answer-essential reasoning from the prior `solution`.

This is a **read-only review document**. It does NOT modify `app/data`.

- Scope: `2015_2회_29` (520→405), `2002_3회_4` (652→447), `2016_1회_44`
  (804→491)
- Method: the prior `solution` (pre-PA snapshot) compared element-by-element
  against the applied v2.1 `solution`
- Note: the prior `solution` is NOT a gold standard — these are 1998-2016 old
  questions whose answers were corrected in the C20 track; the prior
  solutions are auto-generated markdown. The v2.1 solution is a full rewrite,
  not a trim. "Preservation" here means the *correct, answer-essential*
  content survived; dropping stale/tangential content is acceptable.

---

## `2015_2회_29` (520 → 405, −115) · answer 2

1. **Answer-essential reasoning preserved** — YES. Prior: 피뢰기 = 이상전압
   파고치 저감, 과전압 시 방전 경로 제공. New `근거/계산` keeps this and adds
   the discharge/속류-차단 mechanism (방전 개시 전압 초과 시 도통 → 서지 대지
   방류 → 정상 전압 복귀 시 속류 차단) — more precise than the prior.
2. **Unique concept content** — no essential loss. The prior per-device
   descriptions (직렬 리액터=제5고조파, 아킹 혼=애자련 보호, 아모로드=진동
   단선 방지) are all kept in the new `보기 판단` [1]/[3]/[4]. Minor prior
   elaborations ("아크를 유도", "전선 고정점 근처 설치") were dropped — these
   are non-essential detail, not answer reasoning.
3. **Choice [1]-[4] judgments** — all present in `보기 판단` ([1][2][3][4]).
4. **정답 ↔ 근거/계산** — consistent: `정답` 2번(피뢰기); `근거/계산` explains
   the 피뢰기 mechanism; `보기 판단` [2] = 정답. No contradiction.
5. **Reason for reduction** — format cleanup (markdown bold/headers and
   per-device sub-bullet blocks `용도:`/`특성:`/`작동 원리:`/`역할:` removed)
   + dedup (the prior repeated "이상전압 파고치 저감" in the intro, in (2),
   and in the closing paragraph). No correct content removed.

verdict: **content preserved** (new solution is marginally more precise on
the 피뢰기 mechanism).

## `2002_3회_4` (652 → 447, −205) · answer 4

1. **Answer-essential reasoning preserved** — YES. Prior derivation
   (point-charge V=q/4πεr → element dU=ρs·dS/4πεr → integrate
   U=(1/4πε)∬ρs/r dS) is kept verbatim in `보기 판단` + `근거/계산`.
2. **Unique concept content** — one prior block dropped: section "3) 전계와
   전위의 관계: E=−dU/dr; 면전하 전계 E=ρs/2ε 균일 → 전위는 거리에 선형".
   Assessment: this is **tangential and physically shaky** — the question
   asks for the *general surface-charge potential integral* (the answer is
   the integral formula [4]); the dropped block jumps to the infinite-plane
   uniform-field case, and an infinite charged plane's absolute potential
   does not converge, so "전위는 거리에 선형" is a loose statement. Its
   removal is acceptable — arguably a content improvement, not a loss.
3. **Choice [1]-[4] judgments** — IMPROVED. The prior `solution` gave the
   formula and only stated "선택지 ④번과 일치" — it did NOT explain why [1],
   [2], [3] are wrong. The new `보기 판단` explains [1] (분모 2πε ≠ 4πε) and
   [2]/[3] (1/r² = field, not potential). New coverage of [1]-[4] is more
   complete than the prior.
4. **정답 ↔ 근거/계산** — consistent: `정답` 4번; `근거/계산` derives
   U=(1/4πε)∬ρs/r dS; `보기 판단` → [4]. No contradiction. (The prior also
   carried a "참고 풀이의 정답 표기 오류" note — a C20-correction artifact;
   the new solution simply concludes ④ cleanly.)
5. **Reason for reduction** — format cleanup + dedup (the formula was stated
   ~3× in the prior) + removal of the tangential / physically-shaky 전계-전위
   block (an error-prone expression removed).

verdict: **content preserved**; the new solution is more complete on
per-choice judgment and drops a tangential block.

## `2016_1회_44` (804 → 491, −313) · answer 4

1. **Answer-essential reasoning preserved** — YES. The two reasons [4] is the
   answer are both kept: (a) 브러시 단락 코일 기전력 = 정류(commutation)
   과정의 리액턴스 전압, 별개 현상; (b) 전기자 반작용은 감자작용으로 기전력을
   감소시키므로 "증가" 서술과 모순. New `보기 판단` [4] + `함정` carry both.
2. **Unique concept content** — no essential loss. The prior's 3 영향
   (감자작용 / 중성축 이동 / 정류 악화) are kept in `근거/계산` (감자작용 +
   편자작용(중성축 이동) + 정류 악화 — "편자작용" is correct terminology for
   the 중성축-이동 component). The prior word "섬락" (a named consequence of
   정류 악화) was dropped; "정류 악화" itself is kept — a non-essential trim.
3. **Choice [1]-[4] judgments** — all present. [2] and [3] are merged into
   one clause ("[2] 발전기는 회전 방향으로, [3] 전동기는 그 반대 방향으로
   중성축 이동: 둘 다 영향") — both choices are still explicitly referenced
   (this merge was made in the correction-pass trim and noted there).
4. **정답 ↔ 근거/계산** — consistent: `정답` 4번; `근거/계산` "3대 영향에
   '기전력 증가'는 없다"; `보기 판단` [4] = 정답. No contradiction.
5. **Reason for reduction** — heavy dedup (the prior explained 중성축 이동 in
   the intro AND restated it in (2)+(3); explained the 정류 리액턴스 전압 /
   유기기전력 감소 point in the intro AND in (4) AND in the closing
   paragraph) + format cleanup (markdown bold, the intro block, the closing
   summary removed). The −313 is the largest because the prior was the most
   repetitive. No correct content removed.

verdict: **content preserved** (the reduction is almost entirely dedup of a
highly repetitive prior solution).

---

## Summary

| key | before→after | core reasoning preserved | choice [1]-[4] | 정답↔근거 | reduction cause |
| --- | --- | --- | --- | --- | --- |
| `2015_2회_29` | 520→405 | YES (+ more precise) | all 4 | consistent | format + dedup |
| `2002_3회_4` | 652→447 | YES | all 4 (improved) | consistent | format + dedup + tangential block removed |
| `2016_1회_44` | 804→491 | YES | all 4 ([2][3] merged, both referenced) | consistent | dedup (heavy) + format |

- All 3: the answer-essential reasoning and the per-choice judgments survived
  the v2.1 rewrite; `정답` and `근거/계산` connect without contradiction.
- No correct, answer-relevant content was lost. The reductions are explained
  by markdown-format removal, deduplication of repetitive prior solutions,
  and — for `2002_3회_4` — the removal of one tangential / physically-shaky
  block (a content improvement).
- No error or contradiction was introduced by the rewrite (the new per-choice
  claims were re-checked: `2002_3회_4` 1/r² = field vs 1/r = potential,
  `2015_2회_29` 직렬 리액터 = 제5고조파, `2016_1회_44` 편자작용 terminology —
  all correct).

verdict: **sanity review PASS** for all 3. No content-preservation concern;
the PA apply stands.

## Not done in this step

- No `app/data` modification (review only).
- No commit; no push.

## Status

- Content-preservation sanity review complete for the 3 largest-reduction
  items. All 3 preserve answer-essential reasoning and per-choice judgments;
  reductions are format cleanup + dedup (+ one tangential removal). PASS.
