# Concept Card Notes Patch Record

작성일: 2026-05-30 KST
대상: `concept_card_review_summary_2026-05-30.md` 및 `ACCEPT_WITH_NOTES` card

## 1. 사전 확인

`concept_card_review_summary_2026-05-30.md`의 count와 per-card verdict를 대조했다.

확인 결과:

- summary count: `ACCEPT 20`, `ACCEPT_WITH_NOTES 10`
- 실제 per-card count: `ACCEPT 19`, `ACCEPT_WITH_NOTES 11`

불일치 원인:

- per-card table에 `ACCEPT_WITH_NOTES`가 11개인데 summary 문구가 10개로 작성됨.

## 2. 이번 patch 범위

수정할 것:

- review summary count와 문구를 `19 / 11 / 0 / 0`으로 정정
- `ACCEPT_WITH_NOTES` 11개 card의 조건·주의 문장을 좁게 보강

대상 card:

- `thevenin_equivalent.yaml`
- `z_transform.yaml`
- `maximum_power_transfer.yaml`
- `second_order_response.yaml`
- `complex_power.yaml`
- `power_factor.yaml`
- `mutual_inductance.yaml`
- `two_port_network.yaml`
- `fourier_series.yaml`
- `harmonics.yaml`
- `bode_plot.yaml`

## 3. 하지 않는 것

- 30개 전체 재작성은 하지 않는다.
- ACCEPT 19개는 건드리지 않는다.
- corpus 전수 대조는 하지 않는다.
- ee-agent repo staging/commit/push는 하지 않는다.

## 4. 성공 기준

- summary count가 per-card verdict와 일치한다.
- 30개 YAML parse와 field structure가 유지된다.
- 보강은 claim boundary를 선명하게 하는 수준으로 제한된다.
