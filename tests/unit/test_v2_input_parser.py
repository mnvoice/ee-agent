"""Regression tests for ``scripts/v2_input_parser.py``.

These tests pin down the two bugs that were confirmed in the inline parser
used during v2 batch generation:

1. DOTALL greedy contamination (outputs 007, 031, 078, 080)
2. Merged-round split (output 081)

See ``docs/prompt_engineering/explanation_generation_v0/parsing_bug_analysis_2026-05-25.md``
section 7 for the analysis.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.v2_input_parser import ID_PATTERN, parse_input  # noqa: E402

V2_INPUTS = (
    REPO_ROOT
    / "docs"
    / "prompt_engineering"
    / "explanation_generation_v0"
    / "v2_inputs"
)

STRICT_ID = re.compile(r"^\d{4}_(?:[1-6]회|1,2회)_\d+$")


# ---------------------------------------------------------------------------
# Test 1 — normal case
# ---------------------------------------------------------------------------


def test_normal_case_input_001_parses_all_sections():
    """input_001 has standard sections and clean candidates."""
    parsed = parse_input(V2_INPUTS / "input_001.md")

    assert parsed["problem"]["id"] == "2008_3회_1"
    assert parsed["problem"]["subject"] == "전기자기학"
    assert parsed["problem"]["answer"] == 1
    assert len(parsed["problem"]["choices"]) == 4

    assert parsed["v32"]["matched_core_id"] is None
    assert parsed["v32"]["matched_core_name"] == "전자파"
    assert parsed["v32"]["phenomenon_origin"] == "D/Dynamic"

    assert parsed["trap"]["is_trap_map_member"] is False
    assert parsed["dynamic"]["dynamic_link"] is not None

    same_core = parsed["related"]["same_core_candidates"]
    same_trap = parsed["related"]["same_trap_pattern_candidates"]
    assert len(same_core) == 10
    assert len(same_trap) == 5
    assert "1998_4회_17" in same_core
    assert "1998_2회_27" in same_trap


# ---------------------------------------------------------------------------
# Test 2 — output_007 regression (DOTALL greedy contamination)
# ---------------------------------------------------------------------------


def test_output_007_no_field_boundary_contamination():
    """input_007: same_core_candidates and same_trap_pattern_candidates are on
    adjacent lines. The inline parser used DOTALL+greedy and let the first
    list's match swallow the second list's closing bracket. The new parser
    must stop at the first ``]`` on the same line.
    """
    parsed = parse_input(V2_INPUTS / "input_007.md")

    same_core = parsed["related"]["same_core_candidates"]
    same_trap = parsed["related"]["same_trap_pattern_candidates"]

    # Exactly the candidates that appear in input_007.md.
    assert same_core == [
        "2007_1회_35",
        "2008_3회_1",
        "2010_1회_29",
        "2013_2회_21",
        "2016_2회_18",
    ]
    assert same_trap == [
        "1998_2회_27",
        "1998_2회_41",
        "1998_2회_60",
        "1998_6회_62",
        "1998_4회_77",
    ]

    # The previous bug produced an id like
    # "2016_2회_18]same_trap_pattern_candidates: [1998_2회_27".
    # That must never happen again.
    for candidate in same_core + same_trap:
        assert "]" not in candidate
        assert "[" not in candidate
        assert "same_core_candidates" not in candidate
        assert "same_trap_pattern_candidates" not in candidate
        assert "\n" not in candidate
        assert ":" not in candidate


# ---------------------------------------------------------------------------
# Test 3 — output_081 regression (merged-round split)
# ---------------------------------------------------------------------------


def test_output_081_merged_round_id_kept_whole():
    """input_081: same_core_candidates contains ``2020_1,2회_91`` which has an
    internal ``,``. The inline parser used ``split(',')`` and broke this id
    into ``2020_1`` and ``2회_91``. The new parser must keep it whole.
    """
    parsed = parse_input(V2_INPUTS / "input_081.md")

    same_core = parsed["related"]["same_core_candidates"]

    # The merged-round id must be present as a single entry.
    assert "2020_1,2회_91" in same_core
    # And the broken fragments from the previous bug must not be present.
    assert "2020_1" not in same_core
    assert "2회_91" not in same_core

    # Full list (input_081 has 7 candidates, including the merged-round one).
    assert same_core == [
        "2005_3회_85",
        "2019_2회_82",
        "2020_1회_86",
        "2020_1,2회_91",
        "2020_4회_91",
        "2025_1회_81",
        "2025_1회_88",
    ]


# ---------------------------------------------------------------------------
# Test 4 — candidate-poor cases (input_031, input_078, input_080)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "input_n, expected_same_core_count",
    [
        ("031", 4),
        ("078", 3),
        ("080", 2),
    ],
)
def test_candidate_poor_cases_exact_count(input_n, expected_same_core_count):
    """Candidate-poor inputs (031: 4 ids, 078: 3 ids, 080: 2 ids).

    The inline parser's bug was most visible on these inputs because the
    contaminated id ended up inside the ``[:5]`` slice. The new parser must
    extract exactly the documented number of candidates and never include a
    contaminated string.
    """
    parsed = parse_input(V2_INPUTS / f"input_{input_n}.md")
    same_core = parsed["related"]["same_core_candidates"]

    assert len(same_core) == expected_same_core_count
    for candidate in same_core:
        assert STRICT_ID.match(candidate), (
            f"id {candidate!r} from input_{input_n}.md does not match the "
            f"expected form ^YYYY_(N회|1,2회)_NN$"
        )


def test_empty_list_returns_empty_array(tmp_path):
    """A list field of the form ``key: []`` returns an empty array, not a
    list with a single empty string."""
    sample = tmp_path / "input_test.md"
    sample.write_text(
        "# v2 input 999: 전기기기 / test / empty_list\n\n"
        "[연관 문제 후보]\n"
        "same_core_candidates: []\n"
        "same_trap_pattern_candidates: []\n",
        encoding="utf-8",
    )
    parsed = parse_input(sample)
    assert parsed["related"]["same_core_candidates"] == []
    assert parsed["related"]["same_trap_pattern_candidates"] == []


# ---------------------------------------------------------------------------
# Test 5 — id format validation across all 100 inputs
# ---------------------------------------------------------------------------


def test_all_100_inputs_produce_strictly_valid_ids():
    """For every input_001.md ... input_100.md, every extracted id must match
    the strict form ``^YYYY_(N회|1,2회)_NN$``.
    """
    bad_ids = []
    for n in range(1, 101):
        path = V2_INPUTS / f"input_{n:03d}.md"
        parsed = parse_input(path)
        for field in ("same_core_candidates", "same_trap_pattern_candidates"):
            for candidate in parsed["related"][field]:
                if not STRICT_ID.match(candidate):
                    bad_ids.append((f"input_{n:03d}", field, candidate))

    assert not bad_ids, (
        f"{len(bad_ids)} ids do not match the strict form. "
        f"First few: {bad_ids[:5]}"
    )


def test_id_pattern_matches_known_forms():
    """``ID_PATTERN`` accepts the three known id shapes."""
    accepted = [
        "2020_1회_91",
        "2020_1,2회_91",
        "1998_6회_62",
        "2025_3회_100",
    ]
    for candidate in accepted:
        assert ID_PATTERN.fullmatch(candidate), candidate


def test_id_pattern_rejects_split_fragments():
    """``ID_PATTERN`` rejects the fragments produced by the old split bug."""
    rejected = [
        "2020_1",
        "2회_91",
        "2016_2회_18]same_trap_pattern_candidates: [1998_2회_27",
        "",
        "2020_1회_91 ",  # trailing space — fullmatch must reject
    ]
    for candidate in rejected:
        assert not ID_PATTERN.fullmatch(candidate), candidate


# ---------------------------------------------------------------------------
# Helper for tests 11~13
# ---------------------------------------------------------------------------


def _extract_section_raw(text: str, section_name: str) -> str:
    """Extract a [section] block's raw text from input file."""
    in_sec = False
    body = []
    for line in text.split("\n"):
        if line.strip() == f"[{section_name}]":
            in_sec = True
            continue
        stripped = line.strip()
        if (
            in_sec
            and stripped.startswith("[")
            and stripped.endswith("]")
            and stripped[1:-1].strip()
        ):
            break
        if in_sec:
            body.append(line)
    return "\n".join(body).strip()


def _extract_field_raw(section_text: str, field_name: str, multi_line: bool = False):
    if multi_line:
        pattern = rf"^{field_name}:\s*(.*?)(?=^[a-zA-Z_]+:|\Z)"
        match = re.search(pattern, section_text, re.MULTILINE | re.DOTALL)
    else:
        match = re.search(
            rf"^{field_name}:\s*(.+?)$", section_text, re.MULTILINE
        )
    if not match:
        return None
    return match.group(1).strip()


# ---------------------------------------------------------------------------
# Test 11 — solution multi-line preservation regression
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "input_n, expected_min_size",
    [
        ("001", 295),  # raw 301 chars (table-style solution)
        ("081", 440),  # raw 449 chars (multi-paragraph solution)
        ("002", 605),  # raw 611 chars (multi-paragraph + LaTeX)
        ("040", 1220),  # raw 1229 chars (long multi-section solution)
    ],
)
def test_solution_multi_line_preserved(input_n, expected_min_size):
    """solution must preserve multi-line content (>=95% of raw size).

    Regression for the bug where ``r'^solution:\\s*(.*?)$'`` + MULTILINE only
    captured the first line, losing 64.6% on average across the 100 inputs.
    """
    path = V2_INPUTS / f"input_{input_n}.md"
    parsed = parse_input(path)
    solution = parsed["problem"]["solution"] or ""

    prob_sec = _extract_section_raw(path.read_text(), "문제")
    raw_solution = _extract_field_raw(prob_sec, "solution", multi_line=True) or ""

    assert len(solution) >= expected_min_size, (
        f"input_{input_n} solution lost too much: parsed={len(solution)} "
        f"raw={len(raw_solution)}"
    )
    # And >=95% of the raw size
    if raw_solution:
        ratio = len(solution) / len(raw_solution)
        assert ratio >= 0.95, (
            f"input_{input_n} solution preservation ratio={ratio:.3f} "
            f"(parsed={len(solution)}, raw={len(raw_solution)})"
        )


# ---------------------------------------------------------------------------
# Test 12 — all 100 inputs, every text field within 5% loss budget
# ---------------------------------------------------------------------------


def test_all_100_inputs_text_field_loss_under_5pct():
    """For all 100 inputs, every text field (solution, question_text,
    essence_question, representative_trap, matched_core_name) must lose <5%
    of its raw character count.

    Choices, answer, candidate lists are validated by other tests (value
    equality, count, order, strict regex).
    """
    failures = []
    for n in range(1, 101):
        nnn = f"{n:03d}"
        path = V2_INPUTS / f"input_{nnn}.md"
        text = path.read_text()
        parsed = parse_input(path)

        prob_sec = _extract_section_raw(text, "문제")
        v32_sec = _extract_section_raw(text, "v3.2 라벨링 매칭 결과")

        checks = [
            ("solution", _extract_field_raw(prob_sec, "solution", multi_line=True),
             parsed["problem"].get("solution") or ""),
            ("question_text", _extract_field_raw(prob_sec, "question_text"),
             parsed["problem"].get("question_text") or ""),
            ("essence_question", _extract_field_raw(v32_sec, "essence_question"),
             parsed["v32"].get("essence_question") or ""),
            ("representative_trap", _extract_field_raw(v32_sec, "representative_trap"),
             parsed["v32"].get("representative_trap") or ""),
            ("matched_core_name", _extract_field_raw(v32_sec, "matched_core_name"),
             parsed["v32"].get("matched_core_name") or ""),
        ]

        for field, raw, parsed_val in checks:
            if not raw:
                continue
            loss = (len(raw) - len(parsed_val)) / len(raw)
            if loss > 0.05:
                failures.append(
                    (nnn, field, len(raw), len(parsed_val), round(loss * 100, 1))
                )

    assert not failures, (
        f"{len(failures)} field-level losses > 5%. First few: "
        f"{failures[:5]}"
    )


# ---------------------------------------------------------------------------
# Test 13 — non-text essential fields are extracted correctly
# ---------------------------------------------------------------------------


def test_all_100_inputs_have_question_text_choices_answer():
    """question_text, exactly 4 choices, and an integer answer are present
    for all 100 inputs."""
    missing = []
    for n in range(1, 101):
        nnn = f"{n:03d}"
        parsed = parse_input(V2_INPUTS / f"input_{nnn}.md")
        prob = parsed["problem"]
        if not prob.get("question_text"):
            missing.append((nnn, "question_text"))
        choices = prob.get("choices", {})
        if len(choices) != 4:
            missing.append((nnn, f"choices_count={len(choices)}"))
        if sorted(choices.keys()) != [1, 2, 3, 4]:
            missing.append((nnn, f"choices_keys={sorted(choices.keys())}"))
        if not isinstance(prob.get("answer"), int):
            missing.append((nnn, f"answer={prob.get('answer')!r}"))

    assert not missing, f"{len(missing)} issues found. First few: {missing[:5]}"


def test_input_007_choices_order_preserved():
    """Choices are extracted in the original 1..N order, not as a set."""
    parsed = parse_input(V2_INPUTS / "input_007.md")
    choices = parsed["problem"]["choices"]
    assert list(choices.keys()) == [1, 2, 3, 4]
    # Sanity-check that choice text is preserved (first ~20 chars of each)
    assert "금속수록" in choices[1] or "작을수록" in choices[1]
    assert "금속수록" in choices[2] or "클수록" in choices[2]
    assert "가늘수록" in choices[3]
    assert "가늘수록" in choices[4]


# ---------------------------------------------------------------------------
# Test 14~16 — metadata regression (conflict_status, trap_type, dynamic_link)
# ---------------------------------------------------------------------------


def _norm(value):
    """Normalize raw-vs-parsed for equality comparison.

    Treat the following as equivalent:
    - raw text ``"null"`` (literal string)
    - raw text ``""`` (empty)
    - parsed ``None``
    """
    if value is None:
        return None
    text = str(value).strip()
    if text in ("", "null"):
        return None
    return text


def test_all_100_inputs_conflict_status_and_detail_preserved():
    """For all 100 inputs, ``conflict_status`` and ``conflict_detail`` parsed
    values match the raw input.

    This pins the current v2 input format. If the [데이터 품질 사전 점검]
    section format changes, this test should be updated together with the
    parser.
    """
    mismatches = []
    for n in range(1, 101):
        nnn = f"{n:03d}"
        path = V2_INPUTS / f"input_{nnn}.md"
        parsed = parse_input(path)

        quality_sec = _extract_section_raw(path.read_text(), "데이터 품질 사전 점검")

        for field in ("conflict_status", "conflict_detail"):
            raw = _extract_field_raw(quality_sec, field)
            parsed_val = parsed["quality"].get(field)
            if _norm(raw) != _norm(parsed_val):
                mismatches.append(
                    (nnn, field, repr(raw), repr(parsed_val))
                )

    assert not mismatches, (
        f"{len(mismatches)} metadata mismatches in quality section. "
        f"First few: {mismatches[:5]}"
    )


def test_all_100_inputs_trap_type_preserved():
    """For all 100 inputs, ``trap_type`` parsed matches raw."""
    mismatches = []
    for n in range(1, 101):
        nnn = f"{n:03d}"
        path = V2_INPUTS / f"input_{nnn}.md"
        parsed = parse_input(path)

        trap_sec = _extract_section_raw(path.read_text(), "함정 지도 61항 매칭")
        raw = _extract_field_raw(trap_sec, "trap_type")
        parsed_val = parsed["trap"].get("trap_type")

        if _norm(raw) != _norm(parsed_val):
            mismatches.append((nnn, repr(raw), repr(parsed_val)))

    assert not mismatches, (
        f"{len(mismatches)} trap_type mismatches. First few: {mismatches[:5]}"
    )


def test_all_100_inputs_dynamic_link_preserved():
    """For all 100 inputs, ``dynamic_link`` parsed matches raw."""
    mismatches = []
    for n in range(1, 101):
        nnn = f"{n:03d}"
        path = V2_INPUTS / f"input_{nnn}.md"
        parsed = parse_input(path)

        dyn_sec = _extract_section_raw(path.read_text(), "동적 7항 매핑")
        raw = _extract_field_raw(dyn_sec, "dynamic_link")
        parsed_val = parsed["dynamic"].get("dynamic_link")

        if _norm(raw) != _norm(parsed_val):
            mismatches.append((nnn, repr(raw), repr(parsed_val)))

    assert not mismatches, (
        f"{len(mismatches)} dynamic_link mismatches. First few: {mismatches[:5]}"
    )
