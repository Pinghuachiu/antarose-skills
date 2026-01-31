#!/bin/bash
# LinkedIn Post Demo Script

# 顏色定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   LinkedIn Post - Demo Script          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# 檢查是否設定了環境變數
if [ -z "$MYSQL_HOST" ] || [ -z "$MYSQL_USER" ] || [ -z "$MYSQL_PASSWORD" ]; then
    echo -e "${RED}❌ 資料庫環境變數未設定${NC}"
    echo "請設定: MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE"
    exit 1
fi

echo -e "${YELLOW}步驟 1: 取得 LinkedIn 使用者資訊${NC}"
echo "════════════════════════════════════════"
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action get-profile \
  --from-db \
  --channel-id 1

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ 成功取得使用者資訊${NC}"
else
    echo -e "\n${RED}❌ 取得使用者資訊失敗${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}步驟 2: 發布純文字貼文${NC}"
echo "════════════════════════════════════════"
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "Hello LinkedIn! 🚀

這是一條測試貼文，由 LinkedIn Post Script 自動發布。

#Automation #API #LinkedIn"

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ 純文字貼文發布成功${NC}"
else
    echo -e "\n${RED}❌ 純文字貼文發布失敗${NC}"
fi

echo ""
echo -e "${YELLOW}步驟 3: 發布連結貼文${NC}"
echo "════════════════════════════════════════"
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action link \
  --from-db \
  --channel-id 1 \
  --text "分享一個有用的資源 📚

Check out this amazing article about API development!

#Tech #Development #Learning" \
  --link-url "https://github.com/Pinghuachiu/antarose-skills" \
  --link-title "Antarose Skills - Claude Skills Repository" \
  --link-desc "A collection of reusable AI skills for Claude Code and other AI agents."

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ 連結貼文發布成功${NC}"
else
    echo -e "\n${RED}❌ 連結貼文發布失敗${NC}"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Demo 完成！${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
