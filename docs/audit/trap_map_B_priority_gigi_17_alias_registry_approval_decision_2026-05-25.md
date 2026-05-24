# Trap-Map B-Priority — 기기-17 Alias Registry Approval Decision (2026-05-25)

기기-17 alias schema plan 이후, tracked docs registry artifact를 만들지 여부와
artifact 형식/경로를 결정한다. 본 문서는 **registry artifact approval decision**이며,
registry artifact 자체를 생성하지 않는다.

이번 단계는 approval decision 작성까지다. **app/data, `questions.json`, per-year json,
PDF filename, `pdf_pages/index.json`은 수정하지 않는다.** push 없음.
amend/rebase/reset 없음. 기기-17 caution 유지. q52 단독 id 재발급 금지 유지.

- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`
- 관련 correction plan: `docs/audit/trap_map_B_priority_gigi_17_B_track_correction_plan_v2_2026-05-25.md`
- 관련 decision record: `docs/audit/trap_map_B_priority_gigi_17_B_track_decision_record_2026-05-25.md`
- 관련 schema plan: `docs/audit/trap_map_B_priority_gigi_17_alias_schema_plan_2026-05-25.md`
- active prior decision id: `DR-TRAP-GIGI17-BTRACK-ALIAS-FIRST-GATE`
- new decision id: `DR-TRAP-GIGI17-ALIAS-REGISTRY-ARTIFACT`

---

## 1. Decision Summary

| 항목 | 결정 |
|---|---|
| tracked docs registry artifact | 생성 승인 |
| artifact timing | 이 decision 이후 별도 commit에서 생성 |
| artifact format | JSON |
| artifact path | `docs/audit/registries/trap_map_gigi_17_alias_registry_2026-05-25.json` |
| initial rows | q52 candidate row 1건만 |
| runtime effect | 없음. app/data registry나 resolver가 아님 |
| caution effect | 없음. 기기-17 caution 유지 |
| 66항 relation | unresolved residual risk. registry creation과 병렬 gate로 separability evaluation 필요 |

이 결정은 tracked docs registry를 **source/citation review artifact 후보**로 승인한다.
runtime source of truth, app persisted key migration, caution release 근거로 승격하지 않는다.

---

## 2. Approved Artifact Boundary

생성 승인 범위:

- `docs/audit/registries/` 아래 tracked JSON artifact 1개
- alias schema plan §2의 필드 사용
- q52 seed row 1건만 `status=candidate`로 기록
- `evidence_ref`는 targeted audit과 B-track impact audit을 모두 연결
- `storage_id=2020_1회_52` 유지
- `canonical_source_id=2022_1회_52`는 source citation id로만 사용
- `cover_date=2022-04-24`는 "PDF 표지 기재 일자"로만 사용

생성 승인 범위가 아닌 것:

- `app/data` registry 생성
- app alias resolver 구현
- question record metadata 추가
- `questions.json` 또는 per-year json 수정
- PDF filename rename
- `pdf_pages/index.json` 수정
- q52 단독 id 재발급
- 기기-17 caution 해제

---

## 3. Format Rationale

JSON을 선택한다.

| 후보 | 판단 |
|---|---|
| Markdown registry | review는 쉽지만 duplicate mapping, allowed status, evidence field 같은 검증을 수동으로 해야 한다 |
| JSON registry | human review는 약간 덜 편하지만 structured validation과 future integrity check에 유리하다 |
| JSONL registry | append-only 이력에는 좋지만 현재는 작은 active registry라 row set validation이 더 중요하다 |

따라서 registry artifact는 JSON으로 만들고, 해설과 정책 판단은 본 decision 문서와 schema
plan에 둔다. JSON registry는 review 대상 artifact일 뿐 app runtime이 직접 읽는 파일이
아니다.

권장 top-level shape:

```json
{
  "schema_version": 1,
  "artifact_type": "trap_map_alias_registry",
  "scope": "gigi_17_b_track",
  "created_date": "2026-05-25",
  "status": "candidate",
  "rows": []
}
```

`rows`에는 alias schema plan §2의 row schema를 사용한다. 초기 artifact 생성 시 rows는
q52 candidate row 1건만 포함한다.

---

## 4. Required Creation Checks

다음 단계에서 registry artifact를 생성할 때 아래 checks를 같은 commit evidence에 남긴다.

| check | required result |
|---|---|
| path scope | artifact is under `docs/audit/registries/` only |
| app/data untouched | no tracked changes under app/data, `data/questions_기출_*.json`, PDF files, or `pdf_pages/index.json` |
| q52 row status | `status=candidate` |
| storage guardrail | `storage_id=2020_1회_52`; no question id rewrite |
| canonical guardrail | `canonical_source_id=2022_1회_52` used only as source citation |
| evidence ref | targeted audit and B-track impact audit are both referenced |
| cover-date wording | 2022-04-24 is treated as PDF 표지 기재 일자 |
| duplicate active mapping | one active canonical mapping per `storage_id` |

The creation commit may include a lightweight validation note, but must not broaden into app/data
implementation work.

---

## 5. Relationship To 66항

The `2020_1,2회` 66항 issue remains separate.

- The q52 registry row does not normalize `2020_1,2회`.
- The registry artifact must not claim the 66항 issue is resolved.
- 66항 separability evaluation may run in parallel with registry artifact creation/review.
- Caution release review cannot skip the 66항 separability evaluation.

This decision approves only a q52 alias inventory artifact. It does not decide systemic
session-label policy.

---

## 6. Next Gates

1. **Registry artifact creation**
   - Create `docs/audit/registries/trap_map_gigi_17_alias_registry_2026-05-25.json`.
   - Include only the q52 candidate row.
   - Run the creation checks in §4.
2. **Registry artifact review**
   - Confirm JSON shape, q52 row values, evidence refs, and guardrails.
   - Keep q52 candidate unless a later approval explicitly promotes status.
3. **66항 separability evaluation**
   - Decide whether unresolved `2020_1,2회` 66항 risk is separable from q52 source citation.
4. **App/data decision**
   - Decide separately whether runtime resolver, app data registry, or record metadata is needed.
5. **Caution release review**
   - Only after registry artifact review, user-facing impact evidence, 66항 separability decision,
     and redryrun evidence exist.

---

## 7. Forbidden Until Separate Approval

- q52 단독 id 재발급
- `questions.json` 수정
- per-year json 수정
- PDF filename rename
- `pdf_pages/index.json` 수정
- app alias resolver 구현
- app/data alias table 추가
- record metadata field 추가
- registry row promotion from `candidate` to `approved`
- 기기-17 caution 해제 선언

---

## Status

- Registry artifact creation approved.
- Registry artifact not yet created.
- app/data/pdf_pages unchanged by this decision.
- q52 단독 id 재발급 금지 유지.
- 기기-17 caution 유지.
