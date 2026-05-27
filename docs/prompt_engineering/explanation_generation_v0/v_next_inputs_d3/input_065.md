# v_next D-3 input 065: 전력공학 / 전력_보호고장S / 지락·중성점 접지

[문제]
id: 2005_2회_28
year: 2005
session: 2회
q_no: 28
subject: 전력공학
question_text: 소호 리액터 접지 계통에서 리액터의 탭을 완전 공진 상태에서 약간 벗어나도록 하는 이유는？
choices:
  1. 전력 손실을 줄이기 위하여
  2. 선로의 리액턴스를 감소시키기 위하여
  3. 접지 계전기의 동작을 확실하게 하기 위하여
  4. 직렬 공진에 의한 이상 전압의 발생을 방지하기 위하여
answer: 3
solution: 소호 리액터 접지 계통에서 리액터 탭 설정 방법에 관한 문제입니다.

**핵심 개념:**

소호 리액터(접지 리액터)는 대지 정전용량과의 직렬 공진을 이용하여 지락 전류를 제한합니다. 완전 공진 상태에서는 이상 전압(고조파 성분)이 공진으로 인해 과도하게 증폭될 수 있습니다.

**완전 공진 상태의 문제점:**
- 직렬 공진에 의한 이상 전압(고조파) 발생
- 선로에 고주파 영향으로 인한 이상 현상 유발

**해결책:**
리액터 탭을 완전 공진에서 약간 벗어나도록 조정하여, 일반적으로 **10% 정도 과보상** 상태를 유지합니다. 이를 통해:
- 이상 전압 억제
- 지락 전류 제한 효과 유지
- 시스템 안정성 확보

**정답:** (4) 직렬 공진에 의한 이상 전압을 억제하기 위하여

**오답 이유:**
- (1) 전력손실: 주요 목적이 아님
- (2) 리액턴스 감소: 오히려 과보상으로 증가
- (3) 계전기 동작: 보조적 효과일 뿐 주 목적 아님

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=소호리액터; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 지락·중성점 접지
star: null
ds_class: S
phenomenon_origin: S/Fault
six_axis: []
essence_question: 중성점 접지 방식이 지락전류에 어떻게 작용하는가
representative_trap: 직접접지 vs 소호리액터 vs 비접지 특성 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 직접접지 vs 소호리액터 vs 비접지 특성 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 중성점 접지 -> 회로 대칭분 해석

[연관 문제 후보]
same_core_candidates: [1999_3회_23, 2002_1회_33, 2006_3회_21]
same_trap_pattern_candidates: [1999_3회_23, 2002_1회_33, 2006_3회_21]

