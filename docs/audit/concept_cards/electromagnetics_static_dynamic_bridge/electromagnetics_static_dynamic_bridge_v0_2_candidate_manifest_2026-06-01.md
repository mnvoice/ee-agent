# Electromagnetics Static / Dynamic Bridge v0.2 Candidate Manifest - 2026-06-01

Scope: review-only candidate manifest for the next electromagnetic static/dynamic bridge pass.

This document does not create study cards. It selects a review queue from already-reviewed v0.1 evidence and the integrated learning map.

## Guardrails

- Keep PR #1 open, draft, and unmerged.
- Do not patch YAML.
- Do not create new concept-card YAML files.
- Do not promote `expansion_pilot` cards.
- Do not claim gold-set, benchmark, semantic-gain, or production readiness.
- Treat pressure flags as evidence signals only, not patch authorization.

## Selection Principle

The v0.2 queue is selected by physical-quantity movement, not formula-name collection.

Primary question:

```text
What moves into what?
```

Examples:

```text
Q or rho -> E -> D -> Psi
I or J -> H -> B -> Phi
Phi -> dPhi/dt -> e
i -> di/dt -> e = -L di/dt
D -> partial D / partial t -> displacement current -> H
epsilon, mu -> v = 1/sqrt(epsilon mu)
```

## Candidate Summary

| Class | Count | Meaning |
|---|---:|---|
| Usable-review candidate | 14 | Good review candidates for the integrated learning map. |
| Caveated-review candidate | 4 | Useful but must retain cleanup or figure caveat. |
| Cleanup-only / hold | 5 | Must not become study-facing rows. |
| Total tracked rows | 23 | v0.1-derived continuation set. |

This is a review queue count, not a benchmark or readiness claim.

## v0.2 Candidate Queue

| Row | Bundle | Physical quantity flow | Static parent | Dynamic bridge | Cross-subject target | Source status | Candidate decision |
|---|---|---|---|---|---|---|---|
| `p5 q3` | 정전계 / 정자계 앵커 | `Q -> E` | 전하 | none | 정전계 기본 | source-grounded | usable-review |
| `p7 q8` | 정전계 / 정자계 앵커 | `surface charge -> E` | 면전하 | none | 정전계 기본 | source-grounded | usable-review |
| `p11 q3` | 정전계 / 정자계 앵커 | `Q -> V` | 점전하 | none | 정전계 기본 | source-grounded | usable-review |
| `p37 q3` | 정전계 / 정자계 앵커 | `epsilon, geometry -> C` | 유전체 / 도체 형상 | none | 회로이론 C | source-grounded | usable-review |
| `p39 q7` | 정전계 / 정자계 앵커 | `C, V -> stored energy` | 정전용량 | none | 회로 에너지 | source-grounded | usable-review |
| `p147 q1` | 유도기전력 | `N Phi -> d(N Phi)/dt -> e` | 자속 쇄교수 | Faraday induction | 전기기기 | source-grounded | usable-review |
| `p147 q2` | 유도기전력 | `Phi change -> e direction` | 자속 / 방향성 | Faraday + Lenz | 전기기기 | source-grounded | usable-review |
| `p154 q2` | 인덕턴스 / 결합 | `i -> di/dt + L -> e` | 자기인덕턴스 | self-induced voltage | 회로이론 | source-grounded with cleanup caveat | caveated-review |
| `p168 q59` | 인덕턴스 / 결합 | `L1, L2, k -> M` | 자기인덕턴스 | coupling coefficient | 회로이론 / 전기기기 | source-grounded | usable-review |
| `p168 q60` | 인덕턴스 / 결합 | `i1 -> di1/dt + M -> e2` | 상호 유도 | mutual induced voltage | 전기기기 | source-grounded | usable-review |
| `p170 q3` | 맥스웰 / 변위전류 | `D -> partial D / partial t -> displacement current density` | 전속밀도 | displacement current density | Maxwell / 전자파 | source-grounded | usable-review |
| `p170 q4` | 맥스웰 / 변위전류 | `D(t) -> displacement current` | 전속밀도 | displacement current | Maxwell / 전자파 | source-grounded | usable-review |
| `p174 q14` | 맥스웰 / 변위전류 | `partial D / partial t -> H` | 전속밀도 | Maxwell correction | Maxwell / 전자파 | source-grounded | usable-review |
| `p180 q43` | 전자파 속도 | `epsilon, mu -> v` | 매질상수 | wave propagation | 전력공학 / 전자파 | source-grounded | usable-review |
| `p180 q47` | 전자파 속도 | `epsilon_r = 1, mu_r = 1 -> c` | 진공 기준 | vacuum wave speed | 전자파 / 송전 개념 | source-grounded | usable-review |

## Caveat Detail

| Row | Bundle | Physical quantity flow | Caveat | Candidate decision |
|---|---|---|---|---|
| `p36 q1` | 정전계 / 정자계 앵커 | `charge / voltage relation -> capacitance unit` | Extracted choice text carries appended explanation. | caveated-review |
| `p154 q2` | 인덕턴스 / 결합 | `i -> di/dt + L -> e` | Calculation path is usable, but extracted choice text carries cleanup residue. | caveated-review |
| `p166 q50` | 인덕턴스 / 결합 | `magnetic circuit / turns / flux coupling -> M` | Figure dependency must remain visible. | caveated-review |
| `p166 q52` | 인덕턴스 / 결합 | `mu, S, N1, N2, l -> M` | Figure or OCR residue must remain visible. | caveated-review |

## Cleanup-Only / Hold Rows

These rows may be used only as cleanup evidence, not as study-facing candidates.

| Row | Blocker | v0.2 treatment |
|---|---|---|
| `p4 q1` | answer or choice conflict | hold |
| `p154 q1` | calculation/answer conflict | hold |
| `p158 q9` | choice alignment contamination | hold |
| `p57 q7` | boundary-condition answer conflict | hold |
| `p130 q3` | figure dependency and likely calculation conflict | hold |

## v0.2 Review Order

Recommended order:

1. Start with the static anchors: `p5 q3`, `p7 q8`, `p11 q3`, `p37 q3`, `p39 q7`, plus caveated `p36 q1`.
2. Move to induction: `p147 q1`, `p147 q2`.
3. Move to inductance and coupling: `p154 q2`, `p166 q50`, `p166 q52`, `p168 q59`, `p168 q60`.
4. Move to Maxwell and displacement current: `p170 q3`, `p170 q4`, `p174 q14`.
5. Finish with wave speed: `p180 q43`, `p180 q47`.

Reason:

```text
The learner sees static quantities first, then time change, then coupling, then Maxwell, then wave speed.
```

## Next Artifact Recommendation

The next artifact should be an HTML review surface:

```text
electromagnetics_static_dynamic_bridge_v0_2_candidate_review.html
```

The HTML should show:

- five bundles;
- physical quantity flow per row;
- source status;
- caveat labels;
- cleanup-only rows separated from candidates;
- no YAML, JSON, answer-key, or concept-card mutation.

## Git Parallel Save Note

If mirrored to Git later, this manifest should be copied only as a review artifact under a dedicated audit path. It should not be mixed with source data patches.

Recommended path:

```text
docs/audit/concept_cards/electromagnetics_static_dynamic_bridge/electromagnetics_static_dynamic_bridge_v0_2_candidate_manifest_2026-06-01.md
```

Do not use broad add commands in the dirty local repository.

## Non-Authorization Closeout

This manifest does not authorize:

- PR merge;
- PR ready-for-review transition;
- YAML mutation;
- source-data mutation;
- answer-key mutation;
- JSON mutation;
- concept-card creation;
- concept-card promotion;
- `expansion_pilot` promotion.
