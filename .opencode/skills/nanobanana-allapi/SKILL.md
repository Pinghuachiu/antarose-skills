---
name: nanobanana-allapi
description: 使用 AllAPI 提供的 NanoBanana 模型進行圖片生成，支援文生圖、圖生圖、多圖合成。提供兩個模型選項：nanobanana-3-pro-image (NanoBanana Pro) 和 nanobanana-2.5-flash-image (Flash)
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
    - multi-image-composition
  max_reference_images: 14
---

# NanoBanana AllAPI - 圖片生成技能

使用 AllAPI 提供的 NanoBanana 模型進行圖片生成，支援文生圖、圖生圖、多圖合成。

## API 資訊

- **API 提供商**: AllAPI (allapi.store)
- **模型選項**:
  - `nanobanana-3-pro-image` (NanoBanana Pro) - 最強大的圖片生成模型
  - `nanobanana-2.5-flash-image` (Flash) - 快速圖片生成模型
- **Endpoint**: `POST /v1beta/models/{model-name}:generateContent`
- **Base URL**: `https://allapi.store/`
- **官方文檔**: https://help.allapi.store

## 模型說明

### nanobanana-3-pro-image (NanoBanana Pro)

- 最強大的圖片生成模型
- 支援文生圖、圖生圖、多圖合成
- 最高品質輸出（支援 4K）
- 最多支援 14 張參考圖
- 三種分辨率級別：1K、2K、4K

### nanobanana-2.5-flash-image (Flash)

- 快速圖片生成模型
- 適合快速原型和迭代
- 品質略低於 Pro 版本
- 同樣支援多圖參考
- 單一分辨率級別

## 功能支援

### 1. 文生圖 (Text-to-Image)

透過文字描述生成圖片，適合創意生成和概念設計。

### 2. 圖生圖 (Image-to-Image)

基於上傳的圖片進行修改或擴展，適合照片風格轉換和增強。

### 3. 多圖合成

結合多張圖片生成新圖片（最多 14 張），適合風格融合和場景創建。

## 快速開始

### 使用可執行腳本

**Python**：
```bash
python3 .opencode/skills/nanobanana-allapi/scripts/generate.py \
  "一隻可愛的貓咪在陽光下玩耍" \
  --ratio 16:9 \
  --size 4K
```

**Node.js**：
```bash
node .opencode/skills/nanobanana-allapi/scripts/generate.js \
  "一隻可愛的貓咪在陽光下玩耍" \
  --ratio 16:9 \
  --size 4K
```

### 查看詳細範例

- **Python 範例**: 參見 [examples/python.md](examples/python.md)
- **JavaScript 範例**: 參見 [examples/javascript.md](examples/javascript.md)
- **Bash 命令範例**: 參見 [examples/bash.md](examples/bash.md)

## 請求參數

### Query Parameters

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `key` | string | 是 | API Key |

### Headers

| 參數 | 值 | 必填 |
|------|---|------|
| `Content-Type` | `application/json` | 是 |

### Request Body

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        { "text": "圖片描述" },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
            "data": "base64_encoded_image"
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9",
      "imageSize": "1K"
    }
  }
}
```

#### contents 說明

- `text`: 圖片描述文字（文生圖時必需，圖生圖時可選）
- `inline_data`: 圖片的 base64 編碼（圖生圖時必需）
  - `mime_type`: 圖片類型，支援 `image/jpeg`, `image/png`, `image/webp`, `image/heic`
  - `data`: 圖片的 base64 編碼字串

**參考圖數量限制**：
- 最多支援 **14 張**參考圖片
- 可以在 `parts` 數組中添加多個 `inline_data`
- 建議在描述中清楚說明每張圖片的用途

#### generationConfig 說明

- `responseModalities`: 返回類型，必須包含 `["IMAGE"]`
- `imageConfig`:
  - `aspectRatio`: 寬高比
    - Pro 版本支援：`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `16:10`, `21:9`
    - Flash 版本支援：`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`
  - `imageSize`: 圖片大小和分辨率（僅 Pro 版本支援多級別）
    - `1K`: 1024x1024 (1:1) 等
    - `HIGH`: 高品質（別名，等同於 2K）
    - `MEDIUM`: 中等品質（Flash 版本預設）
    - `2K`: 2048x2048 (1:1) 等
    - `4K`: 4096x4096 (1:1) 等

## 分辨率詳解

### NanoBanana 2.5 Flash 版本

**單一分辨率級別**：每個寬高比固定使用 **1290 tokens**

| 寬高比 | 分辨率 | Tokens |
|---------|---------|---------|
| 1:1 | 1024x1024 | 1290 |
| 2:3 | 832x1248 | 1290 |
| 3:2 | 1248x832 | 1290 |
| 3:4 | 864x1184 | 1290 |
| 4:3 | 1184x864 | 1290 |
| 4:5 | 896x1152 | 1290 |
| 9:16 | 768x1344 | 1290 |
| 16:9 | 1344x768 | 1290 |
| 21:9 | 1536x672 | 1290 |

### NanoBanana 3 Pro Image 版本

**三種分辨率級別**：根據需求選擇

| 寬高比 | 1K 分辨率 (1120 tokens) | 2K 分辨率 (1120 tokens) | 4K 分辨率 (2000 tokens) |
|---------|-----------------------|-----------------------|-----------------------|
| 1:1 | 1024x1024 | 2048x2048 | 4096x4096 |
| 2:3 | 848x1264 | 1696x2528 | 3392x5056 |
| 3:2 | 1264x848 | 2528x1696 | 5056x3392 |
| 3:4 | 896x1200 | 1792x2400 | 3584x4800 |
| 4:3 | 1200x896 | 2400x1792 | 4800x3584 |
| 4:5 | 928x1152 | 1856x2304 | 3712x4608 |
| 5:4 | 1152x928 | 2304x1856 | 4608x3712 |
| 9:16 | 768x1376 | 1536x2752 | 3072x5504 |
| 16:9 | 1376x768 | 2752x1536 | 5504x3072 |
| 16:10 | 1376x860 | 2752x1720 | 5504x3440 |
| 21:9 | 1584x672 | 3168x1344 | 6336x2688 |

### 使用建議

- **Flash 版本**：快速迭代，使用預設值（自動調整到 1290 tokens）
- **Pro 版本 - 1K**：快速預覽，1120 tokens
- **Pro 版本 - 2K/HIGH**：平衡品質和成本，1120 tokens（推薦）
- **Pro 版本 - 4K**：最高品質，2000 tokens（需要最多 tokens）

## 可執行腳本

### Python 腳本

**使用方法**：
```bash
# 基本用法
python3 scripts/generate.py "生成一張風景照"

# 使用參考圖
python3 scripts/generate.py "將這些圖片融合" --images photo1.jpg,photo2.jpg

# 指定寬高比和品質
python3 scripts/generate.py "海報" --ratio 21:9 --size 4K

# 使用 Flash 模型
python3 scripts/generate.py "快速生成" --model flash
```

**參數**：
- `prompt`: 圖片描述文字（必需）
- `--images`: 圖片路徑列表，用逗號分隔（最多 14 張）
- `--ratio`: 寬高比（預設 1:1）
- `--size`: 圖片大小（預設 2K）
- `--model`: 模型選擇（預設 pro）

### Node.js 腳本

**使用方法**：
```bash
# 基本用法
node scripts/generate.js "生成一張風景照"

# 使用參考圖
node scripts/generate.js "將這些圖片融合" --images photo1.jpg,photo2.jpg

# 指定寬高比和品質
node scripts/generate.js "海報" --ratio 21:9 --size 4K

# 使用 Flash 模型
node scripts/generate.js "快速生成" --model flash
```

**參數**：
- `prompt`: 圖片描述文字（必需）
- `--images`: 圖片路徑列表，用逗號分隔（最多 14 張）
- `--ratio`: 寬高比（預設 1:1）
- `--size`: 圖片大小（預設 2K）
- `--model`: 模型選擇（預設 pro）

## 回應格式

成功生成圖片後的回應：

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "inlineData": {
              "data": "base64_encoded_image",
              "mimeType": "image/png"
            }
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP"
    }
  ]
}
```

### 回應欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `candidates` | array | 生成結果數組 |
| `content.parts` | array | 內容部分 |
| `inlineData.data` | string | 生成的圖片 (base64 編碼) |
| `inlineData.mimeType` | string | 圖片類型 |
| `finishReason` | string | 完成原因 |

## 圖片參數選項

### aspectRatio (寬高比)

- `1:1` - 正方形
- `16:9` - 橫向
- `9:16` - 直向
- `4:3` - 傳統橫向
- `3:4` - 傳統直向

### imageSize (圖片大小)

- `1K` - 1K 分辨率
- `HIGH` - 高品質（推薦用於最佳效果）
- `MEDIUM` - 中等品質
- `2K` - 2K 分辨率
- `4K` - 4K 分辨率（最高品質）

## 注意事項

1. **API Key**: 必須在 query 參數中提供有效的 API Key
2. **環境變數**: 使用前請設定 `ALLAPI_KEY` 環境變數
   ```bash
   export ALLAPI_KEY="your-api-key-here"
   ```
   請參考 [resource.md](../../../resource.md) 獲取 API Key
3. **圖片格式**: 支援 JPEG、PNG、WebP、HEIC 格式
4. **Base64 編碼**: 圖片需要轉換為 base64 編碼
5. **參考圖數量**: 最多支援 14 張圖片
6. **提示詞**: 清晰的描述能獲得更好的結果
7. **寬高比**: 根據用途選擇合適的寬高比
8. **清理 /tmp**: 腳本會自動清理 /tmp 目錄中的暫存檔案，任務結束後會清除本腳本創建的暫存檔案

## 錯誤處理

### 401 Unauthorized

```json
{
  "error": {
    "code": 401,
    "message": "Request had invalid authentication credentials.",
    "status": "UNAUTHENTICATED"
  }
}
```

**解決方案**: 檢查 API Key 是否正確

### 400 Bad Request

```json
{
  "error": {
    "code": 400,
    "message": "Invalid request",
    "status": "INVALID_ARGUMENT"
  }
}
```

**可能原因**:
- 請求格式錯誤
- 缺少必要參數
- 圖片 base64 編碼錯誤

### 429 Too Many Requests

```json
{
  "error": {
    "code": 429,
    "message": "Quota exceeded",
    "status": "RESOURCE_EXHAUSTED"
  }
}
```

**解決方案**: 等待後重試或升級 API 配額

## 高級用法

### 同時獲取文字和圖片

```json
{
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9"
    }
  }
}
```

### 負面提示詞

在描述中加入「不要」或「避免」等詞來排除不需要的元素：

```json
{
  "contents": [
    {
      "parts": [
        { "text": "生成一張海灘風景圖，不要有人物，不要建築物" }
      ]
    }
  ]
}
```

### 多輪對話

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{ "text": "生成一張日出的圖片" }]
    },
    {
      "role": "model",
      "parts": [{ "text": "好的，這是一張日出的圖片" }]
    },
    {
      "role": "user",
      "parts": [{ "text": "現在改成夕陽的風格" }]
    }
  ]
}
```

## 最佳實踐

### 選擇模型和品質

| 場景 | 推薦模型 | 推薦品質 |
|------|----------|----------|
| 快速原型 | Flash | HIGH |
| 日常使用 | Pro | 2K |
| 高品質輸出 | Pro | 4K |
| 成本敏感 | Pro | 1K |
| 多圖合成 | Pro | 2K |

### 優化提示詞

1. 使用具體的描述詞
2. 指定藝術風格
3. 描述光照和氛圍
4. 添加技術參數

### 錯誤處理

1. 檢查 API Key 配置
2. 驗證圖片格式
3. 確認 base64 編碼正確
4. 檢查請求參數
5. 查看 API 限額

## AllAPI 說明

本技能使用 AllAPI (allapi.store) 提供的 NanoBanana 3 Pro Image API。Base URL 已設置為 `https://allapi.store/v1beta`。

如需獲取 AllAPI 的 API Key，請訪問 https://help.allapi.store
