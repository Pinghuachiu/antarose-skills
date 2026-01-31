#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post Script
發布貼文到 LinkedIn，支援文字、圖片、連結
"""

import os
import sys
import json
import time
import argparse
import requests
from typing import Optional, Dict, Any

# API 端點
LINKEDIN_API_BASE = "https://api.linkedin.com"
USERINFO_ENDPOINT = f"{LINKEDIN_API_BASE}/v2/userinfo"
POSTS_ENDPOINT = f"{LINKEDIN_API_BASE}/rest/posts"
ASSET_ENDPOINT = f"{LINKEDIN_API_BASE}/assets"

# MySQL 配置（從環境變數讀取）
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")


def get_channel_info(channel_id: int) -> Optional[Dict[str, Any]]:
    """從資料庫取得頻道資訊"""
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT channal_id, channal_name, page_id, access_token
        FROM channal_info
        WHERE channal_id = %s AND channal_source = 'linkedin'
        """

        cursor.execute(query, (channel_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result
    except Exception as e:
        print(f"❌ 資料庫查詢失敗: {e}")
        return None


def get_linkedin_profile(access_token: str) -> Optional[Dict[str, Any]]:
    """取得 LinkedIn 使用者資訊"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202503",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    try:
        print("🔍 正在取得 LinkedIn 使用者資訊...")
        response = requests.get(USERINFO_ENDPOINT, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        person_id = data.get("sub")

        if person_id:
            print(f"✅ LinkedIn Person ID: {person_id}")
            print(f"   姓名: {data.get('name', 'N/A')}")
            print(f"   URN: urn:li:person:{person_id}")
            return {
                "person_id": person_id,
                "urn": f"urn:li:person:{person_id}",
                "name": data.get("name"),
                "email": data.get("email")
            }
        else:
            print("❌ 無法取得 Person ID")
            return None

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 錯誤: {e}")
        print(f"   回應: {e.response.text if e.response else 'N/A'}")
        return None
    except Exception as e:
        print(f"❌ 取得使用者資訊失敗: {e}")
        return None


def register_image_upload(access_token: str) -> Optional[Dict[str, str]]:
    """註冊圖片上傳"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202503",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    # 註冊上傳請求
    register_data = {
        "registerUploadRequest": {
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-image"
            ],
            "owner": "urn:li:person:PLACEHOLDER",  # 稍後替換
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "asset": "urn:li:digitalmediaAsset:PLACEHOLDER"
                }
            ]
        }
    }

    try:
        print("📤 註冊圖片上傳...")
        response = requests.post(
            ASSET_ENDPOINT,
            headers=headers,
            params={"action": "registerUpload"},
            json=register_data,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        value = data.get("value", {})
        upload_url = value.get("uploadUrl")
        asset_urn = value.get("asset")

        if upload_url and asset_urn:
            print(f"✅ 上傳 URL 已取得")
            print(f"   Asset URN: {asset_urn}")
            return {
                "upload_url": upload_url,
                "asset_urn": asset_urn
            }
        else:
            print("❌ 無法取得上傳 URL")
            return None

    except requests.exceptions.HTTPError as e:
        print(f"❌ 註冊上傳失敗: {e}")
        print(f"   回應: {e.response.text if e.response else 'N/A'}")
        return None
    except Exception as e:
        print(f"❌ 註冊上傳失敗: {e}")
        return None


def upload_image_to_url(upload_url: str, image_url: str) -> bool:
    """上傳圖片到指定的 URL"""
    try:
        print(f"📥 正在下載圖片: {image_url}")
        # 先下載圖片
        img_response = requests.get(image_url, timeout=30)
        img_response.raise_for_status()

        image_data = img_response.content
        print(f"✅ 圖片已下載，大小: {len(image_data)} bytes")

        # 上傳到 LinkedIn
        print("📤 正在上傳圖片到 LinkedIn...")
        upload_headers = {
            "Authorization": f"Bearer {upload_url.split('?')[0].split('://')[-1].split('/')[0]}",  # 從 URL 提取
            "Content-Type": "application/octet-stream"
        }

        # LinkedIn 上傳 API 不需要 Authorization header
        upload_response = requests.put(
            upload_url,
            data=image_data,
            headers={"Content-Type": "application/octet-stream"},
            timeout=60
        )

        upload_response.raise_for_status()
        print("✅ 圖片上傳成功")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"❌ 圖片上傳失敗: {e}")
        return False
    except Exception as e:
        print(f"❌ 圖片上傳失敗: {e}")
        return False


def post_text(access_token: str, person_urn: str, text: str) -> bool:
    """發布純文字貼文"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202503",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    post_data = {
        "author": person_urn,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    try:
        print("📝 正在發布純文字貼文...")
        print(f"   內容: {text[:100]}{'...' if len(text) > 100 else ''}")

        response = requests.post(
            POSTS_ENDPOINT,
            headers=headers,
            json=post_data,
            timeout=30
        )

        response.raise_for_status()

        # LinkedIn API 可能返回空回應或非 JSON 回應
        try:
            data = response.json()
            post_id = data.get("id")
        except:
            # 如果回應不是 JSON，嘗試從 Location header 取得 post ID
            post_id = None

        if post_id:
            print(f"✅ 貼文發布成功！")
            print(f"   Post ID: {post_id}")
            print(f"   連結: https://www.linkedin.com/feed/update/{post_id}")
        else:
            # 檢查是否有 Location header
            location = response.headers.get("Location")
            if location:
                print(f"✅ 貼文發布成功！")
                print(f"   連結: {location}")
            else:
                print(f"✅ 貼文已發布（HTTP {response.status_code}）")

        return True

    except requests.exceptions.HTTPError as e:
        print(f"❌ 發布失敗: {e}")
        print(f"   回應: {e.response.text if e.response else 'N/A'}")
        return False
    except Exception as e:
        print(f"❌ 發布失敗: {e}")
        return False


def post_image(access_token: str, person_urn: str, text: str, image_url: str) -> bool:
    """發布圖片貼文"""
    try:
        # 1. 註冊上傳（先不指定 owner，稍後在貼文中指定）
        print("\n📋 步驟 1/3: 註冊圖片上傳")
        register_result = register_image_upload(access_token)
        if not register_result:
            return False

        upload_url = register_result["upload_url"]
        asset_urn = register_result["asset_urn"]

        # 2. 上傳圖片
        print("\n📋 步驟 2/3: 上傳圖片檔案")
        if not upload_image_to_url(upload_url, image_url):
            return False

        # 3. 發布貼文（包含圖片）
        print("\n📋 步驟 3/3: 發布貼文")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "LinkedIn-Version": "202503",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }

        post_data = {
            "author": person_urn,
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
            "content": {
                "media": {
                    "id": asset_urn
                }
            }
        }

        print(f"   內容: {text[:100]}{'...' if len(text) > 100 else ''}")
        print(f"   圖片 URN: {asset_urn}")

        response = requests.post(
            POSTS_ENDPOINT,
            headers=headers,
            json=post_data,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()
        post_id = data.get("id")

        if post_id:
            print(f"\n✅ 圖片貼文發布成功！")
            print(f"   Post ID: {post_id}")
            print(f"   連結: https://www.linkedin.com/feed/update/{post_id}")
            return True
        else:
            print("\n✅ 貼文已發布（無 Post ID）")
            return True

    except Exception as e:
        print(f"❌ 發布失敗: {e}")
        return False


def post_link(access_token: str, person_urn: str, text: str, link_url: str,
              link_title: Optional[str] = None, link_desc: Optional[str] = None) -> bool:
    """發布連結貼文"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202503",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    post_data = {
        "author": person_urn,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
        "content": {
            "article": {
                "url": link_url
            }
        }
    }

    # 可選：添加標題和描述
    if link_title:
        post_data["content"]["article"]["title"] = link_title
    if link_desc:
        post_data["content"]["article"]["description"] = link_desc

    try:
        print("🔗 正在發布連結貼文...")
        print(f"   內容: {text[:100]}{'...' if len(text) > 100 else ''}")
        print(f"   連結: {link_url}")

        response = requests.post(
            POSTS_ENDPOINT,
            headers=headers,
            json=post_data,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()
        post_id = data.get("id")

        if post_id:
            print(f"✅ 連結貼文發布成功！")
            print(f"   Post ID: {post_id}")
            print(f"   連結: https://www.linkedin.com/feed/update/{post_id}")
            return True
        else:
            print("✅ 貼文已發布（無 Post ID）")
            return True

    except requests.exceptions.HTTPError as e:
        print(f"❌ 發布失敗: {e}")
        print(f"   回應: {e.response.text if e.response else 'N/A'}")
        return False
    except Exception as e:
        print(f"❌ 發布失敗: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn Post Script - 發布貼文到 LinkedIn",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 取得 LinkedIn 使用者資訊
  python3 post.py --action get-profile --access-token "YOUR_TOKEN"

  # 發布純文字
  python3 post.py --action text --person-urn "urn:li:person:XXX" --access-token "TOKEN" --text "Hello!"

  # 從資料庫發布純文字
  python3 post.py --action text --from-db --channel-id 1 --text "Hello!"

  # 發布圖片
  python3 post.py --action image --from-db --channel-id 1 --text "Check this!" --image-url "https://..."

  # 發布連結
  python3 post.py --action link --from-db --channel-id 1 --text "Article!" --link-url "https://..."
        """
    )

    parser.add_argument("--action", required=True,
                        choices=["get-profile", "text", "image", "link"],
                        help="執行動作")

    # 手動指定參數
    parser.add_argument("--person-urn", help="LinkedIn Person URN (例如: urn:li:person:XXX)")
    parser.add_argument("--access-token", help="LinkedIn Access Token")

    # 資料庫參數
    parser.add_argument("--from-db", action="store_true", help="從資料庫讀取設定")
    parser.add_argument("--channel-id", type=int, help="資料庫頻道 ID")

    # 貼文內容
    parser.add_argument("--text", help="貼文文字內容")
    parser.add_argument("--image-url", help="圖片 URL（action=image 時）")
    parser.add_argument("--link-url", help="連結 URL（action=link 時）")
    parser.add_argument("--link-title", help="連結標題（action=link 時）")
    parser.add_argument("--link-desc", help="連結描述（action=link 時）")

    args = parser.parse_args()

    # 取得 access_token 和 person_urn
    access_token = None
    person_urn = None

    if args.from_db:
        # 從資料庫讀取
        if not args.channel_id:
            print("❌ 使用 --from-db 時必須指定 --channel-id")
            sys.exit(1)

        channel_info = get_channel_info(args.channel_id)
        if not channel_info:
            print(f"❌ 找不到頻道 ID {args.channel_id}")
            sys.exit(1)

        access_token = channel_info.get("access_token")
        page_id = channel_info.get("page_id")

        if not access_token:
            print("❌ 資料庫中沒有 access_token")
            sys.exit(1)

        # 嘗試從 page_id 取得 URN
        if page_id:
            if page_id.startswith("urn:li:person:"):
                person_urn = page_id
            else:
                person_urn = f"urn:li:person:{page_id}"

        print(f"✅ 從資料庫讀取頻道: {channel_info.get('channal_name')}")
        print(f"   Channel ID: {channel_info.get('channal_id')}")

    else:
        # 手動指定
        access_token = args.access_token
        person_urn = args.person_urn

        if not access_token:
            print("❌ 必須指定 --access-token 或使用 --from-db")
            sys.exit(1)

    # 執行動作
    if args.action == "get-profile":
        # 取得使用者資訊
        profile = get_linkedin_profile(access_token)
        if profile:
            print("\n✅ 成功取得使用者資訊")
            print(json.dumps(profile, indent=2, ensure_ascii=False))
            sys.exit(0)
        else:
            print("\n❌ 取得使用者資訊失敗")
            sys.exit(1)

    # 如果沒有 person_URN，自動取得
    if not person_urn:
        print("⚠️  沒有 LinkedIn Person URN，嘗試自動取得...")
        profile = get_linkedin_profile(access_token)
        if profile:
            person_urn = profile["urn"]
        else:
            print("❌ 無法自動取得 Person URN，請使用 --person-urn 指定")
            sys.exit(1)

    # 發布貼文
    success = False

    if args.action == "text":
        if not args.text:
            print("❌ action=text 需要指定 --text")
            sys.exit(1)
        success = post_text(access_token, person_urn, args.text)

    elif args.action == "image":
        if not args.text:
            print("❌ action=image 需要指定 --text")
            sys.exit(1)
        if not args.image_url:
            print("❌ action=image 需要指定 --image-url")
            sys.exit(1)
        success = post_image(access_token, person_urn, args.text, args.image_url)

    elif args.action == "link":
        if not args.text:
            print("❌ action=link 需要指定 --text")
            sys.exit(1)
        if not args.link_url:
            print("❌ action=link 需要指定 --link-url")
            sys.exit(1)
        success = post_link(
            access_token, person_urn, args.text, args.link_url,
            args.link_title, args.link_desc
        )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
