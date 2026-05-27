# v_next D-3 input 063: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2005_1회_29
year: 2005
session: 1회
q_no: 29
subject: 전력공학
question_text: 특고압 차단기 중 개폐 서지 전압이 가장 높은 것은？
choices:
  1. 유입 차단기 \((\mathrm{OCB})\)
  2. 진공 차단기（ VCB ）
  3. 자기 차단기 \((\mathrm{MBB})\)
  4. 공기 차단기 \((\mathrm{ABB})\)
answer: 2
solution: 특고압 차단기의 개폐 서지(Switching Surge) 특성을 비교합니다.

**각 차단기의 개폐 서지 전압 특성:**

1. **유입 차단기(OCB: Oil Circuit Breaker)**
   - 개폐 서지: 중간 수준
   - 소호매질: 절연유

2. **진공 차단기(VCB: Vacuum Circuit Breaker)** ✓
   - 개폐 서지: **가장 높음**
   - 소호매질: 진공
   - 이유: 진공에서의 빠른 차단으로 인한 높은 서지 발생
   - 대책: 2차측에 Mold 변압기가 있을 경우 SA(Surge Absorber) 설치 필수

3. **자기 차단기(MBB: Magnetic Blast Circuit Breaker)**
   - 개폐 서지: 중간 수준
   - 소호매질: 공기

4. **공기 차단기(ABB: Air Blast Circuit Breaker)**
   - 개폐 서지: 낮음
   - 소호매질: 고압 공기

**정답: (2) 진공 차단기(VCB)**

진공 차단기는 빠른 차단 특성으로 인해 개폐 서지가 높아, 연결된 기기 보호를 위해 서지 흡수기 설치가 필요합니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=차단기; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 차단기
star: null
ds_class: S
phenomenon_origin: S/Fault
six_axis: []
essence_question: 소호매질 종류가 차단 특성에 어떻게 작용하는가
representative_trap: 차단 용량 vs 차단 시간 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 차단 용량 vs 차단 시간 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 차단기 -> 회로 단락전류 / 회로 임피던스 환산

[연관 문제 후보]
same_core_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_23, 2003_1회_27, 2004_1회_90, 2004_3회_27, 2004_3회_29]
same_trap_pattern_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26]

