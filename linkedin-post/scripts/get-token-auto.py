#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速取得 LinkedIn Access Token
使用預設的 Client ID 和 Client Secret
"""

import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import requests
import sys
import os

# 配置（從環境變數或命令行參數取得）
CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:9999/callback"
SCOPES = "w_member_social"

# 生成授權 URL
params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPES,
    "state": "random_state_12345"
}

auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urllib.parse.urlencode(params)}"

print("=" * 70)
print("🔑 LinkedIn Access Token 取得工具")
print("=" * 70)
print("\n📱 步驟 1: 在瀏覽器中授權應用程式")
print("-" * 70)
print(f"\n請在瀏覽器中開啟以下 URL 並授權:\n")
print(f"   {auth_url}\n")

auth_code = None

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        if self.path.startswith("/callback"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)

            if "code" in params:
                auth_code = params["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                html = """
                <html>
                <head><title>授權成功</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: green;">✅ 授權成功！</h1>
                    <p>Access Token 已取得，請回到終端機查看。</p>
                    <p>你可以關閉這個視窗。</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode("utf-8"))
                print("\n✅ 收到授權碼！")
            elif "error" in params:
                error = params["error"][0]
                error_description = params.get("error_description", [""])[0]
                self.send_response(400)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                html = f"""
                <html>
                <head><title>授權失敗</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: red;">❌ 授權失敗</h1>
                    <p>錯誤: {error}</p>
                    <p>{error_description}</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode("utf-8"))
                print(f"\n❌ 授權失敗: {error}")
                print(f"   描述: {error_description}")
            else:
                self.send_response(400)
                self.end_headers()

    def log_message(self, format, *args):
        pass  # 抑制 log 訊息

print("⏳ 正在啟動本地伺服器...")
print(f"   監聽: {REDIRECT_URI}")
print("\n💡 提示:")
print("   - 瀏覽器會自動開啟（或手動複製上面的 URL）")
print("   - 登入 LinkedIn 並授權應用程式")
print("   - 授權後會自動回到 localhost")
print("   - 然後本程式會自動取得 Access Token")

# 嘗試自動開啟瀏覽器
try:
    webbrowser.open(auth_url)
    print("\n🌐 已嘗試自動開啟瀏覽器...")
except:
    print("\n⚠️  無法自動開啟瀏覽器，請手動複製上面的 URL")

# 啟動本地伺服器
try:
    server = HTTPServer(("localhost", 9999), CallbackHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.daemon = True
    thread.start()

    # 等待 callback
    print("\n⏳ 等待授權 callback (最多等待 2 分鐘)...\n")
    for i in range(120, 0, -5):
        if auth_code:
            break
        if i % 15 == 0:
            print(f"   等待中... {i // 60} 分 {i % 60} 秒")
        time.sleep(5)

    server.server_close()

except OSError as e:
    print(f"\n❌ 無法啟動伺服器 (端口 9999 可能被佔用): {e}")
    print("\n替代方案:")
    print("1. 使用不同的端口")
    print("2. 手動完成 OAuth 流程")
    sys.exit(1)

if not auth_code:
    print("\n❌ 未收到授權碼，請重試")
    print("   可能原因:")
    print("   - 沒有在瀏覽器中完成授權")
    print("   - 瀏覽器被重新導向到錯誤的 URL")
    print("   - 網路連線問題")
    sys.exit(1)

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

            print(f"\n✅ Token 有效！")
            print(f"   姓名: {name}")
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
                    print(f"\n✅ 已新增頻道")

                conn.commit()
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"\n⚠️  資料庫更新失敗: {e}")
                print("   請手動更新資料庫")

        else:
            print(f"\n⚠️  Token 測試失敗 (HTTP {userinfo_response.status_code})")
            print(f"   回應: {userinfo_response.text}")

    else:
        print("\n❌ 回應中沒有 access_token")
        print(f"   回應: {result}")

except requests.exceptions.HTTPError as e:
    print(f"\n❌ 請求失敗: {e}")
    print(f"   HTTP 狀態碼: {e.response.status_code}")
    print(f"   回應: {e.response.text}")
except Exception as e:
    print(f"\n❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
