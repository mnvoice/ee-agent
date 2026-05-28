# Development Turning Point Policy v0.1

작성일: 2026-05-28  
작성 목적: ee-agent 진행 중 종착점, MVP 범위, 과목 우선순위, 비용 모델, 문서화 전략처럼 장기 판단에 영향을 주는 논의가 발생했을 때 이를 기록하고 재사용하기 위한 정책 초안.

## 0. 정책 결론

이 정책은 개발 방향을 바꾸기 위한 정책이 아니다.

이 정책의 목적은 다음과 같다.

- 중요한 판단이 대화 속에서 사라지지 않게 한다.
- 시간이 지난 뒤에도 왜 그 판단을 했는지 복원할 수 있게 한다.
- MVP와 확장 목표를 분리한다.
- 측정 사실과 추정을 분리한다.
- 현재 후순위와 영구 제외를 분리한다.
- 문서화가 개발을 압도하지 않게 한다.

핵심 원칙:

```text
큰 판단은 구현보다 먼저 기록한다.
단, 기록이 구현 흐름을 과도하게 막아서는 안 된다.
```

## 1. 정책이 필요한 이유

ee-agent는 일반 앱 개발과 다르다.

앞면에는 전기기사 학습 PWA가 있고, 뒷면에는 verify-agent governance 방법론이 있다. 이 때문에 단순 기능 구현뿐 아니라 다음 판단들이 반복적으로 발생한다.

- 어디까지 만들면 MVP인가?
- 어떤 과목을 먼저 다룰 것인가?
- 어떤 작업은 왜 후순위인가?
- gate 반복을 어디까지 허용할 것인가?
- 문서화는 어느 정도까지 해야 하는가?
- 기간과 토큰 비용은 어떻게 예측할 것인가?
- 추정과 측정을 어떻게 구분할 것인가?

이 판단들이 기록되지 않으면 시간이 지난 뒤 다음 문제가 생긴다.

- 같은 논의를 다시 반복한다.
- 후순위 판단이 제외 판단으로 오해된다.
- MVP와 full expansion이 섞인다.
- 문서화가 본 개발보다 커진다.
- 비용 추정이 근거 없는 감각으로 남는다.
- 외부 설명 시 현재 상태와 목표를 명확히 말하기 어렵다.

따라서 turning point 기록 정책이 필요하다.

## 2. 적용 범위

이 정책은 다음 논의가 발생할 때 적용한다.

- project endpoint 재정의
- MVP scope 변경 또는 명확화
- subject priority 결정
- 특정 과목 후순위 또는 제외 판단
- cost/time/token model 논의
- documentation strategy 논의
- gate 단위 확대/축소 논의
- architecture layer 재정의
- verification/governance 원칙 변경

## 3. Turning Point Record Trigger

다음 조건 중 하나라도 충족하면 Turning Point Record를 작성한다.

1. "마무리", "종착점", "MVP", "끝"의 의미가 새로 정리됨
2. 과목 우선순위가 바뀌거나 후순위 이유가 생김
3. 일정 또는 토큰 비용을 역산하려는 논의가 발생함
4. 문서화 구조 또는 SRS 구조가 새로 제안됨
5. 기존 gate 흐름을 계속할지 방향을 바꿀지 고민함
6. 외부 설명용 또는 장기 보존용 판단이 필요함
7. 사용자가 "나중에 이 이유를 알아야 한다"고 명시함

## 4. 정책으로 승격할 항목

### 4.1 Turning Point Record Policy

종착점, MVP 범위, 비용 모델, 과목 우선순위, 문서화 전략이 새로 정리되면 Turning Point Record를 남긴다.

필수 기록:

- 논의가 발생한 이유
- 당시 상태
- 선택지
- 채택한 방향
- 채택하지 않은 방향
- 나중에 재검토할 조건
- 아직 말하면 안 되는 claim

### 4.2 Subject Priority Rationale Policy

과목 우선순위를 정할 때는 반드시 이유와 재검토 조건을 함께 기록한다.

필수 구분:

- 우선 포함
- 후순위
- 현재 제외
- 영구 제외

현재 사례:

전기자기학은 중요도가 낮아서 제외된 것이 아니다. 수식/도형/물리 개념 해설 검증 난이도와 MVP scope 증가 위험 때문에 MVP 1차 후보에서 후순위로 둔다.

### 4.3 MVP vs Expansion Boundary Policy

MVP와 full expansion을 분리해서 기록한다.

MVP:

- 사용자가 실제로 써볼 수 있는 최소 의미 단위
- 3개 과목 기준 가능
- PWA runtime 확인 포함
- 자동화/gate 패턴이 다음 과목으로 복제 가능해야 함

Expansion:

- 6과목 전체 확장
- PDF figure track 보강
- 추가 subject audit
- 방법론 이식

MVP를 full expansion과 섞지 않는다.

### 4.4 Measured vs Estimated Cost Boundary Policy

기간, 토큰, 비용은 측정값과 추정값을 분리한다.

표기 예:

- 측정: gate 하나가 실제로 8분 28초 걸림
- 관찰: 사용자가 gate 1개 약 9분 체감
- 추정: MVP까지 35~70 gates
- 산식: gate 수 × gate당 평균 시간

추정값은 확정값으로 쓰지 않는다.

### 4.5 Documentation Weight Control Policy

좋은 문서 구조가 떠올라도 즉시 여러 문서로 분리하지 않는다.

원칙:

- 먼저 단일 기준 문서로 저장한다.
- 정보 구조는 다층으로 잡는다.
- 파일 분리는 필요해질 때 진행한다.
- 문서화가 본 개발 흐름을 압도하지 않게 한다.

현재 채택:

- 6층 구조는 정보 구조로 채택
- 즉시 6개 문서 작성은 보류
- `ee_agent_development_spec_v0.1.md` 같은 단일 기준 문서로 시작

## 5. 아직 정책으로 승격하지 않을 항목

### 5.1 gate_metrics.jsonl mandatory 기록

아직 mandatory로 승격하지 않는다.

이유:

- 매 gate마다 기록 부담이 증가한다.
- 사용자가 이미 gate 반복 피로를 느끼고 있다.
- 자동화 전 수동 기록은 마찰이 크다.

현재 상태:

- 후속 자동화 후보
- 큰 gate에 한해 수동 기록 가능
- v0.2 이후 Cost Metrics Gate에서 재검토

### 5.2 MVP 과목 3개 영구 확정

아직 정책으로 확정하지 않는다.

현재 상태:

- 전력공학 + 전기기기 + 전기설비기술기준은 권장 MVP 조합
- 사용자 결정과 추가 데이터 검토가 필요함
- 전기자기학 재진입 가능성 유지

### 5.3 전기자기학 후순위 영구화

전기자기학 후순위는 영구 정책이 아니다.

현재 상태:

- MVP 1차 후보에서 후순위
- 재검토 조건이 충족되면 포함 가능

재검토 조건:

- 수식/도형 해설 검증 체계 마련
- 전기자기학 sample audit 통과
- MVP 과목 수 확대
- 사용자 가치 우선순위 변경

### 5.4 6층 SRS 파일 구조 강제

6층 구조는 정보 구조로 채택하지만 파일 구조로 강제하지 않는다.

현재 상태:

- Vision
- Domain Model
- Process Specification
- Architecture
- Cost Model
- Verification Catalog

위 6층은 단일 문서 안의 chapter로 먼저 운영한다.

## 6. Turning Point Record Template

새 Turning Point Record는 다음 구조를 따른다.

```text
# [Topic] Turning Point Record v0.x

작성일:
관련 gate:
관련 commit:

## 1. 논의가 발생한 이유

## 2. 당시 상태

## 3. 선택지

## 4. 채택한 방향

## 5. 채택하지 않은 방향과 이유

## 6. 정책으로 승격할 항목

## 7. 정책으로 승격하지 않을 항목

## 8. 재검토 조건

## 9. 아직 말하면 안 되는 claim

## 10. 다음 자연 gate
```

## 7. Claim Boundary

이 정책이 주장하는 것:

- 중요한 장기 판단은 기록해야 한다.
- 과목 후순위 판단은 이유와 재검토 조건을 포함해야 한다.
- MVP와 full expansion은 분리해야 한다.
- 측정값과 추정값은 분리해야 한다.
- 문서화는 본 개발을 보조해야 하며 본 개발을 압도하면 안 된다.

이 정책이 주장하지 않는 것:

- 모든 대화를 문서화해야 한다는 주장
- 모든 gate마다 metrics JSONL을 써야 한다는 주장
- MVP 과목 3개가 영구 확정되었다는 주장
- 전기자기학이 제외되었다는 주장
- 6층 SRS 파일을 즉시 모두 만들어야 한다는 주장
- 이 정책이 Instance v0.2 흐름을 중단시킨다는 주장

## 8. 현재 사례에 대한 적용

현재 turning point:

- 사용자가 ee-agent 개발 요구조건과 SRS 역산을 요청함
- Claude Web이 6층 SRS 구조를 제안함
- Codex 감독관이 이를 검토하고 보정함
- 전기자기학이 MVP 1차 후보에서 왜 후순위인지 기록 필요성이 발생함

현재 생성된 기록:

- `ee_agent_development_spec_v0.1.md`
- `ee_agent_srs_multilayer_review_v0.1.md`
- `development_turning_point_policy_v0.1.md`

현재 정책 판단:

- Turning point 기록 필요
- 그러나 실제 개발 흐름은 Instance v0.2 Implementation Gate로 계속 진행
- 이 문서들은 방향 전환이 아니라 판단 보존 목적

## 9. 다음 권장 gate

후보: Development Turning Point Record Review Gate  
단일 목적: 위 3개 문서가 repo 산출물로 편입 가능한지 read-only 검토

후보: Development Turning Point Record Commit Gate  
단일 목적: review 통과 후 위 3개 문서만 commit

후보: Instance v0.2 Implementation Gate  
단일 목적: 실제 개발 흐름으로 복귀하여 `policy_change_rules_v0.2_draft_instance.json` 신규 작성

감독관 권장:

위 3개 문서는 repo에 보존할 가치가 있다. 단, 본 기록 편입은 개발 방향 전환이 아니라 특이점 기록이다. 따라서 짧은 review/commit/push 후 Instance v0.2 Implementation Gate로 복귀하는 것이 가장 적합하다.

