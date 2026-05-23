# Trap-Map B-Priority — 기기-18 Redryrun After Steps Cleanup (2026-05-23)

Commit C(`961291e`)로 `2010_2회_47.steps`를 `null`로 정리한 뒤의 기기-18 재검증.
post-closeout errata follow-up(`c6d57d0`)이 기기-18 caution 사유로 식별했던
steps 잔존 결함이 해소됐는지, 그에 따른 clean count 갱신 가능 여부를 검증한다.

본 단계는 검증 문서만 — app/data·questions.json 추가 수정 없음. 학습 패키지·
follow-up erratum 미수정. solution/answer/choices/text 미수정. 유료 API 미호출.
local server 미실행. amend/rebase/reset 없음.

- 검증 대상: 기기-18 변압기 등가회로 / 대표 기출 `2010_2회_47`
- 참조:
  - Commit C(`961291e`) — steps=null 정리
  - Commit C evidence supplement (`docs/audit/trap_map_B_priority_gigi_18_commitC_evidence_supplement_2026-05-23.md`)
  - steps cleanup feasibility (`docs/audit/trap_map_B_priority_gigi_18_steps_cleanup_feasibility_2026-05-23.md`)
  - 정정 후 1차 redryrun (`docs/audit/trap_map_B_priority_gigi_18_redryrun_after_correction_2026-05-23.md`)
  - official answer verification (`docs/audit/trap_map_B_priority_gigi_18_official_answer_verification_2026-05-22.md`)
  - post-closeout errata follow-up (`docs/audit/trap_map_B_priority_gigi_18_correction_followup_erratum_2026-05-23.md`)
  - 원본 PDF `data/문제_2010_2회_20260316.pdf` page 8 문제 47

---

## 결론: **ready_with_note (adjacent) — 데이터 완전 클린, caution 해제 가능**

Commit C로 steps 잔존 결함이 해소되어 `2010_2회_47` 레코드의 **모든 필드**가
원본 PDF·corpus schema와 정합. follow-up erratum이 caution 사유로 지목한 데이터
잔존 결함은 0건이 되었다.

판정은 **ready_with_note (adjacent)** — 데이터 측 PASS, alignment가 adjacent
인 1차 redryrun 분류는 자체적으로 ready_with_note 노트를 동반한다(adjacent 함정
분리 학습 필요는 데이터 결함이 아닌 학습 가이드 사항).

→ clean count 갱신 제안: 기기-18 **caution → 완전 클린**. caution 2/2 → 1/1
(기기-17만 잔존), 완전 클린 34/39 → 35/40, 사용 가능 36/41 불변. (실제 갱신은
별도 follow-up erratum에서 — 본 문서는 제안까지.)

---

## 1. questions.json 현재 상태 (직접 조회)

`app/data/questions.json` HEAD(`6f62da1`) 시점의 `2010_2회_47` 레코드:

| 필드 | 값 | 정정 경로 |
|---|---|---|
| year / session / q_no | 2010 / "2회" / 47 | unchanged |
| subject | "전기기기" | unchanged |
| tag | "변압기의 등가회로" | unchanged |
| q_type | "개념형" | unchanged |
| difficulty | 3 | unchanged |
| quality | "complete" | unchanged |
| text | "변압기의 무부하시험，단락시험에서 구할 수 없는 것은？" | unchanged |
| choices[0..2] | "철손" / "전압 변동률" / "동손" | unchanged |
| choices[3] | **"절연내력"** | Commit A(`6218d85`) |
| answer | **4** | Commit A(`6218d85`) |
| solution | (§1.1 — PDF 풀이 정합 194자) | Commit B(`753a9b2`) |
| **steps** | **null** | **Commit C(`961291e`) — 본 단계 신규 적용** |
| solution_svg | 3,243자 ("정답: ④ 절연내력" 포함) | unchanged |

### 1.1 solution 전문 (현재 상태)

```
변압기의 시험
（1）개방 회로 시험（무부하 시험）으로 측정할 수 있는 항목
－무부하 전류－히스테리시스손－와류손
－여자 어드미턴스－철손
（2）단락 시험으로 측정할 수 있는 항목
－임피던스 와트（전부하 동손）－임피던스 전압（전압 강하）

그러나，절연내력은 절연재의 종류에 따라 정해지는 것으로서 무부하 시험과 단락시험으로는 구할 수 없다．
［답］（4）
```

### 1.2 solution_svg 상태 (정정 없이 이미 정합)

`solution_svg`는 Commit A/B/C 전부터 이미 "정답: ④ 절연내력" 박스와 "변압기
등가회로 시험 항목" 제목으로 정답 (4)에 정합하게 작성돼 있었음(`decaa99` §1
보고). 본 단계까지 미수정 — answer 정정 결과(4)와 자연 정합.

---

## 2. 오염 제거 확인

### 2.1 Part 2 markers (record 전체 — solution + steps + 다른 필드 포함)

| 마커 | 레코드 전체 (`json.dumps(q)`) 내 존재? |
|---|---|
| `483000` | False |
| `유도 전동기` | False |
| `회전수는` | False |
| `문제 \(` | False |
| `전부하 회전수` | False |

→ **5종 마커 전부 0 hits**. 레코드 어느 필드(solution·steps·solution_svg 등)에도
문제 48 흔적 없음. Commit B(solution Part 2 제거) + Commit C(steps null) 결합
효과로 record-level 완전 제거 확인.

### 2.2 solution OCR garble 확인 (Commit B 정합 재확인)

| 이전 OCR garble | solution 내 존재? |
|---|---|
| `시혐` | False |
| `히스태리시스솜` | False |
| `철솜` | False |
| `무부 하 시험` | False |

→ Commit B 정정 결과 그대로 유지.

---

## 3. 원본 PDF 정합

| 항목 | 원본 PDF 문제 47 | questions.json 현재 | 정합 |
|---|---|---|---|
| text | "변압기의 무부하시험, 단락시험에서 구할 수 없는 것은?" | "변압기의 무부하시험，단락시험에서 구할 수 없는 것은？" | ✅ |
| choice [1] | "철손" | "철손" | ✅ |
| choice [2] | "전압 변동률" | "전압 변동률" | ✅ |
| choice [3] | "동손" | "동손" | ✅ |
| choice [4] | "절연내력" | "절연내력" | ✅ |
| 정답 | ④ | 4 | ✅ |
| 풀이 | 무부하시험 측정 항목·단락시험 측정 항목·절연내력 별도 + [답] ④ | (§1.1 solution 전문) | ✅ (절별 1:1 매핑) |

→ text·choices·answer·solution 4 필드 모두 PDF 정합 (Commit A·B 결과 유지).

PDF 풀이 키워드 6종 (변압기의 시험·히스테리시스손·철손·절연내력·［답］（4）·
무부하 시험) 전부 solution 내 present 재확인.

---

## 4. Schema 정합

### 4.1 `steps == null`이 corpus schema상 허용 상태인가

| corpus `steps` 값 타입 (5,331 records 전수) | Pre-Commit-C | Post-Commit-C |
|---|---|---|
| dict (객체) | 5,262 | 5,261 |
| **`null`** | **69** | **70 (+1)** |

`null`은 corpus 내 인정된 schema 옵션(69 → 70 레코드, 1.3%). 본 commit으로 그
선례에 1 추가. schema 정합.

### 4.2 `q_type=개념형`과 `steps=null`의 정합성

- `q_type: '개념형'` — 개념·분류 학습 문항. 수치 계산 단계 없음.
- `{인식, 변환, 계산}` schema — 계산형 문제 친화.
- 개념형 + 단락 풀이 → `steps=null`이 자연스러운 매칭. feasibility(`71f0082`)
  §3에서 확인된 그대로.
- 다른 개념형 + steps=null 레코드의 존재는 본 문서에서 전수 스캔하지 않으나,
  null 69 → 70 분포 자체가 schema 정합 충분 증거.

→ 충돌 없음. steps=null이 q_type=개념형과 정합.

### 4.3 다른 필드 schema 무결성

- `text`·`choices` (array of 4 strings)·`answer` (int)·`solution` (string)·
  `solution_svg` (string)·`difficulty` (int)·`q_type` (string)·`tag` (string)·
  `subject` (string)·`quality` (string) — 전부 표준 타입.
- JSON parse 성공, 5,331 records 유지. 구조 무결.

---

## 5. Trap Alignment 재판정

### 5.1 입력

- **v3.2 기기-18 카드 원래 함정**: "1차 환산값과 2차 실제값을 혼동하는 보기"
  (1차/2차 환산 혼동).
- **대표 기출이 검증하는 함정**: "무부하시험·단락시험에서 구할 수 없는 것?" →
  절연내력. 시험 범위 식별 — 절연내력은 두 시험으로 구할 수 없음.

### 5.2 정정 후 1차 redryrun(`39be9d9`)과 비교

`39be9d9` §3.3에서 이미 판정: **adjacent** — 정답(2)→(4) 변경으로도 검증 축
(시험-측정 매핑·범위 식별)이 동일하게 adjacent. Commit C(steps cleanup)는 *데이터
무결성*을 추가 보강했을 뿐 trap alignment 분류와 무관.

→ **adjacent 유지**. 1차 redryrun 판정과 동일.

### 5.3 두 함정의 관계 (재확인)

| 측면 | 원래 카드 함정 | 대표 기출이 검증하는 함정 |
|---|---|---|
| 주제 | 변압기 등가회로 (1차↔2차 환산 일관성) | 변압기 시험 (시험 범위 식별) |
| 검증 메커니즘 | 환산값/실제값 혼동 보기 식별 | 시험 범위 밖 항목(절연내력) 식별 |
| 같은 광역 주제 | 둘 다 변압기 등가회로 단원 | 같은 단원의 인접 하위 함정 |
| 분류 | adjacent | adjacent |

---

## 6. 판정: **ready_with_note**

| 평가 축 | 결과 | 사유 |
|---|---|---|
| text·choices·answer·solution PDF 정합 | ✅ PASS | §3 |
| OCR garble 제거 (Commit B 결과 유지) | ✅ PASS | §2.2 |
| Part 2 혼입 record-level 제거 | ✅ PASS | §2.1 (5종 마커 0) |
| 정답 ↔ solution 내적 일관성 | ✅ PASS | answer=4 + solution [답](4) |
| solution_svg 정답 정합 | ✅ PASS | "정답: ④ 절연내력" 포함 |
| **steps 필드 정합** | **✅ PASS** | **steps=null, corpus schema 정합 (1차 redryrun에서 FAIL했던 항목 해소)** |
| trap alignment | adjacent | §5 — 1차 redryrun과 동일 |

### 판정 사유

- 데이터 모든 필드 정합 — 1차 redryrun에서 ready_with_note 사유였던 두 가지 중
  **"steps 필드 잔존"은 해소**, **"adjacent 함정 분리 학습 필요"만 잔존**.
- adjacent 함정 분리 학습 필요는 *학습 가이드 사항*(데이터 결함 아님). 1차
  representative re-dryrun 프레임워크에서 adjacent 항목은 일관되게 ready_with_note
  분류.
- needs_replacement 아님 (모든 PASS).
- defer 아님 (검증 완료, 후속 작업 경로 명확).

→ **판정: ready_with_note (adjacent)**. 1차 redryrun과 동일한 분류이나, 노트 사유
2개 중 1개(steps 잔존)가 해소되어 **유일한 노트 사유 = adjacent 학습 분리**로
축소.

### 1차 redryrun(`39be9d9`)과의 비교

| 항목 | 1차 redryrun(`39be9d9`) 시점 | 본 redryrun(post Commit C) |
|---|---|---|
| 판정 | ready_with_note | ready_with_note |
| 노트 사유 | (a) adjacent 함정 분리 + (b) steps 잔존 | (a) adjacent 함정 분리 (b 해소) |
| 데이터 결함 | steps 필드 잔존 | 없음 |
| trap alignment | adjacent | adjacent |

판정 라벨 동일, 노트 사유 1건 감소(데이터 결함 0).

---

## 7. Clean Count 영향 (제안)

본 redryrun은 **제안만** — 실제 갱신은 별도 follow-up erratum에서 수행.

### 7.1 현재 (follow-up erratum `c6d57d0` 기준)

| 분류 | 항 / 문제 |
|---|---|
| A-priority (유지) | 26 / 31 |
| 사용 가능 | 36 / 41 |
| └ 완전 클린 (caution·blocked 제외) | 34 / 39 |
| └ 기기-17 caution | 1 / 1 (choices/solution cleanup residual) |
| └ 기기-18 caution | 1 / 1 (**steps 필드 혼입 residual**) ← 본 redryrun으로 해소 후보 |
| blocked | 0 / 0 |

### 7.2 본 redryrun 이후 제안 갱신

| 분류 | 항 / 문제 |
|---|---|
| A-priority (유지) | 26 / 31 |
| 사용 가능 | 36 / 41 (불변) |
| └ **완전 클린** | **35 / 40 (+1/+1)** |
| └ 기기-17 caution | 1 / 1 (잔존) |
| └ 기기-18 caution | **0 / 0 (−1/−1) → 완전 클린으로 전환** |
| blocked | 0 / 0 (불변) |

### 7.3 변동 요약

| 변동 | 현재 | 제안 후 |
|---|---|---|
| 기기-18 분류 | caution 1/1 | 완전 클린 (전환) |
| 완전 클린 합 | 34 / 39 | **35 / 40** |
| caution 합 | 2 / 2 | **1 / 1** (기기-17만) |
| 사용 가능 합 | 36 / 41 | 36 / 41 (불변) |
| blocked 합 | 0 / 0 | 0 / 0 |
| A-priority | 26 / 31 | 26 / 31 (불변) |
| 전체 합 | 36 / 41 | 36 / 41 (불변) |

→ "기기-18 caution → 완전 클린" 단일 변동. caution은 기기-17(choices/solution
cleanup residual)만 잔존. blocked 0/0 유지. 학습자 사용 준비 상태는 더 청결해짐.

### 7.4 caution 해제 정당성 정리

| follow-up erratum의 기기-18 caution 사유 | 본 redryrun 시점 상태 |
|---|---|
| `steps` 필드 문제 48 혼입 잔존 | ✅ 해소 — Commit C `961291e`로 `steps=null` |
| 학습 docs는 steps 직접 노출 안 함 (영향 미미) | 학습 영향은 미미했지만 데이터 결함 자체가 caution 사유였음. 데이터 결함 해소로 caution 사유 소멸 |

→ caution 해제 정당. 단 alignment adjacent로 인한 ready_with_note 판정 자체는
유지(학습 가이드 사항).

---

## 8. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. questions.json 현재 상태 (answer/choices/solution/steps/svg) | ✅ §1 |
| 2. 오염 제거 (Part 2 5종 marker 0 / OCR garble 4종 0) | ✅ §2 |
| 3. 원본 PDF 정합 (text/choices/answer/solution) | ✅ §3 |
| 4. schema 정합 (steps=null corpus 70 선례 / 개념형 정합 / 다른 필드 무결) | ✅ §4 |
| 5. trap alignment 재판정 (adjacent 유지) | ✅ §5 |
| 6. 판정 (ready_with_note) | ✅ §6 — 1차 redryrun과 동일 라벨, 노트 사유 2 → 1 |
| 7. clean count 영향 제안 (caution 해제 가능 / 완전 클린 34/39 → 35/40 / caution 2/2 → 1/1) | ✅ §7 — 제안만 |
| follow-up erratum 갱신 미실행 | ✅ §7 — 제안까지 |
| app/data·questions.json 추가 수정 없음 | ✅ docs/audit/ 신규 1건만 |
| 학습 패키지·closeout/errata 미수정 | ✅ |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps·학습 패키지·closeout/errata 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- 기기-18 `2010_2회_47` Commit C 이후 redryrun 검증 완료 — 데이터 완전 클린.
- text·choices·answer·solution·steps·solution_svg 6개 데이터 필드 전부 원본 PDF·
  corpus schema와 정합. Part 2 마커 5종·OCR garble 4종 모두 record-level 0 hits.
  steps=null로 corpus 70개 null 레코드 선례에 합류.
- trap alignment: **adjacent** (유지). 1차 redryrun(`39be9d9`)과 동일 분류.
- 판정: **ready_with_note (adjacent)** — 1차 redryrun과 동일 라벨. 노트 사유
  2개("adjacent 학습 분리" + "steps 잔존") 중 steps 잔존 해소로 **유일한 노트
  사유 = adjacent 학습 분리**.
- B-pilot **caution 해제 가능 제안**: 기기-18 caution 1/1 → 완전 클린 (전환).
  완전 클린 34/39 → 35/40, caution 2/2 → 1/1 (기기-17만 잔존). 사용 가능 36/41
  / blocked 0/0 / A-priority 26/31 불변. 실제 갱신은 별도 follow-up erratum.
- 다음 단계: follow-up erratum 갱신(별도 명시 승인 필요) → clean count 공식 갱신.
- 이 문서는 redryrun 검증 문서다. questions.json·학습 패키지·closeout/errata
  미수정.
