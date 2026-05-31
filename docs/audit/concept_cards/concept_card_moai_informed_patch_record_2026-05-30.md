# Concept Card MOAI-informed Patch Record

작성일: 2026-05-30 KST
근거: `concept_card_moai_table_comparison_summary_2026-05-30.md`

## 1. 목적

MOAI review table 비교에서 나온 신호 중, 즉시 반영 가능한 최소 수정만 적용한다.

## 2. 이번 patch 범위

수정:

- `concept_cards/symmetrical_components.yaml`
  - `extension_risk.level`: LOW → MEDIUM
  - condition/caution을 전력계통 고장해석 경계가 보이도록 보강

생성:

- `concept_card_expansion_backlog_2026-05-30.md`

## 3. 하지 않는 것

- MOAI draft로 Codex card를 교체하지 않는다.
- 11개 expansion 후보 card를 지금 생성하지 않는다.
- corpus grounding 전수 확인을 주장하지 않는다.
- gold set 승격을 주장하지 않는다.

## 4. 성공 기준

- 30개 YAML parse와 field structure가 유지된다.
- `symmetrical_components.yaml`의 risk level이 table comparison 결과와 정합한다.
- expansion 후보가 backlog로 분리된다.
