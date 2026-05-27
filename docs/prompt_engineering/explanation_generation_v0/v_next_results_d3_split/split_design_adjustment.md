# Split Design Adjustment (Keyword Boost Design)

> 2026-05-27 KST. Post-manifest_shift_review 후속.
> 본 보고서는 keyword 보강 **design만** 작성. 실제 policy 수정 / hard check 완화 / input 재생성 / commit 0.

---

## 사용자 메시지 잘림 알림

사용자 메시지 끝 "DEVLOG / Vault / MEMORY / decision" 이후 미발현. 본 채널 design 정합 추정:
- 산출물: `v_next_results_d3_split/split_design_adjustment.md` + `.json`
- 최종 상태 옵션: ADJUSTMENT_DESIGN_READY / NEEDS_FIX / BLOCKED 영역
- 금지: decision JSONL 작성 0

---

## 0. 핵심 한 줄 결론

**`ADJUSTMENT_DESIGN_READY`** + 부수적으로 `HARD_CHECK_DESIGN_NEEDED` (post-boost CLEAN 89-90 수용 별 게이트).

- 보강 keyword 5개 추가 (S1 +1 / S3 +3 / S4 +1)
- CLEAN 87 → **89 회복** 예상 (conservative + expected)
- 과매칭 위험 0 (242 중 hits ≤ 3)
- broad `가공전선` 재도입 0 — multi-word only
- 단 94 회복 불가 → hard check 정책 별 게이트 필요

---

## 1. Recoverable Pid 매칭 측정 결과

| pid | actual topic | intended split | hit keywords | recovery |
|---|---|---|---|---|
| 2005_3회_81 | 가공전선 지지물 시설기준 (옳지 않은 것) | S3 | `가공전선로 지지물` / `지지물 기준` / `지지물 시설기준` (3 hit) | **YES** |
| 2006_2회_83 | 시가지 저압 가공전선로 도로 지표상 최저 높이 | S1 | `지표상 높이` (S1 추가) | **YES** |
| 2003_3회_81 | 22.9kV 중성선 다중접지식 접지선 굵기 | S4 | `지선 굵기` (1 hit) | **PARTIAL** (selector priority 차단기 slot 먼저) |
| 2007_1회_84 | 지선 시설기준 (소선 3가닥) | S4 | `도로 횡단` (S1) + `가공전선로 지지물` (S3) — 의도 영역 mismatch | **RISKY** (보류) |
| 2006_1회_85 | 154kV 시가지 애자장치 — 풀이 부재 | S3 | 모든 candidate hit 0 | **NO** (data debt) |

---

## 2. 과매칭 위험 측정 (전체 242)

| candidate | hits in 242 | broad risk |
|---|---:|:---:|
| 가공전선로 지지물 | 3 | NO |
| 지지물 기준 | 1 | NO |
| 발판 볼트 시설 | 0 | NO |
| 옳지 않은 것 지지물 | 0 | NO |
| 지지물 시설기준 | 1 | NO |
| 가공전선 지선 | 0 | NO |
| 지선 안전율 | 0 | NO |
| 지선 도로 횡단 | 0 | NO |
| 특고압 가공지선 | 0 | NO |
| 지선 도로 | 0 | NO |
| 지선 가공전선로 | 0 | NO |
| 지선 굵기 | 1 | NO |
| 지표상 높이 | 3 | NO |
| 도로 횡단 | 1 | NO |

→ 전 candidate hits ≤ 3. **broad 위험 0**. multi-word 정합 양호.

---

## 3. 보강 keyword 최종 design

### 3.1 S1 가공전선 이격거리

| 현재 keywords (7) | 추가 |
|---|---|
| `이격거리` / `이격 거리` / `수평 이격` / `수직 이격` / `식물 이격` / `안테나 이격` / `약전류전선 이격` | **`지표상 높이` (+1)** |

skip: `도로 횡단` — S1 의도 mismatch 위험 (S4 D 영역 sample에 매칭 가능)

### 3.2 S3 가공전선 지지물 시설

| 현재 keywords (10) | 추가 |
|---|---|
| `지지물 시설` / `지지물 분기` / `발판 볼트` / `동일 지지물` / `시가지 가공전선로` / `농사용 가공전선로` / `지지물 종류` / `지지물 시가지` / `교차 시설` / `애자장치 시설` | **`가공전선로 지지물` / `지지물 기준` / `지지물 시설기준` (+3)** |

### 3.3 S4 가공전선 기타 설비기준

| 현재 keywords (11) | 추가 |
|---|---|
| `가공지선` / `지선 시설` / `지선 소선` / `접지선 굵기` / `접지 시설` / `통신선 시설` / `통신선 옥내` / `전선 굵기` / `전선 단면적` / `전선 지름` / `경동선 지름` | **`지선 굵기` (+1)** |

skip: `가공전선 지선` / `지선 안전율` / `지선 도로 횡단` / `특고압 가공지선` / `지선 도로` / `지선 가공전선로` — 모두 hit 0

### 3.4 S2 가공전선 안전율 / 풍압

| 현재 keywords (8) | 추가 |
|---|---|
| `풍압 하중` / `병종 풍압` / `갑종 풍압` / `안전율` / `목주 안전율` / `철탑 안전율` / `지지물 강도` / `인장강도 지지물` | **0** (3/3 정합 양호) |

### 3.5 종합

| split | 현재 | 추가 | 총 |
|---|---:|---:|---:|
| S1 | 7 | +1 | 8 |
| S2 | 8 | 0 | 8 |
| S3 | 10 | +3 | 13 |
| S4 | 11 | +1 | 12 |
| **합** | **36** | **+5** | **41** |

---

## 4. Partial Recoverable 2건 결정

| pid | fate | 결정 |
|---|---|---|
| 2004_3회_92 | gap (data debt 풀이 부재) | **intentional drop** — keyword 회복 불가 |
| 2006_1회_85 | catalog (data debt + S3 영역, hit 0) | **intentional drop** — keyword 회복 불가 |

→ 본 design 회복 대상 제외.

---

## 5. Intentional Drop 2건 확인

| pid | 사유 |
|---|---|
| 1999_4회_84 | data debt OCR/풀이 mismatch |
| 2004_1회_91 | data debt OCR + 풀이 부재 |

→ 회복 대상 제외. questions.json audit 영역.

---

## 6. CLEAN 회복 시나리오

| 시나리오 | CLEAN | Δ from 87 | 회복 pid |
|---|---:|---:|---|
| **conservative** | **89** | +2 | 2005_3회_81 (S3) + 2006_2회_83 (S1) |
| **expected** | **89** | +2 | 동일 (2003_3회_81는 selector priority, 2007_1회_84 mismatch 위험 — 보수 산정) |
| **max** | **90** | +3 | + 2003_3회_81 (S4 selector priority 개선 가정 — 단 사용자 명시 selector 수정 0) |

intentional drop 영구 영역: 4건 (1999_4회_84 / 2004_1회_91 / 2004_3회_92 / 2006_1회_85).
data debt audit 후 회복 가능: +4 (94 도달 가능, 단 questions.json audit 별 영역).

---

## 7. Hard Check 완화 필요 여부 재평가

| 측정 | 값 |
|---|---|
| current state | `input_creator.py:310-312` — CLEAN 94 강제 |
| post-boost expected CLEAN | 89 (또는 max 90) |
| still below 94 | **YES** |
| **necessity** | **필요** — 89 수용 정책 별 게이트 |

옵션:
| 옵션 | 내용 |
|---|---|
| A | CLEAN ≥ 85 등 별 임계값 (input_creator 수정 — 사용자 명시 0) |
| B | CLEAN 94 hard check → warning 격하 + 실행 허용 |
| C | data debt audit 후 questions.json 보강으로 94 회복 |

**본 채널 판단**: hard check 완화 정책 결정은 **별 게이트**. 본 design은 keyword 보강 + CLEAN 회복 예측만.

---

## 8. Implementation 재시도 절차

| step | 작업 |
|---:|---|
| 1 | `scripts/v_next_d3_pre_preview.py` 보정 (S1 +1 / S3 +3 / S4 +1 keywords, 총 +5 line) |
| 2 | `scripts/v_next_d3_selector.py` dry-run 재실행 → CLEAN 측정 (예상 89-90) |
| 3 | Hard check 차단 영역 — input 재생성 위해 별 hard check 완화 정책 결정 필요 |
| 4 | 별 게이트: hard check 완화 design + 적용 |
| 5 | `input_creator` 재실행 → input 재생성 |
| 6 | `synthesizer` + post-split metadata audit 재실행 |
| 7 | 기존 misleading 개선 측정 + 회귀 검증 |

→ Step 3-7은 별 게이트 영역 (사용자 명시).

---

## 9. Claim Boundary

| claim | 본 design 상태 |
|---|---|
| recoverable pid 매칭 측정 (5 pid × 14 candidate) | (a) 측정 |
| 과매칭 위험 측정 (242 sample × 14 candidate) | (a) 측정 |
| 보강 5 keyword 최종 design (S1+1 / S3+3 / S4+1) | (a) 명세 |
| CLEAN 회복 시나리오 (87 → 89 conservative / expected) | (a) 예측 |
| hard check 완화 필요성 평가 | (a) 평가 |
| **policy 실제 수정 적용** | **0** |
| **selector 수정** | **0** |
| **input_creator hard check 수정** | **0** |
| **input 재생성 / generation / audit** | **0** |
| **catalog/gap rescue 실행** | **0** |
| **pre_preview.py 원상복구** | **0** |
| **post-boost CLEAN 정확 측정** | **0** (실측은 implementation 영역) |
| **post-boost metadata audit 개선** | **0** (audit 재실행 영역) |

---

## 10. 보호 영역 매트릭스 (전부 미수정 / 0)

`scripts/v_next_d3_pre_preview.py` 추가 수정 0 ✓ / pre_preview.py 원상복구 0 ✓ / `scripts/v_next_d3_selector.py` 수정 0 ✓ / `scripts/explanation_synthesizer.py` 수정 0 ✓ / `scripts/v_next_d3_input_creator.py` hard check 완화 0 ✓ / `app/data/questions.json` 수정 0 ✓ / D-2 sealed assets 0 ✓ / v_full handoff scope 0 ✓ / input 재생성 0 ✓ / generation 재실행 0 ✓ / audit 재실행 0 ✓ / D-4 0 ✓ / catalog/gap rescue 0 ✓ / commit 0 ✓ / DEVLOG / Vault / MEMORY / decision JSONL 작성 0 ✓.

---

## 11. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_split/split_design_adjustment.md` | 본 design 보고서 (11 섹션) |
| `v_next_results_d3_split/split_design_adjustment.json` | machine-readable — recoverable pid 매칭 / 과매칭 측정 / 5 keyword design / CLEAN 시나리오 / hard check 평가 / implementation 절차 |

---

## 12. 최종 상태 판정

**판정**: `ADJUSTMENT_DESIGN_READY`
**부수적**: `HARD_CHECK_DESIGN_NEEDED` (post-boost CLEAN 89-90 수용 별 게이트)

### 핵심 근거

| 검증 기준 | 결과 |
|---|---|
| 5 recoverable pid 매칭 측정 완료 | ✓ |
| 과매칭 위험 측정 (전 candidate hits ≤ 3) | ✓ |
| 보강 5 keyword 최종 design (broad 0) | ✓ |
| CLEAN 89-90 회복 시나리오 예측 | ✓ |
| Hard check 완화 별 게이트 식별 | ✓ |
| Implementation 절차 7 step 명세 | ✓ |
| `NEEDS_DESIGN_FIX` / `BLOCKED_BY_RECOVERABLE_INSUFFICIENT` 미해당 | ✓ |

다음 단계 (보강 keyword implementation + selector dry-run + hard check 완화 design) 진입은 사용자 명시 영역.

---

End of split design adjustment (design only) report.
