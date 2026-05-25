# Trap-Map B-Priority — `2020_1회` vs `2020_1,2회` Namespace Conflict Audit (2026-05-25)

E3 — 2020 session namespace conflict audit을 수행한다. 직전 evaluation
(`02c985c`, `DR-TRAP-2020-12-MISSING29-DATA-DEBT`) 후 별 트랙으로 분리된 후보
3 영역 (split policy 부적합 재정의 + 100항과의 충돌 영역 검증)을 read-only로
감사한다.

이번 단계는 **read-only audit**. **app/data, questions.json, per-year json, PDF
filename, pdf_pages, app code, 어떤 파일도 수정하지 않는다.** missing 29 recovery
실행 금지. Batch migration 실행 금지. push 없음. amend/rebase/reset 없음.
기기-17 caution 유지. q52 단독 id 재발급 금지 유지. registry row promotion 금지
유지.

- 검토 대상:
  - `app/data/questions.json` `year=2020, session="1회"` (100 records)
  - `app/data/questions.json` `year=2020, session="1,2회"` (66 records)
  - `data/questions_기출_2020_1회.json` (100 records)
  - `data/questions_기출_2020_1_2회.json` (66 records)
- 관련 E2 mapping audit: `docs/audit/trap_map_B_priority_2020_1_2_66item_E2_record_pdf_mapping_audit_2026-05-25.md`
- 관련 E1 source audit: `docs/audit/trap_map_B_priority_2020_1_2_66item_E1_source_audit_2026-05-25.md`
- 관련 missing 29 recovery: `docs/audit/trap_map_B_priority_2020_1_2_66item_missing29_recovery_evaluation_2026-05-25.md`
- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`
- 관련 N1 targeted audit: `docs/audit/trap_map_B_priority_gigi_17_record_identity_targeted_audit_2026-05-23.md`
- 관련 separability evaluation: `docs/audit/trap_map_B_priority_gigi_17_66item_separability_evaluation_2026-05-25.md`

---

## 1. 사전 측정 결과 (Count + Range)

### 1.1 source count

| source | record count |
|---|---:|
| master `year=2020, session="1회"` | 100 |
| master `year=2020, session="1,2회"` | 66 |
| per-year `data/questions_기출_2020_1회.json` | 100 |
| per-year `data/questions_기출_2020_1_2회.json` | 66 |

### 1.2 q_no set

| source | q_no count | q_no range |
|---|---:|---|
| master 2020_1회 | 100 | **1~100** |
| master 2020_1,2회 | 66 | **1~93** |

### 1.3 per-year ↔ master 정합

| pair | 정합 |
|---|---|
| `data/questions_기출_2020_1회.json` q_no ↔ master 2020_1회 q_no | ✓ True |
| `data/questions_기출_2020_1_2회.json` q_no ↔ master 2020_1,2회 q_no | ✓ True |

→ 양 source 간 master ↔ per-year 정합 100% 유지 (E2 audit 결론 재확인).

---

## 2. q_no Overlap 분석

### 2.1 Set 연산 결과

| 연산 | count |
|---|---:|
| `2020_1회 ∩ 2020_1,2회` (intersection) | **66** |
| `2020_1회 ∖ 2020_1,2회` (only in 1회) | 34 |
| `2020_1,2회 ∖ 2020_1회` (only in 1,2회) | **0** |

### 2.2 핵심 발견 1 — Subset 관계

`2020_1,2회 q_no set ⊂ 2020_1회 q_no set` (proper subset)

- 2020_1,2회의 66 q_no **모두**가 2020_1회 100 q_no에 포함
- only_12 = 0 → 2020_1,2회 only q_no **0건**
- 2020_1회 only = 34 (= 100 - 66 = E2 audit 누락 29 + q94/95 등 영역과 별 영역)

→ 양 source가 *별 session 라벨*이지만 *q_no namespace가 100% 중첩* (1,2회가 1회의
subset).

### 2.3 only_1 34 q_no 영역

2020_1회 only (1,2회에 없는) 34 q_no는 미상세 (별 트랙). 추정 영역:
- E2 audit 누락 29 q_no 일부 영역
- 2020_1회 100 q_no = 1~100 (full range), 2020_1,2회 = 1~93 (q94~100 부재) →
  q94~100 영역 (7건) + 1~93 중 1,2회 누락 27건 = 34건

---

## 3. Content Conflict 분석 — 66 Overlap 영역

### 3.1 비교 양식

각 overlap q_no에 대해 master 2020_1회 record와 master 2020_1,2회 record를
비교:
- text normalize (공백 제거, 첫 60자)
- answer 비교

### 3.2 결과 — **100% Conflict**

| 분류 | count | 비율 |
|---|---:|---|
| same (text + answer 동일) | **0** | 0% |
| similar (text prefix 20자 같음, 그 외 다름) | **0** | 0% |
| **diff (별 컨텐츠)** | **66** | **100%** |

→ **66 overlap q_no 모두 별 컨텐츠**. *어떤 q_no도 양 source가 같은 문제가
아님*.

### 3.3 대표 샘플 (diff_content)

| q_no | 2020_1회 본문 prefix | 2020_1,2회 본문 prefix | 1회 정답 | 1,2회 정답 |
|---:|---|---|:---:|:---:|
| 1 | 고유 임피던스 (εr=81, μr=1 매질) | 평행 도체 판 전위차 V | 4 | 3 |
| 2 | 강자성체 B-H 곡선 | 평행 도체 판 (LaTeX) | 3 | 3 |
| 5 | 정전용량 20μF 평행판 커패시터 | 자기 인덕턴스 결합계수 k 범위 | 3 | 2 |
| 6 | 유전율 ε1·ε2 두 유전체 경계 | 평행판 콘덴서 정전용량 (LaTeX) | 1 | 3 |
| 7 | 환상 철심 권수 100·400 A·B 코일 | 반자성체 비투자율 μr 범위 (LaTeX) | 4 | 2 |
| 8 | 환상 솔레노이드 자기인덕턴스 | 반지름 a 무한장 원통형 도체 (LaTeX) | 2 | 1 |
| 14 | 자계의 세기 단위 아닌 것 | 전계·자계 세기 (포인팅 벡터, LaTeX) | 3 | 3 |
| 21 | 피뢰기 충격방전개시전압 | 중성점 직접접지 1선 지락 (LaTeX) | 3 | 3 |
| 22 | 전력용 콘덴서 vs 동기조상기 | 송전계통 절연협조 절연레벨 | 2 | 1 |
| **52** | **변압기 권수비 (단상변압기 3대 1차△·2차Y)** | **동기전동기 V곡선 (여자전류 증가)** | **1** | **1** |

→ q52를 포함 모든 샘플에서 본문이 *완전히 다른 시험 문제*.

---

## 4. 양식 차이 — Source 추출 도구 분리

### 4.1 양식 관찰

- **2020_1회**: plain text 양식 (LaTeX markup 없음)
  - 예: `정전용량이 20μF인 공기의 평행판 커패시터에 0.1C의 전하량을`
- **2020_1,2회**: LaTeX markup 양식 (`\(...\)` 포함)
  - 예: `면적이 \(S\left[\mathrm{~m}^{2}\right]\)이고 극간`

### 4.2 함의

양 source가 *별 추출 도구* 영역에서 생성된 것으로 추정:
- 2020_1회: manual transcription 또는 별 OCR 도구
- 2020_1,2회: Mathpix 또는 LaTeX 출력 OCR 도구 (per-year 파일명 `mathpix_기출_*.json`
  패턴과 정합 가능)

→ source 추출 파이프라인 자체가 *분리된 영역*임을 양식이 시사.

---

## 5. q52 Case — Isolated vs Systemic

### 5.1 q52 양 source content (재확인)

| source | text prefix | answer |
|---|---|:---:|
| master 2020_1회_52 | `권수비가 a인 단상변압기 3대가 있다. 이것을 1차에 △, 2차에 Y로 결선하여 3상 교류 평형회로에 접속할 때 2차측의 단자전압을 V(V)` | 1 |
| master 2020_1,2회_52 | `동기전동기의 공급전압과 부하를 일정하게 유지하면서 역률을 1로 운전하고 있는 상태에서 여자전류를 증가시키면 전기자전류는?` | 1 |

→ E1 audit / E2 audit / N1 targeted audit 명시와 정합 재확인:
- `2020_1회_52` = 변압기 권수비 (true source = `data/20200424_1회.pdf` p.4 q52 =
  2022년 1회)
- `2020_1,2회_52` = 동기전동기 V곡선 (true source = `data/문제_2020_1,2회_20260316.pdf`
  page 19 = 2020년 1,2회 합본)

### 5.2 q52는 Isolated Case가 아님

본 audit의 100% conflict 결과는 q52가 *systemic namespace conflict의 1 사례*임을
확정:

- **66 overlap q_no 모두 conflict** → q52는 그 중 1건 (q52에 한정된 isolated 영역
  아님)
- 다른 65 overlap q_no도 동일 양식으로 conflict — 각 q_no가 양 session 영역에서
  *별 시험 컨텐츠* 보유

### 5.3 q52 + Systemic Framing 영역 확장 가능성

q52 alias registry artifact (`9868f95`)의 q52 row (`2020_1회_52` storage_id →
`2022_1회_52` canonical_source_id)는 본 audit 결과로 *systemic framing 후보의 1
사례*가 됨:

- impact audit §1: "`2020_1회` 100항 batch mis-label 가능성"
- N1 targeted audit (`13edae5`): 2020_1회_52의 true source = 2022 1회 q52
- 본 E3 audit: 2020_1회 100 records가 2020_1,2회 66 records와 *어떤 q_no에서도
  같은 시험이 아님*

→ 2020_1회 100 records 전체가 *별 시험 source* (impact audit 가설 강화). q52 alias
row가 q52 외 99 records 영역으로 확장 가능한 framing 활성화.

단 **확장은 별 명시 승인 영역**. 본 audit은 framing 영역 확장 *가능성*만 명시,
registry artifact 영역 변경 없음 (q52 row 1건 유지).

---

## 6. 2020_1회 100 Records Source 가설 강화

### 6.1 기존 evidence (impact audit + N1 audit)

- impact audit §1: 2020_1회 100항 batch mis-label 가능성
- N1 targeted audit: 2020_1회_52 = 2022 1회 q52 (변압기 권수비)
- registry artifact `9868f95`: q52 storage_id `2020_1회_52` → canonical `2022_1회_52`

### 6.2 본 audit 추가 evidence

- 100 records q_no = 1~100 (full range)
- 양식: plain text (1,2회 LaTeX와 분리)
- 66 overlap 모두 별 컨텐츠 = 양 source가 별 시험 영역

→ **가설 강화**: 2020_1회 100 records는 *2020년 실제 시행 시험*과 *별 source*에서
추출됐을 가능성 매우 높음. true source는 *2022년 1회 또는 다른 별 시험* (q52
외 99 records 영역의 true source는 본 audit 영역 외 — 별 트랙).

### 6.3 단 가설 확정은 별 트랙

본 audit은 가설 강화만 — **확정은 별 트랙** (예: 100 records 전수 source PDF
audit, 외부 한국기술자격검정 시행 기록 cross-reference 등).

---

## 7. 7 Audit Question 답

### Q1 — 2020_1회와 2020_1,2회의 q_no overlap은 어떻게?

**A**: **66 intersection (2020_1,2회가 2020_1회의 proper subset)**. only_1 = 34
/ only_12 = 0.

### Q2 — content conflict count는?

**A**: **66 / 66 = 100%**. 모든 overlap q_no가 *별 컨텐츠*. same 0 / similar 0
/ diff 66.

### Q3 — q52는 isolated case인가 systemic 1 사례인가?

**A**: **systemic 1 사례** (§5.2). 66 overlap 모두 동일 패턴.

### Q4 — Batch migration 영향?

**A**: **차단 유지 + scope 영역 확장 가능성**. 차단 사유 (66항 policy 선결) 유지.
단 본 audit으로 2020_1회 100 records 영역 자체의 별 source 가설이 강화되어
Batch migration scope이 *2020_1회 100 + 2020_1,2회 66 = 두 별 영역*으로 분리
가능성 확장. 단 실행은 별 명시 승인 + 다중 evidence 후만.

### Q5 — alias policy 영향?

**A**: **q52 alias registry framing 영역 확장 가능성 활성화**. q52 row가 systemic
1 사례임이 확정되어 q52 외 99 records 영역으로 alias 확장 후보 영역 활성화. 단
**확장 실행은 별 명시 승인 + 100 records 전수 source audit 후만**. 현재 q52 row
1건 유지.

### Q6 — q52 caution release 영향?

**A**: **차단 유지** (separability Q4 Inseparable + 본 audit 결과 변경 0).

근거:
- 본 audit은 *evidence 영역 강화*만 — 정책 결정 변경 없음
- separability evaluation Q4 Inseparable 결론 유지
- caution release input 요구사항 (별 systemic policy + user-facing impact +
  redryrun) 변경 0

### Q7 — 다음 gate는?

**A**: **5 별 트랙 영역**.

| 트랙 | 영역 |
|---|---|
| 100 records 전수 source audit (별 트랙) | 2020_1회 100 records 각 record의 true source 식별 (q52 외 99 records 영역) |
| q52 외 99 records의 alias 확장 evaluation (별 트랙) | systemic framing 확장 가능성 평가 + alias registry row 추가 정책 결정 |
| E4 다른 합본 PDF 패턴 (별 트랙) | 다른 연도 합본 PDF 사례 비교 |
| E5 app persisted key 영향 (split 부적합 → alias only 재평가) | 본 audit 결과 반영 |
| 66항 policy 재evaluation (E2-A + E3~E6 + 외부 source 후) | 본 E3 결과 입력 |

---

## 8. 결론 — Systemic Namespace Conflict 확정

### 8.1 본 audit 확정 영역

- **66 overlap q_no 100% content conflict 확정** (same 0 / similar 0 / diff 66)
- **q52는 systemic conflict의 1 사례 확정** (isolated case 아님)
- **양 source가 별 추출 파이프라인 영역 확정** (plain text vs LaTeX 양식)
- **2020_1회 100 records가 별 시험 source에서 추출됐을 가능성 강화** (impact
  audit §1 + N1 audit 결론 강화)
- per-year ↔ master 정합 100% 유지 재확인

### 8.2 본 audit 활성화 영역

- q52 alias registry framing 영역 확장 *가능성* (q52 row → systemic 99 records
  영역) — **활성화만**, 실행은 별 명시 승인
- 100 records 전수 source audit (별 트랙) 영역 활성화
- 66항 policy evidence requirement E3 충족 (split policy 부적합 재정의 영역)

### 8.3 본 audit 차단 유지 영역

- **q52 단독 id 재발급** — 본 audit으로 systemic 1 사례 확정 → 단독 재발급 영구
  부적합
- **caution release** — input 요구사항 변경 없음
- **Batch migration** — 66항 policy 선결 조건 유지
- **registry row promotion** — 별 명시 승인 영역
- **registry artifact 변경** (q52 row 외 추가 row) — 별 명시 승인 영역

### 8.4 본 audit 변경 없음 영역

- 66항 policy = **defer 유지** (정책 변경 0)
- q52 separable layer (registry 9868f95 / review f0b462c / design 6ac1a9b /
  App/data 9c1d387 / separability d9b2efd) 모두 PASS baseline 유지
- jsonl decision entry 추가 안 함 (사용자 가이드 정합 — evidence audit, 정책
  변경 없음)

---

## 9. 영향 매트릭스

| 영역 | 본 audit 영향 | 상태 |
|---|---|---|
| q52 alias registry (9868f95) | row 1건 유지, framing 영역 확장 *가능성* 활성화 | candidate 유지 |
| registry artifact review PASS (f0b462c) | 12/12 PASS baseline 유지 | 영향 0 |
| runtime resolver design review (6ac1a9b) | design candidate 유지 | 영향 0 |
| App/data decision (9c1d387) | 후보 A docs-only + B-design-review 유지 | 영향 0 |
| 66항 separability evaluation (d9b2efd) | partial separability 결론 유지 | 영향 0 |
| 66항 session-label policy (df7e932) | defer 유지 + evidence requirement E3 충족 | 영향 0 |
| E1 source audit (5c1fecc) | 합본 시험 확정 유지 + 본 audit으로 source 분리 framing 강화 | 강화 |
| E2 record-PDF mapping (5f1c9c5) | per-year ↔ master 정합 재확인 + missing 29 영역 유지 | 재확인 |
| missing 29 data debt (02c985c) | 후보 A 별 data debt 분리 유지 | 영향 0 |
| caution release (Step 6) | input 요구사항 변경 0 | 차단 유지 |
| Batch migration | 66항 policy 선결 조건 유지 + 본 audit으로 scope 영역 확장 가능성 | 차단 유지 |
| 후보 C (split policy) | E1 부적합 확정 유지 + 본 audit으로 namespace 분리 확정 (split할 동일 시험 영역 부재) | 부적합 유지 |
| 기기-17 caution | 유지 | 유지 |
| q52 단독 id 재발급 | 본 audit으로 systemic 1 사례 확정 → 영구 부적합 | 금지 강화 |

---

## 10. 다음 Gate (각 별 명시 승인 후만 진행)

1. **100 records 전수 source audit** (별 트랙)
   - 2020_1회 100 records 각 record의 true source PDF 식별
   - q52 외 99 records의 source 영역 (2022 1회 또는 별 시험)
2. **q52 외 99 records alias 확장 evaluation** (별 트랙)
   - systemic framing 확장 가능성 + alias registry row 추가 정책
3. **E4 다른 합본 PDF 패턴** (별 트랙)
4. **E5 app persisted key 영향 재평가** (split 부적합 + 본 audit 입력)
5. **E6 separability re-evaluation** (E2~E5 후)
6. **외부 source evidence** (한국기술자격검정 공식 2020 시행 기록)
7. **66항 policy 재evaluation** (E2-A + E3~E6 + 외부 source 후)
8. **missing 29 recovery plan** (별 트랙, R1~R5 후)
9. **1·3·4 과목 verification 보강** (별 트랙, PDF read-only)

---

## 11. Forbidden Until Separate Approval

- q52 단독 id 재발급 (본 audit으로 systemic 1 사례 확정 — 영구 부적합)
- `questions.json` 수정
- per-year json 수정
- PDF filename rename
- PDF 파일 복사 / 편집 / OCR 산출물 신규 생성
- `pdf_pages/index.json` 수정
- app code 수정
- app alias resolver 구현
- app/data alias registry 추가
- record metadata field 추가
- registry row promotion from `candidate` to `approved`
- registry artifact 자체 수정 (q52 row 외 추가 row 포함)
- 기기-17 caution 해제 선언
- Batch migration 진입
- 66항 systemic policy를 q52 registry 영역에 흡수
- 100 records alias 확장 실행 (별 트랙 + 전수 source audit + 별 명시 승인 후)
- missing 29 recovery 실행
- 후보 C (split policy) 진입 (E1 + 본 audit 부적합 확정 유지)

---

## 12. Decision Record 영향

본 audit은 **evidence 영역 추가만** 수행 — 정책 변경 0:

- 66항 policy = **defer 유지** (변경 없음)
- q52 단독 id 재발급 금지 = 영구 부적합 강화 (기존 룰의 evidence 강화)
- Batch migration 차단 유지 (영역 확장 가능성만 명시)
- registry artifact q52 row 1건 유지 (framing 확장은 별 명시 승인 영역)
- caution release 차단 유지
- 후보 C (split policy) 부적합 영역 강화

→ jsonl `trap_map_active_decisions.jsonl`에 별 entry 추가 안 함 (사용자 가이드:
"evidence audit이고 정책 변경 없으면 추가 안 함" 준수).

본 audit 문서 자체가 E3 namespace conflict evidence로 충분.

---

## Status

- E3 namespace conflict audit 작성 완료.
- 핵심 측정:
  - master 2020_1회 100 records (q_no 1~100) / 2020_1,2회 66 records (q_no
    1~93)
  - q_no overlap = 66 (2020_1,2회 ⊂ 2020_1회 proper subset)
  - **content conflict = 66/66 = 100%** (same 0 / similar 0 / diff 66)
  - 양식 차이: 2020_1회 plain text vs 2020_1,2회 LaTeX
  - per-year ↔ master 정합 100% 재확인
- 핵심 발견:
  - **systemic namespace conflict 확정** — q52는 isolated case 아님, 66 overlap
    중 1 사례
  - **양 source가 별 추출 파이프라인 영역** (양식 차이)
  - **2020_1회 100 records가 별 시험 source에서 추출됐을 가능성 강화** (impact
    audit §1 + N1 audit 결론 강화)
- q52 alias registry framing 영역 확장 *가능성* 활성화 (q52 row → systemic 99
  records) — 실행은 별 명시 승인 영역.
- 정책 변경 0 — 66항 defer / q52 separable layer baseline / caution release 차단
  / Batch migration 차단 / 후보 C 부적합 모두 유지.
- q52 단독 id 재발급 금지 = 영구 부적합 강화 (systemic 1 사례 확정).
- jsonl decision entry 추가 안 함 (사용자 가이드 정합 — evidence audit, 정책
  변경 없음).
- app code / app data / questions.json / per-year / PDF / pdf_pages / registry
  artifact 모두 변경 0.
- 기기-17 caution 유지. registry row status=candidate 유지. Batch migration
  차단 유지. caution release 차단 유지.
- 다음 gate: 100 records 전수 source audit / q52 외 99 records alias 확장
  evaluation / E4~E6 / 외부 source / 66항 재evaluation / missing 29 recovery /
  1·3·4 verification 보강.
