#!/usr/bin/env python3
"""
Social Content Writer - Research Data Collection Script
從多個來源收集相關資料並評分（真正整合 MCP）
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ResearchCollector:
    """研究資料收集器 - 真正整合 MCP 工具"""

    def __init__(self, min_score: float = 0.6):
        self.min_score = min_score
        self.collected_data = []

    def collect_from_web_search(self, topic: str, max_results: int = 10) -> List[Dict]:
        """從網路搜尋收集資料（使用 web-search-prime MCP）"""
        print(f"🔍 正在搜尋主題: {topic}")

        # 調用 web-search-prime MCP
        try:
            # 使用 subprocess 調用 MCP 工具（通過臨時 Python 腳本）
            script_content = f'''
import json
import sys
sys.path.insert(0, "/home/jackalchiu/claude/.claude")

from mcp__web_search_prime import webSearchPrime

results = webSearchPrime(
    search_query="{topic}",
    search_recency_filter="oneMonth",
    content_size="high",
    location="cn"
)

print(json.dumps(results))
'''

            # 寫入臨時腳本
            temp_script = "/tmp/mcp_search.py"
            with open(temp_script, 'w') as f:
                f.write(script_content)

            # 執行
            result = subprocess.run(
                ["python3", temp_script],
                capture_output=True,
                text=True,
                timeout=60
            )

            # 清理臨時文件
            os.remove(temp_script)

            if result.returncode == 0 and result.stdout:
                search_results = json.loads(result.stdout)

                if search_results and len(search_results) > 0:
                    processed_results = []
                    for item in search_results[:max_results]:
                        processed = {
                            "source_type": "web_search",
                            "title": item.get("title", ""),
                            "url": item.get("link", ""),
                            "summary": item.get("content", "")[:500],
                            "relevance_score": 0.85,  # 搜尋結果相關性高
                            "credibility_score": 0.75,
                            "recency_score": 0.90,
                            "completeness_score": 0.70
                        }
                        processed_results.append(processed)

                    print(f"✅ 找到 {len(processed_results)} 筆搜尋結果")
                    return processed_results
                else:
                    print("⚠️  搜尋結果為空")
                    return []
            else:
                print(f"⚠️  搜尋失敗: {result.stderr}")
                return []

        except Exception as e:
            print(f"⚠️  搜尋過程出錯: {e}")
            return []

    def collect_from_web_reader(self, urls: List[str]) -> List[Dict]:
        """使用 web-reader MCP 讀取網頁內容"""
        print(f"📖 正在讀取 {len(urls)} 個網頁...")

        results = []

        for url in urls[:5]:  # 限制數量避免超時
            try:
                script_content = f'''
import json
import sys
sys.path.insert(0, "/home/jackalchiu/claude/.claude")

from mcp__web_reader import webReader

result = webReader(
    url="{url}",
    return_format="markdown",
    retain_images=False
)

print(json.dumps({{"url": "{url}", "content": result}}))
'''

                temp_script = "/tmp/mcp_read.py"
                with open(temp_script, 'w') as f:
                    f.write(script_content)

                result = subprocess.run(
                    ["python3", temp_script],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                os.remove(temp_script)

                if result.returncode == 0 and result.stdout:
                    data = json.loads(result.stdout)
                    content = data.get("content", "")

                    if content and len(content) > 100:
                        # 提取摘要（前 500 字）
                        summary = content[:500].replace('\n', ' ')

                        processed = {
                            "source_type": "web_reader",
                            "title": f"內容提取: {url[:50]}...",
                            "url": url,
                            "summary": summary,
                            "relevance_score": 0.90,
                            "credibility_score": 0.85,
                            "recency_score": 0.80,
                            "completeness_score": 0.90
                        }
                        results.append(processed)
                        print(f"  ✅ 已讀取: {url[:50]}...")

            except Exception as e:
                print(f"  ⚠️  讀取失敗 {url}: {e}")
                continue

        return results

    def collect_from_database(self, topic: str, max_results: int = 5) -> List[Dict]:
        """從資料庫收集歷史資料"""
        print(f"💾 正在查詢資料庫: {topic}")

        # 檢查 MySQL 是否配置
        if not os.environ.get("MYSQL_HOST"):
            print("  ⚠️  未配置 MySQL，跳過資料庫查詢")
            return []

        try:
            mysql_script = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "mysql",
                "scripts",
                "query.py"
            )

            if not os.path.exists(mysql_script):
                print("  ⚠️  MySQL 腳本不存在")
                return []

            # 構建查詢
            query = f"""
            SELECT topic, content, platform, created_at
            FROM content_history
            WHERE topic LIKE '%{topic}%'
            ORDER BY created_at DESC
            LIMIT {max_results}
            """

            result = subprocess.run(
                ["python3", mysql_script, query],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                results = []
                for item in data:
                    results.append({
                        "source_type": "database",
                        "title": f"歷史內容: {item.get('topic', '')}",
                        "url": None,
                        "summary": item.get('content', '')[:300],
                        "relevance_score": 0.80,
                        "credibility_score": 0.90,
                        "recency_score": 0.60,
                        "completeness_score": 0.85
                    })
                print(f"  ✅ 找到 {len(results)} 筆歷史資料")
                return results
            else:
                print(f"  ⚠️  查詢失敗: {result.stderr}")
                return []

        except Exception as e:
            print(f"  ⚠️  資料庫查詢錯誤: {e}")
            return []

    def calculate_quality_score(self, item: Dict) -> float:
        """計算綜合質量分數"""
        weights = {
            "relevance": 0.4,
            "credibility": 0.3,
            "recency": 0.2,
            "completeness": 0.1
        }

        score = (
            item["relevance_score"] * weights["relevance"] +
            item["credibility_score"] * weights["credibility"] +
            item["recency_score"] * weights["recency"] +
            item["completeness_score"] * weights["completeness"]
        )

        return round(score, 2)

    def extract_key_insights(self, data: List[Dict]) -> List[str]:
        """從收集的資料中提取關鍵洞察"""
        insights = []

        for item in data:
            summary = item.get("summary", "")
            if len(summary) > 50:
                insights.append(summary)

        return insights[:5]  # 返回前 5 個

    def collect(self, topic: str, sources: str = "web_search,web_reader",
                max_results: int = 20, deep_research: bool = False) -> Dict:
        """收集所有資料來源 - 改進版"""

        source_list = [s.strip() for s in sources.split(",")]
        all_data = []
        urls_to_read = []

        print("\n" + "="*60)
        print("📚 開始資料收集")
        print("="*60 + "\n")

        # 階段 1: 網路搜尋
        if "web_search" in source_list:
            search_results = self.collect_from_web_search(topic, max_results)
            all_data.extend(search_results)

            # 收集 URL 用於深入閱讀
            if deep_research and "web_reader" in source_list:
                urls_to_read = [item["url"] for item in search_results[:5] if item.get("url")]

        # 階段 2: 深入閱讀網頁內容
        if deep_research and urls_to_read and "web_reader" in source_list:
            print("\n📖 深入閱讀網頁內容...")
            reader_results = self.collect_from_web_reader(urls_to_read)
            all_data.extend(reader_results)

        # 階段 3: 資料庫查詢
        if "database" in source_list:
            db_results = self.collect_from_database(topic, max_results)
            all_data.extend(db_results)

        # 計算質量分數並過濾
        scored_data = []
        for item in all_data:
            quality_score = self.calculate_quality_score(item)
            item["quality_score"] = quality_score

            if quality_score >= self.min_score:
                scored_data.append(item)

        # 按分數排序
        scored_data.sort(key=lambda x: x["quality_score"], reverse=True)

        self.collected_data = scored_data

        # 提取關鍵洞察
        key_insights = self.extract_key_insights(scored_data)

        print("\n" + "="*60)
        print("✅ 資料收集完成")
        print("="*60)

        return {
            "topic": topic,
            "total_items": len(scored_data),
            "min_quality_score": self.min_score,
            "data": scored_data,
            "key_insights": key_insights,
            "sources_used": source_list,
            "deep_research": deep_research
        }

    def save_to_file(self, research_data: Dict, filepath: str):
        """保存收集的資料到文件"""
        output = {
            "collected_at": datetime.now().isoformat(),
            **research_data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ 資料已保存到: {filepath}")

    def print_summary(self, research_data: Dict):
        """打印收集摘要"""
        print(f"\n📊 收集摘要:")
        print(f"   主題: {research_data['topic']}")
        print(f"   總共收集: {research_data['total_items']} 項")
        print(f"   最低分數: {research_data['min_quality_score']}")
        print(f"   使用來源: {', '.join(research_data['sources_used'])}")
        print(f"   深度研究: {'是' if research_data['deep_research'] else '否'}")

        if research_data['total_items'] > 0:
            avg_score = sum(d["quality_score"] for d in research_data["data"]) / len(research_data["data"])
            print(f"   平均分數: {avg_score:.2f}")

            print(f"\n📌 頂級資料來源:")
            for i, item in enumerate(research_data["data"][:5], 1):
                print(f"   {i}. [{item['source_type']}] {item['title'][:60]}...")
                print(f"      分數: {item['quality_score']:.2f}")
                if item.get('url'):
                    print(f"      連結: {item['url']}")

        if research_data.get('key_insights'):
            print(f"\n💡 關鍵洞察:")
            for i, insight in enumerate(research_data['key_insights'][:3], 1):
                print(f"   {i}. {insight[:100]}...")


def main():
    parser = argparse.ArgumentParser(
        description="收集研究資料並評分（整合 MCP）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 基礎搜尋
  python3 collect.py --topic "Moltbot" --sources web_search

  # 深度研究（搜尋 + 讀取網頁）
  python3 collect.py --topic "Moltbot" --sources web_search,web_reader --deep-research

  # 包含資料庫
  python3 collect.py --topic "AI工具" --sources web_search,web_reader,database
        """
    )
    parser.add_argument("--topic", required=True, help="研究主題")
    parser.add_argument("--sources", default="web_search",
                       help="資料來源（web_search, web_reader, database）")
    parser.add_argument("--max-results", type=int, default=20,
                       help="最大結果數量")
    parser.add_argument("--min-score", type=float, default=0.6,
                       help="最小質量分數 (0-1)")
    parser.add_argument("--deep-research", action="store_true",
                       help="深度研究：讀取網頁完整內容")
    parser.add_argument("--output", default="research_data.json",
                       help="輸出檔案路徑")

    args = parser.parse_args()

    # 創建收集器
    collector = ResearchCollector(min_score=args.min_score)

    # 收集資料
    research_data = collector.collect(
        topic=args.topic,
        sources=args.sources,
        max_results=args.max_results,
        deep_research=args.deep_research
    )

    # 打印摘要
    collector.print_summary(research_data)

    # 保存到文件
    collector.save_to_file(research_data, args.output)


if __name__ == "__main__":
    main()
