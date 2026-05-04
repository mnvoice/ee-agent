#!/usr/bin/env python3
"""measure_subject_classification.py — 단기기사 JSON subject 분류 오류 측정

목적:
  PWA에서 박지 못한 90건 中 어느 영역이 "진짜 박힘"이고 어느 영역이
  "JSON 분류 오류"인지 측정. 회복 가능 분량 결정 영역.

본질:
  문제 번호 → 과목 매핑이 정합하면, JSON의 subject 박힘과 비교하여
  분류 오류 자동 catch.

(a) 영역:
  - 문제 번호 1~100 → 과목 매핑 (위 paste 박힘)
  - JSON 본문 read 영역 (실행 시점)

(c) 영역:
  - 매핑이 사용자 데이터와 정합 박는지 — 실행 후 확인 박음
  - "전기자기학" / "전력공학" / "전기기기" / "회로이론" / "제어공학"
    문자열이 JSON에 박힌 정확한 표기 — 실행 시 확인

실행:
  cd ~/Developer/ee-agent
  python3 measure_subject_classification.py [JSON_PATH]
  python3 measure_subject_classification.py --target 90  # PWA 박지 못한 90건만
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


# 문제 번호 → 과목 매핑 (set 박음 — 시기별 박음 영역 박음)
# 출처: 데이터 측정으로 박음 (year-bucket × subject × q_no 분포)
# 본질:
#   - 4과목 (61~80): "회로이론 및 제어공학" 통합 영역 — 둘 다 정합
#   - 5과목 (81~100): 시기별 "전기설비기술기준" 또는 "제어공학" 박힘
QNO_TO_SUBJECTS = {
    range(1, 21):   {"전기자기학"},
    range(21, 41):  {"전력공학"},
    range(41, 61):  {"전기기기"},
    range(61, 81):  {"회로이론", "제어공학"},
    range(81, 101): {"전기설비기술기준", "제어공학"},
}


def expected_subjects(q_no: int) -> set | None:
    """문제 번호 → 예상 과목 set."""
    if not isinstance(q_no, int):
        return None
    for r, subjs in QNO_TO_SUBJECTS.items():
        if q_no in r:
            return subjs
    return None


def load_json(path: Path) -> list[dict]:
    """JSON 박음. list 또는 dict 박힘 둘 다 박음."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        # 단기기사 DB 형식 추정 박음 — entries 또는 questions key
        for key in ("entries", "questions", "data", "items"):
            if key in data:
                return data[key]
        return list(data.values())
    return data


def measure(entries: list[dict], target_qnos: set | None = None) -> dict:
    """분류 오류 측정.

    target_qnos: PWA 박지 못한 90건의 (year, session, q_no) tuple set.
                 None 박으면 전체 측정.
    """
    total = 0
    correct = 0
    misclassified = 0
    unknown_qno = 0
    no_subject = 0

    by_subject_pair = defaultdict(int)  # (json_subject, expected) → count
    misclass_examples = []

    for e in entries:
        q_no = e.get("q_no")
        json_subj = e.get("subject")
        year = e.get("year")
        session = e.get("session")

        # target 필터 박음
        if target_qnos is not None:
            key = (year, session, q_no)
            if key not in target_qnos:
                continue

        total += 1

        if not json_subj:
            no_subject += 1
            continue

        expected = expected_subjects(q_no)
        if expected is None:
            unknown_qno += 1
            continue

        if json_subj in expected:
            correct += 1
        else:
            misclassified += 1
            exp_label = "/".join(sorted(expected))
            by_subject_pair[(json_subj, exp_label)] += 1
            if len(misclass_examples) < 10:
                misclass_examples.append({
                    "year": year,
                    "session": session,
                    "q_no": q_no,
                    "json_subject": json_subj,
                    "expected": exp_label,
                    "text_preview": str(e.get("text", e.get("question", "")))[:80],
                })

    return {
        "total": total,
        "correct": correct,
        "misclassified": misclassified,
        "unknown_qno": unknown_qno,
        "no_subject": no_subject,
        "by_subject_pair": dict(by_subject_pair),
        "misclass_examples": misclass_examples,
    }


def report(result: dict, target_label: str = "전체") -> None:
    """측정 결과 박음."""
    print("=" * 70)
    print(f"  Subject 분류 측정 — {target_label}")
    print("=" * 70)
    print()

    total = result["total"]
    correct = result["correct"]
    mis = result["misclassified"]
    unk = result["unknown_qno"]
    nos = result["no_subject"]

    if total == 0:
        print("⚠️  측정 대상 0건 — JSON path 또는 target_qnos 확인 박음")
        return

    print(f"총 {total}건")
    print(f"  ✓ 정합        : {correct} ({100*correct/total:.1f}%)")
    print(f"  ✗ 분류 오류   : {mis} ({100*mis/total:.1f}%)")
    print(f"  ? q_no 비표준 : {unk} ({100*unk/total:.1f}%)")
    print(f"  - subject 부재: {nos} ({100*nos/total:.1f}%)")
    print()

    if mis > 0:
        print("분류 오류 패턴 (json_subject → expected):")
        sorted_pairs = sorted(
            result["by_subject_pair"].items(),
            key=lambda x: -x[1],
        )
        for (json_s, exp), cnt in sorted_pairs:
            print(f"  {cnt:>4}건  {json_s} → {exp}")
        print()

        print("샘플 (최대 10건):")
        for ex in result["misclass_examples"]:
            print(f"  [{ex['year']} {ex['session']} {ex['q_no']:>3}번] "
                  f"{ex['json_subject']} → {ex['expected']}")
            if ex['text_preview']:
                print(f"      text: {ex['text_preview']}")
        print()

    # 본 측정의 의미 박음
    print("─" * 70)
    print("의미:")
    if mis == 0:
        print("  분류 오류 0건 — PWA 박지 못한 영역은 모두 진짜 박힘 박음")
        print("  → 회복 가능 분량 = 0건 박음 박음, 다른 원인 측정 박음")
    elif mis == total:
        print("  100% 분류 오류 박음 — 매핑 자체 의심 박음")
        print("  → QNO_TO_SUBJECT 매핑이 사용자 데이터와 정합 박지 못함 가능")
    else:
        print(f"  {mis}건이 진짜 회복 가능 (JSON 정정 박음)")
        print(f"  {correct}건은 다른 원인 — PWA logic 박음 또는 figure 부재")
        print(f"  G2 (PWA 박음 측정) 진입 시 {correct}건만 대상 박음")


def parse_target_file(path: Path) -> set:
    """PWA 박지 못한 90건 list 박음 (사용자 박힌 경우).

    형식 추정 — 실제 사용자 형식과 다를 수 있음:
      JSON: [{year, session, q_no}, ...]
      또는 TSV: year\tsession\tq_no
    """
    if not path.exists():
        return set()

    text = path.read_text(encoding="utf-8")

    # JSON 박음
    try:
        data = json.loads(text)
        return {(e["year"], e["session"], e["q_no"]) for e in data}
    except json.JSONDecodeError:
        pass

    # TSV/CSV 박음
    qnos = set()
    for line in text.splitlines():
        parts = line.strip().split("\t") if "\t" in line else line.strip().split(",")
        if len(parts) >= 3:
            try:
                qnos.add((int(parts[0]), parts[1], int(parts[2])))
            except (ValueError, IndexError):
                continue
    return qnos


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "json_path",
        nargs="?",
        default="data/questions.json",
        help="단기기사 JSON path (기본: data/questions.json)",
    )
    p.add_argument(
        "--target",
        type=Path,
        default=None,
        help="PWA 박지 못한 90건 list path — 박지 못하면 전체 측정",
    )
    p.add_argument(
        "--show-mapping",
        action="store_true",
        help="문제 번호 → 과목 매핑 박음 후 종료",
    )
    args = p.parse_args()

    if args.show_mapping:
        print("문제 번호 → 과목 매핑 (본 스크립트 가정, set 박음):")
        for r, subjs in QNO_TO_SUBJECTS.items():
            print(f"  {r.start:>3}~{r.stop-1:>3}번  {', '.join(sorted(subjs))}")
        sys.exit(0)

    json_path = Path(args.json_path)
    if not json_path.exists():
        print(f"⚠️  JSON path 박지 못함: {json_path}", file=sys.stderr)
        sys.exit(1)

    entries = load_json(json_path)
    print(f"JSON 박음: {json_path} ({len(entries)} entries)")
    print()

    # 1. 전체 측정
    print("[1] 전체 측정")
    result_all = measure(entries)
    report(result_all, target_label="전체")
    print()

    # 2. PWA 박지 못한 90건만 측정 (target 박힌 경우)
    if args.target:
        target_qnos = parse_target_file(args.target)
        if target_qnos:
            print(f"[2] PWA 박지 못한 {len(target_qnos)}건만 측정")
            result_target = measure(entries, target_qnos=target_qnos)
            report(result_target, target_label=f"PWA 박지 못한 {len(target_qnos)}건")
        else:
            print(f"⚠️  --target {args.target} 박지 못함")


if __name__ == "__main__":
    main()
