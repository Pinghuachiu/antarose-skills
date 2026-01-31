# LinkedIn 連結貼文範例

## 基本範例

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action link \
  --from-db \
  --channel-id 1 \
  --text "Check out this amazing article!" \
  --link-url "https://example.com/article"
```

## 完整連結貼文（含標題和描述）

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action link \
  --from-db \
  --channel-id 1 \
  --text "Just published a deep dive on the future of AI in enterprise! 🤖

This article explores how AI is reshaping business operations and what leaders need to know to stay ahead.

Key topics covered:
• Machine Learning applications
• Ethical AI implementation
• ROI measurement
• Change management" \
  --link-url "https://blog.example.com/ai-enterprise-future" \
  --link-title "The Future of AI in Enterprise: A 2025 Perspective" \
  --link-desc "Explore how artificial intelligence is transforming business operations and discover strategies for successful AI adoption in your organization."
```

## 博客分享範例

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action link \
  --from-db \
  --channel-id 1 \
  --text "New blog post: 5 Common Mistakes When Scaling Your Team 📈

After working with dozens of startups, I've identified these recurring pitfalls that can derail growth.

Link in the comments below! 👇

#Startup #Leadership #TeamBuilding #Growth #Management" \
  --link-url "https://yourblog.com/scaling-team-mistakes" \
  --link-title "5 Common Mistakes When Scaling Your Team (And How to Avoid Them)" \
  --link-desc "Learn from real-world examples of companies that scaled successfully (and those that didn't). Practical advice for startup founders and team leaders."
```

## 新聞分享範例

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action link \
  --from-db \
  --channel-id 1 \
  --text "Interesting development in the tech industry today:

Major acquisition announced that will reshape the cloud computing landscape.

This move signals a broader trend toward consolidation in the sector. What are your thoughts on the impact?

#TechNews #CloudComputing #BusinessStrategy #MergersAndAcquisitions" \
  --link-url "https://news.example.com/tech-acquisition-2025" \
  --link-title "Tech Giant Acquires Cloud Startup for $5B" \
  --link-desc "In one of the largest deals of the year, Tech Giant has acquired Cloud Startup, marking a significant shift in the cloud computing market."
```

## 產品發布範例

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action link \
  --from-db \
  --channel-id 1 \
  --text "🚀 We're live! Announcing our biggest product release of the year.

After months of hard work, our team is thrilled to introduce features that will transform how you work.

Learn more about what's new:

#ProductLaunch #Innovation #Tech #SaaS #ProductManagement" \
  --link-url "https://yourproduct.com/launch-2025" \
  --link-title "Introducing Product Name 2.0: The Future of Work" \
  --link-desc "Discover powerful new features designed to boost productivity, streamline workflows, and help teams collaborate more effectively."
```

## Open Graph 優化

為了讓連結預覽更吸引人，確保目標網站有正確的 Open Graph tags：

```html
<meta property="og:title" content="Your Article Title">
<meta property="og:description" content="A compelling description of your content">
<meta property="og:image" content="https://example.com/preview-image.jpg">
<meta property="og:url" content="https://example.com/article">
<meta property="og:type" content="article">
```

## 連結貼文建議

1. **吸引力標題**: 使用 --link-title 參數
2. **描述**: 使用 --link-desc 參數（可選）
3. **Call to Action**: 在 text 中加入「閱讀更多」等
4. **Hashtags**: 放在 text 中，不在連結標題
5. **預覽圖片**: 確保目標網站有 og:image

## 連結預覽

LinkedIn 會自動抓取：
- ✅ 標題（從頁面標題或 og:title）
- ✅ 描述（從 meta description 或 og:description）
- ✅ 預覽圖片（從 og:image）

**注意**: LinkedIn 會快取預覽，如果更新了 Open Graph tags，可能需要等待才能看到變更。

## 常見問題

### Q: 連結預覽不顯示？

A: 可能原因：
- 目標網站沒有 Open Graph tags
- 網站阻止 LinkedIn 爬蟲
- LinkedIn 還在快取舊資料

### Q: 可以自定義預覽圖片嗎？

A: 不能直接自定義，必須在目標網站設置 `og:image` meta tag。

### Q: 連結貼文的互動率如何？

A: 一般來說：
- 圖片貼文 > 連結貼文 > 純文字
- 但連結貼文適合引流到網站
- 建議混合使用不同類型
