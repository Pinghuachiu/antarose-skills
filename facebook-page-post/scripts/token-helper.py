#!/usr/bin/env python3
"""
Facebook Page Access Token Helper
檢查 Token 有效期和除錯資訊
"""

import os
import sys
import requests
from datetime import datetime

# Configuration
ACCESS_TOKEN = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
API_VERSION = "v24.0"


def format_timestamp(timestamp):
    """格式化時間戳記為可讀格式"""
    if not timestamp:
        return "未知"

    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "無效"


def calculate_days_left(expires_at):
    """計算剩餘天數"""
    if not expires_at:
        return None

    try:
        expires_dt = datetime.fromtimestamp(expires_at)
        now = datetime.now()
        delta = expires_dt - now
        return delta.days
    except:
        return None


def debug_token():
    """檢查 Token 資訊"""
    if not ACCESS_TOKEN:
        print("❌ 錯誤: FACEBOOK_PAGE_ACCESS_TOKEN 環境變數未設定", file=sys.stderr)
        print()
        print("請先設定環境變數:")
        print("  export FACEBOOK_PAGE_ACCESS_TOKEN=\"your-token-here\"")
        print()
        print("取得 Token 的詳細步驟請參考 SKILL.md 的 Token 管理章節", file=sys.stderr)
        sys.exit(1)

    url = f"https://graph.facebook.com/{API_VERSION}/debug_token"
    payload = {
        "input_token": ACCESS_TOKEN,
        "access_token": ACCESS_TOKEN
    }

    try:
        response = requests.get(url, params=payload)

        # 檢查是否為認證錯誤
        if response.status_code == 401 or response.status_code == 400:
            error_data = response.json()
            error = error_data.get('error', {})
            print(f"❌ Token 驗證失敗!", file=sys.stderr)
            print(f"   錯誤碼: {error.get('code')}", file=sys.stderr)
            print(f"   錯誤訊息: {error.get('message')}", file=sys.stderr)
            print()
            print("可能的原因:", file=sys.stderr)
            print("  1. Token 已過期（超過 60 天）", file=sys.stderr)
            print("  2. Token 無效或格式錯誤", file=sys.stderr)
            print("  3. 缺少必要的權限", file=sys.stderr)
            print()
            print("解決方法:", file=sys.stderr)
            print("  請參考 SKILL.md 重新取得 Page Access Token", file=sys.stderr)
            sys.exit(1)

        response.raise_for_status()
        data = response.json()

        if "data" not in data:
            print("❌ 錯誤: 無法解析 API 回應", file=sys.stderr)
            sys.exit(1)

        token_data = data["data"]

        # 顯示 Token 資訊
        print("=" * 60)
        print("📋 Facebook Page Access Token 資訊")
        print("=" * 60)
        print()

        # App ID
        app_id = token_data.get("app_id")
        if app_id:
            print(f"📱 App ID: {app_id}")

        # Token 類型
        token_type = token_data.get("type")
        if token_type:
            type_emoji = "🔑" if token_type == "PAGE" else "👤"
            print(f"{type_emoji} 類型: {token_type}")

        # 是否有效
        is_valid = token_data.get("is_valid")
        if is_valid is not None:
            validity_emoji = "✅" if is_valid else "❌"
            print(f"{validity_emoji} 是否有效: {'是' if is_valid else '否'}")

            if not is_valid:
                print()
                print("⚠️  Token 無效，請重新取得 Page Access Token")
                print("   詳細步驟請參考 SKILL.md 的 Token 管理章節")
                sys.exit(1)

        print()

        # 過期時間
        expires_at = token_data.get("expires_at")
        if expires_at:
            expires_str = format_timestamp(expires_at)
            print(f"⏰ 過期時間: {expires_str}")

            # 計算剩餘天數
            days_left = calculate_days_left(expires_at)
            if days_left is not None:
                if days_left > 0:
                    print(f"   剩餘天數: {days_left} 天")

                    # 根據剩餘天數顯示警告
                    if days_left <= 7:
                        print()
                        print("⚠️⚠️⚠️  警告: Token 即將過期! ⚠️⚠️⚠️")
                        print()
                        print("   請立即更新 Token 以避免服務中斷")
                        print("   更新步驟:")
                        print("   1. 前往 Facebook Graph API Explorer")
                        print("   2. 重新取得 Page Access Token")
                        print("   3. 更新環境變數:")
                        print("      export FACEBOOK_PAGE_ACCESS_TOKEN=\"new-token\"")
                        print("   4. 再次執行此腳本確認")
                    elif days_left <= 30:
                        print()
                        print("💡 提示: Token 將在 30 天內過期，建議盡快更新")
                elif days_left == 0:
                    print()
                    print("⚠️⚠️⚠️  警告: Token 今天就會過期! ⚠️⚠️⚠️")
                    print("   請立即更新 Token")
                else:
                    print()
                    print("⚠️  Token 已過期，請立即更新")
            else:
                print("   (永久 Token)")
        else:
            print("♾️  過期時間: 永不過期")

        print()

        # 權限
        scopes = token_data.get("granular_scopes", [])
        if scopes:
            print("🔐 權限:")
            for scope in scopes:
                scope_name = scope.get("scope", "未知")
                print(f"   • {scope_name}")

            # 檢查必要權限
            required_permissions = ["pages_manage_posts", "pages_read_engagement", "pages_manage_engagement"]
            current_permissions = [s.get("scope") for s in scopes]

            print()
            missing_permissions = [p for p in required_permissions if p not in current_permissions]

            if missing_permissions:
                print("⚠️  缺少必要權限:")
                for perm in missing_permissions:
                    print(f"   • {perm}")
                print()
                print("請在取得 Token 時勾選這些權限")
            else:
                print("✅ 所有必要權限都已授予")

        print()
        print("=" * 60)

        # 顯示使用建議
        if expires_at and days_left and days_left > 7:
            print()
            print("💡 建議:")
            print(f"   • 定期檢查 Token 狀態（每週一次）")
            print(f"   • 在剩餘 30 天內更新 Token")
            print(f"   • 考慮使用永久 Token 以避免定期更新")

    except requests.exceptions.RequestException as e:
        print(f"❌ API 請求失敗: {e}", file=sys.stderr)
        print()
        print("請檢查網路連線或稍後再試", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 發生錯誤: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """主程式"""
    try:
        debug_token()
    except KeyboardInterrupt:
        print("\n\n⚠️  操作已取消")
        sys.exit(1)


if __name__ == "__main__":
    main()
