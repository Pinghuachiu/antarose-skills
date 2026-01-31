#!/usr/bin/env python3
"""
Facebook Page Post - Python 腳本
使用 Facebook Graph API v24.0 發布文字、圖片、影片到 Facebook 粉絲專頁
"""

import os
import sys
import requests
import argparse
import time
from pathlib import Path

# Configuration
PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID")
ACCESS_TOKEN = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
API_VERSION = "v24.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def validate_credentials():
    """驗證環境變數"""
    if not PAGE_ID:
        print("錯誤: 請設定 FACEBOOK_PAGE_ID 環境變數", file=sys.stderr)
        print("範例: export FACEBOOK_PAGE_ID=\"123456789\"", file=sys.stderr)
        print("詳細說明請參考: https://developers.facebook.com/docs/pages/access-tokens/", file=sys.stderr)
        sys.exit(1)

    if not ACCESS_TOKEN:
        print("錯誤: 請設定 FACEBOOK_PAGE_ACCESS_TOKEN 環境變數", file=sys.stderr)
        print("範例: export FACEBOOK_PAGE_ACCESS_TOKEN=\"EAAxxxxxx...\"", file=sys.stderr)
        print("取得方式請參考 SKILL.md 的 Token 管理章節", file=sys.stderr)
        sys.exit(1)


def make_api_request(url, data=None, files=None, max_retries=MAX_RETRIES):
    """
    發送 API 請求，包含重試機制

    Args:
        url: API URL
        data: POST data dict
        files: files dict for multipart upload
        max_retries: 最大重試次數

    Returns:
        API 回應 JSON
    """
    for attempt in range(max_retries):
        try:
            if files:
                response = requests.post(url, data=data, files=files)
            else:
                response = requests.post(url, json=data)

            # 檢查是否為 Rate Limit (368)
            if response.status_code == 200 or response.status_code == 201:
                return response.json()

            # 檢查是否為 Token 過期
            if response.status_code == 401:
                error_data = response.json()
                if error_data.get('error', {}).get('code') == 190:
                    print("⚠️  錯誤: Access Token 已過期或無效", file=sys.stderr)
                    print("請使用以下指令檢查 Token 狀態:", file=sys.stderr)
                    print("  python3 .claude/skills/facebook-page-post/scripts/token-helper.py", file=sys.stderr)
                    print("並參考 SKILL.md 更新 Token", file=sys.stderr)
                    sys.exit(1)

            # 檢查是否為 Rate Limit
            if response.status_code == 429 or \
               (response.status_code == 400 and response.json().get('error', {}).get('code') == 368):
                if attempt < max_retries - 1:
                    print(f"⏳ 達到速率限制，等待 {RETRY_DELAY} 秒後重試... (嘗試 {attempt + 1}/{max_retries})")
                    time.sleep(RETRY_DELAY)
                    continue

            # 其他錯誤
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"⚠️  請求失敗: {e}，重試中... (嘗試 {attempt + 1}/{max_retries})")
                time.sleep(RETRY_DELAY)
                continue
            else:
                print(f"❌ API 請求失敗: {e}", file=sys.stderr)
                sys.exit(1)


def post_text(message):
    """
    發布文字文章到 Facebook Page

    Args:
        message: 文字內容

    Returns:
        API 回應，包含貼文 ID
    """
    if not message:
        print("錯誤: 文字文章需要 --message 參數", file=sys.stderr)
        sys.exit(1)

    url = f"{BASE_URL}/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }

    result = make_api_request(url, data=payload)

    print(f"✅ 文章發布成功!")
    print(f"   貼文 ID: {result.get('id')}")
    print(f"   連結: https://www.facebook.com/{result.get('id').split('_')[1]}")

    return result


def post_photo(image_path, message=None):
    """
    上傳單張圖片到 Facebook Page

    Args:
        image_path: 圖片檔案路徑
        message: 圖片說明（可選）

    Returns:
        API 回應，包含圖片 ID
    """
    if not image_path:
        print("錯誤: 圖片文章需要 --file 參數", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(image_path):
        print(f"錯誤: 檔案不存在 - {image_path}", file=sys.stderr)
        sys.exit(1)

    url = f"{BASE_URL}/{PAGE_ID}/photos"
    payload = {"access_token": ACCESS_TOKEN}

    if message:
        payload["caption"] = message

    with open(image_path, "rb") as f:
        files = {"source": f}
        result = make_api_request(url, data=payload, files=files)

    print(f"✅ 圖片上傳成功!")
    print(f"   圖片 ID: {result.get('id')}")
    if result.get('post_id'):
        print(f"   貼文連結: https://www.facebook.com/{result.get('post_id').split('_')[1]}")

    return result


def post_photos(image_paths, message=None):
    """
    上傳多張圖片到 Facebook Page（會建立相簿）

    Args:
        image_paths: 圖片檔案路徑列表
        message: 相簿標題（可選）

    Returns:
        API 回應列表
    """
    if not image_paths or len(image_paths) == 0:
        print("錯誤: 多圖上傳需要 --files 參數", file=sys.stderr)
        sys.exit(1)

    # 檢查所有檔案是否存在
    for img_path in image_paths:
        if not os.path.exists(img_path):
            print(f"錯誤: 檔案不存在 - {img_path}", file=sys.stderr)
            sys.exit(1)

    print(f"📁 正在建立相簿並上傳 {len(image_paths)} 張圖片...")

    # 建立未發布的相簿
    album_url = f"{BASE_URL}/{PAGE_ID}/albums"
    album_payload = {
        "name": message or "Photo Album",
        "access_token": ACCESS_TOKEN
    }

    album_result = make_api_request(album_url, data=album_payload)
    album_id = album_result.get("id")

    print(f"   相簿 ID: {album_id}")

    # 上傳圖片到相簿
    results = []
    for i, image_path in enumerate(image_paths, 1):
        photo_url = f"{BASE_URL}/{album_id}/photos"

        with open(image_path, "rb") as f:
            files = {"source": f}
            result = make_api_request(photo_url, data={"access_token": ACCESS_TOKEN}, files=files)
            results.append(result)

        print(f"   圖片 {i}/{len(image_paths)} 上傳完成 (ID: {result.get('id')})")

    print(f"✅ 所有圖片上傳成功!")
    print(f"   相簿連結: https://www.facebook.com/media/set/?set={album_id}")

    return results


def post_video(video_path, message=None, title=None, description=None):
    """
    上傳影片到 Facebook Page

    Args:
        video_path: 影片檔案路徑
        message: 影片描述（可選）
        title: 影片標題（可選）
        description: 影片詳細描述（可選）

    Returns:
        API 回應，包含影片 ID
    """
    if not video_path:
        print("錯誤: 影片上傳需要 --file 參數", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(video_path):
        print(f"錯誤: 檔案不存在 - {video_path}", file=sys.stderr)
        sys.exit(1)

    # 檢查檔案大小
    file_size = os.path.getsize(video_path)
    file_size_mb = file_size / (1024 * 1024)

    if file_size_mb > 1000:
        print(f"⚠️  警告: 影片大小 {file_size_mb:.1f} MB，超過 1GB", file=sys.stderr)
        print("建議使用 Facebook 的 Resumable Upload API 上傳大型影片", file=sys.stderr)
        response = input("是否繼續? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

    url = f"{BASE_URL}/{PAGE_ID}/videos"
    payload = {"access_token": ACCESS_TOKEN}

    # 設定影片資訊
    if message:
        payload["description"] = message
    if title:
        payload["title"] = title
    if description:
        payload["description"] = description

    print(f"📹 正在上傳影片... (大小: {file_size_mb:.1f} MB)")

    with open(video_path, "rb") as f:
        files = {"source": f}
        result = make_api_request(url, data=payload, files=files)

    print(f"✅ 影片上傳成功!")
    print(f"   影片 ID: {result.get('id')}")

    # 影片需要處理時間
    print(f"   注意: 影片正在處理中，請稍候片刻後查看")

    return result


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description="Facebook Page Post - 發布文章、圖片、影片到 Facebook 粉絲專頁",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  文字文章:
    python3 %(prog)s text --message "Hello, World!"

  單張圖片:
    python3 %(prog)s photo --file photo.jpg --message "Beautiful photo"

  多張圖片:
    python3 %(prog)s photos --files photo1.jpg photo2.jpg --message "Album"

  影片上傳:
    python3 %(prog)s video --file video.mp4 --title "My Video"

環境變數:
  FACEBOOK_PAGE_ID         Facebook 粉絲專頁 ID
  FACEBOOK_PAGE_ACCESS_TOKEN   Facebook Page Access Token

詳細說明請參考 SKILL.md
        """
    )

    parser.add_argument(
        "type",
        choices=["text", "photo", "photos", "video"],
        help="發文類型"
    )
    parser.add_argument(
        "--message",
        help="文字內容或圖片/影片說明"
    )
    parser.add_argument(
        "--file",
        help="單一檔案路徑（用於 photo 或 video）"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="多個檔案路徑（用於 photos）"
    )
    parser.add_argument(
        "--title",
        help="影片標題"
    )
    parser.add_argument(
        "--description",
        help="影片詳細描述"
    )

    args = parser.parse_args()

    # 驗證環境變數
    validate_credentials()

    try:
        # 根據類型執行對應功能
        if args.type == "text":
            post_text(args.message)

        elif args.type == "photo":
            post_photo(args.file, args.message)

        elif args.type == "photos":
            post_photos(args.files, args.message)

        elif args.type == "video":
            # 合併 message 和 description
            description = args.description or args.message
            post_video(args.file, description, args.title, description)

    except KeyboardInterrupt:
        print("\n\n⚠️  操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 發生錯誤: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
