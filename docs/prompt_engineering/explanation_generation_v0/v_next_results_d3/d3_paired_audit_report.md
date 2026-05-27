# v_next D-3 Paired Audit Report

> 2026-05-27 KST. v_next D-3 paired audit 4차원 분리.
> D-3 generation 완료 / D-3 paired audit (본 보고서) / P5 0 / D-4 0 / catalog rescue 0 / commit 0.
> 본 보고서는 측정 결과 기록. semantic gain claim / 242 improved claim / expansion 57 전체 회복 claim / D-4 진입 필요 claim 모두 0.

---

## 0. 핵심 한 줄

`44 dl_keyword / 50 empty`를 `57 expansion / 37 non_expansion_metadata`와 join한 결과:
- empty 50 = **expansion 13 (unexpected) + non_expansion_metadata 37 (정상)** — 사용자 가설 정확.
- unexpected 13건은 **단일 item "차단기" / 단일 slot_grp "전력_보호고장S" / 단일 dl "전력 차단기 -> 회로 단락전류 / 임피던스 환산"** 일점 집중.
- 즉 expansion 그룹의 일반적 실패가 아니라 **차단기 keyword에 한정된 매핑 미발현**.

---

## 1. 4차원 분리 매트릭스

### 1.1 Join table (audit_group × expansion_source)

| audit_group | dl_keyword | empty | MISSING | total |
|---|---:|---:|---:|---:|
| expansion | 44 | 13 | 0 | **57** |
| non_expansion_metadata | 0 | 37 | 0 | **37** |
| TOTAL | **44** | **50** | 0 | **94** |

### 1.2 4차원 paired CSE status (v_full → D-3)

| (audit_group, expansion_source) | CSE 변화 | 건수 | 해석 (claim boundary 준수) |
|---|---|---:|---|
| (expansion, dl_keyword) | empty → non | 44 | mechanical: expansion 부착 성공. semantic gain claim 0. |
| (expansion, empty) | empty → empty | 13 | mechanical: expansion 미부착. 다음 수리 후보 식별 대상. |
| (non_expansion_metadata, empty) | empty → empty | 37 | 정상. expansion 부착 의도 자체가 없는 metadata 평가 영역. |

### 1.3 4차원 구분 진술

- **paired generated 94 (본 audit 범위)**: v_full과 problem_id 매핑 paired 비교 완료.
- **unpaired baseline 148 (catalog 51 + gap 97 중 D-3 미선정 영역)**: improvement claim 금지. baseline-only.
- **expansion group 57**: dl_keyword 44 (mechanical 부착) + empty 13 (단일 item 차단기 미부착).
- **non_expansion_metadata group 37**: 정상 empty. expansion 실패 해석 금지.

---

## 2. Unexpected expansion-empty 13건 (수리 후보 영역)

### 2.1 일점 집중 패턴

전부 동일 5축 매핑:

| 축 | 값 |
|---|---|
| `audit_group` | expansion |
| `slot_grp` | 전력_보호고장S |
| `item` | 차단기 |
| `matched_keyword` | 차단기 |
| `enriched_dynamic_link` | `전력 차단기 -> 회로 단락전류 / 임피던스 환산` |

### 2.2 13건 명단

| input | pid |
|---|---|
| input_003.md | 1998_4회_22 |
| input_012.md | 2000_2회_23 |
| input_029.md | 2001_3회_81 |
| input_030.md | 2002_1회_22 |
| input_035.md | 2002_3회_26 |
| input_040.md | 2003_1회_23 |
| input_041.md | 2003_1회_27 |
| input_047.md | 2004_1회_90 |
| input_056.md | 2004_3회_27 |
| input_057.md | 2004_3회_29 |
| input_058.md | 2004_3회_82 |
| input_063.md | 2005_1회_29 |
| input_092.md | 2008_1회_23 |

### 2.3 분류 가설 후보 (claim 0 — 다음 게이트 결정 영역)

본 보고서는 분류 후보 3종을 열거할 뿐 단일 결론 주장 안 함. P5 sample experiment 또는 generator keyword map 측정 후 결정 영역.

| 후보 | 내용 | 검증 방법 |
|---|---|---|
| A. generator keyword map 누락 | "차단기" item이 cross_subject_expansion 생성 단계의 keyword/concept map에 등록되어 있지 않음 | generator 내부 keyword map (read-only) 직접 측정 — explanation_synthesizer.py + system_prompt.md 검토 |
| B. dl_keyword 표현 문제 | dl "전력 차단기 -> 회로 단락전류 / 임피던스 환산"의 split/parse가 generator 룰과 불정합 (예: `/` 구분, 다중 target) | dl 표현 정규화 + 1건 재실행 (별 게이트) |
| C. 정책상 정상 empty | 차단기 영역은 generator 측에서 의도적으로 cross_subject 제외 | 정책 문서 / generator decision_records 검토 |

claim boundary: 위 3 후보 중 어느 것이 정답인지 본 보고서 단계에서 결정 0. P5 / D-4 / generator audit 게이트 별 진입 후 결정.

---

## 3. candidate_pool_small 22건 분포 (관찰 only)

### 3.1 audit_group × expansion_source 분포

| 차원 | 분포 |
|---|---|
| audit_group | expansion 11 / non_expansion_metadata 11 (균등) |
| expansion_source | dl_keyword 11 / empty 11 (균등) |

→ candidate_pool_small flag는 audit_group / expansion_source에 편중되지 않음.

### 3.2 slot_grp 분포

| slot_grp | 건수 |
|---|---:|
| 전력_보호고장S | 8 |
| 전력_설비고장 | 7 |
| 전력_함정S | 4 |
| 전력_송배전D | 3 |

### 3.3 item top

| item | 건수 |
|---|---:|
| 지락·중성점 접지 | 4 |
| 단락전류·임피던스 | 4 |
| 가공전선로 경간·이도 | 4 |
| 부하율·수용률·부등률 | 3 |
| 코로나 / 전선 도체 | 3 |
| 절연내력 / 유도장해 | 3 |
| 역률 개선 | 1 |

claim boundary: candidate_pool_small는 generator의 후보군 부족 신호. semantic quality claim 0. 별 audit (related_problems 후보군 측정) 영역.

---

## 4. Paired comparison (n=94, v_full ↔ D-3 동일 problem_id)

### 4.1 paired coverage

- D-3 rows: 94
- v_full pair found: 94 / 94
- missing pair: 0

### 4.2 7 dimension 측정값

| dimension | 측정값 | 해석 (claim 0 영역) |
|---|---|---|
| cross_subject_expansion status (v_full → D-3) | empty→empty 50 / empty→non 44 | v_full은 paired 94 전부 empty. D-3가 44건 신규 부착. semantic 가치 claim 0. |
| phenomenon 길이 delta (D-3 − v_full) | mean -2.69 / min -60 / max +40 | 평균 D-3가 약간 더 짧음. specificity 평가 영역 아님. |
| trap_pattern 길이 delta | mean -12.99 / min -35 / max +7 | D-3가 평균 13자 짧음. quality claim 0 (길이 ≠ 품질). |
| distractor specificity (D-3 − v_full) | mean +0.37 / min 0.0 / max 1.0 | D-3 distractor 282개 전부 `input.trap_type` 기반. v_full은 "수치/단위 차이 함정" 일반화. mechanical 차이. |
| uncertainty change | same 72 / more_flags 22 / cleaner 0 | D-3가 v_full보다 더 많은 flag 발생 (candidate_pool_small 22건 신규). |
| self_corrections | D-3 0 / v_full 0 | 동일. |
| related same_core count delta | mean -0.60 / min -5 / max 0 | D-3가 평균 0.6건 적음 (max 0 = D-3가 v_full 초과 안 함). |

### 4.3 측정 vs claim 분리 (CONSTITUTION §1.6 (바))

- mechanical 측정값: 위 7 dimension은 자동 측정 결과.
- semantic gain claim: 본 보고서에서 0. 텍스트 1건씩 사람 검토 또는 P5 sample experiment 후 별 게이트 결정.
- 즉 "distractor specificity +0.37"은 (a) 측정. "D-3 distractor 품질 개선"은 (c) 추정 — claim 0.

---

## 5. claim boundary 점검 매트릭스

| claim | 본 보고서 상태 |
|---|---|
| D-3 generation 94 mechanical PASS | (a) 측정 — `schema PASS 94`, `FAIL 0`, `parser contamination 0` |
| 44건 신규 cross_subject_expansion 부착 | (a) 측정 — paired empty→non 44 |
| expansion 57 전체 회복 | **claim 0** — 13건 unexpected empty 미부착 |
| 242 improvement | **claim 0** — paired 94만 측정, unpaired 148은 baseline-only |
| non_expansion_metadata 37 expansion 실패 | **claim 0** — 정상 empty, expansion 의도 자체가 없음 |
| semantic gain (distractor / phenomenon / trap_pattern 품질) | **claim 0** — 측정값만 기록, 의미 평가 별 게이트 |
| P5 필요 | **claim 0** — 본 보고서 다음 사용자 명시 게이트 |
| D-4 진입 필요 | **claim 0** — 본 보고서 다음 사용자 명시 게이트 |
| catalog/gap 회수 필요 | **claim 0** — unpaired 148 영역, 별 게이트 |

---

## 6. 4차원 audit 종합 요약

### 6.1 paired generated 94 (본 audit 범위)

- mechanical PASS: 94/94 (D-3 generation)
- v_full pair 매칭: 94/94
- cross_subject_expansion 신규 부착: 44/94 (47%)
- cross_subject_expansion 미부착: 50/94 (53%) = 정상 37 + unexpected 13

### 6.2 unpaired baseline 148

- improvement claim **0**
- D-3 generation 영역 밖
- catalog 51 + gap 97 중 D-3 미선정. baseline-only.

### 6.3 expansion group 57

- mechanical 부착 44/57 (77%)
- unexpected 미부착 13/57 (23%) — 전부 차단기
- semantic gain claim **0** — 측정값만

### 6.4 non_expansion_metadata group 37

- 전부 empty (정상)
- expansion 부착 의도 자체가 없음
- expansion 실패 해석 금지
- metadata quality 평가 영역 (별 audit 영역)

---

## 7. 산출물

본 audit가 생성한 파일 (read-only generator/parser, sealed assets 미수정):

| 파일 | 내용 |
|---|---|
| `v_next_results_d3/d3_paired_audit_report.md` | 본 보고서 |
| `v_next_results_d3/d3_paired_audit_join.json` | 94 rows × (input, pid, audit_group, expansion_source, slot_grp, item, kw, dl, v_full_pair, 측정 proxies) + 13 unexpected list + 22 candidate_pool_small list |
| `v_next_results_d3/d3_paired_audit_pairs.json` | 94 paired rows × (CSE status, phenomenon_len, trap_pattern_len, distractor_specificity, uncertainty_flags, related_same_core) + 7 dimension delta 요약 |

---

## 8. 보호 영역 매트릭스

| 보호 대상 | 상태 |
|---|---|
| D-2 sealed assets | 미수정 ✓ |
| v_full handoff scope | 미수정 ✓ |
| `app/data/questions.json` | 미수정 ✓ |
| `scripts/explanation_synthesizer.py` | 미수정 ✓ |
| `scripts/v2_input_parser.py` | 미수정 ✓ |
| D-3 generator 재실행 | 0 ✓ |
| P5 patch | 0 ✓ |
| P5 sample experiment | 0 ✓ |
| D-4 진입 | 0 ✓ |
| catalog/gap rescue | 0 ✓ |
| keyword expansion | 0 ✓ |
| reuse tranche | 0 ✓ |
| commit | 0 ✓ |

---

## 9. 다음 결정 후보 (사용자 명시 게이트 영역)

claim 0. 후보 열거만.

| 후보 | 내용 | 게이트 |
|---|---|---|
| 후보 1 | unexpected 13건 차단기 dl 매핑 누락 원인 측정 (generator keyword map / system_prompt 검토, read-only) | 별 사용자 명시 게이트 |
| 후보 2 | candidate_pool_small 22건 generator 후보군 부족 측정 | 별 사용자 명시 게이트 |
| 후보 3 | paired semantic gain 사람 sampling 검토 (P5 sample experiment) | 별 사용자 명시 게이트 |
| 후보 4 | catalog 51 / gap 97 (unpaired 148) baseline 별 audit | 별 사용자 명시 게이트 |
| 후보 5 | non_expansion_metadata 37 metadata quality 별 평가 | 별 사용자 명시 게이트 |

---

## 10. 최종 판정

**판정**: `READY_FOR_D3_POST_AUDIT_BRANCH_DECISION`

- ✓ D-3 generation 94 mechanical PASS 확인
- ✓ 4차원 분리 측정 완료 (44 dl / 13 unexpected / 37 정상)
- ✓ 일점 집중 패턴 식별 (차단기 단일 item)
- ✓ paired comparison 7 dimension 측정 완료
- ✓ claim boundary 엄수 (semantic gain / 242 improved / D-4 / P5 / catalog 회수 claim 0)

semantic gain 평가 / 다음 수리 분기 / P5 / D-4 / catalog 회수는 본 보고서 다음 별 사용자 명시 게이트에서 결정.

---

End of v_next D-3 paired audit report.
