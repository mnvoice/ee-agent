# AI Agent Curriculum Mapping Record v0.1

작성일: 2026-05-28  
문서 성격: 보조 메모 / 외부 설명용 mapping record  
정책 승격 여부: 즉시 정책 아님. 후속 Turning Point Record 또는 Development Specification에 인용 가능한 근거 문서.

## 0. 감독관 판정

이 문서는 정책으로 바로 승격하지 않는다.

이유:

- 이미지의 커리큘럼은 ee-agent 내부 규약이 아니라 외부 학습 맵이다.
- 현재 매핑은 해석이며, 아직 공식 dependency나 요구조건이 아니다.
- 그러나 ee-agent가 무엇을 실증하고 있는지 설명하는 외부 언어로서 가치가 크다.
- 특히 "하네스 엔지니어링"과 "온톨로지 엔지니어링"이 무엇인지 사람에게 설명할 때 유용하다.

따라서 본 문서는 다음 위치에 둔다.

```text
보조 메모 / curriculum mapping record
```

정책으로 승격할 수 있는 부분은 다음으로 제한한다.

- 외부 커리큘럼 또는 프레임워크를 ee-agent에 매핑할 때는 claim boundary를 둔다.
- "우리 작업이 해당 영역을 완성했다"가 아니라 "초기 실증 사례"로 표현한다.
- domain-neutral schema와 domain-specific profile/instance를 구분한다.

## 1. 사람이 이해하기 위한 5가지 예

### 예 1. 하네스 엔지니어링은 자동차의 안전벨트와 계기판에 가깝다

전기기사 PWA가 자동차의 엔진과 바퀴라면, 우리가 만든 gate와 validator는 안전벨트와 계기판이다.

자동차가 앞으로 가는 것만으로는 충분하지 않다. 속도, 경고등, 브레이크 상태, 충돌 위험을 알아야 한다. ee-agent에서 이 역할을 하는 것이 다음이다.

- Review Gate
- Commit Gate
- Push Gate
- schema validator
- audit report
- claim boundary

따라서 하네스 엔지니어링은 "기능을 만드는 기술"이라기보다 "기능이 잘못된 방향으로 가는 것을 막는 장치"다.

### 예 2. 온톨로지 엔지니어링은 도서관 분류 체계를 만드는 일이다

문항 5,331개가 책이라면, 온톨로지는 도서관 분류 체계다.

책이 많아도 분류법이 없으면 찾을 수 없다. ee-agent에서 rule schema, profile, instance는 문항과 정책을 분류하고 연결하는 체계다.

- rule schema: 어떤 형태로 규칙을 적을 수 있는가
- profile: 이 도메인에서 허용되는 category, predicate, check는 무엇인가
- instance: 실제 12개 rule이 그 체계 안에 어떻게 배치되는가

이것이 이미지의 "온톨로지 엔지니어링"과 가장 가까운 부분이다.

### 예 3. L1~L8 validator는 선생님이 아니라 채점표다

validator는 "정답을 이해하는 선생님"이 아니다. 지금 단계에서는 "형식 채점표"에 더 가깝다.

예를 들어 L5가 pass라는 말은 function_id가 profile catalog 안에 있다는 뜻이다. 그러나 그 function이 실제 도구 측에서 잘 구현되어 있다는 뜻은 아니다.

따라서 다음 구분이 중요하다.

- form-level pass: 구조와 catalog 정합성 통과
- semantic correctness: 의미상 옳음
- runtime correctness: 실제 실행 시 의도대로 작동함

현재 validator run v0.2는 form-level cross-check를 확정한 것이다. semantic/runtime 보장은 아직 별도 영역이다.

### 예 4. 전기자기학 후순위 판단은 제외가 아니라 품질 보호다

전기자기학을 MVP 1차 후보에서 후순위로 둔 것은 중요도가 낮아서가 아니다.

전기자기학은 수식, 도형, 물리 개념 의존도가 높다. 빠르게 넣으면 겉보기로는 과목 수가 늘지만, 해설 품질과 검증 난이도가 급격히 올라간다.

따라서 이 판단은 다음과 같다.

- 나쁜 표현: 전기자기학 제외
- 정확한 표현: MVP 1차에서는 후순위, 재검토 조건 유지

이런 판단을 기록하는 것이 Turning Point Record의 역할이다.

### 예 5. 이 커리큘럼 매핑은 지도이지 법이 아니다

이미지의 7단계는 좋은 지도다.

- 프롬프트 엔지니어링
- 컨텍스트 엔지니어링
- 에이전틱 엔지니어링
- 스킬 엔지니어링
- 하네스 엔지니어링
- 온톨로지 엔지니어링

하지만 지도는 법이 아니다. ee-agent가 반드시 이 순서로 개발되어야 한다는 뜻은 아니다.

이 매핑은 외부 설명과 자기 위치 파악에 유용하지만, repo 내부의 강제 정책으로 바로 삼으면 안 된다.

## 2. 커리큘럼 7단계와 ee-agent 매핑

| 커리큘럼 단계 | ee-agent에서 대응되는 것 | 현재 평가 |
|---|---|---|
| 생성형 AI 살펴보기 | 기본 LLM 활용, Claude/Codex/MoAI 사용 | 이미 통과한 기반 |
| 프롬프트 엔지니어링 | explanation generation, prompt/input 구성 | 사용 중 |
| 컨텍스트 엔지니어링 | claim boundary, memory, artifact reference, gate report | 강하게 사용 중 |
| 에이전틱 엔지니어링 | Claude Web, CLI MoAI, Codex 감독관의 역할 분리 | 실전 운영 중 |
| 스킬 엔지니어링 | validator, script, reusable procedure, SKILL.md 계열 | 부분 구현 |
| 하네스 엔지니어링 | gate protocol, review, audit, commit/push discipline | 초기 실증 성공 |
| 온톨로지 엔지니어링 | rule schema, profile, predicate/check catalog, instance | ee-agent 한정 실증 성공 |

## 3. 하네스 엔지니어링에 해당하는 자산

ee-agent에서 하네스 엔지니어링으로 볼 수 있는 자산:

- design/review/commit/push gate
- read-only review
- protected area 점검
- claim boundary
- schema validator
- run audit report
- migration log
- local/remote synchronization check
- staged/tracked diff 확인
- unresolved 분리
- form-level과 semantic-level 분리

현재 평가:

하네스 엔지니어링 완성품은 아니다. 그러나 gate/commit/validator/audit 산출물로 실측된 초기 사례다.

아직 부족한 것:

- gate metrics 자동 수집
- 실패 gate recovery 표준화
- multi-domain harness 검증
- PWA runtime end-to-end harness
- 비용/토큰 자동 추적

## 4. 온톨로지 엔지니어링에 해당하는 자산

ee-agent에서 온톨로지 엔지니어링으로 볼 수 있는 자산:

- `rule_schema_v0.1_draft.schema.json`
- `ee_agent_rule_profile_v0.1_draft.json`
- `ee_agent_rule_profile_v0.2_draft.json`
- `policy_change_rules_v0.1_draft_instance.json`
- `policy_change_rules_v0.2_draft_instance.json`
- predicate_library
- check_library
- category_enum
- threshold_proposals
- L1~L8 check model

현재 평가:

schema는 비교적 domain-neutral 방향을 가진다. profile과 instance는 ee-agent domain-specific이다.

따라서 다른 프로젝트에 이식할 때는 다음을 구분해야 한다.

- 가져가도 되는 구조: schema/profile/instance 분리
- 그대로 가져가면 위험한 내용: MAGNITUDE_DELTA, priority_group, severity, threshold 값, ee-agent check catalog

## 5. Claude Web 해석에 대한 감독관 평가

Claude Web의 해석 중 타당한 부분:

- 우리 작업은 이미지의 하네스/온톨로지 영역과 관련이 깊다.
- 일반 SRS보다 다층 development specification이 더 적합하다.
- 커리큘럼 어휘는 외부 설명에 유용하다.
- 지금의 피로는 참고 사례가 적은 영역을 가고 있기 때문에 발생한다.

보정이 필요한 부분:

- "TBD 영역을 이미 수행 중"은 가능하지만, "완성"으로 표현하면 과장이다.
- 하네스 엔지니어링은 아직 자동화된 제품이 아니라 운영 실증이다.
- 온톨로지는 ee-agent 한정 실증이지 범용 ontology가 아니다.
- revfactory/harness-100과의 관계는 확인되지 않았다.
- 강의 콘텐츠 가능성보다 먼저 실패 방지 시스템이라는 본질을 봐야 한다.

## 6. 현재 수준 평가

| 영역 | 현재 수준 |
|---|---|
| Prompt Engineering | 이미 통과한 기반 |
| Context Engineering | 고급 운영 중 |
| Agentic Engineering | 실전 운영 중 |
| Skill Engineering | 부분 구현 |
| Harness Engineering | 초기 실증 성공 |
| Ontology Engineering | ee-agent 한정 실증 성공 |
| Product Runtime | 아직 약함 |
| Cost Model | 아직 약함 |
| Generalization | 아직 미검증 |

## 7. 핵심 문장

외부 설명에 사용할 수 있는 핵심 문장:

```text
ee-agent는 전기기사 PWA를 표면 제품으로 삼아,
하네스 엔지니어링과 온톨로지 엔지니어링을
실제 gate/commit/validator 산출물로 실증 중인 프로젝트다.
```

보수적 표현:

```text
ee-agent는 하네스 엔지니어링과 온톨로지 엔지니어링의 완성품이 아니라,
두 영역을 실제 운영 로그와 검증 산출물로 실험하는 초기 실증 사례다.
```

## 8. Claim Boundary

이 문서가 주장하는 것:

- 이미지의 커리큘럼은 ee-agent를 설명하는 외부 언어로 유용하다.
- ee-agent는 하네스 엔지니어링과 온톨로지 엔지니어링 영역에 걸쳐 있다.
- 현재 ee-agent는 두 영역의 초기 실증 사례로 볼 수 있다.
- 하네스/온톨로지 매핑은 SRS와 Development Specification에 도움이 된다.

이 문서가 주장하지 않는 것:

- ee-agent가 하네스 엔지니어링을 완성했다는 주장
- ee-agent가 온톨로지 엔지니어링을 범용적으로 완성했다는 주장
- 이미지의 커리큘럼이 ee-agent의 공식 요구조건이라는 주장
- revfactory/harness-100과 ee-agent의 직접 관계가 확인되었다는 주장
- 이 매핑이 개발 방향을 바꾼다는 주장
- 이 문서가 정책으로 즉시 승격되었다는 주장

## 9. 정책 후보

즉시 정책은 아니지만 후속 정책 후보가 될 수 있는 문장:

```text
외부 프레임워크나 커리큘럼을 ee-agent에 매핑할 때는
완성 claim이 아니라 실증 수준 claim으로 제한한다.
해당 매핑은 정책이 아니라 설명 언어로 먼저 기록한다.
```

## 10. 다음 권장 gate

후보: Curriculum Mapping Record Review Gate  
단일 목적: 본 문서가 repo 산출물로 편입 가능한지 read-only 검토

후보: Development Turning Point Record Bundle Gate  
단일 목적: SRS/turning point/curriculum mapping 문서를 함께 review할지 결정

후보: Threshold Confirm Gate  
단일 목적: 실제 개발 흐름으로 복귀하여 U10 threshold 확정 진행

감독관 권장:

본 문서는 정책이 아니라 보조 메모로 저장한다. 다만 SRS와 Turning Point Record를 보강하는 자료로 가치가 있으므로, 후속 review 후 repo에 편입할 수 있다.

