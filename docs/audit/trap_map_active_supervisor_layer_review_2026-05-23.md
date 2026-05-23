# Trap-Map Active Supervisor Layer Review (2026-05-23)

`02f7f4b`(`docs: add trap-map active supervisor layer`)가 trap-map 트랙의 능동
감독 레이어로 push 가능한지 리뷰한다. 본 리뷰는 active supervisor layer 자체만
다룬다. b69ab80/d450f67 A-track closeout은 이미 별도 PASS로 닫혔고, app/data,
questions.json, 학습 패키지, 기존 commit은 수정하지 않는다.

- 리뷰 대상 commit: `02f7f4b`
- 리뷰 대상 파일:
  1. `docs/audit/supervisor_logs/2026-05-23_trap_map_active_supervisor_layer.md`
  2. `docs/audit/decision_records/trap_map_active_decisions.jsonl`
- 외부 검토 입력:
  - Claude web: active layer는 자기 자신을 supervise할 수 없으며, 1층 기록 /
    2층 현재 상태 / 3층 외부 audit로 분리해야 한다는 지적
  - Claude CLI: b69ab80/d450f67 A-track review PASS 요약 및 다음 단계로
    02f7f4b review 권고

---

## 판정: **NEEDS_FIX** — push 전 보강 필요

`02f7f4b`는 흩어진 감독 판단을 모으는 1층 decision record로는 유효하다. 하지만
active supervisor layer라는 이름으로 push하기에는 구조적 축 3개가 빠져 있다.

1. layer가 자기 판단 실패를 인정하고 정정하는 record type이 없다.
2. append-only decision log와 현재 활성 상태 요약이 분리되어 있지 않다.
3. layer 외부에서 layer 자체를 audit하는 주기와 절차가 없다.

따라서 이 commit은 "무엇을 결정했는가"의 박스는 만들었지만, "그 결정이 나중에
틀렸을 때 어떻게 발견하고 회수할 것인가"를 아직 만들지 못했다. push 전 보강
commit이 필요하다.

---

## 1. 좋은 점

### 1. decision 원장 도입은 타당

`trap_map_active_decisions.jsonl`은 A closeout, B pilot 제한, 기기-18 correction,
기기-17 source identity escalation, N3a A-track 선행 결정까지 핵심 판단을 한 줄
레코드로 남긴다. 각 record는 decision, rationale, rejected_alternatives,
state_effect, next_gate, forbidden_until_gate를 갖는다.

이 구조는 "왜 그때 그 선택을 했는가"를 복원하는 데 도움이 된다.

### 2. 현재 caution/blocked 상태를 명시한 점은 유효

supervisor log는 사용 가능 36/41, 완전 클린 35/40, caution 1/1 = 기기-17,
blocked 0/0을 명시한다. 기기-17 caution 유지와 data/id/meta 보류 금지도 문서에
들어 있다.

### 3. 금지 범위를 앞에 둔 점은 작업 안전에 기여

questions.json id/year/session/q_no 수정, PDF filename rename, app route/index 수정,
기기-17 caution 해제 선언, B-priority full expansion 금지가 명시되어 있다. 이는
다음 작업자가 고위험 수정을 성급히 여는 것을 막는다.

---

## 2. 결함

### P1-1 — 자기부정 record type 부재

현재 decision record는 새 결정을 append할 수 있지만, 이전 decision이 틀렸다는
사실을 정식으로 표현할 방법이 없다. `supersede`, `revoke`, `amend`,
`post_audit_findings` 같은 record type이 없기 때문에 잘못된 PASS가 들어가도
그 상태를 기계적으로 구분하기 어렵다.

이 결함은 active supervisor layer의 핵심 신뢰성 문제다. 지난 트랙에서 반복된 문제는
"판단이 흩어졌다"가 아니라 "이전 PASS가 다음 단계에서 깨졌다"였기 때문이다.

요구 보강:
- JSONL schema에 `record_type`을 추가한다.
- 최소 record type: `decision`, `supersede`, `revoke`, `amend`, `audit`,
  `consolidation`.
- `supersedes`, `revokes`, `amends` 대상 id 필드를 정의한다.

### P1-2 — 1층 decision log와 2층 active state가 섞여 있음

supervisor log 하나가 decision history, 현재 상태, active queue, 금지 범위를 모두
담고 있다. 이 구조는 초기에는 편하지만 시간이 지나면 append-only 기록과 현재
작업자가 봐야 할 활성 상태가 섞인다.

append-only는 과거 판단 보존에 필요하지만, 현재 상태 요약은 정기적으로 갱신되고
정리되어야 한다. 둘이 섞이면 6개월 뒤에는 오래된 queue와 최신 record가 한 문서
안에서 충돌할 가능성이 높다.

요구 보강:
- 1층: append-only `decision_records/*.jsonl`
- 2층: 현재 상태 요약 `supervisor_state/*.md` 또는 동등한 active-state 문서
- 2층 문서는 마지막 consolidation 기준, active tracks, current forbidden scope,
  next gates, stale 후보를 명시한다.

### P1-3 — 3층 외부 audit 절차 부재

현재 layer는 supervisor가 자기 결정을 직접 기록하는 구조다. 그런데 자기 결정의
옳고 그름을 자기 문서만으로 검증할 수는 없다. layer 외부에서 layer를 점검하는
주기와 기준이 필요하다.

요구 보강:
- 매 5개 decision마다 또는 매주 1회 중 하나 이상을 audit trigger로 둔다.
- audit 기준: 잘못된 PASS, decision log와 active state 불일치, stale record,
  forbidden scope 위반, cross-track dependency 누락.
- audit 산출물 위치와 naming rule을 정의한다.

### P1-4 — cross-track dependency 감지 규칙 부족

현재 active queue는 기기-17 A-track, B-track, redryrun, clean count 갱신 등을
순서대로 적지만, 한 트랙의 결정이 다른 트랙에 영향을 줄 때 이를 감지하는 규칙은
없다. 예를 들어 기기-17 data identity 정책은 app route, per-year json, PDF filename,
clean count, B-priority closeout 기록에 영향을 줄 수 있다.

요구 보강:
- decision record에 `affected_tracks` 또는 `dependency_edges`를 추가한다.
- active state가 "cross-track impact review 필요" 항목을 별도로 보여야 한다.

### P2-1 — 02f7f4b 자체의 active queue가 이미 stale됨

`02f7f4b`의 active queue는 "기기-17 N3a A-track 적용 리뷰"를 1순위로 두고 있다.
하지만 현재 HEAD에는 `d450f67` review commit이 추가되어 b69ab80 A-track review는
PASS로 닫혔다.

이것은 02f7f4b 작성 시점에는 자연스러운 상태였지만, 현재 push 전 stack 기준으로는
active state 갱신 필요성을 보여주는 사례다. active state가 decision log와 분리되어
정기 갱신되어야 한다는 P1-2의 근거이기도 하다.

---

## 3. 클로드 답변 종합

Claude web의 핵심 지적은 타당하다. active supervisor layer는 자기 자신을 supervise할
수 없으므로, 이를 인정한 설계를 넣어야 한다. 즉 layer는 "내가 옳다"를 보장하는
장치가 아니라, "내가 틀렸을 때 그 사실을 기록하고 회수할 수 있다"를 보장하는
장치여야 한다.

Claude CLI의 b69ab80/d450f67 PASS 요약도 타당하다. 다만 CLI 요약의 commit stack은
현재 로컬 실제 상태와 다르다. 현재 로컬은 origin `16c61f2` 위에 `b69ab80`,
`02f7f4b`, `d450f67` 3개 commit이 있다. 따라서 push 판단은 02f7f4b를 포함한
3-commit stack 기준으로 해야 한다.

종합하면:

- b69ab80 + d450f67: A-track closeout으로 인정 가능.
- 02f7f4b: 좋은 시작이지만 active supervisor layer로 push하기 전 보강 필요.
- 다음 행동: 기존 02f7f4b를 amend하지 말고, follow-up commit으로 v2 layer 보강을
  추가한다.

---

## 4. 권고 보강안

### 보강 commit 목표

`docs: harden trap-map active supervisor layer`

### 최소 변경 범위

1. `docs/audit/supervisor_logs/2026-05-23_trap_map_active_supervisor_layer.md`
   - 구조적 한계 명시
   - 1층/2층/3층 분리 원칙 추가
   - record type과 supersede/revoke/amend 규칙 추가
   - 외부 audit trigger 추가
2. `docs/audit/decision_records/trap_map_active_decisions.jsonl`
   - 새 `audit` 또는 `amend` record 1건 append: "active layer v1 review에서
     자기부정/active-state/external-audit 보강 필요 확인"
3. 새 문서(권장):
   - `docs/audit/supervisor_state/trap_map_active_state_2026-05-23.md`
   - `docs/audit/supervisor_audits/trap_map_supervisor_layer_audit_protocol_2026-05-23.md`

### push 판단

`02f7f4b` 단독 push는 비권장. follow-up hardening commit까지 만든 뒤, stack 전체를
다시 리뷰하고 push 여부를 결정한다.

---

## 5. 결론

- 판정: **NEEDS_FIX**.
- 이유: 1층 decision record는 유효하지만, 2층 active state 분리와 3층 외부 audit,
  자기부정 record type이 없다.
- b69ab80/d450f67은 A-track closeout으로 인정 가능하다.
- 02f7f4b는 follow-up hardening commit으로 보강한 뒤 push 판단한다.

이 문서는 active supervisor layer review 전용이다. app/data, questions.json,
학습 패키지, 기존 commit, PDF filename은 수정하지 않았다.

---

## Status

- 02f7f4b active supervisor layer review 완료.
- 판정 **NEEDS_FIX**.
- P1 4건 / P2 1건.
- 다음 권고 작업: active supervisor layer hardening follow-up commit 작성.
