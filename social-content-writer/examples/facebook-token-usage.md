# Facebook Token Helper 使用範例

## 概述

`facebook-token-helper.py` 是專門用於處理 Facebook Token 換取和發文的工具。

**核心概念**：
- 資料庫中存儲的是 **User Token**（長期有效）
- 發文需要使用 **Page Token**（從 User Token 換取）
- 換取的 Page Token **不會存回資料庫**
- 資料庫保持原樣，不影響 n8n 系統

## 工作流程

```
┌─────────────┐
│ 資料庫      │
│ User Token  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ 換取 Page Token │ (臨時)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ 發文到 Facebook │
└─────────────────┘
       │
       ▼
┌─────────────┐
│ 完成        │
│ (資料庫不變) │
└─────────────┘
```

## 使用範例

### 範例 1：從資料庫讀取並發文（推薦）

這是最推薦的方式，直接從資料庫讀取頻道設定並發文。

```bash
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post-from-db \
  --channel-id 1 \
  --message "📱 iPhone 18 Pro 搶先支援星鏈上網！

【這一次，iPhone 真的改變規則】

最新消息：Apple 正與 SpaceX 密會，要在 iPhone 18 Pro 上整合 Starlink 星鏈衛星上網！

深山露營完全沒訊號？海邊度假「無服務」？

iPhone 18 Pro + Starlink 讓這些問題全部解決！

✅ 完整 5G 上網
✅ 看影片、直播、玩遊戲
✅ 速度比現在快 20 倍
✅ 不需要任何額外硬體

#iPhone18Pro #Starlink #星鏈衛星" \
  --photo-url "https://i.pix2.io/5m6gGTpt.png"
```

**輸出**：
```
✅ 從資料庫讀取頻道 1 的設定
🔄 正在換取 Page Access Token...
✅ Page Token 換取成功
📝 正在發布貼文...
✅ 成功發布到 Facebook
貼文 ID: 858773663997089_122115733797158468
貼文連結: https://www.facebook.com/858773663997089/posts/122115733797158468
```

### 範例 2：只換取 Page Token

如果您需要獲取 Page Token 用於其他用途：

```bash
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action get-page-token \
  --page-id 858773663997089 \
  --user-token "EAApGx7JZC6KYBQ..."
```

**輸出**：
```
✅ 成功換取 Page Token
Page Token: EAApGx7JZC6KYBQqpgXvcPM2VCAZB...

💡 提示：請使用此 Page Token 進行後續的 API 呼叫
```

### 範例 3：手動指定 Token 並發文

如果您不想從資料庫讀取，可以直接指定參數：

```bash
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post \
  --page-id 858773663997089 \
  --user-token "EAApGx7JZC6KYBQ..." \
  --message "Hello World!" \
  --photo-url "https://example.com/image.jpg"
```

### 範例 4：驗證 Token 類型

檢查 Token 是 User Token 還是 Page Token：

```bash
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action verify \
  --token "EAApGx7JZC6KYBQ..."
```

**輸出**：
```
✅ Token 驗證成功
類型: USER
有效: True
權限: pages_manage_posts, pages_read_engagement, ...
```

### 範例 5：發布純文字貼文（無圖片）

```bash
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post-from-db \
  --channel-id 1 \
  --message "這是純文字貼文，沒有圖片"
```

### 範例 6：與 social-content-writer 整合

完整的內容創作和發布流程：

```bash
# 1. 生成內容
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "iPhone 18 Pro 支援 Starlink" \
  --platform facebook \
  --framework pas \
  --output content.json

# 2. 生成圖片提示詞並生成圖片
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content content.json \
  --type image \
  --auto-generate \
  --upload-pix2

# 3. 讀取生成的圖片 URL
IMAGE_URL=$(jq '.prompts.image[0].url' content.json)

# 4. 讀取生成的內容
MESSAGE=$(jq -r '.content' content.json)

# 5. 發布到 Facebook
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post-from-db \
  --channel-id 1 \
  --message "$MESSAGE" \
  --photo-url "$IMAGE_URL"
```

## 錯誤處理

### 錯誤 1：換取 Page Token 失敗

**症狀**：
```
❌ 換取失敗：API 請求失敗 (403): {"error": {...}}
```

**解決方案**：
1. 檢查 User Token 是否有效
2. 確認 User Token 有 `pages_manage_posts` 和 `pages_read_engagement` 權限
3. 確認 Page ID 正確

### 錯誤 2：發文失敗

**症狀**：
```
❌ 發布失敗：API 請求失敗 (200): {"error": {"message": "(#200) ..."}}
```

**解決方案**：
1. 確認已成功換取 Page Token
2. 檢查 Page Token 是否有足夠權限
3. 確認貼文內容符合 Facebook 規範

### 錯誤 3：資料庫連接失敗

**症狀**：
```
❌ 資料庫錯誤：Can't connect to MySQL server...
```

**解決方案**：
1. 檢查 MySQL 主機地址
2. 確認使用者名稱和密碼正確
3. 確認資料庫名稱正確

## 注意事項

1. **不要更新資料庫**
   - 資料庫中的 User Token 不應該被更新
   - 每次發文時臨時換取 Page Token 即可

2. **Token 安全性**
   - 不要在日誌或終端輸出中顯示完整 Token
   - Page Token 只臨時使用，不長期存儲

3. **n8n 系統相容性**
   - 此工具設計為不影響 n8n 系統
   - n8n 可以繼續使用資料庫中的 User Token

4. **速率限制**
   - Facebook 有 API 速率限制
   - 短時間大量發文可能被限制

5. **權限管理**
   - User Token 需要權限：`pages_manage_posts`, `pages_read_engagement`
   - Page Token 會繼承 User Token 的權限

## 進階用法

### 自動化腳本

創建一個 bash 腳本自動化整個流程：

```bash
#!/bin/bash
# auto-post.sh

CHANNEL_ID=1
TOPIC="$1"

# 生成內容
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "$TOPIC" \
  --platform facebook \
  --output /tmp/content.json

# 生成圖片
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content /tmp/content.json \
  --type image \
  --auto-generate \
  --upload-pix2

# 發布
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post-from-db \
  --channel-id $CHANNEL_ID \
  --message "$(jq -r '.content' /tmp/content.json)" \
  --photo-url "$(jq -r '.prompts.image[0].url' /tmp/content.json)"
```

使用方式：
```bash
bash auto-post.sh "iPhone 18 Pro 支援 Starlink"
```

## 總結

**重點**：
- ✅ 資料庫中的 User Token 不會被更新
- ✅ 每次發文時臨時換取 Page Token
- ✅ 適用於 n8n 自動化系統
- ✅ 不會影響現有工作流程

**推薦使用方式**：
```bash
python3 .claude/skills/social-content-writer/scripts/facebook-token-helper.py \
  --action post-from-db \
  --channel-id 1 \
  --message "你的內容" \
  --photo-url "圖片URL"
```
