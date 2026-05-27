# Hard Check Policy Design

> 2026-05-27 KST. Post-pre_preview restore 후속.
> 본 보고서는 hard check 정책 **design만** 작성. 실제 코드 수정 / input 재생성 / D-4 자동화 0.

---

## 0. 핵심 한 줄 결론

**`READY_FOR_HARD_CHECK_POLICY_IMPLEMENTATION_GATE`** — C+E 결합 권장 (manifest-shift-aware check + policy_revision mode 분리).

- production mode: strict (fixed 94) 유지 — sealed 영역 보호
- policy_revision mode: manifest-shift-aware — 정책 정교화 허용
- sealed_baseline mode: extra-strict — published baseline 보호

---

## 1. 현재 hard check 분석

### 1.1 input_creator (`scripts/v_next_d3_input_creator.py:310-315`)

```python
if len(main_clean) != 94:
    print(f"ERROR: CLEAN count {len(main_clean)} != 94", file=sys.stderr)
    return 1
if len(catalog) != 51 or len(gap) != 97:
    print(f"ERROR: catalog/gap mismatch catalog={len(catalog)} gap={len(gap)}", file=sys.stderr)
    return 1
```

→ **2 hard checks** (return 1 + ERROR). 전력공학 모집단 242 정합 분류 보장.

### 1.2 parser_validator (`scripts/v_next_d3_parser_validator.py:128, 159-176`)

```python
clean_only_ok = manifest.get("selected_count") == 94
# ...
generated == 94 / parse_pass == 94 / enriched_4_complete == 94 / essence_present == 94 / rep_trap_present == 94
```

→ truthy 측정 (hard fail 아님, 단 94 hardcoded).

---

## 2. Item Split에서 차단된 이유

| 항목 | 값 |
|---|---|
| split 후 CLEAN | 87 |
| input_creator hard check | `len(main_clean) != 94` → ERROR + return 1 |
| 실제 회귀 | 0 (broad keyword 제거 성공, 차단기 영역 영향 0) |
| 실제 manifest shift | 정상 (recoverable 4 + partial 2 + intentional drop 2 + new 1) |
| **false positive 영역** | **YES** — hard check가 정책 정교화 자체를 차단 |

---

## 3. Fixed 94 Check의 한계

| 한계 | 상세 |
|---|---|
| 정책 정교화 차단 | broad keyword 제거 / item split / data debt 분리 등 정합 개선이 CLEAN 수 변화 동반 시 자동 실패 |
| Intentional drop 차단 | data debt sample을 catalog/gap으로 분리하면 CLEAN 감소 — fixed 94 위반 |
| New clean 무시 | 정책 정교화로 신규 CLEAN 진입 (예: 2003_3회_26)이 발생해도 net 변화만 측정 |
| Manifest shift 정합성 측정 불가 | exit/new/recoverable/intentional drop 의미 구분 영역이 hard check에 입력되지 않음 |
| Policy revision 안전 영역 없음 | 정책 실험과 production sealed 영역이 동일 strict mode로 처리 |

---

## 4. 정책 후보 A-E 비교

| ID | 후보 | 장점 | 단점 | 판정 |
|---|---|---|---|---|
| A | fixed 94 유지 | sealed 영역 보호 / 예측 가능 | 정책 정교화 차단 / shift 정상 영역 실패 판정 | production-only mode로 유지 |
| B | expected range (예: 85-100) | 정책 정교화 영역 확보 / 구현 단순 | range 임의 결정 / shift 의미 구분 0 | range만으로는 부족 |
| C | manifest-shift-aware check | exit/new/recoverable 명시 / shift 의미 영역 반영 | check 입력 영역 확장 / 구현 복잡 | **정책 본질에 가장 정합** |
| D | explicit allowed_delta file | 사전 합의 변동 영역 / audit trail 명시 | 사전 작성 필요 / 발견 영역 차단 | revision mode input 활용 가능 |
| E | policy revision mode 분리 | sealed strict 유지 / 정책 mode 별 영역 | mode 전환 결정 영역 필요 | **production safety + 정책 정교화 양립** |

---

## 5. 권장 Hard Check 정책 (단일 추천)

**C+E 결합** — manifest-shift-aware check + policy_revision mode 분리.

### 5.1 Mode 구조 (3종)

| mode | default | check | use case | fail action |
|---|:---:|---|---|---|
| **production** | YES | strict (fixed 94 / catalog 51 / gap 97) | 일반 generation / D-3 baseline / sealed assets | ERROR + return 1 |
| **policy_revision** | NO | manifest-shift-aware (exit/new/recoverable/intentional 명시 시 통과) | split / keyword adjustment / data debt 분리 등 정책 정교화 실험 | shift 미설명 시 ERROR / 설명 시 WARN + 진행 |
| **sealed_baseline** | NO | extra-strict — 기존 manifest 항목 변경 0 강제 | v_full handoff / D-2 sealed / published baseline | ERROR (revision 불가) |

### 5.2 Mode 진입 방법

- CLI flag (예: `--policy-revision`) 또는 환경 변수 (예: `D3_POLICY_REVISION=1`)
- 기본값 = production (mode flag 없으면 strict)

---

## 6. Policy Revision Mode 정의

| 영역 | 명세 |
|---|---|
| Enter conditions | CLI flag 진입 + `manifest_shift_report.json` 입력 + `expected_clean_range` 입력 + `protected_groups` 입력 |
| Exit conditions | 정책 변경 commit 완료 + post-revision audit 통과 + production mode 자동 복귀 |
| Audit trail | 입력 + 결과 + decision은 별 audit log에 기록 |

### 6.1 manifest_shift_report.json 필수 영역

| 영역 | 내용 |
|---|---|
| exit pids | baseline CLEAN → split 비CLEAN list + 각 cause (recoverable / partial / intentional drop / data debt) |
| new pids | baseline 비CLEAN → split CLEAN list + 매칭 keyword |
| delta_total | Δ CLEAN (예: -7) + expected range (예: -10 ~ +10) 안 |
| protected_groups | expansion 57 / 차단기 13 등 보호 영역 회귀 0 확인 |
| catalog_gap_shift | catalog Δ / gap Δ + 설명 |
| broad_keyword_check | broad single-word 재도입 측정 + 의도 broad는 명시 + 인가 |

---

## 7. Manifest-shift-aware Check 조건 (6 category)

| # | category | condition | required |
|---:|---|---|---|
| 1 | exit | baseline CLEAN → 비CLEAN | 각 exit pid의 cause 명시 |
| 2 | new | baseline 비CLEAN → CLEAN | 신규 CLEAN pid + 매칭 keyword 명시 |
| 3 | delta_total | Δ CLEAN | expected range 안 / forbidden broad reintroduction 0 |
| 4 | protected_group | expansion 57 / 차단기 13 | 변경 0 (회귀 0) |
| 5 | catalog_gap_shift | catalog/gap Δ | manifest shift report에 설명 |
| 6 | broad_keyword | broad single-word 재도입 측정 | 0건 / 의도 broad 명시 + 인가 |

---

## 8. Hard Fail / Soft Fail 기준

### 8.1 Hard fail (ERROR + return 1)

| trigger | type |
|---|---|
| protected expansion group 회귀 (차단기 13 또는 expansion 57) | hard fail |
| broad keyword (`가공전선` 등 단일 단어) 재도입 | hard fail |
| sealed baseline mode 위반 | hard fail |
| unexplained CLEAN loss (policy_revision mode 외) | hard fail |

### 8.2 Soft fail (WARN + 진행 허용)

| trigger | type |
|---|---|
| manifest shift 설명 제공 + expected range 안 | soft warn |
| data debt drop (intentional 명시) | soft warn |
| new CLEAN 진입 | soft info |

### 8.3 Input 생성 허용 조건

- CLEAN count 변화가 `manifest_shift_report.json`에 설명
- exit/new pid 목록 제공
- forbidden broad keyword 재도입 0
- protected groups (expansion 57, 차단기 13) 회귀 0
- catalog/gap 이동이 expected range 안
- baseline 보존 경로가 별 디렉토리에 있음

### 8.4 Input 생성 실패 조건

- unexplained CLEAN loss
- protected expansion group 손상
- 차단기 13 영역 회귀
- broad keyword 재도입
- untracked selector drift
- catalog/gap 이동 설명 0

---

## 9. D-4 자동화 재사용 방안

| 항목 | scope |
|---|---|
| subject별 expected range | 전력공학 외 다른 subject도 동일 hard check 구조 → mode 분리 재사용 |
| manifest diff report | subject별 baseline vs new manifest diff 자동 생성 |
| policy revision mode gate | D-4 자동화 시 subject별 정책 정교화 단계 mode 진입 인가 |
| hard fail / soft fail 기준 | 전 subject 공통 적용 — protected group + broad keyword + sealed mode 위반은 hard fail |

---

## 10. Implementation Gate 수정 파일 후보

| 파일 | 변경 영역 | scope |
|---|---|---|
| `scripts/v_next_d3_input_creator.py` | 310-315 (2 hard checks) | fixed 94 strict → mode-aware (production strict / revision relaxed / sealed extra-strict) |
| `scripts/v_next_d3_parser_validator.py` | 128 + 159-176 (truthy checks) | 94 hardcoded → mode-aware truthy |
| `scripts/v_next_d3_pre_preview.py` | (선택) | 0 — manifest shift report 입력 영역 추가 가능 |
| `manifest_shift_report.json` schema | 신규 | exit/new/recoverable/protected/expected_range schema 정의 |

---

## 11. Claim Boundary

| claim | 본 design 상태 |
|---|---|
| 현재 hard check 분석 (input_creator + parser_validator) | (a) 측정 |
| Item split 차단 원인 (fixed 94 false positive) | (a) 분석 |
| fixed 94 한계 5개 분석 | (a) 분석 |
| 5 정책 후보 A-E 비교 | (a) 명세 |
| 권장 정책 C+E 결합 (3 mode 구조) | (a) 명세 |
| Manifest-shift-aware 6 category + allow/fail conditions + hard/soft 기준 | (a) 명세 |
| D-4 자동화 재사용 방안 4 항목 | (a) 명세 |
| Implementation 수정 파일 후보 | (a) 명세 |
| **input_creator 실제 수정** | **0** |
| **parser_validator 실제 수정** | **0** |
| **pre_preview.py 수정 / input 재생성 / generation / audit** | **0** |
| **D-4 자동화 진입** | **0** |
| **policy revision mode 진입 인가 영역 결정** | **0** (사용자 명시 영역) |
| **commit / DEVLOG / Vault / MEMORY / decision JSONL 작성** | **0** |

---

## 12. 보호 영역 매트릭스 (전부 미수정 / 0)

`scripts/v_next_d3_input_creator.py` 수정 0 ✓ / `scripts/v_next_d3_parser_validator.py` 수정 0 ✓ / `scripts/v_next_d3_pre_preview.py` 수정 0 ✓ / `scripts/explanation_synthesizer.py` ✓ / `scripts/v_next_d3_selector.py` ✓ / `app/data/questions.json` ✓ / D-2 sealed assets ✓ / v_full handoff scope ✓ / input 재생성 0 ✓ / generation 재실행 0 ✓ / audit 재실행 0 ✓ / D-4 자동화 실행 0 ✓ / catalog/gap rescue 0 ✓ / commit 0 ✓ / DEVLOG / Vault / MEMORY / decision JSONL 작성 0 ✓.

---

## 13. 산출물

| 파일 | 내용 |
|---|---|
| `v_next_results_d3_split/hard_check_policy_design.md` | 본 design 보고서 (13 섹션) |
| `v_next_results_d3_split/hard_check_policy_design.json` | machine-readable — 현 hard check / 한계 / 5 후보 / 3 mode 구조 / 6 category / hard/soft 기준 / D-4 재사용 / 수정 파일 |

---

## 14. 최종 상태 판정

**판정 (primary)**: `READY_FOR_HARD_CHECK_POLICY_IMPLEMENTATION_GATE`
**판정 (secondary)**: `NEEDS_USER_DECISION_ON_POLICY_REVISION_MODE` (mode 진입 인가 영역)

### 판정 근거

| 검증 기준 | 결과 |
|---|---|
| 현 hard check 정확 위치 측정 (2 input_creator + 5 parser_validator) | ✓ |
| Split false positive 분석 | ✓ |
| 5 정책 후보 비교 + 본질 정합 (C+E) | ✓ |
| 3 mode 구조 (production / policy_revision / sealed_baseline) | ✓ |
| Manifest-shift-aware 6 category + allow/fail conditions | ✓ |
| Hard/soft fail 기준 | ✓ |
| D-4 재사용 4 항목 | ✓ |
| Implementation 수정 파일 후보 | ✓ |

### 대안 옵션 (미해당)

- `NEEDS_HARD_CHECK_POLICY_DESIGN_FIX`: 미해당 — 구조 명확
- `KEEP_STRICT_CHECK_RECOMMENDED`: 미해당 — split 본질 효과 측정 가능, fixed 94 false positive 영역

다음 단계 (mode 구조 implementation + revision mode 진입 인가 결정 + D-4 자동화) 진입은 사용자 명시 영역.

---

End of hard check policy design (design only) report.
