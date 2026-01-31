#!/usr/bin/env python3
"""
Threads 貼文發布工具
支援文字、圖片、影片發布

根據 Meta 官方文檔：
https://developers.facebook.com/docs/threads/posts

發布流程是兩步驟：
1. Step 1: Create Container (POST /{threads-user-id}/threads)
2. Step 2: Publish Container (POST /{threads-user-id}/threads_publish)

官方建議等待平均 30 秒再發布，讓伺服器有足夠時間處理。
"""

import argparse
import sys
import time
import requests
from typing import Dict


class ThreadsPoster:
    """Threads API 貼文發布器"""

    def __init__(self):
        self.graph_api_version = "v1.0"
        self.base_url = f"https://graph.threads.net/{self.graph_api_version}"

    def post_text(self, threads_user_id: str, access_token: str,
                  text: str) -> Dict:
        """
        發布純文字貼文到 Threads

        參數：
            threads_user_id: Threads User ID
            access_token: Access Token（THAA... 開頭的 Threads User Token）
            text: 貼文文字（最多 500 字符）

        返回：
            {
                "success": True/False,
                "media_id": "Threads 媒體 ID",
                "permalink": "貼文連結",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        print("📝 正在發布純文字貼文到 Threads...")

        # Threads 文字限制 500 字符
        if len(text) > 500:
            print(f"⚠️  警告：文字超過 500 字符，將自動截斷（目前：{len(text)} 字符）")
            text = text[:500]

        try:
            # Step 1: 建立 Container（使用 form-urlencoded body，與 n8n 一致）
            container_url = f"{self.base_url}/{threads_user_id}/threads"
            container_data = {
                "media_type": "TEXT",
                "text": text,
                "access_token": access_token
            }

            print(f"   📄 文字內容：{text[:100]}{'...' if len(text) > 100 else ''}")
            print("   1️⃣ 建立 Container...")

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

            # Step 2: 短暫等待後發布（文字建議等待 5 秒）
            print("   2️⃣ 等待 5 秒...")
            time.sleep(5)

            publish_url = f"{self.base_url}/{threads_user_id}/threads_publish"
            publish_data = {
                "creation_id": container_id,
                "access_token": access_token
            }

            print("   3️⃣ 發布貼文...")
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
                    "permalink": f"https://www.threads.net/t/{publish_result['id']}"
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

    def post_image(self, threads_user_id: str, access_token: str,
                   image_url: str, text: str = "") -> Dict:
        """
        發布單張圖片貼文到 Threads（兩步驟，不使用 Carousel）

        單張圖片發布流程：
        1. Create Container (media_type=IMAGE)
        2. Wait and Publish

        註：多張圖片請使用 post_carousel 方法

        參數：
            threads_user_id: Threads User ID
            access_token: Access Token
            image_url: 圖片 URL（必須是公開可訪問的 URL）
            text: 貼文文字（可選，最多 500 字符）

        返回：
            {
                "success": True/False,
                "media_id": "Threads 媒體 ID",
                "permalink": "貼文連結",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        print("📸 正在發布單張圖片貼文到 Threads...")

        if text and len(text) > 500:
            print(f"⚠️  警告：文字超過 500 字符，將自動截斷")
            text = text[:500]

        try:
            # Step 1: 建立 Container（單張圖片用 media_type=IMAGE，不使用 Carousel）
            container_url = f"{self.base_url}/{threads_user_id}/threads"
            container_data = {
                "media_type": "IMAGE",
                "image_url": image_url,
                "access_token": access_token
            }

            # 如果有文字，加入 text
            if text:
                container_data["text"] = text
                print(f"   📄 文字：{text[:100]}{'...' if len(text) > 100 else ''}")

            print(f"   🖼️  圖片 URL：{image_url}")
            print("   1️⃣ 建立 Container...")

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
            print(f"      ✅ Container ID: {container_id}")

            # Step 2: 等待 30 秒讓伺服器處理（官方建議）
            print("   2️⃣ 等待 30 秒讓伺服器處理...")
            time.sleep(30)

            publish_url = f"{self.base_url}/{threads_user_id}/threads_publish"
            publish_data = {
                "creation_id": container_id,
                "access_token": access_token
            }

            print("   3️⃣ 發布貼文...")
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
                    "permalink": f"https://www.threads.net/t/{publish_result['id']}"
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

    def post_video(self, threads_user_id: str, access_token: str,
                   video_url: str, text: str = "") -> Dict:
        """
        發布影片貼文到 Threads

        參數：
            threads_user_id: Threads User ID
            access_token: Access Token
            video_url: 影片 URL（必須是公開可訪問的 URL，MP4/MOV 格式）
            text: 貼文文字（可選，最多 500 字符）

        返回：
            {
                "success": True/False,
                "media_id": "Threads 媒體 ID",
                "permalink": "貼文連結",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        print("🎬 正在發布影片貼文到 Threads...")

        if text and len(text) > 500:
            print(f"⚠️  警告：文字超過 500 字符，將自動截斷")
            text = text[:500]

        try:
            # Step 1: 建立 Container（使用 form-urlencoded body，與 n8n 一致）
            container_url = f"{self.base_url}/{threads_user_id}/threads"
            container_data = {
                "media_type": "VIDEO",
                "video_url": video_url,
                "access_token": access_token
            }

            # 如果有文字，加入 text
            if text:
                container_data["text"] = text
                print(f"   📄 文字：{text[:100]}{'...' if len(text) > 100 else ''}")

            print(f"   🎥 影片 URL：{video_url}")
            print("   1️⃣ 建立 Container...")

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

            # Step 2: 等待影片處理完成（官方建議平均 30 秒）
            print("   2️⃣ 等待 30 秒讓伺服器處理影片...")
            time.sleep(30)

            publish_url = f"{self.base_url}/{threads_user_id}/threads_publish"
            publish_data = {
                "creation_id": container_id,
                "access_token": access_token
            }

            print("   3️⃣ 發布貼文...")
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
                    "permalink": f"https://www.threads.net/t/{publish_result['id']}"
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

    def post_carousel(self, threads_user_id: str, access_token: str,
                      media_items: list, text: str = "") -> Dict:
        """
        發布輪播貼文到 Threads（支援多圖、多影片、混合）

        參數：
            threads_user_id: Threads User ID
            access_token: Access Token
            media_items: 媒體項目列表，每個項目是 dict：
                [
                    {"type": "IMAGE", "url": "https://..."},
                    {"type": "VIDEO", "url": "https://..."},
                    {"type": "IMAGE", "url": "https://..."}
                ]
            text: 貼文文字（可選，最多 500 字符）

        返回：
            {
                "success": True/False,
                "media_id": "Threads 媒體 ID",
                "permalink": "貼文連結",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        print("🎠 正在發布輪播貼文到 Threads...")

        if len(media_items) < 2:
            return {"success": False, "error": "輪播至少需要 2 個媒體項目"}
        if len(media_items) > 20:
            return {"success": False, "error": "輪播最多支援 20 個媒體項目"}

        if text and len(text) > 500:
            print(f"⚠️  警告：文字超過 500 字符，將自動截斷")
            text = text[:500]

        try:
            # Step 1: 為每個媒體項目建立 Container
            print(f"   1️⃣ 建立 {len(media_items)} 個媒體 Container...")
            container_ids = []

            for i, item in enumerate(media_items, 1):
                media_type = item.get("type", "IMAGE")
                media_url = item.get("url", "")

                if not media_url:
                    return {"success": False, "error": f"第 {i} 個媒體項目缺少 URL"}

                container_url = f"{self.base_url}/{threads_user_id}/threads"
                container_data = {
                    "media_type": media_type,
                    "is_carousel_item": "true",
                    "access_token": access_token
                }

                if media_type == "IMAGE":
                    container_data["image_url"] = media_url
                    print(f"      🖼️  圖片 {i}/{len(media_items)}: {media_url[:50]}...")
                elif media_type == "VIDEO":
                    container_data["video_url"] = media_url
                    print(f"      🎥 影片 {i}/{len(media_items)}: {media_url[:50]}...")
                else:
                    return {"success": False, "error": f"不支援的媒體類型: {media_type}"}

                container_response = requests.post(container_url, data=container_data, timeout=60)

                if container_response.status_code != 200:
                    error_data = container_response.json()
                    return {
                        "success": False,
                        "error": f"第 {i} 個 Container 建立失敗: {error_data.get('error', {}).get('message', container_response.text)}"
                    }

                container_result = container_response.json()

                if "id" not in container_result:
                    return {
                        "success": False,
                        "error": f"第 {i} 個 Container 回應中沒有 ID: {container_result}"
                    }

                container_id = container_result["id"]
                container_ids.append(container_id)
                print(f"         ✅ Container ID: {container_id}")

            # Step 2: 建立 Carousel Container
            print("   2️⃣ 建立 Carousel Container...")

            carousel_url = f"{self.base_url}/{threads_user_id}/threads"
            carousel_data = {
                "media_type": "CAROUSEL",
                "children": container_ids,  # 使用陣列格式
                "access_token": access_token
            }

            if text:
                carousel_data["text"] = text
                print(f"      📄 文字：{text[:100]}{'...' if len(text) > 100 else ''}")

            print(f"      📦 發送的 children: {container_ids}")
            carousel_response = requests.post(carousel_url, json=carousel_data, timeout=30)

            if carousel_response.status_code != 200:
                error_data = carousel_response.json()
                return {
                    "success": False,
                    "error": f"Carousel Container 建立失敗: {error_data.get('error', {}).get('message', carousel_response.text)}"
                }

            carousel_result = carousel_response.json()

            if "id" not in carousel_result:
                return {
                    "success": False,
                    "error": f"Carousel Container 回應中沒有 ID: {carousel_result}"
                }

            carousel_container_id = carousel_result["id"]
            print(f"      ✅ Carousel Container ID: {carousel_container_id}")

            # Step 3: 等待 30 秒後發布
            print("   3️⃣ 等待 30 秒讓伺服器處理...")
            time.sleep(30)

            publish_url = f"{self.base_url}/{threads_user_id}/threads_publish"
            publish_data = {
                "creation_id": carousel_container_id,
                "access_token": access_token
            }

            print("   4️⃣ 發布輪播貼文...")
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
                    "permalink": f"https://www.threads.net/t/{publish_result['id']}"
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

    def get_threads_user_id(self, access_token: str) -> Dict:
        """
        直接取得 Threads User ID（推薦方法）

        參數：
            access_token: Access Token（從資料庫的 access_token 欄位）

        返回：
            {
                "success": True/False,
                "threads_user_id": "Threads User ID",
                "username": "Threads 使用者名稱",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        print("🔍 正在取得 Threads User ID...")

        try:
            url = f"{self.base_url}/me"
            params = {
                "fields": "id,username",
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

            if "id" in result:
                print(f"   ✅ Threads User ID: {result['id']}")
                print(f"   👤 使用者名稱: {result.get('username', 'N/A')}")
                return {
                    "success": True,
                    "threads_user_id": result["id"],
                    "username": result.get("username", "")
                }
            else:
                return {
                    "success": False,
                    "error": f"回應中沒有 ID: {result}"
                }

        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Threads 貼文發布工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 取得 Threads User ID（推薦）
  python3 post.py --action get-threads-user-id --from-db --channel-id 3

  # 發布純文字
  python3 post.py --action text --from-db --channel-id 3 --text "Hello Threads! 🧵"

  # 發布單張圖片
  python3 post.py --action image --from-db --channel-id 3 --text "Check this!" --image-url "https://example.com/photo.jpg"

  # 發布單個影片
  python3 post.py --action video --from-db --channel-id 3 --text "Amazing!" --video-url "https://example.com/video.mp4"

  # 發布輪播（多圖、多影片、混合）
  python3 post.py --action carousel --from-db --channel-id 3 --text "Carousel post!" --image-urls "url1,url2" --video-urls "url3"

  # 使用 JSON 格式指定輪播媒體
  python3 post.py --action carousel --from-db --channel-id 3 --media-items '[{"type":"IMAGE","url":"url1"},{"type":"VIDEO","url":"url2"}]'
        """
    )

    parser.add_argument("--action", required=True,
                       choices=["text", "image", "video", "carousel", "get-threads-user-id"],
                       help="執行動作")
    parser.add_argument("--threads-user-id", help="Threads User ID（使用 /me 端點取得）")
    parser.add_argument("--access-token", help="Access Token")
    parser.add_argument("--text", help="貼文文字（最多 500 字符）")
    parser.add_argument("--image-url", help="單張圖片 URL（必須是公開可訪問的）")
    parser.add_argument("--video-url", help="單個影片 URL（必須是公開可訪問的）")

    # 輪播相關參數
    parser.add_argument("--image-urls", help="多張圖片 URL（用逗號分隔）")
    parser.add_argument("--video-urls", help="多個影片 URL（用逗號分隔）")
    parser.add_argument("--media-items", help="JSON 格式的媒體項目列表")

    # 資料庫相關參數
    parser.add_argument("--from-db", action="store_true", help="從資料庫讀取設定")
    parser.add_argument("--channel-id", type=int, help="資料庫中的頻道 ID")
    parser.add_argument("--mysql-host", default="192.168.1.159", help="MySQL 主機")
    parser.add_argument("--mysql-user", default="n8n", help="MySQL 使用者")
    parser.add_argument("--mysql-password", default="!!asshole!!asshole", help="MySQL 密碼")
    parser.add_argument("--mysql-database", default="infoCollection", help="MySQL 資料庫")

    args = parser.parse_args()

    poster = ThreadsPoster()

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

            # 查詢頻道資訊 - Token 在 access_token 欄位
            cursor.execute(
                "SELECT access_token FROM channal_info WHERE channal_id = %s",
                (args.channel_id,)
            )
            channel = cursor.fetchone()

            if not channel:
                print(f"❌ 錯誤：找不到頻道 ID {args.channel_id}")
                cursor.close()
                conn.close()
                return 1

            args.access_token = channel["access_token"]

            cursor.close()
            conn.close()

            print(f"✅ 從資料庫讀取頻道 {args.channel_id} 的設定\n")

        except Exception as e:
            print(f"❌ 資料庫錯誤：{e}")
            return 1

    # 執行動作
    if args.action == "get-threads-user-id":
        if not args.access_token:
            print("❌ 錯誤：--access-token 是必需的")
            return 1

        result = poster.get_threads_user_id(args.access_token)
        if result["success"]:
            print(f"\n✅ Threads User ID: {result['threads_user_id']}")
            if result.get("username"):
                print(f"👤 使用者名稱: {result['username']}")
            return 0
        else:
            print(f"\n❌ 錯誤：{result['error']}")
            return 1

    # 發布貼文動作 - 決定使用哪個 ID
    threads_id = args.threads_user_id

    if not threads_id:
        # 如果沒有提供，自動從 Token 取得
        if args.access_token:
            print("💡 沒有提供 Threads ID，自動從 Token 取得...")
            id_result = poster.get_threads_user_id(args.access_token)
            if id_result["success"]:
                threads_id = id_result["threads_user_id"]
                print(f"✅ 自動取得 Threads User ID: {threads_id}\n")
            else:
                print(f"❌ 無法自動取得 Threads ID: {id_result['error']}")
                print("\n💡 提示：請使用 --action get-threads-user-id 先取得 Threads User ID")
                return 1
        else:
            print("❌ 錯誤：需要提供 --threads-user-id 或 --access-token")
            return 1

    if not args.access_token:
        print("❌ 錯誤：--access-token 是必需的")
        return 1

    if args.action == "text":
        if not args.text:
            print("❌ 錯誤：--text 是必需的")
            return 1

        result = poster.post_text(threads_id, args.access_token, args.text)

    elif args.action == "image":
        if not args.image_url:
            print("❌ 錯誤：--image-url 是必需的")
            return 1

        result = poster.post_image(threads_id, args.access_token, args.image_url, args.text or "")

    elif args.action == "video":
        if not args.video_url:
            print("❌ 錯誤：--video-url 是必需的")
            return 1

        result = poster.post_video(threads_id, args.access_token, args.video_url, args.text or "")

    elif args.action == "carousel":
        # 構建媒體項目列表
        media_items = []

        # 如果提供了 JSON 格式的 media-items
        if args.media_items:
            import json
            try:
                media_items = json.loads(args.media_items)
            except json.JSONDecodeError:
                print("❌ 錯誤：--media-items 必須是有效的 JSON 格式")
                return 1
        else:
            # 從 --image-urls 和 --video-urls 構建媒體項目
            if args.image_urls:
                for url in args.image_urls.split(","):
                    url = url.strip()
                    if url:
                        media_items.append({"type": "IMAGE", "url": url})

            if args.video_urls:
                for url in args.video_urls.split(","):
                    url = url.strip()
                    if url:
                        media_items.append({"type": "VIDEO", "url": url})

        if len(media_items) < 2:
            print("❌ 錯誤：輪播至少需要 2 個媒體項目")
            print("💡 提示：使用 --image-urls 或 --video-urls 提供多個媒體")
            return 1

        result = poster.post_carousel(threads_id, args.access_token, media_items, args.text or "")

    # 輸出結果
    if result["success"]:
        print("\n✅ 成功發布到 Threads！")
        print(f"📱 媒體 ID: {result['media_id']}")
        if result.get("permalink"):
            print(f"🔗 貼文連結: {result['permalink']}")
        return 0
    else:
        print(f"\n❌ 發布失敗：{result['error']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
