import base64
import requests

ANTIGRAVITY_API_KEY = "YOUR_ANTIGRAVITY_API_KEY"
ALLAPI_KEY = "YOUR_ALLAPI_KEY"

# 使用方式：直接調用 generate_image 函數，會自動優先使用 Antigravity，失敗時降級到 NanoBanana

def generate_image(prompt, size="1024x1024", quality="standard", n=1, images=None, force_provider=None):
    """
    智能生成圖片，優先使用 Antigravity，失敗時自動降級到 NanoBanana

    Args:
        prompt: 圖片描述
        size: 尺寸（WIDTHxHEIGHT 格式）
        quality: 品質（hd, medium, standard）
        n: 生成數量
        images: 參考圖路徑列表
        force_provider: 強制使用提供者（antigravity, nanobanana）

    Returns:
        生成結果
    """
    # ... 實現代碼見 scripts/generate.py ...

# 使用範例

# 1. 基本用法 - 會自動選擇最佳的提供者
result = generate_image(
    prompt="一只可爱的猫咪"
)
print(result)

# 2. 指定尺寸和品質
result = generate_image(
    prompt="风景照片",
    size="1920x1080",
    quality="hd"
)
print(result)

# 3. 批次生成
result = generate_image(
    prompt="不同品种的猫咪",
    n=5
)
print(result)

# 4. 使用參考圖
result = generate_image(
    prompt="将这张照片改成动漫风格",
    images=["/path/to/photo.jpg"],
    size="1024x1024"
)
print(result)

# 5. 強制使用特定提供者
result = generate_image(
    prompt="测试图片",
    size="1280x720",
    quality="medium",
    force_provider="nanobanana"  # 強制使用 NanoBanana
)
print(result)

# 6. 圖生圖 - 自動降級到最適合的提供者
result = generate_image(
    prompt="在旁边加一只羊驼",
    images=["/path/to/character.jpg"],
    size="16:9",
    quality="hd"
)
print(result)

# 7. 多種尺寸
sizes = ["1024x1024", "1920x1080", "1080x1920", "1280x720"]
for size in sizes:
    result = generate_image(
        prompt="测试图片",
        size=size,
        quality="medium"
    )
    print(f"尺寸 {size} 生成結果: {result}")

# 8. 品質對比
qualities = ["standard", "medium", "hd"]
for quality in qualities:
    result = generate_image(
        prompt="测试图片",
        size="1024x1024",
        quality=quality
    )
    print(f"品質 {quality} 生成結果: {result}")

# 9. 錯誤處理
try:
    result = generate_image(
        prompt="测试图片",
        size="999999x999999",  # 無效尺寸
        quality="invalid"  # 無效品質
    )
except Exception as e:
    print(f"發生錯誤: {e}")

# 10. 完整參數
result = generate_image(
    prompt="一张台北 101 的风景照片，日落时分，暖色调",
    size="1920x1080",
    quality="hd",
    n=3,
    force_provider=None  # 讓系統自動選擇
)
print(result)

# 保存生成的圖片
if result['success']:
    for i, img_data in enumerate(result['images']):
        ext = 'jpg' if 'jpeg' in img_data['mimeType'] else 'png'
        with open(f"generated_{i}.{ext}", 'wb') as f:
            f.write(base64.b64decode(img_data['data']))
        print(f"圖片已保存: generated_{i}.{ext}")
