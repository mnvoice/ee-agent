---
title: git index.lock race 운영 정책
date: 2026-05-20
branch: feat/phase-b-migration
type: supervisor-ops-policy
tags:
  - 전기기사/supervisor-log
  - ee-agent/운영정책
---

# Git index.lock 운영 정책

## 배경

이번 세션에서 `git add` / `git commit` 중 `.git/index.lock` 충돌이 여러 차례 발생했다.  
조사 결과 저장소 내용 충돌이나 merge conflict가 아니라, 같은 repo에서 git 작업이 겹치며 발생한 일시적 git index 잠금 race로 판단했다.

## 판정

`index.lock` 발생은 위험 신호이지만, 곧바로 저장소 손상으로 보지는 않는다.

이번 세션에서는 다음 조건을 확인했다.

- 활성 git 프로세스 없음
- `.git/index.lock` 자연 해제 확인
- 강제 삭제 없음
- 재시도 후 commit 정상 완료
- 작업 트리 clean 확인
- 데이터/코드 손상 징후 없음

따라서 이번 건은 **내용 충돌이 아니라 운영 방식 충돌**로 분류한다.

## 운영 원칙

1. Git 작업은 단일 실행자만 수행한다.
   - `git add`
   - `git commit`
   - `git status`
   - `git log`
   - `git diff --cached`

2. commit 중 병렬 git 명령을 실행하지 않는다.

3. 검증 작업과 commit 작업을 겹치지 않는다.
   - 검증 완료
   - diff 확인
   - stage
   - commit
   - status 확인  
   순서로 직렬 처리한다.

4. 웹 Claude는 git 작업을 하지 않는다.
   - 웹 Claude 역할은 독립 판정과 문서 검토로 제한한다.

5. 감독자는 git 작업을 직접 병렬 지시하지 않는다.
   - commit 권한은 Claude CLI 한 실행자에게만 준다.

## index.lock 발생 시 처리 순서

1. 즉시 강제 삭제하지 않는다.

2. 활성 git 프로세스를 확인한다.

3. 활성 git 프로세스가 있으면 종료될 때까지 기다린다.

4. 활성 git 프로세스가 없고 `.git/index.lock`이 자연 해제됐으면 같은 명령을 재시도한다.

5. 활성 git 프로세스가 없는데 lock 파일이 계속 남아 있을 때만, 별도 감독자 승인 후 삭제를 검토한다.

6. 삭제가 필요했던 경우에는 반드시 기록한다.
   - 발생 시각
   - 확인한 프로세스 상태
   - 삭제 사유
   - 이후 `git status` 결과

## 금지 사항

- 원인 확인 없이 `.git/index.lock`을 삭제하지 않는다.
- 여러 에이전트가 동시에 `git add` / `git commit`을 수행하지 않는다.
- commit 실패 후 바로 다른 변경을 stage하지 않는다.
- lock 충돌을 merge conflict로 오판하지 않는다.

## 기록 기준

`index.lock`이 반복 발생하면 supervisor log 또는 decision record에 운영 신호로 기록한다.

기록 항목:

- 발생 횟수
- 발생한 명령
- 활성 git 프로세스 확인 결과
- lock 자연 해제 여부
- 강제 삭제 여부
- 최종 commit 성공 여부
- 후속 운영 정책 변경

## 이번 세션 결론

이번 세션의 `index.lock` 반복은 저장소 내용 문제가 아니라 git 작업 직렬화 부족에서 온 운영 신호다.  
앞으로는 **git 단일 실행자 원칙**과 **commit 작업 직렬화**를 적용한다.
