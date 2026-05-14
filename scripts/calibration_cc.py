"""
calibration_cc.py — ee-agent 84 문제 calibration 측정 + HTML 시각화

Robustness: claude npm auto-update 중간 FileNotFoundError 대비 retry + 절대 경로.
"""
import json
import os
import re
import subprocess
import time
from collections import Counter
from pathlib import Path

QUESTIONS = "data/questions_기출_2020_1회.json"
SUBSET = "output/results_2020_before_rag.json"
OUTPUT_JSON = "output/calibration_cc.json"
OUTPUT_HTML = "output/calibration_cc.html"
N = 5

CLAUDE_BIN = os.path.expanduser("~/.npm-global/bin/claude")


def extract_choice(text):
    m = re.search(r"\b([1-4])\b", text)
    return int(m.group(1)) if m else 0


def run_trial(prompt, max_retry=3):
    for attempt in range(max_retry):
        try:
            r = subprocess.run(
                [CLAUDE_BIN, "-p", prompt],
                capture_output=True, text=True, timeout=120
            )
            return r.stdout if r.returncode == 0 else ""
        except (FileNotFoundError, OSError) as e:
            print(f"  ⚠️ retry {attempt+1}/{max_retry}: {type(e).__name__}", flush=True)
            time.sleep(2)
        except subprocess.TimeoutExpired:
            print(f"  ⚠️ timeout", flush=True)
            return ""
        except Exception as e:
            print(f"  ⚠️ unknown: {type(e).__name__}: {e}", flush=True)
            time.sleep(2)
    return ""


def build_prompt(q):
    return f"""다음 4지선다 문제의 정답 번호만 출력. 다른 설명 금지. 출력은 1, 2, 3, 4 중 하나의 숫자만.

문제: {q["text"]}

보기:
1. {q["choices"][0]}
2. {q["choices"][1]}
3. {q["choices"][2]}
4. {q["choices"][3]}

정답:"""


def extract_q_nos(subset):
    items = subset if isinstance(subset, list) else subset.get("results", subset.get("items", []))
    q_nos = set()
    for it in items:
        for k in ("q_no", "question_number", "qn", "question_no", "no"):
            if k in it:
                q_nos.add(it[k])
                break
    return q_nos


def measure():
    with open(SUBSET) as f:
        subset = json.load(f)
    q_nos = extract_q_nos(subset)
    print(f"Extracted {len(q_nos)} q_nos from SUBSET", flush=True)

    with open(QUESTIONS) as f:
        all_q = json.load(f)
    target = [q for q in all_q if q["q_no"] in q_nos]
    print(f"Target: {len(target)} questions", flush=True)

    start = time.time()
    results = []
    Path(OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)

    for i, q in enumerate(target):
        prompt = build_prompt(q)
        answers = []
        for _ in range(N):
            answers.append(extract_choice(run_trial(prompt)))
        c = Counter(answers)
        top, top_n = c.most_common(1)[0]
        cons = top_n / N
        correct = top == q["answer"]
        results.append({
            "q_no": q["q_no"],
            "subject": q["subject"],
            "text": q["text"],
            "choices": q["choices"],
            "gt": q["answer"],
            "model": top,
            "answers": answers,
            "consistency": cons,
            "correct": correct,
        })
        elapsed = time.time() - start
        eta = elapsed / (i + 1) * (len(target) - i - 1)
        mark = "✓" if correct else "✗"
        print(
            f"[{i+1}/{len(target)}] q{q['q_no']:3d} {q['subject'][:10]:10s}: "
            f"GT={q['answer']} model={top} cons={cons:.2f} {mark}  ETA {eta/60:.1f}min",
            flush=True,
        )

        # crash recovery: 매 question 후 intermediate JSON 저장
        if (i + 1) % 5 == 0 or i == len(target) - 1:
            with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
                json.dump({"n": len(results), "results": results, "partial": (i + 1 < len(target))},
                          f, ensure_ascii=False)

    # 통계
    bins = {0.2: [], 0.4: [], 0.6: [], 0.8: [], 1.0: []}
    for r in results:
        if r["consistency"] in bins:
            bins[r["consistency"]].append(r["correct"])
    bin_stats = {b: {"n": len(v), "acc": (sum(v) / len(v) if v else 0)} for b, v in bins.items()}

    subj_stats = {}
    for r in results:
        s = r["subject"]
        subj_stats.setdefault(s, {"n": 0, "correct": 0, "cons_sum": 0.0})
        subj_stats[s]["n"] += 1
        subj_stats[s]["correct"] += int(r["correct"])
        subj_stats[s]["cons_sum"] += r["consistency"]
    for s in subj_stats:
        n = subj_stats[s]["n"]
        subj_stats[s]["acc"] = subj_stats[s]["correct"] / n
        subj_stats[s]["avg_cons"] = subj_stats[s]["cons_sum"] / n

    return {
        "n": len(results),
        "overall_acc": sum(r["correct"] for r in results) / len(results),
        "elapsed_sec": time.time() - start,
        "results": results,
        "bin_stats": bin_stats,
        "subj_stats": subj_stats,
    }


def build_html(data):
    results = data["results"]
    bin_stats = data["bin_stats"]
    subj_stats = data["subj_stats"]
    overall = data["overall_acc"]

    pts = []
    for b in sorted(bin_stats):
        s = bin_stats[b]
        if s["n"] > 0:
            x = b * 400 + 50
            y = 400 - s["acc"] * 350
            pts.append((b, s["acc"], s["n"], x, y))

    circles = "\n".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{min(20, 6 + n*0.4):.0f}" fill="#378ADD" opacity="0.7"/>'
        f'<text x="{x:.0f}" y="{y-15:.0f}" text-anchor="middle" font-size="11" fill="#0C447C">{acc*100:.0f}% (n={n})</text>'
        for b, acc, n, x, y in pts
    )
    x_labels = "\n".join(
        f'<text x="{0.2*i*400+50:.0f}" y="425" text-anchor="middle" font-size="11" fill="#5F5E5A">{0.2*i:.1f}</text>'
        for i in range(0, 6)
    )
    y_labels = "\n".join(
        f'<text x="40" y="{400-0.2*i*350+4:.0f}" text-anchor="end" font-size="11" fill="#5F5E5A">{0.2*i*100:.0f}%</text>'
        for i in range(0, 6)
    )

    svg_curve = f'''
<svg viewBox="0 0 500 460" style="width: 100%; max-width: 600px;">
  <text x="250" y="455" text-anchor="middle" font-size="12" fill="#5F5E5A">Consistency (model confidence)</text>
  <text x="20" y="225" text-anchor="middle" font-size="12" fill="#5F5E5A" transform="rotate(-90, 20, 225)">Accuracy</text>
  <line x1="50" y1="400" x2="450" y2="400" stroke="#888" stroke-width="1"/>
  <line x1="50" y1="400" x2="50" y2="50" stroke="#888" stroke-width="1"/>
  <path d="M 50 400 L 450 50" stroke="#999" stroke-width="1" stroke-dasharray="4,3" fill="none"/>
  <text x="370" y="60" font-size="10" fill="#999">y = x (perfect)</text>
  {circles}
  {x_labels}
  {y_labels}
</svg>
'''

    rows = []
    for r in results:
        trials = ", ".join(str(a) for a in r["answers"])
        text_preview = r["text"][:50].replace("\n", " ").replace("<", "&lt;").replace(">", "&gt;")
        cons_color = "#27500A" if r["consistency"] >= 0.8 else "#854F0B" if r["consistency"] >= 0.6 else "#791F1F"
        correct_bg = "#EAF3DE" if r["correct"] else "#FCEBEB"
        mark = "✓" if r["correct"] else "✗"
        rows.append(f'''<tr style="background: {correct_bg};">
<td>{r["q_no"]}</td><td>{r["subject"]}</td><td>{r["gt"]}</td>
<td style="font-family: monospace; font-size: 13px;">{trials}</td>
<td>{r["model"]}</td>
<td style="color: {cons_color}; font-weight: 500;">{r["consistency"]:.2f}</td>
<td style="text-align: center;">{mark}</td>
<td style="font-size: 12px;">{text_preview}...</td></tr>''')
    table_rows = "\n".join(rows)

    subj_rows = "\n".join(
        f'<tr><td>{s}</td><td>{st["n"]}</td><td>{st["correct"]}/{st["n"]}</td><td>{st["acc"]*100:.1f}%</td><td>{st["avg_cons"]:.2f}</td></tr>'
        for s, st in sorted(subj_stats.items(), key=lambda x: -x[1]["acc"])
    )
    bin_rows = "\n".join(
        f'<tr><td>{b:.1f}</td><td>{s["n"]}</td><td>{s["acc"]*100:.1f}%</td></tr>'
        for b, s in sorted(bin_stats.items())
    )

    html = f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ee-agent calibration</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 1200px; margin: 2rem auto; padding: 1rem; color: #2C2C2A; line-height: 1.5; }}
h1 {{ font-size: 22px; font-weight: 500; margin: 0 0 0.5rem; }}
h2 {{ font-size: 18px; font-weight: 500; margin: 2rem 0 1rem; }}
.summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin: 1rem 0 2rem; }}
.card {{ background: #F1EFE8; padding: 1rem; border-radius: 8px; }}
.card-label {{ font-size: 13px; color: #5F5E5A; margin: 0; }}
.card-value {{ font-size: 24px; font-weight: 500; margin: 4px 0 0; }}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
th {{ background: #F1EFE8; padding: 8px; text-align: left; font-weight: 500; border-bottom: 1px solid #D3D1C7; }}
td {{ padding: 6px 8px; border-bottom: 0.5px solid rgba(0,0,0,0.1); }}
.controls button {{ padding: 6px 12px; margin-right: 8px; background: transparent; border: 0.5px solid #888780; border-radius: 6px; cursor: pointer; font-size: 13px; }}
.controls button:hover {{ background: #F1EFE8; }}
.curve-box {{ background: white; padding: 1rem; border: 0.5px solid #D3D1C7; border-radius: 8px; margin: 1rem 0; }}
.note {{ font-size: 13px; color: #5F5E5A; margin: 0.5rem 0 1rem; }}
</style></head><body>

<h1>ee-agent calibration — {data["n"]} 문제 × {N} trial</h1>
<p class="note">생성: {time.strftime("%Y-%m-%d %H:%M")} / 측정 시간 {data["elapsed_sec"]/60:.1f}분 / claude CLI via npm-global</p>

<div class="summary">
  <div class="card"><p class="card-label">총 문제</p><p class="card-value">{data["n"]}</p></div>
  <div class="card"><p class="card-label">정답률</p><p class="card-value">{overall*100:.1f}%</p></div>
  <div class="card"><p class="card-label">평균 consistency</p><p class="card-value">{sum(r["consistency"] for r in results)/len(results):.2f}</p></div>
  <div class="card"><p class="card-label">High-cons 비율</p><p class="card-value">{sum(1 for r in results if r["consistency"] >= 0.8)/len(results)*100:.0f}%</p></div>
</div>

<h2>Calibration Curve</h2>
<div class="curve-box">{svg_curve}</div>
<p class="note">45도 선 아래 = overconfident (모델 우김, acc &lt; cons), 선 위 = underconfident (자신 부족, acc &gt; cons), 선 위치 = well-calibrated.</p>

<h2>Confidence bin × 정답률</h2>
<table><tr><th>consistency</th><th>n</th><th>정답률</th></tr>{bin_rows}</table>

<h2>과목별 성능</h2>
<table><tr><th>과목</th><th>n</th><th>정답/n</th><th>정답률</th><th>평균 consistency</th></tr>{subj_rows}</table>

<h2>문제별 결과</h2>
<div class="controls">
  <button onclick="sortBy('q_no')">번호순</button>
  <button onclick="sortBy('cons')">consistency 낮은 순</button>
  <button onclick="filterIncorrect()">오답만</button>
  <button onclick="filterAll()">전체</button>
</div>
<table id="result-table"><thead>
<tr><th>q_no</th><th>과목</th><th>GT</th><th>5 trial</th><th>top</th><th>cons</th><th>정/오</th><th>문제 (앞 50자)</th></tr>
</thead><tbody id="result-body">{table_rows}</tbody></table>

<script>
const allRows = Array.from(document.querySelectorAll('#result-body tr'));
function sortBy(key) {{
  const sorted = [...allRows].sort((a, b) => {{
    if (key === 'q_no') return parseInt(a.cells[0].textContent) - parseInt(b.cells[0].textContent);
    if (key === 'cons') return parseFloat(a.cells[5].textContent) - parseFloat(b.cells[5].textContent);
    return 0;
  }});
  const tbody = document.getElementById('result-body');
  tbody.innerHTML = '';
  sorted.forEach(r => tbody.appendChild(r));
}}
function filterIncorrect() {{
  const tbody = document.getElementById('result-body');
  tbody.innerHTML = '';
  allRows.filter(r => r.cells[6].textContent.includes('✗')).forEach(r => tbody.appendChild(r));
}}
function filterAll() {{
  const tbody = document.getElementById('result-body');
  tbody.innerHTML = '';
  allRows.forEach(r => tbody.appendChild(r));
}}
</script>
</body></html>'''
    return html


def main():
    data = measure()
    Path(OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(build_html(data))
    print(f"\n=== Output ===", flush=True)
    print(f"JSON: {OUTPUT_JSON}", flush=True)
    print(f"HTML: {OUTPUT_HTML}", flush=True)
    print(f"Total: {data['n']}건, 정답률 {data['overall_acc']*100:.1f}%, {data['elapsed_sec']/60:.1f}분", flush=True)


if __name__ == "__main__":
    main()
