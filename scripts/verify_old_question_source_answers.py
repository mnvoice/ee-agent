#!/usr/bin/env python3
"""Read-only V0/V1 verifier for the old-question answer source verification track.

Design source: docs/audit/old_question_answer_source_verification_track.md
Decision: DR-T35-Q2A-ANSWER-SOT-001

For each pilot question (1998-2016) listed in the Q2-A dry-run sheet, this verifier
locates the source answer material and reports its machine-readability state. It
NEVER mutates app data, never corrects an answer, never applies a solution, and
never calls a paid API.

Source priority (per the track design):
  1. Original PDF answer table
  2. Original problem-page choices (OCR / crop)
  3. Existing Mathpix OCR
  4. Theory calculation — supporting evidence only, NOT a source answer

V0/V1 finding (established empirically before this verifier was written):
  - The old `문제_*.pdf` files are problem-only; the answer key lives on scanned
    solution pages as inline `[답] N` markers (embedded PDF text = 0 — image scan).
  - `batch_answer_key/mapping.json` pins those answer-key pages per exam.
  - `questions_기출_*.json` answers equal `questions.v2.json` answers 30/30 — it is
    NOT an independent source.
  - Therefore no machine-readable source answer exists for the pilot set. Reliable
    extraction needs a dedicated crop + OCR phase. This verifier records that state
    precisely; it does not guess a source answer.

Usage: python3 scripts/verify_old_question_source_answers.py [dryrun.md]
"""
import json
import re
import sys
import glob
import datetime
import unicodedata
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DRYRUN = ROOT / "docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md"
QV2 = ROOT / "app/data/questions.v2.json"
MAPPING = ROOT / "data/batch_answer_key/mapping.json"
REPORTS_DIR = ROOT / "app/reports"

KEY_RE = re.compile(r"`(\d{4}_\d+회_\d+)`")
# Deterministic choice-corruption markers.
TABLE_JUNK_RE = re.compile(r"\\(?:end|begin|caption)\{|\\captionsetup")
FOOTER_JUNK_RE = re.compile(r"D[-－]60|전기기사\s*펄기|시리즈|\d+년도\s*\d+회")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def norm(v):
    return ("" if v is None else str(v)).strip()


def has_pua(t):
    return any(0xE000 <= ord(c) <= 0xF8FF for c in (t or ""))


def choice_status(choices):
    """clean | ocr_corrupt | partial — deterministic markers only."""
    if not choices or len(choices) < 2:
        return "ocr_corrupt"
    corrupt = 0
    for c in choices:
        s = norm(c)
        if not s:
            corrupt += 1
        elif TABLE_JUNK_RE.search(s) or has_pua(s) or "�" in s or FOOTER_JUNK_RE.search(s):
            corrupt += 1
    if corrupt == 0:
        return "clean"
    if corrupt >= 2:
        return "ocr_corrupt"
    return "partial"


def find_pdf(year, session):
    sess = nfc(session)
    for p in glob.glob(str(ROOT / "data/*.pdf")):
        n = nfc(Path(p).name)
        if "문제" in n and f"_{year}_" in n and sess in n:
            return p
    return None


def ak_pages(mapping, year, session):
    sn = re.sub(r"\D", "", session)
    pages = sorted(set(
        int(v["page_num"]) for k, v in mapping.items()
        if k.startswith(f"ak_{year}_{sn}_")
    ))
    return pages


def parse_keys(dryrun_path):
    text = Path(dryrun_path).read_text(encoding="utf-8")
    seen, keys = set(), []
    for m in KEY_RE.finditer(text):
        k = m.group(1)
        if k not in seen:
            seen.add(k)
            keys.append(k)
    return keys


def main():
    dryrun = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DRYRUN
    keys = parse_keys(dryrun)
    qv = {(q.get("year"), q.get("session"), q.get("q_no")): q
          for q in json.load(open(QV2, encoding="utf-8"))}
    mapping = json.load(open(MAPPING, encoding="utf-8"))

    items = []
    for key in keys:
        y, s, qn = key.split("_")
        y, qn = int(y), int(qn)
        q = qv.get((y, s, qn), {})
        cur = q.get("answer")
        cstatus = choice_status(q.get("choices"))

        pdf = find_pdf(y, s)
        pages = ak_pages(mapping, y, s)
        # Confirm answer-key pages are image scans (embedded text ~ 0).
        ak_text_lens, page_count = [], None
        if pdf:
            try:
                import fitz
                doc = fitz.open(pdf)
                page_count = len(doc)
                for pnum in pages:
                    idx = pnum - 1  # mapping page_num treated as 1-indexed
                    if 0 <= idx < page_count:
                        ak_text_lens.append(len(doc[idx].get_text().strip()))
                doc.close()
            except Exception as e:
                ak_text_lens = [f"err:{e}"]

        if pdf and pages:
            loc = (f"{Path(pdf).name} pages {pages} "
                   f"(scanned 풀이/answer pages, inline [답] markers)")
        elif pdf:
            loc = f"{Path(pdf).name} (answer-key page not in mapping.json)"
        else:
            loc = "source PDF not found"

        scanned = bool(pages) and all(
            isinstance(x, int) and x < 30 for x in ak_text_lens
        ) if ak_text_lens else None

        # Verdict — V0/V1 deterministic routing.
        if cstatus == "ocr_corrupt":
            verdict = "source_choice_ocr_corrupt"
        elif pdf and pages:
            # answer source exists but is an un-OCR'd image scan
            verdict = "needs_pdf_page_crop"
        else:
            verdict = "defer"

        if verdict == "source_choice_ocr_corrupt":
            note = (f"stored choices show OCR-corruption markers ({cstatus}); "
                    f"answer cannot be mapped to a choice reliably. "
                    f"answer key at {loc}.")
            nxt = "route to choice recovery track; then re-verify answer."
        elif verdict == "needs_pdf_page_crop":
            note = (f"answer key located at {loc}; embedded PDF text on those pages "
                    f"= {ak_text_lens} (image scan, not machine-readable). "
                    f"no text-form source answer available.")
            nxt = (f"crop answer-key page(s) {pages} of {Path(pdf).name}, "
                   f"OCR the inline [답] marker for q_no {qn}, then compare to q.answer.")
        else:
            note = "source PDF or answer-key page mapping not found."
            nxt = "locate source exam PDF / answer key before verification."

        items.append({
            "key": key,
            "current_q_answer": cur,
            "source_answer": None,  # no machine-readable source answer in this pass
            "source_answer_location": loc,
            "source_choice_status": cstatus,
            "verdict": verdict,
            "evidence_note": note,
            "next_action": nxt,
        })

    by_verdict = Counter(it["verdict"] for it in items)
    summary = {
        "pilot_items": len(items),
        "source_answer_found": sum(1 for it in items if it["source_answer"] is not None),
        "source_answer_verified": sum(1 for it in items if it["verdict"] == "source_answer_verified"),
        "source_answer_conflict": sum(1 for it in items if it["verdict"] == "source_answer_conflict"),
        "source_choice_ocr_corrupt": by_verdict.get("source_choice_ocr_corrupt", 0),
        "needs_pdf_page_crop": by_verdict.get("needs_pdf_page_crop", 0),
        "defer": by_verdict.get("defer", 0),
        "by_verdict": dict(sorted(by_verdict.items())),
    }

    report = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "verifier": "scripts/verify_old_question_source_answers.py",
        "read_only": True,
        "design_ref": "docs/audit/old_question_answer_source_verification_track.md",
        "decision_ref": "DR-T35-Q2A-ANSWER-SOT-001",
        "inputs": {
            "dryrun": str(dryrun.relative_to(ROOT)) if dryrun.is_relative_to(ROOT) else str(dryrun),
            "questions_v2": "app/data/questions.v2.json",
            "answer_key_mapping": "data/batch_answer_key/mapping.json",
        },
        "verification_limits": [
            "Old 문제_*.pdf files are problem-only; the answer key is on scanned pages "
            "as inline [답] markers with 0 embedded text (image scan).",
            "tesseract binary is available but produced no parseable output on a test "
            "answer page; reliable OCR of these scans is a separate crop+OCR phase.",
            "questions_기출_*.json answers equal questions.v2.json answers 30/30, so it "
            "is not an independent source and cannot verify q.answer.",
            "Theory calculation is not a source answer (track priority 4) and is not "
            "used here to assign a verdict.",
            "Therefore this V0/V1 pass finds 0 machine-readable source answers; it "
            "establishes answer-key locations and choice status only.",
        ],
        "summary": summary,
        "items": items,
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    json_out = REPORTS_DIR / f"old_question_source_answer_verification_{ts}.json"
    md_out = REPORTS_DIR / f"old_question_source_answer_verification_{ts}.md"
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_out.write_text(render_md(report), encoding="utf-8")

    print(f"pilot items            : {summary['pilot_items']}")
    print(f"source answer found    : {summary['source_answer_found']}")
    print(f"  verified (==q.answer) : {summary['source_answer_verified']}")
    print(f"  conflict (!=q.answer) : {summary['source_answer_conflict']}")
    print(f"source_choice_ocr_corrupt: {summary['source_choice_ocr_corrupt']}")
    print(f"needs_pdf_page_crop    : {summary['needs_pdf_page_crop']}")
    print(f"defer                  : {summary['defer']}")
    print(f"json report            : {json_out.relative_to(ROOT)}")
    print(f"md report              : {md_out.relative_to(ROOT)}")


def render_md(report):
    s = report["summary"]
    L = []
    L.append("# Old Question Answer Source Verification — V0/V1")
    L.append("")
    L.append(f"- Generated: {report['generated_at']}")
    L.append(f"- Verifier: `{report['verifier']}` (read-only)")
    L.append(f"- Design: `{report['design_ref']}`")
    L.append(f"- Decision: `{report['decision_ref']}`")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append("| Metric | Count |")
    L.append("| --- | ---: |")
    L.append(f"| Pilot items | {s['pilot_items']} |")
    L.append(f"| Source answer found (machine-readable) | {s['source_answer_found']} |")
    L.append(f"| source_answer_verified (== q.answer) | {s['source_answer_verified']} |")
    L.append(f"| source_answer_conflict (!= q.answer) | {s['source_answer_conflict']} |")
    L.append(f"| source_choice_ocr_corrupt | {s['source_choice_ocr_corrupt']} |")
    L.append(f"| needs_pdf_page_crop | {s['needs_pdf_page_crop']} |")
    L.append(f"| defer | {s['defer']} |")
    L.append("")
    L.append("## Verification limits")
    L.append("")
    for lim in report["verification_limits"]:
        L.append(f"- {lim}")
    L.append("")
    L.append("## Items")
    L.append("")
    L.append("| key | q.answer | choice status | verdict |")
    L.append("| --- | ---: | --- | --- |")
    for it in report["items"]:
        L.append(f"| {it['key']} | {it['current_q_answer']} | "
                 f"{it['source_choice_status']} | {it['verdict']} |")
    L.append("")
    L.append("## Source answer locations")
    L.append("")
    for it in report["items"]:
        L.append(f"- `{it['key']}`: {it['source_answer_location']}")
    L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
