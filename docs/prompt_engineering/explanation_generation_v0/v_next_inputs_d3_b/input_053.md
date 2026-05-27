# v_next D-3 input 053: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2004_2회_86
year: 2004
session: 2회
q_no: 86
subject: 전력공학
question_text: 사용 전압이 \(154[\mathrm{kV}]\) 인 가공 송전선의 시 설에서 전선과 식물과의 이격거리는 몇 [m] 이상으 로 하여야 하는가?
choices:
  1. 2.8
  2. 3.2
  3. 3.6
  4. 4.2
answer: 2
solution: **핵심 기준**: 전기설비기술기준 제333.30조 특고압 가공전선과 식물의 이격거리

**주어진 조건**: 사용전압 154[kV]인 가공송전선

**이격거리 계산 공식**:

\[
\begin{cases}
\text{60[kV] 이하} & : 2\text{[m]} \\
\text{60[kV] 초과} & : 2\text{[m]} + (\text{60[kV]를 초과하는 10[kV]의 단수}) \times 0.12\text{[m]}
\end{cases}
\]

**단계별 계산**:

1. 사용전압이 60[kV]를 초과하는 전압:
   \[ 154 - 60 = 94\text{[kV]} \]

2. 10[kV]의 단수 계산:
   \[ \frac{94}{10} = 9.4 \rightarrow \text{올림하여 10단} \]

3. 이격거리 계산:
   \[ \text{이격거리} = 2 + 10 \times 0.12 = 2 + 1.2 = 3.2\text{[m]} \]

**정답**: **(2) 3.2[m]**

**오답 이유**:
- (1) 2.8[m]: 단수 계산 오류 (8단으로 잘못 계산)
- (3) 3.6[m]: 단수를 11단으로 잘못 계산
- (4) 4.2[m]: 계산 오류

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=이격거리; audit_group=non_expansion_metadata

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
same_core_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82, 2002_3회_85, 2003_3회_81, 2004_1회_84, 2004_1회_91, 2004_3회_83]
same_trap_pattern_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82]

