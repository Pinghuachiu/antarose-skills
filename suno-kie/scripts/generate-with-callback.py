#!/usr/bin/env python3
"""
Kie.ai Suno Music Generation with Ngrok Callback

Automatically sets up ngrok tunnel for callback URL and waits for completion.

Callback Types:
  - text: Lyrics/text generation completed
  - first: First track completed
  - complete: All tracks completed (this is when we get the final MP3 URLs)
  - error: Generation failed

API Documentation: https://docs.kie.ai/suno-api
"""

import os
import sys
import time
import json
import signal
import argparse
import subprocess
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import TCPServer
from typing import Dict, Any, Optional, List

# API Configuration
BASE_URL = "https://api.kie.ai/api/v1"
API_KEY = os.environ.get("KIE_API_KEY", "")

# Global variables
ngrok_process = None
callback_received = False
callback_data = None
callback_lock = threading.Lock()

PORT = 8080

class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP Handler for Kie.ai callbacks

    Callback Types (from docs.kie.ai/suno-api):
      - text: Lyrics/text generation completed
      - first: First track completed (still generating more)
      - complete: All tracks completed (FINAL - has MP3 URLs)
      - error: Generation failed
    """

    def do_POST(self):
        global callback_received, callback_data

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8'))

            # Check callback type
            task_data = data.get("data", {})
            callback_type = task_data.get("callbackType", "")

            # Print to stdout with nice formatting
            print("\n" + "="*60)
            if callback_type == "complete":
                print("✅ 收到 Callback：全部音樂生成完成！")
            elif callback_type == "first":
                print("🎵 收到 Callback：第一首已完成（等待第二首）...")
            elif callback_type == "text":
                print("📝 收到 Callback：歌詞生成完成（等待音頻生成）...")
            elif callback_type == "error":
                print("❌ 收到 Callback：生成失敗")
            else:
                print(f"📬 收到 Callback：{callback_type}")
            print("="*60)
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print("="*60 + "\n")

            # Only mark as complete when callbackType is "complete" or "error"
            if callback_type in ["complete", "error"]:
                with callback_lock:
                    callback_data = data
                    callback_received = True

                if callback_type == "complete" and data.get("code") == 200:
                    task_id = task_data.get("task_id")
                    clips = task_data.get("data", [])

                    print(f"✓ 任務完成: {task_id}")
                    print(f"✓ 生成了 {len(clips)} 首音樂\n")

                    for i, clip in enumerate(clips, 1):
                        print(f"【音樂 {i}】")
                        print(f"  ID: {clip.get('id')}")
                        print(f"  標題: {clip.get('title')}")
                        print(f"  風格: {clip.get('tags')}")
                        if clip.get('duration'):
                            duration = clip.get('duration')
                            if isinstance(duration, (int, float)):
                                print(f"  時長: {duration} 秒")

                        # IMPORTANT: audio_url is the MP3 download URL!
                        if clip.get('audio_url'):
                            print(f"  📥 MP3 下載 URL: {clip.get('audio_url')}")
                        if clip.get('stream_audio_url'):
                            print(f"  🎵 串流 URL: {clip.get('stream_audio_url')}")
                        if clip.get('image_url'):
                            print(f"  🖼️  圖片 URL: {clip.get('image_url')}")
                        print()
                elif callback_type == "error":
                    print("❌ 生成失敗")
                    error_msg = data.get("msg", "Unknown error")
                    print(f"錯誤訊息: {error_msg}")
            else:
                # Continue waiting for other callback types
                status_map = {
                    "text": "歌詞已生成，等待音樂生成...",
                    "first": "第一首已完成，等待第二首..."
                }
                print(f"⏳ {status_map.get(callback_type, '繼續等待...')}\n")

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "received"}).encode())

        except Exception as e:
            print(f"Error processing callback: {e}", file=sys.stderr)
            self.send_response(200)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress default logging
        pass

def check_ngrok_installed() -> bool:
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(
            ["ngrok", "version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def install_ngrok_instructions():
    """Print ngrok installation instructions"""
    print("❌ ngrok 未安裝", file=sys.stderr)
    print("\n請先安裝 ngrok:", file=sys.stderr)
    print("\n# 方法 1: 使用 apt (Linux)", file=sys.stderr)
    print("curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null", file=sys.stderr)
    print('echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list', file=sys.stderr)
    print("sudo apt update && sudo apt install ngrok", file=sys.stderr)
    print("\n# 方法 2: 使用 snap", file=sys.stderr)
    print("sudo snap install ngrok", file=sys.stderr)
    print("\n# 方法 3: 下載二進制檔案", file=sys.stderr)
    print("curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null", file=sys.stderr)
    print("wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz", file=sys.stderr)
    print("tar xvzf ngrok-v3-stable-linux-amd64.tgz", file=sys.stderr)
    print("sudo mv ngrok /usr/local/bin", file=sys.stderr)
    print("\n安裝後需要設定 authtoken:", file=sys.stderr)
    print("ngrok config add-authtoken YOUR_TOKEN", file=sys.stderr)
    print("\n取得 authtoken: https://dashboard.ngrok.com/get-started/your-authtoken\n", file=sys.stderr)

def check_api_key():
    """Check if API key is set"""
    if not API_KEY:
        print("Error: KIE_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it using: export KIE_API_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)

def start_callback_server(port: int = 8080):
    """Start callback server in background thread"""
    global PORT
    PORT = port

    print(f"🚀 啟動 Callback Server (localhost:{port})...")

    # Start server in background thread
    def run_server():
        server = TCPServer(("localhost", PORT), CallbackHandler)
        server.serve_forever()

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Wait for server to start

    print("✓ Callback Server 運行中")
    return server_thread

def start_ngrok_tunnel(port: int = 8080) -> tuple[subprocess.Popen, str]:
    """Start ngrok tunnel and return process and public URL"""
    print(f"🚀 啟動 Ngrok Tunnel (localhost:{port})...")

    # Start ngrok
    ngrok_process = subprocess.Popen(
        ["ngrok", "http", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(3)  # Wait for ngrok to start

    # Get ngrok public URL from API
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        response.raise_for_status()
        tunnels = response.json().get("tunnels", [])

        if not tunnels:
            print("❌ 無法取得 Ngrok URL", file=sys.stderr)
            ngrok_process.terminate()
            sys.exit(1)

        public_url = tunnels[0].get("public_url")
        if not public_url:
            print("❌ Ngrok URL 格式錯誤", file=sys.stderr)
            ngrok_process.terminate()
            sys.exit(1)

        # Add /callback path
        callback_url = f"{public_url}/callback"
        print(f"✓ Ngrok Tunnel 已建立: {public_url}")
        print(f"✓ Callback URL: {callback_url}")

        return ngrok_process, callback_url

    except requests.exceptions.RequestException as e:
        print(f"❌ 無法連接 Ngrok API: {e}", file=sys.stderr)
        ngrok_process.terminate()
        sys.exit(1)

def verify_callback_server(callback_url: str) -> bool:
    """Verify callback server is ready to receive requests"""
    print(f"🔍 驗證 Callback Server...")

    try:
        # Try to make a test request to the callback URL
        test_url = callback_url.replace('/callback', '/health')
        response = requests.get(test_url, timeout=5)

        # We expect this to fail (no /health endpoint), but it proves the tunnel works
        print(f"✓ Callback URL 可訪問")
        return True

    except Exception as e:
        # Try the main callback URL
        try:
            response = requests.post(callback_url, json={"test": True}, timeout=5)
            print(f"✓ Callback Server 準備就緒")
            return True
        except:
            print(f"❌ Callback Server 未準備好: {e}", file=sys.stderr)
            return False

def submit_music_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Submit music generation task to Kie.ai"""
    url = f"{BASE_URL}/generate"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error submitting task: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)

def build_params(args) -> Dict[str, Any]:
    """Build API parameters from arguments"""
    params = {
        "prompt": args.prompt,
        "customMode": args.custom_mode,
        "model": args.model
    }

    # Callback URL will be set by ngrok
    params["callBackUrl"] = ""  # Placeholder

    # Custom mode parameters
    if args.custom_mode:
        params["style"] = args.style
        params["title"] = args.title
        params["instrumental"] = getattr(args, 'instrumental', False)

        # Optional custom mode parameters
        if args.negative_tags:
            params["negativeTags"] = args.negative_tags
        if args.vocal_gender:
            params["vocalGender"] = args.vocal_gender
        if args.style_weight is not None:
            params["styleWeight"] = args.style_weight
        if args.weirdness is not None:
            params["weirdnessConstraint"] = args.weirdness
        if args.audio_weight is not None:
            params["audioWeight"] = args.audio_weight
        if args.persona_id:
            params["personaId"] = args.persona_id
    else:
        # Non-custom mode - only prompt is required
        params["instrumental"] = getattr(args, 'instrumental', False)

    return params

def cleanup(signum=None, frame=None):
    """Clean up background processes"""
    global ngrok_process

    print("\n\n⏹️ 清理中...")

    if ngrok_process:
        print("  關閉 Ngrok Tunnel...")
        ngrok_process.terminate()
        try:
            ngrok_process.wait(timeout=5)
        except:
            ngrok_process.kill()

    print("✓ 清理完成")
    sys.exit(0)

def main():
    # Set up signal handlers for cleanup
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    global ngrok_process

    parser = argparse.ArgumentParser(
        description="Generate AI music using Kie.ai Suno API with automatic ngrok callback",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Custom mode with instrumental
  %(prog)s --prompt "Sleep music" --style "Ambient" --title "Sea Breeze" --instrumental

  # With Persona
  %(prog)s --prompt "Lyrics here" --style "pop" --title "My Song" --persona-id "persona_123"

  # Non-custom mode
  %(prog)s --prompt "A rock song" --custom-mode false
        """
    )

    parser.add_argument("--prompt", required=True, help="Lyrics or description")
    parser.add_argument("--custom-mode", type=bool, default=True, help="Enable custom mode (default: true)")
    parser.add_argument("--model", default="V4_5",
                       choices=["V3_5", "V4", "V4_5", "V4_5PLUS", "V5"],
                       help="Model version (default: V4_5)")

    # Custom mode parameters
    parser.add_argument("--style", help="Music style (required in custom mode)")
    parser.add_argument("--title", help="Song title (required in custom mode)")
    parser.add_argument("--instrumental", action="store_true", help="Instrumental only (no vocals)")
    parser.add_argument("--negative-tags", help="Unwanted styles (optional)")
    parser.add_argument("--vocal-gender", choices=["m", "f"], help="Vocal gender: m/f (optional)")
    parser.add_argument("--style-weight", type=float, help="Style adherence strength (0-1)")
    parser.add_argument("--weirdness", type=float, help="Creative deviation (0-1)")
    parser.add_argument("--audio-weight", type=float, help="Audio feature weight (0-1)")
    parser.add_argument("--persona-id", help="Persona ID to apply (Kie.ai exclusive)")

    args = parser.parse_args()

    # Check prerequisites
    check_api_key()

    if not check_ngrok_installed():
        install_ngrok_instructions()
        sys.exit(1)

    # Validate custom mode requirements
    if args.custom_mode:
        if not args.style or not args.title:
            parser.error("--style and --title are required in custom mode")

    # Start services
    print("\n" + "="*60)
    print("🚀 啟動服務階段")
    print("="*60)

    callback_thread = start_callback_server()
    ngrok_process, callback_url = start_ngrok_tunnel()

    # Verify callback server is ready
    if not verify_callback_server(callback_url):
        print("❌ Callback Server 驗證失敗", file=sys.stderr)
        cleanup()

    print("="*60)
    print("✓ 所有服務已準備就緒")
    print("="*60 + "\n")

    # Build parameters with callback URL
    params = build_params(args)
    params["callBackUrl"] = callback_url

    print("📤 提交參數:")
    print(json.dumps(params, indent=2, ensure_ascii=False))

    # Submit task
    print(f"\n🎵 提交音樂生成任務...")
    if args.persona_id:
        print(f"   使用 Persona: {args.persona_id}")

    result = submit_music_task(params)

    if result.get("code") != 200:
        print(f"❌ Error: {result.get('msg')}", file=sys.stderr)
        cleanup()

    task_id = result.get("data", {}).get("taskId")

    if not task_id:
        print("❌ Error: No task ID in response", file=sys.stderr)
        cleanup()

    print(f"✓ 任務已提交: {task_id}")
    print(f"\n📡 等待 Callback 通知...")
    print(f"   (按 Ctrl+C 提前結束)\n")

    # Wait for callback
    try:
        start_time = time.time()
        timeout = 600  # 10 minutes timeout

        while True:
            # Check timeout
            if time.time() - start_time > timeout:
                print(f"\n⏰ 等待超時 ({timeout} 秒)")
                print(f"   可以前往 https://kie.ai/logs 手動查看結果")
                print(f"   任務 ID: {task_id}")
                cleanup()

            # Check if callback received
            with callback_lock:
                if callback_received and callback_data:
                    # Extract clips from callback data
                    task_data = callback_data.get('data', {})
                    callback_type = task_data.get('callbackType', '')

                    # Stop on complete or error
                    if callback_type == 'complete':
                        task_id_final = task_data.get('task_id')
                        clips = task_data.get('data', [])

                        if clips:
                            print("\n" + "="*60)
                            print("✅ 全部生成完成！")
                            print("="*60)
                            print(f"任務 ID: {task_id_final}")
                            print(f"生成了 {len(clips)} 首音樂\n")

                            # Display music URLs
                            for i, clip in enumerate(clips, 1):
                                print(f"【音樂 {i}】")
                                print(f"  ID: {clip.get('id')}")
                                print(f"  標題: {clip.get('title')}")
                                print(f"  風格: {clip.get('tags')}")
                                if clip.get('duration'):
                                    print(f"  時長: {clip.get('duration')} 秒")

                                # Show URLs
                                if clip.get('audio_url'):
                                    print(f"  📥 MP3 URL: {clip.get('audio_url')}")
                                if clip.get('stream_audio_url'):
                                    print(f"  🎵 音樂 URL: {clip.get('stream_audio_url')}")
                                if clip.get('image_url'):
                                    print(f"  🖼️  圖片 URL: {clip.get('image_url')}")
                                print()

                            print("="*60)
                            print("💡 提示: 使用 pix2-upload skill 上傳這些檔案")
                            print("="*60)

                            # Stop services after displaying results
                            print("\n⏹️ 停止服務...")
                            if ngrok_process:
                                ngrok_process.terminate()
                            print("✓ Ngrok + Callback Server 已停止")

                            print("\n✅ 所有工作完成！")
                            return

                    elif callback_type == 'error':
                        print("\n" + "="*60)
                        print("❌ 生成失敗")
                        print("="*60)
                        print("請檢查任務參數或前往 https://kie.ai/logs 查看詳細信息")

                        # Stop services on error
                        print("\n⏹️ 停止服務...")
                        if ngrok_process:
                            ngrok_process.terminate()
                        print("✓ Ngrok + Callback Server 已停止")
                        return

                    else:
                        # Reset flag to wait for complete callback
                        callback_received = False

            time.sleep(1)

    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
