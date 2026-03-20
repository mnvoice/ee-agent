"""Prompt templates for Agent 4: Memory & Knowledge Sync."""

SYSTEM_PROMPT = """You are a knowledge extraction agent for electrical engineering.
Extract structured knowledge from solved exam problems.
Identify: core concepts tested, formulas applied, regulations referenced."""

KNOWLEDGE_EXTRACTION_PROMPT = """Extract knowledge from this solved exam problem.

Problem: {stem}
Subject: {subject}
Solution method: {law_used}
Correct answer: {correct_choice}

Extract:
1. Core concepts tested (Korean terms)
2. Formula used (LaTeX)
3. Key technical terms

Return JSON:
{{
  "concepts": [{{"name": "", "definition": ""}}],
  "formula": {{"name": "", "latex": "", "variables": {{}}}},
  "technical_terms": []
}}"""
