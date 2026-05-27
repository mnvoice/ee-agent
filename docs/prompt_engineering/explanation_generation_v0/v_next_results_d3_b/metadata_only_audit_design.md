# Metadata-Only Audit Design (non_expansion_metadata 37건)

> 2026-05-27 KST. Post-P5 sampling result push (`be4f7f0`) 후속.
> 본 보고서는 **audit 설계만** 작성. 실제 audit 실행 / generator 수정 / patch / commit / D-4 / catalog 진입 0.

---

## 1. 본질 질문

> D-3 non_expansion_metadata 37건은 dl=None이 정직한 영역.
> 그렇다면 cross_subject_expansion 없이 **essence / representative_trap / trap_type metadata 단독**으로 설명 품질이 충분히 좋아지는가?

P5 sampling은 baseline ↔ B 비교 (patch 효과 측정). non_expansion 그룹은 B = baseline이므로 P5에서는 patch 무관 영역으로 분류됨. 본 audit은 그 영역의 **절대 품질** 평가.

---

## 2. 모집단 분포 (37건)

### 2.1 slot/item 분포

| slot_grp | item | 건수 | 비중 |
|---|---|---:|---:|
| 전력_설비고장 | 가공전선 이격거리 | **26** | 70.3% |
| 전력_설비고장 | 가공전선로 경간·이도 | 4 | 10.8% |
| 전력_함정S | 부하율·수용률·부등률 | 3 | 8.1% |
| 전력_설비고장 | 절연내력 / 유도장해 | 3 | 8.1% |
| 전력_함정S | 역률 개선 | 1 | 2.7% |
| **합계** | | **37** | 100% |

### 2.2 핵심 관찰

- 5 unique (slot, item) 키
- **가공전선 이격거리가 모집단 70.3% 압도** — sample 다양성 vs 모집단 정합 trade-off 처리 필요
- 전력_함정S 4 + 전력_설비고장 33 = 매우 비대칭

---

## 3. Sample 선정 (7건)

### 3.1 선정 전략

- 5 unique items 전 cover
- 가공전선 이격거리 (모집단 70%)는 3건 시기 분산 (1999 / 2005 / 2007)
- 다른 4 items 각 1건
- P5 sample 재사용 가능 (input_005, 008, 045 — 3건은 sha256 identity 측정 영역 외, 본 audit은 절대 품질 평가라 재사용 정합)

### 3.2 7 sample roster

| # | input | pid | slot | item | essence | trap |
|---:|---|---|---|---|---|---|
| M1 | input_005.md | 1998_4회_25 | 전력_함정S | 부하율·수용률·부등률 | 부하율/수용률/부등률을 어떻게 구분해 외우는가 | 부하율 vs 수용률 vs 부등률 정의 혼동 함정 |
| M2 | input_075.md | 2006_2회_26 | 전력_함정S | 역률 개선 | 역률 개선 콘덴서 용량을 어떻게 계산하는가 | Qc 공식 sin / cos 혼동 함정 |
| M3 | input_008.md | 1999_4회_81 | 전력_설비고장 | 가공전선 이격거리 | 가공전선과 다른 시설간 안전 이격거리는 어떻게 정해지는가 | 전선 종류별 이격거리 표 혼동 함정 |
| M4 | input_069.md | 2005_3회_81 | 전력_설비고장 | 가공전선 이격거리 | (동일) | (동일) |
| M5 | input_086.md | 2007_1회_84 | 전력_설비고장 | 가공전선 이격거리 | (동일) | (동일) |
| M6 | input_045.md | 2004_1회_30 | 전력_설비고장 | 가공전선로 경간·이도 | 전선 장력·이도·경간이 어떻게 작용하는가 | 경간 vs 이도 관계 혼동 함정 |
| M7 | input_020.md | 2000_6회_85 | 전력_설비고장 | 절연내력 / 유도장해 | 절연내력 시험전압과 유도장해 경감이 어떻게 작용하는가 | 절연내력 시험전압 배율 / 유도장해 경감대책 혼동 함정 |

### 3.3 coverage

| 측정 | 값 |
|---|---|
| items covered | 5 / 5 (전 cover) |
| 시기 분산 | 1998 / 1999 / 2000 / 2004 / 2005 / 2006 / 2007 |
| 함정S 표본 | 2 |
| 설비고장 표본 | 5 |

가공전선 이격거리 3 / 7 = 42.9% (모집단 70.3%과 절충 — 다양성을 위해 다른 4 items 1건씩 cover).

---

## 4. 파일 경로 매핑

| 자원 | 경로 |
|---|---|
| input.md | `docs/.../v_next_inputs_d3_b/<input>.md` |
| output.json | `docs/.../v_next_results_d3_b/output_NNN.json` |

**중요 분리**: 본 metadata-only audit은 B output **단독 절대 품질** 평가. baseline 비교는 P5에서 이미 완료 (all `same`).

---

## 5. 평가 Rubric (6 axes)

| # | 축 | 질문 | 방향 |
|---:|---|---|---|
| 1 | essence_captures_core | essence_question이 문제 핵심을 잡는가? 학습자가 essence만 보고 무엇을 외우거나 계산해야 하는지 파악 가능한가? | 높을수록 좋음 |
| 2 | trap_alignment | representative_trap이 실제 오답 함정과 의미적으로 일치하는가? (distractor_analysis 내용과 비교) | 높을수록 좋음 |
| 3 | trap_type_distractor_utility | trap_type이 distractor 생성에 실질적 도움을 주는가? | 높을수록 좋음 |
| 4 | dl_null_honesty | dl=None이 정직한가? — 이 item이 정말로 cross-subject 의미가 약한 정적 함정 영역인지, 사실은 dl 후보가 있는데 누락된 것인지 | 높을수록 좋음 (null이 정직할수록 5점) |
| 5 | expansion_absence_safety | expansion 없는 것이 오히려 안전한가? — 억지 link 회피 | 높을수록 좋음 |
| 6 | metadata_overload_risk | essence + trap + trap_type metadata가 과부하/장식적인가? | 낮을수록 좋음 (negative) |

각 축 1-5 척도 또는 N/A. axis 4와 axis 5가 metadata-only 정책의 정직성을 결정하는 핵심.

---

## 6. Label 정의 (4종)

| label | 정의 |
|---|---|
| **metadata_helpful** | essence + trap + trap_type 단독으로 학습자에게 실질적 도움. dl=None이 정직, expansion 부재가 안전 |
| **metadata_neutral** | metadata가 표면적으로 존재하지만 학습 가치 약. 없어도 거의 같은 수준 |
| **metadata_misleading** | essence 또는 trap이 실제 문제와 어긋나거나, trap_type이 distractor 영역과 불일치 |
| **needs_human_review** | rubric 자동 적용 결과 모호 — 깊은 사람 review 필요 |

---

## 7. Diagnostic Signal (4종, label과 독립)

| signal | trigger | action |
|---|---|---|
| `dl_should_exist_candidate` | axis 4 dl_null_honesty 점수 ≤ 2 | 본 audit 후 별 policy review 후보 — catalog/gap rescue 또는 D-3 ITEM_POLICY dl 보정 영역 |
| `metadata_only_value_strong` | majority `metadata_helpful` + 5 axis 평균 ≥ 3.5 | metadata-only 영역의 enrichment 가치 입증 |
| `majority_neutral` | majority `metadata_neutral` + axis 5 expansion_absence_safety 평균 ≥ 3 | metadata 자체는 무해, 적극적 가치 약 |
| `misleading_present` | 1건 이상 `metadata_misleading` | metadata policy review 후보 — essence/trap 정의 재검토 |

---

## 8. 분기 조건 (5 pathways)

| 조건 | 다음 상태 | 결정 |
|---|---|---|
| majority `metadata_helpful` | `metadata_only_value_supported` | metadata-only 영역의 enrichment 가치 입증. 정책 유지 + A1c 불필요 유지. |
| majority `metadata_neutral` | `metadata_surface_only` | enrichment surface 있으나 품질 이득 약함. 정책 유지 default. 향후 patch 우선순위 낮음. |
| `metadata_misleading` 1건 이상 | `metadata_policy_review_candidate` | essence/trap 정의 정합성 확인 별 게이트. |
| `dl_should_exist` 의심 발생 (axis 4 ≤ 2) | `catalog_or_policy_review_candidate` | catalog/gap rescue 또는 D-3 ITEM_POLICY dl 후보 추가 review 영역. |
| majority `needs_human_review` | `deep_human_review_required` | automated rubric 한계 — 깊은 사람 검토 게이트로 escalation. |

---

## 9. Execution 단계 권장 절차 (사용자 명시 권한 후만)

| step | 작업 |
|---:|---|
| 1 | 7 sample 각각 B output_NNN.json + input.md side-by-side 읽기 |
| 2 | 6-axis rubric per sample 적용 (1-5 또는 N/A). axis 4 + 5 특히 신중 |
| 3 | sample당 4 label 중 1개 할당 + diagnostic signal (특히 `dl_should_exist_candidate`) 표시 |
| 4 | 7 sample 집계 — majority label + 5 axis 평균 + misleading 발생 + dl_should_exist 명단 |
| 5 | 분기 5 pathways 매핑 → 다음 게이트 추천 |
| 6 | sample-level + 집계 + 추천 다음 게이트 보고서 작성 |

본 design 단계에서는 step 1-6 모두 수행 0. 권장 절차만 명세.

---

## 10. 지금 하지 말 것 (design 단계 한정)

| 금지 | 사유 |
|---|---|
| Sample 7건 side-by-side read 실행 | execution 게이트 영역 |
| Rubric 적용 / label 할당 / diagnostic signal 평가 | 동일 |
| Generator / scripts / patch 수정 | 보호 영역 |
| Synthesizer / audit 재실행 | 보호 영역 |
| P5 재실행 | 별 게이트 |
| A1c keyword / A2 fallback 추가 | 별 게이트 |
| D-4 진입 | 별 게이트 |
| catalog / gap / reuse 진입 | 별 게이트 |
| commit / push | 별 게이트 |
| DEVLOG / Vault / MEMORY / decision JSONL 작성 | 별 게이트 |

---

## 11. claim boundary 점검

| claim | 본 design 상태 |
|---|---|
| 7 sample 명단 + rubric + label + diagnostic signal + 분기 design | (a) 명세 |
| NNN 기반 deterministic 매핑 가능 | (a) 검증 |
| Mechanical recovery 13/13 + P5 signal B_better (이전 게이트) | (a) 이미 확정 |
| 37 전체 절대 품질 claim | **0** — 본 design 단계는 sample 7건 명세만 |
| dl_should_exist 결정 | **0** — execution 결과 의존 |
| metadata policy 수정 결정 | **0** — execution 결과 의존 |
| catalog/gap rescue 결정 | **0** — execution 결과 의존 |
| A1c 결정 / D-4 결정 | **0** — 별 게이트 |

---

## 12. 보호 영역 매트릭스 (전부 미수정 / 0)

`scripts/explanation_synthesizer.py` ✓ / `scripts/v_next_d3_pre_preview.py` ✓ / `scripts/v_next_d3_selector.py` ✓ / `scripts/v_next_d3_input_creator.py` ✓ / `scripts/v_next_d3_parser_validator.py` ✓ / `scripts/v2_input_parser.py` ✓ / `app/data/questions.json` ✓ / D-2 sealed assets ✓ / v_full handoff scope ✓ / A1c keyword 추가 0 ✓ / D-3 재생성 0 ✓ / audit 재실행 0 ✓ / P5 재실행 0 ✓ / D-4 0 ✓ / catalog/gap/reuse 0 ✓ / commit 0 ✓ / DEVLOG / Vault / MEMORY / decision JSONL 작성 0 ✓.

---

## 13. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_b/metadata_only_audit_design.md` | 본 design 보고서 (13 섹션) |
| `v_next_results_d3_b/metadata_only_audit_design.json` | machine-readable — 모집단 분포 / 7 sample / 6 rubric / 4 label / 4 diagnostic signal / 5 pathways / execution steps |

---

## 14. 최종 상태 판정

**판정**: `READY_FOR_METADATA_ONLY_AUDIT_EXECUTION_GATE`

근거:
- ✓ 7 sample 전부 NNN 기반 deterministic 매핑 가능
- ✓ 5 unique items 전 cover (모집단 5 / 5)
- ✓ 가공전선 이격거리 (모집단 70%) 시기 분산 3건
- ✓ 함정S 2 + 설비고장 5 (모집단 비중과 절충)
- ✓ Rubric 6 axes 구체화 (axis 4 + 5는 dl_null_honesty + expansion_absence_safety 핵심)
- ✓ Label 4종 정의
- ✓ Diagnostic signal 4종 (특히 `dl_should_exist_candidate`) 정의
- ✓ 분기 5 pathways 열거
- ✓ Execution step 1-6 권장 절차 명세
- ✓ `NEEDS_METADATA_ONLY_AUDIT_DESIGN_FIX` 미해당 (구조 빈틈 0)

다음 단계 (audit execution + rubric 적용 + label/diagnostic 할당 + 분기 결정) 진입은 본 design 다음 사용자 명시 게이트 영역.

---

End of metadata-only audit design (design only) report.
