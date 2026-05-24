# Trap-Map B-Priority — 기기-17 B-Track Correction Plan v2 (2026-05-25)

기기-17 B-track impact audit 이후, record identity 정정 실행 전 단계로 작성하는
correction plan v2다. 본 문서는 Alias-first와 Batch migration을 비교하고,
app key compatibility, pdf_pages index, closeout/errata, redryrun, caution 해제 조건을
정의한다.

이번 단계는 plan 작성까지만 수행한다. **app/data, `questions.json`, per-year json,
PDF filename, `pdf_pages/index.json`, 학습 패키지 본문은 수정하지 않는다.** push 없음.
기존 commit amend/rebase/reset 없음. 기기-17 caution 유지. PASS/NEEDS_FIX 판정은
하지 않는다.

- 대상 이슈: 기기-17 변압기 Delta-Y 권수비 문제
- legacy storage key: `2020_1회_52`
- canonical source 표기 후보: `2022_1회_52`
- true source: `data/20200424_1회.pdf` p.4 q52
- PDF 표지 기재 일자: 2022-04-24
- 선행 문서:
  - `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`
  - `docs/audit/trap_map_B_priority_gigi_17_A_track_review_2026-05-23.md`
  - `docs/audit/trap_map_B_priority_gigi_17_record_identity_targeted_audit_2026-05-23.md`
  - `docs/audit/trap_map_B_priority_gigi_17_correction_plan_2026-05-23.md`

---

## 0. Non-Negotiable Guardrails

다음은 본 B-track 전체에 적용하는 hard guardrail이다.

1. **q52 단독 id 재발급 금지.**
   - `2020_1회_52`만 `2022_1회_52`로 바꾸지 않는다.
   - 기기-17 q52는 `2020_1회` 100항 batch mis-label 가능성의 사례로 취급한다.
2. **app 저장 key 영향 없이 `_id` 체계를 변경하지 않는다.**
   - progress, annotations, wrong-note filter, pdfPageIndex lookup이 `_id`에 의존한다.
3. **data만 고치고 index/app/docs를 방치하지 않는다.**
   - `questions.json`, per-year json, `pdf_pages/index.json`, app compatibility, closeout/errata는
     같은 plan 안에서 동기화되어야 한다.
4. **기기-17 caution 해제 선언 금지.**
   - 본 plan은 caution 해제 조건을 정의할 뿐, 해제를 판정하지 않는다.
5. **historical audit/review 문서는 rewrite하지 않는다.**
   - 최종 상태 문서와 errata 계열만 B-track 결과 확정 후 동기화한다.

---

## 1. Current State Summary

Impact audit 기준 현재 상태:

| 항목 | 상태 |
|---|---|
| `app/data/questions.json` 전체 | 5,331 records |
| `year=2020, session="1회"` | 100 records |
| `year=2022, session="1회"` | 0 records |
| `year=2020, session="1,2회"` | 66 records |
| 정확한 `(year, session, q_no)` 중복 | 0 |
| `data/pdf_pages/index.json` `2020_1회_*` | 5 keys |
| `data/pdf_pages/index.json` `2022_1회_*` | 0 keys |
| `data/pdf_pages/index.json` `2020_1,2회_*` | 4 keys |

핵심 해석:

- `2022_1회` 슬롯은 비어 있어 canonical target 자체의 충돌은 낮다.
- 그러나 `2020_1회` 100항 전체가 `data/20200424_1회.pdf`에서 온 batch일 가능성이
  있으므로 q52 단독 정정은 잘못된 축소다.
- app은 `_id = year + '_' + session + '_' + q_no`를 생성해 persisted user data와
  index lookup에 사용한다.
- 따라서 B-track은 data normalization 문제가 아니라 **record identity + persisted key
  compatibility + index/document sync** 문제다.

---

## 2. Option Comparison

### 2.1 Option A — Alias-First

Legacy storage key는 유지하고, canonical source를 별도 필드 또는 alias table로 제공한다.

예시 정책:

| 개념 | 값 |
|---|---|
| storage key | `2020_1회_52` |
| canonical source id | `2022_1회_52` |
| source PDF | `data/20200424_1회.pdf` p.4 q52 |
| PDF 표지 기재 일자 | 2022-04-24 |
| app persisted key | 변경 없음 |

가능한 구현 형태:

- app/data 내부 별도 alias table: `legacy_id -> canonical_source_id`
- question record 내부 canonical source metadata field
- docs-level source registry를 먼저 만들고, app/data 반영은 별도 승인 후 진행

장점:

- progress/annotations/wrong-note key migration이 필요 없다.
- q52 단독 id 재발급을 피하면서 true source를 사용자와 후속 작업자에게 노출할 수 있다.
- `2020_1회` 100항 전수 재귀속 전에도 partial canonical documentation이 가능하다.
- data normalization rollback 비용이 낮다. app alias resolver 도입 후 user-facing rollback
  영향은 §2.3 trade-off 표에서 별도 평가한다.

단점/위험:

- storage key와 canonical source가 다르므로 "clean"의 정의가 복잡하다.
- app UI가 legacy key만 보여주면 사용자 혼란이 남을 수 있다.
- caution 해제는 "canonical source 문서화만으로 충분한가"라는 별도 정책 판단이 필요하다.

### 2.2 Option B — Batch Migration

`2020_1회` 100항을 `2022_1회`로 일괄 재귀속하고, `2020_1,2회` 66항의 session 정책을
함께 정리한다.

필수 범위:

- `app/data/questions.json` 100항 year/session 변경
- `data/questions_기출_2020_1회.json`과 `data/questions_기출_2022_1회.json` 파일 정책
- `2020_1,2회` 66항 분해 또는 alias 정책
- app progress/annotation key migration 또는 bidirectional compatibility alias
- `data/pdf_pages/index.json` key 이동/alias
- closeout/errata/current-state 문서 sync

장점:

- data key와 canonical source가 일치한다.
- 장기적으로 source identity가 가장 명확하다.
- caution 해제 기준을 더 단순하게 만들 수 있다.

단점/위험:

- persisted user data key가 바뀐다.
- pdf_pages index와 app lookup 동기화 실패 시 문제 원문/이미지 연결이 깨질 수 있다.
- `2020_1,2회` 66항까지 같이 다뤄야 해서 blast radius가 크다.
- 전수 검증 없이 100항 전체를 2022 1회로 확정하면 source claim이 과해질 수 있다.

### 2.3 Preferred Direction

현재 plan 단계의 선호 방향은 **Alias-first**다. 정확히는 **위험 회피를 우선할 때의
1순위 설계 후보**다.

이유:

- B-track impact audit이 확인한 가장 큰 위험은 app persisted key와 index key 영향이다.
- Alias-first는 legacy key를 보존하면서 canonical source를 표현할 수 있다.
- Batch migration은 data/app/pdf_pages/user persisted keys가 함께 움직이므로 명시 승인 전
  실행하기에 고위험이다.

trade-off:

| 기준 | Alias-first | Batch migration |
|---|---|---|
| 단기 안전성 | 높음. persisted key와 기존 index key를 유지 | 낮음. data/app/pdf_pages/user key가 같이 이동 |
| 장기 source identity | 중간. storage id와 canonical source id가 분리됨 | 높음. data key와 canonical source가 일치 |
| caution 해제 난이도 | 높음. legacy storage key를 clean으로 볼지 별도 판단 필요 | 낮아질 수 있음. 단 migration 검증 부담 큼 |
| rollback 비용 | data normalization rollback은 낮음. app alias resolver 도입 후에는 사용자-facing 영향 별도 평가 필요 | 높음. id, persisted data, index rollback이 함께 필요 |
| 실행 전 필요 evidence | alias SoT, resolver/read-path, integrity check | 100항 source evidence, 66항 session policy, migration fixture |

단, Alias-first로 caution을 해제할 수 있는지는 별도 기준을 충족해야 한다. 본 plan은
Alias-first를 "즉시 실행안"으로 확정하지 않고, **우선 설계 후보 1순위**로 둔다.

### 2.4 Option C — Docs Errata Only

Impact audit의 후보였던 "data 미수정 + docs errata만 유지"는 본 plan에서
Alias-first 실행 전 또는 실행 보류 시의 **temporary preservation state**로 분류한다.
app/data alias resolver 없이 authoritative docs만으로 canonical source를 설명하는
상태이며, 최종 cleanup variant로 간주하지 않는다.

| 항목 | 평가 |
|---|---|
| 장점 | 변경 범위가 가장 작고 app/data 위험이 없다 |
| 단점 | app/user-facing source identity는 여전히 legacy key 중심으로 남는다 |
| caution | 해제 근거로는 약함. 원칙적으로 caution 유지 또는 별도 review 필요 |
| 사용 조건 | 실행 전 임시 설명 또는 historical errata 유지에 한정 |

Docs Errata Only 진입도 별도 명시 승인 대상이다. 신규 errata 문서 작성 또는 기존
current-state 문서 sync 전에는 사용자 승인과 scope 확인이 필요하다.

---

## 3. App Key Migration / Compatibility Plan

### 3.1 Alias-First Compatibility

Alias-first 채택 시 app persisted key는 유지한다.

| 영역 | 처리 |
|---|---|
| question `_id` | `2020_1회_52` 등 legacy key 유지 |
| progress | migration 없음 |
| annotations | migration 없음 |
| wrong-note filter | legacy id로 계속 동작 |
| display/source citation | canonical source id를 별도 표시하거나 lookup |
| pdfPageIndex lookup | legacy key 우선, canonical alias fallback 가능 |

필수 app 설계:

1. `canonicalSourceId(q)` 또는 alias resolver를 도입한다.
2. 사용자 저장 데이터 lookup은 `storageId` 기준으로 유지한다.
3. source 표시, external citation, errata 표시만 `canonicalSourceId`를 참조한다.
4. alias table은 one-way storage로 시작한다: `storageId -> canonicalSourceId`.
5. 같은 canonical id가 여러 storage id에 매핑되는지 중복 검사를 둔다.

주의:

- alias resolver, `canonicalSourceId(q)`, 중복 검사는 app 코드 변경 영역이다.
- §0의 보호 대상은 persisted storage key와 `_id` 체계이며, app read-path 코드 변경을
  자동 승인하지 않는다.
- app 코드 변경, tracked data alias 추가, docs-only alias registry 추가는 각각 별도
  명시 승인 후 진행한다.
- Alias-first는 "app 미변경"이 아니라 "persisted key 미변경" 전략으로 정의한다.

권장 명명:

| 용어 | 의미 |
|---|---|
| `storage_id` | app persisted key. 현재 `_id`와 동일 |
| `canonical_source_id` | 원본 시험/회차/q_no 기준 citation id |
| `source_pdf` | canonical source PDF path |
| `source_pdf_page` | PDF page |

### 3.1A Alias Table Source-of-Truth Candidates

Alias-first 실행 전 alias table의 source of truth(SoT)를 먼저 결정한다.

| 후보 | 내용 | 장점 | 위험 / 한계 |
|---|---|---|---|
| tracked docs registry | `docs/audit/...` 아래 markdown/json registry | data/app 미수정, review 용이 | app runtime이 직접 참조하지 않으면 user-facing 개선 제한 |
| tracked app data registry | app data 영역에 별도 alias json | app resolver와 연결 쉬움 | app/data 수정이므로 별도 승인 필요 |
| record metadata field | 각 question record에 canonical field 추가 | record와 source가 가까움 | `questions.json`/per-year 수정이므로 고위험 |
| app hardcoded mapping | JS module/object로 mapping 보관 | 구현 빠름 | data ownership 불명확, 장기 유지 부적합 |

위험 회피를 우선할 때의 기본 선호는 **tracked docs registry로 schema를 먼저 확정한 뒤**,
app/data 반영 필요성을 별도 승인 gate로 넘기는 것이다. 이 기본 선호도 실행안은
아니며, SoT 결정은 decision record에 남긴다.

### 3.1B Alias Integrity Checks

Alias-first 실행 전후에 아래 integrity check를 통과해야 한다.

1. 같은 `storage_id`가 두 개 이상의 `canonical_source_id`에 매핑되지 않는다.
2. storage는 one-way로 유지하되, 검증 시 `canonical_source_id -> storage_id` 역방향
   인덱스를 생성한다. 같은 `canonical_source_id`에 여러 `storage_id`가 매핑되는 경우
   의도된 alias인지 별도 목록에 표시한다.
3. 모든 `storage_id`가 current app question set에 존재한다.
4. 모든 `canonical_source_id`는 source PDF, page, q_no evidence와 3-way로 정합해야 한다.
5. orphan canonical id, dangling storage id, duplicate alias row가 0건이어야 한다.
6. q52는 단독 id 재발급이 아니라 alias/inventory entry로만 표현되어야 한다.

### 3.2 Batch Migration Compatibility

Batch migration 채택 시 단순 id 변경은 금지한다. 아래 둘 중 하나가 필요하다.

| 방식 | 내용 | 위험 |
|---|---|---|
| explicit migration | IndexedDB progress/annotations key를 legacy id에서 new id로 이전 | migration 실패/중복 처리 필요 |
| compatibility alias | new id lookup 시 legacy id 저장 데이터도 읽고, write policy를 정의 | 장기 alias 부채 |

필수 migration 규칙:

1. migration 전 legacy/new id mapping table을 frozen artifact로 남긴다.
2. progress와 annotations를 같은 mapping으로 처리한다.
3. conflict가 있으면 new id 우선/legacy id 우선/merge 중 하나를 사전 정의한다.
4. migration은 idempotent해야 한다.
5. rollback 시 legacy id로 읽을 수 있어야 한다.
6. user data migration test fixture를 만든 뒤 app local smoke test를 통과해야 한다.

Batch migration 전 금지:

- `questions.json`만 먼저 변경
- per-year json만 먼저 변경
- app compatibility 없이 `_id` 생성 로직 변경
- progress/annotation backup 없이 migration 실행

---

## 4. pdf_pages Index Sync Plan

### 4.1 Current Index Impact

`data/pdf_pages/index.json`의 관련 key:

| prefix | count |
|---|---:|
| `2020_1회_*` | 5 |
| `2022_1회_*` | 0 |
| `2020_1,2회_*` | 4 |

현재 matching keys:

- `2020_1회_53`
- `2020_1회_71`
- `2020_1회_72`
- `2020_1회_73`
- `2020_1회_79`
- `2020_1,2회_59`
- `2020_1,2회_73`
- `2020_1,2회_76`
- `2020_1,2회_77`

q52 자체는 pdf index key가 없지만, batch 재귀속 시 관련 prefix index가 같이 움직인다.

### 4.2 Alias-First Index Policy

Alias-first의 기본 정책은 **legacy index key 유지 + canonical fallback 제공**이다.

필수 조건:

1. 기존 `2020_1회_*` index key를 삭제하지 않는다.
2. canonical source 표시가 필요한 경우 alias resolver가 `2022_1회_*` 요청을
   `2020_1회_*` index로 fallback할 수 있어야 한다.
3. fallback은 read path에만 적용한다. write/update path는 명시 승인 전 열지 않는다.
4. q52처럼 index key가 없는 항목은 "no pdf page index key" 상태를 그대로 기록한다.

범위 한정:

- q52 자체는 현재 pdf index key가 없다.
- 따라서 alias fallback의 직접 benefit은 q52가 아니라 `2020_1회_*` prefix에 존재하는
  5개 indexed key와 canonical citation/read-path 일관성에 한정된다.
- q52는 source PDF/page citation으로 검증하고, pdfPageIndex hit를 caution 해제 근거로
  사용하지 않는다.

검증:

- legacy key lookup이 기존과 동일하게 동작하는지 확인한다.
- canonical id lookup이 필요한 화면에서 alias fallback이 동작하는지 확인한다.
- 없는 key와 alias miss를 구분해 logging한다.

### 4.3 Batch Migration Index Policy

Batch migration 채택 시 index key 동기화는 필수다.

필수 작업:

1. `2020_1회_*` index key 5건을 `2022_1회_*`로 이동 또는 alias한다.
2. image/page asset path가 key name을 포함하는지 별도 확인한다.
3. `2020_1,2회_*` 4건은 66항 session 정책 확정 전 이동하지 않는다.
4. old key lookup이 필요한 app compatibility 기간을 정의한다.
5. migration 후 duplicate key, missing asset, dangling index를 검사한다.

Batch migration의 pdf_pages gate:

- `index.json` key count before/after diff
- moved/aliased key list
- app pdf page lookup smoke test
- q52 no-index 상태의 명시적 기록

---

## 5. Closeout / Errata Sync Plan

B-track 결과가 확정되기 전 historical 문서는 rewrite하지 않는다. 확정 후 sync 대상은
"현재 상태를 안내하는 문서"에 한정한다.

### 5.1 Sync 대상

| 문서 묶음 | 처리 |
|---|---|
| W-1 학습 패키지 3종 | A-track에서 source citation correction 완료. B-track 결과 확정 시 storage/canonical wording만 필요하면 후속 erratum |
| pilot closeout | caution 사유와 기기-17 count 갱신 필요 |
| post-closeout errata | B-track 결과와 caution 상태 갱신 필요 |
| follow-up errata | Alias-first 또는 Batch migration 결과 반영 필요 |
| active-state / supervisor docs | decision layer 상태만 최신화. 과도한 메타 작업 금지 |
| historical audit/review | rewrite 금지. 필요 시 "superseded by" 문서 링크만 추가 후보 |

supervisor docs sync 범위:

- B-track 결과가 확정되면 active-state 또는 supervisor log에 1개 entry만 추가한다.
- 기존 supervisor policy, metric, cascade rule은 수정하지 않는다.
- decision record가 필요한 정책 판단은 §8의 항목으로 제한한다.
- review 지적 대응을 이유로 supervisor layer 구조를 확장하지 않는다.

### 5.2 Sync 문구 원칙

Alias-first가 채택될 경우:

- "storage key remains `2020_1회_52`"
- "canonical source is documented as `2022_1회_52`"
- "source PDF: `data/20200424_1회.pdf` p.4 q52, PDF cover date 2022-04-24"
- "no app persisted key migration was performed"

Batch migration이 채택될 경우:

- "`2020_1회_*` batch migrated to `2022_1회_*`" 범위 명시
- `2020_1,2회` 66항 정책 명시
- app persisted key migration/compatibility 결과 명시
- pdf_pages index migration/alias 결과 명시

---

## 6. Redryrun Criteria

B-track 실행 후 redryrun은 option별로 기준을 다르게 둔다.

### 6.1 Alias-First Redryrun

필수 확인:

1. 기기-17 representative citation이 canonical source를 보여준다.
2. storage key가 legacy로 유지됨을 문서와 app display가 혼동 없이 표현한다.
3. progress/annotations가 기존 legacy id로 유지된다.
4. wrong-note filter가 기존 id 기반으로 계속 작동한다.
5. pdf page lookup이 legacy key로 깨지지 않는다.
6. canonical alias lookup이 필요한 화면에서 실패하지 않는다.
7. W-1 학습 패키지 3종의 A-track 정정과 B-track 표현이 충돌하지 않는다.

redryrun evidence:

- alias mapping table excerpt
- alias integrity check result
- app key lookup smoke result
- q52 source citation display 또는 docs excerpt
- pdf_pages related key count
- closeout/errata sync diff summary

### 6.2 Batch Migration Redryrun

필수 확인:

1. `2020_1회` 100항이 전수 검증 또는 충분한 evidence 기준으로 `2022_1회`에 재귀속됐다.
2. q52 단독 이동이 아니라 batch policy로 수행됐다.
3. `2020_1,2회` 66항 정책이 함께 확정됐다.
4. progress/annotations migration 또는 compatibility alias가 동작한다.
5. pdf_pages index key 이동/alias가 동작한다.
6. wrong-note filter가 migrated/new id를 찾는다.
7. duplicate id, missing id, dangling index가 없다.
8. closeout/errata/current-state 문서가 결과를 반영한다.

redryrun evidence:

- before/after id count table
- migration mapping artifact
- IndexedDB migration or compatibility smoke test
- pdf_pages before/after key diff
- q52 and at least 4 related 2020_1회 samples
- `2020_1,2회` sample check

### 6.3 Caution Release Review Format

caution 해제 review는 별도 문서로 작성하며, 최소한 아래 항목을 포함한다.

| 항목 | 필수 내용 |
|---|---|
| scope | Alias-first 또는 Batch migration 중 실제 실행 범위 |
| evidence inventory | source PDF/page, alias/migration mapping, app smoke, pdf_pages check |
| guardrail check | q52 단독 id 재발급 없음, app/data/pdf_pages 승인 범위 준수 |
| acceptance criteria | §7의 measurable criteria 결과 |
| residual risk | legacy storage key 잔존, 66항 미해결 여부, user-facing 혼동 가능성 |
| decision | caution 유지 / caution 해제 후보 / BLOCKED 중 하나 |

user-facing citation은 app screen smoke, display-layer code grep, 또는 docs-only state인
경우 current-state 문구 diff 중 하나로 측정한다. review 판정은 PASS/NEEDS_FIX를 자동
선언하지 않는다. 해제 여부는 review 문서와 decision record가 모두 준비된 뒤 별도
gate에서 결정한다.

---

## 7. Caution Release Conditions

본 plan은 기기-17 caution을 해제하지 않는다. 아래 조건을 모두 만족한 뒤 별도 review에서
해제 여부를 판정한다.

### 7.1 Common Conditions

Alias-first와 Batch migration 모두 공통:

1. q52 단독 id 재발급이 발생하지 않았음.
2. true source가 `data/20200424_1회.pdf` p.4 q52로 명시되어 있음.
3. PDF 표지 기재 일자 2022-04-24와 파일명 `20200424`의 불일치가 "표지 기재 일자"
   기준으로 표현되어 있음.
4. 기기-17 학습 내용(변압기 Delta-Y 권수비, 정답 1, `aV/sqrt(3)`, `sqrt(3)I/a`)이
   A-track 정정과 충돌하지 않음.
5. app persisted key 또는 compatibility 영향이 검증됨.
6. pdf_pages index 상태가 검증됨.
7. closeout/errata/current-state 문서가 sync됨.
8. redryrun과 review가 별도 문서로 완료됨.

measurable criteria:

| 조건 | 측정 기준 |
|---|---|
| source citation | q52의 source PDF/page/q_no/canonical id가 1개 authoritative artifact에 존재 |
| app key | progress, annotations, wrong-note lookup smoke가 legacy id 기준으로 모두 통과 |
| pdf_pages | 관련 prefix count와 key list before/after가 문서화되고 dangling index 0건 |
| closeout/errata | sync 대상 문서 목록과 변경/미변경 사유가 diff summary에 존재 |
| redryrun/review | redryrun 문서와 caution release review 문서가 각각 존재 |
| guardrail | q52 단독 id 변경, unapproved app/data/pdf_pages 변경, caution 선해제 0건 |

### 7.2 Alias-First Specific Conditions

Alias-first에서 caution 해제를 검토하려면 아래 정책 판단이 필요하다.

| 질문 | 해제 가능 쪽 기준 | 해제 보류 쪽 기준 |
|---|---|---|
| storage key와 canonical source가 달라도 clean인가? | app/user-facing citation이 canonical source를 명확히 보여주고, storage key가 내부 key임을 분리 표현 | 사용자-facing id가 계속 `2020_1회_52`만 보이면 caution 유지 |
| data 자체는 legacy인데 source identity가 정정됐는가? | canonical source field/alias table이 tracked data 또는 authoritative docs에 존재 | docs errata만 있고 app/data가 canonical source를 모르면 caution 유지 |
| migration 없음이 안전성인가 부채인가? | persisted key 보존이 명시적 compatibility 정책으로 기록됨 | 임시 회피로만 기록되고 resolver/test가 없으면 caution 유지 |

Alias-first caution 해제 최소 기준:

- 사용자 또는 후속 작업자가 `2020_1회_52`를 봤을 때 true source `2022_1회_52`를
  추적할 수 있어야 한다.
- app 내부 storage id와 canonical source id가 명명상 분리되어야 한다.
- "legacy storage key retained by design"이라는 정책 판단이 decision record 또는
  동등한 authoritative 문서에 남아야 한다.

Alias-first measurable criteria:

1. alias SoT artifact 위치가 decision record에 기록되어 있다.
2. `storage_id=2020_1회_52`와 `canonical_source_id=2022_1회_52` mapping이 존재한다.
3. q52 source PDF/page/q_no evidence가 mapping row 또는 linked evidence에 존재한다.
4. alias integrity checks 6개가 모두 통과한다.
5. user-facing citation이 legacy storage key만 보여주는 상태라면 caution 해제 후보가
   아니라 caution 유지로 분류한다.
6. Docs Errata Only variant에 머문 경우 caution 해제 후보로 올리지 않는다.

### 7.3 Batch Migration Specific Conditions

Batch migration에서 caution 해제를 검토하려면 아래가 필요하다.

- `2020_1회` 100항 batch source claim의 evidence가 충분해야 한다.
- app persisted data migration 또는 compatibility alias가 검증되어야 한다.
- `2020_1,2회` 66항 정책이 미해결로 남지 않아야 한다.
- `pdf_pages/index.json` 동기화가 완료되어야 한다.
- old/new id mapping이 문서화되어야 한다.

Batch migration measurable criteria:

1. `2020_1회` 100항 source claim은 전수 check 또는 사전에 정의된 sample/evidence
   protocol을 통과해야 한다.
2. old/new id mapping row count가 migrated question count와 일치한다.
3. progress/annotations migration 또는 compatibility smoke test가 통과한다.
4. `2020_1,2회` 66항은 분해/alias/보류 중 하나로 명시 결정되어야 하며, "미정"이면
   caution 해제 후보로 올리지 않는다.
5. pdf_pages moved/aliased key count가 before/after diff와 일치하고 dangling index가
   0건이어야 한다.

---

## 7A. `2020_1,2회` 66항 Handling

`2020_1,2회` 66항은 기기-17 q52의 직접 수정 대상이 아니라 systemic session-label
문제다. 본 plan에서는 B-track의 blocking risk로 관리하되, 실행은 별도 트랙으로
분리한다.

| 경로 | 66항 처리 |
|---|---|
| Alias-first | 66항을 즉시 수정하지 않는다. 다만 caution release review에서 residual risk로 명시 |
| Batch migration | 66항 session policy가 선결 조건이다. 분해/alias/보류 중 하나를 결정해야 함 |
| Docs Errata Only | 66항은 별도 systemic issue로 유지하고 caution 해제 근거로 사용하지 않음 |

정책:

- Alias-first를 채택해도 66항 문제가 사라진 것으로 간주하지 않는다.
- 66항 처리는 "기기-17 q52 단독 id 재발급 금지"와 같은 guardrail 아래 별도 plan으로
  다룬다.
- 66항 미해결 상태에서 caution을 해제하려면, 그 residual risk가 기기-17 source citation
  clean 여부와 분리 가능하다는 review 근거가 필요하다.

---

## 8. Decision Record Needs

본 plan 단계에서 새 PASS/NEEDS_FIX 판정은 하지 않는다. 다만 실행 전 아래 정책 판단은
decision record에 남겨야 한다.

1. Alias-first를 채택할지 Batch migration을 채택할지.
2. Alias-first 채택 시, "canonical source documented + legacy storage key retained"를
   clean으로 볼지 caution으로 볼지.
3. Batch migration 채택 시, persisted key migration 방식(explicit migration vs
   compatibility alias).
4. `2020_1,2회` 66항을 분해할지 alias로 유지할지.
5. alias table SoT artifact 위치.
6. Docs Errata Only를 임시 상태로 유지할지, Alias-first 실행 범위에 포함할지.
7. caution release review에서 사용할 acceptance criteria set.

---

## 9. Recommended Next Sequence

권장 순서:

1. 본 plan review.
2. Alias-first 채택 여부 정책 결정.
3. Alias-first 채택 시:
   - canonical alias schema 작성 (별도 승인)
   - alias SoT 위치 결정 (decision record)
   - app read-path compatibility 설계 (app 코드 변경 별도 승인)
   - pdf_pages legacy/canonical fallback 설계 (별도 승인)
   - closeout/errata sync plan 확정 (별도 승인)
   - redryrun fixture와 caution release review 양식 정의
4. Batch migration을 선택해야 한다면:
   - `2020_1회` 100항 source evidence 보강
   - `2020_1,2회` 66항 session policy 작성
   - app persisted key migration plan 작성
   - pdf_pages migration plan 작성
5. 별도 승인 후에만 app/data/pdf_pages 수정.

현재 권고:

- 즉시 data normalization은 보류한다.
- q52 단독 id 재발급은 계속 금지한다.
- 다음 실행 후보는 Alias-first로 좁히되, caution 해제 가능성은 review gate에서 별도 판정한다.

---

## Status

- B-track correction plan v2 작성 완료.
- data/app/pdf_pages 미수정.
- q52 단독 id 재발급 금지 유지.
- 기기-17 caution 유지.
- PASS/NEEDS_FIX 판정 없음.
