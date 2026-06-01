# Concept Card MOAI Table Comparison Record

작성일: 2026-05-30 KST
작업 위치: `/Users/jeong-ujin_1/Documents/Codex/2026-05-30/ee-agent-d-3-governance-repo`

## 0. Supersession Note

본 문서는 최초에는 MOAI review table만 받은 상태에서 작성한 table-level comparison record였다.

이후 MOAI YAML 본문이 `/Users/jeong-ujin_1/circuit_theory_concept_cards_independent_draft_v0.1.yaml`로 저장되었고, Codex가 `moai_artifacts/`에 사본을 보존한 뒤 파싱 검증을 재현했다.

최신 verified-body 상태는 `concept_card_moai_verified_body_record_2026-05-30.md`를 따른다.

## 1. 입력 상태

초기 입력으로 사용자가 MOAI의 `Review Table`과 분포 통계를 제공했다.

MOAI 제공 정보:

- 독립 30-card draft 생성 완료
- risk 분포(최초 보고): LOW 17 / MEDIUM 13 / HIGH 0
- risk 분포(verified-body 정정): LOW 18 / MEDIUM 12 / HIGH 0
- possible corpus gap: yes/partial 6
- needs_human_review(verified-body 정정): yes 12
- broad-scope 명시 항목: 4
- mutation 0
- Codex 카드 비교 없음
- corpus grounding claim 없음
- final approval claim 없음

## 2. 비교 가능 범위

초기 작성 당시 MOAI YAML 본문은 제공되지 않았다. 따라서 최초 비교는 아래 범위로 제한했다.

가능:

- concept coverage 비교
- risk level 분포 비교
- broad-scope/corpus-gap 후보 비교
- human-review 후보 비교
- Codex set에 없는 MOAI concept 후보 식별
- MOAI table에서 Codex set 보강에 유용한 risk theme 식별

불가능:

- formula_core 정확성 대조
- word_roles 문장 품질 대조
- memory_logic semantic gain 대조
- YAML schema 준수 직접 검증
- 카드별 최종 merge patch 확정

## 3. Claim Boundary

초기 결과는 **table-level comparison**이었다. 최신 상태에서는 YAML body parse까지는 확인되었으나, semantic/corpus 검증은 아직 별도다.

말할 수 있는 것:

- MOAI review table과 Codex reviewed draft의 concept/risk 분포를 대조했다.
- MOAI가 제안한 human-review 후보 중 Codex set 보강에 유용한 영역을 식별했다.

아직 말하면 안 되는 것:

- MOAI YAML card 본문이 Codex보다 낫다.
- MOAI 30개가 구조 검증을 통과했다.
- corpus grounding이 전수 확인되었다.
- 최종 concept card gold set이 완성되었다.
