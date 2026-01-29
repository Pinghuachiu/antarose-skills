#!/usr/bin/env node
/**
 * Gemini Image Preview - Node.js 腳本
 * 使用 AllAPI 提供的 Gemini 模型生成圖片
 */

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const API_KEY = process.env.ALLAPI_KEY;
if (!API_KEY) {
  console.error('錯誤: 請設定 ALLAPI_KEY 環境變數');
  console.error('請參考 resource.md 獲取 API Key');
  process.exit(1);
}

// 模型選項
const MODEL_PRO = 'gemini-3-pro-image-preview';  // NanoBanana Pro (最強）
const MODEL_FLASH = 'gemini-2.5-flash-image';  // Flash (快速）

// 用於追蹤暫存檔案
const tempFiles = [];

function cleanupTempFiles() {
  tempFiles.forEach(filePath => {
    try {
      if (fs.existsSync(filePath)) {
        const stat = fs.statSync(filePath);
        if (stat.isFile()) {
          fs.unlinkSync(filePath);
        } else if (stat.isDirectory()) {
          fs.rmSync(filePath, { recursive: true, force: true });
        }
      }
    } catch (error) {
      console.error(`警告: 無法刪除暫存檔案 ${filePath}: ${error.message}`);
    }
  });
  tempFiles.length = 0;
}

function imageToBase64(imagePath) {
  try {
    const imageBuffer = fs.readFileSync(imagePath);
    return imageBuffer.toString('base64');
  } catch (error) {
    console.error(`錯誤: 無法讀取檔案 - ${error.message}`);
    process.exit(1);
  }
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

  try {
    const response = await fetch(`${apiUrl}?key=${API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`API 請求失敗: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    console.log('生成結果:', result);
    return result;
  } catch (error) {
    console.error('錯誤:', error.message);
    process.exit(1);
  }
}

function showHelp() {
  console.log('使用方法: node generate.js <prompt> [--images img1,img2,...] [--ratio <ratio>] [--size <size>] [--model <model>]');
  console.log('');
  console.log('範例:');
  console.log('  node generate.js "一隻可愛的貓"');
  console.log('  node generate.js "生成風景" --images photo1.jpg,photo2.jpg --ratio 16:9 --size 4K');
  console.log('  node generate.js "快速生成" --model flash');
  console.log('');
  console.log('參數說明:');
  console.log('  prompt: 圖片描述文字');
  console.log('  --images: 圖片路徑列表，用逗號分隔（最多14張）');
  console.log('  --ratio: 寬高比 (1:1, 16:9, 9:16, 2:3, 3:2 等）');
  console.log('  --size: 圖片大小 (1K, 2K, 4K, HIGH, MEDIUM)');
  console.log('  --model: 模型選擇 (pro, flash)');
}

async function main() {
  try {
    if (process.argv.length < 3) {
      showHelp();
      process.exit(1);
    }

    const prompt = process.argv[2];
    let images = [];
    let aspectRatio = '1:1';
    let imageSize = '2K';
    let model = MODEL_PRO;

    for (let i = 3; i < process.argv.length; i++) {
      const arg = process.argv[i];
      if (arg.startsWith('--images=')) {
        images = arg.split('=')[1].split(',');
      } else if (arg.startsWith('--ratio=')) {
        aspectRatio = arg.split('=')[1];
      } else if (arg.startsWith('--size=')) {
        imageSize = arg.split('=')[1];
      } else if (arg === '--model=flash') {
        model = MODEL_FLASH;
      } else if (arg === '--model=pro') {
        model = MODEL_PRO;
      }
    }

    await generateImage({
      prompt,
      images,
      aspectRatio,
      imageSize,
      model
    });
  } finally {
    cleanupTempFiles();
  }
}

main().catch(error => {
  console.error('未預期的錯誤:', error);
  process.exit(1);
});
