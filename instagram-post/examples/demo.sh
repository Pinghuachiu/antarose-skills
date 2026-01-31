#!/bin/bash
# Instagram 發文範例腳本
# 示範如何使用 instagram-post 技能發布貼文

CHANNEL_ID=1

echo "=================================="
echo "Instagram 發文範例"
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

# 範例 2：發布單張圖片
echo ""
echo "範例 2：發布單張圖片"
echo "-----------------------------------"
# 使用之前生成的 iPhone 圖片作為範例
python3 ../../scripts/post.py \
  --action photo \
  --from-db \
  --channel-id $CHANNEL_ID \
  --caption "📱 iPhone 18 Pro + Starlink

深山海邊都秒連線！

#iPhone18Pro #Starlink #科技新聞" \
  --image-url "https://i.pix2.io/5m6gGTpt.png"

echo ""
echo "✅ 檢查 Instagram 是否發布成功"
read -p "按 Enter 繼續..."

# 範例 3：發布影片（如果你有影片 URL）
echo ""
echo "範例 3：發布影片"
echo "-----------------------------------"
echo "python3 ../../scripts/post.py \\"
echo "  --action video \\"
echo "  --from-db \\"
echo "  --channel-id $CHANNEL_ID \\"
echo "  --caption \"影片標題\" \\"
echo "  --video-url \"https://example.com/video.mp4\""
echo ""
echo "💡 提示：影片需要時間處理，請耐心等待"

# 範例 4：發布 Carousel（多張圖片）
echo ""
echo "範例 4：發布 Carousel"
echo "-----------------------------------"
echo "python3 ../../scripts/post.py \\"
echo "  --action carousel \\"
echo "  --from-db \\"
echo "  --channel-id $CHANNEL_ID \\"
echo "  --caption \"多張圖片展示\" \\"
echo "  --image-urls \"url1,url2,url3\""
echo ""
echo "💡 提示：Carousel 需要 2-10 張圖片"

echo ""
echo "=================================="
echo "範例演示完成！"
echo "=================================="
