# Tier-B Note Merge + Expansion Pilot Advisory v0.1

작성일: 2026-05-30 KST
작성 채널: MoAI (advisory only)
검토 권한: Codex supervisor + user

## Inputs verified

| Source | Path | Status |
|---|---|---|
| Codex baseline 30 cards | `/Users/jeong-ujin_1/Documents/Codex/2026-05-30/ee-agent-d-3-governance-repo/concept_cards/*.yaml` | read OK |
| Codex supervisor decision memo | `.../concept_card_supervisor_decision_memo_2026-05-30.md` | read OK |
| MoAI independent draft | `/Users/jeong-ujin_1/circuit_theory_concept_cards_independent_draft_v0.1.yaml` | session-resident |
| MoAI comparison report | `/Users/jeong-ujin_1/circuit_theory_concept_cards_codex_vs_moai_comparison_v0.1.md` | session-resident |

Mutation: 0 (Codex 파일 / MoAI 파일 / 본 advisory 외 산출물 모두 미접촉).

---

## 1. Gate Summary

**Gate 이름**: Concept Card Tier-B Note Merge + Expansion Pilot Gate
**Mode**: advisory (patch suggestions only, no file mutation)
**Baseline**: Codex 30-card reviewed draft (unchanged)
**MoAI 역할**: note-merge patch 제안 + 3개 신규 pilot YAML 초안 제출

**Scope (supervisor memo §5와 일치)**:

| Part | Target | Count |
|------|--------|------|
| A. NOTE_MERGE (기존 Codex 카드 보강 제안) | thevenin_equivalent / balanced_three_phase / second_order_response / symmetrical_components | 4 |
| B. New pilot YAML 초안 (Codex 신규 카드 후보) | q_bandwidth / power_factor_correction / initial_final_value_theorems | 3 |

**Scope 외 (생성 안 함)**:

- `image_impedance.yaml` — supervisor defer
- `reciprocity.yaml` — supervisor defer
- `routh_hurwitz.yaml` — supervisor defer (broad-scope)
- `state_space.yaml` — supervisor defer (broad-scope)
- `filter_cutoff_frequency.yaml` — supervisor memo §5에 "optional if scope allows"였으나 본 task 명시 3개에 불포함이므로 생성 안 함
- `transfer_function.yaml` — supervisor defer

**Hard constraints (본 advisory 전체 적용)**:

- Codex 파일 무수정 (advisory만)
- MoAI 파일 무수정
- final approval 주장 없음
- corpus grounding 완료 주장 없음
- gold set 선언 없음
- pilot 3개 초과 신규 카드 생성 없음

---

## 2. Part A — Proposed Note-Merge Patches (4 existing cards)

각 카드는 **변경 부분만** 명시. 다른 모든 필드는 Codex 원본을 그대로 유지.

---

### 2.1 `thevenin_equivalent.yaml` — note merge 제안

**Supervisor goal**: 종속전원 시 R_TH를 test source method로 구하는 절차 명시. Norton 카드 합본 회피. extension_risk MEDIUM 유지.

**Change locus**: `word_roles` 1키 추가 + `risk` 보강. formula_core / dynamic_destinations / extension_risk 무변경.

**BEFORE → AFTER (변경 필드만 표시)**:

```yaml
# word_roles  [ADD 1 key: test_source_method]
word_roles:
  equivalent: 특정 단자에서 보면 같다는 뜻
  source_impedance: 전원이 가진 내부 성격
  loading_effect: 부하가 앞단 회로를 끌어내리는 현상
  interface: 두 시스템이 만나는 자리
  test_source_method: 종속전원만 있을 때 외부 시험 전원을 인가해 Rth = V_test / I_test로 구하는 절차    # ADD

# risk  [STRENGTHEN: dependent-source case 절차 명시]
risk: 종속전원이 포함된 회로에서 독립전원만 0으로 두고 등가저항을 직접 합성하면 Rth가 틀리며, 이때는 외부 시험 전원을 단자에 인가해 Rth = V_test / I_test로 구해야 한다. 비선형 회로와 주파수 의존 회로에서는 동작점 또는 주파수 조건을 정해야 한다.    # MODIFY
```

**Unchanged**: concept / static_boundary / formula_core / dynamic_destinations / trigger_words / memory_logic / extension_risk.

**Note**: Norton 카드와의 합본은 회피. Norton 별도 카드는 supervisor Tier C 별도 검토.

**Risk-level after merge**: MEDIUM (변동 없음, supervisor goal 일치).

**Decision flag**: `needs_supervisor_decision: yes (word_roles 키명 / risk 문장 톤 confirm)`.

---

### 2.2 `balanced_three_phase.yaml` — note merge 제안

**Supervisor goal**: Y/Δ 선·상 관계식 추가. 평형 boundary 명시 유지. 불평형 적용 회피.

**Change locus**: `formula_core` 2식 추가 + `extension_risk.condition` 보강. 나머지 무변경.

**BEFORE → AFTER (변경 필드만 표시)**:

```yaml
# formula_core  [ADD 2 entries with explicit balanced-only condition]
formula_core:
  - Va + Vb + Vc = 0
  - phase angle spacing = 120°
  - neutral current = 0
  - "Y connection (balanced only): V_L = sqrt(3) V_phase, I_L = I_phase"            # ADD
  - "Delta connection (balanced only): V_L = V_phase, I_L = sqrt(3) I_phase"        # ADD

# extension_risk  [STRENGTHEN condition: Y/Delta sqrt(3) 관계도 평형 조건 한정 명시]
extension_risk:
  level: LOW
  condition: 세 상 크기와 위상 간격이 같은 표준 평형 문제에서는 안전하며, Y/Delta sqrt(3) 선·상 관계도 동일한 평형 조건에서만 성립함    # MODIFY
  caution: 불평형 부하나 결상 상태를 평형 공식으로 처리하면 위험함
```

**Unchanged**: concept / static_boundary / dynamic_destinations / word_roles / trigger_words / memory_logic / risk.

**Risk-level after merge**: LOW (변동 없음. 평형 조건이 condition에 명시되어 있어 LOW 적정).

**Decision flag**: `needs_supervisor_decision: yes (formula 표기 형식 — "Y connection" vs "Y:" 등 표기 통일 확인)`.

---

### 2.3 `second_order_response.yaml` — note merge 제안

**Supervisor goal**: 직렬 RLC 한정 ζ 식 추가, "formula condition must be explicit". MEDIUM 유지.

**Change locus**: `formula_core` 1식 추가. 나머지 무변경.

**BEFORE → AFTER (변경 필드만 표시)**:

```yaml
# formula_core  [ADD 1 entry, condition explicit: "series RLC only"]
formula_core:
  - omega0 = 1/sqrt(L C)
  - alpha = R / (2 L)
  - zeta = alpha / omega0
  - "series RLC only: zeta = (R/2) sqrt(C/L)"        # ADD (condition explicit per supervisor)
```

**Unchanged**: 다른 모든 필드.

**Note**: 병렬 RLC 또는 임의 2차 시스템에 이 식을 그대로 적용하면 안 됨. supervisor가 명시한 "condition must be explicit"를 식 머리에 `series RLC only:` 접두어로 박제.

**Risk-level after merge**: MEDIUM (변동 없음).

**Decision flag**: `needs_supervisor_decision: low (식 표기만 confirm)`.

---

### 2.4 `symmetrical_components.yaml` — note merge 제안

**Supervisor goal**: V_0 / V_1 / V_2 (또는 I_0/I_1/I_2) 3 분해식 모두 명시. zero-sequence caution 유지. MEDIUM 유지.

**Change locus**: `formula_core` 2식 추가. 나머지 무변경.

**BEFORE → AFTER (변경 필드만 표시)**:

```yaml
# formula_core  [ADD 2 entries for full sequence decomposition]
formula_core:
  - I0 = (Ia + Ib + Ic) / 3
  - "I1 = (Ia + a Ib + a^2 Ic) / 3"        # ADD (positive sequence)
  - "I2 = (Ia + a^2 Ib + a Ic) / 3"        # ADD (negative sequence)
  - a = 1∠120°
```

**Unchanged**: 다른 모든 필드. zero-sequence path caution은 `risk`/`extension_risk.caution`에 이미 박제되어 있음.

**Risk-level after merge**: MEDIUM (변동 없음, supervisor 명시).

**Decision flag**: `needs_supervisor_decision: low (식 표기 confirm)`.

---

## 3. Part B — Proposed Pilot YAML Drafts (3 new cards)

본 3개 YAML은 **advisory drafts**이며 Codex `concept_cards/` 폴더에 저장하지 않습니다. 본 보고서 내부 텍스트로만 제출. supervisor가 채택 시 Codex 측이 직접 파일 생성.

각 YAML은 정해진 schema와 field 순서를 정확히 보존: `concept` → `static_boundary` → `formula_core` → `dynamic_destinations` → `word_roles` → `trigger_words` → `memory_logic` → `risk` → `extension_risk{level, condition, caution}`.

---

### 3.1 `q_bandwidth.yaml` — pilot draft

**Supervisor goal recap** (memo §4 Tier A): RLC 통합 카드 유지 + Q/BW를 분리 pilot으로 신규. 시험 빈출 분리 가치. Q가 보편적으로 좋다는 일반화 금지. MEDIUM 권장.

**Draft YAML**:

```yaml
concept: quality factor and bandwidth
static_boundary: 회로이론에서 2차 RLC 공진 회로의 응답이 얼마나 좁고 날카로운지를 무차원 Q와 -3dB 대역폭 BW로 정량화하는 표현
formula_core:
  - Q = omega0 / BW
  - "BW = omega2 - omega1"
  - "series RLC resonance only: Q = omega0 L / R"
  - "parallel RLC resonance only: Q = R / (omega0 L)"
  - "standard 2nd-order LTI resonance only: zeta ≈ 1/(2Q)"
dynamic_destinations:
  - filter selectivity design
  - resonator and oscillator quality
  - control damping interpretation (conditional)
word_roles:
  selectivity: Q가 클수록 좁은 주파수 대역만 통과시키는 성질
  sharpness: 공진 곡선이 얼마나 뾰족한지
  bandwidth: 응답이 -3dB까지 유지되는 주파수 폭
  damping_relation: 2차 LTI 공진에 한해 Q와 감쇠비가 zeta ≈ 1/(2Q)로 연결되는 조건부 관계
trigger_words:
  - 품질계수
  - 대역폭
  - -3dB
  - 선택도
  - Q값
memory_logic: Q는 공진이 얼마나 좁고 날카로운지를 한 수로 압축한 값이고, BW는 그 공진의 폭을 주파수로 본 값이다.
risk: Q가 클수록 좋다고 외우면 안 되며, 필터 선택도에는 유리하지만 제어 응답에서는 큰 Q가 overshoot와 ringing을 키울 수 있다.
extension_risk:
  level: MEDIUM
  condition: 단일 2차 RLC 공진의 협대역 정상상태 안에서는 안전함
  caution: 광대역 시스템, 다중 공진, 비선형 손실, 시변 부하, 임의 2차 근사 제어 시스템에는 단일 Q 한 값으로 거동을 요약할 수 없음
```

**Boundary notes (advisory)**:

- RLC 공진 카드(`rlc_resonance.yaml`)와의 관계: Q/BW를 분리 pilot으로 두고, 원본 카드에서는 정의만 유지. 두 카드 간 cross-link은 supervisor가 후속 결정.
- 시험 빈출도 관점에서 -3dB / 선택도 / Q 산정이 단독 출제될 수 있어 분리 가치 있음.
- broad-scope 여부: 회로이론 core 범위 (RLC 공진의 직접 파생) → broad-scope 아님. 단 `damping_relation` 항목은 제어공학 경계로 향함.

**Risk-level rationale**: 단일 2차 공진에 한정될 때는 LOW에 가깝지만, 제어계 2차 근사로의 확장 가능성과 다중 공진/비선형 손실 등 일반화 위험을 봐서 MEDIUM 권장. supervisor가 LOW로 낮추거나 MEDIUM 유지 결정 가능.

**Decision flag**: `needs_supervisor_decision: yes (level LOW vs MEDIUM, 식 표기 통일, parallel RLC 항 포함 여부)`.

---

### 3.2 `power_factor_correction.yaml` — pilot draft

**Supervisor goal recap** (memo §4 Tier B): `power_factor.yaml` (정의 카드)와 분리. 보상 절차 / 진상 / 과보상 / 고조파 환경 + 직렬 리액터 위험 명시. MEDIUM 권장.

**Draft YAML**:

```yaml
concept: power factor correction
static_boundary: 회로이론에서 정현파 정상상태의 유도성 부하에 병렬 커패시터를 달아 무효전력을 일부 상쇄해 cos(phi)를 개선하는 절차
formula_core:
  - "Q_C = P (tan(phi1) - tan(phi2))"
  - "C = Q_C / (omega V^2)"
  - "P is unchanged; S and line current decrease after compensation"
dynamic_destinations:
  - utility consumer power factor compensation
  - transmission and distribution loss reduction
  - transformer loading relief
word_roles:
  lagging: 유도성 부하에서 전류가 전압보다 늦는 상태
  leading: 보상이 과해 전류가 전압보다 앞서는 진상 상태
  overcompensation: 콘덴서 용량이 과해 leading 영역으로 넘어간 상태
  series_reactor: 고조파 환경에서 콘덴서와 직렬로 추가하여 공진 위험을 줄이는 인덕터
trigger_words:
  - 역률개선
  - 콘덴서보상
  - 진상
  - 지상
  - 과보상
  - kVar보상
memory_logic: 역률 개선은 콘덴서가 인덕터의 무효전력을 자기 안에서 돌려받아 전원이 안 보낸 것처럼 만드는 절차다.
risk: 콘덴서 용량을 과하게 잡으면 진상으로 넘어가 단자 전압 상승과 계전기 오동작이 발생할 수 있으며, 고조파 부하 환경에서 직렬 리액터 없이 콘덴서만 달면 콘덴서와 계통 인덕턴스가 공진해 고조파가 증폭될 위험이 있다.
extension_risk:
  level: MEDIUM
  condition: 정현파 정상상태, 단일 주파수, 균형 부하, 표준 콘덴서 보상 범위 안에서는 안전함
  caution: 비정현파 환경, 고조파 부하, 콘덴서 직렬 공진 위험, 전압 상승에 의한 절연 부담, 자동 콘덴서 군 동작은 별도 평가가 필요하며 본 식만으로는 부족함
```

**Boundary notes (advisory)**:

- `power_factor.yaml` (정의 카드)와 명시적 분리. 정의는 원본 카드에 유지, 절차/실무 catch는 본 pilot.
- 단순 단상 정현파 케이스 한정. 3상·고조파 시 별도 검토.
- broad-scope 여부: 회로이론 core 범위 (콘덴서 보상은 시험 기본 절차). 단 고조파 + 직렬 리액터 영역은 전력공학 경계로 향함.

**Risk-level rationale**: 단순 정현파 단상 보상은 LOW에 가깝지만, 실무 운용에서 발생 가능한 과보상·고조파 공진 위험을 보면 MEDIUM 권장 (supervisor memo §4 Tier B 명시).

**Decision flag**: `needs_supervisor_decision: yes (level confirm, series_reactor word_role 키명, formula_core 효과 노트 표기)`.

---

### 3.3 `initial_final_value_theorems.yaml` — pilot draft

**Supervisor goal recap** (memo §4 Tier C): 라플라스 카드와 분리. 정의 + 성립 조건 + RHP 극 / 지속 진동 시 적용 금지 경고. MEDIUM.

**Draft YAML**:

```yaml
concept: initial value and final value theorems
static_boundary: 회로이론에서 라플라스 변환 F(s)의 s 극한을 이용해 시간 영역의 t = 0+ 값과 t 무한대 정상상태 값을 직접 역변환 없이 얻는 두 정리
formula_core:
  - "initial value: f(0+) = lim s F(s) as s -> infinity"
  - "final value: f(infinity) = lim s F(s) as s -> 0"
  - "final value theorem requires: all poles of s F(s) lie in LHP, with at most a simple pole at s = 0"
dynamic_destinations:
  - quick steady-state value check
  - control system step-response endpoint estimation
  - transient response sanity check
word_roles:
  s_large: s 무한대 극한이 시간 영역의 t = 0+ 순간을 보는 통로
  s_zero: s 0 극한이 시간 영역의 t 무한대 정상상태를 보는 통로
  applicability_condition: 최종값 정리가 성립하기 위한 극의 위치 조건
  steady_state_endpoint: 충분히 시간이 지난 뒤 응답의 도착값
trigger_words:
  - 초기값정리
  - 최종값정리
  - 정상상태오차
  - 라플라스극한
memory_logic: s가 무한으로 가면 시간 영역의 t = 0 직후 순간을 보고, s가 0으로 가면 시간이 충분히 지난 정상상태를 보는 두 개의 창문이다.
risk: 최종값 정리는 시스템이 안정할 때만 의미가 있으며, 우반평면 극을 가진 불안정 시스템, jw 축 위의 비원점 극을 가진 지속 진동 시스템, 또는 발산 응답에 적용해 0 또는 유한값이라 답하면 틀린다.
extension_risk:
  level: MEDIUM
  condition: 선형 시불변 시스템이고 s F(s)의 극이 모두 좌반평면이거나 s = 0의 단순극만 허용되는 경우에 안전함
  caution: 우반평면 극을 가진 불안정 시스템, jw 축 비원점 극을 가진 지속 진동 시스템, 비선형 시스템, 시변 시스템에는 적용 금지이며 라플라스 자체의 ROC 조건도 함께 확인해야 함
```

**Boundary notes (advisory)**:

- `laplace_transform.yaml` (라플라스 변환 카드)와 분리. 라플라스 도구와 별도로 정리 카드. 두 카드 간 cross-link은 supervisor 결정.
- broad-scope 여부: 회로이론 / 제어공학 공통 도구. 회로이론 시험에서 정상상태 오차 평가 도구로 출제 가능.

**Risk-level rationale**: 성립 조건이 까다롭고 misuse 위험이 높아 MEDIUM. supervisor가 LOW로 낮추기에는 RHP 극 / 지속 진동 시 답이 정반대로 나오는 위험이 있어 MEDIUM 유지 권장.

**Decision flag**: `needs_supervisor_decision: yes (level confirm, formula_core 표기 영문/한글 통일, "lim s F(s) as s -> infinity" vs "lim_{s -> infinity} s F(s)" 표기 confirm)`.

---

## 4. Risk and Claim Boundary Table

### 4.1 Risk-level 분포 (제안 후 예상)

| 카드 | 변경 전 | 변경 후 (제안) | 변동 사유 |
|---|---|---|---|
| `thevenin_equivalent.yaml` | MEDIUM | MEDIUM | supervisor 명시 유지 |
| `balanced_three_phase.yaml` | LOW | LOW | 평형 조건이 condition에 박제. 변경 없음 |
| `second_order_response.yaml` | MEDIUM | MEDIUM | supervisor 명시 유지 |
| `symmetrical_components.yaml` | MEDIUM | MEDIUM | supervisor 명시 유지 |
| `q_bandwidth.yaml` (신규) | — | MEDIUM (제안) | 광대역·다중 공진 일반화 위험 |
| `power_factor_correction.yaml` (신규) | — | MEDIUM (제안) | 과보상·고조파 공진 위험 |
| `initial_final_value_theorems.yaml` (신규) | — | MEDIUM (제안) | RHP 극·지속 진동 misuse 위험 |

### 4.2 Broad-scope / corpus-gap audit

| 카드 | broad-scope? | corpus-gap? | grounding 추가 검증 필요? |
|---|---|---|---|
| `thevenin_equivalent.yaml` 패치 | no | no | no |
| `balanced_three_phase.yaml` 패치 | no | no | no |
| `second_order_response.yaml` 패치 | partial (제어계 2차 근사 경계는 Codex 원본 caveat이 이미 catch) | no | no |
| `symmetrical_components.yaml` 패치 | partial (전력계통 고장해석 경계는 Codex 원본 caveat이 이미 catch) | no | no |
| `q_bandwidth.yaml` (신규) | no (회로이론 core 직접 파생) | low | supervisor confirm |
| `power_factor_correction.yaml` (신규) | partial (고조파 영역 전력공학 경계) | low | supervisor confirm |
| `initial_final_value_theorems.yaml` (신규) | partial (제어공학 공통 도구) | low | supervisor confirm |

### 4.3 Forbidden grounding checks

```yaml
forbidden_grounding_checks:
  answer_key_used_as_grounding: false
  generated_solution_used_as_grounding: false
  generated_explanation_used_as_grounding: false
  generated_rationale_used_as_grounding: false
  evidence_card_summary_treated_as_proof: false
  forbidden_source_used: false
  prior_artifact_mutation_used_as_authority: false
```

### 4.4 Claim boundary (본 advisory 명시)

**말하지 않는 것**:

- ❌ 4개 NOTE_MERGE 패치가 supervisor 최종 승인을 받았다.
- ❌ 3개 pilot YAML이 Codex `concept_cards/`에 추가되었다.
- ❌ 본 advisory가 Codex 30-card baseline을 33-card 또는 34-card로 승격했다.
- ❌ corpus grounding이 완료되었다.
- ❌ semantic gain이 정량 측정되었다.
- ❌ 본 advisory가 정식 학습 자료다.
- ❌ broad-scope 카드(라우스 / 상태공간 / image_impedance / reciprocity)를 본 gate에서 추가했다.

**말할 수 있는 것**:

- ✅ Codex supervisor decision memo와 task scope가 일치함을 직접 확인했다.
- ✅ 4개 NOTE_MERGE 패치는 supervisor goal에 따라 최소 변경 원칙으로 제안되었다.
- ✅ 3개 pilot YAML 초안은 supervisor goal에 따라 schema와 risk 정책을 보존했다.
- ✅ mutation 0 (Codex / MoAI / prior artifact 어떤 파일도 수정하지 않았다).
- ✅ 각 제안에 `needs_supervisor_decision` flag를 명시했다.

---

## 5. Supervisor Decision Checklist

각 항목 supervisor가 yes/no/modify 결정 후 Codex 측에서 patch 적용 또는 polish 진행.

### 5.1 Part A — Note merge decisions (4 카드)

| # | Card | Change | Decision |
|---|------|--------|----------|
| A-1 | `thevenin_equivalent.yaml` | word_roles에 `test_source_method` 추가 | ☐ accept ☐ modify ☐ reject |
| A-2 | `thevenin_equivalent.yaml` | risk에 test source method 절차 명시 | ☐ accept ☐ modify ☐ reject |
| A-3 | `balanced_three_phase.yaml` | formula_core에 Y/Δ sqrt(3) 2식 추가 (balanced only 접두) | ☐ accept ☐ modify ☐ reject |
| A-4 | `balanced_three_phase.yaml` | extension_risk.condition에 Y/Δ 관계도 평형 조건 한정 명시 | ☐ accept ☐ modify ☐ reject |
| A-5 | `second_order_response.yaml` | formula_core에 `series RLC only: zeta = (R/2) sqrt(C/L)` 추가 | ☐ accept ☐ modify ☐ reject |
| A-6 | `symmetrical_components.yaml` | formula_core에 I_1, I_2 분해식 2개 추가 (I_0와 a=1∠120° 사이) | ☐ accept ☐ modify ☐ reject |

### 5.2 Part B — Expansion pilot decisions (3 신규 카드)

| # | Card | Decision points | Decision |
|---|------|-----------------|----------|
| B-1 | `q_bandwidth.yaml` | 채택 여부 (생성 승인) | ☐ accept ☐ modify ☐ reject |
| B-2 | `q_bandwidth.yaml` | extension_risk.level: LOW vs MEDIUM | ☐ LOW ☐ MEDIUM |
| B-3 | `q_bandwidth.yaml` | parallel RLC Q 식 포함 여부 (시리즈만 vs 시리즈+병렬) | ☐ series only ☐ series + parallel |
| B-4 | `power_factor_correction.yaml` | 채택 여부 (생성 승인) | ☐ accept ☐ modify ☐ reject |
| B-5 | `power_factor_correction.yaml` | extension_risk.level: MEDIUM 확정 | ☐ MEDIUM ☐ other |
| B-6 | `power_factor_correction.yaml` | series_reactor를 word_roles 키로 둘지 vs caution에만 둘지 | ☐ key ☐ caution only |
| B-7 | `initial_final_value_theorems.yaml` | 채택 여부 (생성 승인) | ☐ accept ☐ modify ☐ reject |
| B-8 | `initial_final_value_theorems.yaml` | extension_risk.level: MEDIUM 확정 | ☐ MEDIUM ☐ other |
| B-9 | `initial_final_value_theorems.yaml` | formula 표기 형식: "lim s F(s) as s -> infinity" vs "lim_{s -> infinity} s F(s)" | ☐ "as s ->" ☐ "lim_{s ->}" |

### 5.3 Cross-cutting decisions

| # | Item | Decision |
|---|------|----------|
| C-1 | 본 advisory에서 제안된 7개 변경 전체를 한 patch gate에서 처리 vs 단계별 처리 | ☐ batch ☐ staged |
| C-2 | pilot 3개 신규 카드 status: `expansion_pilot` 유지 (supervisor memo §7과 일치) | ☐ confirm ☐ override |
| C-3 | Codex 30-card baseline status: 변경 없음 유지 | ☐ confirm ☐ override |
| C-4 | review summary update 시점: 본 gate 종료 직후 vs 다음 gate | ☐ this gate ☐ next gate |

---

## 6. Recommended Next Steps (MoAI 의견)

1. **supervisor가 Part A 6개 decision (A-1 ~ A-6) 검토** → accept/modify/reject 표기.
2. **supervisor가 Part B 9개 decision (B-1 ~ B-9) 검토** → accept/modify/reject 표기.
3. **supervisor가 Cross-cutting 4개 decision (C-1 ~ C-4) 결정**.
4. Codex 측이 결정된 patch를 Codex `concept_cards/` 폴더에 적용 (mutation은 supervisor 권한 영역).
5. PyYAML safe_load로 patch 후 30+pilot N 카드 전체 parse 재검증.
6. `concept_card_review_summary_2026-05-30.md` update (verdict count 또는 separate `expansion_pilot_review` section 추가).
7. 본 advisory 보고서를 Codex 측 `moai_artifacts/`에 사본 보관 (supervisor 결정 시).

---

## 7. Mutation Audit

```yaml
mutation_counters:
  codex_yaml_mutation_count: 0
  codex_md_mutation_count: 0
  moai_yaml_mutation_count: 0
  moai_md_mutation_count: 0
  pilot_files_created_in_codex_path_count: 0
  pilot_files_created_in_moai_advisory_only_count: 0
  prior_artifact_mutation_count: 0
  source_data_mutation_count: 0
  answer_key_mutation_count: 0
  corpus_mutation_count: 0
notes:
  - 본 advisory는 Codex 파일과 MoAI 파일을 직접 수정하지 않았다.
  - pilot YAML 3개는 본 보고서 안 텍스트로만 제출되었으며 Codex `concept_cards/` 폴더에 생성되지 않았다.
  - patch 적용 권한은 supervisor에게 있다.
```

---

TIER_B_NOTE_MERGE_AND_PILOT_ADVISORY_V0.1_READY_FOR_SUPERVISOR_REVIEW
