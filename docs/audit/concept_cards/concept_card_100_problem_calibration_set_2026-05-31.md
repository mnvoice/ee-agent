# 100 Problem Calibration Set

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This record selects the 20-row stratified calibration set for the open 100 Problem Expansion Validation Gate.

It does not classify the full 100 rows. It does not patch YAML. It does not claim card pass/fail, gold-set status, benchmark status, or semantic-gain proof.

## 2. Source Boundary

```yaml
gate_name: 100 Problem Expansion Validation Gate
gate_status: open
source_inventory: docs/audit/concept_cards/concept_card_100_problem_source_inventory_2026-05-31.md
source_file: app/data/questions.json
selection_pool: first 100 rows from subject == "회로이론", sorted by year/session/q_no
calibration_target_count: 20
calibration_sampling: stratified
full_100_row_classification_completed: false
yaml_mutation_authorized: false
```

## 3. Selection Rules Applied

- Select only rows already present in the frozen 100-row inventory.
- Keep the four required strata at 5 rows each.
- Prefer rows that exercise distinct failure modes rather than repeating one obvious pattern.
- Treat tags as signals only.
- Do not convert a pressure signal into patch, promotion, or new-card authorization.

## 4. Calibration Set

| stratum | inventory row | problem_id | tag signal | source/data stress target | domain stress target | card-fit stress target | calibration reason |
|---|---:|---|---|---|---|---|---|
| clean anchor | 6 | `1998_4회_61` | 공진 | usable | pure circuit phasor/resonance | baseline card family should be findable | Clean text and choices; checks phase/complex quantity mapping without obvious source damage. |
| clean anchor | 33 | `1999_6회_62` | 저항의 직·병렬접속 | usable | pure circuit theory | baseline series/parallel or current-divider family | Simple resistor/instrument scaling row for low-noise baseline calibration. |
| clean anchor | 36 | `2000_2회_61` | R-L 과도현상 | usable | pure circuit theory | baseline transient family | RL transient calculation with visible circuit premise; useful clean anchor for time-constant mapping. |
| clean anchor | 48 | `2000_6회_65` | 테브난 정리와 노튼의 정리 | usable | pure circuit theory | baseline Thevenin/Norton family | Direct equivalent-source formula row with coherent text and choices. |
| clean anchor | 69 | `2001_3회_63` | 테브난 정리와 노튼의 정리 | usable | pure circuit theory | baseline source-transformation / ideal-source boundary | Clean conceptual source row; useful to test whether Thevenin/Norton tag should map to source-transformation support. |
| source-data suspect | 4 | `1998_2회_64` | 테브난 정리와 노튼의 정리 | metadata/source conflict | uncertain | do not infer card failure from damaged row | Text is mostly cross-references, while choices look like a different circuit classification question. |
| source-data suspect | 10 | `1998_4회_67` | 정보 부족 | metadata_only | uncertain | not suitable for card proof unless recovered | Text is only year/session metadata and choices are blank. |
| source-data suspect | 15 | `1998_6회_66` | Y결선과 △결선의 전압, 전류 관계 및 선전류 | metadata_only | uncertain | not suitable for card proof unless recovered | Text is only year/session metadata and choices are blank despite a plausible tag. |
| source-data suspect | 47 | `2000_6회_61` | 상호인덕턴스 | source_conflict / OCR damage | pure circuit theory likely, but source axis non-clean | mutual_inductance may be tempting but choices are corrupted | Text describes mutual inductance, but choices appear unrelated/corrupted. |
| source-data suspect | 98 | `2004_1회_73` | 대칭분 해석 | tag_text_mismatch / source_conflict | pure circuit theory likely after text read | tag family is misleading; likely Laplace family if usable | Tag says symmetrical components, text says Laplace transform, and choices appear mismatched. |
| domain-boundary suspect | 5 | `1998_2회_67` | 허용 태그 목록에 없습니다. | usable | logic_or_digital | likely not_applicable or new-card signal, not card failure | Boolean simplification row inside 회로이론 source pool; tests digital/logic boundary handling. |
| domain-boundary suspect | 14 | `1998_6회_64` | 신호흐름선도 | usable, figure-needed | cross_subject_control_signal | existing transfer/Bode cards may overextend | Signal-flow graph row tests control/signal boundary and figure dependency. |
| domain-boundary suspect | 40 | `2000_2회_67` | 유도전압 조정기 | usable | contamination_or_out_of_scope | no circuit-card stretch | Displacement-pressure transducer row is a source-pool contamination candidate. |
| domain-boundary suspect | 41 | `2000_2회_70` | 피상전력 | tag_text_mismatch | cross_subject_control_signal | likely wrong-card-family if mapped by tag | State-variable system matrix row with misleading apparent-power tag. |
| domain-boundary suspect | 61 | `2001_1회_74` | 비정현파의 실효치 계산 | usable with weak metadata | cross_subject_power_three_phase | symmetrical-components / three-phase boundary | Unbalanced three-phase sequence-current row tests power/three-phase boundary inside 회로이론 pool. |
| card-coverage boundary | 7 | `1998_4회_63` | 라플라스 변환의 초기값 정리와 최종값 정리 | usable | pure circuit theory | pilot-only fit possible | Direct IVT/FVT row; must test pilot-only mapping without promotion. |
| card-coverage boundary | 23 | `1999_3회_65` | 공진 | tag_text_mismatch likely | broad_scope_exam_circuit / control stability | wrong-card-family risk | Bode stability wording under resonance tag; tests tag-as-signal rule. |
| card-coverage boundary | 35 | `1999_6회_69` | 4단자 정수의 회로망 특성 | usable, figure-needed | pure circuit / network theory | two_port_network fit may be partial | 4-terminal constant row tests whether current two-port card is specific enough. |
| card-coverage boundary | 86 | `2003_1회_66` | 공진 | usable, figure-needed | pure circuit theory | RLC / Q-bandwidth / antiresonance boundary | Antiresonance row tests whether existing resonance card is too broad or needs support. |
| card-coverage boundary | 87 | `2003_1회_67` | 전달함수 | usable | broad_scope_exam_circuit / control bandwidth | q_bandwidth pilot or transfer-family boundary | Closed-loop transfer-function bandwidth row tests pilot-only fit and control-boundary handling. |

## 5. Calibration Run Skeleton

When these 20 rows are classified, use the revised schema from `concept_card_100_problem_schema_revision_2026-05-31.md`.

For this setup record, the final row fields remain intentionally unfilled:

| field | setup value |
|---|---|
| `source_condition` | assign during 20-row calibration |
| `domain_classification` | assign during 20-row calibration |
| `concept_card_mapping` | assign during 20-row calibration after source/domain read |
| `card_role` | assign during 20-row calibration |
| `coverage_status` | assign during 20-row calibration only |
| `card_fit_issue` | assign during 20-row calibration |
| `pressure_point_flag` | assign during 20-row calibration, evidence only |
| `requires_human_review` | assign during 20-row calibration using the human-review rule |
| `multi_failure_flag` | assign during 20-row calibration when more than one axis is non-clean |
| `gold_set_disclaimer` | `not_gold_not_benchmark` |
| `review_status` | `codex_calibration` |

## 6. Expected Calibration Checks

The 20-row calibration should verify whether the workflow can consistently distinguish:

- source-data failure from card weakness
- domain-boundary rows from missing-card rows
- misleading tag signals from source text
- pilot-only mapping from baseline coverage
- single-axis issues from multi-failure rows

## 7. Notable Ambiguities To Resolve During Calibration

| problem_id | ambiguity |
|---|---|
| `2000_6회_61` | Text supports mutual inductance, but choices are visibly unrelated/corrupted. |
| `2004_1회_73` | Tag says symmetrical components; text says Laplace transform; choices appear unrelated to text. |
| `1999_3회_65` | Tag says resonance; text is Bode stability judgment. |
| `2003_1회_67` | Bandwidth could tempt `q_bandwidth` mapping, but the row is closed-loop transfer-function bandwidth, not necessarily RLC/Q bandwidth. |
| `2001_1회_74` | The row is inside the 회로이론 pool but its concept may belong to three-phase symmetrical components. |

## 8. Next Allowed Step

Next allowed automated step:

```yaml
next_step: classify_selected_20_calibration_rows
full_100_row_classification_authorized_before_calibration_closeout: false
yaml_mutation_authorized: false
```

The calibration closeout should record whether the revised schema is usable as-is or needs another non-YAML schema/workflow revision before the full 100-row classification.

## 9. Claim Boundary

This calibration-set record does not claim:

- calibration classification completion
- full 100-row classification completion
- card pass/fail outcome
- gold set completion
- benchmark status
- corpus grounding completion
- semantic-gain proof
- YAML patch authorization
- `expansion_pilot` promotion
- PR #1 ready-for-review approval
- PR #1 merge approval
