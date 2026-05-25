# Trap-Map B-Priority — `2020_1,2회` 66항 Session-Label Policy Evaluation (2026-05-25)

기기-17 alias schema plan §8 + correction plan v2 §7A + 66항 separability
evaluation Q6 + App/data decision §7 모두에서 "별 systemic session-label policy
문서 필요"로 확정한 영역의 docs-only policy evaluation을 수행한다. 본 문서는
`2020_1,2회` 66항 systemic session-label problem에 대해 가능한 정책 후보를
비교하고 현 단계 결정/보류를 정의한다.

이번 단계는 **docs-only policy evaluation**. **app code, app/data, questions.json,
per-year json, PDF filename, pdf_pages/index.json, registry artifact 모두
수정 금지**. Batch migration 실행 금지. push 없음. amend/rebase/reset 없음.
기기-17 caution 유지. q52 단독 id 재발급 금지 유지. registry row promotion 금지
유지.

- 관련 separability evaluation: `docs/audit/trap_map_B_priority_gigi_17_66item_separability_evaluation_2026-05-25.md` (`DR-TRAP-GIGI17-66ITEM-SEPARABILITY`, partial separability)
- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`
- 관련 correction plan: `docs/audit/trap_map_B_priority_gigi_17_B_track_correction_plan_v2_2026-05-25.md`
- 관련 App/data decision: `docs/audit/trap_map_B_priority_gigi_17_app_data_decision_2026-05-25.md` (`DR-TRAP-GIGI17-APPDATA-DECISION`)
- 관련 runtime resolver design review: `docs/audit/trap_map_B_priority_gigi_17_runtime_resolver_design_review_2026-05-25.md`
- 관련 registry artifact review: `docs/audit/trap_map_B_priority_gigi_17_alias_registry_artifact_review_2026-05-25.md` (PASS 12/12)
- new decision id: `DR-TRAP-2020-12-66ITEM-SESSION-LABEL-POLICY`

---

## 1. Evidence Summary (read-only count, 수정 0)

### 1.1 questions.json count

| 항목 | count |
|---|---:|
| 전체 records | 5,331 |
| `year=2020, session="1회"` | 100 |
| `year=2020, session="1,2회"` | 66 |
| `year=2022, session="1회"` | 0 |
| 정확한 `(year, session, q_no)` 중복 (non-null) | 0 |

→ impact audit §1 + separability evaluation §1 명시 값과 정확 일치. q52 양 영역
공존:
- `2020_1회_52` = 변압기 권수비 (true source = 2022 1회 q52)
- `2020_1,2회_52` = 동기전동기 V곡선

### 1.2 per-year files

| 파일 | count |
|---|---:|
| `data/questions_기출_2020_1회.json` | 100 |
| `data/questions_기출_2020_1_2회.json` | 66 |

→ master ↔ per-year 1:1 정합.

### 1.3 pdf_pages/index.json keys

| prefix | count | keys |
|---|---:|---|
| `2020_1회_*` | 5 | `2020_1회_53`, `2020_1회_71`, `2020_1회_72`, `2020_1회_73`, `2020_1회_79` |
| `2020_1,2회_*` | 4 | `2020_1,2회_59`, `2020_1,2회_73`, `2020_1,2회_76`, `2020_1,2회_77` |
| `2022_1회_*` | 0 | — |

→ impact audit §4 명시 값과 정확 일치. q52는 양 prefix 모두 index key 없음
(`2020_1회_52` / `2020_1,2회_52` 둘 다 없음).

### 1.4 q52 관계 (66항 separability evaluation §2.1 재확인)

| record | content | 영역 |
|---|---|---|
| `2020_1회_52` | 변압기 권수비 | q52 alias registry 대상 (canonical_source_id = `2022_1회_52`) |
| `2020_1,2회_52` | 동기전동기 V곡선 | **별 66항 population에 포함**. q52 alias row와 별 storage key |

→ q52 alias registry는 `2020_1,2회_52`를 *normalize하지 않음* (separability
evaluation §2.3 / registry artifact review checklist 9 PASS와 정합).

---

## 2. 5 정책 후보 비교

### 2.1 후보 A — 보류 유지 (Defer / Unresolved Residual Risk)

**내용**:
- 66항 session-label은 현 상태 (`year=2020, session="1,2회"`) 유지
- 변경 0건 — 별 정책 결정 보류
- 보류 사유와 evidence 요구사항을 docs에 명시

| axis | 평가 |
|---|---|
| guardrail 정합 | ✓ 모든 forbidden 영역 변경 0 |
| blast radius | 0 (docs-only) |
| evidence 요구 | 낮음 (보류 사유만 명시) |
| caution release 영향 | 차단 유지 (separability Q4 Inseparable) |
| Batch migration 영향 | 차단 유지 (Q5 Inseparable) |
| q52 영역 영향 | 0 (separability Q1·Q2 Separable 정합) |
| 위험 | systemic problem 영구 잔존 |

### 2.2 후보 B — Alias Policy

**내용**:
- 66항 records를 별 정책으로 alias 처리
- 예: `2020_1,2회_*` → `2020_1회_*` 또는 `2020_2회_*` 중 1택 매핑

| axis | 평가 |
|---|---|
| guardrail 정합 | app/data 수정 또는 docs alias registry 추가 — 별 명시 승인 영역 |
| evidence 요구 | 중상 — 각 record가 1회 또는 2회 소속인지 분류 evidence 필요 |
| split 결정 부재 | 어느 회차로 alias할지 결정 evidence 부재 시 임의 alias 위험 |
| q52와의 분리 | alias schema plan §8 Policy bullet 2: "Do not use q52 alias schema to normalize 2020_1,2회" — 별 alias registry 또는 별 정책 영역 |
| 위험 | source identity 임의 결정 위험 |

### 2.3 후보 C — Split Policy (2020 1회/2회 분해)

**내용**:
- 66항을 `year=2020, session="1회"` + `year=2020, session="2회"`로 분해
- per-year 파일 / questions.json / pdf_pages 모두 영향

| axis | 평가 |
|---|---|
| guardrail 정합 | data 영역 다중 수정 — guardrail 정면 차단 |
| evidence 요구 | 매우 높음 — 각 record가 1회/2회 어느 쪽인지 source PDF에서 추적 필요 |
| 100항 영향 | 기존 `2020_1회` 100항 + split된 일부 records 결합 시 `(year, session, q_no)` 중복 위험 (q52 사례 — `2020_1회_52` 본문 vs `2020_1,2회_52` 본문이 다른 컨텐츠) |
| blast radius | 최대 (data + per-year + pdf_pages + app persisted key) |
| 위험 | split 결정 결과 100항과의 식별 충돌 영구 발생 가능 |

→ split policy가 가장 systemic 정합이나, 100항 mis-label 추정 (impact audit §1)
과 결합 시 다중 영역 변경 — 별 evaluation 트랙 필수.

### 2.4 후보 D — Batch migration과 묶어서 처리

**내용**:
- `2020_1회` 100항 → `2022_1회` 재귀속과 `2020_1,2회` 66항 split/alias를 함께
  실행

| axis | 평가 |
|---|---|
| guardrail 정합 | Batch migration 차단 영역 — 정면 차단 |
| 전제 조건 | 100항 source claim 전수 evidence + 66항 split/alias 결정 + app persisted key migration 설계 + pdf_pages sync plan |
| separability | Q5 Inseparable — 66항 policy가 Batch migration 선결 조건 |
| 의존 역방향 | Batch migration이 66항 policy 결정의 *전제*가 아니라, *66항 policy 결정이 Batch migration의 전제*임에 주의 |

→ 후보 D는 *Batch migration이 가능해진 후의 통합 실행 영역*. 66항 policy 자체
결정 영역 아님. 본 evaluation에서 D는 후보 자체로는 부적합.

### 2.5 후보 E — Docs Errata Only

**내용**:
- 66항 systemic problem을 docs errata로만 명시
- data/app 영역 변경 0

| axis | 평가 |
|---|---|
| guardrail 정합 | ✓ data/app 영역 변경 0 |
| blast radius | 0 (docs-only) |
| caution release 영향 | correction plan v2 §7A "Docs Errata Only: 66항은 별도 systemic issue로 유지하고 caution 해제 근거로 사용하지 않음" — caution release 차단 유지 |
| 위험 | systemic problem 영구 잔존, docs errata만으로 resolution claim 부정합 |

→ 후보 E는 후보 A의 *sub-variant*. defer (A) + docs errata 명시 = 사실상 동일
영역. E를 단독 정책으로 분리하지 않고 A에 흡수.

---

## 3. 8 Policy Question 답

### Q1 — 66항 issue를 q52 alias registry와 별 트랙으로 유지할지?

**A**: **Yes — 별 트랙 유지**.

근거:
- separability evaluation Q6 결론: "별 systemic session-label policy 문서 필요"
- alias schema plan §8 Policy bullet 1·2: "Do not fold the 66항 policy into the
  q52 alias seed row. Do not use q52 alias schema to normalize `2020_1,2회`"
- correction plan v2 §7A 정책 2: "66항 처리는 '기기-17 q52 단독 id 재발급 금지'와
  같은 guardrail 아래 별도 plan으로 다룬다"
- registry artifact review checklist 9 PASS: q52 registry는 66항 resolved claim
  0

### Q2 — 현 단계에서 66항을 split/alias/migration 중 하나로 확정할 evidence가 충분한지?

**A**: **No — 부족**.

근거:
- 66항 각 record의 1회/2회 소속 판정 evidence 부재 (split policy 전제)
- alias 시 어느 회차로 매핑할지 결정 evidence 부재 (alias policy 전제)
- Batch migration 전체 evidence (100항 source claim + persisted key migration)
  부재 (D 전제)
- 원본 PDF `data/문제_2020_1,2회_20260316.pdf`의 실제 시행 구조 (1회+2회 합본
  영역인지, 별 시험 영역인지) audit 부재

### Q3 — 부족하다면 보류 유지가 맞는지?

**A**: **Yes — 보류 유지가 정합**.

근거:
- guardrail 영역 변경 0
- Q2 evidence 부족 영역에서 임의 정책 결정은 source identity 임의 결정 위험
- correction plan v2 §7.3 measurable criteria 4번: "`2020_1,2회` 66항은 분해/
  alias/보류 중 하나로 명시 결정되어야 하며, '미정'이면 caution 해제 후보로
  올리지 않는다"
- → **명시 보류**는 "미정" 영역에서 *별 정책 영역으로 분류 결정*. caution
  release 차단 영역 유지하나, separable layer (registry / runtime design)는
  진행 가능.

### Q4 — 보류 유지가 caution release를 계속 차단하는지?

**A**: **Yes — 차단 유지**.

근거:
- separability evaluation Q4 Inseparable: "caution release review는 본 evaluation
  결과 + 별 systemic session-label policy 결정 + user-facing impact evidence +
  redryrun evidence 모두 입력 필요"
- 본 evaluation의 *보류 결정*은 separability decision의 입력이나, 별 policy
  *resolution 결정*은 아님
- 본 evaluation은 separability Q4의 입력 evidence를 *불충분 상태로 명시 동결* —
  caution release input 요구 사항은 미충족

### Q5 — 보류 유지가 q52 영역 (registry artifact / runtime design review / docs-only q52 inventory)에는 어떤 영향을 주는지?

**A**: **영향 0 — separable 영역 유지**.

근거:
- separability evaluation Q1·Q2 Separable 결론: registry creation/review separable
- registry artifact review PASS 12/12 (`f0b462c`) — 66항 resolved claim 0,
  caution remains
- App/data decision: 후보 A docs-only registry 유지 즉시 활성
- runtime resolver design review: design candidate 좁힘 (read-path citation
  resolver only + storage_id 불변)
- 본 evaluation의 보류 결정은 위 separable layer를 *건드리지 않음*

→ 66항 보류 상태에서도 q52 docs-only chain (registry / artifact review /
App/data decision / runtime design review) 모두 **PASS 유지**.

### Q6 — Batch migration 차단을 유지할지?

**A**: **Yes — 차단 유지**.

근거:
- separability evaluation Q5 Inseparable: "Batch migration은 66항 policy 선결
  조건"
- 본 evaluation 결과 = 보류 (resolution 미정)
- Batch migration 진입 조건 미충족 영구 (보류 해제 시까지)
- correction plan v2 §3.2 / §4.3 / §7.3 모두 Batch migration이 66항 policy 정의
  영역과 결합되어 있음

### Q7 — 다음에 66항 policy를 풀려면 필요한 evidence는 무엇인지?

**A**: **6 evidence 후보 영역**. 각 별 명시 승인 후 별 트랙으로 진입.

| evidence | 영역 | 양식 후보 |
|---|---|---|
| **E1 — 원본 PDF source audit** | `data/문제_2020_1,2회_20260316.pdf`의 실제 시행 구조 | PDF 표지 일자 / 페이지 구조 / 1회·2회 분리 영역 식별 |
| **E2 — record 분류 evidence** | 66항 각 record의 1회/2회 소속 판정 | source PDF 페이지 매핑 / q_no 분포 분석 |
| **E3 — 100항과의 충돌 영역 검증** | split 시 `2020_1회_*` 100항과의 `(year, session, q_no)` 중복 가능성 | impact audit §5 패턴 확장 분석 |
| **E4 — 다른 합본 PDF 패턴** | 다른 연도 합본 PDF 사례 비교 (있다면) | 합본 PDF inventory 검색 |
| **E5 — app persisted key 영향** | split / alias 시 storage key 변경 영역 | impact audit §3 패턴 재실행 |
| **E6 — separability re-evaluation** | 본 evaluation 보류 해제 시점 separability evaluation 재실행 | separability evaluation 양식 재사용 |

본 evaluation은 evidence 양식만 명시. 각 evidence 수집은 별 트랙.

### Q8 — decision record jsonl에 추가할 정도의 정책 결정인지?

**A**: **Yes — 진짜 정책 결정**.

근거:
- 본 evaluation은 *66항 policy 보류 + evidence 요구사항*을 동결
- separability evaluation의 입력 영역 (Q4 / Q5)에 영구 영향
- 후속 트랙 (caution release / Batch migration / E1~E6 evidence)의 gate 차단/
  활성 영역 영향
- 사용자 가이드: "이번 건은 66항 policy 상태를 결정하므로 jsonl entry 추가가
  자연스러움"

→ jsonl entry id: `DR-TRAP-2020-12-66ITEM-SESSION-LABEL-POLICY` 추가.

---

## 4. 결정 — 후보 A (Defer with Evidence Requirements)

### 4.1 동결 결정

본 evaluation은 **후보 A — 보류 유지 + evidence 요구사항 명시**를 1택으로 동결한다.

### 4.2 보류 사유

- Q2: split/alias/migration 결정에 필요한 evidence 부재
- 임의 정책 결정 시 source identity 임의 결정 위험
- guardrail (app/data 변경 금지) 정합

### 4.3 보류 상태의 의미

- 66항 systemic session-label problem은 *명시 보류 영역* (미정 아님 — "보류"
  분류)
- caution release input 영역에서 "보류" 상태 = *evidence 요구사항 미충족* —
  차단 유지
- Batch migration 선결 조건 미충족 — 차단 유지
- q52 separable layer 변경 0 — 기존 PASS 유지

### 4.4 보류 해제 조건

별 트랙에서 E1~E6 evidence 모두 또는 충분한 subset 수집 + 별 정책 (B / C / D
중 1택) 결정 + 본 evaluation 재실행.

---

## 5. q52 영역 영향 — Separable Layer 유지

본 보류 결정은 다음 영역에 영향 0:

| 영역 | 상태 |
|---|---|
| registry artifact (`9868f95`) | candidate 유지, baseline 유지 |
| registry artifact review PASS (`f0b462c`) | PASS baseline 유지 |
| 66항 separability evaluation (`d9b2efd`) partial separability 결론 | 유지 |
| App/data decision (`9c1d387`) 후보 A + B-design-review | 유지 |
| Runtime resolver design review (`6ac1a9b`) design candidate | 유지 |
| 기기-17 caution | 유지 (`caution remains` 명시) |
| q52 단독 id 재발급 금지 | 유지 |

separability evaluation Q1·Q2 Separable 결론은 본 보류 결정으로 변경되지 않는다.

---

## 6. Caution Release / Batch Migration 영향 — Inseparable Layer 차단 유지

| layer | 상태 |
|---|---|
| **Caution release** (Step 6) | **차단 유지** — separability evaluation Q4 Inseparable + 본 evaluation 보류 결정으로 input 요구사항 미충족 |
| **Batch migration** | **차단 유지** — separability evaluation Q5 Inseparable + 본 evaluation 보류 결정으로 선결 조건 미충족 |

---

## 7. Forbidden Until Separate Approval

- q52 단독 id 재발급
- `questions.json` 수정 (66항 split / alias 포함)
- per-year json 수정 (`data/questions_기출_2020_1_2회.json` 분해 포함)
- PDF filename rename
- `pdf_pages/index.json` 수정 (66항 prefix 이동/추가 포함)
- app code 수정 (66항 영역 resolver 포함)
- app alias resolver 구현
- app/data alias registry 추가
- record metadata field 추가
- registry row promotion from `candidate` to `approved`
- 기기-17 caution 해제 선언
- Batch migration 진입
- 66항 systemic policy를 q52 registry 영역에 흡수
- registry artifact 자체 수정
- 보류 해제 선언 (별 명시 승인 + E1~E6 evidence 수집 + 별 정책 결정 후만 가능)

---

## 8. Next Gates

각 별 명시 승인 후만 진행:

1. **E1 — 원본 PDF source audit** (별 트랙, read-only)
   - `data/문제_2020_1,2회_20260316.pdf` 표지 일자 + 페이지 구조 + 1회/2회 분리
     영역 식별
2. **E2 — record 분류 evidence 수집** (별 트랙)
   - 66항 각 record의 source PDF 페이지 매핑
3. **E3~E6 evidence 수집** (별 트랙)
4. **66항 policy 재evaluation** (E1~E6 충분 수집 후 본 evaluation 재실행)
5. **Implementation plan** (q52 alias resolver 구현 진입 결정 시, design candidate
   기반)
6. **Caution release review** (Step 6, 본 evaluation 보류 해제 + design candidate
   구현 + user-facing impact evidence + redryrun evidence 모두 입력 후)

---

## Status

- 66항 session-label policy evaluation 작성 완료.
- 결정: **후보 A — 보류 유지 + evidence 요구사항 명시** (defer with evidence
  requirements).
- 보류 사유: split/alias/migration 결정 evidence 부재.
- caution release 차단 유지 (separability Q4 + 본 보류).
- Batch migration 차단 유지 (separability Q5 + 본 보류).
- q52 separable layer (registry / review / App/data / design) 영향 0.
- 기기-17 caution 유지.
- registry row status=candidate 유지.
- E1~E6 evidence 후보 영역 명시 (별 트랙).
- 본 evaluation은 진짜 정책 결정이므로 jsonl entry 1줄 추가 영역.
- 다음 gate: E1~E6 evidence 수집 (별 트랙) / Implementation plan / Caution release
  review.
