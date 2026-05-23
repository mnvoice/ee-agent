# Trap-Map Active Supervisor Layer Hardening Review (2026-05-23)

`f227249`(`docs: harden trap-map active supervisor layer`)가 `dd20392` review의
NEEDS_FIX 항목을 해소했는지 리뷰한다. 본 리뷰는 supervisor layer hardening만
다룬다. app/data, questions.json, 학습 패키지, PDF filename, 기존 commit은 수정하지
않는다.

- 리뷰 대상 commit: `f227249`
- 리뷰 대상 파일:
  1. `docs/audit/supervisor_logs/2026-05-23_trap_map_active_supervisor_layer.md`
  2. `docs/audit/decision_records/trap_map_active_decisions.jsonl`
  3. `docs/audit/supervisor_state/trap_map_active_state_2026-05-23.md`
  4. `docs/audit/supervisor_audits/trap_map_supervisor_layer_audit_protocol_2026-05-23.md`
- 선행 리뷰: `docs/audit/trap_map_active_supervisor_layer_review_2026-05-23.md`

---

## 판정: **PASS** — active supervisor layer hardening 적용 인정

`f227249`는 `dd20392`의 P1 결함 4건을 실질적으로 해소했다.

1. 자기부정 record type 부재 → `record_type` 규칙과 `decision/supersede/revoke/amend/audit/consolidation` 정의 추가.
2. decision log와 active state 혼재 → `supervisor_state/trap_map_active_state_2026-05-23.md` 신설.
3. 외부 audit 절차 부재 → `supervisor_audits/trap_map_supervisor_layer_audit_protocol_2026-05-23.md` 신설.
4. cross-track dependency 감지 부족 → active-state에 `Cross-Track Dependency Watch` 추가.

변경 범위는 supervisor layer docs 4개에 한정된다. app/data, questions.json,
학습 패키지, id/meta, PDF filename 변경은 없다. decision JSONL은 `jq -c .`로
전체 라인 파싱 PASS.

---

## 1. 기준별 검토

### 기준 1 — 자기부정 record type 보강: PASS

supervisor log에 `record_type` 운용 규칙이 추가됐다. 최소 type으로 `decision`,
`supersede`, `revoke`, `amend`, `audit`, `consolidation`을 정의했고,
`supersedes`, `revokes`, `amends` 대상 id 필드 규칙도 명시했다.

decision JSONL에는 다음 record가 append됐다.

- `DR-TRAP-SUPERVISOR-LAYER-REVIEW-NEEDS-FIX` (`record_type: audit`)
- `DR-TRAP-SUPERVISOR-LAYER-HARDENING` (`record_type: consolidation`)

### 기준 2 — 1층/2층 분리: PASS

새 active-state 문서가 생성됐다.

`docs/audit/supervisor_state/trap_map_active_state_2026-05-23.md`

이 문서는 현재 stack, 판정, count, active queue, 금지 범위, stale 후보,
cross-track dependency watch를 분리해 제공한다. 기존 supervisor log의 §4 active queue는
historical snapshot으로 강등됐고, active-state 문서가 canonical임을 명시했다.

### 기준 3 — 3층 외부 audit 절차: PASS

새 audit protocol 문서가 생성됐다.

`docs/audit/supervisor_audits/trap_map_supervisor_layer_audit_protocol_2026-05-23.md`

audit trigger는 every 5 decisions, weekly, before push, after failed PASS,
before caution release로 정의됐다. audit questions, required evidence, record types,
PASS criteria, output naming도 포함한다.

### 기준 4 — cross-track dependency 감지: PASS

active-state 문서에 `Cross-Track Dependency Watch`가 추가됐다.

| decision | 영향 가능 트랙 | 필요한 확인 |
|---|---|---|
| 기기-17 source identity 정책 | questions.json, per-year json, pdf_pages, app route/index, clean count | B-track 전 app/data grep + 100항 sanity |
| active supervisor layer push | 이후 모든 trap-map decision 기록 방식 | hardening review PASS 전 push 금지 |
| 기기-17 caution 해제 | closeout, post-closeout errata, B-pilot count | data/id/meta 정합 결정 전 해제 금지 |

### 기준 5 — stale handling: PASS with note

`02f7f4b` supervisor log의 active queue는 b69ab80 review 전 snapshot이라 현재
상태와 다르다. `f227249`는 이를 historical snapshot으로 강등하고, active-state 문서를
canonical으로 지정했다.

note: active-state의 stack은 hardening follow-up 작성 시작 시점 기준으로 표기되어
있고, hardening commit 생성 후 push 전 `git log --oneline --decorate -6` 재확인을
요구한다. 이는 stale을 숨긴 것이 아니라 stack 재확인 gate로 처리한 것이다.

### 기준 6 — 변경 범위: PASS

`git show --name-status f227249` 기준 변경 파일은 supervisor layer 4개뿐이다.

| 파일 | 상태 |
|---|---|
| `docs/audit/decision_records/trap_map_active_decisions.jsonl` | M |
| `docs/audit/supervisor_logs/2026-05-23_trap_map_active_supervisor_layer.md` | M |
| `docs/audit/supervisor_state/trap_map_active_state_2026-05-23.md` | A |
| `docs/audit/supervisor_audits/trap_map_supervisor_layer_audit_protocol_2026-05-23.md` | A |

app/data, questions.json, 학습 패키지, id/meta, PDF filename 변경은 없다.

### 기준 7 — JSONL 유효성: PASS

`jq -c . docs/audit/decision_records/trap_map_active_decisions.jsonl` 전 라인 파싱
PASS. JSONL 문법 깨짐 없음.

---

## 2. 남은 위험

### R1 — 외부 audit은 절차만 정의됐고 실제 외부 reviewer 수행은 아직 아님

이번 commit은 audit protocol을 만든다. 실제 외부 audit 수행은 다음 push 전 또는
decision 5건 추가 후 별도 산출물로 해야 한다.

### R2 — active-state는 갱신 discipline이 필요

active-state 문서는 canonical이므로, push 전 또는 caution/count 변경 전 반드시 갱신
여부를 확인해야 한다. 이 위험은 protocol의 `before push`, `before caution release`
trigger로 관리한다.

---

## 3. 결론

- 판정: **PASS**.
- `f227249`는 active supervisor layer hardening commit으로 인정한다.
- `dd20392`의 P1 4건은 해소됐다.
- push는 아직 수행하지 않는다. push 전에는 local stack 전체와 active-state 최신성을
  다시 확인한다.

---

## Status

- active supervisor layer hardening review 완료.
- 판정 **PASS**.
- JSONL 파싱 PASS.
- 변경 범위 docs/audit supervisor layer 한정.
- 다음 단계 후보: local stack 전체 push-readiness review 또는 기기-17 B-track 영향 측정.
