# Trap-Map B-Priority — 기기-17 Runtime Resolver Design Review (2026-05-25)

App/data decision (`9c1d387`, `DR-TRAP-GIGI17-APPDATA-DECISION`)에서 "후보 B
runtime alias resolver는 design review only로 다음 gate 승인"으로 동결한 영역의
docs-only design review를 수행한다.

이번 단계는 **docs-only design review**. **app code 수정 금지**. app/data 구현
승인 아님. app/data registry 도입 승인 아님. record metadata field 승인 아님.
caution release 아님. registry row approved promotion 아님.

- 관련 App/data decision: `docs/audit/trap_map_B_priority_gigi_17_app_data_decision_2026-05-25.md` (`DR-TRAP-GIGI17-APPDATA-DECISION`)
- 관련 registry artifact: `docs/audit/registries/trap_map_gigi_17_alias_registry_2026-05-25.json`
- 관련 artifact review: `docs/audit/trap_map_B_priority_gigi_17_alias_registry_artifact_review_2026-05-25.md` (PASS 12/12)
- 관련 schema plan: `docs/audit/trap_map_B_priority_gigi_17_alias_schema_plan_2026-05-25.md`
- 관련 separability evaluation: `docs/audit/trap_map_B_priority_gigi_17_66item_separability_evaluation_2026-05-25.md` (partial separability)
- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`

---

## 1. App Code Read-Only Inspection (Design 입력)

본 design review의 입력으로 사용한 app code read-only inspection 결과. **수정 0**.

### 1.1 `qId()` / `_id` 생성 — 3 위치

| file | line | 양식 |
|---|---|---|
| `app/js/store.js` | L8 | `export function qId(q) { return q.year + '_' + q.session + '_' + q.q_no; }` (module SoT) |
| `app/js/store.js` | L28 | `_questions.forEach((q) => { q._id = qId(q); })` |
| `app/index.html` | L210 | inline `_questions.forEach(function(q) { q._id = q.year + '_' + q.session + '_' + q.q_no; })` |
| `app/js/main.js` | L138 | `function qId(q) { ... }` (legacy bundle) |
| `app/js/main.js` | L151 | `_questions.forEach(function(q) { q._id = qId(q); })` |

→ **3 위치 동시 정합 필요 (또는 SoT 통합 결정 영역)**.

### 1.2 `_id === dataset.qId` lookup — 4 위치

| file | line | 영역 |
|---|---|---|
| `app/index.html` | L774 | search results lookup |
| `app/index.html` | L806 | wrong list lookup |
| `app/js/main.js` | L993 | legacy search lookup |
| `app/js/main.js` | L1075 | legacy wrong lookup |

→ `dataset.qId` 양식 결정 (storage_id only / canonical_source_id / dual)이 design
영역.

### 1.3 IndexedDB stores — `app/js/db.js` + inline

| file | line | store / index |
|---|---|---|
| `app/js/db.js` | L50,55 | annotations (`keyPath=id`, qId 기반) |
| `app/js/db.js` | L64-67 | progress (`keyPath=id`, qId 기반) |
| `app/index.html` | L115 | progress index `by_wrong` on `wrongCount` |
| `app/index.html` | L148-152 | progress wrongCount tracking |
| `app/js/main.js` | L28 | legacy bundle 동일 |

→ persisted user data는 **legacy storage_id 기반**. 보존 정책 유지.

### 1.4 `filterByIds(ids)` — wrong-note filter

| file | line | 영역 |
|---|---|---|
| `app/js/store.js` | L67 | `export function filterByIds(ids)` |
| `app/index.html` | L221 | inline `function filterByIds(ids)` |
| `app/index.html` | L797 | wrong list filter usage |
| `app/index.html` | L873 | filter dispatch (filter.type === 'wrong') |

→ ids = progress 영역의 id 배열 = storage_id 기반. 변경 영역 0.

### 1.5 `pdfPageIndex` / `puaChoicesIndex` lookup

| file | line | 영역 |
|---|---|---|
| `app/index.html` | L397 | `__pua = (window.puaChoicesIndex || {})[__key]` |
| `app/index.html` | L418 | `__pages = (window.pdfPageIndex || {})[__key] \|\| FIGURE_CROP_HOLD[__key]` |
| `app/index.html` | L585-594 | index load (pdf_pages/index.json + pua/choices/index.json) |
| `app/js/main.js` | L644-647 | legacy bundle 동일 |

→ `__key` = storage_id. q52는 pdf index key 없음 (separability evaluation §3.1 Q1
정합). resolver 도입 시 read-path fallback 영역.

### 1.6 user-facing source citation 영역 — **부재**

grep 검색 (`기출|source|citation|대표 기출`) 결과: app 본문에 source citation
표시 UI element 0건. L835는 앱 메타 정보 (전체 문제 수)이며 source citation
아님.

→ **현재 app은 canonical_source_id 표시 영역 부재**. resolver 도입 시 *신규 UI
영역 생성 필요*. 이는 design 영역의 새 결정 영역.

### 1.7 Inspection 결론

- generation: 3 qId 위치 분산
- lookup: 4 위치 + dataset.qId 양식
- persisted: 2 IndexedDB stores + by_wrong index
- pdf index: storage_id 기반, q52 자체는 key 없음
- citation UI: **부재** (신규 영역)

→ resolver 도입 영역은 *generation SoT 통합 + read-path citation 신규 UI* 영역
한정이 design candidate의 자연 좁힘.

---

## 2. 10 Decision Question 답

### Q1 — runtime resolver가 필요한가, 아니면 docs-only registry만으로 다음 gate를 유지할 수 있는가?

**A**: **현재 시점에서는 docs-only registry만으로 충분**. resolver 구현은 caution
release input이 필요해질 시점에 별 명시 승인 영역.

근거:
- App/data decision §1: "현재 app/data 구현 승인: 없음"
- registry artifact review §2.2: "PASS = q52 candidate inventory artifact review에
  한정"
- caution release는 user-facing impact evidence + 별 systemic policy + redryrun
  evidence 모두 입력 필요 (separability evaluation Q4 Inseparable)
- docs-only registry는 PASS된 review artifact baseline 유지

resolver는 *caution release 진입이 결정될 때* design → implementation 트랙으로
이동. 본 design review는 그 시점 대비 설계 준비.

### Q2 — resolver가 필요하다면 read-path 한정으로 가능한가?

**A**: **Yes — read-path 한정으로 충분**.

근거:
- App/data decision §5.3 "후보 B 구현 (design review 통과 + user-facing impact
  smoke + 별 명시 승인 후)"
- alias schema plan §4 Storage And Validation Model: "Storage model: Store alias
  rows one-way: `storage_id -> canonical_source_id`. Do not mutate question `_id`"
- impact audit §3: persisted progress/annotations/wrong-note는 storage_id 기반
  유지 정책
- write-path (progress save / annotation save) 영역은 storage_id 유지로 0 영향

read-path 한정 의미:
- citation display: canonical_source_id 표시 (신규 UI 영역)
- pdf index fallback: 별 평가 (q52는 key 없음, separability §3.1 Q1)
- progress / annotations / wrong-note: storage_id 유지 (변경 0)

### Q3 — resolver가 storage id를 절대 바꾸지 않는 구조인지?

**A**: **Yes — storage id 불변 보장 필수**.

design 룰:
- `qId(q)` 함수 시그니처 변경 0 (return type 유지 — storage_id 반환)
- `q._id` assignment 변경 0 (`q._id = qId(q)` 유지)
- IndexedDB key 양식 변경 0 (`keyPath='id'` + qId 기반 유지)
- DOM `data-q-id` 속성 변경 0 (`q._id` = storage_id 유지)

resolver는 *별 함수*로 도입:
```
canonicalSourceId(q) -> string  // alias registry lookup, returns canonical_source_id
```

위 함수는 *citation display 영역에서만 호출*. storage 영역 미진입.

### Q4 — canonical_source_id를 app id처럼 쓰는 위험을 어떻게 막을지?

**A**: **명명 분리 + lint/grep 룰 + design contract 3중 차단**.

design contract:
- `qId(q)` → 항상 storage_id 반환 (불변)
- `canonicalSourceId(q)` → 별 함수, citation display 전용
- IndexedDB / pdfPageIndex / puaChoicesIndex lookup은 *qId만 사용 가능*
- DOM `data-q-id`는 *qId만 가능*
- citation UI는 *canonicalSourceId만 가능*

차단 룰:
- 1차: grep / lint 룰로 `canonicalSourceId` 사용 위치를 citation display 코드
  path에 한정
- 2차: code review에서 `canonicalSourceId`를 `_id`, `dataset.qId`, IndexedDB key,
  pdfPageIndex key로 사용 시 즉시 차단
- 3차: design contract test (구현 시점 작성, design review 단계에서는 contract
  명시만)

추가 안전장치:
- citation UI는 *명시적 label*과 함께 표시 (예: `대표 기출: 2022_1회_52 (시행
  시기: 2022-04-24)`). label 없이 canonical_source_id 단독 표시 금지.

### Q5 — DOM data-q-id, progress, annotations, wrong-note, pdfPageIndex lookup은 계속 storage_id 기준인지?

**A**: **Yes — 모두 storage_id 유지**.

| 영역 | resolver 영향 |
|---|---|
| DOM `data-q-id` (index.html L389, L472) | **변경 0** — storage_id 유지 |
| progress IndexedDB (db.js L64-67) | **변경 0** — keyPath='id' = storage_id |
| annotations IndexedDB (db.js L50,55) | **변경 0** — keyPath='id' = storage_id |
| wrong-note filter (filterByIds, store.js L67) | **변경 0** — progress id 기반 |
| pdfPageIndex (index.html L418) | **변경 0** — `__key` = storage_id; q52는 key 없음 (separability §3.1 Q1) |
| puaChoicesIndex (index.html L397) | **변경 0** — 동일 패턴 |
| search results lookup (index.html L774) | **변경 0** — `_id === dataset.qId` 양 측 storage_id |
| wrong list lookup (index.html L806) | **변경 0** — 동일 |

→ persisted + lookup + DOM 영역 모두 storage_id 보존. resolver는 *별 read-path
함수*로 격리.

### Q6 — user-facing citation을 canonical_source_id로 보여줄 경우 label을 어떻게 분리할지?

**A**: **명시 label + storage/canonical 분리 표시**.

design candidate (UI 영역):

label 양식 후보 (구현 시 결정):

| 양식 | 예시 |
|---|---|
| **L1 — 정합형** | `대표 기출: 2022_1회_52 (시행 시기: 2022-04-24)` |
| L2 — 분리형 | `저장 id: 2020_1회_52 / 원본 출처: 2022_1회_52 (2022-04-24)` |
| L3 — 단축형 | `2022_1회_52` (canonical only, label 없음) |

design 권고:
- **L1 권장** — user-facing은 canonical citation에 명시 label ("대표 기출",
  "시행 시기" 등). storage_id는 default 비표시, advanced view에서만 표시
- L2는 dual representation으로 information density 높음 (debug/audit view 영역)
- L3는 금지 (Q4 위험 영역 — label 없는 canonical 표시는 app id 오해 영역)

label 분리 contract:
- citation UI는 *label과 value 함께 표시* (label 없는 canonical 표시 금지)
- storage_id 표시 영역은 *별 advanced view*에 한정 (default UI 미노출)

### Q7 — alias registry를 app runtime이 직접 읽을지, docs registry를 app data로 복제할지, hardcoded mapping을 둘지?

**A**: **현재 design 단계에서 결정 보류** — 3 후보의 trade-off만 명시.

| 후보 | 장점 | 위험 | 본 design review 평가 |
|---|---|---|---|
| **S1 — app runtime이 docs registry 직접 read** | docs SoT 단일화 | docs/audit 경로를 app 빌드/배포 영역에 의존 / runtime fetch 위험 | **비권장** — docs/audit는 review artifact 영역, runtime 의존 영역 아님 |
| **S2 — docs registry를 app data로 복제 (build-time sync)** | docs SoT 유지 + app runtime은 app data 영역만 의존 | sync 정책 필요 (build script + integrity check) | **권장 후보** — schema plan §1 "tracked app data registry" 영역의 build-time mirror |
| **S3 — app runtime에 hardcoded mapping** | 구현 빠름 | data ownership 불명확, 장기 유지 부적합 (schema plan §1 "app hardcoded mapping: 비선호") | **비권장** — 임시 실험 외 사용 안 함 |

→ 본 design review는 *S2가 권장 후보*임을 명시. 단 S2 진입은 별 명시 승인 +
build-time sync 정책 결정 + integrity check 양식 결정 후. **현재 design 단계에서
구현 결정 안 함**.

### Q8 — 구현 전 필요한 smoke/evidence는 무엇인지?

**A**: **6 영역 evidence 필수**.

| evidence | 양식 |
|---|---|
| qId SoT 통합 evidence | 3 위치 (store.js / index.html / main.js)의 single SoT 결정 + grep 검증 (qId 정의 위치 = 1, 사용 위치 = N) |
| resolver API contract | `canonicalSourceId(q)` 시그니처 + return type + null/missing fallback 정의 |
| citation UI label smoke | label 양식 (L1 권장) 화면 캡처 — viewport / device / language 영역 명시 |
| progress / annotation regression | 기존 storage_id 기반 IndexedDB lookup이 정확 동작 (smoke test 양식) |
| wrong-note filter regression | filterByIds(ids)가 storage_id 기반으로 정확 동작 |
| pdfPageIndex lookup regression | `__key` = storage_id 기준 기존 5 keys + FIGURE_CROP_HOLD fallback 정확 동작 |

추가 (separability evaluation §6.2 정합):
- canonical_source_id가 *citation display 외* 영역에 사용되지 않음을 grep으로
  증명 (lint rule 영역)
- alias registry SoT (S2 권장 시) build-time sync evidence

본 evidence는 *구현 시점*에 작성. 본 design review에서는 evidence 양식 정의만.

### Q9 — 66항 separability decision이 resolver design에 주는 제약은 무엇인지?

**A**: **3 제약**.

| 제약 | 내용 |
|---|---|
| **C1 — resolver scope = q52 alias 한정 (현재 영역)** | registry artifact `rows`가 q52 1건. resolver는 q52 storage_id → canonical_source_id 매핑만 처리. `2020_1,2회_*` records 영역 미진입 |
| **C2 — `2020_1,2회_*` storage_id resolver miss 명시 처리** | resolver가 `2020_1,2회_*` storage_id 요청 시 null/undefined 반환 (silent fallback). 66항 systemic policy 결정 전 강제 매핑 0 |
| **C3 — separability re-evaluation trigger** | resolver scope가 q52 외 다른 records 영역으로 확장 시 separability evaluation 재실행 필요 (§3 separability evaluation Q3 결론 정합) |

→ 본 design은 *q52 한정 resolver*. 66항 영역 변경 0. Batch migration 영역 변경 0.

### Q10 — 이 design review PASS가 caution release나 app implementation approval을 의미하지 않음을 명확히 할 것

**A**: 본 design review의 PASS는 **design candidate 좁힘에 한정**한다. 다음을
의미하지 않는다:

| 미포함 영역 | 사유 |
|---|---|
| caution release | separability evaluation Q4 Inseparable. user-facing impact evidence 부재. 본 design review는 evidence 1건 아님 — design candidate만 |
| app implementation approval | App/data decision §5.3 "후보 B 구현 (design review 통과 + user-facing impact smoke + 별 명시 승인 후)" — 본 design review는 1 step 통과만, smoke + 별 승인 영역 외 |
| app/data registry 도입 승인 | S2 권장 후보 명시뿐, 진입 결정은 별 트랙 |
| record metadata field 승인 | C/D/E 보류 영역 유지 |
| registry row promotion to approved | schema plan §2 field rule 5 영역 미진입 |
| Batch migration 차단 해제 | 66항 policy 선결 조건 유지 |
| 기기-17 caution 해제 | 본 design review는 caution 유지 baseline 기준 |

본 design review의 PASS는 *runtime resolver design candidate가 read-path
citation resolver only + storage_id 불변 + canonical_source_id label 전용 + S2
권장 후보*로 좁혀졌음을 evidence로 남긴다. 구현/승인/release 결정은 별 트랙.

---

## 3. Design Candidate Summary

본 design review가 좁힌 design candidate:

### 3.1 Resolver scope
- **read-path citation resolver only**
- write-path / persisted / IndexedDB / DOM data-q-id / lookup 영역 미진입
- q52 alias 한정 (66항 영역 미진입)

### 3.2 Storage id 불변 보장
- `qId(q)` → storage_id 반환 (불변)
- `q._id` → storage_id (불변)
- IndexedDB keyPath → storage_id 기반 (불변)
- DOM `data-q-id` → storage_id (불변)
- pdfPageIndex / puaChoicesIndex `__key` → storage_id (불변)

### 3.3 Canonical 격리
- `canonicalSourceId(q)` 별 함수, citation display 전용
- label 양식 L1 권장 (명시 label + value)
- L3 (label 없는 canonical 표시) 금지
- canonical_source_id를 `_id`, `dataset.qId`, IndexedDB key, pdfPageIndex key로
  사용 금지 — 3중 차단 (grep/lint, code review, contract test)

### 3.4 SoT 후보 (구현 시점 결정)
- **S2 권장** — docs registry를 app data로 build-time sync
- S1 (runtime direct read) 비권장
- S3 (hardcoded) 비권장

### 3.5 qId SoT 통합
- 3 qId 위치 (store.js / index.html / main.js)의 single SoT 결정 필요
- store.js의 `export function qId(q)`가 module SoT — index.html/main.js는 같은
  함수를 inline 중복
- 구현 시 module SoT 단일화 또는 3 위치 contract 정합 결정

---

## 4. Residual Risk

| risk | severity | 본 design review에서의 처리 |
|---|---|---|
| qId 3 위치 분산 | Medium | design candidate §3.5 명시. SoT 통합은 구현 시 결정 |
| user-facing source citation UI 부재 | Medium | resolver 도입 시 신규 UI 영역 생성 필요. §1.6 명시 |
| docs registry runtime 의존 위험 | Medium | S2 권장으로 회피 (build-time sync). S1 비권장 |
| canonical_source_id의 app id 오용 위험 | Medium | 3중 차단 명시 (Q4) |
| 66항 systemic problem | Medium | C2 silent fallback으로 resolver scope 한정 |
| 100항 mis-label 영역 | Medium | resolver scope = q52 한정 (C1)으로 회피 |

---

## 5. Decision Record 영향

본 design review는 **정책 변경 없음**:

- App/data decision (`DR-TRAP-GIGI17-APPDATA-DECISION`)의 "후보 B design review
  only" 영역 내부 구체화
- design candidate 좁힘 (read-path citation + storage_id 불변 + L1 label + S2
  SoT)은 design 차원 evidence — 정책 차원의 새 결정 0
- caution release 차단 / row promotion 금지 / Batch migration 차단 / 66항 영역
  분리 — 모두 기존 정책 유지

→ jsonl `trap_map_active_decisions.jsonl`에 별 entry 추가 안 함 (사용자 가이드:
"design review만이고 정책 변경 없으면 추가하지 말 것" 준수).

본 design review 문서 자체가 design candidate 좁힘의 evidence로 충분.

---

## 6. Next Gates

각 별 명시 승인 후만 진행:

1. **별 systemic session-label policy 문서 작성** (별 트랙)
   - 66항 분해 / alias / 보류 중 1택 결정
2. **Implementation plan 작성** (구현 진입 결정 시)
   - 본 design candidate (§3) 기반
   - qId SoT 통합 영역
   - resolver API shape + null/missing fallback
   - S2 build-time sync 정책
   - 6 evidence smoke 영역 (Q8)
   - smoke + 별 명시 승인 후만 구현 진입
3. **Caution release review** (Step 6)
   - 본 design review (design candidate 좁힘) +
   - 별 systemic policy 결정 +
   - user-facing impact evidence (구현 또는 docs-only mock 후) +
   - redryrun evidence
   - 모두 입력 후 plan v2 §6.3 review format 양식

---

## 7. Forbidden Until Separate Approval

- q52 단독 id 재발급
- `questions.json` 수정
- per-year json 수정
- PDF filename rename
- `pdf_pages/index.json` 수정
- app code 수정 (본 design review는 docs-only 영역)
- app alias resolver 구현 (본 design review + implementation plan + 별 승인 후)
- app/data alias registry 추가 (S2 진입 결정 + 별 승인 후)
- record metadata field 추가
- registry row promotion from `candidate` to `approved`
- 기기-17 caution 해제 선언
- Batch migration 진입 (66항 policy 결정 전)
- 66항 systemic policy를 q52 registry 영역에 흡수
- registry artifact 자체 수정 (review baseline 동결)
- canonical_source_id를 `_id` / `dataset.qId` / IndexedDB key / pdfPageIndex key로
  사용
- label 없는 canonical_source_id 단독 표시 (L3 양식 금지)

---

## Status

- Runtime resolver design review 작성 완료.
- design candidate 좁힘 결과:
  - read-path citation resolver only
  - storage_id 불변 보장 (qId / IndexedDB / DOM / pdfPageIndex 모두 유지)
  - canonical_source_id는 label 전용 (L1 권장)
  - SoT 후보 S2 권장 (구현 시 결정)
  - qId SoT 통합 영역 명시
- 정책 변경 0 — jsonl decision entry 추가 안 함 (사용자 가이드 준수).
- app code 변경 0 (read-only inspection만).
- registry artifact 자체 변경 0.
- registry row status=candidate 유지.
- 기기-17 caution 유지.
- Batch migration 차단 유지.
- 다음 gate: 별 systemic session-label policy 문서 / Implementation plan / Caution
  release review.
