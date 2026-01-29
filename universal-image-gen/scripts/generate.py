#!/usr/bin/env python3
"""
Universal Image Gen - Python 腳本
智能圖片生成工具，優先使用 Antigravity API，失敗時自動降級到 NanoBanana
"""

import base64
import requests
import json
import sys
import os
import argparse
import math

ANTIGRAVITY_API_KEY = os.environ.get("ANTIGRAVITY_API_KEY")
ALLAPI_KEY = os.environ.get("ALLAPI_KEY")

if not ANTIGRAVITY_API_KEY and not ALLAPI_KEY:
    print("錯誤: 請設定 ANTIGRAVITY_API_KEY 或 ALLAPI_KEY 環境變數", file=sys.stderr)
    print("請參考 resource.md 獲取 API Key", file=sys.stderr)
    sys.exit(1)

# API 端點
ANTIGRAVITY_BASE_URL = "http://192.168.1.159:8045"
ANTIGRAVITY_GEN_URL = f"{ANTIGRAVITY_BASE_URL}/v1/images/generations"
ANTIGRAVITY_EDITS_URL = f"{ANTIGRAVITY_BASE_URL}/v1/images/edits"
ALLAPI_API_URL_TEMPLATE = "https://allapi.store/v1beta/models/gemini-3-pro-image-preview:generateContent"

# 標準寬高比
STANDARD_ASPECT_RATIOS = {
    "21:9": 2.333333,
    "16:10": 1.6,
    "16:9": 1.777777,
    "4:3": 1.333333,
    "1:1": 1.0,
    "3:4": 0.75,
    "9:16": 0.5625
}

# 品質對應
QUALITY_MAP = {
    "hd": "4K",
    "medium": "2K",
    "standard": "1K"
}

# 品質尺寸對應
QUALITY_SIZE_MAP = {
    "4K": {
        "1:1": "4096x4096",
        "16:9": "5504x3072",
        "9:16": "3072x5504",
        "21:9": "6336x2688",
        "4:3": "4800x3584",
        "3:4": "3584x4800",
        "16:10": "5504x3440"
    },
    "2K": {
        "1:1": "2048x2048",
        "16:9": "2752x1536",
        "9:16": "1536x2752",
        "21:9": "3168x1344",
        "4:3": "2400x1792",
        "3:4": "1792x2400",
        "16:10": "2752x1720"
    },
    "1K": {
        "1:1": "1024x1024",
        "16:9": "1376x768",
        "9:16": "768x1376",
        "21:9": "1584x672",
        "4:3": "1200x896",
        "3:4": "896x1200",
        "16:10": "1376x860"
    }
}

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

def calculate_aspect_ratio(width, height):
    """計算並映射到最近的標準寬高比"""
    ratio = width / height
    closest_ratio = min(STANDARD_ASPECT_RATIOS.items(), key=lambda x: abs(x[1] - ratio))
    return closest_ratio[0]

def get_quality_size(quality, aspect_ratio):
    """根據品質和寬高比獲取尺寸"""
    quality_level = QUALITY_MAP.get(quality, "1K")
    return QUALITY_SIZE_MAP[quality_level].get(aspect_ratio, "1024x1024")

def parse_size(size_str):
    """解析尺寸字串"""
    try:
        width, height = map(int, size_str.lower().split('x'))
        return width, height
    except:
        print(f"錯誤: 無效的尺寸格式 - {size_str}", file=sys.stderr)
        print("請使用 WIDTHxHEIGHT 格式，例如 1280x720", file=sys.stderr)
        sys.exit(1)

def generate_antigravity(prompt, size="1024x1024", quality="standard", n=1, images=None):
    """使用 Antigravity API 生成圖片（OpenAI 格式）"""
    if not ANTIGRAVITY_API_KEY:
        raise Exception("ANTIGRAVITY_API_KEY 未設定")

    headers = {
        "x-api-key": ANTIGRAVITY_API_KEY
    }

    # 圖生圖：使用 /v1/images/edits (multipart/form-data)
    if images:
        # OpenAI images/edits 需要使用 multipart/form-data
        files = {}
        data = {
            "prompt": prompt,
            "n": n,
            "size": size
        }

        # 添加參考圖
        try:
            with open(images[0], 'rb') as f:
                files['image'] = ('image.jpg', f, 'image/jpeg')
        except FileNotFoundError:
            raise Exception(f"找不到參考圖: {images[0]}")

        response = requests.post(ANTIGRAVITY_EDITS_URL, headers=headers, data=data, files=files, timeout=120)
        response.raise_for_status()
        return response.json()

    # 文生圖：使用 /v1/images/generations (JSON)
    else:
        payload = {
            "model": "gemini-3-pro-image",
            "prompt": prompt,
            "n": n,
            "size": size
        }

        headers["Content-Type"] = "application/json"
        response = requests.post(ANTIGRAVITY_GEN_URL, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        return response.json()

def generate_nanobanana(prompt, size="1024x1024", quality="standard", n=1, images=None):
    """使用 NanoBanana API 生成圖片"""
    if not ALLAPI_KEY:
        raise Exception("ALLAPI_KEY 未設定")

    width, height = parse_size(size)
    aspect_ratio = calculate_aspect_ratio(width, height)
    quality_level = QUALITY_MAP.get(quality, "1K")

    parts = [{"text": prompt}]

    if images:
        for image_path in images:
            parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": image_to_base64(image_path)
                }
            })

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": parts
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": quality_level
            }
        }
    }

    params = {"key": ALLAPI_KEY}
    headers = {"Content-Type": "application/json"}

    response = requests.post(ALLAPI_API_URL_TEMPLATE, params=params, json=payload, headers=headers, timeout=120)
    response.raise_for_status()
    return response.json()

def extract_images_from_antigravity(response):
    """從 Antigravity API 響應中提取圖片（OpenAI 格式）"""
    images = []
    data_list = response.get("data", [])

    for i, item in enumerate(data_list):
        # OpenAI 格式可能是 b64_json 或 url
        if "b64_json" in item:
            images.append({
                "index": i,
                "data": item["b64_json"],
                "mimeType": "image/png"  # OpenAI 默認返回 PNG
            })
        elif "url" in item:
            # 如果是 URL，下載並轉為 base64
            try:
                img_response = requests.get(item["url"], timeout=30)
                img_response.raise_for_status()
                import base64
                images.append({
                    "index": i,
                    "data": base64.b64encode(img_response.content).decode('utf-8'),
                    "mimeType": "image/png"
                })
            except Exception as e:
                print(f"⚠️  無法下載圖片 {i}: {e}", file=sys.stderr)

    return images

def extract_images_from_nanobanana(response):
    """從 NanoBanana API 響應中提取圖片"""
    images = []
    candidates = response.get("candidates", [])

    for i, candidate in enumerate(candidates):
        parts = candidate.get("content", {}).get("parts", [])
        for part in parts:
            if "inlineData" in part:
                images.append({
                    "index": i,
                    "data": part["inlineData"]["data"],
                    "mimeType": part["inlineData"].get("mimeType", "image/jpeg")
                })

    return images

def generate_image(prompt, size="1024x1024", quality="standard", n=1, images=None, force_provider=None):
    """
    智能生成圖片，優先使用 Antigravity，失敗時降級到 NanoBanana

    Args:
        prompt: 圖片描述
        size: 尺寸（WIDTHxHEIGHT 格式）
        quality: 品質（hd, medium, standard）
        n: 生成數量
        images: 參考圖路徑列表
        force_provider: 強制使用提供者

    Returns:
        生成結果
    """
    providers = []

    if force_provider == "antigravity" or (force_provider is None and ANTIGRAVITY_API_KEY):
        providers.append(("antigravity", generate_antigravity, extract_images_from_antigravity))
    if force_provider == "nanobanana" or (force_provider is None and ALLAPI_KEY):
        providers.append(("nanobanana", generate_nanobanana, extract_images_from_nanobanana))

    for provider_name, generate_func, extract_func in providers:
        try:
            print(f"🔄 嘗試使用 {provider_name} API...")
            response = generate_func(prompt, size=size, quality=quality, n=n, images=images)
            images_data = extract_func(response)

            if images_data:
                print(f"✅ {provider_name} API 成功生成 {len(images_data)} 張圖片")
                return {
                    "success": True,
                    "provider": provider_name,
                    "images": images_data,
                    "parameters": {
                        "size": size,
                        "quality": quality,
                        "n": n
                    }
                }
        except Exception as e:
            print(f"❌ {provider_name} API 失敗: {e}")
            if provider_name != providers[-1][0]:
                print(f"⏭️  自動切換到下一個提供者...")
            continue

    return {
        "success": False,
        "error": "All providers failed",
        "providers": providers
    }

def main():
    parser = argparse.ArgumentParser(
        description='Universal Image Gen - 智能圖片生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 基本用法
  python3 generate.py "一只可爱的猫咪"

  # 指定尺寸和品質
  python3 generate.py "风景照片" --size 1920x1080 --quality hd

  # 批次生成
  python3 generate.py "猫咪" --n 5

  # 使用參考圖
  python3 generate.py "改成写实风格" --images cat.jpg

  # 強制使用特定提供者
  python3 generate.py "测试" --force-provider nanobanana
        """
    )

    parser.add_argument('prompt', help='圖片描述文字')
    parser.add_argument('--size', default='1024x1024', help='尺寸（WIDTHxHEIGHT 格式）')
    parser.add_argument('--quality', choices=['hd', 'medium', 'standard'], default='standard', help='品質（hd, medium, standard）')
    parser.add_argument('--n', type=int, default=1, help='生成圖片數量（1-10）')
    parser.add_argument('--images', help='參考圖路徑列表，用逗號分隔')
    parser.add_argument('--force-provider', choices=['antigravity', 'nanobanana'], help='強制使用指定提供者')

    args = parser.parse_args()

    # 驗證參數
    if args.n < 1 or args.n > 10:
        print("錯誤: n 參數必須在 1-10 之間", file=sys.stderr)
        sys.exit(1)

    images_list = args.images.split(',') if args.images else None

    # 生成圖片
    try:
        result = generate_image(
            prompt=args.prompt,
            size=args.size,
            quality=args.quality,
            n=args.n,
            images=images_list,
            force_provider=args.force_provider
        )

        if result['success']:
            print(f"\n🎉 成功生成圖片！")
            print(f"提供者: {result['provider']}")
            print(f"數量: {len(result['images'])}")

            # 保存圖片
            for img in result['images']:
                ext = 'jpg' if 'jpeg' in img['mimeType'] else 'png'
                output_file = f"universal_gen_{img['index']}.{ext}"
                with open(output_file, 'wb') as f:
                    f.write(base64.b64decode(img['data']))
                print(f"  ✓ {output_file}")
        else:
            print(f"\n❌ 所有提供者都失敗了")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n已取消", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 發生錯誤: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
