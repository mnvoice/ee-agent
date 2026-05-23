# Trap-Map Active Supervisor Hardening Evidence Pack (2026-05-23)

이 문서는 `f227249` hardening과 `b69e42c` hardening review를 외부 reviewer가 다시
검증할 수 있게 만든 evidence pack이다. 목적은 "hardening을 했다고 선언"하는 것이
아니라, 어떤 결함이 어떤 파일·규칙·record로 패치됐는지 1:1로 대조하게 하는 것이다.

---

## 1. 자기반성

`b69e42c`의 PASS 판정은 방향성 면에서는 맞았지만, 내가 너무 빨리 닫은 부분이 있다.
특히 아래 둘을 더 분리했어야 한다.

- 절차를 문서화했다.
- 절차가 실제로 작동할 수 있게 첫 cycle, 실패 회수 조건, 남용 방지 조건까지 박았다.

`f227249`는 1층/2층/3층 분리의 뼈대는 만들었다. 그러나 외부 reviewer 입장에서는
"실제 내용 확인 전 PASS"가 될 수 있었다. 그래서 이 문서는 G-1/G-2/G-3 보강 evidence와
남은 위험을 명시한다.

---

## 2. 5축 Evidence Mapping

| 검증축 | evidence | 판정 |
|---|---|---|
| f227249 실제 변경 내용 | `git show --name-status f227249` 기준 supervisor layer 4파일만 변경 | 확인됨 |
| b69e42c review 본문 | `docs/audit/trap_map_active_supervisor_layer_hardening_review_2026-05-23.md`에 PASS 근거 7기준 기록 | 확인됨 |
| 3층 분리 | decision JSONL / active-state / audit protocol 3개 층으로 분리 | 확인됨 |
| 외부 audit 절차 | audit trigger와 questions는 있음. 첫 cycle 일자는 본 evidence pack 및 protocol 보강에서 명시 | 보강 필요 → 보강 |
| cross-track dependency | active-state에 dependency watch 있음. 자동 감지는 아님, 수동 gate로 운용 | 부분 충족 |

---

## 3. dd20392 P1 결함별 패치 위치

| dd20392 결함 | f227249 / 후속 보강 evidence | 남은 한계 |
|---|---|---|
| P1-1 자기부정 record type 부재 | supervisor log §1에 `record_type` 표 추가. audit protocol §4에 record type 정의. JSONL에 `audit`, `consolidation` record append | supersede 남용 방지 규칙이 약했음 → protocol에 threshold/freeze 보강 필요 |
| P1-2 decision log와 active state 혼재 | `docs/audit/supervisor_state/trap_map_active_state_2026-05-23.md` 신설. 기존 queue는 historical snapshot으로 강등 | active-state 갱신 discipline은 사람 gate |
| P1-3 외부 audit 절차 부재 | `docs/audit/supervisor_audits/trap_map_supervisor_layer_audit_protocol_2026-05-23.md` 신설 | 첫 audit 일자와 reviewer designation이 약했음 → 본 문서에서 before-push first cycle 명시 |
| P1-4 cross-track dependency 감지 부족 | active-state §6 `Cross-Track Dependency Watch` 추가 | 자동 감지는 아님. 현재는 수동 review gate |

---

## 4. First External Audit Cycle

첫 external audit cycle은 **push 전, 2026-05-23 local stack 기준**으로 수행한다.

- 대상 stack: `b69ab80` → `02f7f4b` → `d450f67` → `dd20392` → `f227249` →
  `b69e42c` → 본 evidence/safeguard follow-up
- reviewer 역할: Codex 작성자가 아닌 외부 reviewer 역할(Claude Web 또는 사용자 감독
  판단 포함)
- audit 질문:
  1. hardening이 4축 P1을 실제로 해소했는가?
  2. 외부 audit이 문서상 약속에 그치지 않고 첫 cycle로 실행 가능한가?
  3. supersede/revoke/amend가 책임 회피 도구가 되지 않도록 조건이 충분한가?
  4. 메타작업 비율이 다음 cycle에서 줄어들 gate가 있는가?
  5. push 전 P0/P1이 남아 있는가?

다음 정기 audit 후보: **2026-05-30** 또는 decision record 5건 추가 시점 중 먼저 오는
때.

---

## 5. Supersede/Revoke/Amend 남용 방지

자기부정 record는 책임 회피 도구가 되면 안 된다. 따라서 다음 규칙이 필요하다.

- `supersede`, `revoke`, `amend` record는 반드시 이전 판단이 틀렸거나 불완전했던
  이유를 `failure_reason` 또는 동등한 필드로 남긴다.
- 같은 track에서 `supersede`/`revoke`/`amend`가 2회 발생하면 external audit trigger.
- 같은 track에서 3회 발생하면 track freeze. freeze 해제에는 별도 audit PASS가 필요하다.
- failed PASS가 발생하면 다음 같은 종류의 PASS 판정에는 이전 실패 재발 방지 항목을
  review 기준에 추가한다.

---

## 6. Meta-Work Ratio Reflection

현재 6 commit stack은 두 트랙이 교차했다.

| 트랙 | commit |
|---|---|
| 기기-17 A-track 본작업 | `b69ab80`, `d450f67` |
| supervisor layer 메타작업 | `02f7f4b`, `dd20392`, `f227249`, `b69e42c` |

비율은 본작업 2 / 메타작업 4다. layer 도입 cycle에서는 한 번 허용 가능한 비용이지만,
다음 cycle부터 이 비율이 유지되면 layer가 자기증식하는 문서가 된다.

운영 기준:

- 다음 trap-map task cycle에서는 supervisor layer 관련 commit이 본작업 commit보다 많아지면
  audit trigger.
- 단, layer 자체 변경을 목적으로 한 cycle은 예외로 두되, 그 경우 active-state에 예외 사유를
  명시한다.
- supervisor layer는 작업을 늘리는 장치가 아니라 stale과 forbidden-scope 위반을 줄이는
  장치여야 한다.

---

## 7. 현재 종합 판정

- 방향성: ACCEPT.
- `f227249` hardening: 구조적 보강의 뼈대는 PASS.
- 남은 보강: 첫 audit cycle, supersede 남용 방지, 메타작업 비율 reflection을 명시해야
  push-readiness로 갈 수 있음.
- push: 이 evidence/safeguard 보강 후에도 별도 push-readiness review 전까지 보류.

---

## Status

- G-1 hardening evidence pack 작성.
- G-2 first external audit cycle 명시.
- G-3 meta-work ratio self-reflection 기록.
- 다음 단계: audit protocol / active decision record에 safeguard 반영 후 review.
