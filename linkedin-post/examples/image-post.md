# LinkedIn 圖片貼文範例

## 基本範例

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "Behind the scenes at our office! 📸" \
  --image-url "https://i.pix2.io/office.jpg"
```

## 與 pix2-upload 整合

```bash
# 1. 上傳圖片到 Pix2
IMAGE_URL=$(python3 .claude/skills/pix2-upload/scripts/upload.py photo.jpg)

# 2. 發布到 LinkedIn
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "Team building day was a huge success! 🎉" \
  --image-url "$IMAGE_URL"
```

## 產品展示範例

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "Introducing our latest product innovation! 🚀

After months of R&D, we're proud to unveil something that will change the way you work.

Key features:
✨ Enhanced productivity
🔒 Enterprise-grade security
📱 Cross-platform support

#ProductLaunch #Innovation #Tech #Productivity" \
  --image-url "https://i.pix2.io/product.jpg"
```

## 活動記錄範例

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "Great networking at today's industry conference! 🤝

It's always inspiring to connect with fellow professionals and share ideas about the future of our industry.

Key takeaways:
1. AI is transforming how we work
2. Collaboration drives innovation
3. Continuous learning is essential

#Networking #Conference #ProfessionalDevelopment #IndustryInsights" \
  --image-url "https://i.pix2.io/conference.jpg"
```

## 圖片限制

| 項目 | 限制 |
|------|------|
| 檔案大小 | 最大 5MB |
| 圖片格式 | JPG, PNG, GIF |
| 數量 | 單張圖片（LinkedIn 不支援多圖） |

## 發布流程

1. **註冊上傳** → 取得 upload URL 和 asset URN
2. **上傳圖片** → 上傳二進制數據
3. **發布貼文** → 包含 asset URN

## 圖片建議

1. **尺寸**: 1200x627px (最適合)
2. **比例**: 1.91:1
3. **格式**: JPG 或 PNG
4. **內容**: 專業、清晰、高品質
5. **文字**: 圖片中的文字要大且清晰

## 常見問題

### Q: 為什麼圖片上傳很慢？

A: LinkedIn 需要三個步驟：
1. 註冊上傳
2. 實際上傳（可能需要 10-30 秒）
3. 發布貼文

### Q: 圖片格式錯誤怎麼辦？

A: 確保：
- URL 是公開可訪問的
- 圖片小於 5MB
- 格式是 JPG/PNG/GIF

### Q: 可以發布多張圖片嗎？

A: LinkedIn API 目前不支援多圖 Carousel，只能發布單張圖片。
