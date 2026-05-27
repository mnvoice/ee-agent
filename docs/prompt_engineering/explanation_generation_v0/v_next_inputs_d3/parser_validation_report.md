# v_next D-3 Parser Validation Report

> 2026-05-27 KST. v_next D-3 input creation 직후 parser validation.
> D-3 generation 0 / audit 0 / commit 0 / v_full handoff scope 미수정 / D-2 sealed assets 미수정.

## 1. 검증 항목 매트릭스

| # | 항목 | 결과 |
|---:|---|---|
| 1 | generated inputs: 94 / 94 | 94 / 94 ✓ |
| 2 | parse PASS: 94 / 94 | 94 / 94 ✓ |
| 3 | related_id_violations: 0 | 0 ✓ |
| 4 | duplicate problem_id: 0 | 0 ✓ |
| 5 | invalid answer: 0 | 0 ✓ |
| 6 | choices != 4: 0 | 0 ✓ |
| 7 | missing question_text: 0 | 0 ✓ |
| 8 | missing solution: 0 | 0 ✓ |
| 9 | CLEAN 94 only | ✓ |
| 10 | preview 94 = generated 94 id 일치 | intersection 94 / preview 94 / generated 94 ✓ |
| 11 | evidence_field tag 0 | tag 0 ✓ |
| 12 | audit_group expansion 57 | 57 / 57 ✓ |
| 13 | audit_group non_expansion_metadata 37 | 37 / 37 ✓ |
| 14 | enriched 4 field present | 94 / 94 ✓ |
| 15 | dynamic_link parser 반영 | 57 / 94 (dl null 의도 37건 허용) |
| 16 | essence_question parser 반영 | 94 / 94 ✓ |
| 17 | representative_trap parser 반영 | 94 / 94 ✓ |
| 18 | trap_type parser 반영 | 94 / 94 ✓ |
| 19 | catalog 51 + gap 97 = 148 | 51 + 97 = 148 ✓ |

## 2. Evidence / Audit Distribution

| field | distribution |
|---|---|
| evidence_field | {'both': 88, 'question_text': 6} |
| audit_group | {'expansion': 57, 'non_expansion_metadata': 37} |

## 3. Per-Input Parse Errors

- per_input_errors: **0** ✓

## 4. Duplicate / Invalid / Missing 상세

- duplicate problem_id: **0** ✓
- invalid answer: **0** ✓
- choices != 4: **0** ✓
- missing question_text (<12자): **0** ✓
- missing solution: **0** ✓

## 5. 보호 영역

| 보호 대상 | 상태 |
|---|---|
| app/data/questions.json | read-only ✓ |
| v_full handoff scope | read-only ✓ |
| D-2 sealed assets | read-only ✓ |
| scripts/explanation_synthesizer.py / scripts/v2_input_parser.py | 미수정 ✓ |
| D-3 generation / audit | 0 ✓ |
| P5 sample experiment / generator code | 0 ✓ |
| commit | 0 ✓ |

## 6. 최종 판정

**판정: READY_FOR_D3_GENERATION_GATE ✓**

- ✓ D-3 CLEAN 94 input 생성 및 parser validation 통과
- ✓ expansion 57 + non_expansion_metadata 37 정합
- ✓ catalog 51 + gap 97 보호

아직:
- D-3 generation / audit / D-4 / catalog review / SUSPECT promotion / keyword expansion / P5 / commit 모두 별 게이트

---
End of v_next D-3 parser validation report.
