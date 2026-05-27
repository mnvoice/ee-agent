# Item Split Implementation Report

> 2026-05-27 KST. Post-item_split_design 후속.
> 본 보고서는 split 실제 적용 시도 + selector dry-run 측정 결과. **input_creator CLEAN 94 hard check 차단**으로 input 재생성 / synthesizer / post-split metadata audit 0.

---

## 0. 핵심 한 줄 결론

**`ITEM_SPLIT_PARTIAL_WITH_MANIFEST_SHIFT`**.

- pre_preview.py patch 적용 (1 entry → 4 entries)
- selector dry-run 통과 (CLEAN 87 / 4 split items 분포 측정)
- broad keyword `가공전선` 제거 성공 (hits 0)
- **CLEAN 87 != 94** → input_creator hard fail → 재생성 / 측정 차단
- 차단기 영역 (expansion 57) 영향 0 — 회귀 0 ✓
- 26 baseline pid fate: CLEAN 18 / catalog 5 / gap 3
- mismatch 발견 4건 (다른 item kw로 흘러감)

---

## 1. 실제 수정 diff 요약

| 항목 | 값 |
|---|---|
| 파일 | `scripts/v_next_d3_pre_preview.py` |
| 라인 | 237-247 (1 entry) → 237-296 (4 entries + 주석) |
| Before keywords | 7개 (`가공전선`/`이격거리`/`가공지선`/`접지선`/`안테나`/`약전류전선`/`식물 이격`) |
| After 4-split keywords | 총 36개 (narrow multi-word set) |
| Broad keyword `가공전선` | DROPPED (4 item 모두에서 제거) |
| Patch 상태 | applied (commit 0) |

---

## 2. Selector dry-run 결과

| 측정 | 이전 baseline | Post-split | Δ |
|---|---:|---:|---|
| CLEAN total | 94 | **87** | **-7** |
| CLEAN expansion | 57 | 57 | 0 ✓ |
| CLEAN non_expansion_metadata | 37 | 30 | **-7** |
| catalog | 51 | 60 | +9 |
| gap | 97 | 95 | -2 |
| **broad keyword hits** | (있음) | **0** | broad `가공전선` 제거 성공 |

→ selector 자체는 정상 통과. CLEAN 7건 감소 = catalog/gap으로 이동.

---

## 3. baseline 26 pid fate (Split 후)

### 3.1 CLEAN 이동 18건

| pid | post-split item | kw | 정합 |
|---|---|---|:---:|
| 1999_4회_81 | 가공전선 안전율 / 풍압 | 풍압 하중 | ✓ S2 |
| 2000_2회_86 | 가공전선 이격거리 | 이격거리 | ✓ S1 |
| 2000_6회_92 | 가공전선 이격거리 | 이격거리 | ✓ S1 |
| 2001_2회_82 | 가공전선로 경간·이도 | 인장강도 | ✗ mismatch (본 문제 케이블 단면적) |
| 2002_3회_85 | 가공전선로 경간·이도 | 경간 | ✓ (경간 영역 정합) |
| 2004_1회_84 | 가공전선 이격거리 | 이격거리 | ✓ S1 |
| 2004_2회_86 | 가공전선 이격거리 | 이격거리 | ✓ S1 |
| 2004_3회_83 | 가공전선 이격거리 | 이격거리 | ✓ S1 |
| 2006_1회_29 | 가공전선 기타 설비기준 | 가공지선 | ✓ S4 |
| 2006_1회_86 | 가공전선 안전율 / 풍압 | 풍압 하중 | ✓ S2 |
| 2006_2회_86 | 가공전선 안전율 / 풍압 | 풍압 하중 | ✓ S2 |
| 2006_3회_81 | 가공전선 지지물 시설 | 동일 지지물 | ✓ S3 |
| 2006_3회_83 | 가공전선 기타 설비기준 | 가공지선 | ✓ S4 |
| 2007_1회_81 | 가공전선 이격거리 | 이격거리 | ✓ S1 |
| 2007_1회_82 | 가공전선로 경간·이도 | 인장강도 | ✗ mismatch (본 문제 400V 전선 굵기 S4 영역) |
| 2007_2회_27 | 가공전선 기타 설비기준 | 가공지선 | ✓ S4 |
| 2007_2회_81 | 절연내력 / 유도장해 | 통신선 | ✗ mismatch (본 문제 통신선 옥내 시설 S4 영역) |
| 2007_2회_82 | 가공전선로 경간·이도 | 이도 | ✗ mismatch (본 문제 이격/접근 S1 영역, 풀이 부재) |

### 3.2 catalog 5건 (NEEDS_REVIEW)

| pid | item | kw |
|---|---|---|
| 1999_4회_84 | 가공전선 이격거리 | 이격거리 |
| 2003_3회_81 | 차단기 | 차단기 (다른 slot으로 흘러감) |
| 2005_3회_81 | 가공전선 이격거리 | 이격거리 |
| 2006_1회_85 | 가공전선 이격거리 | 이격거리 |
| 2006_2회_83 | 가공전선 이격거리 | 이격거리 |

### 3.3 gap 3건 (no match)

| pid | 사유 |
|---|---|
| 2004_1회_91 | OCR 깨짐 + 풀이 부재 |
| 2004_3회_92 | 풀이 부재 |
| 2007_1회_84 | 본 문제 지선 시설 (S4 D 영역) 인데 split 후 매칭 0 |

### 3.4 종합

| 분류 | 건수 |
|---|---:|
| CLEAN | 18 |
| catalog | 5 |
| gap | 3 |
| absent | 0 |
| **합** | **26** |

---

## 4. CLEAN / catalog / gap 변화

| 영역 | baseline | split | Δ |
|---|---:|---:|---|
| CLEAN total | 94 | 87 | -7 |
| CLEAN expansion | 57 | 57 | 0 |
| CLEAN non_expansion | 37 | 30 | -7 |
| catalog | 51 | 60 | +9 |
| gap | 97 | 95 | -2 |
| total pool | 242 | 242 | 0 |

→ 7건이 CLEAN에서 catalog/gap으로 이동.

---

## 5. expansion / non_expansion_metadata 변화

| 영역 | baseline | split |
|---|---:|---:|
| expansion (차단기 13 포함) | 57 | 57 ✓ |
| non_expansion_metadata | 37 | 30 |

→ expansion 영역 영향 0 — **차단기/P5 신호 보존**.

---

## 6. Parser validation 결과

**NOT_RUN** — input_creator hard block (CLEAN 87 != 94)로 input 재생성 0. parser_validator는 v_next_inputs_d3에 대해 hardcoded이므로 새 input 없이 검증 불가.

---

## 7. Generation 결과

**NOT_RUN** — 동일 사유. v_next_inputs_d3_split 디렉토리는 생성 0 (input 없음). v_next_results_d3_split/ 디렉토리는 본 보고서만 포함.

---

## 8. Post-split metadata audit 결과

**NOT_RUN** — 동일 사유. selector dry-run 측정값만 보고 (split distribution + 26 fate + mismatch 발견).

---

## 9. 기존 misleading 개선 여부

**측정 불가 (audit not run)**. 단 selector dry-run 결과로 다음 추정 가능:
- S1 (이격거리) 정합 매칭 6건 — narrow keyword로 정합
- S2 (안전율/풍압) 정합 매칭 3건 — narrow keyword로 정합
- S3 (지지물 시설) 정합 매칭 1건 — narrow keyword가 좁아 1/6만 매칭 (개선 부족)
- S4 (기타 설비기준) 정합 매칭 3건 — narrow keyword 일부만 매칭 (3/8)
- mismatch 4건 — 다른 item kw로 흘러감 (split 외 정합성 영향)

→ split design의 S3 + S4 keywords가 좁아서 일부 sample이 catalog/gap으로 이동. design 재조정 영역.

---

## 10. 차단기 / P5 영역 회귀 여부

| 검증 항목 | 결과 |
|---|---|
| CLEAN expansion 57 / 57 | 유지 ✓ |
| 차단기 13건 영역 영향 | 0 ✓ |
| P5 positive signal | 보존 ✓ |
| Split 외 slot (송배전D / 안정도D / 변환본질4 / 함정S / 보호고장S) | 영향 0 ✓ |
| 단 다른 설비고장 item (경간·이도 +4 / 절연내력 +1) | mismatch sample 이동 |

→ 차단기/P5 영역 회귀 **0**. 단 mismatch 4건 다른 item으로 이동은 회귀 아님 (split 외 정합성 영향, 선택적 audit 영역).

---

## 11. data debt 6건 처리 결과

| pid | fate | data debt |
|---|---|---|
| 1999_4회_84 | catalog | OCR/풀이 mismatch |
| 2000_6회_92 | CLEAN (S1) | 풀이 부재 |
| 2004_1회_91 | gap | OCR 깨짐 + 풀이 부재 |
| 2004_3회_92 | gap | 풀이 부재 |
| 2006_1회_85 | catalog | 풀이 부재 |
| 2007_2회_82 | CLEAN (경간·이도 mismatch) | 풀이 부재 |

| 분류 | 건수 |
|---|---:|
| CLEAN with data debt | 2 |
| catalog with data debt | 2 |
| gap with data debt | 2 |

→ data debt 6건이 CLEAN / catalog / gap 3 영역 모두 분산. 별 bucket 0, split item 내부 flag 분리.

---

## 12. Input_creator Hard Block 분석

| 영역 | 값 |
|---|---|
| Trigger | `scripts/v_next_d3_input_creator.py:310-312` — `if len(main_clean) != 94: ERROR ... return 1` |
| Split CLEAN | 87 |
| Shortfall | 7 (94 → 87) |

### 12.1 진행 옵션 분석

| Option | 내용 | 결정 |
|---|---|---|
| A. input_creator hard check 완화 | 사용자 명시 0 — 수정 금지 영역 | REJECTED |
| B. split design 재조정 (keywords 확대로 7건 회복) | design 재검토 영역 | DEFERRED |
| C. baseline 복원 + split 원상복구 | 진행 영역 (선택적) | DEFERRED |
| **D. pre_preview.py 보정 유지 + 측정 결과만 보고 + 사용자 명시 분기 영역으로 처리** | 본 게이트 선택 | **SELECTED** |

### 12.2 선택 근거

사용자 명시 분기: "catalog/gap 이동이 있으면 실패로 단정하지 말고 별도 측정값으로 보고". `ITEM_SPLIT_PARTIAL_WITH_MANIFEST_SHIFT` 정합.

---

## 13. 현재 상태

| 영역 | 상태 |
|---|---|
| `scripts/v_next_d3_pre_preview.py` | patch_applied (4 entries) — 사용자 결정 후 원상복구 또는 design 재조정 영역 |
| `v_next_inputs_d3/` | baseline 그대로 보존 (input_creator hard fail로 write 0) |
| `v_next_inputs_d3_b/` | 차단기 split B 결과 보존 (이전 commit) |
| `v_next_inputs_d3_baseline_split_round/` | 본 게이트 backup (정합 확인 후 정리 가능) |
| `v_next_results_d3_split/` | 본 보고서 + JSON 만 포함 (generation 0) |

---

## 14. Claim Boundary

| claim | 본 게이트 상태 |
|---|---|
| selector dry-run 결과 (CLEAN 87 / 4 split items 분포) | (a) 측정 |
| 26 baseline pid fate (CLEAN 18 / catalog 5 / gap 3) | (a) 측정 |
| 차단기 expansion 57 보존 (영향 0) | (a) 측정 |
| broad keyword hits 0 | (a) 측정 |
| mismatch 4건 (다른 item으로 흘러감) | (a) 측정 |
| pre_preview.py 4 entries patch 적용 | (a) 측정 |
| Parser validation 결과 | **N/A (NOT_RUN)** |
| Generation 결과 | **N/A (NOT_RUN)** |
| Post-split metadata audit | **N/A (NOT_RUN)** |
| Misleading 개선 측정 | **0** (audit 차단) |
| Split의 본질적 효과 검증 | **부분 측정** (모집단 변동 측정만, semantic 효과 0) |
| **input_creator hard check 완화 결정** | **0** (사용자 명시 영역) |
| **split design 재조정 결정** | **0** (별 게이트) |
| **pre_preview.py 원상복구 결정** | **0** (사용자 명시 영역) |

---

## 15. 보호 영역 매트릭스

| 보호 대상 | 상태 |
|---|---|
| `scripts/explanation_synthesizer.py` | 미수정 ✓ |
| `scripts/v_next_d3_selector.py` | 미수정 ✓ |
| `scripts/v_next_d3_input_creator.py` | 미수정 ✓ |
| `scripts/v_next_d3_parser_validator.py` | 미수정 ✓ |
| `scripts/v2_input_parser.py` | 미수정 ✓ |
| `app/data/questions.json` | 미수정 ✓ |
| D-2 sealed assets | 미수정 ✓ |
| v_full handoff scope | 미수정 ✓ |
| catalog/gap rescue | 0 ✓ |
| D-4 진입 | 0 ✓ |
| commit | 0 ✓ |
| DEVLOG / Vault / MEMORY / decision JSONL 작성 | 0 ✓ |
| **scripts/v_next_d3_pre_preview.py** | **patch_applied** (split implementation 본질 — design 영역) |

---

## 16. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_split/item_split_implementation_report.md` | 본 보고서 (16 섹션) |
| `v_next_results_d3_split/item_split_implementation_report.json` | machine-readable — 모든 측정값 / 26 pid fate / mismatch / data debt / hard block 분석 / 옵션 |

---

## 17. 최종 상태 판정

**판정**: `ITEM_SPLIT_PARTIAL_WITH_MANIFEST_SHIFT`

### 판정 근거

| 검증 기준 | 결과 |
|---|---|
| selector dry-run으로 split 적용 가능 측정 (CLEAN 87 / 4 items) | ✓ |
| input_creator CLEAN 94 hard check 차단 (input 재생성 0) | ✓ |
| catalog/gap 변동 +9/-2 (manifest shift 발현) | ✓ |
| 차단기/P5 영역 영향 0 | ✓ |
| broad keyword hits 0 | ✓ |
| mismatch 4건 + 다른 item 이동 8건 | ✓ |
| data debt 6건 분산 측정 | ✓ |

### 대안 옵션 (미해당)

- `ITEM_SPLIT_IMPLEMENTED_AND_VERIFIED`: 미해당 — input 재생성 / parser / generation / audit 차단으로 verified 불가
- `ITEM_SPLIT_REGRESSION_FOUND`: 미해당 — 차단기/P5 영역 영향 0
- `BLOCKED_BY_SELECTOR_MANIFEST_CHANGE`: 미해당 — selector 자체는 정상 dry-run 통과, manifest 변동만

### 다음 결정 영역 (사용자 명시 게이트)

| # | 후보 | scope |
|---:|---|---|
| 1 | pre_preview.py 원상복구 + split policy 폐기 | 본 게이트 결과 기록만 |
| 2 | split design 재조정 (S3/S4 keywords 확대로 7건 회복 design) | design 재검토 영역 |
| 3 | input_creator hard check 완화 정책 design | 사용자 명시 코드 수정 결정 영역 |
| 4 | 본 결과 commit + push (pre_preview.py patch + 보고서) | 사용자 결정 영역 |
| 5 | mismatch 4건 + 다른 item 이동 8건 별 audit | 별 게이트 |
| 6 | 본 결과를 reflection로 보존 + 다른 영역 진입 (D-4 등) | 사용자 결정 |

---

End of item split implementation report (PARTIAL_WITH_MANIFEST_SHIFT).
