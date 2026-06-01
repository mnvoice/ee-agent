# Codex vs MoAI Concept Card Comparison Report v0.1

작성일: 2026-05-30 KST
작성 채널: MoAI (보조 비교자)
검토 권한: Codex (supervisor) + User (최종 결정자)

## Inputs verified

| Source | Path | Status |
|---|---|---|
| MoAI YAML (30 cards) | `/Users/jeong-ujin_1/circuit_theory_concept_cards_independent_draft_v0.1.yaml` | parsed OK |
| MoAI review table | `/Users/jeong-ujin_1/circuit_theory_concept_cards_independent_draft_v0.1_review_table.md` | read OK |
| Codex YAML (30 cards) | `/Users/jeong-ujin_1/Documents/Codex/2026-05-30/ee-agent-d-3-governance-repo/concept_cards/*.yaml` | 30/30 read OK |
| Codex review summary | `.../concept_card_review_summary_2026-05-30.md` | read OK |
| MoAI verified body record | `.../concept_card_moai_verified_body_record_2026-05-30.md` | read OK |

Mutation: 0 (Codex 파일 / MoAI 파일 양쪽 모두 미접촉).

---

## 1. Executive Summary

**비교 본질**:

- Codex 30 카드 = 30개 **분리 파일**(파일당 1 concept, 약 26-27 lines).
- MoAI 30 카드 = 1개 **합본 YAML**(list of 30 mappings).
- 두 set 모두 동일 schema(concept / static_boundary / formula_core / dynamic_destinations / word_roles / trigger_words / memory_logic / risk / extension_risk).
- 두 set 모두 YAML 구조는 통과. 두 set 모두 final 학습자료 아님.

**결론 (MoAI 비교 의견, 최종 결정은 Codex/User)**:

MoAI draft는 **Codex set을 대체하지 않는다.** Codex set은 **회로이론 시험 본문 core를 더 정밀하게 분해**(ohms_law / series_parallel / voltage_divider / current_divider / mutual_inductance 등 시험 빈출 기초 카드를 단독 보유)했고, MoAI draft는 **회로이론 → 인접 도메인 확장 경계**(Q·BW 단독, 영상 임피던스, 가역성, 라우스, 상태공간 등 broad-scope 카드)에서 추가 가치가 있음.

**권고**: MoAI draft를 Codex set의 **보완(supplement)** 으로 다룬다. MoAI-only 카드 중 3개는 추가 후보로 supervisor 결정 대기, 7개는 Codex 카드의 note 보강용으로만 활용, 2개는 broad-scope corpus-gap이라 별도 검토 필요.

**범위 차이 분포**:

| 분류 | 개수 | 예시 |
|---|---:|---|
| 동일 concept (1:1) | 16 | KVL/KCL, phasor, RLC resonance, complex_power, ... |
| 같은 family를 다른 방식으로 split/merge | 7 | Codex(nodal+mesh) vs MoAI(합본 1), Codex(rc+rl) vs MoAI(합본 1), Codex(rlc_resonance 1) vs MoAI(직렬+병렬+Q 3) |
| Codex-only | 5 | ohms_law, series_parallel_circuits, voltage_divider, current_divider, mutual_inductance |
| MoAI-only | 5 | RLC 병렬 공진 분리, Q·BW 단독, 영상 임피던스, 가역성 정리, 라우스-후르비츠, 상태공간 |

(detail Level 1에서 정리)

**금지 발언 (이 보고서에서 하지 않은 것)**:

- "MoAI draft가 Codex draft보다 우수하다" — 말하지 않았다.
- "Codex draft가 gold set이다" — 말하지 않았다.
- "corpus grounding이 완료되었다" — 말하지 않았다.
- "MoAI-only 카드가 모두 시험 학습 자료로 승격되어야 한다" — 말하지 않았다.

---

## 2. Coverage Map

표 약어:

- C(N) = Codex card "N.yaml"
- M(k) = MoAI card index k (1-30)

| concept_family | Codex file(s) | MoAI concept(s) | relationship | recommendation |
|---|---|---|---|---|
| 회로 보존법칙 | C(kirchhoff_laws) | M(1) KVL/KCL | 1:1 | KEEP_BOTH_CODEX_PRIMARY |
| 노드 해석 | C(nodal_analysis) | M(2) 노드해석+메쉬해석 합본 | 1:2 split | KEEP_CODEX (분리 유지가 시험 학습에 유리) |
| 메쉬 해석 | C(mesh_analysis) | M(2) (위 합본 안에 포함) | 1:2 split | KEEP_CODEX |
| 옴의 법칙 | C(ohms_law) | (없음) | Codex-only | KEEP_CODEX (필수 기초) |
| 직병렬 회로 | C(series_parallel_circuits) | (없음) | Codex-only | KEEP_CODEX (필수 기초) |
| 전압 분배 | C(voltage_divider) | (없음) | Codex-only | KEEP_CODEX |
| 전류 분배 | C(current_divider) | (없음) | Codex-only | KEEP_CODEX |
| 전원 변환 | C(source_transformation) | M(3) 전원 등가 변환 | 1:1 | KEEP_BOTH (Codex 우선, MoAI의 "이상 전원 제외" 조건이 약간 더 명시적) |
| 중첩 | C(superposition_theorem) | M(4) 중첩의 원리 | 1:1 | KEEP_BOTH (MoAI risk가 "전력은 비선형이라 동시 활성 재계산" 명시) |
| 테브난·노턴 | C(thevenin_equivalent) | M(5) 테브난·노턴 등가 | 1:1 (Codex는 Norton 별도 카드 없음) | KEEP_CODEX + NOTE_MERGE (MoAI의 "시험 전원법으로 R_TH" 절차를 Codex card note에 보강 권장) |
| 상호 인덕턴스 | C(mutual_inductance) | (없음) | Codex-only | KEEP_CODEX |
| 최대 전력 전달 | C(maximum_power_transfer) | M(6) | 1:1 | KEEP_BOTH (효율=50% 고정 + 전력계통 운용 caveat 동일) |
| 페이저 | C(phasor) | M(7) 페이저+복소 임피던스 합본 | 1:2 split | KEEP_CODEX (페이저·임피던스 분리가 학습 명료성에 유리) |
| 임피던스 | C(impedance) | M(7) (위 합본 안) | 1:2 split | KEEP_CODEX |
| RLC 공진 | C(rlc_resonance) | M(8) 직렬공진 + M(9) 병렬공진 + M(10) Q/BW = 3 카드 | 1:3 split | DECISION_NEEDED — Codex 1카드는 압축적, MoAI 3카드는 시험 빈출별 분리. 시험 학습 관점에서는 MoAI 분리가 유리할 수 있음. supervisor 결정 |
| 교류 4전력 | C(complex_power) | M(11) | 1:1 | KEEP_BOTH (Codex의 "RMS phasor 기준" 명시 vs MoAI의 "한 주기 평균 남는 게 유효" memory_logic 양쪽 상호 보완) |
| 역률 | C(power_factor) | M(12) 역률 개선 | 1:1 (관점 다름: Codex=정의, MoAI=보상 절차) | KEEP_BOTH + NEW_CARD_CONSIDER (M(12)는 "역률 개선" 실무 카드라 Codex의 power_factor와 보완. supervisor 결정 후 별도 카드로 추가 검토 가능) |
| 3상 평형 | C(balanced_three_phase) | M(13) 3상 평형 Y/Δ | 1:1 (Codex=상태 정의, MoAI=결선식) | KEEP_BOTH + NOTE_MERGE (MoAI의 Y/Δ √3 자리 규칙을 Codex balanced_three_phase에 보강 권장) |
| 3상 전력 | C(three_phase_power) | M(14) | 1:1 | KEEP_BOTH (사실상 동일) |
| 대칭 좌표법 | C(symmetrical_components) | M(15) | 1:1 | KEEP_BOTH (Codex의 zero-sequence 경로 caution이 더 정밀, MoAI의 a=exp(j120°) 분해식이 더 완전) |
| 1차 RC 과도 | C(rc_transient) | M(16) 1차 RC/RL 합본 | 1:2 split | KEEP_CODEX (RC/RL 분리가 시험 학습에 유리) |
| 1차 RL 과도 | C(rl_transient) | M(16) (위 합본) | 1:2 split | KEEP_CODEX |
| 2차 과도 | C(second_order_response) | M(17) | 1:1 | KEEP_BOTH (MoAI의 ζ=1/(2Q) 관계 + 직렬 ζ=(R/2)√(C/L) 식 추가 가치) |
| 라플라스 변환 | C(laplace_transform) | M(18) | 1:1 (Codex는 pole/zero 포함, MoAI는 초기조건 항 강조) | KEEP_BOTH |
| s-domain 회로해석 | C(s_domain_circuit_analysis) | M(18)에 포함 | 1:0.5 | KEEP_CODEX (Codex의 separate s-domain card가 학습 명료성에 유리) |
| 초기값·최종값 정리 | (Codex 없음) | M(19) | MoAI-only | NEW_CARD_CONSIDER (라플라스에 가까운 보조 정리. supervisor 결정) |
| 전달함수 H(s)·극영점 | C(laplace_transform 내부) | M(20) | 1:0.5 | NEW_CARD_CONSIDER (MoAI는 H(s) 전용 카드. Codex laplace_transform가 일부 다룸. 분리 가치 supervisor 결정) |
| 필터 분류 -3dB | (Codex bode_plot에 일부) | M(21) | 0.3:1 | NEW_CARD_CONSIDER (시험 빈출 -3dB / 1차 LPF 식이 MoAI 단독 보유) |
| 보드 선도 | C(bode_plot) | M(22) | 1:1 (둘 다 broad-scope MEDIUM) | KEEP_BOTH (Codex는 magnitude/phase 분리 강조, MoAI는 극·영점 점근선 dB/dec 명시) |
| 2-port | C(two_port_network) | M(23) | 1:1 | KEEP_BOTH (Codex는 ABCD convention 차이 명시, MoAI는 4종(Z/Y/h/ABCD) 분류) |
| 영상 임피던스 | (Codex 없음) | M(24) | MoAI-only | NEW_CARD_CONSIDER (특성 임피던스 Z_0 = √(L/C)와 영상 정합 분리가 학습 가치 있음. supervisor 결정) |
| 가역성 정리 | (Codex 없음) | M(25) | MoAI-only | NEW_CARD_CONSIDER (Z_12 = Z_21 + 종속 전원 시 무효 caveat. 시험 직접 빈출도는 낮을 수 있음) |
| 푸리에 급수 | C(fourier_series) | M(26) | 1:1 (둘 다 broad-scope) | KEEP_BOTH |
| 고조파 | C(harmonics) | M(27) 비정현파 전력/왜형 역률 | 1:1 (관점 다름: Codex=THD 정의, MoAI=비정현파 전력 분해) | KEEP_BOTH (MoAI는 PF=변위×왜형 명시, Codex는 THD 계산식 강점) |
| 라우스-후르비츠 | (Codex 없음) | M(28) | MoAI-only (broad-scope) | HUMAN_REVIEW (제어공학 영역 — 회로이론 시험 범위 여부 supervisor 결정) |
| 상태공간 | (Codex 없음) | M(29) | MoAI-only (broad-scope) | HUMAN_REVIEW (제어공학 영역) |
| z-변환 | C(z_transform) | M(30) | 1:1 (둘 다 broad-scope MEDIUM) | KEEP_BOTH |

**Coverage 통계**:

- 동일/유사 1:1 매칭: 16 family
- 1:2 split (Codex 분리 vs MoAI 합본): 3 family (nodal+mesh / phasor+impedance / rc+rl)
- 1:3 split (MoAI가 RLC를 직렬+병렬+Q로 세분): 1 family
- Codex-only (5): ohms_law, series_parallel, voltage_divider, current_divider, mutual_inductance — **회로이론 시험 본문 필수 기초**
- MoAI-only (7): 초기값·최종값 정리, 전달함수 H(s) 단독, 필터 분류 -3dB, 영상 임피던스, 가역성, 라우스-후르비츠, 상태공간

---

## 3. Quality Comparison

표 약어:

- C = Codex 카드 강점 우세
- M = MoAI 카드 강점 우세
- ≈ = 동등(취향 차이)
- — = 비교 불가(한쪽 부재)

| concept_family | stronger_static_boundary | stronger_risk_boundary | stronger_memory_logic | formula_issue | recommended_source |
|---|---|---|---|---|---|
| KVL/KCL | M (lumped circuit 가정 + 파장 비교 명시) | C (부호 약속 위반 시 부호 오류 catch) | ≈ | 없음 | KEEP_BOTH, MoAI static_boundary 보강 후보 |
| 노드 해석 | C (KCL 기반 명시 + supernode 정의) | C (전압원 두 비기준 노드 간 supernode 처리 catch) | ≈ | 없음 | KEEP_CODEX |
| 메쉬 해석 | C (평면회로 한정 + supermesh 정의) | C (비평면 회로 catch) | ≈ | 없음 | KEEP_CODEX |
| 옴의 법칙 | C (선형 저항 boundary) | C (다이오드·포화·온도) | C | 없음 | KEEP_CODEX (MoAI 부재) |
| 직병렬 | C | C (중간 노드 연결 확인 catch) | C | 없음 | KEEP_CODEX |
| 전압 분배 | C | C (loading effect catch) | C | 없음 | KEEP_CODEX |
| 전류 분배 | C | C (상대 저항 자리 catch) | C | 없음 | KEEP_CODEX |
| 전원 변환 | M (이상 전원 제외 명시) | ≈ | C ("외부 단자 I-V 관계 유지" 응축적) | 없음 | KEEP_BOTH, M의 boundary를 C에 NOTE merge 가능 |
| 중첩 | M (선형 LTI 전제 + 종속 전원 유지) | M (부분 응답 전력 단순 합산 금지 + 동시 활성 재계산 강조) | ≈ | 없음 | KEEP_BOTH, M risk 강점 |
| 테브난·노턴 | M (V_TH/I_N/R_TH 3 식 일괄) | M ("시험 전원법으로 R_TH" 종속 전원 시 절차 명시) | ≈ | C는 노턴 별도 없음 | KEEP_CODEX + M의 R_TH 절차 NOTE merge |
| 상호 인덕턴스 | C | C (dot convention 오해 + 포화 누설 catch) | C | 없음 | KEEP_CODEX (M 부재) |
| 최대 전력 전달 | ≈ | ≈ (둘 다 효율=50% 고정 명시) | ≈ | 없음 | KEEP_BOTH |
| 페이저 | C (단일 주파수 정상상태 명시 + d/dt → jω) | C (서로 다른 주파수 합산 금지 catch) | ≈ | 없음 | KEEP_CODEX |
| 임피던스 | C (R+jX 구분 명시 + 주파수 의존성) | C (한 주파수 값 고정 금지) | C | 없음 | KEEP_CODEX |
| RLC 직렬 공진 | M (omega_0 = 1/√(LC) + Z(ω_0)=R 명시) | M (Q 배 절연 파괴 caution) | M | C는 직병렬 통합 카드라 직렬 단독 식 일부 누락 | KEEP_BOTH 또는 supervisor가 분리/통합 결정 |
| RLC 병렬 공진 | M (반공진 정의) | M (인덕터 직렬 저항 인한 ω_0 이동 catch) | M | C는 별도 없음 | NEW_CARD_CONSIDER from M |
| Q/BW | M (Q = ω_0/BW, 직병렬 Q 식 분리) | M (Q 큰 값이 제어계에서 ringing 키운다 caution) | M (Q는 한 수로 압축한 첨예도) | C는 rlc_resonance 안에 Q 정의만 짧게 | NEW_CARD_CONSIDER from M (시험 빈출도 높음) |
| 교류 4전력 | C (RMS phasor 기준 명시) | ≈ | M ("한 주기 평균 남는 게 유효" 직관적) | 없음 | KEEP_BOTH |
| 역률 | C (정의 카드로서 정확) | C (true PF vs displacement PF 구분) | C | 없음 | KEEP_CODEX, M(역률 개선)은 별도 보완 카드로 |
| 3상 평형 | C (120° + neutral=0 + sequence) | C (불평형 → 평형식 적용 금지) | ≈ | C는 Y/Δ 결선식 명시 부재 | KEEP_CODEX + M의 Y/Δ √3 규칙 NOTE merge |
| 3상 전력 | ≈ | ≈ | ≈ | 없음 | KEEP_BOTH |
| 대칭 좌표법 | M (V_0, V_1, V_2 3 분해식 완전) | C (zero-sequence 경로 = 접지·중성선·변압기 결선 조건 catch) | C ("고장전류 경로의 지도") | M은 a=exp(j120°) 명시 | KEEP_BOTH (양면 보완) |
| 1차 RC | C (커패시터 전압 연속성 명시) | C (커패시터 전류는 순간 변화 가능 catch) | C | 없음 | KEEP_CODEX |
| 1차 RL | C (인덕터 전류 연속성 명시) | C (스위칭 시 코일 과전압 catch) | C | 없음 | KEEP_CODEX |
| 2차 과도 | M (직렬 ζ = (R/2)√(C/L) 명시) | C (자연/공진/감쇠 주파수 혼동 catch) | ≈ | 없음 | KEEP_BOTH (양면 보완) |
| 라플라스 | C (pole/zero/final_value word_roles 포함) | M (초기 조건 누락 시 t=0 직전 에너지 무시 catch 더 구체적) | ≈ | 없음 | KEEP_BOTH |
| s-domain 회로해석 | C (별도 카드로 초기조건 등가 전원 catch) | C (초기 조건 등가 전원 반영 절차 catch) | C | 없음 | KEEP_CODEX |
| 초기값·최종값 정리 | M (성립 조건 RHP 극 없음 명시) | M (발산·진동 시 적용 금지) | M | 없음 | NEW_CARD_CONSIDER from M |
| 전달함수 H(s) | M (분모=극, 분자=영점, 영 IC + ROC) | M (모든 극 LHP가 응답 속도 좋음 아님 catch) | M | 없음 | NEW_CARD_CONSIDER from M (또는 C laplace 카드에 NOTE merge) |
| 필터 분류 -3dB | M (1차 LPF 식 + BPF 중심 √(ω_L ω_H)) | M (1차 차단 vs 2차 공진 혼동 catch) | M | 없음 | NEW_CARD_CONSIDER from M |
| 보드 선도 | ≈ (양쪽 broad-scope 명시) | ≈ | C (한 문장 ≈ "두 장의 그래프로 보여준다") | M에 점근선 dB/dec 규칙 더 명시 | KEEP_BOTH |
| 2-port | M (Z/Y/h/ABCD 4 종 명시) | C (z, y, h, ABCD convention 섞으면 안 됨 catch) | C ("내부를 다 보지 않고 입출력 관계를 행렬 언어로") | 둘 다 convention 명시 양호 | KEEP_BOTH |
| 영상 임피던스 | M (Z_0 = √(L/C) 명시 + 영상 정합 ≠ 최대 전력 정합) | M | M | 없음 | NEW_CARD_CONSIDER from M |
| 가역성 정리 | M (Z_12 = Z_21 + 종속 전원·다이오드·자이레이터 깨짐) | M | M | 없음 | NEW_CARD_CONSIDER from M (시험 빈출도 낮을 수 있음) |
| 푸리에 급수 | ≈ (둘 다 broad-scope) | C (비주기·과도 → 푸리에 적용 금지 + corpus gap 명시) | ≈ | M에 분해 식 더 일반화 | KEEP_BOTH |
| 고조파/THD/왜형 역률 | C (THD = √(Σ V_n²)/V_1 정의) | M (PF = 변위 × 왜형 분해 식) | ≈ | M는 동일 차수만 평균 전력 기여 강점 | KEEP_BOTH (양면 보완) |
| 라우스-후르비츠 | M (라우스 어레이 1열 부호 변화) | M (1열 0 케이스 ε 치환 catch) | M | 없음 | HUMAN_REVIEW (회로이론 corpus-gap) |
| 상태공간 | M (ẋ = Ax + Bu + H(s) = C(sI-A)^-1 B + D) | M (상태변수 선택에 따라 A,B,C 달라짐 catch) | M | 없음 | HUMAN_REVIEW (회로이론 corpus-gap) |
| z-변환 | C ("라플라스가 이산시간으로 넘어감 + 안정 경계 LHP→단위원" memory 좋음) | C | C | ≈ | KEEP_CODEX (M은 ROC 명시 강점 있으나 전체적으로 C 우위) |

**Quality 종합 패턴**:

| 패턴 | 빈도 | 해석 |
|---|---:|---|
| Codex 우위 (기본 회로 카드) | 12 | ohms_law / series_parallel / voltage_divider / current_divider / mutual_inductance / nodal / mesh / phasor / impedance / rc / rl / z_transform — Codex가 시험 본문 분해를 더 정교히 함 |
| MoAI 우위 (확장/세분화 카드) | 9 | Q/BW 분리 / RLC 병렬 / 영상 임피던스 / 가역성 / 초기값·최종값 / H(s) 단독 / 필터 분류 / 라우스 / 상태공간 — MoAI가 인접 도메인 경계를 더 세부 분리 |
| 동등/상호 보완 | 13 | KVL/KCL, 전원 변환, 중첩, 테브난, 최대 전력, 복소 전력, 3상 평형, 3상 전력, 대칭 좌표법, 2차 과도, 라플라스, 보드, 2-port, 푸리에, 고조파 — 양쪽 모두 가치 있음 |

---

## 4. Merge Candidates (High-Value Patches)

표 약어:

- action 유형: ADD_NEW_FILE / NOTE_MERGE / KEEP_AS_IS / SPLIT_DECISION

**High-priority candidates**:

| # | target_file_or_new_file | action | source | reason | risk_level_after_merge | needs_supervisor_decision |
|---|---|---|---|---|---|---|
| 1 | `rlc_resonance.yaml` (Codex) — Q/BW 분리 또는 통합 | SPLIT_DECISION | MoAI M(10) Q/BW 단독 카드 | Codex는 rlc_resonance 1개로 통합, MoAI는 직렬+병렬+Q 3개로 분해. 시험 빈출도 관점에서 Q/BW 단독 카드가 학습 효율 높을 수 있음 | LOW (분리 시) / LOW (통합 유지 시) | YES |
| 2 | `thevenin_equivalent.yaml` (Codex) | NOTE_MERGE | MoAI M(5) risk 항목 | MoAI의 "종속 전원만 있는 경우 시험 전원법으로 R_TH 산출" 절차가 Codex에는 risk note 수준으로만 있음. 절차를 risk 또는 word_roles에 명시 권장 | MEDIUM 유지 | YES |
| 3 | `balanced_three_phase.yaml` (Codex) | NOTE_MERGE | MoAI M(13) formula_core | MoAI의 "Y: V_L=√3 V_p, I_L=I_p / Δ: V_L=V_p, I_L=√3 I_p" 결선식이 Codex balanced_three_phase에는 없음. formula_core 보강 또는 새 카드 후보 | LOW 유지 | YES |
| 4 | 신규 파일 `rlc_parallel_resonance.yaml` 또는 `q_factor_bandwidth.yaml` | ADD_NEW_FILE 후보 | MoAI M(9) + M(10) | 시험 빈출 분리 카드. supervisor가 Codex rlc_resonance 통합 유지를 결정하면 폐기 | LOW | YES |
| 5 | 신규 파일 `voltage_phasor_impedance.yaml` (분리 vs 합본) | KEEP_AS_IS | — | Codex의 phasor + impedance 분리가 학습 명료성에 더 유리. MoAI 합본은 채택하지 않음 | — | NO (Codex 분리 유지 권고) |

**Medium-priority candidates**:

| # | target_file_or_new_file | action | source | reason | risk_level_after_merge | needs_supervisor_decision |
|---|---|---|---|---|---|---|
| 6 | `power_factor.yaml` (Codex) — 역률 개선 절차 보강 | NOTE_MERGE 또는 ADD_NEW_FILE | MoAI M(12) 역률 개선 | Codex power_factor는 정의 위주, MoAI는 "콘덴서 보상 + 과보상 진상 + 고조파 시 직렬 리액터 필요" 절차 강점. 보강 또는 별도 카드 후보 | LOW / MEDIUM | YES |
| 7 | `complex_power.yaml` (Codex) | NOTE_MERGE | MoAI M(11) word_roles | MoAI의 "한 주기 평균으로 남는 게 유효, 사라지는 게 무효" memory_logic이 시험 학습에 직관적. memory_logic 보강 후보 | LOW 유지 | YES |
| 8 | `superposition_theorem.yaml` (Codex) | NOTE_MERGE | MoAI M(4) risk | MoAI의 "전력은 비선형(제곱항)이라 부분 전력 합산 금지" risk가 Codex보다 한 단계 구체적 | LOW 유지 | NO (작은 보강이라 자동 적용도 무방) |
| 9 | `second_order_response.yaml` (Codex) | NOTE_MERGE | MoAI M(17) formula_core | MoAI의 "직렬 ζ = (R/2)·√(C/L)" 식을 Codex card formula_core에 추가 권장 (현재 Codex는 ζ = α/ω0만 명시) | MEDIUM 유지 | YES |
| 10 | `symmetrical_components.yaml` (Codex) | NOTE_MERGE | MoAI M(15) formula_core | MoAI의 V_0, V_1, V_2 3 분해식이 Codex에는 I_0 하나만 있음. 완전 분해식 추가 권장 | MEDIUM 유지 | YES |
| 11 | `laplace_transform.yaml` (Codex) | NOTE_MERGE | MoAI M(18) risk | MoAI의 "초기 조건 항 누락 시 t=0 직전 에너지 무시" risk가 Codex보다 구체적. Codex의 "pole/zero 비유로만 외우면 안 됨"과 양립 | LOW 유지 | NO (small 보강) |

**Defer / supervisor-only candidates**:

| # | target_file_or_new_file | action | source | reason | needs_supervisor_decision |
|---|---|---|---|---|---|
| 12 | 신규 파일 `final_value_theorem.yaml` | ADD_NEW_FILE | MoAI M(19) 초기값·최종값 정리 | 라플라스 보조 정리. supervisor 결정 후 추가 가능 | YES |
| 13 | 신규 파일 `transfer_function.yaml` | ADD_NEW_FILE | MoAI M(20) H(s)·극영점 | Codex는 laplace에 일부 포함. 분리 카드 가치 supervisor 결정 | YES |
| 14 | 신규 파일 `lowpass_highpass_bandpass_classification.yaml` 또는 `cutoff_frequency_-3dB.yaml` | ADD_NEW_FILE | MoAI M(21) 필터 분류 | 시험 빈출 -3dB 카드. supervisor 결정 | YES |
| 15 | 신규 파일 `image_impedance.yaml` | ADD_NEW_FILE | MoAI M(24) 영상 임피던스 | 특성 임피던스 Z_0 = √(L/C) + 영상 정합 ≠ 최대 정합 catch. supervisor 결정 | YES |
| 16 | 신규 파일 `reciprocity.yaml` | ADD_NEW_FILE | MoAI M(25) 가역성 | Z_12 = Z_21 + 종속 전원 시 깨짐. 시험 빈출도 supervisor 검증 | YES |
| 17 | 신규 파일 `routh_hurwitz.yaml` (broad-scope) | ADD_NEW_FILE 또는 DROP_OR_DEFER | MoAI M(28) | 제어공학 영역 — 회로이론 시험 범위 supervisor 결정 | YES |
| 18 | 신규 파일 `state_space.yaml` (broad-scope) | ADD_NEW_FILE 또는 DROP_OR_DEFER | MoAI M(29) | 제어공학 영역 — 회로이론 시험 범위 supervisor 결정 | YES |

**High-priority summary** (5 항목): supervisor가 우선 결정해야 할 점.

**Medium-priority summary** (6 항목): 자동 적용 가능한 작은 NOTE_MERGE 위주.

**Defer summary** (7 항목): 신규 카드 추가 / supervisor 결정 필요.

---

## 5. Human Review Required

### 5-1. Corpus gap (회로이론 corpus 안에 본문이 부족할 가능성)

| concept | 출처 | gap 사유 |
|---|---|---|
| z-변환 | C(z_transform) + M(30) | 디지털 신호 처리·디지털 제어 본문 — 회로이론 PRIMARY corpus 안에 본격 본문 부재 |
| 라우스-후르비츠 | M(28) only | 제어공학 본문 — 회로이론 PRIMARY corpus 부재 |
| 상태공간 | M(29) only | 제어공학 본문 — 회로이론 PRIMARY corpus 부재 |
| 푸리에 급수 | C(fourier_series) + M(26) | 신호해석 broad-scope — Codex review 이미 명시 |
| 보드 선도 | C(bode_plot) + M(22) | 제어공학 broad-scope — Codex review 이미 명시 |
| 비정현파 전력 / 왜형 역률 | M(27) | Codex harmonics는 THD 위주, MoAI 비정현파 전력 분해는 추가 검토 영역 |

### 5-2. Broad-scope boundary (회로이론 core vs 인접 도메인 경계)

| concept | broad-scope 방향 | 검토 사항 |
|---|---|---|
| 최대 전력 전달 | 전력 계통 vs 통신·신호 | "전력 계통 운용은 효율 우선" 양쪽 카드 모두 명시. 학습자 혼동 방지 위해 양쪽 다 유지 |
| 테브난·노턴 | 주파수 의존성 | Codex MEDIUM extension_risk 유지 권고 |
| 2차 과도 | 제어계 2차 근사 | Codex가 "고차 시스템의 지배 극점 근사일 때만" 명시 — 양호 |
| 보드 선도 | 제어계 위상여유·게인여유 | 회로이론 시험 범위 봐 양쪽 카드 모두 broad-scope MEDIUM 유지 |
| z-변환 | 디지털 제어·DSP | 양쪽 카드 모두 broad-scope MEDIUM 유지 + corpus-gap 명시 |
| 라우스 / 상태공간 | 제어공학 본문 | 회로이론 시험에 출제되는지 supervisor 확인 필요 |

### 5-3. Formula convention 차이 가능성

| concept | convention 이슈 |
|---|---|
| 복소 전력 | "S = V·I*" vs "S = V*·I" — 일부 교재 정의 차이. Codex review summary에 이미 RMS phasor 명시 권고 있음 |
| 2-port ABCD | I_2 부호 방향(들어가는 양 vs 나가는 양) — 양쪽 카드 모두 convention 명시 양호 |
| 대칭 좌표법 | a = 1∠120° (Codex) vs a = exp(j*120°) (MoAI) — 같은 의미, 표기만 다름 |
| 상호 인덕턴스 | dot convention — Codex 단독 카드, MoAI 부재. Codex 카드 risk 강점 |
| s-domain 회로해석 | 초기 조건을 전압원 등가로 vs 부가항으로 — 양쪽 카드 모두 명시 양호 |

### 5-4. Cross-domain transfer overclaim 위험

| concept | 위험 패턴 | 양쪽 카드 caution 상태 |
|---|---|---|
| Q/BW | "Q는 항상 좋다"는 일반화 | M(10) caution 양호, C(rlc_resonance) caution도 양호 |
| 최대 전력 전달 | "모든 시스템에 R_L = R_TH 적용" | 양쪽 모두 효율 우선 caveat 명시 |
| 라플라스·s-domain | 비선형·시변 시스템에 LTI 도구 적용 | 양쪽 모두 caveat 명시 |
| 보드 선도 | 비선형·시변 시스템에 점근선 적용 | 양쪽 모두 caveat 명시 |
| 상태공간 | "모든 시스템에 상태공간으로 풀이" 일반화 | M(29) caveat 양호, supervisor 검토 권고 |

---

## 6. Forbidden Claims

이 비교 보고서는 **다음 주장은 하지 않는다**:

1. ❌ "MoAI draft가 Codex draft를 대체할 만큼 완성되었다."
2. ❌ "Codex draft가 회로이론 학습 자료로 최종 승인되었다."
3. ❌ "두 set 중 어느 한쪽이 gold set이다."
4. ❌ "corpus-wide grounding이 검증되었다."
5. ❌ "semantic gain이 정량적으로 측정되었다."
6. ❌ "이 비교가 supervisor의 최종 결정이다."
7. ❌ "Codex의 ACCEPT_WITH_NOTES 11 카드가 자동으로 production-ready다."
8. ❌ "MoAI-only 카드 7개가 자동으로 신규 추가되어야 한다."
9. ❌ "broad-scope 카드가 회로이론 core 카드로 승격되어야 한다."
10. ❌ "본 비교가 Codex pilot30 또는 v0.1 accepted artifact의 status를 변경한다."

**유지되는 claim boundary**:

- 본 비교는 **MoAI 보조 의견**이며, supervisor (Codex) + user 최종 결정이 우선한다.
- 본 비교는 **양쪽 set의 구조·내용 비교**에 한정한다.
- 본 비교는 **양쪽 set 어느 파일도 수정하지 않았다**(mutation 0).
- 본 비교 산출물 자체도 **검토용 draft**이며 정식 학습 자료가 아니다.

---

## 7. Summary of Supervisor Decision Points

다음 항목은 supervisor (Codex + user) 결정이 필요한 핵심 포인트:

### Tier A — High impact, 결정 시급

1. **Codex `rlc_resonance.yaml`을 1 카드로 유지할지, MoAI 식 3 카드(직렬+병렬+Q/BW)로 분리할지**
2. **MoAI-only 신규 후보 3종 채택 여부**: image_impedance, q_factor_bandwidth, cutoff_frequency_-3dB

### Tier B — Medium impact, 보강 NOTE_MERGE

3. **`thevenin_equivalent.yaml`에 MoAI의 "시험 전원법 R_TH 절차" NOTE 추가 여부**
4. **`balanced_three_phase.yaml`에 MoAI의 Y/Δ √3 결선식 NOTE 추가 여부**
5. **`second_order_response.yaml`에 MoAI의 직렬 ζ 식 NOTE 추가 여부**
6. **`symmetrical_components.yaml`에 MoAI의 V_0/V_1/V_2 3 분해식 NOTE 추가 여부**
7. **`power_factor.yaml`을 정의 카드로 유지하고 별도 `power_factor_correction.yaml` 신규 카드 추가 여부** (MoAI M(12))

### Tier C — Defer, 추가 corpus 검증 필요

8. **`reciprocity.yaml` 신규 추가 여부** (시험 빈출도 검증 필요)
9. **`final_value_theorem.yaml` 신규 추가 여부**
10. **`transfer_function.yaml` 신규 추가 (laplace에서 분리)** vs Codex laplace_transform 카드 안에 NOTE merge

### Tier D — Broad-scope, 회로이론 시험 범위 확인 필요

11. **`routh_hurwitz.yaml` 신규 추가 여부** (MoAI M(28), 제어공학 영역)
12. **`state_space.yaml` 신규 추가 여부** (MoAI M(29), 제어공학 영역)

---

## 8. Recommended Next Steps (MoAI 의견)

1. supervisor (Codex) 가 Tier A 2 항목부터 결정.
2. Tier B 5 항목은 supervisor 인가 후 Codex 카드에 NOTE_MERGE 적용 (Codex 측 mutation 권한 필요, MoAI는 patch 제안만 가능).
3. Tier C·D 5 항목은 회로이론 시험 corpus 추가 grounding 검증 후 결정.
4. 본 비교 보고서를 Codex 측에 sharing 후 supervisor 의견 수렴.
5. 후속 단계: supervisor 결정 → Codex 측 patch 적용 → MoAI 측 unused 카드 폐기 또는 deferred backlog 이관.

---

## 9. Mutation & Grounding Audit

```yaml
mutation_counters:
  codex_yaml_mutation_count: 0
  codex_md_mutation_count: 0
  moai_yaml_mutation_count: 0
  moai_md_mutation_count: 0
  prior_artifact_mutation_count: 0
  source_data_mutation_count: 0
  answer_key_mutation_count: 0
  corpus_mutation_count: 0
forbidden_grounding_checks:
  answer_key_used_as_grounding: false
  generated_solution_used_as_grounding: false
  generated_explanation_used_as_grounding: false
  generated_rationale_used_as_grounding: false
  evidence_card_summary_treated_as_proof: false
  forbidden_source_used: false
```

---

CODEX_VS_MOAI_COMPARISON_V0.1_READY_FOR_SUPERVISOR_REVIEW
