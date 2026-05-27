# v_next D-3 input 028: 전력공학 / 전력_보호고장S / 보호계전기·피뢰기

[문제]
id: 2001_3회_26
year: 2001
session: 3회
q_no: 26
subject: 전력공학
question_text: 송변전 계통에 사용되는 피뢰기의 정격 전 압은 선로의 공칭 전압의 보통 몇 배로 선정하는가？
choices:
  1. 직접 접지계: 0.8~1.0배, 저항 또는 소호 리액터 접지: 0.7~0.9배
  2. 직접 접지계: 1.0~1.3배, 저항 또는 소호 리액터 접지: 1.4~1.6배
  3. 직접 접지계: 0.8~1.0배, 저항 또는 소호 리액터 접지: 1.4~1.6배
  4. 직접 접지계: 1.0~1.3배, 저항 또는 소호 리액터 접지: 0.7~0.9배
answer: 3
solution: 피뢰기(LA)의 정격전압 선정은 중성점 접지방식에 따라 달라집니다.

**핵심 공식:**
\[ E_R = \alpha \beta \frac{V_m}{\sqrt{3}} \]
여기서:
- \( \alpha \): 접지계수 (접지방식에 따라 결정)
- \( \beta \): 여유도 (1.15)
- \( V_m \): 선간의 최고 허용전압 = 공칭전압 × \( \frac{1.2}{1.1} \)

**각 접지방식별 정격전압:**

1) **직접접지계**: 공칭전압의 **0.8～1.0배**
   - 접지계수가 작아서 낮은 정격전압 사용

2) **저항 또는 소호리액터 접지계**: 공칭전압의 **1.4～1.6배**
   - 접지계수가 크므로 높은 정격전압 필요
   - 단락시 전압상승이 크기 때문에 여유도 증가 필요

**오답 분석:**
- (1)번: 수치가 반대 (접지계별로 역순)
- (2)번: 순서는 맞으나 수치 범위 오류
- (4)번: 접지계별 배수가 역순으로 잘못됨

정답: **(3)번**

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=피뢰기; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 보호계전기·피뢰기
star: null
ds_class: S
phenomenon_origin: S/Fault
six_axis: []
essence_question: 보호계전기 동작 특성과 피뢰기 정격이 어떻게 작용하는가
representative_trap: 보호계전기 정정 / 피뢰기 정격 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 보호계전기 정정 / 피뢰기 정격 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 보호계전기/피뢰기 -> 설비 절연/보호 -> 회로 임피던스

[연관 문제 후보]
same_core_candidates: [2000_2회_85, 2000_6회_28, 2002_3회_23, 2003_1회_44, 2007_1회_87]
same_trap_pattern_candidates: [2000_2회_85, 2000_6회_28, 2002_3회_23, 2003_1회_44, 2007_1회_87]

