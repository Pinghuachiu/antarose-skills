#!/usr/bin/env node
/**
 * Facebook Page Post - Node.js 腳本
 * 使用 Facebook Graph API v24.0 發布文字、圖片、影片到 Facebook 粉絲專頁
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const querystring = require('querystring');

// Configuration
const PAGE_ID = process.env.FACEBOOK_PAGE_ID;
const ACCESS_TOKEN = process.env.FACEBOOK_PAGE_ACCESS_TOKEN;
const API_VERSION = 'v24.0';
const BASE_URL = `https://graph.facebook.com/${API_VERSION}`;

// Retry settings
const MAX_RETRIES = 3;
const RETRY_DELAY = 5000; // milliseconds

/**
 * Validate environment variables
 */
function validateCredentials() {
    if (!PAGE_ID) {
        console.error('錯誤: 請設定 FACEBOOK_PAGE_ID 環境變數');
        console.error('範例: export FACEBOOK_PAGE_ID="123456789"');
        console.error('詳細說明請參考: https://developers.facebook.com/docs/pages/access-tokens/');
        process.exit(1);
    }

    if (!ACCESS_TOKEN) {
        console.error('錯誤: 請設定 FACEBOOK_PAGE_ACCESS_TOKEN 環境變數');
        console.error('範例: export FACEBOOK_PAGE_ACCESS_TOKEN="EAAxxxxxx..."');
        console.error('取得方式請參考 SKILL.md 的 Token 管理章節');
        process.exit(1);
    }
}

/**
 * Sleep utility
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Make HTTP POST request
 */
function makeRequest(url, data, files = null) {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url);

        if (files) {
            // Multipart form data upload
            const boundary = '----WebKitFormBoundary' + Date.now();
            const body = [];

            // Add form fields
            for (const [key, value] of Object.entries(data)) {
                body.push(`--${boundary}\r\n`);
                body.push(`Content-Disposition: form-data; name="${key}"\r\n\r\n`);
                body.push(`${value}\r\n`);
            }

            // Add file
            if (files.source) {
                body.push(`--${boundary}\r\n`);
                body.push(`Content-Disposition: form-data; name="source"; filename="${files.filename}"\r\n`);
                body.push(`Content-Type: application/octet-stream\r\n\r\n`);
                body.push(files.source);
                body.push('\r\n');
            }

            body.push(`--${boundary}--\r\n`);

            const options = {
                hostname: urlObj.hostname,
                port: 443,
                path: urlObj.pathname + urlObj.search,
                method: 'POST',
                headers: {
                    'Content-Type': `multipart/form-data; boundary=${boundary}`,
                    'Content-Length': Buffer.concat(body.map(b =>
                        Buffer.isBuffer(b) ? b : Buffer.from(b)
                    )).length
                }
            };

            const req = https.request(options, (res) => {
                let responseData = '';
                res.on('data', (chunk) => responseData += chunk);
                res.on('end', () => {
                    try {
                        const jsonResponse = JSON.parse(responseData);
                        if (res.statusCode === 200 || res.statusCode === 201) {
                            resolve(jsonResponse);
                        } else {
                            reject(new Error(`HTTP ${res.statusCode}: ${JSON.stringify(jsonResponse)}`));
                        }
                    } catch (e) {
                        reject(new Error(`Failed to parse response: ${responseData}`));
                    }
                });
            });

            req.on('error', reject);

            // Send body
            const buffers = body.map(b => Buffer.isBuffer(b) ? b : Buffer.from(b));
            req.write(Buffer.concat(buffers));
            req.end();
        } else {
            // JSON request
            const postData = JSON.stringify(data);

            const options = {
                hostname: urlObj.hostname,
                port: 443,
                path: urlObj.pathname + urlObj.search,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(postData)
                }
            };

            const req = https.request(options, (res) => {
                let responseData = '';
                res.on('data', (chunk) => responseData += chunk);
                res.on('end', () => {
                    try {
                        const jsonResponse = JSON.parse(responseData);
                        if (res.statusCode === 200 || res.statusCode === 201) {
                            resolve(jsonResponse);
                        } else {
                            reject(new Error(`HTTP ${res.statusCode}: ${JSON.stringify(jsonResponse)}`));
                        }
                    } catch (e) {
                        reject(new Error(`Failed to parse response: ${responseData}`));
                    }
                });
            });

            req.on('error', reject);
            req.write(postData);
            req.end();
        }
    });
}

/**
 * Make API request with retry logic
 */
async function makeApiRequest(url, data, files = null) {
    for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
        try {
            const result = await makeRequest(url, data, files);
            return result;
        } catch (error) {
            if (attempt < MAX_RETRIES) {
                console.log(`⚠️  請求失敗: ${error.message}，重試中... (嘗試 ${attempt}/${MAX_RETRIES})`);
                await sleep(RETRY_DELAY);
            } else {
                console.error(`❌ API 請求失敗: ${error.message}`);
                process.exit(1);
            }
        }
    }
}

/**
 * Post text message
 */
async function postText(message) {
    if (!message) {
        console.error('錯誤: 文字文章需要 --message 參數');
        process.exit(1);
    }

    const url = `${BASE_URL}/${PAGE_ID}/feed`;
    const payload = {
        message: message,
        access_token: ACCESS_TOKEN
    };

    const result = await makeApiRequest(url, payload);

    console.log('✅ 文章發布成功!');
    console.log(`   貼文 ID: ${result.id}`);
    console.log(`   連結: https://www.facebook.com/${result.id.split('_')[1]}`);

    return result;
}

/**
 * Post photo
 */
async function postPhoto(imagePath, message = null) {
    if (!imagePath) {
        console.error('錯誤: 圖片文章需要 --file 參數');
        process.exit(1);
    }

    if (!fs.existsSync(imagePath)) {
        console.error(`錯誤: 檔案不存在 - ${imagePath}`);
        process.exit(1);
    }

    const url = `${BASE_URL}/${PAGE_ID}/photos`;
    const payload = {
        access_token: ACCESS_TOKEN
    };

    if (message) {
        payload.caption = message;
    }

    const imageBuffer = fs.readFileSync(imagePath);

    const files = {
        source: imageBuffer,
        filename: path.basename(imagePath)
    };

    const result = await makeApiRequest(url, payload, files);

    console.log('✅ 圖片上傳成功!');
    console.log(`   圖片 ID: ${result.id}`);
    if (result.post_id) {
        console.log(`   貼文連結: https://www.facebook.com/${result.post_id.split('_')[1]}`);
    }

    return result;
}

/**
 * Post multiple photos (album)
 */
async function postPhotos(imagePaths, message = null) {
    if (!imagePaths || imagePaths.length === 0) {
        console.error('錯誤: 多圖上傳需要 --files 參數');
        process.exit(1);
    }

    // Check all files exist
    for (const imgPath of imagePaths) {
        if (!fs.existsSync(imgPath)) {
            console.error(`錯誤: 檔案不存在 - ${imgPath}`);
            process.exit(1);
        }
    }

    console.log(`📁 正在建立相簿並上傳 ${imagePaths.length} 張圖片...`);

    // Create album
    const albumUrl = `${BASE_URL}/${PAGE_ID}/albums`;
    const albumPayload = {
        name: message || 'Photo Album',
        access_token: ACCESS_TOKEN
    };

    const albumResult = await makeApiRequest(albumUrl, albumPayload);
    const albumId = albumResult.id;

    console.log(`   相簿 ID: ${albumId}`);

    // Upload photos
    const results = [];
    for (let i = 0; i < imagePaths.length; i++) {
        const imagePath = imagePaths[i];
        const photoUrl = `${BASE_URL}/${albumId}/photos`;

        const imageBuffer = fs.readFileSync(imagePath);
        const files = {
            source: imageBuffer,
            filename: path.basename(imagePath)
        };

        const result = await makeApiRequest(photoUrl, { access_token: ACCESS_TOKEN }, files);
        results.push(result);

        console.log(`   圖片 ${i + 1}/${imagePaths.length} 上傳完成 (ID: ${result.id})`);
    }

    console.log('✅ 所有圖片上傳成功!');
    console.log(`   相簿連結: https://www.facebook.com/media/set/?set=${albumId}`);

    return results;
}

/**
 * Post video
 */
async function postVideo(videoPath, message = null, title = null, description = null) {
    if (!videoPath) {
        console.error('錯誤: 影片上傳需要 --file 參數');
        process.exit(1);
    }

    if (!fs.existsSync(videoPath)) {
        console.error(`錯誤: 檔案不存在 - ${videoPath}`);
        process.exit(1);
    }

    // Check file size
    const stats = fs.statSync(videoPath);
    const fileSizeMB = stats.size / (1024 * 1024);

    if (fileSizeMB > 1000) {
        console.warn(`⚠️  警告: 影片大小 ${fileSizeMB.toFixed(1)} MB，超過 1GB`);
        console.warn('建議使用 Facebook 的 Resumable Upload API 上傳大型影片');
        // Continue anyway
    }

    const url = `${BASE_URL}/${PAGE_ID}/videos`;
    const payload = {
        access_token: ACCESS_TOKEN
    };

    if (message) {
        payload.description = message;
    }
    if (title) {
        payload.title = title;
    }
    if (description) {
        payload.description = description;
    }

    console.log(`📹 正在上傳影片... (大小: ${fileSizeMB.toFixed(1)} MB)`);

    const videoBuffer = fs.readFileSync(videoPath);
    const files = {
        source: videoBuffer,
        filename: path.basename(videoPath)
    };

    const result = await makeApiRequest(url, payload, files);

    console.log('✅ 影片上傳成功!');
    console.log(`   影片 ID: ${result.id}`);
    console.log(`   注意: 影片正在處理中，請稍候片刻後查看`);

    return result;
}

/**
 * Main function
 */
async function main() {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log('Facebook Page Post - 發布文章、圖片、影片到 Facebook 粉絲專頁\n');
        console.log('使用方法:');
        console.log('  node post.js text --message "Hello"');
        console.log('  node post.js photo --file photo.jpg --message "Caption"');
        console.log('  node post.js photos --files p1.jpg p2.jpg --message "Album"');
        console.log('  node post.js video --file video.mp4 --title "Title"\n');
        console.log('環境變數:');
        console.log('  FACEBOOK_PAGE_ID              Facebook 粉絲專頁 ID');
        console.log('  FACEBOOK_PAGE_ACCESS_TOKEN    Facebook Page Access Token\n');
        console.log('詳細說明請參考 SKILL.md');
        process.exit(1);
    }

    validateCredentials();

    const type = args[0];
    const message = args.includes('--message') ? args[args.indexOf('--message') + 1] : null;
    const file = args.includes('--file') ? args[args.indexOf('--file') + 1] : null;
    const filesIndex = args.indexOf('--files');
    const files = filesIndex !== -1 ? args.slice(filesIndex + 1) : null;
    const title = args.includes('--title') ? args[args.indexOf('--title') + 1] : null;
    const description = args.includes('--description') ? args[args.indexOf('--description') + 1] : null;

    try {
        switch (type) {
            case 'text':
                await postText(message);
                break;
            case 'photo':
                await postPhoto(file, message);
                break;
            case 'photos':
                await postPhotos(files, message);
                break;
            case 'video':
                await postVideo(file, description || message, title, description);
                break;
            default:
                console.error(`錯誤: 未知的類型 "${type}"`);
                console.error('支援的類型: text, photo, photos, video');
                process.exit(1);
        }
    } catch (error) {
        console.error(`❌ 發生錯誤: ${error.message}`);
        process.exit(1);
    }
}

// Run
main().catch(console.error);
