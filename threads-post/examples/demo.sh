#!/bin/bash
# Threads 發文範例腳本
# 示範如何使用 threads-post 技能發布貼文

CHANNEL_ID=1

echo "=================================="
echo "Threads 發文範例"
echo "=================================="

# 範例 1：取得 Instagram Business ID
echo ""
echo "範例 1：取得 Instagram Business ID"
echo "-----------------------------------"
python3 ../../scripts/post.py \
  --action get-ig-id \
  --from-db \
  --channel-id $CHANNEL_ID

echo ""
echo "✅ 記下你的 Instagram Business ID，稍後會用到"
read -p "按 Enter 繼續..."

# 範例 2：發布純文字
echo ""
echo "範例 2：發布純文字貼文"
echo "-----------------------------------"
python3 ../../scripts/post.py \
  --action text \
  --from-db \
  --channel-id $CHANNEL_ID \
  --text "這是我的第一條 Threads 貼文！🧵

與社群分享想法...

#Threads #HelloWorld"

echo ""
echo "✅ 檢查 Threads 是否發布成功"
read -p "按 Enter 繼續..."

# 範例 3：發布圖片
echo ""
echo "範例 3：發布圖片貼文"
echo "-----------------------------------"
# 使用之前生成的 iPhone 圖片作為範例
python3 ../../scripts/post.py \
  --action image \
  --from-db \
  --channel-id $CHANNEL_ID \
  --text "iPhone 18 Pro + Starlink 深山海邊都秒連線！📱

#iPhone18Pro #Starlink #科技新聞" \
  --image-url "https://i.pix2.io/5m6gGTpt.png"

echo ""
echo "✅ 檢查 Threads 是否發布成功"
read -p "按 Enter 繼續..."

# 範例 4：發布影片（如果你有影片 URL）
echo ""
echo "範例 4：發布影片"
echo "-----------------------------------"
echo "python3 ../../scripts/post.py \\"
echo "  --action video \\"
echo "  --from-db \\"
echo "  --channel-id $CHANNEL_ID \\"
echo "  --text \\\"影片標題\\\" \\"
echo "  --video-url \\\"https://example.com/video.mp4\\\""
echo ""
echo "💡 提示：影片需要時間處理，請耐心等待"

echo ""
echo "=================================="
echo "範例演示完成！"
echo "=================================="
