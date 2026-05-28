# Policy Change Rules v0.2 Acceptance Review

작성일: 2026-05-28
Gate: Acceptance Review Preservation Gate
분류: read-only acceptance review 결과 보존 문서

## 1. Meta

- 본 문서는 `policy_change_rules_v0.2_draft_instance.json`에 대한 **read-only acceptance review 결과를 보존**하는 문서이다.
- 본 문서는 방향 변경 문서, 구현 문서, 자산 수정 문서가 아니다.
- 본 문서는 F1~F7 발견사항을 해결하지 않는다. severity와 후속 gate routing만 기록한다.
- 본 문서 작성은 신규 markdown 1건 추가에 한정한다. 기존 schema/profile/instance/naming 문서는 수정하지 않는다.

## 2. Reviewed Assets

| 역할 | 파일 | 비고 |
|---|---|---|
| instance | `policy_change_rules_v0.2_draft_instance.json` | 12 rule(R1~R12), instance_version 0.2-draft |
| schema | `rule_schema_v0.1_draft.schema.json` | schema_version const 0.1-draft, 형식 검증용 contract |
| profile | `ee_agent_rule_profile_v0.2_draft.json` | profile_version 0.2-draft, category 10종 / predicate 7종 / check 15종 |

- instance 산출물은 선행 commit `bfcdd67` ("policy change rules instance v0.2 draft 기록")에서 이미 생성·commit 완료된 상태이다.
- 현재 HEAD는 `154ef99` ("docs: profile naming revision 기록")이다.
- 본 review 시점 git 상태: ahead/behind 0/0, tracked diff 0, staged diff 0.

## 3. Verdict

- official verdict: **accepted with non-blocking notes**
- blocking defect: 0
- 12 rule 전부가 schema v0.1 Rule 정의 + profile v0.2 catalog와 구조·교차 정합.
- "PASS with notes" 표현은 과거 대화에서 사용된 표현이며, naming revision §6 R4의 review gate result 어휘(`accepted / rejected`)와의 정합을 위해 공식 verdict 어휘로는 사용하지 않는다. 공식 verdict는 위의 "accepted with non-blocking notes"로만 표기한다.

## 4. Cross-check Summary

검토 기준: schema `_design_notes.known_limits` L1~L8. validator는 실행하지 않았으며, 본 검토는 수동 read-only 대조이다.

| 항목 | 검사 내용 | 결과 |
|---|---|---|
| L1 | Rule.id 유일성 (R1~R12) | 통과. 12/12 유일, `rules_count: 12` 일치 |
| L2 | predicate_id ∈ profile.predicate_library (7종) | 통과. 사용 predicate 전부 등록 |
| L3 | predicate args ↔ args_schema | 통과. R5 zero-direction min_count 생략(optional), R11 to 배열(oneOf) 모두 허용 범위 |
| L4 | Verdict.category ∈ profile.category_enum (10종) | 통과. 사용 category 7종 전부 등록 |
| L5 | function_id ∈ profile.check_library (15종) | 통과. wrapper 5종 포함 사용 12종 전부 등록 |
| L6 | check parameters ↔ parameters_schema | 통과. R6/R9/R11 `{$dynamic}` 객체가 v0.2 완화 type `[string, object]`에 적합 |
| L7 | priority_group × severity 정합 | schema가 "도메인 규약 미정의"로 둠. 관찰만 (F-note 참조) |
| L8 | deprecation_signal × verification_status | schema가 "정책 미정의"로 둠. 관찰만 (F1 참조) |

- validator 미실행 명시: L1~L8의 자동 cross-check 구현은 후속 Schema Validator Gate 책임이며, 본 gate에서는 수동 검토만 수행했다.

## 5. Findings F1~F7

각 항목은 본 gate에서 해결하지 않으며, severity와 후속 routing만 기록한다.

| # | severity | 발견 | 근거 (파일:line) |
|---|---|---|---|
| F1 | LOW | changelog #9 "R5·R7·R8 deprecation_signal 제거"가 R5에 대해 부정확. R7/R8은 제거되었으나 R5는 deprecation_signal(측정 오류 의미)을 유지. schema상 optional 필드라 위반은 아님 | instance:213 (R5 유지) / R7·R8 metadata 부재 |
| F2 | MED | domain_agnostic vs category 도메인성 긴장. R7/R8(`domain_agnostic: true`)이 `MAGNITUDE_DELTA` 사용. profile은 category_enum을 "ee-agent 도메인 한정 어휘"로 규정. R12(`domain_agnostic: true`, `TOOL_CHANGE`)도 동일 | instance:301/323, 340/362, 506/527 / profile:47 |
| F3 | MED | `$dynamic` 바인딩 형식이 미정의 상태에서 사용됨. R6/R9/R11이 `{$dynamic: "..."}` 사용. profile이 "$dynamic 키 패턴 세부 정의"를 `not_validated_in_this_gate`로 명시. 구조는 유효(object 허용)하나 토큰 의미 미규정 | instance:283/406/489 / profile:420 |
| F4 | LOW | R9 `$dynamic` 토큰 의미 적합성. `predicate_dominant_item` 토큰을 R6(item_concentration_pct: 명확한 dominant item)와 R9(zero_hit_items: 단일 dominant item 부재)가 공유. R9 적합성 불명 | instance:283 (R6) / 406 (R9) |
| F5 | MED | runtime state `catalog` 누락/drift. naming §6 R4 runtime data state는 "CLEAN/GAP/NEEDS_REVIEW"(3종)인데 profile v0.2 status_values는 "CLEAN/NEEDS_REVIEW/catalog/GAP"(4종). instance 12 rule은 3종만 사용해 R4와 정합하나, R4 인벤토리가 `catalog`를 누락 | naming:252 / profile:33~34 |
| F6 | INFO | tmp source provenance. source_v0_2_path = `/private/tmp/...` + sha256. tmp는 휘발성이라 provenance 재현 불가 가능 | instance:10~11 |
| F7 | INFO | naming §9 follow-up drift. §9 "후보 I-impl: Instance v0.2 Implementation Gate"가 미래 후보로 나열되나 산출물은 bfcdd67에서 이미 완료 | naming:352 / git bfcdd67 |

## 6. Consistency Gaps C1~C4

외부 검토에서 제기된 일관성 gap. 본 gate에서 해결하지 않으며 관찰/후속 후보로 기록한다.

| # | gap | 처리 |
|---|---|---|
| C1 | `threshold_proposals`와 U10의 상호 참조/어휘 분리 미결 | 후속 후보. routing → Threshold Confirm Extension Gate |
| C2 | schema known_limits L7/L8, instance U9, 본 review 관찰 사이의 중복 미결 | 후속 후보. routing → L7 Policy Decision Gate |
| C3 | "PASS with notes" vs R4 `accepted/rejected` 어휘 충돌 | 본 gate에서 공식 verdict를 "accepted with non-blocking notes"로 표기하여 정합 반영. 관찰로 기록 유지 |
| C4 | review document suffix 선택 근거 | naming §6 R6 `_review` 접미사 의미("read-only 검토 결과")에 부합하여 `_review.md` 채택 |

## 7. Follow-up Gate Routing

| 항목 | routing |
|---|---|
| F3 / F4 | Dynamic Binding Spec Gate |
| F2 / F5 | Naming Revision v0.2 Drift Gate |
| F1 | changelog precision correction 후보 |
| F6 | Source Snapshot / Provenance Policy Gate |
| F7 | Naming follow-up drift 후보 |
| U9 / C2 | L7 Policy Decision Gate |
| U10 / C1 | Threshold Confirm Extension Gate |

- 위 routing은 후속 후보 표기이며, 본 gate는 어느 후속 gate도 시작하지 않는다.

## 8. Claim Boundary

본 문서가 주장하지 않는 것:

- 본 문서는 F1~F7을 해결하지 않는다.
- 본 문서는 accepted verdict를 보존하지만 validator 통과를 주장하지 않는다.
- 본 문서는 schema/profile/instance 변경을 주장하지 않는다.
- 본 문서는 threshold/L7/MVP 결정을 주장하지 않는다.
- Instance v0.2 구현 완료 상태는 `bfcdd67` 산출물 존재에 근거한 관찰로만 둔다.

본 문서가 보존하는 것:

- 본 review 시점의 cross-check 결과(L1~L6 통과, L7/L8 관찰)
- 발견사항 F1~F7의 severity와 후속 routing
- 일관성 gap C1~C4의 관찰과 routing
- 공식 verdict "accepted with non-blocking notes"

## 9. Success Criteria Self-check

- 신규 markdown 1건만 추가: 본 문서.
- 기존 파일 수정: 0 (작성 후 git diff --stat / status로 확인).
- staged: 0.
- commit / push: 0.
- forbidden actions(schema·profile·instance·naming 직접 수정, F1 원본 정정, $dynamic spec 정의, Threshold/MVP/L7 결정, validator 실행, DEVLOG/Vault/MEMORY/decision JSONL 작성): 0.

다음 자연 후보: 사용자 승인 시 §7 routing 중 1건. 본 gate는 보존만 완료하고 후속 gate는 시작하지 않는다.
