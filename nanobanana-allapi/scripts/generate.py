#!/usr/bin/env python3
"""
NanoBanana AllAPI - Python 腳本
使用 AllAPI 提供的 NanoBanana 模型生成圖片
"""

import base64
import requests
import sys
import os
import shutil
import tempfile

API_KEY = os.environ.get("ALLAPI_KEY")
if not API_KEY:
    print("錯誤: 請設定 ALLAPI_KEY 環境變數", file=sys.stderr)
    print("請參考 resource.md 獲取 API Key", file=sys.stderr)
    sys.exit(1)

# 可選模型
MODEL_PRO = "gemini-3-pro-image-preview"  # NanoBanana Pro (最強）
MODEL_FLASH = "gemini-2.5-flash-image"  # Flash (快速）

# 用於追蹤暫存檔案
temp_files = []

def cleanup_temp_files():
    """清理暫存檔案"""
    global temp_files
    for file_path in temp_files:
        try:
            if os.path.exists(file_path):
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        except Exception as e:
            print(f"警告: 無法刪除暫存檔案 {file_path}: {e}", file=sys.stderr)
    temp_files = []

def image_to_base64(image_path):
    """將圖片轉為 base64"""
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"錯誤: 檔案不存在 - {image_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"錯誤: 無法讀取檔案 - {e}", file=sys.stderr)
        sys.exit(1)

def generate_image(prompt="", images=None, aspect_ratio="1:1", image_size="2K", model=MODEL_PRO):
    """
    生成圖片

    Args:
        prompt: 圖片描述文字
        images: 圖片路徑列表（最多14張）
        aspect_ratio: 寬高比
        image_size: 圖片大小
        model: 模型選擇 (MODEL_PRO 或 MODEL_FLASH)

    Returns:
        API 回應
    """
    # 構建 parts
    parts = []

    # 添加文字描述
    if prompt:
        parts.append({"text": prompt})

    # 添加圖片（最多14張）
    if images:
        for image_path in images[:14]:
            parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": image_to_base64(image_path)
                }
            })

    # 構建請求 URL
    api_url = f"https://allapi.store/v1beta/models/{model}:generateContent"

    # 構建請求體
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": parts
            }
        ]
    }

    # Pro 和 Flash 模型都支援 generationConfig
    # 添加圖片生成配置（寬高比、尺寸）
    payload["generationConfig"] = {
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            "aspectRatio": aspect_ratio,
            "imageSize": image_size
        }
    }

    # 🖨️ 打印發送到 API 的內容（除錯用）
    print("=" * 60)
    print("📤 發送到 API 的請求內容：")
    print("=" * 60)
    print(f"🔗 API URL: {api_url}")
    print(f"📝 Prompt (提示詞):\n{prompt}")
    print(f"📐 寬高比: {aspect_ratio}")
    print(f"📏 圖片大小: {image_size}")
    print(f"🤖 模型: {model}")
    print(f"🖼️ 參考圖片數量: {len(images) if images else 0}")
    print("=" * 60)

    # 發送請求
    params = {"key": API_KEY}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, params=params, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 請求失敗: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    try:
        if len(sys.argv) < 2:
            print("使用方法: python3 generate.py <prompt> [--images <img1,img2,...>] [--ratio <ratio>] [--size <size>] [--model <model>]")
            print("範例:")
            print("  python3 generate.py \"一隻可愛的貓\"")
            print("  python3 generate.py \"生成風景\" --images photo1.jpg,photo2.jpg --ratio 16:9 --size 4K")
            print("  python3 generate.py \"快速生成\" --model flash")
            print()
            print("參數說明:")
            print("  prompt: 圖片描述文字")
            print("  --images: 圖片路徑列表，用逗號分隔（最多14張）")
            print("  --ratio: 寬高比 (1:1, 16:9, 9:16, 2:3, 3:2 等）")
            print("  --size: 圖片大小 (1K, 2K, 4K, HIGH, MEDIUM)")
            print("  --model: 模型選擇 (pro, flash)")
            sys.exit(1)

        prompt = sys.argv[1]
        images = None
        aspect_ratio = "1:1"
        image_size = "2K"
        model = MODEL_PRO

        for i in range(2, len(sys.argv)):
            arg = sys.argv[i]
            if arg.startswith("--images="):
                images = arg.split("=")[1].split(",")
            elif arg.startswith("--ratio="):
                aspect_ratio = arg.split("=")[1]
            elif arg.startswith("--size="):
                image_size = arg.split("=")[1]
            elif arg == "--model=flash":
                model = MODEL_FLASH
            elif arg == "--model=pro":
                model = MODEL_PRO

        result = generate_image(
            prompt=prompt,
            images=images,
            aspect_ratio=aspect_ratio,
            image_size=image_size,
            model=model
        )

        # 提取并保存图片
        if 'candidates' in result and len(result['candidates']) > 0:
            content = result['candidates'][0].get('content')
            parts = content.get('parts', []) if isinstance(content, dict) else []
            # 遍歷所有 parts 找到包含 inlineData 的部分
            image_found = False
            if parts:  # 確保 parts 不是 None 且不是空列表
                for part in parts:
                    if 'inlineData' in part:
                        image_data = part['inlineData']['data']
                        image_type = part['inlineData'].get('mimeType', 'image/jpeg')
                        ext = 'png' if 'png' in image_type else 'jpg'

                        # 保存图片
                        output_file = f"generated_image.{ext}"
                        with open(output_file, 'wb') as f:
                            f.write(base64.b64decode(image_data))
                        print(f"图片已保存到: {output_file}")
                        image_found = True
                        break

            if not image_found:
                print("生成结果中未找到图片数据")
        else:
            print("生成结果为空")
    finally:
        cleanup_temp_files()

if __name__ == "__main__":
    main()
