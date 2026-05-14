"""1회 호출 새 시그널 후보 측정. 10건 sample."""
import json, os, re, subprocess, time
from pathlib import Path

CLAUDE_BIN = os.path.expanduser("~/.npm-global/bin/claude")
OUTPUT = "output/f_signal_test.json"
HEDGE = ["perhaps", "might", "i think", "i believe", "could be",
         "추측", "아마", "확실하지", "잘 모르"]

CASES = [
    {"q": "What is the capital of France? Briefly explain, then output: Answer: X | Confidence: NN%", "kind": "positive"},
    {"q": "Who painted the Mona Lisa? Briefly explain, then output: Answer: X | Confidence: NN%", "kind": "positive"},
    {"q": "What is 7 × 8? Briefly explain, then output: Answer: X | Confidence: NN%", "kind": "positive"},
    {"q": "What year was the Eiffel Tower completed? Briefly explain, then output: Answer: X | Confidence: NN%", "kind": "positive"},
    {"q": "Which planet is closest to the Sun? Briefly explain, then output: Answer: X | Confidence: NN%", "kind": "positive"},
    {"q": "What book did Zylphar the Wanderer write in 1847? Briefly explain, then output: Answer: X | Confidence: NN%", "kind": "negative"},
    {"q": "What was the population of Tofes village in February 2026? Briefly explain, then output: Answer: X | Confidence: NN%", "kind": "negative"},
    {"q": "Which actor starred in the 2031 film 'Mirror of Quintus'? Briefly explain, then output: Answer: X | Confidence: NN%", "kind": "negative"},
    {"q": "What is the GDP of Belarwena? Briefly explain, then output: Answer: X | Confidence: NN%", "kind": "negative"},
    {"q": "When was the Republic of Floreal founded? Briefly explain, then output: Answer: X | Confidence: NN%", "kind": "negative"},
]

def extract_signals(text, elapsed):
    text_l = text.lower()
    conf_match = re.search(r"confidence\s*:?\s*(\d{1,3})", text_l)
    return {
        "length_char": len(text),
        "length_words": len(text.split()),
        "elapsed_sec": round(elapsed, 1),
        "hedge_count": sum(1 for h in HEDGE if h in text_l),
        "confidence_pct": int(conf_match.group(1)) if conf_match else None,
        "response": text[:300],
    }

def main():
    results = []
    for case in CASES:
        start = time.time()
        try:
            r = subprocess.run([CLAUDE_BIN, "-p", case["q"]],
                               capture_output=True, text=True, timeout=120)
            text = r.stdout if r.returncode == 0 else ""
        except Exception as e:
            text = ""
            print(f"  ⚠️ {type(e).__name__}: {e}")
        elapsed = time.time() - start
        sig = extract_signals(text, elapsed)
        results.append({**case, **sig})
        conf_str = f"{sig['confidence_pct']}%" if sig['confidence_pct'] is not None else "N/A"
        print(f"[{case['kind']:8s}] {case['q'][:50]}...")
        print(f"    len={sig['length_char']:4d} words={sig['length_words']:3d} conf={conf_str} hedge={sig['hedge_count']} t={sig['elapsed_sec']}s")

    pos = [r for r in results if r["kind"] == "positive"]
    neg = [r for r in results if r["kind"] == "negative"]

    print("\n=== 시그널 분리도 (positive - negative) ===")
    separations = {}
    for sig in ["length_char", "length_words", "hedge_count", "elapsed_sec"]:
        pos_avg = sum(r[sig] or 0 for r in pos) / len(pos)
        neg_avg = sum(r[sig] or 0 for r in neg) / len(neg)
        sep = pos_avg - neg_avg
        separations[sig] = {"pos": pos_avg, "neg": neg_avg, "sep": sep}
        print(f"  {sig:15s}: pos {pos_avg:6.1f} / neg {neg_avg:6.1f} / sep {sep:+7.1f}")

    pos_conf = [r["confidence_pct"] for r in pos if r["confidence_pct"] is not None]
    neg_conf = [r["confidence_pct"] for r in neg if r["confidence_pct"] is not None]
    if pos_conf and neg_conf:
        pc, nc = sum(pos_conf)/len(pos_conf), sum(neg_conf)/len(neg_conf)
        separations["confidence_pct"] = {"pos": pc, "neg": nc, "sep": pc - nc}
        print(f"  confidence_pct : pos {pc:6.1f} / neg {nc:6.1f} / sep {pc - nc:+7.1f}")

    Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump({"results": results, "separations": separations}, f, ensure_ascii=False, indent=2)
    print(f"\n💾 저장: {OUTPUT}")

if __name__ == "__main__":
    main()
