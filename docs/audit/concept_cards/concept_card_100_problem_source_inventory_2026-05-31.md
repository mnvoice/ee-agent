# 100 Problem Source Inventory

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This inventory freezes the 100 selected source rows for the open 100 Problem Expansion Validation Gate.

This file does not classify coverage, does not map cards, does not patch YAML, and does not claim gold-set or benchmark status.

## 2. Selection Rule

```yaml
source_file: app/data/questions.json
source_pool_filter: subject == "회로이론" and q_no is present
sort_order: year asc, session numeric asc, q_no asc
target_count: 100
selected_rows: first 100 rows after sorting
gold_set_claim_authorized: false
semantic_gain_claim_authorized: false
yaml_mutation_authorized: false
```

## 3. Inventory Table

| row | problem_id | source | tag | q_type | difficulty | text preview |
|---:|---|---|---|---|---:|---|
| 1 | `1998_2회_61` | `app/data/questions.json:1998_2회_61` | 원형 2차 계통의 과도응답 | 개념형 | 3 | 그림과 같이 `s` 평면상에 A, B, C, D 4개의 근이 있을 때 이 중에서 가장 빨리 정상 상태에 도달 하는 것은? |
| 2 | `1998_2회_62` | `app/data/questions.json:1998_2회_62` | 전달함수 | 계산형 | 4 | R-C 병렬 회로의 전달 함수. 초기 조건은 모두 0. |
| 3 | `1998_2회_63` | `app/data/questions.json:1998_2회_63` | 함수별 라플라스 변환 | 계산형 | 2 | R-C 병렬 회로에 지수 전압원을 사용할 때 커패시터 전류를 구하는 문제. |
| 4 | `1998_2회_64` | `app/data/questions.json:1998_2회_64` | 테브난 정리와 노튼의 정리 | 계산형 | 3 | 문제 참조/메타데이터 혼입 의심. |
| 5 | `1998_2회_67` | `app/data/questions.json:1998_2회_67` | 허용 태그 목록에 없습니다. | 암기형 | 0 | 논리식 간소화 문제. |
| 6 | `1998_4회_61` | `app/data/questions.json:1998_4회_61` | 공진 | 개념형 | 3 | 전압과 전류 위상차 조건 문제. |
| 7 | `1998_4회_63` | `app/data/questions.json:1998_4회_63` | 라플라스 변환의 초기값 정리와 최종값 정리 | 계산형 | 2 | 라플라스 변환된 전류에서 시간영역 값을 구하는 문제. |
| 8 | `1998_4회_65` | `app/data/questions.json:1998_4회_65` | 라플라스 역변환 | 개념형 | 2 | 임펄스 응답에 관한 옳지 않은 설명. |
| 9 | `1998_4회_66` | `app/data/questions.json:1998_4회_66` | 4단자 정수의 회로망 특성 | 암기형 | 2 | 여파기 종류 판별. |
| 10 | `1998_4회_67` | `app/data/questions.json:1998_4회_67` | 정보 부족 | 암기형 | 1 | 2013년도 2회 메타데이터만 보임. |
| 11 | `1998_4회_68` | `app/data/questions.json:1998_4회_68` | 피상전력 | 분석불가 | 1 | 2009년도 1회 메타데이터만 보임. |
| 12 | `1998_4회_69` | `app/data/questions.json:1998_4회_69` | 대칭분 해석 | 분석불가 | 1 | 문제 참조/메타데이터 혼입 의심. |
| 13 | `1998_4회_70` | `app/data/questions.json:1998_4회_70` | 대칭분 해석 | 분석불가 | 1 | 논리 소자 등가 판별. |
| 14 | `1998_6회_64` | `app/data/questions.json:1998_6회_64` | 신호흐름선도 | 개념형 | 3 | 신호 흐름 선도에서 전달비를 구하는 문제. |
| 15 | `1998_6회_66` | `app/data/questions.json:1998_6회_66` | Y결선과 △결선의 전압, 전류 관계 및 선전류 | 개념형 | 3 | 2013년도 1회 메타데이터만 보임. |
| 16 | `1998_6회_67` | `app/data/questions.json:1998_6회_67` | 공진 | 계산형 | 3 | 커패시터 초기 전하 없음, 스위치 직후 전류 값. |
| 17 | `1998_6회_68` | `app/data/questions.json:1998_6회_68` | 피상전력 | 암기형 | 2 | 2016년도 1회 메타데이터만 보임. |
| 18 | `1998_6회_69` | `app/data/questions.json:1998_6회_69` | R-L-C 과도현상 | 계산형 | 4 | 반파 정류파 평균값 문제. |
| 19 | `1998_6회_70` | `app/data/questions.json:1998_6회_70` | 영상임피던스와 전달정수 | 계산형 | 4 | 기본파와 고조파 전압 관련 문제. |
| 20 | `1999_3회_61` | `app/data/questions.json:1999_3회_61` | 전달함수 | 계산형 | 2 | 전달함수의 고유 각주파수. |
| 21 | `1999_3회_62` | `app/data/questions.json:1999_3회_62` | 시간추이정리 | 암기형 | 2 | 적분식의 라플라스 변환. |
| 22 | `1999_3회_63` | `app/data/questions.json:1999_3회_63` | R-L 과도현상 | 계산형 | 4 | 스위치를 닫을 때 단자 전압 시간함수. |
| 23 | `1999_3회_65` | `app/data/questions.json:1999_3회_65` | 공진 | 계산형 | 3 | 보드 선도의 안정 판정 설명. |
| 24 | `1999_4회_61` | `app/data/questions.json:1999_4회_61` | 대칭분 해석 | 개념형 | 4 | 대칭좌표법으로 3상 회로 상전압 표현. |
| 25 | `1999_4회_63` | `app/data/questions.json:1999_4회_63` | 안정도 판별법 | 계산형 | 4 | 특성방정식의 우반평면 근 개수. |
| 26 | `1999_4회_64` | `app/data/questions.json:1999_4회_64` | 전달함수 | 개념형 | 3 | 블록 선도 전달함수. |
| 27 | `1999_4회_65` | `app/data/questions.json:1999_4회_65` | Y결선과 △결선의 전압, 전류 관계 및 선전류 | 계산형 | 3 | 메타데이터 혼입 의심. |
| 28 | `1999_4회_66` | `app/data/questions.json:1999_4회_66` | 테브난 정리와 노튼의 정리 | 분석불가 | 0 | 메타데이터 혼입 의심. |
| 29 | `1999_4회_67` | `app/data/questions.json:1999_4회_67` | 피상전력 | 분석불가 | 0 | 메타데이터 혼입 의심. |
| 30 | `1999_4회_68` | `app/data/questions.json:1999_4회_68` | 피상전력 | 분석불가 | 0 | 메타데이터 혼입 의심. |
| 31 | `1999_4회_69` | `app/data/questions.json:1999_4회_69` | 피상전력 | 미분석 | 0 | 메타데이터 혼입 의심. |
| 32 | `1999_6회_61` | `app/data/questions.json:1999_6회_61` | Y결선과 △결선의 소비전력 | 계산형 | 3 | 대칭 상전압을 가한 회로의 소비전력. |
| 33 | `1999_6회_62` | `app/data/questions.json:1999_6회_62` | 저항의 직·병렬접속 | 계산형 | 2 | 전류계와 직렬 저항 관련 문제. |
| 34 | `1999_6회_66` | `app/data/questions.json:1999_6회_66` | 비정현파의 소비전력 계산 | 계산형 | 3 | 비정현파 전압·전류에 의한 전력. |
| 35 | `1999_6회_69` | `app/data/questions.json:1999_6회_69` | 4단자 정수의 회로망 특성 | 계산형 | 4 | L형 회로의 4단자 정수. |
| 36 | `2000_2회_61` | `app/data/questions.json:2000_2회_61` | R-L 과도현상 | 계산형 | 4 | 스위치 투입 후 릴레이 동작 시간. |
| 37 | `2000_2회_62` | `app/data/questions.json:2000_2회_62` | 비정현파의 실효치 계산 | 개념형 | 2 | 삼각파 푸리에 급수 전개. |
| 38 | `2000_2회_64` | `app/data/questions.json:2000_2회_64` | 전달함수 | 계산형 | 3 | 미분방정식 관계에서 전달함수 산출. |
| 39 | `2000_2회_65` | `app/data/questions.json:2000_2회_65` | 전달함수 | 계산형 | 4 | 전체 전달함수. |
| 40 | `2000_2회_67` | `app/data/questions.json:2000_2회_67` | 유도전압 조정기 | 암기형 | 2 | 변위-압력 변환 장치. |
| 41 | `2000_2회_70` | `app/data/questions.json:2000_2회_70` | 피상전력 | 암기형 | 0 | 상태변수 관련 문제. |
| 42 | `2000_4회_61` | `app/data/questions.json:2000_4회_61` | 영상임피던스와 전달정수 | 개념형 | 4 | 회로 임피던스가 R이 되기 위한 조건. |
| 43 | `2000_4회_62` | `app/data/questions.json:2000_4회_62` | 전달함수 | 개념형 | 3 | 구동점 임피던스. |
| 44 | `2000_4회_65` | `app/data/questions.json:2000_4회_65` | 전달함수 | 계산형 | 3 | 외란이 있는 블록 선도 출력. |
| 45 | `2000_4회_66` | `app/data/questions.json:2000_4회_66` | 안정도 판별법 | 암기형 | 2 | 특성방정식 근 위치와 안정 여부. |
| 46 | `2000_4회_67` | `app/data/questions.json:2000_4회_67` | 비정현파의 소비전력 계산 | 개념형 | 3 | 고조파 전류 교류의 전력. |
| 47 | `2000_6회_61` | `app/data/questions.json:2000_6회_61` | 상호인덕턴스 | 계산형 | 2 | 상호 인덕턴스 계산. |
| 48 | `2000_6회_65` | `app/data/questions.json:2000_6회_65` | 테브난 정리와 노튼의 정리 | 계산형 | 2 | 개방전압, 합성임피던스, 부하저항으로 전류 계산. |
| 49 | `2000_6회_66` | `app/data/questions.json:2000_6회_66` | z변환 | 암기형 | 3 | 신호의 z 변환 함수. |
| 50 | `2000_6회_68` | `app/data/questions.json:2000_6회_68` | 이득과 위상 | 계산형 | 3 | 주파수 응답 크기와 위상. |
| 51 | `2000_6회_69` | `app/data/questions.json:2000_6회_69` | 피상전력 | 미정 |  | 2016년도 1회 메타데이터만 보임. |
| 52 | `2000_6회_70` | `app/data/questions.json:2000_6회_70` | 공진 | 미정 |  | 2015년도 2회 메타데이터만 보임. |
| 53 | `2000_6회_74` | `app/data/questions.json:2000_6회_74` | 테브난 정리와 노튼의 정리 | 계산형 | 3 | 4단자망 파라미터 정수 서술. |
| 54 | `2000_6회_78` | `app/data/questions.json:2000_6회_78` | 테브난 정리와 노튼의 정리 | 개념형 | 3 | 지수·삼각함수 라플라스 변환. |
| 55 | `2001_1회_62` | `app/data/questions.json:2001_1회_62` | 미분류 | 미분류 | 0 | 보드 선도의 이득 곡선. |
| 56 | `2001_1회_63` | `app/data/questions.json:2001_1회_63` | 테브난 정리와 노튼의 정리 | 계산형 | 2 | 선형 회로망 단자 전압 인가 시 다른 단자 전압. |
| 57 | `2001_1회_64` | `app/data/questions.json:2001_1회_64` | 제어계의 블록선도 | 개념형 | 4 | 블록 선도 합성 전달함수 비교. |
| 58 | `2001_1회_67` | `app/data/questions.json:2001_1회_67` | 4단자 정수의 회로망 특성 | 계산형 | 3 | 회로의 4단자 정수 A. |
| 59 | `2001_1회_69` | `app/data/questions.json:2001_1회_69` | R-L-C 과도현상 | 계산형 | 2 | 저항에서 일정 시간 동안 소비되는 에너지. |
| 60 | `2001_1회_70` | `app/data/questions.json:2001_1회_70` | R-L-C 과도현상 | 계산형 | 4 | RLC 값으로 과도응답 관련 계산. |
| 61 | `2001_1회_74` | `app/data/questions.json:2001_1회_74` | 비정현파의 실효치 계산 | 미분석 |  | 불평형 3상 전류 관련 문제. |
| 62 | `2001_2회_63` | `app/data/questions.json:2001_2회_63` | R-L-C 과도현상 | 계산형 | 2 | 스위치 직후 커패시터/전류 값. |
| 63 | `2001_2회_64` | `app/data/questions.json:2001_2회_64` | 실효값과 평균값 | 계산형 | 3 | 반파 정류파 평균값. |
| 64 | `2001_2회_65` | `app/data/questions.json:2001_2회_65` | 안정도 판별법 | 암기형 | 2 | 루스-후르비츠 표 제1열 부호 변환 의미. |
| 65 | `2001_2회_68` | `app/data/questions.json:2001_2회_68` | 전달함수 | 개념형 | 4 | 미분방정식으로 표시된 계의 상태방정식. |
| 66 | `2001_2회_70` | `app/data/questions.json:2001_2회_70` | 비정현파의 실효치 계산 | 계산형 | 1 | 특성방정식 안정 조건. |
| 67 | `2001_3회_61` | `app/data/questions.json:2001_3회_61` | 피상전력 | 미분석 | 0 | RC 직렬 회로 교류 전류. |
| 68 | `2001_3회_62` | `app/data/questions.json:2001_3회_62` | 4단자 정수의 회로망 특성 | 계산형 | 3 | 4단자 회로 정수 A. |
| 69 | `2001_3회_63` | `app/data/questions.json:2001_3회_63` | 테브난 정리와 노튼의 정리 | 암기형 | 2 | 이상적인 전압원/전류원 성질. |
| 70 | `2001_3회_65` | `app/data/questions.json:2001_3회_65` | 테브난 정리와 노튼의 정리 | 미분석 | 0 | 문제 참조 메타데이터만 보임. |
| 71 | `2001_3회_66` | `app/data/questions.json:2001_3회_66` | Y결선과 △결선의 소비전력 | 계산형 | 2 | 평형 3상 부하 소비전력과 선전류. |
| 72 | `2001_3회_71` | `app/data/questions.json:2001_3회_71` | 미분류 | 분석불가 | 1 | RLC 직렬 공진회로 제3고조파 공진주파수. |
| 73 | `2001_3회_72` | `app/data/questions.json:2001_3회_72` | 피상전력 | 분석불가 |  | 구형파 라플라스 변환. |
| 74 | `2002_1회_64` | `app/data/questions.json:2002_1회_64` | 전달함수 | 계산형 | 4 | 상태방정식의 상태천이행렬. |
| 75 | `2002_1회_65` | `app/data/questions.json:2002_1회_65` | R-L 과도현상 | 계산형 | 2 | 스위치 투입 후 전류가 정상값의 63.2%에 도달하는 시간. |
| 76 | `2002_1회_69` | `app/data/questions.json:2002_1회_69` | 피상전력 | 계산형 | 2 | 유효전력과 무효전력으로 피상전력/역률 관련 계산. |
| 77 | `2002_1회_70` | `app/data/questions.json:2002_1회_70` | 피상전력 | 계산형 | 3 | 전압·전류·전력으로 역률 계산. |
| 78 | `2002_3회_63` | `app/data/questions.json:2002_3회_63` | 영상임피던스와 전달정수 | 계산형 | 4 | 영상 임피던스 조건에서 저항값 계산. |
| 79 | `2002_3회_65` | `app/data/questions.json:2002_3회_65` | 제어계의 블록선도 | 개념형 | 3 | 블록 선도 등가변환. |
| 80 | `2002_3회_67` | `app/data/questions.json:2002_3회_67` | 테브난 정리와 노튼의 정리 | 개념형 | 3 | 선형회로 중첩 관련 전류 비교. |
| 81 | `2002_3회_68` | `app/data/questions.json:2002_3회_68` | 전달함수 | 암기형 | 2 | 이상 OP 증폭기 연산기구 출력. |
| 82 | `2002_3회_69` | `app/data/questions.json:2002_3회_69` | R, L, C 직·병렬접속 | 개념형 | 3 | RL 직렬 회로의 주파수 변화에 따른 전류 궤적. |
| 83 | `2002_3회_70` | `app/data/questions.json:2002_3회_70` | 전달함수 | 개념형 | 4 | 전달함수에 계단 입력이 인가된 시스템 응답. |
| 84 | `2003_1회_63` | `app/data/questions.json:2003_1회_63` | Y결선과 △결선의 소비전력 | 계산형 | 4 | 2전력계법으로 평형 부하 3상 회로 역률 측정. |
| 85 | `2003_1회_64` | `app/data/questions.json:2003_1회_64` | 전달함수 | 개념형 | 3 | 연산 증폭기 회로 출력 전압. |
| 86 | `2003_1회_66` | `app/data/questions.json:2003_1회_66` | 공진 | 계산형 | 2 | 2단자 회로의 반공진 각주파수. |
| 87 | `2003_1회_67` | `app/data/questions.json:2003_1회_67` | 전달함수 | 계산형 | 3 | 폐루프 전달함수의 대역폭. |
| 88 | `2003_1회_70` | `app/data/questions.json:2003_1회_70` | 함수별 라플라스 변환 | 계산형 | 3 | 구형파 라플라스 변환. |
| 89 | `2003_3회_63` | `app/data/questions.json:2003_3회_63` | R-L-C 과도현상 | 계산형 | 2 | 스위치 투입 시 초기 전류. |
| 90 | `2003_3회_65` | `app/data/questions.json:2003_3회_65` | 테브난 정리와 노튼의 정리 | 암기형 | 2 | RL 직렬 회로 교류 역률. |
| 91 | `2003_3회_70` | `app/data/questions.json:2003_3회_70` | 계단함수와 경사함수의 라플라스 변환 | 계산형 | 2 | 단위계단함수 라플라스 변환. |
| 92 | `2003_3회_75` | `app/data/questions.json:2003_3회_75` | 대칭분 해석 | 분석불가 |  | 4단자망 영상 임피던스 관련 문제. |
| 93 | `2004_1회_28` | `app/data/questions.json:2004_1회_28` | 4단자 정수의 회로망 특성 | 계산형 | 3 | 4단자 정수 A, B, C, D. |
| 94 | `2004_1회_63` | `app/data/questions.json:2004_1회_63` | 허용 태그 목록에 해당하는 항목이 없습니다. | 암기형 | 2 | 게이트 명칭 판별. |
| 95 | `2004_1회_66` | `app/data/questions.json:2004_1회_66` | 테브난 정리와 노튼의 정리 | 계산형 | 2 | 등가 전류원 변환. |
| 96 | `2004_1회_68` | `app/data/questions.json:2004_1회_68` | 신호흐름선도 | 계산형 | 3 | 신호 흐름 선도 단순화. |
| 97 | `2004_1회_70` | `app/data/questions.json:2004_1회_70` | 테브난 정리와 노튼의 정리 | 미분석 | 0 | 2014년도 3회 메타데이터만 보임. |
| 98 | `2004_1회_73` | `app/data/questions.json:2004_1회_73` | 대칭분 해석 | 미분석 | 0 | 라플라스 변환 문제로 보이나 태그 혼입 의심. |
| 99 | `2004_1회_78` | `app/data/questions.json:2004_1회_78` | 정보 부족 | 분석불가 |  | 비정현파 교류 평균전력 문제. |
| 100 | `2004_1회_79` | `app/data/questions.json:2004_1회_79` | 라플라스 역변환 | 분석불가 | 0 | 4단자 정수와 전달정수 관련 문제. |

## 4. Next Step

Next allowed automated step: prepare a row-level screening table with empty mapping/classification fields, then classify rows under the frozen criteria.

Classification remains evidence only. Pressure flags are not patch, promotion, or new-card authorization.

## 5. Claim Boundary

This inventory does not claim:

- gold set completion
- benchmark status
- corpus grounding completion
- semantic gain proof
- YAML patch authorization
- `expansion_pilot` promotion to baseline
- PR #1 ready-for-review approval
- PR #1 merge approval
