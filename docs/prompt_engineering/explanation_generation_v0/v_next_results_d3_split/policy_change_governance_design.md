# Policy Change Governance Layer Design

> 2026-05-27 KST. Post-hard_check_policy_design 후속.
> 본 보고서는 governance rule layer **design만** 작성. 자동화 / 코드 / D-4 preview / policy 수정 / commit 0.

---

## 0. 핵심 한 줄 결론

**`READY_FOR_POLICY_GOVERNANCE_IMPLEMENTATION_GATE`** + `NEEDS_USER_DECISION_ON_THRESHOLDS` (default value 사용자 명시).

15 rule set + policy_change_declaration schema + manifest_diff 12 transitions + 10 movement labels + 4 alert severity + configurable thresholds + tool/subject section + D-4 7-step workflow 명세 완료.

---

## 1. 왜 automation 전에 governance layer가 필요한가

### 1.1 Split 실험 교훈

- split 실험에서 CLEAN 94 → 87 manifest shift 발생
- input_creator fixed hard check가 false positive 차단
- 정합 정교화 효과 측정 가능, 단 자동화 도구가 정교화와 회귀 구분 불가

### 1.2 Governance 없이 자동화의 위험

| 위험 | 영역 |
|---|---|
| 정합 정교화를 회귀로 판정 | false positive 차단 |
| 회귀를 정합 정교화로 판정 | false negative 통과 |
| tool drift를 policy change로 오분류 | 책임 영역 흐림 |
| subject drift 무관심 | 추적 누락 |
| broad keyword 재도입 미감지 | 안전 invariant 손상 |
| data debt drop과 unexplained loss 구분 불가 | data 영역 판단 흐림 |

### 1.3 Governance Layer Role

automation이 변동 감지 시 사람이 판정 가능한 카테고리 체계를 사전에 정의. automation 출력 = 분류된 변동 라벨 + alert severity. 사람 review queue에 정합 분류된 변동만 진입.

---

## 2. Claude 웹 v0.2 규칙 검토

| 규칙 | 판정 | 처리 |
|---|---|---|
| R6 60% threshold | **configurable default 격하** | 60% default 유지, 사용자 조정 영역 |
| R9 신규 발생 정의 | **4 sub-category 명시** | R9a/R9b/R9c/R9d 분리 |
| R10/R11 positive movement | **유지** | catalog/NEEDS_REVIEW/GAP → CLEAN 별 라벨 |
| R12 tool change tracking | **유지 + 강화** | policy/tool 분리 추적 |
| catalog ↔ NEEDS_REVIEW 분리 | **별 status 지원** | classification taxonomy 분리 |
| 변동량 0 entry diff | **필수** | same-count drift 추적 |

### 2.1 R9 4 sub-category

| sub | 정의 |
|---|---|
| R9a | before=0 after>0 (전무 → 진입) |
| R9b | before>0 after=0 (소멸) |
| R9c | new item introduced (item 자체 신설) |
| R9d | new status entered (status enum 신설) |

---

## 3. 최종 Rule Set (R1-R15)

| # | rule |
|---:|---|
| R1 | policy change declaration 사전 제출 — declaration 없이 발견된 변동은 hard_alert |
| R2 | CLEAN 감소 기본 investigate — declaration의 expected_exit + cause 명시 시 soft_alert |
| R3 | CLEAN 증가 기본 suspect — positive_recovery (catalog/NEEDS_REVIEW/GAP → CLEAN) 명시 시 soft_info, 다른 영역 진입은 suspicious_gain |
| R4 | broad single-word keyword 재도입은 항상 hard_alert + block 후보 |
| R5 | 변동량 0이어도 entry-level diff 필수 |
| R6 | configurable threshold default 60% (subject별 override 가능) |
| R7 | policy change vs tool change 분리 추적 — 동시 발생 시 hard_alert |
| R8 | subject change 별 section 추적 (추가/제거/rename/merge/split/drift) |
| R9 | 신규 발생 4 sub-category 분리 |
| R10 | positive movement (catalog/NEEDS_REVIEW/GAP → CLEAN) 별 라벨 |
| R11 | data debt drop intentional 명시 분리 |
| R12 | tool change 별 section + reviewer notes |
| R13 | protected groups (expansion 57 / 차단기 13 등) 회귀 0 hard invariant |
| R14 | alert severity 4 단계 — threshold configurable |
| R15 | human review queue는 hard_alert 이상만 진입 — soft/info는 audit log |

---

## 4. policy_change_declaration Schema

### 4.1 Required Fields

| field | description |
|---|---|
| `change_id` | 고유 식별자 (예: `SPLIT-S1S4-001`) |
| `subject` | 전력공학 / 기기 / 설비 등 |
| `affected_slots` | 변경 영향 받는 slot list |
| `affected_items` | (slot, item) 키 list |
| `expected_clean_delta` | 예: -7 또는 range -10 ~ +3 |
| `expected_catalog_delta` | 예: +9 |
| `expected_gap_delta` | 예: -2 |
| `expected_positive_movement` | catalog/NEEDS_REVIEW/GAP → CLEAN 회수 예상 list |
| `expected_exit` | CLEAN → 비CLEAN 예상 pid + cause (recoverable/partial/intentional/data_debt) |
| `expected_new` | 비CLEAN → CLEAN 예상 pid + 매칭 keyword |
| `forbidden_changes` | broad keyword 재도입 / protected 변경 / subject drift |
| `protected_groups` | expansion 57 / 차단기 13 / sealed assets — 회귀 0 영역 |
| `reviewer_notes` | human reviewer 자유 입력 |

### 4.2 Optional Fields

| field | description |
|---|---|
| `tool_change_section` | tool 변경 영역 (R7) |
| `subject_change_section` | subject 변경 영역 (R8) |
| `configurable_thresholds` | subject별 threshold override |

---

## 5. manifest_diff_classification Taxonomy (12 transitions)

| ID | transition | default label |
|---|---|---|
| T1 | CLEAN → GAP | investigate (cause 분류 필요) |
| T2 | CLEAN → catalog (NEEDS_REVIEW) | investigate |
| T3 | CLEAN → CLEAN item 변경 (라우팅) | expected_refinement 또는 mismatch_reroute |
| T4 | catalog/NEEDS_REVIEW → CLEAN | positive_recovery |
| T5 | GAP → CLEAN | positive_recovery (강한 회수) |
| T6 | GAP → catalog | partial_recovery |
| T7 | catalog → GAP | investigate (data debt 가능성) |
| T8 | new CLEAN (전무 → CLEAN 진입) | positive_gain 또는 suspicious_gain |
| T9 | CLEAN exit (CLEAN → 비CLEAN, T1+T2 통합) | recoverable_loss / intentional_drop / data_debt |
| T10 | status unchanged but item changed | mismatch_reroute |
| T11 | count unchanged but entry-level diff | same_count_drift |
| T12 | no transition (status + item + kw 동일) | stable |

---

## 6. Movement Labels (10)

| label | 정의 |
|---|---|
| expected_refinement | declaration 명시된 정합 정교화 |
| recoverable_loss | CLEAN exit, keyword 보강으로 회복 가능 |
| intentional_drop | data debt 등 정책상 intentional 분리 |
| positive_recovery | catalog/NEEDS_REVIEW/GAP → CLEAN 회수 |
| suspicious_gain | 전무 → CLEAN 진입 + declaration 미명시 |
| broad_match_risk | broad single-word keyword 재도입 |
| data_debt | OCR / 풀이 부재 / 답안 부정합 등 questions.json 영역 |
| tool_drift | policy 변경 없이 tool change로 발생한 변동 |
| subject_drift | subject 영역 변경 |
| needs_human_review | 자동 분류 불가 — review queue 진입 |

---

## 7. Alert Severity (4 단계)

| severity | trigger | action |
|---|---|---|
| **info** | stable / expected_refinement / positive_recovery / new CLEAN with declaration | audit log 기록만 |
| **soft_alert** | recoverable_loss + declaration / intentional_drop + cause / data_debt + marker | audit log + WARN |
| **hard_alert** | unexplained CLEAN loss / suspicious_gain / mismatch_reroute without declaration / tool+policy 동시 | human review queue + ERROR |
| **block** | broad_match_risk / protected_group 회귀 / sealed_baseline mode 위반 / unexplained delta > threshold | automation 중단 + ERROR + human 명시 인가 |

---

## 8. Configurable Thresholds (default proposal)

| threshold | default | rationale |
|---|---:|---|
| `delta_percent_threshold` | 0.60 | 절대값 변화량 / baseline 비율 60% 초과 시 hard_alert |
| `unexplained_clean_loss_threshold` | 0.05 | baseline CLEAN의 5% 초과 unexplained loss = block |
| `broad_keyword_word_length_threshold` | 2 | length 1 token keyword는 broad 후보 — multi-word (length 2+) 안전 |
| `positive_gain_threshold` | 0.10 | baseline 비CLEAN의 10% 초과 신규 CLEAN = suspicious_gain |

**모든 threshold configurable** — `configurable_thresholds.json` (subject별 + global default) 영역. 위 값은 default proposal — 사용자 명시 확정 영역.

---

## 9. tool_change_section Design

### 9.1 Tracked Tool Changes

- stopword list 변경
- score threshold 변경 (예: CLEAN cutoff 15 → 14)
- parser library / version 변경
- selector algorithm 변경 (예: priority 룰)
- scoring rule 변경 (예: evidence_field score weight)
- output path 변경

### 9.2 Declaration Fields

| field | description |
|---|---|
| `tool_change_id` | 고유 식별자 |
| `change_type` | stopword / threshold / parser / selector / scoring / output_path |
| `before_value / after_value` | 변경 전/후 값 |
| `affected_subjects` | 영향 받는 subject list |
| `estimated_manifest_impact` | 예상 manifest 영향 |
| `reviewer_notes` | reviewer 자유 입력 |

### 9.3 R7 분리 룰

policy change ↔ tool change 동시 run 시 → **hard_alert 또는 block**. 분리 run 권장. 사용자 명시 인가 시 block 회피.

---

## 10. subject_change_section Design

### 10.1 Tracked Subject Changes

- subject_added (새 과목 신설)
- subject_removed (폐기)
- subject_renamed (예: `전력공학` → `PowerEng`)
- subject_merge (2개 → 1개)
- subject_split (1개 → 2개)
- subject_count_drift (예상치 못한 추가/제거)

### 10.2 Declaration Fields

| field | description |
|---|---|
| `subject_change_id` | 고유 식별자 |
| `change_type` | added / removed / renamed / merge / split / drift |
| `before_subject_list / after_subject_list` | 변경 전/후 subject list |
| `migration_mapping` | rename / merge / split 시 pid 이동 매핑 |
| `expected_manifest_impact` | subject별 expected_clean_delta |
| `reviewer_notes` | reviewer 자유 입력 |

### 10.3 Default Severity

subject_drift declaration 0 시 → **hard_alert**.

---

## 11. D-4 Automation 적용 방식

### 11.1 Subject별 필수 항목

- subject별 `expected_clean_range` (예: 기기 245-275 / 설비 110-130)
- subject별 `protected_groups`
- subject별 `manifest_diff_report` (baseline vs new)
- subject별 `human_review_queue`
- subject별 `automation_stop_condition` (block trigger 시)

### 11.2 Reusable Components

- `policy_change_declaration` schema (subject별 instance)
- `manifest_diff_classification` taxonomy (전 subject 공통)
- movement labels (전 subject 공통)
- alert severity 4 단계 (전 subject 공통)
- configurable thresholds (subject별 override)

### 11.3 D-4 Workflow (7 step)

| step | 작업 |
|---:|---|
| 1 | subject 선택 + policy_change_declaration 제출 |
| 2 | D-3 selector dry-run → manifest diff 생성 |
| 3 | manifest_diff_classification 자동 분류 |
| 4 | alert severity 자동 측정 |
| 5 | block trigger 시 automation 중단 → human review |
| 6 | 통과 시 input_creator (policy_revision mode) 실행 |
| 7 | post-revision audit + commit + push |

### 11.4 Human Review Queue Entry Conditions

- hard_alert 이상 발생
- unexplained_clean_loss > threshold
- broad_match_risk 감지
- tool_drift + policy 동시
- subject_drift declaration 0
- protected_group 회귀 측정

---

## 12. 사용자 결정 필요 항목 (6)

| # | 항목 | default proposal | rationale |
|---:|---|---|---|
| 1 | `delta_percent_threshold` default | 0.60 | Claude 웹 v0.2의 60% 그대로 default — 사용자 조정 영역 |
| 2 | `unexplained_clean_loss_threshold` default | 0.05 | baseline의 5% 초과 = block default |
| 3 | `positive_gain_threshold` default | 0.10 | 비CLEAN의 10% 초과 신규 CLEAN = suspicious_gain default |
| 4 | human_review_queue 진입 trigger 범위 | hard_alert 이상 | soft_alert는 audit log만 — 사용자 명시로 조정 가능 |
| 5 | block trigger 자동 중단 vs WARN | 자동 중단 + 명시 인가 | block은 강한 신호 — 사용자 명시 정책 결정 |
| 6 | policy_revision mode 진입 인가 영역 | CLI flag + declaration 제출 | 사용자 명시 mode 진입 결정 |

---

## 13. 다음 Implementation Gate 조건 (7)

1. 사용자 명시 default threshold 값 확정
2. `policy_change_declaration_schema.json` 영구 파일 정의
3. `manifest_diff_classifier` read-only 측정 도구 implementation
4. alert severity 측정 도구 implementation
5. subject별 `configurable_thresholds.json` 신설
6. human review queue 구조 정의 (markdown 또는 별 파일)
7. tool_change_section / subject_change_section declaration 영역 정의

### 13.1 Implementation 수정/신규 파일 후보

| 파일 | scope |
|---|---|
| `docs/.../governance/policy_change_declaration_schema.json` (신규) | schema 영역 |
| `docs/.../governance/configurable_thresholds.json` (신규) | threshold default + subject override |
| `docs/.../governance/manifest_diff_classifier.py` (신규, 선택) | read-only 측정 도구 |
| `scripts/v_next_d3_input_creator.py` (수정) | hard_check_policy_design 정합 — mode-aware + governance declaration 입력 |
| `scripts/v_next_d3_parser_validator.py` (수정) | 94 hardcoded → mode-aware truthy |
| `human_review_queue/` (신규 디렉토리) | hard_alert 이상 진입 queue |

---

## 14. Claim Boundary

| claim | 본 design 상태 |
|---|---|
| 15 rule set + schema + 12 taxonomy + 10 labels + 4 severity + threshold + tool/subject section + D-4 workflow + 6 user decision + 7 next gate condition 명세 | (a) 명세 |
| Claude 웹 v0.2 규칙 검토 (R6 격하 / R9 분리 / R10/R11 유지 / R12 강화) | (a) 분석 |
| **automation 도구 구현** | **0** |
| **D-4 preview 실행** | **0** |
| **policy / selector / input_creator / parser_validator 실제 수정** | **0** |
| **generation / audit 실행** | **0** |
| **default threshold 값 확정** | **0** (사용자 명시 영역) |
| **policy_revision mode 진입 인가 결정** | **0** (사용자 명시 영역) |
| **commit / DEVLOG / Vault / MEMORY / decision JSONL 작성** | **0** |

---

## 15. 보호 영역 매트릭스 (전부 미수정 / 0)

automation 도구 구현 0 ✓ / D-4 preview 실행 0 ✓ / `scripts/v_next_d3_input_creator.py` 수정 0 ✓ / `scripts/v_next_d3_parser_validator.py` 수정 0 ✓ / `scripts/v_next_d3_pre_preview.py` 수정 0 ✓ / `scripts/v_next_d3_selector.py` 수정 0 ✓ / `scripts/explanation_synthesizer.py` 수정 0 ✓ / `app/data/questions.json` 수정 0 ✓ / D-2 sealed assets 0 ✓ / v_full handoff scope 0 ✓ / policy 실제 수정 0 ✓ / generation 실행 0 ✓ / audit 실행 0 ✓ / commit 0 ✓ / DEVLOG / Vault / MEMORY / decision JSONL 작성 0 ✓.

---

## 16. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_split/policy_change_governance_design.md` | 본 design 보고서 (16 섹션) |
| `v_next_results_d3_split/policy_change_governance_design.json` | machine-readable — 15 rule / schema / 12 taxonomy / 10 labels / 4 severity / 4 threshold / tool/subject section / D-4 workflow / 6 user decision / 7 next gate |

---

## 17. 최종 상태 판정

**판정 (primary)**: `READY_FOR_POLICY_GOVERNANCE_IMPLEMENTATION_GATE`
**판정 (secondary)**: `NEEDS_USER_DECISION_ON_THRESHOLDS`

### 핵심 근거

| 검증 기준 | 결과 |
|---|---|
| 15 rule set 명세 | ✓ |
| 13 schema field (required 12 + optional 3) | ✓ |
| 12 taxonomy transitions | ✓ |
| 10 movement labels | ✓ |
| 4 alert severity + configurable threshold | ✓ |
| Claude 웹 v0.2 규칙 검토 (R6/R9/R10/R11/R12) | ✓ |
| tool_change_section + subject_change_section | ✓ |
| D-4 7-step workflow + 6 entry conditions | ✓ |
| 6 user decision items + 7 next gate conditions | ✓ |
| `NEEDS_DESIGN_FIX` / `BLOCKED_BY_RULE_AMBIGUITY` 미해당 | ✓ |

다음 단계 (governance schema implementation + default threshold 확정 + mode-aware hard check + manifest diff classifier 도구) 진입은 사용자 명시 영역.

---

End of policy change governance layer design (design only) report.
