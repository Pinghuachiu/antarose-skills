#!/usr/bin/env python3
"""
YouTube Shorts Revenue Calculator - 反向計算腳本
從目標收入計算所需的播放量
"""

import sys

# YouTube Shorts RPM 參考數據（每千次觀看收入）
RPM_DATA = {
    'us': {'min': 0.01, 'max': 0.06, 'avg': 0.03, 'name': '美國'},
    'tw': {'min': 0.005, 'max': 0.03, 'avg': 0.015, 'name': '台灣'},
    'uk': {'min': 0.01, 'max': 0.05, 'avg': 0.025, 'name': '英國'},
    'ca': {'min': 0.01, 'max': 0.05, 'avg': 0.025, 'name': '加拿大'},
    'au': {'min': 0.01, 'max': 0.05, 'avg': 0.025, 'name': '澳洲'},
    'jp': {'min': 0.008, 'max': 0.04, 'avg': 0.02, 'name': '日本'},
    'de': {'min': 0.01, 'max': 0.05, 'avg': 0.025, 'name': '德國'},
    'fr': {'min': 0.01, 'max': 0.05, 'avg': 0.025, 'name': '法國'},
    'other': {'min': 0.005, 'max': 0.03, 'avg': 0.015, 'name': '其他地區'}
}

def calculate_views_for_revenue(target_revenue, region='tw'):
    """
    計算達到目標收入所需的播放量

    Args:
        target_revenue: 目標收入（美元）
        region: 地區代碼

    Returns:
        (最小播放量, 平均播放量, 最大播放量)
    """
    if region not in RPM_DATA:
        region = 'tw'

    region_data = RPM_DATA[region]

    # 播放量 = (目標收入 / RPM) * 1000
    min_views = (target_revenue / region_data['min']) * 1000
    avg_views = (target_revenue / region_data['avg']) * 1000
    max_views = (target_revenue / region_data['max']) * 1000

    return min_views, avg_views, max_views

def calculate_shorts_needed(avg_views, avg_views_per_short=10000):
    """
    計算需要發布的 Shorts 數量

    Args:
        avg_views: 平均總播放量
        avg_views_per_short: 每個 Short 平均播放量

    Returns:
        (每月需要, 每天需要)
    """
    monthly_shorts = avg_views / avg_views_per_short
    daily_shorts = monthly_shorts / 30

    return monthly_shorts, daily_shorts

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 reverse.py <收入> [選項]")
        print("\n選項：")
        print("  --region <代碼>        地區代碼（預設 tw）")
        print("  --per-short <數字>     每個 Short 平均播放量（預設 10000）")
        print("\n範例：")
        print('  python3 reverse.py 1000')
        print('  python3 reverse.py 1000 --region us')
        print('  python3 reverse.py 1000 --region tw --per-short 5000')
        sys.exit(1)

    # 解析參數
    try:
        target_revenue = float(sys.argv[1])
    except ValueError:
        print("錯誤: 收入必須是數字")
        sys.exit(1)

    region = 'tw'
    avg_views_per_short = 10000

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == '--region' and i + 1 < len(sys.argv):
            region = sys.argv[i + 1].lower()
            i += 2
        elif arg == '--per-short' and i + 1 < len(sys.argv):
            avg_views_per_short = float(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    # 驗證地區
    if region not in RPM_DATA:
        print(f"警告: 不支援的地區代碼 '{region}'，使用預設 'tw'")
        region = 'tw'

    # 計算播放量
    min_views, avg_views, max_views = calculate_views_for_revenue(target_revenue, region)

    # 計算需要的 Shorts 數量
    monthly_shorts, daily_shorts = calculate_shorts_needed(avg_views, avg_views_per_short)

    # 顯示結果
    print(f"\n{'='*80}")
    print(f"每月賺取 ${target_revenue:.2f} 美金所需的播放量")
    print(f"{'='*80}\n")

    print(f"目標收入: ${target_revenue:.2f}")
    print(f"目標地區: {RPM_DATA[region]['name']} ({region})")
    print(f"每 Short 平均播放: {avg_views_per_short:,.0f}")
    print(f"\n地區 RPM 範圍: ${RPM_DATA[region]['min']:.3f} - ${RPM_DATA[region]['max']:.3f} (平均 ${RPM_DATA[region]['avg']:.3f})")

    print(f"\n{'='*80}")
    print("所需的播放量：")
    print(f"{'='*80}\n")

    print(f"  最小播放量: {min_views:,.0f} 次 (RPM ${RPM_DATA[region]['min']:.3f})")
    print(f"  平均播放量: {avg_views:,.0f} 次 (RPM ${RPM_DATA[region]['avg']:.3f})")
    print(f"  最大播放量: {max_views:,.0f} 次 (RPM ${RPM_DATA[region]['max']:.3f})")

    print(f"\n{'='*80}")
    print("需要發布的 Shorts 數量（基於平均播放量）：")
    print(f"{'='*80}\n")

    print(f"  每月需要: {monthly_shorts:,.0f} 個 Shorts")
    print(f"  每天需要: {daily_shorts:,.1f} 個 Shorts")

    # 計算每個 Short 的收入
    revenue_per_short = target_revenue / monthly_shorts if monthly_shorts > 0 else 0

    print(f"\n  每個 Short 平均收入: ${revenue_per_short:.4f}")
    print(f"  每個 Short 平均創造: {avg_views_per_short:,.0f} 次播放")

    # 顯示其他地區對比
    print(f"\n{'='*80}")
    print("其他地區對比（平均播放量）：")
    print(f"{'='*80}\n")

    print(f"{'地區':<12} {'平均播放量':>20}")
    print(f"{'-'*80}")

    for region_code, region_data in RPM_DATA.items():
        avg_views_region = (target_revenue / region_data['avg']) * 1000
        monthly_shorts_region = avg_views_region / avg_views_per_short

        print(f"{region_data['name']:<12} {avg_views_region:>20,.0f}")

    print(f"\n{'-'*80}")
    print("\n說明：")
    print("  • 實際收入會因觀眾年齡、內容類型等因素而有所不同")
    print("  • RPM 數據基於行業平均值，實際數值可能更高或更低")
    print("  • 持續創作和優化內容有助於提高 RPM")

if __name__ == "__main__":
    main()
