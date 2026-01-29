---
name: pix2-upload
description: 使用 Pix2 API 上傳檔案到圖床服務，支援 PNG、JPEG、WebP、MP3、MP4 格式
---

# Pix2 圖床上傳技能

使用 Pix2 API 上傳檔案到圖床服務，支援 PNG、JPEG、WebP、MP3、MP4 格式。

## API 資訊

- **Production API URL**: `https://api.pix2.io/api/images`
- **API Key**: `23df301b63a33587541a8680ef9472b9`
- **最大檔案大小**: 50MB
- **支援格式**: PNG、JPG、JPEG、WebP、MP3、MP4

## 支援的檔案類型

- 圖片: `image/png`, `image/jpeg`, `image/jpg`, `image/webp`
- 音訊: `audio/mpeg` (MP3)
- 影片: `video/mp4` (MP4)

## 使用方法

### 使用 curl 上傳

```bash
curl -X POST "https://api.pix2.io/api/images" \
  -H "x-api-key: 23df301b63a33587541a8680ef9472b9" \
  -F "file=@/path/to/your/file.ext"
```

### 使用 Python 上傳

```python
import requests

API_KEY = '23df301b63a33587541a8680ef9472b9'
API_URL = 'https://api.pix2.io/api/images'

def upload_file(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        headers = {'x-api-key': API_KEY}
        response = requests.post(API_URL, headers=headers, files=files)
        return response.json()

# 使用範例
result = upload_file('your-file.jpg')
print(result)
```

### 使用 JavaScript (Node.js) 上傳

```javascript
const FormData = require('form-data');
const fs = require('fs');
const fetch = require('node-fetch');

const API_KEY = '23df301b63a33587541a8680ef9472b9';
const API_URL = 'https://api.pix2.io/api/images';

async function uploadFile(filePath) {
  const form = new FormData();
  form.append('file', fs.createReadStream(filePath));

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'x-api-key': API_KEY,
    },
    body: form,
  });

  return response.json();
}

// 使用範例
uploadFile('your-file.jpg').then(console.log);
```

## 回應格式

成功上傳後的回應：

```json
{
  "success": true,
  "id": "PLTeqRK5",
  "url": "https://pix2.io/PLTeqRK5",
  "directUrl": "https://i.pix2.io/PLTeqRK5.jpg",
  "originalName": "my-image.jpg",
  "size": 19903,
  "contentType": "image/jpeg",
  "uploadTime": "2025-12-08T03:54:51.103Z"
}
```

## 回應欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `success` | boolean | 是否成功 |
| `id` | string | 檔案唯一 ID (8 字元) |
| `url` | string | 短網址 (會 redirect 到檔案) |
| `directUrl` | string | 檔案直連 CDN URL |
| `originalName` | string | 原始檔名 |
| `size` | number | 檔案大小 (bytes) |
| `contentType` | string | MIME 類型 |
| `uploadTime` | string | 上傳時間 (ISO 8601) |

## 注意事項

1. **認證**: 所有請求必須在 Header 中提供 `x-api-key`
2. **檔案大小**: 最大 50MB
3. **格式限制**: 只支援 PNG、JPG、JPEG、WebP、MP3、MP4 格式
4. **永久保存**: API Key 上傳的檔案不會被自動清理
5. **CDN 快取**: 檔案上傳後會被 CDN 快取，快取時間為 1 年

## 錯誤處理

### 401 Unauthorized

```json
{
  "error": "Unauthorized",
  "message": "API Key is required. Provide x-api-key header."
}
```

### 400 Bad Request

```json
{
  "error": "No file provided"
}
```

```json
{
  "error": "Invalid file type",
  "message": "Only image files are allowed (PNG, JPG, WEBP)",
  "allowedTypes": ["PNG", "JPG", "WEBP"]
}
```

### 413 Payload Too Large

```json
{
  "error": "File too large (max 50MB)"
}
```

## 其他 API 操作

除了上傳，Pix2 API 還支援以下操作：

- **列出檔案**: `GET /api/images` (支援分頁)
- **查詢單個檔案**: `GET /api/images/:id`
- **刪除檔案**: `DELETE /api/images/:id`

詳細資訊請參考 `resource.md` 檔案中的 Pix2 Image API 章節。
