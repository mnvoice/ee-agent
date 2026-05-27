# v_next D-3 input 011: 전력공학 / 전력_함정S / 부하율·수용률·부등률

[문제]
id: 1999_6회_24
year: 1999
session: 6회
q_no: 24
subject: 전력공학
question_text: 배전선의 손실 계수 \(H\) 와 부하율 \(F\) 와의 관계는？
choices:
  1. \(0 \leq F^2 \leq H \leq F \leq 1\)
  2. \(0 \leq H^2 \leq F \leq H \leq 1\)
  3. \(0 \leq H \leq F^2 \leq F \leq 1\)
  4. \(0 \leq F \leq H^2 \leq H \leq 1\)
answer: 1
solution: 배전선의 손실 계수 H와 부하율 F의 관계식을 이용한 부등식 유도 문제입니다.

**핵심 공식:**
손실 계수와 부하율의 관계식:
\[H = \alpha F + (1-\alpha)F^2\]

여기서 \(\alpha = 0.1 \sim 0.4\)

**부등식 유도:**
0 ≤ F ≤ 1인 범위에서:

1) F² ≤ F (F ≤ 1일 때 성립)

2) \(H = \alpha F + (1-\alpha)F^2\)에서:
   - H의 최소값: F = 0일 때, H = 0
   - H의 최대값: F = 1일 때, H = α + (1-α) = 1

3) \(H - F = (\alpha - 1)F + (1-\alpha)F^2 = (1-\alpha)(F^2 - F) ≤ 0\)
   따라서 H ≤ F (부등식 관계)

4) \(H - F^2 = \alpha F + (1-\alpha)F^2 - F^2 = \alpha F - \alpha F^2 = \alpha F(1-F) ≥ 0\)
   따라서 F² ≤ H

**결론:** \(0 \leq H^2 \leq F \leq H \leq 1\)

**정답:** (1)번

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=부하율; audit_group=non_expansion_metadata

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 부하율·수용률·부등률
star: null
ds_class: S
phenomenon_origin: S/Static
six_axis: []
essence_question: 부하율/수용률/부등률을 어떻게 구분해 외우는가
representative_trap: 부하율 vs 수용률 vs 부등률 정의 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 부하율 vs 수용률 vs 부등률 정의 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: null

[연관 문제 후보]
same_core_candidates: [1998_4회_25, 2008_1회_25]
same_trap_pattern_candidates: [1998_4회_25, 2008_1회_25]

