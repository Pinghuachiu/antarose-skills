#!/usr/bin/env python3
"""
Sora2 KIE - Sora2 AI 視頻生成工具

支持 Kie.ai 的 Sora2 和 Sora2 Pro 模型：
- 文生視頻
- 圖生視頻
- 角色動畫 (sora-2-characters)
- 分鏡視頻 (sora-2-pro-storyboard)

API 文檔: https://docs.kie.ai/cn/market/sora2/
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, Optional, List
import requests


class Sora2Generator:
    """Sora2 視頻生成器"""

    def __init__(self, api_key: Optional[str] = None):
        """初始化生成器

        參數：
            api_key: Kie.ai API Key（如果不提供，從環境變量讀取）
        """
        self.api_key = api_key or os.environ.get("KIE_API_KEY")
        if not self.api_key:
            raise ValueError("請提供 API Key 或設置 KIE_API_KEY 環境變量")

        self.base_url = "https://api.kie.ai/api/v1/jobs"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_task(self, model: str, input_data: dict,
                    callback_url: Optional[str] = None) -> Dict:
        """創建生成任務

        參數：
            model: 模型名稱
            input_data: 輸入參數
            callback_url: 回調 URL（可選）

        返回：
            {
                "success": True/False,
                "task_id": "任務 ID",
                "error": "錯誤訊息（如果失敗）"
            }
        """
        print(f"🎬 正在創建 {model} 任務...")

        request_data = {
            "model": model,
            "input": input_data
        }

        if callback_url:
            request_data["callBackUrl"] = callback_url

        try:
            response = requests.post(
                f"{self.base_url}/createTask",
                headers=self.headers,
                json=request_data,
                timeout=30
            )

            result = response.json()

            if result.get("code") == 200:
                task_id = result.get("data", {}).get("taskId")
                print(f"   ✅ 任務創建成功")
                print(f"   📋 任務 ID: {task_id}")
                return {
                    "success": True,
                    "task_id": task_id
                }
            else:
                error_msg = result.get("msg", "未知錯誤")
                return {
                    "success": False,
                    "error": f"API 錯誤 ({result.get('code')}): {error_msg}"
                }

        except requests.exceptions.Timeout:
            return {"success": False, "error": "請求超時"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_task_status(self, task_id: str) -> Dict:
        """查詢任務狀態

        參數：
            task_id: 任務 ID

        返回：
            {
                "success": True/False,
                "state": "pending/processing/success/failed",
                "result": "生成結果",
                "error": "錯誤訊息"
            }
        """
        print(f"🔍 查詢任務狀態: {task_id}")

        try:
            response = requests.get(
                f"{self.base_url}/recordInfo",
                headers=self.headers,
                params={"taskId": task_id},
                timeout=30
            )

            result = response.json()

            if result.get("code") == 200:
                data = result.get("data", {})
                state = data.get("state", "unknown")
                print(f"   📊 狀態: {state}")

                if state == "success":
                    result_json_str = data.get("resultJson", "{}")
                    # 解析嵌套的 JSON 字符串
                    try:
                        result_json = json.loads(result_json_str)
                    except json.JSONDecodeError:
                        result_json = {}

                    print(f"   ✅ 任務完成")
                    return {
                        "success": True,
                        "state": state,
                        "result": result_json
                    }
                elif state == "failed":
                    error_msg = data.get("failMsg", "生成失敗")
                    print(f"   ❌ 任務失敗: {error_msg}")
                    return {
                        "success": False,
                        "state": state,
                        "error": error_msg
                    }
                else:
                    return {
                        "success": True,
                        "state": state,
                        "result": None
                    }
            else:
                error_msg = result.get("msg", "未知錯誤")
                return {
                    "success": False,
                    "error": f"API 錯誤 ({result.get('code')}): {error_msg}"
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def poll_task(self, task_id: str, interval: int = 10,
                  max_wait: int = 600) -> Dict:
        """輪詢任務直到完成

        參數：
            task_id: 任務 ID
            interval: 輪詢間隔（秒）
            max_wait: 最大等待時間（秒）

        返回：
            {
                "success": True/False,
                "result": "生成結果",
                "error": "錯誤訊息"
            }
        """
        print(f"⏳ 開始輪詢任務（間隔 {interval} 秒，最多 {max_wait} 秒）...")

        waited = 0
        while waited < max_wait:
            status_result = self.get_task_status(task_id)

            if not status_result["success"]:
                return status_result

            state = status_result["state"]

            if state == "success":
                return status_result
            elif state == "failed":
                return {
                    "success": False,
                    "error": status_result.get("error", "任務失敗")
                }

            # 繼續等待
            print(f"   ⏰ 等待 {interval} 秒...")
            time.sleep(interval)
            waited += interval

        return {
            "success": False,
            "error": f"任務超時（已等待 {waited} 秒）"
        }

    def text_to_video(self, model: str, prompt: str,
                     aspect_ratio: str = "landscape",
                     frames: str = "10",
                     remove_watermark: bool = False,
                     callback_url: Optional[str] = None,
                     poll: bool = False,
                     poll_interval: int = 10) -> Dict:
        """文生視頻

        參數：
            model: sora-2-text-to-video 或 sora-2-pro-text-to-video
            prompt: 文字描述
            aspect_ratio: 寬高比 (landscape/portrait/square)
            frames: 幀數
            remove_watermark: 是否移除水印
            callback_url: 回調 URL
            poll: 是否自動輪詢
            poll_interval: 輪詢間隔

        返回：
            {
                "success": True/False,
                "task_id": "任務 ID",
                "result": "生成結果（如果 poll=True 且成功）",
                "error": "錯誤訊息"
            }
        """
        print(f"📝 文生視頻")
        print(f"   📄 提示詞: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        print(f"   📐 寬高比: {aspect_ratio}")
        print(f"   🎞️  幀數: {frames}")

        input_data = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "n_frames": frames
        }

        if "sora-2-text-to-video" in model:
            input_data["remove_watermark"] = remove_watermark

        result = self.create_task(model, input_data, callback_url)

        if result["success"] and poll:
            print()
            poll_result = self.poll_task(result["task_id"], poll_interval)
            if poll_result["success"]:
                result["result"] = poll_result["result"]
            else:
                result["error"] = poll_result["error"]
                result["success"] = False

        return result

    def image_to_video(self, model: str, image_url: str,
                      prompt: Optional[str] = None,
                      aspect_ratio: str = "landscape",
                      frames: str = "10",
                      callback_url: Optional[str] = None,
                      poll: bool = False,
                      poll_interval: int = 10) -> Dict:
        """圖生視頻

        參數：
            model: sora-2-image-to-video 或 sora-2-pro-image-to-video
            image_url: 圖片 URL
            prompt: 文字描述（可選）
            aspect_ratio: 寬高比
            frames: 幀數
            callback_url: 回調 URL
            poll: 是否自動輪詢
            poll_interval: 輪詢間隔

        返回：
            {
                "success": True/False,
                "task_id": "任務 ID",
                "result": "生成結果",
                "error": "錯誤訊息"
            }
        """
        print(f"🖼️  圖生視頻")
        print(f"   🖼️  圖片 URL: {image_url}")
        if prompt:
            print(f"   📄 提示詞: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        print(f"   📐 寬高比: {aspect_ratio}")
        print(f"   🎞️  幀數: {frames}")

        input_data = {
            "image_urls": [image_url],
            "aspect_ratio": aspect_ratio,
            "n_frames": frames
        }

        if prompt:
            input_data["prompt"] = prompt

        result = self.create_task(model, input_data, callback_url)

        if result["success"] and poll:
            print()
            poll_result = self.poll_task(result["task_id"], poll_interval)
            if poll_result["success"]:
                result["result"] = poll_result["result"]
            else:
                result["error"] = poll_result["error"]
                result["success"] = False

        return result

    def characters(self, video_url: str,
                   character_prompt: Optional[str] = None,
                   safety_instruction: Optional[str] = None,
                   callback_url: Optional[str] = None,
                   poll: bool = False,
                   poll_interval: int = 10) -> Dict:
        """角色動畫

        參數：
            video_url: 角色視頻 URL（1-4秒，<10MB）
            character_prompt: 角色描述
            safety_instruction: 安全指令
            callback_url: 回調 URL
            poll: 是否自動輪詢
            poll_interval: 輪詢間隔

        返回：
            {
                "success": True/False,
                "task_id": "任務 ID",
                "result": "生成結果",
                "error": "錯誤訊息"
            }
        """
        print(f"🎭 角色動畫")
        print(f"   🎥 視頻 URL: {video_url}")
        if character_prompt:
            print(f"   📄 角色描述: {character_prompt[:100]}{'...' if len(character_prompt) > 100 else ''}")
        if safety_instruction:
            print(f"   🛡️  安全指令: {safety_instruction[:100]}{'...' if len(safety_instruction) > 100 else ''}")

        input_data = {
            "character_file_url": [video_url]
        }

        if character_prompt:
            input_data["character_prompt"] = character_prompt

        if safety_instruction:
            input_data["safety_instruction"] = safety_instruction

        result = self.create_task("sora-2-characters", input_data, callback_url)

        if result["success"] and poll:
            print()
            poll_result = self.poll_task(result["task_id"], poll_interval)
            if poll_result["success"]:
                result["result"] = poll_result["result"]
            else:
                result["error"] = poll_result["error"]
                result["success"] = False

        return result

    def storyboard(self, image_urls: List[str], shots: List[dict],
                   aspect_ratio: str = "landscape",
                   frames: str = "15",
                   callback_url: Optional[str] = None,
                   poll: bool = False,
                   poll_interval: int = 10) -> Dict:
        """分鏡視頻

        參數：
            image_urls: 圖片 URL 列表
            shots: 場景列表 [{"Scene": "描述", "duration": 7.5}, ...]
            aspect_ratio: 寬高比
            frames: 幀數
            callback_url: 回調 URL
            poll: 是否自動輪詢
            poll_interval: 輪詢間隔

        返回：
            {
                "success": True/False,
                "task_id": "任務 ID",
                "result": "生成結果",
                "error": "錯誤訊息"
            }
        """
        print(f"📋 分鏡視頻")
        print(f"   🖼️  圖片數量: {len(image_urls)}")
        print(f"   🎬 場景數量: {len(shots)}")
        print(f"   📐 寬高比: {aspect_ratio}")
        print(f"   🎞️  幀數: {frames}")

        for i, shot in enumerate(shots, 1):
            print(f"      場景 {i}: {shot.get('Scene', '')[:50]}...")

        input_data = {
            "image_urls": image_urls,
            "shots": shots,
            "aspect_ratio": aspect_ratio,
            "n_frames": frames
        }

        result = self.create_task("sora-2-pro-storyboard", input_data, callback_url)

        if result["success"] and poll:
            print()
            poll_result = self.poll_task(result["task_id"], poll_interval)
            if poll_result["success"]:
                result["result"] = poll_result["result"]
            else:
                result["error"] = poll_result["error"]
                result["success"] = False

        return result


def parse_scenes(scenes_str: str) -> List[dict]:
    """解析場景字符串

    支持格式：
    1. JSON 格式: [{"Scene": "描述", "duration": 7.5}, ...]
    2. 逗號分隔: "場景1: 描述1,場景2: 描述2"
    """
    try:
        # 嘗試 JSON 格式
        scenes = json.loads(scenes_str)
        if isinstance(scenes, list):
            return scenes
    except json.JSONDecodeError:
        pass

    # 解析逗號分隔格式
    scenes = []
    for part in scenes_str.split(","):
        part = part.strip()
        if ":" in part:
            name, desc = part.split(":", 1)
            scenes.append({
                "Scene": desc.strip(),
                "duration": 7.5  # 默认時長
            })
        else:
            scenes.append({
                "Scene": part,
                "duration": 7.5
            })

    return scenes


def main():
    parser = argparse.ArgumentParser(
        description="Sora2 AI 視頻生成工具 - Kie.ai",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 文生視頻
  python3 generate.py --model sora2 --action text-to-video --prompt "一隻貓在陽光下打哈欠"

  # 圖生視頻
  python3 generate.py --model sora2 --action image-to-video --image-url "https://..." --prompt "讓雲彩移動"

  # Sora2 Pro 文生視頻
  python3 generate.py --model sora2-pro --action text-to-video --prompt "科幻城市夜景"

  # 角色動畫
  python3 generate.py --model sora2 --action characters --video-url "https://..."

  # 分鏡視頻
  python3 generate.py --model sora2-pro --action storyboard --image-urls "url1,url2" --scenes "場景1: 描述1,場景2: 描述2"

  # 查詢任務狀態
  python3 generate.py --action status --task-id "task_id_here"

  # 自動輪詢任務
  python3 generate.py --model sora2 --action text-to-video --prompt "..." --poll --poll-interval 10
        """
    )

    parser.add_argument("--api-key", help="Kie.ai API Key（也可使用 KIE_API_KEY 環境變量）")
    parser.add_argument("--model", choices=["sora2", "sora2-pro"], help="模型選擇")
    parser.add_argument("--action", required=True,
                       choices=["text-to-video", "image-to-video", "characters", "storyboard", "status"],
                       help="執行動作")

    # 文生視頻參數
    parser.add_argument("--prompt", help="文字描述")
    parser.add_argument("--aspect-ratio", default="landscape",
                       choices=["landscape", "portrait", "square"],
                       help="寬高比")
    parser.add_argument("--frames", default="10", help="生成幀數")
    parser.add_argument("--remove-watermark", action="store_true",
                       help="移除水印（僅 Sora2 基礎模型）")

    # 圖生視頻參數
    parser.add_argument("--image-url", help="圖片 URL")
    parser.add_argument("--image-urls", help="多張圖片 URL（逗號分隔，用於 storyboard）")

    # 角色動畫參數
    parser.add_argument("--video-url", help="角色視頻 URL")
    parser.add_argument("--character-prompt", help="角色描述")
    parser.add_argument("--safety-instruction", help="安全指令")

    # 分鏡視頻參數
    parser.add_argument("--scenes", help="場景描述（JSON 格式或逗號分隔）")

    # 任務管理參數
    parser.add_argument("--task-id", help="任務 ID")
    parser.add_argument("--callback-url", help="回調 URL")
    parser.add_argument("--poll", action="store_true",
                       help="自動輪詢直到任務完成")
    parser.add_argument("--poll-interval", type=int, default=10,
                       help="輪詢間隔（秒），默認 10")
    parser.add_argument("--max-wait", type=int, default=600,
                       help="最大等待時間（秒），默認 600")
    parser.add_argument("--save-task-id", action="store_true",
                       help="保存任務 ID 到文件")

    args = parser.parse_args()

    try:
        generator = Sora2Generator(api_key=args.api_key)

        # 查詢任務狀態
        if args.action == "status":
            if not args.task_id:
                print("❌ 錯誤：--task-id 是必需的")
                return 1

            result = generator.get_task_status(args.task_id)

            if result["success"]:
                if result["state"] == "success":
                    print("\n✅ 任務成功完成！")
                    print(f"📊 結果: {json.dumps(result['result'], indent=2, ensure_ascii=False)}")
                    return 0
                else:
                    print(f"\n⏳ 任務狀態: {result['state']}")
                    return 0
            else:
                print(f"\n❌ 錯誤：{result['error']}")
                return 1

        # 確定模型
        if not args.model:
            print("❌ 錯誤：--model 是必需的")
            return 1

        # 執行相應動作
        if args.action == "text-to-video":
            if not args.prompt:
                print("❌ 錯誤：--prompt 是必需的")
                return 1

            model = "sora-2-text-to-video" if args.model == "sora2" else "sora-2-pro-text-to-video"
            result = generator.text_to_video(
                model=model,
                prompt=args.prompt,
                aspect_ratio=args.aspect_ratio,
                frames=args.frames,
                remove_watermark=args.remove_watermark,
                callback_url=args.callback_url,
                poll=args.poll,
                poll_interval=args.poll_interval
            )

        elif args.action == "image-to-video":
            if not args.image_url:
                print("❌ 錯誤：--image-url 是必需的")
                return 1

            model = "sora-2-image-to-video" if args.model == "sora2" else "sora-2-pro-image-to-video"
            result = generator.image_to_video(
                model=model,
                image_url=args.image_url,
                prompt=args.prompt,
                aspect_ratio=args.aspect_ratio,
                frames=args.frames,
                callback_url=args.callback_url,
                poll=args.poll,
                poll_interval=args.poll_interval
            )

        elif args.action == "characters":
            if not args.video_url:
                print("❌ 錯誤：--video-url 是必需的")
                return 1

            result = generator.characters(
                video_url=args.video_url,
                character_prompt=args.character_prompt,
                safety_instruction=args.safety_instruction,
                callback_url=args.callback_url,
                poll=args.poll,
                poll_interval=args.poll_interval
            )

        elif args.action == "storyboard":
            if not args.image_urls or not args.scenes:
                print("❌ 錯誤：--image-urls 和 --scenes 是必需的")
                return 1

            image_urls = [url.strip() for url in args.image_urls.split(",")]
            shots = parse_scenes(args.scenes)

            result = generator.storyboard(
                image_urls=image_urls,
                shots=shots,
                aspect_ratio=args.aspect_ratio,
                frames=args.frames,
                callback_url=args.callback_url,
                poll=args.poll,
                poll_interval=args.poll_interval
            )

        # 輸出結果
        if result["success"]:
            task_id = result["task_id"]

            # 保存任務 ID
            if args.save_task_id:
                with open("task_id.txt", "w") as f:
                    f.write(task_id)
                print(f"\n💾 任務 ID 已保存到 task_id.txt")

            # 如果有輪詢結果
            if "result" in result and result["result"]:
                print("\n✅ 視頻生成成功！")
                print(f"📊 結果: {json.dumps(result['result'], indent=2, ensure_ascii=False)}")
            else:
                print(f"\n✅ 任務已提交")
                print(f"📋 任務 ID: {task_id}")
                print(f"💡 使用以下命令查詢狀態：")
                print(f"   python3 {sys.argv[0]} --action status --task-id {task_id}")

            return 0
        else:
            print(f"\n❌ 錯誤：{result['error']}")
            return 1

    except ValueError as e:
        print(f"❌ {e}")
        return 1
    except Exception as e:
        print(f"❌ 未預期的錯誤：{e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
