const fs = require('fs');

const ANTIGRAVITY_API_KEY = 'YOUR_ANTIGRAVITY_API_KEY';
const ALLAPI_KEY = 'YOUR_ALLAPI_KEY';

// 使用方式：直接調用 generateImage 函數，會自動優先使用 Antigravity，失敗時降級到 NanoBanana

async function generateImage({ prompt, size = '1024x1024', quality = 'standard', n = 1, images = [], forceProvider = null }) {
  /**
   * 智能生成圖片，優先使用 Antigravity，失敗時自動降級到 NanoBanana
   *
   * @param {Object} options
   * @param {string} options.prompt - 圖片描述
   * @param {string} options.size - 尺寸（WIDTHxHEIGHT 格式）
   * @param {string} options.quality - 品質（hd, medium, standard）
   * @param {number} options.n - 生成數量
   * @param {Array<string>} options.images - 參考圖路徑列表
   * @param {string} options.forceProvider - 強制使用提供者（antigravity, nanobanana）
   *
   * @returns {Object} 生成結果
   */
  // ... 實現代碼見 scripts/generate.js ...
}

// 使用範例

// 1. 基本用法 - 會自動選擇最佳的提供者
generateImage({
  prompt: '一只可爱的猫咪'
})
  .then(console.log);

// 2. 指定尺寸和品質
generateImage({
  prompt: '风景照片',
  size: '1920x1080',
  quality: 'hd'
})
  .then(console.log);

// 3. 批次生成
generateImage({
  prompt: '不同品种的猫咪',
  n: 5
})
  .then(console.log);

// 4. 使用參考圖
generateImage({
  prompt: '将这张照片改成动漫风格',
  images: ['/path/to/photo.jpg'],
  size: '1024x1024'
})
  .then(console.log);

// 5. 強制使用特定提供者
generateImage({
  prompt: '测试图片',
  size: '1280x720',
  quality: 'medium',
  forceProvider: 'nanobanana'  // 強制使用 NanoBanana
})
  .then(console.log);

// 6. 圖生圖 - 自動降級到最適合的提供者
generateImage({
  prompt: '在旁边加一只羊驼',
  images: ['/path/to/character.jpg'],
  size: '16:9',
  quality: 'hd'
})
  .then(console.log);

// 7. 多種尺寸
const sizes = ['1024x1024', '1920x1080', '1080x1920', '1280x720'];
for (const size of sizes) {
  generateImage({
    prompt: '测试图片',
    size,
    quality: 'medium'
  })
    .then(result => console.log(`尺寸 ${size} 生成結果:`, result));
}

// 8. 品質對比
const qualities = ['standard', 'medium', 'hd'];
for (const quality of qualities) {
  generateImage({
    prompt: '测试图片',
    size: '1024x1024',
    quality
  })
    .then(result => console.log(`品質 ${quality} 生成結果:`, result));
}

// 9. 錯誤處理
generateImage({
  prompt: '测试图片',
  size: '999999x999999',  // 無效尺寸
  quality: 'invalid'  // 無效品質
})
  .catch(error => console.error('發生錯誤:', error.message));

// 10. 完整參數
generateImage({
  prompt: '一张台北 101 的风景照片，日落时分，暖色调',
  size: '1920x1080',
  quality: 'hd',
  n: 3,
  forceProvider: null  // 讓系統自動選擇
})
  .then(result => {
    // 保存生成的圖片
    if (result.success) {
      result.images.forEach((imgData, i) => {
        const ext = imgData.mimeType.includes('jpeg') ? 'jpg' : 'png';
        const outputFile = `generated_${i}.${ext}`;
        fs.writeFileSync(outputFile, Buffer.from(imgData.data, 'base64'));
        console.log(`圖片已保存: ${outputFile}`);
      });
    }
  });

// 11. Async/await 使用方式
(async () => {
  try {
    const result = await generateImage({
      prompt: '一只可爱的猫咪',
      size: '1280x720',
      quality: 'hd'
    });

    if (result.success) {
      console.log('✅ 生成成功！');
      console.log('提供者:', result.provider);
      console.log('數量:', result.images.length);

      result.images.forEach((imgData, i) => {
        const ext = imgData.mimeType.includes('jpeg') ? 'jpg' : 'png';
        const outputFile = `cat_${i}.${ext}`;
        fs.writeFileSync(outputFile, Buffer.from(imgData.data, 'base64'));
        console.log(`  ✓ ${outputFile}`);
      });
    }
  } catch (error) {
    console.error('❌ 發生錯誤:', error.message);
  }
})();

// 12. 批次生成並保存
async function generateBatch(prompts) {
  for (let i = 0; i < prompts.length; i++) {
    const prompt = prompts[i];
    console.log(`\n生成第 ${i + 1}/${prompts.length} 張...`);

    try {
      const result = await generateImage({
        prompt,
        size: '1024x1024',
        quality: 'medium'
      });

      if (result.success) {
        result.images.forEach((imgData, j) => {
          const ext = imgData.mimeType.includes('jpeg') ? 'jpg' : 'png';
          const outputFile = `batch_${i}_${j}.${ext}`;
          fs.writeFileSync(outputFile, Buffer.from(imgData.data, 'base64'));
          console.log(`  ✓ ${outputFile}`);
        });
      }
    } catch (error) {
      console.error(`❌ 第 ${i + 1} 弱失敗:`, error.message);
    }
  }
}

generateBatch([
  '一只白色的猫',
  '一只黑色的狗',
  '一只金色的鱼',
  '一只红色的鸟'
]);
