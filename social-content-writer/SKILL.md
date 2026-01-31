---
name: social-content-writer
description: 智能社交媒體內容創作技能，支持資料收集、勾子生成、內容創作、圖片/影片提示詞生成、平台適配和多平台發布。支援 Facebook、Instagram、LinkedIn、Threads 等平台，自動生成吸引人的勾子和高品質內容，並提供圖片和影片 AI 生成提示詞。
metadata:
  category: content-creation
  type: automation
  languages:
    - python
---

# Social Content Writer - 社交媒體內容作家

智能的社交媒體內容創作技能，能夠自動收集資料、生成吸引人的勾子、創作高價值內容，並適配多個社交平台發布。

## 核心功能

1. **📚 資料收集** - 從多個來源收集相關資料
2. **✨ 勾子生成** - 生成5種類型的吸引人開頭
3. **✍️ 內容創作** - 基於框架生成高品質內容
4. **🖼️ 圖片/影片提示詞生成** - 為內容生成專業精準的圖片和影片提示詞
5. **🎯 平台適配** - 自動調整內容以符合各平台規則
6. **🚀 多平台發布** - 一鍵發布到 Facebook、Instagram、LinkedIn 等
7. **📊 效果分析** - 分析內容質量並提供改進建議

## 支援平台

- Facebook
- Instagram
- LinkedIn
- Threads
- YouTube (coming soon)
- TikTok (coming soon)

## 依賴技能

- `universal-image-gen` - 圖片生成
- `nanobanana-allapi` - 圖片生成備選方案
- `pix2-upload` - 圖床上傳
- `facebook-page-post` - Facebook 發布
- `mysql` - 資料存儲
- `discord-webchannel` - Discord 通知

## 快速開始

### 安裝依賴

```bash
pip install -r .claude/skills/social-content-writer/requirements.txt
```

### 基礎使用

```bash
# 生成內容
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "AI內容創作趨勢" \
  --platform facebook \
  --framework aida
```

### 完整工作流

```bash
# 從主題到發布（一步到位）
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "2025年社交媒體趨勢" \
  --platforms facebook,instagram,linkedin \
  --tone professional \
  --framework pas \
  --generate-prompts \
  --auto-generate-images \
  --auto-publish
```

## 腳本說明

### 1. collect.py - 資料收集

從多個來源收集相關資料並評分。

```bash
python3 .claude/skills/social-content-writer/scripts/collect.py \
  --topic "AI內容創作" \
  --sources web_search,youtube \
  --max-results 20 \
  --output research_data.json
```

**選項**：
- `--topic` - 研究主題
- `--sources` - 資料來源 (web_search, youtube, database)
- `--max-results` - 最大結果數量
- `--min-score` - 最小質量分數 (0-1, 預設 0.6)
- `--output` - 輸出檔案路徑

### 2. hook-generator.py - 勾子生成

生成多種類型的吸引人勾子。

```bash
python3 .claude/skills/social-content-writer/scripts/hook-generator.py \
  --topic "AI內容創作" \
  --platform facebook \
  --num-hooks 10 \
  --select-best
```

**勾子類型**：
- `question` - 提問式勾子
- `story` - 故事式勾子
- `number` - 數字式勾子
- `curiosity` - 好奇心勾子
- `controversial` - 爭議式勾子

**選項**：
- `--topic` - 主題
- `--platform` - 目標平台
- `--num-hooks` - 生成數量
- `--types` - 勾子類型 (逗號分隔)
- `--select-best` - 只輸出最佳勾子

### 3. write-content.py - 內容生成

主內容生成腳本，支援多平台、多框架。

```bash
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "AI改變內容創作" \
  --hook "你是否想知道AI如何改變內容創作？" \
  --platform facebook \
  --framework pas \
  --tone professional
```

**內容框架**：
- `aida` - Attention → Interest → Desire → Action
- `pas` - Problem → Agitation → Solution
- `story` - 故事敘述框架
- `listicle` - 清單式框架
- `tutorial` - 教程式框架

**選項**：
- `--topic` - 主題
- `--hook` - 勾子文字
- `--platform` - 目標平台
- `--framework` - 內容框架
- `--tone` - 語調 (professional, casual, friendly, authoritative)
- `--value-type` - 價值類型 (educational, inspirational, entertaining, informational)
- `--hashtags` - 標籤數量
- `--output` - 輸出檔案

**整合功能**：
- `--generate-prompts` - 同時生成圖片提示詞
- `--auto-generate-images` - 自動生成圖片
- `--auto-publish` - 自動發布
- `--save-db` - 保存到資料庫

### 4. prompt-generator.py - 圖片/影片提示詞生成 ⭐

為內容生成專業的 AI 圖片/影片生成提示詞。

```bash
# 生成圖片提示詞
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "文章內容或 content.json" \
  --type image \
  --styles realistic,3d-render \
  --platform instagram

# 生成圖片提示詞並自動生成圖片
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "文章內容" \
  --type image \
  --auto-generate \
  --upload-pix2

# 生成影片提示詞
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "文章內容" \
  --type video \
  --duration 30 \
  --style cinematic
```

**選項**：
- `--content` - 文章內容或 JSON 檔案路徑
- `--type` - 提示詞類型 (image, video, thumbnail)
- `--styles` - 圖片風格 (realistic, illustration, 3d-render, minimalist, cyberpunk, etc.)
- `--platform` - 目標平台
- `--num-prompts` - 生成提示詞數量
- `--auto-generate` - 自動生成圖片
- `--provider` - 圖片生成服務 (antigravity, nanobanana)
- `--upload-pix2` - 上傳到 Pix2 圖床
- `--duration` - 影片時長（秒）
- `--resolution` - 解析度 (1080p, 4K)
- `--aspect-ratio` - 寬高比

### 5. platform-adapter.py - 平台適配

將內容適配到不同平台的規則和格式。

```bash
python3 .claude/skills/social-content-writer/scripts/platform-adapter.py \
  --input content.json \
  --target-platforms facebook,instagram,linkedin \
  --output adapted_content.json
```

**選項**：
- `--input` - 輸入內容檔案
- `--target-platforms` - 目標平台（逗號分隔）
- `--output` - 輸出檔案
- `--adjust-length` - 自動調整長度
- `--optimize-hashtags` - 優化標籤

### 6. publish.py - 多平台發布

發布內容到多個平台。

```bash
python3 .claude/skills/social-content-writer/scripts/publish.py \
  --content content.json \
  --platforms facebook,instagram \
  --schedule "2025-01-30 09:00"
```

**選項**：
- `--content` - 內容檔案路徑
- `--platforms` - 發布平台
- `--schedule` - 排程發布時間
- `--notify-discord` - 發送 Discord 通知
- `--save-history` - 保存到資料庫

### 7. facebook-token-helper.py - Facebook Token 管理 ⭐

**重要**：資料庫中的 Token **可以直接發文**（與 n8n 系統一致）。

此腳本用於：
1. 從資料庫讀取 Token 並直接發文（預設，與 n8n 一致）
2. 可選：換取 Page Token 發文（如果直接發文失敗時）
3. **資料庫保持不變**

**工作流程**：
```
資料庫 (Token)
    ↓
直接發文到 Facebook（預設）
    ↓
完成（資料庫不變）
```

**使用方式**：

```bash
# 方式 1：從資料庫讀取並發文（推薦，配合 n8n 系統）
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post-from-db \
  --channel-id 1 \
  --message "Hello World!" \
  --photo-url "https://i.pix2.io/xxx.png"

# 方式 2：手動指定 Token 並直接發文（預設）
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post \
  --page-id 858773663997089 \
  --user-token "TOKEN" \
  --message "Hello World!" \
  --photo-url "https://example.com/image.jpg"

# 方式 3：先換取 Page Token 再發文（如果直接發文失敗）
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post \
  --page-id 858773663997089 \
  --user-token "TOKEN" \
  --message "Hello World!" \
  --use-page-token

# 方式 4：只換取 Page Token（不發文）
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action get-page-token \
  --page-id 858773663997089 \
  --user-token "TOKEN"

# 方式 5：驗證 Token 類型和有效性
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action verify \
  --token "TOKEN_TO_VERIFY"
```

**動作選項**：
- `post-from-db` - 從資料庫讀取並發文（推薦）
- `post` - 發布貼文到 Facebook
- `get-page-token` - 換取 Page Token
- `verify` - 驗證 Token 類型和有效性

**參數說明**：
- `--direct-use-token` - 直接使用 Token 發文（預設，與 n8n 一致）
- `--use-page-token` - 先換取 Page Token 再發文（可選）

**重要說明**：
- ✅ 資料庫中的 Token **可以直接發文**（n8n 系統每天這樣做）
- ✅ 預設直接使用 Token，不換取 Page Token
- ✅ 適用於 n8n 自動化系統
- ✅ 不會影響現有的工作流程

### 8. analyze.py - 內容分析

分析內容質量並提供改進建議。

```bash
python3 .claude/skills/social-content-writer/scripts/analyze.py \
  --content content.txt \
  --platform facebook
```

**選項**：
- `--content` - 內容檔案路徑
- `--platform` - 目標平台
- `--detailed` - 詳細分析報告

## 平台規則

| 平台 | 字數限制 | 最佳長度 | 最佳標籤數 | 內容類型 |
|------|---------|---------|-----------|---------|
| Facebook | 60,000 | 40-80 | 3-5 | 長篇內容 |
| Instagram | 2,200 | 138-150 | 20-30 | 視覺導向 |
| Threads | 500 | 100-200 | 3-5 | 對話式 |
| LinkedIn | 3,000 | 1,000-1,500 | 3-5 | 專業內容 |

## 環境變數

```bash
# OpenAI API (用於勾子和內容生成)
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_API_BASE="https://api.openai.com/v1"  # 可選

# MySQL (用於存儲歷史和規則)
export MYSQL_HOST="192.168.1.159"
export MYSQL_USER="n8n"
export MYSQL_PASSWORD="your-password"
export MYSQL_DATABASE="infoCollection"

# Facebook (用於發布)
export FACEBOOK_PAGE_ID="your-page-id"
# 注意：資料庫中的 access_token 可以直接發文
# 使用 facebook-token-helper.py 與 n8n 系統一致
# 不會更新資料庫中的 token

# Discord (用於通知)
export DISCORD_WEBHOOK_URL="your-webhook-url"

# 圖片生成
export ANTIGRAVITY_API_KEY="your-antigravity-key"
export ALLAPI_KEY="your-allapi-key"
export PIX2_API_KEY="your-pix2-key"
```

## 範例

### 完整工作流範例

```bash
# 1. 收集資料
python3 .claude/skills/social-content-writer/scripts/collect.py \
  --topic "2025社交媒體趨勢" \
  --max-results 15

# 2. 生成勾子
python3 .claude/skills/social-content-writer/scripts/hook-generator.py \
  --topic "2025社交媒體趨勢" \
  --num-hooks 10

# 3. 生成內容
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "2025社交媒體趨勢" \
  --hook "為什麼有些內容總能病毒傳播？2025年的秘密揭曉" \
  --platform facebook \
  --framework pas \
  --output my_content.json

# 4. 生成圖片提示詞
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content my_content.json \
  --type image \
  --auto-generate \
  --upload-pix2

# 5. 適配多平台
python3 .claude/skills/social-content-writer/scripts/platform-adapter.py \
  --input my_content.json \
  --target-platforms instagram,linkedin

# 6. 發布
python3 .claude/skills/social-content-writer/scripts/publish.py \
  --content my_content.json \
  --platforms facebook,instagram
```

### 一步到位範例

```bash
# 從主題直接到發布（包含圖片生成）
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "AI如何革命性地改變內容創作產業" \
  --platforms facebook,instagram,linkedin \
  --framework aida \
  --tone professional \
  --generate-prompts \
  --auto-generate-images \
  --auto-publish \
  --notify-discord
```

## 輸出格式

所有腳本輸出 JSON 格式，包含以下欄位：

```json
{
  "topic": "主題",
  "hook": "勾子",
  "content": "完整內容",
  "platform": "平台",
  "hashtags": ["標籤1", "標籤2"],
  "metadata": {
    "framework": "aida",
    "tone": "professional",
    "word_count": 500,
    "reading_time": "2分鐘"
  },
  "prompts": {
    "image": [
      {
        "prompt": "圖片提示詞",
        "style": "realistic",
        "aspect_ratio": "16:9"
      }
    ]
  }
}
```

## 技術架構

- **AI 模型**: OpenAI GPT-4o-mini (性價比高)
- **資料來源**: Web Search, YouTube API, MySQL
- **圖片生成**: Antigravity API, NanoBanana API
- **平台發布**: Facebook Graph API (User Token → Page Token 換取)
- **資料存儲**: MySQL

## Facebook Token 管理

**User Token vs Page Token**：

| 類型 | 來源 | 用途 | 儲存位置 | 有效期 |
|------|------|------|----------|--------|
| User Token | Graph API Explorer | 換取 Page Token | 資料庫 | 長期（60天或永久） |
| Page Token | 從 User Token 換取 | 發布貼文 | 臨時使用 | 臨時（每次換取） |

**換取流程**：
1. 資料庫存儲 User Token（不更新）
2. 發文時用 User Token 換取 Page Token
3. 使用 Page Token 發布貼文
4. Page Token 不存回資料庫

**為什麼這樣設計**？
- ✅ User Token 長期有效，不會過期
- ✅ Page Token 可能過期，但可以隨時重新換取
- ✅ 不會影響 n8n 系統的運作
- ✅ 安全性更高（Page Token 只臨時使用）

## 擴展性

- 支援添加新平台（修改平台規則配置）
- 支援自定義勾子模板
- 支援自定義內容框架
- 支援多語言擴展

## 常見問題

**Q: 如何提高內容質量？**
A: 使用 `analyze.py` 分析現有內容，根據建議改進。調整 AI temperature 參數（較低值更一致）。

**Q: 支援哪些語言？**
A: 目前主要支援繁體中文和簡體中文。英文支援開發中。

**Q: 如何添加新平台？**
A: 在 `platform-adapter.py` 中添加平台規則，並實現對應的發布邏輯。

**Q: 圖片生成失敗怎麼辦？**
A: 腳本會自動嘗試備選服務。檢查 API keys 是否正確配置。

**Q: Facebook 發文失敗，顯示權限不足？**
A: 資料庫中的 Token 應該可以直接發文（與 n8n 系統一致）。如果失敗：

```bash
# 先嘗試直接發文（預設）
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post-from-db \
  --channel-id 1 \
  --message "你的內容" \
  --photo-url "圖片URL"

# 如果直接發文失敗，再嘗試換取 Page Token
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post-from-db \
  --channel-id 1 \
  --message "你的內容" \
  --photo-url "圖片URL" \
  --use-page-token
```

**Q: 資料庫的 Token 可以直接發文嗎？**
A: 可以！n8n 系統每天都在使用資料庫的 Token 直接發文。預設情況下，`facebook-token-helper.py` 也直接使用 Token 發文，與 n8n 系統一致。

**Q: 更新資料庫的 Token 會影響 n8n 系統嗎？**
A: 會！所以 `facebook-token-helper.py` **不會更新資料庫**，只讀取 Token 使用。

## 授權

MIT License
