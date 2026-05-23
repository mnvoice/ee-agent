# Trap-Map B-Priority — 기기-18 Steps Cleanup Feasibility / Review (2026-05-23)

기기-18 correction follow-up erratum(`c6d57d0`)이 caution 사유로 식별한
`2010_2회_47` `steps` 필드의 문제 48(유도전동기 회전수) 혼입에 대한 cleanup
feasibility/review다. 본 단계는 feasibility 검토만 — **app/data/questions.json
미수정**.

본 단계는 feasibility 문서 작성까지 — app/data·questions.json 미수정. solution/
answer/choices/text 미수정. 학습 패키지 문서 미수정. 유료 API 미호출. local
server 미실행. amend/rebase/reset 없음.

- 검토 대상: `app/data/questions.json` / 레코드 `2010_2회_47` / **`steps` 필드만**
- 참조:
  - follow-up erratum (`docs/audit/trap_map_B_priority_gigi_18_correction_followup_erratum_2026-05-23.md`)
  - redryrun after correction (`docs/audit/trap_map_B_priority_gigi_18_redryrun_after_correction_2026-05-23.md`)
  - Commit B evidence supplement (`docs/audit/trap_map_B_priority_gigi_18_commitB_evidence_supplement_2026-05-23.md`)
  - 원본 PDF `data/문제_2010_2회_20260316.pdf` page 8, 문제 47 풀이

---

## 결론: **proceed_minimal_cleanup 권장** — `steps` 필드를 `null`로 설정

PDF 문제 47 풀이는 분류·서술 단락이며 `{인식, 변환, 계산}` 3단계 구조가 자연
스럽지 않다. 따라서 PDF 기반 *재작성*은 추론적 구조화 위험이 크다. 가장 안전한
경로는 **혼입 내용을 제거하고 `steps`를 `null`로 설정** — corpus 내 이미 69개
레코드가 동일한 `null` 상태를 사용 중이며, 표기상 정확하고 G-1 anti-fabrication
취지를 충족.

cleanup 완료 시 기기-18은 **caution → 완전 클린**으로 전환 가능. 단 실제 데이터
수정은 본 feasibility 승인 + Step 1/3와 동등한 명시 권한 부여가 선행되어야 함.

---

## 1. 현재 `steps` 필드 상태 (직접 확인)

`app/data/questions.json` `2010_2회_47` `steps` (json.load decoded):

| sub-key | 길이 | 내용 요약 | 분류 |
|---|---|---|---|
| 인식 | 130 chars | "문제는 '유도 전동기의 전부하 회전수'를 구하는 것으로, 변압기 문제가 아닌 유도 전동기 문제..." | **문제 48 유도전동기 혼입** |
| 변환 | 556 chars | "유도 전동기의 에너지 평형식... $N_s = 120f/P = 900$ [rpm], 슬립, 2차 입력전력..." | **문제 48 유도전동기 혼입** |
| 계산 | 190 chars | "$N_s = 900$ [rpm], $P_2 = 95$ [kW], ... **정답: (4) 약 874[rpm]**" | **문제 48 유도전동기 혼입** |

3 sub-key 전부 문제 48 내용. 흥미롭게도 `인식`의 첫 문장이 "변압기 문제가 아닌
유도 전동기 문제입니다"라고 *자신의 mis-routing을 자인*하고 있다 — 추출 단계에서
인접 문항 혼입이 발생했음을 steps 본문 자체가 증언.

→ 혼입 사실 확정. follow-up erratum §4 결함 logging과 일치.

---

## 2. Schema 분석 (corpus-wide)

5,331 레코드 전수 분석:

| `steps` 값 타입 | 레코드 수 | 비율 |
|---|---|---|
| dict (객체) | 5,262 | 98.7% |
| None (`null`) | 69 | 1.3% |

dict 중 key 구성 (top 분포):

| key 구성 | 레코드 수 | 비율 (dict 중) |
|---|---|---|
| `{인식, 변환, 계산}` | 4,905 | 93.2% |
| `{인식, 계산}` | 57 | 1.1% |
| 기타 | 300 | empty `{}` |

**관찰**:
- 표준 schema = `dict {인식, 변환, 계산}`. 본 레코드도 이 schema.
- `null` 상태는 **69개 레코드의 인정된 schema 옵션** — 정상 데이터 상태.
- empty `{}` (300개)도 사용됨.
- → `steps` 필드를 비우거나 `null`로 두는 것은 corpus 관행상 허용.

---

## 3. PDF 문제 47 풀이 vs `{인식, 변환, 계산}` Schema

원본 PDF `data/문제_2010_2회_20260316.pdf` 문제 47 풀이 (Commit B evidence
supplement §4.2 인용):

```
풀이
변압기의 시험
 (1) 개방 회로 시험(무부하 시험)으로 측정할 수 있는 항목
   · 무부하 전류 · 히스테리시스손 · 와류손 · 여자 어드미턴스 · 철손
 (2) 단락 시험으로 측정할 수 있는 항목
   · 임피던스 와트(전부하 동손) · 임피던스 전압(전압 강하)
 그러나, 절연내력은 절연재의 종류에 따라 정해지는 것으로서 무부하
 시험과 단락시험으로는 구할 수 없다.   [답] ④
```

### Schema 적합성 검토

`{인식, 변환, 계산}` 3단계 schema는 **계산형 문제**에 자연스럽다(인식=문제 식별 →
변환=공식·식 적용 → 계산=수치 도출). 본 문항은:

- `q_type`: **`개념형`** (계산형 아님).
- PDF 풀이: 시험 분류 사실 단락 — 수치 계산 없음, 식 변환 없음.
- 내용 구조: 분류 항목 list + 별도성 단서.

→ PDF 풀이를 `{인식, 변환, 계산}` 3 단계로 강제로 쪼갤 *자연스러운 분할점*이
없다. 강제 쪼갬 시:
- 인식: "변압기 등가회로 시험에서 무엇이 측정 가능한가" — 메타 진술 생성 필요
- 변환: 식이 없음 — 빈 칸 또는 인위적 보충 필요
- 계산: 계산이 없음 — "[답] ④" 같은 단순 결론 또는 빈 칸

위 변환·계산을 채우려면 **PDF에 없는 인위적 진술 생성**이 필요하다 — G-1
anti-fabrication 위반 위험.

---

## 4. Solution ↔ Steps 관계

- `solution` (Commit B 후): 194자 분류 단락 (PDF 풀이 정합).
- `steps` (현재): 유도전동기 혼입 dict.
- 표준 관행: `solution` = 풀이 본문, `steps` = 풀이를 3 단계로 구조화한 학습 도구
  (주로 계산형 문제에서 유의미).
- 본 문항은 **개념형**이며 `solution` 자체가 짧고 분류적 — `steps`의 3 단계
  구조화 가치가 낮다.
- 학습 패키지(study set·day plan·learning log)는 `solution`만 직접 참조하고
  `steps`는 직접 노출하지 않는다 (학습 패키지 카드의 6칸·8칸 구조는 자체
  schema). 따라서 `steps`가 비어있어도 학습 패키지 영향 없음.

→ `solution`이 풀이 정합을 담보하고, `steps` 비움은 학습 영향 없음.

---

## 5. Cleanup 옵션 비교

| 옵션 | 내용 | 장점 | 단점 | 추론 위험 |
|---|---|---|---|---|
| **A. proceed_minimal_cleanup** | `steps` 값을 `null` 또는 `{}`로 설정 | 혼입 완전 제거, 정직한 schema, 69 None / 300 empty 선례 있음, G-1 충족 (생성 0) | steps 데이터 자체는 사라짐 | 없음 |
| B. proceed_source_grounded_rewrite | PDF 풀이를 `{인식, 변환, 계산}` 3 단계로 재작성 | steps 데이터 유지 | PDF에 3 단계 구조 부재 → 인위적 보충 필요, G-1 위반 위험, 변환·계산 단계가 *생성적*이 됨 | **높음** |
| C. defer | 현 contamination 유지, 후속 트랙 대기 | 즉시 작업 없음 | caution 잔존, 데이터 무결성 오염 지속, app에서 steps 노출 시 잘못된 풀이 표시 | 해당 없음 (작업 없음) |
| D. no_action | contamination 영구 유지 | — | 데이터 무결성 영구 오염, 추출 파이프라인 버그 silence | 해당 없음 |

### 권장: **옵션 A (proceed_minimal_cleanup) — `steps`를 `null`로 설정**

근거:
- PDF 풀이의 구조(분류 단락)와 `{인식, 변환, 계산}` schema(계산 3 단계) 사이의
  자연스러운 매핑이 없음 — 옵션 B는 인위적 구조화로 G-1 위험.
- `null`은 corpus의 69개 레코드가 이미 사용 중인 *인정된 schema 상태*.
- 학습 패키지가 steps를 직접 노출하지 않으므로 학습 영향 0.
- 추출 파이프라인 버그(인접 문항 혼입)는 별도 회귀 트랙에서 다룸 — cleanup은
  본 레코드 데이터를 정직한 상태로 되돌리는 데 한정.

`null` vs `{}` 둘 중 어느 것? — corpus가 둘 다 사용. `null`이 더 명시적이고 69개
선례가 있음. 권장: `null` (= JSON `null`). 단 사용자가 `{}`를 선호하면 그것도
허용 (둘 다 schema 정합).

---

## 6. 수정 시 허용 범위 제안

본 feasibility 승인 + Step 1/3와 동등한 명시 권한 부여 시 실행 후보 작업:

| 항목 | 값 |
|---|---|
| 파일 | `app/data/questions.json` |
| 레코드 | `2010_2회_47` **단일** |
| 허용 필드 | `steps` **만** |
| 수정 내용 | `steps`를 `null`로 설정 (또는 `{}`) |
| Diff 예상 규모 | ~20행 (현 steps dict 3 sub-key + 둘러싼 brace) → 1행 `null` 또는 `{}` |
| 금지 필드 | `text`, `choices`, `answer`, `solution`, `solution_svg`, `difficulty`, `q_type`, `tag`, `subject`, `quality`, 다른 레코드 — 전부 미수정 |
| commit 분리 | Commit A·B에 이은 **Commit C** (별도). 다른 cleanup과 묶지 않음 |
| commit message 제안 | `data: clean steps for 2010_2회_47` |
| 검증 (Commit C 적용 후) | 1. file diff 1개만 / 2. 레코드 1개만 / 3. 필드 `steps` 1개만 / 4. `answer=4`, `choices[3]="절연내력"`, `solution` 유지 / 5. `steps == null` 또는 `{}` / 6. 유도전동기 마커 0 hits / 7. JSON parse 정상, 5,331 records 유지 |
| 후속 evidence supplement | Commit A·B와 동등하게 supplement 문서 작성(pre/post snapshot + source label + scope) |

---

## 7. 수정하지 않을 경우 (defer/no_action) Caution 유지 영향

옵션 C·D 선택 시:

| 영역 | 영향 |
|---|---|
| 학습 패키지 docs | 영향 없음 — study set·day plan·learning log는 `steps`를 직접 노출 안 함 |
| 학습자 활용 (학습 패키지 기반) | 영향 없음 |
| 학습자 활용 (app에서 steps 직접 조회 시) | **잘못된 풀이 표시** — "유도 전동기의 전부하 회전수" 인식 문구 노출, 학습자 혼동 가능 |
| follow-up erratum clean count | 기기-18 caution 1/1 잔존, 완전 클린 전환 불가 |
| B-pilot 사용 가능 | 36/41 유지, 단 완전 클린은 34/39 유지 (35/40으로 늘지 않음) |
| 데이터 무결성 | 1 레코드 오염 지속, 추출 파이프라인 버그 증거가 본 레코드에 남음 |
| 잠재적 confusion | "answer=4 + solution=절연내력 + steps=유도전동기" 내적 모순 — 추후 다른 작업자가 혼란 |

→ defer는 학습 측 영향이 작지만 데이터 무결성·확장성 측면에서 비용이 누적.
no_action은 권장 안 함 — 오염 영구 silence는 추출 파이프라인 디버그 가치도 잃음.

---

## 8. 판정 + 다음 조치

### 판정: **proceed_minimal_cleanup** (옵션 A)

근거 요약:
- 옵션 B는 PDF에 없는 구조 생성 → G-1 위반 위험 (높음).
- 옵션 A는 정직한 schema 정정 → 추론 0, corpus 선례 있음, G-1 충족.
- 옵션 C는 학습 영향은 작으나 데이터 무결성 비용 누적.
- 옵션 D는 권장 불가.

### 다음 조치 (별도 명시 승인 후)

1. **Commit C 실행 권한 부여 요청** — `2010_2회_47.steps`를 `null`로 설정.
   commit message: `data: clean steps for 2010_2회_47`. 검증 7항 수행.
2. **Commit C evidence supplement** — Commit A·B와 동등한 G-1/G-2/G-3 보강.
3. **기기-18 redryrun (steps cleanup 후)** — caution → 완전 클린 전환 확인.
4. **follow-up erratum 갱신** — clean count: caution 2/2 → 1/1 (기기-17만 잔존),
   완전 클린 34/39 → 35/40.
5. **추출 파이프라인 회귀 트랙** (별도) — 인접 문항 혼입 재발 방지. 본 레코드의
   "변압기 문제가 아닌 유도 전동기 문제입니다" 자인 문구가 디버그 단서.

본 feasibility 승인 ≠ Commit C 데이터 수정 승인. plan §6.5와 동일 원칙: 단계별
별도 명시 승인 필요.

---

## 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. 현재 steps 필드 = 문제 48 혼입 확인 (3 sub-key 전부) | ✅ §1 — 130/556/190 chars 전수 인용 |
| 2. cleanup 옵션 비교 (A/B/C/D) | ✅ §5 — 표 + 권장 |
| 3. 스키마 형식 확인 (corpus-wide) | ✅ §2 — 5262 dict / 69 None / 300 empty / 4905 표준 3-key |
| 4. solution↔steps 관계 | ✅ §4 |
| 5. 수정 시 허용 범위 제안 (필드·diff·commit·검증) | ✅ §6 |
| 6. 수정하지 않을 경우 caution 유지 영향 | ✅ §7 |
| 판정 (proceed_minimal_cleanup / source_grounded_rewrite / defer / no_action) | ✅ §8 — **proceed_minimal_cleanup** |
| 본 단계 데이터·학습 패키지·closeout/errata 미수정 | ✅ docs/audit/ 신규 1건만 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps·학습 패키지 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- 기기-18 `2010_2회_47` `steps` 필드 cleanup feasibility/review 완료.
- 현재 steps 3 sub-key 전부 문제 48(유도전동기) 혼입 확인. "변압기 문제가 아닌
  유도 전동기 문제입니다" 자인 문구가 인식 단계 첫 문장으로 노출돼 있어 추출
  단계 mis-routing이 데이터에 증언으로 남음.
- corpus schema 분석: 5,262 dict / 69 None / 300 empty / 4,905 표준 `{인식, 변환,
  계산}`. **None은 인정된 schema 상태**.
- PDF 문제 47 풀이는 분류 단락이며 3 단계 schema에 자연 매핑되지 않음 — 옵션
  B(source-grounded rewrite)는 G-1 위반 위험.
- **판정: proceed_minimal_cleanup** — `steps`를 `null`로 설정. corpus 선례 있고
  G-1 충족, 학습 영향 0.
- 다음: Commit C 실행 권한 부여 요청 → evidence supplement → redryrun → followup
  erratum 갱신 (caution → 완전 클린 전환 확인).
- 이 문서는 feasibility/review다. 데이터·학습 패키지·closeout/errata 미수정.
