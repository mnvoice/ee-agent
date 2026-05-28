# ee-agent SRS Multilayer Review v0.1

작성일: 2026-05-28  
작성 목적: Claude Web이 제안한 "역방향 개발문서 / 6층 SRS 구조"를 감독관 관점에서 검토하고, 동의점·부족점·반박·채택안을 기록한다.

## 0. 결론

Claude Web의 핵심 판단은 대체로 맞다.

ee-agent는 일반적인 단일 SRS 문서 하나로 정리하기 어렵다. 사용자에게 보이는 PWA와, 내부에서 작동하는 verify-agent governance 방법론이 동시에 존재하기 때문이다. 따라서 Vision, Domain Model, Process Specification, Architecture, Cost Model, Verification Catalog를 분리해 다층 구조로 정리해야 한다는 제안은 타당하다.

그러나 Claude Web의 제안에는 중요한 부족점도 있다.

가장 큰 부족점은 현재 진행된 실제 gate history와 산출물 상태를 충분히 반영하지 못했다는 점이다. 특히 이미 schema/profile/validator/migration/L7 policy/profile boost/profile v0.2까지 진행된 현재 상태에서는 "SRS를 새로 1~2주 동안 정리한다"는 접근이 너무 무겁다. 지금 필요한 것은 새 프로젝트처럼 문서 체계를 처음 세우는 일이 아니라, 이미 누적된 gate 산출물을 근거 자료로 묶고, MVP 판단과 비용 모델을 갱신 가능한 형태로 고정하는 일이다.

감독관 채택안:

- 단일 표준 SRS는 부적합하다.
- 6층 구조는 채택한다.
- 단, 1~2주 문서화 sprint가 아니라 "핵심 기준 문서 1개 + 필요 시 부속 문서 확장" 방식으로 시작한다.
- Cost Model은 확정값이 아니라 측정 누적 모델로 둔다.
- gate_metrics는 유용하지만, 지금 당장 mandatory로 도입하면 작업 마찰이 커지므로 "선택적 도입 후 자동화 후보"로 둔다.
- ee-agent의 1차 종착점은 6과목 완벽 완료가 아니라 MVP critical mass다.

## 1. Claude Web 제안 요약

Claude Web의 제안은 다음과 같다.

1. 지금 필요한 것은 역방향 개발문서 작성이다.
2. 일반 SRS 하나로는 부족하다.
3. ee-agent는 앞면 PWA와 뒷면 verify-agent 방법론을 동시에 가진다.
4. 문서는 6층 구조가 적합하다.
5. 6층은 Vision, Domain Model, Process Specification, Architecture, Cost Model, Verification Catalog다.
6. Cost Model은 현재 정확히 산출하기 어렵고 측정 누적이 필요하다.
7. 작성은 2단계로 나눈다.
8. 1단계는 기존 자산 정리, 2단계는 비용 측정 누적이다.
9. SRS 작성 자체도 gate 방식으로 진행한다.
10. 우선 Vision Document부터 작성한다.

## 2. 동의하는 부분

### 2.1 역방향 개발문서라는 정의

동의한다.

현재 ee-agent는 개발 전에 요구사항을 쓰는 상태가 아니다. 이미 여러 번의 gate, review, migration, validator 구현을 거친 뒤다. 따라서 일반적인 forward SRS보다, 지금까지의 실제 작업을 근거로 개발 목표와 구조를 재구성하는 reverse specification 방식이 적합하다.

### 2.2 단일 SRS로 부족하다는 판단

동의한다.

ee-agent에는 최소 세 층이 있다.

- Product: 전기기사 학습 PWA
- Data/Content: 문항, metadata, 해설, figure
- Governance/Methodology: schema, profile, validator, gate, claim boundary

일반 SRS는 Product 기능 요구사항에는 강하지만, Governance/Methodology를 충분히 담기 어렵다.

### 2.3 Cost Model은 측정 누적이 필요하다는 판단

동의한다.

토큰 비용과 제작 기간은 한 번에 확정할 수 없다. gate 유형, 모델, 입력 길이, 산출물 크기, review 반복 횟수에 따라 달라진다. 따라서 현재는 산식과 추정 모델을 먼저 만들고, 이후 gate별 측정치를 누적해야 한다.

### 2.4 SRS 작성 자체를 gate로 관리하자는 제안

동의한다.

문서 작성도 governance 산출물이므로 다음을 지켜야 한다.

- 단일 목적
- 변경 가능 영역
- 절대 금지 영역
- review
- commit
- push
- claim boundary

## 3. 부족한 부분

### 3.1 현재 실제 산출물 상태 반영 부족

Claude Web은 정보가 제한되어 있어 현재 상태를 충분히 반영하지 못했다.

현재는 단순히 D-3 도중이 아니다. 이미 다음 산출물이 원격 보존되었다.

- rule schema draft
- profile v0.1
- schema validator design
- schema validator implementation decision
- schema validator implementation
- validator baseline run
- v0.1 instance migration
- L7 policy decision
- profile catalog boost design
- profile v0.2 draft

따라서 "이제 SRS 1단계 정리를 1~2주 진행"이라는 제안은 현재 속도와 산출물 누적 상태에 비해 무겁다.

### 3.2 6층 문서 분리의 비용 과소평가

6개 문서를 각각 gate로 작성하면 다음 gate가 추가된다.

- Vision 작성/review/commit/push
- Domain Model 작성/review/commit/push
- Process Spec 작성/review/commit/push
- Architecture 작성/review/commit/push
- Verification Catalog 작성/review/commit/push
- Cost Model 작성/review/commit/push

최소 24 gates다.

gate 1개를 5~9분으로 보면, 문서 정리만 2~4시간 이상이다. 실제로는 자료 탐색과 판단 시간이 더 들어간다. 이 정도면 현재 instance v0.2와 MVP 진입을 늦출 수 있다.

따라서 6층 구조는 정보 구조로 채택하되, 파일을 처음부터 6개로 쪼개는 것은 보류하는 편이 낫다.

### 3.3 Cost Model을 너무 독립 작업처럼 다룸

Claude Web은 `gate_metrics.jsonl`을 별도 누적 파일로 제안했다. 방향은 좋지만, 바로 mandatory로 도입하면 작업 마찰이 크다.

현재 사용자는 이미 gate 반복 피로를 느끼고 있다. 이 시점에 모든 gate마다 metrics 작성까지 추가하면 피로가 늘어날 수 있다.

더 나은 방식:

- v0.1: 문서 안에 추정 산식과 관찰값만 기록
- v0.2: 중요한 gate만 수동 metrics 기록
- v0.3: 자동화 가능한 형태가 되면 JSONL 도입

### 3.4 Architecture 층의 범위가 흐림

Claude Web은 Architecture에 app/index.html, scripts, paste-bridge, TCC 제약을 넣었다. 이 중 일부는 맞지만, ee-agent architecture의 핵심은 단순 파일 구조가 아니다.

더 중요한 architecture는 다음이다.

- Data Layer
- Policy Layer
- Generation Layer
- Validation Layer
- Runtime Layer
- Governance Layer

TCC, paste-bridge 같은 운영 제약은 architecture 본문이 아니라 "Operational Constraints" 또는 "Environment Constraints"로 분리하는 편이 낫다.

### 3.5 MVP 과목 판단 근거가 약함

Claude Web은 MVP 3과목 후보를 말했지만, 전기자기학이 왜 빠졌는지를 충분히 설명하지 않았다.

이 판단은 반드시 문서화되어야 한다.

전기자기학은 중요도가 낮아서 제외된 것이 아니다. 해설 검증 난이도, 수식/도형 의존성, scope 증가 위험 때문에 MVP 1차 후보에서 후순위로 둔 것이다.

이유를 기록하지 않으면 시간이 지난 뒤 다음 오해가 생긴다.

- 전기자기학을 잊었다는 오해
- 전기자기학 중요도를 낮게 봤다는 오해
- MVP 범위가 즉흥적으로 정해졌다는 오해

## 4. 반박

### 4.1 "1단계 정리 1~2주"에 대한 반박

반박:

현재 필요한 것은 1~2주짜리 문서화 sprint가 아니다. 이미 gate 산출물이 충분히 누적되어 있으므로, 먼저 하나의 기준 문서로 핵심 결정을 고정하고, 나머지 층은 필요할 때 분화하는 편이 낫다.

수정안:

- 먼저 `ee_agent_development_spec_v0.1.md` 단일 문서로 시작한다.
- 그 안에 6층 구조를 chapter로 포함한다.
- 나중에 문서가 커지면 chapter를 별도 문서로 분리한다.

### 4.2 "층마다 gate로 PASS"에 대한 반박

반박:

원칙은 맞지만 지금 모든 층을 각각 gate로 나누면 문서화가 본 개발을 압도할 수 있다.

수정안:

- 중요한 기준 문서 1개만 Review/Commit/Push gate를 거친다.
- Vision/Process/Cost 등은 같은 문서 안에서 v0.1 수준으로 통합한다.
- 외부 제출 또는 방법론 이식이 필요해질 때 6층 분리를 수행한다.

### 4.3 "Cost Model 정확도 중요"에 대한 반박

반박:

외부 제출용이면 정확도가 중요하지만, 현재 사용자의 1차 목적은 내부 정렬과 피로 감소다. 그러므로 지금은 정확한 토큰 비용보다 "비용이 어떤 변수로 결정되는가"를 아는 것이 더 중요하다.

수정안:

- 현재는 비용 산식을 기록한다.
- gate당 시간 관찰값을 rough estimate로 기록한다.
- 실제 비용 정밀화는 후속 Cost Metrics Gate에서 진행한다.

### 4.4 "옵션 A/B 혼합"에 대한 보정

Claude Web은 사용자 목적을 옵션 B + A 혼합으로 추정했다. 대체로 맞지만, 감독관 판단으로는 다음 순서가 더 정확하다.

1. 내부 정렬용
2. 개발 통제용
3. 외부 설명용
4. 방법론 이식용

즉 외부 제출이 2순위가 아니라, 현재는 개발 통제와 자기 정렬이 먼저다.

### 4.5 "Vision Document 먼저"에 대한 보정

Vision만 먼저 쓰면 또 큰 그림만 있고 실행 통제는 약해질 수 있다.

현재 필요한 첫 문서는 Vision 단독이 아니라 다음을 함께 담은 기준 문서다.

- Vision
- MVP boundary
- Architecture
- Gate model
- Cost model
- Subject priority rationale

따라서 첫 문서는 `Vision Document`보다 `Development Specification`이 더 적합하다.

## 5. 감독관 채택 구조

### 5.1 채택할 6층 구조

6층 구조는 정보 구조로 채택한다.

| 층 | 채택 여부 | 보정 |
|---|---|---|
| Vision | 채택 | MVP critical mass 중심 |
| Domain Model | 채택 | questions/schema/profile/instance 포함 |
| Process Specification | 채택 | gate model과 claim boundary 중심 |
| Architecture | 채택 | Data/Policy/Generation/Validation/Runtime/Governance layer로 재정의 |
| Cost Model | 채택 | 확정값이 아니라 산식 + 측정 누적 |
| Verification Catalog | 채택 | validator/audit/self-catch/gate review 포함 |

### 5.2 현재 작성할 문서

현재는 다음 단일 문서가 적합하다.

```text
ee_agent_development_spec_v0.1.md
```

역할:

- 6층 구조를 하나의 기준 문서 안에 통합
- MVP 종착점 명시
- 전기자기학 후순위 이유 기록
- 일정/비용 역산 모델 기록
- gate model 기록
- 이후 분화 가능한 chapter 구조 제공

### 5.3 나중에 분리할 수 있는 부속 문서

필요해지면 다음 문서로 분리한다.

- `ee_agent_vision_v0.1.md`
- `ee_agent_domain_model_v0.1.md`
- `ee_agent_process_spec_v0.1.md`
- `ee_agent_architecture_v0.1.md`
- `ee_agent_cost_model_v0.1.md`
- `ee_agent_verification_catalog_v0.1.md`
- `gate_metrics.jsonl`

단, 지금 즉시 모두 만들지는 않는다.

## 6. 전기자기학 판단 보강

전기자기학은 MVP 1차 후보에서 빠졌지만, 이는 제외가 아니다.

감독관 기록:

전기자기학은 전기기사 시험에서 핵심 과목이다. 그러나 MVP 1차 범위에서는 다음 이유로 후순위가 타당하다.

- 개념 설명 난이도 높음
- 수식 기반 해설 품질 검증 필요
- 장, 전위, 유전체, 자기회로 등 물리 개념의 오답 위험 큼
- figure/PDF track과 결합될 가능성 있음
- 빠른 MVP 완성보다 품질 보존이 중요함
- 현재 D-3 governance 패턴은 전력공학에서 검증되었고, 다음 과목은 pattern replication이 쉬운 쪽이 일정 예측에 유리함

재진입 조건:

- 전기자기학 전용 ITEM_POLICY sample audit 통과
- 수식/도형 의존 문항 분리 가능
- figure track 안정화
- MVP 과목 수를 4개로 확대
- 사용자 가치 판단에서 전기자기학 우선순위가 상승

## 7. 개발 일정과 비용 판단

### 7.1 gate 시간

현재 관찰:

- 사용자가 체감한 gate 1개 시간: 약 9분
- 작은 push/review: 1~3분
- 큰 migration/implementation: 8~10분 이상

planning 기준:

- 단순 gate: 3분
- 일반 gate: 5분
- 복잡 gate: 9분
- 불확실성 포함 평균: 7분

### 7.2 문서화 작업 비용

6층을 모두 별도 문서화하면 최소 20~30 gates가 필요할 수 있다.

현재는 이 비용을 감당하기보다, 단일 기준 문서로 먼저 저장하고 후속 분리 여부를 결정하는 편이 좋다.

### 7.3 Cost Model 도입 단계

v0.1:

- 산식과 rough estimate만 기록

v0.2:

- 큰 gate에 한해 시간/토큰 수동 기록

v0.3:

- `gate_metrics.jsonl` append-only 도입

v0.4:

- metrics 기반 MVP 잔여 비용 자동 계산

## 8. 개발 요구조건 문서화 원칙

ee-agent 개발 요구조건은 다음 원칙으로 작성한다.

1. 제품 요구조건과 governance 요구조건을 분리한다.
2. MVP와 full expansion을 분리한다.
3. 측정값과 추정값을 분리한다.
4. 현재 claim과 아직 말하면 안 되는 claim을 분리한다.
5. subject 우선순위는 반드시 이유와 재검토 조건을 함께 기록한다.
6. 모든 큰 판단은 시간이 지난 뒤 복원 가능해야 한다.
7. gate 반복이 목적이 되지 않도록, gate의 크기는 피로와 위험을 함께 고려해 조정한다.

## 9. 최종 감독관 판단

Claude Web의 제안은 방향은 맞다.

하지만 현재 ee-agent 상황에서는 다음처럼 보정해야 한다.

- 6층 구조는 채택한다.
- 6개 문서를 즉시 만들지는 않는다.
- 먼저 단일 development specification으로 핵심 판단을 저장한다.
- Cost Model은 확정하지 않고 산식과 측정 누적 구조로 둔다.
- 전기자기학 후순위 이유는 반드시 기록한다.
- SRS 작성이 실제 MVP 진입을 막지 않게 한다.
- 다음 실제 개발 흐름은 Instance v0.2 Implementation Gate로 이어간다.

한 줄 결론:

ee-agent의 개발서는 표준 SRS 하나가 아니라, 6층 구조를 품은 development specification으로 시작해야 한다. Claude Web의 "다층 구조" 제안은 채택하되, "1~2주 문서화 sprint"와 "층별 즉시 gate 분리"는 현재 흐름에서는 과하다. 지금은 단일 기준 문서로 저장하고, 실제 개발을 계속 진행하면서 필요한 층을 점진 분리하는 전략이 가장 타당하다.

## 10. 다음 권장 gate

이 문서를 공식 산출물로 편입하려면 다음 gate가 필요하다.

후보: SRS Multilayer Review Addendum Review Gate  
단일 목적: 본 검토/반박 문서가 commit 가능한지 read-only 검토

후보: Development Specification Bundle Commit Gate  
단일 목적: `ee_agent_development_spec_v0.1.md`와 본 문서 2건을 함께 commit할지 결정

후보: Instance v0.2 Implementation Gate  
단일 목적: 실제 개발 흐름으로 복귀하여 `policy_change_rules_v0.2_draft_instance.json` 신규 작성

