const fetch = require('node-fetch');
const FormData = require('form-data');
const fs = require('fs');

// 從環境變數或直接設定 Webhook URL
const WEBHOOK_URL = 'YOUR_WEBHOOK_URL';

async function sendMessage({ content, username, avatarUrl, tts = false }) {
  /**
   * 發送簡單文字訊息

   * @param {Object} options
   * @param {string} options.content - 訊息內容
   * @param {string} options.username - 自訂使用者名稱
   * @param {string} options.avatarUrl - 自訂頭像 URL
   * @param {boolean} options.tts - 是否為 TTS 訊息

   * @returns {Object} API 回應
   */
  const payload = { content, tts };

  if (username) payload.username = username;
  if (avatarUrl) payload.avatar_url = avatarUrl;

  const response = await fetch(WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  return response.json();
}

async function sendEmbed({ title, description, color = 0x5865F2, fields, thumbnail, image }) {
  /**
   * 發送 Embed 訊息

   * @param {Object} options
   * @param {string} options.title - Embed 標題
   * @param {string} options.description - Embed 描述
   * @param {number} options.color - Embed 顏色（十進制）
   * @param {Array} options.fields - 欄位數組 [{"name": "名稱", "value": "值", "inline": false}]
   * @param {string} options.thumbnail - 縮圖 URL
   * @param {string} options.image - 圖片 URL

   * @returns {Object} API 回應
   */
  const embed = {
    title,
    color
  };

  if (description) embed.description = description;
  if (fields) embed.fields = fields;
  if (thumbnail) embed.thumbnail = { url: thumbnail };
  if (image) embed.image = { url: image };

  const payload = { embeds: [embed] };

  const response = await fetch(WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  return response.json();
}

async function sendAttachment({ filePath, content, username }) {
  /**
   * 發送附件訊息

   * @param {Object} options
   * @param {string} options.filePath - 檔案路徑
   * @param {string} options.content - 訊息內容
   * @param {string} options.username - 自訂使用者名稱

   * @returns {Object} API 回應
   */
  const form = new FormData();
  const payload = {};

  if (content) payload.content = content;
  if (username) payload.username = username;

  form.append('payload_json', JSON.stringify(payload));
  form.append('file', fs.createReadStream(filePath));

  const response = await fetch(WEBHOOK_URL, {
    method: 'POST',
    body: form
  });

  return response.json();
}

// 使用範例

// 1. 簡單文字訊息
sendMessage({ content: 'Hello, World!' })
  .then(console.log);

// 2. Markdown 格式
sendMessage({ content: '**粗體** *斜體* ~~刪除線~~' })
  .then(console.log);

// 3. 自訂使用者名稱和頭像
sendMessage({
  content: '自訂 Bot 訊息',
  username: 'My Bot',
  avatarUrl: 'https://example.com/avatar.png'
})
  .then(console.log);

// 4. TTS 訊息
sendMessage({ content: '這是語音訊息', tts: true })
  .then(console.log);

// 5. 基本 Embed
sendEmbed({
  title: '標題',
  description: '這是描述',
  color: 0x5865F2  // Discord 藍色
})
  .then(console.log);

// 6. Embed with 欄位
sendEmbed({
  title: '系統狀態',
  description: '目前的系統狀態',
  color: 0x00FF00,  // 綠色
  fields: [
    { name: 'CPU', value: '45%', inline: true },
    { name: '記憶體', value: '60%', inline: true },
    { name: '磁碟', value: '30%', inline: true }
  ]
})
  .then(console.log);

// 7. Embed with 圖片
sendEmbed({
  title: '圖片分享',
  description: '這是一張圖片',
  color: 0xFF0000,  // 紅色
  image: 'https://example.com/image.png',
  thumbnail: 'https://example.com/thumbnail.png'
})
  .then(console.log);

// 8. 發送附件
sendAttachment({
  filePath: '/path/to/file.jpg',
  content: '這是附件',
  username: 'File Bot'
})
  .then(console.log);

// 9. 複雜 Embed
sendEmbed({
  title: '部署通知',
  description: '部署已成功完成',
  color: 0x00FF00,
  fields: [
    { name: '應用程式', value: 'My App', inline: true },
    { name: '版本', value: 'v1.0.0', inline: true },
    { name: '狀態', value: '✅ 成功', inline: false },
    { name: '時間', value: '2024-01-01 00:00:00', inline: true },
    { name: '持續時間', value: '2分30秒', inline: true },
    { name: '作者', value: '@user', inline: true }
  ],
  thumbnail: 'https://example.com/icon.png'
})
  .then(console.log);

// 10. 錯誤處理
(async () => {
  try {
    const result = await sendMessage({ content: '測試訊息' });
    if (result.id) {
      console.log('訊息發送成功');
    } else {
      console.log('訊息發送失敗:', result);
    }
  } catch (error) {
    console.error('發生錯誤:', error);
  }
})();
