# D-3 Breaker Patch Implementation Report (B-only B2)

> 2026-05-27 KST. D-3 차단기 13건 unexpected expansion-empty B-only B2 sub-option 적용 + mechanical recovery 검증.
> 본 보고서는 mechanical recovery + 회귀 검증 결과. semantic gain / P5 필요 / D-4 필요 / 242 improved claim 0.

---

## 0. 핵심 한 줄

**Mechanical recovery 100% 성공 + 회귀 0 + 4차원 join 기대값 정확 일치**. 다음 상태 = `READY_FOR_BREAKER_PATCH_VERIFIED`.

---

## 1. 실제 수정 파일 + dl before / after

### 1.1 수정 파일

| 파일 | 줄 | 수정 내용 |
|---|---:|---|
| `scripts/v_next_d3_pre_preview.py` | 145 | dl 1줄 보정 (B2 sub-option) |

### 1.2 dl before / after

```
- "dl": "전력 차단기 -> 회로 단락전류 / 임피던스 환산",
+ "dl": "전력 차단기 -> 회로 단락전류 / 회로 임피던스 환산",
```

`회로` 1단어 추가. `회로 임피던스` 키 (`scripts/explanation_synthesizer.py:142`)가 `회로 임피던스 환산` 안에서 연속 substring으로 hit 되도록 구성.

### 1.3 미수정 파일 (보호 invariant 준수)

| 파일 | 상태 |
|---|---|
| `scripts/explanation_synthesizer.py` | 미수정 ✓ |
| `scripts/v_next_d3_selector.py` | 미수정 ✓ |
| `scripts/v_next_d3_input_creator.py` | 미수정 ✓ |
| `scripts/v_next_d3_parser_validator.py` | 미수정 ✓ |
| `scripts/v2_input_parser.py` | 미수정 ✓ |
| `app/data/questions.json` | 미수정 ✓ |
| D-2 sealed assets | 미수정 ✓ |
| v_full handoff scope | 미수정 ✓ |

---

## 2. Selector 결과 변경 범위 (input_creator 실행)

`input_creator.py` 재실행 (selector preview-only logic 재사용).

| 측정 | baseline | B | 변경 |
|---|---:|---:|---|
| input files | 94 | 94 | - |
| selection_manifest items | 94 | 94 | - |
| audit_group expansion | 57 | 57 | - |
| audit_group non_expansion_metadata | 37 | 37 | - |
| catalog | 51 | 51 | - |
| gap | 97 | 97 | - |
| selection_manifest 내 enriched_dynamic_link 변경 | - | - | **13** (전부 차단기) |
| selection_manifest 내 다른 81 항목 enriched_dynamic_link 변경 | - | - | **0** ✓ |

### 2.1 변경된 13건 (전부 차단기, 전부 동일 1줄 변경)

| pid | before | after |
|---|---|---|
| 1998_4회_22 | `전력 차단기 -> 회로 단락전류 / 임피던스 환산` | `전력 차단기 -> 회로 단락전류 / 회로 임피던스 환산` |
| 2000_2회_23 | (동일) | (동일) |
| 2001_3회_81 | (동일) | (동일) |
| 2002_1회_22 | (동일) | (동일) |
| 2002_3회_26 | (동일) | (동일) |
| 2003_1회_23 | (동일) | (동일) |
| 2003_1회_27 | (동일) | (동일) |
| 2004_1회_90 | (동일) | (동일) |
| 2004_3회_27 | (동일) | (동일) |
| 2004_3회_29 | (동일) | (동일) |
| 2004_3회_82 | (동일) | (동일) |
| 2005_1회_29 | (동일) | (동일) |
| 2008_1회_23 | (동일) | (동일) |

---

## 3. Input 재생성 결과

### 3.1 hardcoded 경로 위험 처리

`scripts/v_next_d3_input_creator.py:34` + `:325-345` — `V_NEXT_INPUTS_DIR = EG_DIR / "v_next_inputs_d3"` 정의되어 있어 hardcoded.

코드 수정 금지 정책 준수 + baseline 보존 위해 다음 절차 적용:

1. `cp -R v_next_inputs_d3 v_next_inputs_d3_baseline` (사전 backup)
2. `v_next_d3_input_creator.py` 실행 → `v_next_inputs_d3/` overwrite
3. baseline vs new diff 측정 (13건만 변경 확인)
4. `v_next_d3_parser_validator.py` 실행 (현재 `v_next_inputs_d3` = B에 대해 검증)
5. `explanation_synthesizer.py` 실행 (`v_next_inputs_d3` → `v_next_results_d3_b`)
6. audit 측정
7. `cp -R v_next_inputs_d3 v_next_inputs_d3_b` (B 보존)
8. `rm v_next_inputs_d3 + mv v_next_inputs_d3_baseline v_next_inputs_d3` (baseline 복원)

### 3.2 input_*.md 파일 변경

| 측정 | 값 |
|---|---:|
| 변경된 input_*.md | **13** / 94 |
| 변경된 줄 (per file) | 1 (`dynamic_link:` 줄만) |
| 다른 81 input_*.md | 변경 0 |

샘플 변경 (input_003.md L57):
```
- dynamic_link: 전력 차단기 -> 회로 단락전류 / 임피던스 환산
+ dynamic_link: 전력 차단기 -> 회로 단락전류 / 회로 임피던스 환산
```

### 3.3 사후 디렉토리 상태

| 디렉토리 | 내용 |
|---|---|
| `v_next_inputs_d3/` | **baseline 복원** (dl 원본 `회로 단락전류 / 임피던스 환산`) |
| `v_next_inputs_d3_b/` | **B 보존** (dl B `회로 단락전류 / 회로 임피던스 환산`) |
| `v_next_results_d3/` | **baseline 결과** (D-3 paired audit 산출 포함) |
| `v_next_results_d3_b/` | **B 결과** (94 outputs + JSONL + summary + audit JSON + 본 보고서) |

---

## 4. Parser Validation 결과 (B 입력)

| 항목 | 결과 |
|---|---|
| generated | 94 / 94 ✓ |
| parse PASS | 94 / 94 ✓ |
| related_id_violations | 0 ✓ |
| duplicates | 0 ✓ |
| invalid answers | 0 ✓ |
| choices != 4 | 0 ✓ |
| missing question_text | 0 ✓ |
| missing solution | 0 ✓ |
| preview = generated | True ✓ |
| evidence_field tag = 0 | True ✓ |
| audit_group expansion | 57 ✓ |
| audit_group non_expansion_metadata | 37 ✓ |
| enriched 4 field present | 94 / 94 ✓ |
| gap_report | 148 (catalog 51 + gap 97) ✓ |

판정: `READY_FOR_D3_GENERATION_GATE` (B에 대해서도 baseline 동일 판정).

---

## 5. Generation 결과 (v_next_results_d3_b)

| 항목 | baseline | B |
|---|---:|---:|
| generated | 94 | 94 |
| schema PASS | 94 | 94 |
| schema FAIL | 0 | 0 |
| related_id_violations | 0 | 0 |
| parser contamination | 0 | 0 |
| subject (전력공학) | 94 | 94 |
| phen_origin D/Dynamic | 30 | 30 |
| phen_origin S/Fault | 27 | 27 |
| phen_origin S/Static | 37 | 37 |
| correct_type dynamic | 30 | 30 |
| correct_type fault_compression | 27 | 27 |
| correct_type static_formula | 37 | 37 |
| distractor total | 282 | 282 |
| distractor with input.trap_type | 282 | 282 |
| uncertainty () | 72 | 72 |
| uncertainty candidate_pool_small | 22 | 22 |
| **expansion_source dl_keyword** | **44** | **57** (+13) |
| **expansion_source empty** | **50** | **37** (-13) |
| audit-only flag matched_core_id_null | 94 | 94 |
| audit-only flag cross_subject_hints_empty | 94 | 94 |
| self_corrections | 0 | 0 |

→ dl_keyword 분포만 baseline 44 → B 57 (+13 차단기 회복). 다른 분포 100% 정합.

---

## 6. 4차원 Join 결과 (audit_group × expansion_source)

| cell | baseline | B | 변경 |
|---|---:|---:|---|
| (expansion, dl_keyword) | 44 | **57** | +13 |
| (expansion, empty) | 13 | **0** | -13 (전부 회복) |
| (non_expansion_metadata, dl_keyword) | 0 | 0 | - |
| (non_expansion_metadata, empty) | 37 | 37 | - |

사용자 기대값 정확 일치:
- `(expansion, dl_keyword) = 57` ✓
- `(expansion, empty) = 0` ✓
- `(non_expansion_metadata, empty) = 37` ✓

---

## 7. 차단기 13건 회복 여부

| 측정 | 값 |
|---|---:|
| breaker input set | 13 / 13 ✓ |
| breaker recovered (empty → dl_keyword) | **13 / 13** ✓ |
| breaker expands_count change | 0 → 1 (전건, target=회로이론) |

회복된 13건 전부 동일 패턴:
- `cross_subject_expansion.expands_to` = `[{"target_subject": "회로이론", "via_concept": "전력 차단기 → 회로이론: ... 회로 임피던스 환산 ... 경로", "connection_type": "fault_rule_transfer"}]`
- expansion_source = "dl_keyword"

→ `회로 임피던스` 키가 새 dl `회로 임피던스 환산` 안에서 연속 substring hit (`scripts/explanation_synthesizer.py:223` `if kw in dl`).

---

## 8. 기존 성공 44건 유지 여부

| 측정 | 값 |
|---|---:|
| baseline (expansion, dl_keyword) | 44 |
| B (expansion, dl_keyword) − 13 회복 | 57 − 13 = 44 |
| **44건 dl_keyword 유지** | ✓ |

44건 중 어떤 항목도 src 변경 0. expansion_target_subjects / expansion_via_concepts 변경 0.

---

## 9. non_expansion_metadata 37건 보호 여부

| 측정 | 값 |
|---|---:|
| baseline (non_expansion_metadata, empty) | 37 |
| B (non_expansion_metadata, empty) | 37 ✓ |
| (non_expansion_metadata, dl_keyword) | 0 (baseline / B 모두) ✓ |

37건 중 어떤 항목도 expansion 부당 발현 0. dl=None 정직 정합 유지.

---

## 10. 81건 의미 필드 회귀 검증

검증 대상 의미 필드 (사용자 명시):
- `phenomenon_origin` (learning_meta)
- `correct_type` (answer_analysis)
- `core_extraction.phenomenon`
- `core_extraction.trap_pattern`
- `distractor_analysis[].trap_type` (전체 tuple)
- `uncertainty_flags` (sorted tuple)
- `cross_subject_expansion.expands_to[].target_subject` (tuple)
- `cross_subject_expansion.expands_to[].via_concept` (tuple)
- `related_problems.same_core` (tuple)
- `related_problems.same_trap_pattern` (tuple)

### 10.1 non-breaker 81 측정 결과

| 측정 | 값 |
|---|---:|
| non-breaker rows | 81 / 81 |
| **rows with any semantic field differing** | **0** ✓ |
| field diff counts (per-field) | `{}` (전부 0) |

→ **81건 의미 필드 완전 보존**. 회귀 0.

### 10.2 breaker 13 의미 변경 (예상 영역만)

| 필드 | 변경 건수 | 영역 |
|---|---:|---|
| phenomenon | 13 | phenomenon 텍스트에 dl 표현 포함 (예상) |
| expansion_target_subjects | 13 | empty → 회로이론 (회복 영역) |
| expansion_via_concepts | 13 | empty → "회로 임피던스 환산 경로" (회복 영역) |
| phenomenon_origin | 0 ✓ | S/Fault 유지 |
| correct_type | 0 ✓ | fault_compression 유지 |
| trap_pattern | 0 ✓ | 차단 용량 vs 차단 시간 혼동 함정 유지 |
| distractor_trap_types | 0 ✓ | 함정 유형 유지 |
| uncertainty_flags | 0 ✓ | 빈 [] 유지 |
| related_same_core | 0 ✓ | same_core 5건 유지 |
| related_same_trap | 0 ✓ | same_trap 3건 유지 |

→ 차단기 의미 변경은 cross_subject_expansion 영역 + phenomenon 텍스트 (dl 인용) 만. 의도 영역 정확 일치.

---

## 11. A1/A2 추가 필요 여부 판단

| 후보 | 현 상태 평가 |
|---|---|
| A1c (`회로 단락전류` 키 추가) | B-only로 13/13 회복 + 회로이론 1 target 부착. **현 단계에서 A1 추가 불필요**. multi-target (회로이론 + 전기설비기술기준 / 전기기기) 회복 필요성은 별 게이트 결정 영역 (semantic 판정 영역). |
| A2a (matched_core_fallback `차단기` 추가) | 현 dl path로 회복 충족. fallback 진입 0 → **현 단계에서 A2 불필요**. 미래 차단기 dl 변형 회복 필요성도 별 게이트. |
| A+B 결합 | sequential 정합 — B 결과로 충족. **현 단계 결합 진행 불필요**. |
| C 재분류 | **REJECTED** (이미 design 단계에서 기각, B 회복으로 자연 정당화). |

**판정**: 현 단계 추가 patch 0. step 4 (multi-target 필요 결정) 별 사용자 명시 게이트로 분리.

---

## 12. 다음 상태 판정

**판정**: `READY_FOR_BREAKER_PATCH_VERIFIED`

### 판정 근거

| 검증 기준 | 결과 |
|---|---|
| parser validation 94/94 PASS | ✓ |
| audit_group expansion 57 / non_expansion_metadata 37 유지 | ✓ |
| selection_manifest enriched_dynamic_link 변경 = 13 (전부 차단기) | ✓ |
| 81 비차단기 enriched_dynamic_link 변경 0 | ✓ |
| v_next_results_d3_b 차단기 13건 cross_subject_expansion non-empty | ✓ (13/13, expands 0→1) |
| (expansion, dl_keyword) = 57 | ✓ |
| (expansion, empty) = 0 | ✓ |
| (non_expansion_metadata, empty) = 37 | ✓ |
| 기존 성공 44건 유지 | ✓ |
| non_expansion_metadata 37건 부당 expansion 0 | ✓ |
| 81 의미 필드 회귀 0 | ✓ |
| 차단기 13 의미 변경 = phenomenon + expansion 영역만 (예상) | ✓ |

12 / 12 검증 통과.

### 부수적 상태 옵션 (판정 대안 아님)

- `NEEDS_A1_KEYWORD_DESIGN_AFTER_B_ONLY_RESULT`: 미해당 — B-only로 13/13 회복, multi-target 필요는 별 게이트 결정 영역
- `BREAKER_PATCH_REGRESSION_FOUND`: 미해당 — 회귀 0
- `BLOCKED_BY_OUTPUT_PATH_RISK`: 미해당 — baseline backup + 사후 분리 + dl restore로 정합 처리

---

## 13. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_b/output_001.json` ~ `output_094.json` | 94 B outputs |
| `v_next_results_d3_b/generated_explanations_v_next_results_d3_b.jsonl` | JSONL (94 lines) |
| `v_next_results_d3_b/_synthesizer_summary.json` | summary |
| `v_next_results_d3_b/d3_breaker_patch_implementation_audit.json` | 4차원 join + per-row source change + breaker recovery + non-breaker regression + breaker semantic changes (machine-readable) |
| `v_next_results_d3_b/d3_breaker_patch_implementation_report.md` | 본 보고서 |
| `v_next_inputs_d3_b/` | B 입력 (selection_manifest + input_*.md + parser_validation_report 등) |

git commit / DEVLOG / Vault / MEMORY / decision JSONL 0 (사용자 명시 금지 준수).

---

## 14. dl patch 상태 (`scripts/v_next_d3_pre_preview.py:145`)

| 상태 | 값 |
|---|---|
| 현재 file 상태 | **B (보정 dl 유지)** — `"전력 차단기 -> 회로 단락전류 / 회로 임피던스 환산"` |
| baseline dl 위치 | `v_next_inputs_d3/selection_manifest.json` (복원됨) + `v_next_inputs_d3_baseline/` (작업 중 삭제됨, 현 baseline = restored) |
| B dl 위치 | `v_next_inputs_d3_b/selection_manifest.json` + `v_next_results_d3_b/` outputs |

**rationale**: 사용자가 본 implementation 게이트에서 dl patch를 명시 승인. patch 유지는 자연스러움. 단 baseline 복원 정합성 측면에서 다음 게이트에서 patch 원상복구 vs 유지 결정은 별 사용자 명시 영역.

만약 원상복구 필요 시: `scripts/v_next_d3_pre_preview.py:145`의 `회로 임피던스 환산` → `임피던스 환산` 1단어 제거.

---

## 15. 보호 영역 매트릭스

| 보호 대상 | 상태 |
|---|---|
| `scripts/explanation_synthesizer.py` | 미수정 ✓ |
| `scripts/v_next_d3_selector.py` | 미수정 ✓ |
| `scripts/v_next_d3_input_creator.py` | 미수정 ✓ |
| `scripts/v_next_d3_parser_validator.py` | 미수정 ✓ |
| `scripts/v2_input_parser.py` | 미수정 ✓ |
| `app/data/questions.json` | 미수정 ✓ |
| D-2 sealed assets | 미수정 ✓ |
| v_full handoff scope | 미수정 ✓ |
| keyword map / fallback | 미수정 ✓ |
| A1 / A2 동시 적용 | 0 ✓ |
| D-4 진입 | 0 ✓ |
| P5 sample experiment | 0 ✓ |
| catalog/gap rescue | 0 ✓ |
| commit | 0 ✓ |
| DEVLOG / Vault / MEMORY / decision JSONL 작성 | 0 ✓ |

---

## 16. claim boundary 점검

| claim | 본 보고서 상태 |
|---|---|
| Mechanical recovery 13/13 (empty → dl_keyword) | (a) 측정 — 4차원 join + per-row source change |
| 81 비차단기 의미 필드 회귀 0 | (a) 측정 — 10 semantic field × 81 rows × tuple diff |
| audit_group 분포 유지 (57/37) | (a) 측정 |
| baseline 결과 보존 (v_next_results_d3 미변경) | (a) 측정 — 별 디렉토리 출력 |
| Semantic gain (회복된 expansion의 학습 가치) | **claim 0** — 별 sampling / P5 영역 |
| P5 필요 | **claim 0** |
| D-4 진입 필요 | **claim 0** |
| 242 improved | **claim 0** |
| Multi-target 회복 필요 여부 | **claim 0** — step 4 별 게이트 |
| dl patch 원상복구 vs 유지 결정 | **claim 0** — 별 사용자 결정 |

---

End of D-3 breaker patch implementation report (B-only B2).
