#!/usr/bin/env python3
"""
Social Content Writer - Pain-Point Based Hook Generation Script
基於真正痛點生成勾子（整合 research）
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict
import subprocess
import re

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# 痛點類型定義
PAIN_POINT_TYPES = {
    "time": {
        "name": "時間痛點",
        "description": "浪費時間、效率低、時間不夠用",
        "keywords": ["花時間", "浪費", "效率", "時間", "小時", "分鐘"],
        "hook_templates": [
            "每天花{time}處理{task}？{solution}可以幫你省回來",
            "你還在手動{task}？別人已經用{solution}自動化了",
            "{time}的瑣事，{solution}在你睡覺時幫你做完了",
            "想像一下：如果每天多出{time}，你能做什麼？"
        ]
    },
    "money": {
        "name": "金錢痛點",
        "description": "花費太高、成本失控、不划算",
        "keywords": ["花費", "成本", "錢", "貴", "便宜", "月薪", "年薪"],
        "hook_templates": [
            "聘請助理月薪${money}？{solution}免費還更好用",
            "已經幫{number}人省了${money}，你也可以",
            "為什麼付錢做{task}？{solution}幫你免費做",
            "投資回報率{roi}%：{solution}值得嗎？"
        ]
    },
    "effort": {
        "name": "努力痛點",
        "description": "太累、太複雜、學不會",
        "keywords": ["累", "複雜", "難", "麻煩", "學不會", "搞不懂"],
        "hook_templates": [
            "{task}太累了？{solution}讓你一分鐘搞定",
            "你不是不會，只是還沒用對工具",
            "別人{time}學會，你{time}就能上手",
            "{number}步變{steps}步：{solution}簡化了{task}"
        ]
    },
    "error": {
        "name": "錯誤痛點",
        "description": "容易出錯、遺漏、失敗",
        "keywords": ["錯誤", "失敗", "遺漏", "忘記", "出錯", "搞砸"],
        "hook_templates": [
            "再也不會{mistake}了，{solution}幫你記住",
            "{number}%的人都犯過{mistake}，你也是嗎？",
            "因為{mistake}損失${money}？{solution}幫你避免",
            "一次錯都不能犯？{solution}讓你零失誤"
        ]
    },
    "competition": {
        "name": "競爭痛點",
        "description": "落後於人、輸在起跑線",
        "keywords": ["落後", "輸", "競爭", "對手", "優勢", "搶先"],
        "hook_templates": [
            "別人已經在用{solution}，你還在等什麼？",
            "再不{action}，就真的輸了",
            "{competitor}都在用，你還不知道？",
            "搶先一步：{solution}讓你領先{competitor}"
        ]
    },
    "fear": {
        "name": "恐懼痛點",
        "description": "害怕被淘汰、害怕錯失",
        "keywords": ["淘汰", "錯失", "害怕", "擔心", "風險", "危險"],
        "hook_templates": [
            "再不{action}，就被淘汰了",
            "害怕錯過{opportunity}？{solution}幫你抓住",
            "{number}%的人已經開始{action}，你還在等",
            "這可能是你最後的機會"
        ]
    }
}


class PainPointHookGenerator:
    """基於痛點的勾子生成器"""

    def __init__(self, platform: str = "facebook"):
        self.platform = platform
        self.platform_limits = self._get_platform_limits()

    def _get_platform_limits(self) -> Dict:
        """獲取平台限制"""
        limits = {
            "facebook": {"max_length": 60_000, "optimal_length": 80},
            "instagram": {"max_length": 2_200, "optimal_length": 40},
            "threads": {"max_length": 500, "optimal_length": 50},
            "linkedin": {"max_length": 3_000, "optimal_length": 100}
        }
        return limits.get(self.platform, {"max_length": 10_000, "optimal_length": 80})

    def analyze_pain_points_from_research(self, research_data: Dict) -> List[Dict]:
        """從研究資料中分析痛點"""
        print("\n🔍 分析痛點中...")

        pain_points = []

        # 收集所有內容摘要
        all_summaries = []
        for item in research_data.get("data", []):
            summary = item.get("summary", "")
            if summary:
                all_summaries.append(summary)

        combined_text = " ".join(all_summaries)

        # 分析每種痛點類型
        for pain_type, config in PAIN_POINT_TYPES.items():
            # 檢查關鍵詞出現頻率
            keywords = config["keywords"]
            keyword_count = sum(combined_text.lower().count(kw.lower()) for kw in keywords)

            if keyword_count > 0:
                # 提取相關句子
                relevant_sentences = self._extract_relevant_sentences(combined_text, keywords)

                pain_points.append({
                    "type": pain_type,
                    "name": config["name"],
                    "description": config["description"],
                    "keyword_count": keyword_count,
                    "relevant_sentences": relevant_sentences[:3],  # 前 3 個相關句子
                    "severity": min(1.0, keyword_count / 10)  # 嚴重程度
                })

        # 按嚴重程度排序
        pain_points.sort(key=lambda x: x["severity"], reverse=True)

        print(f"✅ 發現 {len(pain_points)} 種痛點")

        for pp in pain_points:
            print(f"   • {pp['name']}: 嚴重度 {pp['severity']:.2f}")

        return pain_points

    def _extract_relevant_sentences(self, text: str, keywords: List[str]) -> List[str]:
        """提取包含關鍵詞的句子"""
        sentences = re.split(r'[。！？\n]', text)
        relevant = []

        for sentence in sentences:
            if len(sentence) > 10:
                for kw in keywords:
                    if kw.lower() in sentence.lower():
                        relevant.append(sentence.strip())
                        break

        return relevant

    def generate_hooks_from_pain_points(self, topic: str, pain_points: List[Dict],
                                         num_hooks: int = 10) -> List[Dict]:
        """從痛點生成勾子"""
        print(f"\n✨ 生成 {num_hooks} 個勾子...")

        hooks = []
        hooks_per_type = max(1, num_hooks // len(pain_points)) if pain_points else num_hooks

        for pain_point in pain_points[:5]:  # 最多處理前 5 個痛點
            pain_type = pain_point["type"]
            config = PAIN_POINT_TYPES[pain_type]
            templates = config["hook_templates"]

            # 從相關句子中提取實例
            examples = pain_point.get("relevant_sentences", [])

            for i in range(min(hooks_per_type, len(templates))):
                template = templates[i % len(templates)]

                # 填充模板
                hook_text = self._fill_hook_template(template, topic, pain_point, examples)

                # 計算效果分數（基於痛點嚴重程度）
                base_score = 70 + (pain_point["severity"] * 20)
                effectiveness_score = round(min(95, base_score), 0)

                hook = {
                    "type": pain_type,
                    "pain_point": config["name"],
                    "text": hook_text,
                    "effectiveness_score": int(effectiveness_score),
                    "length": len(hook_text),
                    "platform": self.platform,
                    "based_on_research": True
                }
                hooks.append(hook)

                if len(hooks) >= num_hooks:
                    break

            if len(hooks) >= num_hooks:
                break

        # 如果還不夠，補充通用勾子
        if len(hooks) < num_hooks:
            generic_hooks = self._generate_generic_hooks(topic, num_hooks - len(hooks))
            hooks.extend(generic_hooks)

        # 按效果分數排序
        hooks.sort(key=lambda x: x["effectiveness_score"], reverse=True)

        return hooks[:num_hooks]

    def _fill_hook_template(self, template: str, topic: str, pain_point: Dict,
                           examples: List[str]) -> str:
        """填充勾子模板"""
        result = template

        # 從例子中提取實際數值
        import re

        # 提取時間相關
        time_match = re.search(r'(\d+)\s*(小時|分鐘|小時)', " ".join(examples))
        time_value = time_match.group(0) if time_match else "2 小時"

        # 提取金錢相關
        money_match = re.search(r'\$?(\d+[,\d]*)', " ".join(examples))
        money_value = f"${money_match.group(1)}" if money_match else "$3,000"

        # 提取百分比
        percent_match = re.search(r'(\d+)%', " ".join(examples))
        percent_value = percent_match.group(1) if percent_match else "50"

        # 提取任務描述
        task = "處理瑣事"
        if examples:
            # 找最常見的動作詞
            for keyword in ["處理", "整理", "回覆", "管理", "記錄", "控制"]:
                if any(keyword in ex for ex in examples):
                    task = keyword
                    break

        # 替換佔位符
        replacements = {
            "{time}": time_value,
            "{money}": money_value,
            "{number}": percent_value,
            "{task}": task,
            "{solution}": topic,
            "{action}": "使用它",
            "{competitor}": "競爭對手",
            "{opportunity}": "機會",
            "{mistake}": "錯誤",
            "{roi}": percent_value,
            "{steps}": "3"
        }

        for placeholder, value in replacements.items():
            result = result.replace(placeholder, str(value))

        return result

    def _generate_generic_hooks(self, topic: str, count: int) -> List[Dict]:
        """生成通用勾子（當沒有足夠研究資料時）"""
        generic_templates = [
            f"為什麼大家都在討論{topic}？",
            f"{topic}可能會改變你的工作方式",
            f"如果你還沒用{topic}，現在可能是時候了",
            f"這就是{topic}：簡單、強大、免費",
            f"關於{topic}，你需要知道的幾件事"
        ]

        hooks = []
        for i in range(min(count, len(generic_templates))):
            hook = {
                "type": "generic",
                "pain_point": "通用",
                "text": generic_templates[i],
                "effectiveness_score": 70,
                "length": len(generic_templates[i]),
                "platform": self.platform,
                "based_on_research": False
            }
            hooks.append(hook)

        return hooks

    def generate(self, topic: str, research_file: str = None,
                num_hooks: int = 10) -> List[Dict]:
        """生成勾子（整合研究資料）"""

        print("\n" + "="*60)
        print("✨ 勾子生成器（痛點驅動）")
        print("="*60)

        # 階段 1: 如果有研究資料，先分析痛點
        pain_points = []
        if research_file and os.path.exists(research_file):
            print(f"\n📂 讀取研究資料: {research_file}")
            with open(research_file, 'r', encoding='utf-8') as f:
                research_data = json.load(f)

            pain_points = self.analyze_pain_points_from_research(research_data)

        # 階段 2: 從痛點生成勾子
        if pain_points:
            hooks = self.generate_hooks_from_pain_points(topic, pain_points, num_hooks)
        else:
            print("\n⚠️  沒有研究資料，使用通用勾子")
            hooks = self._generate_generic_hooks(topic, num_hooks)

        return hooks

    def print_hooks(self, hooks: List[Dict]):
        """打印勾子列表"""
        print("\n" + "="*60)
        print("✨ 生成的勾子（痛點驅動）")
        print("="*60)

        for i, hook in enumerate(hooks, 1):
            research_tag = "🔬" if hook.get("based_on_research") else "📝"
            print(f"\n{research_tag} [{i}] {hook['pain_point'].upper()} (分數: {hook['effectiveness_score']}/100)")
            print(f"   {hook['text']}")
            print(f"   長度: {hook['length']} 字")

        print("="*60 + "\n")

    def save_to_file(self, hooks: List[Dict], filepath: str):
        """保存勾子到文件"""
        output = {
            "generated_at": datetime.now().isoformat(),
            "platform": self.platform,
            "total_hooks": len(hooks),
            "hooks": hooks
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ 勾子已保存到: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="基於痛點生成勾子（整合 research）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 基於研究資料生成勾子
  python3 hook-generator.py --topic "Moltbot" --research research_data.json

  # 獨立使用（不依賴研究資料）
  python3 hook-generator.py --topic "AI工具" --num-hooks 10

  # 先做研究再生成勾子
  python3 collect.py --topic "Moltbot" --deep-research --output research.json
  python3 hook-generator.py --topic "Moltbot" --research research.json
        """
    )
    parser.add_argument("--topic", required=True, help="主題")
    parser.add_argument("--platform", default="facebook",
                       choices=["facebook", "instagram", "threads", "linkedin"],
                       help="目標平台")
    parser.add_argument("--num-hooks", type=int, default=10,
                       help="生成勾子數量")
    parser.add_argument("--research", help="研究資料檔案路徑（JSON）")
    parser.add_argument("--output", default="hooks.json",
                       help="輸出檔案路徑")

    args = parser.parse_args()

    # 創建生成器
    generator = PainPointHookGenerator(platform=args.platform)

    # 生成勾子
    hooks = generator.generate(
        topic=args.topic,
        research_file=args.research,
        num_hooks=args.num_hooks
    )

    # 打印結果
    generator.print_hooks(hooks)

    # 保存到文件
    generator.save_to_file(hooks, args.output)


if __name__ == "__main__":
    main()
