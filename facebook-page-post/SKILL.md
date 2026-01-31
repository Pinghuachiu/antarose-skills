---
name: facebook-page-post
description: 使用 Facebook Graph API v24.0 發布文章、圖片、影片到 Facebook 粉絲專頁，包含完整的 Token 管理和更新指南
metadata:
  category: social
  type: post
  languages:
    - python
    - javascript
    - bash
  supports:
    - text-post
    - photo-post
    - video-post
    - token-management
  api_version: v24.0
---

# Facebook Page Post - 粉絲專頁發文技能

使用 Facebook Graph API v24.0 發布文字、圖片、影片到 Facebook 粉絲專頁，包含完整的 Token 管理和更新指南。

## 功能特性

- ✅ 發布文字文章到 Facebook 粉絲專頁
- ✅ 上傳單張圖片
- ✅ 上傳多張圖片（自動建立相簿）
- ✅ 上傳影片
- ✅ Token 有效期檢查和警告
- ✅ 完整的 Token 管理指南

## API 資訊

- **API 提供商**: Facebook
- **API 版本**: v24.0 (2025)
- **API 文檔**: https://developers.facebook.com/docs/pages-api/posts/
- **認證方式**: Page Access Token
- **Token 有效期**: 60 天（長期）/ 可申請永久

## 快速開始

### 1. 設定環境變數

```bash
# Facebook Page 設定
export FACEBOOK_PAGE_ID="your-page-id"
export FACEBOOK_PAGE_ACCESS_TOKEN="your-page-access-token"
```

### 2. 驗證 Token

```bash
python3 .claude/skills/facebook-page-post/scripts/token-helper.py
```

### 3. 發布第一篇文章

```bash
# 文字文章
python3 .claude/skills/facebook-page-post/scripts/post.py text \
  --message "Hello, World!"

# 圖片文章
python3 .claude/skills/facebook-page-post/scripts/post.py photo \
  --file photo.jpg \
  --message "Beautiful photo"

# 影片文章
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file video.mp4 \
  --message "Check out this video"
```

## Token 管理

### Token 類型和有效期

| Token 類型 | 有效期 | 用途 |
|-----------|--------|------|
| Short-lived User Token | ~1-2 小時 | 初始認證 |
| Long-lived User Token | 60 天 | 延長存取 |
| **Long-lived Page Token** | **60 天** | **推薦用於此技能** |
| Never-Expiring Page Token | 永久 | 可透過 API Explorer 取得 |

### 取得 Page Access Token

#### 方法 1: 從資料庫查詢（推薦，用於 n8n 系統）

如果你的系統使用資料庫管理 token，可以從 `channal_info` 表中查詢：

```bash
# 查詢所有 Facebook 頻道的 token
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT channal_id, channal_name, channal_source, page_id, access_token \
   FROM channal_info \
   WHERE channal_source = 'facebook'"

# 查詢特定頻道的 token
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT channal_id, channal_name, page_id, access_token \
   FROM channal_info \
   WHERE channal_id = 1"
```

**資料庫欄位說明**：
- `channal_id`: 頻道 ID（主鍵）
- `channal_name`: 頻道名稱
- `channal_source`: 平台來源（`facebook`、`instagram`、`threads`）
- `page_id`: Facebook 頁面 ID
- `access_token`: Page Access Token

**使用資料庫 Token 發文**：
```bash
python3 .claude/skills/facebook-page-post/scripts/post.py text \
  --message "Hello from database!" \
  --from-db \
  --channel-id 1
```

#### 方法 2: 使用 Graph API Explorer（推薦用於測試）

1. **存取 Graph API Explorer**
   - 前往: https://developers.facebook.com/tools/explorer/
   - 從下拉選單選擇你的 App

2. **取得 User Token**
   - 點擊 "Get User Access Token"
   - 選擇權限: `pages_manage_posts`, `pages_read_engagement`, `pages_manage_engagement`
   - 點擊 "Generate Access Token"

3. **取得 Page Access Token**
   ```
   GET /{page-id}?fields=access_token
   ```
   - 複製 `access_token` 的值（這是長期 Page Token）

4. **延長為永久 Token（可選）**
   - 在 Graph API Explorer 中，點擊 "Extend Access Token" 按鈕
   - 或使用 API 呼叫:
   ```
   GET /oauth/access_token?
     grant_type=fb_exchange_token&
     client_id={app-id}&
     client_secret={app-secret}&
     fb_exchange_token={short-lived-token}
   ```

#### 方法 2: 使用 Facebook Login 流程（正式環境）

1. 在你的 App 中實作 Facebook Login
2. 取得短期 User Token
3. 交換為長期 User Token（60 天）
4. 從 User Token 取得 Page Access Token
5. 安全地儲存在環境變數中

### Token 更新流程

#### 自動更新（過期前）

**最佳實踐**: 每週檢查 Token 有效期，並在 60 天前更新。

使用 `token-helper.py` 檢查：
```bash
python3 .claude/skills/facebook-page-post/scripts/token-helper.py
```

輸出示例：
```
=== Token 資訊 ===
App ID: 123456789
Type: PAGE
是否有效: True
過期時間: 2026-03-29 12:34:56
剩餘天數: 58 天
權限: pages_manage_posts, pages_read_engagement
```

#### 手動更新步驟

1. **重新前往 Graph API Explorer**
2. **產生新的 User Token**（相同權限）
3. **取得新的 Page Access Token**
4. **更新環境變數**:
   ```bash
   export FACEBOOK_PAGE_ACCESS_TOKEN="new-token-here"
   ```
5. **驗證新 Token**:
   ```bash
   python3 .claude/skills/facebook-page-post/scripts/token-helper.py
   ```

#### 永久 Token 方法（2025）

根據 [Software Mirrors 指南](https://www.software-mirrors.com/blog/how-to-get-a-never-expiring-facebook-page-access-token-in-2025-step-by-step)：

1. 使用 Graph API Explorer 的 "Extend Access Token" 按鈕
2. 選擇特定的 Page Access Token
3. 使用 `pages_manage_posts` 權限
4. 結果: 永久 Token（除非密碼變更才會失效）

### ⚠️ Token 過期觸發條件

- 使用者變更 Facebook 密碼
- 使用者移除 App 權限
- 60 天期限到達（長期 Token）
- App 被刪除或停用

### ✅ 最佳實踐

- 將 Token 儲存在環境變數中（絕不要寫在程式碼中）
- 在 API 呼叫前實作 Token 驗證
- 設定過期警告監控
- 記錄更新流程
- 定期使用 debug 端點測試 Token

## 必要權限

Page Access Token 需要以下權限：

| 權限 | 用途 |
|------|------|
| `pages_manage_posts` | 建立、編輯和刪除貼文 |
| `pages_read_engagement` | 讀取互動數據 |
| `pages_manage_engagement` | 管理留言和按讚 |

## API 端點

### Graph API v24.0 端點

| 端點 | 方法 | 用途 |
|------|------|------|
| `/{page-id}/feed` | POST | 建立文字貼文 |
| `/{page-id}/photos` | POST | 上傳圖片 |
| `/{page-id}/videos` | POST | 上傳影片 |
| `/{page-id}/albums` | POST | 建立相簿（多張圖片） |
| `/debug_token` | GET | 檢查 Token 資訊 |

## 使用範例

### 文章發布

```bash
# 基本文字文章
python3 .claude/skills/facebook-page-post/scripts/post.py text \
  --message "今天天氣真好！"

# 帶有連結的文章
python3 .claude/skills/facebook-page-post/scripts/post.py text \
  --message "查看我們的網站: https://example.com"
```

### 圖片發布

```bash
# 單張圖片
python3 .claude/skills/facebook-page-post/scripts/post.py photo \
  --file /path/to/photo.jpg \
  --message "美麗的風景"

# 多張圖片（自動建立相簿）
python3 .claude/skills/facebook-page-post/scripts/post.py photos \
  --files photo1.jpg photo2.jpg photo3.jpg \
  --message "相簿標題"
```

### 影片發布

```bash
# 基本影片上傳
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file /path/to/video.mp4 \
  --message "精彩影片"

# 影片加上標題和描述
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file /path/to/video.mp4 \
  --title "影片標題" \
  --message "影片描述"
```

## 回應格式

### 成功回應

```json
{
  "id": "1234567890_987654321"
}
```

`id` 格式為 `{page-id}_{post-id}`

### Token Debug 回應

```json
{
  "data": {
    "app_id": "123456789",
    "type": "PAGE",
    "is_valid": true,
    "expires_at": 1763456789,
    "granular_scopes": [
      {
        "scope": "pages_manage_posts",
        "target_ids": ["123456789"]
      }
    ]
  }
}
```

## 錯誤處理

### 常見錯誤

| 錯誤碼 | 訊息 | 原因 | 解決方案 |
|-------|------|------|----------|
| `190` | Invalid OAuth Token | Token 過期或無效 | 更新 Token |
| `200` | Permissions Error | 缺少必要權限 | 新增權限到 Token |
| `368` | Temporarily Blocked | 超過速率限制 | 等待後重試 |
| `100` | Invalid Parameter | 請求格式錯誤 | 檢查 API 參數 |
| `190` | Access token expired | Token 超過 60 天 | 使用 Graph API Explorer 重新取得 |

### 錯誤處理範例

腳本包含自動重試機制：

```python
MAX_RETRIES = 3
RETRY_DELAY = 5  # 秒

for attempt in range(MAX_RETRIES):
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        break
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 368 and attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)
            continue
        raise
```

## 可執行腳本

### Python 腳本 (post.py)

**使用方法**：
```bash
# 文字文章
python3 scripts/post.py text --message "Hello"

# 圖片文章
python3 scripts/post.py photo --file photo.jpg --message "Caption"

# 多張圖片
python3 scripts/post.py photos --files p1.jpg p2.jpg --message "Album"

# 影片文章
python3 scripts/post.py video --file video.mp4 --title "Title"
```

**參數**：
- `type`: 發文類型（text, photo, photos, video）
- `--message`: 文字內容或說明
- `--file`: 單一檔案路徑（photo/video）
- `--files`: 多個檔案路徑（photos）
- `--title`: 影片標題

### Token Helper 腳本 (token-helper.py)

```bash
python3 scripts/token-helper.py
```

輸出：
- App ID
- Token 類型
- 是否有效
- 過期時間
- 剩餘天數
- 權限列表
- 過期警告（< 7 天）

## 最佳實踐

### 選擇發文類型

| 場景 | 推薦方式 |
|------|----------|
| 文字公告 | text |
| 產品展示 | photo |
| 活動記錄 | photos (相簿) |
| 教學內容 | video |
| 圖文並茂 | photo + message |

### 發文時機

- 工作日早上 9-11 點
- 工作日晚上 7-9 點
- 週末下午
- 避開深夜發文

### Token 安全

1. ✅ 使用環境變數
2. ✅ 定期檢查有效期
3. ❌ 不要提交到 Git
4. ❌ 不要在前端程式碼中使用
5. ✅ 使用 `.env` 檔案（記得加入 .gitignore）

## 注意事項

1. **Token 管理**: Token 會在 60 天後過期，請定期更新
2. **權限**: 確保 Token 有所有必要權限
3. **檔案大小**:
   - 圖片: 最大 4MB
   - 影片: 最大 1GB（建議使用分段上傳）
4. **發文頻率**: Facebook 有速率限制，避免短時間大量發文
5. **隱私**: Page Access Token 可以存放在環境變數中
6. **測試**: 使用測試專頁進行測試

## 參考資源

### 官方文檔

- [Pages API Posts](https://developers.facebook.com/docs/pages-api/posts/)
- [Page Access Tokens](https://developers.facebook.com/docs/pages/access-tokens/)
- [Graph API v24.0](https://developers.facebook.com/blog/post/2025/10/08/introducing-graph-api-v24-and-marketing-api-v24/)
- [Debug Token Tool](https://developers.facebook.com/tools/debug/accesstoken/)
- [Video Publishing Guide](https://developers.facebook.com/docs/video-api/guides/publishing/)

### Token 管理

- [Get Long-Lived Tokens](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/)
- [Never-Expiring Token Guide (2025)](https://www.software-mirrors.com/blog/how-to-get-a-never-expiring-facebook-page-access-token-in-2025-step-by-step)

## 更新日誌

### 2026-01-29 - 初始版本

**功能**:
- 文字發文
- 單張圖片上傳
- 多張圖片上傳（相簿）
- 影片上傳
- Token 有效期檢查工具
- 完整的 Token 管理指南

**特色**:
- 支援 Facebook Graph API v24.0
- 自動錯誤處理和重試
- Token 過期警告系統
- 詳細的使用範例和文檔
