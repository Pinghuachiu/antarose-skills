#!/bin/bash
# 糖果色電車 - 生成脚本
# Japanese City Pop / Acoustic R&B style

echo "=== 生成歌曲：糖果色電車 ==="
echo "風格：Japanese City Pop, Acoustic R&B, Sweet, Breezy"
echo ""

# 设置环境变量
export ALLAPI_BASE_URL="https://allapi.store/"
export ALLAPI_KEY="sk-eJtw92E4YJZrdF6bv0bjiIU4DAwo8nHC3XPZeQFRxwZ5i6mM"

# 执行生成
python3 .claude/skills/suno-music/scripts/generate.py \
  --mode custom \
  --title "糖果色電車 (Candy-Colored Tram)" \
  --tags "japanese city pop,acoustic R&B,melodic rap,male vocal,sweet,breezy,90s J-Pop,light percussion,piano,acoustic guitar,romantic" \
  --vocal-gender m \
  --model chirp-v4 \
  "Style: Japanese City Pop, Acoustic R&B, Melodic Rap, Male Vocal, Sweet, Breezy, 90s J-Pop influence, Light Percussion

歌詞標題：糖果色電車

[Intro]
輕快的鋼琴聲起，伴隨著清脆的單車鈴聲，輕柔的 Acoustic Guitar 掃弦

[Verse 1]
沿著湘南的海岸線 電車緩緩地走過
琥珀色的海浪 閃爍 像你眼底的煙火
自動販賣機 投下了 兩罐冰鎖的蘋果
你淺笑的酒窩 剛好 治癒了我的落魄

[Verse 2]
下北澤的小巷口 膠片相機在定格
午後的風 很暖 吹亂了 你的白色百褶
宇治抹茶的苦 加上 幾分告白的狂熱
這感覺 像一首歌 旋律 正在被你勾勒

[Pre-Chorus]
這種感覺 就像是 薄荷汽水 剛開瓶的味道
不需要 太多的 辭藻 只要 聽著心跳 亂跳

[Chorus]
想把整片藍天 裝進信封 寄到你的夢中
就像那隻 告白氣球 輕輕 飛過彩虹
不用香榭落葉 只要 漫步在 東京的晚風
你低頭說 願意 笑容 比櫻花 還要紅

[Verse 3]
手牽手 穿過 澀谷的人流
你的溫柔 早就 把我 徹底 帶走
不用 考慮 很久 只要 點點頭
我會 陪你 走到 下個 世紀末的 盡頭

[Chorus]
想把整片藍天 裝進信封 寄到你的夢中
就像那隻 告白氣球 輕輕 飛過彩虹
不用香榭落葉 只要 漫步在 東京的晚風
你低頭說 願意 笑容 比櫻花 還要紅

[Bridge]
禮物不必太貴重 只要 你的心動
這個夏天 的悸動 只有 你才懂

[Outro]
風 輕輕吹動 你 躲在我懷中
那隻氣球 飄到了 時空的 另一頭
Fade out with piano notes"

echo ""
echo "✓ 歌曲生成完成！"
echo ""
echo "如需下載音頻，保存任務 ID 後運行："
echo "  python3 .claude/skills/suno-music/scripts/download-wav.py <task-id>"
