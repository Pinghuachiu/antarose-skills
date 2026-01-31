#!/usr/bin/env python3
"""
Instagram Post - Instagram 貼文發布技能
支援文字、圖片、影片發布到 Instagram

與 Facebook 不同：
- Instagram 使用 Instagram Graph API
- 可以直接使用資料庫中的 token（無需換取 Page Token）
- 支援單圖、多圖（Carousel）、影片
- 需要使用 Instagram Business Account 或 Creator Account
"""

import os
import sys
import json
import argparse
import requests
from typing import Dict, Optional, List
from datetime import datetime


class InstagramPoster:
    """Instagram 貼文發布器"""

    def __init__(self):
        self.graph_api_version = "v24.0"
        self.base_url = f"https://graph.facebook.com/{self.graph_api_version}"

    def post_photo(self, instagram_business_id: str, access_token: str,
                  image_url: str, caption: str) -> Dict:
        """
        發布單張圖片到 Instagram

        參數：
            instagram_business_id: Instagram 商業帳號 ID
            access_token: Access Token（直接從資料庫讀取，無需換取）
            image_url: 圖片 URL
            caption: 圖片說明文字

        返回：
            {
                "success": True/False,
                "media_id": "Instagram 媒體 ID",
                "post_url": "貼文連結",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        print("📸 正在發布單張圖片到 Instagram...")

        try:
            # 第一步：建立 Container
            container_url = f"{self.base_url}/{instagram_business_id}/media"
            container_data = {
                "image_url": image_url,
                "caption": caption,
                "access_token": access_token
            }

            print("   1️⃣ 建立圖片 Container...")
            container_response = requests.post(container_url, data=container_data, timeout=30)

            if container_response.status_code != 200:
                error_data = container_response.json()
                return {
                    "success": False,
                    "error": f"建立 Container 失敗: {error_data.get('error', {}).get('message', container_response.text)}"
                }

            container_result = container_response.json()

            if "id" not in container_result:
                return {
                    "success": False,
                    "error": f"Container 回應中沒有 ID: {container_result}"
                }

            container_id = container_result["id"]
            print(f"   ✅ Container ID: {container_id}")

            # 第二步：檢查 Container 狀態
            print("   2️⃣ 檢查 Container 狀態...")
            import time
            max_attempts = 10
            attempt = 0

            while attempt < max_attempts:
                status_result = self.check_container_status(
                    instagram_business_id, container_id, access_token
                )

                if not status_result["success"]:
                    return {"success": False, "error": f"檢查狀態失敗: {status_result['error']}"}

                if status_result["is_ready"]:
                    break

                attempt += 1
                if attempt < max_attempts:
                    print(f"      ⏳ 等待 5 秒後重試... ({attempt}/{max_attempts})")
                    time.sleep(5)

            if attempt >= max_attempts:
                return {
                    "success": False,
                    "error": f"Container 未能在 {max_attempts * 5} 秒內準備好，最後狀態: {status_result.get('status_code', 'UNKNOWN')}"
                }

            # 第三步：發布 Container
            publish_url = f"{self.base_url}/{instagram_business_id}/media_publish"
            publish_data = {
                "creation_id": container_id,
                "access_token": access_token
            }

            print("   3️⃣ 發布 Container...")
            publish_response = requests.post(publish_url, data=publish_data, timeout=30)

            if publish_response.status_code != 200:
                error_data = publish_response.json()
                return {
                    "success": False,
                    "error": f"發布失敗: {error_data.get('error', {}).get('message', publish_response.text)}"
                }

            publish_result = publish_response.json()

            if "id" in publish_result:
                return {
                    "success": True,
                    "media_id": publish_result["id"],
                    "post_url": f"https://www.instagram.com/p/{publish_result['id']}/"
                }
            else:
                return {
                    "success": False,
                    "error": f"發布回應中沒有 ID: {publish_result}"
                }

        except requests.exceptions.Timeout:
            return {"success": False, "error": "請求超時"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def post_video(self, instagram_business_id: str, access_token: str,
                   video_url: str, caption: str) -> Dict:
        """
        發布影片到 Instagram

        參數：
            instagram_business_id: Instagram 商業帳號 ID
            access_token: Access Token
            video_url: 影片 URL（MP4 格式）
            caption: 影片說明文字

        返回：
            {
                "success": True/False,
                "media_id": "Instagram 媒體 ID",
                "post_url": "貼文連結",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        print("🎬 正在發布影片到 Instagram...")

        try:
            # 第一步：建立 Container
            container_url = f"{self.base_url}/{instagram_business_id}/media"
            container_data = {
                "video_url": video_url,
                "caption": caption,
                "access_token": access_token
            }

            print("   1️⃣ 建立影片 Container...")
            container_response = requests.post(container_url, data=container_data, timeout=60)

            if container_response.status_code != 200:
                error_data = container_response.json()
                return {
                    "success": False,
                    "error": f"建立 Container 失敗: {error_data.get('error', {}).get('message', container_response.text)}"
                }

            container_result = container_response.json()

            if "id" not in container_result:
                return {
                    "success": False,
                    "error": f"Container 回應中沒有 ID: {container_result}"
                }

            container_id = container_result["id"]
            print(f"   ✅ Container ID: {container_id}")

            # 第二步：檢查狀態（影片需要處理時間）
            print("   2️⃣ 等待影片處理...")
            status_code = self._wait_for_container_status(
                instagram_business_id, container_id, access_token
            )

            if status_code != "FINISHED":
                return {
                    "success": False,
                    "error": f"影片處理失敗，狀態: {status_code}"
                }

            # 第三步：發布 Container
            publish_url = f"{self.base_url}/{instagram_business_id}/media_publish"
            publish_data = {
                "creation_id": container_id,
                "access_token": access_token
            }

            print("   3️⃣ 發布影片...")
            publish_response = requests.post(publish_url, data=publish_data, timeout=30)

            if publish_response.status_code != 200:
                error_data = publish_response.json()
                return {
                    "success": False,
                    "error": f"發布失敗: {error_data.get('error', {}).get('message', publish_response.text)}"
                }

            publish_result = publish_response.json()

            if "id" in publish_result:
                return {
                    "success": True,
                    "media_id": publish_result["id"],
                    "post_url": f"https://www.instagram.com/p/{publish_result['id']}/"
                }
            else:
                return {
                    "success": False,
                    "error": f"發布回應中沒有 ID: {publish_result}"
                }

        except requests.exceptions.Timeout:
            return {"success": False, "error": "請求超時（影片上傳可能需要更長時間）"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def post_carousel(self, instagram_business_id: str, access_token: str,
                      image_urls: List[str], caption: str) -> Dict:
        """
        發布多張圖片（Carousel）到 Instagram

        參數：
            instagram_business_id: Instagram 商業帳號 ID
            access_token: Access Token
            image_urls: 圖片 URL 列表（2-10 張）
            caption: 圖片說明文字

        返回：
            {
                "success": True/False,
                "media_id": "Instagram 媒體 ID",
                "post_url": "貼文連結",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        if len(image_urls) < 2 or len(image_urls) > 10:
            return {
                "success": False,
                "error": "Carousel 需要 2-10 張圖片"
            }

        print(f"📊 正在發布 Carousel（{len(image_urls)} 張圖片）到 Instagram...")

        try:
            # 第一步：為每張圖片建立 Container
            container_ids = []
            for i, image_url in enumerate(image_urls, 1):
                container_url = f"{self.base_url}/{instagram_business_id}/media"
                container_data = {
                    "image_url": image_url,
                    "is_carousel_item": "true",
                    "access_token": access_token
                }

                print(f"   {i}️⃣ 建立圖片 Container {i}/{len(image_urls)}...")
                container_response = requests.post(container_url, data=container_data, timeout=30)

                if container_response.status_code != 200:
                    error_data = container_response.json()
                    return {
                        "success": False,
                        "error": f"圖片 {i} 建立 Container 失敗: {error_data.get('error', {}).get('message', container_response.text)}"
                    }

                container_result = container_response.json()

                if "id" not in container_result:
                    return {
                        "success": False,
                        "error": f"圖片 {i} Container 回應中沒有 ID: {container_result}"
                    }

                container_ids.append(container_result["id"])
                print(f"      ✅ Container ID: {container_result['id']}")

            # 第二步：建立 Carousel Container
            carousel_url = f"{self.base_url}/{instagram_business_id}/media"
            carousel_data = {
                "media_type": "CAROUSEL",
                "children": ",".join(container_ids),
                "caption": caption,
                "access_token": access_token
            }

            print("   📦 建立 Carousel Container...")
            carousel_response = requests.post(carousel_url, data=carousel_data, timeout=30)

            if carousel_response.status_code != 200:
                error_data = carousel_response.json()
                return {
                    "success": False,
                    "error": f"建立 Carousel Container 失敗: {error_data.get('error', {}).get('message', carousel_response.text)}"
                }

            carousel_result = carousel_response.json()

            if "id" not in carousel_result:
                return {
                    "success": False,
                    "error": f"Carousel 回應中沒有 ID: {carousel_result}"
                }

            carousel_container_id = carousel_result["id"]
            print(f"   ✅ Carousel Container ID: {carousel_container_id}")

            # 第三步：發布 Carousel
            publish_url = f"{self.base_url}/{instagram_business_id}/media_publish"
            publish_data = {
                "creation_id": carousel_container_id,
                "access_token": access_token
            }

            print("   🚀 發布 Carousel...")
            publish_response = requests.post(publish_url, data=publish_data, timeout=30)

            if publish_response.status_code != 200:
                error_data = publish_response.json()
                return {
                    "success": False,
                    "error": f"發布失敗: {error_data.get('error', {}).get('message', publish_response.text)}"
                }

            publish_result = publish_response.json()

            if "id" in publish_result:
                return {
                    "success": True,
                    "media_id": publish_result["id"],
                    "post_url": f"https://www.instagram.com/p/{publish_result['id']}/"
                }
            else:
                return {
                    "success": False,
                    "error": f"發布回應中沒有 ID: {publish_result}"
                }

        except requests.exceptions.Timeout:
            return {"success": False, "error": "請求超時"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_container_status(self, instagram_business_id: str,
                             container_id: str, access_token: str) -> Dict:
        """
        檢查 Container 處理狀態

        參數：
            instagram_business_id: Instagram 商業帳號 ID
            container_id: Container ID
            access_token: Access Token

        返回：
            {
                "success": True/False,
                "status_code": "FINISHED"/"IN_PROGRESS"/"ERROR"/"PUBLISHED"/"EXPIRED",
                "is_ready": True/False,
                "error": "錯誤訊息（如果失敗）"
            }
        """
        print(f"   🔍 檢查 Container {container_id} 狀態...")

        try:
            # 直接查詢 Container ID 的狀態
            status_url = f"{self.base_url}/{container_id}"
            params = {
                "fields": "status_code",
                "access_token": access_token
            }

            response = requests.get(status_url, params=params, timeout=10)

            if response.status_code != 200:
                error_data = response.json()
                return {
                    "success": False,
                    "error": f"檢查失敗: {error_data.get('error', {}).get('message', response.text)}"
                }

            result = response.json()
            status_code = result.get("status_code", "UNKNOWN")

            # 判斷是否 ready
            is_ready = status_code in ["FINISHED", "PUBLISHED"]

            print(f"      狀態: {status_code}")
            if is_ready:
                print("      ✅ Container 已準備好")
            else:
                print("      ⏳ Container 尚未準備好")

            return {
                "success": True,
                "status_code": status_code,
                "is_ready": is_ready,
                "error": None
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _wait_for_container_status(self, instagram_business_id: str,
                                  container_id: str, access_token: str,
                                  max_wait: int = 300) -> str:
        """
        等待 Container 處理完成（用於影片）

        返回：status_code (FINISHED, ERROR, 或其他)
        """
        import time

        status_url = f"{self.base_url}/{instagram_business_id}/media"
        params = {
            "fields": "status_code",
            "access_token": access_token
        }

        waited = 0
        while waited < max_wait:
            response = requests.get(status_url, params=params, timeout=10)

            if response.status_code == 200:
                result = response.json()
                status_code = result.get("status_code")

                if status_code == "FINISHED":
                    print("      ✅ 影片處理完成")
                    return status_code
                elif status_code == "ERROR":
                    print(f"      ❌ 影片處理錯誤: {result}")
                    return status_code
                elif status_code == "IN_PROGRESS":
                    print(f"      ⏳ 處理中... ({waited}s)")
                elif status_code == "PUBLISHED":
                    print("      ✅ 已發布")
                    return "FINISHED"
                else:
                    print(f"      ⏳ 狀態: {status_code}")

            time.sleep(5)
            waited += 5

        return "TIMEOUT"

    def get_instagram_business_account(self, page_id: str, access_token: str) -> Dict:
        """
        取得 Instagram 商業帳號 ID

        參數：
            page_id: Facebook 頁面 ID
            access_token: Access Token

        返回：
            {
                "success": True/False,
                "instagram_business_id": "Instagram 商業帳號 ID",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        print("🔍 正在取得 Instagram 商業帳號 ID...")

        try:
            url = f"{self.base_url}/{page_id}"
            params = {
                "fields": "instagram_business_account",
                "access_token": access_token
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                error_data = response.json()
                return {
                    "success": False,
                    "error": f"取得失敗: {error_data.get('error', {}).get('message', response.text)}"
                }

            result = response.json()

            if "instagram_business_account" in result:
                ig_data = result["instagram_business_account"]
                if "id" in ig_data:
                    print(f"   ✅ Instagram 商業帳號 ID: {ig_data['id']}")
                    return {
                        "success": True,
                        "instagram_business_id": ig_data["id"]
                    }

            return {
                "success": False,
                "error": "此 Facebook 頁面沒有連接 Instagram 商業帳號"
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Instagram 貼文發布工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 發布單張圖片
  python3 instagram-post.py --action photo --caption "Hello Instagram!" --image-url "https://example.com/photo.jpg"

  # 發布影片
  python3 instagram-post.py --action video --caption "Check this out!" --video-url "https://example.com/video.mp4"

  # 發布 Carousel（多張圖片）
  python3 instagram-post.py --action carousel --caption "Multiple photos" --image-urls "url1,url2,url3"

  # 從資料庫讀取並發布
  python3 instagram-post.py --action photo --from-db --caption "Hello!" --image-url "https://..."
        """
    )

    parser.add_argument("--action", required=True,
                       choices=["photo", "video", "carousel", "get-ig-id"],
                       help="執行動作")
    parser.add_argument("--instagram-business-id", help="Instagram 商業帳號 ID")
    parser.add_argument("--page-id", help="Facebook 頁面 ID（用於取得 Instagram 帳號）")
    parser.add_argument("--access-token", help="Access Token")
    parser.add_argument("--caption", help="貼文說明文字")
    parser.add_argument("--image-url", help="單張圖片 URL")
    parser.add_argument("--video-url", help="影片 URL")
    parser.add_argument("--image-urls", help="多張圖片 URL（逗號分隔）")

    # 資料庫相關參數
    parser.add_argument("--from-db", action="store_true", help="從資料庫讀取設定")
    parser.add_argument("--channel-id", type=int, help="資料庫中的頻道 ID")
    parser.add_argument("--mysql-host", default="192.168.1.159", help="MySQL 主機")
    parser.add_argument("--mysql-user", default="n8n", help="MySQL 使用者")
    parser.add_argument("--mysql-password", default="!!asshole!!asshole", help="MySQL 密碼")
    parser.add_argument("--mysql-database", default="infoCollection", help="MySQL 資料庫")

    args = parser.parse_args()

    poster = InstagramPoster()

    # 從資料庫讀取設定
    if args.from_db:
        if not args.channel_id:
            print("❌ 錯誤：--channel-id 是必需的")
            return 1

        try:
            import mysql.connector

            conn = mysql.connector.connect(
                host=args.mysql_host,
                user=args.mysql_user,
                password=args.mysql_password,
                database=args.mysql_database
            )

            cursor = conn.cursor(dictionary=True)

            # 查詢頻道資訊
            cursor.execute(
                "SELECT page_id, access_token FROM channal_info WHERE channal_id = %s",
                (args.channel_id,)
            )
            channel = cursor.fetchone()

            if not channel:
                print(f"❌ 錯誤：找不到頻道 ID {args.channel_id}")
                cursor.close()
                conn.close()
                return 1

            args.page_id = channel["page_id"]
            args.access_token = channel["access_token"]

            cursor.close()
            conn.close()

            print(f"✅ 從資料庫讀取頻道 {args.channel_id} 的設定")

        except Exception as e:
            print(f"❌ 資料庫錯誤：{e}")
            return 1

    # 如果沒有 Instagram Business ID，嘗試從 Page ID 取得
    if not args.instagram_business_id and args.page_id:
        print("💡 沒有 Instagram Business ID，嘗試從 Facebook 頁面取得...")
        ig_result = poster.get_instagram_business_account(args.page_id, args.access_token)

        if not ig_result["success"]:
            print(f"❌ 取得 Instagram 商業帳號失敗：{ig_result['error']}")
            print("\n💡 提示：請確保您的 Facebook 頁面已連接到 Instagram 商業帳號")
            return 1

        args.instagram_business_id = ig_result["instagram_business_id"]

    # 執行動作
    if args.action == "get-ig-id":
        if not args.page_id or not args.access_token:
            print("❌ 錯誤：--page-id 和 --access-token 是必需的")
            return 1

        result = poster.get_instagram_business_account(args.page_id, args.access_token)
        if result["success"]:
            print(f"\n✅ Instagram 商業帳號 ID: {result['instagram_business_id']}")
            return 0
        else:
            print(f"\n❌ 錯誤：{result['error']}")
            return 1

    elif args.action == "photo":
        if not args.instagram_business_id or not args.access_token:
            print("❌ 錯誤：--instagram-business-id 和 --access-token 是必需的")
            return 1
        if not args.caption or not args.image_url:
            print("❌ 錯誤：--caption 和 --image-url 是必需的")
            return 1

        result = poster.post_photo(
            args.instagram_business_id,
            args.access_token,
            args.image_url,
            args.caption
        )

    elif args.action == "video":
        if not args.instagram_business_id or not args.access_token:
            print("❌ 錯誤：--instagram-business-id 和 --access-token 是必需的")
            return 1
        if not args.caption or not args.video_url:
            print("❌ 錯誤：--caption 和 --video-url 是必需的")
            return 1

        result = poster.post_video(
            args.instagram_business_id,
            args.access_token,
            args.video_url,
            args.caption
        )

    elif args.action == "carousel":
        if not args.instagram_business_id or not args.access_token:
            print("❌ 錯誤：--instagram-business-id 和 --access-token 是必需的")
            return 1
        if not args.caption or not args.image_urls:
            print("❌ 錯誤：--caption 和 --image-urls 是必需的")
            return 1

        image_urls = [url.strip() for url in args.image_urls.split(",")]
        result = poster.post_carousel(
            args.instagram_business_id,
            args.access_token,
            image_urls,
            args.caption
        )

    # 輸出結果
    if result["success"]:
        print("\n✅ 成功發布到 Instagram！")
        print(f"📱 媒體 ID: {result['media_id']}")
        print(f"🔗 貼文連結: {result['post_url']}")
        return 0
    else:
        print(f"\n❌ 發布失敗：{result['error']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
