#!/usr/bin/env python3
"""
Phase 1 태깅 테스트 — V1 → V2 → V3 프롬프트 반복 개선
100문제 소규모 테스트로 프롬프트 품질을 측정하고 HTML 리포트를 생성합니다.

Usage:
    python scripts/tag_phase1_test.py
    python scripts/tag_phase1_test.py --version v2   # V2만 실행
    python scripts/tag_phase1_test.py --version all  # V1→V2→V3 순차 실행
"""

import argparse
import json
import os
import random
import re
import time
from collections import Counter
from pathlib import Path

import anthropic

# ── 경로 ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = DATA_DIR / "tag_phase1"
RESULTS_DIR.mkdir(exist_ok=True)

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL   = "claude-haiku-4-5-20251001"   # 비용 최소화
N_SAMPLE = 100                          # 소규모 테스트 크기


# ── 프롬프트 정의 ──────────────────────────────────────────────────────────────

PROMPT_V1 = """\
당신은 전기기사 문제 분류 전문가입니다.

규칙:
- 태그는 반드시 1개만
- 태그 = "이 공식을 알면 이 문제를 풀 수 있다"는 공식의 이름
- 단원명·챕터명 금지 (너무 넓음)

문제: {text}
과목: {subject}
기존 개념: {concept}

[출력 규칙] 태그 이름만 한 줄. 설명·이유·마크다운 절대 금지.
태그:"""


PROMPT_V2 = """\
당신은 전기기사 문제 분류 전문가입니다.

【태그 정의】
태그 = 이 공식 하나를 알면 이 문제를 풀 수 있다
공식 1개 = 태그 1개

【나쁜 태그 vs 좋은 태그 예시】

예시 1 (너무 넓은 경우)
  문제: εr=81, μr=1 매질의 고유 임피던스는?
  ❌ "전자기파"       → 단원명, 10가지 공식 포함
  ❌ "매질의 특성"    → 의미 없는 묘사
  ✅ "고유 임피던스"  → η = η₀√(μr/εr) 공식 하나

예시 2 (재료가 아닌 도구를 태그로 씀)
  문제: 무한 평면도체와 d[m] 떨어진 선전하가 받는 힘은?
  ❌ "선전하와 도체"  → 문제의 재료 묘사
  ❌ "정전기력"       → 너무 넓음
  ✅ "영상법"         → 도체를 영상전하로 대체하는 핵심 도구

예시 3 (너무 좁은 경우)
  문제: I(s) = (2s+5)/s(s+1)(s+2), t=∞ 에서 전류값은?
  ❌ "라플라스 부분분수 전개" → 풀이 방법이지 개념이 아님
  ✅ "최종값 정리"             → lim(s→0) sF(s) 공식 하나

예시 4 (올바른 경우)
  문제: 점전하 Q에 의한 전계 내에서 q를 A→B 이동시킬 때 일은?
  ✅ "점전하 전위"  → W = q(VA-VB) = Qq/4πε₀(1/r₁−1/r₂)

【판단 체크리스트】
1. 이 태그로 묶인 문제들이 같은 공식을 쓰는가?
2. 더 좁게 만들 이유가 없는가?
3. 더 넓게 만들면 다른 공식이 섞이는가?

문제: {text}
과목: {subject}
기존 개념: {concept}

[출력 규칙] 태그 이름만 한 줄. 설명·이유·마크다운 절대 금지.
태그:"""


# V3: 허용 어휘집 포함 (V2 결과 분석 후 자동 생성)
PROMPT_V3_TEMPLATE = """\
당신은 전기기사 문제 분류 전문가입니다.

【태그 정의】
태그 = 이 공식 하나를 알면 이 문제를 풀 수 있다

【나쁜 예 vs 좋은 예 (동일 원칙 적용)】
  ❌ "전자기파", "회로이론", "정전계" → 단원명 (너무 넓음)
  ❌ "선전하와 도체" → 문제 재료 묘사
  ✅ "고유 임피던스", "영상법", "최종값 정리" → 공식 하나의 이름

【허용 태그 목록 — 이 중에서만 선택, 없으면 가장 유사한 것】
{tag_list}

문제: {text}
과목: {subject}
기존 개념: {concept}

[출력 규칙] 태그 이름만 한 줄. 설명·이유·마크다운 절대 금지.
태그:"""


# ── 데이터 로드 ────────────────────────────────────────────────────────────────

def load_sample(n: int = N_SAMPLE, seed: int = 42) -> list[dict]:
    """과목별 균등 샘플링으로 n개 문제 추출."""
    files = sorted(DATA_DIR.glob("questions_기출_*.json"))
    by_subject: dict[str, list[dict]] = {}

    for fp in files:
        with open(fp, encoding="utf-8") as f:
            qs = json.load(f)
        for q in qs:
            subj = q.get("subject", "기타")
            by_subject.setdefault(subj, []).append(q)

    subjects = sorted(by_subject)
    per_subj = max(1, n // len(subjects))

    rng = random.Random(seed)
    sample = []
    for subj in subjects:
        pool = [q for q in by_subject[subj] if q.get("text")]
        chosen = rng.sample(pool, min(per_subj, len(pool)))
        sample.extend(chosen)

    # n개로 맞추기
    rng.shuffle(sample)
    return sample[:n]


# ── API 호출 ───────────────────────────────────────────────────────────────────

def clean_tag(raw: str) -> str:
    """첫 줄만 추출하고 마크다운·따옴표·공백 제거."""
    # 첫 줄만
    line = raw.strip().split("\n")[0].strip()
    # 마크다운 bold/italic 제거
    line = re.sub(r"\*+", "", line)
    # 따옴표 제거
    line = line.strip('"').strip("'").strip()
    # 설명 패턴 감지 → 오류 처리
    if len(line) > 60 or "분석" in line or "문제" in line[:5]:
        return "PARSE_ERROR"
    return line


def call_api(client: anthropic.Anthropic, prompt: str) -> str:
    for attempt in range(3):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=50,          # 어휘집 긴 이름 대응
                messages=[{"role": "user", "content": prompt}],
            )
            return clean_tag(response.content[0].text)
        except Exception as e:
            if attempt < 2:
                print(f"    재시도 ({attempt+1}): {e}")
                time.sleep(3)
            else:
                return f"ERROR: {e}"
    return "ERROR"


def run_tagging(
    questions: list[dict],
    prompt_template: str,
    version: str,
    tag_list: list[str] | None = None,
) -> list[dict]:
    """주어진 프롬프트로 전체 문제 태깅 실행."""
    client = anthropic.Anthropic(api_key=API_KEY)
    results = []
    total = len(questions)

    print(f"\n[{version}] {total}문제 태깅 시작...")

    for i, q in enumerate(questions, 1):
        concept_str = ", ".join(q.get("concept") or []) if isinstance(q.get("concept"), list) else str(q.get("concept") or "")

        if tag_list and "{tag_list}" in prompt_template:
            prompt = prompt_template.format(
                text=q.get("text", ""),
                subject=q.get("subject", ""),
                concept=concept_str,
                tag_list="\n".join(f"  - {t}" for t in tag_list),
            )
        else:
            prompt = prompt_template.format(
                text=q.get("text", ""),
                subject=q.get("subject", ""),
                concept=concept_str,
            )

        tag = call_api(client, prompt)

        results.append({
            "year": q.get("year"),
            "session": q.get("session"),
            "q_no": q.get("q_no"),
            "subject": q.get("subject"),
            "text": q.get("text", "")[:100],
            "original_concept": q.get("concept"),
            "tag": tag,
            "version": version,
        })

        if i % 10 == 0:
            print(f"  {i}/{total} 완료")
        time.sleep(0.3)   # rate limit

    return results


# ── 품질 평가 ─────────────────────────────────────────────────────────────────

# 너무 넓은 태그 판단 키워드
BROAD_KEYWORDS = [
    "전기자기학", "회로이론", "전력공학", "전기기기", "전기설비",
    "제어공학", "법칙", "이론", "정전계", "자기장", "전자기",
    "회로", "전기", "물리", "개론",
]


def evaluate(results: list[dict]) -> dict:
    tags = [r["tag"] for r in results]
    tag_counts = Counter(tags)

    too_broad = [r for r in results if any(k in r["tag"] for k in BROAD_KEYWORDS)]
    unique_ratio = len(set(tags)) / len(tags)
    error_count = sum(1 for t in tags if t.startswith("ERROR"))

    # 태그당 평균 문제 수 (중앙값)
    counts = sorted(tag_counts.values(), reverse=True)
    avg_per_tag = len(tags) / len(set(tags)) if set(tags) else 0

    return {
        "total": len(results),
        "unique_tags": len(set(tags)),
        "unique_ratio": round(unique_ratio, 3),
        "avg_per_tag": round(avg_per_tag, 2),
        "too_broad_count": len(too_broad),
        "too_broad_pct": round(len(too_broad) / len(results) * 100, 1),
        "error_count": error_count,
        "top_tags": tag_counts.most_common(15),
        "too_broad_examples": too_broad[:5],
    }


def extract_tag_vocabulary(results: list[dict]) -> list[str]:
    """V2 결과에서 너무 넓지 않은 태그만 추출해 어휘집 생성."""
    good_tags = [
        r["tag"] for r in results
        if not any(k in r["tag"] for k in BROAD_KEYWORDS)
        and not r["tag"].startswith("ERROR")
    ]
    counts = Counter(good_tags)
    # 2회 이상 등장한 태그만 포함 (노이즈 제거)
    vocab = sorted(t for t, c in counts.items() if c >= 1)
    return vocab


# ── HTML 리포트 ────────────────────────────────────────────────────────────────

def build_report(all_results: dict[str, list[dict]], evals: dict[str, dict]) -> str:
    versions = list(all_results.keys())

    # 버전별 메트릭 테이블
    metric_rows = ""
    for v in versions:
        e = evals[v]
        broad_style = "color:#c0392b;font-weight:bold;" if e["too_broad_pct"] > 20 else "color:#2d7a2d;"
        ratio_style = "color:#2d7a2d;" if 0.3 <= e["unique_ratio"] <= 0.6 else "color:#e67e22;"
        metric_rows += f"""
        <tr>
          <td style="font-weight:bold;">{v}</td>
          <td>{e['total']}</td>
          <td>{e['unique_tags']}</td>
          <td style="{ratio_style}">{e['unique_ratio']}</td>
          <td>{e['avg_per_tag']}</td>
          <td style="{broad_style}">{e['too_broad_count']} ({e['too_broad_pct']}%)</td>
          <td>{e['error_count']}</td>
        </tr>"""

    # 버전별 상세 카드
    detail_cards = ""
    for v in versions:
        results = all_results[v]
        e = evals[v]

        # 상위 태그 바 차트
        max_count = e["top_tags"][0][1] if e["top_tags"] else 1
        tag_bars = ""
        for tag, cnt in e["top_tags"]:
            pct = cnt / max_count * 100
            color = "#c0392b" if any(k in tag for k in BROAD_KEYWORDS) else "#2d6abf"
            tag_bars += f"""
            <div style="margin-bottom:6px;">
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="min-width:200px;font-size:13px;color:#333;">{tag}</span>
                <div style="background:{color};height:16px;width:{pct:.0f}%;min-width:4px;border-radius:3px;"></div>
                <span style="font-size:12px;color:#888;">{cnt}개</span>
              </div>
            </div>"""

        # 문제별 결과 테이블
        rows = ""
        for r in results:
            tag = r["tag"]
            is_broad = any(k in tag for k in BROAD_KEYWORDS)
            is_error = tag.startswith("ERROR")
            if is_error:
                row_bg = "#fff0f0"
                tag_html = f'<span style="color:#c0392b;">{tag}</span>'
            elif is_broad:
                row_bg = "#fff8e1"
                tag_html = f'<span style="color:#e67e22;font-weight:bold;">⚠ {tag}</span>'
            else:
                row_bg = "#f8fff8"
                tag_html = f'<span style="color:#2d7a2d;">{tag}</span>'

            orig = r["original_concept"]
            orig_str = ", ".join(orig) if isinstance(orig, list) else str(orig or "-")
            text_short = r["text"][:60] + ("…" if len(r["text"]) >= 60 else "")

            rows += f"""
            <tr style="background:{row_bg};">
              <td style="font-size:11px;color:#888;">{r['year']} {r['session']} Q{r['q_no']}</td>
              <td style="font-size:11px;color:#555;">{r['subject']}</td>
              <td style="font-size:12px;">{text_short}</td>
              <td style="font-size:11px;color:#888;">{orig_str[:40]}</td>
              <td style="font-size:13px;">{tag_html}</td>
            </tr>"""

        detail_cards += f"""
        <div class="card" id="card-{v}">
          <div class="card-hd" onclick="toggle('body-{v}')">
            <span style="font-weight:bold;">{v}</span>
            <span style="font-size:13px;color:rgba(255,255,255,.8);">
              고유태그 {e['unique_tags']}개 · 넓은태그 {e['too_broad_pct']}% · 평균 {e['avg_per_tag']}문제/태그
            </span>
          </div>
          <div id="body-{v}" style="padding:20px;">
            <h3 style="font-size:14px;color:#1a3c6e;margin-bottom:12px;">상위 태그 분포</h3>
            <div style="margin-bottom:20px;">{tag_bars}</div>
            <h3 style="font-size:14px;color:#1a3c6e;margin-bottom:10px;">문제별 태깅 결과</h3>
            <div style="overflow-x:auto;">
            <table style="width:100%;border-collapse:collapse;font-size:12px;">
              <tr style="background:#f0f4f8;">
                <th style="padding:6px 8px;text-align:left;">회차</th>
                <th style="padding:6px 8px;text-align:left;">과목</th>
                <th style="padding:6px 8px;text-align:left;">문제</th>
                <th style="padding:6px 8px;text-align:left;">기존 concept</th>
                <th style="padding:6px 8px;text-align:left;">새 태그</th>
              </tr>
              {rows}
            </table>
            </div>
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Phase 1 태깅 프롬프트 비교 리포트</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Apple SD Gothic Neo','Noto Sans KR',sans-serif;background:#f0f2f5;padding:24px 12px;color:#222;line-height:1.65}}
h1{{text-align:center;font-size:20px;margin-bottom:6px;color:#1a3c6e}}
.sub{{text-align:center;font-size:13px;color:#888;margin-bottom:28px}}
.summary{{max-width:900px;margin:0 auto 24px;background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.08);padding:20px}}
.summary h2{{font-size:15px;color:#1a3c6e;margin-bottom:12px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{padding:9px 12px;border-bottom:1px solid #eee;text-align:left}}
th{{background:#f5f7fa;font-weight:600;color:#555}}
.legend{{display:flex;gap:16px;flex-wrap:wrap;margin-top:14px;font-size:12px}}
.legend span{{display:flex;align-items:center;gap:6px}}
.dot{{width:12px;height:12px;border-radius:50%;display:inline-block}}
.card{{max-width:900px;margin:0 auto 16px;background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.08);overflow:hidden}}
.card-hd{{background:linear-gradient(135deg,#1a3c6e,#2d6abf);color:#fff;padding:14px 20px;cursor:pointer;display:flex;justify-content:space-between;align-items:center}}
</style>
</head>
<body>
<h1>Phase 1 태깅 프롬프트 비교 리포트</h1>
<p class="sub">모델: {MODEL} · 샘플: {N_SAMPLE}문제 · 목표: 공식 1개 = 태그 1개</p>

<div class="summary">
  <h2>버전별 품질 요약</h2>
  <table>
    <tr>
      <th>버전</th><th>총 문제</th><th>고유 태그</th>
      <th>다양성<br><small>(목표: 0.3~0.6)</small></th>
      <th>평균문제/태그</th>
      <th>넓은 태그<br><small>(목표: &lt;10%)</small></th>
      <th>오류</th>
    </tr>
    {metric_rows}
  </table>
  <div class="legend">
    <span><span class="dot" style="background:#2d7a2d;"></span> 좋은 태그</span>
    <span><span class="dot" style="background:#e67e22;"></span> ⚠ 너무 넓음</span>
    <span><span class="dot" style="background:#c0392b;"></span> 오류</span>
  </div>
</div>

{detail_cards}

<script>
function toggle(id){{
  var el=document.getElementById(id);
  el.style.display=el.style.display==='none'?'block':'none';
}}
// 기본: V1만 열림
document.addEventListener('DOMContentLoaded',function(){{
  document.querySelectorAll('[id^="body-"]').forEach(function(el){{
    el.style.display='none';
  }});
  var first=document.querySelector('[id^="body-"]');
  if(first) first.style.display='block';
}});
</script>
</body>
</html>"""


# ── 메인 ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="all",
                        choices=["v1", "v2", "v3", "all"],
                        help="실행할 프롬프트 버전 (기본: all)")
    parser.add_argument("--sample", type=int, default=N_SAMPLE,
                        help=f"샘플 크기 (기본: {N_SAMPLE})")
    args = parser.parse_args()

    if not API_KEY:
        print("ANTHROPIC_API_KEY 환경변수가 없습니다.")
        return

    print(f"샘플 {args.sample}개 로드...")
    questions = load_sample(args.sample)
    print(f"과목별 분포: { {s: sum(1 for q in questions if q['subject']==s) for s in set(q['subject'] for q in questions)} }")

    all_results: dict[str, list[dict]] = {}
    evals: dict[str, dict] = {}

    run_v1 = args.version in ("v1", "all")
    run_v2 = args.version in ("v2", "all")
    run_v3 = args.version in ("v3", "all")

    # ── V1 ──────────────────────────────────────────────────────────────────
    if run_v1:
        v1_path = RESULTS_DIR / "v1_results.json"
        if v1_path.exists():
            print("\n[V1] 기존 결과 로드...")
            with open(v1_path, encoding="utf-8") as f:
                v1_results = json.load(f)
        else:
            v1_results = run_tagging(questions, PROMPT_V1, "V1")
            with open(v1_path, "w", encoding="utf-8") as f:
                json.dump(v1_results, f, ensure_ascii=False, indent=2)

        all_results["V1"] = v1_results
        evals["V1"] = evaluate(v1_results)
        e = evals["V1"]
        print(f"\n[V1 분석] 고유태그={e['unique_tags']} 다양성={e['unique_ratio']} 넓은태그={e['too_broad_pct']}%")
        print("  상위 태그:", [t for t, _ in e["top_tags"][:8]])

    # ── V2 ──────────────────────────────────────────────────────────────────
    if run_v2:
        v2_path = RESULTS_DIR / "v2_results.json"
        if v2_path.exists():
            print("\n[V2] 기존 결과 로드...")
            with open(v2_path, encoding="utf-8") as f:
                v2_results = json.load(f)
        else:
            v2_results = run_tagging(questions, PROMPT_V2, "V2")
            with open(v2_path, "w", encoding="utf-8") as f:
                json.dump(v2_results, f, ensure_ascii=False, indent=2)

        all_results["V2"] = v2_results
        evals["V2"] = evaluate(v2_results)
        e = evals["V2"]
        print(f"\n[V2 분석] 고유태그={e['unique_tags']} 다양성={e['unique_ratio']} 넓은태그={e['too_broad_pct']}%")
        print("  상위 태그:", [t for t, _ in e["top_tags"][:8]])

    # ── V3 (공식 어휘집: full_concept_mapping.json 사용) ─────────────────────
    if run_v3:
        # full_concept_mapping.json에서 과목별 어휘집 로드
        concept_map_path = DATA_DIR / "full_concept_mapping.json"
        with open(concept_map_path, encoding="utf-8") as f:
            concept_map = json.load(f)

        # 전체 어휘집 (과목 무관)
        vocab: list[str] = []
        for subj_concepts in concept_map.values():
            for c in subj_concepts:
                name = c["name"] if isinstance(c, dict) else c
                if name not in vocab:
                    vocab.append(name)

        vocab_path = RESULTS_DIR / "tag_vocabulary.json"
        with open(vocab_path, "w", encoding="utf-8") as f:
            json.dump(vocab, f, ensure_ascii=False, indent=2)
        print(f"\n[V3] concept_mapping 어휘집 {len(vocab)}개 로드: {vocab[:5]}...")

        v3_path = RESULTS_DIR / "v3_results.json"
        if v3_path.exists():
            print("[V3] 기존 결과 로드...")
            with open(v3_path, encoding="utf-8") as f:
                v3_results = json.load(f)
        else:
            v3_results = run_tagging(questions, PROMPT_V3_TEMPLATE, "V3", tag_list=vocab)
            with open(v3_path, "w", encoding="utf-8") as f:
                json.dump(v3_results, f, ensure_ascii=False, indent=2)

        all_results["V3"] = v3_results
        evals["V3"] = evaluate(v3_results)
        e = evals["V3"]
        print(f"\n[V3 분석] 고유태그={e['unique_tags']} 다양성={e['unique_ratio']} 넓은태그={e['too_broad_pct']}%")

    # ── HTML 리포트 생성 ────────────────────────────────────────────────────
    report_path = DATA_DIR / "tag_phase1_report.html"
    html = build_report(all_results, evals)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n리포트 저장: {report_path}")

    # 요약 JSON
    summary_path = RESULTS_DIR / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({v: {k: val for k, val in e.items() if k != "too_broad_examples"} for v, e in evals.items()},
                  f, ensure_ascii=False, indent=2)

    import subprocess
    subprocess.Popen(["open", str(report_path)])
    print("브라우저 오픈...")


if __name__ == "__main__":
    main()
