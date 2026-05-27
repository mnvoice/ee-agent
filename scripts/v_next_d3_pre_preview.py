"""v_next D-3 전력공학 exploration + preview — candidate policy draft + measurement.

User-authorized 2026-05-27 KST (D-3 power preview gate design 정합).

This script:
1. Loads v_full selection_manifest 전력공학 242건.
2. Defines a CANDIDATE_POWER_POLICY draft (slot/item/keyword/dl/essence/trap).
   - This draft is NOT promoted to official ITEM_POLICY.
   - Official promotion is a separate user gate.
3. Reuses D-2 preview logic via import (evidence_field / score / classify_status / broad keyword check).
4. Applies CANDIDATE policy to 242 power entries.
5. Reports CLEAN / NEEDS_REVIEW / SUSPECT / unmatched / gap distribution.

Important policies (사용자 명시 정합):
- D-2 ITEM_POLICY: 미수정
- D-2 sealed assets: 미수정
- D-2 CLEAN70 비율을 D-3에 일반화하지 않음
- 전력공학 ITEM_POLICY 확정 0 (draft만)
- broad keyword rescue 0
- tag-only rescue 0
- SUSPECT rescue 0
- quota filling 0
- CLEAN main 후보, tag-only catalog, SUSPECT/unmatched gap
- 기준 미달 시 기준을 낮추지 않음 (gold sample baseline 정합)

Outputs:
- docs/.../v_next_policy/d3_pre_preview_report.md

Forbidden (hardcoded):
- D-3 selector / input / generation
- D-3 audit
- D-2 scripts 수정
- D-2 sealed assets 수정
- v_full handoff scope 수정
- commit
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

# === Reuse D-2 preview logic (evidence/score/classify/broad keyword) ===
# D-2 sealed assets에서 logic만 import — D-2 ITEM_POLICY는 사용 0
from v_next_d2_pre_preview import (  # type: ignore
    BROAD_KEYWORD_BLACKLIST,
    QUESTIONS_JSON,
    V_FULL_MANIFEST,
    EG_DIR,
    _normalize_ws,
    keyword_hit,
    is_broad,
)

REPORT_PATH = EG_DIR / "v_next_policy/d3_pre_preview_report.md"

# Target subject (D-3)
TARGET_SUBJECT = "전력공학"

# ---------------------------------------------------------------------------
# CANDIDATE_POWER_POLICY (DRAFT — NOT OFFICIAL ITEM_POLICY)
# ---------------------------------------------------------------------------
# Derived from v_full 242 전력공학 entries' tag patterns + P1 slice schema 정합.
# Narrow + evidence-grounded keywords only. broad keyword 0 (BLACKLIST 정합).
# This draft is preview-only. Official promotion requires separate user gate.
# ---------------------------------------------------------------------------

CANDIDATE_POWER_POLICY: dict[tuple[str, str, str], dict[str, Any]] = {
    # ===== candidate slot 1: 전력_송배전D (D/Dynamic + 송전) =====
    ("전력공학", "전력_송배전D", "분포정수 송전"): {
        "keywords": [
            "분포정수", "작용인덕턴스", "작용정전용량",
            "L₀", "C₀", "Cₛ", "대지정전용량",
            "특성 임피던스", "전파상수",
        ],
        "dl": "전력 분포정수 -> 회로 분포정수 -> 회로 4단자망",
        "essence": "송전선을 분포정수 모델로 어떻게 표현하는가",
        "trap": "집중정수 vs 분포정수 모델 혼동 함정",
    },
    ("전력공학", "전력_송배전D", "전압강하·전력손실"): {
        "keywords": [
            "전압강하", "전압변동률", "Vd", "전압강하율",
            "전력손실", "전력손실률", "Pₗ",
            "송전 손실", "송전효율",
        ],
        "dl": "전력 전압강하/손실 -> 회로 임피던스 -> 회로 옴의 법칙",
        "essence": "송전 거리·전류·임피던스가 전압강하에 어떻게 작용하는가",
        "trap": "단상 vs 3상 전압강하 공식 혼동 함정",
    },
    ("전력공학", "전력_송배전D", "송전 용량/거리"): {
        "keywords": [
            "송전전압", "송전용량", "송전 거리",
            "선로 정수", "송전선",
        ],
        "dl": "전력 송전용량 -> 회로 4단자망 -> 회로 분포정수",
        "essence": "송전 거리와 전압이 송전 용량에 어떻게 작용하는가",
        "trap": "송전 전압급 단위 혼동 함정",
    },
    ("전력공학", "전력_송배전D", "코로나 / 전선 도체"): {
        "keywords": [
            "코로나", "코로나 손실", "코로나 임계전압",
            "표피두께", "표피효과 전력",
            "도체 손실", "도체 설계",
            "복도체", "분할 도체",
        ],
        "dl": "전력 코로나/표피효과 -> 회로 분포정수 -> 회로 임피던스",
        "essence": "전선 표면 전계와 도체 손실이 어떻게 작용하는가",
        "trap": "코로나 임계전압 vs 정격 전압 혼동 함정",
    },

    # ===== candidate slot 2: 전력_보호고장S (S/Fault + 보호) =====
    ("전력공학", "전력_보호고장S", "단락전류·임피던스"): {
        "keywords": [
            "단락전류", "Iₛ", "%Z", "%임피던스",
            "단락용량", "Pₛ",
            "임피던스 환산", "기준용량",
        ],
        "dl": "전력 단락전류 -> 회로 옴의 법칙 -> 회로 임피던스 환산",
        "essence": "%Z와 기준용량을 어떻게 환산해 단락전류를 구하는가",
        "trap": "기준용량 환산 비율 함정 / %Z 기준 변경 혼동",
    },
    ("전력공학", "전력_보호고장S", "지락·중성점 접지"): {
        "keywords": [
            "지락전류", "중성점", "중성점 접지",
            "소호리액터", "비접지", "직접접지",
            "접지방식",
        ],
        "dl": "전력 중성점 접지 -> 회로 대칭분 해석",
        "essence": "중성점 접지 방식이 지락전류에 어떻게 작용하는가",
        "trap": "직접접지 vs 소호리액터 vs 비접지 특성 혼동 함정",
    },
    ("전력공학", "전력_보호고장S", "차단기"): {
        "keywords": [
            "차단기", "차단용량",
            "소호매질", "진공차단기", "SF6",
            "공기차단기", "유입차단기",
            "차단 시간",
        ],
        "dl": "전력 차단기 -> 회로 단락전류 / 회로 임피던스 환산",
        "essence": "소호매질 종류가 차단 특성에 어떻게 작용하는가",
        "trap": "차단 용량 vs 차단 시간 혼동 함정",
    },
    ("전력공학", "전력_보호고장S", "보호계전기·피뢰기"): {
        "keywords": [
            "보호계전기", "거리계전기", "차동계전기",
            "과전류 차단기", "역시한 계전기",
            "피뢰기", "LA",
            "절연 협조",
        ],
        "dl": "전력 보호계전기/피뢰기 -> 설비 절연/보호 -> 회로 임피던스",
        "essence": "보호계전기 동작 특성과 피뢰기 정격이 어떻게 작용하는가",
        "trap": "보호계전기 정정 / 피뢰기 정격 혼동 함정",
    },

    # ===== candidate slot 3: 전력_안정도D (D/Dynamic + 안정도) =====
    ("전력공학", "전력_안정도D", "정태·과도 안정도"): {
        "keywords": [
            "정태 안정도", "과도 안정도", "동태 안정도",
            "동기화력", "동기 화력",
            "안정도 한계",
        ],
        "dl": "전력 안정도 -> 회로 라플라스 극점 -> 제어 안정도",
        "essence": "동기발전기 회전자 진동이 안정도에 어떻게 작용하는가",
        "trap": "정태 vs 과도 vs 동태 안정도 정의 혼동 함정",
    },
    ("전력공학", "전력_안정도D", "안정도 개선책"): {
        "keywords": [
            "안정도 개선", "직렬콘덴서", "분로리액터",
            "FACTS",
            "송전선 보상",
        ],
        "dl": "전력 안정도 개선 -> 회로 임피던스 보상 -> 제어 안정도",
        "essence": "직렬/분로 보상이 안정도에 어떻게 작용하는가",
        "trap": "직렬콘덴서 vs 분로리액터 효과 혼동 함정",
    },

    # ===== candidate slot 4: 전력_변환본질4 (S/Conversion + 발전기) =====
    ("전력공학", "전력_변환본질4", "동기발전기 운전"): {
        "keywords": [
            "동기속도", "Ns",
            "단절권", "분포권",
            "권선계수", "Kw",
            "동기발전기",
        ],
        "dl": "전력 동기발전기 -> 기기 동기 / 유기기전력",
        "essence": "동기속도와 권선계수가 발전기 출력에 어떻게 작용하는가",
        "trap": "단절권 vs 분포권 계수 혼동 함정",
    },
    ("전력공학", "전력_변환본질4", "유기기전력 전력"): {
        "keywords": [
            "E = 4.44 f N Φ", "4.44 f N", "4.44fN",
            "변압기 유기기전력", "변압기 유도기전력",
            "교류 발전기 유기기전력",
        ],
        "dl": "전력 유기기전력 -> 기기 변압기 / 동기발전기",
        "essence": "주파수와 권선이 유기기전력에 어떻게 작용하는가",
        "trap": "4.44 공식 변수 의미 혼동 함정",
    },
    ("전력공학", "전력_변환본질4", "병렬운전·효율"): {
        "keywords": [
            "병렬운전", "병렬 운전 조건",
            "발전기 효율", "부하손", "무부하손",
            "철손", "동손",
        ],
        "dl": "전력 병렬운전/효율 -> 기기 변환 효율",
        "essence": "병렬운전 조건과 손실 분배가 어떻게 작용하는가",
        "trap": "병렬운전 4 조건 혼동 함정",
    },

    # ===== candidate slot 5: 전력_함정S (S/Static + 함정) =====
    ("전력공학", "전력_함정S", "부하율·수용률·부등률"): {
        "keywords": [
            "부하율", "수용률", "부등률",
            "일부하", "평균전력", "최대전력",
        ],
        "dl": None,  # 정직 (정적 함정 영역)
        "essence": "부하율/수용률/부등률을 어떻게 구분해 외우는가",
        "trap": "부하율 vs 수용률 vs 부등률 정의 혼동 함정",
    },
    ("전력공학", "전력_함정S", "역률 개선"): {
        "keywords": [
            "역률 개선", "역률 보상",
            "전력용 콘덴서", "콘덴서 용량", "Qc",
            "진상 콘덴서",
        ],
        "dl": None,  # 정직
        "essence": "역률 개선 콘덴서 용량을 어떻게 계산하는가",
        "trap": "Qc 공식 sin / cos 혼동 함정",
    },

    # ===== candidate slot 6: 전력_설비고장 (S/Static + 설비) =====
    ("전력공학", "전력_설비고장", "가공전선 이격거리"): {
        "keywords": [
            "가공전선", "이격거리",
            "가공지선", "접지선",
            "안테나", "약전류전선", "식물 이격",
        ],
        "dl": None,
        "essence": "가공전선과 다른 시설간 안전 이격거리는 어떻게 정해지는가",
        "trap": "전선 종류별 이격거리 표 혼동 함정",
    },
    ("전력공학", "전력_설비고장", "가공전선로 경간·이도"): {
        "keywords": [
            "경간", "이도", "실장",
            "인장강도", "풍속하중",
            "전선 장력",
        ],
        "dl": None,
        "essence": "전선 장력·이도·경간이 어떻게 작용하는가",
        "trap": "경간 vs 이도 관계 혼동 함정",
    },
    ("전력공학", "전력_설비고장", "절연내력 / 유도장해"): {
        "keywords": [
            "절연내력시험전압", "절연내력",
            "유도장해", "통신·유도장해", "통신선",
            "전자유도 송전",
        ],
        "dl": None,
        "essence": "절연내력 시험전압과 유도장해 경감이 어떻게 작용하는가",
        "trap": "절연내력 시험전압 배율 / 유도장해 경감대책 혼동 함정",
    },
}


# ---------------------------------------------------------------------------
# Evidence classification + score (D-2 preview logic 정합)
# ---------------------------------------------------------------------------

def classify_evidence_local(q: dict, kw: str) -> Optional[str]:
    """Evidence field — both / question_text / solution / tag / None."""
    text = q.get("text") or ""
    sol = q.get("solution") or ""
    tag = q.get("tag") or ""
    qh = keyword_hit(text, kw)
    sh = keyword_hit(sol, kw)
    th = keyword_hit(tag, kw)
    if qh and sh:
        return "both"
    if qh:
        return "question_text"
    if sh:
        return "solution"
    if th:
        return "tag"
    return None


def compute_score_local(q: dict, item: str, kw: str, slot_kws: list[str]) -> int:
    """P1 slice score (max 18). D-2 preview 정합."""
    score = 0
    text, sol, tag = q.get("text") or "", q.get("solution") or "", q.get("tag") or ""
    if item:
        score += 5
    if keyword_hit(text, kw):
        score += 5
    if keyword_hit(sol, kw):
        score += 2
    tag_hit = False
    if keyword_hit(tag, kw):
        tag_hit = True
    else:
        for k in slot_kws:
            if is_broad(k):
                continue
            if keyword_hit(tag, k):
                tag_hit = True
                break
        if not tag_hit and item:
            base = item.split("_")[0] if "_" in item else item
            if keyword_hit(tag, base):
                tag_hit = True
    if tag_hit:
        score += 3
    # essence default +3
    score += 3
    return score


def classify_status_local(score: int, evidence: str) -> str:
    if evidence == "tag":
        return "NEEDS_REVIEW"
    if score >= 15:
        return "CLEAN"
    if score >= 10:
        return "SUSPECT"
    return "EXCLUDE_LOW"


def match_candidate_item(q: dict) -> Optional[dict]:
    """전력공학 entry → best candidate (slot, item) match."""
    sub = q.get("subject")
    if sub != TARGET_SUBJECT:
        return None
    best: Optional[dict] = None
    for (subject, slot, item), policy in CANDIDATE_POWER_POLICY.items():
        if subject != sub:
            continue
        for kw in policy["keywords"]:
            if is_broad(kw):
                continue
            ev = classify_evidence_local(q, kw)
            if ev is None:
                continue
            score = compute_score_local(q, item, kw, policy["keywords"])
            status = classify_status_local(score, ev)
            cand = {
                "subject": subject, "slot": slot, "item": item,
                "matched_keyword": kw, "evidence_field": ev,
                "score": score, "status": status,
                "dl": policy["dl"], "essence": policy["essence"], "trap": policy["trap"],
            }
            if best is None or cand["score"] > best["score"]:
                best = cand
    return best


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    for arg in sys.argv[1:]:
        if arg in ("--generate", "--create-inputs", "--commit", "--force", "--promote-policy"):
            print(f"ERROR: {arg} is permanently disabled (preview-only).", file=sys.stderr)
            return 1

    if not QUESTIONS_JSON.exists():
        print(f"ERROR: {QUESTIONS_JSON} not found", file=sys.stderr); return 1
    if not V_FULL_MANIFEST.exists():
        print(f"ERROR: {V_FULL_MANIFEST} not found", file=sys.stderr); return 1

    manifest = json.loads(V_FULL_MANIFEST.read_text(encoding="utf-8"))
    qs = json.loads(QUESTIONS_JSON.read_text(encoding="utf-8"))

    def q_id(q): return f"{q.get('year')}_{q.get('session')}_{q.get('q_no')}"
    q_by_id = {q_id(q): q for q in qs}

    # Extract 242 power entries
    target_items = [it for it in manifest["items"] if it["subject"] == TARGET_SUBJECT]
    target_ids = [it["selected_id"] for it in target_items]

    # Apply candidate policy
    matched: list[dict] = []
    unmatched: list[dict] = []
    for it in target_items:
        sid = it["selected_id"]
        q = q_by_id.get(sid)
        if q is None:
            unmatched.append({"id": sid, "reason": "not_in_questions_json"})
            continue
        m = match_candidate_item(q)
        if m is None:
            unmatched.append({
                "id": sid,
                "tag": (q.get("tag") or "")[:60],
                "reason": "no_candidate_item_match",
            })
            continue
        m["id"] = sid
        matched.append(m)

    # === Measurements ===
    total = len(target_items)
    matched_n = len(matched)
    unmatched_n = len(unmatched)

    # status 분포
    status_dist = Counter(m["status"] for m in matched)
    clean = status_dist.get("CLEAN", 0)
    needs_review = status_dist.get("NEEDS_REVIEW", 0)
    suspect = status_dist.get("SUSPECT", 0)
    exclude_low = status_dist.get("EXCLUDE_LOW", 0)

    # catalog (tag-only) / gap (SUSPECT + EXCLUDE_LOW + unmatched)
    catalog_n = needs_review
    gap_n = suspect + exclude_low + unmatched_n

    # evidence_field 분포
    ev_dist = Counter(m["evidence_field"] for m in matched)

    # D/Dynamic 후보 수 — candidate slot에서 D 또는 S/Fault 영역 추출
    d_dynamic_slots = {"전력_송배전D", "전력_안정도D", "전력_변환본질4", "전력_보호고장S"}  # D/Dynamic + S/Fault + S/Conversion (generator path 3 적용 영역)
    dynamic_candidates = sum(1 for m in matched if m["slot"] in d_dynamic_slots)

    # metadata 부착 가능 수
    dl_attached = sum(1 for m in matched if m.get("dl") is not None)
    essence_attached = sum(1 for m in matched if m.get("essence") is not None)
    trap_attached = sum(1 for m in matched if m.get("trap") is not None)

    # broad keyword hit 검증
    broad_hits = sum(1 for m in matched if m["matched_keyword"].strip() in BROAD_KEYWORD_BLACKLIST)

    # expected expansion non-zero (CLEAN + dl)
    clean_with_dl = sum(1 for m in matched if m["status"] == "CLEAN" and m.get("dl") is not None)

    # slot/item 분포
    slot_item_dist = Counter((m["slot"], m["item"]) for m in matched)

    # ===========================================================================
    # Render report
    # ===========================================================================
    L: list[str] = []
    P = L.append

    P("# v_next D-3 전력공학 Preview Report (Exploration + Candidate Policy Draft)\n")
    P("> 2026-05-27 KST. D-3 전력공학 preview gate 실행 결과.")
    P("> **본 record는 exploration + candidate policy draft 단계** — D-2-pre와 달리 ITEM_POLICY가 이미 있는 상태에서의 단순 측정 아님.")
    P("> D-3 selector 작성 0 / D-3 input 생성 0 / D-3 generation 0 / D-3 audit 0 / D-2 sealed assets 미수정 / v_full handoff scope 미수정 / commit 0.")
    P("> **공식 ITEM_POLICY 승격 0** — 본 draft는 preview-only, 별 사용자 게이트 결정 영역.\n")

    P("## 1. D-3 단계 위치 정합\n")
    P("- 본 단계는 **측정 단계가 아니라 exploration + candidate policy draft 단계**")
    P("- D-2 ITEM_POLICY (회로+제어 20 item)는 이미 있음 → D-2-pre는 단순 측정 가능")
    P("- D-3 전력공학 ITEM_POLICY는 부재 → D-3 preview는 candidate slot/item draft 신설 + measurement")
    P("- 본 draft는 본 script 내부 hardcoded, 공식 ITEM_POLICY 미혼합")
    P("- 공식 D-3 ITEM_POLICY 승격은 본 preview 결과 후 별 사용자 게이트\n")

    P("## 2. 측정 11 항목 매트릭스\n")
    P("| # | 항목 | 측정 |")
    P("|---:|---|---:|")
    P(f"| 1 | 전력공학 전체 후보 수 (v_full manifest) | **{total}** |")
    P(f"| 2 | evidence 기반 D/Dynamic 후보 수 (candidate slot D/S-Fault/S-Conversion 영역) | **{dynamic_candidates}** ({dynamic_candidates/total*100:.1f}%) |")
    P(f"| 3 | candidate slot/item 후보 목록 | {len(set((s,i) for s,i in slot_item_dist.keys()))} item × {len(set(s for s,_ in slot_item_dist.keys()))} slot |")
    P(f"| 4 | dynamic_link 부착 가능 수 | **{dl_attached}** ({dl_attached/total*100:.1f}%) |")
    P(f"| 5 | essence_question 부착 가능 수 | **{essence_attached}** ({essence_attached/total*100:.1f}%) |")
    P(f"| 6 | representative_trap / trap_type 부착 가능 수 | **{trap_attached}** ({trap_attached/total*100:.1f}%) |")
    P(f"| 7 | evidence_field 분포 | both {ev_dist.get('both',0)} / qt {ev_dist.get('question_text',0)} / sol {ev_dist.get('solution',0)} / tag {ev_dist.get('tag',0)} |")
    P(f"| 8 | CLEAN / NEEDS_REVIEW / SUSPECT / EXCLUDE_LOW / unmatched | {clean} / {needs_review} / {suspect} / {exclude_low} / {unmatched_n} |")
    P(f"| 9 | broad keyword hit | **{broad_hits}** {'✓' if broad_hits == 0 else '✗'} |")
    P(f"| 10 | expected expansion non-zero (CLEAN + dl) | **{clean_with_dl}** ({clean_with_dl/total*100:.1f}%) |")
    P(f"| 11 | catalog ({catalog_n}) / gap ({gap_n}) 분류 | catalog {catalog_n} / gap {gap_n} |")
    P("")

    P("## 3. Candidate Policy Draft (전력공학 D-3) — NOT OFFICIAL\n")
    P(f"본 candidate policy는 **draft only** — 본 D-3 preview script 내부 hardcoded.\n")
    P(f"공식 ITEM_POLICY 승격은 본 preview 결과 후 **별 사용자 게이트 결정 영역**.\n")
    P("| slot | item | candidate keywords (narrow + evidence-grounded) | dl | matched count |")
    P("|---|---|---|---|---:|")
    for (sub, slot, item), policy in CANDIDATE_POWER_POLICY.items():
        kws = ", ".join(policy["keywords"][:3]) + f" ... (총 {len(policy['keywords'])}개)"
        dl_short = "✓" if policy["dl"] else "null (정직)"
        n = slot_item_dist.get((slot, item), 0)
        P(f"| {slot} | {item} | {kws} | {dl_short} | {n} |")
    P("")
    P(f"**총 candidate**: {len(CANDIDATE_POWER_POLICY)} item × {len(set(s for _,s,_ in CANDIDATE_POWER_POLICY.keys()))} slot.\n")

    P("## 4. Slot/Item 매칭 분포 상세\n")
    P("| slot | item | matched | CLEAN | NEEDS_REVIEW | SUSPECT | EXCLUDE_LOW |")
    P("|---|---|---:|---:|---:|---:|---:|")
    for (slot, item), n in sorted(slot_item_dist.items(), key=lambda x: (-x[1], x[0])):
        entries = [m for m in matched if m["slot"] == slot and m["item"] == item]
        c = sum(1 for e in entries if e["status"] == "CLEAN")
        nr = sum(1 for e in entries if e["status"] == "NEEDS_REVIEW")
        s = sum(1 for e in entries if e["status"] == "SUSPECT")
        el = sum(1 for e in entries if e["status"] == "EXCLUDE_LOW")
        P(f"| {slot} | {item} | {n} | {c} | {nr} | {s} | {el} |")
    P("")

    P("## 5. CLEAN 후보 수\n")
    P(f"- **CLEAN: {clean} entries** ({clean/total*100:.1f}% of 242)")
    P(f"- CLEAN + dl 부착: **{clean_with_dl}** entries ({clean_with_dl/total*100:.1f}% of 242) — D-3 selector 진입 시 main 후보")
    P("")

    P("## 6. Catalog / Gap 분포\n")
    P("| 영역 | count | 정의 |")
    P("|---|---:|---|")
    P(f"| **catalog (NEEDS_REVIEW tag-only)** | {needs_review} | tag evidence만, 본 D-3 main 미반영 |")
    P(f"| **gap (SUSPECT)** | {suspect} | score 10-14, evidence 약함, main 미반영 |")
    P(f"| **gap (EXCLUDE_LOW)** | {exclude_low} | score < 10, main 미반영 |")
    P(f"| **gap (unmatched — candidate policy 미매칭)** | {unmatched_n} | candidate policy 어떤 keyword에도 미매칭 |")
    P(f"| **합계 catalog + gap** | **{catalog_n + gap_n}** | gold sample baseline 정합 (영구 제외 X) |")
    P("")

    P("## 7. Broad Keyword 0 정합 검증\n")
    P(f"- broad keyword hit: **{broad_hits}** {'✓' if broad_hits == 0 else '✗'}")
    P(f"- BLACKLIST 9 항목: {', '.join(sorted(BROAD_KEYWORD_BLACKLIST))}")
    P("")
    if broad_hits > 0:
        P("**위반 entry 영역 명시 필요** — 정책 조정 단계 진입.\n")
    else:
        P("**broad keyword 정책 정합 ✓** — candidate keywords 모두 narrow + evidence-grounded.\n")

    P("## 8. Unmatched 분포 분석\n")
    if unmatched:
        unmatched_tags = Counter()
        for u in unmatched:
            tag = u.get("tag", "?")
            unmatched_tags[tag[:50]] += 1
        P(f"- unmatched 합계: **{unmatched_n}** ({unmatched_n/total*100:.1f}% of 242)")
        P("\n### 8.1 unmatched top 10 tag 패턴 (사전 신설 영역 후보)\n")
        P("| tag | count |")
        P("|---|---:|")
        for tag, n in unmatched_tags.most_common(10):
            P(f"| {tag if tag else '(empty)'} | {n} |")
        P("\n→ 본 unmatched 영역은 candidate policy 사전 확장 후보 (별 사용자 게이트).")
    P("")

    P("## 9. D-3 ITEM_POLICY 공식 승격 영역 (아직 0)\n")
    P("- 본 preview는 **draft only** — 공식 ITEM_POLICY 승격 0")
    P("- D-3 selector 작성 0 / D-3 input 생성 0 / D-3 generation 0 / D-3 audit 0")
    P("- 공식 승격은 다음 영역 결정 후만 가능:")
    P("  - candidate policy 검증 (slot/item 정합성 + keyword narrow 검증)")
    P("  - 사용자 명시 D-3 ITEM_POLICY 승격 결정")
    P("  - D-3 slot definition gate record 작성")
    P("")

    P("## 10. D-3 candidate policy draft가 D-2와 어떻게 다른가\n")
    P("| 차원 | D-2 (회로+제어) | D-3 (전력공학 draft) |")
    P("|---|---|---|")
    P("| slot 수 | 5 (회로_D15 + 회로_함정2 + 제어_안정전달8 + 제어_시간주파수5 + 제어_블록2) | 6 (전력_송배전D + 보호고장S + 안정도D + 변환본질4 + 함정S + 설비고장) |")
    P("| item 수 | 20 (P1 slice 검증) | 17 (draft, 미검증) |")
    P("| 정책 status | 공식 ITEM_POLICY (P1 slice 검증 완료) | **draft only** (preview-only) |")
    P("| ds_class 영역 | 모두 D/Dynamic (회로_함정2 dl=null 정직) | D + S/Fault + S/Conversion + S/Static 혼재 |")
    P("| evidence 기반 | P1 slice 28 sample 검증 정합 | 본 D-3 preview 측정 결과로 평가 |")
    P("| broad keyword 위험 | 회피 검증됨 (P1 slice 0건 broad) | 본 preview 측정 결과로 평가 |")
    P("| 전체 풀 | 277 (회로 110 + 제어 167) | 242 (전력공학) |")
    P("")

    P("## 11. 보호 영역\n")
    P("| 보호 대상 | 상태 |")
    P("|---|---|")
    P("| app/data/questions.json | read-only ✓ |")
    P("| v_full handoff scope (1,003 + 1,003 + audit + promotion + handoff) | read-only ✓ |")
    P("| **v_next D-2 sealed assets** (v_next_inputs/ + v_next_results_d2/ + D-2 scripts 5 + D-2 policy records 8) | **read-only ✓** |")
    P("| 기존 v1/v2/v2_v2/v3_canary/P1 inputs/results | 미수정 ✓ |")
    P("| v3_policy / 기존 scripts (v_next_d2_*, v_full_*, generator/parser) | 미수정 ✓ |")
    P("| `scripts/v_next_d2_pre_preview.py` | **미수정** (D-2 sealed asset, logic만 import) ✓ |")
    P("| decision JSONL / MEMORY.md / Obsidian | 미수정 ✓ |")
    P("| D-3 selector / input / generation / audit | 0 ✓ |")
    P("| D-3 ITEM_POLICY 공식 승격 | 0 ✓ (draft only) |")
    P("| reuse tranche | 0 ✓ |")
    P("| commit | 0 ✓ |")
    P("| 본 D-3 preview write | script 1 + report 1 |")
    P("")

    # ===== 최종 판정 =====
    broad_ok = broad_hits == 0
    match_rate = matched_n / total if total else 0
    clean_rate_matched = clean / matched_n if matched_n else 0
    has_clean = clean > 0

    P("## 12. 최종 판정\n")

    if not broad_ok:
        P("**판정: NEEDS_D3_POLICY_ADJUSTMENT**\n")
        P("근거: broad keyword 위반 — candidate policy keyword narrow 검증 필요")
        verdict = "NEEDS_D3_POLICY_ADJUSTMENT"
    elif matched_n == 0 or clean == 0:
        P("**판정: D3_GAP_ONLY**\n")
        P("근거: CLEAN entry 0 — 전력공학 영역 enrichment 영역 가용 0, catalog/gap만")
        verdict = "D3_GAP_ONLY"
    elif clean < 10:
        P(f"**판정: D3_GAP_ONLY (보수)** (CLEAN {clean} 작음)\n")
        P(f"근거: CLEAN {clean} 작음 — 전력공학 candidate policy 효과 매우 약함, slot definition 보강 필요")
        verdict = "D3_GAP_ONLY"
    else:
        # CLEAN > 0 + broad 0 → 두 분기 가능:
        # READY_FOR_D3_SLOT_DEFINITION_GATE (공식 정책 승격 단계)
        # READY_FOR_D3_SELECTOR_DESIGN_WITH_CLEAN_N (selector 진입 단계)
        # 본 채널은 사용자 정책 정합 (draft → 공식 ITEM_POLICY 승격은 별 게이트) — SLOT_DEFINITION_GATE 권장
        P(f"**판정: READY_FOR_D3_SLOT_DEFINITION_GATE ✓**\n")
        P("근거:")
        P(f"- ✓ broad keyword 0 ({broad_hits}건)")
        P(f"- ✓ candidate policy draft가 {matched_n} / {total} entry 매칭 ({match_rate*100:.1f}% match rate)")
        P(f"- ✓ CLEAN **{clean} entries** 측정 (CLEAN + dl 부착 {clean_with_dl}건 = D-3 main 후보)")
        P(f"- ✓ catalog {catalog_n} + gap {gap_n} 분리 (gold sample baseline 정합)")
        P(f"- ✓ unmatched {unmatched_n}건은 별 사전 확장 게이트 영역")
        P("")
        P("**다음 권장 단계 (사용자 명시 게이트)**:")
        P("- (1) candidate policy draft 검토 + 공식 D-3 ITEM_POLICY 승격 record 작성")
        P("- (2) 승격 후 D-3 selector design (CLEAN N main 정합) 진입")
        P("- (3) D-3 selector script 작성")
        P("- (4) D-3 input creation + parser validation")
        P("- (5) D-3 generation + paired audit")
        P("")
        P("**대안 분기 (사용자 결정)**:")
        P(f"- READY_FOR_D3_SELECTOR_DESIGN_WITH_CLEAN_{clean} — draft를 그대로 selector 진입 (공식 승격 단계 생략)")
        verdict = "READY_FOR_D3_SLOT_DEFINITION_GATE"

    P("")
    P("아직:")
    P("- D-3 ITEM_POLICY 공식 승격 0")
    P("- D-3 selector / input / generation / audit 0")
    P("- D-4 (기기 + 설비) 진입 결정 0")
    P("- catalog / gap 회수 / SUSPECT promotion / keyword expansion 모두 별 게이트")
    P("- reuse tranche / commit 모두 별 게이트\n")

    P("---")
    P("End of D-3 전력공학 preview report.")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(L) + "\n", encoding="utf-8")

    # console summary
    print(f"=== v_next D-3 전력공학 preview completed ===")
    print(f"target pool (전력공학): {total}")
    print(f"matched (candidate draft): {matched_n} / {total} ({match_rate*100:.1f}%)")
    print(f"unmatched: {unmatched_n}")
    print(f"CLEAN: {clean} / NEEDS_REVIEW (catalog): {needs_review} / SUSPECT: {suspect} / EXCLUDE_LOW: {exclude_low}")
    print(f"catalog: {catalog_n} / gap (SUSPECT + EXCLUDE_LOW + unmatched): {gap_n}")
    print(f"dl_attached: {dl_attached} / essence: {essence_attached} / trap: {trap_attached}")
    print(f"evidence_field: both {ev_dist.get('both',0)} / qt {ev_dist.get('question_text',0)} / sol {ev_dist.get('solution',0)} / tag {ev_dist.get('tag',0)}")
    print(f"broad keyword hits: {broad_hits}")
    print(f"expected expansion non-zero (CLEAN + dl): {clean_with_dl}")
    print(f"candidate slots: {len(set(s for _,s,_ in CANDIDATE_POWER_POLICY.keys()))} / items: {len(CANDIDATE_POWER_POLICY)}")
    print(f"report written: {REPORT_PATH}")
    print(f"=> {verdict}")
    if verdict == "READY_FOR_D3_SLOT_DEFINITION_GATE":
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
