# @MX:NOTE: [AUTO] Verify layer — independent audit of builder outputs (builder-auditor separation).
"""Verify layer for EE-Agent.

Provides independent audit of artefacts produced by builder components:
- parse_audit: audits parsed question batches for quality issues
- (planned) retrieval_audit: audits RAG retrieval bias
- (planned) output_audit: audits solver results for failure signatures
"""

from ee_agent.verify.parse_audit import (
    AuditReport,
    AuditSeverity,
    ParseAuditConfig,
    audit_parsed_batch,
)

__all__ = [
    "AuditReport",
    "AuditSeverity",
    "ParseAuditConfig",
    "audit_parsed_batch",
]
