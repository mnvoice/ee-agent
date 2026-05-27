# Metadata Policy Review Execution Report

> 2026-05-27 KST. Post-metadata_policy_review_design 후속.
> 본 보고서는 **가공전선 이격거리 26 sample 전수 read + taxonomy 분류 + cross-tab + split 후보 + selector keyword integrity 판정**. policy 실제 수정 / item split 적용 / selector 코드 수정 / catalog rescue / D-4 / commit 0.

---

## 사용자 메시지 잘림 알림

사용자 메시지 끝 잘림: "selector keyword integrity 판단: '이격거리' keyword가 실제 이격거리와 얼마나" 이후 명시 영역 미발현. 본 채널은 design 정합 추정으로 산출물 경로 / 최종 상태 옵션 / 금지 영역 진행. 추정 영역 명시.

---

## 0. 핵심 한 줄 결론

**`ITEM_SPLIT_RECOMMENDED`** (primary) + `SELECTOR_BROAD_MATCH_CONFIRMED` + `POLICY_DEFINITION_ISSUE_CONFIRMED` (secondary).

- 정합 20건 중 A (이격거리) **30%만**, 70%는 다른 영역
- "가공전선" kw 적중률 **28.6%** (broad), "이격거리" + "가공지선" kw 100% (narrow)
- 4 split 후보 (A/B/C/E+D) 모두 threshold ≥3건 충족
- 5 원인 중 C1+C2+C3 동시 CONFIRMED, C4 MEDIUM, C5 REJECTED

---

## 1. Sample별 분류 (26건 전수)

| input | pid | kw | 본 문제 | 카테고리 | X |
|---|---|---|---|:---:|:---:|
| 008 | 1999_4회_81 | 가공전선 | 목주 풍압 하중 안전율 1.3 | **B** | |
| 009 | 1999_4회_84 | 가공전선 | 66kV 시가지 전선 단면적 (50mm²) — 풀이는 발전소 계측장치 | **E** | **X** |
| 014 | 2000_2회_86 | 이격거리 | 애자공사 고압 옥내배선 이격거리 (15cm) | **A** | |
| 021 | 2000_6회_92 | 가공전선 | 고압 가공전선 ↔ 안테나 이격거리 (60cm) | **A** | **X** |
| 026 | 2001_2회_82 | 가공전선 | 저압 가공전선 ↔ 25kV 교류전차선 교차 케이블 단면적 35mm² | **C** | |
| 037 | 2002_3회_85 | 가공전선 | 농사용 저압 가공전선로 최대 경간 30m | **C** | |
| 044 | 2003_3회_81 | 가공전선 | 22.9kV 중성선 다중접지식 접지선 굵기 | **E** | |
| 046 | 2004_1회_84 | 이격거리 | 특고압 지중전선 ↔ 가연성 관 이격거리 (1m) | **A** | |
| 048 | 2004_1회_91 | 가공전선 | 22.9kV 가공전선 도로 횡단 시 높이 | **A** | **X** |
| 053 | 2004_2회_86 | 이격거리 | 154kV 가공송전선 ↔ 식물 이격거리 (3.2m) | **A** | |
| 059 | 2004_3회_83 | 가공전선 | 154kV 가공전선로 ↔ 도로 이격거리 (4.8m) | **A** | |
| 060 | 2004_3회_92 | 가공전선 | 66kV+6kV 동일 지지물 시설 단면적 | **C** | **X** |
| 069 | 2005_3회_81 | 가공전선 | 가공전선 지지물 시설기준 | **C** | |
| 072 | 2006_1회_29 | 가공지선 | 가공지선 설명 틀린 것 | **E** | |
| 073 | 2006_1회_85 | 가공전선 | 154kV 가공전선 애자장치 시가지 시설 | **C** | **X** |
| 074 | 2006_1회_86 | 가공전선 | 가공전선로 구성재 풍압 하중 (병종) | **B** | |
| 076 | 2006_2회_83 | 가공전선 | 시가지 저압 가공전선로 지표상 최저 높이 | **A** | |
| 077 | 2006_2회_86 | 가공전선 | 강관 철탑 병종 풍압 하중 | **B** | |
| 080 | 2006_3회_81 | 가공전선 | 특고압 가공전선 ↔ 약전류전선 동일 지지물 (35kV 초과) | **C** | |
| 081 | 2006_3회_83 | 가공전선 | 특고압 가공지선 지름 규격 (5mm) | **E** | |
| 084 | 2007_1회_81 | 가공전선 | 저압 가공전선 상호간 + 지지물 이격거리 | **A** | |
| 085 | 2007_1회_82 | 가공전선 | 400V 이하 저압 가공전선 굵기 (3.2mm) | **E** | |
| 086 | 2007_1회_84 | 가공전선 | 지선 시설기준 (소선 3가닥) | **D** | |
| 089 | 2007_2회_27 | 가공지선 | 가공지선 설치 목적 | **E** | |
| 090 | 2007_2회_81 | 가공전선 | 통신선 옥내 시설 400V 초과 적용 | **E** | |
| 091 | 2007_2회_82 | 가공전선 | 154kV 가공전선 ↔ 도로 제2차 접근 길이 합계 | **A** | **X** |

---

## 2. 카테고리 분포 (전체 26건)

| 카테고리 | 건수 | 비중 |
|---|---:|---:|
| A. 실제 이격거리 | 9 | 34.6% |
| B. 안전율 / 풍압 | 3 | 11.5% |
| C. 지지물 시설기준 | 6 | 23.1% |
| D. 지선 시설기준 | 1 | 3.8% |
| E. 기타 설비기준 | 7 | 26.9% |
| 합 | **26** | 100% |

X (data debt) 동시 표시: **6건** (009 / 021 / 048 / 060 / 073 / 091).

---

## 3. 정합 분포 (X 제외 20건)

| 카테고리 | 정합 건수 | 비중 (정합 20 기준) |
|---|---:|---:|
| A | 6 | **30.0%** |
| B | 3 | 15.0% |
| C | 4 | 20.0% |
| D | 1 | 5.0% |
| E | 6 | 30.0% |
| 합 | 20 | 100% |

→ **A (실제 이격거리)는 30%만**. 70%는 안전율 / 지지물 / 지선 / 기타 영역. policy issue 확정.

---

## 4. matched_keyword × Category Cross-tab

| kw \ 카테고리 | A | B | C | D | E | X overlap | 합 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 가공전선 (21) | 6 | 3 | 6 | 1 | 5 | 6 | 21 |
| 이격거리 (3) | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| 가공지선 (2) | 0 | 0 | 0 | 0 | 2 | 0 | 2 |

### 4.1 keyword integrity 결과

| keyword | 매칭 | A 적중 | A 적중률 | 판정 |
|---|---:|---:|---:|---|
| **가공전선** | 21 | 6 | **28.6%** | broad — 5 카테고리 분산 |
| 이격거리 | 3 | 3 | 100.0% | narrow + accurate |
| 가공지선 | 2 | 0 (E 2) | 0% / E 100% | narrow + accurate to E |

→ "가공전선" 단일 keyword가 **broad match 메커니즘** 입증.

---

## 5. Item Split 결정

| 새 item 후보 | scope | 정합 건수 | 결정 |
|---|---|---:|---|
| 가공전선 이격거리 (기존 유지) | A | 6 | **SPLIT_RECOMMENDED** |
| 가공전선 안전율 / 풍압 | B | 3 | **SPLIT_RECOMMENDED** |
| 가공전선 지지물 시설 | C | 4 | **SPLIT_RECOMMENDED** |
| 가공전선 지선 시설 | D | 1 | **MERGE_TO_E** (1건만이라 통합) |
| 가공전선 기타 설비기준 (D+E 통합) | D+E | 7 | **SPLIT_RECOMMENDED** |

→ **4 split 권장 + D는 E에 통합**.

Split 실제 적용 0 — 본 게이트는 design + measurement만.

---

## 6. 원인 분해 최종 가중치

| ID | 원인 | 판정 | 근거 |
|---|---|---|---|
| **C1** | policy definition issue | **CONFIRMED_HIGH** | 기존 essence가 이격거리 중심 — 70% non-A 영역 미흡 |
| **C2** | selector broad match | **CONFIRMED_HIGH** | '가공전선' kw 적중률 28.6% — broad |
| **C3** | item split needed | **CONFIRMED_HIGH** | 4 후보 (A/B/C/E+D) 모두 ≥3건 |
| C4 | data debt | CONFIRMED_MEDIUM | 6/26 = 23.1% X 발현, policy issue와 별 영역 |
| C5 | sample-only exception | **REJECTED** | 정합 14/20 (70%) misleading — 우연 아님 |

→ **C1+C2+C3 동시 발현 입증**. 본질적 해결법은 item split + selector kw 정합화 + essence 영역 확장.

---

## 7. 5 Pathway 매핑 (design 정합 추정)

| 조건 | 매칭 | 다음 상태 |
|---|:---:|---|
| item_split_recommended (4 후보 ≥3건) | ✓ | **`ITEM_SPLIT_RECOMMENDED`** |
| selector_broad_match_confirmed (가공전선 28.6%) | ✓ | `SELECTOR_BROAD_MATCH_CONFIRMED` |
| policy_definition_issue_confirmed (essence 영역 미흡) | ✓ | `POLICY_DEFINITION_ISSUE_CONFIRMED` |
| data_debt_dominant | 미해당 | X 23% < policy issue 70% |
| sample_only_exception | 미해당 | 패턴 일관 |

---

## 8. 다음 게이트 추천 (우선순위)

| # | 후보 | scope |
|---:|---|---|
| 1 | **item_split_design** | 가공전선 이격거리 → 4 sub-item (A/B/C/E) split design + 각 essence/trap 신정의 + matched_keyword narrow set design |
| 2 | **selector_keyword_integrity_design** | "가공전선" kw → multi-word kw set ("가공전선 이격거리" / "가공전선 풍압" / "가공전선 지지물" / "가공전선 기타") design |
| 3 | data_debt_audit_design | 6 X sample 별 audit (questions.json 영역) — policy issue와 분리 처리 |
| 4 | 본 결과 commit + push | 사용자 명시 별 게이트 |
| 5 | 37 모집단 확대 audit | 다른 4 item (역률 개선 / 부하율·수용률·부등률 / 가공전선로 경간·이도 / 절연내력 / 유도장해) 영역 정합성 |

### 본 채널 권장 (§1.4 책임 — 단일 선택)

**1순위 = 후보 4 (본 결과 commit + push)**. 본 결과 영구 보존 우선. 그 후 후보 1 (item_split_design) 또는 후보 2 (selector_keyword_integrity_design) 사용자 명시 선택.

---

## 9. Claim Boundary 점검

| claim | 본 audit 상태 |
|---|---|
| 26 sample 전수 분류 (A 9 / B 3 / C 6 / D 1 / E 7) | (a) 측정 |
| 정합 20건 A 30% / non-A 70% | (a) 측정 |
| keyword 적중률 (가공전선 28.6% / 이격거리 100% / 가공지선 100%) | (a) 측정 |
| C1+C2+C3 동시 CONFIRMED | (a) 분석 |
| 4 split 후보 + D 통합 권장 | (a) threshold 적용 |
| **policy 실제 수정** | **0** |
| **selector 코드 수정** | **0** |
| **item split 적용** | **0** |
| **37 모집단 전체 확정** | **0** (가공전선 이격거리 26건만 본 audit) |
| **catalog/gap rescue 결정** | **0** |
| **D-4 / A1c** | **0** |
| **generation / audit 재실행** | **0** |

---

## 10. 보호 영역 매트릭스 (전부 미수정 / 0)

`scripts/explanation_synthesizer.py` ✓ / `scripts/v_next_d3_pre_preview.py` ✓ / `scripts/v_next_d3_selector.py` ✓ / `scripts/v_next_d3_input_creator.py` ✓ / `scripts/v_next_d3_parser_validator.py` ✓ / `scripts/v2_input_parser.py` ✓ / `app/data/questions.json` ✓ / D-2 sealed assets ✓ / v_full handoff scope ✓ / policy 수정 0 ✓ / selector 수정 0 ✓ / split 적용 0 ✓ / generation 재실행 0 ✓ / audit 재실행 0 ✓ / catalog/gap/reuse 0 ✓ / D-4 0 ✓ / commit 0 ✓ / DEVLOG / Vault / MEMORY / decision JSONL 작성 0 ✓.

---

## 11. 산출물 (사용자 잘림 영역 — design 정합 추정)

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_b/metadata_policy_review_execution_report.md` | 본 보고서 (11 섹션) |
| `v_next_results_d3_b/metadata_policy_review_execution_report.json` | machine-readable — 26 sample 분류 / 카테고리 분포 / cross-tab / keyword integrity / split 결정 / 원인 가중치 / pathway / 다음 게이트 |

---

## 12. 최종 상태 판정 (잘림 영역 — design 정합 추정)

**판정 (primary)**: `ITEM_SPLIT_RECOMMENDED`
**판정 (secondary)**:
- `SELECTOR_BROAD_MATCH_CONFIRMED`
- `POLICY_DEFINITION_ISSUE_CONFIRMED`

### 판정 근거

| 검증 기준 | 결과 |
|---|---|
| 4 split 후보 모두 ≥3건 threshold 충족 | ✓ |
| "가공전선" kw 적중률 28.6% (broad) | ✓ |
| 정합 20건 A 30% / non-A 70% | ✓ |
| C1+C2+C3 동시 CONFIRMED_HIGH | ✓ |
| C5 sample-only REJECTED | ✓ |

### 대안 옵션 (미해당)

- `DATA_DEBT_DOMINANT`: X 23% < policy issue 70%
- `POLICY_REVIEW_INCONCLUSIVE`: rubric 명확, inconclusive 아님
- `MIXED_CAUSE_FOUND`: C1+C2+C3 동시이나 가장 actionable은 ITEM_SPLIT으로 primary 선정

### 사용자 잘림 영역 결정 필요

| 항목 | 본 채널 추정 | 사용자 명시 필요 영역 |
|---|---|---|
| 산출물 경로 | `v_next_results_d3_b/metadata_policy_review_execution_report.{md,json}` | 정합 추정 |
| 최종 상태 옵션 | design 동일 추정 (위 12개) | 정합 추정 |
| 금지 영역 | design 동일 추정 (policy 수정 0 / selector 0 / commit 0 등) | 정합 추정 |

---

End of metadata policy review execution report (26-sample classification).
