# @MX:NOTE: [AUTO] Builder-auditor separation: audits ParsedQuestionBatch independently of the parser.
"""Parse audit module.

Audits a ParsedQuestionBatch for quality issues without calling the parser itself.
Detects: needs_ocr ratio, empty/short choices, low-entropy garbage text,
subject distribution imbalance, and duplicate failure signatures.

Motivation (2026-04-13): "82/100 parsed" does not mean "82 are good".
This module produces a structured report so downstream code can gate on quality.
"""

from __future__ import annotations

import logging
import math
from collections import Counter
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from ee_agent.domain.models.question import ParsedQuestionBatch, Question, Subject

logger = logging.getLogger(__name__)


class AuditSeverity(str, Enum):
    """Severity levels for audit findings."""

    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"


class ParseAuditConfig(BaseModel):
    """Thresholds for parse audit checks. All ratios are in [0.0, 1.0]."""

    needs_ocr_ratio_warn: float = Field(default=0.10, ge=0.0, le=1.0)
    needs_ocr_ratio_error: float = Field(default=0.30, ge=0.0, le=1.0)
    min_choice_text_length: int = Field(default=2, ge=1)
    min_stem_text_length: int = Field(default=10, ge=1)
    min_shannon_entropy_bits: float = Field(default=1.5, ge=0.0)
    subject_dominance_warn: float = Field(default=0.60, ge=0.0, le=1.0)
    duplicate_signature_cluster_warn: int = Field(default=3, ge=2)


class AuditFinding(BaseModel):
    """Single audit finding. Serializable for JSON export."""

    check: str
    severity: AuditSeverity
    count: int = 0
    ratio: Optional[float] = None
    message: str
    sample_ids: list[str] = Field(default_factory=list)


class AuditReport(BaseModel):
    """Structured audit report. pass_gate=True means batch is safe to use downstream."""

    source_file: str
    total_questions: int
    findings: list[AuditFinding] = Field(default_factory=list)
    pass_gate: bool = True
    worst_severity: AuditSeverity = AuditSeverity.INFO

    @field_validator("worst_severity", mode="before")
    @classmethod
    def _coerce_severity(cls, v: str | AuditSeverity) -> AuditSeverity:
        if isinstance(v, AuditSeverity):
            return v
        return AuditSeverity(v)

    def add(self, finding: AuditFinding) -> None:
        """Add a finding and update pass_gate / worst_severity accordingly."""
        self.findings.append(finding)
        if _severity_rank(finding.severity) > _severity_rank(self.worst_severity):
            self.worst_severity = finding.severity
        if finding.severity in {AuditSeverity.ERROR, AuditSeverity.CRITICAL}:
            self.pass_gate = False


_SEVERITY_ORDER: dict[AuditSeverity, int] = {
    AuditSeverity.INFO: 0,
    AuditSeverity.WARN: 1,
    AuditSeverity.ERROR: 2,
    AuditSeverity.CRITICAL: 3,
}


def _severity_rank(s: AuditSeverity) -> int:
    return _SEVERITY_ORDER[s]


# @MX:ANCHOR: [AUTO] Primary entry point called by pipeline and CLI runner.
# @MX:REASON: Single source of truth for parse-time quality gating; downstream depends on AuditReport schema.
def audit_parsed_batch(
    batch: ParsedQuestionBatch,
    config: Optional[ParseAuditConfig] = None,
) -> AuditReport:
    """Audit a parsed batch and return a structured report.

    Args:
        batch: The output of the PDF parser.
        config: Optional threshold overrides. Uses defaults if None.

    Returns:
        AuditReport with pass_gate flag and per-check findings.
    """
    cfg = config or ParseAuditConfig()
    report = AuditReport(
        source_file=batch.source_file,
        total_questions=batch.total_count,
    )

    if batch.total_count == 0:
        report.add(
            AuditFinding(
                check="empty_batch",
                severity=AuditSeverity.CRITICAL,
                count=0,
                message="Batch has zero parsed questions.",
            )
        )
        return report

    _check_needs_ocr_ratio(batch, cfg, report)
    _check_choice_completeness(batch, cfg, report)
    _check_stem_completeness(batch, cfg, report)
    _check_entropy(batch, cfg, report)
    _check_subject_distribution(batch, cfg, report)
    _check_duplicate_signatures(batch, cfg, report)

    logger.info(
        "parse_audit done: total=%d pass_gate=%s worst=%s findings=%d",
        batch.total_count,
        report.pass_gate,
        report.worst_severity,
        len(report.findings),
    )
    return report


def _check_needs_ocr_ratio(
    batch: ParsedQuestionBatch, cfg: ParseAuditConfig, report: AuditReport
) -> None:
    flagged = [q for q in batch.questions if q.needs_ocr]
    ratio = len(flagged) / batch.total_count if batch.total_count else 0.0
    if ratio >= cfg.needs_ocr_ratio_error:
        severity = AuditSeverity.ERROR
    elif ratio >= cfg.needs_ocr_ratio_warn:
        severity = AuditSeverity.WARN
    else:
        severity = AuditSeverity.INFO
    report.add(
        AuditFinding(
            check="needs_ocr_ratio",
            severity=severity,
            count=len(flagged),
            ratio=ratio,
            message=(
                f"{len(flagged)}/{batch.total_count} questions require Vision OCR "
                f"(ratio={ratio:.1%})."
            ),
            sample_ids=[q.id for q in flagged[:5]],
        )
    )


def _check_choice_completeness(
    batch: ParsedQuestionBatch, cfg: ParseAuditConfig, report: AuditReport
) -> None:
    bad: list[Question] = []
    for q in batch.questions:
        for c in q.choices:
            if len(c.text.strip()) < cfg.min_choice_text_length:
                bad.append(q)
                break
    if bad:
        report.add(
            AuditFinding(
                check="choice_too_short",
                severity=AuditSeverity.ERROR,
                count=len(bad),
                ratio=len(bad) / batch.total_count,
                message=(
                    f"{len(bad)} questions have at least one choice shorter than "
                    f"{cfg.min_choice_text_length} characters."
                ),
                sample_ids=[q.id for q in bad[:5]],
            )
        )


def _check_stem_completeness(
    batch: ParsedQuestionBatch, cfg: ParseAuditConfig, report: AuditReport
) -> None:
    bad = [
        q for q in batch.questions if len(q.stem.strip()) < cfg.min_stem_text_length
    ]
    if bad:
        report.add(
            AuditFinding(
                check="stem_too_short",
                severity=AuditSeverity.WARN,
                count=len(bad),
                ratio=len(bad) / batch.total_count,
                message=(
                    f"{len(bad)} questions have a stem shorter than "
                    f"{cfg.min_stem_text_length} characters."
                ),
                sample_ids=[q.id for q in bad[:5]],
            )
        )


def _shannon_entropy_bits(text: str) -> float:
    """Return Shannon entropy (in bits) of a string. Empty string returns 0.0."""
    if not text:
        return 0.0
    freq = Counter(text)
    total = len(text)
    return -sum((n / total) * math.log2(n / total) for n in freq.values())


def _check_entropy(
    batch: ParsedQuestionBatch, cfg: ParseAuditConfig, report: AuditReport
) -> None:
    low_entropy: list[tuple[Question, float]] = []
    for q in batch.questions:
        combined = q.stem + "".join(c.text for c in q.choices)
        entropy = _shannon_entropy_bits(combined)
        if entropy < cfg.min_shannon_entropy_bits and len(combined) >= 20:
            low_entropy.append((q, entropy))
    if low_entropy:
        report.add(
            AuditFinding(
                check="low_entropy_text",
                severity=AuditSeverity.ERROR,
                count=len(low_entropy),
                ratio=len(low_entropy) / batch.total_count,
                message=(
                    f"{len(low_entropy)} questions have suspiciously low Shannon entropy "
                    f"(<{cfg.min_shannon_entropy_bits} bits) — likely garbage text."
                ),
                sample_ids=[q.id for q, _ in low_entropy[:5]],
            )
        )


def _check_subject_distribution(
    batch: ParsedQuestionBatch, cfg: ParseAuditConfig, report: AuditReport
) -> None:
    counts: Counter[Subject] = Counter(q.subject for q in batch.questions)
    if not counts:
        return
    top_subject, top_count = counts.most_common(1)[0]
    ratio = top_count / batch.total_count
    if ratio >= cfg.subject_dominance_warn:
        report.add(
            AuditFinding(
                check="subject_dominance",
                severity=AuditSeverity.WARN,
                count=top_count,
                ratio=ratio,
                message=(
                    f"Subject '{top_subject.value}' dominates batch: "
                    f"{top_count}/{batch.total_count} ({ratio:.1%}). "
                    "Check classifier keyword map."
                ),
            )
        )


def _check_duplicate_signatures(
    batch: ParsedQuestionBatch, cfg: ParseAuditConfig, report: AuditReport
) -> None:
    # A "signature" = stem first 40 chars + first choice first 20 chars.
    # Multiple questions sharing a signature often indicates parser collapse.
    sigs: Counter[str] = Counter()
    for q in batch.questions:
        sig = (q.stem[:40] + "||" + (q.choices[0].text[:20] if q.choices else "")).strip()
        sigs[sig] += 1
    clusters = [(sig, n) for sig, n in sigs.items() if n >= cfg.duplicate_signature_cluster_warn]
    if clusters:
        total_clustered = sum(n for _, n in clusters)
        report.add(
            AuditFinding(
                check="duplicate_signature_cluster",
                severity=AuditSeverity.WARN,
                count=total_clustered,
                ratio=total_clustered / batch.total_count,
                message=(
                    f"{len(clusters)} signature cluster(s) with >= "
                    f"{cfg.duplicate_signature_cluster_warn} questions each, "
                    f"total {total_clustered} questions. Possible parser collapse."
                ),
            )
        )
