# Trap-Map B-Priority — 기기-18 Correction Follow-Up Erratum (After Steps Cleanup, 2026-05-23)

Commit C(`961291e`) + Commit C evidence supplement(`6f62da1`) + redryrun after
steps cleanup(`1562390`) 이후의 **post-closeout errata 후속 erratum (v2)**이다.
이전 follow-up(`c6d57d0`)이 caution 사유로 기록했던 기기-18 steps 잔존 결함이
해소돼 caution → 완전 클린으로 전환한다.

본 단계는 상태 정리 문서 작성만 — **실제 data/doc 수정 없음**. app/data·
questions.json·학습 패키지·closeout/이전 erratum 원문 미수정. solution/steps
미적용. answer/choices/text 미수정. 유료 API 미호출. local server 미실행.
amend/rebase/reset 없음.

- 참조:
  - 이전 follow-up erratum (`docs/audit/trap_map_B_priority_gigi_18_correction_followup_erratum_2026-05-23.md`)
  - steps cleanup feasibility (`docs/audit/trap_map_B_priority_gigi_18_steps_cleanup_feasibility_2026-05-23.md`)
  - Commit C evidence supplement (`docs/audit/trap_map_B_priority_gigi_18_commitC_evidence_supplement_2026-05-23.md`)
  - redryrun after steps cleanup (`docs/audit/trap_map_B_priority_gigi_18_redryrun_after_steps_cleanup_2026-05-23.md`)

---

## 결론

- **기기-18 caution → 완전 클린 전환.** Commit C로 steps 잔존 결함 해소, redryrun
  데이터 정합 PASS.
- **clean count 갱신**: 완전 클린 34/39 → **35/40**, caution 2/2 → **1/1** (기기-17만
  잔존), 사용 가능 36/41 불변, blocked 0/0 불변.
- 본 erratum이 이전 follow-up(`c6d57d0`)의 기기-18 caution 상태를 **완전 클린**으로
  갱신한다. 이전 follow-up·closeout 원문은 수정하지 않고, 본 v2가 정정 기록의
  최신 상태를 보유한다.

---

## 1. 정정 트랙 누적 요약 (Commit Chain — 16 commits)

이전 follow-up(`c6d57d0`)의 12-commit chain에 4 commits 추가:

| 순번 | Commit | 단계 | 내용 |
|---|---|---|---|
| 1~12 | `1061a9f` ~ `c6d57d0` | (이전 follow-up `c6d57d0` §1 참조) | feasibility → ... → follow-up erratum (v1) |
| 13 | `71f0082` | steps cleanup feasibility/review | proceed_minimal_cleanup 권장 |
| 14 | `961291e` | **Commit C** — steps cleanup | `2010_2회_47.steps` dict (문제 48 혼입) → `null` |
| 15 | `6f62da1` | Commit C evidence supplement | G-1/G-2/G-3 보강 + rollback 경로 |
| 16 | `1562390` | redryrun after steps cleanup | 데이터 완전 클린 확인, 판정 ready_with_note (adjacent) |
| 17 | (본 문서) | **follow-up erratum v2** | caution → 완전 클린 전환, clean count 갱신 |

---

## 2. 기기-18 상태 결정 (caution → 완전 클린)

### 2.1 caution 해제 근거

이전 follow-up(`c6d57d0`)이 명시한 기기-18 caution 사유:

| caution 사유 | 정정 후 상태 |
|---|---|
| `steps` 필드 문제 48(유도전동기) 혼입 잔존 | ✅ 해소 — Commit C `961291e`로 `steps=null` |

→ 기기-18 caution 사유 **0건**. 해제 정당.

### 2.2 데이터 정합 재확인 (redryrun `1562390` 결과)

| 필드 | 상태 |
|---|---|
| answer | 4 ✅ PDF 정합 |
| choices[3] | "절연내력" ✅ PDF 정합 |
| solution | 194자 PDF 풀이 정합 ✅ |
| **steps** | **null ✅ corpus schema 정합 (70/5,331 선례)** |
| solution_svg | "정답: ④ 절연내력" 정합 ✅ |
| Part 2 마커 5종 (record 전체) | 모두 0 hits ✅ |
| OCR garble 4종 (solution) | 모두 0 hits ✅ |

→ 데이터 모든 필드 PDF·schema 정합.

### 2.3 판정 분류 (재확인)

- trap alignment: **adjacent** (시험 범위 식별 — 절연내력은 두 시험으로 구할 수 없음)
- 판정: **ready_with_note** (adjacent — 학습 함정 분리 가이드만, 데이터 결함 0)

기기-18은 1차 representative redryrun(`6164d6f`)의 ready_with_note(adjacent)
분류로 완전 복귀. 다른 6개 adjacent B 항목(기기-4·23, 설비-14·10·21, 전력-25)과
동급의 **완전 클린**.

---

## 3. Clean Count 갱신

### 3.1 갱신 전 (follow-up erratum v1 `c6d57d0`)

| 분류 | 항 / 문제 |
|---|---|
| A-priority (유지) | 26 / 31 |
| 사용 가능 | 36 / 41 |
| └ 완전 클린 (caution·blocked 제외) | 34 / 39 |
| └ 기기-17 caution | 1 / 1 (choices/solution cleanup residual) |
| └ **기기-18 caution** | **1 / 1 (steps 필드 혼입 residual)** ← Commit C로 해소 |
| blocked | 0 / 0 |
| 합계 | 36 / 41 |

### 3.2 갱신 후 (본 v2)

| 분류 | 항 / 문제 |
|---|---|
| A-priority (유지) | 26 / 31 |
| 사용 가능 | 36 / 41 (불변) |
| └ **완전 클린 (caution·blocked 제외)** | **35 / 40** (+1/+1) |
| └ 기기-17 caution | 1 / 1 (잔존 — choices/solution cleanup) |
| └ 기기-18 caution | **0 / 0** (−1/−1 — **완전 클린으로 전환**) |
| blocked | 0 / 0 (불변) |
| 합계 | 36 / 41 (불변) |

### 3.3 변동 요약

| 변동 | 갱신 전 | 갱신 후 |
|---|---|---|
| 기기-18 분류 | caution 1/1 | **완전 클린 (전환)** |
| 완전 클린 합 | 34 / 39 | **35 / 40** |
| caution 합 | 2 / 2 (기기-17 + 기기-18) | **1 / 1 (기기-17만)** |
| 사용 가능 합 | 36 / 41 | 36 / 41 (불변) |
| blocked 합 | 0 / 0 | 0 / 0 (불변) |
| A-priority | 26 / 31 | 26 / 31 (불변) |
| 전체 합 | 36 / 41 | 36 / 41 (불변) |

→ "기기-18 caution → 완전 클린" 단일 변동. 사용 가능·blocked·A-priority·전체 합
불변. 완전 클린 분모만 34/39 → 35/40으로 증가.

### 3.4 학습자 사용 준비 상태

**"학습자 사용 준비 완료": 36항 사용 가능 = 완전 클린 35 + caution 1**.

남은 caution 1항(기기-17): 보기 [1] LaTeX 잉여 √3 + solution 전류식 오류 —
학습 docs는 이미 정확 풀이 사용 중, app 표시 시 자료 변환 권장. 별도 cleanup
트랙.

---

## 4. 잔존 결함 Logging (이전 follow-up §4 갱신)

| 결함 | 위치 | 영향 | 처리 | 갱신 |
|---|---|---|---|---|
| 기기-17 보기 [1] LaTeX 잉여 √3 | `2020_1회_52` `choices[0]` | app 표시 영향 | 기기-17 cleanup 트랙 | 유지 |
| 기기-17 solution 전류식 오류·결선 라벨 오기 | `2020_1회_52` `solution` | app 풀이 표시 영향 | 기기-17 cleanup 트랙 | 유지 |
| ~~기기-18 `steps` 필드 문제 48 혼입~~ | `2010_2회_47` `steps` | ~~app 표시 영향~~ | ~~별도 cleanup 트랙~~ | **✅ 해소 — Commit C `961291e`** |
| questions.json 추출 파이프라인 인접 문항 혼입 | 파이프라인 자체 | 향후 추출 작업 재발 가능 | 파이프라인 회귀 트랙 | 유지 (디버그 단서: 본 cleanup 전 `steps[인식]`의 자인 문구) |
| v3.2 §5.2 셀 오류 | trap-map source | canonical 사용 시 오도 | v3.3 정정 트랙 | 유지 |
| 회로 커버리지 0 / S/F 6/10 / reserve 5항 소진 | B-pool 모집단 구조 | B-pool 한계 | 미해결 residual | 유지 |

---

## 5. 다음 권장 트랙 (이전 follow-up §5 갱신)

| 우선순위 | 트랙 | 내용 | 갱신 |
|---|---|---|---|
| ~~1~~ | ~~기기-18 steps cleanup~~ | ~~steps=null 적용~~ | **✅ 완료 — Commit C + redryrun + 본 erratum** |
| **1** | **기기-17 PDF 대조 및 cleanup feasibility** | `2020_1회_52` 원본 PDF 보기 [1]·풀이 전류식 검증 후 cleanup 결정. 완료 시 기기-17 caution → 완전 클린, **완전 클린 36/41 / caution 0/0 도달 가능** | 우선순위 승격 (이전 2 → 신규 1) |
| **2** | **추출 파이프라인 인접 문항 혼입 회귀 방지** | 본 cleanup 전의 `steps[인식]` 자인 문구("변압기 문제가 아닌 유도 전동기 문제입니다")가 디버그 단서로 git history(`961291e^`)에 보존. 동일 패턴 재발 방지 | 우선순위 승격 |
| 3 | v3.2 §5.2 셀 오류 v3.3 정정 | §5.2 기기 row A17/B10 / 전력 row A8/B3 정정 + §5.3 cell 단위 검증 | 우선순위 유지 |
| 4 | B-priority full expansion | **보류** — B-pool 한계 (reserve 5항 소진 / 회로 커버리지 0) | 보류 유지 |

기기-17 cleanup이 완료되면 **B-pilot 완전 클린 36/41 (전 항목) 도달** 가능 — 본
erratum 이후의 최종 정합 목표.

---

## 6. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 기기-18 caution 해제 결정 | ✅ §2.1 — steps 잔존 결함 해소(Commit C) |
| 데이터 정합 재확인 (redryrun `1562390` 인용) | ✅ §2.2 |
| 판정 분류 재확인 (ready_with_note adjacent) | ✅ §2.3 |
| clean count 갱신 (caution 2/2 → 1/1, 완전 클린 34/39 → 35/40) | ✅ §3 |
| 사용 가능·blocked·A-priority·전체 합 불변 명시 | ✅ §3.3 |
| 학습자 사용 준비 상태 (36항 = 완전 클린 35 + caution 1) | ✅ §3.4 |
| 잔존 결함 logging 갱신 (steps 결함 해소 표기, 나머지 유지) | ✅ §4 |
| 다음 권장 트랙 갱신 (기기-18 steps 완료, 기기-17 우선순위 승격) | ✅ §5 |
| 이전 follow-up(`c6d57d0`)·closeout(`3f2a840`)·이전 erratum 원문 amend 없음 | ✅ docs/audit/ 신규 1건만 |
| 데이터·학습 패키지 미수정 | ✅ |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps·학습 패키지·이전 follow-up/closeout 원문 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## 7. 결론 및 다음 단계

- **기기-18 caution → 완전 클린 전환** 확정.
- B-pilot **완전 클린 35/40**, caution 1/1 (기기-17만), blocked 0/0, 사용 가능 36/41.
- 본 erratum v2가 이전 follow-up(`c6d57d0`)의 기기-18 상태를 갱신하며, 이전 erratum·
  closeout 원문은 수정하지 않고 본 v2가 최신 상태 source.
- **다음 트랙 우선순위 (갱신)**:
  1. 기기-17 PDF 대조 및 cleanup feasibility (완료 시 완전 클린 36/41 도달)
  2. 추출 파이프라인 인접 문항 혼입 회귀 방지
  3. v3.2 §5.2 셀 오류 v3.3 정정
  4. B-priority full expansion (보류, B-pool 한계)

(이 문서는 follow-up erratum v2다. 데이터·학습 패키지·이전 erratum/closeout 원문
미수정.)

---

## Status

- 기기-18 correction follow-up erratum v2 작성 완료 — Commit C(`961291e`) + redryrun
  (`1562390`) 반영.
- 기기-18 **caution → 완전 클린 전환**. steps 잔존 결함 해소 + 데이터 모든 필드
  정합 + 판정 ready_with_note(adjacent) 유지.
- clean count: 완전 클린 **34/39 → 35/40** (+1/+1), caution **2/2 → 1/1** (기기-17만
  잔존), 사용 가능 36/41 / blocked 0/0 / A-priority 26/31 불변.
- commit chain 16개 누적 (feasibility `1061a9f` → 본 v2).
- 다음 권장: 1순위 **기기-17 PDF 대조 및 cleanup** (완료 시 완전 클린 36/41 도달
  가능), 2 추출 파이프라인 회귀, 3 v3.2 §5.2 v3.3, 4 B-priority full expansion
  보류.
- 이 문서는 follow-up erratum v2다. 데이터·학습 패키지·closeout/이전 erratum
  원문 amend 없음.
