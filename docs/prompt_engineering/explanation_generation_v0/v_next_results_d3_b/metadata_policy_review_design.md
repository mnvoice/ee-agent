# Metadata Policy Review Design

> 2026-05-27 KST. Post-metadata-only audit push (`d8154a1`) 후속.
> 본 보고서는 **policy review 설계만** 작성. 실제 policy / selector 수정 / 26 audit execution / commit 0.

---

## 1. Metadata-only audit finding 요약

| 항목 | 값 |
|---|---|
| majority label | `metadata_misleading` (4/7) |
| misleading 4건 pid | 1998_4회_25 / 1999_4회_81 / 2005_3회_81 / 2007_1회_84 |
| dl_should_exist_candidate | 3 (가공전선 이격거리 item 영역 오부착) |
| 가공전선 이격거리 sample 3건의 실제 영역 | 안전율 (M3) / 지지물 시설기준 (M4) / 지선 시설기준 (M5) |

---

## 2. 원인 후보 분해 (5종)

| ID | 원인 | 근거 신호 | 가중치 추정 |
|---|---|---|---|
| **C1** | **policy definition issue** — essence/trap이 좁게 정의되어 다양성 미흡 | 가공전선 이격거리 essence "이격거리는 어떻게 정해지는가"가 안전율/지지물/지선 영역 미포괄 | **high** |
| **C2** | **selector matched_keyword broad match** | 가공전선 이격거리 26건 중 21건 (80.8%)이 matched_keyword=`가공전선`. M3/M4/M5 모두 `가공전선` kw. 단일 단어 `가공전선`은 매우 broad. | **high** |
| **C3** | **단일 item이 다양한 영역 포괄 — split 후보** | 가공전선 이격거리 item이 실제로는 이격거리 + 안전율/풍압 + 지지물 + 지선 + 기타 설비기준 동시 포괄 | **high** |
| C4 | data debt (답안/본문/OCR) | M2 답안 부정합 / M4 답안 부정합 / M6 OCR 깨짐 | medium |
| C5 | sample-only exception (모집단 정상) | 가공전선 이격거리 sample 3/3 misleading — 우연 확률 낮음 | low |

→ C1+C2+C3 동시 발현 가능성 강함. C4 부수적. C5는 26 모집단 audit으로 확인 가능.

---

## 3. 가공전선 이격거리 26건 전수 audit 설계

### 3.1 26건 명단

| matched_keyword | 건수 | 비중 |
|---|---:|---:|
| 가공전선 | **21** | 80.8% |
| 이격거리 | 3 | 11.5% |
| 가공지선 | 2 | 7.7% |

| input | pid | kw | year |
|---|---|---|---:|
| input_008.md | 1999_4회_81 | 가공전선 | 1999 |
| input_009.md | 1999_4회_84 | 가공전선 | 1999 |
| input_014.md | 2000_2회_86 | 이격거리 | 2000 |
| input_021.md | 2000_6회_92 | 가공전선 | 2000 |
| input_026.md | 2001_2회_82 | 가공전선 | 2001 |
| input_037.md | 2002_3회_85 | 가공전선 | 2002 |
| input_044.md | 2003_3회_81 | 가공전선 | 2003 |
| input_046.md | 2004_1회_84 | 이격거리 | 2004 |
| input_048.md | 2004_1회_91 | 가공전선 | 2004 |
| input_053.md | 2004_2회_86 | 이격거리 | 2004 |
| input_059.md | 2004_3회_83 | 가공전선 | 2004 |
| input_060.md | 2004_3회_92 | 가공전선 | 2004 |
| input_069.md | 2005_3회_81 | 가공전선 | 2005 |
| input_072.md | 2006_1회_29 | 가공지선 | 2006 |
| input_073.md | 2006_1회_85 | 가공전선 | 2006 |
| input_074.md | 2006_1회_86 | 가공전선 | 2006 |
| input_076.md | 2006_2회_83 | 가공전선 | 2006 |
| input_077.md | 2006_2회_86 | 가공전선 | 2006 |
| input_080.md | 2006_3회_81 | 가공전선 | 2006 |
| input_081.md | 2006_3회_83 | 가공전선 | 2006 |
| input_084.md | 2007_1회_81 | 가공전선 | 2007 |
| input_085.md | 2007_1회_82 | 가공전선 | 2007 |
| input_086.md | 2007_1회_84 | 가공전선 | 2007 |
| input_089.md | 2007_2회_27 | 가공지선 | 2007 |
| input_090.md | 2007_2회_81 | 가공전선 | 2007 |
| input_091.md | 2007_2회_82 | 가공전선 | 2007 |

### 3.2 Audit 절차

| step | 작업 |
|---:|---|
| 1 | 각 sample input.md read (question_text + solution + answer + choices) |
| 2 | question_text 영역 식별 — 무엇을 묻는가? |
| 3 | solution 영역 식별 — 풀이가 어떤 표/규정을 인용하는가? |
| 4 | 6 taxonomy (A/B/C/D/E/X) 중 1개 할당 |
| 5 | data debt 신호 (답안 mismatch / OCR / 본문 부재) 별도 X 마킹 |

### 3.3 산출

- 26 sample × (pid, kw, actual_category, data_debt_flag)
- kw별 카테고리 분포 (가공전선 21 / 이격거리 3 / 가공지선 2)
- year별 카테고리 분포 (시기 변화)
- policy issue 비율 정량화

---

## 4. 재분류 Taxonomy (6 카테고리)

| ID | label | 정의 |
|---|---|---|
| **A** | 실제 이격거리 | 가공전선 ↔ 다른 시설 (전차/광섬유/약전류/안테나/식물/통신) 간 안전 이격거리 수치 / 기준 |
| **B** | 안전율 / 풍압 하중 | 지지물 안전율, 풍압 하중, 강도 규정 |
| **C** | 지지물 시설기준 | 지지물 분기, 발판 볼트, 시설 위치, 종류 등 |
| **D** | 지선 / 지지선 시설기준 | 지선 안전율, 소선 가닥수, 지름, 도로 횡단 높이 등 |
| **E** | 기타 가공전선 설비기준 | 가공지선/접지, 시설 가능 여부, 일반 기준 등 (A-D 외) |
| **X** | data debt | 답안 부정합 / OCR 깨짐 / 본문 부재 / 원문 자체 부족 |

X는 A-E와 동시 표시 가능 (예: A+X = 이격거리 영역인데 답안 부정합).

---

## 5. 판정 Rubric

| boundary 규칙 |
|---|
| 이격거리 수치 (저압/고압/특고압 별 m 단위) → **A** |
| 안전율 (1.2 / 1.3 / 1.5 / 2.5 / 풍압 하중) → **B** |
| 지지물 분기 / 발판 볼트 / 시설 위치 / 종류 → **C** |
| 지선 소선 가닥수 / 지름 / 안전율 / 횡단 높이 → **D** |
| 가공지선 / 접지 / 일반 가능 여부 / A-D 외 → **E** |
| 답안 부정합 / OCR / 본문 부재 → **X** 동시 표시 (A-E 1개 + X) |

각 sample에 (A-E 1개, X 여부) 부여.

---

## 6. Item Split 후보 (5종)

audit execution 후 카테고리 분포 측정 후만 결정.

| 새 item | scope | essence 제안 |
|---|---|---|
| 가공전선 이격거리 (기존 유지) | A. 실제 이격거리 | "가공전선과 다른 시설간 안전 이격거리는 어떻게 정해지는가" |
| 가공전선 안전율 / 풍압 | B. 안전율 / 풍압 하중 | "가공전선 지지물의 안전율과 풍압 하중 기준은 어떻게 결정되는가" |
| 가공전선 지지물 시설 | C. 지지물 시설기준 | "가공전선로 지지물 시설기준 (분기/발판/위치)이 어떻게 정해지는가" |
| 가공전선 지선 시설 | D. 지선 / 지지선 시설기준 | "가공전선 지선의 소선/안전율/높이 기준이 어떻게 정해지는가" |
| 가공전선 기타 설비기준 | E. 기타 | "가공전선 일반 설비기준 (가공지선/접지 등)이 어떻게 정해지는가" |

**Split 결정 threshold**: 각 split 후보가 audit 결과 ≥ 3건 모집단 보유 시에만 split 권장. 1-2건은 'E. 기타'에 통합. 실제 split 적용 0 — 본 design 단계는 후보만 명세.

---

## 7. Selector Keyword Integrity 확인 방법

`scripts/v_next_d3_pre_preview.py:237-247` keywords 7개 (가공전선/이격거리/가공지선/접지선/안테나/약전류전선/식물 이격)의 broad match 정도 측정.

### 7.1 측정 절차

| step | 작업 |
|---:|---|
| 1 | ITEM_POLICY keywords 7개 list 확보 |
| 2 | 26 sample audit 결과 (카테고리 A-X)와 matched_keyword (가공전선 21 / 이격거리 3 / 가공지선 2) cross-tab 작성 |
| 3 | 각 keyword별 카테고리 적중률 측정 |
| 4 | broad keyword 식별 (`가공전선` 등 단일 단어가 의미 영역과 무관한 매칭 유발 시 broad) |
| 5 | narrow keyword 후보 design (예: `가공전선` → `가공전선 이격거리` / `가공전선 시설기준` / `가공전선 보호` 등 multi-word) |

### 7.2 예상 산출

- keyword × category 2D 표 (3 keywords × 6 categories)
- 각 keyword 적중률 (가설: `이격거리` kw → A 100%, `가공전선` kw → A/B/C/D/E 분산)
- narrow keyword design 후보 list

코드 수정 0 — 측정 + design만.

---

## 8. Data Debt 분리 기준

policy issue ↔ data debt 분리.

### 8.1 Data debt 신호 (4종)

| signal | detection |
|---|---|
| 답안 부정합 | input answer 필드 vs solution 본문 정답 표시 불일치 |
| 본문 부재 | device_or_concept = "문제 데이터 부재" 또는 짧은 placeholder |
| OCR 깨짐 | choices에 비표준 단어 (예: "리률로지", "써지널라이저", "읍선수지게" 등) |
| 원문 자체 부족 | questions.json에 해당 pid의 raw solution 자체 비어 있음 |

### 8.2 분리 룰

| 작업 | 방법 |
|---|---|
| data debt 신호 발견 sample | 카테고리 (A-E) + X 동시 표시 |
| policy issue 측정 | data debt 별도 영역으로 분리하여 X 제외 N건 기반 policy issue 비율 산출 |

### 8.3 출력 형식

26 sample table에 두 컬럼:
- `actual_category` (A-E)
- `data_debt_flag` (X 여부)

---

## 9. 다음 Execution Gate 조건

| # | 조건 |
|---:|---|
| 1 | 26 sample 전수 read + 카테고리 분류 완료 |
| 2 | kw × category cross-tab 작성 |
| 3 | data debt 분리 측정 완료 |
| 4 | item split 후보 (split 권장 / 통합 권장) 결정 design |
| 5 | selector keyword integrity 결과 design |
| 6 | 최종 다음 게이트 추천 (policy 수정 design / selector 수정 design / data debt audit / split 적용 등) |

본 design 단계에서는 step 1-6 모두 수행 0. 권장 절차만 명세.

---

## 10. claim boundary 점검

| claim | 본 design 상태 |
|---|---|
| 26 sample 명단 + taxonomy + rubric + split 후보 + selector integrity + data debt 분리 design | (a) 명세 |
| NNN 기반 deterministic 매핑 가능 | (a) 검증 |
| Metadata-only audit signal (이전 게이트) | (a) 이미 확정 |
| **policy 실제 수정** | **0** (review 영역만 식별) |
| **selector 코드 수정** | **0** |
| **26 전체 분류 결과** | **0** (execution 게이트 영역) |
| **item split 적용** | **0** (audit 결과 후 결정) |
| **catalog/gap rescue 결정** | **0** |
| **D-4 / A1c** | **0** (별 게이트) |
| **generation / audit 재실행** | **0** |

---

## 11. 보호 영역 매트릭스 (전부 미수정 / 0)

`scripts/explanation_synthesizer.py` ✓ / `scripts/v_next_d3_pre_preview.py` ✓ / `scripts/v_next_d3_selector.py` ✓ / `scripts/v_next_d3_input_creator.py` ✓ / `scripts/v_next_d3_parser_validator.py` ✓ / `scripts/v2_input_parser.py` ✓ / `app/data/questions.json` ✓ / D-2 sealed assets ✓ / v_full handoff scope ✓ / policy 실제 수정 0 ✓ / selector 수정 0 ✓ / generation 재실행 0 ✓ / audit 재실행 0 ✓ / catalog/gap/reuse 0 ✓ / D-4 0 ✓ / commit 0 ✓ / DEVLOG / Vault / MEMORY / decision JSONL 작성 0 ✓.

---

## 12. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_b/metadata_policy_review_design.md` | 본 design 보고서 (12 섹션) |
| `v_next_results_d3_b/metadata_policy_review_design.json` | machine-readable — finding / 원인 분해 / 26 sample / taxonomy / rubric / split 후보 / selector method / data debt 분리 / execution 조건 |

---

## 13. 최종 상태 판정

**판정**: `READY_FOR_METADATA_POLICY_REVIEW_EXECUTION_GATE`

근거:
- ✓ 26 sample 전수 명단 확보 (kw 분포 가공전선 21 / 이격거리 3 / 가공지선 2)
- ✓ Taxonomy 6종 (A-E + X) 정의
- ✓ Judgment rubric 5 step + 6 boundary 규칙
- ✓ Item split 5 candidate design (split decision threshold ≥ 3건)
- ✓ Selector keyword integrity 5 step method
- ✓ Data debt 4 signal + separation rule
- ✓ 5 원인 분해 (C1-C5) 가중치 추정
- ✓ Execution 단계 6 조건 명세
- ✓ `NEEDS_POLICY_REVIEW_DESIGN_FIX` / `BLOCKED_BY_MISSING_MANIFEST_MAPPING` 미해당

다음 단계 (26 sample read + 카테고리 분류 + cross-tab + split 결정 + 다음 게이트 추천) 진입은 사용자 명시 영역.

---

End of metadata policy review design (design only) report.
