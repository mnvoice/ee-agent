#!/usr/bin/env python3
"""페이지별 문제 매핑 — 6장 통째 → 문제별 1~2장"""
import fitz, re, json, sys, shutil, unicodedata
from pathlib import Path
from collections import defaultdict

PDF_DIR = Path("data")
PNG_DIR = Path("data/pdf_pages")
INDEX = PNG_DIR / "index.json"
BACKUP = PNG_DIR / "index.json.bak.before_per_q"

def find_pdf_for_round(year, session):
    ty = unicodedata.normalize('NFC', str(year))
    ts = unicodedata.normalize('NFC', f"{session}회")
    for pdf in PDF_DIR.glob("*.pdf"):
        n = unicodedata.normalize('NFC', pdf.name)
        if ty in n and ts in n: return pdf
    return None

def extract_problems_per_page(pdf_path):
    doc = fitz.open(pdf_path)
    result, text_total = [], 0
    for page in doc:
        text = page.get_text()
        text_total += len(text.strip())
        problems = sorted(set(int(m) for m in re.findall(r"문제\s*(\d+)", text)))
        result.append(problems)
    doc.close()
    return result, text_total

def build_mapping():
    if not INDEX.exists():
        print(f"❌ {INDEX} 없음"); sys.exit(1)
    with open(INDEX, encoding='utf-8') as f:
        old_index = json.load(f)
    
    rounds = set()
    for key in old_index:
        parts = key.split("_")
        if len(parts) >= 3:
            rounds.add((parts[0], parts[1].rstrip('회')))
    
    new_map = defaultdict(list)
    ok_rounds, no_text, no_problem = [], [], []
    
    for year, session in sorted(rounds):
        pdf = find_pdf_for_round(year, session)
        if not pdf: continue
        
        pages, text_total = extract_problems_per_page(pdf)
        if text_total < 100:
            no_text.append((year, session, pdf.name)); continue
        
        total_p = sum(len(p) for p in pages)
        if total_p == 0:
            no_problem.append((year, session, pdf.name)); continue
        
        ok_rounds.append((year, session))
        for page_idx, problems in enumerate(pages):
            for q_no in problems:
                key = f"{year}_{session}회_{q_no}"
                path = f"pdf_pages/{year}_{session}회/page_{page_idx+1}.png"
                if path not in new_map[key]:
                    new_map[key].append(path)
    
    return dict(new_map), ok_rounds, no_text, no_problem, old_index

def dry_run():
    new_map, ok, no_text, no_prob, old_map = build_mapping()
    print("\n=== Dry-Run ===")
    print(f"텍스트 추출 OK 회차: {len(ok)}")
    print(f"스캔본 (OCR 필요): {len(no_text)}")
    print(f"텍스트 있으나 매칭 0: {len(no_prob)}")
    
    if no_text:
        print("\n스캔본 회차 (기존 6장 통째 유지):")
        for y, s, n in no_text[:10]:
            print(f"  {y} {s}회: {n}")
        if len(no_text) > 10: print(f"  ... 외 {len(no_text)-10}건")
    
    print(f"\n기존 매핑 (통째): {len(old_map)}건")
    print(f"새 매핑 (문제별): {len(new_map)}건")
    
    if new_map:
        old_avg = sum(len(v) for v in old_map.values()) / len(old_map)
        new_avg = sum(len(v) for v in new_map.values()) / len(new_map)
        print(f"평균 페이지: {old_avg:.1f}장 → {new_avg:.1f}장")
        
        print("\n샘플:")
        for k in list(new_map.keys())[:5]:
            print(f"  {k}: {len(old_map.get(k,[]))}장 → {len(new_map[k])}장")
    
    print("\n=== 적용 ===")
    print("python3 map_pages.py --apply")

def apply():
    if BACKUP.exists():
        print(f"⚠️  {BACKUP} 있음 — --revert 또는 수동 정리"); sys.exit(1)
    
    new_map, ok, no_text, no_prob, old_map = build_mapping()
    if not new_map:
        print("❌ 매핑 0건 — apply 취소"); sys.exit(1)
    
    final_map = dict(old_map)
    final_map.update(new_map)
    
    shutil.copy(INDEX, BACKUP)
    print(f"✅ 백업: {BACKUP}")
    
    with open(INDEX, 'w', encoding='utf-8') as f:
        json.dump(final_map, f, ensure_ascii=False, indent=2)
    print(f"✅ 갱신: {INDEX}")
    
    print(f"\n세분화: {len(new_map)}건 / 통째 유지(스캔본): {len(final_map)-len(new_map)}건")
    print("\n=== 검증 ===")
    print("1. 사파리 ⌘+Option+R")
    print("2. 1998 2회 Q17 진입 → 페이지 줄었나?")
    print(f"\n문제 있으면: python3 map_pages.py --revert")

def revert():
    if not BACKUP.exists():
        print(f"❌ 백업 없음"); sys.exit(1)
    shutil.copy(BACKUP, INDEX)
    print(f"✅ 복원: {INDEX} ← {BACKUP}")

if __name__ == "__main__":
    if "--apply" in sys.argv: apply()
    elif "--revert" in sys.argv: revert()
    else: dry_run()
