#!/usr/bin/env python3
"""
YouTube Shorts Revenue Estimator - Python 腳本
預估 YouTube Shorts 的收入
"""

import sys
import os
import requests

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

def estimate_revenue(views, region='tw', use='avg'):
    """
    預估收入

    Args:
        views: 觀看次數
        region: 地區代碼（預設 tw）
        use: 使用哪個 RPM 值（min, max, avg）

    Returns:
        預估收入（美元）
    """
    if region not in RPM_DATA:
        region = 'tw'

    rpm = RPM_DATA[region][use]
    revenue = (views / 1000) * rpm

    return revenue

def estimate_revenue_range(views, region='tw'):
    """
    預估收入範圍

    Args:
        views: 觀看次數
        region: 地區代碼（預設 tw）

    Returns:
        (最小收入, 平均收入, 最大收入)
    """
    if region not in RPM_DATA:
        region = 'tw'

    region_data = RPM_DATA[region]
    min_revenue = (views / 1000) * region_data['min']
    avg_revenue = (views / 1000) * region_data['avg']
    max_revenue = (views / 1000) * region_data['max']

    return min_revenue, avg_revenue, max_revenue

def batch_estimate(videos):
    """
    批量預估多個視頻

    Args:
        videos: 視頻列表，每個元素包含 views 和 region

    Returns:
        預估結果列表
    """
    results = []
    for video in videos:
        views = video.get('views', 0)
        region = video.get('region', 'tw')

        min_rev, avg_rev, max_rev = estimate_revenue_range(views, region)

        results.append({
            'views': views,
            'region': region,
            'region_name': RPM_DATA[region]['name'],
            'min_revenue': min_rev,
            'avg_revenue': avg_rev,
            'max_revenue': max_rev
        })

    return results

def get_channel_revenue(channel_id, period_days=30):
    """
    使用 YouTube API 獲取頻道收入預估

    Args:
        channel_id: 頻道 ID
        period_days: 統計週期（天數）

    Returns:
        總收入預估
    """
    api_key = os.environ.get('YOUTUBE_API_KEY')

    if not api_key:
        print("錯誤: 請設定 YOUTUBE_API_KEY 環境變數")
        return None

    base_url = "https://www.googleapis.com/youtube/v3"

    try:
        # 獲取頻道的視頻列表
        search_url = f"{base_url}/search"
        params = {
            'key': api_key,
            'channelId': channel_id,
            'part': 'snippet',
            'maxResults': 50,
            'order': 'date',
            'type': 'video'
        }

        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'items' not in data:
            print("錯誤: 無法找到頻道視頻")
            return None

        video_ids = [item['id']['videoId'] for item in data['items']]

        # 獲取視頻統計數據
        videos_url = f"{base_url}/videos"
        params = {
            'key': api_key,
            'id': ','.join(video_ids),
            'part': 'statistics'
        }

        response = requests.get(videos_url, params=params)
        response.raise_for_status()
        data = response.json()

        total_views = 0
        if 'items' in data:
            for video in data['items']:
                view_count = int(video['statistics'].get('viewCount', 0))
                total_views += view_count

        # 使用平均 RPM 預估收入（假設為台灣）
        total_revenue = (total_views / 1000) * RPM_DATA['tw']['avg']

        return total_revenue

    except requests.exceptions.RequestException as e:
        print(f"API 請求失敗: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 estimate.py [選項]")
        print("\n選項：")
        print("  --views <數字>         觀看次數")
        print("  --region <代碼>        地區代碼（us, tw, uk, ca, au, jp, de, fr, other）")
        print("  --channel <頻道ID>      頻道 ID（需要 YOUTUBE_API_KEY）")
        print("  --period <天數>          統計週期（預設 30）")
        print("  --batch <JSON>          批量預估（JSON 格式）")
        print("\n範例：")
        print('  python3 estimate.py --views 100000 --region tw')
        print('  python3 estimate.py --views 1000000 --region us')
        print('  python3 estimate.py --channel UCXXXXXXXXXXXXX --period 30')
        print('  python3 estimate.py --batch \'[{"views":50000,"region":"tw"},{"views":100000,"region":"us"}]\'')
        sys.exit(1)

    # 解析參數
    views = None
    region = 'tw'
    channel_id = None
    period_days = 30
    batch_data = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == '--views' and i + 1 < len(sys.argv):
            views = int(sys.argv[i + 1])
            i += 2
        elif arg == '--region' and i + 1 < len(sys.argv):
            region = sys.argv[i + 1].lower()
            i += 2
        elif arg == '--channel' and i + 1 < len(sys.argv):
            channel_id = sys.argv[i + 1]
            i += 2
        elif arg == '--period' and i + 1 < len(sys.argv):
            period_days = int(sys.argv[i + 1])
            i += 2
        elif arg == '--batch' and i + 1 < len(sys.argv):
            import json
            batch_data = json.loads(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    # 執行預估
    if batch_data:
        # 批量預估
        print(f"\n批量預估 {len(batch_data)} 個視頻:")
        print(f"{'='*80}")

        results = batch_estimate(batch_data)

        total_min = 0
        total_avg = 0
        total_max = 0

        for result in results:
            print(f"\n{result['views']:,} 觀看 ({result['region_name']})")
            print(f"  最小收入: ${result['min_revenue']:.2f}")
            print(f"  平均收入: ${result['avg_revenue']:.2f}")
            print(f"  最大收入: ${result['max_revenue']:.2f}")

            total_min += result['min_revenue']
            total_avg += result['avg_revenue']
            total_max += result['max_revenue']

        print(f"\n{'='*80}")
        print(f"總計:")
        print(f"  最小收入: ${total_min:.2f}")
        print(f"  平均收入: ${total_avg:.2f}")
        print(f"  最大收入: ${total_max:.2f}")

    elif channel_id:
        # 頻道預估
        print(f"\n獲取頻道 {channel_id} 的收入預估（過去 {period_days} 天）")
        print(f"{'='*80}")

        total_revenue = get_channel_revenue(channel_id, period_days)

        if total_revenue is not None:
            print(f"預估總收入: ${total_revenue:.2f}")
        else:
            print("無法獲取頻道收入預估")

    elif views:
        # 單一視頻預估
        min_rev, avg_rev, max_rev = estimate_revenue_range(views, region)

        print(f"\nYouTube Shorts 收入預估:")
        print(f"{'='*80}")
        print(f"觀看次數: {views:,}")
        print(f"地區: {RPM_DATA[region]['name']} ({region})")
        print(f"RPM 範圍: ${RPM_DATA[region]['min']:.3f} - ${RPM_DATA[region]['max']:.3f}")
        print(f"\n預估收入:")
        print(f"  最小收入: ${min_rev:.2f}")
        print(f"  平均收入: ${avg_rev:.2f}")
        print(f"  最大收入: ${max_rev:.2f}")
        print(f"\n說明: 實際收入可能因觀眾年齡、內容類型等因素而有所不同")

    else:
        print("錯誤: 請指定 --views 或 --channel")
        sys.exit(1)

if __name__ == "__main__":
    main()
