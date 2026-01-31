---
name: instagram-post
description: Instagram 貼文發布技能，支援文字、圖片、影片和 Carousel（多張圖片）發布到 Instagram。與 Facebook 不同，Instagram 可以直接使用資料庫中的 token 發文，無需換取 Page Token。
metadata:
  category: social-media
  type: automation
  languages:
    - python
  platforms:
    - instagram
  compatibility:
    - claude-code
    - opencode
    - any-agent
---

# Instagram Post - Instagram 貼文發布

直接從資料庫發布貼文到 Instagram，支援圖片、影片和 Carousel。

## 核心功能

1. **📸 單張圖片發布** - 發布單張圖片到 Instagram
2. **🎬 影片發布** - 發布影片到 Instagram（MP4 格式）
3. **📚 Carousel 發布** - 發布多張圖片（2-10 張）
4. **🔍 自動取得 IG ID** - 從 Facebook 頁面自動取得 Instagram 商業帳號 ID
5. **💾 資料庫整合** - 直接從資料庫讀取 token 和頁面 ID

## 與 Facebook 的差異

| 特性 | Instagram | Facebook |
|------|-----------|----------|
| Token 使用 | **直接使用資料庫 token** | 需要換取 Page Token |
| API 端點 | Instagram Graph API | Facebook Graph API |
| 發布流程 | Container → Publish | 直接發布 |
| 影片處理 | 需要等待處理完成 | 即時發布 |
| Carousel 支援 | ✅ 原生支援（2-10張） | ❌ 不支援 |
| 商業帳號 | 需要 Instagram Business Account | 需要 Facebook 頁面 |

## 前置要求

### 1. Instagram 商業帳號

- 必須是 **Instagram Business Account** 或 **Creator Account**
- 帳號必須連接到 **Facebook 頁面**
- 在 Facebook 頁面設定中連接 Instagram

### 2. Access Token

需要具有以下權限的 Facebook Page Access Token：
- `pages_show_list`
- `instagram_basic`
- `instagram_content_publish`
- `pages_manage_posts`

### 3. 資料庫設定

資料庫中的 `channal_info` 表需要包含：
- `page_id`: Facebook 頁面 ID
- `access_token`: Facebook Page Access Token

## 快速開始

### 發布單張圖片

```bash
python3 .claude/skills/instagram-post/scripts/post.py \
  --action photo \
  --from-db \
  --channel-id 1 \
  --caption "Hello Instagram! 📸" \
  --image-url "https://i.pix2.io/xxx.png"
```

### 發布影片

```bash
python3 .claude/skills/instagram-post/scripts/post.py \
  --action video \
  --from-db \
  --channel-id 1 \
  --caption "Check this out! 🎬" \
  --video-url "https://example.com/video.mp4"
```

### 發布 Carousel（多張圖片）

```bash
python3 .claude/skills/instagram-post/scripts/post.py \
  --action carousel \
  --from-db \
  --channel-id 1 \
  --caption "Multiple photos! 📚" \
  --image-urls "url1,url2,url3"
```

### 取得 Instagram 商業帳號 ID

```bash
python3 .claude/skills/instagram-post/scripts/post.py \
  --action get-ig-id \
  --from-db \
  --channel-id 1
```

## 從資料庫查找 Access Token

如果你的系統使用資料庫管理 token，可以從 `channal_info` 表中查詢：

### 查詢所有 Instagram 頻道

```bash
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT channal_id, channal_name, channal_source, page_id, access_token \
   FROM channal_info \
   WHERE channal_source = 'instagram'"
```

### 查詢特定頻道

```bash
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT channal_id, channal_name, page_id, access_token \
   FROM channal_info \
   WHERE channal_id = 1"
```

### 按平台來源查詢

```bash
# 查詢所有平台類型
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT DISTINCT channal_source FROM channal_info"

# 查詢特定平台的頻道
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT * FROM channal_info WHERE channal_source IN ('facebook', 'instagram', 'threads')"
```

**資料庫欄位說明**：
- `channal_id`: 頻道 ID（主鍵）
- `channal_name`: 頻道名稱
- `channal_source`: 平台來源（`facebook`、`instagram`、`threads`）
- `page_id`: Facebook 頁面 ID
- `access_token`: Access Token

## 使用方式

### 方式 1：從資料庫發布（推薦）

自動從資料庫讀取 Facebook 頁面 ID 和 Access Token：

```bash
python3 scripts/post.py \
  --action photo \
  --from-db \
  --channel-id 1 \
  --caption "你的內容" \
  --image-url "圖片URL"
```

**優點**：
- ✅ 自動讀取 token
- ✅ 自動取得 Instagram Business ID
- ✅ 無需手動設定參數
- ✅ 與 n8n 系統兼容

### 方式 2：手動指定參數

```bash
python3 scripts/post.py \
  --action photo \
  --instagram-business-id "17841401234567890" \
  --access-token "YOUR_ACCESS_TOKEN" \
  --caption "你的內容" \
  --image-url "圖片URL"
```

## 發布流程

### 圖片發布流程

```
1. 建立 Container (POST /{ig-id}/media)
   ├── image_url: 圖片 URL
   ├── caption: 說明文字
   └── access_token: Token

2. 發布 Container (POST /{ig-id}/media_publish)
   ├── creation_id: Container ID
   └── access_token: Token

3. 完成 ✅
```

### 影片發布流程

```
1. 建立 Container (POST /{ig-id}/media)
   ├── video_url: 影片 URL
   ├── caption: 說明文字
   └── access_token: Token

2. 等待處理完成
   └── 輪詢狀態直到 FINISHED

3. 發布 Container (POST /{ig-id}/media_publish)
   ├── creation_id: Container ID
   └── access_token: Token

4. 完成 ✅
```

### Carousel 發布流程

```
1. 為立多個圖片 Container (2-10 張)
   └── 每張圖片一個 Container

2. 建立 Carousel Container
   ├── media_type: CAROUSEL
   ├── children: Container IDs (逗號分隔)
   └── caption: 說明文字

3. 發布 Carousel
   └── creation_id: Carousel Container ID

4. 完成 ✅
```

## 參數說明

| 參數 | 說明 | 必需 |
|------|------|------|
| `--action` | 執行動作 (photo/video/carousel/get-ig-id) | ✅ |
| `--from-db` | 從資料庫讀取設定 | ❌ |
| `--channel-id` | 資料庫頻道 ID | ❌ (使用 --from-db 時必需) |
| `--instagram-business-id` | Instagram 商業帳號 ID | ❌ |
| `--page-id` | Facebook 頁面 ID | ❌ |
| `--access-token` | Access Token | ❌ |
| `--caption` | 貼文說明文字 | ✅ |
| `--image-url` | 單張圖片 URL | ✅ (action=photo 時) |
| `--video-url` | 影片 URL | ✅ (action=video 時) |
| `--image-urls` | 多張圖片 URL（逗號分隔） | ✅ (action=carousel 時) |

## 限制與規範

### Instagram 限制

| 項目 | 限制 |
|------|------|
| 單張圖片大小 | 最大 8MB |
| 影片大小 | 最大 50MB |
| 影片長度 | 最長 60 秒 |
| Caption 長度 | 最大 2,200 字符 |
| Hashtag 數量 | 最多 30 個 |
| Carousel 圖片數 | 2-10 張 |

### 支援的格式

**圖片**：
- JPG
- JPEG
- PNG

**影片**：
- MP4
- MOV
- WebM（可能不支援）

## 常見問題

### Q: 為什麼 Instagram 可以直接用資料庫的 token？

A: Instagram 和 Facebook 使用不同的 API 端點。Instagram Graph API 接受直接使用 Facebook Page Access Token，無需像 Facebook 那樣換取。

### Q: 如何取得 Instagram Business Account ID？

A: 有兩種方式：
1. 使用本腳本的 `--action get-ig-id` 自動取得
2. 在 Facebook 頁面設定 → Instagram 中查看

### Q: 為什麼我的影片一直顯示「處理中」？

A: Instagram 影片需要時間處理：
- 短影片（< 30 秒）：通常 1-5 分鐘
- 長影片（30-60 秒）：可能需要 5-15 分鐘

腳本會自動等待最多 5 分鐘。

### Q: Carousel 發布失敗？

A: 檢查：
1. 圖片數量是否在 2-10 張之間
2. 所有圖片 URL 是否有效
3. 圖片大小是否超過 8MB
4. Caption 是否超過 2,200 字符

### Q: 如何與 pix2-upload 整合？

A: 先上傳圖片到 Pix2，再發布到 Instagram：

```bash
# 1. 上傳圖片到 Pix2
IMAGE_URL=$(python3 .claude/skills/pix2-upload/scripts/upload.py photo.jpg)

# 2. 發布到 Instagram
python3 .claude/skills/instagram-post/scripts/post.py \
  --action photo \
  --from-db \
  --channel-id 1 \
  --caption "我的圖片" \
  --image-url "$IMAGE_URL"
```

## 範例

### 範例 1：發布產品圖片

```bash
python3 scripts/post.py \
  --action photo \
  --from-db \
  --channel-id 1 \
  --caption "新產品上市！🔥

限時優惠中，敬請把握！

#新產品 #優惠 #限時" \
  --image-url "https://i.pix2.io/product.jpg"
```

### 範例 2：發布品牌影片

```bash
python3 scripts/post.py \
  --action video \
  --from-db \
  --channel-id 1 \
  --caption "品牌故事 🎬

從零到一的創業旅程...

#品牌故事 #創業 #SME" \
  --video-url "https://example.com/brand-story.mp4"
```

### 範例 3：發布多張產品展示圖片

```bash
python3 scripts/post.py \
  --action carousel \
  --from-db \
  --channel-id 1 \
  --caption "新品發布！🎉

滑動查看所有顏色...

#新品 #產品展示 #Carousel" \
  --image-urls "https://i.pix2.io/1.jpg,https://i.pix2.io/2.jpg,https://i.pix2.io/3.jpg"
```

## 與其他技能整合

### social-content-writer

```bash
# 1. 生成 Instagram 內容
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "新產品發布" \
  --platform instagram \
  --framework aida \
  --output ig_content.json

# 2. 生成圖片
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content ig_content.json \
  --type image \
  --auto-generate \
  --upload-pix2

# 3. 讀取生成的圖片 URL
IMAGE_URL=$(jq -r '.prompts.image[0].url' ig_content.json)

# 4. 發布到 Instagram
python3 .claude/skills/instagram-post/scripts/post.py \
  --action photo \
  --from-db \
  --channel-id 1 \
  --message "$(jq -r '.content' ig_content.json)" \
  --image-url "$IMAGE_URL"
```

## 注意事項

1. **商業帳號要求**
   - 必須使用 Instagram Business Account
   - 必須連接到 Facebook 頁面
   - 個人帳號無法使用 API 發文

2. **Token 權限**
   - 確保包含所有必要權限
   - Token 過期需要更新

3. **影片處理時間**
   - 影片上傳後需要等待處理
   - 處理時間取決於影片長度和伺服器負載

4. **發布頻率**
   - Instagram 有速率限制
   - 避免短時間大量發文

5. **內容規範**
   - 遵守 Instagram 社群指導原則
   - 避免違規內容

## 授權

MIT License
