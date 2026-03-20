# EE-Agent Project Context

## 목적
전기기사 기출문제 PDF 자동 풀이 시스템. 4-Agent 파이프라인.

## 현재 성능
- 2020년 1회: **91.7%** (77/84) / 2022년 2회: **93.8%** (75/80) / 합산: ~92.7%

## LLM
- Logic Solver: **Claude API** (solver_llm = anthropic)
- 로컬 폴백: qwen2.5:7b (Ollama, 정확도 ~42%)

## 실행
```bash
python3 scripts/run_sample.py --pdf data/20200424_1회.pdf --year 2020
python3 scripts/seed_knowledge.py  # RAG DB 재구축
```

## 핵심 설계
- PDF 2컬럼 분리: `_extract_two_column_text()` (page.width/2)
- 질문 타입 감지: calc(숫자+단위) vs concept(텍스트)
- RAG: TF-IDF (data/knowledge_store.json, 884개 — 전자기학297+전력공학134+기타)
- 프롬프트: `"selected_choice": 정답번호` (숫자 예시 금지)

## 주의사항
- Subject.ELECTROMAGNETISM = "전기자기학" (예전: "전기이론" — 변경됨)
- MAX_CONCURRENT=1 (Ollama는 동시 요청 불가)
- results.json은 실행 완료 후 덮어쓰임
