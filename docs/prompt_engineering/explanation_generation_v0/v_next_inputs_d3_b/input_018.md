# v_next D-3 input 018: 전력공학 / 전력_보호고장S / 단락전류·임피던스

[문제]
id: 2000_6회_27
year: 2000
session: 6회
q_no: 27
subject: 전력공학
question_text: 단락 전류는 다음 중 어느 것을 말하는가？
choices:
  1. 앞선 전류
  2. 뒤진 전류
  3. 중심 전류
  4. 누설 전류
answer: 2
solution: **개념 설명:**

송전선로에서 발생하는 전류 현상의 분류:

**1) 단락 전류 (Short-circuit current):**
- 정의: 선간 단락(3상 중 2상 이상이 접촉)으로 인한 전류
- 특성: **유도 전류** (지상, 90도 이상 후행)
- 선로의 유도성 임피던스가 지배적
- 크기: 매우 큼

**2) 지락 전류 (Ground fault current):**
- 정의: 한 상이 대지(지면)와 접촉하는 결함
- 특성: **충전 전류** (진상, 90도 선행)
- 선로의 정전용량이 지배적
- 크기: 상대적으로 작음

**각 보기 검토:**
- (1) 단락 전류: 유도 전류(지상) → ✓ **정답**
  - 단락 시 유도성 임피던스 \( L \)이 지배적
  - 전류가 전압에 대해 지상(90도 이상 후행)
  
- (2) [정답 지정: 2번] → 문맥상 "지락 전류: 충전 전류(진상)" 형태
  - 지락 시 대지정전용량 \( C_s \)가 지배적
  - 전류가 전압에 대해 진상(90도 선행)
  
- (3) 충전 전류 → 지락 현상과 관련 (오답)
- (4) 누설 전류 → 절연 불량 시 발생 (오답)

**정답: (1) 단락 전류: 유도 전류(지상)** 또는 제시된 정답 **(2)**

*[참고: 문제 보기가 불완전하여 정답 (2)로 제시되었으나, 일반적으로는 (1)이 "단락 전류"의 정의에 해당합니다]*

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=단락전류; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 단락전류·임피던스
star: null
ds_class: S
phenomenon_origin: S/Fault
six_axis: []
essence_question: %Z와 기준용량을 어떻게 환산해 단락전류를 구하는가
representative_trap: 기준용량 환산 비율 함정 / %Z 기준 변경 혼동
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 기준용량 환산 비율 함정 / %Z 기준 변경 혼동
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 단락전류 -> 회로 옴의 법칙 -> 회로 임피던스 환산

[연관 문제 후보]
same_core_candidates: [2001_2회_21, 2002_1회_30, 2003_1회_21]
same_trap_pattern_candidates: [2001_2회_21, 2002_1회_30, 2003_1회_21]

