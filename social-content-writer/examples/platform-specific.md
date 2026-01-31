# Platform-Specific Examples

## 平台特定範例

這個指南提供各個平台的具體使用範例。

## Facebook

### 基礎範例

```bash
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "2025年社交媒體營銷趨勢" \
  --platform facebook \
  --framework aida \
  --tone professional
```

**Facebook 特色**：
- 支援長篇內容（最多 60,000 字）
- 建議長度：300-800 字
- 標籤：3-5 個
- 支援 Markdown 格式
- 可包含圖片和連結

### Facebook 最佳實踐

```bash
# 生成帶圖片的 Facebook 貼文
python3 write-content.py \
  --topic "產品發布" \
  --platform facebook \
  --framework pas \
  --generate-prompts

# 分析 Facebook 內容
python3 analyze.py \
  --content fb_content.json \
  --platform facebook \
  --detailed
```

**Facebook 發布**：
```bash
python3 publish.py \
  --content fb_content.json \
  --platforms facebook \
  --notify-discord
```

## Instagram

### 基礎範例

```bash
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "旅遊攝影技巧" \
  --platform instagram \
  --framework story \
  --tone casual
```

**Instagram 特色**：
- 限制：2,200 字
- 建議長度：138-150 字（首句最重要）
- 標籤：15-30 個
- 視覺優先平台
- 不支援 Markdown

### Instagram 最佳實踐

```bash
# 生成 Instagram 圖片提示詞
python3 prompt-generator.py \
  --content "旅遊攝影技巧" \
  --type image \
  --platform instagram \
  --styles realistic,3d-render \
  --num-prompts 5

# 自動生成圖片
python3 prompt-generator.py \
  --content "旅遊攝影技巧" \
  --type image \
  --auto-generate \
  --upload-pix2
```

**Instagram 發布**：
```bash
# Instagram 需要手動發布
python3 publish.py \
  --content ig_content.json \
  --platforms instagram
```

腳本會提供發布指南：
1. 打開 Instagram 應用
2. 上傳生成的圖片
3. 複製生成的內容
4. 粘貼到說明欄位
5. 點擊分享

## LinkedIn

### 基礎範例

```bash
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "企業數位轉型策略" \
  --platform linkedin \
  --framework listicle \
  --tone professional
```

**LinkedIn 特色**：
- 限制：3,000 字
- 建議長度：1,000-1,500 字
- 標籤：3-5 個
- 專業內容平台
- 限制表情符號使用

### LinkedIn 最佳實踐

```bash
# 生成專業 LinkedIn 文章
python3 write-content.py \
  --topic "行業洞察" \
  --platform linkedin \
  --framework pas \
  --tone authoritative \
  --value-type educational

# 分析 LinkedIn 內容
python3 analyze.py \
  --content linkedin_content.json \
  --platform linkedin
```

**LinkedIn 內容結構建議**：
1. **強力開頭**：抓住注意力的統計數據或問題
2. **個人故事**：增加可信度和連結
3. **實用洞察**：提供可執行的建議
4. **行動召喚**：鼓勵討論

## Threads

### 基礎範例

```bash
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "今日科技新聞" \
  --platform threads \
  --framework story \
  --tone casual
```

**Threads 特色**：
- 限制：500 字
- 建議長度：100-200 字
- 標籤：3-5 個
- 對話式平台
- 快速互動

### Threads 最佳實踐

```bash
# 生成 Threads 短貼文
python3 write-content.py \
  --topic "快速分享" \
  --platform threads \
  --tone friendly \
  --hashtags 3

# 適配長內容到 Threads
python3 platform-adapter.py \
  --input long_content.json \
  --target-platforms threads \
  --adjust-length
```

## 多平台同步

### 一次生成，多平台發布

```bash
# Step 1: 生成多平台內容
python3 write-content.py \
  --topic "AI技術革命" \
  --platforms facebook,instagram,linkedin,threads \
  --framework aida \
  --tone professional \
  --output multi_platform.json
```

這會生成包含所有平台的 JSON 文件。

```bash
# Step 2: 發布到所有平台
python3 publish.py \
  --content multi_platform.json \
  --platforms facebook,instagram,linkedin,threads \
  --notify-discord \
  --save-db
```

### 平台間內容調整

```bash
# 自動適配內容到不同平台
python3 platform-adapter.py \
  --input facebook_content.json \
  --target-platforms instagram,threads,linkedin \
  --output adapted.json
```

## 平台特定提示

### Facebook 提示

```python
# 最佳發布時間
工作日 9-10 AM 或 2-4 PM

# 內容建議
- 使用問句開頭
- 包含清晰的 CTA
- 添加相關圖片
- 分段提升可讀性
```

### Instagram 提示

```python
# 首句最重要（會被截斷）
# 使用 20-30 個標籤
# 視覺內容是關鍵
# 使用 Stories 增加互動

# 標籤位置
將標籤放在最後或第一條評論
```

### LinkedIn 提示

```python
# 提供專業洞察
# 使用個人故事
# 避免過度推銷
# 最佳長度：1,000-1,500 字

# 排版建議
- 使用空行分隔段落
- 使用項目符號
- 保持專業語調
```

### Threads 提示

```python
# 保持簡短有力
# 第一句就要抓住注意力
# 使用對話式語調
# 快速回覆評論

# 互動技巧
- 回覆所有評論
- 使用引文功能
- 參與話題討論
```

## 平台規則快速參考

| 平台 | 字數限制 | 最佳長度 | 標籤數 | 格式 | 發布方式 |
|------|---------|---------|--------|------|---------|
| Facebook | 60,000 | 300-800 | 3-5 | Markdown | 自動 |
| Instagram | 2,200 | 138-150 | 15-30 | 純文字 | 手動 |
| Threads | 500 | 100-200 | 3-5 | 純文字 | 手動 |
| LinkedIn | 3,000 | 1,000-1,500 | 3-5 | Markdown | 手動 |

## 平台適配策略

### 長內容適配

從 Facebook 適配到 Instagram/Threads：

```bash
python3 platform-adapter.py \
  --input facebook_post.json \
  --target-platforms instagram,threads \
  --adjust-length
```

腳本會：
1. 提取核心訊息
2. 縮短內容到平台限制
3. 移除 Markdown 格式
4. 優化標籤數量

### 標籤優化

不同平台使用不同的標籤策略：

```bash
python3 platform-adapter.py \
  --input content.json \
  --target-platforms facebook,instagram \
  --optimize-hashtags
```

- **Facebook**: 3-5 個，聚焦主題
- **Instagram**: 15-30 個，包含流行標籤
- **LinkedIn**: 3-5 個，專業相關
- **Threads**: 3-5 個，話題驅動

## 實際工作流範例

### 產品發布活動

```bash
# 1. 為所有平台生成內容
python3 write-content.py \
  --topic "新產品發布：革命性的智能手錶" \
  --platforms facebook,instagram,linkedin \
  --framework pas \
  --tone professional \
  --output product_launch.json

# 2. 生成產品圖片
python3 prompt-generator.py \
  --content product_launch.json \
  --type image \
  --styles realistic,3d-render \
  --num-prompts 5 \
  --auto-generate

# 3. 生成宣傳影片提示詞
python3 prompt-generator.py \
  --content product_launch.json \
  --type video \
  --duration 60 \
  --style cinematic \
  --output video_prompts.json

# 4. 發布到所有平台
python3 publish.py \
  --content product_launch.json \
  --platforms facebook,instagram,linkedin \
  --notify-discord
```

### 每日內容排程

```bash
#!/bin/bash
# daily_content.sh

# 主題列表
topics=("營銷技巧" "效率提升" "科技趨勢" "創意靈感")

for topic in "${topics[@]}"; do
  # 生成 Facebook 內容
  python3 write-content.py \
    --topic "$topic" \
    --platform facebook \
    --framework listicle \
    --output "${topic// /_}_fb.json"

  # 生成 Instagram 內容
  python3 write-content.py \
    --topic "$topic" \
    --platform instagram \
    --framework story \
    --output "${topic// /_}_ig.json"
done
```

## 故障排除

### Instagram 手動發布

對於需要手動發布的平台，腳本會提供詳細指南：

```
📱 Instagram 發布指南:
   1. 打開 Instagram 應用
   2. 點擊 + 創建新貼文
   3. 上傳圖片（如已生成）
   4. 複製以下內容:
      [內容文字]
   5. 粘貼到說明欄位
   6. 點擊分享
```

### 內容過長處理

如果內容超過平台限制：

```bash
python3 platform-adapter.py \
  --input long_content.json \
  --target-platforms instagram \
  --adjust-length
```

腳本會：
- 智能截斷
- 保留核心訊息
- 添加省略標記
- 警告用戶內容被縮短
