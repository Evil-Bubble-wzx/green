#!/bin/bash
# =========================================================================
# 绿色算力决策平台 — 服务器一键部署脚本
# 在宝塔终端中执行:  bash deploy/setup.sh
# =========================================================================
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo ""
echo "============================================"
echo -e "  ${GREEN}🌿 绿色算力决策平台 — 部署开始${NC}"
echo "============================================"
echo "  项目目录: $PROJECT_DIR"
echo ""

# ---- 检查 .env ----
echo -e "${YELLOW}[1/5] 检查 .env 配置...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "  ${RED}⚠️  请先编辑 .env 文件，修改数据库密码后重新运行此脚本${NC}"
    exit 1
fi
echo "  ✅ .env 已就绪"

# ---- 检查 PostgreSQL ----
echo -e "${YELLOW}[2/5] 检查数据库连接...${NC}"
source .env 2>/dev/null || true
DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\(.*\):.*/\1/p')
DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\(.*\)$/\1/p')

if command -v pg_isready &> /dev/null; then
    pg_isready -h $DB_HOST -p $DB_PORT
    echo "  ✅ 数据库连接正常"
else
    echo "  ⚠️  pg_isready 不可用，跳过检测（请确保 PostgreSQL 已启动）"
fi

# ---- 导入数据库 ----
echo -e "${YELLOW}[3/5] 导入数据库表结构和数据...${NC}"

# 检查表是否已存在
TABLE_COUNT=$(psql -U postgres -d $DB_NAME -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null || echo "0")
TABLE_COUNT=$(echo $TABLE_COUNT | xargs)

if [ "$TABLE_COUNT" -gt "30" ]; then
    echo "  ✅ 数据库已有 $TABLE_COUNT 张表，跳过导入"
else
    echo "  正在创建表结构..."
    psql -U postgres -d $DB_NAME -f backend/db/schema.sql
    echo "  ✅ 表结构创建完成"
    echo "  正在导入 Excel 数据..."
    pip3 install -r requirements.txt -q
    python3 backend/importers/import_excel_to_db.py
    echo "  ✅ 数据导入完成"
fi

# ---- 安装 Python 依赖 ----
echo -e "${YELLOW}[4/5] 安装 Python 依赖...${NC}"
pip3 install -r requirements.txt -q
echo "  ✅ Python 依赖已安装"

# ---- 构建前端 ----
echo -e "${YELLOW}[5/5] 构建前端（约 1-2 分钟）...${NC}"
cd "$PROJECT_DIR/frontend"

# 生成 .env.local（Next.js 用）
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_BASE_URL=
NEXT_PUBLIC_USE_MOCK=false
EOF

npm install --silent
npm run build
cd "$PROJECT_DIR"
echo "  ✅ 前端构建完成"

# ---- 完成 ----
echo ""
echo "============================================"
echo -e "  ${GREEN}✅ 部署完成！接下来手动操作：${NC}"
echo "============================================"
echo ""
echo "  1. 宝塔 → 网站 → Python项目 → 添加："
echo "     启动命令: python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"
echo "     项目目录: $PROJECT_DIR"
echo ""
echo "  2. 宝塔 → 网站 → Node.js项目 → 添加："
echo "     启动命令: node .next/standalone/server.js"
echo "     项目目录: $PROJECT_DIR/frontend"
echo "     端口: 3000"
echo ""
echo "  3. 宝塔 → 网站 → 你的站点 → 配置文件"
echo "     用 deploy/nginx.conf 的内容替换"
echo ""
echo "  完成后访问 http://你的IP 即可"
echo "============================================"
