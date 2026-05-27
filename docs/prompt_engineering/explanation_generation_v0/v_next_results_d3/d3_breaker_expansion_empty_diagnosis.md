# D-3 Breaker Unexpected Expansion-Empty Diagnosis (Read-Only)

> 2026-05-27 KST. D-3 paired audit 후속 read-only 진단.
> 본 보고서는 13건 차단기 unexpected expansion-empty의 원인을 4 후보(A/B/A+B/C)로 좁힘. patch / generation / semantic gain / P5 / D-4 / commit claim 0.

---

## 0. 핵심 한 줄 결론

**A+B 결합 가장 유력** (A keyword map 누락 + B dl 표현 substring 매칭 단절). C 정책 정상 empty 배제 (S/Fault는 expansion 허용, 같은 slot의 다른 item 14건 dl_keyword 성공).

---

## 1. 13건 전체 명단 (5축 일점 집중 재확인)

전부 동일 5축:

| 축 | 값 |
|---|---|
| audit_group | expansion |
| slot_grp | 전력_보호고장S |
| item | 차단기 |
| matched_keyword | 차단기 |
| enriched_dynamic_link | `전력 차단기 -> 회로 단락전류 / 임피던스 환산` |

| input | pid |
|---|---|
| input_003.md | 1998_4회_22 |
| input_012.md | 2000_2회_23 |
| input_029.md | 2001_3회_81 |
| input_030.md | 2002_1회_22 |
| input_035.md | 2002_3회_26 |
| input_040.md | 2003_1회_23 |
| input_041.md | 2003_1회_27 |
| input_047.md | 2004_1회_90 |
| input_056.md | 2004_3회_27 |
| input_057.md | 2004_3회_29 |
| input_058.md | 2004_3회_82 |
| input_063.md | 2005_1회_29 |
| input_092.md | 2008_1회_23 |

---

## 2. 대표 input/output evidence (실패 3건)

전부 동일 메타 (대표 3건):

| 항목 | input_003 / output_003 | input_012 / output_012 | input_092 / output_092 |
|---|---|---|---|
| pid | 1998_4회_22 | 2000_2회_23 | 2008_1회_23 |
| matched_core_name | 차단기 | 차단기 | 차단기 |
| phen_origin | S/Fault | S/Fault | S/Fault |
| dynamic_link | 전력 차단기 -> 회로 단락전류 / 임피던스 환산 | (동일) | (동일) |
| input 내 cross_subject_hints | 없음 | 없음 | 없음 |
| output.cross_subject_expansion.expands_to | `[]` | `[]` | `[]` |
| uncertainty_flags | `[]` | `[]` | `[]` |

→ 3건 모두 cross_subject_hints 없음 + dl_keyword 매칭 실패 + matched_core_fallback 실패 → empty.

---

## 3. 성공 비교군 evidence (같은 slot_grp / 같은 phen_origin S/Fault)

| input | pid | item | dl | expands_to 결과 | hit keyword |
|---|---|---|---|---|---|
| input_018.md | 2000_6회_27 | 단락전류·임피던스 | `전력 단락전류 -> 회로 옴의 법칙 -> 회로 임피던스 환산` | 회로이론 1건 (`회로 임피던스 환산 경로`) | `회로 임피던스` (line 142) — `회로 임피던스 환산` 안에 연속 substring |
| input_013.md | 2000_2회_85 | 보호계전기·피뢰기 | `전력 보호계전기/피뢰기 -> 설비 절연/보호 -> 회로 임피던스` | 전기설비기술기준 1건 + 회로이론 1건 | `보호계전기` (line 132), `회로 임피던스` (line 142) |
| input_007.md | 1999_3회_23 | 지락·중성점 접지 | `전력 중성점 접지 -> 회로 대칭분 해석` | 전기설비기술기준 1건 + 회로이론 1건 | `접지` (line 128), `회로 대칭분` (line 140) |

→ 같은 slot_grp의 S/Fault 14건(6+4+4)는 dl 안에 `CROSS_TARGET_KEYWORDS`의 키가 **연속 substring**으로 포함되어 있어 매칭 성공.

---

## 4. Generator keyword map hit/miss 분석

### 4.1 매칭 룰 (read-only `scripts/explanation_synthesizer.py:186-251`)

`parse_dynamic_link`:

1. Path 1 (`cross_subject_hints`): input에 명시 hints → 우선 사용. 차단기 input에는 없음.
2. Path 2 (`dl_keyword scan`): `for kw, tgt in CROSS_TARGET_KEYWORDS: if kw in dl and tgt != primary_subject ...` — **substring 매칭**.
3. Path 3 (`matched_core_name fallback`): `phen_origin in ("D/Dynamic", "S/Fault", "S/Conversion")` 이고 `matched_core_name in MATCHED_CORE_FALLBACK` → 매핑.
4. 모두 실패 → `return expansions, "empty"`.

### 4.2 차단기 dl 매칭 시도 표

dl = `전력 차단기 -> 회로 단락전류 / 임피던스 환산`

| 후보 keyword | `CROSS_TARGET_KEYWORDS`에 존재? | dl 내 substring? | 결과 |
|---|---|---|---|
| `차단기` | **NO** | yes | map entry 없음 |
| `단락전류` | **NO** | yes | map entry 없음 |
| `회로 단락전류` | **NO** | yes | map entry 없음 |
| `임피던스 환산` | **NO** | yes | map entry 없음 |
| `회로 임피던스` | **YES (line 142, 회로이론)** | **NO** | dl 텍스트가 `회로 단락전류 / 임피던스` 사이에 `단락전류 /` 위치 — `회로 임피던스` 연속 substring 안 됨 |
| `전력 보호` | YES (line 114, 전력공학) | NO | dl head는 `전력 차단기`, `전력 보호` 아님 |

### 4.3 matched_core_fallback 시도

- matched_core_name = `차단기`
- `MATCHED_CORE_FALLBACK` keys (line 150-174): 전자파, 맥스웰 방정식, 변위전류, 전자유도, 유기기전력, 히스테리시스, 표피효과, 로렌츠/플레밍 힘, 고유 임피던스, 직선도체 자계, 자속밀도, 자기회로·인덕턴스, 유전체 경계조건, 라플라스 변환, 라플라스 역변환, R-L-C 과도현상, z변환, 전달함수, 안정도 판별
- → **`차단기` 없음**. Path 3도 실패.

### 4.4 S/Fault 자체는 expansion 허용 (질문 5 답)

`scripts/explanation_synthesizer.py:237`:
```
if phen_origin in ("D/Dynamic", "S/Fault", "S/Conversion"):
```
S/Fault는 fallback 허용 대상. 같은 slot_grp의 S/Fault 14건이 dl_keyword path로 성공한 사실 자체가 정책 허용 증거.

---

## 5. 4 후보 평가

| 후보 | 판정 | 근거 |
|---|---|---|
| **A. generator keyword map 누락** | **지지** | `CROSS_TARGET_KEYWORDS`에 `차단기`, `단락전류`, `회로 단락전류`, `임피던스 환산` 모두 없음. `MATCHED_CORE_FALLBACK`에 `차단기` 없음. |
| **B. dl 표현 문제** | **지지** | 기존 키 `회로 임피던스`는 성공 비교군 (output_018, output_013)에서 연속 substring으로 매칭됨. 차단기 dl `회로 단락전류 / 임피던스 환산`은 `단락전류 /`가 `회로`와 `임피던스` 사이에 위치하여 substring 단절. |
| **A+B 결합** | **가장 유력** | A와 B가 동시에 성립. A 단독 또는 B 단독으로는 13건 전부 실패 설명 불가 (한 path만 살아 있어도 dl_keyword 부착 가능). |
| **C. 정책상 정상 empty** | **배제** | S/Fault는 fallback 허용 대상 (line 237). 같은 slot의 다른 S/Fault item 14건 성공. 차단기는 회로 단락전류 / 회로 임피던스 환산으로 자연스럽게 연결되는 영역이므로 정책상 expansion 차단 의도 없음. |

### 5.1 A 단독 가설이 부족한 이유

A 단독이라면 dl 자체가 다른 형태로 포함되어 있어도 매칭 실패. 그러나 dl의 마지막 segment가 만약 `회로 임피던스 환산`이라면 (성공 비교군 output_018 패턴) 기존 키 `회로 임피던스`가 substring으로 hit 가능했을 것. 즉 키 신규 추가 없이도 dl 표현 보정만으로 매칭 가능.

### 5.2 B 단독 가설이 부족한 이유

B 단독으로 dl 표현을 `회로 임피던스 환산` 형태로 보정하면 1 target (회로이론)은 매칭. 그러나 `차단기` 자체가 다른 도메인(전기설비기술기준 / 전기기기)으로 cross-mapping 되어야 할 의도가 있다면 (보호계전기처럼 multi-target), keyword map 자체 추가 필요. 따라서 B 단독은 1 target은 회복하지만 의도된 multi-target 회복은 부족할 가능성.

### 5.3 A+B 결합이 가장 유력한 이유

- A: `차단기` 키를 `MATCHED_CORE_FALLBACK` 또는 `CROSS_TARGET_KEYWORDS`에 추가하면 Path 3 (fallback) 또는 Path 2 (직접 hit)로 회복 가능.
- B: dl을 `회로 단락전류 환산 + 회로 임피던스 환산` 형태로 보정하면 Path 2 (`회로 임피던스` substring hit)로 회복 가능.
- 양자가 동시에 작동하면 cross-subject expansion이 회로이론 1건 + (잠재적) 다른 도메인 1건으로 multi-target 발현 가능.

A와 B를 배타로 보지 않은 사용자의 가설 보정이 정확.

---

## 6. claim boundary 점검

| claim | 본 보고서 상태 |
|---|---|
| 13건 차단기 dl_keyword path 미발현 측정 | (a) 측정 — 3건 직접 확인 + generator 코드 (line 186-251) 직접 read |
| 같은 slot 14건 S/Fault dl_keyword 성공 측정 | (a) 측정 — output_018, output_013, output_007 직접 확인 |
| S/Fault expansion 허용 정책 | (a) 측정 — `scripts/explanation_synthesizer.py:237` 직접 read |
| A+B 결합 가장 유력 | (a) 판정 — 4 후보 각 path 트레이스 후 결론. 단독 가설 부족 이유 명시. |
| 13건 차단기 patch (어떤 키를 어떻게 추가) | **claim 0** — 다음 게이트 design 영역 |
| dl 보정안 (어떤 표현으로 정규화) | **claim 0** — 다음 게이트 design 영역 |
| 차단기 13건 후 추가 입력 매핑 결과 | **claim 0** — 다음 게이트 generation 영역 |
| semantic gain (차단기 expansion 회복 시 학습 가치) | **claim 0** |
| P5 sample experiment 필요 | **claim 0** |
| D-4 진입 필요 | **claim 0** |

---

## 7. 다음 게이트 후보 (사용자 명시 영역, claim 0)

4 후보. 본 보고서는 patch/generation 0.

| 후보 | scope | 의존 |
|---|---|---|
| 후보 1: narrow keyword map patch design | `CROSS_TARGET_KEYWORDS`에 `차단기` (target 후보: 회로이론 + 전기설비기술기준 또는 전기기기) 또는 `MATCHED_CORE_FALLBACK`에 `차단기` key 추가 design. **단** 실제 patch 0. | 사용자 명시 게이트 |
| 후보 2: dynamic_link 표현 보정 design | D-3 ITEM_POLICY 차단기 dl을 `회로 임피던스` 연속 substring을 보존하는 형태로 정규화 design (예: `-> 회로 단락전류 환산 -> 회로 임피던스 환산`). **단** 실제 patch 0. | 사용자 명시 게이트 |
| 후보 3: 차단기 policy 재분류 design | 차단기 13건을 `audit_group=expansion`에서 `non_expansion_metadata`로 재분류 design. **단** S/Fault + 회로 단락전류 / 회로 임피던스 환산 자연 연결 영역이라는 점에서 의미 부적합 가능성. | 사용자 명시 게이트 |
| 후보 4: semantic sampling (P5) | 13건 중 3-5건과 v_full pair를 사람 sampling 비교. 본 진단의 4 후보 판정이 사람 readability와 정합하는지 확인. | 사용자 명시 게이트 |

본 보고서는 후보 1/2 결합 design (A+B 동시 보정)이 가장 유력 후보로 봄. 단 design 자체 진입은 별 게이트.

---

## 8. 보호 영역 매트릭스 (전부 미수정 / 0)

| 보호 대상 | 상태 |
|---|---|
| `scripts/explanation_synthesizer.py` | read-only, 미수정 ✓ |
| `scripts/v2_input_parser.py` | 미수정 ✓ |
| `app/data/questions.json` | 미수정 ✓ |
| D-2 sealed assets | 미수정 ✓ |
| v_full handoff scope | 미수정 ✓ |
| D-3 generation 재실행 | 0 ✓ |
| D-3 audit 재실행 | 0 ✓ |
| P5 patch | 0 ✓ |
| P5 sample experiment | 0 ✓ |
| D-4 진입 | 0 ✓ |
| catalog/gap rescue | 0 ✓ |
| keyword map 실제 추가 | 0 ✓ |
| dl 실제 정규화 | 0 ✓ |
| commit | 0 ✓ |

---

## 9. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3/d3_breaker_expansion_empty_diagnosis.md` | 본 보고서 |
| `v_next_results_d3/d3_breaker_expansion_empty_diagnosis.json` | 13건 5축 일점 집중 + 3건 실패 evidence + 3건 성공 비교군 evidence + keyword hit/miss 표 + 4 후보 판정 (machine-readable) |

---

## 10. 최종 판정

**원인 후보 좁힘**: **A+B 결합 가장 유력**.

- A: `CROSS_TARGET_KEYWORDS` + `MATCHED_CORE_FALLBACK` 양자에 `차단기` 또는 관련 키 부재.
- B: 차단기 dl `회로 단락전류 / 임피던스 환산`이 기존 키 `회로 임피던스`의 연속 substring 매칭을 단절.
- C 배제: S/Fault는 expansion 허용 + 같은 slot 14건 성공.

**상태**: `READY_FOR_BREAKER_PATCH_DESIGN_BRANCH_DECISION`

다음 결정은 사용자 명시 게이트 (후보 1+2 결합 design / 후보 1 단독 / 후보 2 단독 / 후보 3 / 후보 4) 영역.

---

End of D-3 breaker unexpected expansion-empty diagnosis report.
