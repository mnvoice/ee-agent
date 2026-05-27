# P5 Sampling Design (Semantic Spot Check, Design Only)

> 2026-05-27 KST. Post D-3 breaker B-only patch commit (`00dfdf0`) 후속.
> 본 보고서는 sampling **설계만** 작성. 실제 sampling 실행 / generator 수정 / patch / commit / D-4 / catalog 진입 0.

---

## 1. P5 sampling의 본질 질문

> generator 안에서 metadata가 mechanical하게 작동한 것은 확인 완료.
> 그 결과 사람이 봤을 때 설명이 실제로 더 좋아졌는가?

**핵심 분리**:
- mechanical recovery (13/13) — 이전 게이트에서 측정 완료 (commit `00dfdf0`)
- semantic gain — **본 sampling의 측정 영역**, 본 design에서는 측정 0 (구조만 작성)

---

## 2. Sampling 대상군 정의

| 그룹 | 모집단 | 표본 수 | 선정 전략 | 측정 목적 |
|---|---:|---:|---|---|
| A. breaker_13_recovered | 13 | **5** | 시기 분산 (1998 / 2000 / 2004 × 2 / 2008) — 차단기 dl이 13건 모두 동일하므로 raw solution 표현 다양성을 시기로 확보 | 회로이론 expansion이 사람 입장에서 도움이 되는가? |
| B. non_breaker_expansion_44_spot_check | 44 | **4** | (slot, item) unique 다양성 — 송배전D / 보호고장S × 회로이론 / 전기설비 multi-target | 81 회귀 0 (mechanical)이 사람 기준에서도 정합인가? |
| C. non_expansion_metadata_37_audit | 37 | **3** | slot/item 다양성 — 전력_함정S 1건 + 전력_설비고장 2건 (5 unique items 중) | dl=None 정직 영역에서 enriched metadata만으로 설명 품질이 합리적인가? |
| **합계** | 94 | **12** | | |

---

## 3. 추천 샘플 problem_id 목록

### 3.1 Group A: 차단기 회복 5건

| # | input | pid | year | 선정 이유 |
|---:|---|---|---:|---|
| 1 | input_003.md | 1998_4회_22 | 1998 | 가장 이른 시기 |
| 2 | input_012.md | 2000_2회_23 | 2000 | 2000년 초반 |
| 3 | input_047.md | 2004_1회_90 | 2004 | q_no 90 (계산/응용 영역 후보) |
| 4 | input_056.md | 2004_3회_27 | 2004 | 2004년 4건 중 대표 |
| 5 | input_092.md | 2008_1회_23 | 2008 | 가장 후기 |

차단기 13건은 5축 (slot_grp / item / matched_keyword / dl / audit_group) 모두 동일하므로 시기별 raw solution 변동성이 사람 평가에 영향 가능 — 시기 분산이 유일하게 의미 있는 선정 축.

### 3.2 Group B: 비차단기 expansion 4건

| # | input | pid | slot_grp | item | dl | 선정 이유 |
|---:|---|---|---|---|---|---|
| 6 | input_001.md | 1998_2회_23 | 전력_송배전D | 송전 용량/거리 | `전력 송전용량 -> 회로 4단자망 -> 회로 분포정수` | D/Dynamic 송배전 대표 |
| 7 | input_007.md | 1999_3회_23 | 전력_보호고장S | 지락·중성점 접지 | `전력 중성점 접지 -> 회로 대칭분 해석` | S/Fault non-차단기, multi-target hit (전기설비기술기준 + 회로이론) |
| 8 | input_018.md | 2000_6회_27 | 전력_보호고장S | 단락전류·임피던스 | `전력 단락전류 -> 회로 옴의 법칙 -> 회로 임피던스 환산` | 차단기의 closest neighbor (회로 임피던스 환산 영역 공유) — 비교 유용 |
| 9 | input_015.md | 2000_4회_23 | 전력_송배전D | 코로나 / 전선 도체 | `전력 코로나/표피효과 -> 회로 분포정수 -> 회로 임피던스` | D/Dynamic 송배전 다른 영역 |

### 3.3 Group C: non_expansion_metadata 3건

| # | input | pid | slot_grp | item | 선정 이유 |
|---:|---|---|---|---|---|
| 10 | input_005.md | 1998_4회_25 | 전력_함정S | 부하율·수용률·부등률 | 전력_함정S 대표 |
| 11 | input_008.md | 1999_4회_81 | 전력_설비고장 | 가공전선 이격거리 | 전력_설비고장 대표 1 |
| 12 | input_045.md | 2004_1회_30 | 전력_설비고장 | 가공전선로 경간·이도 | 전력_설비고장 대표 2 (다른 item) |

---

## 4. baseline / B 파일 경로 매핑 규칙

NNN 기반 일관 매핑 (input → output 동일 번호):

| 자원 | baseline | B |
|---|---|---|
| input.md | `docs/.../v_next_inputs_d3/<input>.md` | `docs/.../v_next_inputs_d3_b/<input>.md` |
| output.json | `docs/.../v_next_results_d3/output_NNN.json` | `docs/.../v_next_results_d3_b/output_NNN.json` |
| manifest item | `v_next_inputs_d3/selection_manifest.json` items[] | `v_next_inputs_d3_b/selection_manifest.json` items[] |

매핑 검증: 12 samples 전부 NNN 기반 deterministic mapping 가능 ✓.

---

## 5. 평가 rubric (6 axes)

| # | 축 | 질문 | 방향 |
|---:|---|---|---|
| 1 | comprehension_ease | 학습자가 이 설명을 이해하기 더 쉬운가? | 높을수록 좋음 |
| 2 | cross_subject_link_value | 회로이론 (또는 다른 도메인) 연결이 실제로 학습자의 기존 개념과 의미 있는 다리를 만드는가? | 높을수록 좋음 (link 존재 시 조건부) |
| 3 | forced_link_risk | cross-subject expansion이 장식적/억지스러운가? | 낮을수록 좋음 (negative) |
| 4 | distractor_specificity | 오답 분석이 함정 패턴에 더 구체적인가, 아니면 일반적 표현인가? | 높을수록 좋음 |
| 5 | phenomenon_trap_utility | `core_extraction.phenomenon` / `trap_pattern` / `distractor_analysis.trap_type`이 학습 단서로 유용한가? | 높을수록 좋음 |
| 6 | metadata_overload_risk | metadata 과잉으로 설명이 흩어지거나 스캔이 어려운가? | 낮을수록 좋음 (negative) |

각 축 1-5 척도 또는 N/A. axis 2는 expansion empty 그룹(C)에서 N/A.

---

## 6. 판정 label (4종)

| label | 정의 |
|---|---|
| **B_better** | B output이 학습자에게 명확히 더 유용함 |
| **same** | 차이 없음 또는 무시할 수 있는 수준 — mechanical 변경이 품질 변화로 기록되지 않음 |
| **B_worse** | B output이 오히려 덜 유용함 — cross_subject_expansion 또는 metadata가 명확성을 훼손 |
| **needs_human_review** | rubric 자동 적용 결과가 모호 — 깊은 사람 review로 escalation |

판정은 sample 단위로 1 label. 그룹 단위는 majority label로 집계.

---

## 7. 예상 분기 조건 (6 pathways)

| 조건 | 다음 상태 | 결정 |
|---|---|---|
| 차단기 표본 majority B_better | `patch_semantic_value_supported` | B-only patch semantic value 지지. A1c 추가 불필요 유지. |
| 차단기 표본 majority same | `mechanical_only_no_semantic_gain` | mechanical recovery는 성공했으나 semantic gain 약함. generator utilization / P5 template 검토. |
| 차단기 표본 majority B_worse | `patch_reconsider` | cross-subject 연결이 설명 명확성 훼손 가능. patch 유지 여부 또는 link rendering 정제 검토. |
| 비차단기 spot check 이상 없음 | `regression_human_clean` | 10-field 회귀 0이 사람 기준과 정합. 추가 조치 0. |
| 비차단기 spot check B_worse 발견 | `hidden_regression_found` | 10-field semantic field diff가 놓친 품질 회귀 — audit scope 확대 필요. |
| non_expansion_metadata 표본 품질 향상 약 | `metadata_quality_audit_candidate` | dl-null 영역의 enriched metadata 단독 충분성 부족 — metadata-only audit 별 게이트 후보. |

---

## 8. 지금 하지 말 것 (design 단계 한정)

| 금지 | 사유 |
|---|---|
| Sample 12건 side-by-side read 실행 | 본 단계는 design — execution은 별 사용자 명시 게이트 |
| Rubric 적용 / label 할당 | 동일 |
| Generator / scripts / patch 수정 | 보호 영역 invariant |
| Synthesizer / audit 재실행 | 보호 영역 invariant |
| A1c keyword / A2 fallback 추가 | 별 게이트 |
| D-4 / catalog / gap / reuse 진입 | 별 게이트 |
| commit / push | 별 게이트 |
| DEVLOG / Vault / MEMORY / decision JSONL 작성 | 별 게이트 |

---

## 9. Execution 단계 권장 절차 (사용자 명시 권한 후만)

| step | 작업 |
|---:|---|
| 1 | 12 sample 각각: baseline `output_NNN.json` + B `output_NNN.json` + input.md baseline + input.md B side-by-side 읽기 |
| 2 | 6-axis rubric per sample. 축당 1-5 score 또는 N/A 기록 |
| 3 | sample당 4 label 중 1개 할당 |
| 4 | group별 (A / B / C) majority label 집계 |
| 5 | group 결과를 분기 조건 표에 매핑 → 다음 게이트 추천 |
| 6 | sample-level 결과 + group-level 집계 + 추천 다음 게이트 보고서 작성 |

본 design 단계에서는 step 1-6 모두 수행하지 0. 권장 절차만 명세.

---

## 10. claim boundary 점검

| claim | 본 design 상태 |
|---|---|
| 12 sample 명단 + rubric + label + 분기 조건 design | (a) 명세 |
| baseline/B 매핑 NNN 기반 deterministic 가능 | (a) 검증 — selection_manifest items + 파일 명명 규칙 정합 |
| Mechanical recovery 13/13 (이전 게이트) | (a) 이미 확정 |
| Sample 실제 비교 / 품질 판정 / semantic gain claim | **0** (별 execution 게이트) |
| A1c 필요 결정 | **0** (execution 결과 의존) |
| Patch 유지 재검토 결정 | **0** (execution 결과 의존) |
| Metadata-only audit 별 게이트 필요 결정 | **0** (execution 결과 의존) |

---

## 11. 보호 영역 매트릭스 (전부 미수정 / 0)

`scripts/explanation_synthesizer.py` ✓ / `scripts/v_next_d3_pre_preview.py` ✓ / `scripts/v_next_d3_selector.py` ✓ / `scripts/v_next_d3_input_creator.py` ✓ / `scripts/v_next_d3_parser_validator.py` ✓ / `scripts/v2_input_parser.py` ✓ / `app/data/questions.json` ✓ / D-2 sealed assets ✓ / v_full handoff scope ✓ / A1c keyword 추가 0 ✓ / D-3 재생성 0 ✓ / audit 재실행 0 ✓ / D-4 진입 0 ✓ / catalog/gap/reuse 진입 0 ✓ / commit 0 ✓ / DEVLOG / Vault / MEMORY / decision JSONL 작성 0 ✓.

---

## 12. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_b/p5_sampling_design.md` | 본 design 보고서 (12 섹션) |
| `v_next_results_d3_b/p5_sampling_design.json` | machine-readable — 3 sample group / 12 sample / rubric 6축 / label 4종 / 분기 6 pathways / execution steps |

---

## 13. 최종 상태 판정

**판정**: `READY_FOR_P5_SAMPLING_EXECUTION_GATE`

근거:
- ✓ 12 sample 전부 (slot, item, year) 다양성 기반 선정
- ✓ baseline/B 파일 경로 NNN 기반 deterministic 매핑 검증 완료
- ✓ Rubric 6 axes 구체화
- ✓ Label 4종 정의
- ✓ 분기 조건 6 pathways 열거
- ✓ Execution 단계 권장 절차 step 1-6 명세
- ✓ `NEEDS_P5_SAMPLING_DESIGN_FIX` 미해당 (구조 빈틈 0)
- ✓ `BLOCKED_BY_MISSING_SAMPLE_MAPPING` 미해당 (전 sample mapping 가능)

다음 단계 (P5 execution + rubric 적용 + label 할당 + 분기 결정) 진입은 본 design 다음 사용자 명시 게이트 영역.

---

End of P5 sampling design (design only) report.
