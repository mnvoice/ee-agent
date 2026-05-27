# Metadata-Only Audit Execution Report (7-sample signal)

> 2026-05-27 KST. Post-P5 result push (`be4f7f0`) 후속.
> 본 보고서는 **7 sample 기준 metadata-only signal 측정**. non_expansion_metadata 37 전체 / dl-null 정책 전체 success / catalog-gap rescue / D-4 필요 claim 모두 0.

---

## 0. 핵심 한 줄 결론

**`METADATA_POLICY_REVIEW_CANDIDATE`** (1순위) + `CATALOG_OR_POLICY_REVIEW_CANDIDATE` (2순위).

- 7 sample 중 4건 `metadata_misleading` (majority)
- 가공전선 이격거리 item sample 3건 (M3/M4/M5) 모두 실제로는 이격거리가 아닌 **안전율 / 지지물 시설기준 / 지선 시설기준** 영역 — item-매칭 정합성 문제
- axis_means: essence_captures_core 2.21 / trap_alignment 2.14 / trap_type_distractor_utility 1.71 모두 낮음
- expansion_absence_safety 3.57만 평균 3 이상 (dl 없는 것이 안전한 부분은 정직)

---

## 1. Sample별 핵심 관찰

### M1: input_005 (1998_4회_25, 부하율·수용률·부등률)

| 항목 | 내용 |
|---|---|
| 실제 문제 | 변전소 최대 전력 계산 (부등률 1.17 → 4598 kW). **계산 문제** |
| essence | "부하율/수용률/부등률을 어떻게 구분해 외우는가" — **정의 외우기** 영역 |
| trap | "부하율 vs 수용률 vs 부등률 정의 혼동 함정" — **정의 혼동** |
| 핵심 관찰 | essence + trap이 본 문제(계산)와 mismatch. 단 계산에 부등률 정의 이해가 전제이므로 부분 정합. |

### M2: input_075 (2006_2회_26, 역률 개선)

| 항목 | 내용 |
|---|---|
| 실제 문제 | 콘덴서 설치 후 합성 역률 계산 |
| essence | "역률 개선 콘덴서 용량을 어떻게 계산하는가" |
| trap | "Qc 공식 sin / cos 혼동 함정" |
| 핵심 관찰 | essence는 콘덴서 용량 계산, 본 문제는 합성 역률 계산 — 부분 어긋남. trap sin/cos 혼동은 본 풀이와 관련. **데이터 부정합**: input answer=2 (0.86), 풀이는 (3) 0.89 정답이라 표기. |

### M3: input_008 (1999_4회_81, "가공전선 이격거리")

| 항목 | 내용 |
|---|---|
| 실제 문제 | 목주 풍압 하중 **안전율 1.3** |
| essence | "가공전선과 다른 시설간 안전 이격거리는 어떻게 정해지는가" |
| trap | "전선 종류별 이격거리 표 혼동 함정" |
| 핵심 관찰 | **이격거리가 아닌 안전율 영역**. matched_keyword "가공전선"이 broad 매칭이라 영역 오부착. essence + trap이 본 문제와 완전 다름. |

### M4: input_069 (2005_3회_81, "가공전선 이격거리")

| 항목 | 내용 |
|---|---|
| 실제 문제 | 가공전선 지지물 시설기준 (옳지 않은 것) |
| essence | (M3 동일) |
| trap | (M3 동일) |
| 핵심 관찰 | **이격거리가 아닌 지지물 시설기준** 영역. 답안 부정합 (input answer=1, 풀이는 (3)이 틀리다고 표기). |

### M5: input_086 (2007_1회_84, "가공전선 이격거리")

| 항목 | 내용 |
|---|---|
| 실제 문제 | 지선(가공전선로 지지물) 시설기준 |
| essence | (M3 동일) |
| trap | (M3 동일) |
| 핵심 관찰 | **이격거리가 아닌 지선 시설기준** 영역. M3/M4/M5는 모두 "가공전선 이격거리" item으로 매칭됨에도 불구하고 실제는 안전율 / 지지물 / 지선 — **item-매칭 정합성 문제**. |

### M6: input_045 (2004_1회_30, 가공전선로 경간·이도)

| 항목 | 내용 |
|---|---|
| 실제 문제 | 이도(Dip) 설명 옳은 것 — 이도 개념 정합 |
| essence | "전선 장력·이도·경간이 어떻게 작용하는가" |
| trap | "경간 vs 이도 관계 혼동 함정" |
| 핵심 관찰 | essence + trap 정합. 단 choices [구분점수/리률로지/써지널라이저/구분개폐기]는 OCR 깨진 영역 (data debt). 답안 부정합 (input answer=4, 풀이 (3) 정답). |

### M7: input_020 (2000_6회_85, 절연내력 / 유도장해)

| 항목 | 내용 |
|---|---|
| 실제 문제 | 22.9kV 다중접지 절연내력 시험전압 배율 0.92 |
| essence | "절연내력 시험전압과 유도장해 경감이 어떻게 작용하는가" |
| trap | "절연내력 시험전압 배율 / 유도장해 경감대책 혼동 함정" |
| 핵심 관찰 | essence + trap 정합 (시험전압 배율 표 영역). 본 문제는 유도장해가 아닌 절연내력 영역이라 essence 후반은 본 문제와 무관, 단 정직. |

---

## 2. Sample별 6-axis 점수

| Sample | essence | trap_align | trap_type_util | dl_null_honest | exp_absence_safe | overload_risk | Label |
|---|---:|---:|---:|---:|---:|---:|---|
| M1 (부하율·부등률) | 2 | 2 | 2 | 3 | 4 | 2 | metadata_misleading |
| M2 (역률 개선) | 2.5 | 3 | 2 | 3 | 4 | 2 | metadata_neutral |
| M3 (이격거리→안전율) | 1 | 1 | 1 | 2 | 3 | 4 | metadata_misleading |
| M4 (이격거리→지지물) | 1 | 1 | 1 | 2 | 3 | 4 | metadata_misleading |
| M5 (이격거리→지선) | 1 | 1 | 1 | 2 | 3 | 4 | metadata_misleading |
| M6 (경간·이도) | 4 | 3 | 2 | 4 | 4 | 2 | metadata_helpful |
| M7 (절연내력) | 4 | 4 | 3 | 4 | 4 | 2 | metadata_helpful |
| **평균** | **2.21** | **2.14** | **1.71** | **2.86** | **3.57** | **2.86** | |

---

## 3. Sample별 Label + Diagnostic Signal

| Sample | Label | Diagnostic Signal |
|---|---|---|
| M1 | `metadata_misleading` | `misleading_present` |
| M2 | `metadata_neutral` | (none) |
| M3 | `metadata_misleading` | `misleading_present`, `dl_should_exist_candidate` |
| M4 | `metadata_misleading` | `misleading_present`, `dl_should_exist_candidate` |
| M5 | `metadata_misleading` | `misleading_present`, `dl_should_exist_candidate` |
| M6 | `metadata_helpful` | (none) |
| M7 | `metadata_helpful` | (none) |

---

## 4. Group Aggregate

| Label | Count |
|---|---:|
| metadata_helpful | 2 (M6, M7) |
| metadata_neutral | 1 (M2) |
| **metadata_misleading** | **4** (M1, M3, M4, M5) |
| needs_human_review | 0 |
| **majority** | **metadata_misleading** |

| Diagnostic | Count |
|---|---:|
| `misleading_present` | 4 |
| `dl_should_exist_candidate` | 3 (M3, M4, M5 — 전부 가공전선 이격거리 item이 안전율/지지물/지선 영역) |

---

## 5. dl_should_exist 후보 여부

**예** — 3 sample 발현:

| pid | item (현재) | 실제 영역 | dl 후보 추정 |
|---|---|---|---|
| 1999_4회_81 (M3) | 가공전선 이격거리 | 안전율 (목주 풍압 하중) | "전력 안전율 / 풍압 하중 -> 설비 강도 규정 / 안전율 표" |
| 2005_3회_81 (M4) | 가공전선 이격거리 | 지지물 시설기준 | "전력 지지물 시설 -> 설비 기준 규정" |
| 2007_1회_84 (M5) | 가공전선 이격거리 | 지선 시설기준 | "전력 지선 시설 -> 설비 강도 / 안전율" |

→ 핵심: 본 finding은 sample 3건 기반. 단 3/3 패턴은 가공전선 이격거리 모집단 26건 (70.3%) 전체에 대한 정밀 audit 후보의 강한 신호.

---

## 6. metadata_misleading 여부

**4건 발현** (M1, M3, M4, M5).

핵심 패턴:
- **M1**: essence 영역 ↔ 실제 문제 영역 mismatch (정의 외우기 vs 계산)
- **M3 / M4 / M5**: matched_keyword broad 매칭 + item 영역 오부착 (가공전선 → 이격거리만 매칭하는데 실제는 안전율/지지물/지선)

→ 두 차원 동시 발현: (1) essence policy 영역 자체 vs 문제 영역 mismatch + (2) selector matched_keyword 정합성.

---

## 7. 5 Pathway 매핑

| 조건 | 매칭 | 다음 상태 |
|---|---|---|
| majority `metadata_misleading` (4/7) | ✓ | **`metadata_policy_review_candidate`** |
| `dl_should_exist` 의심 발생 (M3/M4/M5 axis 4 ≤ 2) | ✓ | **`catalog_or_policy_review_candidate`** |
| majority `metadata_helpful` | 미해당 | n/a |
| majority `metadata_neutral` | 미해당 | n/a |
| majority `needs_human_review` | 미해당 | n/a |

→ 2 pathway 동시 매칭 (primary + secondary).

---

## 8. 다음 게이트 추천 (우선순위)

| # | 후보 | scope |
|---:|---|---|
| 1 | **metadata_policy_review** | essence/trap 정의 영역 + selector matched_keyword broad 매칭의 정합성 검토 별 게이트 |
| 2 | **item_matching_integrity_audit** | 가공전선 이격거리 26건 영역 분리 audit — 실제 이격거리 vs 안전율/지지물/지선 분류 |
| 3 | questions_json_data_debt_audit | 답안 부정합 + OCR 깨짐 sample (M2 / M4 / M6) — 모집단 확대 audit |
| 4 | 본 보고서 commit + push | 결과 정착 별 사용자 명시 영역 |
| 5 | D-4 진입 | 본 결과와 독립 별 영역 |

### 본 채널 권장 (§1.4 책임 — 단일 선택)

본 게이트 다음 즉시 진입은 **후보 4 (본 보고서 commit + push)**.
- 본 P5 결과 (B_better) ↔ metadata-only audit 결과 (misleading) 의 비교 결과가 대비된 신호. 영구 보존 우선.
- 그 후 후보 1 (metadata_policy_review) 또는 후보 2 (item_matching_integrity_audit) 사용자 명시 선택.

---

## 9. Claim Boundary 점검

| claim | 본 audit 상태 |
|---|---|
| majority `metadata_misleading` (4/7) | (a) 측정 — 7 sample 한정 |
| 가공전선 이격거리 3/3 영역 오부착 | (a) 측정 — sample 한정 |
| axis_means 6 dimension | (a) 측정 |
| `dl_should_exist_candidate` 3건 발현 | (a) 측정 |
| **non_expansion_metadata 37 전체 품질 확정** | **0** |
| **dl-null 정책 전체 성공 claim** | **0** |
| **가공전선 이격거리 26 전체 영역 오부착 claim** | **0** (sample 3건 기반, 26 전체 확정 별 audit 필요) |
| **catalog/gap rescue 결정** | **0** |
| **D-4 필요 claim** | **0** |
| **A1c 추가 / patch 재검토 결정** | **0** |
| **metadata policy 실제 수정** | **0** (review 영역만 식별, 수정 별 게이트) |

---

## 10. 보호 영역 매트릭스 (전부 미수정 / 0)

`scripts/explanation_synthesizer.py` ✓ / `scripts/v_next_d3_pre_preview.py` ✓ / `scripts/v_next_d3_selector.py` ✓ / `scripts/v_next_d3_input_creator.py` ✓ / `scripts/v_next_d3_parser_validator.py` ✓ / `scripts/v2_input_parser.py` ✓ / `app/data/questions.json` ✓ / D-2 sealed assets ✓ / v_full handoff scope ✓ / A1c keyword 추가 0 ✓ / D-3 재생성 0 ✓ / audit 재실행 0 ✓ / P5 재실행 0 ✓ / D-4 0 ✓ / catalog/gap/reuse 0 ✓ / commit 0 ✓ / DEVLOG / Vault / MEMORY / decision JSONL 작성 0 ✓.

---

## 11. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_b/metadata_only_audit_execution_report.md` | 본 보고서 (11 섹션) |
| `v_next_results_d3_b/metadata_only_audit_execution_report.json` | machine-readable — 7 sample / rubric / label / diagnostic / aggregate / pathway / 다음 게이트 |

---

## 12. 최종 상태 판정

**판정 (primary)**: `METADATA_POLICY_REVIEW_CANDIDATE`
**판정 (secondary)**: `CATALOG_OR_POLICY_REVIEW_CANDIDATE`

### 판정 근거

| 검증 기준 | 결과 |
|---|---|
| majority `metadata_misleading` (4/7) | ✓ |
| `misleading_present` Diagnostic 4건 | ✓ |
| `dl_should_exist_candidate` Diagnostic 3건 (M3/M4/M5) | ✓ |
| axis_means: essence/trap_align/trap_type_util 모두 2 미만~중간 | ✓ |
| expansion_absence_safety 평균 3.57 (단독 평균 3 이상) | dl 없는 것이 안전한 부분만 정직 |
| metadata_overload_risk 평균 2.86 (낮음 영역) | ✓ |

### 대안 옵션 (미해당)

- `METADATA_ONLY_VALUE_SUPPORTED`: 미해당 — majority helpful 아님 (2건만)
- `METADATA_SURFACE_ONLY`: 미해당 — majority neutral 아님 (1건만)
- `METADATA_ONLY_NEEDS_HUMAN_REVIEW`: 미해당 — needs_human_review 0건

### P5 결과와의 대비

| audit | 차단기 / 비차단기 / non_expansion | 신호 |
|---|---|---|
| P5 (12 sample) | 차단기 B_better 3 / same 1 / NHR 1 / 비차단기 same 4 / non_expansion same 3 | positive (patch 신호) |
| **Metadata-only (7 sample)** | **misleading 4 / helpful 2 / neutral 1 / NHR 0** | **negative (policy 신호)** |

→ P5는 patch 효과 측정 (mechanical 차이 → semantic 차이), Metadata-only는 절대 품질 (essence/trap 정합성). 두 audit이 측정하는 영역이 다르므로 결과 대비는 자연 — patch는 차단기 영역에서 도움, 단 metadata policy 자체는 일부 영역에서 misleading.

---

End of metadata-only audit execution report (7-sample signal).
