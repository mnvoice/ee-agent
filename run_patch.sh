#!/bin/bash
cd ~/Developer/ee-agent || { echo "❌ ee-agent 디렉토리 없음"; exit 1; }

if [ ! -f patch_figure.py ]; then
  echo "❌ patch_figure.py 없음. 먼저 생성 필요."
  exit 1
fi

TS=$(date +%Y%m%d_%H%M%S)
LOG="patch_apply_${TS}.log"

{
  echo "=== BEFORE === $(date)"
  python3 patch_figure.py --check
  echo ""
  echo "=== APPLY ==="
  python3 patch_figure.py
  echo ""
  echo "=== AFTER ==="
  python3 patch_figure.py --check
} 2>&1 | tee "$LOG"

echo ""
echo "📄 로그: $LOG"
echo ""
echo "=== 다음 ==="
echo "1. 사파리 ⌘+Option+R"
echo "2. 1998 2회 Q17 (15/1246)"
echo "3. figure 박스 6장 떴나?"
echo ""
echo "안 떴으면: python3 patch_figure.py --revert"
