"""Unit tests for parse_audit module."""

from __future__ import annotations

import pytest

from ee_agent.domain.models.question import (
    Choice,
    DifficultyLevel,
    ParsedQuestionBatch,
    Question,
    QuestionType,
    Subject,
)
from ee_agent.verify.parse_audit import (
    AuditSeverity,
    ParseAuditConfig,
    audit_parsed_batch,
)


def _make_question(
    number: int = 1,
    stem: str = "정상적인 문제 지문입니다. 충분한 길이.",
    choices: list[str] | None = None,
    subject: Subject = Subject.CIRCUIT_THEORY,
    needs_ocr: bool = False,
) -> Question:
    if choices is None:
        choices = ["선지1 텍스트", "선지2 텍스트", "선지3 텍스트", "선지4 텍스트"]
    return Question(
        year=2022,
        exam_session=2,
        question_number=number,
        subject=subject,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=DifficultyLevel.MEDIUM,
        stem=stem,
        choices=[Choice(index=i + 1, text=t) for i, t in enumerate(choices)],
        correct_answer=1,
        needs_ocr=needs_ocr,
    )


def _make_batch(questions: list[Question]) -> ParsedQuestionBatch:
    return ParsedQuestionBatch(
        source_file="test.pdf",
        year=2022,
        total_count=len(questions),
        questions=questions,
    )


def test_empty_batch_is_critical():
    batch = ParsedQuestionBatch(
        source_file="empty.pdf", year=2022, total_count=0, questions=[]
    )
    report = audit_parsed_batch(batch)
    assert report.pass_gate is False
    assert report.worst_severity == AuditSeverity.CRITICAL
    assert any(f.check == "empty_batch" for f in report.findings)


def test_healthy_batch_passes():
    batch = _make_batch([_make_question(n) for n in range(1, 11)])
    report = audit_parsed_batch(batch)
    assert report.pass_gate is True
    assert report.worst_severity in {AuditSeverity.INFO, AuditSeverity.WARN}


def test_needs_ocr_high_ratio_fails_gate():
    questions = [_make_question(n, needs_ocr=(n <= 4)) for n in range(1, 11)]
    batch = _make_batch(questions)
    report = audit_parsed_batch(batch)
    ocr_finding = next(f for f in report.findings if f.check == "needs_ocr_ratio")
    assert ocr_finding.severity == AuditSeverity.ERROR
    assert report.pass_gate is False


def test_short_choice_detected():
    q_bad = _make_question(1, choices=["정상 선지", "A", "정상 선지3", "정상 선지4"])
    batch = _make_batch([q_bad])
    report = audit_parsed_batch(batch)
    assert any(f.check == "choice_too_short" for f in report.findings)
    assert report.pass_gate is False


def test_low_entropy_text_detected():
    garbage = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    q = _make_question(1, stem=garbage, choices=[garbage] * 4)
    batch = _make_batch([q])
    report = audit_parsed_batch(batch)
    assert any(f.check == "low_entropy_text" for f in report.findings)


def test_subject_dominance_warning():
    questions = [
        _make_question(n, subject=Subject.CIRCUIT_THEORY) for n in range(1, 11)
    ]
    batch = _make_batch(questions)
    report = audit_parsed_batch(batch)
    dom = next((f for f in report.findings if f.check == "subject_dominance"), None)
    assert dom is not None
    assert dom.severity == AuditSeverity.WARN


def test_duplicate_signature_cluster_warning():
    same_stem = "동일한 지문 패턴의 질문. 충분히 길이 있음."
    same_first_choice = "첫 번째 선지 동일"
    questions = [
        _make_question(
            n,
            stem=same_stem,
            choices=[same_first_choice, "다른2", "다른3", "다른4"],
        )
        for n in range(1, 6)
    ]
    batch = _make_batch(questions)
    report = audit_parsed_batch(batch)
    assert any(f.check == "duplicate_signature_cluster" for f in report.findings)


def test_config_overrides_thresholds():
    questions = [_make_question(n, needs_ocr=(n <= 2)) for n in range(1, 11)]
    batch = _make_batch(questions)
    strict = ParseAuditConfig(needs_ocr_ratio_error=0.15)
    report = audit_parsed_batch(batch, config=strict)
    ocr_finding = next(f for f in report.findings if f.check == "needs_ocr_ratio")
    assert ocr_finding.severity == AuditSeverity.ERROR
    assert report.pass_gate is False


@pytest.mark.parametrize(
    "ratio_warn,ratio_error,ocr_count,expected",
    [
        (0.10, 0.30, 0, AuditSeverity.INFO),
        (0.10, 0.30, 2, AuditSeverity.WARN),
        (0.10, 0.30, 4, AuditSeverity.ERROR),
    ],
)
def test_needs_ocr_thresholds(ratio_warn, ratio_error, ocr_count, expected):
    questions = [_make_question(n, needs_ocr=(n <= ocr_count)) for n in range(1, 11)]
    batch = _make_batch(questions)
    cfg = ParseAuditConfig(
        needs_ocr_ratio_warn=ratio_warn, needs_ocr_ratio_error=ratio_error
    )
    report = audit_parsed_batch(batch, config=cfg)
    finding = next(f for f in report.findings if f.check == "needs_ocr_ratio")
    assert finding.severity == expected
