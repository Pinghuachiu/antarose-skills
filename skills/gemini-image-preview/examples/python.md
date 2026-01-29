import base64
import requests

API_KEY = "YOUR_API_KEY"
# 可選模型
MODEL_PRO = "gemini-3-pro-image-preview"  # NanoBanana Pro (最強）
MODEL_FLASH = "gemini-2.5-flash-image"  # Flash (快速）

def image_to_base64(image_path):
    """將圖片轉為 base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

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
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": image_size
            }
        }
    }

    # 發送請求
    params = {"key": API_KEY}
    headers = {"Content-Type": "application/json"}

    response = requests.post(api_url, params=params, json=payload, headers=headers)
    return response.json()

# 使用範例

# 1. 文生圖 - Pro 版本 4K 品質
result = generate_image(
    prompt="一隻可愛的貓咪在陽光下玩耍",
    aspect_ratio="1:1",
    image_size="4K",  # 最高品質
    model=MODEL_PRO
)
print(result)

# 2. 文生圖 - Flash 版本（快速）
result = generate_image(
    prompt="一隻貓",
    aspect_ratio="1:1",
    image_size="HIGH",  # Flash 版本使用 HIGH
    model=MODEL_FLASH
)
print(result)

# 3. 圖生圖 - Pro 版本 2K 品質
result = generate_image(
    prompt="在旁邊加一隻羊駝",
    images=["/path/to/your/image.jpg"],
    aspect_ratio="16:9",
    image_size="2K",  # 平衡品質和成本
    model=MODEL_PRO
)
print(result)

# 4. 多圖合成（最多14張）
result = generate_image(
    prompt="將這些圖片融合在一起，創建一個場景",
    images=["/path/to/image1.jpg", "/path/to/image2.jpg", "/path/to/image3.jpg"],
    aspect_ratio="16:9",
    image_size="2K",  # 推薦用於多圖合成
    model=MODEL_PRO
)
print(result)

# 5. 使用別名
result = generate_image(
    prompt="創建一張海報",
    aspect_ratio="21:9",  # 寬屏格式
    image_size="4K",
    model=MODEL_PRO
)
print(result)
