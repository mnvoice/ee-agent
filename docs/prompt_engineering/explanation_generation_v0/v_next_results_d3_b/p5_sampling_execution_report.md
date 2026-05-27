# P5 Sampling Execution Report (12-sample semantic signal)

> 2026-05-27 KST. Post-D-3 breaker B-only patch commit (`00dfdf0`) 후속.
> 본 보고서는 **12 sample 기준 semantic signal 측정**. D-3 전체 / 94 / 242 improved claim 0.

---

## 0. 핵심 한 줄 결론

**`P5_SIGNAL_B_BETTER`**.

- 차단기 5건: 3 B_better / 1 same / 1 needs_human_review (본문 부재) — **majority B_better**
- 비차단기 4건: all `same` (baseline ↔ B sha256 identical) — hidden regression 0
- non_expansion 3건: all `same` (patch 무관 영역) — metadata-only 절대 품질은 본 측정 외 영역

→ B-only patch의 cross_subject_expansion이 차단기 학습 본질에서 의미 있는 link 제공. patch 유지 신호 positive.

---

## 1. 측정 전략

| 그룹 | 측정 방식 | 표본 수 |
|---|---|---:|
| A. breaker_recovered | baseline + B output side-by-side read + 6-axis rubric | 5 |
| B. non_breaker_expansion | sha256 identity check (baseline vs B) — file 변경 0 ↔ auto `same` | 4 |
| C. non_expansion_metadata | sha256 identity check — file 변경 0 ↔ auto `same` | 3 |

근거: 이전 게이트 audit JSON에서 비차단기 81 + non_expansion 37의 의미 필드 회귀 0 기록됨. 사람 spot check는 file identity 검증으로 자동 보강.

---

## 2. Sample별 baseline / B 핵심 차이 + 6-axis 점수 + Label

### Group A: 차단기 5건

차단기 5건 공통 baseline ↔ B 차이 (mechanical 동일):
1. `phenomenon`: `회로 단락전류 / 임피던스 환산` → `회로 단락전류 / 회로 임피던스 환산` (`회로` 1단어 추가)
2. `cross_subject_expansion.expands_to`: `[]` → `[회로이론 1건 via "전력 차단기 → 회로이론: 회로 단락전류 / 회로 임피던스 환산 경로"]`
3. 다른 모든 필드 동일

#### Sample A-1: input_003.md (1998_4회_22) — 유전 차단기 특성

| Axis | baseline | B | 평가 |
|---|---|---|---|
| comprehension_ease | 3 | 3.5 | phenomenon에 `회로` 명시로 회로 단락전류 ↔ 회로 임피던스 분리 표기 |
| cross_subject_link_value | N/A | 4 | 차단기 특성 학습 시 회로 임피던스 환산 영역과 다리 유용 |
| forced_link_risk | N/A | 2 | link valid, mechanical wording 약 |
| distractor_specificity | 3 | 3 | trap_type 동일 (차단 용량 vs 차단 시간 혼동 함정) |
| phenomenon_trap_utility | 3 | 3 | phenomenon 약간 명확, 나머지 동일 |
| metadata_overload_risk | 1 | 1.5 | expansion 1건 추가, overload 없음 |

**Label: B_better**

#### Sample A-2: input_012.md (2000_2회_23) — 차단기 종류 (MBB/ABB/VCB/ACB) 정격 전압 비교

| Axis | baseline | B | 평가 |
|---|---|---|---|
| comprehension_ease | 3 | 3.5 | 차단기 종류 비교 시 회로 임피던스 영역 link 도움 |
| cross_subject_link_value | N/A | 4 | 차단기 정격 / 차단 용량은 회로 단락전류 / 임피던스 환산 사용 영역 — link 유용 |
| forced_link_risk | N/A | 2 | link 자연 |
| distractor_specificity | 3 | 3 | 동일 |
| phenomenon_trap_utility | 3 | 3 | 동일 |
| metadata_overload_risk | 1 | 1.5 | 낮음 |

**Label: B_better**

#### Sample A-3: input_047.md (2004_1회_90) — **본문 데이터 부재**

baseline + B 둘 다 `device_or_concept` = "문제 데이터 부재: 2008년도 3회 문제 82의 구체적인 문제 내용, 보기, 풀이가 제공되지 않아 분석이 불가능합니다." 동일. 즉 원본 questions.json에서 본 sample은 raw solution이 비어 있는 상태.

| Axis | baseline | B | 평가 |
|---|---|---|---|
| comprehension_ease | N/A | N/A | 본문 부재로 평가 곤란 |
| cross_subject_link_value | N/A | N/A | link 자체는 정합, 본문 없음 |
| forced_link_risk | N/A | N/A | 본문 없어 link 적절성 평가 불가 |
| distractor_specificity | 2 | 2 | distractor 본문도 일부 깨짐 (OCR 영역 추정) |
| phenomenon_trap_utility | N/A | N/A | 본문 부재 |
| metadata_overload_risk | 1 | 1.5 | 낮음 |

**Label: needs_human_review** (본문 부재로 정상 평가 불가 — 본 sample은 questions.json data debt 영역)

#### Sample A-4: input_056.md (2004_3회_27) — 콘덴서용 차단기 정격 전류 (150%)

| Axis | baseline | B | 평가 |
|---|---|---|---|
| comprehension_ease | 3 | 4 | 콘덴서 차단기 정격 (120% vs 150%) — 회로 임피던스 환산 link 잘 맞음 |
| cross_subject_link_value | N/A | 4 | 콘덴서 회로 단락전류 / 임피던스 환산 영역과 link 직접 관련 |
| forced_link_risk | N/A | 2 | link 자연 |
| distractor_specificity | 3 | 3 | 동일 (수치/단위 차이 함정) |
| phenomenon_trap_utility | 3 | 3 | 동일 |
| metadata_overload_risk | 1 | 1.5 | 낮음 |

**Label: B_better**

#### Sample A-5: input_092.md (2008_1회_23) — 차단기 부품 명칭 (A/B/C/D)

본문 device_or_concept = "A:가동 접촉자 / B:고정 접촉자 / C:승강간 / D:절연 liner" — 부품 명칭 영역.

| Axis | baseline | B | 평가 |
|---|---|---|---|
| comprehension_ease | 3 | 3 | 부품 명칭 영역은 회로 단락전류 / 임피던스 환산과 직접 거리 |
| cross_subject_link_value | N/A | 3 | link 자체 정합하나 본 문제 (부품 명칭)에는 덜 적절 |
| forced_link_risk | N/A | 3 | 부품 명칭과 회로 임피던스 환산 연결 약간 forced |
| distractor_specificity | 3 | 3 | 동일 |
| phenomenon_trap_utility | 3 | 3 | 동일 |
| metadata_overload_risk | 1 | 1.5 | 낮음 |

**Label: same**

---

### Group B: 비차단기 expansion 4건 (sha256 identity check)

| Sample | pid | baseline sha256 | B sha256 | 동일성 | Label |
|---|---|---|---|---|---|
| input_001.md | 1998_2회_23 | `f22103428239` | `f22103428239` | identical ✓ | `same` |
| input_007.md | 1999_3회_23 | `256004e7a5bc` | `256004e7a5bc` | identical ✓ | `same` |
| input_018.md | 2000_6회_27 | `c6a4905d16e7` | `c6a4905d16e7` | identical ✓ | `same` |
| input_015.md | 2000_4회_23 | `9807ee107ea1` | `9807ee107ea1` | identical ✓ | `same` |

→ 4 sample 전부 baseline = B (byte-level). hidden regression signal 0.

---

### Group C: non_expansion_metadata 3건 (sha256 identity check)

| Sample | pid | baseline sha256 | B sha256 | 동일성 | Label |
|---|---|---|---|---|---|
| input_005.md | 1998_4회_25 | `dcfe6970f0ca` | `dcfe6970f0ca` | identical ✓ | `same` |
| input_008.md | 1999_4회_81 | `276f4f122bf9` | `276f4f122bf9` | identical ✓ | `same` |
| input_045.md | 2004_1회_30 | `56d25db94f2d` | `56d25db94f2d` | identical ✓ | `same` |

→ 3 sample 전부 baseline = B. patch 무관 영역.

**중요한 분리**: B = baseline이므로 본 측정은 metadata-only **절대 품질** 평가가 아님. dl=None 영역의 enriched metadata 단독 충분성은 본 P5 외 별 audit 영역.

---

## 3. Group별 majority 집계

| 그룹 | 모집단 | 표본 | B_better | same | B_worse | needs_human_review | majority |
|---|---:|---:|---:|---:|---:|---:|---|
| A. breaker | 13 | 5 | **3** | 1 | 0 | 1 | **B_better** |
| B. non_breaker_exp | 44 | 4 | 0 | **4** | 0 | 0 | **same** |
| C. non_expansion | 37 | 3 | 0 | **3** | 0 | 0 | **same** |

---

## 4. 차단기 5건에서 회로이론 link가 실제로 도움이 됐는가

| 영역 | 평가 | 사례 |
|---|---|---|
| 유용 | 차단기 학습 본질 (정격 / 차단 용량 / 콘덴서 회로) 영역 | 003 (유전 차단기 특성) / 012 (정격 전압 비교) / 056 (콘덴서 정격) |
| 덜 적절 | 부품 명칭 / 본문 부재 영역 | 092 (부품 명칭) / 047 (본문 부재) |

**요약**: cross_subject_expansion link는 차단기 학습 본질 영역에서는 의미 있는 다리. 부품/구조 영역에서는 약 forced. 단 차단기 13건 전체에서 학습 본질 영역 비율이 더 높을 것으로 보임 (5건 sample 기준 3:2 = 학습 본질:부품/부재).

---

## 5. 비차단기 4건에서 hidden regression signal

| 측정 | 결과 |
|---|---|
| baseline ↔ B sha256 identical | 4/4 ✓ |
| 의미 필드 변경 | 0 (file-level 변경 0) |
| Hidden regression found | **NO** |

→ 81 회귀 0 (이전 mechanical audit) ↔ 4 sample file identity ↔ label `same` — 3중 정합.

---

## 6. non_expansion 3건에서 metadata-only 품질 충분성

| 측정 | 결과 |
|---|---|
| baseline ↔ B sha256 identical | 3/3 ✓ |
| patch 효과 변경 | 0 (B = baseline) |
| metadata-only 절대 품질 measurable | **NO** (본 비교 영역 외) |

**중요**: 본 P5는 baseline vs B 비교. non_expansion 그룹은 둘 다 dl=None 정직 영역으로 B 패치와 무관. metadata-only 절대 품질 평가는 별 audit 영역.

---

## 7. 6 pathway 매핑

| 조건 | 매칭 | 다음 상태 | 결정 |
|---|---|---|---|
| 차단기 majority B_better | ✓ | `patch_semantic_value_supported` | B-only patch semantic value 지지. A1c 추가 불필요 유지. |
| 비차단기 spot check 이상 없음 | ✓ | `regression_human_clean` | 81 회귀 0 사람 기준 정합. 추가 조치 0. |
| non_expansion 표본 품질 향상 약 | not_measurable | `deferred` | 본 비교로는 metadata-only 절대 품질 평가 불가 — 별 audit 후보. |
| 차단기 majority same | 미해당 | - | - |
| 차단기 majority B_worse | 미해당 | - | - |
| 비차단기 spot check B_worse | 미해당 | - | - |

---

## 8. 다음 게이트 추천 (우선순위)

| # | 후보 | scope |
|---:|---|---|
| 1 | P5 결과 정착 | 본 보고서 commit + push 별 사용자 명시 영역 |
| 2 | A1c keyword design 보류 유지 | 차단기 majority B_better이므로 추가 patch 불필요 — deferred 유지 |
| 3 | metadata-only audit | non_expansion_metadata 37 절대 품질 별 sampling — 본 P5와 분리 |
| 4 | D-4 진입 | unpaired 148 baseline audit — 별 독립 영역 |
| 5 | needs_human_review 1건 (input_047) 후속 | 본문 부재 sample — questions.json data debt audit 후보 |

### 본 채널 권장 (§1.4 책임 — 단일 선택)

**1순위 = P5 결과 정착 (commit + push) 사용자 명시 영역**. 본 결과를 기록으로 보존한 후 다음 영역 (2-5) 결정.

---

## 9. Claim Boundary 점검

| claim | 본 P5 상태 |
|---|---|
| 차단기 majority B_better (3/5) | (a) 측정 — 12 sample 한정 |
| 비차단기 4 sample identical → `same` × 4 | (a) sha256 측정 |
| non_expansion 3 sample identical → `same` × 3 | (a) sha256 측정 |
| hidden regression 4 sample 영역 0 | (a) 측정 |
| metadata-only 절대 품질 평가 | **0** (본 비교 영역 외) |
| **D-3 전체 semantic gain claim** | **0** |
| **94 전체 개선 claim** | **0** |
| **242 improved claim** | **0** |
| A1c 추가 결정 | **0** (deferred 유지) |
| Patch 유지 재검토 결정 | **0** (B_better 신호로 유지 default) |
| input_047 본문 부재 처리 결정 | **0** (별 data debt audit 영역) |

---

## 10. 보호 영역 매트릭스 (전부 미수정 / 0)

`scripts/explanation_synthesizer.py` ✓ / `scripts/v_next_d3_pre_preview.py` ✓ / `scripts/v_next_d3_selector.py` ✓ / `scripts/v_next_d3_input_creator.py` ✓ / `scripts/v_next_d3_parser_validator.py` ✓ / `scripts/v2_input_parser.py` ✓ / `app/data/questions.json` ✓ / D-2 sealed assets ✓ / v_full handoff scope ✓ / A1c keyword 추가 0 ✓ / D-3 재생성 0 ✓ / audit 재실행 0 ✓ / D-4 0 ✓ / catalog/gap/reuse 0 ✓ / commit 0 ✓ / DEVLOG / Vault / MEMORY / decision JSONL 작성 0 ✓.

---

## 11. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_b/p5_sampling_execution_report.md` | 본 보고서 (11 섹션) |
| `v_next_results_d3_b/p5_sampling_execution_report.json` | machine-readable — sample 12 / rubric / label / majority / pathway 매핑 / 다음 게이트 추천 |

---

## 12. 최종 상태 판정

**판정**: `P5_SIGNAL_B_BETTER`

### 판정 근거

| 검증 기준 | 결과 |
|---|---|
| Group A 차단기 majority B_better (3/5) | ✓ |
| Group B 비차단기 ALL `same` (sha256 identical 4/4) | ✓ |
| Group C non_expansion ALL `same` (sha256 identical 3/3) | ✓ |
| Hidden regression signal | 0 |
| Forced link risk (5건 평균 ≤ 2.5) | low |
| Metadata overload risk (5건 평균 1.5) | low |

### 대안 옵션 (미해당)

- `P5_SIGNAL_SAME_OR_WEAK`: 미해당 — Group A majority same 아님
- `P5_SIGNAL_B_WORSE_OR_RISK`: 미해당 — Group A에 B_worse 0
- `P5_NEEDS_HUMAN_REVIEW`: 미해당 — 5건 중 1건만 needs_human_review (본문 부재 영역 — 평가 곤란 사유)

---

End of P5 sampling execution report (12-sample semantic signal).
