# Universal Image Gen - Bash 使用範例

## 設置 API Key

```bash
# Antigravity API (優先）
export ANTIGRAVITY_API_KEY="sk-78ccc58191b14c10911c61be665691f0"

# NanoBanana API (降級）
export ALLAPI_KEY="sk-eJtw92E4YJZrdF6bv0bjiIU4DAwo8nHC3XPZeQFRxwZ5i6mM"
```

## 1. 基本用法 - 自動選擇提供者

```bash
# 使用 Python 腳本
python3 .opencode/skills/universal-image-gen/scripts/generate.py "一只可爱的猫咪"

# 使用 Node.js 腳本
node .opencode/skills/universal-image-gen/scripts/generate.js "一只可爱的猫咪"
```

**說明**: 自動優先使用 Antigravity API，失敗時降級到 NanoBanana

## 2. 指定尺寸和品質

```bash
# 1920x1080, HD 品質
python3 .opencode/skills/universal-image-gen/scripts/generate.py "风景照片" \
  --size 1920x1080 \
  --quality hd

# 1280x720, Medium 品質
node .opencode/skills/universal-image-gen/scripts/generate.js "风景照片" \
  --size 1280x720 \
  --quality medium
```

**支持的尺寸**: 任意 WIDTHxHEIGHT 格式（如 1024x1024, 1920x1080, 1080x1920）  
**支持的品質**: hd (4K), medium (2K), standard (預設)

## 3. 批次生成

```bash
# 生成 5 張圖片
python3 .opencode/skills/universal-image-gen/scripts/generate.py "不同品种的猫咪" \
  --n 5

# 生成 3 張圖片（Node.js）
node .opencode/skills/universal-image-gen/scripts/generate.js "不同品种的猫咪" \
  --n 3
```

**說明**: 一次生成多張圖片，提高效率（最多 10 張）

## 4. 使用參考圖

```bash
# 單張參考圖
python3 .opencode/skills/universal-image-gen/scripts/generate.py \
  "将这张照片改成动漫风格" \
  --images /path/to/photo.jpg \
  --size 1024x1024

# 多張參考圖
node .opencode/skills/universal-image-gen/scripts/generate.js \
  "融合这些图片的风格" \
  --images img1.jpg,img2.jpg,img3.jpg \
  --size 1920x1080
```

## 5. 強制使用特定提供者

```bash
# 強制使用 Antigravity
python3 .opencode/skills/universal-image-gen/scripts/generate.py \
  "测试图片" \
  --force-provider antigravity

# 強制使用 NanoBanana
node .opencode/skills/universal-image-gen/scripts/generate.js \
  "测试图片" \
  --force-provider nanobanana
```

## 6. 常用尺寸範例

### 正方形（1:1）
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" --size 1024x1024
```

### 橫向 16:9
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" --size 1920x1080
```

### 直向 9:16
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" --size 1080x1920
```

### 超寬屏 21:9
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" --size 3840x1640
```

## 7. 品質對比

### Standard (標準）- 最快
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" \
  --size 1024x1024 \
  --quality standard
```

### Medium (中等）- 平衡
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" \
  --size 1024x1024 \
  --quality medium
```

### HD (高清）- 最好
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" \
  --size 1024x1024 \
  --quality hd
```

## 8. 實際應用範例

### Instagram 貼文（1:1）
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "美食照片" \
  --size 1080x1080 \
  --quality hd
```

### YouTube 縮圖（16:9）
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "科技感場景" \
  --size 1280x720 \
  --quality hd
```

### 手機桌布（9:16）
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "風景照片" \
  --size 1080x1920 \
  --quality hd
```

### Twitter 橫幅（21:9）
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "抽象藝術" \
  --size 3840x1640 \
  --quality medium
```

## 9. 錯誤處理

### 檢查 API Key 是否設定
```bash
# 檢查 Antigravity API Key
echo $ANTIGRAVITY_API_KEY

# 檢查 NanoBanana API Key
echo $ALLAPI_KEY
```

### 測試連線
```bash
# 測試 Antigravity API
curl -X POST http://192.168.1.159:8045/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTIGRAVITY_API_KEY" \
  -d '{
    "model": "gemini-3-pro-image",
    "size": "1280x720",
    "quality": "hd",
    "messages": [{"role": "user", "content": "测试"}]
  }'
```

## 10. 批次腳本範例

```bash
#!/bin/bash

# 批次生成不同主題的圖片
PROMPTS=(
  "一只可爱的猫咪"
  "风景照片"
  "科技感場景"
  "美食照片"
  "抽象藝術"
)

for i in "${!PROMPTS[@]}"; do
  PROMPT="${PROMPTS[$i]}"
  echo "生成第 $((i+1))/5 張: $PROMPT"

  python3 .opencode/skills/universal-image-gen/scripts/generate.py \
    "$PROMPT" \
    --size 1024x1024 \
    --quality medium
done

echo "✅ 全部完成！"
```

## 11. 組合使用範例

### 生成 + 上傳到 Pix2 + Discord 通知
```bash
#!/bin/bash

# 生成圖片
python3 .opencode/skills/universal-image-gen/scripts/generate.py \
  "一只可爱的猫咪" \
  --size 1280x720 \
  --quality hd

# 等待生成完成
sleep 2

# 上傳到 Pix2
curl -X POST "https://api.pix2.io/api/images" \
  -H "x-api-key: YOUR_PIX2_API_KEY" \
  -F "file=@universal_gen_0.jpg"

# 發送 Discord 通知
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "embeds": [{
      "title": "✅ 圖片生成完成",
      "description": "使用 Universal Image Gen 生成",
      "color": 5814783
    }]
  }'
```

## 12. 尺寸自動映射說明

系統會自動將輸入的尺寸映射到最近的標準寬高比：

| 輸入尺寸 | 自動映射 | 寬高比 |
|---------|---------|---------|
| 1920x1080 | 5504x3072 (HD) | 16:9 |
| 1280x720 | 2752x1536 (Medium) | 16:9 |
| 1024x1024 | 4096x4096 (HD) | 1:1 |
| 1080x1920 | 3072x5504 (HD) | 9:16 |
| 自定義 | 最近標準尺寸 | 自動調整 |

## 13. 快速參考

### 完整參數列表

```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py \
  "提示詞" \
  --size 1920x1080 \
  --quality hd \
  --n 5 \
  --images img1.jpg,img2.jpg \
  --force-provider antigravity
```

### 參數說明

| 參數 | 必填 | 預設值 | 說明 |
|------|------|--------|------|
| prompt | ✅ | - | 圖片描述文字 |
| --size | ❌ | 1024x1024 | 尺寸（WIDTHxHEIGHT 格式） |
| --quality | ❌ | standard | 品質（hd, medium, standard） |
| --n | ❌ | 1 | 生成圖片數量（1-10） |
| --images | ❌ | - | 參考圖路徑（逗號分隔） |
| --force-provider | ❌ | - | 強制提供者（antigravity, nanobanana） |

## 14. 故障排除

### 問題：Antigravity 連線失敗
```bash
# 檢查 IP 和端口
ping -c 3 192.168.1.159
telnet 192.168.1.159 8045

# 強制使用 NanoBanana
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" \
  --force-provider nanobanana
```

### 問題：圖片尺寸不對
```bash
# 檢查輸入尺寸格式（必須是 WIDTHxHEIGHT）
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" \
  --size 1920x1080  # ✅ 正確
```

### 問題：品質參數錯誤
```bash
# 確保品質是 hd, medium 或 standard
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" \
  --quality hd  # ✅ 正確
```

## 15. 性能優化

### 快速預覽（使用 Standard）
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "测试" \
  --quality standard
```

### 高品質輸出（使用 HD）
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "測試" \
  --quality hd
```

### 批次生成（提高效率）
```bash
python3 .opencode/skills/universal-image-gen/scripts/generate.py "測試" \
  --n 10
```
