"""v2 input parser for explanation_generation_v0 batch pipeline.

This module replaces the inline Bash heredoc Python script that was used during
v2 batch generation. It applies the fix recommended in
``docs/prompt_engineering/explanation_generation_v0/parsing_bug_analysis_2026-05-25.md``
section 7.6 (권장안 B — parser 영구 분리 + pytest 단위 테스트 + solution multi-line 보강).

Two bugs were confirmed in the inline parser used during v2 batch generation:

1. DOTALL greedy contamination
   - Symptom: outputs 007, 031, 078, 080 had the 5th id of ``same_core``
     contaminated with the following list literal text, e.g. the last id became
     ``"2016_2회_18]same_trap_pattern_candidates: [1998_2회_27"``.
   - Cause: ``re.MULTILINE | re.DOTALL`` together with ``(.*)`` greedy capture
     allowed the ``.*`` group to swallow the newline and the second list's
     closing bracket.
   - Fix: drop DOTALL and use a ``[^\\]]*`` character class so the match stops
     at the first ``]`` on the same line.

2. Merged-round split
   - Symptom: output 081 had ``"2020_1,2회_91"`` split into ``"2020_1"`` and
     ``"2회_91"`` because the parser called ``split(',')`` on a string that
     contained a merged-round id with an internal comma.
   - Fix: extract ids with the ``ID_PATTERN`` regex instead of splitting on
     commas; the pattern matches the ``1,2회`` alternative explicitly.

Public API
----------
- ``ID_PATTERN``: module-level compiled regex that matches a valid related id.
- ``parse_input(path)``: read a v2 input markdown file and return a dict with
  the parsed sections used by the explanation generator.

Example
-------
::

    from scripts.v2_input_parser import parse_input, ID_PATTERN

    parsed = parse_input("docs/prompt_engineering/explanation_generation_v0/"
                         "v2_inputs/input_081.md")
    assert "2020_1,2회_91" in parsed["related"]["same_core_candidates"]
    for candidate in parsed["related"]["same_core_candidates"]:
        assert ID_PATTERN.match(candidate)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ID_PATTERN = re.compile(r"\d{4}_(?:[1-6]회|1,2회)_\d+")
"""Compiled regex that matches a valid related-problem id.

Form: ``YYYY_{회차}_NN`` where 회차 is ``1회`` .. ``6회`` or ``1,2회``.

Used in two places:

1. To extract ids from the captured group of ``same_core_candidates`` and
   ``same_trap_pattern_candidates``. This handles the merged-round id form
   ``YYYY_1,2회_NN`` correctly because the ``,`` is inside the regex, not a
   split delimiter.
2. To validate that every produced id matches the expected form. The strict
   form ``^...$`` is used for validation; see ``_id_is_valid``.
"""

_ID_PATTERN_STRICT = re.compile(r"^\d{4}_(?:[1-6]회|1,2회)_\d+$")

_SECTION_HEADER = re.compile(r"^\[([^\]]+)\]\s*$")

_LIST_LINE_TEMPLATE = r"^{fld}:\s*\[([^\]]*)\]\s*$"
"""Regex template for a single-line ``key: [...]`` list field.

Note the use of ``[^\\]]*`` (non-``]`` characters) instead of ``(.*)``. This is
the fix for the DOTALL greedy contamination bug: the match cannot cross a
``]`` character, so it always stops at the first closing bracket on the same
line. We also drop ``re.DOTALL`` from the search call.
"""

_CHOICE_LINE_NUMERIC = re.compile(r"^\s+(\d+)[.:]\s*(.+)$")
_CHOICE_LINE_CIRCLED = re.compile(r"^\s+([①②③④⓵⓶⓷⓸❶❷❸❹])\s*(.+)$")
_CHOICE_LINE_PAREN = re.compile(r"^\s+\((\d+)\)\s*(.+)$")
_CIRCLED_MAP = {
    "①": 1, "②": 2, "③": 3, "④": 4,
    "⓵": 1, "⓶": 2, "⓷": 3, "⓸": 4,
    "❶": 1, "❷": 2, "❸": 3, "❹": 4,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _id_is_valid(candidate: str) -> bool:
    """Return True iff ``candidate`` is a valid related-problem id."""
    return bool(_ID_PATTERN_STRICT.match(candidate))


def _split_sections(text: str) -> Dict[str, str]:
    """Split a v2 input markdown text into ``[section name]`` blocks.

    The header line ``# v2 input NNN: ...`` is not a section; it is ignored.
    Body lines preceding the first ``[section]`` header are also ignored.
    """
    sections: Dict[str, str] = {}
    current: Optional[str] = None
    body: List[str] = []

    for line in text.split("\n"):
        match = _SECTION_HEADER.match(line)
        if match:
            if current is not None:
                sections[current] = "\n".join(body)
            current = match.group(1)
            body = []
        else:
            if current is not None:
                body.append(line)
    if current is not None:
        sections[current] = "\n".join(body)
    return sections


def _parse_single_value(text: str, field: str) -> Optional[str]:
    match = re.search(rf"^{field}:\s*(.+)$", text, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    return None if value in ("null", "") else value


def _parse_int_value(text: str, field: str) -> Optional[Union[int, str]]:
    raw = _parse_single_value(text, field)
    if raw is None:
        return None
    try:
        return int(raw)
    except ValueError:
        return raw


def _parse_list_field(text: str, field: str) -> List[str]:
    """Extract a single-line ``key: [...]`` list field as a list of ids.

    This is the fixed extractor. It uses ``[^\\]]*`` to avoid DOTALL greedy
    contamination, and uses ``ID_PATTERN.findall`` instead of splitting on
    commas to preserve the merged-round id form ``YYYY_1,2회_NN``.
    """
    pattern = _LIST_LINE_TEMPLATE.format(fld=re.escape(field))
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return []
    inside = match.group(1)
    return ID_PATTERN.findall(inside)


def _parse_choices(prob_text: str) -> Dict[int, str]:
    """Parse the ``choices:`` block. Supports numeric, circled, and ``(N)``."""
    choices: Dict[int, str] = {}
    in_choices = False
    for line in prob_text.split("\n"):
        if re.match(r"^choices:\s*$", line):
            in_choices = True
            continue
        if not in_choices:
            continue
        for pattern in (_CHOICE_LINE_NUMERIC, _CHOICE_LINE_PAREN):
            match = pattern.match(line)
            if match:
                choices[int(match.group(1))] = match.group(2).strip()
                break
        else:
            match = _CHOICE_LINE_CIRCLED.match(line)
            if match:
                number = _CIRCLED_MAP.get(match.group(1))
                if number:
                    choices[number] = match.group(2).strip()
                continue
            if re.match(r"^\S", line):
                in_choices = False
    return choices


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_input(path: Union[str, Path]) -> Dict[str, Any]:
    """Parse a v2 input markdown file into a structured dict.

    Parameters
    ----------
    path:
        Filesystem path to ``input_NNN.md``.

    Returns
    -------
    dict
        Keys: ``problem``, ``quality``, ``v32``, ``trap``, ``dynamic``,
        ``cross_subject_hints``, ``related``, ``header_subject``.

    Notes
    -----
    Every id returned in ``related["same_core_candidates"]`` and
    ``related["same_trap_pattern_candidates"]`` is guaranteed to match
    ``ID_PATTERN``; ill-formed ids in the input are silently dropped.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")

    # Header subject (line 1)
    header_subject = None
    header_match = re.match(r"^#\s+v2 input \d+:\s*(.+)$", text.split("\n")[0])
    if header_match:
        parts = [p.strip() for p in header_match.group(1).split("/")]
        if parts:
            header_subject = parts[0]

    sections = _split_sections(text)

    # 문제 section
    prob_text = sections.get("문제", "")
    problem: Dict[str, Any] = {}
    for field in ("id", "year", "session", "q_no", "subject", "question_text"):
        value = _parse_single_value(prob_text, field)
        if value is None:
            continue
        if field in ("year", "q_no"):
            try:
                problem[field] = int(value)
            except ValueError:
                problem[field] = value
        else:
            problem[field] = value
    answer = _parse_int_value(prob_text, "answer")
    if answer is not None:
        problem["answer"] = answer
    problem["choices"] = _parse_choices(prob_text)
    # solution: [문제] 섹션의 마지막 field. 'solution:' 라벨 이후부터 섹션 끝까지
    # 모두 추출 (multi-line 본문 보존).
    #
    # 결함 catch: 이전 구현은 ``r"^solution:\s*(.*?)$"`` + ``re.MULTILINE | re.DOTALL``
    # + ``[:2000]`` truncation. ``$`` + MULTILINE 조합이 line end에서 catch를 중단해
    # 첫 줄만 추출됨 (input_001/081 측정: 평균 64.6% 손실, 74/100 input에서 5% 이상
    # 손실 발현). 자세한 측정 결과는 parser_regression_2026-05-25.md §6.
    #
    # 수정: ``$`` anchor 제거 + DOTALL 유지. ``prob_text``는 ``_split_sections``에서
    # 이미 [문제] 섹션 본문만 추출되었으므로 ``(.*)`` greedy는 섹션 끝까지만 catch.
    # truncation도 제거 — 본 양식의 가장 긴 solution이 약 1.5KB라 2000자 제한은
    # 실질 영향이 작으나 안전을 위해 명시적으로 제거.
    sol_match = re.search(r"^solution:\s*(.*)", prob_text, re.MULTILINE | re.DOTALL)
    problem["solution"] = sol_match.group(1).strip() if sol_match else None

    # 데이터 품질 사전 점검
    quality_text = sections.get("데이터 품질 사전 점검", "")
    quality: Dict[str, Optional[str]] = {}
    for field in ("conflict_status", "conflict_detail"):
        quality[field] = _parse_single_value(quality_text, field)

    # v3.2 라벨링 매칭 결과
    v32_text = sections.get("v3.2 라벨링 매칭 결과", "")
    v32: Dict[str, Any] = {}
    for field in (
        "matched_core_id", "matched_core_name", "ds_class",
        "phenomenon_origin", "essence_question", "memorize_hint",
        "representative_trap",
    ):
        v32[field] = _parse_single_value(v32_text, field)
    v32["star"] = _parse_int_value(v32_text, "star")
    six_axis_match = re.search(
        r"^six_axis:\s*\[([^\]]*)\]\s*$", v32_text, re.MULTILINE
    )
    if six_axis_match:
        v32["six_axis"] = [
            item.strip()
            for item in six_axis_match.group(1).split(",")
            if item.strip()
        ]
    else:
        v32["six_axis"] = []

    # 함정 지도 61항 매칭
    trap_text = sections.get("함정 지도 61항 매칭", "")
    trap: Dict[str, Any] = {}
    is_trap_raw = _parse_single_value(trap_text, "is_trap_map_member")
    if is_trap_raw is not None:
        trap["is_trap_map_member"] = is_trap_raw.lower() == "true"
    trap["trap_type"] = _parse_single_value(trap_text, "trap_type")
    trap["trap_alignment_hint"] = _parse_single_value(
        trap_text, "trap_alignment_hint"
    )

    # 동적 7항 매핑
    dynamic_text = sections.get("동적 7항 매핑", "")
    dynamic = {"dynamic_link": _parse_single_value(dynamic_text, "dynamic_link")}

    # cross_subject_hints (rarely present as a separate section)
    cross_hints: List[Dict[str, str]] = []
    cross_text = sections.get("cross_subject_hints", "")
    if cross_text:
        current: Optional[Dict[str, str]] = None
        for line in cross_text.split("\n"):
            target = re.match(r"^\s*-\s*target_subject:\s*(.+)$", line)
            via = re.match(r"^\s+via_concept:\s*(.+)$", line)
            ctype = re.match(r"^\s+connection_type:\s*(.+)$", line)
            if target:
                if current:
                    cross_hints.append(current)
                current = {"target_subject": target.group(1).strip()}
            elif via and current is not None:
                current["via_concept"] = via.group(1).strip()
            elif ctype and current is not None:
                current["connection_type"] = ctype.group(1).strip()
        if current:
            cross_hints.append(current)

    # 연관 문제 후보 — the section that triggered the bugs.
    related_text = sections.get("연관 문제 후보", "")
    related = {
        "same_core_candidates": _parse_list_field(
            related_text, "same_core_candidates"
        ),
        "same_trap_pattern_candidates": _parse_list_field(
            related_text, "same_trap_pattern_candidates"
        ),
    }

    return {
        "problem": problem,
        "quality": quality,
        "v32": v32,
        "trap": trap,
        "dynamic": dynamic,
        "cross_subject_hints": cross_hints,
        "related": related,
        "header_subject": header_subject,
    }


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        print("usage: python -m scripts.v2_input_parser <input_NNN.md>")
        sys.exit(1)
    parsed = parse_input(sys.argv[1])
    print(json.dumps(parsed, ensure_ascii=False, indent=2))
