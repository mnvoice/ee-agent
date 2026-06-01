# Electromagnetics Static / Dynamic Bridge v0.2 Exam Memory Lines - 2026-06-01

Scope: review-only learning surface derived from the v0.2 candidate manifest.

This document adds a human study layer to the v0.2 review queue. It does not create concept cards, patch YAML, mutate source data, alter answer keys, or promote any `expansion_pilot` card.

## Guardrails

- Keep PR #1 open, draft, and unmerged.
- Do not patch YAML.
- Do not create new concept-card YAML files.
- Do not promote `expansion_pilot` cards.
- Do not claim gold-set, benchmark, semantic-gain, or production readiness.
- Treat pressure flags as evidence signals only, not patch authorization.

## Use

Read each row as a physical-quantity movement.

The exam memory line is not a replacement for source recovery. It is a review phrase that helps a learner remember what the row is doing.

Recommended mental sequence:

```text
source quantity -> field quantity -> medium response -> flux/coupling -> time change -> circuit or wave meaning
```

## Bundle 0. 정전계 / 정자계 앵커

| Row | Flow | Exam memory line | Learner action | Status |
|---|---|---|---|---|
| `p5 q3` | `Q -> E` | 전계는 전하가 공간에 만든 힘의 장이다. | 먼저 “무엇이 E를 만들었는가”를 찾는다. | usable-review |
| `p7 q8` | `surface charge -> E` | 면전하는 대칭을 잡으면 E가 바로 나온다. | 면, 선, 점 중 어떤 분포인지 먼저 고른다. | usable-review |
| `p11 q3` | `Q -> V` | 전위는 전하가 만든 장을 거리로 적분해 본 값이다. | E와 V를 섞지 말고 거리 의존성을 확인한다. | usable-review |
| `p36 q1` | `charge / voltage relation -> capacitance unit` | 정전용량은 전하를 전압으로 나눈 비율이다. | 단위 문제는 식보다 차원 `C/V`를 먼저 떠올린다. | caveated-review |
| `p37 q3` | `epsilon, geometry -> C` | 정전용량은 매질과 형상이 같이 만든다. | `epsilon`과 반지름/거리 같은 형상값을 분리한다. | usable-review |
| `p39 q7` | `C, V -> stored energy` | 축전기 에너지는 장에 저장된 회로 에너지다. | `1/2 CV^2`, `1/2 QV`, `Q^2/(2C)`를 같은 계열로 본다. | usable-review |

Supervisor note:

```text
This bundle is the floor. Dynamic bridge rows become easier only after E, D, C, energy, and medium constants are separated.
```

## Bundle 1. 유도기전력

| Row | Flow | Exam memory line | Learner action | Status |
|---|---|---|---|---|
| `p147 q1` | `N Phi -> d(N Phi)/dt -> e` | 자속 쇄교수가 변하면 기전력이 생긴다. | `N Phi`인지 `Phi`인지 먼저 구분한다. | usable-review |
| `p147 q2` | `Phi change -> e direction` | 크기는 Faraday, 방향은 Lenz가 잡는다. | 부호는 “변화를 방해하는 방향”으로 읽는다. | usable-review |

Supervisor note:

```text
Induction should be taught as flux movement before it is taught as a named law.
```

## Bundle 2. 인덕턴스 / 결합

| Row | Flow | Exam memory line | Learner action | Status |
|---|---|---|---|---|
| `p154 q2` | `i -> di/dt + L -> e` | 자기인덕턴스는 자기 자신 전류 변화가 만든 전압이다. | `di/dt`와 L을 곱하되 cleanup caveat를 유지한다. | caveated-review |
| `p166 q50` | `magnetic circuit / turns / flux coupling -> M` | 상호인덕턴스는 한 권선의 변화가 다른 권선에 묶이는 정도다. | 그림 의존을 숨기지 말고 결합 경로만 review한다. | caveated-review |
| `p166 q52` | `mu, S, N1, N2, l -> M` | M은 매질, 단면적, 권수, 자로 길이의 결합 결과다. | `mu`, `S`, `N1N2`, `l`의 자리만 분리한다. | caveated-review |
| `p168 q59` | `L1, L2, k -> M` | 결합계수 k는 두 인덕턴스가 얼마나 같이 묶였는가다. | `M = k sqrt(L1 L2)`로 회로이론과 연결한다. | usable-review |
| `p168 q60` | `i1 -> di1/dt + M -> e2` | 한 코일의 전류 변화가 다른 코일의 기전력이 된다. | 자기인덕턴스 L과 상호인덕턴스 M을 구분한다. | usable-review |

Supervisor note:

```text
The key distinction is self versus mutual: L is self-coupling, M is cross-coupling.
```

## Bundle 3. 맥스웰 / 변위전류

| Row | Flow | Exam memory line | Learner action | Status |
|---|---|---|---|---|
| `p170 q3` | `D -> partial D / partial t -> displacement current density` | 전속밀도 D가 시간에 따라 변하면 변위전류밀도가 된다. | `D`, `B`, `Phi` 중 어떤 시간 변화인지 먼저 확인한다. | usable-review |
| `p170 q4` | `D(t) -> displacement current` | 변위전류는 전하 흐름이 아니라 시간 변화 항이다. | 전도전류와 변위전류를 분리해서 읽는다. | usable-review |
| `p174 q14` | `partial D / partial t -> H` | D의 시간 변화도 자계를 만든다. | Maxwell 보정항이 전자파의 다리라는 점을 기억한다. | usable-review |

Supervisor note:

```text
Displacement current is the bridge from electrostatics to electromagnetic waves.
```

## Bundle 4. 전자파 속도

| Row | Flow | Exam memory line | Learner action | Status |
|---|---|---|---|---|
| `p180 q43` | `epsilon, mu -> v` | 전자파 속도는 유전율과 투자율이 정한다. | 진공인지 매질인지 먼저 확인한다. | usable-review |
| `p180 q47` | `epsilon_r = 1, mu_r = 1 -> c` | 진공에서는 상대 유전율과 상대 투자율이 1이라 c가 된다. | `c`와 `v = 1/sqrt(epsilon mu)`를 같은 계열로 묶는다. | usable-review |

Supervisor note:

```text
Wave-speed rows should be used as the endpoint of the medium-constant story, not as isolated formula memorization.
```

## Hold Rows

These remain cleanup-only or hold. Do not turn them into exam memory lines.

| Row | Reason | Treatment |
|---|---|---|
| `p4 q1` | answer or choice conflict | hold |
| `p154 q1` | calculation/answer conflict | hold |
| `p158 q9` | choice alignment contamination | hold |
| `p57 q7` | boundary-condition answer conflict | hold |
| `p130 q3` | figure dependency and likely calculation conflict | hold |

## Cross-Bundle Reading

The integrated review surface should let a learner read rows in this order:

```text
E and C anchors
-> flux change and induction
-> self/mutual inductance
-> D time variation and Maxwell
-> epsilon/mu and wave speed
```

The important study insight:

```text
전기자기학은 공식명 목록이 아니라 물리량 이동 지도다.
```

## Non-Authorization Closeout

This document does not authorize:

- PR merge;
- PR ready-for-review transition;
- YAML mutation;
- source-data mutation;
- answer-key mutation;
- JSON mutation;
- concept-card creation;
- concept-card promotion;
- `expansion_pilot` promotion.
