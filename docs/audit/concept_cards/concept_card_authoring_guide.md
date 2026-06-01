# Concept Card Authoring Guide

## 1. Purpose

Concept card는 시험 개념을 단순 암기 항목으로 저장하지 않고, 다음 세 가지를 동시에 보존한다.

- core grounding: 해당 과목 안에서 안전하게 말할 수 있는 정적 경계
- transfer path: 다른 과목·응용으로 자연스럽게 확장되는 방향
- risk boundary: 확장할 때 생기는 오개념·과장·corpus gap

## 2. Required YAML Shape

모든 card는 아래 필드 순서를 유지한다.

```yaml
concept:
static_boundary:
formula_core:
dynamic_destinations:
word_roles:
trigger_words:
memory_logic:
risk:
extension_risk:
  level:
  condition:
  caution:
```

## 3. Field Rules

`concept`
: 영어 또는 혼합 표기로 개념명을 쓴다. 하나의 card에는 하나의 중심 개념만 둔다.

`static_boundary`
: 이 개념이 원래 과목 안에서 무엇을 뜻하는지 한 문장으로 제한한다. 과목 밖 응용을 여기서 주장하지 않는다.

`formula_core`
: 핵심 공식·관계식·계산 기준만 적는다. 공식이 없으면 핵심 관계를 짧게 적는다. 너무 많은 식을 넣지 않는다.

`dynamic_destinations`
: 이 개념이 자연스럽게 이어지는 응용·타 과목·시스템 관점을 적는다. 검증된 연결만 쓴다.

`word_roles`
: 자주 나오는 단어가 문제 안에서 어떤 역할을 하는지 풀이 언어로 바꾼다.

`trigger_words`
: 문제에서 이 개념을 떠올리게 하는 신호어를 적는다. 너무 일반적인 단어는 피한다.

`memory_logic`
: 암기 문장이 아니라 “왜 이 개념이 이렇게 움직이는가”를 한 문장으로 적는다.

`risk`
: 학생이 흔히 잘못 일반화하거나 계산에서 놓칠 위험을 적는다.

`extension_risk.level`
: `LOW`, `MEDIUM`, `HIGH` 중 하나를 쓴다.

`extension_risk.condition`
: 어떤 문맥에서는 확장이 안전한지 적는다.

`extension_risk.caution`
: 어떤 문맥에서는 과장되거나 틀릴 수 있는지 적는다.

## 4. Quality Rules

- `static_boundary`는 좁고 단단해야 한다.
- `dynamic_destinations`는 넓어도 되지만, `risk`가 반드시 따라야 한다.
- `memory_logic`은 외우기 쉬우면서도 개념의 방향을 담아야 한다.
- `word_roles`는 사전식 정의가 아니라 문제풀이 역할이어야 한다.
- `trigger_words`는 개념을 호출하는 단서여야 한다.
- `extension_risk`는 단순 경고가 아니라 claim boundary여야 한다.

## 5. Extension Risk Guide

`LOW`
: 표준 교과 연결이고, 오개념 위험이 작다. 그래도 조건과 주의는 적는다.

`MEDIUM`
: 다른 과목이나 시스템으로 확장 가능하지만 조건이 중요하다. corpus gap, 동작점, 선형성, 주파수 조건 등을 명시한다.

`HIGH`
: 비유는 가능하지만 직접 공식·판정으로 쓰면 위험하다. 대량 생성에서는 가능하면 피하고 review 대상으로 보낸다.

## 6. Forbidden Claims

아래 주장은 card 안에서 조심한다.

- 한 과목의 개념이 모든 시스템에 그대로 적용된다는 주장
- 공식 하나로 모든 문맥을 해결한다는 주장
- corpus grounding이 약한 개념을 core 개념처럼 취급하는 주장
- 비유를 계산 규칙처럼 쓰는 주장
- `LOW` risk를 붙였지만 caution이 비어 있는 형태

## 7. MOAI Batch Input Rule

MOAI에 30개 batch를 맡길 때는 이 guide와 pilot 3개를 함께 입력한다.

MOAI 출력은 최종본이 아니라 draft로 본다. 코덱스 김독자 review 전에는 다음 claim을 하지 않는다.

- 30개가 품질 통과했다.
- corpus gap이 없다.
- extension risk가 확정되었다.
- 학습자료에 바로 편입 가능하다.
