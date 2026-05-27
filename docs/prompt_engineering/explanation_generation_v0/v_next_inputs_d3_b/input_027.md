# v_next D-3 input 027: 전력공학 / 전력_송배전D / 전압강하·전력손실

[문제]
id: 2001_3회_25
year: 2001
session: 3회
q_no: 25
subject: 전력공학
question_text: 동일 전력을 동일 선간 전압，동일 역률로 동일 거리에 보낼 때 사용하는 전선의 총 중량이 같 으면 3상 3선식인 때와 단상 2선식일 때의 전력 손 실비는？
choices:
  1. 1
  2. 3/4
  3. 2/3
  4. 1/√3
answer: 2
solution: 동일 전력, 동일 전압, 동일 역률, 동일 거리에서 사용 전선의 총 중량이 같을 때, 3상 3선식과 단상 2선식의 전력손실 비를 구하는 문제입니다.

**주어진 조건:**
- 송전 전력: P (동일)
- 선간 전압: V (동일)
- 역률: cos φ (동일)
- 거리: l (동일)
- 전선 총 중량: 동일

**Step 1: 각 방식의 전류 비교**

단상 2선식 전력: \(P = V I_1 \cos \phi\)

3상 3선식 전력: \(P = \sqrt{3} V I_3 \cos \phi\)

양쪽이 같으므로:
\[V I_1 = \sqrt{3} V I_3\]

따라서:
\[\frac{I_1}{I_3} = \sqrt{3}\]

**Step 2: 전선 단면적 비교**

전선 총 중량: \(W = \sigma A l\) (σ: 밀도, A: 단면적, l: 길이)

단상 2선식: \(W_1 = 2 \sigma A_1 l\)

3상 3선식: \(W_3 = 3 \sigma A_3 l\)

중량이 같으므로:
\[2 \sigma A_1 l = 3 \sigma A_3 l\]

\[\frac{A_1}{A_3} = \frac{3}{2}\]

**Step 3: 전기 저항 비교**

저항: \(R = \rho \frac{l}{A}\) 이므로 \(R \propto \frac{1}{A}\)

\[\frac{R_1}{R_3} = \frac{A_3}{A_1} = \frac{2}{3}\]

따라서:
\[\frac{R_3}{R_1} = \frac{3}{2}\]

**Step 4: 전력손실 비교**

전력손실: \(P_L = I^2 R\)

단상 2선식: \(P_{L1} = I_1^2 \cdot 2R_1\) (2가닥 전선)

3상 3선식: \(P_{L3} = 3 I_3^2 R_3\) (3가닥 전선)

**Step 5: 손실비 계산**

\[\frac{P_{L3}}{P_{L1}} = \frac{3 I_3^2 R_3}{2 I_1^2 R_1}\]

\[= \frac{3}{2} \times \left(\frac{I_3}{I_1}\right)^2 \times \frac{R_3}{R_1}\]

\[= \frac{3}{2} \times \left(\frac{1}{\sqrt{3}}\right)^2 \times \frac{3}{2}\]

\[= \frac{3}{2} \times \frac{1}{3} \times \frac{3}{2}\]

\[= \frac{3}{4}\]

**정답:** 2번 \(\left(\frac{3}{4}\right)\)

**물리적 의미:**
3상 3선식이 단상 2선식보다 전력손실이 약 25% 적습니다. 이는 같은 중량의 전선으로도 3상 방식이 더 효율적임을 의미합니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=전력손실; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 전압강하·전력손실
star: null
ds_class: D
phenomenon_origin: D/Dynamic
six_axis: []
essence_question: 송전 거리·전류·임피던스가 전압강하에 어떻게 작용하는가
representative_trap: 단상 vs 3상 전압강하 공식 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 단상 vs 3상 전압강하 공식 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 전압강하/손실 -> 회로 임피던스 -> 회로 옴의 법칙

[연관 문제 후보]
same_core_candidates: [1999_3회_22, 2000_6회_23, 2004_2회_23, 2004_2회_31, 2005_1회_28, 2005_2회_23, 2006_1회_2, 2006_1회_28, 2008_1회_29]
same_trap_pattern_candidates: [1999_3회_22, 2000_6회_23, 2004_2회_23, 2004_2회_31, 2005_1회_28]

