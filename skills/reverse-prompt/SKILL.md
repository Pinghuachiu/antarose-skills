---
name: reverse-prompt
description: 分析圖片或影片並反推出可能生成它們的提示詞，適合學習 AI 生成風格和編寫更好的提示詞
metadata:
  category: analysis
  formats:
    - image
    - video
  supported_formats:
    - jpg
    - png
    - gif
    - webp
    - mp4
    - mov
    - avi
---

# Reverse Prompt 技能

分析圖片或短影片並反推出可能生成它們的提示詞，這對於理解 AI 生成圖片的風格和要素、學習如何編寫更好的提示詞、分析影片短片的創作意圖非常有用。

## 我的功能

當你提供圖片或影片時，我會：
1. 接收檔案位置（URL 或本地路徑）
2. 如果是 URL，下載到暫存檔案
3. 分析視覺內容並生成詳細的提示詞
4. 清理暫存檔案

## 使用方法

### 本地圖片
```
請分析這張圖片的提示詞: /path/to/image.jpg
```

### URL 圖片
```
幫我反推這個圖片的提示詞: https://example.com/image.png
```

### 影片分析
```
分析這個短影音可能使用的提示詞: https://example.com/video.mp4
```

## 分析維度

### 對於圖片
我會分析以下維度：

- **主題內容**
  - 人物、物體、場景
  - 動作和互動
  - 主要焦點和次要元素

- **藝術風格**
  - 寫實、卡通、油畫、水彩等
  - 線條和渲染風格
  - 美學特徵

- **構圖和視角**
  - 拍攝角度（平視、俯視、仰視）
  - 構圖規則（三分法、中心對稱）
  - 深度和空間感

- **光照和色調**
  - 光源方向和類型
  - 色溫和飽和度
  - 對比度和陰影

- **氛圍和情緒**
  - 情感基調
  - 氛圍描述詞
  - 情緒強度

- **技術細節**
  - 解析度和清晰度
  - 品質評估
  - 特殊效果

### 對於影片
額外分析：

- **動作和運動**
  - 運動軌跡
  - 動作節奏
  - 轉場方式

- **時長和節奏**
  - 短片長度
  - 剪輯節奏
  - 音樂配合

- **場景轉換**
  - 轉場方式
  - 視覺過渡
  - 場景連貫性

- **敘事結構**
  - 故事線索
  - 情節發展
  - 結局處理

## 輸出格式

我會提供以下內容：

### 1. 簡短描述
一句話總結核心內容和主要特徵

### 2. 詳細提示詞
按照常見 AI 生成工具格式組織：

```markdown
## 主題描述
[詳細描述主要內容]

## 風格指示
- 藝術風格: [風格類型]
- 渲染方式: [渲染特徵]
- 視覺風格: [視覺特徵]

## 構圖
- 角度: [拍攝角度]
- 構圖: [構圖方式]
- 焦點: [主要焦點]

## 技術參數
- 解析度: [解析度設定]
- 品質: [品質設定]
- 光照: [光照描述]

## 品質關鍵詞
[相關的品質和風格關鍵詞]
```

### 3. 分類標籤
相關的類別、風格、主題標籤，便於搜索和分類

**標籤範例**：
- 類別: `portrait`, `landscape`, `abstract`, `fantasy`
- 風格: `realistic`, `anime`, `oil-painting`, `digital-art`
- 主題: `nature`, `urban`, `character`, `sci-fi`
- 品質: `high-resolution`, `detailed`, `4K`, `8K`
- 光照: `cinematic`, `golden-hour`, `studio-light`

### 4. 建議工具
適合使用的 AI 生成工具，針對不同特點給出建議：

| 工具 | 優點 | 適合場景 |
|------|------|----------|
| Midjourney | 藝術性強、風格多樣 | 概念藝術、插畫 |
| DALL-E | 理解能力強、細節精確 | 寫實場景、具體描述 |
| Stable Diffusion | 可控性高、模型豐富 | 定製化需求、專業用途 |
| Ideogram | 文字處理優秀 | 有文字的圖片 |

## 技術實作

### 處理流程

#### 1. 接收輸入
```bash
# 驗證輸入格式
if [[ "$INPUT" =~ ^https?:// ]]; then
  # 是 URL
  echo "檢測到 URL 格式"
else
  # 是本地路徑
  echo "檢測到本地路徑"
  if [ ! -f "$INPUT" ]; then
    echo "錯誤: 檔案不存在"
    exit 1
  fi
fi
```

#### 2. 下載檔案（如果是 URL）
```bash
# 使用 curl 下載到暫存
TEMP_FILE="/tmp/opencode_reverse_prompt_${RANDOM}.${EXT}"

curl -L -o "$TEMP_FILE" "$URL"
DOWNLOAD_STATUS=$?

if [ $DOWNLOAD_STATUS -ne 0 ]; then
  echo "錯誤: 下載失敗"
  rm -f "$TEMP_FILE"
  exit 1
fi

echo "檔案已下載到 $TEMP_FILE"
```

#### 3. 分析內容
根據檔案類型選擇分析方法：

**圖片分析**：
- 使用 Read 工具讀取圖片
- 識別視覺元素和特徵
- 分析藝術風格和技術細節

**影片分析**：
- 提取關鍵幀（首幀、中間幀、結尾幀）
- 分析每幀的內容和變化
- 綜合動態資訊

#### 4. 生成提示詞
```python
# 偽代碼示例
def generate_prompt(analysis_result):
    prompt = {
        "subject": extract_subject(analysis_result),
        "style": determine_style(analysis_result),
        "composition": analyze_composition(analysis_result),
        "lighting": describe_lighting(analysis_result),
        "quality_keywords": generate_quality_tags(analysis_result)
    }
    return format_prompt(prompt)
```

#### 5. 清理暫存
```bash
# 分析完成後刪除暫存檔案
if [ -f "$TEMP_FILE" ]; then
  rm -f "$TEMP_FILE"
  echo "已清理暫存檔案"
fi
```

## 使用範例

### 範例 1: 風景照片分析

**輸入**：
```
分析這張風景照: ~/Pictures/sunset.jpg
```

**輸出**：
```
## 簡短描述
一張在金色時刻拍攝的壯觀日落風景，前景有剪影式的樹木，天空呈現橙紅色漸變。

## 詳細提示詞
主題描述: 海邊日落時刻，前景有深色剪影的松樹，海面倒映著橙紅色的天空

風格指示:
- 藝術風格: 寫實攝影
- 渲染方式: 高動態範圍攝影
- 視覺風格: 電影感光影

構圖:
- 角度: 低角度仰拍
- 構圖: 三分法構圖，剪影與天空各佔三分之二
- 焦點: 遠景

技術參數:
- 解析度: 高解析度
- 品質: 專業攝影品質
- 光照: 逆光，剪影效果

品質關鍵詞:
cinematic, golden-hour, silhouette, high-dynamic-range, professional-photography, sunset, seascape

## 分類標籤
#landscape #sunset #golden-hour #silhouette #seascape #photography #cinematic

## 建議工具
推薦工具: DALL-E, Midjourney
原因: 適合生成寫實攝影風格的風景
```

### 範例 2: 動漫風格角色

**輸入**：
```
幫我分析這個角色圖: https://example.com/anime-character.png
```

**輸出**：
```
## 簡短描述
一位年輕女性動漫角色，擁有銀色長髮和紫色眼睛，穿著科幻風格的戰鬥服，背景充滿霓虹燈元素。

## 詳細提示詞
主題描述: 年輕女性角色，銀色長髮披散在肩上，紫色閃亮的眼睛，表情溫柔堅定。穿著緊身科幻戰鬥服，有藍色光效條紋

風格指示:
- 藝術風格: 日式動漫風格
- 渲染方式: 數位繪圖，賽博龐克風格
- 視覺風格: 明亮的霓虹配色

構圖:
- 角度: 正面肖像
- 構圖: 中心對稱構圖
- 焦點: 面部特寫

技術參數:
- 解析度: 高清數位繪圖
- 品質: 精細線條和著色
- 光照: 賽博龐克霓虹光照

品質關鍵詞:
anime, cyberpunk, character-design, neon, sci-fi, detailed-illustration, digital-art, silver-hair, purple-eyes

## 分類標籤
#anime #character #cyberpunk #sci-fi #digital-art #neon #illustration

## 建議工具
推薦工具: Midjourney, Stable Diffusion (anime 模型)
原因: 對動漫風格生成有優勢
```

### 範例 3: 短影片分析

**輸入**：
```
分析這個短影片: https://example.com/food-video.mp4
```

**輸出**：
```
## 簡短描述
一個美食製作的短影片，展示從食材準備到最終成品的過程，節奏輕快，色彩鮮豔。

## 詳細提示詞
主題描述: 專業廚師製作義大利麵的過程，從切新鮮番茄、研磨香料，到麵條烹煮和最後裝盤

風格指示:
- 藝術風格: 美食攝影風格
- 渲染方式: 高品質影片拍攝
- 視覺風格: 溫暖色調，食物特寫

構圖:
- 角度: 多角度切換
- 構圖: 特寫和中景交替
- 焦點: 食物細節和烹飪動作

技術參數:
- 解析度: 4K 影片品質
- 品質: 廣告級製作品質
- 光照: 專業廚房照明

動作元素:
- 動作節奏: 輕快流暢
- 運動軌跡: 流暢的食材處理
- 轉場: 柔和的交叉淡化

品質關鍵詞:
food-photography, cooking, 4K-video, culinary, pasta, professional-lighting, vibrant-colors, smooth-motion

## 分類標籤
#food #cooking #video #4K #culinary #pasta #professional

## 建議工具
推薦工具: Runway, Pika Labs, Sora (如果可用)
原因: 專門針對影片生成的工具
```

## 權限要求

此技能需要以下權限：
- **檔案讀取**: 使用 Read 工具讀取本地圖片和影片
- **網路存取**: 下載 URL 檔案到暫存
- **檔案系統寫入**: 創建暫存檔案
- **Bash 命令執行**: 執行下載、清理等操作

## 注意事項

### 檔案限制
- **支援格式**: JPG, PNG, GIF, WebP, MP4, MOV, AVI
- **影片大小**: 建議不超過 100MB
- **圖片大小**: 建議不超過 50MB
- **解析度**: 自動適應，建議 720p 以上

### URL 限制
- 必須可公開存取
- 支援 HTTP 和 HTTPS
- 不支援需要認證的私有檔案
- 大檔案下載可能需要較長時間

### 分析精度
- 分析結果是推測性的
- 可能與原始提示詞有差異
- 藝術風格識別基於特徵匹配
- 複雜場景的分析可能不完整

### 隱私和清理
- 下載的暫存檔案會在分析後立即刪除
- 不會保存用戶提供的檔案
- 分析結果僅存儲在當前會話中

## 何時使用我

在以下情況下應該呼叫此技能：

1. **明確要求反推提示詞**
   ```
   請幫我分析這張圖片的提示詞
   ```

2. **提供視覺內容並詢問如何生成類似內容**
   ```
   我有這張圖片，想要生成類似的風格
   ```

3. **學習提示詞編寫技巧**
   ```
   這張圖片是用什麼提示詞生成的？我該怎麼寫？
   ```

4. **分析視覺內容的創作要素**
   ```
   分析這個短影片用了哪些視覺元素
   ```

5. **改進現有提示詞**
   ```
   我的提示詞是 [提示詞內容]，參考這張圖片幫我改進
   ```

## 最佳實踐

### 獲得最佳分析結果

1. **使用高品質圖片**
   - 分辨率越高分析越準確
   - 避免壓縮或模糊的圖片
   - 確保焦點清晰

2. **提供完整上下文**
   - 說明你感興趣的特定方面
   - 提及你想要達到的目標
   - 分享你已有的想法

3. **多次嘗試不同角度**
   - 同一圖片可以從不同視角分析
   - 試試不同的分析重點（風格、構圖、技術）
   - 比較多個分析結果

4. **結合其他工具**
   - 用於學習後，嘗試使用 gemini-image-preview 技能生成
   - 驗證分析結果的準確性
   - 持續改進提示詞編寫

### 避免常見問題

- ❌ 不要期望 100% 準確的原始提示詞
- ❌ 不要對極度抽象或超現實的藝術抱有過高期望
- ❌ 不要跳過驗證步驟直接使用建議的提示詞
- ✅ 提供清晰的圖片或影片
- ✅ 說明你的需求和期望
- ✅ 多次嘗試並比較結果
