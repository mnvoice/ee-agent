"""CLI: run parse audit against a parsed JSON batch file or a live PDF parse.

Usage:
    python scripts/run_parse_audit.py --json path/to/parsed.json
    python scripts/run_parse_audit.py --pdf data/20220305_2회.pdf --year 2022
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from ee_agent.domain.models.question import ParsedQuestionBatch
from ee_agent.verify.parse_audit import (
    AuditSeverity,
    ParseAuditConfig,
    audit_parsed_batch,
)

logger = logging.getLogger(__name__)


def _load_from_json(path: Path) -> ParsedQuestionBatch:
    data = json.loads(path.read_text(encoding="utf-8"))
    return ParsedQuestionBatch.model_validate(data)


def _load_from_pdf(pdf_path: Path, year: int) -> ParsedQuestionBatch:
    from ee_agent.ingestion.pdf_extractor import extract_questions_from_pdf

    return extract_questions_from_pdf(pdf_path=pdf_path, year=year)


def _print_report(report) -> None:
    print(f"\n=== Parse Audit Report ===")
    print(f"Source: {report.source_file}")
    print(f"Total questions: {report.total_questions}")
    print(f"Pass gate: {report.pass_gate}")
    print(f"Worst severity: {report.worst_severity}")
    print(f"Findings: {len(report.findings)}")
    for f in report.findings:
        ratio_str = f" ratio={f.ratio:.1%}" if f.ratio is not None else ""
        samples = f" samples={f.sample_ids[:3]}" if f.sample_ids else ""
        print(
            f"  [{f.severity.upper():8}] {f.check:30} count={f.count}{ratio_str} "
            f"— {f.message}{samples}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--json", type=Path, help="Path to parsed batch JSON")
    src.add_argument("--pdf", type=Path, help="PDF file to parse and audit")
    parser.add_argument("--year", type=int, help="Exam year (required with --pdf)")
    parser.add_argument(
        "--needs-ocr-warn", type=float, default=0.10, help="needs_ocr WARN threshold"
    )
    parser.add_argument(
        "--needs-ocr-error", type=float, default=0.30, help="needs_ocr ERROR threshold"
    )
    parser.add_argument(
        "--output", type=Path, help="Optional JSON output path for the report"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    if args.pdf and args.year is None:
        parser.error("--year is required when using --pdf")

    if args.json:
        batch = _load_from_json(args.json)
    else:
        batch = _load_from_pdf(args.pdf, args.year)

    cfg = ParseAuditConfig(
        needs_ocr_ratio_warn=args.needs_ocr_warn,
        needs_ocr_ratio_error=args.needs_ocr_error,
    )
    report = audit_parsed_batch(batch, config=cfg)
    _print_report(report)

    if args.output:
        args.output.write_text(
            report.model_dump_json(indent=2), encoding="utf-8"
        )
        print(f"\nReport written to: {args.output}")

    if report.worst_severity in {AuditSeverity.ERROR, AuditSeverity.CRITICAL}:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
