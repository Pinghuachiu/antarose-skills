#!/usr/bin/env python3
"""
Facebook Page Token Helper
Facebook Page Token 換取和發文助手

重要說明：
- 資料庫中儲存的是 User Token（長期有效）
- User Token 不能直接用於發布到粉絲專頁
- 必須使用 User Token 換取 Page Token（臨時，但可用於發文）
- 換取的 Page Token 不應存回資料庫（保持 User Token 不變）

工作流程：
1. 從資料庫讀取 User Token
2. 使用 User Token 換取 Page Token
3. 使用 Page Token 發文到 Facebook
4. 資料庫保持原樣（User Token 不變）
"""

import os
import sys
import requests
import json
import argparse
from typing import Dict, Optional
from datetime import datetime


class FacebookTokenHelper:
    """Facebook Token 輔助工具"""

    def __init__(self):
        self.graph_api_version = "v24.0"
        self.base_url = f"https://graph.facebook.com/{self.graph_api_version}"

    def get_page_token_from_user_token(self, page_id: str, user_token: str) -> Dict:
        """
        使用 User Token 換取 Page Token

        參數：
            page_id: Facebook 粉絲專頁 ID
            user_token: User Access Token（從資料庫讀取）

        返回：
            {
                "success": True/False,
                "page_token": "Page Access Token",
                "page_id": "Page ID",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        try:
            # 構建 API 請求
            url = f"{self.base_url}/{page_id}"
            params = {
                "fields": "access_token",
                "access_token": user_token
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if "access_token" in data:
                    return {
                        "success": True,
                        "page_token": data["access_token"],
                        "page_id": data.get("id", page_id)
                    }
                else:
                    return {
                        "success": False,
                        "error": "API 回應中沒有 access_token"
                    }
            else:
                return {
                    "success": False,
                    "error": f"API 請求失敗 ({response.status_code}): {response.text}"
                }

        except requests.exceptions.Timeout:
            return {"success": False, "error": "API 請求超時"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def post_to_facebook(self, page_id: str, token: str,
                        message: str, photo_url: Optional[str] = None,
                        video_url: Optional[str] = None,
                        use_page_token: bool = True) -> Dict:
        """
        發布貼文到 Facebook 粉絲專頁

        支援：
        - 純文字貼文
        - 文字 + 圖片
        - 文字 + 影片

        參數：
            page_id: Facebook 粉絲專頁 ID
            token: Access Token（從資料庫讀取，可以是 User Token 或 Page Token）
            message: 貼文內容
            photo_url: 圖片 URL（可選）
            video_url: 影片 URL（可選）
            use_page_token: 是否先換取 Page Token（預設 True）

        返回：
            {
                "success": True/False,
                "post_id": "貼文 ID",
                "post_url": "貼文連結",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        access_token = token

        # 如果需要，先換取 Page Token
        if use_page_token:
            print("🔄 正在換取 Page Access Token...")
            token_result = self.get_page_token_from_user_token(page_id, token)

            if not token_result["success"]:
                print(f"⚠️  換取 Page Token 失敗: {token_result.get('error', '未知錯誤')}")
                print("💡 嘗試直接使用提供的 Token 發文...")
                access_token = token  # 使用原始 token
            else:
                access_token = token_result["page_token"]
                print("✅ Page Token 換取成功")
        else:
            print("📝 直接使用提供的 Token 發文")

        # 發文
        if video_url:
            print("📹 正在發布影片貼文...")
        elif photo_url:
            print("🖼️  正在發布圖片貼文...")
        else:
            print("📝 正在發布文字貼文...")

        try:
            if video_url:
                # 發布帶影片的貼文
                url = f"{self.base_url}/{page_id}/videos"
                data = {
                    "file_url": video_url,
                    "description": message,
                    "access_token": access_token
                }
            elif photo_url:
                # 發布帶圖片的貼文
                url = f"{self.base_url}/{page_id}/photos"
                data = {
                    "url": photo_url,
                    "caption": message,
                    "access_token": access_token
                }
            else:
                # 發布純文字貼文
                url = f"{self.base_url}/{page_id}/feed"
                data = {
                    "message": message,
                    "access_token": access_token
                }

            # 影片上傳需要更長的 timeout
            timeout = 120 if video_url else 30
            response = requests.post(url, data=data, timeout=timeout)

            if response.status_code == 200:
                result = response.json()

                if "id" in result:
                    post_id = result["id"]
                    return {
                        "success": True,
                        "post_id": post_id,
                        "post_url": f"https://www.facebook.com/{page_id}/posts/{post_id.split('_')[1] if '_' in post_id else post_id}"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API 回應中沒有 post_id: {result}"
                    }
            else:
                error_data = response.json()
                return {
                    "success": False,
                    "error": f"API 請求失敗 ({response.status_code}): {error_data.get('error', {}).get('message', response.text)}"
                }

        except requests.exceptions.Timeout:
            return {"success": False, "error": "發布貼文超時（影片上傳可能需要更長時間）"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def verify_token(self, token: str) -> Dict:
        """
        驗證 Token 有效性

        參數：
            token: Access Token

        返回：
            {
                "success": True/False,
                "token_type": "USER/PAGE",
                "is_valid": True/False,
                "expires_at": "過期時間",
                "permissions": ["權限列表"],
                "error": "錯誤訊息（如果失敗）"
            }
        """
        try:
            url = f"{self.base_url}/debug_token"
            data = {
                "input_token": token
            }

            response = requests.get(url, data=data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                data = result.get("data", {})

                return {
                    "success": True,
                    "token_type": data.get("type"),
                    "is_valid": data.get("is_valid", False),
                    "expires_at": data.get("expires_at"),
                    "permissions": [scope.get("scope") for scope in data.get("granular_scopes", [])]
                }
            else:
                return {
                    "success": False,
                    "error": f"驗證失敗 ({response.status_code}): {response.text}"
                }

        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Facebook Token 換取和發文工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 換取 Page Token
  python3 facebook-token-helper.py --page-id 858773663997089 --user-token USER_TOKEN --action get-page-token

  # 發布純文字貼文
  python3 facebook-token-helper.py --page-id 858773663997089 --user-token USER_TOKEN --action post --message "Hello World"

  # 發布帶圖片的貼文
  python3 facebook-token-helper.py --page-id 858773663997089 --user-token USER_TOKEN --action post --message "Check this out" --photo-url "https://example.com/image.jpg"

  # 驗證 Token
  python3 facebook-token-helper.py --token TOKEN --action verify

  # 從資料庫讀取並發文（配合 n8n 系統）
  python3 facebook-token-helper.py --channel-id 1 --action post-from-db --message "Hello" --photo-url "https://..."
        """
    )

    parser.add_argument("--action", required=True,
                       choices=["get-page-token", "post", "verify", "post-from-db"],
                       help="執行動作")

    parser.add_argument("--page-id", help="Facebook 粉絲專頁 ID")
    parser.add_argument("--user-token", help="User Access Token")
    parser.add_argument("--token", help="Access Token（用於驗證）")
    parser.add_argument("--message", help="貼文內容")
    parser.add_argument("--photo-url", help="圖片 URL（可選）")
    parser.add_argument("--video-url", help="影片 URL（可選，支援 MP4 等格式）")

    # 資料庫相關參數
    parser.add_argument("--channel-id", type=int, help="資料庫中的頻道 ID（從資料庫讀取設定）")
    parser.add_argument("--mysql-host", default="192.168.1.159", help="MySQL 主機")
    parser.add_argument("--mysql-user", default="n8n", help="MySQL 使用者")
    parser.add_argument("--mysql-password", default="!!asshole!!asshole", help="MySQL 密碼")
    parser.add_argument("--mysql-database", default="infoCollection", help="MySQL 資料庫")

    # Token 使用方式
    parser.add_argument("--use-page-token", action="store_true",
                       help="先換取 Page Token 再發文（如果資料庫的 token 無法直接發文時使用）")
    parser.add_argument("--direct-use-token", action="store_true", default=True,
                       help="直接使用 Token 發文（預設，與 n8n 系統一致）")

    args = parser.parse_args()

    helper = FacebookTokenHelper()

    # 從資料庫讀取設定
    if args.action == "post-from-db":
        if not args.channel_id:
            print("❌ 錯誤：--channel-id 是必需的")
            return 1

        if not args.message:
            print("❌ 錯誤：--message 是必需的")
            return 1

        try:
            import mysql.connector

            # 連接資料庫
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

            page_id = channel["page_id"]
            token = channel["access_token"]

            cursor.close()
            conn.close()

            print(f"✅ 從資料庫讀取頻道 {args.channel_id} 的設定")

            # 判斷是否要使用 Page Token（預設直接使用 token，與 n8n 系統一致）
            use_page_token = args.use_page_token and not args.direct_use_token

            # 直接發文
            result = helper.post_to_facebook(
                page_id,
                token,
                args.message,
                args.photo_url,
                args.video_url,
                use_page_token=use_page_token
            )

            if result["success"]:
                print("✅ 成功發布到 Facebook")
                print(f"貼文 ID: {result['post_id']}")
                print(f"貼文連結: {result['post_url']}")
            else:
                print(f"❌ 發布失敗：{result['error']}")
                return 1

            return 0

        except Exception as e:
            print(f"❌ 資料庫錯誤：{e}")
            return 1

    # 執行動作
    if args.action == "get-page-token":
        if not args.page_id or not args.user_token:
            print("❌ 錯誤：--page-id 和 --user-token 是必需的")
            return 1

        result = helper.get_page_token_from_user_token(args.page_id, args.user_token)

        if result["success"]:
            print("✅ 成功換取 Page Token")
            print(f"Page Token: {result['page_token']}")
            print(f"\n💡 提示：請使用此 Page Token 進行後續的 API 呼叫")
        else:
            print(f"❌ 換取失敗：{result['error']}")
            return 1

    elif args.action == "post":
        if not args.page_id or not args.user_token or not args.message:
            print("❌ 錯誤：--page-id, --user-token 和 --message 是必需的")
            return 1

        # 判斷是否要使用 Page Token（預設直接使用 token）
        use_page_token = args.use_page_token and not args.direct_use_token

        result = helper.post_to_facebook(
            args.page_id,
            args.user_token,
            args.message,
            args.photo_url,
            args.video_url,
            use_page_token=use_page_token
        )

        if result["success"]:
            print("✅ 成功發布到 Facebook")
            print(f"貼文 ID: {result['post_id']}")
            print(f"貼文連結: {result['post_url']}")
        else:
            print(f"❌ 發布失敗：{result['error']}")
            return 1

    elif args.action == "verify":
        if not args.token:
            print("❌ 錯誤：--token 是必需的")
            return 1

        result = helper.verify_token(args.token)

        if result["success"]:
            print("✅ Token 驗證成功")
            print(f"類型: {result['token_type']}")
            print(f"有效: {result['is_valid']}")
            print(f"權限: {', '.join(result['permissions'])}")
        else:
            print(f"❌ 驗證失敗：{result['error']}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
