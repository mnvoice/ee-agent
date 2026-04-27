# 세션 2026-04-27 — ee-agent 정답키 패치 + 풀이 도구 MVP

## 메타

- **시작 컨텍스트**: 사용자가 "전기기사 문제를 아이패드에서 풀어보고 싶다" 발의
- **두 트랙 동시 진행**:
  - (T1) ee-agent 정답키 추출 버그 진단 + 패치
  - (T2) 풀이 도구 MVP 빌드
- **토큰 사용**: 세션 27% / 주간 11% (스크린샷 기준 중반)
- **종료 상태**: v2 풀이 도구 + Vite 패키지 + 다음 단계 후보 정리

## 1. T1 — ee-agent 정답키 추출 버그

### 1.1 발단
solver 평가 결과에서 Q1, Q7, Q8, Q9, Q10, Q65, Q69 등이 *오답으로 잘못 집계*. solver pred는 정답인데 정답키가 1로 박혀있음.

### 1.2 진단 (CLI 위임, 3단계)
- **분포 검사**: 1번 비율 33% (균등 25%에서 +8%p) — fallback 의심
- **fallback grep**: `runner.py` `_apply_answer_key_from_explanations`. 정규식 누락 시 `correct_answer = 1` 초기값 그대로 유지
- **raw 추출**: 의심 7건 중 6건이 `NOT IN answer_map` → fallback=1 확정

### 1.3 근본 원인 (자가 정정 1회 거침)
- 1차 진단: 32건 누락 (라인 경계 정규식 시뮬레이션)
- 정정: production 정규식으로는 11건 누락 (Q1~Q11)
- 진짜 원인: `start_page = len(pdf.pages) // 2` 휴리스틱이 이 PDF에만 미스매치. 답키가 page 16-17(전체 34쪽)에 있는데 production은 page 18부터 스캔 → 앞부분 답키 통째로 누락

### 1.4 영향 범위
- 84개 PDF 중 production이 답키 추출 통과하면서 누락하는 건 **2026 1회 CBT 1개뿐**
- 다른 PDF는 추출 로직 안 타거나 통과 시 100/100

### 1.5 패치
- **(D) PDF별 start_page override** 채택 — `_ANSWER_KEY_START_PAGE_OVERRIDE` 맵에 이 PDF만 page 16
- (B) 자동 페이지 탐지는 일반화 트랙으로 별도

### 1.6 재채점 결과
- 정답키 분포: 1번 33% → **23%** (정상화)
- 진짜 점수: 84 → **89** (+5)
- Q1~Q11 변화 표:
  - 오답→정답: 7건 (Q1, Q2, Q4, Q6, Q7, Q9, Q10)
  - 정답→오답: 2건 (Q3, Q5 — fallback=1과 solver pred=1 우연 일치한 *가짜 정답*)
  - 유지 정답: 1건 (Q11)
  - 유지 오답: 1건 (Q8 — 진짜 solver 오답)

### 1.7 verify-agent 원칙 사례
"정답키도 *주장*이고 원본 PDF가 *증거*" — 84/100도 가짜 baseline이었음. Q3·Q5의 가짜 정답 발견이 핵심.

## 2. T2 — 풀이 도구 MVP

### 2.1 진화

| 버전 | 무엇 | 상태 |
|---|---|---|
| MVP-0 | 5문제 sample, 좌 PDF / 우 풀이, window.storage 진척 저장 | 흐름 검증용 |
| MVP-1 | + 학습 네비게이션 (concepts/freq/related/prereqs/cross_subject/notes) — mock 5건 | 디자인 검증용 |
| **MVP-1 결정**: notes를 *이해/암기 두 슬롯*으로 분리 (사용자 발의) | 마음에 드는 디자인 확정 |
| MVP-2 후보 (a~d) — 새 LLM 호출의 비용/품질 trade-off 검토 | (a) 채택 |
| **MVP-2 (a)** | ee-agent solver의 `agent_outputs[0].law_used` 재활용 — 새 LLM 호출 0건 | extract_solutions.py 작성 |
| **MVP-2 갱신** | 두 textarea → **펜 캔버스 1개** (Apple Pencil 압력 감지) | 현재 ee_practice_v2.jsx |

### 2.2 핵심 의사결정 트레이스

1. **그림 처리**: (γ) 페이지별 PNG 변환 채택. 단 stem-페이지 자동 매핑은 PDF 텍스트 PUA 깨짐으로 0/100. *PNG 캐러셀*이 차선책 — MVP 차단 요인 아님
2. **MVP 모드**: 연습 모드 (즉시 채점 + 노트)
3. **배포**: Artifact 먼저 → 흐름 확정 후 PWA
4. **메타데이터 깊이**: MVP-1 디자인 검증 → MVP-2 자동 추출 → MVP-3 다회차 누적
5. **(a)~(d) 비용 검토**: API 비용 회피하기 위해 (a) `law_used` 재활용 채택. 30문제 풀어본 후 부족이 구체화되면 그때 (b)/(c)/(d) 결정
6. **노트 형식**: 텍스트 2개 → 펜 1개로 통합 (사용자 발의). Apple Pencil 압력 감지 + 좌표 데이터 저장 → 향후 OCR 인식 가능

### 2.3 산출물

- `/mnt/user-data/outputs/ee_practice_v0.jsx` — MVP-0 (sample 5건, 단순)
- `/mnt/user-data/outputs/ee_practice_v1.jsx` — MVP-1 (학습 네비게이션 + 두 textarea)
- `/mnt/user-data/outputs/ee_practice_v2.jsx` — MVP-2 (a) + 펜 캔버스 (현재)
- `/mnt/user-data/outputs/extract_solutions.py` — `law_used` 재활용 스크립트
- `/mnt/user-data/outputs/enrich_meta.py` — (b)/(d) 옵션 사용 시 LLM 추출 스크립트 (보류)
- `/mnt/user-data/outputs/ee-practice/` — Vite 로컬 실행 패키지 (이번 세션 마지막)

## 3. 미해결 / 다음 단계 후보

### 3.1 ee-agent 별건
- **Q3 / Q5 진짜 답 spot check**: fallback=1과 우연 일치한 가짜 정답이 본인 풀이로도 검증되는지
- **Q65 별건**: 추출=1인데 사용자 reasoning은 3 — PDF 답안지 오류 / 사용자 풀이 오류 / 문제 결함 중 하나
- **production=0 PDF의 답키 경로**: 84개 PDF 대부분이 다른 답키 경로 사용. 풀이 도구 다른 회차 확장 시 baseline 신뢰성 점검 필요
- **자동 페이지 탐지 일반화 (B 옵션)**: 임계값 N≥3 이상인 페이지를 답키로 자동 인식

### 3.2 풀이 도구 — 30문제 풀어본 후 결정
- AI 풀이(`law_used`) 품질이 학습에 충분한가
- 부족이 *이해/암기 분리*면: (b) Gemini 무료 API or (d) Sonnet $2 일회성 LLM 추출
- 부족이 *함정 보기 식별*만이면: 그것만 좁게 추출
- 부족 안 느끼면: 종결

### 3.3 풀이 도구 일반화
- **다회차 확장**: 진짜 출제 빈도(`freq`) 산출하려면 5~10회차 누적 필요. 매 회차마다 정답키 검증 + concept 추출
- **펜 입력 OCR**: 좌표 데이터 → MyScript / Google digital ink / Apple PencilKit으로 텍스트 변환. 한국어+수식 모델 필요
- **PDF 페이지 자동 매핑**: 현재 0/100. PUA 우회 방법 — vision_solver 호출 직전 페이지 번호 별도 로깅 등

### 3.4 Vite 프로젝트 → PWA → 호스팅
- 로컬 Vite로 iPad 같은 와이파이 접속 (이번 세션 산출)
- PWA manifest로 홈화면 추가 (이번 세션 일부 포함)
- Vercel/GitHub Pages 호스팅으로 어디서든 접속 (다음 단계)

## 4. 메타 관찰

### 4.1 §1.5 자기 적용 실패 1회
세션 초반 §3.1 항목 2~4를 형식적으로 진술하여 사용자 차단됨. 항목 1로 진술의 본질이 끝났는데 4개 항목 슬롯을 (a) 출처처럼 처리. 사용자 메시지: *"§1.5 자기 적용 또 실패. 사례 6과 같은 패턴."* 차단 후 즉시 정상 작업으로 복귀.

### 4.2 verify-agent 원칙의 ee-agent 적용
- "주장은 증거가 아니다"가 ee-agent 정답키에 직접 적용됨 (T1)
- AI 풀이(`law_used`)도 *주장*이지 *증거*가 아님 — 풀이 도구에 "AI 생성 텍스트 · 검증되지 않음 · 참고용" 명시 (T2)

### 4.3 비용 의식
사용자가 토큰 사용량을 명시적으로 언급("새창을 띄우면서 쓴 토큰이 이 정도야"). API 비용 결정에서도 "꼭 API 써야 하나?" 발의 → (a) `law_used` 재활용으로 비용 0 옵션 채택. *주장 검증을 작은 N으로 먼저 → 큰 N에 적용* (D51b-1 패턴)이 비용 검토에도 그대로 적용됨.

## 5. 세션 종료 시점 권고

다음 세션 첫 작업: **30문제 풀어보기 (Vite + iPad 접속)**. 그 후 부족이 무엇인지 *실데이터로* 결정.
