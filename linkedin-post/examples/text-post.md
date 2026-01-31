# LinkedIn 純文字貼文範例

## 基本範例

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "Excited to share our latest project! 🚀

We've been working hard on this for months...

#Innovation #Tech #Leadership"
```

## 使用手動指定參數

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action text \
  --person-urn "urn:li:person:785XXXX" \
  --access-token "AQXXXXXXXXXXXXXXXXXXXXXX" \
  --text "Hello LinkedIn!"
```

## 專業貼文範例

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "Thrilled to announce that I've just completed my certification in Cloud Architecture! 🎓

This journey has been incredibly rewarding, and I'm excited to apply these new skills to drive innovation at work.

A big thank you to my team for their support throughout this process. Here's to continuous learning and growth! 🚀

#CloudComputing #AWS #ProfessionalDevelopment #Certification #TechLeadership"
```

## 限量貼文範例（中文）

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "很榮幸能參與這次的專案！

團隊的合作是這次成功的關鍵。我們花了三個月的時間，從概念到實作，終於推出了一個真正能解決問題的產品。

感謝所有參與的成員，你們的專業和投入讓這個專案變得特別。

#產品發布 #團隊合作 #創新 #職場成長"
```

## 文字限制

- 最多 **3,000 字符**
- 支援換行
- 支援 hashtags
- 建議使用 2-5 個 hashtags

## 最佳實踐

1. **開頭吸引人**: 前兩行最重要
2. **使用空行**: 提高可讀性
3. **Hashtags**: 放在文末，2-5 個
4. **提及他人**: 使用特殊格式（需要 URN）
5. **保持專業**: LinkedIn 是專業平台
