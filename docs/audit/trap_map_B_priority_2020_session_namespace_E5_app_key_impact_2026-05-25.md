# Trap-Map B-Priority — 2020 Session Namespace E5 App Persisted Key Impact (2026-05-25)

E5 — app persisted key 영향 재평가. E3 namespace conflict audit (`b7b2b0b`)의
*66/66 systemic conflict* 결과를 app persisted key (qId / IndexedDB / DOM
data-q-id / pdfPageIndex / wrong-note filter) 관점에서 재평가한다.

이번 단계는 **docs-only evaluation**. **app code, app/data, questions.json,
per-year json, PDF filename, pdf_pages, 어떤 파일도 수정하지 않는다.** missing 29
recovery / Batch migration / resolver implementation / migration / registry
framing 확장 모두 실행 금지. push 없음. amend/rebase/reset 없음. 기기-17 caution
유지. q52 단독 id 재발급 금지 유지 (영구 부적합 영역). registry row promotion
금지 유지.

- 관련 E3 audit: `docs/audit/trap_map_B_priority_2020_1_vs_2020_1_2_conflict_audit_2026-05-25.md`
- 관련 missing 29 recovery: `docs/audit/trap_map_B_priority_2020_1_2_66item_missing29_recovery_evaluation_2026-05-25.md`
- 관련 session-label policy: `docs/audit/trap_map_B_priority_2020_1_2_66item_session_label_policy_2026-05-25.md`
- 관련 App/data decision: `docs/audit/trap_map_B_priority_gigi_17_app_data_decision_2026-05-25.md`
- 관련 runtime resolver design review: `docs/audit/trap_map_B_priority_gigi_17_runtime_resolver_design_review_2026-05-25.md`
- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`

---

## 1. App Code Read-Only Inventory (Evidence 입력)

본 evaluation의 입력으로 사용한 app code read-only inventory 결과. **수정 0**.

### 1.1 `qId` / `_id` 생성 위치 — 3 영역, 양식 = `year_session_q_no`

| file | line | 양식 |
|---|---|---|
| `app/js/store.js` | L8 | `export function qId(q) { ... }` (module SoT) |
| `app/js/store.js` | L28 | `_questions.forEach((q) => { q._id = qId(q); })` |
| `app/index.html` | L210 | inline `_questions.forEach(function(q) { q._id = q.year + '_' + q.session + '_' + q.q_no; })` |
| `app/js/main.js` | L138 | `function qId(q) { ... }` (legacy bundle) |
| `app/js/main.js` | L151 | `_questions.forEach(function(q) { q._id = qId(q); })` |

→ 모든 영역 `_id = year + '_' + session + '_' + q_no` **session 포함 양식**.

### 1.2 IndexedDB stores — 3 stores, keyPath 모두 `id`

| file | line | store | keyPath |
|---|---|---|---|
| `app/js/db.js` | L20 | `annotations` | `id` |
| `app/js/db.js` | L25 | `progress` | `id` |
| `app/js/db.js` | L26 | progress index `by_wrong` on `wrongCount` | — |
| `app/js/db.js` | L31 | `questions_cache` | `key` |
| `app/index.html` | L112-118 | 동일 양식 (inline) | 동일 |
| `app/js/main.js` | L24-31 | 동일 양식 (legacy bundle) | 동일 |

→ persisted user data (annotations / progress)의 `id` = `qId(q)` = storage_id
양식 (`year_session_q_no`).

### 1.3 DOM `data-q-id` — 2 위치 × 2 bundle = 4 영역

| file | line | 영역 |
|---|---|---|
| `app/index.html` | L389 | question view rendering |
| `app/index.html` | L472 | wrong-note item rendering |
| `app/js/main.js` | L387 | question view rendering (legacy) |
| `app/js/main.js` | L400 | wrong item rendering (legacy) |

→ DOM `data-q-id = q._id` = storage_id 양식 (`year_session_q_no`).

### 1.4 `_id === dataset.qId` lookup — 4 영역

| file | line | 영역 |
|---|---|---|
| `app/index.html` | L774 | search results lookup |
| `app/index.html` | L806 | wrong list lookup |
| `app/js/main.js` | L993 | legacy search lookup |
| `app/js/main.js` | L1075 | legacy wrong lookup |

→ lookup 양 측이 storage_id (양 측 `_id` / `dataset.qId` 모두 `year_session_q_no`
양식).

### 1.5 `filterByIds(ids)` — wrong-note filter — 3 file

| file | line | 영역 |
|---|---|---|
| `app/js/store.js` | L67 | `export function filterByIds(ids)` |
| `app/index.html` | L221 | inline `function filterByIds(ids)` |
| `app/index.html` | L797 | wrong list filter usage |
| `app/index.html` | L873 | filter dispatch (filter.type === 'wrong') |
| `app/js/main.js` | L171 | legacy bundle |
| `app/js/main.js` | L1026, L1409 | legacy usage |

→ ids 영역 = progress IndexedDB id 영역 = storage_id 양식.

### 1.6 `pdfPageIndex` / `puaChoicesIndex` lookup — 2 영역 × 2 bundle

| file | line | 영역 |
|---|---|---|
| `app/index.html` | L397 | `__pua = (window.puaChoicesIndex \|\| {})[__key]` |
| `app/index.html` | L418 | `__pages = (window.pdfPageIndex \|\| {})[__key] \|\| FIGURE_CROP_HOLD[__key]` |
| `app/index.html` | L585-594 | index load (pdf_pages/index.json + pua/choices) |
| `app/js/main.js` | L644-647 | legacy bundle |

→ `__key` = storage_id (양식 `year_session_q_no`).

### 1.7 Inventory 결론

- 모든 app key (qId / _id / IndexedDB / DOM / lookup / filter / pdfPageIndex)이
  storage_id 양식 (`year_session_q_no`) 단일 영역 사용
- session 포함 양식이라 `2020_1회_*` ↔ `2020_1,2회_*` *별 namespace*

---

## 2. App Key Namespace vs Human/Source Citation Namespace

### 2.1 App Key Namespace — `year_session_q_no` (Collision-Free)

| app key 양식 | session 영역 | collision |
|---|---|---|
| `2020_1회_52` | 2020년 1회 | 별 key |
| `2020_1,2회_52` | 2020년 1,2회 | 별 key |
| `2022_1회_52` | 2022년 1회 | 별 key (현재 questions.json 부재, count 0) |

→ session까지 포함하므로 app key namespace에서는 *3 영역 모두 collision-free*
공존 가능.

impact audit §5 명시: `(year, session, q_no)` 중복 0 — 본 evaluation 재확인.

### 2.2 Human/Source Citation Namespace — q_no만 (Collision-Heavy)

| human/source 표현 영역 | namespace | collision |
|---|---|---|
| "2020년 1회 52번" (사용자 표현) | (year, session, q_no) | 정확하면 collision 0 |
| "2020년 52번" (session 누락 사용자 표현) | (year, q_no) | **collision 2건** (1회 / 1,2회 별 컨텐츠) |
| "52번" (year/session 모두 누락) | (q_no) | **collision 다수** (모든 시험 52번이 충돌) |

→ 사용자 또는 source citation이 session을 누락한 채 q_no만 다루면 **별 시험
컨텐츠 충돌** (E3 audit 100% conflict 결과 정합).

### 2.3 두 namespace의 분리 영역

| 영역 | namespace |
|---|---|
| app persisted key (IndexedDB id / DOM data-q-id / lookup) | (year, session, q_no) collision-free |
| app pdfPageIndex / puaChoicesIndex `__key` | (year, session, q_no) collision-free |
| 사용자 facing display (현재 부재) | 영역 부재 — 신규 영역 결정 시 collision 위험 |
| source citation (registry artifact + alias) | canonical_source_id 영역으로 분리 (storage_id 별 영역) |

→ app key 영역은 안전하나, *사용자 facing 또는 source citation 영역에서 q_no만
다루면 위험*.

---

## 3. E3 100% Conflict가 만드는 위험

### 3.1 app key 영역 — 위험 0

- session 포함 양식이라 collision 0
- IndexedDB persisted data 영역 unaffected
- DOM data-q-id 영역 unaffected
- pdfPageIndex 영역 unaffected

→ **app key 영역은 E3 결과에 영향 받지 않음**.

### 3.2 사용자 facing 영역 — 위험 활성

- 현재 app은 user-facing source citation UI 영역 *부재* (runtime resolver design
  review §1.6 명시)
- 미래 citation UI 도입 시 q_no만 표시하거나 session 누락 표시할 경우 **사용자
  혼동 영역 활성**
- 예: "52번"만 표시 시 변압기 권수비(2020_1회_52)와 동기전동기 V곡선(2020_1,2회_52)이
  사용자에게 같은 문제로 인식될 위험

→ design review §6 (citation label L1 권장: "대표 기출: 2022_1회_52 (시행 시기:
2022-04-24)")의 *명시 label* 규칙이 본 위험을 차단.

### 3.3 source citation 영역 — 위험 활성

- registry artifact의 canonical_source_id 영역에서 q_no namespace 사용 시
  collision 위험
- 예: 본 registry artifact의 q52 row가 canonical_source_id `2022_1회_52`로 정의 —
  년도 + 회차 + 문제번호 영역 모두 포함이라 collision 0
- 단 후속 row 추가 시 (q52 외 99 records alias 확장 영역) canonical_source_id를
  q_no만 또는 session 누락으로 정의하면 collision 영역 발생

→ registry artifact schema plan §2 row schema (storage_id / canonical_source_id /
source_pdf / source_pdf_page / source_q_no / cover_date 모두 포함)가 본 위험을
*scheme 차원에서 차단*.

### 3.4 외부 도구 영역 — 위험 가능성

- 외부 OCR / extraction tool / 외부 도구가 q_no만 키로 사용 시 collision 위험
- 예: missing 29 recovery 도구가 q_no만 키로 사용 시 1회/1,2회 영역 충돌
- 외부 도구 영역은 본 evaluation scope 외이나, recovery plan / 100 records audit
  진입 시 *session 포함 키 양식 강제* 권고

---

## 4. q52 단독 재발급 = 부적합 강화

### 4.1 기존 부적합 사유 (E1 + E3 결론)

- E1 audit: PDF 합본 시험 양식 (split 부적합 확정)
- E3 audit: q52는 systemic 1 사례 (isolated case 아님)
- impact audit §1 + N1 audit: 100 records batch mis-label 가능성

### 4.2 본 E5 audit 추가 부적합 사유 (app key 관점)

- **A1 — persisted user data inconsistency**:
  q52 storage_id를 `2020_1회_52` → `2022_1회_52`로 단독 변경 시 다음 영역 깨짐:
  - IndexedDB progress: 기존 사용자 풀이 기록 (id = `2020_1회_52`)이 새 id와
    연결 안 됨
  - IndexedDB annotations: 기존 사용자 필기/스크리블이 새 id와 연결 안 됨
  - wrong-note filter (filterByIds): 기존 오답 목록에서 새 id 문제 미발견
  - → 사용자 입장에서는 *기존에 풀었던 변압기 권수비 문제가 사라짐* 영역

- **A2 — namespace asymmetry 강화**:
  q52만 새 namespace로 이동 + 99 records는 기존 namespace 유지 = systemic 1
  사례 단독 처리로 *inconsistency 영역 영구화*. E3 audit이 확정한 systemic
  패턴과 충돌.

- **A3 — registry artifact framing 영역 부정합**:
  q52 row는 systemic 1 사례 (E3) → 단독 storage_id 변경은 *나머지 99 records
  영역과의 framing 영역 영구 분리*. 후속 99 records alias 확장 시 q52만 별
  처리 영역이 됨.

### 4.3 결론

q52 단독 storage_id 재발급은 **app key 영역 + persisted user data + framing
영역 3 차원 모두에서 부적합 영구 강화**. 별 명시 승인 영역 아님 — **영구 금지**.

---

## 5. Batch Migration Mapping Granularity 요구사항

### 5.1 단순 q52 단건 mapping 불가

E3 audit 결과 q52는 systemic 1 사례. 단건 mapping은 §4 A2/A3 부정합 영역.

### 5.2 필요한 mapping granularity

| 영역 | 요구사항 |
|---|---|
| **2020_1회 100 records mapping** | 각 record의 true source 식별 + canonical_source_id 매핑 (예: q52 = 2022_1회_52, q53 = 2022_1회_53, …) |
| **2020_1,2회 66 records coexistence policy** | session-label policy 결정 (defer 영역 / 별 source 영역 / alias 영역 중 1택) |
| **persisted user data migration 또는 compatibility alias** | 기존 storage_id 기반 progress/annotations를 새 namespace로 이전 또는 양 namespace bidirectional lookup |
| **DOM data-q-id 양식 결정** | storage_id 유지 / canonical 표시 / dual 중 1택 |
| **pdfPageIndex 동기화** | impact audit §4 명시 5 keys (2020_1회_53/71/72/73/79)의 canonical 이동 또는 alias |

### 5.3 mapping granularity 결정 전 차단 영역

- q52 단독 재발급 (§4 영구 부적합)
- 99 records alias 확장 (현재 E3 framing 활성화만, 실행 별 명시 승인)
- Batch migration 전체 진입 (66항 policy 선결 + 100 records 전수 source audit
  선결)

---

## 6. Alias-Only / Read-Path Resolver = 가장 안전 (재확인)

### 6.1 안전 영역 (app key 관점)

| 영역 | alias-only resolver 영향 |
|---|---|
| `qId(q)` 함수 (3 위치) | **변경 0** — storage_id 반환 유지 |
| `q._id` assignment | **변경 0** — storage_id 유지 |
| IndexedDB keyPath (3 stores) | **변경 0** — `keyPath: 'id'` + storage_id 기반 |
| `by_wrong` index (wrongCount) | **변경 0** — progress wrongCount 기반 |
| DOM `data-q-id` (4 영역) | **변경 0** — storage_id 유지 |
| `_id === dataset.qId` lookup (4 영역) | **변경 0** — 양 측 storage_id |
| `filterByIds(ids)` (3 file) | **변경 0** — progress id 영역 = storage_id |
| `pdfPageIndex` / `puaChoicesIndex` (`__key`) | **변경 0** — storage_id 기반 |

→ **app persisted key + IndexedDB + DOM + lookup + filter + pdfPageIndex 모두
변경 0** 가능.

### 6.2 신규 영역 (alias resolver 도입 시)

- `canonicalSourceId(q)` 별 함수 (citation display 전용)
- citation UI 영역 신규 (현재 부재, design review §1.6 명시)
- alias table SoT (S2 권장 = docs registry → app data build-time sync)

→ runtime resolver design review §3 design candidate 정합. **read-path citation
resolver only + storage_id 불변 + canonical_source_id label 전용**.

### 6.3 본 E5 결론

alias-only / read-path resolver = **persisted user data 보호 + namespace
collision 회피 + systemic framing 영역 호환** 3 차원 모두 만족하는 1택.

---

## 7. Implementation 금지 영역 (별 명시 승인 전)

E3 + 본 E5 결과로 다음 영역 모두 **별 명시 승인 + 다중 evidence 후만 진입**:

| 금지 영역 | 차단 사유 |
|---|---|
| **q52 단독 storage_id 변경** | §4 영구 부적합 (3 차원) |
| **99 records alias 확장 실행** | 100 records 전수 source audit 선결 + 별 명시 승인 |
| **registry framing 영역 확장** (q52 row 외 추가 row) | 별 명시 승인 영역 (E3 결과 활성화만) |
| **Batch migration 진입** | 66항 policy 선결 + §5 mapping granularity 결정 선결 |
| **record metadata field 추가** | App/data decision §1 보류 영역 + 100 records mis-label 영역 연동 |
| **app/data alias registry 즉시 도입** | docs SoT 안정화 후 별 트랙 |
| **app code 수정 (resolver 구현)** | design review 통과 + user-facing impact smoke + 별 명시 승인 후만 |
| **persisted user data migration** | mapping granularity + compatibility alias 결정 + 별 명시 승인 후만 |

---

## 8. Caution Release 영향

**A**: **차단 유지** — 본 evaluation input 영역 변경 0.

근거:
- separability evaluation Q4 Inseparable 유지
- caution release input 요구사항 (별 systemic policy + user-facing impact +
  redryrun) 변경 0
- 본 evaluation은 *evidence 영역 강화*만 — implementation 영역 결정 변경 0
- 66항 policy = defer 유지
- registry row status=candidate 유지

---

## 9. 8 Question 답

### Q1 — app persisted key는 session 포함이라 2020_1회 / 2020_1,2회 collision-free 공존?

**A**: **Yes** (§2.1).

`_id = year + '_' + session + '_' + q_no` 양식 + IndexedDB keyPath = `id` 모두
session 포함 → app key namespace에서 별 영역. impact audit §5 `(year, session,
q_no)` 중복 0건 재확인.

### Q2 — q_no namespace 100% conflict가 만드는 위험?

**A**: **3 위험 영역 + 1 위험 가능성**.

- §3.1 app key 영역: **위험 0** (session 포함)
- §3.2 사용자 facing 영역: **위험 활성** (citation UI 도입 시 session 누락 표시
  영역 — 단 design review §6 L1 양식 권장으로 차단)
- §3.3 source citation 영역: **위험 활성** (canonical_source_id가 q_no만 또는
  session 누락 시 — 단 registry schema §2 양식으로 차단)
- §3.4 외부 도구 영역: **위험 가능성** (recovery / source audit 도구 영역 —
  session 포함 키 양식 강제 권고)

### Q3 — q52 단독 재발급은 왜 app key/user data 관점에서 더 부적합?

**A**: **3 차원 부적합 강화** (§4.2).

- A1: persisted user data inconsistency (IndexedDB progress / annotations /
  wrong-note 영역 단절)
- A2: namespace asymmetry 강화 (systemic 1 사례 단독 처리 = inconsistency 영구화)
- A3: registry artifact framing 영역 부정합 (99 records 영역과의 framing 영구
  분리)

→ **영구 금지** 영역 강화.

### Q4 — Batch migration mapping granularity 요구사항?

**A**: **5 영역** (§5.2).

1. 2020_1회 100 records mapping (각 record true source 식별)
2. 2020_1,2회 66 records coexistence policy
3. persisted user data migration 또는 compatibility alias
4. DOM data-q-id 양식 결정
5. pdfPageIndex 동기화

→ 단순 q52 단건 mapping 불가.

### Q5 — alias-only/read-path resolver 후보가 app key 보존에 여전히 가장 안전한가?

**A**: **Yes** (§6).

근거:
- qId (3 위치) / IndexedDB (3 stores) / DOM (4 영역) / lookup (4 영역) /
  filterByIds (3 file) / pdfPageIndex (2 영역) **모두 변경 0** 가능
- canonical_source_id는 citation display 전용 (별 함수 + 별 UI)
- runtime resolver design review §3 design candidate 정합

### Q6 — 어떤 implementation을 금지해야?

**A**: **8 영역 금지** (§7).

- q52 단독 storage_id 변경 (영구)
- 99 records alias 확장 실행
- registry framing 확장
- Batch migration 진입
- record metadata field 추가
- app/data alias registry 즉시 도입
- app code 수정 (resolver 구현)
- persisted user data migration

### Q7 — caution release 영향?

**A**: **차단 유지** (§8). input 영역 변경 0.

### Q8 — E6 separability re-evaluation에 넘길 app-key 결론?

**A**: **3 영역 결론** (§10 영역 참조).

1. **app key 영역 separable 강화** — session 포함 양식이라 collision-free,
   read-path resolver 도입 시 0 변경 가능 = separable layer (Q1/Q2 Separable
   결론 강화)
2. **Batch migration inseparable 강화** — mapping granularity 5 영역 + persisted
   user data migration 영역 = systemic 분리 불가 (Q5 Inseparable 결론 강화)
3. **q52 단독 재발급 = 영구 부적합 강화** — separability framework에서 q52 alias
   row의 storage_id 불변 = 강제 invariant 영역으로 등재 권고

---

## 10. E6 Separability Re-Evaluation 입력 (App-Key 결론)

본 E5 evaluation이 E6에 넘기는 app-key 결론:

| separability Q | E5 입력 |
|---|---|
| Q1·Q2 Registry creation/review (Separable) | **강화** — app key 영역 0 변경으로 registry artifact creation/review 영역이 app key 영역과 완전 분리 가능 |
| Q3 App/data decision (Partial Separable) | **재정의** — alias-only resolver = separable / app data registry · record metadata = inseparable (persisted data 영역 영향) |
| Q4 Caution release review (Inseparable) | 유지 — input 요구사항 변경 0 |
| Q5 Batch migration (Inseparable) | **강화** — §5 mapping granularity 5 영역 + persisted data migration 영역 = systemic 분리 불가 영구 |
| Q6 별 systemic session-label policy | 유지 — defer 영역 |

추가 새 결론 후보:
- **q52 단독 storage_id 변경 = 영구 invariant 영역으로 등재** (separability
  framework의 명시 guardrail로 추가 권고)

---

## 11. 영향 매트릭스

| 영역 | 본 E5 영향 |
|---|---|
| q52 alias registry (9868f95) | row 1건 유지, framing 영역 확장 가능성 명시 (실행 별 명시 승인) |
| registry artifact review PASS (f0b462c) | 12/12 baseline 유지 |
| runtime resolver design review (6ac1a9b) | design candidate (read-path resolver only) 강화 |
| App/data decision (9c1d387) | 후보 A docs-only + B-design-review 강화 |
| 66항 separability evaluation (d9b2efd) | partial separability 결론 유지 + Q1/Q2/Q5 강화 |
| 66항 policy (df7e932) | defer 유지 + evidence requirement E5 충족 |
| E1 source audit (5c1fecc) | split 부적합 강화 |
| E2 record-PDF mapping (5f1c9c5) | per-year ↔ master 정합 재확인 |
| missing 29 data debt (02c985c) | 후보 A 별 data debt 분리 유지 + recovery 도구 session 키 강제 권고 |
| E3 namespace conflict (b7b2b0b) | 100% conflict 결과를 app key 관점에서 재평가 = app key separable 강화 |
| caution release (Step 6) | 차단 유지 |
| Batch migration | 차단 유지 + 영구 분리 불가 영역 강화 |
| q52 단독 id 재발급 | **영구 부적합 3 차원 강화** |
| 후보 C (split policy) | 부적합 강화 (E1 + E3 + 본 E5) |
| 기기-17 caution | 유지 |
| registry row status=candidate | 유지 |

---

## 12. Forbidden Until Separate Approval

- **q52 단독 id 재발급 (영구 부적합 — 3 차원 부적합 강화)**
- `questions.json` 수정
- per-year json 수정
- PDF filename rename
- PDF 파일 복사 / 편집 / OCR 산출물 신규 생성
- `pdf_pages/index.json` 수정
- app code 수정 (alias resolver / qId 변경 / IndexedDB keyPath 변경 모두 포함)
- app alias resolver 구현
- app/data alias registry 추가
- record metadata field 추가
- registry row promotion from `candidate` to `approved`
- registry artifact 자체 수정 (q52 row 외 추가 row 포함)
- registry framing 확장 실행 (99 records 영역)
- 기기-17 caution 해제 선언
- Batch migration 진입
- 66항 systemic policy를 q52 registry 영역에 흡수
- 100 records alias 확장 실행
- missing 29 recovery 실행
- persisted user data migration
- 후보 C (split policy) 진입 (E1 + E3 + 본 E5 부적합 확정 유지)

---

## 13. Decision Record 영향

본 evaluation은 **evidence 영역 추가만** 수행 — 정책 변경 0:

- 66항 policy = **defer 유지** (변경 없음)
- App/data decision direction (후보 A + B-design-review) 강화
- runtime resolver design candidate (read-path only) 강화
- q52 단독 id 재발급 = 영구 부적합 강화 (기존 룰 evidence 강화)
- Batch migration 차단 유지 + 영구 분리 불가 영역 강화
- caution release 차단 유지

→ jsonl `trap_map_active_decisions.jsonl`에 별 entry 추가 안 함 (사용자 가이드:
"JSONL은 evidence evaluation이면 수정하지 말 것. 정책 결정이 바뀌면 별도 판단"
정합).

본 evaluation 문서 자체가 E5 evidence로 충분.

---

## Status

- E5 app persisted key 영향 재평가 작성 완료.
- 핵심 측정 (app code read-only inventory, 수정 0):
  - qId 3 위치 / IndexedDB 3 stores / DOM 4 영역 / lookup 4 영역 / filterByIds
    3 file / pdfPageIndex 2 영역 — 모두 storage_id 양식 (`year_session_q_no`)
- 핵심 결론:
  - app persisted key namespace = **collision-free** (session 포함)
  - human/source citation namespace = **collision-heavy** (q_no만 보면 66/66
    conflict)
  - **q52 단독 재발급 = 3 차원 부적합 강화** (persisted data + namespace asymmetry
    + framing 부정합)
  - **alias-only/read-path resolver = 가장 안전** (qId / IndexedDB / DOM /
    lookup / filter / pdfPageIndex 모두 0 변경)
  - **Batch migration mapping granularity 5 영역 요구** (단순 q52 단건 mapping
    불가)
- 정책 변경 0 — 66항 defer / App/data direction / runtime design candidate /
  q52 separable layer / caution release / Batch migration 모두 유지·강화.
- jsonl decision entry 추가 안 함 (사용자 가이드 정합 — evidence evaluation).
- E6 separability re-evaluation 입력: Q1/Q2/Q5 강화 + q52 영구 invariant 등재
  권고.
- app code / app data / questions.json / per-year / PDF / pdf_pages / registry
  artifact 모두 변경 0.
- 기기-17 caution 유지. registry row status=candidate 유지. Batch migration
  차단 유지. caution release 차단 유지. q52 단독 재발급 영구 부적합 강화. 후보 C
  부적합 강화.
- 다음 gate: E6 separability re-evaluation (E1~E5 + missing 29 입력) / 100 records
  전수 source audit / 99 records alias 확장 evaluation / E4 다른 합본 PDF /
  외부 source / 66항 재evaluation / missing 29 recovery plan / 1·3·4 verification.
