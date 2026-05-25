# Trap-Map B-Priority — `2020_1,2회` 66항 Missing-29 Recovery Evaluation (2026-05-25)

E2 record-PDF mapping audit (`5f1c9c5`)에서 식별한 누락 29 q_no가 *PDF source
정상 출제 + per-year/master 미등재* 영역임이 확정된 후, 본 누락 영역을 recovery
대상으로 볼지 / 별 data debt로 분리할지 / 현 B-track에서 보류할지 평가한다.

이번 단계는 **docs-only evaluation**. **app/data, questions.json, per-year json,
PDF filename, pdf_pages, app code, OCR 산출물, 어떤 파일도 수정하지 않는다.**
missing29 recovery 실행 금지. push 없음. amend/rebase/reset 없음. 기기-17
caution 유지. q52 단독 id 재발급 금지 유지. registry row promotion 금지 유지.
Batch migration 실행 금지.

- 관련 E2 audit: `docs/audit/trap_map_B_priority_2020_1_2_66item_E2_record_pdf_mapping_audit_2026-05-25.md`
- 관련 E1 audit: `docs/audit/trap_map_B_priority_2020_1_2_66item_E1_source_audit_2026-05-25.md`
- 관련 policy evaluation: `docs/audit/trap_map_B_priority_2020_1_2_66item_session_label_policy_2026-05-25.md` (`DR-TRAP-2020-12-66ITEM-SESSION-LABEL-POLICY`)
- 관련 separability evaluation: `docs/audit/trap_map_B_priority_gigi_17_66item_separability_evaluation_2026-05-25.md`
- 관련 App/data decision: `docs/audit/trap_map_B_priority_gigi_17_app_data_decision_2026-05-25.md`
- new decision id: `DR-TRAP-2020-12-MISSING29-DATA-DEBT`

---

## 1. 사전 측정 재확인

### 1.1 누락 29 q_no 양 source 부재 재확인

| source | missing 29 중 등재된 q_no count | 기대값 |
|---|---:|---:|
| `data/questions_기출_2020_1_2회.json` (per-year) | 0 | 0 |
| `app/data/questions.json` `year=2020, session="1,2회"` (master) | 0 | 0 |

→ **누락 29 q_no가 per-year + master 양 source에 모두 부재 재확인** (`True`).

### 1.2 보조 PDF Verification — q43 (page 16) 추가 확인

E2 audit에서 직접 verification 영역 외였던 3과목 누락 영역 중 q43 추가 read:

- PDF page 16 (book page 921) 영역
- q43 본문 인용:
  > "3선 중 2선의 전원 단자를 서로 바꾸어서 결선하면 회전방향이 바뀌는 기기가
  > 아닌 것은?"
- 보기 ①~④, 정답 **④ 정류자형 주파수 변환기**

→ **q43 PDF 정상 출제 등재 확인**. E2 핵심 발견 ("누락 원인 = 데이터 추출/등재
누락") **강화**. 3과목 3건 (q43, q50, q55) 중 q43 직접 verification 통과.

---

## 2. 5 Recovery 후보 비교

### 2.1 후보 A — 별 data debt로 분리 (B-track과 분리, 별 트랙)

**내용**:
- missing 29 q_no를 *별 data recovery debt*로 분리
- 현 B-track (q52 alias / caution release / 66항 policy)과 *명시 분리*
- recovery 실행은 별 트랙·별 명시 승인 후

| axis | 평가 |
|---|---|
| guardrail 정합 | ✓ docs-only, app/data 변경 0 |
| blast radius | 0 (docs-only) |
| recovery 가능성 | source exists → recovery 후보 |
| B-track 영향 | 0 (분리 명시) |
| q52 영역 영향 | 0 (q52는 누락 영역 외) |
| 위험 | data debt가 영구 잔존 가능성 (별 트랙 진행 결정에 의존) |

### 2.2 후보 B — 현 B-track에서 recovery 즉시 실행

**내용**:
- missing 29 q_no를 현 B-track 영역에서 직접 recovery
- per-year + master에 29 records 추가

| axis | 평가 |
|---|---|
| guardrail 정합 | per-year + master 수정 영역 — guardrail 직접 차단 |
| blast radius | 중상 (per-year + master 29 records 추가 + pdf_pages 영역 평가 + app IndexedDB 무영향 확인) |
| evidence 요구 | 매우 높음 — OCR 또는 별 source + answer key + extraction tool 영역 정책 |
| B-track 영향 | scope creep — q52 alias / caution release / 66항 policy와 영역 충돌 |
| q52 영역 영향 | 0 (q52 누락 영역 외) — recovery 자체는 q52 영역 변경 안 함 |
| 위험 | B-track scope 영역 확장 + recovery 실패 시 부분 등재 영역 잔존 |

→ **비권장**. B-track scope 영역 영구 확장 위험.

### 2.3 후보 C — 보류 (recovery 가능성 부재 가정)

**내용**:
- missing 29를 recovery 영역으로 인정하지 않음
- 현 66 records를 영구 유지

| axis | 평가 |
|---|---|
| guardrail 정합 | ✓ 변경 0 |
| evidence 부정합 | E2 audit 확정 ("source exists, data missing")과 충돌 |
| 위험 | recovery 후보가 실제로 존재함에도 불구하고 인정 안 함 = source identity 부정확 |

→ **부적합**. E2 audit evidence와 충돌.

### 2.4 후보 D — per-year만 정정, master 미수정

**내용**:
- per-year file에 29 records 추가
- master는 별 트랙으로 미루기

| axis | 평가 |
|---|---|
| guardrail 정합 | per-year 수정 영역 — guardrail 차단 |
| 정합성 | E2 audit 확정 "per-year ↔ master 100% 정합" 영역 깨짐 |
| 위험 | per-year ↔ master 정합 영구 깨짐 → 후속 audit 영역 영구 불일치 |

→ **부적합**. 정합 영역 깨짐 위험.

### 2.5 후보 E — recovery 영역 무시 (현 상태 영구 유지)

**내용**:
- recovery 영역 자체를 docs에서도 다루지 않음
- 현 상태 영구 유지

| axis | 평가 |
|---|---|
| guardrail 정합 | ✓ 변경 0 |
| evidence 영역 | E2 audit 결과 + 본 evaluation 영역이 ignored |
| 위험 | data debt 자체가 documented evidence에서 보이지 않음 → 후속 audit에서 영역 재발견 영구 |

→ **부적합**. evidence 영역 무시는 audit history 부정합.

---

## 3. 8 Evaluation Question 답

### Q1 — missing 29는 recovery 후보인가, source policy 후보인가?

**A**: **recovery 후보**.

근거:
- E2 audit §3 확정: "source exists, data missing" (PDF 18건 직접 verification +
  본 audit §1.2 q43 추가 verification으로 19건)
- source identity 영역에는 누락 0건 (PDF 1~95 정상 출제)
- per-year/master 영역에서 데이터 추출/등재 누락 = recovery 영역
- E1 audit이 확정한 source policy (PDF 합본 시험 + split 부적합)와 **별 영역**

→ **recovery 후보** (source policy 후보가 *아님*).

### Q2 — 누락 29를 지금 B-track에서 복구해야 하는가?

**A**: **No — 현 B-track에서 복구 안 함**.

근거:
- 현 B-track scope = q52 alias registry / runtime resolver design / App/data
  decision / 66항 session-label policy / caution release / Batch migration
  evidence
- missing 29 q_no는 위 6 영역 어느 곳과도 *직접 연결 없음* (Q5 답 참조)
- 후보 B 분석: scope creep + recovery 실패 시 부분 등재 영역 잔존 위험
- 현 guardrail "app/data·questions.json·per-year json 명시 승인 전 수정 금지"
  직접 차단

→ **현 B-track 영역 외 — 별 트랙으로 분리**.

### Q3 — recovery를 하려면 필요한 최소 evidence는 무엇인가?

**A**: **5 evidence 영역**.

| evidence | 영역 |
|---|---|
| **R1 — extraction tool 영역 결정** | OCR (Mathpix 또는 별 도구) / manual transcription / 다른 source |
| **R2 — answer key source** | 누락 29 q_no의 정답 source (PDF 자체 정답 + 별 검증 source) |
| **R3 — 추출 누락 cause 식별** | 연속 pair/triple 패턴 (2과목 24-25-26 / 4과목 61-62/67-68/71-72) 원인 — 추출 도구 영역의 page-batch 누락 vs OCR 단계 부재 등 |
| **R4 — per-year + master sync 정책** | 29 records 추가 시 양 source 동시 sync 양식 결정 (E2 audit 정합 영역 유지) |
| **R5 — pdf_pages index 동기화 정책** | 누락 29 q_no 중 pdf_pages 영역 필요한 q_no 식별 (현재 `2020_1,2회_*` 4 keys만, 추가 영역 결정) |

본 evaluation은 evidence 양식만 명시. R1~R5 수집은 별 트랙.

### Q4 — recovery가 app/data/questions/per-year/pdf_pages에 미치는 범위는?

**A**: **4 영역 변경 + 1 영역 무영향**.

| 영역 | 변경 영역 |
|---|---|
| `data/questions_기출_2020_1_2회.json` (per-year) | 29 records 추가 (66 → 95) |
| `app/data/questions.json` (master) | 29 records 추가 (5,331 → 5,360) |
| `data/pdf_pages/index.json` | 누락 29 중 pdf_pages 필요 q_no만 추가 (현재 4 keys → 평가 후 +N) |
| PDF source | **무영향** (이미 정상 출제, 변경 0) |
| app code (IndexedDB / qId / lookup) | **무영향** — 신규 q_no가 동일 `year_session_q_no` 양식이라 IndexedDB key path 변경 0 / `qId()` 함수 변경 0 / lookup 영역 변경 0 |

→ recovery는 *data 영역 추가만* 발생. app code 영향 0. 단 별 명시 승인 영역.

### Q5 — recovery가 q52 alias registry / runtime resolver / caution release와 직접 연결되는가?

**A**: **No — 모두 무관**.

근거:

| 영역 | 연결 분석 |
|---|---|
| q52 alias registry (9868f95) | row `2020_1회_52` storage_id → `2022_1회_52` canonical (별 PDF `data/20200424_1회.pdf` p.4 q52). 본 PDF `2020_1,2회`의 q52 (`2020_1,2회_52`, 동기전동기 V곡선)는 **별 영역**. 누락 29 q_no에 `2020_1,2회_52` 포함 0 (q52는 per-year present) |
| runtime resolver design (6ac1a9b) | design candidate = q52 한정 (66항 영역 미진입). missing 29 영역은 *66항 별 영역*과도 별 — *추출 누락 영역* |
| caution release (Step 6) | input 영역 = 본 evaluation + 별 systemic policy + user-facing impact + redryrun. missing 29는 *위 4 input 어느 영역과도 직접 연결 없음* |
| App/data decision (9c1d387) | direction = 후보 A docs-only + 후보 B design review only. missing 29 recovery는 *후보 B 영역 외*, 별 data 영역 |

→ **모두 무관**. missing 29 recovery는 *완전 별 트랙*.

### Q6 — 66항 policy defer 상태를 유지할지 갱신할지?

**A**: **Defer 유지 + evidence requirement에 missing 29 recovery policy 추가**.

근거:
- 본 evaluation은 *66항 split/alias/migration 결정 evidence를 추가하지 않음*
- 66항 policy의 핵심 영역 (`2020_1,2회` records 자체의 1회/2회 소속 또는
  alias 정책) = 본 evaluation 영역 외
- missing 29는 *66항 records 영역의 부분 데이터 누락*이며, 66항 자체의 systemic
  label 영역과 *별 cause*

단 evidence requirement 갱신 영역:
- E1: 원본 PDF source audit (완료, 5c1fecc)
- E2: record-PDF page mapping (완료, 5f1c9c5)
- **E2-A (신규)**: missing 29 recovery policy (본 evaluation 결정 영역)
- E3~E6: 기존 영역 유지
- 외부 source: 기존 영역 유지

본 evaluation으로 **E2-A 추가** = 66항 policy defer 영역에 1개 evidence
requirement 영역 추가. 단 *66항 policy decision 자체*는 변경 0 (defer 유지).

### Q7 — missing 29를 별도 data debt로 분리할지?

**A**: **Yes — 별 data debt로 분리**.

근거:
- 후보 A (별 data debt 분리) = 5 후보 중 정합 1택
- Q5 답: q52 alias registry / runtime resolver / caution release와 모두 무관
- Q2 답: 현 B-track scope 영역 외
- separability evaluation 양식 정합: q52 separable layer 영역 영향 0

→ **missing 29를 별 data debt로 분리 결정**. 본 evaluation 1차 정책 결정 영역.

### Q8 — 다음 gate는 무엇인지?

**A**: **3 별 트랙 영역**.

| 트랙 | 영역 |
|---|---|
| **missing 29 recovery plan** (별 트랙) | R1~R5 evidence 수집 + recovery 정책 결정 + 별 명시 승인 후 실행 |
| **1·3 과목 verification 보강** (별 트랙, read-only) | E2 audit에서 직접 verification 영역 외였던 1과목 7건 (q3, q4, q9, q10, q13, q16, q20) + 3과목 2건 (q50, q55) + 4과목 1건 (q80) 추가 PDF read-only verification |
| **66항 policy 재evaluation** (별 트랙) | E1~E2 + missing 29 분리 결정 + E3~E6 + 외부 source 충분 수집 후 |

본 evaluation은 위 3 트랙 진입을 *gate로 활성화* 영역만. 실제 진입은 별 명시
승인 후.

---

## 4. 결정 — 후보 A (별 data debt 분리)

### 4.1 동결 결정

본 evaluation은 **후보 A — missing 29를 별 data recovery debt로 분리**를 1택으로
동결한다.

### 4.2 분리 룰

- missing 29 q_no recovery는 *별 트랙*에서 다룬다 — `data debt: missing29
  for 2020_1,2회 per-year + master extraction`
- 현 B-track의 q52 alias / runtime resolver / caution release / 66항 policy /
  Batch migration 영역과 *명시 분리*
- recovery 실행은 별 명시 승인 영역 (R1~R5 evidence 수집 후)
- 별 트랙 진행 결정 없으면 *data debt 영구 잔존* — docs에는 명시 영역으로 기록

### 4.3 66항 policy defer 유지

- 66항 systemic policy 결정 = **defer 유지** (변경 0)
- evidence requirement에 **E2-A (missing 29 recovery policy)** 추가

### 4.4 q52 영역 정합

- q52는 누락 영역 외 (per-year present set 포함)
- q52 alias registry / runtime design / artifact review PASS / App/data decision /
  separability evaluation 모두 영향 0
- 기기-17 caution 유지

### 4.5 차단 유지 영역

- caution release (Step 6) — separability Q4 + 66항 policy defer + 본 evaluation
  분리
- Batch migration — separability Q5 + 66항 policy 선결
- registry row promotion to approved
- 후보 C (split policy) — E1 부적합 확정

---

## 5. Residual Risk

| risk | severity | 본 evaluation에서의 처리 |
|---|---|---|
| missing 29 data debt 영구 잔존 | Medium | 별 트랙 진입 결정 없으면 영구. docs에 명시 영역으로 기록 |
| R1~R5 evidence 수집 미진행 | Medium | 별 트랙 영역, 본 evaluation 영역 외 |
| 추출 도구 영역의 동일 누락 패턴이 다른 연도 PDF에도 있을 가능성 | Medium | 별 evaluation 트랙 영역 (`missing pattern across years` 가설) |
| 1·3·4 과목 일부 누락 q_no 직접 verification 미완 | Low | 별 트랙 read-only verification 영역 |
| missing 29 recovery가 별 systemic label policy 영역과 결합될 가능성 | Low | 본 evaluation에서 무관 확정, 단 별 트랙 결정 시 재평가 영역 |

---

## 6. 다음 Gate (각 별 명시 승인 후만 진행)

### 6.1 직접 활성화된 후보 영역

- **missing 29 recovery plan 작성** (별 트랙) — R1~R5 evidence 양식 + 정책 결정
- **R1 extraction tool 영역 결정** — OCR / manual / 다른 source 1택
- **R2 answer key source 영역 결정** — PDF 자체 정답 + 별 검증 source
- **R3 추출 누락 cause 식별** — 연속 pair/triple 패턴 분석
- **R4 per-year + master sync 정책** — 양 source 동시 sync 양식
- **R5 pdf_pages index 동기화 정책** — 누락 q_no 중 pdf_pages 필요 영역

### 6.2 1·3·4 과목 직접 verification 보강 (별 트랙, read-only)

- 1과목: q3, q4, q9, q10, q13, q16, q20 (7건)
- 3과목: q50, q55 (2건, q43은 본 evaluation에서 추가 verification 완료)
- 4과목: q80 (1건)

### 6.3 E1 audit이 정의한 후속 evidence (유지)

- E3, E4, E5, E6
- 외부 source evidence
- 66항 policy 재evaluation

---

## 7. Forbidden Until Separate Approval

- q52 단독 id 재발급
- `questions.json` 수정 (missing 29 추가 포함)
- per-year json 수정 (missing 29 추가 포함)
- PDF filename rename
- PDF 파일 복사 / 편집 / OCR 산출물 신규 생성
- `pdf_pages/index.json` 수정
- app code 수정
- app alias resolver 구현
- app/data alias registry 추가
- record metadata field 추가
- registry row promotion from `candidate` to `approved`
- 기기-17 caution 해제 선언
- Batch migration 진입
- 66항 systemic policy를 q52 registry 영역에 흡수
- registry artifact 자체 수정
- 66항 policy defer 해제 선언 (E3~E6 + missing 29 별 트랙 + 별 정책 결정 후만)
- missing 29 recovery 실행 (R1~R5 evidence + 별 명시 승인 후만)
- 후보 C (split policy) 진입 (E1 부적합 확정 유지)

---

## 8. Decision Record 영향

본 evaluation은 **진짜 정책 결정 영역**:

- missing 29를 별 data debt로 분리 (1차 결정)
- 66항 policy evidence requirement에 E2-A 추가 (defer 유지)
- 후보 A 동결 / B·C·D·E 비권장 또는 부적합

→ jsonl `trap_map_active_decisions.jsonl`에 별 entry 1줄 추가 (사용자 가이드:
"missing29를 별도 debt로 분리할지 결정하면 jsonl entry 추가가 자연스러움"
정합).

new decision id: `DR-TRAP-2020-12-MISSING29-DATA-DEBT`

---

## Status

- missing 29 recovery evaluation 작성 완료.
- 결정: **후보 A — missing 29를 별 data recovery debt로 분리**.
- B/C/D/E 모두 비권장 또는 부적합.
- missing 29 recovery 실행 = 별 트랙 + 별 명시 승인 + R1~R5 evidence 후.
- q43 page 16 직접 verification 추가 — E2 핵심 발견 ("source exists, data
  missing") 강화 (19건 총 verification 통과).
- 66항 policy = **defer 유지** + evidence requirement E2-A (missing 29 recovery
  policy) 추가.
- q52 separable layer 영향 0 — registry artifact 9868f95 / review PASS / design
  review / separability 결론 모두 baseline 유지.
- 기기-17 caution 유지. caution release 차단 유지. Batch migration 차단 유지.
- 후보 C (split policy) 부적합 확정 유지.
- PDF / app code / app data / questions.json / per-year / pdf_pages / registry
  artifact 모두 변경 0.
- 본 evaluation은 진짜 정책 결정 영역이므로 jsonl entry 1줄 추가.
- 다음 gate: missing 29 recovery plan / 1·3·4 과목 verification 보강 / E3~E6 /
  외부 source / 66항 policy 재evaluation.
