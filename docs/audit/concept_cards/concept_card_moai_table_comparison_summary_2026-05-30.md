# Concept Card MOAI Table Comparison Summary

작성일: 2026-05-30 KST
비교 대상:

- Codex reviewed draft: 30 YAML cards
- MOAI independent draft: YAML body + review table available in `moai_artifacts/`

## 0. Supervisor Update Reflected

감독자/MOAI 후속 결과를 반영했다.

MOAI artifact status:

- YAML body saved and copied to `moai_artifacts/`
- Codex-side parse verified: 30 entries
- required 9 fields complete: 30/30
- extension_risk subkeys complete: 30/30
- corrected risk distribution: LOW 18 / MEDIUM 12 / HIGH 0
- corrected human-review count: 12

## 1. Top-line Verdict

MOAI 결과는 **참조 가치 있음**이다.

이제 MOAI YAML body의 구조 검증까지는 확인되었다. 다만 corpus grounding과 semantic gain은 여전히 미검증이므로, MOAI draft를 바로 merge하거나 최종 학습자료로 승격할 수는 없다. 이번 단계에서의 가장 큰 가치는 **Codex set의 coverage gap과 risk-level 재검토 후보를 드러낸 것**이다.

## 2. Distribution Comparison

| metric | Codex reviewed draft | MOAI table | interpretation |
|---|---:|---:|---|
| total cards | 30 | 30 | 동일 |
| LOW | not normalized as risk distribution | 18 | MOAI는 risk distribution을 명시적으로 산출 |
| MEDIUM | not normalized as risk distribution | 12 | MOAI는 human review 대상을 MEDIUM과 동일 집합으로 둠 |
| HIGH | 0 observed | 0 | 양쪽 모두 HIGH는 없음 |
| human/review notes | 11 ACCEPT_WITH_NOTES | 12 needs_human_review | MOAI가 1개 더 보수적 |
| corpus gap / broad-scope | Codex: broad-scope 주요 3~4개 | MOAI: yes/partial 6, broad-scope 4 | MOAI가 경계 과목을 더 넓게 포착 |

주의: Codex의 `ACCEPT_WITH_NOTES`는 review verdict이고, MOAI의 `needs_human_review`는 자체 risk flag다. 두 숫자를 동일 의미로 해석하면 안 된다.

## 3. Concept Coverage Comparison

### 3.1 Strong overlap

MOAI와 Codex가 거의 같은 개념군을 다루는 영역:

| concept family | Codex card(s) | MOAI concept(s) | action |
|---|---|---|---|
| KCL/KVL | `kirchhoff_laws.yaml` | KVL/KCL | keep Codex, MOAI risk note already covered |
| node/mesh | `nodal_analysis.yaml`, `mesh_analysis.yaml` | 노드/메쉬 해석 | keep Codex separate cards |
| source transform | `source_transformation.yaml` | 전원 등가 변환 | keep |
| superposition | `superposition_theorem.yaml` | 중첩의 원리 | keep |
| Thevenin/Norton | `thevenin_equivalent.yaml` | 테브난·노턴 | keep, Norton mention may be added later |
| maximum power | `maximum_power_transfer.yaml` | 최대 전력 전달 | keep MEDIUM |
| phasor/impedance | `phasor.yaml`, `impedance.yaml` | 페이저·복소 임피던스 | keep Codex split |
| RLC resonance/Q/BW | `rlc_resonance.yaml`, `second_order_response.yaml` | RLC 직렬/병렬 공진, Q·BW | Codex may need split expansion later |
| AC power/PF | `complex_power.yaml`, `power_factor.yaml` | 교류 4전력, 역률 개선, 비정현파 전력 | Codex may need extra cards |
| 3-phase | `balanced_three_phase.yaml`, `three_phase_power.yaml` | 3상 평형 Y/Δ, 3상 평형 전력 | Codex may need Y/Delta detail card |
| symmetrical components | `symmetrical_components.yaml` | 대칭 좌표법 | keep MEDIUM review candidate |
| transients | `rc_transient.yaml`, `rl_transient.yaml`, `second_order_response.yaml` | 1차/2차 과도응답 | keep |
| Laplace/s-domain | `laplace_transform.yaml`, `s_domain_circuit_analysis.yaml` | 라플라스 변환, 전달함수 H(s), 초기값·최종값 정리 | Codex may need extra cards |
| Bode/filter | `bode_plot.yaml`, `rlc_resonance.yaml` | 필터 분류·차단주파수, 보드 선도 | Codex may need filter-specific card |
| two-port | `two_port_network.yaml` | 2-port, 영상 임피던스 | Codex may need image impedance card |
| Fourier/harmonics | `fourier_series.yaml`, `harmonics.yaml` | 푸리에 급수/고조파 | keep |
| z-transform | `z_transform.yaml` | z-변환 | keep MEDIUM corpus-gap |

### 3.2 MOAI concepts not directly covered by Codex as standalone cards

| MOAI concept | status in Codex set | recommendation |
|---|---|---|
| RLC 병렬 공진 | folded into `rlc_resonance.yaml` | candidate new card or subcard |
| Q·BW | folded into `rlc_resonance.yaml` | candidate standalone card |
| 역률 개선 | partially in `power_factor.yaml` | candidate new card |
| 3상 평형 Y/Δ | partially in 3-phase cards | candidate new card |
| 초기값·최종값 정리 | partially in `laplace_transform.yaml` | candidate new card |
| 전달함수 H(s) | partially in `laplace_transform.yaml` / `s_domain_circuit_analysis.yaml` | candidate new card |
| 필터 분류·차단주파수 | only implicit | candidate new card |
| 영상 임피던스 | absent | candidate new card, human review |
| 가역성 정리 | absent | candidate new card, check corpus priority |
| 비정현파 전력·왜형 역률 | partially in PF/harmonics | candidate new card |
| 라우스-후르비츠 | absent, control boundary | candidate broad-scope card only |
| 상태공간 | absent, control boundary | candidate broad-scope card only |

## 4. Risk Signal Comparison

MOAI가 유용하게 잡은 risk signals:

| MOAI signal | Codex status | action |
|---|---|---|
| 분포정수·고주파 전송선에서 KVL/KCL 무리 적용 | Codex `kirchhoff_laws` caution에 already covered | no change |
| 최대전력전달을 전력계통 운용 기준으로 적용 위험 | Codex patched | no change |
| Q/BW의 광대역·다중공진·2차계 확장 위험 | Codex has Q risk, but standalone split useful | candidate split |
| 역률 개선에서 고조파 환경 콘덴서 단독 사용 위험 | Codex PF has non-sinusoidal caution, but compensation detail absent | candidate card, but MOAI risk level LOW |
| 대칭좌표법이 전력공학 경계라는 corpus gap | Codex currently LOW; MOAI MEDIUM yes | re-evaluate Codex risk level |
| 초기값·최종값 정리 성립 조건 | Codex has Laplace but no standalone theorem card | candidate card |
| 보드 선도 제어공학 경계 | Codex patched broad-scope MEDIUM | aligned |
| 영상 임피던스와 최대전력 정합 혼동 | Codex absent | candidate card |
| 라우스/상태공간 제어공학 경계 | Codex absent | broad-scope candidates only |
| z-transform 안정 영역 LHP vs unit circle | Codex caution aligned | no change |

## 5. Recommended Actions

### Action A: Do not replace Codex set

MOAI table만으로 Codex reviewed draft를 교체하지 않는다.

### Action B: Add candidate expansion list

MOAI가 드러낸 standalone 후보를 별도 backlog로 만든다.

High-value candidate cards:

1. `q_bandwidth.yaml`
2. `parallel_rlc_resonance.yaml`
3. `power_factor_correction.yaml`
4. `initial_final_value_theorems.yaml`
5. `transfer_function.yaml`
6. `filter_cutoff_frequency.yaml`
7. `distortion_power_factor.yaml`

Human-review / broad-scope candidate cards:

1. `image_impedance.yaml`
2. `reciprocity_theorem.yaml`
3. `routh_hurwitz.yaml`
4. `state_space.yaml`

### Action C: Re-evaluate one Codex card risk level

`symmetrical_components.yaml` currently has `extension_risk.level: LOW`, while MOAI marks 대칭 좌표법 as MEDIUM with power-engineering boundary.

Recommendation:

- Change Codex `symmetrical_components.yaml` from LOW to MEDIUM, or
- Keep LOW only if the project treats power-system fault analysis as expected extension rather than corpus gap.

Status: reflected. Codex `symmetrical_components.yaml` was updated to MEDIUM because the card itself bridges 회로이론 and 전력계통 고장해석.

## 6. Next Gate

Recommended next gate:

**MOAI-informed patch gate**

Scope:

- Preserve MOAI artifacts under `moai_artifacts/`.
- Update `symmetrical_components.yaml` risk level to MEDIUM. 완료.
- Create `concept_card_expansion_backlog_2026-05-30.md`. 완료.
- Do not create the 11 new cards yet.
- Do not claim corpus grounding completion.

## 7. Claim Boundary

말할 수 있는 것:

- MOAI table-level comparison found useful expansion and risk-review signals.
- Codex set should not be replaced by MOAI table.
- At least one Codex risk level should be reconsidered: `symmetrical_components.yaml`.
- MOAI suggests a useful expansion backlog.

아직 말하면 안 되는 것:

- MOAI card bodies are better than Codex bodies.
- MOAI YAML structure was verified.
- New expansion cards are approved.
- Codex set is gold.
