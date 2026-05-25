# 2026-05-25 Parser and Supervisor Layer Decision

## Purpose

This record is the repo-local source of truth for the parser/supervisor-layer decision made before entering another v2 rerun or any v3 expansion.

It is intentionally operational. The richer reasoning trace is stored separately in Obsidian, while this file captures the decisions that future batch runs must obey.

## Context

The v2 explanation generation track exposed three classes of quality risk:

1. Input selection risk: `input_001` was selected for an `전자파` slot because its tag matched, while the actual question and solution were about `표피효과`.
2. Related-problem parsing risk: outputs `007`, `031`, `078`, and `080` contained field-boundary contamination such as `2016_2회_18]same_trap_pattern_candidates: [1998_2회_27`.
3. Merged-round id parsing risk: output `081` split `2020_1,2회_91` into `2020_1` and `2회_91`.

Later parser review found a fourth risk:

4. The first permanent parser draft fixed related-problem ids, but truncated multi-line `solution` content to the first line. That would preserve id hygiene while damaging explanation quality.

## Decisions

### Decision 1: Do not enter v3 yet

v3 expansion is blocked until the input selection algorithm and parser layer are both verified.

### Decision 2: Do not trust tag-only selection

Input selection must use the hard-filter and scoring policy in `input_selection_algorithm_v2.md`:

- tag alone is never sufficient.
- tag-content hard mismatch is excluded before score calculation.
- `input_001` style cases must be `EXCLUDE`, even if surface scoring would produce a `SUSPECT` range score.

### Decision 3: Use a permanent parser, not inline parser fragments

The batch pipeline must import `scripts/v2_input_parser.py` instead of rewriting parser logic inside temporary heredoc scripts.

The parser must be protected by pytest tests.

### Decision 4: Related-problem ids must be extracted by id regex

Candidate lists must not be split by comma. This is required because `1,2회` is a valid session value inside one id.

Required id pattern:

```regex
^\d{4}_(?:[1-6]회|1,2회)_\d+$
```

### Decision 5: Multi-line fields must be verified before rerun

Parser validation must not stop at related-problem candidates. It must verify that multi-line fields, especially `solution`, are preserved.

The first parser review found:

| input | raw solution length | parsed solution length | issue |
|---|---:|---:|---|
| input_001 | 301 | 57 | first line only |
| input_081 | 449 | 90 | first line only |

Therefore, v2 rerun is blocked until `solution` extraction is fixed and tested.

## Required Guardrails

Before any v2 rerun or v3 generation:

1. `scripts/v2_input_parser.py` preserves multi-line `solution`.
2. `tests/unit/test_v2_input_parser.py` includes regression tests for:
   - field-boundary contamination,
   - merged-round `1,2회` id preservation,
   - strict id validity over all 100 v2 inputs,
   - multi-line solution preservation,
   - appropriate field validation for string fields vs structured fields.
3. `parser_regression_2026-05-25.md` records field-loss validation results.
4. `parser_usage_guide.md` tells future batch runs to import the permanent parser.
5. Existing `v2_inputs/` and `v2_results/` remain unchanged during parser hardening.

## Validation Semantics

String fields should be checked by content preservation or loss ratio:

- `question_text`
- `solution`
- `matched_core_name`
- `essence_question`
- `dynamic_link`
- `trap_type`

Structured fields should not be checked by string length. They should be checked by equality, count, order, or strict regex:

- `answer`
- `choices`
- boolean fields
- candidate id arrays

## Current Risk Assessment

The Cloud Web direction was broadly correct:

- Permanent parser plus pytest is the right layer.
- v2 rerun is necessary before v3.
- v2 input reselection plus v2 rerun is the safest path after parser hardening.

Codex review corrected three overstatements or omissions:

- "100% underlying parser defect" is true for the old parser's full candidate arrays, but it does not mean every existing v2 output visibly contains invalid ids.
- The first permanent parser draft was not complete because it truncated multi-line `solution`.
- Field-loss tests must distinguish string fields from structured fields.

## Next Allowed Step

As of 2026-05-26, parser hardening is complete and verified.

Completed guardrails:

- `scripts/v2_input_parser.py` is the permanent parser for v2/v3 batch input parsing.
- `tests/unit/test_v2_input_parser.py` has 20 passing tests.
- Related id parsing rejects field-boundary contamination and preserves `1,2회`.
- Multi-line `solution` is preserved.
- Metadata regression tests pin `conflict_status`, `conflict_detail`, `trap_type`, and `dynamic_link`.
- `parser_regression_2026-05-25.md` and `parser_usage_guide.md` have no stray `영역` tokens.
- `option A` / `권장안 A` naming has been replaced with `권장안 B`.

Next allowed step:

1. Create `v2_inputs_v2/` using `input_selection_algorithm_v2.md`.
2. Do not run generation yet.
3. Validate the new `v2_inputs_v2/` folder with the permanent parser or equivalent checks before any v2 rerun.

Do not do these until `v2_inputs_v2/` is created and validated:

- v2 rerun
- v3 input generation
- v3 output generation
- app/data edits
- label edits
- commits

## Related Files

- `docs/prompt_engineering/explanation_generation_v0/input_selection_algorithm_v2.md`
- `docs/prompt_engineering/explanation_generation_v0/system_prompt.md`
- `docs/prompt_engineering/explanation_generation_v0/v2_quality_audit_report.md`
- `docs/prompt_engineering/explanation_generation_v0/parser_regression_2026-05-25.md`
- `docs/prompt_engineering/explanation_generation_v0/parser_usage_guide.md`
- `scripts/v2_input_parser.py`
- `tests/unit/test_v2_input_parser.py`
