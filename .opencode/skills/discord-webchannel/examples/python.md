import requests
import json

# 從環境變數或直接設定 Webhook URL
WEBHOOK_URL = "YOUR_WEBHOOK_URL"

def send_message(content, username=None, avatar_url=None, tts=False):
    """
    發送簡單文字訊息

    Args:
        content: 訊息內容
        username: 自訂使用者名稱
        avatar_url: 自訂頭像 URL
        tts: 是否為 TTS 訊息

    Returns:
        API 回應
    """
    payload = {"content": content, "tts": tts}

    if username:
        payload["username"] = username
    if avatar_url:
        payload["avatar_url"] = avatar_url

    response = requests.post(WEBHOOK_URL, json=payload)
    return response.json()

def send_embed(title, description=None, color=0x5865F2, fields=None, thumbnail=None, image=None):
    """
    發送 Embed 訊息

    Args:
        title: Embed 標題
        description: Embed 描述
        color: Embed 顏色（十進制）
        fields: 欄位數組 [{"name": "名稱", "value": "值", "inline": False}]
        thumbnail: 縮圖 URL
        image: 圖片 URL

    Returns:
        API 回應
    """
    embed = {
        "title": title,
        "color": color
    }

    if description:
        embed["description"] = description
    if fields:
        embed["fields"] = fields
    if thumbnail:
        embed["thumbnail"] = {"url": thumbnail}
    if image:
        embed["image"] = {"url": image}

    payload = {"embeds": [embed]}
    response = requests.post(WEBHOOK_URL, json=payload)
    return response.json()

def send_attachment(file_path, content=None, username=None):
    """
    發送附件訊息

    Args:
        file_path: 檔案路徑
        content: 訊息內容
        username: 自訂使用者名稱

    Returns:
        API 回應
    """
    payload = {}

    if content:
        payload["content"] = content
    if username:
        payload["username"] = username

    with open(file_path, "rb") as f:
        files = {"file": f}
        payload_json = json.dumps(payload)

        response = requests.post(
            WEBHOOK_URL,
            data={"payload_json": payload_json},
            files=files
        )

    return response.json()

# 使用範例

# 1. 簡單文字訊息
result = send_message("Hello, World!")
print(result)

# 2. Markdown 格式
result = send_message("**粗體** *斜體* ~~刪除線~~")
print(result)

# 3. 自訂使用者名稱和頭像
result = send_message(
    "自訂 Bot 訊息",
    username="My Bot",
    avatar_url="https://example.com/avatar.png"
)
print(result)

# 4. TTS 訊息
result = send_message("這是語音訊息", tts=True)
print(result)

# 5. 基本 Embed
result = send_embed(
    title="標題",
    description="這是描述",
    color=0x5865F2  # Discord 藍色
)
print(result)

# 6. Embed with 欄位
result = send_embed(
    title="系統狀態",
    description="目前的系統狀態",
    color=0x00FF00,  # 綠色
    fields=[
        {"name": "CPU", "value": "45%", "inline": True},
        {"name": "記憶體", "value": "60%", "inline": True},
        {"name": "磁碟", "value": "30%", "inline": True}
    ]
)
print(result)

# 7. Embed with 圖片
result = send_embed(
    title="圖片分享",
    description="這是一張圖片",
    color=0xFF0000,  # 紅色
    image="https://example.com/image.png",
    thumbnail="https://example.com/thumbnail.png"
)
print(result)

# 8. 發送附件
result = send_attachment(
    file_path="/path/to/file.jpg",
    content="這是附件",
    username="File Bot"
)
print(result)

# 9. 複雜 Embed
result = send_embed(
    title="部署通知",
    description="部署已成功完成",
    color=0x00FF00,
    fields=[
        {"name": "應用程式", "value": "My App", "inline": True},
        {"name": "版本", "value": "v1.0.0", "inline": True},
        {"name": "狀態", "value": "✅ 成功", "inline": False},
        {"name": "時間", "value": "2024-01-01 00:00:00", "inline": True},
        {"name": "持續時間", "value": "2分30秒", "inline": True},
        {"name": "作者", "value": "@user", "inline": True}
    ],
    thumbnail="https://example.com/icon.png"
)
print(result)

# 10. 錯誤處理
try:
    result = send_message("測試訊息")
    if "id" in result:
        print("訊息發送成功")
    else:
        print("訊息發送失敗:", result)
except Exception as e:
    print("發生錯誤:", e)
