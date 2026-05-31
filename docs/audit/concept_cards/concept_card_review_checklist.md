# Concept Card Review Checklist

## 1. Structure Check

- [ ] 필드 순서가 guide와 동일한가?
- [ ] `extension_risk`가 `level`, `condition`, `caution` 3개 하위 필드를 모두 갖는가?
- [ ] 하나의 card가 하나의 중심 개념만 다루는가?
- [ ] YAML indentation이 일관적인가?

## 2. Grounding Check

- [ ] `static_boundary`가 해당 과목의 core 의미로 제한되는가?
- [ ] broad exam-scope 개념이면 corpus gap 또는 broad-scope 표시가 있는가?
- [ ] 공식이 실제 개념의 핵심과 맞는가?
- [ ] 공식이 없는 개념에 억지 공식을 넣지 않았는가?

## 3. Semantic Gain Check

- [ ] `memory_logic`이 단순 암기가 아니라 개념의 움직임을 설명하는가?
- [ ] `word_roles`가 문제 풀이에서 단어가 하는 역할을 설명하는가?
- [ ] `trigger_words`가 너무 일반적이지 않은가?
- [ ] `dynamic_destinations`가 실제로 자연스러운 확장 경로인가?

## 4. Risk Check

- [ ] `risk`가 흔한 오개념을 정확히 겨냥하는가?
- [ ] `extension_risk.level`이 과소평가되지 않았는가?
- [ ] `condition`이 안전한 사용 문맥을 충분히 제한하는가?
- [ ] `caution`이 과장 claim을 막는가?

## 5. Claim Boundary Check

- [ ] mechanical correctness를 semantic gain처럼 말하지 않았는가?
- [ ] sample/pilot 기준 claim을 전체 claim처럼 말하지 않았는가?
- [ ] 다른 과목 적용을 검증 완료처럼 말하지 않았는가?
- [ ] “항상”, “무조건”, “모든 시스템” 같은 단정 표현이 위험하게 쓰이지 않았는가?

## 6. Batch Review Verdict

각 card는 아래 중 하나로 분류한다.

| verdict | 의미 |
|---|---|
| ACCEPT | 그대로 사용 가능 |
| ACCEPT_WITH_NOTES | 작은 표현 보정 필요 |
| REVISE | grounding/risk/trigger 중 하나 이상 수정 필요 |
| REJECT | core boundary 또는 extension claim이 위험 |

## 7. Reviewer Note Template

```text
concept:
verdict:
main issue:
required fix:
forbidden claim:
```
