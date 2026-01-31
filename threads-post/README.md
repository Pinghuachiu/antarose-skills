# Threads Post Skill - 完整指南

## 概述

這個技能讓你可以直接從資料庫發布貼文到 Threads（Meta 的社群媒體平台），支援：
- ✅ 純文字貼文（最多 500 字符）
- ✅ 圖片貼文（JPG、PNG、WEBP）
- ✅ 影片貼文（MP4、MOV）
- ✅ 自動取得 Instagram Business ID
- ✅ 無需換取 Page Token（與 Facebook 不同）

## 與 Facebook、Instagram 的主要差異

### Token 使用方式

**Facebook**：
```
資料庫 User Token → 換取 Page Token → 發文
```

**Instagram**：
```
資料庫 Token → 建立 Container → 等待 → 發布
```

**Threads**：
```
資料庫 Token → 直接發布（Container = 發布）
```

### 發布流程

**Facebook**：
```
直接 POST /{page-id}/feed 或 /{page-id}/photos
```

**Instagram**：
```
1. POST /{ig-id}/media （建立 Container）
2. POST /{ig-id}/media_publish （發布 Container）
```

**Threads**：
```
POST /{ig-id}/threads （一次性發布）
```

## 設定流程

### 步驟 1：準備 Instagram 商業帳號

1. 將 Instagram 帳號轉換為 **Business Account** 或 **Creator Account**
2. 在 Instagram App 中設定 → 帳號 → 建立專業帳號

### 步驟 2：連接到 Facebook 頁面

1. 前往 Facebook 頁面
2. 設定 → Instagram → 連接帳號
3. 選擇你的 Instagram 商業帳號

### 步驟 3：申請 Threads API 權限

1. 前往 https://developers.facebook.com/tools/explorer/
2. 選擇你的 App
3. 申請 Threads API 測試權限
4. 等待審核通過

### 步驟 4：取得 Access Token

1. 在 Facebook 開發者工具中
2. 點擊 "Get User Access Token"
3. 勾選權限：
   - `pages_show_list`
   - `threads_basic`
   - `threads_content_publish`
4. 執行：`GET /{page-id}?fields=access_token,instagram_business_account`
5. 複製 `access_token` 和 `instagram_business_account.id`

### 步驟 5：更新資料庫

```sql
UPDATE channal_info
SET
  page_id = "你的Facebook頁面ID",
  access_token = "你的Access Token"
WHERE channal_id = 1;
```

## 使用範例

### 範例 1：純文字貼文

```bash
python3 scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "這是一條 Threads 貼文！🧵

與社群分享你的想法...

#Threads #SocialMedia"
```

### 範例 2：圖片貼文

```bash
python3 scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "分享一張照片 📸" \
  --image-url "https://i.pix2.io/summer-sale.jpg"
```

### 範例 3：影片貼文

```bash
python3 scripts/post.py \
  --action video \
  --from-db \
  --channel-id 1 \
  --text "分享一段影片 🎬" \
  --video-url "https://example.com/reel.mp4"
```

### 範例 4：從 URL 下載並發布

```bash
# 下載圖片
wget https://example.com/photo.jpg -O /tmp/photo.jpg

# 上傳到 Pix2
IMAGE_URL=$(python3 .claude/skills/pix2-upload/scripts/upload.py /tmp/photo.jpg)

# 發布到 Threads
python3 scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "下載並發布的圖片" \
  --image-url "$IMAGE_URL"
```

## 自動化腳本

### 批次發布多張圖片

```bash
#!/bin/bash
# batch-post-threads.sh

CHANNEL_ID=1

# 圖片列表
IMAGES=(
  "https://i.pix2.io/img1.jpg"
  "https://i.pix2.io/img2.jpg"
  "https://i.pix2.io/img3.jpg"
)

# 迴圈發布
for i in "${!IMAGES[@]}"; do
  IMAGE="${IMAGES[$i]}"
  echo "正在發布: $IMAGE"

  python3 scripts/post.py \
    --action image \
    --from-db \
    --channel-id $CHANNEL_ID \
    --text "批次發布 #$((i+1))" \
    --image-url "$IMAGE"

  # 避免速率限制
  sleep 60
done
```

### 同時發布到 Instagram 和 Threads

```bash
#!/bin/bash
# cross-post.sh

CHANNEL_ID=1
IMAGE_URL=$1
CAPTION=$2

echo "📸 發布到 Instagram..."
python3 .claude/skills/instagram-post/scripts/post.py \
  --action photo \
  --from-db \
  --channel-id $CHANNEL_ID \
  --caption "$CAPTION" \
  --image-url "$IMAGE_URL"

echo ""
echo "🧵 發布到 Threads..."
python3 .claude/skills/threads-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id $CHANNEL_ID \
  --text "$CAPTION" \
  --image-url "$IMAGE_URL"

echo ""
echo "✅ 跨平台發布完成！"
```

## 故障排除

### 錯誤 1：找不到 Instagram Business Account

**症狀**：
```
❌ 取得 Instagram 商業帳號失敗：此 Facebook 頁面沒有連接 Instagram 商業帳號
```

**解決方案**：
1. 確認 Facebook 頁面已連接到 Instagram
2. 在 Facebook 頁面設定中重新連接
3. 確認 Instagram 帳號是 Business Account

### 錯誤 2：Container 建立失敗

**症狀**：
```
❌ 建立 Container 失敗: Invalid URL
```

**解決方案**：
1. 確認圖片 URL 可以公開訪問
2. 確認圖片格式正確（JPG、PNG、WEBP）
3. 確認圖片大小不超過 5MB

### 錯誤 3：權限不足

**症狀**：
```
❌ 發布失敗: (#200) Requires threads_basic permission
```

**解決方案**：
1. 檢查 Access Token 權限
2. 確認包含 `threads_basic` 和 `threads_content_publish` 權限
3. 重新生成 Access Token

### 錯誤 4：文字超過限制

**症狀**：
```
⚠️  警告：文字超過 500 字符，將自動截斷
```

**解決方案**：
1. Threads 限制文字為 500 字符
2. 縮短文字或分段發布
3. 腳本會自動截斷並發布前 500 字符

### 錯誤 5：影片處理超時

**症狀**：
```
❌ 影片處理失敗，狀態: TIMEOUT
```

**解決方案**：
1. 影片可能需要更長時間處理
2. 檢查影片格式（建議 MP4）
3. 檢查影片大小（不超過 50MB）
4. 嘗試重新上傳

## 整合範例

### 與 social-content-writer 完整流程

```bash
#!/bin/bash
# complete-threads-workflow.sh

TOPIC="$1"
CHANNEL_ID=1

echo "📝 步驟 1：生成 Threads 內容"
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "$TOPIC" \
  --platform threads \
  --framework pas \
  --output threads_content.json

echo ""
echo "🎨 步驟 2：生成圖片提示詞"
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content threads_content.json \
  --type image \
  --auto-generate \
  --upload-pix2

echo ""
echo "📸 步驟 3：讀取圖片 URL"
IMAGE_URL=$(jq -r '.prompts.image[0].url' threads_content.json)

echo ""
echo "🧵 步驟 4：發布到 Threads"
python3 .claude/skills/threads-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id $CHANNEL_ID \
  --text "$(jq -r '.content' threads_content.json)" \
  --image-url "$IMAGE_URL"

echo ""
echo "✅ 完成！"
```

使用方式：
```bash
bash complete-threads-workflow.sh "夏日促銷活動"
```

### 與 Instagram 同時發布

```bash
# 使用相同的內容和圖片同時發布到 Instagram 和 Threads

IMAGE_URL="https://i.pix2.io/product.jpg"
CAPTION="新產品上市！🔥

限時優惠中，敬請把握！

#新產品 #優惠 #限時"

# Instagram 支援較長的文字
python3 .claude/skills/instagram-post/scripts/post.py \
  --action photo \
  --from-db \
  --channel-id 1 \
  --caption "$CAPTION" \
  --image-url "$IMAGE_URL"

# Threads 文字限制 500 字符，會自動截斷
python3 .claude/skills/threads-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "$CAPTION" \
  --image-url "$IMAGE_URL"
```

## 平台特色比較

| 特性 | Threads | Instagram | Facebook |
|------|---------|-----------|----------|
| **文字限制** | 500 字符 | 2,200 字符 | 63,206 字符 |
| **圖片支援** | ✅ 單張 | ✅ 單張 + Carousel | ✅ 單張 + 多張 |
| **影片支援** | ✅ 最長 5 分鐘 | ✅ 最長 60 秒 | ✅ 最長 240 分鐘 |
| **發布流程** | 一次性 | Container → Publish | 直接發布 |
| **連結支援** | ✅ | ❌ | ✅ |
| **Hashtag** | ✅ | ✅ | ✅ |
| **提及** | ✅ | ✅ | ✅ |

## 最佳實踐

### 1. 內容策略

**Threads 適合的內容**：
- 短暫的想法和觀點
- 對話式互動
- 快速更新
- 輕鬆、休閒的內容

**Instagram 適合的內容**：
- 精美的視覺內容
- 深度故事
- 產品展示
- 品牌形象

**Facebook 適合的內容**：
- 長篇內容
- 教程和指南
- 活動資訊
- 社群互動

### 2. 發布頻率建議

- **Threads**：每天 1-5 則（快速、頻繁）
- **Instagram**：每天 1-3 則（精質）
- **Facebook**：每天 1-2 則（穩定）

### 3. 跨平台發布建議

1. **優先發布到 Threads**（最快、最簡單）
2. **調整後發布到 Instagram**（增加更多視覺元素）
3. **擴展後發布到 Facebook**（提供更多細節）

### 4. 文字長度處理

由於 Threads 限制 500 字符，建議：

```bash
# 方法 1：自動截斷（腳本內建）
LONG_TEXT="很長的文字內容..."
# 腳本會自動截斷到 500 字符

# 方法 2：手動縮短
THREADS_TEXT=$(echo "$LONG_TEXT" | cut -c1-500)

# 方法 3：分段發布
# 第一段
python3 scripts/post.py --action text --text "第一段..."
# 第二段
python3 scripts/post.py --action text --text "第二段..."
```

## 參考資源

- [Threads Graph API 文檔](https://developers.facebook.com/docs/threads-api)
- [Instagram Content Publishing API](https://developers.facebook.com/docs/instagram-api/content-publishing/)
- [Facebook 開發者工具](https://developers.facebook.com/tools/explorer/)
- [Threads 社群指導原則](https://help.threads.net)

## 更新日誌

### 2026-01-30 - 初始版本
- ✅ 支援純文字發布
- ✅ 支援圖片發布
- ✅ 支援影片發布
- ✅ 自動取得 Instagram Business ID
- ✅ 從資料庫讀取設定
- ✅ 完整錯誤處理
