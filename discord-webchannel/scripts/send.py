#!/usr/bin/env python3
"""
Discord Webchannel - Python 腳本
使用 Discord Webhook 發送訊息
"""

import requests
import json
import sys
import os
import argparse

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
if not WEBHOOK_URL:
    print("錯誤: 請設定 DISCORD_WEBHOOK_URL 環境變數", file=sys.stderr)
    print("請參考 resource.md 獲取 Webhook URL", file=sys.stderr)
    sys.exit(1)

def send_message(content, username=None, avatar_url=None, tts=False):
    """發送簡單文字訊息"""
    payload = {"content": content, "tts": tts}

    if username:
        payload["username"] = username
    if avatar_url:
        payload["avatar_url"] = avatar_url

    try:
        response = requests.post(str(WEBHOOK_URL), json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"✅ 訊息發送成功 - ID: {result.get('id', 'N/A')}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"❌ 訊息發送失敗: {e}", file=sys.stderr)
        if response := getattr(e, 'response', None):
            print(f"回應: {response.text}", file=sys.stderr)
        sys.exit(1)

def send_embed(title, description=None, color=0x5865F2, fields=None, thumbnail=None, image=None):
    """發送 Embed 訊息"""
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

    try:
        response = requests.post(str(WEBHOOK_URL), json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"✅ Embed 發送成功 - ID: {result.get('id', 'N/A')}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"❌ Embed 發送失敗: {e}", file=sys.stderr)
        if response := getattr(e, 'response', None):
            print(f"回應: {response.text}", file=sys.stderr)
        sys.exit(1)

def send_attachment(file_path, content=None, username=None):
    """發送附件訊息"""
    payload = {}

    if content:
        payload["content"] = content
    if username:
        payload["username"] = username

    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            payload_json = json.dumps(payload)

            response = requests.post(
                str(WEBHOOK_URL),
                data={"payload_json": payload_json},
                files=files
            )
            response.raise_for_status()
            result = response.json()
            print(f"✅ 附件發送成功 - ID: {result.get('id', 'N/A')}")
            return result
    except FileNotFoundError:
        print(f"❌ 檔案不存在: {file_path}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ 附件發送失敗: {e}", file=sys.stderr)
        if response := getattr(e, 'response', None):
            print(f"回應: {response.text}", file=sys.stderr)
        sys.exit(1)

def parse_fields(fields_str):
    """解析欄位字串"""
    if not fields_str:
        return None

    fields = []
    for field in fields_str.split('|'):
        parts = field.split(':')
        if len(parts) >= 2:
            name = parts[0].strip()
            value = parts[1].strip()
            inline = False
            if len(parts) >= 3 and parts[2].strip().lower() == 'true':
                inline = True
            fields.append({"name": name, "value": value, "inline": inline})
    return fields

def parse_color(color_str):
    """解析顏色字串（支援十六進制）"""
    if not color_str:
        return 0x5865F2

    if color_str.startswith('0x') or color_str.startswith('0X'):
        return int(color_str, 16)
    elif color_str.startswith('#'):
        return int(color_str[1:], 16)
    else:
        return int(color_str)

def main():
    parser = argparse.ArgumentParser(
        description='Discord Webhook 訊息發送工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 基本訊息
  python3 send.py "Hello, World!"

  # Markdown 格式
  python3 send.py "**粗體** *斜體*"

  # 自訂使用者名稱
  python3 send.py --username "My Bot" "訊息"

  # 基本 Embed
  python3 send.py --embed --title "標題" --description "描述"

  # Embed with 欄位
  python3 send.py --embed --title "系統" --fields "CPU:45%|記憶體:60%"

  # Embed with 顏色（十六進制）
  python3 send.py --embed --title "錯誤" --color 0xFF0000

  # 發送附件
  python3 send.py --file image.jpg "這是附件"

  # TTS 訊息
  python3 send.py --tts "這是語音訊息"
        """
    )

    parser.add_argument('message', nargs='?', help='訊息內容')
    parser.add_argument('--embed', action='store_true', help='發送 Embed 訊息')
    parser.add_argument('--title', help='Embed 標題')
    parser.add_argument('--description', help='Embed 描述')
    parser.add_argument('--color', help='Embed 顏色（十進制或 0x/十六進制）')
    parser.add_argument('--fields', help='Embed 欄位（格式：name:value:inline|name2:value2:inline2）')
    parser.add_argument('--thumbnail', help='Embed 縮圖 URL')
    parser.add_argument('--image', help='Embed 圖片 URL')
    parser.add_argument('--file', help='附件檔案路徑')
    parser.add_argument('--username', help='自訂使用者名稱')
    parser.add_argument('--avatar', help='自訂頭像 URL')
    parser.add_argument('--tts', action='store_true', help='TTS 訊息')

    args = parser.parse_args()

    # 驗證參數
    if args.embed:
        if not args.title:
            print("錯誤: 使用 --embed 時必須提供 --title", file=sys.stderr)
            sys.exit(1)
    elif not args.file and not args.message:
        parser.print_help()
        sys.exit(1)

    # 發送訊息
    try:
        if args.file:
            send_attachment(
                file_path=args.file,
                content=args.message,
                username=args.username
            )
        elif args.embed:
            send_embed(
                title=args.title,
                description=args.description,
                color=parse_color(args.color),
                fields=parse_fields(args.fields),
                thumbnail=args.thumbnail,
                image=args.image
            )
        else:
            send_message(
                content=args.message,
                username=args.username,
                avatar_url=args.avatar,
                tts=args.tts
            )
    except KeyboardInterrupt:
        print("\n已取消", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
