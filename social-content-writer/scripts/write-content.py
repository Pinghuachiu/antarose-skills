#!/usr/bin/env python3
"""
Social Content Writer - Value-Driven Content Generation Script
價值驅動的內容生成（小白友善版）
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# 價值類型定義（重新設計）
VALUE_TYPES = {
    "save_time": {
        "name": "節省時間",
        "description": "幫讀者省下寶貴時間",
        "reader_benefit": "你每天可以多出X小時做更重要的事",
        "keywords": ["省時間", "效率", "快", "立即", "自動化"]
    },
    "save_money": {
        "name": "節省金錢",
        "description": "幫讀者省錢或賺錢",
        "reader_benefit": "不用花錢聘助理，或增加收入",
        "keywords": ["免費", "省錢", "賺錢", "成本", "便宜"]
    },
    "reduce_effort": {
        "name": "減少努力",
        "description": "讓複雜的事變簡單",
        "reader_benefit": "從繁瑣中解放，做你喜歡的事",
        "keywords": ["簡單", "輕鬆", "不用", "自動", "一步搞定"]
    },
    "avoid_mistakes": {
        "name": "避免錯誤",
        "description": "幫讀者不犯錯",
        "reader_benefit": "再也不會遺漏或搞砸重要的事",
        "keywords": ["不忘記", "不遺漏", "零錯誤", "提醒", "記住"]
    },
    "learn_skill": {
        "name": "學習技能",
        "description": "教讀者新技能",
        "reader_benefit": "掌握未來必備的AI能力",
        "keywords": ["學會", "掌握", "技能", "教學", "教程"]
    }
}


class ValueDrivenContentGenerator:
    """價值驅動的內容生成器"""

    def __init__(self, platform: str = "facebook"):
        self.platform = platform
        self.platform_rules = self._get_platform_rules()

    def _get_platform_rules(self) -> Dict:
        """獲取平台規則"""
        rules = {
            "facebook": {
                "max_length": 60_000,
                "optimal_length": 800,
                "max_hashtags": 5,
                "optimal_hashtags": 3,
                "format": "markdown",
                "tone": "friendly"
            },
            "instagram": {
                "max_length": 2_200,
                "optimal_length": 150,
                "max_hashtags": 30,
                "optimal_hashtags": 20,
                "format": "plain",
                "tone": "casual"
            },
            "threads": {
                "max_length": 500,
                "optimal_length": 150,
                "max_hashtags": 5,
                "optimal_hashtags": 3,
                "format": "plain",
                "tone": "conversational"
            },
            "linkedin": {
                "max_length": 3_000,
                "optimal_length": 1_200,
                "max_hashtags": 5,
                "optimal_hashtags": 3,
                "format": "markdown",
                "tone": "professional"
            }
        }
        return rules.get(self.platform, rules["facebook"])

    def identify_value_proposition(self, topic: str, research_data: Dict = None) -> Dict:
        """識別核心價值主張"""
        print("\n💎 識別核心價值...")

        # 如果有研究資料，分析關鍵詞
        value_scores = {}

        if research_data:
            all_text = " ".join([item.get("summary", "") for item in research_data.get("data", [])])

            for value_type, config in VALUE_TYPES.items():
                keywords = config["keywords"]
                score = sum(all_text.lower().count(kw.lower()) for kw in keywords)
                value_scores[value_type] = score

        # 按分數排序
        sorted_values = sorted(value_scores.items(), key=lambda x: x[1], reverse=True)

        # 選擇最主要的價值
        if sorted_values and sorted_values[0][1] > 0:
            primary_value = sorted_values[0][0]
        else:
            # 根據主題推斷
            if any(kw in topic.lower() for kww in ["助理", "幫手", "自動", "工具"]):
                primary_value = "save_time"
            elif any(kw in topic.lower() for kw in ["免費", "開源", "省錢"]):
                primary_value = "save_money"
            else:
                primary_value = "save_time"

        value_info = VALUE_TYPES[primary_value]

        print(f"   核心價值: {value_info['name']}")
        print(f"   讀者受益: {value_info['reader_benefit']}")

        return {
            "type": primary_value,
            "name": value_info["name"],
            "description": value_info["description"],
            "reader_benefit": value_info["reader_benefit"]
        }

    def generate_with_ai(self, topic: str, hook: str, value_proposition: Dict,
                        research_data: Dict = None, word_count: int = 800) -> Dict:
        """使用 AI 生成價值驅動的內容"""
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            print("⚠️  未設置 OPENAI_API_KEY，使用模板生成")
            return self.generate_with_template(topic, hook, value_proposition, research_data, word_count)

        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)

            # 構建研究背景
            research_context = ""
            if research_data and research_data.get("key_insights"):
                insights = research_data["key_insights"][:3]
                research_context = "\n".join([f"- {insight}" for insight in insights])

            prompt = f"""請基於以下資訊，生成一篇吸引人的社交媒體內容：

【主題】{topic}

【勾子】{hook}

【核心價值】{value_proposition['name']}
- 說明：{value_proposition['description']}
- 讀者受益：{value_proposition['reader_benefit']}

【目標平台】{self.platform}
- 字數：約 {word_count} 字
- 最佳長度：{self.platform_rules['optimal_length']} 字
- 標籤數量：{self.platform_rules['optimal_hashtags']} 個
- 語調：{self.platform_rules['tone']}

【研究背景】
{research_context}

【重要要求】
1. **小白友善**：
   - 避免技術術語（如「API」、「Agent」、「LLM」）
   - 用生活化的比喻和例子
   - 解釋複雜概念時用「想像一下...」

2. **強調價值**：
   - 開頭就說明讀者能得到什麼好處
   - 用「以前→現在」對比展示改變
   - 給出具體數字或案例

3. **結構清晰**：
   - 勾子（吸引注意）
   - 價值說明（為什麼重要）
   - 實際案例（怎麼運作）
   - 行動召喚（下一步）

4. **語言風格**：
   - 口語化，像朋友聊天
   - 用短句，避免長難句
   - 加入反問句增加互動

5. **結尾行動召喚**：
   - 明確告訴讀者該做什麼
   - 製造緊迫感或好處

返回 JSON 格式：
{{
  "title": "吸引人的標題",
  "content": "完整內容（使用 {self.platform_rules['tone']} 語氣，小白友善）",
  "summary": "一句話總結價值",
  "key_takeaways": ["要點1", "要點2", "要點3"],
  "cta": "強烈的行動召喚",
  "hashtags": ["標籤1", "標籤2", "標籤3"]
}}"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是專業的社交媒體內容作家，擅長創作小白友善、高互動率的內容。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=3000
            )

            # 解析 AI 回應
            content_text = response.choices[0].message.content

            # 嘗試提取 JSON
            import re
            json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # 如果找不到 JSON，使用文本
                result = {
                    "title": f"{topic} - 小白必看",
                    "content": content_text,
                    "summary": f"關於 {topic} 的實用指南",
                    "key_takeaways": [],
                    "cta": "分享你的看法！",
                    "hashtags": self._generate_hashtags(topic, 3)
                }

            # 添加元數據
            result["metadata"] = {
                "value_type": value_proposition["type"],
                "value_name": value_proposition["name"],
                "word_count": len(result.get("content", "")),
                "reading_time": f"{len(result.get('content', '')) // 200} 分鐘",
                "platform": self.platform,
                "tone": self.platform_rules["tone"]
            }

            return result

        except Exception as e:
            print(f"⚠️  AI 生成失敗: {e}")
            print("使用模板生成作為備選方案")
            return self.generate_with_template(topic, hook, value_proposition, research_data, word_count)

    def generate_with_template(self, topic: str, hook: str, value_proposition: Dict,
                             research_data: Dict = None, word_count: int = 800) -> Dict:
        """使用模板生成價值驅動的內容（小白友善版）"""

        value_type = value_proposition["type"]
        value_name = value_proposition["name"]
        reader_benefit = value_proposition["reader_benefit"]

        # 根據價值類型選擇模板
        if value_type == "save_time":
            content = self._generate_save_time_content(topic, hook, reader_benefit)
        elif value_type == "save_money":
            content = self._generate_save_money_content(topic, hook, reader_benefit)
        elif value_type == "reduce_effort":
            content = self._generate_reduce_effort_content(topic, hook, reader_benefit)
        elif value_type == "avoid_mistakes":
            content = self._generate_avoid_mistakes_content(topic, hook, reader_benefit)
        else:
            content = self._generate_learn_skill_content(topic, hook, reader_benefit)

        # 確保不超過平台限制
        max_length = self.platform_rules["max_length"]
        if len(content) > max_length:
            content = content[:max_length-100] + "...（內容過長已截斷，完整版請看留言）"

        result = {
            "title": f"{topic} - {value_name}指南",
            "content": content,
            "summary": f"{value_name}：{reader_benefit}",
            "key_takeaways": [
                f"✅ {value_name}",
                "✅ 簡單易用",
                "✅ 立即開始"
            ],
            "cta": f"想了解更多{topic}？留言告訴我！",
            "hashtags": self._generate_hashtags(topic, self.platform_rules["optimal_hashtags"]),
            "metadata": {
                "value_type": value_type,
                "value_name": value_name,
                "word_count": len(content),
                "reading_time": f"{len(content) // 200} 分鐘",
                "platform": self.platform,
                "tone": self.platform_rules["tone"],
                "generated_by": "template"
            }
        }

        return result

    def _generate_save_time_content(self, topic: str, hook: str, benefit: str) -> str:
        """生成節省時間類型的內容"""
        return f"""{hook}

想像一下：每天多出 2 小時，你會做什麼？

- 追完那部追了很久的劇？
- 陪家人孩子玩？
- 還是... 其實什麼都不做，純粹休息？

我發現了一個工具，真的幫我省下大量時間：**{topic}**

## 以前 vs 現在

**以前**：
- 每天花 2 小時回郵件
- 手動排行程，還會忘記
- 開會時忙著記錄跟不上
- 瑣事堆積，越做越累

**現在**：
- 郵件它幫我整理、分類
- 行程自動安排，還會提前提醒
- 開會它自動記錄並重點整理
- 我只要做重要的事

## 它是什麼？

簡單說，{topic} 就像你的私人助理。

但你不用付它薪水（免費的！），它 24 小時上班不會累，透過 WhatsApp 或 Telegram 就能對話。

## 真實案例

早上起床，手機響了：

> 「早安！今天 3 個會議已經排好了。客戶的郵件我幫你起草好了草稿，你看一下要修改嗎？」

你還在刷牙，它已經幫你處理完一半的工作。

## 為什麼要試試？

如果你符合以下任一項，建議試試：

✅ 每天花 >1 小時處理重複性事務
✅ 有多個平台需要切換（Gmail、日曆、Slack...）
✅ 常常忘記重要事情
✅ 想體驗「AI 未來」長什麼樣

## 怎麼開始？

簡單 3 步：

1. 準備一台電腦（Mac、Windows 都行）
2. 看 YouTube 教學（搜尋「Moltbot 教學」）
3. 30 分鐘內搞定

**你的時間很寶貴，別浪費在瑣事上。**

讓 AI 幫你處理瑣事，你做真正重要的事。

---

👇 試過嗎？分享你的經驗！
沒試過？有問題？留言問我！

#效率工具 #AI助理 #省時間 #生活技巧"""

    def _generate_save_money_content(self, topic: str, hook: str, benefit: str) -> str:
        """生成節省金錢類型的內容"""
        return f"""{hook**

**聘請一個助理要多少錢？**

- 全職助理：月薪 $3,000 起
- 兼職助理：月薪 $1,500 起
- 行政人員：月薪 $2,000 起

一年下來... **至少 $18,000 - $36,000**

但如果我告訴你，有一個助理：
- ✅ 免費
- ✅ 24/7 全天候
- ✅ 不會累
- ✅ 越用越聰明

你會想要嗎？

## 它就是：{topic}

{topic} 是一個開源 AI 助理，可以幫你：

📧 **處理郵件** - 自動分類、回覆、歸檔
📅 **管理行程** - 排會議、提醒、衝突檢查
📝 **會議紀錄** - 自動記錄並整理重點
🔔 **主動提醒** - 該出門、該準備、不遺漏

## 真實案例

有個朋友用 {topic} 幫他：

- 自動回覆客戶信件
- 生成發票和報表
- 追蹬項目進度

結果：**一個月省了 $5,000** 行政成本。

## 為什麼免費？

因為它是開源專案！

- 不用付月費
- 不用付年費
- 只需要付 AI 模型費用（每月可能 $10-30）

## 適合誰？

✅ 自由工作者 - 一人公司，需要幫手
✅ 小團隊 - 免費的 AI 員工
✅ 學生 - 幫你整理課程、作業
✅ 主婦/家庭主夫 - 管理家庭事務

## 怎麼開始？

1. 打開 YouTube 搜尋「Moltbot 教學」
2. 找一個小白友善的教學影片
3. 跟著做，30 分鐘內完成

**不用花錢聘助理，{topic} 幫你省回來。**

---

💰 你覺得值嗎？還是你已經在用了？
留言告訴我你的使用心得！

#省錢 #AI助理 #免費工具 #效率 #開源"""

    def _generate_reduce_effort_content(self, topic: str, hook: str, benefit: str) -> str:
        """生成減少努力類型的內容"""
        return f"""{hook}

**你覺得哪些事最煩？**

- 整理會議紀錄？
- 回覆重複的郵件？
- 排複雜的行程？
- 追蹤各種待辦事項？

我以前也覺得這些超煩。

直到我用了 **{topic}**。

## 它是什麼？

{topic} 是一個 AI 助理，你可以透過 WhatsApp 或 Telegram 跟它對話。

你只要說「幫我做 X」，它就幫你做。

## 真實案例

### 案例 1：自動整理會議紀錄

**以前**：
開會時拼命打字，還是漏掉重點
會後花 30 分鐘整理紀錄

**現在**：
開會時它自動錄音、轉文字
會後立刻給我整理好的重點
還自動發到 Slack 給團隊

### 案例 2：主動管理行程

**以前**：
每天早上花 15 分鐘確認今天的行程
怕忘記，設了 5 個鬧鐘

**現在**：
每天早上發送今日簡報
會議前 15 分鐘提醒我該出門
根據交通狀況調整提醒時間

### 案例 3：一鍵完成複雜任務

**以前**：
要打開 5 個網站、登入 3 個帳號
來回切換，至少 20 分鐘

**現在**：
在 WhatsApp 說一句「幫我處理」
它 5 分鐘搞定

## 為什麼這麼神奇？

因為它：
- **有記憶** - 記得你說過的每句話
- **會主動** - 不用你叫，它自己提醒你
- **能執行** - 不只是聊天，是真的「做事」
- **可擴展** - 社群不斷開發新功能

## 適合誰嗎？

如果你：
✅ 想減少瑣事
✅ 想提高效率
✅ 不想學複雜工具
✅ 喜歡用 chat 聊天的方式操作

那 {topic} 可能適合你。

## 怎麼開始？

超簡單：

1. 準備一台電腦
2. 看 YouTube 教學（搜尋「{topic} 小白」）
3. 跟著做，30 分鐘

**從繁瑣中解放，做你喜歡的事。**

---

😴 你最想自動化什麼事？
留言告訴我，我看看 {topic} 能不能幫你做到！

#簡單生活 #減少壓力 #自動化 #AI助理 #效率神器"""

    def _generate_avoid_mistakes_content(self, topic: str, hook: str, benefit: str) -> str:
        """生成避免錯誤類型的內容"""
        return f"""{hook}

**你有過這些經驗嗎？**

❌ 忘記重要會議，遲到 15 分鐘
❌ 回覆郵件漏了附件，被客戶罵
❌ 記錯會議時間，雙方都白等
❌ 忘記繳費，被罰錢

我以前也常犯這些錯。

直到我用了 **{topic}**。

## 它是什麼？

{topic} 是一個有「長期記憶」的 AI 助理。

它就像你的大腦外掛，幫你記住所有事。

## 真實案例

### 案例 1：再也不会忘記會議

**以前**：
- 記在手機，還是忘記
- 設鬧鐘，時間到了還沒看到
- 客戶等了我 20 分鐘...

**現在**：
{topic} 會提前 15 分鐘提醒我
根據交通狀況建議我該出門了
還會幫我準備會議資料

### 案例 2：不會漏掉重要郵件

**以前**：
郵件太多，看不到重要信
客戶等了 3 天都沒回覆
結果... 客戶跑了

**現在**：
{topic} 自動分類郵件
重要的標紅提醒
還幫我草擬回覆

### 案例 3：正確執行任務

有人的 {topic} 甚至幫他：
- 自動跟保險公司溝通
- 處理理賠申請
- 還幫他爭取到更多賠償

## 為什麼它這麼強？

因為它：

🧠 **有記憶** - 記得你說過的話
⏰ **會提醒** - 主動告訴你該做什麼
✅ **不犯錯** - 精確執行你的指令
🔄 **可擴展** - 可以連接你用的工具

## 有什麼風險嗎？

嗯，有幾個要注意：

⚠️ **安全問題** - 別暴露在公網
⚠️ **AI 成本** - 用太兇可能費用品嚇人
⚠️ **太聰明** - 可能自作主張（需要設定界限）

## 怎麼安全使用？

1. 在本地電腦跑（不要上雲）
2. 定期審核它做的事
3. 設定好權限和界限

## 適合誰？

✅ 常常忘記事情的人
✅ 處理重要任務的人
✅ 想要零失誤的人
✅ 想要專注不被打擾的人

## 怎麼開始？

1. YouTube 搜尋「{topic} 安全教學」
2. 先在測試環境試試
3. 確認沒問題再正式使用

**再也不會犯這些錯，因為有 AI 幫你記住。**

---

😅 你犯過哪些尷尬錯誤？
留言分享（我會保守秘密）！

#零失誤 #效率 #AI助理 #生活技巧 #避免錯誤"""

    def _generate_learn_skill_content(self, topic: str, hook: str, benefit: str) -> str:
        """生成學習技能類型的內容"""
        return f"""{hook}

**你想學習「AI 時代」的技能嗎？**

現在是 2026 年。

如果你還不會用 AI 工具，可能已經落後了。

但好消息是：**{topic}** 是最好的入門選擇。

## 為什麼是最佳入門？

因為它：

✅ **很實用** - 馬上能用在工作上
✅ **很安全** - 數據在本地，不外洩
✅ **很簡單** - 用 chat 就能操作
✅ **免費** - 不用花錢學
✅ **開源** - 可以看別人怎麼做

## 你能學到什麼？

### 技能 1：AI 自動化思維

學會怎麼把「手動任務」變成「AI 自動」：

- {topic} 怎麼自動回郵件？
- {topic} 怎麼自動排行程？
- {topic} 怎麼自動記錄會議？

這些思維可以套用到任何工具。

### 技能 2：Prompt 工程

你會學會怎麼跟 AI 講話：

- ❌ 不要說「幫我處理郵件」
- ✅ 要說「幫我分類郵件，標記緊急的，草擬回覆」

你會變成「AI 溝通大師」。

### 技能 3：系統思維

學會怎麼把不同工具串起來：

{topic} + Gmail + Calendar + Slack = 全自動化辦公

這是未來最重要的能力。

## 真實案例

有個學生用 {topic}：

- 自動整理課程表
- 自動提醒作業期限
- 自動搜尋學習資料

結果：成績提升，時間多了。

## 怎麼快速上手？

### 第 1 步：看教學（30 分鐘）

YouTube 搜尋「{topic} 小白教學」

找觀看量最高、最新的影片。

### 第 2 步：跟著做（30 分鐘）

照著教學一步步做：

1. 下載安裝
2. 設置基本功能
3. 測試第一個任務

### 第 3 步：擴充功能（持續）

加入社群，看別人怎麼用：

- Discord 社群
- GitHub 討論
- Twitter 相關話題

## 學會後能做什麼？

✅ 幫公司自動化流程
✅ 幫自己提高效率
✅ 幫家人處理事務
✅ 甚至可以幫別人設計，賺錢

## 什麼背景適合學？

- 學生 - 提升學習效率
- 上班族 - 提升工作效率
- 自由工作者 - 自動化業務
- 創業者 - 快速驗證想法

**總結**：

學會 {topic} 不只是學一個工具，而是學會「未來的做事方式」。

現在開始，為未來投資自己。

---

🎓 你想學哪些 AI 技能？
留言告訴我，我分享更多資源！

#AI技能 #學習 #未來技能 #自動化 #教學"""

    def _generate_hashtags(self, topic: str, num: int) -> List[str]:
        """生成標籤"""
        # 基礎標籤
        base_tags = [
            f"#{topic.replace(' ', '')}",
            "#AI助理",
            "#效率工具",
            "#自動化",
            "#生活黑客"
        ]

        # 平台特定標籤
        platform_tags = {
            "facebook": ["#facebook", "#fb", "#分享"],
            "instagram": ["#instagram", "#ig", "#instagood", "#生活記錄"],
            "threads": ["#threads", "#thread", "#對話"],
            "linkedin": ["#linkedin", "#professional", "#職場"]
        }

        all_tags = base_tags + platform_tags.get(self.platform, [])
        return all_tags[:num]

    def print_content(self, content_data: Dict):
        """打印生成的內容"""
        print("\n" + "="*60)
        print("✅ 內容生成成功（價值驅動 + 小白友善）")
        print("="*60)

        print(f"\n📌 標題: {content_data['title']}")
        print(f"💎 核心價值: {content_data['metadata']['value_name']}")
        print(f"📊 字數: {content_data['metadata']['word_count']:,}")
        print(f"⏱️  閱讀時間: {content_data['metadata']['reading_time']}")
        print(f"🎯 平台: {content_data['metadata']['platform']}")
        print(f"💬 語調: {content_data['metadata']['tone']}")

        print("\n📝 內容預覽:")
        print("-" * 60)
        preview = content_data['content'][:500]
        if len(content_data['content']) > 500:
            preview += "..."
        print(preview)
        print("-" * 60)

        print(f"\n🏷️  標籤: {' '.join(content_data['hashtags'])}")

        print("="*60 + "\n")

    def save_to_file(self, content_data: Dict, filepath: str):
        """保存內容到文件"""
        output = {
            "generated_at": datetime.now().isoformat(),
            **content_data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ 內容已保存到: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="生成價值驅動、小白友善的內容",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 基於研究資料生成
  python3 write-content.py --topic "Moltbot" --research research.json --use-ai

  # 快速生成（使用模板）
  python3 write-content.py --topic "AI工具" --hook "勾子" --platform facebook

  # 指定價值類型
  python3 write-content.py --topic "Moltbot" --value-type save_time --use-ai
        """
    )
    parser.add_argument("--topic", required=True, help="主題")
    parser.add_argument("--hook", help="勾子文字（如不提供將自動生成）")
    parser.add_argument("--platform", default="facebook",
                       choices=["facebook", "instagram", "threads", "linkedin"],
                       help="目標平台")
    parser.add_argument("--value-type",
                       choices=["save_time", "save_money", "reduce_effort", "avoid_mistakes", "learn_skill"],
                       help="價值類型（留空自動識別）")
    parser.add_argument("--research", help="研究資料檔案路徑（JSON）")
    parser.add_argument("--word-count", type=int, default=800,
                       help="目標字數")
    parser.add_argument("--use-ai", action="store_true",
                       help="使用 AI 生成（需要 OPENAI_API_KEY）")
    parser.add_argument("--output", default="content.json",
                       help="輸出檔案路徑")

    args = parser.parse_args()

    # 創建生成器
    generator = ValueDrivenContentGenerator(platform=args.platform)

    # 讀取研究資料
    research_data = None
    if args.research and os.path.exists(args.research):
        print(f"\n📂 讀取研究資料: {args.research}")
        with open(args.research, 'r', encoding='utf-8') as f:
            research_data = json.load(f)

    # 識別價值主張
    if args.value_type:
        value_proposition = {
            "type": args.value_type,
            "name": VALUE_TYPES[args.value_type]["name"],
            "description": VALUE_TYPES[args.value_type]["description"],
            "reader_benefit": VALUE_TYPES[args.value_type]["reader_benefit"]
        }
    else:
        value_proposition = generator.identify_value_proposition(args.topic, research_data)

    # 生成或使用勾子
    hook = args.hook
    if not hook:
        # 使用簡單的價值勾子
        hook = f"想像一下：如果{value_proposition['name']}，你的生活會變怎樣？"

    # 生成內容
    if args.use_ai:
        content_data = generator.generate_with_ai(
            topic=args.topic,
            hook=hook,
            value_proposition=value_proposition,
            research_data=research_data,
            word_count=args.word_count
        )
    else:
        content_data = generator.generate_with_template(
            topic=args.topic,
            hook=hook,
            value_proposition=value_proposition,
            research_data=research_data,
            word_count=args.word_count
        )

    # 打印結果
    generator.print_content(content_data)

    # 保存到文件
    generator.save_to_file(content_data, args.output)


if __name__ == "__main__":
    main()
