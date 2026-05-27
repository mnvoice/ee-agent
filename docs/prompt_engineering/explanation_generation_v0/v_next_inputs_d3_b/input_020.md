# v_next D-3 input 020: 전력공학 / 전력_설비고장 / 절연내력 / 유도장해

[문제]
id: 2000_6회_85
year: 2000
session: 6회
q_no: 85
subject: 전력공학
question_text: 전압이 \(22,900[\mathrm{~V}]\) 로서 중성선에 다중 접 지하는 전선로의 절연 내력 시험 전압은 최대 사용 전압의 몇 배인가?
choices:
  1. 0.72
  2. 0.92
  3. 1.1
  4. 1.25
answer: 2
solution: 전압 22,900[V](≈22.9[kV])에서 중성선에 다중 접지하는 전선로의 절연내력 시험 전압을 구하는 문제입니다.

**전기설비기술기준 132 절연내력시험 기준표:**

최대사용전압 범위별 시험전압 배수:
- 7[kV] 이하: 1.5배
- **7[kV] 초과 25[kV] 이하, 다중접지**: **0.92배** ✓
- 7[kV] 초과 60[kV] 이하 (비접지): 1.25배
- 60[kV] 초과 (접지식): 1.1배

**풀이:**
주어진 전압 22,900[V] = 22.9[kV]는 7[kV]를 초과하고 25[kV] 이하이며, 중성선에 다중 접지하므로

\[ \text{시험전압 배수} = 0.92\text{배} \]

따라서 정답은 **(2) 0.92**입니다.

**오답 이유**: 비접지 방식은 1.25배, 고압 접지식은 1.1배이므로 헷갈릴 수 있습니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=절연내력시험전압; audit_group=non_expansion_metadata

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 절연내력 / 유도장해
star: null
ds_class: S
phenomenon_origin: S/Static
six_axis: []
essence_question: 절연내력 시험전압과 유도장해 경감이 어떻게 작용하는가
representative_trap: 절연내력 시험전압 배율 / 유도장해 경감대책 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 절연내력 시험전압 배율 / 유도장해 경감대책 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: null

[연관 문제 후보]
same_core_candidates: [2001_2회_24, 2003_1회_22]
same_trap_pattern_candidates: [2001_2회_24, 2003_1회_22]

