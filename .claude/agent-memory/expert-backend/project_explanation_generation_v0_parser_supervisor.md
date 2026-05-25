---
name: Explanation Generation v0 Parser Supervisor
description: explanation_generation_v0 v2/v3 진입 전 parser hardening, input selection, 감독자 레이어 결정
type: project
---

Updated: 2026-05-26 KST.

**Current state:** parser hardening is complete. Next safe step is v2 input reselection only, creating `docs/prompt_engineering/explanation_generation_v0/v2_inputs_v2/`, followed by parser validation before any v2 rerun.

**Source of truth:**
- Repo decision record: `docs/prompt_engineering/explanation_generation_v0/decision_records/2026-05-25_parser_supervisor_layer_decision.md`
- Obsidian reasoning note: `/Users/jeong-ujin_1/Downloads/Documents/Obsidian Vault/ee-agent/2026-05-25_v2_parser_supervisor_raw_reasoning.md`
- Parser: `scripts/v2_input_parser.py`
- Tests: `tests/unit/test_v2_input_parser.py`

**Key decisions:**
- Do not enter v3 yet.
- Do not rerun v2 until new `v2_inputs_v2/` is created and validated.
- Use permanent parser import only: `from scripts.v2_input_parser import parse_input, ID_PATTERN`.
- Inline parser rewrites are forbidden for v2/v3/v_full generation.
- `1,2회` is part of a single id; never split candidate ids by comma.
- `[문제]` section must keep `solution:` as the final field unless parser/tests are updated together.
- `input_001` style tag-only mismatch must be hard-filtered before score calculation.
- raw session `1` means `1회`, but candidates with empty `question_text` remain excluded.

**Verified parser guardrails:**
- `pytest` for `tests/unit/test_v2_input_parser.py`: 20/20 pass.
- Related id contamination fixed.
- `2020_1,2회_91` preserved as one id.
- Multi-line `solution` preserved; prior first-line truncation fixed.
- Metadata regression pins `conflict_status`, `conflict_detail`, `trap_type`, and `dynamic_link`.
- `parser_regression_2026-05-25.md` and `parser_usage_guide.md` cleaned of stray `영역` tokens.
- `option A` / `권장안 A` naming removed; use `권장안 B`.

**Next workflow:**
1. Codex creates `v2_inputs_v2/` using `input_selection_algorithm_v2.md`.
2. Validate `v2_inputs_v2/` with permanent parser/equivalent checks.
3. Only then ask Claude CLI to run v2 generation into a new `v2_results_v2/` folder using the permanent parser import.
4. Re-audit v2 output before any v3 decision.

**Do not modify:** `app/data`, 5,331 problem data, labels, existing `v2_inputs/`, existing `v2_results/`, PDF/pdf_pages/app code, decision JSONL.
