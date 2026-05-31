# Concept Card Expansion Backlog

작성일: 2026-05-30 KST
근거: MOAI verified YAML body + review table vs Codex reviewed draft comparison

## 1. Purpose

현재 30개 Codex reviewed draft를 교체하지 않고, MOAI가 드러낸 standalone concept 후보를 backlog로 분리한다.

MOAI artifact는 `moai_artifacts/`에 보존되어 있으며 Codex-side parse 검증도 통과했다. 다만 corpus grounding과 semantic gain은 아직 미검증이다.

이 backlog는 생성 승인 목록이 아니다. 다음 batch 후보 목록이다.

## 2. High-value Candidate Cards

| priority | proposed file | concept | rationale | review risk |
|---:|---|---|---|---|
| 1 | `q_bandwidth.yaml` | Q·BW | Codex에서는 RLC resonance에 포함되어 있으나 MOAI가 별도 risk를 잘 포착 | MEDIUM |
| 2 | `parallel_rlc_resonance.yaml` | RLC 병렬 공진 | 직렬 공진과 병렬 공진의 시험 함정이 다를 수 있음 | LOW/MEDIUM |
| 3 | `power_factor_correction.yaml` | 역률 개선 | 고조파 환경에서 콘덴서 단독 보상 위험을 분리 가능. MOAI risk는 LOW이나 corpus partial 표시가 있어 별도 card 가치 있음 | LOW/MEDIUM |
| 4 | `initial_final_value_theorems.yaml` | 초기값·최종값 정리 | 라플라스 card 안에 넣기보다 성립 조건을 별도 card로 관리 가능 | MEDIUM |
| 5 | `transfer_function.yaml` | 전달함수 H(s) | 라플라스/s-domain과 겹치지만 제어 확장 boundary를 분리 가능 | MEDIUM |
| 6 | `filter_cutoff_frequency.yaml` | 필터 분류·차단주파수 | RLC/Bode와 연결되나 시험 trigger가 독립적 | LOW/MEDIUM |
| 7 | `distortion_power_factor.yaml` | 비정현파 전력·왜형 역률 | complex power / power factor / harmonics 사이의 위험 경계 보강 | MEDIUM |

## 3. Human-review / Broad-scope Candidate Cards

| proposed file | concept | reason for caution |
|---|---|---|
| `image_impedance.yaml` | 영상 임피던스 | 최대전력 정합과 혼동 위험. local corpus grounding 확인 필요 |
| `reciprocity_theorem.yaml` | 가역성 정리 | 모든 회로 가역적이라는 overclaim 위험 |
| `routh_hurwitz.yaml` | 라우스-후르비츠 | 제어공학 경계. 회로이론 core로 승격 금지 |
| `state_space.yaml` | 상태공간 | 제어공학 경계. broad-scope card로만 검토 |

## 4. Not a Claim

이 문서는 다음을 주장하지 않는다.

- 후보 card들이 생성 승인되었다.
- corpus grounding이 확인되었다.
- 기존 30개가 부족하다는 최종 판정이다.
- MOAI draft가 Codex draft보다 우월하다.

## 5. Recommended Next Gate

다음 gate 후보:

**Expansion Pilot Gate**

추천 범위:

- high-value candidate 중 3개만 먼저 작성
- 추천 3개:
  - `q_bandwidth.yaml`
  - `power_factor_correction.yaml`
  - `initial_final_value_theorems.yaml`

이 3개는 기존 30개와 겹치면서도 risk boundary를 선명하게 만들 가능성이 크다.
