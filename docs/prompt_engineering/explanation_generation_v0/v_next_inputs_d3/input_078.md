# v_next D-3 input 078: 전력공학 / 전력_보호고장S / 지락·중성점 접지

[문제]
id: 2006_3회_21
year: 2006
session: 3회
q_no: 21
subject: 전력공학
question_text: 선로의 길이가 \(50[\mathrm{~km}]\) 인 \(66[\mathrm{kV}]\) 3상 3선 식， 1 회선 송전선의 1 선당 대지 정전 용량은 0.0058 \([\mu \mathrm{F} / \mathrm{km}]\) 이다．여기에 시설할 소호 리액터의 용량은 약 몇［kVA］인가？단，소호 리액터의 용량은 10 ［\％］ 의 여유를 주도록 한다．
choices:
  1. 386
  2. 435
  3. 524
  4. 712
answer: 3
solution: **핵심 공식:**
소호 리액터 용량은 다음 공식으로 계산됩니다.
\[ P_c = 3 \times 2\pi f C_s E^2 \text{ [VA]} \]
여기서:
- \( f = 60 \text{ [Hz]} \) (국내 전력 주파수)
- \( C_s = 0.0058 \times 10^{-6} \times 50 = 0.29 \times 10^{-6} \text{ [F]} \) (선로 전체 대지정전용량)
- \( E = \frac{66000}{\sqrt{3}} = 38105.1 \text{ [V]} \) (선간전압 → 상전압)

**단계별 계산:**

1) 선로 전체 대지정전용량:
\[ C_s = 0.0058 \times 10^{-6} \times 50 = 0.29 \times 10^{-6} \text{ [F]} \]

2) 소호 리액터 기본 용량:
\[ P_c = 3 \times 2\pi \times 60 \times 0.29 \times 10^{-6} \times (38105.1)^2 \times 10^{-3} \]
\[ P_c = 3 \times 2\pi \times 60 \times 0.0058 \times 10^{-6} \times 50 \times \frac{66000^2}{3} \times 10^{-3} \]
\[ P_c = 476.23 \text{ [kVA]} \]

3) 10% 여유를 고려한 최종 용량:
\[ P_c' = 476.23 \times 1.1 = 523.85 \text{ [kVA]} \]

**정답:** (3) 524 kVA (또는 523.85 kVA)

**오답 분석:**
- (1) 386 kVA: 여유를 미적용하고 잘못된 계산
- (2) 435 kVA: 불완전한 계산 (여유 미적용)
- (4) 712 kVA: 과도한 여유 또는 중복 계산

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
same_core_candidates: [1999_3회_23, 2002_1회_33, 2005_2회_28]
same_trap_pattern_candidates: [1999_3회_23, 2002_1회_33, 2005_2회_28]

