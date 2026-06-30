#!/bin/bash
# ============================================================
# Green Compute System — 公网一键启动（生产模式）
# ============================================================
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

cleanup() {
    echo -e "\n${YELLOW}正在关闭...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $NGROK_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "已关闭。"
}
trap cleanup EXIT INT TERM

echo ""
echo "============================================================"
echo -e "  ${GREEN}🌿 Green Compute System — 公网模式${NC}"
echo "============================================================"
echo ""

# ---- 1. 后端（崩溃自动重启）----
echo "🔧 [1/4] 启动后端（崩溃自动重启）..."
cd "$PROJECT_DIR"
(
  while true; do
    python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --log-level warning
    echo "⚠️ 后端已停止，3秒后自动重启..."
    sleep 3
  done
) &
BACKEND_PID=$!
sleep 3
echo "   ✅ 后端就绪"

# ---- 2. 构建前端（生产模式）----
echo "🔧 [2/4] 构建前端（生产模式，约 30 秒）..."
cd "$PROJECT_DIR/frontend"
rm -rf .next

cat > .env.local << 'EOF'
NEXT_PUBLIC_API_BASE_URL=
NEXT_PUBLIC_USE_MOCK=false
EOF

npx next build > /tmp/next-build.log 2>&1
echo "   ✅ 构建完成"

# ---- 3. 启动前端 ----
echo "🔧 [3/4] 启动前端..."
npx next start --port 3000 --hostname 0.0.0.0 > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 3
echo "   ✅ 前端就绪"

# ---- 4. ngrok ----
echo "🌐 [4/4] 启动 ngrok..."
ngrok http 3000 --log=stdout --log-level=warn > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!
sleep 4

PUBLIC_URL=$(curl -s http://127.0.0.1:4040/api/tunnels 2>/dev/null | python3 -c "
import sys, json
for t in json.load(sys.stdin)['tunnels']:
    print(t['public_url']); break
" 2>/dev/null)

if [ -z "$PUBLIC_URL" ]; then
    sleep 2
    PUBLIC_URL=$(curl -s http://127.0.0.1:4040/api/tunnels 2>/dev/null | python3 -c "
import sys, json
print(json.load(sys.stdin)['tunnels'][0]['public_url'])
" 2>/dev/null)
fi

echo ""
echo "============================================================"
echo -e "  ${GREEN}✅ 公网可访问！${NC}"
echo "============================================================"
echo ""
echo -e "  👉 网页地址:"
echo -e "  ${CYAN}${PUBLIC_URL}${NC}"
echo ""
echo "  按 Ctrl+C 关闭所有服务"
echo "============================================================"
echo ""

wait
