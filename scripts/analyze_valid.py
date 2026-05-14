"""유효 데이터 분석 + V2 FAIL 사례 발굴."""
import json
from pathlib import Path

INPUT = "output/calibration_cc.json"
OUTPUT_JSON = "output/calibration_valid.json"
OUTPUT_HTML = "output/calibration_valid.html"

def find_cutoff(results):
    """5 trial 모두 0이면 rate limit 오염 — 시작 index 반환."""
    for i, r in enumerate(results):
        if all(a == 0 for a in r["answers"]):
            return i
    return len(results)

def analyze(results, cutoff):
    valid = results[:cutoff]
    if not valid:
        return {"error": "no valid data"}

    quadrants = {"high_correct": [], "high_incorrect": [],
                 "low_correct": [], "low_incorrect": []}
    for r in valid:
        if r["consistency"] >= 0.8:
            key = "high_correct" if r["correct"] else "high_incorrect"
        elif r["consistency"] < 0.6:
            key = "low_correct" if r["correct"] else "low_incorrect"
        else:
            continue
        quadrants[key].append(r)

    correct_items = [r for r in valid if r["correct"]]
    incorrect_items = [r for r in valid if not r["correct"]]
    correct_avg = sum(r["consistency"] for r in correct_items) / max(1, len(correct_items))
    incorrect_avg = sum(r["consistency"] for r in incorrect_items) / max(1, len(incorrect_items))

    return {
        "cutoff": cutoff,
        "n_valid": len(valid),
        "accuracy": sum(r["correct"] for r in valid) / len(valid),
        "quadrants": {k: len(v) for k, v in quadrants.items()},
        "v2_fail_cases": [
            {"q_no": r["q_no"], "subject": r["subject"],
             "gt": r["gt"], "model": r["model"],
             "consistency": r["consistency"],
             "text": r["text"][:80]}
            for r in quadrants["high_incorrect"]
        ],
        "low_incorrect_cases": [
            {"q_no": r["q_no"], "gt": r["gt"], "model": r["model"],
             "answers": r["answers"]}
            for r in quadrants["low_incorrect"][:5]
        ],
        "separation": correct_avg - incorrect_avg,
        "correct_avg_cons": correct_avg,
        "incorrect_avg_cons": incorrect_avg,
    }

def main():
    with open(INPUT) as f:
        data = json.load(f)
    results = data["results"]
    cutoff = find_cutoff(results)
    analysis = analyze(results, cutoff)

    Path(OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"=== 유효 데이터 분석 ===")
    print(f"Cutoff: q{cutoff} (전체 {len(results)} 중 {cutoff}건 유효)")
    print(f"정답률: {analysis['accuracy']*100:.1f}%")
    print(f"\n4 사분면:")
    for k, n in analysis['quadrants'].items():
        print(f"  {k}: {n}건")
    print(f"\n★ V2 FAIL 사례 (high cons + incorrect = {analysis['quadrants']['high_incorrect']}건):")
    for c in analysis['v2_fail_cases']:
        print(f"  q{c['q_no']} {c['subject']}: GT={c['gt']} model={c['model']} cons={c['consistency']:.1f}")
        print(f"    → {c['text']}...")
    print(f"\n분리도: {analysis['separation']:+.2f} (correct {analysis['correct_avg_cons']:.2f} - incorrect {analysis['incorrect_avg_cons']:.2f})")

if __name__ == "__main__":
    main()
