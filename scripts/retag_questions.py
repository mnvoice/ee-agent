#!/usr/bin/env python3
"""
태깅 누락된 기출문제 재처리 스크립트.

이미 저장된 JSON 파일 중 concept 태깅이 50% 미만인 회차를 찾아
Claude Haiku로 재태깅하고 Obsidian 파일을 업데이트합니다.

Usage:
    python scripts/retag_questions.py [--threshold 0.5] [--dry-run]
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONCEPT_MAP_FILE = DATA_DIR / "full_concept_mapping.json"
VAULT_BASE = Path("/Users/jeong-ujin_1/Documents/Obsidian Vault")

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


# ── Haiku 태깅 (batch_gichul_pipeline.py 에서 복사) ──────────────────────────
def build_haiku_client(api_key: str):
    import anthropic
    return anthropic.Anthropic(api_key=api_key)


def tag_questions_with_haiku(
    questions: list[dict],
    concept_map: dict,
    api_key: str,
    batch_size: int = 7,
) -> list[dict]:
    """concept/difficulty/q_type 누락 문제만 Haiku로 태깅."""
    client = build_haiku_client(api_key)
    result = list(questions)

    # 태깅이 필요한 문제만 추출
    needs_tag = [q for q in result if not q.get("concept")]
    if not needs_tag:
        log.info("  모든 문제 태깅 완료 — 건너뜀")
        return result

    log.info(f"  Haiku 태깅: {len(needs_tag)}문제 (배치 {batch_size}개씩)")

    for batch_start in range(0, len(needs_tag), batch_size):
        batch = needs_tag[batch_start: batch_start + batch_size]
        batch_prompts: list[str] = []

        for q in batch:
            subj = q.get("subject", "")
            concepts = concept_map.get(subj, [])
            concept_names = [c["name"] if isinstance(c, dict) else c for c in concepts]
            concept_list_str = ", ".join(concept_names[:60])
            choices_text = "\n".join(
                f"  ({i+1}) {c}" for i, c in enumerate(q.get("choices", []))
            )
            sol_text = (q.get("solution") or q.get("solution_ocr") or "없음")[:300]

            batch_prompts.append(
                f"Q{q['q_no']} [{subj}]\n"
                f"문제: {q['text']}\n"
                f"보기:\n{choices_text}\n"
                f"정답: {q.get('answer', 0)}번\n"
                f"풀이: {sol_text}\n"
                f"사용 가능한 개념 목록: {concept_list_str}"
            )

        prompt = (
            "아래 전기기사 기출 문제들을 분석하여 JSON으로 반환하세요.\n"
            "각 문제에 대해 다음 필드를 채워주세요:\n"
            "- concept: 사용 가능한 개념 목록에서 핵심 개념 최대 2개 선택 (배열)\n"
            "- difficulty: 1-5 (1=쉬움, 5=어려움)\n"
            "- q_type: '계산형' or '암기형' or '개념형'\n\n"
            "반환 형식 (Q번호 기준 객체):\n"
            '{"1": {"concept": ["개념A"], "difficulty": 3, "q_type": "계산형"}, ...}\n\n'
            "---\n\n"
            + "\n\n---\n\n".join(batch_prompts)
        )

        for attempt in range(3):
            try:
                import anthropic
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=2048,
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.content[0].text.strip()

                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if not json_match:
                    raise ValueError("JSON 없음")

                assignments = json.loads(json_match.group())

                for q in batch:
                    key = str(q["q_no"])
                    if key in assignments:
                        data = assignments[key]
                        q["concept"] = data.get("concept", [])[:2]
                        if data.get("difficulty"):
                            q["difficulty"] = data["difficulty"]
                        if data.get("q_type"):
                            q["q_type"] = data["q_type"]

                log.info(f"  태깅 완료: Q{batch[0]['q_no']}~Q{batch[-1]['q_no']}")
                break

            except Exception as e:
                if attempt < 2:
                    log.warning(f"  오류 (시도 {attempt+1}): {e}; 재시도...")
                    time.sleep(2)
                else:
                    log.error(f"  [실패] Q{batch[0]['q_no']}~Q{batch[-1]['q_no']}: {e}")

        time.sleep(8)  # rate limit 대응

    return result


# ── Obsidian 인덱스 파일 업데이트 ─────────────────────────────────────────────
def update_obsidian_index(questions: list[dict], year: int, session: str) -> None:
    """Obsidian 인덱스 파일의 태깅 통계만 업데이트."""
    session_tag = f"{year}_{session}"
    index_path = VAULT_BASE / "기출문제" / f"{session_tag}.md"

    if not index_path.exists():
        log.warning(f"  Obsidian 인덱스 없음: {index_path}")
        return

    n_total = len(questions)
    n_solutions = sum(1 for q in questions if q.get("solution"))
    n_tagged = sum(1 for q in questions if q.get("concept"))

    content = index_path.read_text(encoding="utf-8")
    # 통계 줄 업데이트
    new_stat = f"총 {n_total}문제 | 풀이: {n_solutions}/{n_total} | 개념태깅: {n_tagged}/{n_total}"
    content = re.sub(r"총 \d+문제 \| 풀이: \d+/\d+ \| 개념태깅: \d+/\d+", new_stat, content)
    index_path.write_text(content, encoding="utf-8")
    log.info(f"  Obsidian 업데이트: {index_path.name} ({n_tagged}/{n_total} 태깅)")


# ── 메인 ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="기출문제 재태깅 스크립트")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="concept 태깅률 이 값 미만이면 재태깅 (기본: 0.5)")
    parser.add_argument("--dry-run", action="store_true",
                        help="실제 처리 없이 대상 목록만 출력")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key and not args.dry_run:
        log.error("ANTHROPIC_API_KEY 환경변수가 없습니다.")
        sys.exit(1)

    # 개념 맵 로드
    with open(CONCEPT_MAP_FILE, encoding="utf-8") as f:
        concept_map = json.load(f)

    # 재태깅 대상 파일 수집
    json_files = sorted(DATA_DIR.glob("questions_기출_*.json"))
    targets = []

    for fp in json_files:
        with open(fp, encoding="utf-8") as f:
            questions = json.load(f)
        n = len(questions)
        c = sum(1 for q in questions if q.get("concept"))
        if n > 0 and c / n < args.threshold:
            name = fp.stem.replace("questions_기출_", "")
            targets.append((fp, questions, name, c, n))

    log.info(f"\n재태깅 대상: {len(targets)}개 회차 (threshold={args.threshold})\n")
    for _, _, name, c, n in targets:
        log.info(f"  {name}: {c}/{n} ({c/n*100:.0f}%)")

    if args.dry_run:
        log.info("\n[dry-run] 실제 처리 없이 종료")
        return

    log.info("")
    for i, (fp, questions, name, c, n) in enumerate(targets, 1):
        log.info(f"[{i}/{len(targets)}] {name} 재태깅 시작...")

        updated = tag_questions_with_haiku(questions, concept_map, api_key)

        # JSON 저장
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(updated, f, ensure_ascii=False, indent=2)

        new_tagged = sum(1 for q in updated if q.get("concept"))
        log.info(f"  저장 완료: {name} ({new_tagged}/{n} 태깅)")

        # Obsidian 업데이트
        year_str, session = name.split("_", 1)
        update_obsidian_index(updated, int(year_str), session)

        log.info("")

    log.info(f"완료: {len(targets)}개 회차 재태깅")


if __name__ == "__main__":
    main()
