---
name: youtube-shorts-revenue
description: 使用 Python 和 Node.js 腳本預估 YouTube Shorts 的收入，基於觀看次數和地區 RPM
metadata:
  category: analytics
  type: youtube
  languages:
    - python
    - javascript
    - bash
  supports:
    - revenue-estimation
    - multi-region
    - historical-analysis
---

# YouTube Shorts Revenue - 收入預估技能

使用 Python 和 Node.js 腳本預估 YouTube Shorts 的收入，基於觀看次數和地區 RPM（Revenue Per Mille）。

## 功能特性

- 基於觀看次數預估收入
- 支援多個地區的 RPM 設定
- 歷史數據分析
- 視頻頻道總收入計算

## YouTube Shorts RPM 參考數據

根據行業平均數據，YouTube Shorts 的 RPM 通常遠低於長視頻：

| 地區 | RPM 範圍（每千次觀看） | 平均值 |
|------|----------------------|--------|
| 美國 | $0.01 - $0.06 | $0.03 |
| 台灣 | $0.005 - $0.03 | $0.015 |
| 英國 | $0.01 - $0.05 | $0.025 |
| 加拿大 | $0.01 - $0.05 | $0.025 |
| 澳洲 | $0.01 - $0.05 | $0.025 |
| 日本 | $0.008 - $0.04 | $0.02 |
| 德國 | $0.01 - $0.05 | $0.025 |
| 法國 | $0.01 - $0.05 | $0.025 |
| 其他 | $0.005 - $0.03 | $0.015 |

**注意：** 這些數據是行業平均值，實際收入會因以下因素而有很大差異：
- 觀眾年齡層
- 觀眾地理位置
- 主題內容類型
- 廣告填充率
- 留存率和互動率

## 環境變數

使用前請設定以下環境變數：

```bash
export YOUTUBE_API_KEY="your-youtube-api-key"
export YOUTUBE_CHANNEL_ID="your-channel-id"
```

請參考 [resource.md](../../../resource.md) 獲取 API Key。

## 快速開始

### Python 腳本

```bash
# 單一視頻預估
python3 skills/youtube-shorts-revenue/scripts/estimate.py --views 100000 --region tw

# 頻道總收入預估（需要 API Key）
python3 skills/youtube-shorts-revenue/scripts/estimate.py --channel UCXXXXXXXXXXXXXX --period 30

# 反向計算：從目標收入計算播放量
python3 skills/youtube-shorts-revenue/scripts/reverse.py 1000
```

### Node.js 腳本

```bash
# 單一視頻預估
node skills/youtube-shorts-revenue/scripts/estimate.js --views 100000 --region tw

# 頻道總收入預估（需要 API Key）
node skills/youtube-shorts-revenue/scripts/estimate.js --channel UCXXXXXXXXXXXXXX --period 30
```

## 腳本說明

### 預估腳本 (estimate.py / estimate.js)

預估 YouTube Shorts 收入。

**參數：**
- `--views`: 觀看次數（必需，未指定頻道時）
- `--region`: 地區代碼（可選，預設 tw）
- `--channel`: 頻道 ID（可選，需要 API Key）
- `--period`: 統計週期（天數，預設 30）

**支援的地區代碼：**
- `us` - 美國
- `tw` - 台灣
- `uk` - 英國
- `ca` - 加拿大
- `au` - 澳洲
- `jp` - 日本
- `de` - 德國
- `fr` - 法國
- `other` - 其他地區

**範例：**
```bash
# 10 萬次觀看，台灣地區
python3 skills/youtube-shorts-revenue/scripts/estimate.py --views 100000 --region tw

# 100 萬次觀看，美國地區
python3 skills/youtube-shorts-revenue/scripts/estimate.py --views 1000000 --region us

# 頻道過去 30 天總收入
python3 skills/youtube-shorts-revenue/scripts/estimate.py --channel UCXXXXXXXXXXXXXX --period 30
```

### 反向計算腳本 (reverse.py)

從目標收入反向計算需要的播放量。

**參數：**
- `收入`: 目標收入（必需，美元）
- `--region`: 地區代碼（可選，預設 tw）
- `--per-short`: 每個 Short 平均播放量（可選，預設 10000）

**範例：**
```bash
# 計算每月賺 $1000 需要多少播放量（台灣地區）
python3 skills/youtube-shorts-revenue/scripts/reverse.py 1000

# 計算每月賺 $1000 需要多少播放量（美國地區）
python3 skills/youtube-shorts-revenue/scripts/reverse.py 1000 --region us

# 計算每月賺 $1000 需要多少播放量（每個 Short 平均 5000 播放）
python3 skills/youtube-shorts-revenue/scripts/reverse.py 1000 --per-short 5000
```

## Python 程式碼範例

### 基本預估

```python
from scripts.estimate import estimate_revenue

# 預估 10 萬次觀看的收入
views = 100000
region = "tw"
revenue = estimate_revenue(views, region)
print(f"預估收入: ${revenue:.2f}")
```

### 批量預估

```python
from scripts.estimate import batch_estimate

# 批量預估多個視頻
videos = [
    {"views": 50000, "region": "tw"},
    {"views": 100000, "region": "us"},
    {"views": 75000, "region": "jp"}
]

results = batch_estimate(videos)
for video, revenue in results:
    print(f"{video['views']} 觀看 ({video['region']}): ${revenue:.2f}")
```

### 使用 YouTube API

```python
from scripts.estimate import get_channel_revenue

# 獲取頻道收入（需要 API Key）
channel_id = "UCXXXXXXXXXXXXXX"
period_days = 30
revenue = get_channel_revenue(channel_id, period_days)

print(f"過去 {period_days} 天預估收入: ${revenue:.2f}")
```

## Node.js 程式碼範例

### 基本預估

```javascript
const { estimateRevenue } = require('./estimate.js');

// 預估 10 萬次觀看的收入
const views = 100000;
const region = 'tw';
const revenue = estimateRevenue(views, region);

console.log(`預估收入: $${revenue.toFixed(2)}`);
```

### 批量預估

```javascript
const { batchEstimate } = require('./estimate.js');

// 批量預估多個視頻
const videos = [
  { views: 50000, region: 'tw' },
  { views: 100000, region: 'us' },
  { views: 75000, region: 'jp' }
];

const results = batchEstimate(videos);
results.forEach(result => {
  console.log(`${result.views} 觀看 (${result.region}): $${result.revenue.toFixed(2)}`);
});
```

## 常用公式

### 收入計算公式

```python
收入 = (觀看次數 / 1000) × RPM
```

**範例：**
- 觀看次數：100,000
- 地區：台灣（RPM = $0.015）
- 收入 = (100,000 / 1,000) × $0.015 = $1.50

### 反向計算公式（從收入計算播放量）

```python
播放量 = (目標收入 / RPM) × 1000
```

**範例：**
- 目標收入：$1,000
- 地區：台灣（平均 RPM = $0.015）
- 播放量 = ($1,000 / $0.015) × 1,000 = 66,666,667 次

### 需要的 Shorts 數量計算

```python
每月需要的 Shorts = 平均總播放量 / 每個 Short 平均播放量
每天需要的 Shorts = 每月需要的 Shorts / 30
```

**範例：**
- 平均總播放量：66,666,667 次
- 每個 Short 平均播放：10,000 次
- 每月需要的 Shorts = 66,666,667 / 10,000 = 6,667 個
- 每天需要的 Shorts = 6,667 / 30 ≈ 222 個

### 批量計算

```python
總收入 = Σ(視頻_i_收入)
```

**範例：**
- 視頻 1: 50,000 觀看，tw → $0.75
- 視頻 2: 100,000 觀看，us → $3.00
- 視頻 3: 75,000 觀看，jp → $1.50
- 總收入 = $0.75 + $3.00 + $1.50 = $5.25
```

## 注意事項

1. **RPM 差異**: YouTube Shorts 的 RPM 通常比長視頻低 5-10 倍
2. **API 限制**: YouTube Data API 有每日請求配額限制
3. **準確性**: 這只是預估，實際收入會有差異
4. **貨幣**: 收入以美元（USD）計算，實際支付時可能轉換為本地貨幣
5. **付款週期**: YouTube 通常在每月 21-26 日發放上月收入

## 依賴套件

### Python

```bash
pip install requests
```

### Node.js

```bash
npm install axios
```

## 最佳實踐

1. **設定合理的預期**: YouTube Shorts 收入通常較低，不要過度期待
2. **持續創作**: 數量和質量同樣重要
3. **優化內容**: 提高觀看時長和互動率可以提升 RPM
4. **多平台分發**: 可以將 Shorts 同步到其他平台增加曝光
5. **分析數據**: 定期分析哪些類型的內容表現最好

## 常見問題

### Q: 為什麼 Shorts 收入比長視頻低？
A: 因為 Shorts 時間短，廣告插入機會少，且觀眾跳躍率較高。

### Q: 如何提高 RPM？
A: 提升內容質量、目標高價值觀眾、增加視頻時長（到 60 秒）、提高互動率。

### Q: 需要多少觀看才能賺到 $100？
A: 假設台灣 RPM $0.015，需要約 6,666,667 次觀看。

### Q: 每月賺 $1000 需要多少播放量？
A: 假設台灣平均 RPM $0.015，需要約 66,666,667 次播放，如果每個 Short 平均有 10,000 次播放，需要每月發布約 6,667 個 Shorts。

### Q: 每天需要發布多少個 Shorts？
A: 取決於你的目標收入和每個 Short 的平均播放量。使用反向計算腳本可以快速計算：`python3 scripts/reverse.py 1000`

### Q: 影響收入的因素有哪些？
A: 觀眾地區、年齡、內容類型、廣告填充率、季節性因素等。

## API 使用說明

### YouTube Data API

本技能使用 YouTube Data API v3 來獲取頻道和視頻數據。

**主要端點：**
- `GET /youtube/v3/channels` - 獲取頻道資訊
- `GET /youtube/v3/search` - 搜索視頻
- `GET /youtube/v3/videos` - 獲取視頻統計數據

**認證方式：**
- API Key（通過 `key` 查詢參數）

**配額限制：**
- 每日 10,000 單位

**詳細文檔：**
https://developers.google.com/youtube/v3
