# Trap-Map B-Priority — 기기-18 Correction Follow-Up Erratum (2026-05-23)

correction plan(`d1ca5b2`) Step 7 — questions.json 정정(Commit A `6218d85` /
Commit B `753a9b2`) + 학습 패키지 정정(Step 5 `6051e21`) + 리뷰 PASS(`ec39ce9`)
이후의 **post-closeout errata 후속 erratum**이다. 기기-18 blocked 해제 여부 결정,
B-pilot clean count 갱신, 잔존 결함·다음 트랙 정리를 한다.

본 단계는 상태 정리 문서 작성만 — **실제 data/doc 수정 없음**. app/data·
questions.json·학습 패키지·closeout/post-closeout errata 원문 미수정. solution/
steps 미적용. answer/choices/text 미수정. 유료 API 미호출. local server 미실행.
amend/rebase/reset 없음.

- 참조:
  - B-pilot closeout (`docs/audit/trap_map_B_priority_pilot_learning_package_closeout_2026-05-22.md`)
  - post-closeout errata (`docs/audit/trap_map_B_priority_post_closeout_errata_2026-05-22.md`)
  - cleanup feasibility review (`docs/audit/trap_map_B_priority_cleanup_feasibility_review_2026-05-22.md`)
  - official answer verification (`docs/audit/trap_map_B_priority_gigi_18_official_answer_verification_2026-05-22.md`)
  - correction plan (`docs/audit/trap_map_B_priority_gigi_18_correction_plan_2026-05-23.md`)
  - Commit A evidence supplement (`docs/audit/trap_map_B_priority_gigi_18_commitA_evidence_supplement_2026-05-23.md`)
  - Commit B evidence supplement (`docs/audit/trap_map_B_priority_gigi_18_commitB_evidence_supplement_2026-05-23.md`)
  - redryrun after correction (`docs/audit/trap_map_B_priority_gigi_18_redryrun_after_correction_2026-05-23.md`)
  - learning materials correction review (`docs/audit/trap_map_B_priority_gigi_18_learning_materials_correction_review_2026-05-23.md`)

---

## 결론

- **기기-18 blocked 해제**. 데이터(questions.json)와 학습 패키지가 모두 공식
  정답 (4) 절연내력 기준으로 정정 완료, redryrun 및 학습 materials correction
  review 모두 PASS.
- **기기-18은 완전 clean이 아니라 caution으로 분류**. 사유: `steps` 필드에 문제
  48(유도전동기 회전수) 내용이 잔존 — 별도 cleanup 트랙(외부 결함, 학습 자체에는
  영향 미미).
- **B-pilot 사용 가능: 35/40 → 36/41**. 완전 클린 34/39, caution 2/2(기기-17 +
  기기-18), blocked 0/0.

post-closeout errata(`0045ce4`)의 "기기-18 blocked"는 본 erratum으로 **caution
1항/1문제로 전환**한다. closeout(`3f2a840`)·post-closeout errata 원문은 수정하지
않고, 본 follow-up이 정정 기록의 최신 상태를 보유한다.

---

## 1. 정정 트랙 요약 (Commit Chain)

| 순번 | Commit | 단계 | 내용 |
|---|---|---|---|
| 1 | `1061a9f` | feasibility review | 기기-18 answer 충돌·choice OCR·solution 혼입 escalation |
| 2 | `0045ce4` | post-closeout errata | 기기-18 blocked로 분류, B-pilot 9항 체계로 정정 |
| 3 | `decaa99` | official answer verification | 원본 PDF 대조로 공식 정답 (4) 절연내력 확정 |
| 4 | `d1ca5b2` | correction plan | Step 1~7 + 옵션 S2 + commit 분리 + 위험 관리 |
| 5 | `6218d85` | Commit A (data) | `answer` 2→4 / `choices[3]` "철손내력"→"절연내력" |
| 6 | `cc46d66` | Commit A evidence supplement | G-1/G-2/G-3 보강 + git 재구성 snapshot |
| 7 | `753a9b2` | Commit B (data) | `solution` cleanup — Part 2(문제 48 혼입) 제거 + OCR 미세 정리 (옵션 S2) |
| 8 | `6f825fa` | Commit B evidence supplement | 변경 단위별 source label + PDF 절별 매핑 |
| 9 | `39be9d9` | redryrun after correction | 정정 후 데이터 정합 PASS, 판정 ready_with_note / adjacent |
| 10 | `6051e21` | learning materials correction | study set v1 / day plan / learning log v1.1 기기-18 카드 (4) 절연내력 기준 정정 |
| 11 | `ec39ce9` | learning materials correction review | Step 5 정정 6 기준 검토, PASS, P0/P1/P2 0 |
| 12 | (본 문서) | follow-up erratum | blocked 해제 → caution 전환, clean count 갱신, 다음 트랙 정리 |

---

## 2. 기기-18 상태 결정

### 2.1 blocked 해제 근거

| blocked 사유 (post-closeout errata `0045ce4`) | 정정 후 상태 |
|---|---|
| `answer` 필드(2) ↔ 공식 정답(4) 충돌 | ✅ 해소 (Commit A `6218d85`) |
| `choices[3]` "철손내력" OCR garble | ✅ 해소 (Commit A `6218d85`) |
| solution 필드 Part 2(문제 48 유도전동기) 혼입 | ✅ 해소 (Commit B `753a9b2`) |
| solution 필드 미세 OCR garble (시혐·솜·무부 하) | ✅ 해소 (Commit B 옵션 S2) |
| 학습 패키지(study set v1·day plan·learning log v1.1) 정답 (2) 기준 학습 | ✅ 해소 (Step 5 `6051e21`) — (4) 절연내력 기준 정정 |
| redryrun 미수행 | ✅ 해소 (`39be9d9`) — ready_with_note / adjacent |
| 학습 materials correction review 미수행 | ✅ 해소 (`ec39ce9`) — PASS |

→ post-closeout errata가 제시한 blocked 사유 전부 해소. **blocked 해제**.

### 2.2 완전 clean이 아닌 caution으로 분류한 이유

`steps` 필드(인식·변환·계산 3 sub-key)는 여전히 **문제 48 유도전동기 회전수**
기준으로 작성된 상태이며 정정되지 않았다. 이는:

- correction plan(`d1ca5b2`) §3.2에서 명시적으로 **Commit A/B 범위 외**로 분리됨.
- redryrun(`39be9d9`) §1.4에서 잔존 결함으로 logging됨.
- 학습 materials correction review(`ec39ce9`) 기준 6에서 별도 트랙 명시 확인됨.

steps 필드는 questions.json 데이터 무결성 차원의 잔존 결함이며, 학습 패키지
카드는 questions.json의 steps를 직접 노출하지 않으므로 *학습 자체 영향은 미미*.
단 데이터 차원의 cleanup이 끝나지 않은 상태이므로 **caution** 분류가 정직하다.

→ 기기-18: **blocked 해제 + caution 분류** (사유: steps 필드 혼입 잔존).

### 2.3 alignment·판정 (재확인)

- alignment: **adjacent** (시험 범위 식별, 절연내력은 두 시험으로 구할 수 없음)
- 판정: **ready_with_note** (사유: adjacent 함정 분리 학습 + steps 필드 잔존)

---

## 3. Clean Count 갱신

### 3.1 갱신 전 (post-closeout errata `0045ce4`)

| 분류 | 항 / 문제 |
|---|---|
| A-priority (유지) | 26 / 31 |
| 확정 클린 (사용 가능, blocked 제외) | 35 / 40 |
| └ 기기-17 caution | 1 / 1 |
| 기기-18 blocked | 1 / 1 |
| 합계 | 36 / 41 |

### 3.2 갱신 후 (본 follow-up)

| 분류 | 항 / 문제 |
|---|---|
| A-priority (유지) | 26 / 31 |
| **사용 가능** | **36 / 41** (전 항목 사용 가능) |
| └ 완전 클린 (caution·blocked 제외) | 34 / 39 |
| └ 기기-17 caution | 1 / 1 (choices/solution cleanup residual) |
| └ 기기-18 caution | 1 / 1 (steps 필드 혼입 residual) |
| blocked | 0 / 0 |
| 합계 | 36 / 41 |

### 3.3 변동점 요약

| 변동 | 갱신 전 | 갱신 후 |
|---|---|---|
| 기기-18 분류 | blocked 1/1 | caution 1/1 |
| 사용 가능 합 | 35 / 40 | 36 / 41 (+1/+1) |
| blocked 합 | 1 / 1 | 0 / 0 (−1/−1) |
| caution 합 | 1 / 1 | 2 / 2 (+1/+1) |
| 완전 클린 합 | 34 / 39 (기기-17 caution만 제외) | 34 / 39 (기기-17·18 caution 둘 다 제외) |
| A-priority | 26 / 31 | 26 / 31 (불변) |
| 전체 합 | 36 / 41 | 36 / 41 (불변) |

→ "기기-18 blocked 1/1 → caution 1/1" 단일 변동. A-priority 및 전체 합은 불변.
완전 클린 합 34/39은 표면적으로 같지만 *구성 변화*가 있다 — 갱신 전엔 기기-18이
사용 가능 풀 자체에서 제외돼 "사용 가능" 분모가 35/40였고, 갱신 후엔 기기-18이
사용 가능 풀에 포함되되 caution으로 분류돼 분모가 36/41로 확대됐다.

### 3.4 학습자 사용 준비 상태

**"학습자 사용 준비 완료": 36항 사용 가능 (= 완전 클린 34 + caution 2)**.

caution 항목 사용 시 학습자에게 안내해야 할 사항:
- **기기-17 caution**: 보기 [1] LaTeX 잉여 √3 — 학습 자료 노출 전 `aV/√3`로 정리
  필요 (학습 패키지 docs는 이미 정확한 풀이 사용, app 표시 시 자료 변환 권장).
- **기기-18 caution**: questions.json `steps` 필드에 문제 48(유도전동기) 내용
  잔존 — 학습 패키지 docs(study set/day plan/learning log)는 정답 (4) 절연내력
  기준으로 재작성 완료. app에서 steps를 직접 노출하지 않으면 학습 영향 미미.
  app에서 steps 노출 시 학습자에게 "steps는 별도 cleanup 트랙 대기" 명시.

---

## 4. 잔존 결함 Logging

| 결함 | 위치 | 영향 | 처리 |
|---|---|---|---|
| 기기-17 보기 [1] LaTeX 잉여 √3 | `2020_1회_52` `choices[0]` | 학습 docs 영향 없음 (정확한 풀이 사용 중), app 표시 시 학습자 혼동 가능 | 기기-17 cleanup 트랙 |
| 기기-17 solution 필드 전류식 오류·결선 라벨 오기 | `2020_1회_52` `solution` | app 풀이 표시에만 영향 (학습 docs는 √3I/a 정확) | 기기-17 cleanup 트랙 |
| 기기-18 `steps` 필드 문제 48 혼입 | `2010_2회_47` `steps` (인식·변환·계산 3 sub-key) | 학습 docs 영향 없음 (steps 직접 노출 안 함), app에서 steps 노출 시 잘못된 풀이 표시 | **기기-18 steps cleanup 트랙** (본 erratum 신규 분리) |
| questions.json 추출 파이프라인 인접 문항 혼입 | 파이프라인 자체 | 향후 추출 작업에서 재발 가능 | 파이프라인 회귀 트랙 |
| v3.2 §5.2 셀 오류 (기기 A18/B9·전력 A7/B4) | trap-map source | B-pilot 영향 없음 (§4 본문 기반), 향후 canonical 사용 시 오도 가능 | v3.3 정정 트랙 |
| 회로 커버리지 0 / S/F 6/10 편중 / reserve 5항 소진 | B-pool 모집단 구조 | residual로 closeout에 이미 이월 | 미해결 — B-pool 자체 한계 |

---

## 5. 다음 권장 트랙

| 우선순위 | 트랙 | 내용 |
|---|---|---|
| 1 | **기기-18 steps cleanup feasibility/review** | `2010_2회_47` `steps`(인식·변환·계산)를 문제 47 기준으로 재작성하거나 비워둘지 feasibility 검토. PDF 풀이는 짧고 명시적 단계 구조가 없어 steps 필드의 적정 처리 방식 결정 필요. 완료 시 기기-18 caution → 완전 클린 전환 가능 |
| 2 | **기기-17 PDF 대조 및 cleanup feasibility** | `2020_1회_52` 원본 PDF 보기 [1] 공식 표기 확인 → choices[0] artifact·solution 전류식 정정 결정. 완료 시 기기-17 caution → 완전 클린 전환 가능 |
| 3 | **v3.2 §5.2 셀 오류 v3.3 정정** | §5.2 우선순위 분포 기기 row A17/B10 / 전력 row A8/B3로 정정 + §5.3 합 검증을 cell 단위로 확장. canonical 사용 전 보완 |
| 4 | **B-priority full expansion** | **보류** — reserve 5항 소진 / 회로 커버리지 0 (B-pool 한계). defer 풀(기기-7·26·설비-12·23·27·29) representative mapping을 targeted dryrun으로 완료 후 재검토 |

추출 파이프라인 회귀 트랙(인접 문항 혼입 재발 방지)은 우선순위 2~3 트랙 진행 중
또는 후에 별도 다루는 게 효율적.

---

## 6. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 기기-18 blocked 해제 결정 | ✅ §2.1 — post-closeout errata blocked 사유 7건 전수 해소 |
| 기기-18 caution 분류 + 사유 명시 (steps 잔존) | ✅ §2.2 |
| alignment(adjacent)·판정(ready_with_note) 재확인 | ✅ §2.3 |
| clean count 갱신 (사용 가능 35/40 → 36/41, caution +1, blocked -1) | ✅ §3 |
| 완전 클린 / caution / blocked 분류 정합 | ✅ §3.2 — 34 + 2 + 0 = 36, 39 + 2 + 0 = 41 |
| commit chain 12개 (feasibility → followup) 요약 | ✅ §1 |
| 잔존 결함 logging (기기-17·기기-18 steps·파이프라인·v3.2·B-pool) | ✅ §4 |
| 다음 권장 트랙 (steps cleanup / 기기-17 PDF / v3.3 / full expansion 보류) | ✅ §5 |
| closeout 원문·post-closeout errata 원문 amend 없음 (별도 follow-up 문서로 정정) | ✅ docs/audit/ 신규 1건만 |
| 데이터·학습 패키지 미수정 | ✅ 본 문서 작성 외 변경 없음 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps·학습 패키지·closeout/post-closeout errata 원문 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## 7. 결론 및 다음 단계

- **기기-18 blocked 해제 + caution 분류** 결정 확정.
- B-pilot 사용 가능 = **36 / 41** (완전 클린 34/39 + caution 2/2: 기기-17 + 기기-18).
- blocked 0 / 0.
- 본 erratum이 post-closeout errata(`0045ce4`)의 기기-18 상태를 갱신하며, 원문은
  수정하지 않고 본 follow-up이 최신 상태 source.
- **다음 트랙 우선순위**: 1 기기-18 steps cleanup, 2 기기-17 PDF 대조 cleanup,
  3 v3.2 §5.2 v3.3 정정, 4 B-priority full expansion (보류).

(이 문서는 follow-up erratum이다. 데이터·학습 패키지·closeout 원문 미수정.)

---

## Status

- 기기-18 correction plan Step 7 완료 — follow-up erratum 작성.
- 기기-18 **blocked 해제**, **caution 분류** (사유: steps 필드 혼입 잔존, 별도
  cleanup 트랙).
- alignment **adjacent** / 판정 **ready_with_note** (재확인).
- B-pilot clean count: 사용 가능 **35/40 → 36/41**, 완전 클린 **34/39** 불변,
  caution **1→2** (기기-17 + 기기-18), blocked **1→0**.
- A-priority 26항/31문제 변동 없음, 전체 합 36항/41문제 불변.
- Commit chain 12개 (feasibility `1061a9f` → 본 follow-up) 요약 완료.
- 다음 권장: 기기-18 steps cleanup → 기기-17 PDF 대조 → v3.2 §5.2 v3.3 정정
  → B-priority full expansion 보류.
- 이 문서는 follow-up erratum이며, post-closeout errata(`0045ce4`)의 기기-18
  상태를 갱신한다. closeout/post-closeout errata 원문 amend 없음.
