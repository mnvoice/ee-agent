# v2 Parser Regression Report (2026-05-25)

`scripts/v2_input_parser.py` (신규 작성)와 v2 batch generation cycle에서 사용된 inline Bash heredoc Python parser의 회귀 비교 검증 결과.

- **source**: `docs/prompt_engineering/explanation_generation_v0/v2_inputs/input_001.md` ~ `input_100.md`
- **NEW parser**: `scripts/v2_input_parser.py` (권장안 B 적용 — parser 영구 분리 + pytest 단위 테스트, parsing_bug_analysis §7.6의 `re.MULTILINE only` + `[^\]]*` + `ID_PATTERN.findall()` 코드 수정 포함)
- **OLD parser**: v2 batch cycle inline script — `re.MULTILINE | re.DOTALL + (.*)` greedy regex + `split(',')` 사용
- **테스트 파일**: `tests/unit/test_v2_input_parser.py` (pytest 17 case, 모두 PASS — 2026-05-25 보강 후)

---

## 1. pytest 결과

```text
============================== 17 passed in 0.55s ==============================
```

(2026-05-25 보강 후 17 case 전수 통과 — solution multi-line 보강 + 전수 필드 손실 검증 추가)

기존 10 case:
- `test_normal_case_input_001_parses_all_sections` ✓
- `test_output_007_no_field_boundary_contamination` ✓ (DOTALL greedy 회귀)
- `test_output_081_merged_round_id_kept_whole` ✓ (합본 회차 split 회귀)
- `test_candidate_poor_cases_exact_count[031-4]` ✓
- `test_candidate_poor_cases_exact_count[078-3]` ✓
- `test_candidate_poor_cases_exact_count[080-2]` ✓
- `test_empty_list_returns_empty_array` ✓
- `test_all_100_inputs_produce_strictly_valid_ids` ✓
- `test_id_pattern_matches_known_forms` ✓
- `test_id_pattern_rejects_split_fragments` ✓

2026-05-25 보강 7 case:
- `test_solution_multi_line_preserved[001-295]` ✓ (input_001 solution >=295자)
- `test_solution_multi_line_preserved[081-440]` ✓ (input_081 solution >=440자)
- `test_solution_multi_line_preserved[002-605]` ✓ (input_002 solution >=605자)
- `test_solution_multi_line_preserved[040-1220]` ✓ (input_040 solution >=1220자)
- `test_all_100_inputs_text_field_loss_under_5pct` ✓ (전수 필드 손실 5% 미만)
- `test_all_100_inputs_have_question_text_choices_answer` ✓ (필수 필드 보존)
- `test_input_007_choices_order_preserved` ✓ (choices 순서 보존)

---

## 2. 100 input 회귀 검증 결과

| Parser | 처리 input | 유효 id 추출 | invalid id 개수 | invalid id가 있는 input |
|---|---:|---|---:|---:|
| **NEW parser** | 100 | 모두 strict regex 통과 | **0** | **0** |
| **OLD parser** (재현) | 100 | 일부 contamination | **102** | **100** |

→ **NEW parser는 100 input 전수에서 invalid id 0건**.
→ **OLD parser는 100 input 전수에서 invalid id 발현** (모든 input에 영향).

---

## 3. 5 known bugs 회귀 확인

| input | OLD invalid | NEW invalid | 상태 |
|---|---:|---:|---|
| input_007 | 1 | 0 | **FIXED** ✓ |
| input_031 | 1 | 0 | **FIXED** ✓ |
| input_078 | 1 | 0 | **FIXED** ✓ |
| input_080 | 1 | 0 | **FIXED** ✓ |
| input_081 | 3 | 0 | **FIXED** ✓ |

5건 known bugs 전수 해결.

---

## 4. 이전 parser와의 핵심 차이

### 4.1 OLD parser 결함 발현 패턴

OLD parser (inline script)는 100 input 전수에서 다음 형태의 invalid id를 발현:

- input_001~100: 마지막 same_core_candidates id 위치에 `]same_trap_pattern_candidates: [...` 패턴 contamination
- input_081: 위 contamination 외에 `2020_1,2회_91`이 `2020_1` + `2회_91`로 split (총 3 invalid)

### 4.2 v2 batch 출력에서 5건만 가시화된 이유

v2 batch cycle에서 inline parser는 100 input 전수에 동일 결함을 발생시켰으나, 출력 단계의 `[:5]` slice (스키마 maxItems=5)가 contamination을 가렸다:

- **후보 6건 이상 input**: contamination이 6번째 위치 이후로 밀려나서 `[:5]` slice가 정상 id만 통과시킴 → 가시화 0
- **후보 5건 이하 input (5건 + 후보 부족 case)**: contamination이 5번째 위치 안에 포함되어 `[:5]` slice 후에도 출력에 남음 → 가시화

가시화된 5건:
- output_007: 후보 5건 정확 (5번째 contamination 노출)
- output_031: 후보 4건 → 5번째 슬롯에 contamination 노출
- output_078: 후보 3건 → 4번째 슬롯에 contamination 노출
- output_080: 후보 2건 → 3번째 슬롯에 contamination 노출
- output_081: 합본 회차 split이 4번째+5번째 위치에 발현 (별 종류 버그)

### 4.3 5,331 적용 잠재 발현 추정 정정

`parsing_bug_analysis_2026-05-25.md` §5의 추정 (약 213건, v2 4/100 단순 환산)은 **출력 가시화 기준 추정**이다.

실제 결함 발생률은 100% (모든 input에 결함 발현). 단:
- 가시화 비율은 후보 수 분포에 의존 — 후보 5건 이하 case에서만 출력에 노출
- v2 100건 중 5건 가시화 = 5%
- 5,331 단순 환산 시 **가시화 잠재 발현 약 266건** (5% 적용)
- 실제 underlying 결함은 **100% (5,331건 전수)** — 단 [:5] slice가 가려서 출력 측정으로 catch 불가

### 4.4 NEW parser 개선

| 항목 | OLD | NEW |
|---|---|---|
| regex flags | `re.MULTILINE \| re.DOTALL` | `re.MULTILINE` only |
| capture pattern | `(.*)` greedy | `[^\]]*` character class |
| id 추출 | `split(',')` | `ID_PATTERN.findall()` |
| 합본 회차 처리 | 미고려 | `1,2회`를 ID_PATTERN에 명시 |
| 출력 검증 | 없음 | strict regex 정합 자동 확인 |

---

## 5. v3 batch 진입 권장 사항

본 회귀 검증 결과를 토대로 다음을 권장한다:

1. **v3 batch generation cycle에서 inline parser 사용 금지** — 본 `scripts/v2_input_parser.py`를 import하여 사용
2. **v2 batch 결과 재실행 시 본 parser 사용** (옵션) — output 5건의 invalid id가 자동 정정됨
3. **pytest를 CI 파이프라인에 추가** — input 양식 변경 시 회귀 자동 catch
4. **system_prompt 가드 (parsing_bug_analysis §4.1) 유지** — parser와 별 layer로 LLM 자가 검증 보강

---

---

## 6. 전체 필드 손실 측정 (2026-05-25 보강)

### 6.1 측정 배경

`scripts/v2_input_parser.py` 신규 작성 후 별 외부 검증에서 다음이 발견됨:

- input_001 raw solution 301자 → 보강 전 parser 결과 57자 (81% 손실)
- input_081 raw solution 449자 → 보강 전 parser 결과 90자 (80% 손실)

이는 solution 필드의 multi-line 추출 결함 — `re.search(r"^solution:\s*(.*?)$", ..., re.MULTILINE | re.DOTALL)`에서 `$` anchor + MULTILINE 조합이 첫 줄 끝에서 catch를 중단한 것.

### 6.2 보강 전 100 input 손실 측정

| 필드 | 손실 5% 이상 input | 평균 손실 | 최대 손실 |
|---|---:|---:|---:|
| **solution** | **74/100** | **64.6%** | 99.2% (input_002) |
| question_text | 0/100 | 0.0% | 0.0% |
| essence_question | 0/100 | 0.0% | 0.0% |
| representative_trap | 0/100 | 0.0% | 0.0% |
| matched_core_name | 0/100 | 0.0% | 0.0% |
| choices 4개 보존 | 100/100 ✓ | — | — |
| answer 정확 추출 | 100/100 ✓ | — | — |

→ **solution 단일 필드만 심각한 손실 발현**. 다른 text 필드 5개 + choices + answer는 모두 0% 손실 (정상).

### 6.3 보강 적용 — solution multi-line 수정

`scripts/v2_input_parser.py`의 solution 추출 코드 정정:

```python
# 보강 전 (결함)
solution_match = re.search(
    r"^solution:\s*(.*?)$", prob_text, re.MULTILINE | re.DOTALL
)
problem["solution"] = (
    solution_match.group(1).strip()[:2000] if solution_match else None
)

# 보강 후 (수정)
# solution은 [문제] 섹션의 마지막 field. _split_sections에서 이미 [문제]
# 섹션 본문만 추출했으므로 (.*) greedy는 섹션 끝까지만 catch.
# $ anchor 제거 + DOTALL 유지 + [:2000] truncation 제거
sol_match = re.search(r"^solution:\s*(.*)", prob_text, re.MULTILINE | re.DOTALL)
problem["solution"] = sol_match.group(1).strip() if sol_match else None
```

핵심 변경:
- `(.*?)` non-greedy → `(.*)` greedy
- `$` anchor 제거
- `[:2000]` truncation 제거 (사용자 명시: 가장 긴 solution이 약 1.5KB라 실질 영향 없으나 안전을 위해 명시 제거)

### 6.4 보강 후 100 input 재측정

| 필드 | 손실 5% 이상 input | 평균 손실 | 최대 손실 |
|---|---:|---:|---:|
| **solution** | **0/100** ✓ | **0.0%** ✓ | 0.0% ✓ |
| question_text | 0/100 | 0.0% | 0.0% |
| essence_question | 0/100 | 0.0% | 0.0% |
| representative_trap | 0/100 | 0.0% | 0.0% |
| matched_core_name | 0/100 | 0.0% | 0.0% |
| choices 4개 보존 | 100/100 ✓ | — | — |
| answer 정확 추출 | 100/100 ✓ | — | — |

input_001 + input_081 특정 catch:
- input_001: raw 301자 → parsed **301자** (100.0% 보존) ✓
- input_081: raw 449자 → parsed **449자** (100.0% 보존) ✓

### 6.5 보강 효과 요약

| 항목 | 보강 전 | 보강 후 |
|---|---|---|
| solution 평균 손실 | 64.6% | **0.0%** ✓ |
| solution 5% 이상 손실 input | 74/100 | **0/100** ✓ |
| 다른 4 text 필드 손실 | 0/100 (이미 정상) | 0/100 (유지) |
| pytest 통과 | 10/10 | **17/17** (보강 7 case 추가) |
| `[:2000]` truncation | 적용 | **제거** (사유: 가장 긴 solution 약 1.5KB, 본 양식에서 실질 영향 없음) |

---

## Status

- `scripts/v2_input_parser.py` 신규 작성 완료 (권장안 B 적용 — 영구 분리 + pytest 단위 테스트). 2026-05-25 보강: solution multi-line 추출 + truncation 제거.
- `tests/unit/test_v2_input_parser.py` 신규 작성 완료 (17 case, 전수 PASS). 보강 7 case 추가: solution multi-line preservation (4 parametrize) + 전수 필드 손실 5% 미만 + 필수 필드 보존 + choices 순서 보존.
- 100 input 회귀 검증 완료: NEW parser 0 invalid / OLD parser 102 invalid
- 5 known bugs (output_007/031/078/080/081) 모두 FIXED ✓
- 잠재 발현 추정 정정: 실제 결함 100% (5,331건 전수) / 가시화 5% (약 266건)
- 2026-05-25 보강: solution multi-line 손실 결함 catch + 정정 — 100건 평균 64.6% → 0.0% 손실
- 본 검증은 docs-only + parser 코드 자체 신규 작성 + 보강만 — v2_inputs / v2_results 파일 수정 0
- app/ / data/ / docs/audit/ / MEMORY.md 수정 0
- commit 0
