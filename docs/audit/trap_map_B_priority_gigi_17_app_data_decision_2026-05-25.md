# Trap-Map B-Priority — 기기-17 App/Data Decision (2026-05-25)

alias schema plan §9 Step 5 / registry approval decision §6 Step 4에 정의된
"App/data decision"을 수행한다. 본 문서는 q52 alias registry를 app/runtime/data
쪽에 어떻게 반영할지(또는 반영하지 않을지) 결정한다.

이번 단계는 **decision-only**. app/data 구현이나 data 수정을 진행하지 않는다.
**app/data, `questions.json`, per-year json, PDF filename, `pdf_pages/index.json`,
app code는 수정하지 않는다.** push 없음. amend/rebase/reset 없음. 기기-17 caution
유지. q52 단독 id 재발급 금지 유지. registry row promotion to approved 금지 유지.

- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`
- 관련 correction plan: `docs/audit/trap_map_B_priority_gigi_17_B_track_correction_plan_v2_2026-05-25.md`
- 관련 schema plan: `docs/audit/trap_map_B_priority_gigi_17_alias_schema_plan_2026-05-25.md`
- 관련 approval decision: `docs/audit/trap_map_B_priority_gigi_17_alias_registry_approval_decision_2026-05-25.md`
- 관련 registry artifact: `docs/audit/registries/trap_map_gigi_17_alias_registry_2026-05-25.json`
- 관련 artifact review: `docs/audit/trap_map_B_priority_gigi_17_alias_registry_artifact_review_2026-05-25.md` (PASS 12/12)
- 관련 separability evaluation: `docs/audit/trap_map_B_priority_gigi_17_66item_separability_evaluation_2026-05-25.md` (partial separability, `DR-TRAP-GIGI17-66ITEM-SEPARABILITY`)
- new decision id: `DR-TRAP-GIGI17-APPDATA-DECISION`

---

## 1. Decision Summary

| 항목 | 결정 |
|---|---|
| 현재 app/data 구현 승인 | **없음** |
| docs-only registry 상태 | PASS된 q52 candidate inventory artifact로 **유지** |
| runtime alias resolver | **설계 검토 (design review)만 다음 gate로 승인** — 구현은 별 명시 승인 영역 |
| app/data alias registry | **보류** — 별 명시 승인 + design review 통과 전 진입 금지 |
| question record metadata field | **보류** — record 양식 변경은 100항 mis-label 영역과 연동, 별 트랙 |
| Batch migration | **차단 유지** — 66항 policy 선결 조건 |
| caution release | **불가** — separability evaluation Q4 + user-facing impact evidence 부재 |
| registry row promotion | **금지 유지** — candidate → approved 승격 없음 |

이 결정은 **A (docs-only registry 유지) + B의 design review만 다음 gate로 승인**을
1택으로 동결한다. C / D / E는 보류, B의 구현은 별 명시 승인 영역.

---

## 2. App Code Read-Only Inspection (Decision 입력)

본 decision의 입력으로 사용한 app code read-only inspection 결과 (수정 0):

### 2.1 `qId()` / `_id` 생성 위치 — 3 영역

| 위치 | line | 양식 |
|---|---|---|
| `app/js/store.js` | L8 | `export function qId(q) { ... }` (module 양식) |
| `app/index.html` | L210 | inline `_questions.forEach(function(q) { q._id = q.year + '_' + q.session + '_' + q.q_no; })` |
| `app/js/main.js` | L138 | `function qId(q) { ... }` (legacy bundle) |

→ alias resolver 도입 시 3 위치 동시 정합 필요. 또는 단일 SoT 도입 영역 결정 필요.

### 2.2 `_id` 사용 위치 — `app/index.html` 다중

| line | 영역 |
|---|---|
| L210 | `_id` 생성 |
| L222 | `_questions` map 인덱스 |
| L389 | DOM `data-q-id` 속성 (question view) |
| L472 | DOM `data-q-id` 속성 (wrong-note item) |
| L625 | annotation save |
| L770 / L800 | progressMap lookup (search results / wrong list) |
| L887 | progress lookup (current question) |
| L911 | annotation load |
| L920 / L921 | progress save + progressMap update |
| L1046 | annotation clear |
| `app/js/main.js` L173 | _questions map indexing |

→ alias resolver 도입 시 영향 영역 = generation (3 위치) + lookup (다중 위치) + display (DOM `data-q-id`).

### 2.3 IndexedDB stores — `app/js/db.js`

| line | store | keyPath |
|---|---|---|
| L50 / L55 | annotations | `id` (qId 기반) |
| L64-67 | progress | `id` (qId 기반, `existing = { id: qId, wrongCount: 0 }`) |

→ persisted user data는 `qId` 기반 `id`로 indexed. legacy storage key 유지 시
persisted data migration 없음. canonical id 도입 시 migration 또는 compatibility
alias 필수 (impact audit §3 L96-105 영역과 정합).

### 2.4 Inspection 결과 종합

- app code 수정 영역이 크고 분산되어 있다 (qId 3 위치 + lookup 다중 + DOM 다중 +
  IndexedDB 2 stores)
- legacy storage key 유지 정책 (schema plan §3.1 + impact audit §3 권고)이 app
  code 수정 범위를 최소화한다
- runtime alias resolver는 read-path 한정으로도 multiple 진입점 처리가 필요하다
- 본 inspection은 app code 수정 영역을 식별만 한다. 구현 결정 영역 아님.

---

## 3. 5 후보 비교 (A·B·C·D·E)

### 3.1 후보 A — docs-only registry 유지

**내용**:
- `docs/audit/registries/trap_map_gigi_17_alias_registry_2026-05-25.json`을 SoT
  영역에 유지
- app/runtime/data 영역에 alias 반영 없음
- user-facing citation은 legacy storage key만 표시

| axis | 평가 |
|---|---|
| guardrail 정합 | ✓ app/data 0 변경 / persisted key 0 변경 / registry row promotion 0 |
| blast radius | 최소 (docs-only) |
| caution release | 불가 (user-facing legacy only) |
| rollback 비용 | 0 (docs 영역 한정) |
| separability | Q1·Q2 Separable 정합 |
| 위험 | user-facing source identity가 legacy key 중심 잔존 |

### 3.2 후보 B — app runtime alias resolver 도입

**내용**:
- app read-path에 `canonicalSourceId(q)` 또는 alias resolver 함수 도입
- legacy storage key 유지하면서 display layer에서 canonical 표시
- IndexedDB 미변경

| axis | 평가 |
|---|---|
| guardrail 정합 | persisted key 0 변경 정합, app code 수정은 별 승인 영역 |
| blast radius | 중간 (app code 3 위치 + display layer) |
| caution release | possible (user-facing canonical 표시 가능) |
| rollback 비용 | app code revert + display change revert |
| separability | Q3 Partial separable (범위 한정 결정 시) |
| 위험 | resolver 도입 시 §2.1 3 qId 위치 동시 정합 필요, display 양식 결정 필요 |

→ B의 design review만 다음 gate로 진입 가능. 구현은 별 명시 승인 영역.

### 3.3 후보 C — app/data alias registry 도입

**내용**:
- `app/data/aliases.json` 또는 별 app data 영역에 alias table 추가
- runtime resolver가 app data registry 참조

| axis | 평가 |
|---|---|
| guardrail 정합 | app/data 수정 영역 → 현재 guardrail 차단 |
| blast radius | 중상 (app/data + runtime) |
| caution release | possible after implementation |
| rollback 비용 | app/data revert + 사용자 신뢰성 영향 |
| separability | Q3 Partial separable |
| 위험 | docs SoT vs app/data SoT 이중화 위험 (schema plan §1 SoT position) |

→ 보류. docs SoT를 우선 안정화 후 별 트랙으로 검토 가능.

### 3.4 후보 D — question record metadata field 추가

**내용**:
- 각 `questions.json` record에 `canonical_source_id` field 추가
- record-level metadata로 alias 표현

| axis | 평가 |
|---|---|
| guardrail 정합 | `questions.json` 수정 영역 → guardrail 직접 차단 |
| blast radius | 최대 (5,331 records 모두 영향) |
| caution release | possible after migration |
| rollback 비용 | data revert + migration tooling 필요 |
| separability | impact audit §1 100항 mis-label 영역과 연동 — Q3 inseparable 측면 |
| 위험 | q52 외 99항 mis-label 추정 미확정 영역에 record 양식 변경 영향 확산 |

→ 보류. q52 외 99항 alias inventory 별 evaluation 통과 전 진입 금지 영역.

### 3.5 후보 E — Batch migration

**내용**:
- `2020_1회` 100항 → `2022_1회` 일괄 재귀속
- `2020_1,2회` 66항 분해/alias 정책 포함
- app persisted key migration / pdf_pages index sync

| axis | 평가 |
|---|---|
| guardrail 정합 | 다중 forbidden 영역 변경 — guardrail 정면 차단 |
| blast radius | 최대 (data + app + pdf_pages + persisted user data + per-year + PDF) |
| caution release | possible after full migration |
| rollback 비용 | 최대 (모든 영역 revert) |
| separability | Q5 Inseparable (66항 policy 선결 조건) |
| 위험 | 100항 source claim 전수 검증 부재 시 source claim 과도 |

→ **차단 유지**. 66항 systemic session-label policy 결정 + 100항 전수 evidence
+ app persisted key migration 설계 전 진입 금지.

---

## 4. 8 Decision Question 답변

### Q1 — docs-only registry를 당분간 authoritative review artifact로 유지할지?

**A**: **Yes — 유지**.

근거:
- registry artifact review PASS 12/12 (`f0b462c`)
- schema plan §1 "schema-authoritative: 본 plan + 후속 schema review가 alias
  row shape와 validation을 정의한다"
- runtime resolver / app data registry / record metadata 영역은 별 design 통과
  전 docs SoT 우선
- docs-only registry는 PASS된 baseline으로 후속 row 추가 또는 review 입력 영역

### Q2 — app runtime alias resolver 설계 검토를 다음 gate로 열지?

**A**: **Conditional Yes** — **design review only**, 구현은 별 명시 승인.

근거:
- alias schema plan §9 Step 5 본문: "Decide whether runtime resolver, app data
  registry, or record metadata is needed"
- separability evaluation Q3 Partial separable — 범위 한정 결정 시 separable
- §2 inspection: app code 3 qId 위치 + lookup 다중 + display 다중 + IndexedDB 2
  stores — design review 단계가 명확 필요
- 단 구현은 caution release input + user-facing impact evidence + 별 명시 승인
  후만 진입

design review 양식 (별 트랙에서 작성):
- 3 qId 위치 통합 SoT 결정 (단일 module vs 3 위치 동시 정합)
- read-path 한정 적용 영역 (display only vs lookup + display)
- IndexedDB 영향 영역 (없음 / canonical fallback / migration)
- DOM `data-q-id` 양식 결정 (storage / canonical / dual)

### Q3 — app/data alias registry는 지금 보류할지?

**A**: **Yes — 보류**.

근거:
- 현재 guardrail "app/data 명시 승인 전 수정 금지" 직접 차단
- schema plan §1 SoT 후보 표: "tracked app data registry | 보류 | app/data 수정
  승인, schema migration, app read-path review 뒤"
- docs SoT 우선 안정화 후 별 트랙으로 검토 가능
- 본 decision은 docs SoT (registry artifact)를 우선 안정화 영역으로 유지

### Q4 — record metadata field는 지금 보류할지?

**A**: **Yes — 보류**.

근거:
- 현재 guardrail "`questions.json` 수정 금지" 직접 차단
- schema plan §1 SoT 후보 표: "record metadata field | 보류 | `questions.json`/per-year
  수정 승인과 migration plan 뒤"
- impact audit §1 100항 mis-label 추정 미확정 — q52 외 99 records의 alias
  inventory 별 evaluation 통과 전 record 양식 변경 영향 확산 위험
- record 단위 변경은 100항 전수 영역과 연동 — Q3 inseparable 측면

### Q5 — Batch migration은 계속 보류할지?

**A**: **Yes — 차단 유지**.

근거:
- separability evaluation Q5 Inseparable
- alias schema plan §8 Timing bullet 4: "Batch migration cannot proceed until
  the 66항 policy is defined"
- correction plan v2 §7.3 measurable criteria 4번: 66항 분해/alias/보류 미정
  영역 차단
- 본 decision은 Batch migration 차단을 해제하지 않는다

### Q6 — user-facing citation이 legacy storage key만 보여주는 상태에서 caution release가 가능한지?

**A**: **No — 불가**.

근거:
- correction plan v2 §7.2 Alias-first measurable criteria 5번: "user-facing
  citation이 legacy storage key만 보여주는 상태라면 caution 해제 후보가 아니라
  caution 유지로 분류한다"
- alias schema plan §6 Required result: "If user-facing citation still shows
  only `2020_1회_52`, caution remains"
- separability evaluation Q4 Inseparable: caution release review는 본 evaluation
  결과 + 별 systemic policy 결정 + user-facing impact evidence + redryrun
  evidence 모두 입력 필요
- 본 decision은 후보 A (docs-only registry 유지) — user-facing은 legacy storage
  key만 표시 — caution release 자격 미달

### Q7 — registry row candidate → approved promotion이 필요한지?

**A**: **No — 금지 유지**.

근거:
- schema plan §2 field rule 5: "`status=approved`가 되려면 schema review,
  registry artifact approval, integrity check를 통과해야 한다"
- 본 decision은 schema review (artifact review PASS) + registry artifact
  approval + integrity check를 통과한 상태이나, approved promotion은 *별 명시
  승인 영역*으로 분리 유지
- registry artifact review §2.2 "PASS ≠ registry row approved promotion" 룰
  준수
- approval decision §7 forbidden: "registry row promotion from `candidate` to
  `approved`"

### Q8 — 66항 separability evaluation 결과가 App/data decision에 주는 제약은 무엇인지?

**A**: **3 제약**.

1. **Step 5 범위 한정 결정 시 separability 재평가 필요** (separability evaluation
   Q3 결론). 본 decision은 후보 A + B-design-review로 한정 — record metadata 영역
   미진입으로 재평가 불필요. 단 B 구현 진입 시점에 재평가 필요.

2. **Batch migration 차단 영역 유지** (Q5 Inseparable). 본 decision이 차단 해제
   안 함.

3. **caution release 차단 영역 유지** (Q4 Inseparable). 본 decision이 caution
   release 입력 evidence 1건만 추가 — 별 systemic policy 결정 + user-facing
   impact evidence + redryrun evidence 모두 필요.

---

## 5. Approved Direction — A + B-design-review

본 decision은 다음 1택을 동결한다:

**direction**: 후보 A (docs-only registry 유지) + 후보 B의 design review만 다음
gate로 승인.

### 5.1 즉시 활성 영역

- docs-only registry (`9868f95`) PASS된 baseline 유지
- registry artifact review (`f0b462c`) PASS 12/12 baseline 유지
- separability evaluation (`d9b2efd`) partial separability 결론 baseline 유지

### 5.2 다음 gate 영역 (각 별 명시 승인 후)

- **runtime resolver design review** (별 트랙) — B 후보의 design 검토만, 구현 X
- **별 systemic session-label policy 문서 작성** (별 트랙) — 66항 분해/alias/보류
  1택
- **Caution release review** (Step 6) — 본 decision + 별 systemic policy +
  user-facing impact evidence + redryrun evidence 모두 입력 후

### 5.3 영구 차단 영역 (별 명시 승인 + 추가 evidence 후)

- 후보 B 구현 (design review 통과 + user-facing impact smoke + 별 명시 승인 후)
- 후보 C (app/data alias registry) — docs SoT 안정화 후 별 트랙
- 후보 D (record metadata field) — 100항 전수 evidence + migration plan 후
- 후보 E (Batch migration) — 66항 policy + 100항 전수 evidence + persisted key
  migration 설계 + pdf_pages sync plan 모두 후

---

## 6. Residual Risk

| risk | severity | 본 decision에서의 처리 |
|---|---|---|
| user-facing citation이 legacy key 잔존 | Medium | caution release input 1건만 부족 — 후보 B design review가 다음 gate |
| `qId()` 3 위치 분산 (store.js / index.html / main.js) | Medium | B design review 시 통합 SoT 결정 영역 |
| IndexedDB persisted key가 legacy 영역 | Medium | A 후보에서는 0 영향. B 구현 시 read-path 한정 결정 필요 |
| 100항 mis-label 영역 잔존 | Medium | 본 decision 영역 외 — 별 evaluation 트랙 |
| 66항 systemic problem 영구 잔존 | Medium | 본 decision 영역 외 — 별 systemic policy 트랙 |

---

## 7. Next Gates

각 별 명시 승인 후만 진행:

1. **Runtime resolver design review** (별 트랙)
   - 3 qId 위치 통합 SoT 결정
   - read-path 한정 적용 영역
   - DOM `data-q-id` 양식 결정
   - IndexedDB 영향 영역 결정
   - 본 design review는 docs-only — app code 변경 없음
2. **별 systemic session-label policy 문서** (별 트랙)
   - 66항 분해 / alias / 보류 중 1택
3. **Caution release review** (Step 6, 본 decision + 위 2 트랙 통과 후)
   - 본 decision (App/data direction) +
   - 별 systemic policy 결정 +
   - user-facing impact evidence +
   - redryrun evidence
   - 모두 입력 후 plan v2 §6.3 review format 양식

---

## 8. Forbidden Until Separate Approval

- q52 단독 id 재발급
- `questions.json` 수정
- per-year json 수정
- PDF filename rename
- `pdf_pages/index.json` 수정
- app code 수정 (design review 단계 docs-only 한정)
- app alias resolver 구현 (design review 통과 + 별 명시 승인 후만)
- app/data alias registry 추가
- record metadata field 추가
- registry row promotion from `candidate` to `approved`
- 기기-17 caution 해제 선언
- Batch migration 진입 (66항 policy 결정 전)
- 66항 systemic policy를 q52 registry 영역에 흡수
- registry artifact 자체 수정 (review baseline 동결)

---

## Status

- App/data decision 작성 완료.
- direction: 후보 A (docs-only registry 유지) + 후보 B의 design review만 다음 gate
  로 승인.
- 후보 C / D / E 보류 또는 차단 유지.
- 기기-17 caution 유지.
- registry row status=candidate 유지 (approved promotion 0).
- Batch migration 차단 유지 (66항 policy 선결).
- app/data/pdf_pages/app code 변경 0.
- 본 decision은 진짜 정책 결정이므로 jsonl entry 1줄 추가 영역.
- 다음 gate: runtime resolver design review / 별 systemic session-label policy /
  Caution release review.
