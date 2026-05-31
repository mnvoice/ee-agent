# circuit_theory_concept_cards_independent_draft_v0.1 — Review Table

> Companion to `circuit_theory_concept_cards_independent_draft_v0.1.yaml`
>
> **Status**: INDEPENDENT_DRAFT (NOT compared to Codex reviewed-draft 30-card set)
> **Claim boundary**:
> - corpus-wide grounding NOT verified
> - NOT final learning material
> - broad-scope items are NOT core circuit-theory concepts
> - semantic gain NOT proven
>
> **Mutation counters** (vs accepted artifacts): all 0
> **Forbidden grounding checks**: all false (answer key / generated solution / generated explanation / generated rationale / evidence card summary — none used as grounding)

## Review Table (30 cards)

| # | concept | risk_level | possible_corpus_gap | overextension_risk | needs_human_review |
|---|---------|-----------|---------------------|--------------------|--------------------|
| 1 | KVL/KCL | LOW | no | 분포 정수·고주파 전송선에서 무리 적용 시 | no |
| 2 | 노드/메쉬 해석 | LOW | no | 비선형 대신호 직접 적용 시 | no |
| 3 | 전원 등가 변환 | LOW | no | 내부 손실 비교에 사용할 때 | no |
| 4 | 중첩의 원리 | LOW | no | 부분 응답 전력 단순 합산 시 | no |
| 5 | 테브난·노턴 | LOW | no | 종속 전원 회로에서 R_TH 산출법 오류 | no |
| 6 | 최대 전력 전달 | MEDIUM | no | 전력 계통 운용 기준으로 적용 시 | yes |
| 7 | 페이저·복소 임피던스 | LOW | no | 비정현·과도에 적용 시 | no |
| 8 | RLC 직렬 공진 | LOW | no | "공진=좋다" 일반화 | no |
| 9 | RLC 병렬 공진 | LOW | no | 손실 큰 인덕터에 이상식 적용 시 | no |
| 10 | Q·BW | MEDIUM | no | 광대역·다중공진·2차계 제어 응답으로 무리 확장 시 | yes |
| 11 | 교류 4전력 | LOW | no | 비정현 부하에 cos(theta)만으로 적용 시 | no |
| 12 | 역률 개선 | LOW | partial(고조파 부하 시) | 고조파 환경에서 직렬 리액터 없이 콘덴서만 사용 | no |
| 13 | 3상 평형 Y/Δ | LOW | no | 불평형 회로에 직접 적용 시 | no |
| 14 | 3상 평형 전력 | LOW | no | 불평형·고조파에서 단일식 적용 시 | no |
| 15 | 대칭 좌표법 | MEDIUM | yes (전력공학 경계) | 고장 종류별 결합식 미구분 시 | yes |
| 16 | 1차 과도응답 | LOW | no | y(0+) ≠ y(0-) 혼동 | no |
| 17 | 2차 과도응답 | MEDIUM | no | zeta = 1/(2Q) 가정 한계 무시 시 | yes |
| 18 | 라플라스 변환 | LOW | no | 초기 조건 항 누락 | no |
| 19 | 초기값·최종값 정리 | MEDIUM | no | 성립 조건 미확인 적용 | yes |
| 20 | 전달함수 H(s) | MEDIUM | no | 비선형·시변 시스템에 적용 시 | yes |
| 21 | 필터 분류·차단주파수 | LOW | no | 1차 차단 vs 2차 공진 혼동 | no |
| 22 | 보드 선도 | MEDIUM | yes (제어공학 경계) | 점근선만 보고 공진 첨두 누락 | yes |
| 23 | 2-port (Z/Y/h/ABCD) | LOW | no | 비양방향·강한 비선형 단 적용 시 | no |
| 24 | 영상 임피던스 | MEDIUM | no | 최대 전력 정합과 혼동 | yes |
| 25 | 가역성 정리 | LOW | no | "모든 회로 가역적" 일반화 | no |
| 26 | 푸리에 급수/고조파 | LOW | no | 비선형 부하에 단순 합산 적용 시 | no |
| 27 | 비정현파 전력·왜형 역률 | MEDIUM | no | 일반 PF = cos(theta)만으로 풀 때 | yes |
| 28 | 라우스-후르비츠 | MEDIUM | yes (제어공학 경계) | 1열 0 케이스 보정 누락 | yes |
| 29 | 상태공간 | MEDIUM | yes (제어공학 경계) | 두 표현 동등성을 행렬 직접비교로 판단 시 | yes |
| 30 | z-변환 | MEDIUM | yes (디지털 경계) | 안정 영역 LHP vs 단위원 혼동 | yes |

## Distribution (verified by grep on YAML)

| 지표 | 수치 |
|------|-----|
| 총 카드 수 | 30 |
| extension_risk LOW | 18 (60%) |
| extension_risk MEDIUM | 12 (40%) |
| extension_risk HIGH | 0 |
| possible_corpus_gap = yes/partial | 6 (20%) |
| needs_human_review = yes | 12 (40%) |
| broad-scope 명시 항목 | 4 (22 보드선도, 28 라우스, 29 상태공간, 30 z변환) |

> 정정 기록: 본 표는 YAML grep으로 실측 (LOW 18 / MEDIUM 12). 직전 채팅 응답에 17/13으로 잘못 적혔던 부분을 정정함.

## Concept Selection Rationale

| 범주 | 카드 | 의도 |
|------|-----|------|
| Core DC 해석 | 1-5 | 회로이론 첫 학습 단계 |
| Core 정합·전력 전달 | 6 | static→dynamic의 대표 예 |
| Core AC 정상상태 | 7-12 | 시험 빈출 핵심 |
| Core 3상 | 13-14 | 시험 빈출, 전력공학 연결점 |
| 전력공학 경계 | 15 | broad-scope 명시 |
| 과도/시정수 | 16-17 | 1차·2차 모두 |
| s-domain 도구 | 18-20 | 라플라스·H(s) |
| 주파수 응답 | 21-22 | LTI 필터·Bode |
| Network 표현 | 23-25 | 2-port·영상·가역성 |
| 비정현 | 26-27 | 푸리에·왜형 역률 |
| 제어공학 경계 | 28-29 | broad-scope 명시 |
| 디지털 경계 | 30 | broad-scope 명시 |

## What this artifact does NOT claim

- 본 30장은 Codex reviewed-draft 30-card set과 **비교되지 않았음**
- pilot30 / v0.1 accepted 카드와 **개념 매핑 검증 안 됨**
- 전기기사 회로이론 corpus와의 **grounding 검증 안 됨**
- semantic learning gain **미증명**
- DATA_KEY 후보 / OCR figure 경고와의 연결성 **없음**
- 시험 합격 보장 **없음**
- 정식 학습 자료 아님 — **검토용 draft**

## Next-step options (사용자/Codex 결정)

1. 본 draft를 Codex reviewed-draft 30 카드와 직접 비교 (Codex 카드 paste 또는 TCC 해제 필요)
2. 본 draft 중 needs_human_review = yes 13장만 별도 점검
3. 본 draft를 폐기·보류·참조 자료로만 사용
4. 본 draft 카드 중 일부를 Codex pilot30 카드와 매핑해 보완 자료로 활용

---

DRAFT_30_CARDS_FOR_REVIEW
