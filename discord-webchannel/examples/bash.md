# Discord Webchannel - Bash 使用範例

## 設置 Webhook URL

```bash
export WEBHOOK_URL="YOUR_WEBHOOK_URL"
```

## 1. 簡單文字訊息

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello, World!"
  }'
```

## 2. Markdown 格式

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "**粗體** *斜體* ~~刪除線~~"
  }'
```

## 3. 自訂使用者名稱和頭像

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "自訂 Bot 訊息",
    "username": "My Bot",
    "avatar_url": "https://example.com/avatar.png"
  }'
```

## 4. TTS 訊息

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "這是語音訊息",
    "tts": true
  }'
```

## 5. 基本 Embed

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "embeds": [
      {
        "title": "標題",
        "description": "這是描述",
        "color": 5814783
      }
    ]
  }'
```

## 6. Embed with 欄位

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "embeds": [
      {
        "title": "系統狀態",
        "description": "目前的系統狀態",
        "color": 65280,
        "fields": [
          {
            "name": "CPU",
            "value": "45%",
            "inline": true
          },
          {
            "name": "記憶體",
            "value": "60%",
            "inline": true
          },
          {
            "name": "磁碟",
            "value": "30%",
            "inline": true
          }
        ]
      }
    ]
  }'
```

## 7. Embed with 圖片

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "embeds": [
      {
        "title": "圖片分享",
        "description": "這是一張圖片",
        "color": 16711680,
        "image": {
          "url": "https://example.com/image.png"
        },
        "thumbnail": {
          "url": "https://example.com/thumbnail.png"
        }
      }
    ]
  }'
```

## 8. 發送附件

```bash
curl -X POST "$WEBHOOK_URL" \
  -F "file=@/path/to/file.jpg" \
  -F 'payload_json={"content":"這是附件","username":"File Bot"}'
```

## 9. 複雜 Embed

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "embeds": [
      {
        "title": "部署通知",
        "description": "部署已成功完成",
        "color": 65280,
        "fields": [
          {
            "name": "應用程式",
            "value": "My App",
            "inline": true
          },
          {
            "name": "版本",
            "value": "v1.0.0",
            "inline": true
          },
          {
            "name": "狀態",
            "value": "✅ 成功",
            "inline": false
          },
          {
            "name": "時間",
            "value": "2024-01-01 00:00:00",
            "inline": true
          },
          {
            "name": "持續時間",
            "value": "2分30秒",
            "inline": true
          },
          {
            "name": "作者",
            "value": "@user",
            "inline": true
          }
        ],
        "thumbnail": {
          "url": "https://example.com/icon.png"
        }
      }
    ]
  }'
```

## 10. 常用顏色代碼

| 顏色 | 十進制 | 十六進制 | 用途 |
|------|--------|----------|------|
| 紅色 | 16711680 | FF0000 | 錯誤、警告 |
| 綠色 | 65280 | 00FF00 | 成功、完成 |
| 黃色 | 16776960 | FFFF00 | 警告、注意 |
| 藍色 | 5793266 | 5865F2 | 資訊、一般 |
| 紫色 | 16711745 | 9922EE | 特殊、突出 |

## 11. 程式碼區塊

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "```javascript\nconsole.log(\"Hello\");\n```"
  }'
```

## 12. 引用

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "> 這是引用文字\n\n這是普通文字"
  }'
```

## 13. 清單

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "- 項目一\n- 項目二\n  - 子項目 A\n  - 子項目 B"
  }'
```

## 14. 連結和圖片

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "[連結文字](https://example.com)\n\n![圖片描述](https://example.com/image.png)"
  }'
```

## 15. 多個附件

```bash
curl -X POST "$WEBHOOK_URL" \
  -F "files[0]=@image1.jpg" \
  -F "files[1]=@image2.png" \
  -F 'payload_json={"content":"多個附件"}'
```

## 16. 設定提及

```bash
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "@everyone 重要通知",
    "allowed_mentions": {
      "parse": ["everyone"]
    }
  }'
```

## 17. 發送到執行緒

```bash
curl -X POST "$WEBHOOK_URL?thread_id=THREAD_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "發送到執行緒的訊息"
  }'
```

## 18. 使用 jq 動態內容

```bash
# 從檔案讀取內容
MESSAGE=$(cat message.txt)

curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"content\": \"$MESSAGE\"
  }"

# 使用變數
TITLE="系統通知"
DESCRIPTION="這是動態內容"
COLOR=65280

curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"embeds\": [
      {
        \"title\": \"$TITLE\",
        \"description\": \"$DESCRIPTION\",
        \"color\": $COLOR
      }
    ]
  }"
```

## 19. 系統監控範例

```bash
# CPU 使用率
CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)

# 記憶體使用率
MEM=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100)}')

# 發送監控訊息
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"embeds\": [
      {
        \"title\": \"系統監控\",
        \"color\": 5793266,
        \"fields\": [
          {
            \"name\": \"CPU 使用率\",
            \"value\": \"${CPU}%\",
            \"inline\": true
          },
          {
            \"name\": \"記憶體使用率\",
            \"value\": \"${MEM}%\",
            \"inline\": true
          },
          {
            \"name\": \"時間\",
            \"value\": \"$(date +'%Y-%m-%d %H:%M:%S')\",
            \"inline\": false
          }
        ]
      }
    ]
  }"
```

## 20. CI/CD 部署通知

```bash
# CI/CD 變數
APP_NAME="My Application"
VERSION="v1.0.0"
STATUS="Success"
BUILD_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
DURATION="2m 30s"
AUTHOR="@user"

curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"embeds\": [
      {
        \"title\": \"🚀 部署通知\",
        \"description\": \"部署已成功完成\",
        \"color\": 65280,
        \"fields\": [
          {
            \"name\": \"應用程式\",
            \"value\": \"$APP_NAME\",
            \"inline\": true
          },
          {
            \"name\": \"版本\",
            \"value\": \"$VERSION\",
            \"inline\": true
          },
          {
            \"name\": \"狀態\",
            \"value\": \"✅ $STATUS\",
            \"inline\": false
          },
          {
            \"name\": \"部署時間\",
            \"value\": \"$BUILD_TIME\",
            \"inline\": true
          },
          {
            \"name\": \"持續時間\",
            \"value\": \"$DURATION\",
            \"inline\": true
          },
          {
            \"name\": \"作者\",
            \"value\": \"$AUTHOR\",
            \"inline\": true
          }
        ]
      }
    ]
  }"
```

## 快速參考

### 檢查 Webhook 資訊

```bash
curl "$WEBHOOK_URL"
```

### 修改 Webhook

```bash
curl -X PATCH "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Webhook Name"
  }'
```

### 刪除 Webhook

```bash
curl -X DELETE "$WEBHOOK_URL"
```
