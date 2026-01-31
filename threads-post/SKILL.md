---
name: threads-post
description: Threads 貼文發布技能，支援文字、圖片和影片發布到 Threads。與 Facebook 不同，Threads 可以直接使用資料庫中的 token 發文，無需換取 Page Token。
metadata:
  category: social-media
  type: automation
  languages:
    - python
  platforms:
    - threads
  compatibility:
    - claude-code
    - opencode
    - any-agent
---

# Threads Post - Threads 貼文發布

直接從資料庫發布貼文到 Threads，支援文字、圖片和影片。

## 核心功能

1. **📝 純文字發布** - 發布純文字貼文到 Threads（最多 500 字符）
2. **📸 圖片發布** - 發布圖片貼文到 Threads
3. **🎬 影片發布** - 發布影片貼文到 Threads（MP4、MOV 格式）
4. **🆔 直接取得 Threads User ID** - 使用 `/me` 端點直接取得（推薦）
5. **🔄 自動取得 IG Business ID** - 從 Facebook 頁面自動取得 Instagram 商業帳號 ID
6. **💾 資料庫整合** - 直接從資料庫讀取 token（access_token 欄位）

## 與 Facebook 的差異

| 特性 | Threads | Facebook |
|------|---------|----------|
| Token 使用 | **直接使用資料庫 token** | 需要換取 Page Token |
| API 端點 | Instagram Threads API | Facebook Graph API |
| 發布流程 | 一次性發布（Container = 發布） | 直接發布 |
| 文字限制 | 500 字符 | 63,206 字符 |
| 圖片支援 | ✅ 單張圖片 | ✅ 單張圖片 |
| 影片支援 | ✅ 影片（MP4/MOV） | ✅ 影片 |
| 商業帳號 | 需要 Instagram Business Account | 需要 Facebook 頁面 |

## 與 Instagram 的差異

| 特性 | Threads | Instagram |
|------|---------|----------|
| 文字限制 | 500 字符 | 2,200 字符 |
| 發布流程 | Container 即發布（單張）→ Publish（Carousel） | Container → Publish 兩步驟 |
| 圖片格式 | JPG、PNG、WEBP | JPG、JPEG、PNG |
| 影片格式 | MP4、MOV | MP4、MOV、WebM |
| Carousel 支援 | ✅ 支援（2-20張圖片/影片混合） | ✅ 支援（2-10張） |

## 前置要求

### 1. Instagram 商業帳號

- 必須是 **Instagram Business Account** 或 **Creator Account**
- 帳號必須連接到 **Facebook 頁面**
- 在 Facebook 頁面設定中連接 Instagram

### 2. Access Token

需要具有以下權限的 Facebook Page Access Token：
- `threads_basic`
- `threads_content_publish`
- `pages_show_list`

### 3. Threads 測試權限

- 目前 Threads API 需要申請測試權限
- 前往 https://developers.facebook.com/tools/explorer/ 申請

### 4. 資料庫設定

資料庫中的 `channal_info` 表需要包含：
- `page_id`: Facebook 頁面 ID
- `access_token`: Facebook Page Access Token

## 快速開始

### 取得 Threads User ID（推薦）

```bash
# 從資料庫取得
python3 .claude/skills/threads-post/scripts/post.py \
  --action get-threads-user-id \
  --from-db \
  --channel-id 1

# 手動指定 token
python3 .claude/skills/threads-post/scripts/post.py \
  --action get-threads-user-id \
  --access-token "YOUR_TOKEN"
```

### 發布純文字

```bash
# 方式 1：從資料庫自動取得 Threads ID（推薦）
python3 .claude/skills/threads-post/scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "Hello Threads! 🧵"

# 方式 2：手動指定 Threads User ID
python3 .claude/skills/threads-post/scripts/post.py \
  --action text \
  --threads-user-id "THREADS_USER_ID" \
  --access-token "YOUR_TOKEN" \
  --text "Hello Threads! 🧵"
```

### 發布圖片

```bash
python3 .claude/skills/threads-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "Check this out! 📸" \
  --image-url "https://i.pix2.io/xxx.png"
```

### 發布影片

```bash
python3 .claude/skills/threads-post/scripts/post.py \
  --action video \
  --from-db \
  --channel-id 1 \
  --text "Amazing video! 🎬" \
  --video-url "https://example.com/video.mp4"
```

### 發布 Carousel（多張圖片/影片）

**重要**: Threads 支援最多 **20 張**圖片/影片（最少 2 張）的 carousel！

```bash
python3 .claude/skills/threads-post/scripts/post.py \
  --action carousel \
  --from-db \
  --channel-id 3 \
  --text "Multiple images carousel! 📚✨" \
  --media-urls "https://i.pix2.io/YxcWSnTE.jpg,https://i.pix2.io/J5SY8DzU.png"
```

**Carousel 限制**：
- 最多 20 張圖片/影片（或混合）
- 最少 2 張
- 支援 JPG、PNG、WEBP、MP4、MOV 格式

### 取得 Instagram 商業帳號 ID（舊方法）

```bash
python3 .claude/skills/threads-post/scripts/post.py \
  --action get-ig-id \
  --from-db \
  --channel-id 1
```

## 從資料庫查找 Access Token

如果你的系統使用資料庫管理 token，可以從 `channal_info` 表中查詢：

### 查詢 Threads 頻道

```bash
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT channal_id, channal_name, channal_source, page_id, access_token \
   FROM channal_info \
   WHERE channal_source = 'threads'"
```

### 查詢特定頻道

```bash
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT channal_id, channal_name, page_id, access_token \
   FROM channal_info \
   WHERE channal_id = 3"
```

### 查詢所有平台類型

```bash
# 查看有哪些平台
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT DISTINCT channal_source FROM channal_info"

# 查詢特定平台的頻道
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT channal_id, channal_name, channal_source FROM channal_info \
   WHERE channal_source IN ('facebook', 'instagram', 'threads') \
   ORDER BY channal_source, channal_id"
```

**資料庫欄位說明**：
- `channal_id`: 頻道 ID（主鍵）
- `channal_name`: 頻道名稱
- `channal_source`: 平台來源（`facebook`、`instagram`、`threads`）
- `page_id`: Facebook 頁面 ID（可選）
- `access_token`: Access Token

**實際範例**：
```bash
# 1. 查找 Threads 頻道
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT channal_id, channal_name FROM channal_info WHERE channal_source = 'threads'"

# 輸出：
# +------------+------------------+
# | channal_id | channal_name      |
# +------------+------------------+
# |          3 | jackalchiu7610   |
# +------------+------------------+

# 2. 使用該頻道發文
python3 .claude/skills/threads-post/scripts/post.py \
  --action text \
  --from-db \
  --channel-id 3 \
  --text "Hello from database! 🧵"
```

## 使用方式

### 方式 1：從資料庫發布（推薦）

自動從資料庫讀取 Access Token 並取得 Threads User ID：

```bash
python3 scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "你的內容"
```

**優點**：
- ✅ 自動讀取 token（access_token 欄位）
- ✅ 自動取得 Threads User ID
- ✅ 無需手動設定參數
- ✅ 與 n8n 系統兼容

### 方式 2：手動指定參數

```bash
# 使用 Threads User ID（推薦）
python3 scripts/post.py \
  --action text \
  --threads-user-id "THREADS_USER_ID" \
  --access-token "YOUR_ACCESS_TOKEN" \
  --text "你的內容"

# 使用 Instagram Business Account ID（舊方法）
python3 scripts/post.py \
  --action text \
  --instagram-business-id "17841401234567890" \
  --access-token "YOUR_ACCESS_TOKEN" \
  --text "你的內容"
```

## 發布流程

### 純文字發布流程

```
1. POST /{ig-id}/threads
   ├── media_type: TEXT
   ├── text: 貼文內容
   └── access_token: Token

2. 完成 ✅
```

### 圖片發布流程

```
1. POST /{ig-id}/threads
   ├── media_type: IMAGE
   ├── image_url: 圖片 URL
   ├── text: 說明文字（可選）
   └── access_token: Token

2. 等待處理完成（可選）

3. 完成 ✅
```

### 影片發布流程

```
1. POST /{ig-id}/threads
   ├── media_type: VIDEO
   ├── video_url: 影片 URL
   ├── text: 說明文字（可選）
   └── access_token: Token

2. 等待處理完成
   └── 輪詢狀態直到 FINISHED

3. 完成 ✅
```

## 參數說明

| 參數 | 說明 | 必需 |
|------|------|------|
| `--action` | 執行動作 (text/image/video/get-threads-user-id/get-ig-id) | ✅ |
| `--threads-user-id` | Threads User ID（使用 /me 端點取得，推薦） | ❌ |
| `--instagram-business-id` | Instagram 商業帳號 ID（舊方法） | ❌ |
| `--from-db` | 從資料庫讀取設定 | ❌ |
| `--channel-id` | 資料庫頻道 ID | ❌ (使用 --from-db 時必需) |
| `--page-id` | Facebook 頁面 ID | ❌ |
| `--access-token` | Access Token | ❌ |
| `--text` | 貼文文字（最多 500 字符） | ✅ (action=text 時) |
| `--image-url` | 圖片 URL | ✅ (action=image 時) |
| `--video-url` | 影片 URL | ✅ (action=video 時) |

## 限制與規範

### Threads 限制

| 項目 | 限制 |
|------|------|
| 文字長度 | 最多 500 字符 |
| 單張圖片大小 | 最大 5MB |
| 影片大小 | 最大 50MB |
| 影片長度 | 最長 5 分鐘 |
| 圖片格式 | JPG、PNG、WEBP |

### 支援的格式

**圖片**：
- JPG
- PNG
- WEBP

**影片**：
- MP4
- MOV

## 常見問題

### Q: 為什麼 Threads 可以直接用資料庫的 token？

A: Threads 使用 Instagram Threads API，接受直接使用 Facebook Page Access Token，無需像 Facebook 那樣換取。

### Q: Threads 和 Instagram 發文有什麼不同？

A:
1. Threads 文字限制較短（500 vs 2,200 字符）
2. Threads 發布更簡單（Container 即發布，無需額外 publish 步驟）
3. Threads 不支援 Carousel

### Q: 如何取得 Threads 測試權限？

A:
1. 前往 Facebook 開發者工具
2. 申請 Threads API 測試權限
3. 等待審核通過

### Q: 為什麼我的影片一直顯示「處理中」？

A: Threads 影片需要時間處理：
- 短影片（< 1 分鐘）：通常 1-3 分鐘
- 長影片（1-5 分鐘）：可能需要 3-10 分鐘

腳本會自動等待最多 5 分鐘。

### Q: 如何與 pix2-upload 整合？

A: 先上傳圖片到 Pix2，再發布到 Threads：

```bash
# 1. 上傳圖片到 Pix2
IMAGE_URL=$(python3 .claude/skills/pix2-upload/scripts/upload.py photo.jpg)

# 2. 發布到 Threads
python3 .claude/skills/threads-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "我的圖片" \
  --image-url "$IMAGE_URL"
```

## 範例

### 範例 1：發布文字貼文

```bash
python3 scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "這是一條 Threads 貼文！🧵\n\n#Threads #SocialMedia"
```

### 範例 2：發布圖片貼文

```bash
python3 scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "分享一張照片 📸" \
  --image-url "https://i.pix2.io/photo.jpg"
```

### 範例 3：發布影片貼文

```bash
python3 scripts/post.py \
  --action video \
  --from-db \
  --channel-id 1 \
  --text "分享一段影片 🎬" \
  --video-url "https://example.com/video.mp4"
```

## 與其他技能整合

### social-content-writer

```bash
# 1. 生成 Threads 內容
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "新產品發布" \
  --platform threads \
  --framework pas \
  --output threads_content.json

# 2. 生成圖片
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content threads_content.json \
  --type image \
  --auto-generate \
  --upload-pix2

# 3. 讀取生成的圖片 URL
IMAGE_URL=$(jq -r '.prompts.image[0].url' threads_content.json)

# 4. 發布到 Threads
python3 .claude/skills/threads-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "$(jq -r '.content' threads_content.json)" \
  --image-url "$IMAGE_URL"
```

### instagram-post 同時發布

```bash
# 同時發布到 Instagram 和 Threads

IMAGE_URL="https://i.pix2.io/photo.jpg"
CAPTION="這是一張很棒的照片！📸"

# 發布到 Instagram
python3 .claude/skills/instagram-post/scripts/post.py \
  --action photo \
  --from-db \
  --channel-id 1 \
  --caption "$CAPTION" \
  --image-url "$IMAGE_URL"

# 發布到 Threads
python3 .claude/skills/threads-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "$CAPTION" \
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

3. **文字限制**
   - Threads 嚴格限制 500 字符
   - 超過會自動截斷

4. **影片處理時間**
   - 影片上傳後需要等待處理
   - 處理時間取決於影片長度和伺服器負載

5. **內容規範**
   - 遵守 Threads 社群指導原則
   - 避免違規內容

6. **API 測試權限**
   - Threads API 目前需要申請測試權限
   - 確保已獲得權限再使用

## 授權

MIT License
