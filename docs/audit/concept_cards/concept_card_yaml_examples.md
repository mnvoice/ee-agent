# Concept Card YAML Examples

```yaml
concept: RLC resonance
static_boundary: 회로이론에서 L과 C 리액턴스가 상쇄되는 조건
formula_core:
  - omega0 = 1/sqrt(LC)
  - Q = omega0 / BW
dynamic_destinations:
  - filters
  - communication tuning
  - power quality harmonic resonance
word_roles:
  resonance: 특정 주파수에 강하게 반응
  bandwidth: 허용하는 주파수의 폭
  Q: 선택의 날카로움 또는 감쇠의 작음
  selectivity: 원하는 주파수를 골라내는 능력
trigger_words:
  - 공진
  - 대역폭
  - -3dB
  - 선택도
  - 고조파
memory_logic: 공진은 주파수를 찾고, Q는 그 주파수 반응이 얼마나 날카롭고 오래 남는지 말한다.
risk: Q를 무조건 좋은 것으로 외우면 안 됨. 필터에서는 좋지만 제어 응답에서는 ringing/overshoot 위험이 된다.
extension_risk:
  level: LOW
  condition: RLC 공진, 필터, Q, bandwidth의 표준 연결 안에서는 안전함
  caution: Q를 모든 시스템에서 무조건 좋은 값으로 해석하면 안 됨
```

```yaml
concept: Laplace transform
static_boundary: 회로이론에서 미분방정식 기반 과도현상을 s-domain 대수식으로 바꾸는 도구
formula_core:
  - L{f'(t)} = sF(s) - f(0)
  - Z_L = sL
  - Z_C = 1/(sC)
dynamic_destinations:
  - control transfer function
  - system stability
  - transient response analysis
word_roles:
  transfer_function: 입력이 출력으로 바뀌는 규칙
  pole: 시스템 자연응답이 사는 위치
  zero: 응답 모양을 바꾸는 위치
  final_value: 시간이 충분히 지난 뒤 도착값
trigger_words:
  - 전달함수
  - 극점
  - 안정도
  - 과도응답
  - 최종값
memory_logic: 라플라스는 회로에서는 과도현상을 풀고, 제어에서는 pole과 transfer function으로 시스템의 성격을 말한다.
risk: pole/zero 설명을 비유로만 외우고 실제 극점 위치 계산을 놓치면 안 됨.
extension_risk:
  level: LOW
  condition: 선형 시불변 시스템과 표준 라플라스/전달함수 문맥에서는 안전함
  caution: 비선형 시스템이나 초기조건 처리에서는 단순 전달함수 설명만으로 부족함
```

```yaml
concept: Thevenin equivalent
static_boundary: 회로이론에서 복잡한 2단자 회로를 Vth와 Rth의 직렬 등가로 바꾸는 방법
formula_core:
  - Vth = open-circuit voltage
  - Rth = equivalent resistance seen from terminals
  - I_load = Vth / (Rth + R_load)
dynamic_destinations:
  - source-load interface
  - electronics input/output impedance
  - impedance matching
word_roles:
  equivalent: 특정 단자에서 보면 같다는 뜻
  source_impedance: 전원이 가진 내부 성격
  loading_effect: 부하가 앞단 회로를 끌어내리는 현상
  interface: 두 시스템이 만나는 자리
trigger_words:
  - 등가회로
  - 개방전압
  - 단락전류
  - 부하
  - 출력임피던스
memory_logic: 테브난은 회로를 줄이는 공식이 아니라, 다음 회로가 앞 회로를 어떻게 보게 되는지 설명하는 인터페이스 언어다.
risk: 종속전원, 비선형 회로, 주파수 의존 회로에서는 단순 Rth 계산이 달라질 수 있다.
extension_risk:
  level: MEDIUM
  condition: 선형 회로, 특정 동작점 또는 특정 주파수에서 사용하면 안전함
  caution: 모든 시스템 인터페이스를 테브난 하나로 설명하면 과장될 수 있음
```

```yaml
concept: symmetrical components
static_boundary: 회로이론에서 불평형 3상을 영상분, 정상분, 역상분으로 분해하는 방법
formula_core:
  - I0 = (Ia + Ib + Ic) / 3
  - a = 1∠120°
dynamic_destinations:
  - power system fault analysis
  - protection relay
  - grounding analysis
word_roles:
  positive_sequence: 정상 회전 성분
  negative_sequence: 반대 회전 성분
  zero_sequence: 세 상이 같이 움직이는 성분
  fault_path: 고장전류가 흐르는 경로
trigger_words:
  - 영상분
  - 정상분
  - 역상분
  - 지락
  - 불평형
  - 고장전류
memory_logic: 대칭좌표법은 불평형을 계산하는 공식이 아니라, 고장전류가 어떤 성분과 경로로 흐르는지 보여주는 지도다.
risk: zero sequence는 항상 흐르는 것이 아니라 귀로, 접지, 변압기 결선 조건에 따라 달라진다.
extension_risk:
  level: LOW
  condition: 전력계통 고장해석과 대칭좌표법의 표준 연결에서는 안전함
  caution: 실제 zero-sequence 경로는 접지/중성선/변압기 결선 조건을 반드시 봐야 함
```

```yaml
concept: z-transform
static_boundary: 회로이론 core보다는 broad exam-scope에서 등장하는 이산시간 변환
formula_core:
  - X(z) = sum x[n] z^(-n)
  - z = e^(sT)
  - unit delay = z^(-1)
dynamic_destinations:
  - digital control
  - discrete signal processing
  - sampled-data systems
word_roles:
  sampling: 연속 신호를 일정 간격으로 보는 것
  delay: 한 샘플 늦어지는 동작
  unit_circle: 이산 시스템의 안정 경계
  discrete_pole: 샘플마다 줄거나 커지는 비율
trigger_words:
  - z변환
  - 샘플링
  - 단위지연
  - 단위원
  - 이산시스템
memory_logic: z-transform은 라플라스가 이산시간 세계로 넘어간 것이고, 안정의 경계가 좌반평면에서 단위원 내부로 바뀐다.
risk: 회로이론 local PRIMARY corpus gap이 있으므로 core 회로이론처럼 취급하면 안 된다.
extension_risk:
  level: MEDIUM
  condition: 표준 디지털 제어/DSP 문맥에서는 안전함
  caution: 회로이론 core grounding이 아니라 broad-scope 확장이므로 corpus-gap 표시가 필요함
```
