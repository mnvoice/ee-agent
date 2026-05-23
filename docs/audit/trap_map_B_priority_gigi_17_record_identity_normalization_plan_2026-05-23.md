# Trap-Map B-Priority — 기기-17 Record Identity Normalization Plan (2026-05-23)

기기-17 cleanup feasibility(`2bfc065`)에서 발견된 **record 메타 식별 오류 (C)**를
해소하기 위한 plan 문서다. 실제 data 수정 전에 조사·정정 범위·전략·검증·실행
순서를 명문화한다.

본 단계는 plan 작성까지 — **app/data·questions.json·학습 패키지 미수정.
id/year/session/q_no 미수정. answer/choices/text/solution/steps 미수정.** 유료
API 미호출. local server 미실행. amend/rebase/reset 없음.

- 참조:
  - 기기-17 cleanup feasibility (`docs/audit/trap_map_B_priority_gigi_17_cleanup_feasibility_2026-05-23.md`)
  - steps cleanup follow-up erratum (`docs/audit/trap_map_B_priority_gigi_18_steps_cleanup_followup_erratum_2026-05-23.md`)
  - 1차 cleanup feasibility review (`docs/audit/trap_map_B_priority_cleanup_feasibility_review_2026-05-22.md`)
  - representative re-dryrun (`docs/audit/trap_map_B_priority_10_item_representative_redryrun_2026-05-22.md`)
  - study set v1 (`docs/audit/trap_map_B_priority_pilot_study_set_v1_2026-05-22.md`)
  - 원본 PDF `data/문제_2020_1,2회_20260316.pdf` page 19

---

## 1. 문제 정의

### 1.1 발견된 불일치

`questions.json`의 `2020_1회_52` 식별자가 원본 PDF 2020년 1회 52번과 다른
문제를 가리킨다. 같은 PDF 문제는 corpus 내 `2020_1,2회_52` 식별자로 별도 저장돼
있다.

| 식별자 | session 라벨 | 본문 주제 | answer | PDF 정합 |
|---|---|---|---|---|
| `2020_1회_52` | "1회" | 권수비 a 단상변압기 3대 / 1차△·2차Y | 1 | ✗ PDF 2020년 1회 52와 불일치 |
| `2020_1,2회_52` | "1,2회" | 동기전동기 V곡선 / 여자전류 | 1 | ✅ PDF 2020년 1회 52와 정합 |
| `2020_3회_52` | "3회" | IGBT (제어공학) | 3 | (별개 — 2020년 3회 52) |

### 1.2 학습 패키지의 대표 기출 표기 신뢰성

B-priority study set v1 / day plan / learning log v1.1의 기기-17 카드는 대표
기출을 **`2020_1회_52`**로 명시한다. 본문(권수비 △-Y) 자체는 유효한 기기-17
representative이나, 그 id의 원본 PDF 출처는 PDF 2020년 1회 52(동기전동기 V곡선)
이므로 학습자가 PDF로 cross-check 시 불일치를 발견한다.

### 1.3 systemic 양상 — 본 case는 isolated가 아님

corpus 전수 분석:

| 측정 | 값 |
|---|---|
| 전체 레코드 | 5,331 |
| `session = "1,2회"` 레코드 수 | 66 |
| year+q_no가 다중 session 라벨을 갖는 case | 1,819 |
| 그 중 "1,2회" 라벨이 포함된 case | **66 cases** |

→ "1회"와 "1,2회" 두 session 라벨이 같은 year+q_no를 두고 공존하는 패턴이
**최소 66 case 존재**. 본 기기-17 case(2020 q52)는 그 중 한 사례에 불과 —
**systemic 추출 파이프라인 양상**.

---

## 2. Known Facts

### 2.1 원본 PDF — 2020년 1회 문제 52

`data/문제_2020_1,2회_20260316.pdf` PDF page 19 직접 인용:

```
문제 52  동기전동기의 공급 전압과 부하를 일정하게 유지하면서 역률을 1로
운전하고 있는 상태에서 여자 전류를 증가시키면 전기자 전류는?
 ① 앞선 무효전류가 증가
 ② 앞선 무효전류가 감소
 ③ 뒤진 무효전류가 증가
 ④ 뒤진 무효전류가 감소
[답] ①
```

### 2.2 questions.json `2020_1회_52` 현재 내용

- subject: 전기기기 / tag: "변압기의 권수비 및 전압비" / q_type: 개념형 / difficulty: 4
- text: "권수비가 a인 단상변압기 3대가 있다. 이것을 1차에 △, 2 차에 Y로 결선하여..."
- choices: 4지 LaTeX 전압·전류 식
- answer: 1
- solution: V1 = aV/√3 (정합) / I1 = I/(√3a) (물리값 √3I/a와 어긋남, 결선 라벨 "Y-△" 오기)
- steps: {인식, 변환, 계산} 모두 △-Y 권수비 풀이 (solution과 동일 전류식 오류)
- solution_svg: 4,213자, aV/√3 포함

→ 본문 = 권수비 △-Y / answer = 1 (choice [1] 잉여 √3 제거 시 물리 정답과 정합).

### 2.3 questions.json `2020_1,2회_52` 현재 내용

- subject: 전기기기 / tag: "동기발전기의 전기자반작용과 동기전동기의 전기자반작용"
- text: "동기전동기의 공급 전압과 부하를 일정하게 유지하면서 역률을 1 로 운전하고
  있는 상태에서 여자 전류를 증가시키면 전기자 전류는?"
- answer: 1

→ 본문 = 동기전동기 V곡선 / answer = 1. **PDF 2020년 1회 52와 text·answer 정합.**

### 2.4 정합 매트릭스

| PDF 출처 | 본문 정합 questions.json 레코드 | 메타 라벨 정합 | 종합 |
|---|---|---|---|
| PDF 2020년 1회 52 (V곡선) | `2020_1,2회_52` | ✗ (session "1,2회"가 "1회"여야) | 본문 ✓ / 라벨 부분 불일치 |
| 미상 (권수비 △-Y) | `2020_1회_52` | ✗ (이 id 자체가 PDF 2020 1회 52 아님) | 본문 ✓ valid 권수비 기출 / 라벨 ✗ |

→ "1,2회" 라벨이 본래 "1회"(또는 "2회") 추출분을 담는 임시 라벨이었을 가능성.
"권수비 △-Y" 본문이 어떻게 `2020_1회_52` id로 들어왔는지는 추출 단계 logs 부재로
미상.

---

## 3. 영향 범위

### 3.1 B-priority 학습 패키지

| 산출물 | 기기-17 참조 위치 | 영향 |
|---|---|---|
| `trap_map_B_priority_pilot_study_set_v1_2026-05-22.md` | 기기-17 카드 — "대표 기출: `2020_1회_52` (정답 1)" | 표기 신뢰성 — id ↔ PDF 불일치 |
| `trap_map_B_priority_pilot_day_plan_2026-05-22.md` | 동일 | 동일 |
| `trap_map_B_priority_pilot_learning_log_v1_1_2026-05-22.md` | 동일 + 6칸 학습 로그 | 동일 (학습 본문은 유효) |

### 3.2 검증·플로우 문서

| 문서 | 참조 위치 | 영향 |
|---|---|---|
| 1차 representative re-dryrun (`6164d6f`) | `2020_1회_52` 검증 표 | 본문 기반 alignment 판정(exact)은 유효, id 라벨 신뢰성은 본 plan에서 escalate |
| 1차 cleanup feasibility review (`1061a9f`) | choice/solution caution 식별 | 부분 캡처 (메타 식별 오류 미식별) |
| 본 기기-17 cleanup feasibility (`2bfc065`) | 메타 식별 오류 escalation | 본 plan의 입력 |
| closeout / post-closeout errata / followup erratum | 기기-17 caution 분류 | caution 사유 강화 필요 (cleanup feasibility §6.3) |

### 3.3 questions.json 메타 (id 차원)

- record key = (year, session, q_no) 조합. 본 case는 (2020, "1회", 52)에 잘못된
  본문이 attached.
- 정정 전략에 따라 record 분리/병합/삭제·재이입 가능 — §4 옵션 비교.

### 3.4 app/ 코드의 question id 의존성

- `app/` 디렉토리 구조 확인: `index.html`, `js/` (bundle.js, store.js, render.js,
  main.js, study.js), `data/questions.json` 등.
- 다수의 JS 파일이 `questions.json`을 참조하는 것으로 보임 (grep로 확인).
- **app 코드가 record id를 어떻게 key로 사용하는지 본 plan 단계에서는 미탐색** —
  §6 추가 검증 항목으로 남김. id 변경 시 app routing/url에 영향이 있는지는 변경
  실행 전에 반드시 확인해야 함.

### 3.5 systemic 영향 (66 case)

본 기기-17 case 외에 65개의 다른 year+q_no가 동일 "1,2회 + 1회" 공존 패턴을
가짐. normalization 전략이 본 case에 한정할지, corpus 전체에 적용할지는 별도
정책 결정 사항 (§5 권장안 참조).

---

## 4. Normalization 전략 옵션

| 옵션 | 내용 | 장점 | 단점 / 위험 | 수정 범위 |
|---|---|---|---|---|
| **A. 학습 패키지 표기만 정정** | 학습 카드의 "대표 기출 id"를 true source 식별자로 갱신. questions.json 메타 자체는 미수정 | 데이터 변경 0, app 영향 0, low-risk | true source가 미확정인 상태에서는 id를 무엇으로 적을지 결정 불가. data 차원의 메타 오류 잔존 | 학습 패키지 3 docs / 기기-17 카드만 |
| **B. questions.json 메타 정정** | `2020_1회_52` record의 year/session/q_no를 true source로 갱신, 또는 record 삭제 후 올바른 id로 재이입 | data 차원의 메타 오류 해소 | (1) id 변경이 app routing에 영향 가능 — §3.4 확인 필요. (2) true source 미확정. (3) `2020_1,2회_52`도 함께 정리해야 일관됨 (1회로 통합) | questions.json 1~2 records + 학습 패키지 표기 동기 + (app 영향 확인 시) app 코드 |
| **C. duplicate alias / errata 명시** | record는 그대로 두고, `2020_1회_52`가 실제 PDF 출처 다름을 alias 또는 errata table로 명시 (예: docs에 mapping table) | 데이터 변경 최소, 추적성 확보 | 메타 오류 자체는 잔존 — 영구 정정 아닌 문서화 우회. caution 해제 어려움 | docs(alias table) + 학습 패키지 cross-reference |
| **D. 기기-17 representative 교체** | 권수비 △-Y 본문 대신 다른 record(예: 다른 연도의 동일 trap representative)를 기기-17 학습 카드 대표 기출로 채택 | 메타 오류 record를 우회. caution 해제 명확 가능 | redryrun·study set·day plan·learning log 재작성 필요 (Step 5와 동등한 작업). 기존 B-pilot 게이트 재수행 필요 | 학습 패키지 3 docs / 기기-17 카드 + redryrun 재수행 |

### 4.1 위험 매트릭스

| 옵션 | 데이터 변경 | app 영향 | 학습 패키지 변경 | 게이트 재수행 | 메타 정합 회복 | 추적성 |
|---|---|---|---|---|---|---|
| A | 없음 | 없음 | 최소 (id 표기만) | 없음 | 부분 (학습 시점) | 보통 |
| B | 있음 (id 변경) | 가능 | 동기 갱신 | 부분 (redryrun) | 완전 | 좋음 |
| C | 없음 | 없음 | 없음 + alias docs 추가 | 없음 | 없음 (문서화 우회) | 우수 (명시적) |
| D | 없음 | 없음 | 카드 재작성 + 게이트 재수행 | 있음 (redryrun + review) | 우회 (다른 record) | 좋음 |

---

## 5. 권장안

### 5.1 즉시 권장: **C를 임시 적용 + A 또는 B 결정 트랙 분리**

근거:
- **B는 위험** — id 변경이 app 영향 미지수 (§3.4). 데이터 수정 위험이 크므로
  바로 진행 권장 안 함.
- **A는 정보 부족** — true source가 미확정. 학습 패키지 id를 무엇으로 정정할지
  결정 불가. true source 식별 트랙(§6) 완료 후 실행 가능.
- **C가 정직한 단기 조치** — record 메타 오류를 alias/errata로 *명시적 문서화*.
  학습자가 cross-check 시 mapping을 참조할 수 있게 함. 데이터/학습 패키지 미수정
  으로 위험 0.
- **D는 후순위** — 기기-17 학습 콘텐츠 자체는 유효하므로 교체는 불필요. true
  source 식별 실패 시 fallback.

### 5.2 권장 순서

1. **C 임시 적용**: 본 plan 직후 alias/errata table 문서 작성 — `2020_1회_52`
   본문이 PDF 2020 1회 52와 다름을 명시, 학습자/후속 작업자 cross-reference 가능.
2. **추가 검증 트랙** (§6): true source 식별 + app 코드 영향 확인 + corpus 66
   cases 전수 감사.
3. **검증 결과에 따라 A 또는 B 결정**:
   - true source가 명확히 식별되면 → A (학습 패키지 표기만 정정).
   - app 영향이 안전하다고 확인되고 메타 정합이 우선이면 → B (questions.json
     id 정정).
4. **마지막으로 D는 보류** — A/B 진행 불가 또는 비용 과다 시에만.

### 5.3 데이터 key/id 수정 직접 금지 — 본 plan의 핵심 안전 원칙

- 본 plan 단계에서는 questions.json id/year/session/q_no를 절대 수정하지 않는다.
- B 옵션 채택 시에도 별도 명시 승인 + app 코드 영향 검증 완료 후에만 진행.
- 기기-18 case의 Commit A/B/C 패턴을 따라: feasibility → plan → 단계별 명시 승인
  → 검증 → 실행 → evidence supplement → redryrun → review → erratum.

---

## 6. 필요한 추가 검증

본 plan 다음 단계에서 수행할 검증 항목. 각 항목은 별도 명시 승인 후 audit
트랙으로 실행.

### 6.1 두 레코드 전문 비교

- `2020_1회_52` vs `2020_1,2회_52` 전 필드 비교 — id 차이 외에 본문·풀이·메타가
  완전히 다른 두 문제임을 재확인.

### 6.2 원본 PDF page 대조 (확장)

- PDF `data/문제_2020_1,2회_20260316.pdf` 페이지 라벨 분포 확인 — "1,2회" 라벨이
  실제로 PDF에서 어떤 범위(전체 1회 + 2회 / 일부만)를 가리키는지.
- "권수비 △-Y" 본문이 다른 년도 PDF에서 어디 등장하는지 추적 — 2020 외 연도
  PDF 전수 검색 필요 (또는 외부 기출 사이트 대조). 이는 별도 source 탐색 트랙.

### 6.3 corpus 내 같은 본문/같은 q_no duplicate 전수 탐색

- year+q_no overlap 1,819 case 중 본문이 *완전히 다른* case 추출 — 본 기기-17
  case가 isolated인지 systemic인지 정량화.
- "1,2회" 라벨 66 case 전수: 각 case의 본문이 같은 year/q_no의 "1회" 본문과
  같은지 다른지 표 작성.

### 6.4 app 코드의 question id 참조 방식 확인

- `app/index.html`, `app/js/bundle.js`, `app/js/store.js`, `app/js/render.js`,
  `app/js/main.js`, `app/js/study.js`에서 `questions.json`을 어떻게 로드·index
  하는지 분석.
- 특히 record id가 (year, session, q_no) 조합으로 key 역할을 하는지, URL
  routing/storage key로 쓰이는지 확인.
- id 변경 시 영향 범위 사전 식별 (B 옵션 안전성 평가의 핵심 입력).

### 6.5 학습 패키지 내 기기-17 참조 전수 검색

- B-priority study set v1·day plan·learning log v1.1·redryrun·1차 cleanup
  feasibility·기기-17 cleanup feasibility·closeout·post-closeout errata·
  followup erratum 등 docs에서 `2020_1회_52` 또는 "기기-17" 참조를 전수 grep.
- A·B·C 옵션 적용 시 동기 갱신 대상 문서 list 확정.

---

## 7. 다음 단계 제안

본 plan 승인 후 진행 가능한 후속 트랙. 각 단계는 별도 명시 승인 필요.

| 단계 | 작업 | 산출물 |
|---|---|---|
| **Step N1 — record identity targeted audit** | §6 검증 항목 5건 수행 (전문 비교 / PDF 추가 대조 / corpus duplicate 전수 / app id 참조 / 학습 docs 전수 검색) | audit report 문서 |
| **Step N2 — correction plan** | audit 결과에 따라 A/B/C/D 최종 옵션 확정 및 실행 plan 작성 (Commit 분리·허용 필드·검증 항목·rollback 경로) | correction plan 문서 |
| **Step N3 — data/doc sync 실행** | 승인된 옵션 실행. data 변경 시 단일 commit 분리(Commit A/B 등) + evidence supplement | commit + evidence supplements |
| **Step N4 — 기기-17 redryrun** | 정정 후 데이터·학습 패키지 정합 재검증 | redryrun 문서 |
| **Step N5 — clean count 갱신** | redryrun PASS 시 기기-17 caution → 완전 클린 전환, followup erratum 발행. 완전 클린 36/41 / caution 0/0 가능 | follow-up erratum 문서 |
| (병행) **추출 파이프라인 회귀 트랙 확장** | 66 cases systemic 양상 회귀 방지 (기기-18 인접 혼입 + 본 case session 라벨링/duplicate 패턴 통합) | 별도 회귀 트랙 |

---

## 8. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. 문제 정의 (id ↔ 본문 불일치 / duplicate / 학습 신뢰성) | ✅ §1 |
| 2. known facts (PDF / 두 레코드 / 정합 매트릭스) | ✅ §2 |
| 3. 영향 범위 (학습 패키지 / 검증 docs / questions.json 메타 / app 코드 / systemic 66 case) | ✅ §3 |
| 4. 옵션 비교 (A/B/C/D 장단·위험·범위) | ✅ §4 |
| 5. 권장안 (C 임시 + audit → A/B 결정, key/id 직접 수정 금지) | ✅ §5 |
| 6. 추가 검증 (5건 — 전문 비교 / PDF 대조 / duplicate / app 참조 / 학습 docs grep) | ✅ §6 |
| 7. 다음 단계 (audit → correction plan → data/doc sync → redryrun → clean count) | ✅ §7 |
| 본 plan 단계 데이터·학습 패키지·closeout/errata 미수정 | ✅ docs/audit/ 신규 1건만 |
| id/year/session/q_no 미수정 | ✅ |
| 금지사항 준수 | ✅ app/data·questions.json·id 메타·answer/choices/text·solution/steps·학습 패키지·closeout/errata 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- 기기-17 record identity normalization plan 작성 완료 — 데이터·학습 패키지
  미수정.
- 문제 정의: questions.json `2020_1회_52` 본문이 원본 PDF 2020년 1회 52와 불일치,
  PDF 정합 본문은 `2020_1,2회_52`로 별도 저장. 66 case의 "1,2회 + 1회" 공존
  패턴 중 한 사례 — systemic 양상.
- 권장: **C 임시 적용 + audit → A/B 결정 트랙 분리.** key/id 직접 수정은 위험
  (app 영향 미지수 + true source 미확정)으로 보류, 우선 alias/errata 문서화로
  추적성 확보. true source·app 영향 확인 후 A(학습 표기만) 또는 B(메타 정정)
  채택.
- 다음 단계: Step N1 (audit) → N2 (correction plan) → N3 (실행) → N4 (redryrun)
  → N5 (clean count 갱신). 병행 추출 파이프라인 회귀 트랙 확장.
- 본 plan 승인 ≠ N1~N5 실행 승인. 각 단계별 명시 승인 필요.
- 이 문서는 normalization plan이다. 데이터·학습 패키지·closeout/errata 미수정.
