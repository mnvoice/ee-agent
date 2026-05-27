# v_next D-3 Selection Report

> v_next D-3 input creation 완료 — 전력공학 CLEAN 94 main.
> D-3 generation 0 / audit 0 / commit 0 / D-2 sealed assets 미수정 / v_full handoff scope 미수정.

## 1. 측정 요약

| 단계 | 측정 |
|---|---:|
| target pool (전력공학) | 242 |
| CLEAN selected | 94 / 94 |
| input files generated | 94 |
| holdout-new (v_full handoff read-only) | ✓ |
| reuse tranche | 사용 0 |

## 2. Audit Group Distribution

| audit_group | count |
|---|---:|
| expansion | 57 |
| non_expansion_metadata | 37 |

## 3. Slot/Item Distribution

| slot | item | count |
|---|---|---:|
| 전력_보호고장S | 단락전류·임피던스 | 4 |
| 전력_보호고장S | 보호계전기·피뢰기 | 6 |
| 전력_보호고장S | 지락·중성점 접지 | 4 |
| 전력_보호고장S | 차단기 | 13 |
| 전력_설비고장 | 가공전선 이격거리 | 26 |
| 전력_설비고장 | 가공전선로 경간·이도 | 4 |
| 전력_설비고장 | 절연내력 / 유도장해 | 3 |
| 전력_송배전D | 분포정수 송전 | 6 |
| 전력_송배전D | 송전 용량/거리 | 11 |
| 전력_송배전D | 전압강하·전력손실 | 10 |
| 전력_송배전D | 코로나 / 전선 도체 | 3 |
| 전력_함정S | 부하율·수용률·부등률 | 3 |
| 전력_함정S | 역률 개선 | 1 |

## 4. Evidence Field Distribution (CLEAN 94)

| field | count | 비율 |
|---|---:|---:|
| both | 88 | 93.6% |
| question_text | 6 | 6.4% |
| solution | 0 | 0.0% |
| tag | 0 | 0.0% 필수 = 0 |

## 5. Enriched Metadata 4 Field 부착

| field | 부착 | 비고 |
|---|---:|---|
| dynamic_link | 57 / 94 | null 허용 (37건 정직) |
| essence_question | 94 / 94 | 모든 entry 필수 |
| representative_trap | 94 / 94 | 모든 entry 필수 |
| trap_type | 94 / 94 | 모든 entry 필수 |

## 6. Policy 정합

- source_design: decision_records/2026-05-27_d3_selector_design.md
- item_policy_promotion: decision_records/2026-05-27_d3_power_item_policy_promotion.md
- gold_sample_baseline: decision_records/2026-05-27_gold_sample_quality_baseline_policy.md
- clean_only_main: True
- tag_only_rescue: False
- suspect_rescue: False
- keyword_expansion: False
- broad_keyword_banned: True
- quota_filling_banned: True
- audit_group_split: True
- dl_null_honest: True
- enriched_fields_in_parser_sections: True
- sidecar_metadata: False

## 7. 다음 단계

- parser validation (`v_next_d3_parser_validator.py`)
- parser PASS 확인 후 사용자 명시 D-3 generation 진입 게이트

---
End of v_next D-3 selection report.
