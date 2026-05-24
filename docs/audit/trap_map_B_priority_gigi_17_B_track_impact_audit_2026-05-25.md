# Trap-Map B-Priority — 기기-17 B-Track Impact Audit (2026-05-25)

기기-17 record identity B-track 진입 전 영향 범위를 read-only로 측정한다. 본 문서는
data/id/meta를 수정하지 않고, `app/data/questions.json`, per-year json, app key 사용,
pdf_pages index, downstream docs 참조만 확인한다.

본 단계는 audit 문서 작성까지 — app/data, questions.json, per-year json, PDF filename,
pdf_pages, 학습 패키지 미수정. push 없음.

- 대상 이슈: `2020_1회_52` 변압기 Delta-Y 권수비 문제의 true source는
  `data/20200424_1회.pdf` p.4 q52 (PDF 표지 일자 2022-04-24)
- 선행 결론:
  - N1 targeted audit: true source 확정, `2020_1회` 100항 전체 mis-label 가능성
  - N3a A-track: W-1 학습 문서 표기만 `2022_1회_52`로 정정, data/id/meta 보류
  - 기기-17 caution 유지

---

## 판정: **B-track 영향 큼 — q52 단독 id 정정 금지**

`2022_1회` 슬롯은 현재 비어 있어 재귀속 대상 자체의 충돌은 낮다. 그러나 app은
`year_session_q_no` 조합을 `_id`로 생성하고, 이 `_id`를 IndexedDB progress,
annotations, wrong-note filter, pdfPageIndex/puaChoicesIndex lookup에 사용한다.

따라서 `2020_1회_52`만 `2022_1회_52`로 고치는 단독 정정은 금지한다. B-track은
최소한 아래를 함께 설계해야 한다.

1. `2020_1회` 100항 batch 재귀속 여부
2. `2020_1,2회` 66항과의 관계 정리
3. app `_id` migration 또는 alias 정책
4. pdf_pages index key 동기화
5. W-1 학습 문서와 closeout/errata citation 재동기화

---

## 1. Master Data Count

`app/data/questions.json` 기준:

| 항목 | count |
|---|---:|
| 전체 레코드 | 5,331 |
| `year=2020, session="1회"` | 100 |
| `year=2022, session="1회"` | 0 |
| `year=2020, session="1,2회"` | 66 |

핵심 q52:

| key | content | 판정 |
|---|---|---|
| `2020_1회_52` | 변압기 Delta-Y 권수비 / 정답 1 | true source는 2022-04-24 PDF q52, meta label 불일치 |
| `2020_1,2회_52` | 동기전동기 V곡선 / 정답 1 | 2020 1회 q52 PDF content와 정합 |

`year=2022, session="1회"` 레코드는 0개라 2022_1회 재귀속 슬롯 자체는 비어 있다.
하지만 `2020_1회` 100항 전체가 같은 mis-named PDF에서 왔을 가능성이 높으므로,
q52만 이동하는 것은 불완전하다.

---

## 2. Per-Year Files

| 파일 | count | q52 content |
|---|---:|---|
| `data/questions_기출_2020_1회.json` | 100 | 변압기 Delta-Y 권수비 |
| `data/questions_기출_2020_1_2회.json` | 66 | 동기전동기 V곡선 |
| `data/questions_기출_2022_2회.json` | 100 | 2022 2회 |
| `data/questions_기출_2022_1회.json` | 없음 | 없음 |

정책 후보:

- `2020_1회` 100항을 `2022_1회`로 일괄 재귀속
- `2020_1,2회` 66항을 실제 2020 1회/2회 구조로 분해 또는 alias 처리
- per-year filename과 app master를 동시에 다루는 migration plan 필요

---

## 3. App Key Impact

앱은 질문 로드 후 다음 ID를 생성한다.

```js
q._id = q.year + '_' + q.session + '_' + q.q_no
```

확인 위치:

| 파일 | 역할 |
|---|---|
| `app/index.html` | `_id` 생성, `filterByIds`, progress/annotation lookup, pdf index lookup |
| `app/js/store.js` | `qId(q) = \`${year}_${session}_${q_no}\`` |
| `app/js/main.js` / `app/js/bundle.js` | 동일 로직 bundle/legacy |
| `app/js/db.js` | IndexedDB `annotations`, `progress` keyPath = `id` |

영향:

| 영향 영역 | 현재 key | id 변경 시 |
|---|---|---|
| progress | `2020_1회_52` 등 `_id` | 기존 풀이 기록이 새 id와 연결되지 않음 |
| annotations | `_id` | 기존 필기/스크리블이 새 id와 연결되지 않음 |
| wrong note | progress id 기반 `filterByIds` | 기존 오답 목록에서 새 id 문제를 못 찾을 수 있음 |
| pdfPageIndex | `year_session_q_no` key | index key 동기화 필요 |
| puaChoicesIndex | `year_session_q_no` key | 현재 2020_1/2022_1/2020_1,2 관련 key 0, 영향 낮음 |

따라서 option (ii)처럼 id 자체를 재발급하려면 app 사용자 저장 데이터 migration 또는
alias map이 필요하다.

---

## 4. pdf_pages Index Impact

`data/pdf_pages/index.json` 기준:

| key prefix | count |
|---|---:|
| `2020_1회_` | 5 |
| `2022_1회_` | 0 |
| `2020_1,2회_` | 4 |

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

q52 자체는 pdf index key가 없지만, `2020_1회` batch 재귀속 시 위 5개 key도
`2022_1회_*`로 이동 또는 alias되어야 한다.

---

## 5. Systemic Scope

`app/data/questions.json` 기준:

| 측정 | count |
|---|---:|
| 같은 `year+q_no`에 여러 session이 존재하는 case | 1,829 |
| 그중 `2020_1,2회` 포함 case | 66 |
| `year=2020`에서 여러 session이 존재하는 q_no case | 99 |
| `year=2020`에서 `1,2회` 포함 case | 66 |
| 같은 `(year, session, q_no)` 중복(q_no non-null) | 0 |

의미:

- 현재 앱 `_id` 충돌은 없다.
- 하지만 `2020_1회`와 `2020_1,2회`의 공존은 systemic label/pipeline 문제다.
- 기기-17 q52만의 isolated cleanup으로 보지 말고, 2020 1회/1,2회 session policy로
  별도 설계해야 한다.

---

## 6. Downstream Docs Impact

문서 grep 결과 `2020_1회_52`, `2022_1회_52`, `data/20200424`, `기기-17` 참조가
다수 존재한다. 큰 묶음은 아래와 같다.

| 묶음 | 상태 |
|---|---|
| W-1 학습 패키지 3종 | N3a A-track으로 `2022_1회_52` 표기 반영 완료 |
| N1 targeted audit / N2 plan | true source와 B-track 필요성 기록 |
| closeout / post-closeout errata / follow-up errata | 기기-17 caution 사유와 count 기록, 후속 정정 시 동기화 필요 |
| representative redryrun / pilot selection | 과거 `2020_1회_52` 기준 history. historical record로 보존 가능 |
| supervisor layer | 기기-17 caution / B-track 대기 상태 기록 |

정책:

- historical audit/review 문서는 일괄 rewrite하지 않는다.
- final/current-state 문서(closeout/errata/active-state)는 B-track 결과가 확정되면
  후속 erratum으로 갱신한다.

---

## 7. Option Assessment

| 옵션 | 판정 | 이유 |
|---|---|---|
| q52 단독 `2022_1회_52` 재발급 | 금지 | 100항 batch mis-label 가능성과 app `_id` key 영향 과소평가 |
| `2020_1회` 100항 → `2022_1회` batch 재귀속 | 후보 | 슬롯 충돌은 낮지만 app progress/annotation/pdf index migration 필요 |
| alias map 유지 (`2020_1회_*` → `2022_1회_*`) | 후보 | app 저장 key 보존 가능. canonical source와 legacy key 분리 필요 |
| data 미수정 + docs errata만 유지 | 후보 | 저위험이나 caution 해제 어려움 |
| representative 교체 | 비권장 | content valid이고 true source 확정. 교체는 불필요한 재작업 |

---

## 8. 권고

### 8.1 즉시 권고

B-track data normalization은 바로 실행하지 않는다. 다음 plan은 아래 둘 중 하나로 좁힌다.

1. **Alias-first plan**
   - data key는 legacy로 유지
   - canonical source field 또는 alias table로 `2022_1회_*`를 제공
   - app 저장 데이터 migration 없음
   - 기기-17 caution 해제 가능 여부는 "canonical source가 문서화됐는가" 기준으로 별도 판단

2. **Batch migration plan**
   - `2020_1회` 100항을 `2022_1회`로 일괄 재귀속
   - `2020_1,2회` 66항 분해/alias 정책 포함
   - app progress/annotation key migration 또는 compatibility alias 구현
   - pdf_pages index key 동기화

### 8.2 금지

다음은 금지한다.

- q52 단독 id 재발급
- `questions.json`만 바꾸고 per-year/pdf index/app key를 방치
- app progress/annotation migration 없이 `_id` 체계 변경
- 기기-17 caution 해제 선언
- 2020_1회 전체가 2022_1회라고 전수검증 없이 완전 확정 선언

### 8.3 다음 gate

`trap_map_B_priority_gigi_17_B_track_correction_plan_v2_2026-05-25.md` 작성:

- Alias-first vs Batch migration 비교
- app key migration/compatibility plan
- pdf_pages index sync plan
- closeout/errata sync plan
- redryrun 기준
- caution 해제 조건

---

## Status

- B-track impact audit 완료.
- data/app 미수정.
- q52 단독 id 재발급 금지.
- B-track은 alias-first 또는 batch migration plan으로만 진행.
- 기기-17 caution 유지.
