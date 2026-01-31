# 圖片發文範例

## 單張圖片

### 基本圖片上傳

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py photo \
  --file /path/to/photo.jpg
```

輸出:
```
✅ 圖片上傳成功!
   圖片 ID: 1234567890
   貼文連結: https://www.facebook.com/987654321
```

### 帶說明的圖片

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py photo \
  --file /path/to/product.jpg \
  --message "📱 新產品登場！

Super Widget 3000
現在開始預購！

🛒 購買: https://example.com

#新產品 #科技"
```

### 風景照片

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py photo \
  --file /path/to/landscape.jpg \
  --message "🌄 美麗的日出

拍攝地點: 台灣陽明山
時間: 清晨 5 點

#風景 #攝影 #台灣"
```

### 產品展示

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py photo \
  --file /path/to/product1.jpg \
  --message "✨ 產品特寫

我們的新產品採用頂級材質打造
細節處理完美無瑕

#產品 #設計 #品質"
```

### 活動照片

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py photo \
  --file /path/to/event.jpg \
  --message "🎉 活動精彩瞬間

2026 開發者大會圓滿落幕
感謝所有參與的朋友！

#活動 #開發者大會 #回顧"
```

## 多張圖片（相簿）

### 基本相簿上傳

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py photos \
  --files photo1.jpg photo2.jpg photo3.jpg \
  --message "產品展示相簿"
```

輸出:
```
📁 正在建立相簿並上傳 3 張圖片...
   相簿 ID: 1234567890
   圖片 1/3 上傳完成 (ID: 1111111111)
   圖片 2/3 上傳完成 (ID: 2222222222)
   圖片 3/3 上傳完成 (ID: 3333333333)
✅ 所有圖片上傳成功!
   相簿連結: https://www.facebook.com/media/set/?set=1234567890
```

### 產品系列展示

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py photos \
  --files product1.jpg product2.jpg product3.jpg product4.jpg \
  --message "🎨 2026 春季產品系列

全新設計，多款選擇
滿足你的不同需求

#新品上市 #春季系列 #選購"
```

### 活動記錄相簿

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py photos \
  --files event1.jpg event2.jpg event3.jpg event4.jpg event5.jpg \
  --message "📸 活動精彩回顧

2026 年度開發者大會
現場熱烈非凡

✨ 重點:
• 超過 500 位參與者
• 10 位專業講者
• 精彩演講和工作坊

#活動 #開發者大會 #回顧"
```

### 旅遊相簿

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py photos \
  --files travel1.jpg travel2.jpg travel3.jpg \
  --message "🏖️ 旅遊日記

宜蘭三日遊

Day 1:Traditional Market
Day 2:National Center for Traditional Arts
Day 3:Turtle Island

#旅遊 #宜蘭 #美食"
```

### 教學步驟

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py photos \
  --files step1.jpg step2.jpg step3.jpg step4.jpg \
  --message "📚 使用教學

如何使用我們的產品

Step 1: 開啟包裝
Step 2: 連接電源
Step 3: 下載 App
Step 4: 開始使用

詳細說明: https://example.com/guide

#教學 #使用說明 #新手指南"
```

## 圖片建議

### 最佳實踐

1. **圖片尺寸**:
   - 建議: 1200 x 630 pixels (1.91:1)
   - 最小: 470 x 246 pixels
   - 最大: 4MB

2. **格式**:
   - 推薦: JPG (壓縮後品質佳)
   - 支援: PNG, JPG, BMP, TIFF

3. **內容**:
   - 高品質照片
   - 清晰的主題
   - 適度的文字說明
   - 吸引人的標題

4. **說明文字**:
   - 簡潔有力
   - 包含關鍵資訊
   - 加入相關 Hashtag
   - 使用 emoji 增加視覺效果

## 錯誤處理

### 檔案不存在

```bash
❌ 錯誤: 檔案不存在 - /path/to/photo.jpg
```

**解決方法**: 檢查檔案路徑是否正確

### 檔案太大

```bash
⚠️  警告: 圖片大小超過 4MB
```

**解決方法**: 壓縮圖片後再上傳

### Token 過期

```bash
⚠️  錯誤: Access Token 已過期或無效
```

**解決方法**: 使用 token-helper.py 檢查 Token 狀態並更新

## Node.js 範例

### 單張圖片

```bash
node .claude/skills/facebook-page-post/scripts/post.js photo \
  --file photo.jpg \
  --message "Beautiful photo"
```

### 多張圖片

```bash
node .claude/skills/facebook-page-post/scripts/post.js photos \
  --files photo1.jpg photo2.jpg photo3.jpg \
  --message "Photo album"
```

## 進階技巧

### 批次上傳

使用 shell 腳本批次上傳多個圖片:

```bash
#!/bin/bash
# batch_upload.sh

for photo in /path/to/photos/*.jpg; do
  python3 .claude/skills/facebook-page-post/scripts/post.py photo \
    --file "$photo" \
    --message "每日照片分享"

  sleep 10  # 避免速率限制
done
```

### 定時發文

使用 cron 定時發文:

```bash
# 每天早上 9 點發文
0 9 * * * /usr/bin/python3 /path/to/post.py photo --file /path/to/morning.jpg --message "早安！"
```

### 自動化工作流程

```python
#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

# 監控資料夾，自動上傳新圖片
WATCH_DIR = "/path/to/watch"

for file in Path(WATCH_DIR).glob("*.jpg"):
    subprocess.run([
        "python3", ".claude/skills/facebook-page-post/scripts/post.py",
        "photo",
        "--file", str(file),
        "--message", "自動上傳"
    ])
    # 移動已上傳的檔案
    file.rename(f"/path/to/uploaded/{file.name}")
```
