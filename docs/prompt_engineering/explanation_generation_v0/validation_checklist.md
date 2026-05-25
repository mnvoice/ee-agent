# Validation Checklist v0

이 체크리스트는 Claude Code가 생성한 JSONL 결과를 Codex 검증 단계에서 확인하기 위한 기준이다.

## 1. JSON 스키마

- JSON 객체 하나만 출력했는가.
- `output_schema.json`으로 파싱/검증이 통과하는가.
- enum 값이 허용 목록과 정확히 일치하는가.
- 정답이 아닌 모든 선택지가 `distractor_analysis`에 들어갔는가.
- `uncertainty_flags`가 배열로 존재하는가.

## 2. 핵심 추출 5줄

- `phenomenon`은 실제 현상을 말하는가, 단원명을 반복하지 않는가.
- `problem`은 막아야 할 위험, 구해야 할 값, 해결해야 할 구조를 말하는가.
- `device_or_concept`는 장치/개념이 어떻게 해결하는지 말하는가.
- `memorize`는 시험장에서 꺼낼 3~5개 키워드 수준으로 압축됐는가.
- `trap_pattern`은 보기 함정 한 줄로 작동하는가.

## 3. 정답/오답 분석

- `why_correct`가 정답 문장 반복이 아니라 핵심과 연결되는가.
- `correct_type`이 문제 성격과 맞는가.
- 오답 분석이 진짜 헷갈림을 짚는가.
- 전기기기·전력·설비의 S/Fault 또는 S/Conversion 문제에서 동적/고장/변환 압축이 설명됐는가.
- 자기학·회로·제어의 정직한 문제를 억지 함정으로 만들지 않았는가.

## 4. 연관 문제 검증

- `same_core`의 모든 id가 입력 `same_core_candidates`에 존재하는가.
- `same_trap_pattern`의 모든 id가 입력 `same_trap_pattern_candidates`에 존재하는가.
- 모든 연관 문제 id가 `^[0-9]{4}_([1-6]회|1,2회)_[0-9]+$` 정규식을 통과하는가. `]`, `[`, `:`, 다른 필드명, 후보 라벨이 섞인 id는 PARSING_CONTAMINATED로 판정한다.
- 같은 핵심과 같은 함정 패턴을 섞지 않았는가.
- 후보가 없을 때 빈 배열과 uncertainty flag를 남겼는가.

## 5. 학습 메타

- `v32_core_id`가 입력 matched_core_id와 일치하는가. 없으면 `null`인가.
- `phenomenon_origin`이 입력과 일치하거나, 입력이 없을 때 추정 근거가 uncertainty_flags에 남았는가.
- `trap_map_61_member`가 입력 `is_trap_map_member`와 일치하는가.
- `study_priority`가 별점, 함정 여부, 과목 연결성을 반영하는가.
- `study_phase`가 핵심 학습 단계와 맞는가.

## 6. 실패/재시도 기준

- JSON 파싱 실패: 같은 입력으로 1회 재시도. 재시도 프롬프트에는 "JSON only, no markdown"을 첫 줄에 추가.
- 스키마 실패: 실패 필드와 enum 목록만 추가해 1회 재시도.
- 연관 문제 후보 밖 id 출력: related_problems를 빈 배열로 강제해 1회 재시도.
- core_extraction이 정의 나열 수준: 피뢰기 모범 사례를 재삽입해 1회 재시도.
- 2회 재시도 후 실패: 해당 problem_id를 `failed_explanations_v0.jsonl`에 입력, 오류, 마지막 출력과 함께 저장.
