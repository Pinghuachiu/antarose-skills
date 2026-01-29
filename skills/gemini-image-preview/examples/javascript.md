const fs = require('fs');
const fetch = require('node-fetch');

const API_KEY = 'YOUR_API_KEY';
// 模型選項
const MODEL_PRO = 'gemini-3-pro-image-preview';  // NanoBanana Pro (最強）
const MODEL_FLASH = 'gemini-2.5-flash-image';  // Flash (快速）

function imageToBase64(imagePath) {
  const imageBuffer = fs.readFileSync(imagePath);
  return imageBuffer.toString('base64');
}

async function generateImage({ prompt = '', images = [], aspectRatio = '1:1', imageSize = '2K', model = MODEL_PRO }) {
  const parts = [];

  if (prompt) {
    parts.push({ text: prompt });
  }

  if (images.length > 0) {
    // 最多支援 14 張圖片
    images.slice(0, 14).forEach(imagePath => {
      parts.push({
        inline_data: {
          mime_type: 'image/jpeg',
          data: imageToBase64(imagePath)
        }
      });
    });
  }

  // 構建 API URL
  const apiUrl = `https://allapi.store/v1beta/models/${model}:generateContent`;

  const payload = {
    contents: [
      {
        role: 'user',
        parts: parts
      }
    ],
    generationConfig: {
      responseModalities: ['IMAGE'],
      imageConfig: {
        aspectRatio: aspectRatio,
        imageSize: imageSize
      }
    }
  };

  const response = await fetch(`${apiUrl}?key=${API_KEY}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  return response.json();
}

// 使用範例

// 1. 文生圖 - Pro 版本 4K 品質
generateImage({
  prompt: '一隻可愛的貓咪在陽光下玩耍',
  aspectRatio: '1:1',
  imageSize: '4K',  // 最高品質
  model: MODEL_PRO
})
  .then(console.log);

// 2. 文生圖 - Flash 版本（快速）
generateImage({
  prompt: '一隻貓',
  aspectRatio: '1:1',
  imageSize: 'HIGH',  // Flash 版本使用 HIGH
  model: MODEL_FLASH
})
  .then(console.log);

// 3. 圖生圖 - Pro 版本 2K 品質
generateImage({
  prompt: '在旁邊加一隻羊駝',
  images: ['/path/to/your/image.jpg'],
  aspectRatio: '16:9',
  imageSize: '2K',  // 平衡品質和成本
  model: MODEL_PRO
})
  .then(console.log);

// 4. 多圖合成（最多14張）
generateImage({
  prompt: '將這些圖片融合在一起，創建一個場景',
  images: ['/path/to/image1.jpg', '/path/to/image2.jpg', '/path/to/image3.jpg'],
  aspectRatio: '16:9',
  imageSize: '2K',  // 推薦用於多圖合成
  model: MODEL_PRO
})
  .then(console.log);

// 5. 使用寬屏格式
generateImage({
  prompt: '創建一張海報',
  aspectRatio: '21:9',  // 寬屏格式
  imageSize: '4K',
  model: MODEL_PRO
})
  .then(console.log);
