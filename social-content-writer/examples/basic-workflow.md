# Social Content Writer - Basic Workflow

## 基礎工作流程

這個指南將帶你完成使用 social-content-writer 技能的基礎工作流程。

### 第一步：收集資料

首先，收集相關資料以了解你的主題：

```bash
python3 .claude/skills/social-content-writer/scripts/collect.py \
  --topic "AI內容創作" \
  --sources web_search,youtube \
  --max-results 15 \
  --output research_data.json
```

**輸出示例**：
```
============================================================
📊 資料收集摘要
============================================================
總共收集: 10 項
最低分數: 0.6
平均分數: 0.77

📌 頂級資料來源:
  1. [web_search] 關於 AI內容創作 的相關研究 #1
     分數: 0.85 | 這是一篇關於 AI內容創作 的詳細研究文章...
  2. [youtube] AI內容創作 - 實用指南 #1
     分數: 0.78 | 詳細介紹 AI內容創作 的實際應用...
============================================================
```

### 第二步：生成勾子

使用收集到的資料生成吸引人的勾子：

```bash
python3 .claude/skills/social-content-writer/scripts/hook-generator.py \
  --topic "AI內容創作" \
  --platform facebook \
  --num-hooks 10 \
  --output hooks.json
```

**輸出示例**：
```
============================================================
✨ 生成的勾子
============================================================

1. [STORY] (分數: 90/100)
   當我嘗試100種方法後，我發現了AI內容創作的秘密
   長度: 25 字 | 平台: facebook

2. [CURIOSITY] (分數: 88/100)
   為什麼有些內容總能病毒傳播？真相是其實有科學依據
   長度: 28 字 | 平台: facebook

3. [QUESTION] (分數: 85/100)
   你是否曾經發文後無人問津？
   長度: 13 字 | 平台: facebook
============================================================
```

### 第三步：生成內容

使用選定的勾子生成完整內容：

```bash
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "AI內容創作" \
  --hook "為什麼有些內容總能病毒傳播？AI內容創作的秘密揭曉" \
  --platform facebook \
  --framework pas \
  --tone professional \
  --output content.json
```

**輸出示例**：
```
🎯 正在生成 FACEBOOK 內容...

============================================================
✅ 內容生成成功
============================================================

📌 標題: AI內容創作 - 深度解析
📊 字數: 542
⏱️  閱讀時間: 2 分鐘
🎯 平台: facebook
📋 框架: pas

📝 內容:
------------------------------------------------------------
為什麼有些內容總能病毒傳播？AI內容創作的秘密揭曉

很多人都在面臨這個問題：不知道如何有效應對AI內容創作。這導致了效率低下、成果不佳的困境。

如果不及時解決，這個問題會越來越嚴重...
------------------------------------------------============

🏷️  標籤: #AI內容創作 #contentcreation #socialmedia #marketing

============================================================

✅ 內容已保存到: content.json
```

### 第四步：分析內容

分析生成內容的質量：

```bash
python3 .claude/skills/social-content-writer/scripts/analyze.py \
  --content content.json \
  --platform facebook \
  --output analysis.json
```

**輸出示例**：
```
============================================================
📊 內容分析報告 (FACEBOOK)
============================================================

總體評分: 78.5/100

📈 各項指標:
------------------------------------------------------------

LENGTH
  分數: 85/100  [█████████░░]
  長度: 542 字
  狀態: 理想

STRUCTURE
  分數: 70/100  [███████░░░░]
  ✓ 包含勾子
  ✓ 包含行動召喚

ENGAGEMENT
  分數: 65/100  [███████░░░░]
  問句數: 2
  情感詞: 1

HASHTAGS
  分數: 60/100  [██████░░░░░]
  標籤數: 4 (理想)

✅ 優勢:
   • 內容長度適中
   • 包含勾子
   • 包含行動召喚

⚠️  需要改進:
   • 互動性需要提升

💡 改進建議:
   1. 互動性不足，建議增加問句以引發討論
   2. 可以加入更多強力詞彙增強情感衝擊
============================================================
```

### 第五步：適配多平台

將內容適配到不同的社交平台：

```bash
python3 .claude/skills/social-content-writer/scripts/platform-adapter.py \
  --input content.json \
  --target-platforms instagram,threads,linkedin \
  --output adapted_content.json
```

**輸出示例**：
```
============================================================
🎯 平台適配結果
============================================================

✅ INSTAGRAM
   原始長度: 542 字
   適配後長度: 150 字
   在限制內: 是
   更改: 長度已調整
   預覽: 為什麼有些內容總能病毒傳播？AI內容創作的秘密揭曉...

✅ THREADS
   原始長度: 542 字
   適配後長度: 150 字
   在限制內: 是
   更改: 長度已調整, Markdown 格式已移除
   預覽: 為什麼有些內容總能病毒傳播？AI內容創作的秘密揭曉...

✅ LINKEDIN
   原始長度: 542 字
   適配後長度: 542 字
   在限制內: 是
   預覽: 為什麼有些內容總能病毒傳播？AI內容創作的秘密揭曉...

============================================================
```

### 第六步：發布內容

將內容發布到各平台：

```bash
python3 .claude/skills/social-content-writer/scripts/publish.py \
  --content content.json \
  --platforms facebook \
  --notify-discord \
  --save-db \
  --output publish_results.json
```

**輸出示例**：
```
🚀 正在發布到 FACEBOOK...
✅ FACEBOOK 發布成功

============================================================
📊 發布結果摘要
============================================================

FACEBOOK: ✅ 成功
   貼文 ID: 123456789_987654321

============================================================

✅ Discord 通知已發送
✅ 發布歷史已保存到資料庫
✅ 發布結果已保存到: publish_results.json
```

## 完整一步到位工作流

你也可以一次性完成所有步驟：

```bash
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "AI如何革命性地改變內容創作產業" \
  --platforms facebook,instagram,linkedin \
  --framework aida \
  --tone professional \
  --output final_content.json
```

然後發布：

```bash
python3 .claude/skills/social-content-writer/scripts/publish.py \
  --content final_content.json \
  --platforms facebook,instagram,linkedin \
  --notify-discord
```

## 提示和技巧

1. **使用 AI 生成更高質量的內容**：
   ```bash
   export OPENAI_API_KEY="your-api-key"
   python3 write-content.py --topic "..." --use-ai
   ```

2. **調整內容長度**：
   - Facebook: 300-800 字
   - Instagram: 100-200 字
   - LinkedIn: 800-1500 字

3. **選擇正確的框架**：
   - AIDA: 經典營銷，適合大多數內容
   - PAS: 解決問題型內容
   - Story: 故事敘述，情感連結
   - Listicle: 清單式，易讀性高

4. **優化標籤**：
   - Facebook: 3-5 個
   - Instagram: 15-25 個
   - LinkedIn: 3-5 個

## 故障排除

### 內容生成失敗

如果 AI 生成失敗，腳本會自動使用模板生成。確保：
- 檢查網絡連接
- 驗證 `OPENAI_API_KEY` 環境變量
- 確認 API 配額充足

### 發布失敗

對於需要手動發布的平台（Instagram, LinkedIn），腳本會提供發布指南：
1. 複製生成的內容
2. 打開對應的社交媒體應用
3. 粘貼內容並發布

### 平台適配問題

如果內容超過平台限制：
- 腳本會自動縮短內容
- 檢查輸出中的警告訊息
- 考慮手動調整內容
