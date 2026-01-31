# LinkedIn Post - OAuth State 錯誤解決方案

## 錯誤訊息

```
Oops. We can't verify the authenticity of your request because the state parameter was modified.
```

## 什麼是 State 參數？

OAuth 2.0 中的 `state` 參數是一個安全機制，用於防止 CSRF (Cross-Site Request Forgery) 攻擊：

1. 你的應用程式發送授權請求時，生成一個隨機的 `state` 值
2. LinkedIn 會在回傳時附上相同的 `state` 值
3. 應用程式驗證 `state` 是否匹配
4. 如果不匹配，就會出現「state parameter was modified」錯誤

## 常見原因

1. ✅ **授權碼已使用** - Authorization code 只能使用一次
2. ✅ **授權碼過期** - 通常 5-10 分鐘後過期
3. ✅ **State 不匹配** - 會話中斷或逾時
4. ✅ **重複請求** - 重新整理或重複提交

## 解決方案：使用 Token Generator（推薦）⭐

**不需要完整 OAuth 流程！**

### 步驟 1: 建立 LinkedIn Application

1. 前往: https://www.linkedin.com/developers/apps/new
2. 填寫應用程式資訊
3. 驗證應用程式
4. 啟用產品:
   - Share on LinkedIn
   - Sign In with LinkedIn using OpenID Connect
5. 設定 OAuth 2.0 Scopes: `w_member_social`

### 步驟 2: 使用 Token Generator

1. **前往 Token Generator**:
   ```
   https://www.linkedin.com/developers/tools/oauth/token-generator
   ```

2. **選擇你的應用程式**

3. **勾選 Scopes**:
   - ✅ `w_member_social`（必需）
   - ✅ `w_organization_social`（可選，用於公司頁面）
   - ✅ `r_emailaddress`（可選）
   - ✅ `r_liteprofile`（可選）

4. **點擊「Request access token」**

5. **複製 Access Token**:
   - 格式: `AQXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
   - 有效期: **60 天**

### 步驟 3: 測試 Access Token

```bash
curl -H "Authorization: Bearer {YOUR_ACCESS_TOKEN}" \
  "https://api.linkedin.com/v2/userinfo"
```

**成功回應**:
```json
{
  "sub": "785XXXX",
  "email": "your@email.com",
  "name": "Your Name"
}
```

### 步驟 4: 使用 Access Token 發文

```bash
python3 .claude/skills/linkedin-post/scripts/post.py \
  --action text \
  --person-urn "urn:li:person:785XXXX" \
  --access-token "YOUR_ACCESS_TOKEN" \
  --text "Hello LinkedIn! 🚀"
```

## 對照表：OAuth vs Token Generator

| 特性 | OAuth 2.0 Flow | Token Generator |
|------|---------------|-----------------|
| 設定時間 | 1-2 小時 | 5 分鐘 |
| 需要伺服器 | ✅ 是 | ❌ 否 |
| 需要處理 callback | ✅ 是 | ❌ 否 |
| Token 有效期 | 60 天 | 60 天 |
| 適合場景 | 生產環境、多用戶 | 個人使用、自動化 |
| 難度 | 中等 | 簡單 |

## 資料庫整合

將 Access Token 存入資料庫：

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
  'AQXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
);
```

## Token 過期處理

LinkedIn Access Token 有效期為 **60 天**。過期後：

1. 重新前往 Token Generator
2. 生成新的 Access Token
3. 更新資料庫或環境變數

**提醒**: 可以設定 50 天後自動提醒更新。

## n8n 整合

如果你在 n8n 中遇到 OAuth state 錯誤：

### 選項 1: 使用 Token Generator

1. 使用本技能的 `--from-db` 模式
2. 將 Token Generator 生成的 token 存入資料庫
3. n8n 呼叫腳本時使用 `--from-db --channel-id N`

### 選項 2: 修復 n8n OAuth

1. 清除 n8n LinkedIn credentials
2. 重新建立 OAuth 連接
3. 確保沒有重複使用授權碼
4. 檢查 redirect URI 設定

## 常見問題

### Q: 為什麼不直接修復 OAuth？

A: OAuth 流程複雜，需要：
- 應用程式驗證
- Callback URL 設定
- 會話管理
- State 參數處理

Token Generator 更簡單快速，適合個人自動化。

### Q: Token Generator 安全嗎？

A: 是的， LinkedIn 官方工具：
- 官方提供，非第三方
- 生成標準 OAuth token
- 適合生產環境使用
- 60 天後需重新生成

### Q: 可以自動刷新 Token 嗎？

A: LinkedIn 提供 refresh token，但需要初始 OAuth 流程。
Token Generator 方式需要手動更新（60 天一次）。

### Q: 公司頁面發文怎麼辦？

A: 使用 `w_organization_social` scope：
1. 在 Token Generator 勾選該 scope
2. 取得的 token 可以發文到你有權限的公司頁面
3. 使用 `urn:li:organization:{ORG_ID}` 作為 author

## 總結

對於個人自動化或 n8n 整合，**推薦使用 Token Generator**：

✅ 簡單快速
✅ 無需 OAuth 流程
✅ 官方工具
✅ 60 天有效期
✅ 與其他社交媒體技能一致

---

**相關資源**:
- [LinkedIn Token Generator](https://www.linkedin.com/developers/tools/oauth/token-generator)
- [LinkedIn API 文檔](https://learn.microsoft.com/en-us/linkedin/shared/references/v2/api/)
- [OAuth 2.0 State 參數說明](https://oauth.net/2/#state)
