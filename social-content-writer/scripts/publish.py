#!/usr/bin/env python3
"""
Social Content Writer - Multi-Platform Publisher
多平台發布腳本
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import subprocess
import time


class ContentPublisher:
    """內容發布器"""

    def __init__(self):
        self.supported_platforms = ["facebook", "instagram", "linkedin", "threads"]
        self.integration_scripts = {
            "facebook": self._publish_to_facebook,
            "instagram": self._publish_to_instagram,
            "linkedin": self._publish_to_linkedin,
            "threads": self._publish_to_threads
        }

    def publish(self, content_data: Dict, platforms: List[str],
                schedule: Optional[str] = None,
                notify_discord: bool = False) -> Dict:
        """發布內容到多個平台"""
        results = {}

        for platform in platforms:
            if platform not in self.supported_platforms:
                results[platform] = {
                    "success": False,
                    "error": f"不支援的平台: {platform}"
                }
                continue

            print(f"\n🚀 正在發布到 {platform.upper()}...")

            try:
                # 檢查是否需要排程
                if schedule:
                    results[platform] = self._schedule_publish(
                        content_data, platform, schedule
                    )
                else:
                    # 立即發布
                    results[platform] = self.integration_scripts[platform](
                        content_data
                    )

                if results[platform]["success"]:
                    print(f"✅ {platform.upper()} 發布成功")
                else:
                    print(f"❌ {platform.upper()} 發布失敗: {results[platform].get('error', '未知錯誤')}")

            except Exception as e:
                results[platform] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ {platform.upper()} 發布錯誤: {e}")

        # 發送 Discord 通知
        if notify_discord:
            self._notify_discord(content_data, results)

        return results

    def _publish_to_facebook(self, content_data: Dict) -> Dict:
        """發布到 Facebook"""
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "facebook-page-post",
            "scripts",
            "post.py"
        )

        # 檢查腳本是否存在
        if not os.path.exists(script_path):
            return {
                "success": False,
                "error": f"Facebook 發布腳本不存在: {script_path}"
            }

        try:
            # 提取內容
            content = content_data.get("content", "")
            title = content_data.get("title", "")

            # 構建命令
            cmd = ["python3", script_path, content]

            # 如果有圖片，添加圖片參數
            if "prompts" in content_data and content_data["prompts"]:
                # 這裡可以添加圖片生成和上傳邏輯
                pass

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "post_id": result.stdout.strip(),
                    "platform": "facebook",
                    "published_at": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr or result.stdout
                }

        except subprocess.TimeoutExpired:
            return {"success": False, "error": "發布超時"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _publish_to_instagram(self, content_data: Dict) -> Dict:
        """發布到 Instagram（需要手動發布）"""
        # Instagram Basic Display API 有限制
        # 這裡我們提供生成好的內容，用戶需要手動發布

        content = content_data.get("content", "")
        hashtags = " ".join(content_data.get("hashtags", []))

        print("\n📱 Instagram 發布指南:")
        print("   1. 打開 Instagram 應用")
        print("   2. 點擊 + 創建新貼文")
        print("   3. 上傳圖片（如已生成）")
        print("   4. 複製以下內容:")
        print(f"\n   {content}\n")
        print(f"   {hashtags}\n")
        print("   5. 粘貼到說明欄位")
        print("   6. 點擊分享\n")

        return {
            "success": True,
            "platform": "instagram",
            "method": "manual",
            "note": "需要手動發布",
            "published_at": datetime.now().isoformat()
        }

    def _publish_to_linkedin(self, content_data: Dict) -> Dict:
        """發布到 LinkedIn（需要手動發布）"""
        # LinkedIn API 需要複雜的認證
        # 這裡我們提供生成好的內容，用戶需要手動發布

        content = content_data.get("content", "")

        print("\n💼 LinkedIn 發布指南:")
        print("   1. 打開 LinkedIn 網站或應用")
        print("   2. 點擊開始發布")
        print("   3. 複製以下內容:")
        print(f"\n{content}\n")
        print("   4. 粘貼到發布框")
        print("   5. 點擊發布\n")

        return {
            "success": True,
            "platform": "linkedin",
            "method": "manual",
            "note": "需要手動發布",
            "published_at": datetime.now().isoformat()
        }

    def _publish_to_threads(self, content_data: Dict) -> Dict:
        """發布到 Threads（需要手動發布）"""
        # Threads API 還在開發中
        content = content_data.get("content", "")

        print("\n💬 Threads 發布指南:")
        print("   1. 打開 Threads 應用")
        print("   2. 點擊創建新貼文")
        print("   3. 複製以下內容:")
        print(f"\n{content}\n")
        print("   4. 粘貼到貼文框")
        print("   5. 點擊發布\n")

        return {
            "success": True,
            "platform": "threads",
            "method": "manual",
            "note": "需要手動發布",
            "published_at": datetime.now().isoformat()
        }

    def _schedule_publish(self, content_data: Dict, platform: str,
                         schedule_time: str) -> Dict:
        """排程發布（需要實現排程系統）"""
        # 這裡可以實現一個簡單的排程系統
        # 或者集成到任務調度器如 cron

        print(f"   ⏰ 排程發布時間: {schedule_time}")
        print(f"   ℹ️  請手動設置排程任務或使用定時工具")

        return {
            "success": True,
            "platform": platform,
            "method": "scheduled",
            "scheduled_for": schedule_time,
            "note": "請設置定時任務"
        }

    def _notify_discord(self, content_data: Dict, results: Dict) -> bool:
        """發送 Discord 通知"""
        webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

        if not webhook_url:
            print("⚠️  未設置 DISCORD_WEBHOOK_URL，跳過通知")
            return False

        script_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "discord-webchannel",
            "scripts",
            "send.py"
        )

        if not os.path.exists(script_path):
            print("⚠️  Discord 通知腳本不存在")
            return False

        try:
            # 構建通知訊息
            title = content_data.get("title", "內容發布")
            message = f"**{title}**\n\n"

            # 統計成功和失敗
            successful = [p for p, r in results.items() if r.get("success")]
            failed = [p for p, r in results.items() if not r.get("success")]

            message += f"✅ 成功發布: {', '.join(successful).upper()}\n"
            if failed:
                message += f"❌ 發布失敗: {', '.join(failed).upper()}\n"

            message += f"\n時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # 調用 Discord 通知腳本
            result = subprocess.run(
                ["python3", script_path, message],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                print("✅ Discord 通知已發送")
                return True
            else:
                print(f"⚠️  Discord 通知發送失敗")
                return False

        except Exception as e:
            print(f"⚠️  Discord 通知錯誤: {e}")
            return False

    def save_to_database(self, content_data: Dict, results: Dict,
                        table: str = "content_history") -> bool:
        """保存發布歷史到資料庫"""
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "mysql",
            "scripts",
            "insert.py"
        )

        if not os.path.exists(script_path):
            print("⚠️  MySQL 插入腳本不存在")
            return False

        try:
            # 構建插入數據
            title = content_data.get("title", "")
            content = content_data.get("content", "")
            hashtags_json = json.dumps(content_data.get("hashtags", []))
            metadata_json = json.dumps(content_data.get("metadata", {}))

            # 統計發布結果
            platforms = list(results.keys())
            successful = sum(1 for r in results.values() if r.get("success"))

            # 構建 SQL
            sql = f"""
            INSERT INTO {table} (topic, platform, content, hashtags, metadata, status)
            VALUES (
                '{title[:255]}',
                '{','.join(platforms)}',
                '{content[:1000]}',
                '{hashtags_json}',
                '{metadata_json}',
                'published'
            )
            """

            # 調用 MySQL 插入腳本
            result = subprocess.run(
                ["python3", script_path, sql],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                print("✅ 發布歷史已保存到資料庫")
                return True
            else:
                print(f"⚠️  保存到資料庫失敗")
                return False

        except Exception as e:
            print(f"⚠️  保存到資料庫錯誤: {e}")
            return False

    def print_publish_results(self, results: Dict):
        """打印發布結果"""
        print("\n" + "="*60)
        print("📊 發布結果摘要")
        print("="*60)

        for platform, result in results.items():
            status = "✅ 成功" if result.get("success") else "❌ 失敗"
            print(f"\n{platform.upper()}: {status}")

            if result.get("success"):
                if result.get("method") == "manual":
                    print(f"   方法: 手動發布")
                    print(f"   說明: {result.get('note', '')}")
                elif result.get("method") == "scheduled":
                    print(f"   方法: 排程發布")
                    print(f"   時間: {result.get('scheduled_for', '')}")
                else:
                    print(f"   貼文 ID: {result.get('post_id', 'N/A')}")
            else:
                print(f"   錯誤: {result.get('error', '未知錯誤')}")

        print("="*60 + "\n")

    def save_to_file(self, results: Dict, filepath: str):
        """保存發布結果到文件"""
        output = {
            "published_at": datetime.now().isoformat(),
            "results": results
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ 發布結果已保存到: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="多平台發布內容",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 發布到單一平台
  python3 publish.py --content content.json --platforms facebook

  # 發布到多平台
  python3 publish.py --content content.json --platforms facebook,instagram,linkedin

  # 排程發布
  python3 publish.py --content content.json --platforms facebook --schedule "2025-01-30 09:00"

  # 發布並通知
  python3 publish.py --content content.json --platforms facebook --notify-discord --save-db
        """
    )
    parser.add_argument("--content", required=True, help="內容檔案路徑（JSON）")
    parser.add_argument("--platforms", required=True,
                       help="發布平台（逗號分隔）")
    parser.add_argument("--schedule",
                       help="排程發布時間（格式: YYYY-MM-DD HH:MM）")
    parser.add_argument("--notify-discord", action="store_true",
                       help="發送 Discord 通知")
    parser.add_argument("--save-db", action="store_true",
                       help="保存到資料庫")
    parser.add_argument("--output", default="publish_results.json",
                       help="輸出檔案路徑")

    args = parser.parse_args()

    # 讀取內容
    with open(args.content, 'r', encoding='utf-8') as f:
        content_data = json.load(f)

    # 處理多平台內容
    if "platforms" in content_data:
        # 多平台內容，提取指定平台
        platforms = [p.strip() for p in args.platforms.split(",")]
        # 使用第一個平台的內容作為基礎
        first_platform = platforms[0]
        if first_platform in content_data["platforms"]:
            content_data = content_data["platforms"][first_platform]

    # 解析平台列表
    if "platforms" in args.platforms:
        # 從內容文件中獲取
        platforms = list(content_data.get("platforms", {}).keys())
    else:
        platforms = [p.strip() for p in args.platforms.split(",")]

    # 創建發布器
    publisher = ContentPublisher()

    # 發布內容
    results = publisher.publish(
        content_data,
        platforms,
        schedule=args.schedule,
        notify_discord=args.notify_discord
    )

    # 保存到資料庫
    if args.save_db:
        publisher.save_to_database(content_data, results)

    # 打印結果
    publisher.print_publish_results(results)

    # 保存到文件
    publisher.save_to_file(results, args.output)


if __name__ == "__main__":
    main()
