---
tags:
  - 전기기사/batch이력
  - 전기기사/모델사용
  - 전기기사/실패원인
  - 비용분석
created: 2026-04-29
cssclass: paper-review
---

> ee-agent batch API 실행 이력 — 어떤 모델로 무엇을 했고, 무엇이 실패했고, 왜 실패했는가

# ee-agent Batch 모델 사용 이력 + 실패 원인 분석

📅 2026년 4월 29일 작성 (전수 직접 측정)

---

## 1. 4개 batch 모델 사용 이력

| Batch 디렉토리 | 시점 | 모델 | batch_id | 용도 | 결과 |
|---------------|------|------|----------|------|------|
| `batch_phase2/` | 2026-03-20 18:18 | **Haiku 4.5** (claude-haiku-4-5-20251001) | msgbatch_01XcFUS8uPPG2KFfeT9ZWKx4 | OCR 후 3단계(인식/변환/계산) 풀이 추출 | 80건 실패 |
| `batch_figures/` | 2026-03-18 19:42 | **Sonnet 4.6** (claude-sonnet-4-6) | msgbatch_016j4UFW1YNpi6E45RGW6Hfi | figure_svg 자동 생성 시도 | **83건 실패 — 사실상 트랙 폐기** |
| `batch_solution_figures/` | 2026-03-19 17:14 | **Sonnet 4.6** (스크립트 명시) | msgbatch_01Y5wfbob3f16yPBXiBcC3aL | solution_svg 풀이 SVG 생성 | **691건 성공 / 29건 실패** |
| `batch_repair/` | 2026-03-20 20:55 | **Haiku 4.5** | (batch_ids.json) | OCR 결과 repair (선지/수식 정정) | 1,417페이지 처리, 400건 복구 |

스크립트 명시 인용 — `scripts/generate_figures_batch.py:38`:

```python
MODEL = "claude-sonnet-4-6"  # SVG 생성은 Sonnet 필요
```

→ **정책: SVG 생성은 Sonnet 사용** (사용자 결제 비용 + 품질 트레이드오프 결정)

---

## 2. 실패 원인 — batch별 분석

### 2-1. batch_phase2 (Haiku, 80건 실패)

- **원인**: `parse_failed` 80건 (100%)
- **상세**: 3단계(인식/변환/계산) 형식 파싱 실패 — 일부 섹션 누락
- **대표 사례**:
  ```
  custom_id: q_1998_2_10
  raw_preview: "# 안내문\n전기기사 기출문제를 제공해주시면 위 3단계 형식으로 풀이를 작성하겠습니다.\n
                현재 문제에서 **선택지와 수치가 누락**되어 있습니다."
  ```
- **진단**: 모델이 풀이를 만들지 않고 *안내문*을 반환. 입력 데이터(OCR 결과)에 선지/수치가 누락된 상태로 batch에 들어갔기 때문
- **근본 원인**: OCR 단계(Mathpix)에서 일부 문제의 선지/수치가 잘려 나간 채 batch_phase2에 입력 → 모델이 "데이터 부족"으로 응답 거부
- **해결 경로**: batch_repair에서 OCR 결과 정정 후 재시도 (실제로 1,417페이지 repair 진행)

### 2-2. batch_figures (Sonnet, 83건 실패 — 트랙 폐기)

- **원인**: `svg_parse_failed` 83건 (100%)
- **상세**: "SVG 태그를 찾을 수 없음"
- **대표 사례**:
  ```
  custom_id: fig_1998_2json_19
  raw_preview: '<svg viewBox="0 0 500 350" xmlns="..." font-family="Arial, san...'
  ```
- **진단**: raw_preview를 보면 모델 출력은 정상 SVG 시작. **파싱 로직 버그로 SVG 태그를 못 잡은 가능성 큼**
- **근본 원인 추정**:
  1. SVG 응답 앞에 모델 인사말("Here's the SVG: ...")이 붙어 정규식 매칭 실패
  2. 또는 SVG 태그 추출 정규식이 multi-line 처리 안 됨
- **결과**: 이 트랙 사실상 폐기 → 별도 batch_solution_figures로 전환 (figure 대신 solution 시각화로 우회)

### 2-3. batch_solution_figures (Sonnet, 29건 실패 / 691건 성공)

- **원인**:
  - `errored`: 28건 (API 에러, 96%)
  - `svg_parse_failed`: 1건 (4%)
- **대표 svg_parse 사례**:
  ```
  custom_id: sol_2016_3json_45
  raw_preview: "Looking at this image, I can see what appears to be a scenic landscape photograph..."
  ```
- **진단**: 1건은 모델이 PDF 스캔 페이지에서 *문제 그림이 아닌 다른 이미지*(풍경 사진)를 인식 → SVG 풀이 못 만듦. 입력 데이터 오염
- **errored 28건 근본 원인**: API rate limit, timeout, 또는 input token 초과 추정 (구체 메시지 미기록)
- **성공률**: 691/720 = **96%**

### 2-4. batch_repair (Haiku, 정정 작업)

- 1,417페이지 처리 → 400건 복구
- text_fixed: 13 / choices_fixed: 399 / answer_fixed: 0
- 실패 1건 (`failed_pages.json` 495B)
- 용도: batch_phase2 입력 품질 보완

---

## 3. 691건 분포 — 정책 특이점

### 과목별 (편중 강함)

| 과목 | 보유/전체 | 비율 | 정책 추정 |
|------|---------|------|----------|
| 회로이론 | 226/1,029 | **22%** | 우선순위 높음 |
| 전기기기 | 177/1,038 | **17%** | 우선순위 높음 |
| 전기자기학 | 130/1,175 | 11% | 후순위로 밀림 |
| 전력공학 | 117/1,097 | 11% | 후순위 |
| 전기설비기술기준 | 41/896 | **4.6%** | 거의 회피 (법규/암기 → SVG 의미 적음 판단 추정) |

### 연도별 (시간 편중)

- 1998~2013 (구회차): **6~14%** (균등하게 낮음)
- 2014~2022 (신회차): **20~28%** (균등하게 높음)

→ **신회차 우선 정책**

### 결제 입자

- 첫 batch: 722건 요청 → 691건 성공 (96%)
- Sonnet batch 50% 할인 적용 시 ≈ **약 $14 결제 추정**
- 즉 **회당 ~$14 가 사용자 결제 한도**였음
- 추가 batch 미실행 → 우선순위가 다른 작업(figure 시도 → 학습 도구 → study.html → 데이터 품질 복구)으로 이동

---

## 4. 핵심 결론

### 정책 = 결제 비용 트레이드오프

- "SVG 생성은 Sonnet 필요"는 **품질 정책** (Haiku는 SVG 마크업 정확도 낮음 추정)
- "722건/회"는 **결제 한도 정책** (회당 ~$14)
- "회로/기기 우선 + 신회차 우선"은 **학습 가치 기반 우선순위** (그림 많고 시각화 가치 높은 영역)
- "전기설비 회피"는 **의도적 정책** (법규/암기형 → SVG 의미 적음)
- "전기자기학 후순위"는 **의도적 정책 아님 추정** (회로/기기와 같은 그룹에 묶여야 했지만 결제 입자 한도로 밀림)

### 실패 패턴 — 3가지 카테고리

1. **입력 데이터 오염** (parse_failed): OCR 단계의 누락이 batch에 전파 → batch_repair로 부분 해결
2. **파싱 로직 버그** (svg_parse_failed in batch_figures): 모델 출력은 정상이지만 후처리 정규식 실패 → 트랙 폐기
3. **API 에러** (errored): rate limit / timeout / token 초과 추정 → retry 28건 시도

### 추가 batch 시 권장 사항

- 모델: **Sonnet 4.6 유지** (정책 정합)
- 입자: 회당 ~$14 (722건) 한도 유지 또는 확장
- 우선 영역: 회로이론(803건 미보유) + 전기자기학(1,045건 미보유) = **1,848건 / Sonnet batch ~$36**
- 분할: 1회 일괄 또는 2~3회 분할 결정 가능
- 파싱 버그: batch_figures의 svg_parse_failed 패턴 재발 방지 — 정규식 multi-line + 인사말 prefix 처리

---

## 5. 데이터 출처 (직접 측정)

- `~/Developer/ee-agent/data/batch_phase2/failed_ids.json`
- `~/Developer/ee-agent/data/batch_figures/failed_ids.json`
- `~/Developer/ee-agent/data/batch_solution_figures/failed_ids.json`
- `~/Developer/ee-agent/data/batch_repair/repair_log.json`
- `~/Developer/ee-agent/scripts/generate_figures_batch.py:38`
- `~/Developer/ee-agent/app/data/questions.json` (5,307건 전수 카운트)

§1.6 (나+라) 적용 — description 의존 없이 (a) 출처 직접 읽기.
