---
name: discord-webchannel
description: 使用 Discord Webhook 發送訊息到 Discord 頻道，支援純文字、富文字、Embeds、附件等功能
metadata:
  category: communication
  type: messaging
  languages:
    - python
    - javascript
    - bash
  supports:
    - text-messages
    - embeds
    - attachments
    - mentions
---

# Discord Webchannel - Discord 訊息發送技能

使用 Discord Webhook 發送訊息到指定 Discord 頻道，支援純文字、富文字、Embeds、附件等功能。

## API 資訊

- **API 提供商**: Discord
- **Webhook URL**: `https://discord.com/api/webhooks/{webhook-id}/{webhook-token}`
- **官方文檔**: https://discord.com/developers/docs/resources/webhook#execute-webhook

## 功能支援

### 1. 純文字訊息

發送簡單的文字訊息。

### 2. Markdown 格式

Discord 支援以下 Markdown 語法：
- **粗體**: `**文字**`
- *斜體*: `*文字*` 或 `_文字_`
- ~~刪除線~~: `~~文字~~`
- `行內程式碼`: `` `程式碼` ``
- 程式碼區塊:
  ````
  ```語言
  程式碼
  ```
  ````
- 引用: `> 引用文字`
- 清單:
  - 項目
    - 子項目
- 連結: `[連結文字](URL)`
- 圖片: `![圖片描述](URL)`

### 3. Embeds

豐富的嵌入式訊息，支援標題、描述、顏色、欄位、縮圖、圖片等。

### 4. 附件

上傳檔案並發送到 Discord。

### 5. 提及

提及使用者 `@user` 或角色 `@role`。

### 6. TTS (文字轉語音)

將訊息轉換為語音播放。

## 快速開始

### 使用可執行腳本

**Python**：
```bash
python3 .opencode/skills/discord-webchannel/scripts/send.py "Hello, World!"
```

**Node.js**：
```bash
node .opencode/skills/discord-webchannel/scripts/send.js "Hello, World!"
```

### 查看詳細範例

- **Python 範例**: 參見 [examples/python.md](examples/python.md)
- **JavaScript 範例**: 參見 [examples/javascript.md](examples/javascript.md)
- **Bash 命令範例**: 參見 [examples/bash.md](examples/bash.md)

## 請求格式

### URL 結構

```
https://discord.com/api/webhooks/{webhook-id}/{webhook-token}
```

### HTTP Method

- `POST`: 發送訊息
- `GET`: 取得 Webhook 資訊
- `PATCH`: 修改 Webhook
- `DELETE`: 刪除 Webhook

### Headers

| Header | Value | 必填 |
|--------|-------|------|
| `Content-Type` | `application/json` | 是（訊息內容） |
| `Content-Type` | `multipart/form-data` | 是（附件） |

## 請求參數

### Query Parameters

| 參數 | 類型 | 說明 |
|------|------|------|
| `wait` | boolean | 是否等待伺服器確認回應（預設 false） |
| `thread_id` | snowflake | 發送到指定執行緒 |

### Request Body

#### 基本訊息

```json
{
  "content": "訊息內容",
  "username": "自訂使用者名稱",
  "avatar_url": "https://example.com/avatar.png",
  "tts": false
}
```

#### 欄位說明

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `content` | string | 否 | 訊息內容（最多 2000 字元） |
| `username` | string | 否 | 覆蓋預設的使用者名稱 |
| `avatar_url` | string | 否 | 覆蓋預設的頭像 |
| `tts` | boolean | 否 | 是否為 TTS 訊息（預設 false） |
| `embeds` | array | 否 | 嵌入物件數組（最多 10 個） |
| `allowed_mentions` | object | 否 | 控制提及設定 |
| `components` | array | 否 | 訊息元件（按鈕、選單等） |
| `attachments` | array | 否 | 附件資訊 |
| `flags` | number | 否 | 訊息旗標（例如 SUPPRESS_EMBEDS） |

#### Embed 結構

```json
{
  "embeds": [
    {
      "title": "標題",
      "description": "描述",
      "url": "https://example.com",
      "color": 5814783,
      "fields": [
        {
          "name": "欄位名稱",
          "value": "欄位值",
          "inline": false
        }
      ],
      "thumbnail": {
        "url": "https://example.com/thumbnail.png"
      },
      "image": {
        "url": "https://example.com/image.png"
      },
      "author": {
        "name": "作者名稱",
        "url": "https://example.com",
        "icon_url": "https://example.com/icon.png"
      },
      "footer": {
        "text": "頁腳文字",
        "icon_url": "https://example.com/icon.png"
      },
      "timestamp": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

#### Embed 欄位說明

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `title` | string | 否 | 標題（最多 256 字元） |
| `description` | string | 否 | 描述（最多 4096 字元） |
| `url` | string | 否 | 標題點擊連結 |
| `color` | integer | 否 | 顏色（十進制） |
| `fields` | array | 否 | 欄位數組（最多 25 個） |
| `thumbnail` | object | 否 | 縮圖 |
| `image` | object | 否 | 大圖 |
| `author` | object | 否 | 作者資訊 |
| `footer` | object | 否 | 頁腳資訊 |
| `timestamp` | ISO8601 | 否 | 時間戳記 |

#### Allowed Mentions

```json
{
  "allowed_mentions": {
    "parse": ["users", "roles", "everyone"],
    "users": ["user-id"],
    "roles": ["role-id"],
    "replied_user": false
  }
}
```

| 欄位 | 類型 | 說明 |
|------|------|------|
| `parse` | array | 允許提及的類型 |
| `users` | array | 允許提及的使用者 ID |
| `roles` | array | 允許提及的角色 ID |
| `replied_user` | boolean | 是否提及回覆的使用者 |

## 附件上傳

### 使用 multipart/form-data

```bash
curl -X POST "https://discord.com/api/webhooks/{webhook-id}/{webhook-token}" \
  -F "file=@/path/to/file.jpg" \
  -F "payload_json={\"content\":\"這是附件訊息\"}"
```

### 多個附件

```bash
curl -X POST "https://discord.com/api/webhooks/{webhook-id}/{webhook-token}" \
  -F "files[0]=@image1.jpg" \
  -F "files[1]=@image2.png" \
  -F "payload_json={\"content\":\"多個附件\"}"
```

## 回應格式

### 成功回應 (200 OK)

```json
{
  "id": "123456789012345678",
  "type": 0,
  "content": "訊息內容",
  "channel_id": "123456789012345678",
  "author": {
    "id": "123456789012345678",
    "username": "Bot",
    "discriminator": "0000",
    "avatar": null,
    "bot": true
  },
  "embeds": [],
  "attachments": [],
  "timestamp": "2024-01-01T00:00:00.000Z",
  "edited_timestamp": null,
  "tts": false,
  "pinned": false,
  "mention_everyone": false,
  "mentions": [],
  "mention_roles": [],
  "flags": 0
}
```

### 錯誤回應

#### 400 Bad Request

```json
{
  "code": 50006,
  "message": "Cannot send an empty message"
}
```

#### 401 Unauthorized

```json
{
  "code": 10004,
  "message": "Unknown Webhook"
}
```

#### 429 Too Many Requests

```json
{
  "code": 0,
  "message": "You are being rate limited.",
  "retry_after": 5000
}
```

## 可執行腳本

### Python 腳本

**使用方法**：
```bash
# 基本用法
python3 scripts/send.py "Hello, World!"

# 發送 Embed
python3 scripts/send.py --embed --title "標題" --description "描述"

# 上傳附件
python3 scripts/send.py --file /path/to/file.jpg "這是附件"

# 自訂使用者名稱和頭像
python3 scripts/send.py --username "Bot" --avatar "https://example.com/avatar.png" "訊息"
```

**參數**：
- `message`: 訊息內容（必需）
- `--embed`: 發送 Embed 訊息
- `--title`: Embed 標題
- `--description`: Embed 描述
- `--color`: Embed 顏色（十六進制）
- `--file`: 附件路徑
- `--username`: 自訂使用者名稱
- `--avatar`: 自訂頭像 URL
- `--tts`: TTS 訊息

### Node.js 腳本

**使用方法**：
```bash
# 基本用法
node scripts/send.js "Hello, World!"

# 發送 Embed
node scripts/send.js --embed --title "標題" --description "描述"

# 上傳附件
node scripts/send.js --file /path/to/file.jpg "這是附件"
```

**參數**：
- 與 Python 腳本相同

## 最佳實踐

### 選擇訊息類型

| 場景 | 推薦方式 |
|------|----------|
| 簡單通知 | 純文字訊息 |
| 結構化資料 | Embed |
| 圖片/檔案分享 | 附件 |
| 重要提醒 | Embed + 附件 |
| 系統日誌 | Embed + 欄位 |

### Embed 顏色建議

| 顏色 | 十進制 | 用途 |
|------|--------|------|
| 紅色 | 16711680 | 錯誤、警告 |
| 綠色 | 65280 | 成功、完成 |
| 黃色 | 16776960 | 警告、注意 |
| 藍色 | 5793266 | 資訊、一般 |
| 紫色 | 16711745 | 特殊、突出 |

### 錯誤處理

1. 檢查 Webhook URL 是否正確
2. 驗證訊息內容格式
3. 確認檔案大小（最大 25MB）
4. 處理 Rate Limit（429）
5. 檢查 API 回應狀態碼

## 注意事項

1. **Webhook URL**: 請妥善保管 Webhook URL，不要公開分享
2. **訊息長度**: 訊息內容最多 2000 字元
3. **附件大小**: 單個附件最大 25MB
4. **Rate Limit**: Discord 有 API 請求限制
5. **Embeds**: 最多 10 個 Embed
6. **Fields**: 每個 Embed 最多 25 個欄位
7. **刪除**: Webhook 可以被伺服器管理員刪除

## 安全提示

1. 不要在程式碼中硬編碼 Webhook URL
2. 使用環境變數或設定檔
3. 請參考 [resource.md](../../../resource.md) 獲取 Webhook URL
