"""Offline confidence-proxy analysis from existing Phase 3a responses.

No model calls. Reads output/calibration_cc.json, removes the rate-limit cutoff,
and evaluates whether the existing 5-trial answer distribution can be used as an
F/confidence signal.
"""
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

INPUT = "output/calibration_cc.json"
OUTPUT_JSON = "output/confidence_proxy_analysis.json"
OUTPUT_HTML = "output/confidence_proxy_analysis.html"


def find_cutoff(results):
    """First all-zero row marks rate-limit pollution."""
    for i, r in enumerate(results):
        if all(a == 0 for a in r.get("answers", [])):
            return i
    return len(results)


def answer_counts(answers):
    return Counter(a for a in answers if a in (1, 2, 3, 4))


def entropy_norm(counts):
    total = sum(counts.values())
    if total <= 0:
        return 1.0
    ent = 0.0
    for c in counts.values():
        p = c / total
        ent -= p * math.log2(p)
    return ent / math.log2(4)


def enrich_result(r):
    counts = answer_counts(r.get("answers", []))
    total = sum(counts.values())
    ranked = counts.most_common()
    top_n = ranked[0][1] if ranked else 0
    second_n = ranked[1][1] if len(ranked) > 1 else 0
    top_margin = (top_n - second_n) / total if total else 0.0
    entropy = entropy_norm(counts)
    confidence_proxy = r.get("consistency", 0.0)

    return {
        **r,
        "answer_counts": dict(sorted(counts.items())),
        "valid_trials": total,
        "confidence_proxy": confidence_proxy,
        "top_margin": top_margin,
        "entropy_norm": entropy,
        "uncertainty_proxy": 1.0 - confidence_proxy,
    }


def mean(values):
    return sum(values) / len(values) if values else 0.0


def median(values):
    if not values:
        return 0.0
    values = sorted(values)
    mid = len(values) // 2
    if len(values) % 2:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2


def metric_summary(valid, metric, higher_is_confident=True):
    correct = [r for r in valid if r["correct"]]
    incorrect = [r for r in valid if not r["correct"]]
    c_avg = mean([r[metric] for r in correct])
    i_avg = mean([r[metric] for r in incorrect])
    sep = c_avg - i_avg if higher_is_confident else i_avg - c_avg
    return {
        "correct_avg": c_avg,
        "incorrect_avg": i_avg,
        "separation_confident_direction": sep,
        "correct_median": median([r[metric] for r in correct]),
        "incorrect_median": median([r[metric] for r in incorrect]),
    }


def threshold_stats(valid, metric="confidence_proxy", thresholds=None):
    if thresholds is None:
        thresholds = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    out = []
    n = len(valid)
    for t in thresholds:
        covered = [r for r in valid if r[metric] >= t]
        rejected = [r for r in valid if r[metric] < t]
        out.append({
            "threshold": t,
            "coverage_n": len(covered),
            "coverage_pct": len(covered) / n if n else 0.0,
            "accuracy_covered": mean([1.0 if r["correct"] else 0.0 for r in covered]),
            "rejected_n": len(rejected),
            "accuracy_rejected": mean([1.0 if r["correct"] else 0.0 for r in rejected]),
            "wrong_covered_n": sum(1 for r in covered if not r["correct"]),
        })
    return out


def subject_stats(valid):
    grouped = defaultdict(list)
    for r in valid:
        grouped[r["subject"]].append(r)
    out = {}
    for subject, rows in sorted(grouped.items()):
        out[subject] = {
            "n": len(rows),
            "accuracy": mean([1.0 if r["correct"] else 0.0 for r in rows]),
            "avg_consistency": mean([r["confidence_proxy"] for r in rows]),
            "high_conf_wrong": sum(1 for r in rows if r["confidence_proxy"] >= 0.8 and not r["correct"]),
        }
    return out


def compact_case(r):
    return {
        "q_no": r["q_no"],
        "subject": r["subject"],
        "gt": r["gt"],
        "model": r["model"],
        "answers": r["answers"],
        "answer_counts": r["answer_counts"],
        "consistency": r["consistency"],
        "top_margin": r["top_margin"],
        "entropy_norm": r["entropy_norm"],
        "text": r["text"][:140],
    }


def build_interpretation(valid, metrics, high_conf_wrong, ambiguous):
    cons_sep = metrics["consistency"]["separation_confident_direction"]
    top_sep = metrics["top_margin"]["separation_confident_direction"]
    ent_sep = metrics["entropy_norm"]["separation_confident_direction"]
    high_wrong_rate = len(high_conf_wrong) / len(valid) if valid else 0.0
    ambiguous_rate = len(ambiguous) / len(valid) if valid else 0.0

    verdict = "weak_proxy"
    if cons_sep >= 0.15 and high_wrong_rate < 0.05:
        verdict = "usable_proxy"
    elif high_wrong_rate >= 0.10:
        verdict = "unsafe_as_gate"

    return {
        "verdict": verdict,
        "summary": (
            "기존 5-trial consistency는 호출 없이 쓸 수 있는 confidence proxy지만, "
            "high-confidence wrong 사례가 존재하므로 단독 자동승인 gate로는 위험합니다. "
            "새 confidence-prompt 실험은 rate limit 비용 대비 효율이 낮아 보류하는 편이 타당합니다."
        ),
        "consistency_separation": cons_sep,
        "top_margin_separation": top_sep,
        "entropy_separation": ent_sep,
        "high_conf_wrong_rate": high_wrong_rate,
        "ambiguous_rate": ambiguous_rate,
        "recommended_next": (
            "Phase 3c는 offline 재해석으로 종결하고, high_conf_wrong 사례를 오류 유형별로 분류해 "
            "V2 보정 규칙 또는 과목별 검증 루틴 후보를 찾는 쪽으로 전환합니다."
        ),
    }


def analyze(data):
    results = data["results"]
    cutoff = find_cutoff(results)
    valid = [enrich_result(r) for r in results[:cutoff]]
    polluted = results[cutoff:]

    correct = [r for r in valid if r["correct"]]
    incorrect = [r for r in valid if not r["correct"]]
    high_conf_wrong = [r for r in valid if r["confidence_proxy"] >= 0.8 and not r["correct"]]
    low_conf_correct = [r for r in valid if r["confidence_proxy"] < 0.8 and r["correct"]]
    ambiguous = [r for r in valid if r["confidence_proxy"] < 0.8]

    metrics = {
        "consistency": metric_summary(valid, "confidence_proxy", True),
        "top_margin": metric_summary(valid, "top_margin", True),
        "entropy_norm": metric_summary(valid, "entropy_norm", False),
    }

    return {
        "source": INPUT,
        "cutoff_index": cutoff,
        "n_total_source": len(results),
        "n_valid": len(valid),
        "n_polluted_after_cutoff": len(polluted),
        "accuracy": mean([1.0 if r["correct"] else 0.0 for r in valid]),
        "correct_n": len(correct),
        "incorrect_n": len(incorrect),
        "metrics": metrics,
        "thresholds": threshold_stats(valid),
        "subject_stats": subject_stats(valid),
        "high_conf_wrong_cases": [compact_case(r) for r in high_conf_wrong],
        "low_conf_correct_cases": [compact_case(r) for r in low_conf_correct],
        "ambiguous_cases": [compact_case(r) for r in ambiguous],
        "interpretation": build_interpretation(valid, metrics, high_conf_wrong, ambiguous),
    }


def write_html(analysis):
    rows = []
    for c in analysis["high_conf_wrong_cases"]:
        rows.append(
            "<tr>"
            f"<td>{c['q_no']}</td><td>{c['subject']}</td><td>{c['gt']}</td><td>{c['model']}</td>"
            f"<td>{c['consistency']:.2f}</td><td>{c['top_margin']:.2f}</td><td>{c['entropy_norm']:.2f}</td>"
            f"<td>{c['answers']}</td><td>{c['text']}</td>"
            "</tr>"
        )

    metric_rows = []
    for name, m in analysis["metrics"].items():
        metric_rows.append(
            "<tr>"
            f"<td>{name}</td><td>{m['correct_avg']:.3f}</td><td>{m['incorrect_avg']:.3f}</td>"
            f"<td>{m['separation_confident_direction']:+.3f}</td>"
            "</tr>"
        )

    th_rows = []
    for t in analysis["thresholds"]:
        th_rows.append(
            "<tr>"
            f"<td>{t['threshold']:.1f}</td><td>{t['coverage_n']}</td><td>{t['coverage_pct']:.1%}</td>"
            f"<td>{t['accuracy_covered']:.1%}</td><td>{t['wrong_covered_n']}</td>"
            f"<td>{t['rejected_n']}</td><td>{t['accuracy_rejected']:.1%}</td>"
            "</tr>"
        )

    html = f"""<!doctype html>
<meta charset=\"utf-8\">
<title>Confidence Proxy Analysis</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 24px; color: #222; }}
table {{ border-collapse: collapse; width: 100%; margin: 14px 0 28px; font-size: 13px; }}
th, td {{ border: 1px solid #ddd; padding: 6px 8px; vertical-align: top; }}
th {{ background: #f5f5f5; text-align: left; }}
.kpi {{ display: flex; gap: 12px; flex-wrap: wrap; }}
.kpi div {{ border: 1px solid #ddd; padding: 10px 12px; border-radius: 6px; }}
</style>
<h1>Offline Confidence Proxy Analysis</h1>
<p>{analysis['interpretation']['summary']}</p>
<div class=\"kpi\">
  <div>Valid N<br><b>{analysis['n_valid']}</b></div>
  <div>Accuracy<br><b>{analysis['accuracy']:.1%}</b></div>
  <div>High-conf wrong<br><b>{len(analysis['high_conf_wrong_cases'])}</b></div>
  <div>Verdict<br><b>{analysis['interpretation']['verdict']}</b></div>
</div>
<h2>Metric Separation</h2>
<table><thead><tr><th>metric</th><th>correct avg</th><th>incorrect avg</th><th>separation</th></tr></thead><tbody>{''.join(metric_rows)}</tbody></table>
<h2>Thresholds</h2>
<table><thead><tr><th>threshold</th><th>covered n</th><th>coverage</th><th>covered acc</th><th>wrong covered</th><th>rejected n</th><th>rejected acc</th></tr></thead><tbody>{''.join(th_rows)}</tbody></table>
<h2>High-Confidence Wrong Cases</h2>
<table><thead><tr><th>q</th><th>subject</th><th>gt</th><th>model</th><th>cons</th><th>margin</th><th>entropy</th><th>answers</th><th>text</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
"""
    Path(OUTPUT_HTML).write_text(html, encoding="utf-8")


def main():
    with open(INPUT, encoding="utf-8") as f:
        data = json.load(f)
    analysis = analyze(data)

    Path(OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    write_html(analysis)

    print("=== Offline Confidence Proxy Analysis ===")
    print(f"cutoff index: {analysis['cutoff_index']} / valid N: {analysis['n_valid']} / polluted: {analysis['n_polluted_after_cutoff']}")
    print(f"accuracy: {analysis['accuracy']*100:.1f}% ({analysis['correct_n']}/{analysis['n_valid']})")
    print("\nmetric separation:")
    for name, m in analysis["metrics"].items():
        print(f"  {name:12s}: correct {m['correct_avg']:.3f} / incorrect {m['incorrect_avg']:.3f} / sep {m['separation_confident_direction']:+.3f}")
    print("\nthreshold coverage:")
    for t in analysis["thresholds"]:
        print(f"  >= {t['threshold']:.1f}: cover {t['coverage_n']:2d}/{analysis['n_valid']} ({t['coverage_pct']*100:5.1f}%), acc {t['accuracy_covered']*100:5.1f}%, wrong {t['wrong_covered_n']}")
    print(f"\nhigh-confidence wrong cases: {len(analysis['high_conf_wrong_cases'])}")
    for c in analysis["high_conf_wrong_cases"]:
        print(f"  q{c['q_no']:3d} {c['subject']:8s}: GT={c['gt']} model={c['model']} cons={c['consistency']:.1f} answers={c['answers']}")
    print(f"\nverdict: {analysis['interpretation']['verdict']}")
    print(analysis["interpretation"]["recommended_next"])
    print(f"\nSaved: {OUTPUT_JSON}")
    print(f"Saved: {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
