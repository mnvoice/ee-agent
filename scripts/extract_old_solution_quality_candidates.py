#!/usr/bin/env python3
"""Read-only extractor for the answer-mismatch / old-solution quality track.

Scans questions.v2.json and emits a deterministic candidate manifest for old or
weak explanations whose conclusion, evidence, or rendered learning value is unsafe.

Design source: docs/audit/answer_mismatch_old_solution_quality_track.md
Decision: DR-T35-QTRACK-001

This script is strictly read-only. It never mutates app data. It only reads the
input JSON and writes report files under app/reports/.

Triggers (deterministic signals):
  conclusion_mismatch     - solution's last explicit "정답: N번" mention != q.answer
  placeholder_like_solution - solution text matches a placeholder pattern
  empty_solution          - solution is empty / whitespace
  empty_steps             - steps dict has no substantive 인식/변환/계산 text
  pua_solution            - PUA chars (U+E000..U+F8FF) in solution
  fffd_solution           - U+FFFD in solution
  answer_sentinel_0       - q.answer == 0 (sentinel; answer SoT not usable as-is)
  figure_asset_present    - figure_svg or stem_figure present (figure-aware routing)

Route (one per candidate, most-blocking wins):
  already_verified           - answer-locked verified item (excluded from candidates)
  defer_policy               - answer sentinel / domain decision needed
  needs_source_crop          - figure/diagram required; no text-only regen
  needs_source_answer_check  - corrupted glyphs or insufficient text to rewrite
  regen_text_only            - enough text/choices/answer to rewrite without paid API

Verified answer-locked items (excluded from the default candidate set):
  answer-locked-regen-T3.5, answer-locked-regen-T3.5-H2-local-crop

Usage: python3 scripts/extract_old_solution_quality_candidates.py [questions.v2.json]
"""
import json
import re
import sys
import hashlib
import datetime
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "app/data/questions.v2.json"
REPORTS_DIR = ROOT / "app/reports"

VERIFIED_TOOLS = {"answer-locked-regen-T3.5", "answer-locked-regen-T3.5-H2-local-crop"}
PREVIEW_LEN = 160
PILOT_TARGET = 30  # C1 regen_text_only pilot batch size (20..50 range)

# Placeholder pattern — kept in sync with SOLUTION_PLACEHOLDER_RE in app/index.html.
PLACEHOLDER_RE = re.compile(
    r"(문제\s*정보\s*부족|정보\s*부족|분석\s*불가능|분석\s*불가|전문\s*재제출|재제출|"
    r"문제\s*내용\s*누락|문제\s*내용\s*부재|문제\s*및\s*선택지\s*정보\s*부재|"
    r"문제\s*내용\s*및\s*보기\s*필요|인식\s*불가|모두\s*누락|모두\s*비어)"
)

# Explicit answer-mention pattern — v2 rule (solution_regen_validation_rules_v2):
# circled numbers stand alone; arabic 1-4 require a trailing "번" not followed by a digit.
ANSWER_MENTION_RE = re.compile(
    r"정답[은는]?[\s:]*[(]?([①②③④])[)]?"
    r"|정답[은는]?[\s:]*[(]?([1-4])[)]?\s*번(?![0-9])"
    r"|답[은는]?[\s:]*[(]?([①②③④])[)]?"
    r"|답[은는]?[\s:]*[(]?([1-4])\s*번(?![0-9])"
    r"|따라서[\s,]+(?:정답[은는]?\s*)?[(]?([①②③④])[)]?"
    r"|따라서[\s,]+(?:정답[은는]?\s*)?[(]?([1-4])[)]?\s*번(?![0-9])"
)
CIRCLED = {"①": 1, "②": 2, "③": 3, "④": 4}

BASELINE = {
    "total_entries": 5331,
    "tool_name_null_old": 4563,
    "missing_solution_metadata": 693,
    "explicit_answer_mention_mismatch": 190,
    "placeholder_like": 261,
    "pua_solution": 204,
    "figure_asset_present": 340,
}


def sha12(s):
    return hashlib.sha1(str(s if s is not None else "").encode("utf-8")).hexdigest()[:12]


def steps_sha12(steps):
    return hashlib.sha1(json.dumps(steps, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]


def norm(v):
    return ("" if v is None else str(v)).strip()


def has_pua(t):
    return any(0xE000 <= ord(c) <= 0xF8FF for c in (t or ""))


def has_fffd(t):
    return "�" in (t or "")


def answer_mentions(text):
    """All explicit answer numbers mentioned in order; last one is the conclusion."""
    out = []
    for m in ANSWER_MENTION_RE.finditer(text or ""):
        for g in m.groups():
            if g:
                out.append(CIRCLED[g] if g in CIRCLED else int(g))
                break
    return out


def steps_is_empty(steps):
    if not isinstance(steps, dict) or not steps:
        return True
    return not any(norm(steps.get(k)) for k in ("인식", "변환", "계산"))


def preview(t):
    return " ".join(norm(t).split())[:PREVIEW_LEN]


def session_sort_key(key):
    # key like "2025_2회_60" -> (2025, 2, 60) for deterministic ordering
    try:
        y, s, qn = key.split("_")
        return (int(y), int(re.sub(r"\D", "", s) or 0), int(qn))
    except Exception:
        return (0, 0, 0)


def classify(q):
    """Return (triggers, route, detected_mentions, has_figure, tool_name, source)."""
    src = q.get("solution_source")
    tool_name = src.get("tool_name") if isinstance(src, dict) else None
    source = src.get("source") if isinstance(src, dict) else None
    verified = tool_name in VERIFIED_TOOLS

    solution = q.get("solution")
    steps = q.get("steps")
    answer = q.get("answer")
    text = q.get("text")
    choices = q.get("choices") or []
    has_figure = bool(q.get("figure_svg") or q.get("stem_figure"))

    detected = answer_mentions(solution)
    triggers = []

    if answer in (1, 2, 3, 4) and detected and detected[-1] != answer:
        triggers.append("conclusion_mismatch")
    if norm(solution) and PLACEHOLDER_RE.search(solution):
        triggers.append("placeholder_like_solution")
    if not norm(solution):
        triggers.append("empty_solution")
    if steps_is_empty(steps):
        triggers.append("empty_steps")
    if has_pua(solution):
        triggers.append("pua_solution")
    if has_fffd(solution):
        triggers.append("fffd_solution")
    if answer == 0:
        triggers.append("answer_sentinel_0")
    if has_figure:
        triggers.append("figure_asset_present")

    # Route — most-blocking wins.
    if verified:
        route = "already_verified"
    elif "answer_sentinel_0" in triggers:
        route = "defer_policy"
    elif "figure_asset_present" in triggers:
        route = "needs_source_crop"
    elif "pua_solution" in triggers or "fffd_solution" in triggers:
        route = "needs_source_answer_check"
    elif triggers:
        # repairable signal present; confirm enough material to rewrite text-only
        if norm(text) and len(choices) >= 2 and answer in (1, 2, 3, 4):
            route = "regen_text_only"
        else:
            route = "needs_source_answer_check"
    else:
        route = None  # no trigger -> not a candidate

    return triggers, route, detected, has_figure, tool_name, source


def main():
    inp = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    if not inp.exists():
        print(f"ERROR: input not found: {inp}", file=sys.stderr)
        sys.exit(1)

    data = json.load(open(inp, encoding="utf-8"))
    ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

    candidates = []
    verified_count = 0
    tool_name_null = 0
    missing_metadata = 0

    for q in data:
        src = q.get("solution_source")
        if not isinstance(src, dict):
            missing_metadata += 1
        elif src.get("tool_name") is None:
            tool_name_null += 1

        triggers, route, detected, has_figure, tool_name, source = classify(q)

        if route == "already_verified":
            verified_count += 1
            continue
        if not triggers:
            continue

        key = f"{q.get('year')}_{q.get('session')}_{q.get('q_no')}"
        candidates.append({
            "key": key,
            "year": q.get("year"),
            "session": q.get("session"),
            "subject": q.get("subject"),
            "q_no": q.get("q_no"),
            "answer": q.get("answer"),
            "solution_source": {"tool_name": tool_name, "source": source},
            "triggers": triggers,
            "detected_answer_mentions": detected,
            "route": route,
            "solution_hash": sha12(q.get("solution")),
            "steps_hash": steps_sha12(q.get("steps")),
            "has_figure_asset": has_figure,
            "text_preview": preview(q.get("text")),
            "solution_preview": preview(q.get("solution")),
        })

    candidates.sort(key=lambda c: session_sort_key(c["key"]))

    by_trigger = Counter(t for c in candidates for t in c["triggers"])
    by_route = Counter(c["route"] for c in candidates)
    by_subject = Counter(c["subject"] for c in candidates)

    c1_regen = [c for c in candidates
                if "conclusion_mismatch" in c["triggers"] and c["route"] == "regen_text_only"]
    pilot = [c["key"] for c in c1_regen[:PILOT_TARGET]]

    summary = {
        "total_entries": len(data),
        "verified_excluded": verified_count,
        "tool_name_null_old": tool_name_null,
        "missing_solution_metadata": missing_metadata,
        "candidate_count": len(candidates),
        "by_trigger": dict(sorted(by_trigger.items())),
        "by_route": dict(sorted(by_route.items())),
        "by_subject": dict(sorted(by_subject.items(), key=lambda x: -x[1])),
        "c1_conclusion_mismatch_regen_text_only": len(c1_regen),
    }

    report = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": str(inp.relative_to(ROOT)) if inp.is_relative_to(ROOT) else str(inp),
        "extractor": "scripts/extract_old_solution_quality_candidates.py",
        "read_only": True,
        "baseline_ref": BASELINE,
        "summary": summary,
        "pilot_recommendation": {
            "class": "C1 conclusion_mismatch + route regen_text_only",
            "size": len(pilot),
            "keys": pilot,
        },
        "candidates": candidates,
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    json_out = REPORTS_DIR / f"old_solution_quality_candidates_{ts}.json"
    md_out = REPORTS_DIR / f"old_solution_quality_candidates_{ts}.md"
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_out.write_text(render_md(report), encoding="utf-8")

    print(f"input             : {report['source']}")
    print(f"total entries     : {summary['total_entries']}")
    print(f"verified excluded : {summary['verified_excluded']}")
    print(f"candidates        : {summary['candidate_count']}")
    print(f"by route          : {summary['by_route']}")
    print(f"by trigger        : {summary['by_trigger']}")
    print(f"C1 regen_text_only: {summary['c1_conclusion_mismatch_regen_text_only']}")
    print(f"pilot batch       : {len(pilot)} keys")
    print(f"json report       : {json_out.relative_to(ROOT)}")
    print(f"md report         : {md_out.relative_to(ROOT)}")


def render_md(report):
    s = report["summary"]
    b = report["baseline_ref"]
    L = []
    L.append("# Old Solution Quality Candidates")
    L.append("")
    L.append(f"- Generated: {report['generated_at']}")
    L.append(f"- Source: `{report['source']}` (read-only scan)")
    L.append(f"- Extractor: `{report['extractor']}`")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append("| Metric | Count |")
    L.append("| --- | ---: |")
    L.append(f"| Total entries | {s['total_entries']} |")
    L.append(f"| Verified answer-locked (excluded) | {s['verified_excluded']} |")
    L.append(f"| tool_name=null old solutions | {s['tool_name_null_old']} |")
    L.append(f"| Missing solution metadata | {s['missing_solution_metadata']} |")
    L.append(f"| **Candidates** | **{s['candidate_count']}** |")
    L.append("")
    L.append("## By route")
    L.append("")
    L.append("| Route | Count |")
    L.append("| --- | ---: |")
    for k, v in s["by_route"].items():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("## By trigger")
    L.append("")
    L.append("| Trigger | Count |")
    L.append("| --- | ---: |")
    for k, v in s["by_trigger"].items():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("## By subject")
    L.append("")
    L.append("| Subject | Count |")
    L.append("| --- | ---: |")
    for k, v in s["by_subject"].items():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("## Baseline comparison")
    L.append("")
    L.append("| Metric | Baseline | This scan |")
    L.append("| --- | ---: | ---: |")
    L.append(f"| Total entries | {b['total_entries']} | {s['total_entries']} |")
    L.append(f"| tool_name=null old | {b['tool_name_null_old']} | {s['tool_name_null_old']} |")
    L.append(f"| Missing metadata | {b['missing_solution_metadata']} | {s['missing_solution_metadata']} |")
    L.append(f"| conclusion mismatch | ~{b['explicit_answer_mention_mismatch']} | "
             f"{s['by_trigger'].get('conclusion_mismatch', 0)} |")
    L.append(f"| placeholder-like | ~{b['placeholder_like']} | "
             f"{s['by_trigger'].get('placeholder_like_solution', 0)} |")
    L.append(f"| PUA in solution | ~{b['pua_solution']} | "
             f"{s['by_trigger'].get('pua_solution', 0)} |")
    L.append(f"| figure asset present | ~{b['figure_asset_present']} | "
             f"{s['by_trigger'].get('figure_asset_present', 0)} |")
    L.append("")
    pilot = report["pilot_recommendation"]
    L.append("## Pilot batch recommendation")
    L.append("")
    L.append(f"Class: {pilot['class']}")
    L.append(f"Size: {pilot['size']}")
    L.append("")
    if pilot["keys"]:
        L.append("Keys:")
        L.append("")
        L.append("```")
        L.append(" ".join(pilot["keys"]))
        L.append("```")
    else:
        L.append("(no C1 regen_text_only candidates found)")
    L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
