# Item Split Manifest Shift Review

> 2026-05-27 KST. Post-item_split_implementation 후속.
> 본 보고서는 manifest shift **분석/설계만** 작성. policy 재수정 / hard check 완화 / input 재생성 0.

---

## 0. 핵심 한 줄 결론

**`SPLIT_DESIGN_ADJUSTMENT_RECOMMENDED`**.

- CLEAN 94 → 87 = -7 정합: exit 8 - new 1 = -7 ✓
- 8 exit 분류: **4 recoverable + 2 partial + 2 intentional drop (data debt)**
- 4 mismatch 전부 CLEAN 87 안 포함 (라우팅 변화, count 손실 0)
- S3/S4 keyword 보강 multi-word만 (broad `가공전선` 재도입 0)으로 CLEAN 91-93 도달 가능

---

## 1. CLEAN 94 → 87 감소 원인 분해 (수식 정합)

| 영역 | 값 |
|---|---:|
| baseline CLEAN | 94 |
| split CLEAN | 87 |
| Δ | -7 |
| exit (baseline CLEAN → split 비CLEAN) | **8** |
| new (baseline 비CLEAN → split CLEAN) | **1** |
| **공식** | **94 - 8 + 1 = 87** ✓ |

→ 사용자 명시 "1건 차이" 답: **1 NEW pid 발견** (`2003_3회_26` → S4 가공전선 기타 설비기준).

---

## 2. 숫자 정합 해명 (catalog 5 + gap 3 vs CLEAN 감소 7)

| 영역 | baseline | split | Δ |
|---|---:|---:|---|
| CLEAN | 94 | 87 | -7 |
| catalog | 51 | 60 | +9 |
| gap | 97 | 95 | -2 |
| total pool | 242 | 242 | 0 |

**불일치 영역**:
- catalog 5 + gap 3 = **8 exit pids** (baseline CLEAN 26 → split 비CLEAN)
- 그러나 catalog Δ = +9 (5건 + 4건 기존 비CLEAN→catalog 이동)
- gap Δ = -2 (3건 신규 gap 이동 + 5건 catalog/CLEAN으로 회복)
- 1 NEW pid (2003_3회_26) baseline 비CLEAN → split CLEAN

전체 수식:
- CLEAN -7 = exit 8 + new 1 (net)
- 다른 영역 이동 (catalog/gap 자체 내부 + 비CLEAN 영역 변동)이 catalog +9 / gap -2 영역에 추가 발현

---

## 3. 26 baseline pid fate Table

### 3.1 8 Exit pids 상세

| pid | fate | post-split item | kw | actual topic | cause |
|---|---|---|---|---|---|
| 1999_4회_84 | catalog | 가공전선 이격거리 | 이격거리 | 66kV 시가지 단면적 — 풀이 발전소 계측장치 | **data_debt** (OCR/풀이 mismatch) |
| 2003_3회_81 | catalog | **차단기** | 차단기 | 22.9kV 접지선 굵기 | **selector slot priority** (S4 kw 매칭 전 차단기 slot이 먼저) |
| 2004_1회_91 | gap | (no match) | - | 22.9kV 도로 횡단 높이 (OCR 깨짐) | **data_debt** |
| 2004_3회_92 | gap | (no match) | - | 66kV+6kV 동일 지지물 — 분석 불가 | **data_debt + S3 영역** |
| 2005_3회_81 | catalog | 가공전선 이격거리 | 이격거리 | 지지물 시설기준 | **S3 keyword 부족** |
| 2006_1회_85 | catalog | 가공전선 이격거리 | 이격거리 | 시가지 애자장치 — 풀이 부재 | **data_debt + S3 keyword 부족** |
| 2006_2회_83 | catalog | 가공전선 이격거리 | 이격거리 | 시가지 저압 가공전선로 도로 높이 | **score 영역** (S1 정합, NEEDS_REVIEW) |
| 2007_1회_84 | gap | (no match) | - | 지선 시설기준 (소선 3가닥) | **S4 D 지선 keyword 부족** |

### 3.2 1 New pid

| pid | post-split item | kw | rationale |
|---|---|---|---|
| 2003_3회_26 | 가공전선 기타 설비기준 (S4) | 전선 단면적 | baseline 비CLEAN → split S4 narrow keyword 매칭으로 CLEAN 진입 |

### 3.3 baseline 26 fate 종합

| 분류 | 건수 |
|---|---:|
| CLEAN (이동) | 18 |
| catalog | 5 |
| gap | 3 |
| **합** | **26** |

---

## 4. catalog 5 원인 분류

| pid | 원인 1차 | 원인 2차 | recoverable |
|---|---|---|---|
| 1999_4회_84 | data_debt | - | **NO** (intentional drop) |
| 2003_3회_81 | selector slot priority | S4 keyword 우선순위 | **YES** (S4 kw 우선순위 조정 후보) |
| 2005_3회_81 | S3 keyword 부족 | - | **YES** (S3 보강) |
| 2006_1회_85 | data_debt | S3 keyword 부족 | **PARTIAL** |
| 2006_2회_83 | score 영역 | S1 정합, NEEDS_REVIEW | **YES** (score/keyword 보강) |

---

## 5. gap 3 원인 분류

| pid | 원인 1차 | 원인 2차 | recoverable |
|---|---|---|---|
| 2004_1회_91 | data_debt (OCR 깨짐) | - | **NO** (intentional drop) |
| 2004_3회_92 | data_debt (풀이 부재) | S3 영역 | **PARTIAL** |
| 2007_1회_84 | S4 D 지선 keyword 부족 | - | **YES** (S4 지선 보강) |

---

## 6. mismatch 4 CLEAN count 귀속 판정

**전부 CLEAN 87 안 포함** ✓ — 라우팅 변화일 뿐 count 손실 0.

| pid | in CLEAN 87 | moved to | kw |
|---|:---:|---|---|
| 2001_2회_82 | ✓ | 가공전선로 경간·이도 | 인장강도 |
| 2007_1회_82 | ✓ | 가공전선로 경간·이도 | 인장강도 |
| 2007_2회_81 | ✓ | 절연내력 / 유도장해 | 통신선 |
| 2007_2회_82 | ✓ | 가공전선로 경간·이도 | 이도 |

→ **CLEAN count 회귀 0**. 단 학습자 입장 라우팅 변화는 metadata misleading 가능 — 별 audit 후보.

---

## 7. Recoverable vs Intentional Drop 분류

| 분류 | 건수 | pids |
|---|---:|---|
| **recoverable** (multi-word kw 보강) | 4 | 2003_3회_81 / 2005_3회_81 / 2006_2회_83 / 2007_1회_84 |
| **partial recoverable** (data debt + keyword) | 2 | 2004_3회_92 / 2006_1회_85 |
| **intentional drop** (data debt only) | 2 | 1999_4회_84 / 2004_1회_91 |
| **합** | **8** | |

→ keyword 보강 + 정책 결정으로 **최대 4-6건 회복 가능**.

---

## 8. S3 / S4 keyword 보강 후보

### 8.1 S3 (가공전선 지지물 시설) 보강 후보

| 현재 keywords (10개) | 보강 후보 |
|---|---|
| `지지물 시설` / `지지물 분기` / `발판 볼트` / `동일 지지물` / `시가지 가공전선로` / `농사용 가공전선로` / `지지물 종류` / `지지물 시가지` / `교차 시설` / `애자장치 시설` | `가공전선로 지지물` / `지지물 기준` / `발판 볼트 시설` / `옳지 않은 것 지지물` / `지지물 시설기준` |

**Broad 금지**: 단일 단어 `가공전선` 재도입 0. multi-word만.

**예상 회복 pids**: 2005_3회_81 (S3 정합) / 2006_1회_85 (S3 정합 + data debt 동시)

### 8.2 S4 (가공전선 기타 설비기준) 보강 후보

| 현재 keywords (11개) | 보강 후보 |
|---|---|
| `가공지선` / `지선 시설` / `지선 소선` / `접지선 굵기` / `접지 시설` / `통신선 시설` / `통신선 옥내` / `전선 굵기` / `전선 단면적` / `전선 지름` / `경동선 지름` | `가공전선 지선` / `지선 안전율` / `지선 도로 횡단` / `특고압 가공지선` / `지선 도로` / `지선 가공전선로` / `지선 굵기` |

**Broad 금지**: 단일 단어 `가공전선` 재도입 0.

**예상 회복 pids**: 2007_1회_84 (S4 D 지선 영역)

### 8.3 S1 / S2 — 보강 불필요

| split | 정합 | 결정 |
|---|---:|---|
| S1 (이격거리) | 6/6 | 현재 keyword 양호 |
| S2 (안전율/풍압) | 3/3 | 현재 keyword 양호 |

---

## 9. CLEAN 87 수용 가능성 평가

| 수용 영역 | 도달 CLEAN | 조건 |
|---|---:|---|
| 현 상태 (즉시) | 87 | split 적용 + keyword 보강 0 |
| keyword 보강 후 | 91 | S3/S4 keyword 보강 + 4 recoverable 회복 |
| data debt 부분 처리 후 | 93 | + 2 partial recoverable 회복 (data debt audit 동시) |
| 최대 도달 | 93 | 2 intentional drop은 data debt OCR/풀이 mismatch — questions.json 영역 audit 후 결정 |

**결정 영역**:
- CLEAN 94 hard check 완화 정책 채택 여부
- split design 보강 시간 비용
- data debt audit 별 영역 처리 결정

---

## 10. Hard Check 완화 필요 여부

| 경로 | hard check 완화 필요 |
|---|---|
| split design 보강으로 CLEAN 94 회복 | **불필요** |
| CLEAN 87 또는 91 수용 | **필요** (CLEAN ≥ 85 등 별 임계값) |
| split 폐기 | 불필요 |

**본 채널 판단**: split design 보강이 권장 경로 — hard check 완화 현 단계 **불필요**. 보강 후 CLEAN 91-93 도달 가능 시 data debt 별 audit 영역으로 분리 처리.

hard check design 결정: 별 게이트 — 본 게이트는 결정 0.

---

## 11. 추천 다음 게이트 (단일 추천 — §1.4)

**`SPLIT_DESIGN_ADJUSTMENT_RECOMMENDED`**.

### 11.1 근거

- 8 exit 중 4건 (50%) 또는 6건 (75% partial 포함) recoverable
- keyword 보강 multi-word만 사용 (broad `가공전선` 재도입 0)
- data debt 4건은 별 audit 영역 분리
- split의 본질 정합 효과 측정 완료 (1 new + 정합 14건 + recoverable 4-6건)
- 보강 design 후 implementation 재시도 시 CLEAN 91-93 도달 가능, hard check 차단 영역 회피

### 11.2 대안 (미해당)

| 옵션 | 미해당 사유 |
|---|---|
| CLEAN_87_ACCEPTANCE_RECOMMENDED | hard check 완화 결정 별 영역, 본 채널은 보강 우선 권장 |
| RESTORE_PREVIEW_RECOMMENDED | split 본질 효과 측정 가능 (정합 14건 + recoverable 4-6건) — 폐기 부적합 |
| HARD_CHECK_POLICY_DESIGN_NEEDED | 보강 우선 권장, 본 단계 정책 design 0 |
| NEEDS_HUMAN_DECISION_ON_SPLIT_SCOPE | 구조 분명히 분류됨 |

---

## 12. Claim Boundary

| claim | 본 게이트 상태 |
|---|---|
| CLEAN 94 → 87 = -7 (exit 8 + new 1 수식 정합) | (a) 측정 |
| 8 exit pids 원인 분류 (4 recoverable + 2 partial + 2 intentional) | (a) 분석 |
| mismatch 4건 CLEAN 87 안 포함 (라우팅 변화) | (a) 측정 |
| S3/S4 keyword 보강 후보 명세 | (a) 명세 |
| CLEAN 87/91/93 수용 영역 평가 | (a) 평가 |
| **policy 실제 수정** | **0** |
| **selector 코드 수정** | **0** |
| **input 재생성 / generation / audit** | **0** |
| **catalog/gap rescue 실행** | **0** |
| **hard check 완화 결정** | **0** (별 게이트) |
| **split design 실제 보강 적용** | **0** (별 게이트) |
| **pre_preview.py 원상복구** | **0** (사용자 결정 영역) |

---

## 13. 보호 영역 매트릭스 (전부 미수정 / 0)

`scripts/v_next_d3_pre_preview.py` 추가 수정 0 ✓ / pre_preview.py 원상복구 0 ✓ / input_creator hard check 완화 0 ✓ / `scripts/v_next_d3_selector.py` 수정 0 ✓ / `scripts/explanation_synthesizer.py` 수정 0 ✓ / `app/data/questions.json` 수정 0 ✓ / D-2 sealed assets 0 ✓ / v_full handoff scope 0 ✓ / input 재생성 0 ✓ / generation 재실행 0 ✓ / audit 재실행 0 ✓ / D-4 0 ✓ / catalog/gap rescue 0 ✓ / commit 0 ✓ / DEVLOG / Vault / MEMORY / decision JSONL 작성 0 ✓.

---

## 14. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_split/item_split_manifest_shift_review.md` | 본 보고서 (14 섹션) |
| `v_next_results_d3_split/item_split_manifest_shift_review.json` | machine-readable — 수식 정합 / 8 exit 상세 / 1 new / mismatch 귀속 / recoverable 분류 / keyword 보강 후보 / CLEAN 수용 평가 |

---

## 15. 최종 상태 판정

**판정**: `SPLIT_DESIGN_ADJUSTMENT_RECOMMENDED`

### 핵심 근거

- ✓ 수식 정합 확정 (94 - 8 + 1 = 87)
- ✓ 4 recoverable + 2 partial + 2 intentional drop 분류
- ✓ mismatch 4건 CLEAN count 손실 0
- ✓ S3/S4 keyword 보강 후보 명세 (broad 재도입 0)
- ✓ CLEAN 91-93 도달 가능 평가
- ✓ hard check 완화 현 단계 불필요 판정
- ✗ 대안 4 옵션 모두 미해당

다음 단계 (split design adjustment 적용 + S3/S4 keyword 보강) 진입은 사용자 명시 영역.

---

End of item split manifest shift review.
