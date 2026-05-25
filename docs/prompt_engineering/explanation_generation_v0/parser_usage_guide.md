# v2 Input Parser — 사용 가이드

`scripts/v2_input_parser.py` (2026-05-25 신규 작성) 사용 방법.

이 가이드는 다음 사례를 다룬다:
- v3 batch generation cycle에서 inline parser 대신 본 parser 사용
- 단일 input 파일을 CLI로 parse
- pytest 회귀 검증 실행
- ID_PATTERN을 다른 모듈에서 재사용

---

## 1. Parser 위치

| 항목 | 경로 |
|---|---|
| Parser 본체 | `scripts/v2_input_parser.py` |
| pytest 단위 테스트 | `tests/unit/test_v2_input_parser.py` |
| 회귀 검증 보고 | `docs/prompt_engineering/explanation_generation_v0/parser_regression_2026-05-25.md` |
| 추정 가설 검증 본문 | `docs/prompt_engineering/explanation_generation_v0/parsing_bug_analysis_2026-05-25.md` §7 |

Parser는 다음 2개 함수를 export한다:
- `parse_input(path: str | Path) -> dict` — input 파일을 dict로 parse
- `ID_PATTERN` — 유효 id의 module-level compiled regex (`re.findall` / `re.match`에 재사용 가능)

---

## 2. Python에서 import + 사용

### 2.1 단일 input parse

```python
from pathlib import Path
import sys

# Repo root를 sys.path에 추가 (필요 시)
sys.path.insert(0, "/Users/jeong-ujin_1/Developer/ee-agent")

from scripts.v2_input_parser import parse_input

base = Path("docs/prompt_engineering/explanation_generation_v0/v2_inputs")
parsed = parse_input(base / "input_081.md")

print(parsed["problem"]["id"])
# → 2006_2회_84

print(parsed["related"]["same_core_candidates"])
# → ['2005_3회_85', '2019_2회_82', '2020_1회_86',
#    '2020_1,2회_91', '2020_4회_91', '2025_1회_81', '2025_1회_88']
# 합본 회차 '2020_1,2회_91'이 한 id로 유지됨 (OLD parser에서는 분리됨)
```

### 2.2 100 input 일괄 parse

```python
from pathlib import Path
from scripts.v2_input_parser import parse_input

base = Path("docs/prompt_engineering/explanation_generation_v0/v2_inputs")
all_parsed = {}
for n in range(1, 101):
    path = base / f"input_{n:03d}.md"
    all_parsed[n] = parse_input(path)

# 후보 통계
total_core = sum(
    len(p["related"]["same_core_candidates"]) for p in all_parsed.values()
)
total_trap = sum(
    len(p["related"]["same_trap_pattern_candidates"]) for p in all_parsed.values()
)
print(f"total same_core: {total_core}")
print(f"total same_trap_pattern: {total_trap}")
```

### 2.3 ID_PATTERN 재사용

ID_PATTERN은 module-level compiled regex로 export된다. 출력 검증, 별 데이터 처리에 재사용 가능:

```python
import re
from scripts.v2_input_parser import ID_PATTERN

# strict match는 fullmatch 또는 ^/$ 앵커로
STRICT_ID = re.compile(r"^\d{4}_(?:[1-6]회|1,2회)_\d+$")

candidates = ["2020_1회_91", "2020_1,2회_91", "2020_1", "broken_id"]
for c in candidates:
    valid = bool(STRICT_ID.match(c))
    print(f"{c}: {'valid' if valid else 'invalid'}")
# 2020_1회_91: valid
# 2020_1,2회_91: valid
# 2020_1: invalid
# broken_id: invalid
```

---

## 3. v2/v3 batch generation 강제 정책 (HARD)

다음 정책은 v2 재실행 / v3 batch / 5,331 v_full 진입 시 **반드시** 적용한다.

### 3.1 inline parser 재작성 금지

v2/v3/v_full batch generation cycle에서 inline Bash heredoc Python script로 parser 본문을 다시 작성하지 않는다. v2 batch에서 발견된 두 결함 (DOTALL greedy / 합본 회차 split) + 한 손실 (solution multi-line)은 inline 영구화의 직접 결과다.

### 3.2 import 강제

batch generation cycle의 Python script는 반드시 다음 import만 사용한다:

```python
from scripts.v2_input_parser import parse_input, ID_PATTERN
```

- `parse_input(path)` — input 파일을 dict로 parse
- `ID_PATTERN` — 출력 후 자가 검증용 compiled regex

본 import 없이 직접 `re.search(...)`로 input parsing을 수행하는 코드는 PR/cycle에서 reject 대상.

### 3.3 input 폴더 변경 시 사전 검증 의무

새 input 폴더 (예: `v3_inputs/`, `v_full_inputs/`, `v2_inputs_v2/`)를 만들면 **batch 실행 전에** 다음을 진행해야 한다:

1. `tests/unit/test_v2_input_parser.py`의 `V2_INPUTS` 상수를 새 폴더로 일시 변경하여 17 case가 모두 PASS하는지 확인
2. 또는 새 폴더 대상의 equivalent regression test 파일 작성 (`tests/unit/test_v3_input_parser.py` 등)
3. 입력 양식이 v2와 다르면 parser와 test를 함께 갱신

### 3.4 [문제] 섹션 양식 제약 (HARD)

현재 parser는 다음 양식 가정에 기반한다:
- `[문제]` 섹션에서 `solution:`은 **마지막 field**
- solution 본문은 섹션 끝까지 multi-line으로 이어짐
- `_split_sections`가 다음 `[section]` 헤더 전까지를 [문제] 섹션 본문으로 추출

**solution 뒤에 새 field를 추가하면 greedy solution parser가 해당 field까지 본문으로 흡수한다.** [문제] 섹션 템플릿을 변경할 경우 다음을 함께 갱신해야 한다:

- `scripts/v2_input_parser.py` 안의 solution 추출 regex
- `tests/unit/test_v2_input_parser.py`의 solution preservation 테스트 (test 11)

이 정책은 시간 절약을 위한 권장이 아니라 정확성 보장을 위한 hard rule이다.

---

## 4. v3 batch generation에서 inline parser 대체

v2 batch cycle에서는 다음과 같은 inline Bash heredoc Python script가 사용되었다 (parser 결함 포함):

```bash
# OLD (결함 있음) — v2 cycle 시점의 inline script
python3 <<'PYEOF'
import re
...
def parse_input(path):
    ...
    for fld_key, list_name in [...]:
        m = re.search(rf'^{fld_key}:\s*\[(.*)\]\s*$', rel_text,
                      re.MULTILINE | re.DOTALL)
        if m:
            related[list_name] = [
                x.strip() for x in m.group(1).replace('\n', '').split(',')
                if x.strip()
            ]
    ...
PYEOF
```

v3 batch cycle에서는 이 inline script를 다음과 같이 본 parser import로 대체한다:

```bash
# NEW (권장) — v3 cycle 진입 시 사용할 패턴
python3 <<'PYEOF'
import sys
sys.path.insert(0, "/Users/jeong-ujin_1/Developer/ee-agent")
from scripts.v2_input_parser import parse_input, ID_PATTERN
...
# inline script에서 직접 parse_input() 호출
# parser 본문을 다시 작성하지 않음 (재작성 금지)
parsed = parse_input(input_path)
related_core = parsed["related"]["same_core_candidates"][:5]
related_trap = parsed["related"]["same_trap_pattern_candidates"][:3]
# 추가 자가 검증 (안전 layer)
import re
STRICT_ID = re.compile(r"^\d{4}_(?:[1-6]회|1,2회)_\d+$")
for ids_list in [related_core, related_trap]:
    invalid = [x for x in ids_list if not STRICT_ID.match(x)]
    if invalid:
        # uncertainty_flags에 추가 + 해당 id 제외
        ids_list[:] = [x for x in ids_list if STRICT_ID.match(x)]
...
PYEOF
```

---

## 5. CLI로 parse 실행

`scripts/v2_input_parser.py`는 `__main__` 진입점을 가진다. 단일 input을 CLI로 parse + JSON 출력:

```bash
python3 scripts/v2_input_parser.py docs/prompt_engineering/explanation_generation_v0/v2_inputs/input_007.md
```

출력 예시 (JSON):
```json
{
  "problem": {
    "id": "2005_1회_33",
    "year": 2005,
    "session": "1회",
    "q_no": 33,
    "subject": "전기자기학",
    ...
  },
  "related": {
    "same_core_candidates": [
      "2007_1회_35",
      "2008_3회_1",
      "2010_1회_29",
      "2013_2회_21",
      "2016_2회_18"
    ],
    "same_trap_pattern_candidates": [
      "1998_2회_27",
      "1998_2회_41",
      "1998_2회_60",
      "1998_6회_62",
      "1998_4회_77"
    ]
  },
  ...
}
```

---

## 6. pytest 실행

### 6.1 단위 테스트 전수 실행

```bash
cd /Users/jeong-ujin_1/Developer/ee-agent
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/unit/test_v2_input_parser.py
```

`PYTHONDONTWRITEBYTECODE=1`은 `.pyc` 파일 생성을 차단하고, `-p no:cacheprovider`는 `.pytest_cache/` 생성을 차단한다. 본 정책은 캐시 / pyc 오염 회피를 위해 권장된 실행 양식이다.

예상 결과:
```text
tests/unit/test_v2_input_parser.py::test_normal_case_input_001_parses_all_sections PASSED
tests/unit/test_v2_input_parser.py::test_output_007_no_field_boundary_contamination PASSED
tests/unit/test_v2_input_parser.py::test_output_081_merged_round_id_kept_whole PASSED
tests/unit/test_v2_input_parser.py::test_candidate_poor_cases_exact_count[031-4] PASSED
tests/unit/test_v2_input_parser.py::test_candidate_poor_cases_exact_count[078-3] PASSED
tests/unit/test_v2_input_parser.py::test_candidate_poor_cases_exact_count[080-2] PASSED
tests/unit/test_v2_input_parser.py::test_empty_list_returns_empty_array PASSED
tests/unit/test_v2_input_parser.py::test_all_100_inputs_produce_strictly_valid_ids PASSED
tests/unit/test_v2_input_parser.py::test_id_pattern_matches_known_forms PASSED
tests/unit/test_v2_input_parser.py::test_id_pattern_rejects_split_fragments PASSED
tests/unit/test_v2_input_parser.py::test_solution_multi_line_preserved[001-295] PASSED
tests/unit/test_v2_input_parser.py::test_solution_multi_line_preserved[081-440] PASSED
tests/unit/test_v2_input_parser.py::test_solution_multi_line_preserved[002-605] PASSED
tests/unit/test_v2_input_parser.py::test_solution_multi_line_preserved[040-1220] PASSED
tests/unit/test_v2_input_parser.py::test_all_100_inputs_text_field_loss_under_5pct PASSED
tests/unit/test_v2_input_parser.py::test_all_100_inputs_have_question_text_choices_answer PASSED
tests/unit/test_v2_input_parser.py::test_input_007_choices_order_preserved PASSED
tests/unit/test_v2_input_parser.py::test_all_100_inputs_conflict_status_and_detail_preserved PASSED
tests/unit/test_v2_input_parser.py::test_all_100_inputs_trap_type_preserved PASSED
tests/unit/test_v2_input_parser.py::test_all_100_inputs_dynamic_link_preserved PASSED
============================== 20 passed in 0.66s ==============================
```

### 6.2 특정 케이스만 실행

```bash
# DOTALL greedy 회귀만
python3 -m pytest tests/unit/test_v2_input_parser.py::test_output_007_no_field_boundary_contamination -v

# 합본 회차 split 회귀만
python3 -m pytest tests/unit/test_v2_input_parser.py::test_output_081_merged_round_id_kept_whole -v

# 100 input 전수 검증만
python3 -m pytest tests/unit/test_v2_input_parser.py::test_all_100_inputs_produce_strictly_valid_ids -v
```

### 6.3 CI 통합 권장

`tests/unit/test_v2_input_parser.py`를 CI 파이프라인에 포함하여 다음을 자동 catch:
- v2_inputs 양식 변경 시 회귀
- parser 코드 수정 시 회귀 (특히 권장안 B의 regex / split / solution multi-line 보강 부분)
- 신규 input (v3, v_full) 추가 시 양식 정합

---

## 7. 회귀 검증 결과 요약

`docs/prompt_engineering/explanation_generation_v0/parser_regression_2026-05-25.md` 본문 요약:

| 항목 | OLD parser | NEW parser |
|---|---:|---:|
| 100 input 처리 | 100 | 100 |
| invalid id 발현 input | **100** (전수 결함 발현) | **0** ✓ |
| invalid id 개수 | **102** | **0** ✓ |
| output_007 contamination | 1 | 0 (FIXED) |
| output_031/078/080 contamination | 각 1 | 0 (FIXED) |
| output_081 합본 회차 split | 3 | 0 (FIXED) |

5 known bugs 전수 해결. 100 input 전수 strict regex 통과.

---

## 8. 알려진 한계 + 추가 권장 사항

### 8.1 알려진 한계

- **본 parser는 v2 input 양식 한정**: 다른 양식 (v_full, 다른 batch)에 적용 시 양식 변경 점검 필요
- **id 양식 변경 시 ID_PATTERN 갱신 필요**: 새 회차 양식 추가 시 (예: `7회` 또는 `반기제`) ID_PATTERN 정정
- **section name 변경 시 parser 갱신 필요**: 한국어 section header (`[문제]`, `[연관 문제 후보]` 등) 변경 시 parser 갱신

### 8.2 추가 권장 사항

- **system_prompt 가드 유지**: parser와 별 layer로 LLM 자가 검증 가드 유지 (`parsing_bug_analysis_2026-05-25.md` §4.1)
- **v3 batch cycle 즉시 적용**: inline parser 대신 본 parser import
- **v2 batch 재실행 시 고려**: 본 parser 사용 시 output 5건의 invalid id가 자동 정정됨
- **신규 입력 양식 변경 시 회귀 테스트 추가**: 새 양식 fixture를 `tests/unit/test_v2_input_parser.py`에 추가

---

## 9. 변경 사항 (2026-05-25)

| 구분 | 내용 |
|---|---|
| 신규 작성 | `scripts/v2_input_parser.py` (권장안 B 적용 — parser 영구 분리 + pytest 단위 테스트 + solution multi-line 보강. `parsing_bug_analysis_2026-05-25.md` §7.6의 regex / split / solution multi-line 보강 포함) |
| 신규 작성 | `tests/unit/test_v2_input_parser.py` (10 case) |
| 신규 작성 | `docs/prompt_engineering/explanation_generation_v0/parser_regression_2026-05-25.md` |
| 신규 작성 | `docs/prompt_engineering/explanation_generation_v0/parser_usage_guide.md` (본 파일) |

기존 파일 수정 0건:
- `docs/prompt_engineering/explanation_generation_v0/v2_inputs/` — 수정 안 함
- `docs/prompt_engineering/explanation_generation_v0/v2_results/` — 수정 안 함
- v2 batch generation cycle의 inline script — 회고용 분석만, 수정 안 함
- `app/`, `data/`, `docs/audit/`, `MEMORY.md`, Obsidian, JSONL decision_records — 수정 0
