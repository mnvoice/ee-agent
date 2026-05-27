# v_next D-3 input 040: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2003_1회_23
year: 2003
session: 1회
q_no: 23
subject: 전력공학
question_text: 전력 회로에 사용되는 차단기의 차단 용량 을 결정할 때 이용되는 것은？
choices:
  1. 예상 적대 단락 전류
  2. 회로에 접속되는 전부하 전류
  3. 계통의 최고 전압
  4. 회로를 구성하는 전선의 최대 허용 전류
answer: 1
solution: 차단기의 차단용량(Breaking Capacity) 결정 요소를 분석합니다.

**핵심 개념:**
차단기는 정상 부하전류뿐만 아니라 단락시 발생하는 큰 전류를 차단할 수 있어야 합니다.

**차단기 용량 결정시 필수 고려사항:**
1) **정격전압 (Rated Voltage)**: 차단기가 견디어야 할 전압 수준
2) **최대 단락(차단)전류 (Maximum Fault/Breaking Current)**: 차단기가 차단할 수 있는 최대 전류

**보기 검토:**
- (1) **정격전압**: 차단기 선정의 필수요소 ✓
- (2) 전부하 전류: 정상 상태 전류로, 차단기 용량 결정에 직접 영향 없음 ✗
- (3) 계통의 최고전압: (1)의 정격전압과 유사하나 '최고전압'은 부정확
- (4) 전선의 최대허용전류: 과전류계전기 등 다른 기기의 고려사항

**정답: (1) 정격전압 및 최대 단락전류**

차단기는 반드시 계통의 단락전류를 견디고 차단할 수 있는 등급으로 선정하여야 합니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=차단기; audit_group=expansion

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
same_core_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_27, 2004_1회_90, 2004_3회_27, 2004_3회_29, 2004_3회_82]
same_trap_pattern_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26]

