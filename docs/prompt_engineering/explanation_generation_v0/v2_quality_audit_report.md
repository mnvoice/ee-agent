# v2 Quality Audit Report

> 2026-05-25 정규식 정책 addendum: 최초 감사의 output 후보 id 정규식은 `^[0-9]{4}_[1-3]회_[0-9]+$`였으나, `app/data/questions.json` 실제 session 분포에 `4회`, `6회`, `1,2회`가 존재해 과도하게 FORMAT_INVALID를 만들었다. 수정 정책은 `^[0-9]{4}_([1-6]회|1,2회)_[0-9]+$`이며, 아래 기존 표의 output FORMAT_INVALID 87건은 섹션 8의 재분류 결과로 대체해 해석한다.

## 1. Executive Summary

100개 v2 input/output 전수 점검 결과, 입력 쪽에는 명확한 TAG_CONTENT_MISMATCH 1건과 AMBIGUOUS 5건, 출력 쪽에는 후보 id PARSING_CONTAMINATED 4건이 확인됐다. v3로 곧장 확장하기보다 입력 선택 알고리즘을 tag + content 이중 매칭으로 재설계하는 것이 안전하다.

| 항목 | 결과 |
|---|---:|
| input CLEAN | 60 |
| input TAG_CONTENT_MISMATCH | 1 |
| input TAG_CONTENT_AMBIGUOUS | 5 |
| input TAG_CONTENT_SUSPECT | 34 |
| output VALID | 9 |
| output PARSING_CONTAMINATED | 4 |
| output FORMAT_INVALID | 87 |
| output EMPTY | 0 |
| 가설 1 시나리오 | B |
| v3 진입 권장 | 옵션 D 선행 후 진입 |

## 2. 축 1 결과: input tag-content 일관성

| input | problem_id | subject | matched_core_name | 분류 | 핵심 키워드 | 사유 |
|---|---|---|---|---|---|---|
| input_001.md | 2008_3회_1 | 전기자기학 | 전자파 | TAG_CONTENT_MISMATCH | 표피효과 | 동적7 strict: matched_core_name=전자파이나 question/solution 핵심은 표피효과 |
| input_002.md | 1998_2회_1 | 전기자기학 | 맥스웰 방정식 | CLEAN | - | 동적7 strict exact keyword matched |
| input_003.md | 1999_6회_12 | 전기자기학 | 변위전류 | TAG_CONTENT_SUSPECT | - | 동적7 strict: matched_core_name 핵심어가 본문에서 약함 |
| input_004.md | 2021_2회_19 | 전기자기학 | 전자유도 | TAG_CONTENT_SUSPECT | 유기기전력, 자속밀도 | 동적7 strict: matched_core_name 핵심어가 본문에서 약함 |
| input_005.md | 2003_1회_41 | 전기자기학 | 유기기전력 | CLEAN | 유기기전력, 유도전동기 | 동적7 strict exact keyword matched |
| input_006.md | 2012_1회_14 | 전기자기학 | 히스테리시스 | CLEAN | 전자유도, 히스테리시스 | 동적7 strict exact keyword matched |
| input_007.md | 2005_1회_33 | 전기자기학 | 표피효과 | CLEAN | 표피효과 | 동적7 strict exact keyword matched |
| input_008.md | 2000_2회_3 | 전기자기학 | 직선도체 자계 | CLEAN | 유도기전력, 플레밍 | matched_core_name keyword aligns with text/solution |
| input_009.md | 2001_3회_4 | 전기자기학 | 평행판 정전용량 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_010.md | 2004_1회_2 | 전기자기학 | 점전하 전계 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_011.md | 2002_1회_2 | 전기자기학 | 자기회로·인덕턴스 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_012.md | 2006_2회_3 | 전기자기학 | 유전체 경계조건 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_013.md | 2007_1회_14 | 전기자기학 | 자속밀도 | CLEAN | 맥스웰, 자속밀도 | matched_core_name keyword aligns with text/solution |
| input_014.md | 2009_2회_9 | 전기자기학 | 로렌츠/플레밍 힘 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_015.md | 2010_1회_4 | 전기자기학 | 고유 임피던스 | TAG_CONTENT_SUSPECT | 전자파 | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_016.md | 2011_2회_77 | 회로이론 | 라플라스 변환 | CLEAN | 라플라스 | matched_core_name keyword aligns with text/solution |
| input_017.md | 2013_1회_66 | 회로이론 | 라플라스 변환 | TAG_CONTENT_SUSPECT | - | 본문/해설 정보가 부족해 수동 검토 필요 |
| input_018.md | 2016_3회_70 | 회로이론 | 라플라스 역변환 | CLEAN | 라플라스 | matched_core_name keyword aligns with text/solution |
| input_019.md | 2018_2회_78 | 회로이론 | 라플라스 역변환 | CLEAN | 라플라스 | matched_core_name keyword aligns with text/solution |
| input_020.md | 2014_1회_62 | 회로이론 | R-L-C 과도현상 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_021.md | 2019_1회_65 | 회로이론 | R-L-C 과도현상 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_022.md | 2015_3회_61 | 회로이론 | 전달함수 | CLEAN | 공진 | matched_core_name keyword aligns with text/solution |
| input_023.md | 2020_3회_70 | 회로이론 | 전달함수 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_024.md | 2025_1회_65 | 회로이론 | 4단자망 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_025.md | 1998_4회_66 | 회로이론 | 4단자망 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_026.md | 2017_2회_75 | 회로이론 | 공진 | CLEAN | 공진 | matched_core_name keyword aligns with text/solution |
| input_027.md | 1999_3회_65 | 회로이론 | 공진 | TAG_CONTENT_SUSPECT | - | 본문/해설 정보가 부족해 수동 검토 필요 |
| input_028.md | 2026_1회_65 | 회로이론 | 신호흐름선도 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_029.md | 2022_2회_61 | 회로이론 | z변환 | CLEAN | 라플라스 | matched_core_name keyword aligns with text/solution |
| input_030.md | 2000_4회_66 | 회로이론 | 안정도 판별 | CLEAN | 안정도 | matched_core_name keyword aligns with text/solution |
| input_031.md | 2001_2회_64 | 회로이론 | 실효값과 평균값 | CLEAN | 평균값 | matched_core_name keyword aligns with text/solution |
| input_032.md | 2010_2회_70 | 회로이론 | 파고율과 파형률 | CLEAN | 실효값 | matched_core_name keyword aligns with text/solution |
| input_033.md | 2002_3회_67 | 회로이론 | 테브난·노턴 등가 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_034.md | 2004_1회_66 | 회로이론 | 테브난·노턴 등가 | CLEAN | 노튼 | matched_core_name keyword aligns with text/solution |
| input_035.md | 2003_3회_75 | 회로이론 | 대칭분 해석 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_036.md | 2005_1회_69 | 회로이론 | 대칭분 해석 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_037.md | 2006_1회_61 | 회로이론 | RLC 직병렬 임피던스 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_038.md | 2008_1회_66 | 회로이론 | RLC 직병렬 임피던스 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_039.md | 2014_1회_69 | 회로이론 | 전력 계산 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_040.md | 2019_1회_80 | 회로이론 | 전력 계산 | CLEAN | 실효값 | matched_core_name keyword aligns with text/solution |
| input_041.md | 2007_1회_68 | 제어공학 | 전달함수 | TAG_CONTENT_AMBIGUOUS | - | 같은 영역이나 정확 항목 다름: 추치 제어 |
| input_042.md | 2009_1회_66 | 제어공학 | 전달함수 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_043.md | 2013_2회_68 | 제어공학 | 안정도 | CLEAN | 안정도 | matched_core_name keyword aligns with text/solution |
| input_044.md | 2015_3회_63 | 제어공학 | 안정도 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_045.md | 2011_1회_66 | 제어공학 | 근궤적 | CLEAN | 근궤적 | matched_core_name keyword aligns with text/solution |
| input_046.md | 2012_2회_72 | 제어공학 | 근궤적 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_047.md | 2017_1회_76 | 제어공학 | 라플라스·정상상태오차 | CLEAN | 라플라스 | matched_core_name keyword aligns with text/solution |
| input_048.md | 2018_1회_61 | 제어공학 | 라플라스·정상상태오차 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_049.md | 2021_1회_67 | 제어공학 | 시간응답·과도응답 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_050.md | 2025_1회_77 | 제어공학 | 시간응답·과도응답 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_051.md | 2016_1회_63 | 제어공학 | 주파수응답·나이퀴스트 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_052.md | 2020_1회_62 | 제어공학 | 주파수응답·나이퀴스트 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_053.md | 2022_2회_64 | 제어공학 | PID/정상오차 | CLEAN | 블록선도 | matched_core_name keyword aligns with text/solution |
| input_054.md | 1999_6회_70 | 제어공학 | 블록선도 | TAG_CONTENT_AMBIGUOUS | 시퀀스, 계전기 | 상위 topic과 하위/인접 내용 혼재: 시퀀스 |
| input_055.md | 2010_1회_64 | 제어공학 | 신호흐름선도 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_056.md | 1998_2회_52 | 전기기기 | 동기발전기 병렬운전 조건 | CLEAN | 동기발전기, 직류기 | matched_core_name keyword aligns with text/solution |
| input_057.md | 2026_1회_48 | 전기기기 | 동기기 전기자반작용 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_058.md | 2000_2회_42 | 전기기기 | 동기속도·권계수·유기기전력 | TAG_CONTENT_SUSPECT | - | 본문/해설 정보가 부족해 수동 검토 필요 |
| input_059.md | 2003_3회_59 | 전기기기 | 동기기 단락비 | TAG_CONTENT_SUSPECT | 변압기 | 본문/해설 정보가 부족해 수동 검토 필요 |
| input_060.md | 2001_1회_57 | 전기기기 | 변압기 전압변동률 | TAG_CONTENT_SUSPECT | - | 본문/해설 정보가 부족해 수동 검토 필요 |
| input_061.md | 2004_3회_22 | 전기기기 | 변압기 효율 | CLEAN | 변압기 | matched_core_name keyword aligns with text/solution |
| input_062.md | 2005_3회_42 | 전기기기 | 변압기 병렬운전 | CLEAN | 변압기 | matched_core_name keyword aligns with text/solution |
| input_063.md | 2002_1회_43 | 전기기기 | 유도전동기 토크-슬립 | CLEAN | 유도전동기 | matched_core_name keyword aligns with text/solution |
| input_064.md | 2006_1회_49 | 전기기기 | 유도전동기 전력변환 | TAG_CONTENT_SUSPECT | 유도전동기 | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_065.md | 2007_2회_41 | 전기기기 | 유도전동기 비례추이 | CLEAN | 유기기전력, 유도전동기 | matched_core_name keyword aligns with text/solution |
| input_066.md | 2008_2회_46 | 전기기기 | 변압기 등가회로 | TAG_CONTENT_SUSPECT | 변압기 | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_067.md | 2017_3회_42 | 전기기기 | 변압기 내부고장 보호 | CLEAN | 변압기, 계전기 | matched_core_name keyword aligns with text/solution |
| input_068.md | 2009_1회_53 | 전기기기 | 직류기 일반 특성 | TAG_CONTENT_SUSPECT | - | 본문/해설 정보가 부족해 수동 검토 필요 |
| input_069.md | 2011_1회_47 | 전기기기 | 변압기 일반 구조 | CLEAN | 변압기 | matched_core_name keyword aligns with text/solution |
| input_070.md | 2012_3회_52 | 전기기기 | 동기기 일반 특성 | TAG_CONTENT_AMBIGUOUS | - | 같은 영역이나 정확 항목 다름: 단락비 |
| input_071.md | 2013_1회_52 | 전기기기 | 유도전동기 일반 특성 | TAG_CONTENT_AMBIGUOUS | 유도전동기 | 상위 topic과 하위/인접 내용 혼재: 토크 |
| input_072.md | 2014_3회_53 | 전기기기 | 직류기 유기기전력 | CLEAN | 유기기전력 | matched_core_name keyword aligns with text/solution |
| input_073.md | 2016_2회_52 | 전기기기 | 변압기 권수비·전압비 | CLEAN | 변압기 | matched_core_name keyword aligns with text/solution |
| input_074.md | 2018_2회_51 | 전기기기 | 유도전동기 속도제어 | CLEAN | 유도기전력, 유도전동기 | matched_core_name keyword aligns with text/solution |
| input_075.md | 2019_1회_55 | 전기기기 | 동기전동기 V곡선 | CLEAN | 계전기 | matched_core_name keyword aligns with text/solution |
| input_076.md | 2015_2회_83 | 전기설비기술기준 | 절연내력시험전압 | CLEAN | 접지, 절연내력 | matched_core_name keyword aligns with text/solution |
| input_077.md | 2020_1회_84 | 전기설비기술기준 | 제1종 접지공사 | TAG_CONTENT_SUSPECT | 접지 | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_078.md | 2025_1회_81 | 전기설비기술기준 | 제2종 접지공사 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_079.md | 1998_4회_86 | 전기설비기술기준 | 제3종 접지공사 | TAG_CONTENT_SUSPECT | - | 본문/해설 정보가 부족해 수동 검토 필요 |
| input_080.md | 2005_3회_85 | 전기설비기술기준 | 특별 제3종 접지공사 | CLEAN | 접지 | matched_core_name keyword aligns with text/solution |
| input_081.md | 2006_2회_84 | 전기설비기술기준 | 접지공사 시설(사람 접촉 우려) | CLEAN | 접지 | matched_core_name keyword aligns with text/solution |
| input_082.md | 2021_1회_89 | 전기설비기술기준 | 전로 절연·절연저항 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_083.md | 2022_2회_81 | 전기설비기술기준 | 가공전선 이격거리 | CLEAN | 이격거리 | matched_core_name keyword aligns with text/solution |
| input_084.md | 2026_1회_93 | 전기설비기술기준 | 과전류 차단기 시설 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_085.md | 1999_4회_92 | 전기설비기술기준 | 지락차단장치 시설 | CLEAN | 차단기 | matched_core_name keyword aligns with text/solution |
| input_086.md | 2000_2회_83 | 전기설비기술기준 | 옥내배선 전선 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_087.md | 2001_1회_82 | 전기설비기술기준 | 전압 구분·시설 기준 | TAG_CONTENT_AMBIGUOUS | 접지, 절연내력 | 상위 topic과 하위/인접 내용 혼재: 절연내력, 전기설비 |
| input_088.md | 2021_1회_83 | 전기설비기술기준 | KEC/전기설비 일반 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_089.md | 2007_2회_37 | 전기설비기술기준 | 발전기·변압기 보호장치 | TAG_CONTENT_SUSPECT | - | 본문/해설 정보가 부족해 수동 검토 필요 |
| input_090.md | 2012_1회_81 | 전기설비기술기준 | 가공지선·가공공동지선 | CLEAN | 접지 | matched_core_name keyword aligns with text/solution |
| input_091.md | 2002_3회_33 | 전력공학 | 코로나 현상 | TAG_CONTENT_SUSPECT | - | 본문/해설 정보가 부족해 수동 검토 필요 |
| input_092.md | 2009_1회_29 | 전력공학 | 피뢰기 LA | TAG_CONTENT_SUSPECT | 가공지선 | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_093.md | 2004_1회_31 | 전력공학 | 소호리액터 접지방식 | CLEAN | 공진, 접지, 소호리액터 | matched_core_name keyword aligns with text/solution |
| input_094.md | 2008_2회_31 | 전력공학 | 직접접지방식 | TAG_CONTENT_SUSPECT | 계전기 | 본문/해설 정보가 부족해 수동 검토 필요 |
| input_095.md | 2003_3회_45 | 전력공학 | 차단기 종류(소호매질) | CLEAN | 차단기 | matched_core_name keyword aligns with text/solution |
| input_096.md | 2016_3회_22 | 전력공학 | 보호계전기 기능별 분류 | CLEAN | 계전기 | matched_core_name keyword aligns with text/solution |
| input_097.md | 2010_1회_27 | 전력공학 | 전력손실·전압강하 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_098.md | 2011_1회_26 | 전력공학 | 송전용량·송전전압 | TAG_CONTENT_SUSPECT | - | matched_core_name 핵심어가 question_text/solution에서 확인되지 않음 |
| input_099.md | 2014_3회_25 | 전력공학 | 장거리 송전선로·분포정수 | CLEAN | - | matched_core_name keyword aligns with text/solution |
| input_100.md | 2015_1회_25 | 전력공학 | 대칭분·단락계산 | CLEAN | - | matched_core_name keyword aligns with text/solution |

### TAG_CONTENT_MISMATCH 발견 입력

- input_001.md `2008_3회_1`: 전자파 / 동적7 strict: matched_core_name=전자파이나 question/solution 핵심은 표피효과

### TAG_CONTENT_AMBIGUOUS 발견 입력

- input_041.md `2007_1회_68`: 전달함수 / 같은 영역이나 정확 항목 다름: 추치 제어
- input_054.md `1999_6회_70`: 블록선도 / 상위 topic과 하위/인접 내용 혼재: 시퀀스
- input_070.md `2012_3회_52`: 동기기 일반 특성 / 같은 영역이나 정확 항목 다름: 단락비
- input_071.md `2013_1회_52`: 유도전동기 일반 특성 / 상위 topic과 하위/인접 내용 혼재: 토크
- input_087.md `2001_1회_82`: 전압 구분·시설 기준 / 상위 topic과 하위/인접 내용 혼재: 절연내력, 전기설비

### TAG_CONTENT_SUSPECT 발견 입력

- input_003.md `1999_6회_12`: 변위전류 / 동적7 strict: matched_core_name 핵심어가 본문에서 약함
- input_004.md `2021_2회_19`: 전자유도 / 동적7 strict: matched_core_name 핵심어가 본문에서 약함
- input_009.md `2001_3회_4`: 평행판 정전용량 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_012.md `2006_2회_3`: 유전체 경계조건 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_014.md `2009_2회_9`: 로렌츠/플레밍 힘 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_015.md `2010_1회_4`: 고유 임피던스 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_017.md `2013_1회_66`: 라플라스 변환 / 본문/해설 정보가 부족해 수동 검토 필요
- input_020.md `2014_1회_62`: R-L-C 과도현상 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_021.md `2019_1회_65`: R-L-C 과도현상 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_023.md `2020_3회_70`: 전달함수 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_027.md `1999_3회_65`: 공진 / 본문/해설 정보가 부족해 수동 검토 필요
- input_033.md `2002_3회_67`: 테브난·노턴 등가 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_036.md `2005_1회_69`: 대칭분 해석 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_038.md `2008_1회_66`: RLC 직병렬 임피던스 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_039.md `2014_1회_69`: 전력 계산 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_046.md `2012_2회_72`: 근궤적 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_057.md `2026_1회_48`: 동기기 전기자반작용 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_058.md `2000_2회_42`: 동기속도·권계수·유기기전력 / 본문/해설 정보가 부족해 수동 검토 필요
- input_059.md `2003_3회_59`: 동기기 단락비 / 본문/해설 정보가 부족해 수동 검토 필요
- input_060.md `2001_1회_57`: 변압기 전압변동률 / 본문/해설 정보가 부족해 수동 검토 필요
- input_064.md `2006_1회_49`: 유도전동기 전력변환 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_066.md `2008_2회_46`: 변압기 등가회로 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_068.md `2009_1회_53`: 직류기 일반 특성 / 본문/해설 정보가 부족해 수동 검토 필요
- input_077.md `2020_1회_84`: 제1종 접지공사 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_078.md `2025_1회_81`: 제2종 접지공사 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_079.md `1998_4회_86`: 제3종 접지공사 / 본문/해설 정보가 부족해 수동 검토 필요
- input_084.md `2026_1회_93`: 과전류 차단기 시설 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_088.md `2021_1회_83`: KEC/전기설비 일반 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_089.md `2007_2회_37`: 발전기·변압기 보호장치 / 본문/해설 정보가 부족해 수동 검토 필요
- input_091.md `2002_3회_33`: 코로나 현상 / 본문/해설 정보가 부족해 수동 검토 필요
- input_092.md `2009_1회_29`: 피뢰기 LA / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_094.md `2008_2회_31`: 직접접지방식 / 본문/해설 정보가 부족해 수동 검토 필요
- input_097.md `2010_1회_27`: 전력손실·전압강하 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음
- input_098.md `2011_1회_26`: 송전용량·송전전압 / matched_core_name 핵심어가 question_text/solution에서 확인되지 않음

### 자기학 동적 7항 특별 점검

| input | 동적 항목 | 분류 | 영향 |
|---|---|---|---|
| input_001.md | 전자파 | TAG_CONTENT_MISMATCH | 가설 1 표본에서 제외 권장 |
| input_002.md | 맥스웰 방정식 | CLEAN | 가설 1 표본 유지 가능 |
| input_003.md | 변위전류 | TAG_CONTENT_SUSPECT | 가설 1 표본 유지 가능 |
| input_004.md | 전자유도 | TAG_CONTENT_SUSPECT | 가설 1 표본 유지 가능 |
| input_005.md | 유기기전력 | CLEAN | 가설 1 표본 유지 가능 |
| input_006.md | 히스테리시스 | CLEAN | 가설 1 표본 유지 가능 |
| input_007.md | 표피효과 | CLEAN | 가설 1 표본 유지 가능 |

## 3. 축 2 결과: output 후보 리스트 정규식 검증

| output | problem_id | 분류 | 깨진 id 예시 |
|---|---|---|---|
| output_001.json | 2008_3회_1 | FORMAT_INVALID | same_core=1998_4회_17; same_core=1998_6회_19; same_core=1999_4회_5 |
| output_002.json | 1998_2회_1 | FORMAT_INVALID | same_core=1998_4회_4; same_core=1998_4회_6 |
| output_003.json | 1999_6회_12 | FORMAT_INVALID | same_core=1998_6회_2; same_core=2000_6회_19 |
| output_004.json | 2021_2회_19 | FORMAT_INVALID | same_core=1999_6회_16 |
| output_005.json | 2003_1회_41 | FORMAT_INVALID | same_core=1998_4회_41 |
| output_006.json | 2012_1회_14 | FORMAT_INVALID | same_core=1998_4회_3; same_core=1998_4회_7; same_core=1998_4회_9 |
| output_007.json | 2005_1회_33 | PARSING_CONTAMINATED | same_core=2016_2회_18]same_trap_pattern_candidates: [1998_2회_27 |
| output_008.json | 2000_2회_3 | VALID | - |
| output_009.json | 2001_3회_4 | FORMAT_INVALID | same_core=1998_4회_13; same_core=1998_6회_6; same_core=1999_4회_7 |
| output_010.json | 2004_1회_2 | FORMAT_INVALID | same_core=1998_4회_14; same_core=1998_6회_1; same_core=1998_6회_4 |
| output_011.json | 2002_1회_2 | FORMAT_INVALID | same_core=1998_4회_3; same_core=1998_4회_7; same_core=1998_4회_10 |
| output_012.json | 2006_2회_3 | FORMAT_INVALID | same_core=1998_4회_8; same_core=1998_4회_9 |
| output_013.json | 2007_1회_14 | VALID | - |
| output_014.json | 2009_2회_9 | FORMAT_INVALID | same_core=2000_4회_3; same_core=2000_4회_5; same_core=2000_6회_3 |
| output_015.json | 2010_1회_4 | FORMAT_INVALID | same_core=1999_4회_5 |
| output_016.json | 2011_2회_77 | FORMAT_INVALID | same_core=1998_4회_63; same_core=1998_4회_65 |
| output_017.json | 2013_1회_66 | FORMAT_INVALID | same_core=1998_4회_63; same_core=1998_4회_65 |
| output_018.json | 2016_3회_70 | FORMAT_INVALID | same_core=1998_4회_65 |
| output_019.json | 2018_2회_78 | FORMAT_INVALID | same_core=1998_4회_65 |
| output_020.json | 2014_1회_62 | FORMAT_INVALID | same_core=1998_6회_69 |
| output_021.json | 2019_1회_65 | FORMAT_INVALID | same_core=1998_6회_69 |
| output_022.json | 2015_3회_61 | FORMAT_INVALID | same_core=1998_4회_65; same_core=1998_6회_64; same_core=1999_4회_64 |
| output_023.json | 2020_3회_70 | FORMAT_INVALID | same_core=1998_4회_65; same_core=1998_6회_64; same_core=1999_4회_64 |
| output_024.json | 2025_1회_65 | FORMAT_INVALID | same_core=1998_4회_66; same_core=1999_6회_69 |
| output_025.json | 1998_4회_66 | FORMAT_INVALID | same_core=1999_6회_69 |
| output_026.json | 2017_2회_75 | FORMAT_INVALID | same_core=1998_4회_61; same_core=1998_6회_67; same_core=2000_6회_70 |
| output_027.json | 1999_3회_65 | FORMAT_INVALID | same_core=1998_4회_61; same_core=1998_6회_67; same_core=2000_6회_70 |
| output_028.json | 2026_1회_65 | FORMAT_INVALID | same_core=1998_6회_64 |
| output_029.json | 2022_2회_61 | FORMAT_INVALID | same_core=2000_6회_66 |
| output_030.json | 2000_4회_66 | FORMAT_INVALID | same_core=1999_4회_63 |
| output_031.json | 2001_2회_64 | PARSING_CONTAMINATED | same_core=2025_2회_62]same_trap_pattern_candidates: [1998_2회_27 |
| output_032.json | 2010_2회_70 | FORMAT_INVALID | same_core=1998_6회_70 |
| output_033.json | 2002_3회_67 | FORMAT_INVALID | same_core=1999_4회_66; same_core=2000_6회_65; same_core=2000_6회_74 |
| output_034.json | 2004_1회_66 | FORMAT_INVALID | same_core=1999_4회_66; same_core=2000_6회_65; same_core=2000_6회_74 |
| output_035.json | 2003_3회_75 | FORMAT_INVALID | same_core=1998_4회_69; same_core=1998_4회_70; same_core=1999_4회_61 |
| output_036.json | 2005_1회_69 | FORMAT_INVALID | same_core=1998_4회_69; same_core=1998_4회_70; same_core=1999_4회_61 |
| output_037.json | 2006_1회_61 | FORMAT_INVALID | same_core=1998_6회_69 |
| output_038.json | 2008_1회_66 | FORMAT_INVALID | same_core=1998_6회_69 |
| output_039.json | 2014_1회_69 | FORMAT_INVALID | same_core=1998_4회_68; same_core=1998_6회_68; same_core=1999_4회_67 |
| output_040.json | 2019_1회_80 | FORMAT_INVALID | same_core=1998_4회_68; same_core=1998_6회_68; same_core=1999_4회_67 |
| output_041.json | 2007_1회_68 | FORMAT_INVALID | same_core=1998_4회_62; same_core=1998_4회_71; same_core=1998_6회_75 |
| output_042.json | 2009_1회_66 | FORMAT_INVALID | same_core=1998_4회_62; same_core=1998_4회_71; same_core=1998_6회_75 |
| output_043.json | 2013_2회_68 | FORMAT_INVALID | same_core=1998_6회_75; same_core=2000_6회_63 |
| output_044.json | 2015_3회_63 | FORMAT_INVALID | same_core=1998_6회_75; same_core=2000_6회_63 |
| output_045.json | 2011_1회_66 | FORMAT_INVALID | same_core=1999_6회_79 |
| output_046.json | 2012_2회_72 | FORMAT_INVALID | same_core=1999_6회_79 |
| output_047.json | 2017_1회_76 | FORMAT_INVALID | same_core=1998_4회_62; same_core=1998_6회_63; same_core=1999_4회_78 |
| output_048.json | 2018_1회_61 | FORMAT_INVALID | same_core=1998_4회_62; same_core=1998_6회_63; same_core=1999_4회_78 |
| output_049.json | 2021_1회_67 | FORMAT_INVALID | same_core=1998_4회_62 |
| output_050.json | 2025_1회_77 | FORMAT_INVALID | same_core=1998_4회_62 |
| output_051.json | 2016_1회_63 | FORMAT_INVALID | same_core=1999_4회_79 |
| output_052.json | 2020_1회_62 | FORMAT_INVALID | same_core=1999_4회_79 |
| output_053.json | 2022_2회_64 | FORMAT_INVALID | same_core=1998_4회_76 |
| output_054.json | 1999_6회_70 | FORMAT_INVALID | same_core=1999_6회_73; same_core=1999_6회_78 |
| output_055.json | 2010_1회_64 | VALID | - |
| output_056.json | 1998_2회_52 | FORMAT_INVALID | same_core=1998_6회_43; same_core=1998_6회_59; same_core=1999_6회_51 |
| output_057.json | 2026_1회_48 | FORMAT_INVALID | same_core=2000_4회_47; same_core=2000_4회_52; same_core=2000_6회_42 |
| output_058.json | 2000_2회_42 | VALID | - |
| output_059.json | 2003_3회_59 | FORMAT_INVALID | same_core=1998_6회_59 |
| output_060.json | 2001_1회_57 | FORMAT_INVALID | same_core=1998_4회_42; same_core=1999_4회_59; same_core=2000_4회_41 |
| output_061.json | 2004_3회_22 | FORMAT_INVALID | same_core=2000_4회_50 |
| output_062.json | 2005_3회_42 | FORMAT_INVALID | same_core=1998_4회_64 |
| output_063.json | 2002_1회_43 | FORMAT_INVALID | same_core=1999_4회_44; same_core=1999_4회_57; same_core=2000_6회_54 |
| output_064.json | 2006_1회_49 | FORMAT_INVALID | same_core=1998_6회_60 |
| output_065.json | 2007_2회_41 | VALID | - |
| output_066.json | 2008_2회_46 | FORMAT_INVALID | same_core=1999_4회_21; same_core=1999_4회_43; same_core=2000_6회_59 |
| output_067.json | 2017_3회_42 | FORMAT_INVALID | same_core=1999_4회_21; same_core=2000_6회_59 |
| output_068.json | 2009_1회_53 | FORMAT_INVALID | same_core=1998_4회_43; same_core=1998_4회_44 |
| output_069.json | 2011_1회_47 | VALID | - |
| output_070.json | 2012_3회_52 | FORMAT_INVALID | same_core=1998_4회_56; same_core=1999_4회_46 |
| output_071.json | 2013_1회_52 | FORMAT_INVALID | same_core=1998_6회_60; same_core=1999_4회_44; same_core=1999_4회_57 |
| output_072.json | 2014_3회_53 | FORMAT_INVALID | same_core=1998_4회_43; same_core=1998_4회_44; same_core=1998_4회_47 |
| output_073.json | 2016_2회_52 | FORMAT_INVALID | same_core=1998_4회_30; same_core=2000_4회_42; same_core=2000_4회_46 |
| output_074.json | 2018_2회_51 | VALID | - |
| output_075.json | 2019_1회_55 | FORMAT_INVALID | same_core=2000_4회_47; same_core=2000_4회_52; same_core=2000_6회_42 |
| output_076.json | 2015_2회_83 | FORMAT_INVALID | same_core=1998_6회_96; same_core=1999_4회_88; same_core=1999_4회_94 |
| output_077.json | 2020_1회_84 | FORMAT_INVALID | same_core=1998_4회_83; same_core=1998_6회_84; same_core=1999_4회_89 |
| output_078.json | 2025_1회_81 | PARSING_CONTAMINATED | same_core=2016_3회_95]same_trap_pattern_candidates: [1998_2회_33 |
| output_079.json | 1998_4회_86 | FORMAT_INVALID | same_core=1998_6회_85; same_core=1999_4회_89 |
| output_080.json | 2005_3회_85 | PARSING_CONTAMINATED | same_core=2016_3회_95]same_trap_pattern_candidates: [1998_2회_33 |
| output_081.json | 2006_2회_84 | FORMAT_INVALID | same_core=2020_1; same_core=2회_91 |
| output_082.json | 2021_1회_89 | VALID | - |
| output_083.json | 2022_2회_81 | FORMAT_INVALID | same_core=1999_4회_88; same_core=1999_4회_90; same_core=1999_6회_81 |
| output_084.json | 2026_1회_93 | FORMAT_INVALID | same_core=1998_4회_84; same_core=1998_6회_88 |
| output_085.json | 1999_4회_92 | FORMAT_INVALID | same_core=1999_4회_91; same_core=1999_6회_85; same_core=2000_4회_81 |
| output_086.json | 2000_2회_83 | FORMAT_INVALID | same_core=1998_6회_81; same_core=1999_4회_91; same_core=1999_6회_82 |
| output_087.json | 2001_1회_82 | FORMAT_INVALID | same_core=1998_6회_81; same_core=1998_6회_96 |
| output_088.json | 2021_1회_83 | FORMAT_INVALID | same_core=1998_4회_77; same_core=1998_6회_81; same_core=1999_4회_83 |
| output_089.json | 2007_2회_37 | FORMAT_INVALID | same_core=1999_4회_31; same_core=2000_4회_81 |
| output_090.json | 2012_1회_81 | FORMAT_INVALID | same_core=1998_4회_86; same_core=1998_6회_85 |
| output_091.json | 2002_3회_33 | FORMAT_INVALID | same_core=1998_4회_40; same_core=1999_4회_38; same_core=2000_4회_23 |
| output_092.json | 2009_1회_29 | FORMAT_INVALID | same_core=1998_4회_22; same_core=2000_6회_28; same_core=2000_6회_40 |
| output_093.json | 2004_1회_31 | FORMAT_INVALID | same_core=1998_4회_35; same_core=1998_6회_39 |
| output_094.json | 2008_2회_31 | VALID | - |
| output_095.json | 2003_3회_45 | FORMAT_INVALID | same_core=1998_4회_22; same_core=1998_6회_83 |
| output_096.json | 2016_3회_22 | FORMAT_INVALID | same_core=1998_4회_22 |
| output_097.json | 2010_1회_27 | FORMAT_INVALID | same_core=1998_4회_26; same_core=1998_4회_32; same_core=1998_4회_36 |
| output_098.json | 2011_1회_26 | FORMAT_INVALID | same_core=1998_4회_39; same_core=1998_6회_24; same_core=1999_4회_28 |
| output_099.json | 2014_3회_25 | FORMAT_INVALID | same_core=2000_6회_26 |
| output_100.json | 2015_1회_25 | FORMAT_INVALID | same_core=1998_4회_21; same_core=1998_4회_27; same_core=1998_4회_38 |

### PARSING_CONTAMINATED 발견 output

- output_007.json: same_core=`2016_2회_18]same_trap_pattern_candidates: [1998_2회_27`
- output_031.json: same_core=`2025_2회_62]same_trap_pattern_candidates: [1998_2회_27`
- output_078.json: same_core=`2016_3회_95]same_trap_pattern_candidates: [1998_2회_33`
- output_080.json: same_core=`2016_3회_95]same_trap_pattern_candidates: [1998_2회_33`

### FORMAT_INVALID 발견 output

- output_001.json: same_core=`1998_4회_17`; same_core=`1998_6회_19`; same_core=`1999_4회_5`; same_core=`1999_6회_2`; same_core=`2000_4회_1`
- output_002.json: same_core=`1998_4회_4`; same_core=`1998_4회_6`
- output_003.json: same_core=`1998_6회_2`; same_core=`2000_6회_19`
- output_004.json: same_core=`1999_6회_16`
- output_005.json: same_core=`1998_4회_41`
- output_006.json: same_core=`1998_4회_3`; same_core=`1998_4회_7`; same_core=`1998_4회_9`; same_core=`1998_4회_10`; same_core=`1998_4회_12`
- output_009.json: same_core=`1998_4회_13`; same_core=`1998_6회_6`; same_core=`1999_4회_7`; same_core=`1999_6회_8`
- output_010.json: same_core=`1998_4회_14`; same_core=`1998_6회_1`; same_core=`1998_6회_4`; same_core=`1998_6회_7`
- output_011.json: same_core=`1998_4회_3`; same_core=`1998_4회_7`; same_core=`1998_4회_10`; same_core=`1998_4회_12`
- output_012.json: same_core=`1998_4회_8`; same_core=`1998_4회_9`
- output_014.json: same_core=`2000_4회_3`; same_core=`2000_4회_5`; same_core=`2000_6회_3`
- output_015.json: same_core=`1999_4회_5`
- output_016.json: same_core=`1998_4회_63`; same_core=`1998_4회_65`
- output_017.json: same_core=`1998_4회_63`; same_core=`1998_4회_65`
- output_018.json: same_core=`1998_4회_65`
- output_019.json: same_core=`1998_4회_65`
- output_020.json: same_core=`1998_6회_69`
- output_021.json: same_core=`1998_6회_69`
- output_022.json: same_core=`1998_4회_65`; same_core=`1998_6회_64`; same_core=`1999_4회_64`
- output_023.json: same_core=`1998_4회_65`; same_core=`1998_6회_64`; same_core=`1999_4회_64`
- output_024.json: same_core=`1998_4회_66`; same_core=`1999_6회_69`
- output_025.json: same_core=`1999_6회_69`
- output_026.json: same_core=`1998_4회_61`; same_core=`1998_6회_67`; same_core=`2000_6회_70`
- output_027.json: same_core=`1998_4회_61`; same_core=`1998_6회_67`; same_core=`2000_6회_70`
- output_028.json: same_core=`1998_6회_64`
- output_029.json: same_core=`2000_6회_66`
- output_030.json: same_core=`1999_4회_63`
- output_032.json: same_core=`1998_6회_70`
- output_033.json: same_core=`1999_4회_66`; same_core=`2000_6회_65`; same_core=`2000_6회_74`; same_core=`2000_6회_78`
- output_034.json: same_core=`1999_4회_66`; same_core=`2000_6회_65`; same_core=`2000_6회_74`; same_core=`2000_6회_78`
- output_035.json: same_core=`1998_4회_69`; same_core=`1998_4회_70`; same_core=`1999_4회_61`
- output_036.json: same_core=`1998_4회_69`; same_core=`1998_4회_70`; same_core=`1999_4회_61`
- output_037.json: same_core=`1998_6회_69`
- output_038.json: same_core=`1998_6회_69`
- output_039.json: same_core=`1998_4회_68`; same_core=`1998_6회_68`; same_core=`1999_4회_67`; same_core=`1999_4회_68`; same_core=`1999_4회_69`
- output_040.json: same_core=`1998_4회_68`; same_core=`1998_6회_68`; same_core=`1999_4회_67`; same_core=`1999_4회_68`; same_core=`1999_4회_69`
- output_041.json: same_core=`1998_4회_62`; same_core=`1998_4회_71`; same_core=`1998_6회_75`; same_core=`1999_4회_62`
- output_042.json: same_core=`1998_4회_62`; same_core=`1998_4회_71`; same_core=`1998_6회_75`; same_core=`1999_4회_62`
- output_043.json: same_core=`1998_6회_75`; same_core=`2000_6회_63`
- output_044.json: same_core=`1998_6회_75`; same_core=`2000_6회_63`
- output_045.json: same_core=`1999_6회_79`
- output_046.json: same_core=`1999_6회_79`
- output_047.json: same_core=`1998_4회_62`; same_core=`1998_6회_63`; same_core=`1999_4회_78`
- output_048.json: same_core=`1998_4회_62`; same_core=`1998_6회_63`; same_core=`1999_4회_78`
- output_049.json: same_core=`1998_4회_62`
- output_050.json: same_core=`1998_4회_62`
- output_051.json: same_core=`1999_4회_79`
- output_052.json: same_core=`1999_4회_79`
- output_053.json: same_core=`1998_4회_76`
- output_054.json: same_core=`1999_6회_73`; same_core=`1999_6회_78`
- output_056.json: same_core=`1998_6회_43`; same_core=`1998_6회_59`; same_core=`1999_6회_51`; same_core=`2000_4회_48`
- output_057.json: same_core=`2000_4회_47`; same_core=`2000_4회_52`; same_core=`2000_6회_42`; same_core=`2000_6회_45`
- output_059.json: same_core=`1998_6회_59`
- output_060.json: same_core=`1998_4회_42`; same_core=`1999_4회_59`; same_core=`2000_4회_41`; same_core=`2000_4회_42`; same_core=`2000_6회_57`
- output_061.json: same_core=`2000_4회_50`
- output_062.json: same_core=`1998_4회_64`
- output_063.json: same_core=`1999_4회_44`; same_core=`1999_4회_57`; same_core=`2000_6회_54`
- output_064.json: same_core=`1998_6회_60`
- output_066.json: same_core=`1999_4회_21`; same_core=`1999_4회_43`; same_core=`2000_6회_59`
- output_067.json: same_core=`1999_4회_21`; same_core=`2000_6회_59`
- output_068.json: same_core=`1998_4회_43`; same_core=`1998_4회_44`
- output_070.json: same_core=`1998_4회_56`; same_core=`1999_4회_46`
- output_071.json: same_core=`1998_6회_60`; same_core=`1999_4회_44`; same_core=`1999_4회_57`; same_core=`2000_4회_41`
- output_072.json: same_core=`1998_4회_43`; same_core=`1998_4회_44`; same_core=`1998_4회_47`
- output_073.json: same_core=`1998_4회_30`; same_core=`2000_4회_42`; same_core=`2000_4회_46`
- output_075.json: same_core=`2000_4회_47`; same_core=`2000_4회_52`; same_core=`2000_6회_42`
- output_076.json: same_core=`1998_6회_96`; same_core=`1999_4회_88`; same_core=`1999_4회_94`; same_core=`1999_4회_95`
- output_077.json: same_core=`1998_4회_83`; same_core=`1998_6회_84`; same_core=`1999_4회_89`; same_core=`1999_4회_93`; same_core=`1999_6회_83`
- output_079.json: same_core=`1998_6회_85`; same_core=`1999_4회_89`
- output_081.json: same_core=`2020_1`; same_core=`2회_91`
- output_083.json: same_core=`1999_4회_88`; same_core=`1999_4회_90`; same_core=`1999_6회_81`
- output_084.json: same_core=`1998_4회_84`; same_core=`1998_6회_88`
- output_085.json: same_core=`1999_4회_91`; same_core=`1999_6회_85`; same_core=`2000_4회_81`
- output_086.json: same_core=`1998_6회_81`; same_core=`1999_4회_91`; same_core=`1999_6회_82`
- output_087.json: same_core=`1998_6회_81`; same_core=`1998_6회_96`
- output_088.json: same_core=`1998_4회_77`; same_core=`1998_6회_81`; same_core=`1999_4회_83`; same_core=`1999_4회_88`
- output_089.json: same_core=`1999_4회_31`; same_core=`2000_4회_81`
- output_090.json: same_core=`1998_4회_86`; same_core=`1998_6회_85`
- output_091.json: same_core=`1998_4회_40`; same_core=`1999_4회_38`; same_core=`2000_4회_23`
- output_092.json: same_core=`1998_4회_22`; same_core=`2000_6회_28`; same_core=`2000_6회_40`
- output_093.json: same_core=`1998_4회_35`; same_core=`1998_6회_39`
- output_095.json: same_core=`1998_4회_22`; same_core=`1998_6회_83`
- output_096.json: same_core=`1998_4회_22`
- output_097.json: same_core=`1998_4회_26`; same_core=`1998_4회_32`; same_core=`1998_4회_36`; same_core=`1998_4회_37`
- output_098.json: same_core=`1998_4회_39`; same_core=`1998_6회_24`; same_core=`1999_4회_28`
- output_099.json: same_core=`2000_6회_26`
- output_100.json: same_core=`1998_4회_21`; same_core=`1998_4회_27`; same_core=`1998_4회_38`; same_core=`1998_6회_28`

### 후보 부족 입력 3건 정밀 점검

| input | output | output 분류 | 비고 |
|---|---|---|---|
| input_031.md | output_031.json | PARSING_CONTAMINATED | 후보 부족과 파싱 오염 동시 발생 |
| input_078.md | output_078.json | PARSING_CONTAMINATED | 후보 부족과 파싱 오염 동시 발생 |
| input_080.md | output_080.json | PARSING_CONTAMINATED | 후보 부족과 파싱 오염 동시 발생 |

## 4. 축 3 결과: 가설 1 검증 재계산

- 시나리오: **B**
- 자기학 동적 7항 중 1건 TAG_CONTENT_MISMATCH. 해당 건은 가설 1 계산에서 제외하고 재계산한다.

| 지표 | 기존 dyn9 | mismatch 제외 후 dyn set | static6 baseline |
|---|--:|--:|--:|
| 표본 수 | 9 | 8 | 6 |
| expand 합계 | 12 | 10 | 1 |
| 평균 expand | 1.333 | 1.250 | 0.167 |
| non-zero ratio | 1.000 | 1.000 | 0.167 |
| dynamic/static 평균 비율 | 8.00x | 7.50x | 1.00x |

- 새 target 과목 다양성(dynamic set): 전기기기, 전기설비기술기준, 전력공학, 제어공학, 회로이론
- static6 target 과목 다양성: 회로이론
- 현재 신뢰도: input_001을 제외하면 동적 표본의 cross_subject_expansion 우위는 유지되지만, v2 보고서의 숫자는 재계산본으로 대체해야 한다.

## 5. 축 4 결과: 5,331문제 시스템적 품질 추정

| 추정 항목 | 100건 관측 | 5,331건 환산 | v3 1,000건 환산 |
|---|--:|--:|--:|
| TAG_CONTENT_MISMATCH | 1 | 53 | 10 |
| TAG_CONTENT_AMBIGUOUS | 5 | 267 | 50 |
| TAG_CONTENT_SUSPECT | 34 | 1813 | 340 |
| PARSING_CONTAMINATED | 4 | 213 | 40 |
| 후보 부족 입력 | 3 | 160 | 30 |
| 후보 부족 중 오염 | 3 | 160 | 30 |

- 5,331 전체 tag-content 불일치 추정은 단순 표본 환산이므로 실제 전수율은 별도 audit가 필요하다. 다만 100건에서 이미 mismatch와 다수 ambiguous가 보였으므로 tag 단독 매칭은 v3/v_full에 부적합하다.
- 후보 풀 파싱 오염은 1건 관측됐고, 후보 부족 3건 중 1건에서 발생했다. 후보 부족 케이스가 늘면 같은 파싱 오염이 비례 확대될 위험이 있다.
- v3 1,000문제 진입은 정책 보강 없이 위험하다. 특히 input selection과 후보 문자열 formatting/parsing을 먼저 고쳐야 한다.

## 6. 권장 다음 단계

| 옵션 | 장점 | 단점 | 평가 |
|---|---|---|---|
| A. 발견된 MISMATCH/CONTAMINATED만 교체 후 v3 진입 | 빠름, v2 산출 일부 보존 | ambiguous/suspect가 남아 v3에서 반복 가능 | 보류 |
| B. input 100건 전체 재선정 후 v2 재실행 | v2 가설 검증을 깨끗하게 다시 확보 | 시간이 더 듦 | D 이후 실행 권장 |
| C. 5,331문제 데이터 정제 트랙 전환 | 근본 품질 개선 | v3 진입이 오래 지연 | 병행 권장 |
| D. 입력 선택 알고리즘 자체 재설계 | tag-content mismatch와 후보 파싱을 동시에 차단 | 구현 필요 | **추천** |

추천: **옵션 D**. 입력 선택 알고리즘에 `tag + question_text + solution` 이중/삼중 매칭을 넣고, 후보 배열은 JSON 구조 또는 줄 단위 parser-safe 형식으로 재설계한 뒤, 옵션 B처럼 v2 100건을 재선정·재실행하는 것이 가장 안전하다.

## 7. 데이터 품질 패턴 발견

| 과목 | CLEAN | MISMATCH | AMBIGUOUS | SUSPECT |
|---|--:|--:|--:|--:|
| 전기기기 | 11 | 0 | 2 | 7 |
| 전기설비기술기준 | 8 | 0 | 1 | 6 |
| 전기자기학 | 8 | 1 | 0 | 6 |
| 전력공학 | 5 | 0 | 0 | 5 |
| 제어공학 | 12 | 0 | 2 | 1 |
| 회로이론 | 16 | 0 | 0 | 9 |

- 전기자기학 동적 7항에서 tag-content mismatch가 발견됐다. 이는 가설 1의 출발점 표본을 직접 흔드는 유형이다.
- 제어공학/전기기기/전기설비의 broad topic은 하위 주제가 섞여 TAG_CONTENT_AMBIGUOUS가 자주 발생한다. 이 경우 matched_core_name을 상위명으로 둘지 하위 핵심으로 좁힐지 정책이 필요하다.
- 후보 부족과 파싱 오염은 상관관계가 있다. 후보 부족 3건 중 output_031 1건에서 parsing contamination이 발생했다.
- 개선 방향: 입력 선택 단계에서 exact keyword, negative keyword, content sanity check를 도입하고, output 생성 프롬프트에는 후보 배열을 절대 문자열로 재파싱하지 말고 입력 배열에서만 복사하라는 정책을 추가한다.

## 8. 정규식 정책 수정 후 PARSING 재분류

### 8.1 session 필드 실제 값 분포

`app/data/questions.json` 5,331개 record의 `session` 실제 분포는 다음과 같다.

| session 값 | 건수 | 해석 |
|---|--:|---|
| `1` | 97 | id 생성 시 `1회`로 정규화 필요 |
| `1,2회` | 66 | 통합 회차. 정규식에 명시 포함 필요 |
| `1회` | 1,615 | 표준 회차 |
| `2회` | 1,596 | 표준 회차 |
| `3회` | 1,441 | 표준 회차 |
| `4회` | 283 | 과거 회차. 기존 `[1-3]회` 정규식에서 누락 |
| `6회` | 233 | 과거 회차. 기존 `[1-3]회` 정규식에서 누락 |

`5회` record는 현재 데이터에는 없지만 1~6회 정책 범위 안에 포함한다. `1차`, `2차`, `기사`, `정기` 같은 별도 session 패턴은 발견되지 않았다.

### 8.2 새 후보 id 정규식

새 정책 정규식:

```regex
^[0-9]{4}_([1-6]회|1,2회)_[0-9]+$
```

이 정규식은 실제 데이터의 `1회`~`6회`와 `1,2회`를 포함한다. raw session 값 `1`은 id 생성 단계에서 `1회`로 정규화하는 것을 전제로 한다.

### 8.3 v2 output_001~100 재분류 결과

| 분류 | 기존 정규식 | 새 정규식 |
|---|--:|--:|
| VALID | 9 | 95 |
| PARSING_CONTAMINATED | 4 | 4 |
| FORMAT_INVALID | 87 | 1 |
| EMPTY | 0 | 0 |

이전 FORMAT_INVALID 87건 중 86건은 새 정규식에서 VALID로 재분류됐다. 대부분 `4회`, `6회` 회차를 기존 정규식이 허용하지 않아 생긴 가짜 invalid였다.

### 8.4 새 정규식에서도 남는 문제

**PARSING_CONTAMINATED 4건**:

| output | 오염 id 예시 | 원인 |
|---|---|---|
| output_007.json | `2016_2회_18]same_trap_pattern_candidates: [1998_2회_27` | 필드 경계/배열 문자열 파싱 오염 |
| output_031.json | `2025_2회_62]same_trap_pattern_candidates: [1998_2회_27` | 후보 부족/배열 문자열 파싱 오염 |
| output_078.json | `2016_3회_95]same_trap_pattern_candidates: [1998_2회_33` | 후보 부족/배열 문자열 파싱 오염 |
| output_080.json | `2016_3회_95]same_trap_pattern_candidates: [1998_2회_33` | 후보 부족/배열 문자열 파싱 오염 |

**FORMAT_INVALID 1건**:

| output | invalid id 예시 | 원인 |
|---|---|---|
| output_081.json | `2020_1`, `2회_91` | 하나의 id가 `2020_1`, `2회_91`로 분할됨 |

### 8.5 해석

정규식 정책 수정으로 가짜 FORMAT_INVALID는 거의 제거됐다. 남은 문제는 정규식 범위 문제가 아니라 후보 배열을 문자열로 읽으면서 다른 필드명이나 쉼표 단위가 섞이는 순수 파싱 문제다. 따라서 v3 진입 전 필요한 조치는 정규식 확장만이 아니라, 후보를 구조화된 배열로 전달하고 출력 생성기가 후보 문자열을 재파싱하지 않게 하는 것이다.

## 9. output_007/081 파싱 버그 분석

### 9.1 output_007 패턴

`input_007.md`의 후보는 다음처럼 정상이다.

```text
same_core_candidates: [2007_1회_35, 2008_3회_1, 2010_1회_29, 2013_2회_21, 2016_2회_18]
same_trap_pattern_candidates: [1998_2회_27, 1998_2회_41, 1998_2회_60, 1998_6회_62, 1998_4회_77]
```

그러나 `output_007.json`은 `related_problems.same_core`의 마지막 원소를 다음처럼 생성했다.

```text
2016_2회_18]same_trap_pattern_candidates: [1998_2회_27
```

이는 `same_core_candidates` 마지막 id와 다음 필드명 `same_trap_pattern_candidates` 및 그 첫 후보가 한 문자열로 붙은 **필드 경계 오염**이다. `input_031/078/080`처럼 same_core 후보 부족을 채우려다 trap 후보를 끌어온 패턴과 같은 계열이지만, `input_007`은 same_core 후보가 이미 5개였으므로 후보 부족 자체가 원인은 아니다. 더 정확한 원인은 후보 라인 전체를 구조화 배열이 아니라 문자열로 재파싱하면서 닫는 대괄호 뒤 필드 경계를 넘겨 읽은 것이다.

### 9.2 output_081 패턴

`input_081.md`의 후보에는 합본 회차 id가 정상적으로 들어 있다.

```text
same_core_candidates: [2005_3회_85, 2019_2회_82, 2020_1회_86, 2020_1,2회_91, 2020_4회_91, 2025_1회_81, 2025_1회_88]
```

그러나 `output_081.json`은 `2020_1,2회_91`을 하나의 id로 복사하지 못하고 다음 두 원소로 분리했다.

```text
2020_1
2회_91
```

이는 `1,2회` 내부 콤마를 배열 구분자로 오인한 **합본 회차 콤마 분리 버그**다. output_007/031/078/080의 필드 경계 오염과 원인은 모두 "후보 배열을 문자열로 재파싱"한 데 있지만, 구체 패턴은 다르다.

| output | 패턴 | 같은 계열 여부 | 직접 원인 |
|---|---|---|---|
| output_007 | 필드 경계 오염 | 031/078/080과 같은 계열 | `]same_trap_pattern_candidates: [` 경계가 id에 붙음 |
| output_081 | 합본 회차 콤마 분리 | 다른 하위 패턴 | `2020_1,2회_91` 내부 콤마를 구분자로 처리 |

### 9.3 보강 가드

`system_prompt.md` 출력 규칙에 다음 가드를 추가했다.

- `1,2회` 같은 합본 회차 id 안의 콤마는 회차 표기의 일부이며, `2020_1,2회_91`은 단일 id로 복사해야 한다.
- `same_core_candidates`와 `same_trap_pattern_candidates`의 필드 경계를 넘겨 붙이지 않는다.
- 한 후보 id에 `]`, `[`, `:`, 다른 필드명이 섞이면 그 id는 출력하지 않고 uncertainty flag를 남긴다.

### 9.4 5,331 적용 시 추정

단순 v2 100건 표본 환산 기준으로 필드 경계 오염은 4/100이므로 5,331건 적용 시 약 213건까지 재발할 수 있다. 합본 회차 콤마 분리 버그는 v2에서 1/100으로 관측되어 단순 환산 약 53건이다. 별도 상한으로는 전체 데이터의 `1,2회` record가 66건이므로, 이 회차가 related candidate에 등장하는 경로 전체가 위험 구간이다.

따라서 v2 재선정 전 안전 조건은 두 가지다. 첫째, 후보 id는 정규식 검증 전에도 배열 원소 단위로 다뤄야 한다. 둘째, id 내부의 `1,2회` 콤마를 절대 split 기준으로 쓰면 안 된다.
