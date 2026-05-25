# Trap-Map B-Priority — 2020_1회 100 Record Source Audit Plan (2026-05-25)

E6 separability re-evaluation (`a787cc3`, `DR-TRAP-GIGI17-SEPARABILITY-REEVAL`)
이후, 별 트랙 후보 1번 = **2020_1회 100 records 전수 source audit**의 범위와
절차를 정의한다. 본 문서는 **audit plan only** — *실제 audit 실행 영역 외*.

이번 단계는 **docs-only plan**. **app/data, questions.json, per-year json, PDF
filename, pdf_pages, app code, 어떤 파일도 수정하지 않는다.** 실제 100 records
전수 PDF 대조 / OCR / data patch / alias 확장 / 99 records framing 확장 / Batch
migration 모두 실행 금지. push 없음. amend/rebase/reset 없음. 기기-17 caution
유지. **q52 storage_id `2020_1회_52` 단독 변경 = Permanent Invariant 유지**.
registry row promotion 금지 유지.

- 관련 E6 re-evaluation: `docs/audit/trap_map_B_priority_2020_session_namespace_E6_separability_reevaluation_2026-05-25.md` (`DR-TRAP-GIGI17-SEPARABILITY-REEVAL`)
- 관련 E5 app key impact: `docs/audit/trap_map_B_priority_2020_session_namespace_E5_app_key_impact_2026-05-25.md`
- 관련 E3 namespace conflict: `docs/audit/trap_map_B_priority_2020_1_vs_2020_1_2_conflict_audit_2026-05-25.md`
- 관련 registry artifact review: `docs/audit/trap_map_B_priority_gigi_17_alias_registry_artifact_review_2026-05-25.md` (PASS 12/12)
- 관련 registry artifact: `docs/audit/registries/trap_map_gigi_17_alias_registry_2026-05-25.json`
- 관련 N1 targeted audit: `docs/audit/trap_map_B_priority_gigi_17_record_identity_targeted_audit_2026-05-23.md`
- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`

---

## 1. 사전 측정 결과 (read-only)

### 1.1 2020_1회 records count

| source | record count | q_no range | per-year ↔ master 정합 |
|---|---:|---|---|
| `data/questions_기출_2020_1회.json` (per-year) | 100 | 1~100 | ✓ True |
| `app/data/questions.json` `year=2020, session="1회"` (master) | 100 | 1~100 | ✓ True |

### 1.2 과목별 q_no 분포 (20건 균등)

| 과목 | q_no 범위 | count |
|---|---|---:|
| 1과목 전기자기학 | 1~20 | 20 |
| 2과목 전력공학 | 21~40 | 20 |
| 3과목 전기기기 | 41~60 | 20 |
| 4과목 회로이론·제어공학 | 61~80 | 20 |
| 5과목 전기설비기술기준 | 81~100 | 20 |

→ full 100 records 표준 5 과목 × 20 문항 양식.

### 1.3 record 양식 (14 필드)

`answer`, `choices`, `difficulty`, `q_no`, `q_type`, `quality`, `session`,
`solution`, `solution_svg`, `steps`, `subject`, `tag`, `text`, `year`

### 1.4 q52 현 row 영역 (alias registry baseline)

| field | value |
|---|---|
| storage_id | `2020_1회_52` |
| canonical_source_id | `2022_1회_52` |
| source_pdf | `data/20200424_1회.pdf` |
| source_pdf_page | 4 |
| source_q_no | 52 |
| cover_date | 2022-04-24 |
| status | candidate |

→ q52 row 1건만 registry artifact에 등재. 99 records 영역은 registry 외.

---

## 2. Audit 목적 + 범위

### 2.1 목적

| 목적 | 영역 |
|---|---|
| **P1** 2020_1회 100 records 각 record의 *true source* 영역 식별 | per-record source PDF / page / q_no 매핑 |
| **P2** q52 systemic 1 사례 (E3 확정)의 99 records 영역 확장 가능성 evidence 수집 | 99 records의 source가 q52와 동일 mis-label 패턴 영역인지 검증 |
| **P3** 99 records alias 확장 evaluation의 선행 evidence 영역 충족 | E6 Q3 Refined Partial Separable + Q5 Inseparable 영역 + Permanent Invariant 영역에서 단독 변경 없이 systemic mapping 영역 결정 |
| **P4** impact audit §1 가설 (`2020_1회` 100항 batch mis-label) 확정 또는 부정 | N1 audit이 q52에 한정 확인 → 99 records 확장 영역 |

### 2.2 audit 범위 (P1~P4 한정)

- 100 records 전수 PDF source 영역 식별 + canonical_source_id 매핑 후보 영역
- mis-label 패턴 영역 분류 (q52와 동일 / 별 패턴 / 정합)
- 99 records alias 확장 evidence 영역 충족 여부 판정

### 2.3 audit scope 외 영역 (별 트랙)

- 실제 data patch / OCR / migration / registry row 추가 → 별 명시 승인 영역
- 99 records alias 확장 실행 → 별 evaluation + 별 명시 승인 영역
- Batch migration 영역 → 66항 policy + mapping granularity 5 영역 모두 충족 후
- caution release 진입 → E6 Q4 Inseparable 유지 영역
- missing 29 data recovery debt → 별 트랙 (본 100 records source audit scope 외)

---

## 3. Audit Unit — Record 단위

### 3.1 결정

**audit unit = record 단위** (q_no = 1, 2, …, 100 각각 별 unit).

### 3.2 근거

| 근거 | 영역 |
|---|---|
| record 단위 = q52 alias registry의 row 단위와 정합 | schema plan §2 row schema 영역 |
| record 단위 evidence가 99 records alias 확장 시 row 추가 영역과 1:1 | registry artifact 확장 양식 정합 |
| page 단위는 PDF 영역 분할이며 record 영역 분할 아님 | record와 page는 별 차원 |

### 3.3 record-page 매핑 정책

- 1 record = 1 PDF page 한정 매핑 (대표 page) + 보조 page (figure / solution 영역
  page 별도 가능)
- record가 여러 PDF에 분산 등재된 경우 (예: 출제기준 변경으로 별 책에 등재) 별
  매핑 영역 분리

---

## 4. Audit 절차 (5 Phase)

### 4.1 Phase A — Source PDF 후보 inventory (read-only)

**범위**:
- 사용 가능 PDF 후보 영역 inventory (untracked data 파일 다수, 사용자 명시 승인
  영역 한정 read-only)
- 후보 PDF의 표지 / 페이지 수 / 시행 일자 / 책 페이지 양식 영역 확인
- PDF source 식별 양식 (예: 전자문제집 CBT / vFlat 스캔 / 별 양식) 영역 분류
- E4 다른 합본 PDF 패턴 트랙 결과는 본 Phase A inventory의 input reference로 참조 가능 (단 E4 트랙 자체 실행은 별 트랙 §13 영역 유지)

**산출**:
- PDF 후보 inventory (별 docs/audit 영역)
- 각 후보의 시행 영역 가설 (확정 / 강한 가설 / 추정 분리 표기 — N1 audit 양식
  정합)

**금지**:
- PDF 복사 / rename / 편집 / OCR 산출물 신규 생성

### 4.2 Phase B — record-PDF 1:1 매핑 (read-only)

**범위**:
- 100 records × 후보 PDF 매핑 (record 단위, q_no 매칭 + text prefix 매칭 +
  answer 매칭)
- 매핑 결과 = (storage_id, candidate PDF, page, q_no, cover_date) tuple

**산출**:
- record-PDF 매핑 표 (별 docs/audit 영역)
- 매핑 confidence 영역 분류 (3-way 정합 / 부분 정합 / 미매칭)

**금지**:
- 실제 data patch / per-year 수정 / master 수정

### 4.3 Phase C — Mis-Label 패턴 분류

**범위**:
- 100 records를 다음 4 패턴 영역으로 분류:
  - **C1 — q52와 동일 mis-label**: 2020_1회 라벨이나 실제 source = 2022_1회 (또는
    별 시험)
  - **C2 — 정합**: 2020_1회 라벨이 실제 source와 일치
  - **C3 — 별 mis-label 패턴**: 2020_1회 라벨이나 실제 source = 별 영역 (예:
    2020_1,2회 / 2019_3회 등)
  - **C4 — 미매칭**: 어떤 후보 PDF에도 매칭 안 됨 (별 source 영역)

**산출**:
- 패턴별 record 수 + 영역 분포
- C1 영역 = 99 records alias 확장 후보 영역의 1차 영역

### 4.4 Phase D — Alias 확장 evidence 충족 여부 판정

**범위**:
- C1 영역의 record 수가 99에 근접하는지 판정 (impact audit §1 가설 검증)
- 99 records 영역의 canonical_source_id 매핑 evidence 영역 충족 여부
- registry artifact 확장 진입 가능성 영역 판정

**산출**:
- alias 확장 evidence 충족 영역 평가 (충족 / 부분 충족 / 미충족)
- 99 records alias 확장 evaluation 트랙 진입 권고

### 4.5 Phase E — Audit 보고서 작성

**범위**:
- Phase A~D 결과 종합
- 99 records alias 확장 evaluation 입력 evidence 영역
- guardrail 영역 (Permanent Invariant + Batch migration 차단 + caution release
  차단) 영구 적용 확인

**산출**:
- audit 보고서 (별 docs/audit 영역, plan 본 문서가 입력)
- jsonl decision entry (정책 변경 영역 있을 시)

---

## 5. PDF Source 후보 + 확정/미확정 표현 정책

### 5.1 PDF source 후보 영역 (Phase A inventory)

| 후보 영역 | 영역 |
|---|---|
| `data/20200424_1회.pdf` (N1 audit confirmed for q52) | q52 + 99 records 확장 가능성 |
| `data/문제_2020_1,2회_20260316.pdf` (E1 audit confirmed for 2020_1,2회) | 별 시험 영역 (E3 conflict) |
| `data/문제_*_20260316.pdf` 영역 (다른 연도) | 별 후보 |
| `data/전기기기_20260312.pdf` / `data/전력공학_20260312.pdf` 등 과목별 | 별 영역 (시험 문제 아님 가능성) |

→ Phase A에서 후보 영역 inventory 후 record-PDF 매핑 영역 진입.

### 5.2 확정 vs 강한 가설 vs 추정 분리 표기 (N1 audit 양식 정합)

| 표기 | 영역 |
|---|---|
| **확정** | PDF text + answer + page 3-way 정합 + 외부 source 영역 확인 (예: 한국기술자격검정 공식 시행 기록) |
| **강한 가설** | PDF 3-way 정합 (text + answer + page) 단 외부 source 영역 미확인 (예: q52의 2022 1회 source = 강한 가설) |
| **추정** | text 또는 answer 일부 정합, 또는 patron 영역만 일치 |
| **미매칭** | 어떤 PDF에도 매칭 안 됨 |

→ audit 결과의 모든 record에 표기 영역 명시. *추정 영역을 확정처럼 처리 금지*.

→ **외부 official source가 없을 때는 *확정* 영역으로 승급하지 않고 *source-internal confirmed* (PDF 3-way 정합) 또는 *강한 가설* 영역으로 유지한다.** *확정* 영역 승급은 외부 official source evidence 트랙 (§13) 별 결정 후만 활성화.

---

## 6. 99 Records Alias 확장 Evidence 요구사항

99 records alias 확장 evaluation 트랙 진입 영역의 최소 evidence:

| evidence | 영역 |
|---|---|
| **R1** Phase A~D 완료 | 100 records 전수 audit 완료 |
| **R2** C1 패턴 record 수 명확 | q52와 동일 mis-label 영역의 정량 결과 |
| **R3** 99 records 각각의 candidate canonical_source_id 매핑 | row schema 9 필드 영역 충족 |
| **R4** evidence_ref 양식 충족 | N1 audit + impact audit + Phase B/C 결과 link |
| **R5** Permanent Invariant 영역 준수 | 각 record의 storage_id 보존 영역 명시 |
| **R6** registry artifact 확장 양식 결정 | 99 records 추가 양식 (별 row 추가 / 별 artifact / 별 영역) 영역 |
| **R7** app key 영역 영향 0 재확인 | E5 §6 + E6 Q1·Q2 Separable 영역 유지 |

본 plan 단계에서 R1~R7 *수집 영역 정의*만 — 실제 수집은 별 명시 승인 후만.

---

## 7. q52 Permanent Invariant Guardrail 적용

### 7.1 invariant 영역 명시

E6 §3 신규 invariant:

```
q52 storage_id = `2020_1회_52` 영구 유지.
단독 storage_id 변경 = 금지.
변경 가능 영역 = canonical_source_id (citation display 전용, alias-only).
```

### 7.2 본 plan 적용 영역

| 영역 | invariant 적용 |
|---|---|
| Phase A~B record-PDF 매핑 | q52 매핑 결과는 N1 audit + 본 registry q52 row와 일치 영역 (변경 0) |
| Phase C mis-label 패턴 | q52는 C1 영역 (확정), 99 records의 C1 영역 분류는 별 evidence |
| Phase D alias 확장 evidence | q52 row는 systemic mapping의 1 사례 영역, 단독 영역 변경 영구 금지 |
| Phase E 보고서 | invariant 영역 영구 명시 |
| audit 결과 적용 | systemic 99 records mapping이 결정될 경우 q52 storage_id가 같이 이동 가능 (단독 영역 아님), 변경 시 q52 row의 storage_id 영역 영구 보존 |

### 7.3 invariant 위반 영역 차단

- audit 결과로 q52 row의 storage_id 단독 변경 영역 = **차단**
- 99 records alias 확장 시점에서 q52 row 단독 처리 영역 = **차단**
- registry artifact 확장 시 q52 row 영역 변경 영역 (storage_id 한정) = **차단**

---

## 8. Registry Artifact 확장 조건

audit 결과가 registry artifact를 확장할 수 있는 조건:

| 조건 | 영역 |
|---|---|
| **C1** Phase A~D 완료 + alias 확장 evidence R1~R7 모두 충족 | 본 plan §6 |
| **C2** 99 records alias 확장 evaluation 트랙 별 명시 승인 + 별 결정 | 별 트랙 영역 |
| **C3** registry artifact 확장 양식 결정 (R6) — row 추가 / 별 artifact / 별 영역 중 1택 | 별 명시 승인 영역 |
| **C4** Permanent Invariant 영역 준수 (q52 storage_id 영역 영구 보존) | 본 plan §7 |
| **C5** integrity checks 양식 확장 영역 결정 — 8 checks (schema plan §5) + 100 records 영역 추가 check | 별 design 영역 |
| **C6** registry artifact review (별 review session) PASS | 별 review 영역 |
| **C7** app key 영역 영향 0 재확인 (E5 §6 + E6 Q1·Q2 Separable 영역 유지) | 본 plan §6 R7 |

→ C1~C7 모두 충족 영역에서만 registry artifact 확장 진입.

---

## 9. Batch Migration Gate 분리

audit 결과가 **Batch migration으로 바로 이어지지 않도록** 명시 gate 분리:

| Gate | 영역 |
|---|---|
| **G1** audit 결과는 *alias 확장* 영역만 활성화 | Batch migration 영역 별 |
| **G2** alias 확장 = read-path citation resolver / docs registry 영역 (E5 §6) | Batch migration = persisted user data migration 영역 (E5 §5) |
| **G3** Batch migration은 별 inseparable 영역 (E6 Q5 Inseparable 강화) | mapping granularity 5 영역 + 66항 policy 선결 |
| **G4** audit 결과가 Batch migration의 mapping 영역에 *input evidence*가 될 수는 있으나, 진입 영역 결정 자체는 별 트랙 | 본 audit은 *audit only* |

→ audit 결과의 *Batch migration 자동 진입 영역 = 0*. 진입 결정은 별 명시 승인
+ 66항 policy 선결 + persisted user data migration 영역 결정 모두 충족 후.

---

## 10. 산출물 + 검증 양식

### 10.1 audit 산출물 (별 트랙 진행 시)

| 산출물 | 영역 |
|---|---|
| Phase A PDF inventory | 별 docs/audit/ |
| Phase B record-PDF 매핑 표 | 별 docs/audit/ 또는 별 JSON artifact (별 명시 승인 영역) |
| Phase C mis-label 패턴 분류 | 별 docs/audit/ |
| Phase D alias 확장 evidence 충족 평가 | 별 docs/audit/ |
| Phase E audit 보고서 | 별 docs/audit/ |
| jsonl decision entry (필요 시) | `trap_map_active_decisions.jsonl` 1줄 (정책 변경 영역 있을 시) |

### 10.2 검증 양식

| 검증 | 양식 |
|---|---|
| 각 record matching 검증 | text prefix 정합 + answer 정합 + page 영역 정합 3-way |
| 표기 정합 | 확정 / 강한 가설 / 추정 / 미매칭 분류 명시 |
| Permanent Invariant 준수 | q52 storage_id 영역 변경 0 verification |
| app key 영역 영향 0 | E5 §6 + E6 Q1·Q2 영역 유지 verification |
| guardrail 영역 준수 | app/data / app code / registry artifact / PDF / pdf_pages 변경 0 verification |

---

## 11. 9 Question 답

### Q1 — 100 records 전수 audit의 목적은 무엇인가?

**A**: **4 영역 목적** (§2.1) — P1 source 식별 + P2 99 records 확장 가능성 evidence
+ P3 alias 확장 evaluation 선행 evidence + P4 impact audit §1 가설 검증.

### Q2 — q52 단독 row에서 99 records alias 확장으로 넘어가기 위한 최소 evidence는?

**A**: **R1~R7 7 영역** (§6) — Phase A~D 완료 + C1 패턴 정량 + 99 records 매핑 +
evidence_ref 양식 + Permanent Invariant 준수 + registry 확장 양식 결정 + app key
영향 0 재확인.

### Q3 — audit unit은 record 단위인지 page 단위인지?

**A**: **record 단위** (§3.1). q52 alias registry row 단위와 정합.

### Q4 — PDF source 후보는 무엇인지, 확정/미확정 표현을 어떻게 구분?

**A**: **§5.1 PDF 후보 영역 + §5.2 4 표기** (확정 / 강한 가설 / 추정 / 미매칭).
N1 audit 양식 정합. *추정을 확정처럼 처리 금지*.

### Q5 — q52 Permanent Invariant를 어떻게 guardrail로 적용?

**A**: **§7 5 영역 적용** — Phase A~E 각 단계에서 q52 storage_id 영역 영구 보존
verification. 위반 영역 (단독 변경 / 단독 처리 / storage_id 영역 변경) 모두
차단.

### Q6 — audit 결과가 registry artifact를 확장할 수 있는 조건은?

**A**: **§8 C1~C7 7 영역 충족** — audit 완료 + alias 확장 evaluation 별 명시
승인 + 확장 양식 결정 + Permanent Invariant 준수 + integrity check 확장 + review
PASS + app key 영향 0.

### Q7 — audit 결과가 Batch migration으로 바로 이어지지 않도록 어떤 gate?

**A**: **§9 G1~G4 4 영역 gate** — audit 결과는 alias 확장 영역만 활성화 /
Batch migration은 별 inseparable 영역 / persisted user data migration 영역 결정
선결.

### Q8 — 예상 산출물과 검증 방식은?

**A**: **§10 5 산출물 + 5 검증 양식**.

### Q9 — 다음 실행 gate는?

**A**: **§13 별 명시 승인 후 진입 영역**.

---

## 12. Forbidden Until Separate Approval

- **q52 storage_id 단독 변경 (Permanent Invariant — 영구 금지)**
- 100 records 전수 audit 실행 (본 plan은 plan only, 별 명시 승인 후 실행)
- 99 records alias 확장 실행
- registry artifact 확장 (q52 row 외 추가 row)
- registry row promotion from `candidate` to `approved`
- `questions.json` 수정
- per-year json 수정
- PDF filename rename
- PDF 파일 복사 / 편집 / OCR 산출물 신규 생성
- `pdf_pages/index.json` 수정
- app code 수정
- app alias resolver 구현
- app/data alias registry 추가
- record metadata field 추가
- 기기-17 caution 해제 선언
- Batch migration 진입 (Inseparable 영역)
- persisted user data migration (Inseparable 영역)
- 66항 systemic policy를 q52 registry 영역에 흡수
- missing 29 recovery 실행 (별 트랙 분리 유지)
- 100 records audit 결과로 Batch migration 자동 진입 (§9 G1~G4 gate 영역)
- 추정 영역을 확정 영역으로 처리 (§5.2)
- 후보 C (split policy) 진입 (E1 + E3 + E5 + E6 부적합 확정 유지)

---

## 13. 다음 실행 Gate (각 별 명시 승인 후)

| step | 영역 |
|---|---|
| **S1** 본 plan 별 review (별 트랙) | plan 적절성 검토 영역 |
| **S2** 100 records audit 실행 별 명시 승인 | 본 plan §4 5 phase 실행 영역 |
| **S3** Phase A PDF inventory 실행 (read-only) | 별 명시 승인 + audit 영역 진입 |
| **S4** Phase B record-PDF 매핑 (read-only) | 별 명시 승인 + 매핑 영역 |
| **S5** Phase C mis-label 패턴 분류 | 별 명시 승인 + 분류 영역 |
| **S6** Phase D alias 확장 evidence 충족 평가 | 별 명시 승인 + 평가 영역 |
| **S7** Phase E audit 보고서 작성 | 별 명시 승인 + 보고서 영역 |
| **S8** 99 records alias 확장 evaluation 트랙 진입 결정 | audit 결과 입력 후 별 명시 승인 |
| **S9** registry artifact 확장 (별 명시 승인) | §8 C1~C7 충족 영역 |

본 plan 단계 = S0 (plan 작성). 실제 실행 S2~S9는 별 명시 승인 후만.

Batch migration은 본 audit / alias 확장 영역과 별 트랙 — §9 G1~G4 모두 충족 영역까지 진입 차단 유지.

---

## 14. Decision Record 영향

본 plan은 **plan-only 영역** — 정책 변경 0:

- separability framework (E6) 유지
- registry artifact baseline 유지
- q52 Permanent Invariant 유지
- 66항 policy = defer 유지
- caution release 차단 유지
- Batch migration 차단 유지

→ jsonl `trap_map_active_decisions.jsonl`에 별 entry 추가 안 함 (사용자 가이드:
"JSONL은 plan-only면 추가하지 말 것. 정책 결정이 새로 생기면 별도 판단"
정합).

본 plan 문서 자체가 100 records source audit plan으로 충분.

---

## Status

- 100 records 전수 source audit plan 작성 완료.
- audit unit = record 단위 (q52 alias registry row 영역과 정합).
- 5 phase 절차: A PDF inventory → B record-PDF 매핑 → C mis-label 패턴 분류 →
  D alias 확장 evidence 충족 평가 → E 보고서.
- 표기 정책: 확정 / 강한 가설 / 추정 / 미매칭 4 영역 분리.
- 99 records alias 확장 evidence 요구사항: R1~R7 7 영역.
- q52 Permanent Invariant guardrail 5 영역 적용.
- registry artifact 확장 조건: C1~C7 7 영역.
- Batch migration gate 분리: G1~G4 4 영역.
- 본 plan = S0 (plan 작성 단계). 실제 audit 실행 S2~S9는 별 명시 승인 후만.
- 정책 변경 0 — separability framework / registry baseline / Permanent Invariant /
  66항 defer / caution release / Batch migration 모두 유지.
- jsonl decision entry 추가 안 함 (사용자 가이드 정합 — plan-only).
- app code / app data / questions.json / per-year / PDF / pdf_pages / registry
  artifact 모두 변경 0. resolver implementation / migration / framing 확장 0.
- 기기-17 caution 유지. registry row status=candidate 유지. Batch migration 차단
  유지. caution release 차단 유지. q52 storage_id 단독 변경 영구 금지.
- 다음 gate: S1 plan review / S2 audit 실행 별 명시 승인 / 별 트랙 6 영역 (99
  records alias 확장 / E4 / 외부 source / 66항 재evaluation / missing 29 recovery
  / 1·3·4 verification).
