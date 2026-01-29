# Gemini Image Preview - Bash 使用範例

## 設置 API Key

```bash
export API_KEY="YOUR_API_KEY"
```

## 1. 文生圖

### 使用 Pro 版本
```bash
curl -X POST "https://allapi.store/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "role": "user",
        "parts": [
          { "text": "一隻可愛的貓咪在陽光下玩耍" }
        ]
      }
    ],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "1:1",
        "imageSize": "HIGH"
      }
    }
  }'
```

### 使用 Flash 版本（快速）
```bash
curl -X POST "https://allapi.store/v1beta/models/gemini-2.5-flash-image:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "role": "user",
        "parts": [
          { "text": "快速生成一隻貓" }
        ]
      }
    ],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "1:1",
        "imageSize": "HIGH"
      }
    }
  }'
```

## 2. 圖生圖

```bash
# 先將圖片轉為 base64
IMAGE_BASE64=$(base64 -i /path/to/your/image.jpg)

curl -X POST "https://allapi.store/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [
      {
        \"role\": \"user\",
        \"parts\": [
          { \"text\": \"在旁邊加一隻羊駝\" },
          {
            \"inline_data\": {
              \"mime_type\": \"image/jpeg\",
              \"data\": \"$IMAGE_BASE64\"
            }
          }
        ]
      }
    ],
    \"generationConfig\": {
      \"responseModalities\": [\"IMAGE\"],
      \"imageConfig\": {
        \"aspectRatio\": \"16:9\",
        \"imageSize\": \"2K\"
      }
    }
  }"
```

## 3. 多圖合成（最多 14 張）

```bash
# 將多張圖片轉為 base64
IMAGE1_BASE64=$(base64 -i /path/to/image1.jpg)
IMAGE2_BASE64=$(base64 -i /path/to/image2.jpg)
IMAGE3_BASE64=$(base64 -i /path/to/image3.jpg)

curl -X POST "https://allapi.store/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [
      {
        \"role\": \"user\",
        \"parts\": [
          { \"text\": \"將這些圖片融合在一起\" },
          {
            \"inline_data\": {
              \"mime_type\": \"image/jpeg\",
              \"data\": \"$IMAGE1_BASE64\"
            }
          },
          {
            \"inline_data\": {
              \"mime_type\": \"image/jpeg\",
              \"data\": \"$IMAGE2_BASE64\"
            }
          },
          {
            \"inline_data\": {
              \"mime_type\": \"image/jpeg\",
              \"data\": \"$IMAGE3_BASE64\"
            }
          }
        ]
      }
    ],
    \"generationConfig\": {
      \"responseModalities\": [\"IMAGE\"],
      \"imageConfig\": {
        \"aspectRatio\": \"16:9\",
        \"imageSize\": \"2K\"
      }
    }
  }"
```

## 4K 品質生成

```bash
curl -X POST "https://allapi.store/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "role": "user",
        "parts": [
          { "text": "高品質風景照片" }
        ]
      }
    ],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9",
        "imageSize": "4K"
      }
    }
  }'
```

## 保存回應中的圖片

```bash
# 使用 jq 解析 JSON 並保存圖片
curl -X POST "https://allapi.store/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"role":"user","parts":[{"text":"生成一張圖片"}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1","imageSize":"HIGH"}}}' \
  | jq -r '.candidates[0].content.parts[0].inlineData.data' \
  | base64 -d > output.jpg

echo "圖片已保存到 output.jpg"
```

## 常用寬高比

| 寬高比 | 說明 | 用途 |
|---------|------|------|
| 1:1 | 正方形 | Instagram, 頭像 |
| 16:9 | 橫向 | YouTube, 桌面 |
| 9:16 | 直向 | 手機牆紙, Instagram Stories |
| 4:3 | 傳統橫向 | 平板, 舊螢幕 |
| 3:4 | 傳統直向 | 平板直向 |
| 16:10 | 超寬屏 | 海報, 橫幅 |
| 21:9 | 電影院寬屏 | 電影海報 |
