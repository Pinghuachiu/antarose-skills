---
name: linkedin-post
description: LinkedIn 貼文發布技能，支援文字、圖片、連結和文章發布到 LinkedIn 個人檔案或公司頁面。使用 LinkedIn Token Generator 取得 Access Token，無需完整 OAuth 流程。
metadata:
  category: social-media
  type: automation
  languages:
    - python
  platforms:
    - linkedin
  compatibility:
    - claude-code
    - opencode
    - any-agent
---

# LinkedIn Post - LinkedIn 貼文發布

使用 LinkedIn REST API 發布貼文到 LinkedIn，支援文字、圖片、連結和文章分享。

## 核心功能

1. **📝 純文字發布** - 發布純文字貼文到 LinkedIn
2. **📸 圖片發布** - 發布圖片貼文（單張）
3. **🔗 連結發布** - 分享連結（帶預覽）
4. **📄 文章發布** - 發布長文
5. **🆔 取得 LinkedIn Person ID** - 使用 `/v2/userinfo` 端點自動取得
6. **💾 資料庫整合** - 直接從資料庫讀取 token（access_token 欄位）

## 與其他平台的差異

| 特性 | LinkedIn | Facebook | Instagram | Threads |
|------|----------|----------|-----------|---------|
| Token 使用 | **直接使用 Access Token** | 需要換取 Page Token | 直接使用資料庫 token | 直接使用資料庫 token |
| API 版本 | REST API (202210) | Graph API v24.0 | Instagram Graph API | Threads API |
| 發布流程 | 一次性發布 | 直接發布 | Container → Publish | Container 即發布 |
| 文字限制 | 3,000 字符 | 63,206 字符 | 2,200 字符 | 500 字符 |
| 圖片支援 | ✅ 單張圖片 | ✅ 單張圖片 | ✅ Carousel (2-10張) | ✅ Carousel (2-20張) |
| 連結預覽 | ✅ 原生支援 | ✅ 原生支援 | ❌ 不支援 | ❌ 不支援 |
| Token 有效期 | 60 天 | 60 天 | 60 天 | 60 天 |

## 前置要求

### 1. LinkedIn Developer Application

1. **建立應用程式**
   - 前往: https://www.linkedin.com/developers/apps/new
   - 需要連接到 LinkedIn Company Page
   - 驗證應用程式

2. **啟用產品**
   - Share on LinkedIn
   - Sign In with LinkedIn using OpenID Connect

3. **設定 OAuth 2.0 Scopes**
   - `profile` - **必需**，讀取個人資料（取得 Person ID）
   - `w_member_social` - **必需**，個人檔案發文
   - `w_organization_social` - 可選，公司頁面發文

**重要**: 必須同時勾選 `profile` 和 `w_member_social`，否則無法取得 Person ID 或發文。

### 2. Access Token 取得

有兩種方式取得 Access Token：

#### 方式 A: Token Generator（官方工具，但可能有 state 錯誤）

**優點**：
- ✅ 官方工具
- ✅ 無需編寫程式碼

**缺點**：
- ❌ 常出現「state parameter was modified」錯誤
- ❌ 需要多次重試

**步驟**：

1. **前往 Token Generator**
   ```
   https://www.linkedin.com/developers/tools/oauth/token-generator
   ```

2. **選擇你的應用程式**

3. **勾選 Scopes**
   - `w_member_social`（必需，發文用）
   - `profile`（必需，取得 Person ID）

4. **點擊「Request access token」**

5. **複製 Access Token**
   - 格式: `AQXXXXXXXXXXXXXXXXXXXXXX`
   - 有效期: 60 天

---

#### 方式 B: 手動 OAuth 流程（推薦，更穩定）⭐

**優點**：
- ✅ 穩定，不會有 state 錯誤
- ✅ 完全控制流程
- ✅ 可重複使用

**完整步驟**：

**步驟 1: 設定應用程式 Scopes**

1. 前往: https://www.linkedin.com/developers/apps
2. 選擇你的應用程式
3. 點擊「Auth」標籤
4. 在「OAuth 2.0 Scopes」中勾選：
   - ✅ `profile` - 讀取個人資料（取得 Person ID）
   - ✅ `w_member_social` - 發布貼文
5. 確認「OAuth 2.0 Redirect URLs」包含：
   ```
   https://www.linkedin.com/developers/tools/oauth/redirect
   ```
6. 儲存設定

**步驟 2: 產生授權 URL**

使用以下格式（替換 `YOUR_CLIENT_ID`）：

```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=https://www.linkedin.com/developers/tools/oauth/redirect&scope=profile%20w_member_social&state=random_state_12345
```

**參數說明**：
- `client_id`: 你的應用程式 Client ID
- `redirect_uri`: 必須與應用程式中註冊的完全一致
- `scope`: `profile w_member_social`（用 URL 編碼：%20 代表空格）
- `state`: 隨機字串，防止 CSRF 攻擊

**步驟 3: 執行授權**

1. 將授權 URL 複製到瀏覽器
2. 登入 LinkedIn 帳號
3. 點擊「Allow」授權應用程式
4. 瀏覽器會重新導向到：
   ```
   https://www.linkedin.com/developers/tools/oauth/redirect?code=AUTHORIZATION_CODE&state=random_state_12345
   ```
5. 複製完整 URL（包括 `?code=...` 部分）

**步驟 4: 交換 Access Token**

使用 Python 腳本或 curl：

```python
import requests

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "https://www.linkedin.com/developers/tools/oauth/redirect"
AUTH_CODE = "從 callback URL 提取的授權碼"

token_url = "https://www.linkedin.com/oauth/v2/accessToken"
data = {
    "grant_type": "authorization_code",
    "code": AUTH_CODE,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

response = requests.post(token_url, data=data)
result = response.json()

access_token = result["access_token"]
expires_in = result["expires_in"]

print(f"Access Token: {access_token}")
print(f"過期時間: {expires_in} 秒 (約 {expires_in // 86400} 天)")
```

或使用 curl：

```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "redirect_uri=https://www.linkedin.com/developers/tools/oauth/redirect" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

**步驟 5: 取得 LinkedIn Person ID**

```bash
curl -H "Authorization: Bearer {ACCESS_TOKEN}" \
  "https://api.linkedin.com/v2/me"
```

**回應**：
```json
{
  "id": "785XXXX",  ← 這就是 person_id
}
```

**步驟 6: 更新資料庫**

```sql
INSERT INTO channal_info (
  channal_name,
  channal_source,
  page_id,
  access_token
) VALUES (
  'LinkedIn Profile',
  'linkedin',
  'urn:li:person:785XXXX',
  'AQXXXXXXXXXXXXXXXXXXXXXX'
);
```

---

### 快捷腳本

使用本技能提供的腳本快速取得 Access Token：

```bash
python3 .claude/skills/linkedin-post/scripts/get-token-final.py
```

腳本會引導你完成：
1. 顯示授權 URL
2. 等待你輸入 callback URL
3. 自動交換 Access Token
4. 取得 Person ID
5. 更新資料庫
6. 測試發布貼文

### 3. LinkedIn Person ID（URN）

發文需要使用 URN 格式：`urn:li:person:{person_id}`

**取得方式**：

```bash
curl -H "Authorization: Bearer {ACCESS_TOKEN}" \
  "https://api.linkedin.com/v2/userinfo"
```

**回應**：
```json
{
  "sub": "785XXXX",  ← 這就是 person_id
  "email": "...",
  "name": "..."
}
```

### 4. 資料庫設定

資料庫中的 `channal_info` 表需要包含：
- `page_id`: LinkedIn Person ID（URN 格式或純 ID）
- `access_token`: LinkedIn Access Token

## 快速開始

### 取得 LinkedIn Person ID

```bash
# 從資料庫取得
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action get-profile \
  --from-db \
  --channel-id 1

# 手動指定 token
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action get-profile \
  --access-token "YOUR_TOKEN"
```

### 發布純文字

```bash
# 方式 1：從資料庫自動取得 LinkedIn ID（推薦）
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "Hello LinkedIn! #Networking #Professional"

# 方式 2：手動指定 LinkedIn Person ID
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action text \
  --person-urn "urn:li:person:785XXXX" \
  --access-token "YOUR_TOKEN" \
  --text "Hello LinkedIn!"
```

### 發布圖片

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "Check this out! 📸" \
  --image-url "https://i.pix2.io/xxx.jpg"
```

### 發布連結

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action link \
  --from-db \
  --channel-id 1 \
  --text "Amazing article!" \
  --link-url "https://example.com/article" \
  --link-title "Article Title" \
  --link-desc "Article description"
```

## 從資料庫查找 Access Token

如果你的系統使用資料庫管理 token，可以從 `channal_info` 表中查詢：

### 查詢 LinkedIn 頻道

```bash
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT channal_id, channal_name, channal_source, page_id, access_token \
   FROM channal_info \
   WHERE channal_source = 'linkedin'"
```

### 查詢特定頻道

```bash
python3 .claude/skills/mysql/scripts/query.py \
  "SELECT channal_id, channal_name, page_id, access_token \
   FROM channal_info \
   WHERE channal_id = 1"
```

**資料庫欄位說明**：
- `channal_id`: 頻道 ID（主鍵）
- `channal_name`: 頻道名稱
- `channal_source`: 平台來源（`linkedin`）
- `page_id`: LinkedIn Person ID 或 URN（例如：`urn:li:person:785XXXX` 或 `785XXXX`）
- `access_token`: LinkedIn Access Token

## 使用方式

### 方式 1：從資料庫發布（推薦）

自動從資料庫讀取 Access Token 並取得 LinkedIn Person ID：

```bash
python3 scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "你的內容"
```

**優點**：
- ✅ 自動讀取 token（access_token 欄位）
- ✅ 自動取得 LinkedIn Person ID
- ✅ 無需手動設定參數
- ✅ 與 n8n 系統兼容

### 方式 2：手動指定參數

```bash
python3 scripts/post.py \
  --action text \
  --person-urn "urn:li:person:785XXXX" \
  --access-token "YOUR_ACCESS_TOKEN" \
  --text "你的內容"
```

## 發布流程

### 純文字發布流程

```
1. POST https://api.linkedin.com/rest/posts
   ├── author: urn:li:person:{person_id}
   ├── commentary: 貼文內容
   ├── visibility: PUBLIC
   ├── lifecycleState: PUBLISHED
   └── distribution: {feedDistribution: MAIN_FEED}

2. 完成 ✅
```

### 圖片發布流程

```
1. 註冊上傳 (POST /assets?action=registerUpload)
   ├── 返回 uploadUrl
   └── 返回 asset URN

2. 上傳圖片 (PUT uploadUrl)
   └── 二進制圖片數據

3. 發布貼文 (POST /rest/posts)
   ├── author: urn:li:person:{person_id}
   ├── content: {media: {id: asset_URN}}
   └── commentary: 說明文字

4. 完成 ✅
```

### 連結發布流程

```
1. POST https://api.linkedin.com/rest/posts
   ├── author: urn:li:person:{person_id}
   ├── commentary: 貼文內容
   ├── content: {article: {url, title, description}}
   ├── visibility: PUBLIC
   └── lifecycleState: PUBLISHED

2. LinkedIn 自動生成連結預覽

3. 完成 ✅
```

## 參數說明

| 參數 | 說明 | 必需 |
|------|------|------|
| `--action` | 執行動作 (text/image/link/get-profile) | ✅ |
| `--person-urn` | LinkedIn Person URN（手動指定時） | ❌ |
| `--from-db` | 從資料庫讀取設定 | ❌ |
| `--channel-id` | 資料庫頻道 ID | ❌ (使用 --from-db 時必需) |
| `--access-token` | Access Token | ❌ |
| `--text` | 貼文文字（最多 3,000 字符） | ✅ (action=text 時) |
| `--image-url` | 圖片 URL | ✅ (action=image 時) |
| `--link-url` | 連結 URL | ✅ (action=link 時) |
| `--link-title` | 連結標題 | ❌ (action=link 時) |
| `--link-desc` | 連結描述 | ❌ (action=link 時) |

## 限制與規範

### LinkedIn 限制

| 項目 | 限制 |
|------|------|
| 文字長度 | 最多 3,000 字符 |
| 圖片大小 | 最大 5MB |
| 圖片格式 | JPG、PNG、GIF |
| 連結預覽 | 自動生成（需 Open Graph tags） |
| 發文頻率 | 每日有速率限制 |

### 支援的格式

**圖片**：
- JPG
- PNG
- GIF

**文字**：
- 支援 Hashtags
- 支援提及（需要特殊格式）
- 支援換行

## 常見問題

### Q: 為什麼 LinkedIn 可以直接用 Access Token？

A: LinkedIn 提供 Token Generator 工具，可以直接生成 60 天有效的 Access Token，無需完整 OAuth 流程。這與其他平台類似。

### Q: LinkedIn 和其他社交媒體發文有什麼不同？

A:
1. LinkedIn 支援連結預覽（Open Graph）
2. LinkedIn 需要使用 URN 格式（`urn:li:person:{id}`）
3. LinkedIn 文字限制較長（3,000 字符）
4. LinkedIn 圖片需要先上傳註冊才能發布

### Q: OAuth state 驗證失敗怎麼辦？

A: 這是 LinkedIn Token Generator 的常見錯誤：「Oops. We can't verify the authenticity of your request because the state parameter was modified.」

**解決方案**：

**方案 1: 使用手動 OAuth 流程（推薦）**

參考「方式 B: 手動 OAuth 流程」章節，完整步驟：
1. 設定應用程式 Scopes（`profile` + `w_member_social`）
2. 產生授權 URL
3. 在瀏覽器執行授權
4. 複製 callback URL
5. 使用腳本交換 Access Token

```bash
python3 .claude/skills/linkedin-post/scripts/get-token-final.py
```

**方案 2: 清除 LinkedIn Cookies（嘗試 Token Generator）**

1. 開啟無痕視窗 (Ctrl+Shift+N)
2. 前往 Token Generator
3. 重新授權

**方案 3: 檢查 Redirect URI**

確保應用程式的「OAuth 2.0 Redirect URLs」包含：
```
https://www.linkedin.com/developers/tools/oauth/redirect
```

### Q: 如何與 pix2-upload 整合？

A: 先上傳圖片到 Pix2，再發布到 LinkedIn：

```bash
# 1. 上傳圖片到 Pix2
IMAGE_URL=$(python3 .claude/skills/pix2-upload/scripts/upload.py photo.jpg)

# 2. 發布到 LinkedIn
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "我的圖片" \
  --image-url "$IMAGE_URL"
```

### Q: LinkedIn Token 過期了怎麼辦？

A: LinkedIn Access Token 有效期 60 天，過期後需要重新生成：
1. 前往 Token Generator
2. 重新生成 Access Token
3. 更新資料庫或環境變數

## API 端點

### LinkedIn REST API

| 端點 | 方法 | 用途 |
|------|------|------|
| `/rest/posts` | POST | 建立貼文 |
| `/v2/userinfo` | GET | 取得使用者資訊（含 Person ID） |
| `/assets?action=registerUpload` | POST | 註冊圖片上傳 |

### Headers

```
LinkedIn-Version: 202210
X-Restli-Protocol-Version: 2.0.0
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json
```

## 範例

### 範例 1：發布文字貼文

```bash
python3 scripts/post.py \
  --action text \
  --from-db \
  --channel-id 1 \
  --text "Excited to share our latest project! 🚀

We've been working hard on this...

#Innovation #Tech #Leadership"
```

### 範例 2：發布圖片貼文

```bash
python3 scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "Behind the scenes at our office 📸" \
  --image-url "https://i.pix2.io/office.jpg"
```

### 範例 3：發布連結貼文

```bash
python3 scripts/post.py \
  --action link \
  --from-db \
  --channel-id 1 \
  --text "Great article on industry trends!" \
  --link-url "https://example.com/article" \
  --link-title "Industry Trends 2025" \
  --link-desc "Explore the latest trends..."
```

## 與其他技能整合

### social-content-writer

```bash
# 1. 生成 LinkedIn 內容
python3 .claude/skills/social-content-writer/scripts/write-content.py \
  --topic "新產品發布" \
  --platform linkedin \
  --framework pas \
  --output linkedin_content.json

# 2. 生成圖片
python3 .claude/skills/social-content-writer/scripts/prompt-generator.py \
  --content linkedin_content.json \
  --type image \
  --auto-generate \
  --upload-pix2

# 3. 讀取生成的圖片 URL
IMAGE_URL=$(jq -r '.prompts.image[0].url' linkedin_content.json)

# 4. 發布到 LinkedIn
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "$(jq -r '.content' linkedin_content.json)" \
  --image-url "$IMAGE_URL"
```

### 多平台同時發布

```bash
# 同時發布到多個平台

TEXT="Check out our new product! 🚀"
IMAGE_URL="https://i.pix2.io/product.jpg"

# LinkedIn
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 1 \
  --text "$TEXT" \
  --image-url "$IMAGE_URL"

# Facebook
python3 .claude/skills/facebook-page-post/scripts/post.py photo \
  --message "$TEXT" \
  --file product.jpg

# Threads
python3 .claude/skills/threads-post/scripts/post.py \
  --action image \
  --from-db \
  --channel-id 3 \
  --text "$TEXT" \
  --image-url "$IMAGE_URL"
```

## 注意事項

1. **Access Token 有效期**
   - Token 有效期 60 天
   - 過期需要重新生成

2. **Rate Limiting**
   - LinkedIn 有速率限制
   - 避免短時間大量發文

3. **連結預覽**
   - 需要目標網站有 Open Graph tags
   - LinkedIn 會自動抓取預覽

4. **內容規範**
   - 遵守 LinkedIn 專業社群指導原則
   - 避免違規內容

5. **URN 格式**
   - Person URN: `urn:li:person:{person_id}`
   - Organization URN: `urn:li:organization:{org_id}`

6. **公司頁面發文**
   - 需要 `w_organization_social` scope
   - 使用 Organization URN 作為 author

## 授權

MIT License
