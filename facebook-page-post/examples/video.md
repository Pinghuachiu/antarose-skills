# 影片發文範例

## 基本影片上傳

### 簡單影片

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file /path/to/video.mp4
```

輸出:
```
📹 正在上傳影片... (大小: 125.3 MB)
✅ 影片上傳成功!
   影片 ID: 1234567890
   注意: 影片正在處理中，請稍候片刻後查看
```

### 帶標題和說明的影片

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file /path/to/product-demo.mp4 \
  --title "產品示範影片" \
  --message "📹 產品功能示範

Super Widget 3000 的強大功能
一目了然！

🛵 瞭解更多: https://example.com

#產品 #示範 #教學"
```

## 不同類型的影片

### 產品展示

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file /path/to/product-showcase.mp4 \
  --title "全新產品發布" \
  --message "🚀 Super Widget 3000

重新定義你的工作流程

✨ 主要特色:
• 超高效能
• 簡單易用
• 物超所值

立即體驗: https://example.com

#新產品 #發布 #科技"
```

### 教學影片

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file /path/to/tutorial.mp4 \
  --title "5 分鐘快速入門" \
  --message "📚 快速入門教學

5 分鐘學會使用我們的產品

📋 內容大綱:
00:00 - 產品介紹
01:00 - 基本操作
03:00 - 進階功能
04:30 - 小技巧

完整教學: https://example.com/tutorial

#教學 #入門 #新手指南"
```

### 活動紀錄

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file /path/to/event-video.mp4 \
  --title "2026 開發者大會精華" \
  --message "🎉 活動精華回顧

2026 年度開發者大會
圓滿落幕！

✨ 活動亮點:
• 500+ 參與者
• 10 位專業講者
• 精彩演講和工作坊

明年再見！

#開發者大會 #活動 #回顧"
```

### 證見分享

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file /path/to/testimonial.mp4 \
  --title "用戶真實心得" \
  --message "💬 用戶評價

聽聽他們怎麼說

「這是我用過最好的產品！」
- 張先生

「簡單易用，強力推薦！」
- 李小姐

#用戶評價 #真實見證"
```

### 幕後花絮

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file /path/to/behind-scene.mp4 \
  --title "幕後花絮" \
  --message "🎬 幕後花絮

看看我們如何打造優質產品

#幕後 #製作 #團隊"
```

### 宣傳影片

```bash
python3 .claude/skills/facebook-page-post/scripts/post.py video \
  --file /path/to/promo.mp4 \
  --title "品牌宣傳片" \
  --message "✨ 我們的故事

從 2020 年開始
我們致力於創造更好的產品

#品牌 #故事 #宣傳"
```

## 影片規格建議

### 最佳實踐

1. **檔案格式**:
   - 推薦: MP4 (H.264 編碼)
   - 支援: MOV, MP4, AVI

2. **影片長度**:
   - 建議: 1-5 分鐘
   - 最長: 240 分鐘 (4 小時)
   - 最小: 1 秒

3. **檔案大小**:
   - 最大: 1GB
   - 建議: < 500MB (較快上傳)

4. **解析度**:
   - 推薦: 1080p (1920x1080)
   - 最低: 720p (1280x720)
   - 最高: 4K (3840x2160)

5. **長寬比**:
   - 16:9 (橫向，最常見)
   - 9:16 (直向，適合手機)
   - 1:1 (正方形)
   - 4:5 (直向)

6. **編碼設定**:
   - 視訊編碼: H.264
   - 音訊編碼: AAC
   - 桔率: 30fps 或 60fps
   - 位元率: 5-10 Mbps (1080p)

### 針對不同用途的建議

| 用途 | 解析度 | 長度 | 大小 |
|------|--------|------|------|
| 產品展示 | 1080p | 1-2 分鐘 | < 200MB |
| 教學影片 | 1080p | 5-10 分鐘 | < 500MB |
| 活動紀錄 | 1080p | 3-5 分鐘 | < 300MB |
| 社群媒體 | 720p-1080p | < 1 分鐘 | < 100MB |
| 宣傳影片 | 1080p-4K | 1-3 分鐘 | < 500MB |

## 上傳最佳化

### 壓縮影片

使用 FFmpeg 壓縮大型影片:

```bash
# 壓縮為 1080p, 5Mbps
ffmpeg -i input.mp4 \
  -c:v libx264 \
  -preset medium \
  -b:v 5M \
  -maxrate 5M \
  -bufsize 10M \
  -c:a aac \
  -b:a 128k \
  output.mp4
```

### 轉換格式

```bash
# 轉換為 MP4 (H.264)
ffmpeg -i input.mov \
  -c:v libx264 \
  -c:a aac \
  output.mp4
```

### 調整解析度

```bash
# 調整為 1080p
ffmpeg -i input.mp4 \
  -vf scale=1920:1080 \
  -c:a copy \
  output_1080p.mp4

# 調整為 720p
ffmpeg -i input.mp4 \
  -vf scale=1280:720 \
  -c:a copy \
  output_720p.mp4
```

## 錯誤處理

### 檔案太大

```bash
⚠️  警告: 影片大小 1250.3 MB，超過 1GB
建議使用 Facebook 的 Resumable Upload API 上傳大型影片
是否繼續? (y/n):
```

**解決方法**:
1. 壓縮影片
2. 降低解析度
3. 減少位元率

### 上傳失敗

```bash
❌ API 請求失敗: Connection error
⚠️  請求失敗，重試中... (嘗試 1/3)
```

**解決方法**:
- 檢查網路連線
- 等待自動重試
- 稍後再試

### 處理時間長

```bash
✅ 影片上傳成功!
   影片 ID: 1234567890
   注意: 影片正在處理中，請稍候片刻後查看
```

**說明**: 大型影片需要較長處理時間，通常 5-30 分鐘

## Node.js 範例

```bash
node .claude/skills/facebook-page-post/scripts/post.js video \
  --file video.mp4 \
  --title "My Video" \
  --message "Video description"
```

## 進階技巧

### 批次上傳

```bash
#!/bin/bash
# batch_upload_videos.sh

for video in /path/to/videos/*.mp4; do
  python3 .claude/skills/facebook-page-post/scripts/post.py video \
    --file "$video" \
    --title "$(basename "$video" .mp4)" \
    --message "每日影片分享"

  sleep 60  # 避免速率限制，等待 1 分鐘
done
```

### 自動化工作流程

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path

# 監控資料夾，自動上傳新影片
WATCH_DIR = "/path/to/videos"

for video in Path(WATCH_DIR).glob("*.mp4"):
    subprocess.run([
        "python3", ".claude/skills/facebook-page-post/scripts/post.py",
        "video",
        "--file", str(video),
        "--title", video.stem,
        "--message", "自動上傳影片"
    ])

    # 移動已上傳的檔案
    video.rename(f"/path/to/uploaded/{video.name}")
```

### 定時發文

```bash
# 每週一早上 10 點發布教學影片
0 10 * * 1 /usr/bin/python3 /path/to/post.py video --file /path/to/weekly.mp4 --message "本週教學"
```

## 影片處理時間參考

| 影片大小 | 處理時間 (估計) |
|---------|----------------|
| < 100MB | 2-5 分鐘 |
| 100-500MB | 5-15 分鐘 |
| 500MB-1GB | 15-30 分鐘 |
| > 1GB | 30-60 分鐘 |

**注意**: 實際處理時間取決於 Facebook 伺服器負載

## 提示

1. **上傳時段**: 避開尖峰時段 (晚上 8-11 點)
2. **等待處理**: 上傳後需等待處理完成才能播放
3. **檔案名稱**: 使用有意義的檔案名稱
4. **縮圖**: Facebook 會自動選取縮圖，或上傳後手動選擇
5. **字幕**: 可以上傳後新增字幕檔
6. **隱私設定**: Page 預設為公開，可在上傳後調整
7. **分析**: 上傳後可查看觀看數據和互動統計
