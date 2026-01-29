#!/usr/bin/env node
/**
 * Universal Image Gen - Node.js 腳本
 * 智能圖片生成工具，優先使用 Antigravity API，失敗時自動降級到 NanoBanana
 */

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const ANTIGRAVITY_API_KEY = process.env.ANTIGRAVITY_API_KEY;
const ALLAPI_KEY = process.env.ALLAPI_KEY;

if (!ANTIGRAVITY_API_KEY && !ALLAPI_KEY) {
  console.error('錯誤: 請設定 ANTIGRAVITY_API_KEY 或 ALLAPI_KEY 環境變數');
  console.error('請參考 resource.md 獲取 API Key');
  process.exit(1);
}

// API 端點
const ANTIGRAVITY_API_URL = 'http://192.168.1.159:8045/v1/messages';
const ALLAPI_API_URL = 'https://allapi.store/v1beta/models/gemini-3-pro-image-preview:generateContent';

// 標準寬高比
const STANDARD_ASPECT_RATIOS = {
  '21:9': 2.333333,
  '16:10': 1.6,
  '16:9': 1.777777,
  '4:3': 1.333333,
  '1:1': 1.0,
  '3:4': 0.75,
  '9:16': 0.5625
};

// 品質對應
const QUALITY_MAP = {
  'hd': '4K',
  'medium': '2K',
  'standard': '1K'
};

// 品質尺寸對應
const QUALITY_SIZE_MAP = {
  '4K': {
    '1:1': '4096x4096',
    '16:9': '5504x3072',
    '9:16': '3072x5504',
    '21:9': '6336x2688',
    '4:3': '4800x3584',
    '3:4': '3584x4800',
    '16:10': '5504x3440'
  },
  '2K': {
    '1:1': '2048x2048',
    '16:9': '2752x1536',
    '9:16': '1536x2752',
    '21:9': '3168x1344',
    '4:3': '2400x1792',
    '3:4': '1792x2400',
    '16:10': '2752x1720'
  },
  '1K': {
    '1:1': '1024x1024',
    '16:9': '1376x768',
    '9:16': '768x1376',
    '21:9': '1584x672',
    '4:3': '1200x896',
    '3:4': '896x1200',
    '16:10': '1376x860'
  }
};

function imageToBase64(imagePath) {
  try {
    const imageBuffer = fs.readFileSync(imagePath);
    return imageBuffer.toString('base64');
  } catch (error) {
    console.error(`錯誤: 無法讀取檔案 - ${error.message}`);
    process.exit(1);
  }
}

function calculateAspectRatio(width, height) {
  const ratio = width / height;
  let closestRatio = '1:1';
  let closestDiff = Math.abs(ratio - 1.0);

  for (const [name, value] of Object.entries(STANDARD_ASPECT_RATIOS)) {
    const diff = Math.abs(ratio - value);
    if (diff < closestDiff) {
      closestDiff = diff;
      closestRatio = name;
    }
  }

  return closestRatio;
}

function parseSize(sizeStr) {
  try {
    const [width, height] = sizeStr.toLowerCase().split('x').map(Number);
    return { width, height };
  } catch {
    console.error(`錯誤: 無效的尺寸格式 - ${sizeStr}`);
    console.error('請使用 WIDTHxHEIGHT 格式，例如 1280x720');
    process.exit(1);
  }
}

async function generateAntigravity({ prompt, size = '1280x720', quality = 'hd', n = 1, images = [] }) {
  if (!ANTIGRAVITY_API_KEY) {
    throw new Error('ANTIGRAVITY_API_KEY 未設定');
  }

  const payload = {
    model: 'gemini-3-pro-image',
    size,
    quality,
    messages: [{ role: 'user', content: prompt }]
  };

  // 如果有參考圖，添加到 payload
  if (images.length > 0) {
    const imageBase64 = imageToBase64(images[0]);
    payload.image = `data:image/jpeg;base64,${imageBase64}`;
  }

  const response = await fetch(ANTIGRAVITY_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': ANTIGRAVITY_API_KEY
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Antigravity API 錯誤: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

async function generateNanobanana({ prompt, size = '1024x1024', quality = 'standard', n = 1, images = [] }) {
  if (!ALLAPI_KEY) {
    throw new Error('ALLAPI_KEY 未設定');
  }

  const { width, height } = parseSize(size);
  const aspectRatio = calculateAspectRatio(width, height);
  const qualityLevel = QUALITY_MAP[quality] || '1K';

  const parts = [{ text: prompt }];

  if (images.length > 0) {
    images.forEach(imagePath => {
      parts.push({
        inline_data: {
          mime_type: 'image/jpeg',
          data: imageToBase64(imagePath)
        }
      });
    });
  }

  const payload = {
    contents: [
      {
        role: 'user',
        parts
      }
    ],
    generationConfig: {
      responseModalities: ['IMAGE'],
      imageConfig: {
        aspectRatio: aspectRatio,
        imageSize: qualityLevel
      }
    }
  };

  const response = await fetch(`${ALLAPI_API_URL}?key=${ALLAPI_KEY}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`NanoBanana API 錯誤: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

function extractImagesFromAntigravity(response) {
  const images = [];
  const content = response.content?.[0];
  const text = content?.text || '';

  const regex = /data:image\/jpeg;base64,([A-Za-z0-9+/=]+)/g;
  let match;
  let index = 0;

  while ((match = regex.exec(text)) !== null) {
    images.push({
      index: index++,
      data: match[1],
      mimeType: 'image/jpeg'
    });
  }

  return images;
}

function extractImagesFromNanobanana(response) {
  const images = [];
  const candidates = response.candidates || [];

  candidates.forEach((candidate, i) => {
    const parts = candidate.content?.parts || [];
    parts.forEach(part => {
      if (part.inlineData) {
        images.push({
          index: i,
          data: part.inlineData.data,
          mimeType: part.inlineData.mimeType || 'image/jpeg'
        });
      }
    });
  });

  return images;
}

async function generateImage({ prompt, size = '1024x1024', quality = 'standard', n = 1, images = [], forceProvider = null }) {
  const providers = [];

  if (forceProvider === 'antigravity' || (forceProvider === null && ANTIGRAVITY_API_KEY)) {
    providers.push({ name: 'antigravity', fn: generateAntigravity, extract: extractImagesFromAntigravity });
  }
  if (forceProvider === 'nanobanana' || (forceProvider === null && ALLAPI_KEY)) {
    providers.push({ name: 'nanobanana', fn: generateNanobanana, extract: extractImagesFromNanobanana });
  }

  for (let i = 0; i < providers.length; i++) {
    const { name, fn, extract } = providers[i];
    try {
      console.log(`🔄 嘗試使用 ${name} API...`);
      const response = await fn({ prompt, size, quality, n, images });
      const imagesData = extract(response);

      if (imagesData.length > 0) {
        console.log(`✅ ${name} API 成功生成 ${imagesData.length} 張圖片`);
        return {
          success: true,
          provider: name,
          images: imagesData,
          parameters: { size, quality, n }
        };
      }
    } catch (error) {
      console.log(`❌ ${name} API 失敗: ${error.message}`);
      if (i < providers.length - 1) {
        console.log('⏭️  自動切換到下一個提供者...');
      }
    }
  }

  return {
    success: false,
    error: 'All providers failed',
    providers: providers.map(p => p.name)
  };
}

function showHelp() {
  console.log('使用方法: node generate.js <prompt> [options]');
  console.log('');
  console.log('範例:');
  console.log('  node generate.js "一只可爱的猫咪"');
  console.log('  node generate.js "风景照片" --size 1920x1080 --quality hd');
  console.log('  node generate.js "猫咪" --n 5');
  console.log('  node generate.js "改成写实风格" --images cat.jpg');
  console.log('  node generate.js "测试" --force-provider nanobanana');
  console.log('');
  console.log('參數說明:');
  console.log('  prompt: 圖片描述文字');
  console.log('  --size: 尺寸（WIDTHxHEIGHT 格式）');
  console.log('  --quality: 品質（hd, medium, standard）');
  console.log('  --n: 生成圖片數量（1-10）');
  console.log('  --images: 參考圖路徑列表，用逗號分隔');
  console.log('  --force-provider: 強制使用提供者（antigravity, nanobanana）');
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    showHelp();
    process.exit(1);
  }

  const prompt = args[0];
  let size = '1024x1024';
  let quality = 'standard';
  let n = 1;
  let images = [];
  let forceProvider = null;

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];

    if (arg.startsWith('--size=')) {
      size = arg.split('=')[1];
    } else if (arg.startsWith('--quality=')) {
      quality = arg.split('=')[1];
    } else if (arg.startsWith('--n=')) {
      n = parseInt(arg.split('=')[1], 10);
    } else if (arg.startsWith('--images=')) {
      images = arg.split('=')[1].split(',');
    } else if (arg.startsWith('--force-provider=')) {
      forceProvider = arg.split('=')[1];
    }
  }

  if (n < 1 || n > 10) {
    console.error('錯誤: n 參數必須在 1-10 之間');
    process.exit(1);
  }

  try {
    const result = await generateImage({ prompt, size, quality, n, images, forceProvider });

    if (result.success) {
      console.log('\n🎉 成功生成圖片！');
      console.log(`提供者: ${result.provider}`);
      console.log(`數量: ${result.images.length}`);

      // 保存圖片
      result.images.forEach(img => {
        const ext = img.mimeType.includes('jpeg') ? 'jpg' : 'png';
        const outputFile = `universal_gen_${img.index}.${ext}`;
        fs.writeFileSync(outputFile, Buffer.from(img.data, 'base64'));
        console.log(`  ✓ ${outputFile}`);
      });
    } else {
      console.log('\n❌ 所有提供者都失敗了');
      process.exit(1);
    }
  } catch (error) {
    console.error('❌ 發生錯誤:', error.message);
    process.exit(1);
  }
}

main().catch(error => {
  console.error('❌ 未預期的錯誤:', error);
  process.exit(1);
});
