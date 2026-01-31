#!/usr/bin/env python3
"""
Social Content Writer - Content Analyzer
分析內容質量並提供改進建議
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List
import re


# 質量評估標準
QUALITY_METRICS = {
    "length": {
        "weight": 0.15,
        "optimal_range": {
            "facebook": (300, 800),
            "instagram": (100, 200),
            "threads": (50, 200),
            "linkedin": (800, 1500)
        }
    },
    "structure": {
        "weight": 0.25,
        "criteria": ["has_hook", "has_body", "has_cta", "clear_flow"]
    },
    "engagement": {
        "weight": 0.20,
        "criteria": ["questions", "emotional_words", "action_verbs"]
    },
    "readability": {
        "weight": 0.15,
        "criteria": ["sentence_length", "paragraph_length", "jargon_usage"]
    },
    "hashtags": {
        "weight": 0.10,
        "optimal_count": {
            "facebook": (2, 5),
            "instagram": (15, 25),
            "threads": (2, 5),
            "linkedin": (2, 5)
        }
    },
    "emotional_impact": {
        "weight": 0.15,
        "criteria": ["power_words", "story_elements", "personal_touch"]
    }
}


class ContentAnalyzer:
    """內容分析器"""

    def __init__(self, platform: str = "facebook"):
        self.platform = platform
        self.metrics = QUALITY_METRICS

    def analyze(self, content: str, hashtags: List[str] = None) -> Dict:
        """全面分析內容"""
        if hashtags is None:
            hashtags = []

        results = {
            "platform": self.platform,
            "overall_score": 0,
            "metrics": {},
            "suggestions": [],
            "strengths": [],
            "improvements": []
        }

        # 1. 長度分析
        length_score, length_analysis = self._analyze_length(content)
        results["metrics"]["length"] = length_analysis
        results["overall_score"] += length_score * self.metrics["length"]["weight"]

        # 2. 結構分析
        structure_score, structure_analysis = self._analyze_structure(content)
        results["metrics"]["structure"] = structure_analysis
        results["overall_score"] += structure_score * self.metrics["structure"]["weight"]

        # 3. 互動性分析
        engagement_score, engagement_analysis = self._analyze_engagement(content)
        results["metrics"]["engagement"] = engagement_analysis
        results["overall_score"] += engagement_score * self.metrics["engagement"]["weight"]

        # 4. 可讀性分析
        readability_score, readability_analysis = self._analyze_readability(content)
        results["metrics"]["readability"] = readability_analysis
        results["overall_score"] += readability_score * self.metrics["readability"]["weight"]

        # 5. 標籤分析
        hashtag_score, hashtag_analysis = self._analyze_hashtags(hashtags)
        results["metrics"]["hashtags"] = hashtag_analysis
        results["overall_score"] += hashtag_score * self.metrics["hashtags"]["weight"]

        # 6. 情感影響力分析
        emotional_score, emotional_analysis = self._analyze_emotional_impact(content)
        results["metrics"]["emotional_impact"] = emotional_analysis
        results["overall_score"] += emotional_score * self.metrics["emotional_impact"]["weight"]

        # 轉換為百分比
        results["overall_score"] = round(results["overall_score"] * 100, 1)

        # 生成建議
        results["suggestions"] = self._generate_suggestions(results)

        # 識別優勢和改進點
        results["strengths"] = self._identify_strengths(results)
        results["improvements"] = self._identify_improvements(results)

        return results

    def _analyze_length(self, content: str) -> tuple:
        """分析內容長度"""
        length = len(content)
        optimal = self.metrics["length"]["optimal_range"][self.platform]
        min_opt, max_opt = optimal

        if min_opt <= length <= max_opt:
            score = 1.0
            status = "理想"
        elif length < min_opt:
            score = max(0.3, length / min_opt)
            status = "偏短"
        else:
            score = max(0.5, max_opt / length)
            status = "偏長"

        analysis = {
            "length": length,
            "optimal_range": optimal,
            "status": status,
            "score": round(score, 2)
        }

        return score, analysis

    def _analyze_structure(self, content: str) -> tuple:
        """分析內容結構"""
        criteria = self.metrics["structure"]["criteria"]
        scores = {}

        # 檢查是否有勾子（開頭問句或感嘆句）
        has_hook = bool(re.search(r'^.{0,50}[?！]', content))
        scores["has_hook"] = 1.0 if has_hook else 0.3

        # 檢查是否有正文（內容是否足夠長）
        has_body = len(content) > 100
        scores["has_body"] = 1.0 if has_body else 0.5

        # 檢查是否有行動召喚
        cta_keywords = ["留言", "分享", "關注", "點擊", "comment", "share", "follow"]
        has_cta = any(keyword in content for keyword in cta_keywords)
        scores["has_cta"] = 1.0 if has_cta else 0.4

        # 檢查流程（是否分段清晰）
        clear_flow = content.count('\n\n') >= 1 or len(re.findall(r'[。！？]', content)) >= 3
        scores["clear_flow"] = 1.0 if clear_flow else 0.6

        avg_score = sum(scores.values()) / len(scores)

        analysis = {
            "criteria": scores,
            "score": round(avg_score, 2),
            "details": {
                "has_hook": has_hook,
                "has_body": has_body,
                "has_cta": has_cta,
                "clear_flow": clear_flow
            }
        }

        return avg_score, analysis

    def _analyze_engagement(self, content: str) -> tuple:
        """分析互動性"""
        # 檢查問句
        questions = len(re.findall(r'[?？]', content))
        question_score = min(1.0, questions / 2)

        # 檢查情感詞
        emotional_words = ["驚喜", "興奮", "喜歡", "愛", "開心", "amazing", "love", "excited"]
        emotional_count = sum(1 for word in emotional_words if word in content.lower())
        emotional_score = min(1.0, emotional_count / 2)

        # 檢查行動動詞
        action_verbs = ["立即", "現在", "趕快", "開始", "start", "now", "discover"]
        action_count = sum(1 for verb in action_verbs if verb in content.lower())
        action_score = min(1.0, action_count / 2)

        avg_score = (question_score + emotional_score + action_score) / 3

        analysis = {
            "questions": questions,
            "emotional_words": emotional_count,
            "action_verbs": action_count,
            "score": round(avg_score, 2)
        }

        return avg_score, analysis

    def _analyze_readability(self, content: str) -> tuple:
        """分析可讀性"""
        # 平均句子長度
        sentences = re.split(r'[。！？\n]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences) if sentences else 0

        # 句子長度評分
        if avg_sentence_length < 30:
            sentence_score = 1.0
        elif avg_sentence_length < 50:
            sentence_score = 0.8
        else:
            sentence_score = 0.6

        # 段落長度
        paragraphs = content.split('\n\n')
        avg_paragraph_length = sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0

        # 段落長度評分
        if avg_paragraph_length < 200:
            paragraph_score = 1.0
        elif avg_paragraph_length < 400:
            paragraph_score = 0.8
        else:
            paragraph_score = 0.6

        avg_score = (sentence_score + paragraph_score) / 2

        analysis = {
            "avg_sentence_length": round(avg_sentence_length, 1),
            "avg_paragraph_length": round(avg_paragraph_length, 1),
            "score": round(avg_score, 2)
        }

        return avg_score, analysis

    def _analyze_hashtags(self, hashtags: List[str]) -> tuple:
        """分析標籤"""
        count = len(hashtags)
        optimal = self.metrics["hashtags"]["optimal_count"][self.platform]
        min_opt, max_opt = optimal

        if min_opt <= count <= max_opt:
            score = 1.0
            status = "理想"
        elif count < min_opt:
            score = max(0.5, count / min_opt)
            status = "偏少"
        else:
            score = max(0.5, max_opt / count)
            status = "偏多"

        analysis = {
            "count": count,
            "hashtags": hashtags,
            "optimal_range": optimal,
            "status": status,
            "score": round(score, 2)
        }

        return score, analysis

    def _analyze_emotional_impact(self, content: str) -> tuple:
        """分析情感影響力"""
        # 強力詞彙
        power_words = [
            "革命性", "突破", "驚人", "絕佳", "必須", "revolutionary",
            "breakthrough", "amazing", "must-have", "essential"
        ]
        power_count = sum(1 for word in power_words if word in content.lower())
        power_score = min(1.0, power_count / 3)

        # 故事元素
        story_indicators = ["當我", "我曾經", "經歷", "故事", "when I", "my story", "experience"]
        story_score = 1.0 if any(indicator in content for indicator in story_indicators) else 0.6

        # 個人觸摸
        personal_indicators = ["我", "我的", "I", "my", "me"]
        personal_count = sum(content.lower().count(indicator) for indicator in personal_indicators)
        personal_score = min(1.0, personal_count / 10)

        avg_score = (power_score + story_score + personal_score) / 3

        analysis = {
            "power_words": power_count,
            "story_elements": story_score,
            "personal_touch": personal_count,
            "score": round(avg_score, 2)
        }

        return avg_score, analysis

    def _generate_suggestions(self, results: Dict) -> List[str]:
        """生成改進建議"""
        suggestions = []

        # 長度建議
        length_status = results["metrics"]["length"]["status"]
        if length_status == "偏短":
            suggestions.append("內容偏短，建議增加更多細節和例子")
        elif length_status == "偏長":
            suggestions.append("內容偏長，考慮分段或縮減部分內容")

        # 結構建議
        if not results["metrics"]["structure"]["details"]["has_hook"]:
            suggestions.append("缺少吸引人的開頭勾子，建議加入問句或驚人事實")

        if not results["metrics"]["structure"]["details"]["has_cta"]:
            suggestions.append("缺少明確的行動召喚，建議在結尾加入「留言分享」等提示")

        # 互動性建議
        if results["metrics"]["engagement"]["questions"] < 2:
            suggestions.append("互動性不足，建議增加問句以引發討論")

        # 標籤建議
        hashtag_status = results["metrics"]["hashtags"]["status"]
        if hashtag_status == "偏少":
            suggestions.append(f"標籤偏少，建議增加到 {self.metrics['hashtags']['optimal_count'][self.platform][0]} 個以上")
        elif hashtag_status == "偏多":
            suggestions.append("標籤過多可能顯得垃圾，考慮只保留最相關的")

        # 情感影響力建議
        if results["metrics"]["emotional_impact"]["power_words"] < 2:
            suggestions.append("可以加入更多強力詞彙增強情感衝擊")

        if not results["metrics"]["emotional_impact"]["story_elements"]:
            suggestions.append("考慮加入個人故事或案例增加真實感")

        return suggestions

    def _identify_strengths(self, results: Dict) -> List[str]:
        """識別內容優勢"""
        strengths = []

        if results["metrics"]["length"]["status"] == "理想":
            strengths.append("內容長度適中")

        if results["metrics"]["structure"]["details"]["has_hook"]:
            strengths.append("有吸引人的開頭勾子")

        if results["metrics"]["structure"]["details"]["has_cta"]:
            strengths.append("包含明確的行動召喚")

        if results["metrics"]["engagement"]["questions"] >= 2:
            strengths.append("互動性良好（包含多個問句）")

        if results["metrics"]["hashtags"]["status"] == "理想":
            strengths.append("標籤使用恰當")

        if results["metrics"]["emotional_impact"]["story_elements"]:
            strengths.append("包含故事元素增強吸引力")

        return strengths

    def _identify_improvements(self, results: Dict) -> List[str]:
        """識別需要改進的地方"""
        improvements = []

        if results["metrics"]["structure"]["score"] < 0.7:
            improvements.append("內容結構需要優化")

        if results["metrics"]["engagement"]["score"] < 0.6:
            improvements.append("互動性需要提升")

        if results["metrics"]["readability"]["score"] < 0.7:
            improvements.append("可讀性需要改善")

        if results["metrics"]["emotional_impact"]["score"] < 0.6:
            improvements.append("情感影響力不足")

        return improvements

    def print_analysis(self, results: Dict):
        """打印分析結果"""
        print("\n" + "="*60)
        print(f"📊 內容分析報告 ({results['platform'].upper()})")
        print("="*60)

        print(f"\n總體評分: {results['overall_score']}/100")

        print("\n📈 各項指標:")
        print("-" * 60)

        for metric_name, metric_data in results["metrics"].items():
            score = metric_data.get("score", 0)
            score_bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            print(f"\n{metric_name.upper().replace('_', ' ')}")
            print(f"  分數: {score*100:.0f}/100  [{score_bar}]")

            # 顯示詳細信息
            if metric_name == "length":
                print(f"  長度: {metric_data['length']:,} 字")
                print(f"  狀態: {metric_data['status']}")
            elif metric_name == "structure":
                details = metric_data.get("details", {})
                if details.get("has_hook"):
                    print(f"  ✓ 包含勾子")
                if details.get("has_cta"):
                    print(f"  ✓ 包含行動召喚")
            elif metric_name == "engagement":
                print(f"  問句數: {metric_data['questions']}")
                print(f"  情感詞: {metric_data['emotional_words']}")
            elif metric_name == "hashtags":
                print(f"  標籤數: {metric_data['count']} ({metric_data['status']})")

        # 優勢
        if results["strengths"]:
            print(f"\n✅ 優勢:")
            for strength in results["strengths"]:
                print(f"   • {strength}")

        # 改進建議
        if results["improvements"]:
            print(f"\n⚠️  需要改進:")
            for improvement in results["improvements"]:
                print(f"   • {improvement}")

        # 具體建議
        if results["suggestions"]:
            print(f"\n💡 改進建議:")
            for i, suggestion in enumerate(results["suggestions"], 1):
                print(f"   {i}. {suggestion}")

        print("="*60 + "\n")

    def save_to_file(self, results: Dict, filepath: str):
        """保存分析結果到文件"""
        output = {
            "analyzed_at": datetime.now().isoformat(),
            **results
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ 分析結果已保存到: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="分析內容質量並提供改進建議",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 分析內容文件
  python3 analyze.py --content content.json --platform facebook

  # 分析文字內容
  python3 analyze.py --content "你的內容文字" --platform instagram --detailed

  # 使用交互模式
  python3 analyze.py --interactive
        """
    )
    parser.add_argument("--content", help="內容檔案路徑或內容文字")
    parser.add_argument("--platform", default="facebook",
                       choices=["facebook", "instagram", "threads", "linkedin"],
                       help="目標平台")
    parser.add_argument("--hashtags", help="標籤列表（逗號分隔）")
    parser.add_argument("--detailed", action="store_true",
                       help="顯示詳細分析")
    parser.add_argument("--output", default="analysis_results.json",
                       help="輸出檔案路徑")

    args = parser.parse_args()

    if not args.content:
        # 交互模式
        print("📝 請輸入要分析的内容（按 Ctrl+D 結束輸入）:")
        content_lines = []
        try:
            for line in sys.stdin:
                content_lines.append(line)
        except KeyboardInterrupt:
            pass
        content = "".join(content_lines)
        hashtags = []
    elif os.path.exists(args.content):
        # 從文件讀取
        with open(args.content, 'r', encoding='utf-8') as f:
            data = json.load(f)
            content = data.get("content", "")
            hashtags = data.get("hashtags", [])
    else:
        # 直接使用輸入的文字
        content = args.content
        hashtags = args.hashtags.split(",") if args.hashtags else []

    if not content:
        print("❌ 錯誤：內容為空")
        return

    # 創建分析器
    analyzer = ContentAnalyzer(platform=args.platform)

    # 分析內容
    results = analyzer.analyze(content, hashtags)

    # 打印結果
    analyzer.print_analysis(results)

    # 保存到文件
    analyzer.save_to_file(results, args.output)


if __name__ == "__main__":
    main()
