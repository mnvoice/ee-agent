"""Phase 3c - confidence_pct calibration with clean failure handling.

Key rule: CLI/timeout/quota/parse failures are not scored as wrong answers.
They are tracked as statuses and excluded from accuracy/calibration metrics.

Default run: N=1 over the valid Phase 3a cutoff set.
Useful options:
  python3 scripts/conf_calibration.py --resume
  python3 scripts/conf_calibration.py --limit 10
  python3 scripts/conf_calibration.py --output output/conf_calibration_v2.json
"""
import argparse
import html
import json
import os
import re
import subprocess
import time
from collections import Counter
from pathlib import Path

QUESTIONS = "data/questions_기출_2020_1회.json"
SOURCE = "output/calibration_cc.json"
OUTPUT_JSON = "output/conf_calibration_v2.json"
OUTPUT_HTML = "output/conf_calibration_v2.html"
CLAUDE_BIN = os.path.expanduser("~/.npm-global/bin/claude")
SELF_CONS_SEPARATION_PCT = 8.0

QUOTA_PATTERNS = (
    "hit your limit",
    "usage limit",
    "rate limit",
    "quota",
    "resets",
)


def find_cutoff(results):
    """Return first index where Phase 3a answers became rate-limit pollution."""
    for i, r in enumerate(results):
        if all(a == 0 for a in r.get("answers", [])):
            return i
    return len(results)


def load_targets(source_path, questions_path, limit=None):
    with open(source_path, encoding="utf-8") as f:
        src = json.load(f)
    cutoff = find_cutoff(src["results"])
    valid_q_nos = [src["results"][i]["q_no"] for i in range(cutoff)]
    valid_set = set(valid_q_nos)

    with open(questions_path, encoding="utf-8") as f:
        all_q = json.load(f)
    targets = [q for q in all_q if q["q_no"] in valid_set]
    if limit is not None:
        targets = targets[:limit]
    return cutoff, valid_q_nos, targets


def build_prompt(q):
    return f"""다음 4지선다 문제를 신중하게 풀이하세요.

마지막 줄은 반드시 아래 형식 하나만 사용하세요.
Answer: N | Confidence: NN%

규칙:
- N은 1, 2, 3, 4 중 하나입니다.
- NN은 0부터 100까지의 정수입니다.
- 확실하지 않으면 confidence를 낮게 쓰세요.

문제: {q["text"]}

보기:
1. {q["choices"][0]}
2. {q["choices"][1]}
3. {q["choices"][2]}
4. {q["choices"][3]}
"""


def detect_quota(text):
    text_l = text.lower()
    return any(p in text_l for p in QUOTA_PATTERNS)


def run_trial(prompt, timeout=120):
    start = time.time()
    try:
        r = subprocess.run(
            [CLAUDE_BIN, "-p", prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        return {
            "run_status": "timeout",
            "returncode": None,
            "stdout": e.stdout or "",
            "stderr": e.stderr or "",
            "elapsed_sec": time.time() - start,
        }
    except FileNotFoundError as e:
        return {
            "run_status": "cli_missing",
            "returncode": None,
            "stdout": "",
            "stderr": str(e),
            "elapsed_sec": time.time() - start,
        }
    except OSError as e:
        return {
            "run_status": "os_error",
            "returncode": None,
            "stdout": "",
            "stderr": str(e),
            "elapsed_sec": time.time() - start,
        }

    stdout = r.stdout or ""
    stderr = r.stderr or ""
    combined = f"{stdout}\n{stderr}"
    if detect_quota(combined):
        run_status = "quota_failed"
    elif r.returncode != 0:
        run_status = "cli_failed"
    elif not stdout.strip():
        run_status = "empty_response"
    else:
        run_status = "completed"

    return {
        "run_status": run_status,
        "returncode": r.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "elapsed_sec": time.time() - start,
    }


def extract_answer_conf(text):
    """Extract answer/confidence without inventing a fallback answer."""
    answer = None
    confidence = None

    answer_patterns = (
        r"answer\s*[:：]\s*[\(\[]?\s*([1-4])\b",
        r"답\s*[:：]?\s*[\(\[]?\s*([1-4])\b",
        r"정답\s*[:：]?\s*[\(\[]?\s*([1-4])\b",
    )
    for pattern in answer_patterns:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            answer = int(m.group(1))
            break

    conf_patterns = (
        r"confidence\s*[:：]\s*(100|\d{1,2})\s*%?",
        r"확신\s*(?:도|정도)?\s*[:：]?\s*(100|\d{1,2})\s*%",
        r"신뢰\s*(?:도)?\s*[:：]?\s*(100|\d{1,2})\s*%",
    )
    for pattern in conf_patterns:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            confidence = int(m.group(1))
            break

    return answer, confidence


def classify_result(run, answer, confidence):
    if run["run_status"] != "completed":
        return run["run_status"]
    if answer is None and confidence is None:
        return "parse_failed"
    if answer is None:
        return "answer_parse_failed"
    if confidence is None:
        return "confidence_parse_failed"
    if confidence < 0 or confidence > 100:
        return "confidence_range_failed"
    return "ok"


def compact_error(stderr, stdout):
    text = (stderr or stdout or "").strip().replace("\n", " ")
    return text[:300]


def make_result(q, run):
    answer, confidence = extract_answer_conf(run["stdout"])
    status = classify_result(run, answer, confidence)
    correct = (answer == q["answer"]) if status == "ok" else None
    return {
        "q_no": q["q_no"],
        "subject": q["subject"],
        "gt": q["answer"],
        "model": answer,
        "confidence_pct": confidence,
        "correct": correct,
        "status": status,
        "run_status": run["run_status"],
        "returncode": run["returncode"],
        "elapsed_sec": round(run["elapsed_sec"], 2),
        "response": run["stdout"][:1000],
        "error": compact_error(run["stderr"], run["stdout"]),
    }


def load_resume_results(output_path):
    path = Path(output_path)
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("results", [])


def result_is_reusable(result):
    return result.get("status") == "ok"


def save_report(output_json, output_html, payload):
    out = Path(output_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rows = []
    for r in payload["results"]:
        mark = "" if r.get("correct") is None else ("Y" if r["correct"] else "N")
        rows.append(
            "<tr>"
            f"<td>{r['q_no']}</td>"
            f"<td>{html.escape(r.get('subject', ''))}</td>"
            f"<td>{r.get('gt')}</td>"
            f"<td>{r.get('model')}</td>"
            f"<td>{r.get('confidence_pct')}</td>"
            f"<td>{mark}</td>"
            f"<td>{html.escape(r.get('status', ''))}</td>"
            f"<td>{html.escape(r.get('error', ''))}</td>"
            "</tr>"
        )

    s = payload["summary"]
    page = f"""<!doctype html>
<meta charset=\"utf-8\">
<title>Phase 3c Confidence Calibration</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 24px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
th, td {{ border: 1px solid #ddd; padding: 6px 8px; vertical-align: top; }}
th {{ background: #f6f6f6; text-align: left; }}
code {{ background: #f6f6f6; padding: 2px 4px; }}
</style>
<h1>Phase 3c Confidence Calibration</h1>
<p>Total: {s['total']} / OK: {s['ok']} / Failed: {s['failed']} / Partial: {payload['partial']}</p>
<p>Accuracy(ok only): {s['accuracy_ok']:.1%} / Confidence extraction(completed basis): {s['confidence_extract_rate_completed_basis']:.1%}</p>
<p>Separation: {s['separation_pct']:+.1f}%</p>
<table>
<thead><tr><th>q</th><th>subject</th><th>gt</th><th>model</th><th>conf</th><th>correct</th><th>status</th><th>error</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
"""
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(page)


def mean(items):
    return sum(items) / len(items) if items else 0.0


def analyze(results, target_count, elapsed_sec):
    status_counts = Counter(r["status"] for r in results)
    completed = [r for r in results if r.get("run_status") == "completed"]
    answer_extracted = [r for r in completed if r.get("model") is not None]
    confidence_extracted = [r for r in completed if r.get("confidence_pct") is not None]
    ok = [r for r in results if r["status"] == "ok"]
    correct = [r for r in ok if r["correct"]]
    incorrect = [r for r in ok if r["correct"] is False]

    correct_avg = mean([r["confidence_pct"] for r in correct])
    incorrect_avg = mean([r["confidence_pct"] for r in incorrect])
    separation = correct_avg - incorrect_avg if correct and incorrect else 0.0

    bins = {str(b): {"n": 0, "correct": 0, "acc": 0.0} for b in range(0, 101, 10)}
    for r in ok:
        b = min(100, (r["confidence_pct"] // 10) * 10)
        key = str(b)
        bins[key]["n"] += 1
        bins[key]["correct"] += 1 if r["correct"] else 0
    for b in bins.values():
        b["acc"] = b["correct"] / b["n"] if b["n"] else 0.0

    total = len(results)
    failed = total - len(ok)
    return {
        "target_count": target_count,
        "total": total,
        "ok": len(ok),
        "failed": failed,
        "status_counts": dict(status_counts),
        "accuracy_ok": (sum(r["correct"] for r in ok) / len(ok)) if ok else 0.0,
        "accuracy_total_attempted_including_failures": None,
        "completed_count": len(completed),
        "answer_extract_rate_completed_basis": len(answer_extracted) / len(completed) if completed else 0.0,
        "confidence_extract_rate_completed_basis": len(confidence_extracted) / len(completed) if completed else 0.0,
        "ok_rate_attempted": len(ok) / total if total else 0.0,
        "correct_count": len(correct),
        "incorrect_count": len(incorrect),
        "correct_avg_conf": correct_avg,
        "incorrect_avg_conf": incorrect_avg,
        "separation_pct": separation,
        "self_cons_separation_pct": SELF_CONS_SEPARATION_PCT,
        "self_cons_ratio": (separation / SELF_CONS_SEPARATION_PCT) if separation > 0 else None,
        "bin_stats": bins,
        "elapsed_sec": elapsed_sec,
    }


def print_progress(i, n, q, result, reused=False):
    status = result["status"]
    model = result.get("model")
    conf = result.get("confidence_pct")
    conf_s = f"{conf}%" if conf is not None else "N/A"
    if result.get("correct") is None:
        mark = "-"
    else:
        mark = "OK" if result["correct"] else "WRONG"
    reuse = " reuse" if reused else ""
    print(
        f"[{i}/{n}] q{q['q_no']:3d} {q['subject'][:10]:10s}: "
        f"status={status}{reuse} GT={q['answer']} model={model} conf={conf_s} {mark}",
        flush=True,
    )


def print_summary(summary):
    print("\n=== Phase 3c confidence calibration v2 ===", flush=True)
    print(
        f"target={summary['target_count']}, attempted={summary['total']}, "
        f"ok={summary['ok']}, failed={summary['failed']}",
        flush=True,
    )
    print(f"status_counts: {summary['status_counts']}", flush=True)
    print(f"accuracy(ok only): {summary['accuracy_ok']*100:.1f}%", flush=True)
    print(
        f"extract(completed basis): answer "
        f"{summary['answer_extract_rate_completed_basis']*100:.1f}% / confidence "
        f"{summary['confidence_extract_rate_completed_basis']*100:.1f}%",
        flush=True,
    )
    print(
        f"confidence: correct({summary['correct_count']}건) "
        f"{summary['correct_avg_conf']:.1f}% / incorrect({summary['incorrect_count']}건) "
        f"{summary['incorrect_avg_conf']:.1f}%",
        flush=True,
    )
    print(f"separation: {summary['separation_pct']:+.1f}%", flush=True)
    if summary["self_cons_ratio"] is not None:
        print(f"self-cons 8% 대비: {summary['self_cons_ratio']:.1f}배", flush=True)
    print("\nbin x accuracy:", flush=True)
    for key, stat in summary["bin_stats"].items():
        if stat["n"]:
            b = int(key)
            print(f"  conf={b:3d}~{b+9:3d}%: n={stat['n']:3d} acc={stat['acc']*100:.1f}%", flush=True)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--questions", default=QUESTIONS)
    p.add_argument("--source", default=SOURCE)
    p.add_argument("--output", default=OUTPUT_JSON)
    p.add_argument("--html", default=OUTPUT_HTML)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--no-stop-on-quota", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    start = time.time()
    cutoff, valid_q_nos, targets = load_targets(args.source, args.questions, args.limit)
    print(f"Cutoff: {cutoff}, valid q_nos: {len(valid_q_nos)}", flush=True)
    print(f"Target: {len(targets)} questions", flush=True)

    existing_by_q = {}
    if args.resume:
        for r in load_resume_results(args.output):
            if result_is_reusable(r):
                existing_by_q[r["q_no"]] = r
        print(f"Resume: reusable ok results={len(existing_by_q)}", flush=True)

    results = []
    stop_reason = None
    for idx, q in enumerate(targets, start=1):
        if q["q_no"] in existing_by_q:
            result = existing_by_q[q["q_no"]]
            results.append(result)
            print_progress(idx, len(targets), q, result, reused=True)
            continue

        run = run_trial(build_prompt(q), timeout=args.timeout)
        result = make_result(q, run)
        results.append(result)
        print_progress(idx, len(targets), q, result)

        summary = analyze(results, len(targets), time.time() - start)
        save_report(args.output, args.html, {
            "partial": idx < len(targets),
            "stop_reason": None,
            "cutoff": cutoff,
            "valid_q_nos": valid_q_nos,
            "summary": summary,
            "results": results,
        })

        if result["status"] == "quota_failed" and not args.no_stop_on_quota:
            stop_reason = "quota_failed"
            print("\nquota_failed 감지: 실패를 오답으로 세지 않고 partial 저장 후 중단합니다.", flush=True)
            break

    summary = analyze(results, len(targets), time.time() - start)
    payload = {
        "partial": len(results) < len(targets),
        "stop_reason": stop_reason,
        "cutoff": cutoff,
        "valid_q_nos": valid_q_nos,
        "summary": summary,
        "results": results,
    }
    save_report(args.output, args.html, payload)
    print_summary(summary)
    print(f"\nSaved: {args.output}", flush=True)
    print(f"Saved: {args.html}", flush=True)


if __name__ == "__main__":
    main()
