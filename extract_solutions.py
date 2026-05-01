"""
extract_solutions.py — solver 결과의 law_used를 슬림 JSON에 병합
(a) 옵션: 새 LLM 호출 0건. 이미 있는 풀이 텍스트만 재활용.
"""

import json
from pathlib import Path

SLIM = Path("output/questions_2026_q1.json")
RESULTS = Path("output/results_2026_1_repatched.json")  # 다른 이름이면 조정
OUT = Path("output/questions_2026_q1_with_solutions.json")


def get_law_used(result_item):
    ao = result_item.get("agent_outputs") or []
    if not ao:
        return None
    first = ao[0]
    if not isinstance(first, dict):
        return None
    sol = first.get("law_used") or first.get("final_answer") or None
    if isinstance(sol, str):
        sol = sol.strip()
        return sol if sol else None
    return None


def main():
    if not SLIM.exists():
        raise SystemExit(f"ERROR: {SLIM} 없음")
    if not RESULTS.exists():
        raise SystemExit(f"ERROR: {RESULTS} 없음 — 다른 results 파일명일 수 있음")

    slim = json.loads(SLIM.read_text(encoding="utf-8"))
    results = json.loads(RESULTS.read_text(encoding="utf-8"))

    if isinstance(results, dict):
        if "questions" in results:
            results = results["questions"]
        elif "results" in results:
            results = results["results"]

    res_by_qn = {r["question_number"]: r for r in results if "question_number" in r}

    n_with = 0
    for q in slim:
        qn = q["question_number"]
        r = res_by_qn.get(qn)
        sol = get_law_used(r) if r else None
        q["ai_solution"] = sol  # 단일 문자열 또는 None — App.jsx가 q.ai_solution을 직접 읽음
        if sol:
            n_with += 1

    OUT.write_text(json.dumps(slim, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK → {OUT}  ai_solution 보유: {n_with}/{len(slim)}")


if __name__ == "__main__":
    main()
