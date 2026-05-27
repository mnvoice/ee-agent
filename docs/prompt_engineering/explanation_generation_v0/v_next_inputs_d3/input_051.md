# v_next D-3 input 051: 전력공학 / 전력_설비고장 / 가공전선로 경간·이도

[문제]
id: 2004_2회_25
year: 2004
session: 2회
q_no: 25
subject: 전력공학
question_text: 온도가 \(t\left[{ }^{\circ} \mathrm{C}\right]\) 상승했을 때의 딥（dip）은 몇 ［m］인가？단．온도 변화 전의 딥을 \(D_{1}[\mathrm{~m}]\) ，경간을 \(s\) ［m］，전선의 온도 계수를 \(\alpha\) 라 한다．
choices:
  1. \(\sqrt{D_{1}+\frac{3}{8} s \alpha t}\)
  2. \(\sqrt{D_{1}{ }^{2}+\frac{8}{3} s \alpha^{2} t^{2}}\)
  3. \(\sqrt{D_{1}{ }^{2}+\frac{3}{8} s^{2} \alpha t}\)
  4. \(\sqrt{D_{1}{ }^{2}+\frac{8}{3} s^{2} \alpha^{2} t}\)
answer: 3
solution: **핵심 공식:**
카테나리 곡선의 근사식에서 경간 $s$에 대한 길이:
$$L = s + \frac{8D^2}{3s}$$

온도 변화에 따른 전선 신축:
$$L_2 = L_1(1 + \alpha t)$$

**단계별 풀이:**

1단계: 온도 상승 전 길이 식
$$L_1 = s + \frac{8D_1^2}{3s}$$

2단계: 온도 상승 후 길이 식
$$L_2 = L_1(1 + \alpha t) = s + \frac{8D_1^2}{3s} + \alpha t\left(s + \frac{8D_1^2}{3s}\right)$$

3단계: 온도 상승 후 딥 $D_2$에 대한 길이식
$$L_2 = s + \frac{8D_2^2}{3s}$$

4단계: 두 식을 같다고 놓으면 (첫 항은 $s$로 동일)
$$s + \frac{8D_2^2}{3s} = s + \frac{8D_1^2}{3s} + \alpha t \cdot s$$

5단계: $s$ 항 소거 및 정리
$$\frac{8D_2^2}{3s} = \frac{8D_1^2}{3s} + \alpha t \cdot s$$

$$D_2^2 = D_1^2 + \frac{3}{8}\alpha t s^2$$

6단계: $D_2$ 계산
$$D_2 = \sqrt{D_1^2 + \frac{3}{8}\alpha t s^2}$$

**정답:** (3) $\sqrt{D_1^2 + \frac{3}{8}s^2\alpha t}$

**물리적 의미:**
- 온도 상승 → 전선 길어짐 → 같은 길이 경간에서 딥 증가
- 딥 증가량은 온도계수 $\alpha$와 온도 변화 $t$에 비례
- 경간 $s$에 비례 ($s^2$항으로 나타남)

**오답 이유:**
- (1): 제곱근 안에 $D_1$이 아닌 합으로 표현 (차원 오류)
- (2): $\alpha^2$ 항이 포함 (물리적 의미 없음)
- (4): $\alpha^2$ 항과 $t$ 항의 차원 오류

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=경간; audit_group=non_expansion_metadata

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 가공전선로 경간·이도
star: null
ds_class: S
phenomenon_origin: S/Static
six_axis: []
essence_question: 전선 장력·이도·경간이 어떻게 작용하는가
representative_trap: 경간 vs 이도 관계 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 경간 vs 이도 관계 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: null

[연관 문제 후보]
same_core_candidates: [2004_1회_30, 2004_3회_25, 2006_3회_25]
same_trap_pattern_candidates: [2004_1회_30, 2004_3회_25, 2006_3회_25]

