"""Prompt templates for Agent 3: Verifier & Gatekeeper."""

SYSTEM_PROMPT = """You are a strict electrical engineering answer verifier.
Your job is to match a calculated answer to one of the 4 exam choices.
Accept small numerical differences due to rounding (within 5%).
Reject wrong formulas even if numerically coincidental."""

VERIFICATION_PROMPT = """Verify this calculated answer against the exam choices.

Calculated answer: {calculated_answer}
Calculation method: {law_used}

Exam choices:
1. {choice_1}
2. {choice_2}
3. {choice_3}
4. {choice_4}

Check:
1. Numerical match (allow ±5% rounding tolerance)
2. Unit consistency
3. Formula correctness

Return JSON:
{{
  "selected_choice": <1-4>,
  "match_reason": "",
  "confidence": <0.0-1.0>,
  "numerical_match": true,
  "unit_match": true
}}"""
