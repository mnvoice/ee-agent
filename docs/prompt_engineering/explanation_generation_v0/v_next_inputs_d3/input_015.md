# v_next D-3 input 015: 전력공학 / 전력_송배전D / 코로나 / 전선 도체

[문제]
id: 2000_4회_23
year: 2000
session: 4회
q_no: 23
subject: 전력공학
question_text: 3상 3선식 송전 선로에서 코로나 임계 전 압 \(E_{0}[\mathrm{kV}]\) 는？（단，\(d=2 r=\) 전선의 지름［cm］，\(D=\) 전선（3선）의 평균 선간 거리 \([\mathrm{cm}]\) 이며 전선표면계 수，날씨계수，상대공기 밀도 등의 영향계수는 곱하 지 않는 것으로 한다．）
choices:
  1. \(E_o = 24.3d \log_{10}\frac{D}{r}\)
  2. \(E_o = 24.3d \log_{10}\frac{r}{D}\)
  3. \(E_o = \frac{24.3}{d \log_{10}\frac{r}{D}}\)
  4. \(E_o = \frac{24.3}{d \log_{10}\frac{D}{r}}\)
answer: 1
solution: **핵심 공식:** 3상 3선식 송전선로의 코로나 임계 전압

**기본 코로나 임계 전압식:**

\[
E_0 = 24.3 \, m_0 m_1 \delta \, d \log_{10}\frac{2D}{d} \text{ [kV]}
\]

여기서:
- $m_0$: 전선 표면계수
- $m_1$: 기후계수(날씨계수)
- $\delta$: 상대 공기 밀도
- $d$: 전선의 지름 [cm]
- $D$: 선간 거리 [cm]

**문제 조건:** 영향계수($m_0, m_1, \delta$)를 곱하지 않음 → 1로 간주

**단계별 계산:**

1) 기본식에서 계수를 제거:
\[
E_0 = 24.3 \, d \log_{10}\frac{2D}{d}
\]

2) 로그 성질 적용 (단, $d = 2r$):
\[
E_0 = 24.3 \, d \log_{10}\frac{2D}{2r} = 24.3 \, d \log_{10}\frac{D}{r}
\]

**정답:** (1) $E_o = 24.3 d \log_{10}\frac{D}{r}$

**오답 분석:**
- (2): 분자·분모 역순 (오류)
- (3), (4): 분모에 로그 함수가 위치 (차원 오류)

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=코로나; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 코로나 / 전선 도체
star: null
ds_class: D
phenomenon_origin: D/Dynamic
six_axis: []
essence_question: 전선 표면 전계와 도체 손실이 어떻게 작용하는가
representative_trap: 코로나 임계전압 vs 정격 전압 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 코로나 임계전압 vs 정격 전압 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 코로나/표피효과 -> 회로 분포정수 -> 회로 임피던스

[연관 문제 후보]
same_core_candidates: [2002_3회_21, 2007_2회_24]
same_trap_pattern_candidates: [2002_3회_21, 2007_2회_24]

