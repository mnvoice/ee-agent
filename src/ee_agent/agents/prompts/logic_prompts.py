"""Prompt templates for Agent 2: Logic First-Principles Solver."""

SYSTEM_PROMPT = """You are an expert Korean electrical engineer (전기기사).
Solve exam problems step by step and respond with ONLY valid JSON, no markdown."""

# Calculation-type: stem contains numbers/units → CoT calculation
CALC_PROMPT = """전기기사 시험 계산 문제.

문제: {stem}
{formulas_section}
보기:
{choices}

풀이 단계:
1. 주어진 값 정리
2. 적용 공식 선택
3. 수치 계산 (단위 확인)
4. 계산 결과와 일치하는 보기 번호 결정 (1, 2, 3, 4 중 하나)

위 풀이 후 JSON만 출력 (마크다운 없이):
{{"law_used": "적용 법칙/공식", "steps": "계산 과정 요약", "final_answer": "계산값+단위", "selected_choice": 정답번호}}

selected_choice는 보기 중 정답 번호(숫자만). 계산값이 보기와 정확히 일치하지 않으면 가장 가까운 보기 선택."""

# Concept/regulation-type: no numbers → knowledge recall
CONCEPT_PROMPT = """전기기사 시험 개념/법규 문제.

문제: {stem}

보기:
{choices}

풀이 단계:
1. 핵심 키워드 파악
2. 관련 법규/원리 확인
3. 문제 유형 판단: '틀린 것은?'/'옳지 않은 것은?' → 거짓인 보기 선택 / '옳은 것은?'/'맞는 것은?' → 참인 보기 선택
4. 각 보기를 하나씩 검토하여 참/거짓 판별
5. 3번에서 판단한 유형에 맞는 보기 번호 결정 (1, 2, 3, 4 중 하나)

★ 핵심 주의사항: '틀린 것은?' 문제는 반드시 거짓 진술을 담은 보기를 선택해야 합니다.

위 풀이 후 JSON만 출력 (마크다운 없이):
{{"law_used": "관련 법칙/조항", "question_type": "틀린것|옳은것", "reasoning": "선택 근거 한 줄", "final_answer": "정답 내용 요약", "selected_choice": 정답번호}}

selected_choice는 보기 중 정답 번호(숫자만)."""

# Keep for targeted hint fallback (unused in current approach)
WRONG_QUESTION_HINT = "★주의: 이 문제는 '틀린 것'/'옳지 않은 것'을 묻습니다. 거짓인 진술이 담긴 보기를 선택하세요.\n\n"

JIT_REMINDER = """REMINDER before calculation:
- Check unit consistency (V, A, Ω, W, Hz, etc.)
- Convert prefixes (k=10³, m=10⁻³, μ=10⁻⁶)
- Verify formula domain (AC vs DC, single vs 3-phase)
- Double-check significant figures"""

# Keep for backward compatibility
BLIND_INFERENCE_PROMPT = CALC_PROMPT
