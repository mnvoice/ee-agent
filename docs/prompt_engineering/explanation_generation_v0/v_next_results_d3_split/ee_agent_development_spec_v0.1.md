# ee-agent Development Specification v0.1

작성일: 2026-05-28  
작성 목적: ee-agent 개발 목표, 아키텍처, 검증 절차, 일정 역산, 토큰/비용 역산, MVP 범위 판단 근거를 하나의 기준 문서로 보존한다.

## 0. 문서 성격

이 문서는 새 기능 구현 문서가 아니다. 지금까지의 schema-first governance 흐름, gate 기록, validator 작성, profile/instance migration, L7 policy decision, profile v0.2 boost 과정을 근거로 ee-agent의 개발 요구조건을 재구성한 기준 문서다.

이 문서는 다음 질문에 답하기 위해 작성한다.

- ee-agent의 제품 목표는 무엇인가?
- ee-agent의 방법론 목표는 무엇인가?
- MVP의 종착점은 어디인가?
- 어떤 과목을 먼저 포함하고, 어떤 과목은 왜 후순위로 두는가?
- 개발 아키텍처는 어떤 층으로 나뉘는가?
- gate 단위로 어떻게 진행 상황을 확인하는가?
- 남은 기간과 토큰/비용은 어떻게 역산하는가?
- 시간이 지난 뒤에도 당시 판단을 복원할 수 있는가?

## 1. ee-agent의 이중 목표

ee-agent는 두 가지 목표를 동시에 가진다.

### 1.1 앞면: 전기기사 학습 PWA

사용자 관점의 목표는 전기기사 시험 준비용 PWA다.

핵심 기능:

- 6과목 문항 풀이
- 해설 읽기
- 과목별 학습 흐름
- 모바일 및 PWA 사용성
- 사용자 관점에서 신뢰 가능한 문제/해설/도형 표시

### 1.2 뒷면: verify-agent 방법론 실증

방법론 관점의 목표는 verify-agent 패턴의 첫 실증이다.

핵심 기능:

- ITEM_POLICY
- selector
- rule schema
- profile catalog
- schema validator
- migration log
- audit report
- claim boundary
- design/review/commit/push gate
- 다른 프로젝트로 이식 가능한 governance pattern

## 2. 현재 상태

본 문서 작성 시점의 기준 상태:

- branch: `feat/phase-b-migration`
- latest remote HEAD: `0799544`
- 본 세션 흐름 산출물: 15종 원격 보존 완료
- profile v0.2 draft 원격 보존 완료
- instance v0.2는 아직 작성 전
- validator v0.2 run은 아직 수행 전

### 2.1 완료된 큰 축

- Metadata layer: 5,331 문항 v2 변환 완료로 알려져 있음
- Rule schema draft 작성
- EE-agent rule profile v0.1 작성
- Schema validator 설계/결정/구현
- Validator baseline run
- v0.2 원천 규칙 12개를 v0.1-draft instance로 migration
- L7 policy decision 작성
- Profile catalog boost design 작성
- Profile v0.2 draft 작성

### 2.2 아직 남은 큰 축

- Instance v0.2 작성
- Profile v0.2 + instance v0.2 validator run
- Threshold 확정
- L7 review_later 후속 정책
- Subject별 ITEM_POLICY 확장
- Subject별 explanation generation
- PWA runtime risk track
- PDF figure track
- MVP release validation

## 3. 개발 목표 정의

### 3.1 1차 종착점: MVP critical mass

ee-agent의 1차 종착점은 모든 과목의 완전한 최종본이 아니다. 1차 종착점은 다음 조건을 만족하는 MVP critical mass다.

- 3개 과목이 사용자에게 의미 있게 작동한다.
- 해당 과목의 ITEM_POLICY, selector, generation, audit 흐름이 재현 가능하다.
- PWA runtime smoke test가 완료되어 실제 사용 가능성이 확인된다.
- schema/profile/validator/gate 방법론이 다음 과목으로 이식 가능하다.
- 남은 3개 과목은 새 구축이 아니라 확장 작업으로 분류할 수 있다.

### 3.2 2차 목표: 6과목 확장

2차 목표는 6과목 전체 확장이다.

이 단계는 MVP 이후 확장 목표다. 이를 1차 종착점으로 잡으면 반복 gate가 너무 많아져 전체 작업의 끝이 보이지 않는다.

### 3.3 3차 목표: verify-agent pattern extraction

3차 목표는 ee-agent에서 검증된 구조를 다른 프로젝트로 이식 가능한 패턴으로 추출하는 것이다.

후보 이식 대상:

- react-confidence
- NACHI venture
- 기타 rule/profile/validator 기반 agent 프로젝트

## 4. MVP 과목 구성 판단

### 4.1 권장 MVP 과목

현재 기준 권장 MVP 과목:

1. 전력공학
2. 전기기기
3. 전기설비기술기준

이 조합은 확정된 제품 정책이 아니라 현재 gate history와 작업 효율 관점의 권장안이다.

### 4.2 전기자기학이 빠진 이유

전기자기학은 중요도가 낮아서 빠진 것이 아니다. MVP 1차 후보에서 후순위로 둔 것이다.

판단 이유:

1. 전기자기학은 수식, 개념 구조, 단위, 물리 직관 의존도가 높다.
2. 단순 키워드 기반 해설 생성보다 오답 위험이 크다.
3. 도형, 벡터, 장(field), 플럭스, 전위, 유전체, 자기회로 등 시각적/수학적 설명 품질이 중요하다.
4. 해설 품질 검증 기준이 전력공학이나 설비기준보다 더 까다로울 가능성이 높다.
5. MVP에서는 사용자에게 빠르게 체감되는 작동 상태를 만드는 것이 우선이며, 전기자기학은 품질 기준을 낮추고 빠르게 넣기보다 별도 품질 track으로 다루는 편이 안전하다.
6. 전기자기학을 먼저 넣으면 PDF figure track, 수식 표현, 해설 검증 기준이 동시에 열릴 가능성이 있어 MVP scope가 커진다.
7. 현재 D-3 흐름은 전력공학 기반으로 정교화되어 있으며, 다음 과목은 이 패턴을 빠르게 복제할 수 있는 쪽이 일정 예측에 유리하다.

따라서 전기자기학은 제외가 아니라 다음 상태로 기록한다.

상태: MVP 1차 후보에서는 후순위  
이유: 중요도 부족이 아니라 검증 난이도와 scope 증가 위험  
재검토 조건: 수식/도형/물리 개념 해설 검증 체계가 마련되거나, MVP 과목 구성을 4과목 이상으로 확대할 때

### 4.3 전기자기학 재진입 조건

전기자기학은 다음 조건 중 하나가 충족되면 MVP에 다시 포함할 수 있다.

- 전기자기학 문항 중 도형/수식 의존도가 낮은 subset을 먼저 분리할 수 있음
- figure crop/수식 rendering 검증 track이 안정됨
- 전기자기학 전용 ITEM_POLICY가 소규모 샘플에서 audit 통과함
- 사용자가 MVP 과목을 3개에서 4개로 확대하기로 결정함
- 전기자기학이 실제 시험 준비 사용자 가치에서 우선순위가 더 높다고 판단됨

### 4.4 기록 이유

이 판단을 문서에 남기는 이유는 시간이 지난 뒤 다음 오해를 막기 위해서다.

- 전기자기학을 잊어버렸다는 오해
- 전기자기학의 중요도를 낮게 봤다는 오해
- MVP 범위가 임의로 정해졌다는 오해
- 빠른 출시와 품질 검증 사이의 trade-off가 기록되지 않는 문제

본 문서는 전기자기학을 후순위로 둔 이유를 보존하여, 이후 다시 과목 우선순위를 정할 때 정확한 판단을 가능하게 한다.

## 5. 소프트웨어 아키텍처

### 5.1 Data Layer

책임:

- 원천 문항
- metadata v2
- 과목 분류
- 문항 id
- PDF/figure linkage
- generated explanation 결과

주요 산출물:

- `questions.json`
- subject별 input/result/audit 파일
- figure crop 결과

### 5.2 Policy Layer

책임:

- ITEM_POLICY
- subject별 selector rule
- rule schema
- profile catalog
- threshold proposal
- L7/L8 policy

주요 산출물:

- `rule_schema_v0.1_draft.schema.json`
- `ee_agent_rule_profile_v0.1_draft.json`
- `ee_agent_rule_profile_v0.2_draft.json`
- policy decision documents

### 5.3 Generation Layer

책임:

- 해설 생성
- prompt/input 구성
- generation result 생성
- model output 정리

주요 산출물:

- subject별 generation input
- subject별 generation result
- synthesis report

### 5.4 Validation Layer

책임:

- schema/profile/instance 검증
- L1~L8 cross-check
- report_only 분류
- audit report 생성
- claim boundary 확인

주요 산출물:

- `scripts/schema_validator.py`
- validation report JSON
- audit report MD

### 5.5 Runtime Layer

책임:

- PWA 실행
- 문항 렌더링
- 해설 렌더링
- 모바일 사용성
- offline/cache 동작

주요 검증:

- local server smoke test
- browser rendering
- mobile viewport
- installability
- navigation and question flow

### 5.6 Governance Layer

책임:

- gate 진행
- review
- commit/push 분리
- protected area 보존
- claim boundary 유지
- 기록 가능한 decision 생성

주요 gate:

- Design Gate
- Review Gate
- Commit Gate
- Push Gate
- Implementation Gate
- Run Gate
- Migration Gate
- Decision Gate
- Revision Gate

## 6. Gate Model

### 6.1 기본 gate 규칙

각 gate는 다음 항목을 가져야 한다.

- 단일 목적
- 변경 가능 영역
- 절대 금지 영역
- 성공 판정
- 아직 말하면 안 되는 claim
- 다음 자연 gate

### 6.2 gate 유형별 역할

Design Gate:
요구사항, 정책, 설계, 미확정 사항을 문서화한다.

Review Gate:
read-only로 commit 가능 여부를 검토한다.

Commit Gate:
정해진 파일만 staging하고 single commit을 만든다.

Push Gate:
정해진 commit만 원격에 보존한다.

Implementation Gate:
설계에 따라 신규 구현 또는 신규 산출물을 작성한다.

Run Gate:
도구나 validator를 실행하고 결과를 audit으로 남긴다.

Migration Gate:
기존 자료를 새 schema/profile/instance 구조로 변환한다.

Decision Gate:
정책 결정 또는 unresolved 처리를 문서화한다.

Revision Gate:
기존 산출물을 새 버전으로 보강한다.

## 7. 남은 작업 분해

### 7.1 가까운 순서

1. Instance v0.2 Implementation Gate
2. Instance v0.2 Review Gate
3. Instance v0.2 Commit Gate
4. Instance v0.2 Push Gate
5. Validator Run Gate v0.2
6. Validator Run Review/Commit/Push
7. MVP Roadmap Decision Gate
8. Subject 2 ITEM_POLICY Gate
9. Subject 2 selector/generation/audit gates
10. Subject 3 ITEM_POLICY Gate
11. Subject 3 selector/generation/audit gates
12. PWA Runtime Risk Gate
13. MVP Release Readiness Gate

### 7.2 독립 후속 후보

- Threshold Confirm Gate
- L7 review_later policy revision
- Validator boundary N1 revision
- PDF figure track
- 전기자기학 re-entry decision

## 8. 일정 역산 모델

### 8.1 gate 단위 시간 관찰

현재 관찰된 gate 시간:

- 작은 review/push gate: 약 1~3분
- 중간 design/review gate: 약 2~5분
- implementation gate: 약 3~9분
- migration gate: 약 8~10분
- 사용자가 언급한 평균 체감: gate 1개 약 9분

안전한 planning 기준:

- 일반 gate 평균: 5분
- 복잡 gate 평균: 9분
- review/commit/push 3종 묶음: 6~12분
- 큰 implementation + review + commit + push 묶음: 15~30분

### 8.2 MVP까지 gate 수 추정

MVP 3과목 기준 남은 작업은 다음처럼 추정한다.

Profile/instance v0.2 마무리:

- instance v0.2 작성/검토/commit/push: 4 gates
- validator run v0.2/report/commit/push: 4~5 gates

Subject 2:

- ITEM_POLICY design/review/commit/push: 4 gates
- selector/run/audit/commit/push: 4~6 gates
- explanation generation/audit/commit/push: 4~6 gates

Subject 3:

- Subject 2와 유사: 12~16 gates

PWA runtime MVP:

- runtime smoke design/run/review/fix/commit/push: 5~10 gates

총 추정:

- 낙관: 35 gates
- 기준: 50 gates
- 보수: 70 gates

### 8.3 기간 추정

gate당 9분 기준:

- 35 gates: 315분, 약 5.25시간
- 50 gates: 450분, 약 7.5시간
- 70 gates: 630분, 약 10.5시간

현실 보정:

- 실제 calendar 기간은 gate 실행 시간보다 길다.
- 중간 판단, 피로, 재검토, 오류 수정, 문맥 복원 시간이 추가된다.
- 하루 60~90분 집중 기준이면 MVP까지 약 2~4주가 현실적이다.
- 하루 2~3시간 집중 기준이면 약 1~2주까지 단축 가능하다.

## 9. 토큰/비용 역산 모델

### 9.1 전제

토큰 비용은 모델, 입력 길이, 출력 길이, 재시도 횟수, 첨부 문서 크기에 따라 변한다. 이 문서는 특정 모델 단가를 고정하지 않고 산식으로 보존한다.

### 9.2 gate별 토큰 모델

각 gate의 토큰 사용량:

```text
gate_tokens =
  input_context_tokens
  + referenced_artifact_tokens
  + reasoning_tokens
  + output_report_tokens
  + retry_tokens
```

비용:

```text
gate_cost =
  input_tokens * input_price_per_token
  + output_tokens * output_price_per_token
```

전체 비용:

```text
total_cost =
  sum(gate_cost)
  + rerun_cost
  + failed_gate_cost
  + review_overhead_cost
```

### 9.3 gate 유형별 상대 비용

낮음:

- Push Gate
- Commit Gate
- 단순 Review Gate

중간:

- Design Gate
- Policy Decision Gate
- Run Report Review Gate

높음:

- Implementation Gate
- Migration Gate
- Explanation Generation Gate
- PWA Runtime Debug Gate

매우 높음:

- 과목 전체 generation
- 대량 문항 audit
- figure extraction/review
- 긴 context 기반 architecture rewrite

### 9.4 비용 절감 전략

- gate report template 고정
- Review Gate 질문 목록 재사용
- commit/push gate 자동화
- validator JSON report 중심으로 사람이 읽는 MD 최소화
- subject별 반복 gate를 batch 단위로 묶기
- claim boundary는 template화
- 큰 context를 매번 붙이지 않고 source artifact path만 참조
- MVP 이후 6과목 확장 시 subject template 재사용

## 10. MVP 요구조건

### 10.1 Product Requirements

MVP 사용자는 다음을 할 수 있어야 한다.

- 선택된 3개 과목의 문제를 볼 수 있음
- 문제별 해설을 볼 수 있음
- 모바일 브라우저에서 학습 가능
- 기본 navigation이 깨지지 않음
- 누락/오류가 audit에 기록되어 있음

### 10.2 Data Requirements

- metadata v2가 유지됨
- subject 분류가 명시됨
- generation input/result가 추적 가능함
- audit result가 commit 단위로 보존됨
- figure 의존 문항은 상태가 명시됨

### 10.3 Governance Requirements

- gate 단위로 변경됨
- commit과 push는 분리됨
- protected area가 gate마다 명시됨
- claim boundary가 문서마다 포함됨
- read-only review가 implementation/commit보다 먼저 수행됨

### 10.4 Automation Requirements

- selector가 반복 가능해야 함
- explanation generation이 subject 단위로 재실행 가능해야 함
- validator가 schema/profile/instance를 검증해야 함
- audit report가 사람이 검토 가능한 형식이어야 함

## 11. Claim Boundary

이 문서가 주장하는 것:

- ee-agent는 제품 목표와 방법론 목표를 함께 가진다.
- MVP 1차 종착점은 3과목 + 자동화 체계 + PWA runtime 확인으로 정의하는 것이 현실적이다.
- 전기자기학은 제외가 아니라 MVP 1차 후보에서 후순위로 둔 것이다.
- 전기자기학 후순위 판단 이유는 품질 검증 난이도와 scope 증가 위험이다.
- 일정과 비용은 gate 수와 gate당 평균 시간/토큰으로 역산해야 한다.

이 문서가 주장하지 않는 것:

- 전기자기학이 중요하지 않다는 주장
- MVP 과목 구성이 영구 확정되었다는 주장
- 6과목 전체 완료가 불필요하다는 주장
- 토큰/비용 단가가 확정되었다는 주장
- 현재 산식이 실제 청구 비용과 동일하다는 주장
- profile v0.2 이후 모든 unresolved가 해소되었다는 주장

## 12. 다음 권장 gate

이 문서를 공식 산출물로 편입하려면 다음 gate가 필요하다.

후보: Development Specification Review Gate  
단일 목적: 본 문서가 commit 가능한 기준 문서인지 read-only 검토

후보: Development Specification Commit Gate  
단일 목적: review 통과 후 본 문서 1건만 commit

후보: Development Specification Push Gate  
단일 목적: commit 후 원격 보존

단, 현재 실제 개발 흐름의 자연 후속은 Instance v0.2 Implementation Gate다. 따라서 이 문서는 제품/방법론 기준 문서로 별도 보존하거나, v0.2 instance 이후 MVP Roadmap Decision Gate의 입력 자료로 사용할 수 있다.

