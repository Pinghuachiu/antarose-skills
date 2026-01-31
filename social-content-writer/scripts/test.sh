#!/bin/bash
# Social Content Writer - Test Suite
# 測試腳本

set -e

# 顏色定義
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

# 測試函數
run_test() {
    local test_name=$1
    local test_command=$2

    echo -e "${BLUE}測試: $test_name${NC}"
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 通過${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ 失敗${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Social Content Writer - Test Suite             ║${NC}"
echo -e "${BLUE}║  測試套件                                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# 基礎測試
echo -e "${BLUE}═══ 基礎測試 ═══${NC}"

run_test "Python 可用性" "command -v python3"
run_test "腳本可執行權限" "test -x .claude/skills/social-content-writer/scripts/hook-generator.py"
run_test "SKILL.md 存在" "test -f .claude/skills/social-content-writer/SKILL.md"
run_test "requirements.txt 存在" "test -f .claude/skills/social-content-writer/requirements.txt"

echo ""

# 腳本語法測試
echo -e "${BLUE}═══ 腳本語法測試 ═══${NC}"

SCRIPTS=(
    "collect.py"
    "hook-generator.py"
    "write-content.py"
    "prompt-generator.py"
    "platform-adapter.py"
    "publish.py"
    "analyze.py"
)

for script in "${SCRIPTS[@]}"; do
    run_test "$script 語法" \
        "python3 -m py_compile .claude/skills/social-content-writer/scripts/$script"
done

echo ""

# 功能測試
echo -e "${BLUE}═══ 功能測試 ═══${NC}"

# 測試勾子生成
echo -e "${BLUE}測試: 勾子生成${NC}"
if python3 .claude/skills/social-content-writer/scripts/hook-generator.py \
    --topic "測試主題" \
    --platform facebook \
    --num-hooks 3 \
    --output /tmp/test_hooks.json > /dev/null 2>&1; then

    if [ -f "/tmp/test_hooks.json" ]; then
        echo -e "${GREEN}✓ 勾子生成通過${NC}"
        ((TESTS_PASSED++))

        # 驗證輸出
        if python3 -c "import json; data = json.load(open('/tmp/test_hooks.json')); assert 'hooks' in data; assert len(data['hooks']) == 3" 2>/dev/null; then
            echo -e "${GREEN}✓ 勾子格式正確${NC}"
            ((TESTS_PASSED++))
        else
            echo -e "${RED}✗ 勾子格式錯誤${NC}"
            ((TESTS_FAILED++))
        fi
    else
        echo -e "${RED}✗ 勾子文件未生成${NC}"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}✗ 勾子生成失敗${NC}"
    ((TESTS_FAILED++))
fi

# 測試內容生成
echo -e "${BLUE}測試: 內容生成${NC}"
if python3 .claude/skills/social-content-writer/scripts/write-content.py \
    --topic "測試內容" \
    --platform facebook \
    --framework pas \
    --output /tmp/test_content.json > /dev/null 2>&1; then

    if [ -f "/tmp/test_content.json" ]; then
        echo -e "${GREEN}✓ 內容生成通過${NC}"
        ((TESTS_PASSED++))

        # 驗證輸出
        if python3 -c "import json; data = json.load(open('/tmp/test_content.json')); assert 'content' in data; assert len(data['content']) > 0" 2>/dev/null; then
            echo -e "${GREEN}✓ 內容格式正確${NC}"
            ((TESTS_PASSED++))
        else
            echo -e "${RED}✗ 內容格式錯誤${NC}"
            ((TESTS_FAILED++))
        fi
    else
        echo -e "${RED}✗ 內容文件未生成${NC}"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}✗ 內容生成失敗${NC}"
    ((TESTS_FAILED++))
fi

# 測試提示詞生成
echo -e "${BLUE}測試: 提示詞生成${NC}"
if python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
    --content "測試圖片生成" \
    --type image \
    --num-prompts 2 \
    --output /tmp/test_prompts.json > /dev/null 2>&1; then

    if [ -f "/tmp/test_prompts.json" ]; then
        echo -e "${GREEN}✓ 提示詞生成通過${NC}"
        ((TESTS_PASSED++))

        # 驗證輸出
        if python3 -c "import json; data = json.load(open('/tmp/test_prompts.json')); assert 'prompts' in data or 'scenes' in data" 2>/dev/null; then
            echo -e "${GREEN}✓ 提示詞格式正確${NC}"
            ((TESTS_PASSED++))
        else
            echo -e "${RED}✗ 提示詞格式錯誤${NC}"
            ((TESTS_FAILED++))
        fi
    else
        echo -e "${RED}✗ 提示詞文件未生成${NC}"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}✗ 提示詞生成失敗${NC}"
    ((TESTS_FAILED++))
fi

# 測試平台適配
echo -e "${BLUE}測試: 平台適配${NC}"
if python3 .claude/skills/social-content-writer/scripts/platform-adapter.py \
    --platform-info facebook > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 平台資訊查詢通過${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ 平台資訊查詢失敗${NC}"
    ((TESTS_FAILED++))
fi

echo ""

# 總結
echo -e "${BLUE}═══ 測試總結 ═══${NC}"
TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
echo -e "總計: $TOTAL_TESTS 項測試"
echo -e "${GREEN}通過: $TESTS_PASSED${NC}"
echo -e "${RED}失敗: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✓ 所有測試通過！                               ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ✗ 部分測試失敗                                 ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════╝${NC}"
    exit 1
fi
