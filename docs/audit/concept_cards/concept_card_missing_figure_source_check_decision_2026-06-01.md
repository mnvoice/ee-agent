# Missing-Figure Source Check Decision

작성일: 2026-06-01 KST
작성자: Codex supervisor

## 1. Purpose

이 문서는 `source_check_3_problem_review.html`에서 사람이 검토한 figure_missing high-pressure 3건의 결정을 기록한다.

이 기록은 YAML patch가 아니다. 새 concept-card YAML을 만들지 않는다. `expansion_pilot`을 승격하지 않는다. gold set, benchmark, semantic-gain, production readiness를 주장하지 않는다.

## 2. Human Decision Summary

| problem_id | source state | human decision | exam-purpose handling | system disposition |
|---|---|---|---|---|
| `2003_1회_66` | figure missing; answer/step conflict | Patch Hold | 2단자망 공진/반공진 유형으로 기억하되, 원본 도면 매칭 전 공식 노트 확정 편입은 보류 | source cleanup backlog. YAML patch 금지 |
| `2000_4회_61` | figure missing; recorded answer vs solution conflict | Card Evidence 제외 | 정저항 회로 표준 조건은 `Z_1 Z_2 = R^2`, `L/C = R^2`, `R = sqrt(L/C)` 방향으로 별도 암기 가능 | 원본 그림/정답 시비 확인 전까지 card evidence와 model-training evidence에서 격리 |
| `2002_3회_63` | figure missing; choices contaminated | Data Cleanup 1순위 | 영상임피던스 계산형이라는 유형만 남긴다. 실제 숫자 보기와 회로도는 원본 기출에서 재입력 필요 | choices 복구 또는 flush 후보. card evidence에서 즉시 탈락 |

## 3. Row-Level Notes

### 3.1 `2003_1회_66`: 반공진 각주파수

판단:

```text
선택 A와 C의 중간 단계: Patch Hold
```

근거:

- stem은 “그림과 같은 2단자 회로에서 반공진 각주파수”를 묻는다.
- 보기와 recorded answer는 `100`, `200`, `400`, `800`; recorded answer는 `200`이다.
- 생성 풀이 본문은 `200`을 지지하지만, generated steps는 `400`을 산출한다.
- 그림이 없으면 회로 구조, L/C 값, 반공진 공식 적용 범위를 확정할 수 없다.

처리:

- 정답 데이터 자체는 비교적 신뢰 가능하지만, generated steps는 회로 구조 오인 또는 계산 버그로 본다.
- 원본 기출 도면을 찾아 매칭하기 전까지 YAML patch 금지.
- source cleanup backlog에 둔다.

### 3.2 `2000_4회_61`: 정저항 회로 조건

판단:

```text
선택 C: Card Evidence 제외
```

근거:

- stem은 “다음 회로의 임피던스가 R이 되기 위한 조건”을 묻는다.
- 정저항 회로의 표준 조건은 일반적으로 `Z_1 Z_2 = R^2`이다.
- recorded answer는 `Z_1 Z_2 = R`로 되어 있어 표준식 및 generated solution과 정면 충돌한다.
- 원본 회로 그림 또는 정답 시비 이력을 확인하지 않으면 어떤 선택지를 공식 evidence로 쓸 수 없다.

처리:

- 시험용으로는 정저항 조건 `Z_1 Z_2 = R^2` 및 `R = sqrt(L/C)` 방향을 별도 암기 가능하다.
- 그러나 이 row는 원본 검증 전까지 concept-card evidence에서 제외한다.
- model-training evidence로 자동 투입하지 않는다.

### 3.3 `2002_3회_63`: 영상임피던스 계산

판단:

```text
선택 B: Data Cleanup 무조건 대상
```

근거:

- stem은 `Z_01 = 6 Ω`에서 저항 `R` 값을 묻는 계산형 문제다.
- 현재 choices는 `s` domain 라플라스/삼각함수 표현으로, stem의 단위와 도메인에 전혀 맞지 않는다.
- 본문 solution과 steps도 서로 다른 영상임피던스 공식을 적용하고 있어 내부 정합성이 낮다.

처리:

- card evidence에서 즉시 탈락.
- choices 전체 복구 또는 flush 후보.
- 원본 기출문제집의 실제 회로도와 숫자 보기를 수동 복구해야 한다.

## 4. Missing Figure Protocol Draft

세 row는 모두 `figure_missing`이지만 손상 유형은 다르다. 다음 프로토콜을 초안으로 둔다.

| protocol type | description | example | action |
|---|---|---|---|
| Type 1: 단순 유실 / 정답 정합성 높음 | stem, choices, recorded answer가 대체로 맞고 generated steps만 충돌 | `2003_1회_66` | source figure match 시도; patch hold |
| Type 2: 정답 충돌 | 표준 이론 또는 generated solution과 recorded answer가 충돌 | `2000_4회_61` | 원본 검증 전 evidence 격리 |
| Type 3: 선지 오염 | stem과 choices의 단위/도메인이 불일치 | `2002_3회_63` | data contaminated alert; choices 복구 또는 flush |

## 5. Claim Boundary

이 문서는 다음을 주장하지 않는다.

- YAML patch authorization
- new concept-card creation authorization
- `expansion_pilot` promotion
- gold set completion
- benchmark status
- semantic-gain proof
- production readiness
- PR #1 ready-for-review approval
- PR #1 merge approval

## 6. Recommended Next Step

시험 합격 트랙:

- 정저항 회로 표준 조건과 2단자망 공진/반공진을 별도 시험용 공식 노트 후보로 둔다.
- 단, source figure 복구 전에는 해당 row들을 hard evidence로 쓰지 않는다.

시스템 트랙:

- `2003_1회_66`: source figure matching backlog
- `2000_4회_61`: answer-key / original-source dispute check
- `2002_3회_63`: choices contamination cleanup
