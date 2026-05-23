# Trap-Map Supervisor Layer Audit Protocol (2026-05-23)

이 문서는 trap-map active supervisor layer의 3층 외부 audit 절차다. decision
record와 active state는 supervisor가 작성할 수 있지만, 그 정합성은 별도 audit로
다시 물어야 한다.

---

## 1. Audit Trigger

아래 조건 중 하나가 발생하면 supervisor layer audit을 수행한다.

| trigger | 설명 |
|---|---|
| every 5 decisions | `decision_records/*.jsonl`에 decision/audit/amend 등 record 5건이 추가될 때마다 |
| weekly | 같은 트랙이 7일 이상 이어질 때 주 1회 |
| before push | supervisor layer 관련 commit을 push하기 전 |
| after failed PASS | 이전 PASS가 후속 단계에서 깨졌을 때 |
| before caution release | caution/blocked/clean count가 바뀌기 전 |
| repeated supersede | 같은 track에서 supersede/revoke/amend가 2회 발생할 때 |
| meta-work ratio | 다음 일반 task cycle에서 supervisor-layer commit 수가 본작업 commit 수를 초과할 때 |

첫 audit cycle은 push 전 2026-05-23 local stack 기준으로 수행한다. 다음 정기 audit
후보는 2026-05-30 또는 decision record 5건 추가 시점 중 먼저 오는 때다.

---

## 2. Audit Questions

audit reviewer는 최소한 아래 질문에 답한다.

1. 지난 N개 decision 중 후속 단계에서 깨진 PASS가 있는가?
2. append-only decision log와 active-state 문서가 같은 현재 상태를 가리키는가?
3. active-state의 queue가 stale되지 않았는가?
4. forbidden scope를 어긴 commit이나 문서가 있는가?
5. cross-track dependency가 누락되지 않았는가?
6. supersede/revoke/amend가 필요한 이전 decision이 있는가?
7. push해도 되는 stack인지, 아니면 hardening/fix commit이 먼저 필요한가?

---

## 3. Required Evidence

audit 문서는 아래 evidence를 포함한다.

| evidence | 예시 |
|---|---|
| git stack | `git log --oneline --decorate -6` |
| diff scope | `git show --name-status <commit>` 또는 `git diff --name-only` |
| state match | active-state count와 closeout/errata count 대조 |
| stale scan | active queue와 이미 완료된 commit 비교 |
| forbidden scan | app/data/questions.json/PDF filename 변경 여부 |
| dependency scan | source identity, app route, count, closeout 영향 |

---

## 4. Record Types

audit 결과는 필요하면 decision JSONL에 append한다.

| record_type | 사용 시점 |
|---|---|
| audit | layer/state 정합성 점검 결과 |
| amend | 기존 decision 일부 보정 |
| supersede | 기존 decision을 새 decision으로 대체 |
| revoke | 기존 decision 철회 |
| consolidation | active-state 문서를 갱신해 현재 상태를 정리 |

`amend`, `supersede`, `revoke`는 반드시 대상 record id를 함께 적는다.

`amend`, `supersede`, `revoke`는 책임 회피 도구가 되면 안 된다. 따라서 아래 필드를
필수로 둔다.

| 필드 | 의미 |
|---|---|
| failure_reason | 이전 판단이 왜 틀렸거나 불완전했는지 |
| prevention_check | 같은 실패를 다음 review에서 어떻게 막을지 |
| affected_records | 영향을 받는 decision id 목록 |

같은 track에서 `amend`/`supersede`/`revoke`가 2회 발생하면 external audit을 수행한다.
3회 발생하면 해당 track을 freeze하고, 별도 audit PASS 전까지 새 normalization,
clean count 갱신, push를 금지한다.

---

## 5. PASS Criteria

supervisor layer audit이 PASS가 되려면 아래를 모두 만족해야 한다.

| 기준 | PASS 조건 |
|---|---|
| decision log | record id 중복 없음, 필요한 record_type 존재 |
| active state | 현재 stack, count, caution/blocked, active queue가 최신 |
| external audit | trigger와 질문이 문서화되어 있음 |
| stale handling | historical snapshot과 canonical state가 구분됨 |
| cross-track dependency | 영향 트랙과 다음 확인이 명시됨 |
| forbidden scope | 금지 범위 위반 없음 |

---

## 6. Output Naming

audit 산출물은 아래 위치에 둔다.

- `docs/audit/supervisor_audits/trap_map_supervisor_layer_audit_YYYY-MM-DD.md`
- active-state 갱신이 필요하면 `docs/audit/supervisor_state/trap_map_active_state_YYYY-MM-DD.md`
- decision record 갱신은 `docs/audit/decision_records/trap_map_active_decisions.jsonl`에 append

---

## Status

- 3층 외부 audit protocol 생성.
- audit trigger: every 5 decisions / weekly / before push / after failed PASS /
  before caution release.
- 다음 필요 작업: hardening commit review.
