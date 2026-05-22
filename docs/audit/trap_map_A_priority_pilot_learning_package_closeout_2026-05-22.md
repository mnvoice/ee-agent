# Trap-Map A-Priority — Pilot Learning Package Closeout (2026-05-22)

trap-map A-priority 26항 학습 패키지 트랙을 공식 종료하는 closeout 문서다.
상태 인계용으로 자기충족적이며, 새 사실을 만들지 않고 기존 리뷰 결과와 commit
chain을 요약한다.

app/data 미수정. solution/steps 미적용. answer/choices/text 미수정. 유료 API
미호출. local server 미실행. 기존 commit amend/rebase/reset 없음.

---

## 1. 최종 결론

- **A-priority 26항 pilot learning package — PASS.**
- package 통합 리뷰(`d6c3a73`) 결과: 7개 기준 전부 PASS, P0·P1·사실 오류·범위 외
  혼입·wrong mapping 0건. P2 1건(accepted residual, Section 5).
- **학습자 사용 준비 완료** — Day 1~4 전 과정을 26항 6칸 학습 로그로 바로 사용 가능.
- closeout 완료 후 다음 트랙: **B-priority 10항 pilot 선별** (Section 7).

---

## 2. 산출물 목록

trap-map A-priority 학습 패키지 9개 문서 (전부 `docs/audit/`):

| # | 산출물 | 파일 | commit |
|---|---|---|---|
| 1 | study-set v2.1 final | `trap_map_A_priority_study_set_v2_1_final_2026-05-22.md` | 9cff87f |
| 2 | day plan (26항) | `trap_map_A_priority_26_item_day_plan_2026-05-22.md` | 8fd33d7 |
| 3 | inline trap cues v2 | `trap_map_A_priority_day_plan_v2_inline_trap_cues_2026-05-22.md` | 1c8fd21 |
| 4 | inline trap cues review | `trap_map_A_priority_day_plan_v2_inline_trap_cues_review_2026-05-22.md` | 669479b |
| 5 | inline trap cues v2.1 | `trap_map_A_priority_day_plan_v2_1_inline_trap_cues_2026-05-22.md` | adf1824 |
| 6 | Day 1 pilot log | `trap_map_A_priority_day1_pilot_learning_log_2026-05-22.md` | 72837c1 |
| 7 | Day 1 pilot review | `trap_map_A_priority_day1_pilot_learning_log_review_2026-05-22.md` | 0c3affd |
| 8 | Day 2~4 pilot logs | `trap_map_A_priority_day2_4_pilot_learning_logs_2026-05-22.md` | 32f518f |
| 9 | package 통합 리뷰 | `trap_map_A_priority_pilot_learning_package_review_2026-05-22.md` | d6c3a73 |

build 단계 산출물(study-set v1·v2, dryrun, representative questions review,
sub-question verification, v3.2 입력 문서)은 commit `9cff87f`에 함께 포함됨.

---

## 3. commit chain 요약

trap-map A-priority 트랙 9개 commit (전부 `feat/phase-b-migration`, push 완료):

```
9cff87f docs: build trap-map A-priority study set
8fd33d7 docs: add trap-map A-priority day plan
1c8fd21 docs: add inline trap cues for A-priority day plan
669479b docs: review inline trap cues for A-priority day plan
adf1824 docs: refine inline trap cues for A-priority day plan
72837c1 docs: add Day 1 pilot log for A-priority trap-map
0c3affd docs: review Day 1 pilot log for A-priority trap-map
32f518f docs: add Day 2-4 pilot logs for A-priority trap-map
d6c3a73 docs: review A-priority pilot learning package
```

이 closeout 문서의 commit은 별도(`docs: close out A-priority pilot learning
package`)로, 위 chain의 종결 commit이 된다.

---

## 4. 최종 coverage

- v3.2 ★4~5 함정 A등급 **31항** 중 study-set-ready **26항**이 학습 패키지 대상.
  (제외 5항: needs-cleanup 3 — 기기-9·설비-9·설비-18 / statute-safe-defer 2 —
  설비-5·설비-6.)
- **Day 1 8항 + Day 2~4 18항 = 26항** — study-set v2.1 final과 정확히 일치.
  - Day 1 (전력공학 Fault/보호): 전력-3·5·7·8·9·21·24·26
  - Day 2 (변압기·동기기): 기기-1·2·3·5·6·8·29
  - Day 3 (유도기): 기기-10·11·12·13
  - Day 4 (직류기 + 전기설비): 기기-14·15·16·27·30·설비-1·19
- **31문제 = 26 main + 5 sub.**
- **partial+sub 3항** (main+sub 축 분리):
  - 전력-21 — main `2016_3회_38`(전압상승 축) + sub `2009_1회_22`(다축 비교) +
    sub `2012_1회_39`(지락전류 축)
  - 기기-3 — main `2012_1회_59`(동기속도 축) + sub `2011_2회_47`(권선계수 계산
    축) + sub `2015_2회_55`(분포계수 식 축)
  - 기기-13 — main `2015_1회_41`(2차 여자 축) + sub `2008_1회_41`(f2=sf 계산 축)
- **adjacent 17항** — 원래 카드 함정 + 대표 기출 함정 둘 다 반영 (3회독 체크가
  두 함정 prompt).
- **exact 6항** (전력-8·24, 기기-2·8·11·12) — 대표 기출이 직접 검증하는 함정 중심,
  과장 없음.
- 범위 외 항목(전력-25·기기-31·기기-32) 미혼입 확인 완료.

---

## 5. known residual (accepted)

closeout 시점에 남아 있는 잔여 항목 — 모두 **학습 차단 없음, closeout에서 수용**.

### R1 — deferred `2001_3회_43`
- 출처: answer-selection pedagogy expansion 트랙(별 트랙)의 deferred 항목 —
  `hold-source-external-textbook-needed`. 정답 ②는 source-verified이나 보기 [2]의
  오류 메커니즘이 repo 내부 source로 확인 불가(외부 전기기기 교재 필요).
- A-priority 학습 패키지 영향: 없음 (A-priority 26항에 미포함).
- 처리: B-priority 후속 트랙의 pilot 선별 후보로 이월 (Section 7).

### R2 — P2-1: Day 1 로그 "쓰는 법" 용어 설명 부재
- 내용: Day 1 pilot log "쓰는 법"에는 adjacent/exact/partial+sub 용어 설명이 없고,
  Day 2~4 pilot logs "쓰는 법"에는 있다 (Day 1은 P2-1 지적 전 작성).
- 처리 방침:
  - 학습 차단 없음 — 6칸 내용은 자기충족적이고, 학습자는 2일차에 Day 2~4 로그에서
    용어 설명을 보게 된다.
  - **closeout에서는 accepted residual로 수용** (NEEDS_FIX 아님).
  - 후속 "통합 학습자용 단일판"을 만들 때 "쓰는 법" 섹션을 정규화한다 — 그때
    Day 1·Day 2~4의 "쓰는 법"을 통일.

---

## 6. 금지사항 준수 요약

trap-map A-priority 트랙 전 단계(build → day plan → trap cues → pilot logs →
reviews → closeout)에서:

- app/data 수정 없음 (`questions.json`/`questions.v2.json` 무변경).
- solution/steps apply 없음.
- answer/choices/text 수정 없음.
- 유료 API 호출 없음.
- local server 실행 없음.
- 기존 commit amend/rebase/reset 없음.

전 산출물은 `docs/audit/` 문서로만 작성·commit. tracked working tree clean 유지.

---

## 7. 다음 권장 트랙 — B-priority 10항 pilot 선별

(closeout에는 다음 트랙 **제안만** 기록 — 산출물은 미작성.)

- **트랙명**: B-priority 10항 pilot 선별.
- **목적**: A-priority에서 검증된 방식(study-set → day plan → inline trap cues →
  6칸 pilot log → 리뷰)이 B등급 함정 항목으로 확장 가능한지 **작은 단위로 검증**.
- **범위 참고**: v3.2 ★4~5 함정 중 B등급은 25항(기기 9 / 설비 11 / 전력 4 / 회로 1
  — study-set v1 review §1.1 기준). 그중 10항을 pilot로 선별.
- **우선 포함 후보**:
  - deferred `2001_3회_43` (R1) — 외부 전기기기 교재 확보 시 우선 처리.
  - B등급 상위 함정 중 representative-ready 후보 — study-set v1 dryrun의
    needs-cleanup/DQ 분류를 거치지 않은 clean 항목 우선.
- **선행 작업**: B등급 항목은 A-priority dryrun 범위 밖이었으므로, 대표 기출
  representative mapping과 source-clean 검증이 pilot 선별의 1단계가 된다.
- **착수 조건**: 본 closeout 승인 후 별도 트랙으로 시작 — A-priority 패키지는
  이 closeout으로 종료된다.

---

## Status

- trap-map A-priority 26항 pilot learning package 트랙 **closeout 완료**.
- 최종 결론: package PASS, 학습자 사용 준비 완료.
- 산출물 9종 / commit chain 9개(`9cff87f`~`d6c3a73`) / coverage 26항·31문제 요약.
- known residual 2건(R1 deferred 2001_3회_43, R2 P2-1) — 모두 accepted residual,
  학습 차단 없음.
- 금지사항 전 단계 준수 (app/data·solution·API·server·amend 무변경).
- 다음 트랙: B-priority 10항 pilot 선별 — 제안만 기록, 별도 트랙으로 착수.
- 이 문서는 상태 인계용 closeout이다. 다음 작업자는 B-priority pilot 선별로 바로
  진행 가능.
