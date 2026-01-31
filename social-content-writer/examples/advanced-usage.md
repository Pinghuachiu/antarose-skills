# Advanced Usage Guide

## 高級使用指南

這個指南介紹 social-content-writer 技能的高級功能和最佳實踐。

## AI 輔助內容生成

### 配置 OpenAI API

首先設置環境變量：

```bash
export OPENAI_API_KEY="sk-your-openai-api-key"
export OPENAI_API_BASE="https://api.openai.com/v1"  # 可選，使用自定義端點
```

### 使用 AI 生成高質量勾子

```bash
python3 .claude/skills/social-content-writer/scripts/hook-generator.py \
  --topic "AI驅動的內容營銷策略" \
  --platform facebook \
  --num-hooks 15 \
  --use-ai
```

**優勢**：
- 更多樣化的勾子
- 更精準的語氣調整
- 平台特定的優化
- 更高的互動潛力

### 使用 AI 生成專業內容

```bash
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "企業數位轉型完整指南" \
  --hook "為什麼90%的數位轉型項目都失敗了？" \
  --platform linkedin \
  --framework pas \
  --tone authoritative \
  --value-type educational \
  --use-ai
```

**AI 生成內容特點**：
- 更深入的洞察
- 更好的結構組織
- 專業級寫作品質
- SEO 優化

## 完整工作流自動化

### 一鍵生成並發布

```bash
#!/bin/bash
# auto-publish.sh

TOPIC="$1"
PLATFORMS="facebook,instagram,linkedin"

echo "🚀 自動內容生成和發布流程"
echo "主題: $TOPIC"

# Step 1: 生成勾子
echo "1️⃣ 生成勾子..."
python3 .claude/skills/social-content-writer/scripts/hook-generator.py \
  --topic "$TOPIC" \
  --platform facebook \
  --num-hooks 10 \
  --output hooks.json

# Step 2: 選擇最佳勾子
BEST_HOOK=$(jq -r '.hooks[0].text' hooks.json)
echo "選擇的勾子: $BEST_HOOK"

# Step 3: 生成內容
echo "2️⃣ 生成內容..."
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "$TOPIC" \
  --hook "$BEST_HOOK" \
  --platforms $PLATFORMS \
  --framework aida \
  --use-ai \
  --output content.json

# Step 4: 生成圖片提示詞
echo "3️⃣ 生成圖片提示詞..."
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content content.json \
  --type image \
  --auto-generate \
  --upload-pix2

# Step 5: 分析內容
echo "4️⃣ 分析內容質量..."
python3 .claude/skills/social-content-writer/scripts/analyze.py \
  --content content.json \
  --platform facebook \
  --output analysis.json

# Step 6: 發布
echo "5️⃣ 發布到平台..."
python3 .claude/skills/social-content-writer/scripts/publish.py \
  --content content.json \
  --platforms $PLATFORMS \
  --notify-discord \
  --save-db

echo "✅ 完成！"
```

使用方式：
```bash
chmod +x auto-publish.sh
./auto-publish.sh "2025年AI營銷趨勢"
```

## 批量內容生產

### 生成一週內容

```bash
#!/bin/bash
# weekly-content.sh

TOPICS=(
  "周一:AI工具分享"
  "周二:效率提升技巧"
  "周三:案例研究分析"
  "周四:行業趨勢洞察"
  "周五:周末休閒內容"
)

PLATFORM="facebook"
FRAMEWORK="listicle"

for topic in "${TOPICS[@]}"; do
  # 提取主題名稱（移除前綴）
  clean_topic="${topic#*:}"

  echo "生成內容: $clean_topic"

  python3 .claude/skills/social-content-writer/scripts/write-content.py \
    --topic "$clean_topic" \
    --platform $PLATFORM \
    --framework $FRAMEWORK \
    --output "${clean_topic// /_}_content.json"
done

echo "✅ 一週內容生成完成！"
```

### 主題系列內容生成

```bash
#!/bin/bash
# series-generator.sh

SERIES_TITLE="從零到英雄：內容創作完整系列"
PARTS=(
  "part1:選題策略"
  "part2:勾子設計"
  "part3:內容框架"
  "part4:視覺呈現"
  "part5:發布推廣"
)

for part in "${PARTS[@]}"; do
  part_num="${part%:*}"
  part_title="${part#*:}"

  full_title="$SERIES_TITLE - $part_title"

  python3 .claude/skills/social-content-writer/scripts/write-content.py \
    --topic "$full_title" \
    --hook "【${part_num^^}】${part_title}：從零開始的完整指南" \
    --platform facebook \
    --framework tutorial \
    --use-ai \
    --output "${part_num}_${part_title// /_}.json"
done
```

## 內容質量優化

### A/B 測試不同勾子

```bash
#!/bin/bash
# ab-test-hooks.sh

TOPIC="電商轉化率優化"
PLATFORM="facebook"

# 生成多個勾子
python3 .claude/skills/social-content-writer/scripts/hook-generator.py \
  --topic "$TOPIC" \
  --platform $PLATFORM \
  --num-hooks 10 \
  --use-ai \
  --output hooks_ab.json

# 為每個勾子生成完整內容
jq -c '.hooks[]' hooks_ab.json | while read -r hook; do
  hook_text=$(echo "$hook" | jq -r '.text')
  hook_type=$(echo "$hook" | jq -r '.type')

  echo "生成 $hook_type 勾子的內容..."

  python3 .claude/skills/social-content-writer/scripts/write-content.py \
    --topic "$TOPIC" \
    --hook "$hook_text" \
    --platform $PLATFORM \
    --framework aida \
    --output "ab_test_${hook_type}_${hook_text:0:10}.json"
done
```

### 質量評分和改進循環

```bash
#!/bin/bash
# quality-improvement-loop.sh

CONTENT_FILE="draft_content.json"
PLATFORM="facebook"
MIN_SCORE=75

# 分析初稿
python3 .claude/skills/social-content-writer/scripts/analyze.py \
  --content "$CONTENT_FILE" \
  --platform $PLATFORM \
  --output analysis.json

# 獲取分數
SCORE=$(jq -r '.overall_score' analysis.json)

echo "當前質量分數: $SCORE"

if (( $(echo "$SCORE < $MIN_SCORE" | bc -l) )); then
  echo "⚠️  分數低於 $MIN_SCORE，需要改進"

  # 獲取改進建議
  SUGGESTIONS=$(jq -r '.suggestions[]' analysis.json)

  echo "改進建議："
  echo "$SUGGESTIONS"

  # 根據建議重新生成
  ORIGINAL_TOPIC=$(jq -r '.topic' "$CONTENT_FILE")

  python3 .claude/skills/social-content-writer/scripts/write-content.py \
    --topic "$ORIGINAL_TOPIC" \
    --platform $PLATFORM \
    --use-ai \
    --output "improved_${CONTENT_FILE}"

  echo "✅ 已生成改進版本"
else
  echo "✅ 內容質量符合標準"
fi
```

## 進階圖片/影片生成

### 批量生成多風格圖片

```bash
#!/bin/bash
# batch-image-generation.sh

CONTENT="你的內容描述"
STYLES=("realistic" "3d-render" "minimalist" "illustration" "cyberpunk")

for style in "${STYLES[@]}"; do
  echo "生成 $style 風格圖片..."

  python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
    --content "$CONTENT" \
    --type image \
    --styles "$style" \
    --auto-generate \
    --upload-pix2 \
    --output "prompt_${style}.json"
done

echo "✅ 所有風格圖片生成完成"
```

### 生成宣傳影片完整流程

```bash
#!/bin/bash
# video-production-pipeline.sh

TOPIC="產品發布宣傳"
DURATION=60  # 60秒宣傳片

# Step 1: 生成影片提示詞
echo "1️⃣ 生成影片提示詞..."
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "$TOPIC" \
  --type video \
  --duration $DURATION \
  --style cinematic \
  --use-ai \
  --output video_prompts.json

# Step 2: 生成影片縮圖
echo "2️⃣ 生成影片縮圖..."
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "$TOPIC" \
  --type image \
  --styles pop-art,cyberpunk \
  --auto-generate

# Step 3: 生成配套文字內容
echo "3️⃣ 生成配套文字..."
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "$TOPIC" \
  --platform youtube \
  --framework pas \
  --use-ai \
  --output video_description.json

echo "✅ 影片製作準備完成！"
echo "📝 請查看 video_prompts.json 並使用 Runway/Pika 生成影片"
```

## 平台特定高級技巧

### Facebook 算法優化

```bash
# 使用 PAS 框架（Facebook 算法喜歡問題-解決方案結構）
python3 write-content.py \
  --topic "產品教學" \
  --platform facebook \
  --framework pas \
  --tone friendly
```

**Facebook 算法提示**：
- 使用問題式勾子
- 包含清晰的 CTA
- 第一小時內回覆所有評論
- 避免過度推銷

### Instagram 算法優化

```bash
# 生成多個 Instagram 圖片變體
python3 prompt-generator.py \
  --content "旅行攝影" \
  --type image \
  --platform instagram \
  --styles realistic,3d-render,minimalist \
  --num-prompts 10
```

**Instagram 算法提示**：
- 使用 20-30 個精準標籤
- 在發布後 30 分鐘內互動
- 使用 Stories 增加曝光
- 保持一致的視覺風格

### LinkedIn 算法優化

```bash
# LinkedIn 需要長篇、專業內容
python3 write-content.py \
  --topic "行業洞察" \
  --platform linkedin \
  --framework listicle \
  --tone authoritative \
  --value-type educational \
  --hashtags 5
```

**LinkedIn 算法提示**：
- 文章長度 1,200-1,500 字
- 使用個人故事建立可信度
- 提供可執行的建議
- 在工作日早上發布

## 數據分析和改進

### 追蹤內容表現

```sql
-- 查看最近 30 天的內容統計
SELECT
    platform,
    COUNT(*) as total_posts,
    AVG(CHAR_LENGTH(content)) as avg_length,
    SUM(CASE WHEN status = 'published' THEN 1 ELSE 0 END) as published
FROM content_history
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY platform;
```

### 分析最佳勾子類型

```sql
-- 找出表現最好的勾子類型
SELECT
    JSON_EXTRACT(metadata, '$.hook_type') as hook_type,
    COUNT(*) as usage_count,
    AVG(JSON_EXTRACT(metadata, '$.effectiveness_score')) as avg_score
FROM content_history
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY JSON_EXTRACT(metadata, '$.hook_type')
ORDER BY avg_score DESC;
```

## 自定義擴展

### 添加新的勾子類型

編輯 `hook-generator.py`，在 `HOOK_TEMPLATES` 中添加：

```python
HOOK_TEMPLATES = {
    # ... 現有類型 ...
    "testimonial": {
        "templates": [
            "{person}說：{quote}",
            "客戶反饋：{result}"
        ],
        "examples": {
            "person": "用戶小王",
            "quote": "這個方法讓我的銷售提升了3倍！",
            "result": "使用後效果驚人"
        },
        "effectiveness": 0.87
    }
}
```

### 添加新的內容框架

編輯 `write-content.py`，在 `CONTENT_FRAMEWORKS` 中添加：

```python
CONTENT_FRAMEWORKS = {
    # ... 現有框架 ...
    "star": {
        "name": "STAR 方法",
        "sections": ["Situation", "Task", "Action", "Result"],
        "description": "情境-任務-行動-結果，適合案例研究"
    }
}
```

## 故障排除高級技巧

### API 速率限制處理

```python
# 在腳本中添加重試邏輯
import time
from openai import OpenAI

def call_openai_with_retry(client, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指數退避
                print(f"速率限制，等待 {wait_time} 秒...")
                time.sleep(wait_time)
            else:
                raise
```

### 內容去重

```bash
# 檢查是否已生成類似內容
python3 .claude/skills/social-content-writer/scripts/collect.py \
  --topic "你的主題" \
  --sources database \
  --max-results 5

# 如果發現相似內容，調整主題或角度
```

## 性能優化

### 並行生成多平台內容

```bash
#!/bin/bash
# parallel-generation.sh

TOPIC="你的主題"

# 使用後台進程並行生成
python3 write-content.py --topic "$TOPIC" --platform facebook \
  --output fb_content.json &
FB_PID=$!

python3 write-content.py --topic "$TOPIC" --platform instagram \
  --output ig_content.json &
IG_PID=$!

python3 write-content.py --topic "$TOPIC" --platform linkedin \
  --output li_content.json &
LI_PID=$!

# 等待所有進程完成
wait $FB_PID $IG_PID $LI_PID

echo "✅ 所有平台內容生成完成"
```

## 安全和隱私

### API Key 管理

```bash
# 使用 .env 文件（記得加入 .gitignore）
cat > .env << EOF
OPENAI_API_KEY=sk-your-key
FACEBOOK_ACCESS_TOKEN=your-token
DISCORD_WEBHOOK_URL=your-webhook
EOF

# 加載環境變量
export $(cat .env | xargs)
```

### 敏感信息過濾

```python
# 在發布前過濾敏感信息
SENSITIVE_PATTERNS = [
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
    r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
    r'\b\d{16}\b'  # Credit card
]

def sanitize_content(content):
    import re
    for pattern in SENSITIVE_PATTERNS:
        content = re.sub(pattern, '[REDACTED]', content)
    return content
```

## 最佳實踐總結

1. **始終分析目標平台規則**
2. **使用 AI + 模板混合方法**（AI 生成質量更高，模板更可靠）
3. **測試多個勾子變體**
4. **保持內容日曆一致性**
5. **追蹤並分析表現數據**
6. **定期更新勾子模板庫**
7. **批量生產但保持質量**
8. **自動化重複性任務**
9. **保護敏感信息和 API keys**
10. **持續優化和改進**
