#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Access Token 取得腳本
手動執行 OAuth 2.0 流程取得 Access Token
"""

import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import threading
import time

# 配置
CLIENT_ID = input("請輸入 LinkedIn 應用程式的 Client ID: ").strip()
REDIRECT_URI = "http://localhost:8080/callback"
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

print("=" * 60)
print("📱 步驟 1: 授權應用程式")
print("=" * 60)
print(f"\n在瀏覽器中開啟以下 URL:\n")
print(auth_url)
print("\n或將自動開啟瀏覽器...")

# 自動開啟瀏覽器
webbrowser.open(auth_url)

# 本地伺服器接收 callback
auth_code = None

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        if self.path.startswith("/callback"):
            # 解析 query 參數
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)

            if "code" in params:
                auth_code = params["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Authorization Successful!</h1><p>You can close this window.</p>")
                print("\n✅ 授權成功！")
                print(f"   Authorization Code: {auth_code[:20]}...")
            elif "error" in params:
                error = params["error"][0]
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f"<h1>Authorization Failed</h1><p>Error: {error}</p>".encode())
                print(f"\n❌ 授權失敗: {error}")
            else:
                self.send_response(400)
                self.end_headers()

    def log_message(self, format, *args):
        pass  # 抑制 log 訊息

# 啟動本地伺服器
server = HTTPServer(("localhost", 8080), CallbackHandler)
thread = threading.Thread(target=server.handle_request)
thread.daemon = True
thread.start()

# 等待 callback
print("\n⏳ 等待授權 callback...")
print("   (本地伺服器運行在 http://localhost:8080)")
for i in range(30, 0, -5):
    print(f"   等待中... {i} 秒")
    time.sleep(5)
    if auth_code:
        break

server.shutdown()

if not auth_code:
    print("\n❌ 未收到授權碼，請重試")
    exit(1)

print("\n" + "=" * 60)
print("🔑 步驟 2: 交換 Access Token")
print("=" * 60)

CLIENT_SECRET = input("請輸入 LinkedIn 應用程式的 Client Secret: ").strip()

# 交換 Access Token
import requests

token_url = "https://www.linkedin.com/oauth/v2/accessToken"
data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

print("\n正在請求 Access Token...")

try:
    response = requests.post(token_url, data=data)
    response.raise_for_status()

    result = response.json()

    if "access_token" in result:
        access_token = result["access_token"]
        expires_in = result.get("expires_in", 0)

        print("\n" + "=" * 60)
        print("✅ 成功取得 Access Token！")
        print("=" * 60)
        print(f"\nAccess Token:\n{access_token}")
        print(f"\n過期時間: {expires_in} 秒 ({expires_in // 86400} 天)")
        print("\n請將此 Token 存入資料庫或環境變數:")
        print(f"export LINKEDIN_ACCESS_TOKEN=\"{access_token}\"")

        # 測試 Token
        print("\n" + "=" * 60)
        print("🧪 測試 Access Token")
        print("=" * 60)

        userinfo_response = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if userinfo_response.status_code == 200:
            userinfo = userinfo_response.json()
            print(f"\n✅ Token 有效！")
            print(f"   姓名: {userinfo.get('name', 'N/A')}")
            print(f"   Person ID: {userinfo.get('sub', 'N/A')}")
            print(f"   URN: urn:li:person:{userinfo.get('sub', 'N/A')}")
        else:
            print(f"\n⚠️  Token 測試失敗: {userinfo_response.status_code}")

    else:
        print("\n❌ 回應中沒有 access_token")
        print(f"回應: {result}")

except requests.exceptions.HTTPError as e:
    print(f"\n❌ 請求失敗: {e}")
    print(f"回應: {e.response.text}")
except Exception as e:
    print(f"\n❌ 錯誤: {e}")
