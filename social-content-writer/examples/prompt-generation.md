# Image/Video Prompt Generation Guide

## 圖片/影片提示詞生成指南

social-content-writer 技能包含強大的圖片和影片 AI 生成提示詞生成功能。

## 基礎用法

### 生成圖片提示詞

```bash
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "2025年AI技術將如何改變我們的工作方式" \
  --type image \
  --platform instagram \
  --num-prompts 3
```

**輸出示例**：
```json
{
  "prompts": [
    {
      "order": 1,
      "main_prompt": "Professional visual representation of 2025年AI技術將如何改變我們的工作方式, photorealistic, professional photography, high detail, sharp focus, high quality, detailed, professional composition, perfect lighting, 8k resolution",
      "chinese_prompt": "2025年AI技術將如何改變我們的工作方式的專業視覺呈現，寫實攝影風格，高品質，細節豐富，專業構圖，完美光照",
      "style": "realistic",
      "style_description": "真實照片風格，專業攝影質量",
      "aspect_ratio": "1:1",
      "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy, watermark, text",
      "enhancement_tips": [
        "使用 寫實攝影 風格獲得最佳效果",
        "推薦寬高比: 1:1",
        "高解析度建議: 1920x1080 或更高"
      ]
    }
  ]
}
```

### 生成多風格圖片提示詞

```bash
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "文章標題和內容" \
  --type image \
  --styles realistic,illustration,3d-render,minimalist \
  --num-prompts 5 \
  --platform instagram
```

### 生成影片提示詞

```bash
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "5個提升工作效率的技巧" \
  --type video \
  --duration 30 \
  --style cinematic \
  --platform tiktok
```

**輸出示例**：
```json
{
  "video_type": "電影感",
  "duration": 30,
  "scenes": [
    {
      "order": 1,
      "duration": "3s",
      "visual_description": "Opening shot featuring 5個提升工作效率的技巧 with dramatic entrance",
      "camera_movement": "Slow zoom in",
      "audio": "Background music starts building up"
    },
    {
      "order": 2,
      "duration": "24s",
      "visual_description": "Main content showcasing key aspects of 5個提升工作效率的技巧, dynamic transitions, engaging visuals",
      "camera_movement": "Mix of tracking shots and close-ups",
      "audio": "Upbeat background music with rhythmic cuts"
    },
    {
      "order": 3,
      "duration": "3s",
      "visual_description": "Call-to-action with branding or key message",
      "camera_movement": "Pull back to reveal full scene",
      "audio": "Music crescendo then fade out"
    }
  ],
  "technical_specs": {
    "resolution": "1080p",
    "aspect_ratio": "9:16",
    "frame_rate": "30fps",
    "style": "電影感"
  },
  "overall_prompt": "A 30-second 電影感 video about 5個提升工作效率的技巧, cinematic, dramatic lighting, film grain, professional, professional quality, smooth transitions, engaging visual storytelling",
  "chinese_prompt": "一部關於5個提升工作效率的技巧的30秒電影感影片，專業品質，流暢轉場，引人入勝的視覺敘事",
  "enhancement_tips": [
    "使用 電影感 風格",
    "推薦寬高比: 9:16",
    "確保音樂與畫面節奏匹配"
  ]
}
```

## 高級功能

### 生成提示詞並自動生成圖片

```bash
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "文章內容" \
  --type image \
  --auto-generate \
  --provider nanobanana \
  --size 1920x1080 \
  --quality hd
```

這會：
1. 生成圖片提示詞
2. 自動調用 `universal-image-gen` 生成圖片
3. 返回生成的圖片路徑

### 生成並上傳到圖床

```bash
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "文章內容" \
  --type image \
  --auto-generate \
  --upload-pix2
```

這會：
1. 生成提示詞
2. 生成圖片
3. 自動上傳到 Pix2 圖床
4. 返回圖片 URL

### 使用 AI 生成高級提示詞

```bash
export OPENAI_API_KEY="your-openai-api-key"

python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content "文章內容" \
  --type image \
  --use-ai \
  --num-prompts 5
```

使用 OpenAI API 生成更精準、更詳細的提示詞。

## 支援的圖片風格

| 風格 | 名稱 | 描述 | 最佳用途 |
|------|------|------|---------|
| `realistic` | 寫實攝影 | 真實照片風格 | 專業內容、商業用途 |
| `illustration` | 數位插畫 | 現代插畫風格 | 休閒內容、教育用途 |
| `3d-render` | 3D 渲染 | 3D 軟件渲染 | 科技內容、創意設計 |
| `minimalist` | 極簡主義 | 簡潔乾淨設計 | 專業平台、LinkedIn |
| `cyberpunk` | 赛博朋克 | 科幻未來風格 | 科技趨勢、未來主題 |
| `watercolor` | 水彩畫 | 藝術水彩風格 | 創意內容、柔和風格 |
| `pop-art` | 波普藝術 | 大眾藝術風格 | 娛樂內容、年輕受眾 |
| `isometric` | 等距視圖 | 2.5D 等距視角 | 技術圖解、結構化內容 |

## 支援的影片風格

| 風格 | 描述 | 最佳用途 |
|------|------|---------|
| `cinematic` | 電影感，戲劇性光效 | 品牌宣傳、故事敘述 |
| `animation` | 2D 或 3D 動畫 | 教育內容、輕鬆主題 |
| `documentary` | 紀錄片風格 | 專業內容、真實故事 |
| `commercial` | 商業廣告風格 | 產品推廣、品牌建設 |

## 平台特色適配

### Instagram

- **圖片**: 1:1 或 4:5，色彩鮮明，視覺衝擊
- **影片**: 9:16 或 1:1，15-60 秒，快節奏

```bash
python3 prompt-generator.py \
  --content "內容" \
  --type image \
  --platform instagram \
  --styles realistic,3d-render
```

### Facebook

- **圖片**: 16:9 或 1:1，清晰易讀
- **影片**: 16:9，30秒-3分鐘，敘事性

```bash
python3 prompt-generator.py \
  --content "內容" \
  --type image \
  --platform facebook \
  --styles realistic,illustration
```

### LinkedIn

- **圖片**: 16:9 或 4:5，專業、商業風
- **影片**: 16:9，30秒-2分鐘，專業感

```bash
python3 prompt-generator.py \
  --content "內容" \
  --type image \
  --platform linkedin \
  --styles minimalist,realistic
```

## 從 JSON 文件生成

如果你已經有 `content.json`：

```bash
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content content.json \
  --type image \
  --num-prompts 3
```

## 提示詞品質評估

生成的提示詞會自動評估以下維度：

1. **清晰度** (25%): 主體描述是否清晰明確
2. **具體性** (25%): 細節描述是否具體充分
3. **風格一致性** (20%): 風格定義是否一致
4. **技術準確性** (15%): 技術參數是否正確
5. **平台匹配度** (15%): 是否符合平台特色

最低分數閾值：0.7

## 優化建議系統

如果提示詞分數低於閾值，系統會提供優化建議：

```json
{
  "enhancement_tips": [
    "建議：增加主體的具體描述，明確人物、物體或場景",
    "建議：添加更多細節，如顏色、材質、光照、角度等",
    "建議：使用更具體的藝術風格"
  ]
}
```

## 常見問題

### Q: 如何選擇正確的風格？

A: 考慮內容類型和受眾：
- 專業內容 → `realistic`, `minimalist`
- 科技內容 → `3d-render`, `cyberpunk`
- 創意內容 → `illustration`, `watercolor`
- 教育內容 → `isometric`, `minimalist`

### Q: 圖片生成失敗怎麼辦？

A: 腳本會嘗試備選服務：
1. 檢查 API keys 配置
2. 確認網絡連接
3. 嘗試使用 `--provider nanobanana`

### Q: 如何生成縮圖？

A: 使用高對比度、吸引眼球的風格：

```bash
python3 prompt-generator.py \
  --content "內容" \
  --type image \
  --styles pop-art,cyberpunk \
  --platform youtube
```

### Q: 影片提示詞可以直接生成影片嗎？

A: 目前不支持直接生成影片。提示詞可以用於：
- Runway (runwayml.com)
- Pika (pika.art)
- Sora (coming soon)

將生成的 `overall_prompt` 粘貼到這些平台即可。
