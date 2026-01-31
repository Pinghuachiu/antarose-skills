#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手動取得 LinkedIn Access Token
複製授權碼並手動輸入
"""

import requests
import sys

# 配置（從環境變數取得）
import os
CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:9999/callback"
SCOPES = "w_member_social"

# 檢查參數
if not CLIENT_ID or not CLIENT_SECRET:
    print("❌ 錯誤: 請設定環境變數 LINKEDIN_CLIENT_ID 和 LINKEDIN_CLIENT_SECRET")
    print("\n範例:")
    print("  export LINKEDIN_CLIENT_ID='your_client_id'")
    print("  export LINKEDIN_CLIENT_SECRET='your_client_secret'")
    print("  python3 scripts/get-token-manual.py")
    sys.exit(1)

# 生成授權 URL
params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPES,
    "state": "random_state_12345"
}

auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{params['response_type']}&client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&scope={params['scope']}&state={params['state']}"

print("=" * 70)
print("🔑 LinkedIn Access Token 取得工具")
print("=" * 70)
print("\n📱 步驟 1: 在瀏覽器中授權")
print("-" * 70)
print("\n1. 複製下面的 URL 到瀏覽器中開啟:\n")
print(auth_url)
print("\n2. 登入你的 LinkedIn 帳號")
print("3. 點擊「Allow」授權應用程式")
print("4. 瀏覽器會重新導向到 localhost 頁面（顯示錯誤是正常的）")
print("5. 從瀏覽器網址列複製整個 URL")
print("6. 粘貼到下面\n")

# 讓用戶輸入 callback URL
callback_url = input("📋 請粘貼瀏覽器重新導向的完整 URL: ").strip()

# 解析授權碼
if "code=" not in callback_url:
    print("\n❌ URL 中沒有找到授權碼")
    print(f"   你輸入的 URL: {callback_url}")
    sys.exit(1)

# 從 URL 中提取 code
auth_code = callback_url.split("code=")[1].split("&")[0] if "&" in callback_url else callback_url.split("code=")[1]

print(f"\n✅ 成功提取授權碼: {auth_code[:20]}...")

print("\n" + "=" * 70)
print("🔑 步驟 2: 交換 Access Token")
print("-" * 70)

# 交換 Access Token
token_url = "https://www.linkedin.com/oauth/v2/accessToken"
data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

try:
    print("正在請求 Access Token...")

    response = requests.post(token_url, data=data, timeout=30)
    response.raise_for_status()

    result = response.json()

    if "access_token" in result:
        access_token = result["access_token"]
        expires_in = result.get("expires_in", 0)

        print("\n" + "=" * 70)
        print("✅ 成功取得 Access Token！")
        print("=" * 70)
        print(f"\n🔑 Access Token:\n")
        print(f"   {access_token}")
        print(f"\n⏰ 過期時間: {expires_in} 秒 (約 {expires_in // 86400} 天)")
        print(f"\n📝 將此 Token 存入資料庫或環境變數:")
        print(f"\n   export LINKEDIN_ACCESS_TOKEN=\"{access_token}\"\n")

        # 測試 Token
        print("=" * 70)
        print("🧪 測試 Access Token")
        print("-" * 70)

        userinfo_response = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30
        )

        if userinfo_response.status_code == 200:
            userinfo = userinfo_response.json()
            person_id = userinfo.get("sub", "N/A")
            name = userinfo.get("name", "N/A")
            email = userinfo.get("email", "N/A")

            print(f"\n✅ Token 有效！")
            print(f"   姓名: {name}")
            print(f"   Email: {email}")
            print(f"   Person ID: {person_id}")
            print(f"   URN: urn:li:person:{person_id}")

            # 更新資料庫
            print("\n" + "=" * 70)
            print("💾 更新資料庫")
            print("-" * 70)

            import mysql.connector

            try:
                conn = mysql.connector.connect(
                    host=os.environ.get("MYSQL_HOST"),
                    user=os.environ.get("MYSQL_USER"),
                    password=os.environ.get("MYSQL_PASSWORD"),
                    database=os.environ.get("MYSQL_DATABASE")
                )
                cursor = conn.cursor(dictionary=True)

                # 檢查是否已有 LinkedIn 頻道
                cursor.execute(
                    "SELECT channal_id FROM channal_info WHERE channal_source = 'linkedin'"
                )
                existing = cursor.fetchone()

                if existing:
                    # 更新
                    channel_id = existing["channal_id"]
                    cursor.execute("""
                        UPDATE channal_info
                        SET page_id = %s, access_token = %s
                        WHERE channal_id = %s
                    """, (f"urn:li:person:{person_id}", access_token, channel_id))
                    print(f"\n✅ 已更新頻道 ID {channel_id}")
                else:
                    # 新增
                    cursor.execute("""
                        INSERT INTO channal_info (channal_name, channal_source, page_id, access_token)
                        VALUES (%s, %s, %s, %s)
                    """, (f"{name}'s LinkedIn", "linkedin", f"urn:li:person:{person_id}", access_token))
                    print(f"\n✅ 已新增 LinkedIn 頻道到資料庫")

                conn.commit()
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"\n⚠️  資料庫更新失敗: {e}")
                print("   請手動更新資料庫")
                print("\n   SQL 指令:")
                print(f"   UPDATE channal_info")
                print(f"   SET access_token = '{access_token}',")
                print(f"       page_id = 'urn:li:person:{person_id}'")
                print(f"   WHERE channal_source = 'linkedin';")

        else:
            print(f"\n⚠️  Token 測試失敗 (HTTP {userinfo_response.status_code})")
            print(f"   回應: {userinfo_response.text}")

        # 顯示測試指令
        print("\n" + "=" * 70)
        print("📝 測試發布貼文")
        print("-" * 70)
        print(f"\npython3 .claude/skills/linkedin-post/scripts/post.py \\")
        print(f"  --action text \\")
        print(f"  --from-db \\")
        print(f"  --channel-id 1 \\")
        print(f'  --text "Hello from LinkedIn API! 🚀"')

    else:
        print("\n❌ 回應中沒有 access_token")
        print(f"   完整回應: {result}")

except requests.exceptions.HTTPError as e:
    print(f"\n❌ 請求失敗: {e}")
    print(f"   HTTP 狀態碼: {e.response.status_code}")
    print(f"   回應: {e.response.text}")

    if e.response.status_code == 400:
        print("\n可能的原因:")
        print("  - 授權碼已過期（10 分鐘）")
        print("  - 授權碼已被使用")
        print("  - redirect_uri 不匹配")

except Exception as e:
    print(f"\n❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
