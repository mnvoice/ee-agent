# D-3 Breaker Patch Design (Read-Only)

> 2026-05-27 KST. D-3 breaker patch design gate.
> 본 보고서는 차단기 13건 unexpected expansion-empty 회복을 위한 **수리 설계만** 수행.
> 실제 patch / generation 재실행 / audit 재실행 / commit / DEVLOG / Vault 0.
> 핵심 질문: "13건 회복 가능?" 아니라 **"13건 회복하면서 기존 성공 44 / non_expansion_metadata 37 / D-2 sealed / v_full baseline / 향후 D-4/P5 경로를 흔들지 않는가?"**.

---

## 0. 핵심 한 줄 결론

**최종 추천: B-only (B2 sub-option) — `scripts/v_next_d3_pre_preview.py:145` 1줄 보정**.

- Generator 전역 미수정 (회귀 위험 최저)
- Per-(slot,item) lookup이라 다른 81 항목 enriched_dynamic_link 변경 0
- v_full handoff scope / D-2 sealed assets 영향 0
- audit_group은 dl≠None 유지로 expansion 분류 보존
- Codex 감독관 1순위와 정합

A1 (narrow keyword) / A+B 결합은 step 4 별 게이트로 연기. A2 (fallback) 보수적 연기. C 재분류 **기각**.

---

## 1. A/B/C 진단 요약 (앞 보고서 인용)

진단 보고서 (`d3_breaker_expansion_empty_diagnosis.md`) 결론:

| 후보 | 판정 | 근거 |
|---|---|---|
| A. generator keyword map 누락 | 지지 | `CROSS_TARGET_KEYWORDS`에 차단기/단락전류/회로 단락전류/임피던스 환산 없음. `MATCHED_CORE_FALLBACK`에 차단기 없음. |
| B. dl 표현 substring 매칭 단절 | 지지 | dl `회로 단락전류 / 임피던스 환산`에서 기존 키 `회로 임피던스`가 연속 substring 매칭 안 됨. |
| **A+B 결합** | **가장 유력** | 양자 동시 성립 |
| C. 정책 정상 empty | 배제 | S/Fault expansion 허용 + 같은 slot 14건 dl_keyword 성공 |

---

## 2. dl Source of Truth 흐름 (회귀 분석 기반)

| step | file | line | role |
|---|---|---|---|
| 1 | `scripts/v_next_d3_pre_preview.py` | 138-148 | `CANDIDATE_POWER_POLICY[("전력공학","전력_보호고장S","차단기")]` 정의. **단일 출처**. |
| 2 | `scripts/v_next_d3_selector.py` | 185 | `"enriched_dynamic_link": policy.get("dl")` — preview 정책 read-only consumer |
| 3 | `scripts/v_next_d3_input_creator.py` | 106-107, 134 | input.md `dynamic_link:` 줄 + selection_manifest.json `enriched_dynamic_link` 필드 |
| 4 | `scripts/explanation_synthesizer.py` | 186-251 | `parse_dynamic_link` substring 매칭 |

**audit_group 자동 결정 룰** (`scripts/v_next_d3_selector.py:171`):
- `group = "expansion" if entry.get("dl") is not None else "non_expansion_metadata"`
- → 차단기 dl을 None으로 박으면 자동 non_expansion_metadata 진입 (이것이 C 후보의 메커니즘)

---

## 3. 후보 1-5 비교표

| # | 후보 | 변경 파일 | 변경 줄 | 예상 회복 | 회귀 위험 | 범위 |
|---:|---|---|---:|---|---|---|
| 1 | **B-only** (dl 정규화) | `v_next_d3_pre_preview.py` | 1 | 13/13 (회로이론 1 target) | **very low** | D-3 국소 (per-(slot,item) lookup) |
| 2 | A1 (좁은 keyword 추가) | `explanation_synthesizer.py` | 1-3 | 13/13 + 미래 차단기 변형 | medium | Generator 전역 |
| 3 | A2 (fallback 추가) | `explanation_synthesizer.py` | 2-5 | 13/13 + 미래 모든 차단기 (dl 불문) | medium-high | Generator 전역 fallback |
| 4 | A+B 결합 | 위 1+2 또는 1+3 | 합산 | 위 결합 | 합산 | 회복 attribution 모호 |
| 5 | C (재분류 → non_expansion) | `v_next_d3_pre_preview.py` (dl=None) | 1 | 0 (회복 아님, 재분류) | low (mechanical) | 의미 부적합 / framework 훼손 |

---

## 4. 후보별 상세 설계

### 4.1 후보 1: B-only (D-3 ITEM_POLICY dl 정규화) — **1순위**

**변경 위치**: `scripts/v_next_d3_pre_preview.py:145`

| sub-option | 새 dl 표현 | 매칭 hit | scope |
|---|---|---|---|
| B1 | `전력 차단기 -> 회로 단락전류 환산 -> 회로 임피던스 환산` | `회로 임피던스` substring hit | 두 회로 segment 분리, 대칭형 |
| **B2** (권장) | `전력 차단기 -> 회로 단락전류 / 회로 임피던스 환산` | `회로 임피던스` substring hit | **최소 변경** (`임피던스 환산` 앞에 `회로` 1단어 추가) |
| B3 | `전력 차단기 -> 회로 임피던스 환산 -> 설비 차단 보호` | `회로 임피던스` + `설비 보호` 2 hit | 더 공격적, 새 단어 도입 |

**B2 추천 이유**: scope clamp 가장 좁음. 단어 신규 도입 0, 기존 `회로` 토큰 1개만 추가.

**예상 회복**: 13/13 → cross_subject_expansion target=회로이론 (1 expansion entry). Multi-target (회로이론 + 전기설비) 회복은 A1 키워드 추가 필요.

**회귀 위험 분석**:
- ITEM_POLICY lookup은 `(subject, slot, item)` 정확 일치 (`scripts/v_next_d3_selector.py:182`). 다른 17 item 영향 0.
- selection_manifest 갱신 범위: 차단기 13 rows의 `enriched_dynamic_link` 만. 다른 81 rows 영향 0.
- v_full handoff scope 영향 **0** (D-3 정책은 v_full 영역 외부).
- D-2 sealed assets 영향 **0**.
- Generator (explanation_synthesizer.py) 미수정.
- audit_group: 차단기 dl ≠ None 유지 → expansion 분류 보존 (selector line 171).

**필요한 검증 절차** (별 implementation 게이트 영역):

1. `v_next_d3_selector.py` 재실행 → selection_manifest 차단기 13 rows의 `enriched_dynamic_link`만 변경 / 다른 81 rows diff 0 확인.
2. `v_next_d3_parser_validator.py` 재실행 → parse PASS 94/94 + audit_group expansion 57/57 + non_expansion 37/37 보존 확인.
3. `explanation_synthesizer.py` 재실행 (별 출력 디렉토리 `v_next_results_d3_b/`) → 13 차단기 outputs의 `cross_subject_expansion.expands_to` non-empty 확인.
4. 81 비차단기 outputs를 v_next_results_d3와 diff → 변경 0 확인 (회귀 게이트).
5. `d3_audit.py` 재실행 → 4차원 join table에서 `(expansion, dl_keyword)=57 / (expansion, empty)=0` 확인.
6. 7 dimension delta 측정: 13 차단기에서만 발현, 81 항목 delta=0 확인.

---

### 4.2 후보 2: A1 (CROSS_TARGET_KEYWORDS narrow 추가) — 2순위 (B-only 후 추가 결정 영역)

**변경 위치**: `scripts/explanation_synthesizer.py:100-147`

| sub-option | 추가 entry | dl substring hit? | 회로이론 target overshoot 위험 |
|---|---|---|---|
| A1a | `("차단기", "전기기기")` | dl head `전력 차단기` 안에 `차단기` 있음 → hit | target=전기기기는 차단기 학습 본질(회로 단락전류) 거리 — 의미 부적합 가능 |
| A1b | `("단락전류", "회로이론")` | dl `회로 단락전류` 안에 `단락전류` 있음 → hit | 일반 단어 — 단락전류·임피던스 item dl에도 hit (중복 dedup으로 무해 가능성, 측정 필요) |
| **A1c** | `("회로 단락전류", "회로이론")` | dl `회로 단락전류` substring 정확 hit | 더 구체적, overshoot 위험 낮음 |

**A1c 추천 (sub-option 중)**. 단 **standalone 권장 안 함** — B-only first 후 step 4에서 multi-target 필요 판단 시 추가 결정.

**회귀 위험**:
- Generator 전역 변경. v_full 1000 + v_next D-3 94 + 미래 모든 generation 영향 가능.
- A1c (`회로 단락전류`)는 구체적이라 overshoot 가능성 낮음. 단 측정 필수.
- explanation_synthesizer.py는 v_full handoff scope 보호 영역. 수정 자체가 사용자 명시 게이트 영역.

---

### 4.3 후보 3: A2 (MATCHED_CORE_FALLBACK 추가) — 보수적

**변경 위치**: `scripts/explanation_synthesizer.py:150-174`

| sub-option | 추가 entry |
|---|---|
| A2a | `"차단기": [("회로이론", "차단기 → 회로 단락전류 / 임피던스 환산 경로")]` |
| A2b | `"차단기": [("회로이론", ...), ("전기설비기술기준", ...)]` (multi-target) |

**보수 권고 이유**:
- A2는 Path 3 fallback이므로 dl_keyword path 성공 항목 영향 0 (Path 2 hit 시 Path 3 안 들어옴).
- 그러나 matched_core_name='차단기'인 **모든** input (현재 13 + 미래 unbounded)에 자동 작동.
- 미래 dl=None을 의도적으로 박을 차단기 input이 있으면 자동 expansion 발현 — 정책 자유도 축소.

**판정**: deferred — A1/B로 회복 안 되는 영역에 한해 마지막 고려.

---

### 4.4 후보 4: A+B 결합

**경고**: 동시 적용 시 회복 attribution 모호. 어떤 변경이 어느 케이스를 회복했는지 분리 측정 불가.

**Codex 감독관 권고와 본 채널 정합**: B-only first → measure → if needed, add A1c.

---

### 4.5 후보 5: C 재분류 — **기각**

**메커니즘**: `scripts/v_next_d3_pre_preview.py:145` dl=None → selector line 171 자동 non_expansion_metadata.

**기각 이유**:
1. S/Fault는 expansion 정책 허용 (`scripts/explanation_synthesizer.py:237`).
2. 같은 slot 14건 dl_keyword 성공.
3. 차단기 학습 본질이 회로 단락전류 / 회로 임피던스 환산 영역으로 자연 연결됨 — 의미 부적합.
4. 실제 gap을 masking — 수리 아님.
5. paired audit framework의 expansion vs non_expansion 분리 정합성 훼손 (57 → 44).

**판정**: **REJECTED**.

---

## 5. 추천 구현 순서 (step 1-4)

| step | action | 사용 file | gate |
|---:|---|---|---|
| 1 | B-only (B2 sub-option) — `v_next_d3_pre_preview.py:145` dl 1줄 보정 | 정책 단일 출처 | 사용자 명시 implementation 게이트 |
| 2 | `v_next_d3_selector.py` → `v_next_d3_parser_validator.py` → `explanation_synthesizer.py` 순차 재실행 (출력 dir: `v_next_results_d3_b/`) | 재생성 | 동일 게이트 (재생성 허용 명시 시) |
| 3 | `d3_audit.py` 재실행 → 4차원 join에서 `(expansion, dl_keyword)=57 / (expansion, empty)=0` 확인 + 81 비차단기 항목 delta=0 회귀 검증 | audit | 동일 게이트 |
| 4 | 13 차단기 회복 measurement 후 multi-target 필요 판단 → A1c 추가 결정 / step 종결 결정 | 결정 | 별 사용자 명시 결정 게이트 |

**Codex 감독관 가설 정합**: B-only 1순위 → step 4에서 A1 추가 판단. 본 design 일치.

---

## 6. 최종 추천안 (§1.4 책임)

**1개 선택**: **B-only (B2 sub-option)**.

### 추천 근거

1. Single line change (`v_next_d3_pre_preview.py:145`)
2. Generator 전역 미수정 — `explanation_synthesizer.py` read-only 유지
3. Per-(slot,item) lookup으로 다른 81 항목 enriched_dynamic_link 변경 0
4. v_full 1000 영향 0 (D-3 정책은 v_full handoff scope 외부)
5. D-2 sealed assets 영향 0
6. audit_group 자동 결정 룰이 dl≠None 그대로 보존 → expansion 분류 유지 (paired audit framework 정합 보존)
7. Codex 감독관 1순위와 정합
8. 13건 일점 집중 패턴 (5축 모두 동일)에 정확히 대응 — 1줄 수정으로 전건 회복
9. 4차원 join table의 `(expansion, dl_keyword)` 단조 증가 측정 가능 (44 → 57, 기존 44 변경 0)

### 본 추천이 처리하지 못하는 영역 (deferred)

- Multi-target 회복 (회로이론 + 전기설비기술기준 / 전기기기): step 4 A1c 추가 결정 영역
- 미래 차단기 dl 변형 (다른 표현으로 다시 변형되는 경우): step 4 A1c / A2a 결정 영역

---

## 7. 보류 / 기각 후보

| 후보 | 상태 | 조건 |
|---|---|---|
| A1c (narrow keyword `회로 단락전류`) | **deferred** to step 4 | B-only step 3 측정 결과 multi-target 필요 판단 시 / overshoot 측정 통과 시 |
| A2a (matched_core_fallback) | **deferred** — conservative | dl 변형 영역이 너무 다양해서 keyword/dl 정규화 모두 한계일 때만 |
| A+B 결합 | **deferred** — sequential | step 1-3 단독 B-only 측정 후 step 4에서 결합 결정 |
| C 재분류 | **REJECTED** | 의미 부적합 + audit framework 훼손 |

---

## 8. claim boundary 점검

| claim | 본 design 상태 |
|---|---|
| B-only가 13건 회복 가능 (mechanical) | (a) 분석 — substring 매칭 룰 직접 트레이스 |
| B-only 회귀 위험 very low | (a) 분석 — per-(slot,item) lookup 룰 + v_full handoff 외부 |
| 실제 patch 적용 | **claim 0** — implementation 게이트 영역 |
| 재실행 / audit 재현 | **claim 0** — implementation 게이트 영역 |
| Semantic gain (회복된 expansion의 학습 가치) | **claim 0** — 별 sampling/P5 영역 |
| A1c 추가 결정 | **claim 0** — step 4 별 게이트 |
| Multi-target 회복 필요 여부 | **claim 0** — step 3 측정 후 결정 |
| 미래 차단기 변형 회복 정책 | **claim 0** — 별 정책 영역 |

---

## 9. 보호 영역 매트릭스 (전부 미수정 / 0)

| 보호 대상 | 본 design 단계 상태 |
|---|---|
| `scripts/explanation_synthesizer.py` | 미수정 ✓ (read-only 분석만) |
| `scripts/v_next_d3_pre_preview.py` | 미수정 ✓ (수정 design만 — step 1 영역) |
| `scripts/v_next_d3_selector.py` | 미수정 ✓ |
| `scripts/v_next_d3_input_creator.py` | 미수정 ✓ |
| `scripts/v_next_d3_parser_validator.py` | 미수정 ✓ |
| `scripts/v2_input_parser.py` | 미수정 ✓ |
| `app/data/questions.json` | 미수정 ✓ |
| D-2 sealed assets | 미수정 ✓ |
| v_full handoff scope | 미수정 ✓ |
| D-3 generation 재실행 | 0 ✓ |
| D-3 audit 재실행 | 0 ✓ |
| P5 sample experiment | 0 ✓ |
| D-4 진입 | 0 ✓ |
| catalog/gap rescue | 0 ✓ |
| keyword expansion | 0 ✓ |
| reuse tranche | 0 ✓ |
| commit | 0 ✓ |
| DEVLOG / Vault / MEMORY / decision JSONL 작성 | 0 ✓ |

---

## 10. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3/d3_breaker_patch_design.md` | 본 design 보고서 (10 섹션) |
| `v_next_results_d3/d3_breaker_patch_design.json` | machine-readable — 5 후보 비교 + sub-option / 회귀 위험 / 검증 절차 / 추천 순서 / 최종 추천 / 보류/기각 |

---

## 11. 최종 상태

**판정**: `READY_FOR_BREAKER_PATCH_IMPLEMENTATION_GATE`

- ✓ 5 후보 비교 완료
- ✓ 각 후보 변경 파일 / 회복 범위 / 회귀 위험 / 검증 절차 design 완료
- ✓ 단일 추천안 (B-only B2 sub-option) 확정
- ✓ 보류 (A1c, A2a, A+B) / 기각 (C) 분리
- ✓ 다음 구현 게이트 진입 조건 명시
- ✓ Codex 감독관 1순위 가설 정합

다음 단계 (실제 patch + 재생성 + 회귀 검증) 진입은 본 design 다음 별 사용자 명시 게이트.

---

End of D-3 breaker patch design (read-only) report.
