# Token 管理範例

## 檢查 Token 狀態

### 基本檢查

```bash
python3 .claude/skills/facebook-page-post/scripts/token-helper.py
```

輸出示例:
```
============================================================
📋 Facebook Page Access Token 資訊
============================================================

📱 App ID: 123456789012345
🔑 類型: PAGE
✅ 是否有效: 是

⏰ 過期時間: 2026-03-29 12:34:56
   剩餘天數: 58 天

🔐 權限:
   • pages_manage_posts
   • pages_read_engagement
   • pages_manage_engagement

✅ 所有必要權限都已授予

============================================================
```

### Token 即將過期

```bash
python3 .claude/skills/facebook-page-post/scripts/token-helper.py
```

輸出:
```
============================================================
📋 Facebook Page Access Token 資訊
============================================================

📱 App ID: 123456789012345
🔑 類型: PAGE
✅ 是否有效: 是

⏰ 過期時間: 2026-02-05 12:34:56
   剩餘天數: 5 天

⚠️⚠️⚠️  警告: Token 即將過期! ⚠️⚠️⚠️

   請立即更新 Token 以避免服務中斷
   更新步驟:
   1. 前往 Facebook Graph API Explorer
   2. 重新取得 Page Access Token
   3. 更新環境變數:
      export FACEBOOK_PAGE_ACCESS_TOKEN="new-token"
   4. 再次執行此腳本確認

============================================================
```

### Token 已過期

```bash
python3 .claude/skills/facebook-page-post/scripts/token-helper.py
```

輸出:
```
❌ Token 驗證失敗!
   錯誤碼: 190
   錯誤訊息: Access token has expired

可能的原因:
  1. Token 已過期（超過 60 天）
  2. Token 無效或格式錯誤
  3. 缺少必要的權限

解決方法:
  請參考 SKILL.md 重新取得 Page Access Token
```

### Token 無效

```bash
❌ 錯誤: FACEBOOK_PAGE_ACCESS_TOKEN 環境變數未設定

請先設定環境變數:
  export FACEBOOK_PAGE_ACCESS_TOKEN="your-token-here"

取得 Token 的詳細步驟請參考 SKILL.md 的 Token 管理章節
```

## 取得新的 Page Access Token

### 步驟 1: 存取 Graph API Explorer

1. 前往: https://developers.facebook.com/tools/explorer/
2. 從下拉選單選擇你的 Facebook App
3. 如果沒有 App，建立一個新的

### 步驟 2: 取得 User Access Token

1. 點擊 "Get User Access Token" 按鈕
2. 在彈出的視窗中，勾選以下權限:
   - ✅ `pages_manage_posts` - 管理貼文
   - ✅ `pages_read_engagement` - 讀取互動數據
   - ✅ `pages_manage_engagement` - 管理互動
   - ✅ `pages_show_list` - 顯示管理的專頁列表（可選）
3. 點擊 "Generate Access Token"

### 步驟 3: 取得 Page Access Token

在 Graph API Explorer 的查詢框中輸入:

```
GET /me/accounts
```

或指定專頁 ID:

```
GET /{page-id}?fields=access_token,name
```

點擊 "Submit" 後，你會看到回應:

```json
{
  "data": [
    {
      "access_token": "EAAxxxxxx...",
      "category": "Software",
      "id": "1234567890",
      "name": "Your Page Name"
    }
  ]
}
```

複製 `access_token` 的值。

### 步驟 4: 延長 Token 有效期（可選）

#### 方法 A: 使用 "Extend Access Token" 按鈕

1. 在 Graph API Explorer 中，點擊 "Extend Access Token" 按鈕
2. 確認延長後，Token 將變成永久有效

#### 方法 B: 使用 API 呼叫

```
GET /oauth/access_token?
  grant_type=fb_exchange_token&
  client_id={your-app-id}&
  client_secret={your-app-secret}&
  fb_exchange_token={short-lived-token}
```

### 步驟 5: 設定環境變數

```bash
# Linux/Mac
export FACEBOOK_PAGE_ACCESS_TOKEN="EAAxxxxxx..."

# Windows (CMD)
set FACEBOOK_PAGE_ACCESS_TOKEN=EAAxxxxxx...

# Windows (PowerShell)
$env:FACEBOOK_PAGE_ACCESS_TOKEN="EAAxxxxxx..."
```

### 步驟 6: 驗證新 Token

```bash
python3 .claude/skills/facebook-page-post/scripts/token-helper.py
```

確認顯示 "✅ 是否有效: 是" 和剩餘天數。

## 永久 Token 取得方法 (2025)

### 完整步驟

1. **建立 Facebook App**
   - 前往: https://developers.facebook.com/apps/
   - 點擊 "Add a New App"
   - 選擇應用類型（例如: "Business"）
   - 填寫基本資訊

2. **設定 App**
   - 在 App Dashboard 中
   - 前往 "App Settings" > "Basic"
   - 複製 "App ID" 和 "App Secret"

3. **使用 Graph API Explorer**
   - 前往: https://developers.facebook.com/tools/explorer/
   - 選擇你剛建立的 App
   - 點擊 "Get User Access Token"
   - 勾選權限:
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `pages_manage_engagement`
   - 生成 Token

4. **取得 Page Token**
   - 在 Explorer 中執行: `GET /me/accounts`
   - 找到你的 Page
   - 複製 `access_token`

5. **延長為永久 Token**
   - 點擊 "Extend Access Token" 按鈕
   - 確認延長
   - 這個 Token 現在是永久有效的

6. **驗證**
   - 執行 token-helper.py
   - 應該顯示 "♾️  過期時間: 永不過期"

## 更新環境變數

### 臨時設定（當前終端機）

```bash
export FACEBOOK_PAGE_ACCESS_TOKEN="new-token-here"
```

### 永久設定

#### Linux/Mac - 添加到 ~/.bashrc 或 ~/.zshrc

```bash
# 編輯 ~/.bashrc
nano ~/.bashrc

# 添加以下行
export FACEBOOK_PAGE_ACCESS_TOKEN="your-token-here"

# 重新載入
source ~/.bashrc
```

#### Windows - 系統環境變數

1. 右鍵點擊 "此電腦" > "內容"
2. 點擊 "進階系統設定"
3. 點擊 "環境變數"
4. 在 "使用者變數" 中新增:
   - 變數名稱: `FACEBOOK_PAGE_ACCESS_TOKEN`
   - 變數值: `your-token-here`

#### 使用 .env 檔案

建立 `.env` 檔案:

```bash
FACEBOOK_PAGE_ID="your-page-id"
FACEBOOK_PAGE_ACCESS_TOKEN="your-token-here"
```

在 Python 中載入:

```python
from dotenv import load_dotenv
load_dotenv()

import os
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
```

**重要**: 記得將 `.env` 加入 `.gitignore`:

```bash
echo ".env" >> .gitignore
```

## Token 備份

### 安全備份

1. **使用密碼管理器**
   - LastPass
   - 1Password
   - Bitwarden

2. **加密儲存**

```bash
# 使用 GPG 加密
echo "your-token" | gpg -e -r your@email.com > token.gpg

# 解密
gpg -d token.gpg
```

3. **雲端儲存（加密後）**
   - Google Drive
   - Dropbox
   - OneDrive

## 定期檢查腳本

### 自動檢查腳本

建立 `check_token.sh`:

```bash
#!/bin/bash
# 每週檢查 Token 狀態

echo "檢查 Facebook Token 狀態..."
python3 .claude/skills/facebook-page-post/scripts/token-helper.py

# 檢查退出碼
if [ $? -ne 0 ]; then
    echo "❌ Token 檢查失敗"
    # 發送通知（可選）
    # sendmail you@example.com <<EOF
    # Subject: Facebook Token 檢查失敗
    #
    # 請檢查你的 Facebook Page Access Token
    # EOF
fi
```

設定 cron 任務:

```bash
# 每週一早上 9 點檢查
0 9 * * 1 /path/to/check_token.sh >> /var/log/token_check.log 2>&1
```

### Python 檢查腳本

建立 `check_token.py`:

```python
#!/usr/bin/env python3
"""
檢查 Token 並發送警告
"""
import subprocess
import sys
from datetime import datetime

def check_token():
    result = subprocess.run(
        ["python3", ".claude/skills/facebook-page-post/scripts/token-helper.py"],
        capture_output=True,
        text=True
    )

    output = result.stdout
    print(output)

    # 檢查是否包含警告
    if "剩餘天數" in output:
        # 提取天數
        for line in output.split('\n'):
            if "剩餘天數" in line:
                days = int(line.split(':')[1].strip().split()[0])
                if days < 7:
                    print(f"⚠️  警告: Token 將在 {days} 天內過期!")
                    # 可以在這裡添加通知邏輯

if __name__ == "__main__":
    check_token()
```

## 常見問題

### Q: Token 過期後會怎樣?

A: 過期後無法發文，會看到錯誤訊息:
```
⚠️  錯誤: Access Token 已過期或無效
```

### Q: 如何避免 Token 過期?

A: 使用永久 Token 方法（見上文），或定期在過期前更新。

### Q: Token 在哪裡過期最快?

A: 以下情況會導致 Token 提前失效:
- 變更 Facebook 密碼
- 移除 App 權限
- 刪除 Facebook App
- 60 天期限到達

### Q: 可以使用同一個 Token 給多個專案嗎?

A: 可以，但建議為不同專案建立不同的 App 和 Token。

### Q: Token 被盜用怎麼辦?

A: 立即在 Facebook 中移除 App 權限:
1. 前往: https://www.facebook.com/settings?tab=applications
2. 找到你的 App
3. 點擊 "移除"

### Q: 如何測試 Token 是否有效?

A: 使用 token-helper.py 或直接測試 API:
```bash
curl "https://graph.facebook.com/v24.0/me?access_token=YOUR_TOKEN"
```

## 安全最佳實踐

1. ✅ 使用環境變數儲存 Token
2. ✅ 定期檢查 Token 有效期
3. ✅ 設定過期提醒
4. ✅ 加密備份 Token
5. ✅ 使用不同的 App 和 Token 給不同環境
6. ❌ 不要將 Token 提交到 Git
7. ❌ 不要在前端程式碼中使用 Token
8. ❌ 不要與他人分享 Token
9. ❌ 不要在公開場所顯示 Token
10. ✅ Token 洩露時立即撤銷並重新生成

## 參考連結

- [Facebook Page Access Tokens](https://developers.facebook.com/docs/pages/access-tokens/)
- [Get Long-Lived Tokens](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/)
- [Debug Token Tool](https://developers.facebook.com/tools/debug/accesstoken/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Never-Expiring Token Guide (2025)](https://www.software-mirrors.com/blog/how-to-get-a-never-expiring-facebook-page-access-token-in-2025-step-by-step)
