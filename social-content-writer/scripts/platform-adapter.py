#!/usr/bin/env python3
"""
Social Content Writer - Platform Adapter
將內容適配到不同平台的規則和格式
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List


# 平台規則配置
PLATFORM_RULES = {
    "facebook": {
        "max_length": 60_000,
        "optimal_length": 500,
        "min_length": 40,
        "max_hashtags": 5,
        "optimal_hashtags": 3,
        "supports_markdown": True,
        "supports_emojis": True,
        "line_breaks": "double",  # single, double, none
        "link_placement": "after_content",  # in_content, after_content, none
        "tone_suggestions": ["professional", "friendly", "authoritative"],
        "content_type": "long_form",
        "call_to_action": "強烈建議",
        "image_ratio": "16:9 or 1:1",
        "video_ratio": "16:9"
    },
    "instagram": {
        "max_length": 2_200,
        "optimal_length": 150,
        "min_length": 50,
        "max_hashtags": 30,
        "optimal_hashtags": 20,
        "supports_markdown": False,
        "supports_emojis": True,
        "line_breaks": "double",
        "link_placement": "bio_only",  # Instagram only allows links in bio
        "tone_suggestions": ["casual", "friendly", "inspirational"],
        "content_type": "visual_first",
        "call_to_action": "建議",
        "image_ratio": "1:1 or 4:5",
        "video_ratio": "9:16 or 1:1"
    },
    "threads": {
        "max_length": 500,
        "optimal_length": 150,
        "min_length": 20,
        "max_hashtags": 5,
        "optimal_hashtags": 3,
        "supports_markdown": False,
        "supports_emojis": True,
        "line_breaks": "single",
        "link_placement": "in_content",
        "tone_suggestions": ["casual", "friendly", "conversational"],
        "content_type": "short_form",
        "call_to_action": "可選",
        "image_ratio": "16:9 or 1:1",
        "video_ratio": "9:16 or 16:9"
    },
    "linkedin": {
        "max_length": 3_000,
        "optimal_length": 1_200,
        "min_length": 100,
        "max_hashtags": 5,
        "optimal_hashtags": 3,
        "supports_markdown": True,
        "supports_emojis": False,  # Limited emoji support
        "line_breaks": "double",
        "link_placement": "after_content",
        "tone_suggestions": ["professional", "authoritative", "insightful"],
        "content_type": "professional",
        "call_to_action": "強烈建議",
        "image_ratio": "16:9 or 4:5",
        "video_ratio": "16:9"
    },
    "twitter": {  # For future use
        "max_length": 280,
        "optimal_length": 100,
        "min_length": 10,
        "max_hashtags": 3,
        "optimal_hashtags": 2,
        "supports_markdown": False,
        "supports_emojis": True,
        "line_breaks": "single",
        "link_placement": "in_content",
        "tone_suggestions": ["casual", "conversational", "witty"],
        "content_type": "micro",
        "call_to_action": "可選",
        "image_ratio": "16:9",
        "video_ratio": "16:9"
    }
}


class PlatformAdapter:
    """平台適配器"""

    def __init__(self):
        self.rules = PLATFORM_RULES

    def adapt_content(self, content: str, platform: str,
                     adjust_length: bool = True,
                     optimize_hashtags: bool = True) -> Dict:
        """適配內容到指定平台"""
        if platform not in self.rules:
            raise ValueError(f"不支援的平台: {platform}")

        platform_rule = self.rules[platform]

        result = {
            "platform": platform,
            "original_length": len(content),
            "adapted_content": content,
            "changes": []
        }

        # 調整長度
        if adjust_length:
            adapted = self._adjust_length(content, platform_rule)
            if adapted != content:
                result["adapted_content"] = adapted
                result["changes"].append("長度已調整")

        # 格式化換行
        result["adapted_content"] = self._format_line_breaks(
            result["adapted_content"],
            platform_rule["line_breaks"]
        )

        # 處理鏈接
        result["link_handling"] = platform_rule["link_placement"]

        # 移除 Markdown（如果平台不支援）
        if not platform_rule["supports_markdown"]:
            result["adapted_content"] = self._remove_markdown(result["adapted_content"])
            result["changes"].append("Markdown 格式已移除")

        # 處理表情符號
        if not platform_rule["supports_emojis"]:
            result["adapted_content"] = self._remove_emojis(result["adapted_content"])
            result["changes"].append("表情符號已移除")

        # 檢查長度
        result["final_length"] = len(result["adapted_content"])
        result["within_limit"] = result["final_length"] <= platform_rule["max_length"]

        if not result["within_limit"]:
            result["warning"] = f"內容超過平台限制 ({result['final_length']} > {platform_rule['max_length']})"

        return result

    def _adjust_length(self, content: str, rule: Dict) -> str:
        """調整內容長度"""
        max_length = rule["max_length"]
        optimal_length = rule["optimal_length"]

        if len(content) <= max_length:
            return content

        # 內容過長，需要縮短
        if len(content) > max_length:
            # 嘗試智能截斷
            sentences = content.split('。')
            shortened = ""

            for sentence in sentences:
                if len(shortened) + len(sentence) + 1 <= max_length - 50:  # 留 50 字給結尾
                    shortened += sentence + "。"
                else:
                    break

            if shortened:
                shortened += "…（內容已縮短）"
                return shortened

            # 如果無法智能截斷，直接截斷
            return content[:max_length - 20] + "…（內容已截斷）"

        return content

    def _format_line_breaks(self, content: str, style: str) -> str:
        """格式化換行"""
        if style == "double":
            # 確保段落間有雙換行
            import re
            content = re.sub(r'\n{3,}', '\n\n', content)  # 移除多餘換行
            content = re.sub(r'(?<=[。！？])\n', '\n\n', content)  # 句號後加雙換行
        elif style == "single":
            # 確保只有單換行
            import re
            content = re.sub(r'\n{2,}', '\n', content)
        elif style == "none":
            # 移除所有換行
            content = content.replace('\n', ' ')

        return content

    def _remove_markdown(self, content: str) -> str:
        """移除 Markdown 格式"""
        import re

        # 移除粗體
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
        content = re.sub(r'__(.*?)__', r'\1', content)

        # 移除斜體
        content = re.sub(r'\*(.*?)\*', r'\1', content)
        content = re.sub(r'_(.*?)_', r'\1', content)

        # 移除標題
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)

        # 移除鏈接格式但保留 URL
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\2', content)

        # 移除代碼塊
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content = re.sub(r'`([^`]+)`', r'\1', content)

        return content

    def _remove_emojis(self, content: str) -> str:
        """移除表情符號"""
        import re
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub('', content)

    def optimize_hashtags_for_platform(self, hashtags: List[str],
                                       platform: str) -> List[str]:
        """為平台優化標籤"""
        rule = self.rules.get(platform, self.rules["facebook"])

        # 限制標籤數量
        optimized = hashtags[:rule["max_hashtags"]]

        # 平台特定優化
        if platform == "instagram":
            # Instagram 喜歡更多標籤
            pass
        elif platform == "linkedin":
            # LinkedIn 移除過於隨意的標籤
            optimized = [tag for tag in optimized if not any(
                word in tag.lower() for word in ["#fun", "#cute", "#lol"]
            )]

        return optimized

    def adapt_to_multiple_platforms(self, content: str,
                                    platforms: List[str]) -> Dict[str, Dict]:
        """適配內容到多個平台"""
        results = {}

        for platform in platforms:
            try:
                results[platform] = self.adapt_content(content, platform)
            except ValueError as e:
                results[platform] = {"error": str(e)}

        return results

    def get_platform_suggestions(self, platform: str) -> Dict:
        """獲取平台建議"""
        if platform not in self.rules:
            return {"error": f"不支援的平台: {platform}"}

        rule = self.rules[platform]

        return {
            "platform": platform,
            "content_type": rule["content_type"],
            "optimal_length": rule["optimal_length"],
            "recommended_tones": rule["tone_suggestions"],
            "call_to_action": rule["call_to_action"],
            "supports_markdown": rule["supports_markdown"],
            "supports_emojis": rule["supports_emojis"],
            "image_ratio": rule.get("image_ratio", "N/A"),
            "video_ratio": rule.get("video_ratio", "N/A"),
            "tips": self._get_platform_tips(platform)
        }

    def _get_platform_tips(self, platform: str) -> List[str]:
        """獲取平台特定提示"""
        tips = {
            "facebook": [
                "使用吸引人的開頭句",
                "包含清晰的行動召喚",
                "考慮使用相關的圖片或影片",
                "最佳發布時間：工作日 9-10 AM 或 2-4 PM"
            ],
            "instagram": [
                "首句最重要（會被截斷）",
                "使用 20-30 個相關標籤",
                "視覺內容是關鍵",
                "使用 Instagram Stories 增加互動"
            ],
            "threads": [
                "保持簡短有力",
                "第一句就要抓住注意力",
                "使用對話式語調",
                "快速回覆評論建立互動"
            ],
            "linkedin": [
                "提供專業洞察",
                "使用個人故事增加可信度",
                "避免過度推銷",
                "最佳長度：1,000-1,500 字"
            ],
            "twitter": [
                "使用視覺內容增加互動",
                "第一句就要抓住注意力",
                "使用相關標籤（1-2 個）",
                "考慮使用 thread 講述完整故事"
            ]
        }
        return tips.get(platform, [])

    def print_adaptation_results(self, results: Dict):
        """打印適配結果"""
        print("\n" + "="*60)
        print("🎯 平台適配結果")
        print("="*60)

        for platform, result in results.items():
            if "error" in result:
                print(f"\n❌ {platform.upper()}: {result['error']}")
                continue

            print(f"\n✅ {platform.upper()}")
            print(f"   原始長度: {result['original_length']:,} 字")
            print(f"   適配後長度: {result['final_length']:,} 字")
            print(f"   在限制內: {'是' if result['within_limit'] else '否'}")

            if result.get("changes"):
                print(f"   更改: {', '.join(result['changes'])}")

            if result.get("warning"):
                print(f"   ⚠️  {result['warning']}")

            # 顯示部分內容
            preview = result['adapted_content'][:100]
            if len(result['adapted_content']) > 100:
                preview += "..."
            print(f"   預覽: {preview}")

        print("="*60 + "\n")

    def save_to_file(self, results: Dict, filepath: str):
        """保存適配結果到文件"""
        output = {
            "adapted_at": datetime.now().isoformat(),
            "platforms": results
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ 適配結果已保存到: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="將內容適配到不同平台",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 適配單一平台
  python3 platform-adapter.py --input content.json --target-platforms facebook

  # 適配多平台
  python3 platform-adapter.py --input content.json --target-platforms facebook,instagram,linkedin

  # 獲取平台建議
  python3 platform-adapter.py --platform-info instagram
        """
    )
    parser.add_argument("--input", help="輸入內容檔案（JSON）")
    parser.add_argument("--content", help="直接輸入內容文字")
    parser.add_argument("--target-platforms",
                       help="目標平台（逗號分隔）")
    parser.add_argument("--adjust-length", action="store_true", default=True,
                       help="自動調整長度")
    parser.add_argument("--optimize-hashtags", action="store_true", default=True,
                       help="優化標籤")
    parser.add_argument("--platform-info",
                       help="獲取平台資訊和建议")
    parser.add_argument("--output", default="adapted_content.json",
                       help="輸出檔案路徑")

    args = parser.parse_args()

    adapter = PlatformAdapter()

    # 獲取平台資訊
    if args.platform_info:
        suggestions = adapter.get_platform_suggestions(args.platform_info)

        print("\n" + "="*60)
        print(f"📱 {args.platform_info.upper()} 平台資訊")
        print("="*60)

        print(f"\n內容類型: {suggestions['content_type']}")
        print(f"建議長度: {suggestions['optimal_length']:,} 字")
        print(f"推薦語調: {', '.join(suggestions['recommended_tones'])}")
        print(f"行動召喚: {suggestions['call_to_action']}")
        print(f"支援 Markdown: {'是' if suggestions['supports_markdown'] else '否'}")
        print(f"支援表情符號: {'是' if suggestions['supports_emojis'] else '否'}")
        print(f"建議圖片比例: {suggestions['image_ratio']}")
        print(f"建議影片比例: {suggestions['video_ratio']}")

        print(f"\n💡 平台提示:")
        for tip in suggestions['tips']:
            print(f"   • {tip}")

        print("="*60 + "\n")
        return

    # 適配內容
    if not args.input and not args.content:
        print("❌ 錯誤：請提供 --input 或 --content")
        return

    # 讀取內容
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 提取內容（可能是單個內容或多平台內容）
            if "platforms" in data:
                # 多平台內容，取第一個
                first_platform = list(data["platforms"].keys())[0]
                content = data["platforms"][first_platform]["content"]
            else:
                content = data.get("content", "")
    else:
        content = args.content

    if not content:
        print("❌ 錯誤：無法提取內容")
        return

    # 解析目標平台
    platforms = [p.strip() for p in args.target_platforms.split(",")]

    # 適配到多平台
    results = adapter.adapt_to_multiple_platforms(content, platforms)

    # 打印結果
    adapter.print_adaptation_results(results)

    # 保存到文件
    adapter.save_to_file(results, args.output)


if __name__ == "__main__":
    main()
