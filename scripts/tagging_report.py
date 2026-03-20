#!/usr/bin/env python3
"""Generate tagging status HTML report for 기출문제 concept tags."""

import glob
import json
import os
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "tagging_report.html")


def load_all_questions():
    pattern = os.path.join(DATA_DIR, "questions_기출_*.json")
    files = sorted(glob.glob(pattern))
    sessions = []
    for path in files:
        with open(path, encoding="utf-8") as f:
            questions = json.load(f)
        if not questions:
            continue
        q0 = questions[0]
        year = q0.get("year", "")
        session = q0.get("session", "")
        sessions.append({"year": year, "session": session, "questions": questions, "file": os.path.basename(path)})
    return sessions


def is_tagged(q):
    c = q.get("concept")
    if c is None:
        return False
    if isinstance(c, list):
        return len(c) > 0
    if isinstance(c, str):
        return c.strip() != ""
    return False


def concept_display(q):
    c = q.get("concept")
    if not c:
        return ""
    if isinstance(c, list):
        return ", ".join(c)
    return str(c)


def tag_color(rate):
    if rate == 100:
        return "#2d7a2d"
    elif rate >= 80:
        return "#6abf6a"
    elif rate >= 60:
        return "#d4c02a"
    elif rate >= 50:
        return "#e08030"
    else:
        return "#c0392b"


def tag_text_color(rate):
    if rate >= 60:
        return "#000"
    return "#fff"


def build_heatmap(sessions):
    # Group by year
    year_sessions = defaultdict(list)
    for s in sessions:
        year_sessions[s["year"]].append(s)

    years = sorted(year_sessions.keys())
    all_session_labels = sorted(set(str(s["session"]) for s in sessions))

    rows = []
    for year in years:
        cells = []
        for sl in all_session_labels:
            match = next((s for s in year_sessions[year] if str(s["session"]) == sl), None)
            if match:
                qs = match["questions"]
                tagged = sum(1 for q in qs if is_tagged(q))
                total = len(qs)
                rate = round(tagged / total * 100) if total else 0
                bg = tag_color(rate)
                fg = tag_text_color(rate)
                sid = f"{year}_{sl}"
                cells.append(
                    f'<td style="background:{bg};color:{fg};cursor:pointer;" '
                    f'onclick="scrollTo(\'{sid}\')" title="{year} {sl}: {tagged}/{total}">'
                    f'{rate}%</td>'
                )
            else:
                cells.append('<td style="background:#eee;color:#aaa;">-</td>')
        rows.append(f'<tr><td style="font-weight:bold;padding:4px 8px;">{year}</td>{"".join(cells)}</tr>')

    header_cells = "".join(f'<th style="padding:4px 8px;">{sl}</th>' for sl in all_session_labels)
    table = (
        '<table style="border-collapse:collapse;font-size:13px;">'
        f'<tr><th></th>{header_cells}</tr>'
        + "".join(rows)
        + "</table>"
    )
    return table


def build_accordion(sessions):
    parts = []
    for s in sessions:
        year = s["year"]
        session = s["session"]
        qs = s["questions"]
        tagged = sum(1 for q in qs if is_tagged(q))
        total = len(qs)
        rate = round(tagged / total * 100) if total else 0
        bg = tag_color(rate)
        fg = tag_text_color(rate)
        sid = f"{year}_{session}"

        rows = []
        for q in qs:
            q_no = q.get("q_no", "?")
            subject = q.get("subject", "")
            text = q.get("text", "")
            text_short = text[:50].replace("<", "&lt;").replace(">", "&gt;")
            if len(text) > 50:
                text_short += "…"
            answer = q.get("answer", "")
            tagged_q = is_tagged(q)
            concepts = concept_display(q)

            if tagged_q:
                row_style = "background:#e8f5e9;"
                status = f'<span style="color:#2d7a2d;font-size:12px;">{concepts}</span>'
            else:
                row_style = "background:#fdecea;"
                status = '<span style="color:#c0392b;">❌ 미태깅</span>'

            rows.append(
                f'<tr style="{row_style}">'
                f'<td style="padding:4px 8px;color:#555;font-size:12px;">{q_no}</td>'
                f'<td style="padding:4px 8px;font-size:12px;color:#333;">{subject}</td>'
                f'<td style="padding:4px 8px;font-size:12px;">{text_short}</td>'
                f'<td style="padding:4px 8px;font-size:12px;color:#666;">정답:{answer}</td>'
                f'<td style="padding:4px 8px;font-size:12px;">{status}</td>'
                f"</tr>"
            )

        table_html = (
            '<table style="width:100%;border-collapse:collapse;margin-top:8px;">'
            '<tr style="background:#f5f5f5;font-size:12px;">'
            "<th>번호</th><th>과목</th><th>문제</th><th>정답</th><th>태깅</th></tr>"
            + "".join(rows)
            + "</table>"
        )

        parts.append(
            f'<div id="{sid}" style="margin-bottom:4px;">'
            f'<div onclick="toggle(\'{sid}_body\')" style="cursor:pointer;padding:10px 14px;'
            f"background:{bg};color:{fg};border-radius:4px;display:flex;"
            f'justify-content:space-between;align-items:center;">'
            f'<span style="font-weight:bold;">{year} {session}</span>'
            f'<span style="font-size:13px;">{tagged}/{total} ({rate}%)</span>'
            f"</div>"
            f'<div id="{sid}_body" style="display:none;">{table_html}</div>'
            f"</div>"
        )

    return "".join(parts)


def generate_html(sessions):
    total_q = sum(len(s["questions"]) for s in sessions)
    total_tagged = sum(sum(1 for q in s["questions"] if is_tagged(q)) for s in sessions)
    overall_rate = round(total_tagged / total_q * 100, 1) if total_q else 0

    heatmap = build_heatmap(sessions)
    accordion = build_accordion(sessions)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>전기기사 기출문제 태깅 현황</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {{delimiters:[
    {{left:'\\\\(',right:'\\\\)',display:false}},
    {{left:'\\\\[',right:'\\\\]',display:true}},
    {{left:'$',right:'$',display:false}}
  ]}});"></script>
<style>
  body {{ font-family: 'Apple SD Gothic Neo', sans-serif; margin: 0; padding: 20px; background: #fafafa; color: #222; }}
  h1 {{ font-size: 22px; margin-bottom: 4px; }}
  .summary {{ display: flex; gap: 20px; margin: 16px 0; flex-wrap: wrap; }}
  .card {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 14px 20px; min-width: 140px; text-align: center; }}
  .card .val {{ font-size: 28px; font-weight: bold; color: #2d7a2d; }}
  .card .lbl {{ font-size: 12px; color: #888; margin-top: 4px; }}
  .section {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
  h2 {{ font-size: 16px; margin: 0 0 12px 0; }}
</style>
</head>
<body>
<h1>전기기사 기출문제 태깅 현황 리포트</h1>
<div class="summary">
  <div class="card"><div class="val">{len(sessions)}</div><div class="lbl">총 회차</div></div>
  <div class="card"><div class="val">{total_q:,}</div><div class="lbl">총 문제 수</div></div>
  <div class="card"><div class="val">{total_tagged:,}</div><div class="lbl">태깅 완료</div></div>
  <div class="card"><div class="val" style="color:{'#2d7a2d' if overall_rate >= 80 else '#c0392b'}">{overall_rate}%</div><div class="lbl">전체 태깅률</div></div>
</div>

<div class="section">
  <h2>회차별 태깅률 히트맵</h2>
  <p style="font-size:12px;color:#888;margin:0 0 8px 0;">셀 클릭 시 해당 회차로 스크롤</p>
  {heatmap}
  <div style="margin-top:10px;font-size:12px;display:flex;gap:12px;flex-wrap:wrap;">
    <span><span style="background:#2d7a2d;color:#fff;padding:2px 6px;border-radius:3px;">100%</span> 완료</span>
    <span><span style="background:#6abf6a;color:#000;padding:2px 6px;border-radius:3px;">80~99%</span></span>
    <span><span style="background:#d4c02a;color:#000;padding:2px 6px;border-radius:3px;">60~79%</span></span>
    <span><span style="background:#e08030;color:#000;padding:2px 6px;border-radius:3px;">50~59%</span></span>
    <span><span style="background:#c0392b;color:#fff;padding:2px 6px;border-radius:3px;">&lt;50%</span></span>
  </div>
</div>

<div class="section">
  <h2>회차별 상세 (클릭하여 펼치기)</h2>
  {accordion}
</div>

<script>
function toggle(id) {{
  var el = document.getElementById(id);
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
}}
function scrollTo(id) {{
  var el = document.getElementById(id);
  if (!el) return;
  el.scrollIntoView({{behavior:'smooth', block:'start'}});
  var body = document.getElementById(id + '_body');
  if (body) body.style.display = 'block';
}}
</script>
</body>
</html>"""
    return html


def main():
    print("Loading questions...")
    sessions = load_all_questions()
    print(f"Loaded {len(sessions)} sessions")

    total_q = sum(len(s["questions"]) for s in sessions)
    total_tagged = sum(sum(1 for q in s["questions"] if is_tagged(q)) for s in sessions)
    print(f"Total questions: {total_q}, tagged: {total_tagged} ({total_tagged/total_q*100:.1f}%)")

    print("Generating HTML...")
    html = generate_html(sessions)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
