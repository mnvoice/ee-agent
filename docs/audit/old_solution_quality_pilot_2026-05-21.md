# Old Solution Quality — Pilot Candidates (2026-05-21)

Review doc for the C1 conclusion-mismatch pilot batch. Read-only; no data or
solution was modified to produce this document.

## Provenance

- Extractor commit: `832e285`
- Extractor: `scripts/extract_old_solution_quality_candidates.py`
- Report (large, not committed): `old_solution_quality_candidates_20260521T094951.json` (+ `.md`)
- Source scan: `app/data/questions.v2.json`

## Route / trigger summary

| Route | Count |
| --- | ---: |
| defer_policy | 154 |
| needs_source_answer_check | 182 |
| needs_source_crop | 330 |
| regen_text_only | 1234 |

| Trigger | Count |
| --- | ---: |
| answer_sentinel_0 | 154 |
| conclusion_mismatch | 52 |
| empty_solution | 693 |
| empty_steps | 369 |
| figure_asset_present | 339 |
| placeholder_like_solution | 268 |
| pua_solution | 204 |

- conclusion_mismatch total: **52**
- conclusion_mismatch with route `regen_text_only`: **48**
- pilot batch (this doc): **30** (first 30 of the 48)

## Pilot candidate keys (30)

```
1998_4회_10 2001_1회_21 2001_1회_68 2001_3회_41 2001_3회_43 2002_1회_32 2002_3회_4 2005_3회_83 2006_1회_6 2006_1회_7 2006_2회_27 2007_1회_9 2007_2회_64 2014_2회_50 2014_3회_62 2015_1회_13 2015_1회_22 2015_1회_71 2015_1회_87 2015_2회_23 2015_2회_29 2015_3회_22 2015_3회_25 2015_3회_27 2016_1회_44 2016_1회_69 2016_1회_70 2016_1회_71 2016_3회_21 2016_3회_44
```

## Per-item detail

Each item is C1 (`conclusion_mismatch`) routed `regen_text_only`. Exclusion check
confirms: no figure asset, not an `answer=0` sentinel, route is `regen_text_only`.

### 1. `1998_4회_10`

- subject: 전기자기학 | answer (SoT): 1 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 동질，선형，등방성인 두 물질이 \(x=0\) 인 무한 평면을 경계면으로 접해있고，경계면상에는 전 류가 흐르지 않는다고 한다．지금 \(x<0\) 인 영역에서 비투지율 \(\mu_{R 1}=2\) 이고，자계 \(H_{1}=2 a_{x}-2 a_{y} +2 a_{z}[\mathrm{H} / 
- solution conclusion: ..._0(4\boldsymbol{a}_x - 8\boldsymbol{a}_y + 8\boldsymbol{a}_z) \text{ [Wb/m}^2\text{]}\] **정답: 4번** (선택지 미제시)

### 2. `2001_1회_21`

- subject: 전력공학 | answer (SoT): 2 | detected_answer_mentions: [1]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 선간 거리가 \(D\) 이고，반지름이 \(r\) 인 선로의 인덕턴스 \(L[\mathrm{mH} / \mathrm{km}]\) 은？
- solution conclusion: ...도 0.5로 오류 **(4) \( L=0.4605 \log_{10} \frac{r}{D}+0.05 \)** - 오답 - 로그 인수가 역수이고 상수항도 잘못됨 **정답: (1)번으로 추정** (문제에서 정답번호가 0으로 표기되어 있으나, 선택지 중 가장 근접한 답은 

### 3. `2001_1회_68`

- subject: 제어공학 | answer (SoT): 1 | detected_answer_mentions: [3]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 제어시스템의 정상상태 오차에서 포물선 함수 입력에 의한 정상 상태 오차를 \[K_{s}=\lim _{s \rightarrow 0} s^{2} G(s) H(s)\] 로 표현된다．이때 \(K_{s}\) 를 무엇이라고 부르는가？
- solution conclusion: ... = \lim_{s \to 0} s^2 G(s)H(s) \)는 포물선 함수 입력에 의한 오차이므로 **가속도 오차 상수(\( K_a \))**에 해당합니다. **정답: 3번 (가속도 오차 상수 또는 가속 편차 상수)**

### 4. `2001_3회_41`

- subject: 전기기기 | answer (SoT): 2 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 변압기의 부하가 증가할 때의 현상으로서 옳지 않은 것은？
- solution conclusion: ...참 (일정한 1차 전압에 의존) (3) 온도가 상승한다 → 참 (손실 증가로 발열) (4) 철손이 증가한다 → **거짓** (철손은 부하와 무관한 무부하손) **정답: (4)번** 철손은 변압기 철심의 히스테리시스 손실과 와전류 손실로서 부하의 크기와 관계없이 일정

### 5. `2001_3회_43`

- subject: 전기기기 | answer (SoT): 1 | detected_answer_mentions: [2]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 정류자형 주파수 변환기의 설명 중 틀린 것은？
- solution conclusion: ...을 3등분한 점에 각각 접속되어 있다 → **참** (4) 용량이 큰 것은 정류작용을 좋게 하기 위해 보상 권선과 보극권선을 고정자에 설치한다 → **참** **정답: (2)번** 문제에서 (2)번 보기가 불완전하게 제시되었으나, 기존 풀이에 따르면 (2)번이 정답

### 6. `2002_1회_32`

- subject: 전력공학 | answer (SoT): 1 | detected_answer_mentions: [2]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 송전 선로 고장시 대칭 좌표법에 의해 해 석할 때 정상 및 역상 임피던스가 필요한 경우는？
- solution conclusion: ...**: 정상분, 역상분, 영상분 모두 필요 ✓ - **(3) 2선 단선 고장**: 정상분, 역상분 필요 - **(4) 3선 단선 고장**: 3상 단락과 같음 **정답: 2번** (1선 접지 고장에서만 정상 및 역상 임피던스가 모두 필요함)

### 7. `2002_3회_4`

- subject: 전기자기학 | answer (SoT): 2 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 면전하 밀도가 \(\rho_{s}\left[\mathrm{C} / \mathrm{m}^{2}\right]\) 인 평면으로부터 \(r[\mathrm{~m}]\) 떨어진 점에서의 전위 \(U\) 는 몇 \(V\) 인가?
- solution conclusion: ... -\frac{dU}{dr} \] 면전하에 의한 전계 \ (E = \frac{\rho_s}{2\epsilon}\) 는 균일하므로, 전위는 거리에 선형입니다. **정답: 4번** \[ U = \frac{1}{4\pi\epsilon} \iint \frac{\rho_

### 8. `2005_3회_83`

- subject: 전기설비기술기준 | answer (SoT): 4 | detected_answer_mentions: [2]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 금속관공사에서 절연 부싱을 사용하는 가 장 주된 목적은?
- solution conclusion: ...끝부분이 전선 피복을 손상하는 것 방지) - (3) 관내 해충 및 이물질 출입 방지: 봉쇄적 목적 - (4) 명시되지 않음 **정답**: 4번 (기술기준 내용상 정답은 (2)번이며, 문제에서 "4번"이라고 표기된 것은 정정 필요) **핵심**: 절연부싱의 **주목적

### 9. `2006_1회_6`

- subject: 전기자기학 | answer (SoT): 4 | detected_answer_mentions: [3]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 유전율 \(\epsilon[\mathrm{F} / \mathrm{m}]\) ，고유저항 \(\rho[\Omega \cdot \mathrm{m}]\) 인 유 전체로 채운 정전용량 \(C[\mathrm{~F}]\) 의 콘덴서에 전압 \(V[\mathrm{~V}]\) 를 가할 때 유전체 중의 
- solution conclusion: ...2 t}{\rho}\] 근데 문제에서 유전율 ε이 주어졌으므로, 더 정밀한 해석: \[Q = \frac{0.24 CV^2 t}{\rho \epsilon}\] **정답: (3)번** (보기 표시 누락되었으나 위 식) **오답 분석:** - (1) \(4.2 \time

### 10. `2006_1회_7`

- subject: 전기자기학 | answer (SoT): 2 | detected_answer_mentions: [3]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 전계 \(E=i 2 e^{3 x} \sin 5 y-j e^{3 x} \cos 5 y+k 3 Z e^{\overline{4 z}}\) 일 때，점 \((x=0, y=0, z=0)\) 에서의 발산은？
- solution conclusion: ...)에서의 발산: \[\nabla \cdot \mathbf{E}|_{(0,0,0)} = 11e^0 \cdot 0 + 3(1+0)e^0 = 0 + 3 = 3\] **정답: (3)번 (값: 3)** **오답 이유:** - (1) 0 - 계산 완료 후 점에 대입하지 않은 

### 11. `2006_2회_27`

- subject: 전력공학 | answer (SoT): 3 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 취수구에 제수문을 설치하는 주된 목적은？
- solution conclusion: ...수문은 방수로 앞의 스크린 장비 (3) 모래를 배제하기 위하여 - 모래 배제는 사방(Sand Trap) 또는 모래제거기의 역할 - 제수문의 일차적 기능 아님 **정답: (4)번** (제시되지 않은 옵션) **핵심:** "제수문은 취수량을 조절하고 물의 유입을 단절하

### 12. `2007_1회_9`

- subject: 전기자기학 | answer (SoT): 4 | detected_answer_mentions: [2]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 벡터 \(A=i-j+3 k, B=i+a k\) 일 때 벡터 \(A\) 와 벡터 \(B\) 가 수직이 되기 위한 \(a\) 의 값은？ （단，\(i, j, k\) 는 \(x, y, z\) 방향의 기본 벡터이다．）
- solution conclusion: ...A \cdot B = 1(1) + (-1)(0) + 3\left(-\frac{1}{3}\right) = 1 + 0 - 1 = 0 \,\checkmark \] **정답: (2)번** \(a = -\dfrac{1}{3}\)

### 13. `2007_2회_64`

- subject: 회로이론 | answer (SoT): 2 | detected_answer_mentions: [1]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 특성 방정식이 \(s^{4}+2 s^{3}+5 s^{2}+4 s+2=0\) 로 주어졌을 때 이것을 훌비쯔（Hurwitz）의 안정 조건으 로 판별하면 이 계는？
- solution conclusion: ...\[D_4 = a_4 \cdot D_3 = 2 \times 16 = 32 > 0\] **안정성 판정:** 모든 행렬식이 양수이므로 **안정(Stable)** **정답: (1번) 안정** **오답 이유:** - (2) 불안정: 행렬식이 모두 양수가 아닌 경우 - (

### 14. `2014_2회_50`

- subject: 전기기기 | answer (SoT): 3 | detected_answer_mentions: [2]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 동기전동기의 위상특성곡선（ V 곡선）에 대한 설명으로 옳은 것은？
- solution conclusion: ... V곡선의 정확한 정의 (3) ❌ "계자전류를 일정" - 이는 오히려 V곡선을 만드는 것과 반대 (4) ❌ "역률을 일정" - V곡선은 역률이 변하는 곡선임 **정답: 2번 (보기 번호상 2번)** **핵심 암기 포인트** V곡선 = (단자전압 + 출력)일정 조

### 15. `2014_3회_62`

- subject: 회로이론 | answer (SoT): 4 | detected_answer_mentions: [1]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 단위계단함수의 라플라스변환과 \(z\) 변환함수는？
- solution conclusion: ...ac{z}{z-1} \] 변환표: | f(t) | F(s) | F(z) | |------|------|------| | u(t) | 1/s | z/(z-1) | 정답: 1번 (\( \frac{1}{s}, \frac{z}{z-1} \)) 오답 이유: - 2번: s

### 16. `2015_1회_13`

- subject: 전기자기학 | answer (SoT): 1 | detected_answer_mentions: [2]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 공기 중에서 \(x\) 방향으로 진행하는 전자파가 있다． \[E_{y}=3 \times 10^{-2} \sin \omega(x-v t)[\mathrm{V} / \mathrm{m}], \quad E_{z}=4 \times 10^{-2} \sin \omega(x-v t)[\mathrm{V}
- solution conclusion: ... 6.63 \times 10^{-6} \times \frac{1}{2} = 3.31 \times 10^{-6} \text{ [W/m}^2\text{]} \] **정답: 2번** (\( 6.63 \times 10^{-6} \cos^2\omega(x-vt) \) -

### 17. `2015_1회_22`

- subject: 전력공학 | answer (SoT): 1 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 송전계통의 안정도를 향상시키는 방법이 아닌 것은?
- solution conclusion: ...적게 한다**는 것이 정답입니다. 이는 안정도 향상의 표준적인 대책에 포함되지 않습니다. **정답: (4)** (문제에서 답을 1번이라 표기했으나, 보기 구성상 정답은 (4)번입니다)

### 18. `2015_1회_71`

- subject: 전기자기학 | answer (SoT): 4 | detected_answer_mentions: [1, 1]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 권수가 2000 회이고, 저항이 \(12[\Omega]\) 인 솔레노이드에 전류 \(10[\mathrm{~A}]\) 를 흘릴 때, 자속이 \(6 \times \overline{10^{-2}}\) [Wb]가 발생하였다. 이 회로의 시정수[sec]는?
- solution conclusion: ...%에 도달하는 시간을 의미합니다. $$i(t) = I_f(1 - e^{-t/\tau})$$ **정답: 1번 (정정 주의: OCR에서 "0번"이라 표기되어 있으나 정답은 1번)**

### 19. `2015_1회_87`

- subject: 전기설비기술기준 | answer (SoT): 3 | detected_answer_mentions: [2]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 사무실 건물의 조명설비에 사용되는 백열전등 또는 방전등에 전기를 공급하는 옥내 전로의 대지 전압은 몇 [V] 이하인가?
- solution conclusion: ... 또는 방전등에 전기를 공급하는 옥내 전로의 대지전압은 300[V] 이하여야 합니다. **정답 도출:** 규정상 명시된 값: 대지전압 ≤ 300[V] 따라서 **정답: 2번 (300[V])** **참고:** - 250[V]는 일부 특정 용도의 제한이 아님 - 3

### 20. `2015_2회_23`

- subject: 전력공학 | answer (SoT): 3 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 중거리 송전선로의 \(\pi\) 형 회로에서 송전단전류 \(I_{s}\) 는？（단，\(Z, Y\) 는 선로의 직렬 임피던스와 병렬 어드미턴스이고 \(E_{r}, I_{r}\) 은 수전단 전압과 전류이다．）
- solution conclusion: ... 송전단 전류: $$I_s = Y\left(1 + \frac{ZY}{4}\right)E_r + \left(1 + \frac{ZY}{2}\right)I_r$$ **정답: (4)번** **보기 검토:** - (1): 송전단 전압 공식 - (2): 형태는 맞으나 계수가 

### 21. `2015_2회_29`

- subject: 전력공학 | answer (SoT): 1 | detected_answer_mentions: [2]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 이상전압의 파고치를 저감시켜 기기를 보호하기 위하여 설치하는 것은?
- solution conclusion: ...(아크)를 유도하여 애자 손상 방지 **(4) 아모로드(Armour Rod)** - 용도: 전선의 진동에 의한 단선 방지 - 위치: 전선 고정점 근처에 설치 **정답: 2번 (피뢰기)** 피뢰기는 이상전압(뇌 서지, 개폐 과전압 등)의 파고치를 빠르게 흡수하고 

### 22. `2015_3회_22`

- subject: 전력공학 | answer (SoT): 4 | detected_answer_mentions: [1]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 송전선로에서 변압기의 유기 기전력에 의해 발생하는 고조파중 제 3 고조파를 제거하기 위 한 방법으로 가장 적당한 것은?
- solution conclusion: ...동으로 상쇄 - (2) 동기조상기 설치 → 역률 개선용(고조파 제거 X) - (3) 직렬 리액터 → 5고조파 제거용 - (4) 전력용 콘덴서 → 역률 개선용 **정답: 1번 (변압기 △ 결선)**

### 23. `2015_3회_25`

- subject: 전력공학 | answer (SoT): 1 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 보호 계전기의 반한시•정한시 특성은？
- solution conclusion: ... 동작 | 두 특성의 장점을 결합 | **각 선택지:** - (1) 반한시 특성 - (2) 순한시 특성 - (3) 정한시 특성 - (4) 반한시-정한시 특성 **정답: 4번 (반한시-정한시 특성)** 현대 보호계전 시스템은 선별성(selectivity) 향상을 

### 24. `2015_3회_27`

- subject: 전력공학 | answer (SoT): 3 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 송전계통의 안정도를 증진시키는 방법이 아닌 것은?
- solution conclusion: ...적당한 중성점 접지 방식 - 고속 차단 방식 - 재폐로 방식 (4) 고장 중의 발전기 돌입 출력의 불평형을 적게 한다 - **이는 안정도 향상과 관계없음** **정답: 4번** 고장 중 발전기의 돌입 출력 불평형은 안정도 개선과 직접적 관련이 없습니다. 안정도는

### 25. `2016_1회_44`

- subject: 전기기기 | answer (SoT): 2 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 직류기의 전기자 반작용에 의한 영향이 아닌 것은？
- solution conclusion: ... 편간의 불꽃 섬락 발생** ✓ - 중성축 이동으로 브러시가 정류 시점을 놓쳐 섬락 발생 (4) **발전기의 출력감소** ✓ - 유기기전력 감소로 출력 감소 **정답: 4번** 문제에서 "영향이 **아닌** 것"을 묻고 있으므로, 모든 선택지가 전기자 반작용의 

### 26. `2016_1회_69`

- subject: 전력공학 | answer (SoT): 1 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 주파수 응답에 의한 위치제어계의 설계에서 계통의 안정도 척도와 관계가 적은 것은？
- solution conclusion: ... - 안정도는 극의 위치(감쇠비)에 의해 결정됨 - 고유 주파수는 극의 크기만 결정 3) 결론: 보기 **(4) 고유 주파수**는 안정도 척도와 무관합니다. **정답: (4)번** **개념 설명:** 고유 주파수는 회로의 공진점을 나타내지만, 시스템이 얼마나 안정한

### 27. `2016_1회_70`

- subject: 제어공학 | answer (SoT): 2 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 나이퀴스트（Nyquist）선도에서의 임계점（ \(-1, j 0\) ）에 대응하는 보드선도에서의 이득과 위상 은？
- solution conclusion: ...(2) 0[dB], -90°: 오류 (위상값 잘못됨) - (3) 0[dB], 90°: 오류 (위상값 잘못됨) - (4) **0[dB], ±180°**: 정답 **정답: (4)번 0[dB], ±180°** **개념 설명:** - Nyquist 선도: 복소평면에서 주파

### 28. `2016_1회_71`

- subject: 제어공학 | answer (SoT): 3 | detected_answer_mentions: [1]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 평형 3상 △ 결선 회로에서 선간전압 \(\left(E_{l}\right)\) 과 상전압 \(\left(E_{p}\right)\) 의 관계로 옳은 것은？
- solution conclusion: ... I_p$$ 3) 문제: 평형 3상 △ 결선에서 선간전압($E_l$)과 상전압($E_p$)의 관계 - △ 결선이므로: $$\boxed{E_l = E_p}$$ **정답: (1)번 $E_l = E_p$** **비교 정리:** | 항목 | △ 결선 | Y 결선 | |--

### 29. `2016_3회_21`

- subject: 전력공학 | answer (SoT): 1 | detected_answer_mentions: [4]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 송전 거리，전력，손실률 및 역률이 일정하다면 전선의 굵기는？
- solution conclusion: ...text{상수} \Rightarrow R \propto V^2 \] \[ A \propto \frac{1}{R} \propto \frac{1}{V^2} \] **정답: 4번 - 전압의 제곱에 반비례한다** **개념 정리 (제시된 표):** - 송전전력 \((P)

### 30. `2016_3회_44`

- subject: 전기기기 | answer (SoT): 4 | detected_answer_mentions: [1]
- exclusion check: figure=no / sentinel=no / route=regen_text_only
- text_preview: 변압기에서 철손을 구할 수 있는 시험은?
- solution conclusion: ...전압 - 동손 계산: \[ P_{cu} = I_1^2 \times R_{eq} \] 3. **부하시험** - 변압기를 실제 부하 조건에서 운전하여 효율 측정 **정답: 1번 (개방 회로 시험/무부하 시험)** **오답 분석:** - (2) 단락 시험: 동손은 측

## Exclusion confirmation

- figure asset present: 0 (none)
- answer=0 sentinel: 0 (none)
- route != regen_text_only: 0 (none)
- missing conclusion_mismatch trigger: 0 (none)

All 30 pilot items are figure-free, non-sentinel, `regen_text_only` C1 candidates.
