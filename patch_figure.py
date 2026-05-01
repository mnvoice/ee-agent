#!/usr/bin/env python3
"""figure fallback 패치 — app/index.html 인라인 script에 박음"""
import sys, shutil, pathlib

TARGET = pathlib.Path("app/index.html")
BACKUP = pathlib.Path("app/index.html.bak")

def check():
    if not TARGET.exists():
        print(f"❌ {TARGET} 없음"); return False
    text = TARGET.read_text(encoding='utf-8')
    checks = {
        "pdfPageIndex": text.count("pdfPageIndex"),
        "q-figure-pdf": text.count("q-figure-pdf"),
        "pdf_pages/index.json": text.count("pdf_pages/index.json"),
    }
    print("=== 박힘 상태 ===")
    all_ok = True
    for k, v in checks.items():
        status = "✅" if v > 0 else "❌"
        print(f"{status} '{k}': {v}건")
        if v == 0: all_ok = False
    print(f"백업: {'✅ 있음' if BACKUP.exists() else '❌ 없음'}")
    return all_ok

def revert():
    if not BACKUP.exists():
        print(f"❌ 백업 없음: {BACKUP}"); sys.exit(1)
    shutil.copy(BACKUP, TARGET)
    print(f"✅ 복원: {TARGET} ← {BACKUP}")

def apply():
    if not TARGET.exists():
        print(f"❌ {TARGET} 없음"); sys.exit(1)
    if BACKUP.exists():
        print(f"⚠️  {BACKUP} 이미 존재 — 먼저 --revert 또는 수동 정리"); sys.exit(1)

    text = TARGET.read_text(encoding='utf-8')

    OLD_1 = "    if (q.figure_svg) h += '<div class=\"q-figure\">' + q.figure_svg + '</div>';"
    NEW_1 = """    if (q.figure_svg) {
      h += '<div class="q-figure">' + q.figure_svg + '</div>';
    } else {
      var __key = q.year + '_' + q.session + '_' + q.q_no;
      var __pages = (window.pdfPageIndex || {})[__key];
      if (__pages && __pages.length > 0) {
        var __imgs = __pages.map(function(p) {
          return '<img src="data/' + p + '" alt="PDF 페이지" loading="lazy" style="max-width:100%;height:auto;display:block;margin-bottom:8px;border:1px solid #d1d5db;border-radius:4px;" />';
        }).join('');
        h += '<div class="q-figure-pdf" aria-label="PDF 페이지">' + __imgs + '</div>';
      }
    }"""

    cnt1 = text.count(OLD_1)
    if cnt1 == 0:
        print(f"❌ 패치 1 매칭 0건 — line 339 내용/들여쓰기 다름. 수동 확인 필요."); sys.exit(1)
    if cnt1 > 1:
        print(f"❌ 패치 1 매칭 {cnt1}건 — 1곳 아님"); sys.exit(1)

    OLD_2 = "  function init() {"
    NEW_2 = """  function init() {
    window.pdfPageIndex = {};
    fetch('data/pdf_pages/index.json')
      .then(function(r) { return r.ok ? r.json() : {}; })
      .then(function(d) { window.pdfPageIndex = d; })
      .catch(function() {});"""

    cnt2 = text.count(OLD_2)
    if cnt2 == 0:
        print(f"❌ 패치 2: 'function init()' 못 찾음"); sys.exit(1)

    shutil.copy(TARGET, BACKUP)
    print(f"✅ 백업: {BACKUP}")

    text = text.replace(OLD_1, NEW_1)
    print(f"✅ 패치 1 박음 (figure_svg fallback)")

    if cnt2 > 1:
        print(f"⚠️  'function init()' {cnt2}곳 — 첫 번째만 정정")
        text = text.replace(OLD_2, NEW_2, 1)
    else:
        text = text.replace(OLD_2, NEW_2)
    print(f"✅ 패치 2 박음 (init fetch)")

    TARGET.write_text(text, encoding='utf-8')
    print()
    check()
    print()
    print("=== 다음 ===")
    print("1. 사파리 ⌘+Option+R (강제 새로고침)")
    print("2. 1998 2회 Q17 진입 (15/1246)")
    print("3. figure 박스 떠오르는지 확인")
    print()
    print("문제 있으면: python3 patch_figure.py --revert")

if __name__ == "__main__":
    if "--revert" in sys.argv: revert()
    elif "--check" in sys.argv: check()
    else: apply()
