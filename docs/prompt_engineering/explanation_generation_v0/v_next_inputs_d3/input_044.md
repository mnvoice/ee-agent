# v_next D-3 input 044: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2003_3회_81
year: 2003
session: 3회
q_no: 81
subject: 전력공학
question_text: 사용전압 \(22.9[\mathrm{kV}]\) 인 가공전선로의 중성 선 다중접지식에 사용되는 접지선의 굵기는 단면적 몇 \(\left[\mathrm{mm}^{2}\right]\) 의 연동선 또는 이와 동등이상의 굵기로서 고장전류를 안전하게 통할 수 있는 것이어야 하는 가？단，전로에 지기가 생긴 경우 2초안에 전로로부 터 자동 차단하는 장치를 하였다．
choices:
  1. 4
  2. 6
  3. 10
  4. 16
answer: 2
solution: **핵심 기준:**
전기설비기술기준에 따른 가공전선로 접지선 굵기 규정

**문제 분석:**
- 사용전압: 22.9[kV] (15kV 초과 25kV 이하)
- 중성선 다중접지식
- 지락 발생 시 2초 이내 자동 차단 장치 설치

**기술기준 적용:**
전기설비기술기준 규정에 따르면, 사용전압이 15[kV]를 초과하고 25[kV] 이하인 특고압 가공전선로(중성선 다중접지식)의 중성선 접지도체는:

$$\text{공칭단면적} \geq 6[\text{mm}^2]$$

이상의 연동선 또는 이와 동등 이상의 세기 및 굵기의 쉽게 부식하지 않는 금속선으로 시설해야 합니다.

**선택지 검토:**
- (1) 4[mm²] - 기준 미만 ❌
- **(2) 6[mm²] - 기준 충족 ✓**
- (3) 10[mm²] - 필요 이상 (과다)
- (4) 16[mm²] - 필요 이상 (과다)

**정답: (2) 6[mm²]**

**오답 이유:**
- 4mm²는 저전압용 기준으로 부족
- 10mm², 16mm²는 규정값보다 과도하며 경제성 위배

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
same_core_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82, 2002_3회_85, 2004_1회_84, 2004_1회_91, 2004_2회_86, 2004_3회_83]
same_trap_pattern_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82]

