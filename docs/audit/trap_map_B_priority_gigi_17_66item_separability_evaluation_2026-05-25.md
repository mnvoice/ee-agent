# Trap-Map B-Priority — 기기-17 `2020_1,2회` 66항 Separability Evaluation (2026-05-25)

alias schema plan §9 Step 3 / registry approval decision §6 Step 3에 정의된
"66항 separability evaluation"을 수행한다. 본 문서는 **separability 평가**이며,
66항 자체의 resolution이나 systemic session-label policy 결정을 하지 않는다.

이번 단계는 evaluation 작성까지다. **app/data, `questions.json`, per-year json,
PDF filename, `pdf_pages/index.json`은 수정하지 않는다.** push 없음.
amend/rebase/reset 없음. 기기-17 caution 유지. q52 단독 id 재발급 금지 유지.
registry row promotion to approved 금지 유지.

- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`
- 관련 correction plan: `docs/audit/trap_map_B_priority_gigi_17_B_track_correction_plan_v2_2026-05-25.md`
- 관련 schema plan: `docs/audit/trap_map_B_priority_gigi_17_alias_schema_plan_2026-05-25.md`
- 관련 approval decision: `docs/audit/trap_map_B_priority_gigi_17_alias_registry_approval_decision_2026-05-25.md`
- 관련 registry artifact: `docs/audit/registries/trap_map_gigi_17_alias_registry_2026-05-25.json`
- new decision id: `DR-TRAP-GIGI17-66ITEM-SEPARABILITY`

---

## 1. Evaluation Scope

본 evaluation이 답하는 질문:

| Q | 질문 |
|---|---|
| Q1 | q52 alias registry artifact **creation** (9868f95)이 66항 systemic policy 결정 없이 정합한가? |
| Q2 | q52 alias registry artifact **review** (별 review session 영역)가 66항 systemic policy 결정 없이 정합한가? |
| Q3 | **app/data decision** (Step 5, runtime resolver / app data registry / record metadata)이 66항 policy 없이 진입 가능한가? |
| Q4 | **caution release review** (Step 6)가 66항 separability decision 없이 진입 가능한가? |
| Q5 | **Batch migration**이 66항 policy 없이 진입 가능한가? |
| Q6 | 66항 자체 resolution은 q52 cleanup과 분리된 별 systemic session-label policy 문서가 필요한가? |

각 질문은 별 layer의 separability를 측정한다. 본 evaluation은 5 layer를 분리
평가하여 partial separability 결론에 도달한다.

---

## 2. Evidence Summary

### 2.1 영역 분리 근거

**q52 row scope (registry artifact `rows[0]`)**:
- `storage_id = 2020_1회_52` (legacy app key)
- `canonical_source_id = 2022_1회_52` (source citation id)
- `source_pdf = data/20200424_1회.pdf` p.4 q52
- 본 row는 *citation alias*만 표현. data normalization 아님.

**66항 scope (impact audit §1·§2·§5)**:
- `year=2020, session="1,2회"` 66 records
- per-year file `data/questions_기출_2020_1_2회.json` 66 records
- 별 systemic session-label problem (per-year + master 양식 분리)
- impact audit §1: `2020_1,2회_52` = 동기전동기 V곡선 (q52 자체와 *완전히 다른
  컨텐츠*)
- impact audit §5 L141-153: "같은 (year, session, q_no) 중복 0" / "2020_1회와
  2020_1,2회의 공존은 systemic label/pipeline 문제" / "기기-17 q52만의 isolated
  cleanup으로 보지 말고, 2020 1회/1,2회 session policy로 별도 설계해야 한다"

**두 scope 관계**:
- q52 row의 storage_id `2020_1회_52`와 66항의 `2020_1,2회_*` prefix가 *별 session
  값*. 직접 record-level 충돌 0건.
- impact audit §5: "정확한 `(year, session, q_no)` 중복 0" — 두 scope가 independent
  record set
- q52 row의 canonical_source_id `2022_1회_52`는 *비어 있는 슬롯*(2022_1회 0 records)에
  citation 영역. 66항(`2020_1,2회`)와 namespace 충돌 0건

→ **record-level separability 성립**.

### 2.2 systemic-level 비분리 근거

- impact audit §5: `2020_1회`(100 records) ↔ `2020_1,2회`(66 records) 공존이
  systemic label/pipeline 문제임을 명시
- correction plan v2 §7A 정책: "Alias-first를 채택해도 66항 문제가 사라진 것으로
  간주하지 않는다"
- correction plan v2 §7.3 Batch migration measurable criteria 4번 (L531-532):
  "`2020_1,2회` 66항은 분해/alias/보류 중 하나로 명시 결정되어야 하며, '미정'이면
  caution 해제 후보로 올리지 않는다"
- alias schema plan §8 Policy bullet 4: "Any caution release review must state
  whether unresolved 66항 risk is separable from q52 source citation cleanup"
- approval decision §5: "Caution release review cannot skip the 66항 separability
  evaluation"

→ **systemic-level 비분리 (caution release 차원)**.

### 2.3 registry artifact의 66항 resolved claim 부재 검증

`docs/audit/registries/trap_map_gigi_17_alias_registry_2026-05-25.json` 직접
inspection 결과:

| 항목 | 값 | 평가 |
|---|---|---|
| `rows` count | 1 (q52만) | 66항 row 0건. normalize claim 0 |
| `rows[0].storage_id` | `2020_1회_52` | `2020_1,2회_*` 영역 외 |
| `rows[0].canonical_source_id` | `2022_1회_52` | `2020_1,2회` namespace 외 |
| `rows[0].notes` | "legacy storage key retained; PDF filename/date mismatch handled as cover-date evidence; caution remains" | 66항 resolved claim 없음 |
| top-level `status` | `candidate` | approved promotion 0 — 66항 영향 평가 영역 외 |
| top-level `scope` | `gigi_17_b_track` | gigi_17 한정 — 66항 scope 외 |

→ **registry artifact 9868f95는 66항 resolved claim 없음 확인**. q52 alias
inventory에 한정.

---

## 3. Separability 평가 (Layer별)

### 3.1 Q1·Q2 — Registry artifact creation/review

**Layer**: alias schema plan §9 Step 4 (Registry artifact creation) + 후속
artifact review

**평가**: **Separable** (66항 policy 없이 정합)

**근거**:
- registry artifact 9868f95는 q52 candidate row 1건만 포함. 66항 row 0
- §2.3 검증: artifact가 66항 resolved claim을 하지 않음
- approval decision §5: registry artifact creation은 66항 separability evaluation과
  *parallel* 가능 영역
- alias schema plan §8 Timing bullet 2: "After alias schema review passes, 66항
  separability evaluation should start in parallel with registry artifact approval"
- artifact가 *gigi_17_b_track scope*로 한정 (top-level `scope` 필드)

**제약**:
- registry artifact가 66항 normalize 영역으로 확장될 경우 separability 재평가 필요
- 후속 row 추가 시 `2020_1,2회_*` storage_id가 등장하면 본 separability 무효
- artifact review는 q52 row 한정 — 66항 row review 영역 외

### 3.2 Q3 — App/data decision

**Layer**: alias schema plan §9 Step 5 (App/data decision — runtime resolver /
app data registry / record metadata)

**평가**: **Partial Separable** (조건부 분리 가능)

**근거 (separable 측)**:
- runtime resolver가 *q52 한정 read-path*로 한정될 경우 66항 policy 없이 진입
  가능 (technical layer 분리)
- app data registry가 docs registry mirror로 한정될 경우 q52 row만 다룸

**근거 (inseparable 측)**:
- impact audit §3 L96-105: app `_id` 체계가 `year_session_q_no` 기반 — 66항의
  `2020_1,2회_*` records도 같은 `_id` 체계 사용
- runtime resolver가 *전체 storage_id pool*을 다루면 66항 records도 영향 영역
- record metadata field 추가는 *모든 records 양식 변경* — 66항 records 영향 영역

→ **decision 의존**. App/data decision의 *범위 한정 결정* 시점에 본 separability
재평가 필요. 본 evaluation 단계에서는 Step 5 진입 가능성만 인정, 실행 분리
가능성은 Step 5 decision의 범위 한정으로 위임.

### 3.3 Q4 — Caution release review

**Layer**: alias schema plan §9 Step 6 (Caution release review)

**평가**: **Inseparable** (66항 separability decision 입력 필수)

**근거**:
- alias schema plan §8 Policy bullet 4: "Any caution release review must state
  whether unresolved 66항 risk is separable from q52 source citation cleanup"
- alias schema plan §9 Step 3 bullet 3: "Caution release review cannot skip this
  evaluation"
- approval decision §5: "Caution release review cannot skip the 66항 separability
  evaluation"
- approval decision §6 Step 5: "Only after registry artifact review, user-facing
  impact evidence, 66항 separability decision, and redryrun evidence exist"
- correction plan v2 §7.3 measurable criteria 4번: "'미정'이면 caution 해제 후보로
  올리지 않는다"
- correction plan v2 §7A 정책 3: "66항 미해결 상태에서 caution을 해제하려면, 그
  residual risk가 기기-17 source citation clean 여부와 분리 가능하다는 review
  근거가 필요하다"

→ **caution release review는 본 separability evaluation 결과를 입력으로 받음**.
본 evaluation 없이 caution release review 진입 금지.

### 3.4 Q5 — Batch migration

**Layer**: alias schema plan §8 Timing bullet 4 + correction plan v2 §2.2 / §3.2 /
§4.3 / §7.3

**평가**: **Inseparable** (66항 policy 선결 조건)

**근거**:
- alias schema plan §8 Timing bullet 4: "Batch migration cannot proceed until the
  66항 policy is defined"
- correction plan v2 §2.2 (Batch migration 단점 영역): blast radius에 66항 포함
- correction plan v2 §4.3 L261: "`2020_1,2회_*` 4건은 66항 session 정책 확정 전
  이동하지 않는다"
- correction plan v2 §7.3 measurable criteria 4번: 66항 분해/alias/보류 결정 필수

→ **Batch migration은 66항 policy 차단 영역 유지**. 본 evaluation은 Batch
migration 차단을 해제하지 않는다.

### 3.5 Q6 — 별 systemic session-label policy 문서 필요성

**평가**: **Yes — 별 문서 필요**

**근거**:
- impact audit §5: "기기-17 q52만의 isolated cleanup으로 보지 말고, 2020 1회/1,2회
  session policy로 별도 설계해야 한다"
- correction plan v2 §7A 정책 2: "66항 처리는 '기기-17 q52 단독 id 재발급 금지'와
  같은 guardrail 아래 별도 plan으로 다룬다"
- alias schema plan §8 Policy bullet 1: "Do not fold the 66항 policy into the q52
  alias seed row"
- alias schema plan §8 Policy bullet 2: "Do not use q52 alias schema to normalize
  `2020_1,2회`"

→ **66항 자체 resolution은 별 systemic session-label policy 문서가 필요**. 본
evaluation은 그 문서의 필요성을 확정하나, 작성 자체는 별 트랙으로 분리.

---

## 4. 평가 결론 — Partial Separability

5 layer 종합:

| Layer | 결론 | 근거 요약 |
|---|---|---|
| Q1·Q2 Registry creation/review | **Separable** | registry artifact가 q52 한정. 66항 row/normalize 없음 |
| Q3 App/data decision | **Partial Separable** | decision 범위 한정 시 separable. record metadata field는 inseparable |
| Q4 Caution release review | **Inseparable** | 본 evaluation 결과가 입력. 별 systemic policy 결정도 필요 |
| Q5 Batch migration | **Inseparable** | 66항 policy 선결 조건. 차단 영역 유지 |
| Q6 systemic session-label policy | **별 문서 필요** | q52 cleanup으로 해결 안 됨 |

종합 결론:
- **q52 alias inventory layer (Step 4 creation + 후속 review)는 separable** —
  registry artifact 9868f95는 이 가정 위에서 정합
- **caution release layer (Step 6)는 inseparable** — 본 evaluation 결과 + 별
  systemic policy 결정이 입력
- **Batch migration layer는 inseparable** — 66항 policy 차단 영역 유지
- **별 systemic session-label policy 문서가 필요** — 본 evaluation은 필요성만
  확정, 작성은 별 트랙

본 결론은 partial separability를 명시 인정한다. q52 alias inventory의 separability를
확정하되, 66항 systemic problem이 *영구 잔존*함을 caution release review의 입력
조건으로 둔다.

---

## 5. Residual Risk

### 5.1 Active residual

| risk | severity | 영향 |
|---|---|---|
| 66항 systemic session-label problem | Medium | caution release 차단 / Batch migration 차단 / 별 policy 문서 필요 |
| 100항 mis-label 추정 미확정 | Medium | impact audit §1: `2020_1회` 100 records 전체가 2022_1회 PDF에서 왔을 가능성. q52 외 99 records의 alias inventory는 별 evaluation 영역 |
| App/data decision 범위 한정 미정 | Medium | Step 5 decision의 범위 한정 결정 시 본 separability 재평가 필요 |

### 5.2 별 트랙 영역

다음 영역은 본 evaluation scope 외이며 별 트랙에서 처리:

- 66항 systemic session-label policy 문서 작성 (Q6 결론)
- 100항 (q52 외 99항) alias inventory 결정 (impact audit §1 추정 검증)
- App/data decision 범위 한정 (Step 5)

---

## 6. Decision Implications

### 6.1 본 evaluation이 활성화하는 gate

- **Step 4 (Registry artifact creation)**: 이미 9868f95에서 진입 완료. 본
  evaluation은 그 진입의 separability를 사후 확정
- **Step 4 후속 (Registry artifact review)**: 별 review session 진입 가능
- **App/data decision (Step 5)**: 범위 한정 결정으로 진입 가능 (단 범위 한정
  결정 시 본 separability 재평가)

### 6.2 본 evaluation이 차단 유지하는 gate

- **Caution release review (Step 6)**: 본 evaluation 결과 + 별 systemic policy
  결정 + redryrun evidence 모두 입력 필요
- **Batch migration**: 66항 policy 선결 조건 차단 유지
- **registry row promotion to approved**: 본 evaluation 영역 외 — 별 approval
  영역

### 6.3 본 evaluation이 명시 인정하는 한계

- 66항 systemic problem은 *영구 잔존* 영역 — q52 cleanup으로 해결 안 됨
- partial separability는 *layer별 분리 결론* — 모든 layer가 separable이라는
  주장 아님
- registry artifact가 separability decision 입력 영역에 한정 — runtime SoT 아님

---

## 7. Next Gates

별 명시 승인 후만 진행:

1. **Registry artifact review** (별 review session)
   - 9868f95 registry artifact 양식 / q52 row 값 / evidence_ref / guardrail
     review
   - row promotion 금지 룰 준수 review
2. **App/data decision** (Step 5, 범위 한정 결정)
   - runtime resolver / app data registry / record metadata 중 1택
   - 범위 한정 결정 시 본 separability 재평가
3. **별 systemic session-label policy 문서 작성** (별 트랙)
   - 66항 분해 / alias / 보류 중 1택 결정 필요
   - q52 cleanup과 분리된 별 plan
4. **Caution release review** (Step 6)
   - 본 evaluation 결과 + 별 systemic policy 결정 + redryrun evidence 입력
   - plan v2 §6.3 review format 양식

---

## 8. Forbidden Until Separate Approval

- q52 단독 id 재발급
- `questions.json` 수정
- per-year json 수정
- PDF filename rename
- `pdf_pages/index.json` 수정
- app alias resolver 구현
- app/data alias table 추가
- record metadata field 추가
- registry row promotion from `candidate` to `approved`
- 기기-17 caution 해제 선언
- Batch migration 진입 (66항 policy 결정 전)
- 66항 systemic policy를 q52 registry 영역에 흡수

---

## Status

- 66항 separability evaluation 작성 완료.
- 결론: partial separability — q52 alias inventory (Step 4) layer separable,
  caution release / Batch migration layer inseparable, 별 systemic policy 문서 필요.
- registry artifact 9868f95는 66항 resolved claim 0 확인.
- app/data/pdf_pages 미수정.
- q52 단독 id 재발급 금지 유지.
- 기기-17 caution 유지.
- Batch migration 차단 유지.
- 별 systemic session-label policy 문서 필요성 확정 (작성은 별 트랙).
