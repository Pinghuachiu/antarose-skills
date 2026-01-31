# Threads API 權限說明

## 快速開始

### 步驟 1：取得 Threads User ID（推薦）

使用新的 `/me` 端點直接取得 Threads User ID：

```bash
python3 .claude/skills/threads-post/scripts/post.py \
  --action get-threads-user-id \
  --from-db \
  --channel-id 1
```

這會返回你的 Threads User ID 和使用者名稱。

### 步驟 2：測試發布

使用自動取得的 Threads User ID 發布測試貼文：

```bash
python3 .claude/skills/threads-post/scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "Hello Threads! 🧵"
```

腳本會自動從 Token 取得 Threads User ID 並發布。

## 當前狀態

Threads API 目前需要特殊權限才能使用。如果你看到以下錯誤：

```
❌ 發布失敗：發布失敗: Unsupported post request. Object with ID '17841402854360694' does not exist, cannot be loaded due to missing permissions, or does not support this operation.
```

這表示你的 Access Token 沒有 Threads API 權限。

## 如何申請 Threads API 權限

### 步驟 1：確認 Facebook App 設定

1. 前往 https://developers.facebook.com/apps/
2. 選擇你的 App
3. 在 App 設定中確認：
   - App 類型：Business
   - App 模式：Live

### 步驟 2：測試 Threads API 權限

先使用以下命令測試是否已有權限：

```bash
# 測試取得 Threads User ID（需要 threads_basic 權限）
python3 .claude/skills/threads-post/scripts/post.py \
  --action get-threads-user-id \
  --access-token "YOUR_ACCESS_TOKEN"
```

如果成功，表示你已有權限！可以直接使用。

### 步驟 3：申請 Threads API 權限（如果步驟 2 失敗）

1. 前往 https://developers.facebook.com/apps/
2. 選擇你的 App
3. 在 App 設定中確認：
   - App 類型：Business
   - App 模式：Live

### 步驟 2：申請 Threads API 權限

1. 前往 https://developers.facebook.com/tools/explorer/
2. 選擇你的 App
3. 點擊 "Get Token" → "Get User Access Token"
4. 在權限清單中找到並勾選：
   - `threads_basic`
   - `threads_content_publish`
   - `pages_show_list`

### 步驟 4：提交審核

如果 `threads_basic` 和 `threads_content_publish` 權限無法選擇：

1. 前往 App Dashboard → App Review → Permissions and Features
2. 點擊 "Request to add permissions"
3. 搜尋並選擇：
   - `threads_basic`
   - `threads_content_publish`
4. 填寫申請表單，說明使用原因
5. 提交審核

### 步驟 5：等待審核

- 審核時間：通常 1-5 個工作天
- 審核通過後，你會收到通知
- 通過後即可使用 Threads API

## 測試權限

一旦獲得權限，你可以使用以下命令測試：

```bash
# 1. 測試取得 Threads User ID（推薦）
python3 .claude/skills/threads-post/scripts/post.py \
  --action get-threads-user-id \
  --from-db \
  --channel-id 1

# 2. 測試發布純文字（會自動取得 Threads User ID）
python3 .claude/skills/threads-post/scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "Hello Threads! 🧵"

# 3. 測試發布圖片
python3 .claude/skills/threads-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "Check this out!" \
  --image-url "https://i.pix2.io/xxx.png"
```

## 權限說明

### threads_basic

- 基本讀取權限
- 可以讀取 Threads 帳號資訊
- 必需權限

### threads_content_publish

- 發布內容權限
- 可以發布文字、圖片、影片
- 必需權限

### pages_show_list

- 顯示已授權的頁面清單
- 取得 Instagram Business Account
- 必需權限

## 替代方案

在等待 Threads API 權限期間，你可以：

### 1. 使用 Instagram 技能

Instagram 和 Threads 都是 Meta 旗下的平台，可以先用 Instagram：

```bash
# 發布到 Instagram
python3 .claude/skills/instagram-post/scripts/post.py \
  --action photo \
  --from-db \
  --channel-id 1 \
  --caption "你的內容" \
  --image-url "圖片URL"
```

### 2. 使用 Facebook 技能

Facebook 也支援多種內容格式：

```bash
# 發布到 Facebook
python3 .claude/skills/facebook-page-post/scripts/post.py \
  --from-db \
  --channel-id 1 \
  --message "你的內容"
```

### 3. 手動發布到 Threads

1. 使用技能生成內容
2. 複製內容和圖片
3. 手動貼到 Threads App

## 更新資料庫 Token

一旦獲得 Threads API 權限，需要更新 Access Token：

1. 重新生成包含 Threads 權限的 Access Token
2. 更新資料庫：

```sql
UPDATE channal_info
SET access_token = "新的包含 Threads 權限的 Token"
WHERE channal_id = 1;
```

3. 重新測試發布功能

## 參考資源

- [Threads API 官方文檔](https://developers.facebook.com/docs/threads-api)
- [Facebook App Review](https://developers.facebook.com/docs/app-review)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)

## 常見問題

### Q: 為什麼需要特殊權限？

A: Threads API 目前在測試階段，Meta 採行審核制度以確保平台穩定性和內容品質。

### Q: 審核需要多久？

A: 通常 1-5 個工作天，但可能因申請量而延長。

### Q: 所有人都能申請嗎？

A: 是的，只要是有效的 Facebook App 開發者都可以申請。

### Q: 權限會過期嗎？

A: Access Token 會過期（通常 60 天），但權限本身不會過期。可以重新生成 Token。

### Q: 可以使用測試帳號嗎？

A: 可以，但需要在 Facebook App 設定中添加測試帳號。
