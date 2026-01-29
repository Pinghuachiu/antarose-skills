---
name: universal-image-gen
description: 智能圖片生成技能，優先使用 Antigravity API，失敗時自動降級到 NanoBanana。支援任意尺寸、多種品質和批次生成。
metadata:
  category: generation
  type: image
  languages:
    - python
    - javascript
    - bash
  supports:
    - text-to-image
    - image-to-image
    - flexible-resolutions
    - auto-fallback
  max_images_per_request: 10
---

# Universal Image Gen - 智能圖片生成技能

智能圖片生成工具，優先使用 Antigravity API，失敗時自動降級到 NanoBanana。支援任意尺寸、多種品質和批次生成。

## API 資訊

### 優先：Antigravity API

- **API 提供商**: Antigravity
- **API Key**: `sk-78ccc58191b14c10911c61be665691f0`
- **Base URL**: `http://192.168.1.159:8045/v1`
- **Endpoint**: `/messages`
- **模型**: `gemini-3-pro-image`

### 降級：NanoBanana (AllAPI)

- **API 提供商**: AllAPI
- **API Key**: `sk-eJtw92E4YJZrdF6bv0bjiIU4DAwo8nHC3XPZeQFRxwZ5i6mM`
- **Base URL**: `https://allapi.store/v1beta`
- **Endpoint**: `/models/gemini-3-pro-image-preview:generateContent`
- **模型**: `gemini-3-pro-image-preview`

## 功能特性

### 1. 智能降級機制

- 優先使用 Antigravity API（**只支持文生圖**）
- 失敗時自動切換到 NanoBanana
- NanoBanana 支援文生圖和圖生圖
- 無需手動切換，完全自動化

**⚠️ 重要提示**：Antigravity API 目前確認**只支持文生圖**，不支援圖生圖功能。如果需要圖生圖（使用參考圖），請使用 `--force-provider nanobanana` 參數。

### 2. 彈性尺寸支援

支援任意 `WIDTHxHEIGHT` 格式，自動映射到標準寬高比：

| 輸入尺寸 | 自動映射 | 寬高比 |
|---------|---------|---------|
| 1920x1080 | 1920x1080 | 16:9 |
| 1280x720 | 1280x720 | 16:9 |
| 1024x1024 | 1024x1024 | 1:1 |
| 1080x1920 | 1080x1920 | 9:16 |
| 1440x2560 | 1440x2560 | 9:16 |
| 7680x4320 | 7680x4320 | 16:9 (8K) |
| 自定義 | 最近標準尺寸 | 自動調整 |

支援的標準寬高比：
- `21:9` - 超寬屏
- `16:9` - 橫向
- `16:10` - 寬屏
- `9:16` - 直向
- `4:3` - 傳統橫向
- `3:4` - 傳統直向
- `1:1` - 正方形

### 3. 多種品質選項

| 品質選項 | 分辨率 | 說明 |
|---------|--------|------|
| `hd` | 4K | 最高品質，適合列印或展示 |
| `medium` | 2K | 中等品質，平衡速度和品質 |
| `standard` | 標準 | 預設品質，快速生成 |

### 4. 批次生成

- 支援一次生成 1-10 張圖片
- 提高生成效率
- 適合多樣化需求

### 5. 圖生圖支援

支援基於參考圖生成新圖片。

## 快速開始

### 使用可執行腳本

**Python**：
```bash
# 基本用法
python3 .opencode/skills/universal-image-gen/scripts/generate.py "一只可爱的猫咪"

# 指定尺寸和品質
python3 .opencode/skills/universal-image-gen/scripts/generate.py "风景照片" --size 1920x1080 --quality hd

# 批次生成
python3 .opencode/skills/universal-image-gen/scripts/generate.py "猫咪" --n 5

# 使用參考圖
python3 .opencode/skills/universal-image-gen/scripts/generate.py "改成写实风格" --images cat.jpg
```

**Node.js**：
```bash
node .opencode/skills/universal-image-gen/scripts/generate.js "一只可爱的猫咪" --size 1920x1080 --quality hd --n 5
```

### 查看詳細範例

- **Python 範例**: 參見 [examples/python.md](examples/python.md)
- **JavaScript 範例**: 參見 [examples/javascript.md](examples/javascript.md)
- **Bash 命令範例**: 參見 [examples/bash.md](examples/bash.md)

## 請求參數

### Python 腳本參數

| 參數 | 必填 | 預設值 | 說明 |
|------|------|--------|------|
| `prompt` | ✅ | - | 圖片描述文字 |
| `--size` | ❌ | `1024x1024` | 尺寸（WIDTHxHEIGHT 格式） |
| `--quality` | ❌ | `standard` | 品質（hd, medium, standard） |
| `--n` | ❌ | `1` | 生成圖片數量（1-10） |
| `--images` | ❌ | - | 參考圖路徑（逗號分隔） |
| `--force-provider` | ❌ | - | 強制使用指定提供者（antigravity, nanobanana） |

### Node.js 腳本參數

與 Python 腳本相同。

## API 請求格式

### Antigravity API 格式

```json
{
  "model": "gemini-3-pro-image",
  "size": "1280x720",
  "quality": "hd",
  "messages": [
    {
      "role": "user",
      "content": "一只可爱的猫咪"
    }
  ]
}
```

### NanoBanana API 格式

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        { "text": "一只可爱的猫咪" }
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
}
```

## 尺寸映射規則

系統會根據輸入尺寸自動映射到最近的標準寬高比：

### 1. 計算目標寬高比

```
目標寬高比 = 輸入寬度 / 輸入高度
```

### 2. 查找最近的標準寬高比

比對以下標準寬高比：
- 21:9 (2.333...)
- 16:10 (1.6)
- 16:9 (1.777...)
- 4:3 (1.333...)
- 1:1 (1.0)
- 3:4 (0.75)
- 9:16 (0.5625)

### 3. 計算實際輸出尺寸

根據品質和寬高比計算最終尺寸：

| 品質 | 1:1 | 16:9 | 9:16 | 21:9 |
|------|------|-------|-------|-------|
| standard | 1024x1024 | 1344x768 | 768x1344 | 1536x672 |
| medium | 2048x2048 | 2752x1536 | 1536x2752 | 3168x1344 |
| hd | 4096x4096 | 5504x3072 | 3072x5504 | 6336x2688 |

## 品質選項詳解

### HD (高品質)

- **解析度**: 4K
- **用例**: 列印、展示、專業用途
- **生成時間**: 較長
- **成本**: 最高

### Medium (中等品質)

- **解析度**: 2K
- **用例**: 網站、社交媒體、一般用途
- **生成時間**: 中等
- **成本**: 中等

### Standard (標準)

- **解析度**: 預設
- **用例**: 快速預覽、測試
- **生成時間**: 最快
- **成本**: 最低

## 批次生成

### Python 範例

```python
result = generate_image(
    prompt="不同品种的猫咪",
    n=5  # 生成 5 張圖片
)

for i, image_data in enumerate(result['images']):
    with open(f"cat_{i+1}.jpg", 'wb') as f:
        f.write(base64.b64decode(image_data))
```

### Node.js 範例

```javascript
const result = await generateImage({
  prompt: '不同品种的猫咪',
  n: 5
});

result.images.forEach((imageData, i) => {
  fs.writeFileSync(`cat_${i+1}.jpg`, Buffer.from(imageData, 'base64'));
});
```

## 圖生圖

### 使用參考圖

```bash
python3 scripts/generate.py \
  "将这张照片改成动漫风格" \
  --images /path/to/reference.jpg \
  --size 1024x1024
```

### 多張參考圖

```bash
python3 scripts/generate.py \
  "融合这些图片的风格" \
  --images img1.jpg,img2.jpg,img3.jpg \
  --size 1920x1080 \
  --quality hd
```

## 回應格式

### 成功回應

```json
{
  "success": true,
  "provider": "antigravity",
  "images": [
    {
      "index": 0,
      "data": "base64_encoded_image",
      "mimeType": "image/jpeg"
    }
  ],
  "parameters": {
    "size": "1280x720",
    "quality": "hd",
    "n": 1
  }
}
```

### 錯誤回應

```json
{
  "success": false,
  "error": "All providers failed",
  "providers": [
    {
      "name": "antigravity",
      "error": "Connection timeout",
      "fallback_attempted": true
    },
    {
      "name": "nanobanana",
      "error": "API key invalid"
    }
  ]
}
```

## 錯誤處理

### 自動重試機制

1. 第一次嘗試：Antigravity API
2. 如果失敗：自動降級到 NanoBanana
3. 如果都失敗：返回錯誤資訊

### 常見錯誤

| 錯誤 | 原因 | 解決方案 |
|------|------|----------|
| Connection timeout | 網路連線失敗 | 檢查網路連線 |
| API key invalid | API Key 錯誤 | 檢查 API Key 設定 |
| Invalid size | 尺寸格式錯誤 | 使用 WIDTHxHEIGHT 格式 |
| Invalid quality | 品質參數錯誤 | 使用 hd, medium 或 standard |
| All providers failed | 所有提供者都失敗 | 檢查設定或稍後重試 |

## 最佳實踐

### 選擇適當的尺寸

| 用途 | 推薦尺寸 | 寬高比 |
|------|---------|--------|
| Instagram 貼文 | 1080x1080 | 1:1 |
| YouTube 縮圖 | 1280x720 | 16:9 |
| 手機桌布 | 1080x1920 | 9:16 |
| 電腦桌布 | 1920x1080 | 16:9 |
| 社交媒體直版 | 1080x1920 | 9:16 |

### 選擇適當的品質

| 場景 | 推薦品質 | 原因 |
|------|----------|------|
| 快速測試 | standard | 生成快速 |
| 日常使用 | medium | 平衡速度和品質 |
| 專業用途 | hd | 最高品質 |
| 批次生成 | medium | 平衡效率和品質 |

### 優化提示詞

1. 使用具體的描述
2. 指定藝術風格
3. 描述光照和氛圍
4. 添加技術參數

## 注意事項

1. **API Key**: 必須設定環境變數 `ANTIGRAVITY_API_KEY` 和 `ALLAPI_KEY`
2. **尺寸格式**: 必須使用 `WIDTHxHEIGHT` 格式（如 1280x720）
3. **品質限制**: 必須使用 hd、medium 或 standard
4. **數量限制**: 最多一次生成 10 張圖片
5. **自動降級**: 優先使用 Antigravity，失敗自動切換到 NanoBanana
6. **網路連線**: 需要穩定的網路連線
7. **檔案格式**: 輸出格式為 JPEG

## 環境變數

```bash
# Antigravity API (優先)
export ANTIGRAVITY_API_KEY="sk-78ccc58191b14c10911c61be665691f0"

# NanoBanana API (降級)
export ALLAPI_KEY="sk-eJtw92E4YJZrdF6bv0bjiIU4DAwo8nHC3XPZeQFRxwZ5i6mM"
```

請參考 [resource.md](../../../resource.md) 獲取 API Key。

## 安全提示

1. 不要在程式碼中硬編碼 API Key
2. 使用環境變數或設定檔
3. 請參考 [resource.md](../../../resource.md) 獲取 API Key
