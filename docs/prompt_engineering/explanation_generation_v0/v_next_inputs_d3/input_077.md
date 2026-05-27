# v_next D-3 input 077: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2006_2회_86
year: 2006
session: 2회
q_no: 86
subject: 전력공학
question_text: 가공 전선로에 사용하는 지지물을 강관으 로 구성되는 철탑으로 할 경우，지지물의 강도계산에 적용하는 병종 풍압 하중은 구성재의 수직 투영 면적 \(1\left[\mathrm{~m}^{2}\right]\) 에 대한 풍압을 몇 \([\mathrm{Pa}]\) 를 기초로 하여 계산하 는가？단，단주는 제외한다．
choices:
  1. 441
  2. 627
  3. 705
  4. 1078
answer: 3
solution: 가공전선로 지지물의 강관 철탑에 적용하는 병종 풍압하중을 구하는 문제입니다.

핵심 공식:
\[ \text{병종 풍압하중} = \text{갑종 풍압하중} \times \frac{1}{2} \]

단계별 계산:

1단계: 갑종 풍압하중 확인
   강관으로 구성되는 철탑(단주 제외)의 갑종 풍압하중:
   \[ P_{\text{갑}} = 1,255 \text{ [Pa]} \]

2단계: 병종 풍압하중 계산
   \[ P_{\text{병}} = 1,255 \times \frac{1}{2} = 627.5 \approx 627 \text{ [Pa]} \]

3단계: 답 확인
   \[ P_{\text{병}} = 627 \text{ [Pa]} \]

오답 분석:
- (1) 441[Pa]: 갑종 값을 1/3로 계산한 오류
- (2) 627[Pa]: **정답** - 갑종의 1/2
- (3) 705[Pa]: 잘못된 계산
- (4) 1078[Pa]: 갑종 값 자체를 선택한 오류

정답: **(2) 627[Pa]**

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=가공전선; audit_group=non_expansion_metadata

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 가공전선 이격거리
star: null
ds_class: S
phenomenon_origin: S/Static
six_axis: []
essence_question: 가공전선과 다른 시설간 안전 이격거리는 어떻게 정해지는가
representative_trap: 전선 종류별 이격거리 표 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 전선 종류별 이격거리 표 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: null

[연관 문제 후보]
same_core_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82, 2002_3회_85, 2003_3회_81, 2004_1회_84, 2004_1회_91, 2004_2회_86]
same_trap_pattern_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82]

