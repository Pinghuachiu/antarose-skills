# Instagram Post Skill - 完整指南

## 概述

這個技能讓你可以直接從資料庫發布貼文到 Instagram，支援：
- ✅ 單張圖片
- ✅ 影片（MP4）
- ✅ Carousel（多張圖片）
- ✅ 自動取得 Instagram Business ID
- ✅ 無需換取 Page Token（與 Facebook 不同）

## 與 Facebook 的主要差異

### Token 使用方式

**Facebook**：
```
資料庫 User Token → 換取 Page Token → 發文
```

**Instagram**：
```
資料庫 Token → 直接發文
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

## 設定流程

### 步驟 1：準備 Instagram 商業帳號

1. 將 Instagram 帳號轉換為 **Business Account** 或 **Creator Account**
2. 在 Instagram App 中設定 → 帳號 → 建立專業帳號

### 步驟 2：連接到 Facebook 頁面

1. 前往 Facebook 頁面
2. 設定 → Instagram → 連接帳號
3. 選擇你的 Instagram 商業帳號

### 步驟 3：取得 Access Token

1. 前往 https://developers.facebook.com/tools/explorer/
2. 選擇你的 App
3. 點擊 "Get User Access Token"
4. 勾選權限：
   - `pages_show_list`
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_manage_posts`
5. 執行：`GET /{page-id}?fields=access_token,instagram_business_account`
6. 複製 `access_token` 和 `instagram_business_account.id`

### 步驟 4：更新資料庫

```sql
UPDATE channal_info
SET
  page_id = "你的Facebook頁面ID",
  access_token = "你的Access Token"
WHERE channal_id = 1;
```

## 使用範例

### 範例 1：單張圖片 + Hashtag

```bash
python3 scripts/post.py \
  --action photo \
  --from-db \
  --channel-id 1 \
  --caption "夏日限時優惠 ☀️

所有商品 8 折！

#夏日優惠 #限時 #促銷" \
  --image-url "https://i.pix2.io/summer-sale.jpg"
```

### 範例 2：短片（Reels 風格）

```bash
python3 scripts/post.py \
  --action video \
  --from-db \
  --channel-id 1 \
  --caption "Reels 👻

#Reels #Shorts #Viral" \
  --video-url "https://example.com/reel.mp4"
```

### 範例 3：產品展示 Carousel

```bash
python3 scripts/post.py \
  --action carousel \
  --from-db \
  --channel-id 1 \
  --caption "全新系列 🆕

滑動查看所有顏色與款式！

#新品 #系列 #商品展示" \
  --image-urls "https://i.pix2.io/p1.jpg,https://i.pix2.io/p2.jpg,https://i.pix2.io/p3.jpg,https://i.pix2.io/p4.jpg,https://i.pix2.io/p5.jpg"
```

### 範例 4：從 URL 下載並發布

```bash
# 下載圖片
wget https://example.com/photo.jpg -O /tmp/photo.jpg

# 上傳到 Pix2
IMAGE_URL=$(python3 .claude/skills/pix2-upload/scripts/upload.py /tmp/photo.jpg)

# 發布到 Instagram
python3 scripts/post.py \
  --action photo \
  --from-db \
  --channel-id 1 \
  --caption "下載並發布的圖片" \
  --image-url "$IMAGE_URL"
```

## 自動化腳本

### 批次發布多張圖片

```bash
#!/bin/bash
# batch-post.sh

CHANNEL_ID=1

# 圖片列表
IMAGES=(
  "https://i.pix2.io/img1.jpg"
  "https://i.pix2.io/img2.jpg"
  "https://i.pix2.io/img3.jpg"
)

# 迴圈發布
for IMAGE in "${IMAGES[@]}"; do
  echo "正在發布: $IMAGE"

  python3 scripts/post.py \
    --action photo \
    --from-db \
    --channel-id $CHANNEL_ID \
    --caption "批次發布 #$((i+1))" \
    --image-url "$IMAGE"

  # 避免速率限制
  sleep 60
done
```

### 排程發布

```bash
# 使用 cron 排程
# 每天早上 9 點發布

0 9 * * * /path/to/instagram-post.sh
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
2. 確認圖片格式正確（JPG、JPEG、PNG）
3. 確認圖片大小不超過 8MB

### 錯誤 3：影片一直處理中

**症狀**：
```
⏳ 處理中... (超過 5 分鐘)
```

**解決方案**：
1. 等待更長時間（影片可能需要 15 分鐘）
2. 檢查影片格式（建議 MP4）
3. 檢查影片大小（不超過 50MB）
4. 嘗試重新上傳

### 錯誤 4：發布失敗 - 權限不足

**症狀**：
```
❌ 發布失敗: (#200) Not authorized to access this Instagram business account
```

**解決方案**：
1. 檢查 Access Token 權限
2. 確認包含 `instagram_content_publish` 權限
3. 重新生成 Access Token

## 整合範例

### 與 social-content-writer 完整流程

```bash
#!/bin/bash
# complete-instagram-workflow.sh

TOPIC="$1"
CHANNEL_ID=1

echo "📝 步驟 1：生成 Instagram 內容"
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "$TOPIC" \
  --platform instagram \
  --framework pas \
  --output ig_content.json

echo ""
echo "🎨 步驟 2：生成圖片提示詞"
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content ig_content.json \
  --type image \
  --auto-generate \
  --upload-pix2

echo ""
echo "📸 步驟 3：讀取圖片 URL"
IMAGE_URL=$(jq -r '.prompts.image[0].url' ig_content.json)

echo ""
echo "📱 步驟 4：發布到 Instagram"
python3 .claude/skills/instagram-post/scripts/post.py \
  --action photo \
  --from-db \
  --channel-id $CHANNEL_ID \
  --message "$(jq -r '.content' ig_content.json)" \
  --image-url "$IMAGE_URL"

echo ""
echo "✅ 完成！"
```

使用方式：
```bash
bash complete-instagram-workflow.sh "夏日促銷活動"
```

## 參考資源

- [Instagram Graph API 文檔](https://developers.facebook.com/docs/instagram-api/)
- [Instagram Content Publishing API](https://developers.facebook.com/docs/instagram-api/content-publishing/)
- [Instagram Business Account](https://www.facebook.com/business/help/205946343308532)
- [Facebook 開發者工具](https://developers.facebook.com/tools/explorer/)

## 更新日誌

### 2026-01-30 - 初始版本
- ✅ 支援單張圖片發布
- ✅ 支援影片發布
- ✅ 支援 Carousel（多張圖片）
- ✅ 自動取得 Instagram Business ID
- ✅ 從資料庫讀取設定
- ✅ 完整錯誤處理
