#!/bin/bash
# Social Content Writer - Quick Start Script
# 快速開始腳本

set -e

# 顏色定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Social Content Writer - Quick Start            ║${NC}"
echo -e "${BLUE}║  社交媒體內容作家 - 快速開始                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 未安裝${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 已安裝${NC}"

# 檢查依賴
echo ""
echo -e "${BLUE}📦 檢查依賴...${NC}"

MISSING_DEPS=()

python3 -c "import requests" 2>/dev/null || MISSING_DEPS+=("requests")
python3 -c "import openai" 2>/dev/null || MISSING_DEPS+=("openai")
python3 -c "import dotenv" 2>/dev/null || MISSING_DEPS+=("python-dotenv")
python3 -c "import pandas" 2>/dev/null || MISSING_DEPS+=("pandas")
python3 -c "import mysql.connector" 2>/dev/null || MISSING_DEPS+=("mysql-connector-python")

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠️  缺少依賴: ${MISSING_DEPS[*]}${NC}"
    echo ""
    read -p "是否安裝缺少的依賴？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip3 install -r requirements.txt
    fi
else
    echo -e "${GREEN}✓ 所有依賴已安裝${NC}"
fi

# 檢查環境變量
echo ""
echo -e "${BLUE}🔑 檢查環境變量...${NC}"

check_env() {
    if [ -n "$2" ]; then
        echo -e "${GREEN}✓ $1${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  $1 未設置${NC}"
        return 1
    fi
}

MISSING_ENV=0

check_env "OPENAI_API_KEY" "$OPENAI_API_KEY" || MISSING_ENV=1
check_env "MYSQL_HOST" "$MYSQL_HOST" || MISSING_ENV=1
check_env "DISCORD_WEBHOOK_URL" "$DISCORD_WEBHOOK_URL" || true  # Optional

if [ $MISSING_ENV -eq 1 ]; then
    echo ""
    echo -e "${YELLOW}💡 建議設置以下環境變量：${NC}"
    echo "export OPENAI_API_KEY=\"sk-your-key\""
    echo "export MYSQL_HOST=\"192.168.1.159\""
    echo "export MYSQL_USER=\"n8n\""
    echo "export MYSQL_PASSWORD=\"your-password\""
    echo "export MYSQL_DATABASE=\"infoCollection\""
    echo ""
fi

# 詢問用戶想要做什麼
echo ""
echo -e "${BLUE}請選擇操作：${NC}"
echo "1. 快速生成內容"
echo "2. 生成勾子"
echo "3. 生成圖片提示詞"
echo "4. 分析內容"
echo "5. 查看平台資訊"
echo "6. 運行測試"
echo "7. 退出"
echo ""
read -p "請輸入選項 (1-7): " choice

case $choice in
    1)
        echo ""
        read -p "請輸入主題: " topic
        read -p "請輸入平台 (facebook/instagram/linkedin/threads): " platform
        echo ""
        echo -e "${BLUE}🚀 正在生成內容...${NC}"
        python3 .claude/skills/social-content-writer/scripts/write-content.py \
            --topic "$topic" \
            --platform "$platform" \
            --framework aida \
            --tone professional
        ;;
    2)
        echo ""
        read -p "請輸入主題: " topic
        read -p "請輸入平台 (facebook/instagram/linkedin/threads): " platform
        read -p "生成數量: " num_hooks
        num_hooks=${num_hooks:-5}
        echo ""
        echo -e "${BLUE}✨ 正在生成勾子...${NC}"
        python3 .claude/skills/social-content-writer/scripts/hook-generator.py \
            --topic "$topic" \
            --platform "$platform" \
            --num-hooks "$num_hooks"
        ;;
    3)
        echo ""
        read -p "請輸入內容描述: " content
        read -p "類型 (image/video): " type
        type=${type:-image}
        echo ""
        echo -e "${BLUE}🖼️  正在生成提示詞...${NC}"
        python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
            --content "$content" \
            --type "$type"
        ;;
    4)
        echo ""
        read -p "請輸入內容文件路徑 (或直接輸入內容): " content_input
        read -p "平台 (facebook/instagram/linkedin/threads): " platform
        echo ""
        echo -e "${BLUE}📊 正在分析內容...${NC}"
        python3 .claude/skills/social-content-writer/scripts/analyze.py \
            --content "$content_input" \
            --platform "$platform"
        ;;
    5)
        echo ""
        read -p "平台 (facebook/instagram/linkedin/threads): " platform
        echo ""
        python3 .claude/skills/social-content-writer/scripts/platform-adapter.py \
            --platform-info "$platform"
        ;;
    6)
        echo ""
        echo -e "${BLUE}🧪 運行測試...${NC}"
        bash .claude/skills/social-content-writer/scripts/test.sh
        ;;
    7)
        echo "再見！"
        exit 0
        ;;
    *)
        echo -e "${YELLOW}無效選項${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ 操作完成！${NC}"
echo ""
echo -e "${BLUE}📚 更多資源：${NC}"
echo "• 查看文檔: cat .claude/skills/social-content-writer/SKILL.md"
echo "• 基礎教程: cat .claude/skills/social-content-writer/examples/basic-workflow.md"
echo "• 高級用法: cat .claude/skills/social-content-writer/examples/advanced-usage.md"
