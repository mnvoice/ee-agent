# Trap-Map B-Priority — 2020 Session Namespace E6 Separability Re-Evaluation (2026-05-25)

E6 — separability re-evaluation. 직전 separability evaluation (`d9b2efd`,
`DR-TRAP-GIGI17-66ITEM-SEPARABILITY`)의 5 layer (Q1·Q2 / Q3 / Q4 / Q5 / Q6)
결론을 E1~E5 evidence chain으로 재평가한다.

이번 단계는 **docs-only re-evaluation**. **app/data, questions.json, per-year
json, PDF filename, pdf_pages, app code, 어떤 파일도 수정하지 않는다.** missing
29 recovery / Batch migration / resolver implementation / registry framing
확장 모두 실행 금지. push 없음. amend/rebase/reset 없음. 기기-17 caution 유지.
q52 단독 id 재발급 금지 유지 (영구 invariant 승격 영역). registry row promotion
금지 유지.

- 직전 separability evaluation: `docs/audit/trap_map_B_priority_gigi_17_66item_separability_evaluation_2026-05-25.md` (`DR-TRAP-GIGI17-66ITEM-SEPARABILITY`)
- 관련 E1 source audit: `docs/audit/trap_map_B_priority_2020_1_2_66item_E1_source_audit_2026-05-25.md`
- 관련 E2 record-PDF mapping: `docs/audit/trap_map_B_priority_2020_1_2_66item_E2_record_pdf_mapping_audit_2026-05-25.md`
- 관련 missing 29 recovery: `docs/audit/trap_map_B_priority_2020_1_2_66item_missing29_recovery_evaluation_2026-05-25.md` (`DR-TRAP-2020-12-MISSING29-DATA-DEBT`)
- 관련 E3 namespace conflict: `docs/audit/trap_map_B_priority_2020_1_vs_2020_1_2_conflict_audit_2026-05-25.md`
- 관련 E5 app key impact: `docs/audit/trap_map_B_priority_2020_session_namespace_E5_app_key_impact_2026-05-25.md`
- 관련 registry artifact review: `docs/audit/trap_map_B_priority_gigi_17_alias_registry_artifact_review_2026-05-25.md` (PASS 12/12)
- 관련 App/data decision: `docs/audit/trap_map_B_priority_gigi_17_app_data_decision_2026-05-25.md` (`DR-TRAP-GIGI17-APPDATA-DECISION`)
- 관련 runtime resolver design review: `docs/audit/trap_map_B_priority_gigi_17_runtime_resolver_design_review_2026-05-25.md`
- 관련 66항 session-label policy: `docs/audit/trap_map_B_priority_2020_1_2_66item_session_label_policy_2026-05-25.md` (`DR-TRAP-2020-12-66ITEM-SESSION-LABEL-POLICY`)
- new decision id: `DR-TRAP-GIGI17-SEPARABILITY-REEVAL`

---

## 1. Evidence Chain 요약 (E1~E5)

| evidence | 핵심 결과 | separability 영향 |
|---|---|---|
| **E1** PDF source audit (5c1fecc) | 합본 시험 명시, 1회/2회 분리 단서 0, split policy 부적합 확정 | Q5 Batch migration inseparable 강화, Q6 split 영역 부재 |
| **E2** record-PDF mapping (5f1c9c5) | per-year ↔ master 100% 정합, missing 29 = source exists data missing | Q1·Q2 separable 유지, missing 29 별 영역 활성 |
| **missing 29 recovery** (02c985c) | 별 data recovery debt 분리 결정 | q52 separability 영향 0 (별 트랙 분리 확정) |
| **E3** namespace conflict (b7b2b0b) | 66/66 systemic conflict, q52는 isolated 아닌 systemic 1 사례 | q52 단독 재발급 영구 부적합, Batch migration scope 5 영역 |
| **E5** app key impact (dac6121) | app key namespace collision-free, alias-only resolver가 가장 안전, q52 단독 재발급 3 차원 부적합 강화 | Q1·Q2·Q3·Q5 갱신 입력, q52 invariant 승격 권고 |

---

## 2. 5 Layer Re-Evaluation (Q1~Q6)

### 2.1 Q1·Q2 — Registry artifact creation/review

**직전 결론** (d9b2efd): **Separable**.

**E6 갱신 결론**: **Separable 강화**.

| 갱신 영역 | 입력 evidence |
|---|---|
| registry artifact 9868f95는 q52 candidate row 1건만 | 변경 없음 (E2 / E3 / E5 재확인) |
| registry artifact review PASS 12/12 (f0b462c) | baseline 유지 |
| q52 row가 66항 normalize 0 | E1 + E3 재확인 |
| **app key 영역 0 변경** | **E5 §6 강화** (qId / IndexedDB / DOM / lookup / filter / pdfPageIndex 모두 separable) |
| registry artifact가 systemic framing 확장 가능성 활성화 | E3 §5.3 (단 확장 실행은 별 명시 승인 영역) |

→ Q1·Q2는 **Separable 강화**. registry artifact creation/review는 app key 영역과
완전 분리 가능 (E5 §6) + 66항 systemic policy 영역과 완전 분리 가능 (E2 +
missing 29 별 트랙 분리).

### 2.2 Q3 — App/data decision

**직전 결론** (d9b2efd): **Partial Separable** (decision 범위 한정 시).

**E6 갱신 결론**: **Refined Partial Separable** — 영역별 분리 명시화.

| 영역 | 갱신 separability |
|---|---|
| **alias-only / read-path resolver** | **Separable** (E5 §6 모든 app key 0 변경 가능) |
| docs-only registry 유지 (App/data decision 후보 A) | Separable (현재 active) |
| runtime resolver design review (별 트랙 docs-only) | Separable (E5 §6 강화) |
| **app data alias registry (후보 C)** | **Inseparable 강화** (E5 §10 — persisted data 영역 영향) |
| **record metadata field (후보 D)** | **Inseparable 강화** (E5 §10 + 100 records mis-label 영역 연동) |
| **persisted user data migration** | **Inseparable 강화** (E5 §5 mapping granularity 5 영역) |

→ Q3은 *별 영역 분리*가 명확화됨. **alias-only / read-path resolver 영역은
separable**, 나머지 app data 변경 영역은 inseparable.

### 2.3 Q4 — Caution release review

**직전 결론** (d9b2efd): **Inseparable**.

**E6 갱신 결론**: **Inseparable 유지** (input 영역 변경 0).

| input 영역 | 상태 |
|---|---|
| 본 separability evaluation 결과 | 유지 (E6 = 갱신본) |
| 별 systemic session-label policy 결정 | 66항 policy = **defer 유지** (df7e932) → input 미충족 영역 유지 |
| user-facing impact evidence | 부재 유지 (runtime resolver design review §1.6 명시) |
| redryrun evidence | 부재 유지 |

추가 invariant (E6 결정):
- missing 29 recovery 별 트랙은 caution release input에 포함되지 않음 (q52 separability 영향 0)
- E1~E5 evidence는 *evidence 영역 강화*만, caution release 자격 변경 0

→ Q4은 **Inseparable 유지**. caution release 차단 영역 영구.

### 2.4 Q5 — Batch migration

**직전 결론** (d9b2efd): **Inseparable** (66항 policy 선결 조건).

**E6 갱신 결론**: **Inseparable 강화 — 영구 분리 불가**.

| 차단 차원 | 입력 evidence |
|---|---|
| 66항 policy 선결 조건 | defer 유지 (df7e932) |
| split policy 부적합 확정 | E1 + E3 (66/66 systemic conflict로 split 영역 부재) |
| mapping granularity 5 영역 요구 | E5 §5 (100 records mapping + 66 coexistence + user data + DOM + pdfPageIndex) |
| persisted user data migration 영역 | E5 §10 inseparable |
| 100 records 전수 source claim evidence 부재 | impact audit §1 가설 강화 (E3 §6) |

→ Q5은 **Inseparable 강화**. 단순 systemic 차단이 아니라 **다중 영역 (5+ layer)의
systemic 분리 불가 영역**. 영구 차단 영역 유지.

### 2.5 Q6 — 별 systemic session-label policy

**직전 결론** (d9b2efd): **별 문서 필요**.

**E6 갱신 결론**: **별 문서 필요 + defer 유지** (66항 policy = defer with evidence
requirements, df7e932).

| 영역 | 상태 |
|---|---|
| 66항 policy 결정 | **defer 유지** |
| evidence requirement | E1·E2·E2-A (missing 29)·E3·E5 충족 + E4·외부 source·재evaluation 잔존 |
| split policy 부적합 확정 | E1 + E3 + 본 E6 |
| missing 29 별 트랙 분리 | 본 E6 확정 (q52 separability 영향 0) |

→ Q6은 **별 문서 필요 + defer 유지**. evidence requirement 영역 진행 중.

---

## 3. q52 단독 storage_id 변경 — Permanent Invariant 승격

### 3.1 승격 결정

**결정**: q52 단독 storage_id 변경 금지를 **permanent invariant**로 승격한다.

### 3.2 승격 근거

| 근거 | source |
|---|---|
| systemic 1 사례 확정 (q52는 isolated 아님) | E3 §5.2 |
| 3 차원 부적합 (persisted data + namespace asymmetry + framing 부정합) | E5 §4.2 (A1·A2·A3) |
| split policy 부적합 확정 (별 사례로 처리할 source 부재) | E1 + E3 |
| 100 records mis-label 가능성 (단독 변경 = systemic inconsistency 영구화) | impact audit §1 + N1 audit 강화 |

### 3.3 Invariant 양식

```
INVARIANT (permanent):
  q52 storage_id = `2020_1회_52` 영구 유지.
  단독 storage_id 변경 = 금지.
  변경 가능 영역 = canonical_source_id (citation display 전용, alias-only).
```

### 3.4 Invariant 영향 영역

| 영역 | invariant 적용 |
|---|---|
| registry artifact (9868f95) | q52 row의 storage_id 영구 보존 |
| runtime resolver design (6ac1a9b) | qId / IndexedDB / DOM 모두 storage_id 유지 영역 영구 강화 |
| App/data decision (9c1d387) | 후보 B 구현 시점에도 storage_id 변경 금지 |
| Batch migration | q52 storage_id 단독 변경 0 — 별 mapping granularity 영역에서만 |
| 100 records alias 확장 (별 트랙) | q52 row 단독 처리 금지, systemic mapping으로만 진입 |

### 3.5 Invariant 해제 조건

**해제 불가** (permanent). 단:
- systemic 100 records mapping이 별 명시 승인 + 다중 evidence + persisted user
  data migration 통과 후 진입 시, *systemic mapping의 1 사례로* q52 storage_id가
  같이 이동 가능 (단독 변경 영역 아님)

→ 단독 변경 영역에서는 *영구 금지*. systemic 영역에서만 *별 mapping granularity*
범위로 처리.

---

## 4. missing 29 Data Debt — q52 Separability 영향 재확인

**E6 결론**: missing 29 data debt = q52 separability 영향 **0** (별 트랙 분리
확정).

| 영역 | 영향 |
|---|---|
| q52 row 자체 | 영향 0 (q52는 per-year present, missing 영역 외) |
| q52 alias registry framing | 영향 0 (missing 29는 별 cause 영역) |
| App/data decision direction | 영향 0 |
| runtime resolver design | 영향 0 |
| caution release input | missing 29는 *input 영역에 포함되지 않음* (E6 확정) |
| 66항 policy defer | 영향 0 (별 트랙) |
| Batch migration | 영향 0 (별 cause 영역) |

→ missing 29 recovery (`DR-TRAP-2020-12-MISSING29-DATA-DEBT`)는 q52 separability
framework에 대해 **완전 외부 영역**. 본 E6에서 재확인.

---

## 5. 10 Question 답

### Q1 — q52 registry artifact creation/review는 66항 systemic policy와 여전히 separable?

**A**: **Yes — Separable 강화** (§2.1).

E1·E2·E3·E5 모두 q52 row의 systemic policy 독립성을 강화.

### Q2 — q52 app/data decision은 어떤 범위에서 separable?

**A**: **Refined Partial Separable** (§2.2).

- alias-only / read-path resolver = **Separable**
- docs-only registry 유지 = Separable (현재 active)
- runtime resolver design review = Separable
- app data alias registry / record metadata field / persisted user data migration
  = **Inseparable**

### Q3 — read-path citation resolver design은 separable?

**A**: **Yes — Separable 강화** (§2.2 + E5 §6).

qId (3 위치) / IndexedDB (3 stores) / DOM (4 영역) / lookup (4 영역) /
filterByIds (3 file) / pdfPageIndex (2 영역) **모두 0 변경 가능**.

### Q4 — app/data registry, record metadata field, Batch migration은 inseparable?

**A**: **모두 Yes — Inseparable** (§2.2 + §2.4).

| 영역 | 사유 |
|---|---|
| app data alias registry | E5 §10 persisted data 영역 영향 |
| record metadata field | E5 §10 + 100 records mis-label 영역 연동 |
| Batch migration | E5 §5 mapping granularity 5 영역 + 66항 policy 선결 |

### Q5 — caution release는 여전히 inseparable?

**A**: **Yes — Inseparable 유지** (§2.3).

input 4 영역 (separability evaluation 결과 + 별 systemic policy + user-facing
impact + redryrun) 중 *66항 policy = defer 유지*로 input 미충족 영역 영구.

### Q6 — missing 29 data debt가 q52 separability에 미치는 영향은 0?

**A**: **Yes — 영향 0** (§4).

missing 29는 별 cause 영역 + 별 트랙 분리 확정 + caution release input 영역 외.

### Q7 — q52 단독 storage_id 변경 금지를 permanent invariant로 승격할지?

**A**: **Yes — Permanent Invariant 승격** (§3).

승격 근거: systemic 1 사례 확정 + 3 차원 부적합 + split 부적합 + mis-label
가능성.

invariant 양식: q52 storage_id = `2020_1회_52` 영구 유지. 변경 가능 영역 =
canonical_source_id (citation display 전용, alias-only).

### Q8 — 66항 policy defer 상태를 유지할지?

**A**: **Yes — defer 유지** (§2.5).

evidence requirement 충족 영역 진행 중 (E1·E2·E2-A·E3·E5 충족 / E4·외부
source·재evaluation 잔존).

### Q9 — 다음 gate는 q52 본류에서는 무엇이고, 별 트랙에서는 무엇인가?

**A**: **q52 본류 = 현 baseline 유지 / 별 트랙 = 7 영역** (§7).

| 영역 | 다음 gate |
|---|---|
| **q52 본류 (현 active baseline)** | 변경 없음 — registry artifact candidate / artifact review PASS / runtime design candidate / App/data direction / separability framework 모두 maintained. caution release blocked/precheck only. |
| **별 트랙 7 영역** | (1) 100 records 전수 source audit / (2) 99 records alias 확장 evaluation / (3) E4 다른 합본 PDF / (4) 외부 source evidence / (5) 66항 policy 재evaluation / (6) missing 29 recovery plan / (7) 1·3·4 verification |

### Q10 — JSONL decision entry?

**A**: **Yes — 진짜 정책 결정 영역**.

근거:
- q52 단독 변경 금지 = **permanent invariant 승격** (기존 룰의 영역 강화 + framework 변경)
- Q3 (App/data decision) **refined partial separable**로 명시화
- 5 layer 갱신 결과 framework 영역 영구화

→ jsonl entry id: `DR-TRAP-GIGI17-SEPARABILITY-REEVAL` 추가.

---

## 6. Separability Framework 영역 갱신 요약

| Layer | 직전 (d9b2efd) | E6 갱신 |
|---|---|---|
| Q1·Q2 Registry creation/review | Separable | **Separable 강화** |
| Q3 App/data decision | Partial Separable | **Refined Partial Separable** (alias-only resolver = Separable / app data registry / metadata / migration = Inseparable) |
| Q4 Caution release review | Inseparable | **Inseparable 유지** |
| Q5 Batch migration | Inseparable | **Inseparable 강화 — 영구 분리 불가 (다중 영역 systemic)** |
| Q6 systemic session-label policy | 별 문서 필요 | **별 문서 필요 + defer 유지** |
| (신규) q52 단독 storage_id 변경 | (직전 framework 외) | **Permanent Invariant** |

---

## 7. 다음 Gate

### 7.1 q52 본류 (현 baseline 유지)

- registry artifact `9868f95` (candidate, q52 row 1건)
- registry artifact review PASS 12/12 (`f0b462c`)
- runtime resolver design candidate (`6ac1a9b`)
- App/data decision direction (`9c1d387`, A + B-design-review)
- separability framework (본 E6 baseline)
- 기기-17 caution (유지)
- registry row status=candidate (유지)
- q52 storage_id permanent invariant (본 E6 신설)

### 7.2 별 트랙 7 영역 (각 별 명시 승인 후)

1. **100 records 전수 source audit** — 2020_1회 100 records의 true source 영역
2. **99 records alias 확장 evaluation** — systemic framing 확장 정책
3. **E4 다른 합본 PDF 패턴** (별 트랙)
4. **외부 source evidence** (한국기술자격검정 공식 2020 시행 기록)
5. **66항 policy 재evaluation** (E4 + 외부 source 후)
6. **missing 29 recovery plan** (R1~R5 evidence + 별 명시 승인)
7. **1·3·4 과목 verification 보강** (PDF read-only)

---

## 8. Forbidden Until Separate Approval

- **q52 단독 storage_id 변경 (Permanent Invariant — 영구 금지)**
- `questions.json` 수정
- per-year json 수정
- PDF filename rename
- PDF 파일 복사 / 편집 / OCR 산출물 신규 생성
- `pdf_pages/index.json` 수정
- app code 수정
- app alias resolver 구현
- app/data alias registry 추가 (Inseparable 영역)
- record metadata field 추가 (Inseparable 영역)
- registry row promotion from `candidate` to `approved`
- registry artifact 자체 수정 (q52 row 외 추가 row 포함)
- registry framing 확장 실행 (99 records 영역)
- 기기-17 caution 해제 선언
- Batch migration 진입 (Inseparable 영구 강화)
- persisted user data migration (Inseparable 영역)
- 66항 systemic policy를 q52 registry 영역에 흡수
- missing 29 recovery 실행
- 100 records alias 확장 실행
- 후보 C (split policy) 진입 (E1 + E3 + E5 부적합 확정 유지)
- 66항 policy defer 해제 선언 (evidence requirement 미충족 영역 유지)
- caution release 선언 (Inseparable 유지)

---

## 9. 영향 매트릭스

| 영역 | E6 영향 |
|---|---|
| q52 alias registry (9868f95) | candidate baseline 유지 + storage_id permanent invariant |
| registry artifact review PASS (f0b462c) | 12/12 baseline 유지 |
| runtime resolver design review (6ac1a9b) | design candidate 강화 (read-path resolver only) |
| App/data decision (9c1d387) | direction 강화 + Refined Partial Separable 명시 |
| 직전 separability evaluation (d9b2efd) | **본 E6로 갱신** |
| 66항 policy (df7e932) | defer 유지 |
| E1 source audit (5c1fecc) | split 부적합 강화 |
| E2 record-PDF mapping (5f1c9c5) | 정합 재확인 |
| missing 29 data debt (02c985c) | 별 트랙 분리 확정 + q52 separability 영향 0 재확인 |
| E3 namespace conflict (b7b2b0b) | q52 systemic 1 사례 + 단독 재발급 영구 부적합 강화 |
| E5 app key impact (dac6121) | 갱신 입력 + alias-only resolver Separable 강화 |
| caution release (Step 6) | Inseparable 유지 |
| Batch migration | Inseparable 강화 — 영구 분리 불가 |
| q52 단독 storage_id 변경 | **Permanent Invariant** (영구 금지) |
| 후보 C (split policy) | 부적합 강화 (E1 + E3 + E5 + E6) |
| 기기-17 caution | 유지 |
| registry row status=candidate | 유지 |

---

## 10. Decision Record 영향

본 evaluation은 **진짜 정책 결정 영역**:

- separability framework 5 layer 갱신 (Q1·Q2 강화 / Q3 refined / Q5 강화)
- q52 storage_id permanent invariant 승격 (신규)
- missing 29 영향 0 재확인 (분리 확정 강화)

→ jsonl `trap_map_active_decisions.jsonl`에 별 entry 1줄 추가.

new decision id: `DR-TRAP-GIGI17-SEPARABILITY-REEVAL`

---

## Status

- E6 separability re-evaluation 작성 완료.
- separability framework 5 layer 갱신:
  - Q1·Q2 Separable 강화 (registry creation/review = app key + 66항 정책 모두
    분리)
  - Q3 Refined Partial Separable (alias-only resolver Separable / app data
    registry · metadata · migration Inseparable)
  - Q4 Inseparable 유지 (caution release input 영역 미충족)
  - Q5 Inseparable 강화 — 영구 분리 불가 (mapping granularity 5 영역 + persisted
    data migration)
  - Q6 별 문서 필요 + defer 유지 (66항 policy)
- 신규 **q52 storage_id permanent invariant 승격** (단독 변경 영구 금지).
- missing 29 data debt = q52 separability 영향 0 재확인 (별 트랙 분리 확정).
- q52 본류 baseline 모두 유지 (registry / review / design / App/data /
  framework).
- 별 트랙 7 영역 활성 (100 records audit / 99 records alias / E4 / 외부 source /
  66항 재evaluation / missing 29 recovery / 1·3·4 verification).
- 본 evaluation은 진짜 정책 결정이므로 jsonl entry 1줄 추가 영역.
- app code / app data / questions.json / per-year / PDF / pdf_pages / registry
  artifact 모두 변경 0. resolver implementation / migration / framing 확장 0.
- 기기-17 caution 유지. caution release 차단 유지. Batch migration 차단 유지·
  강화. registry row status=candidate 유지. q52 단독 변경 영구 금지 강화.
