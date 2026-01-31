#!/usr/bin/env python3
"""
Kie.ai Callback Server
Receives task completion notifications from Kie.ai API
"""

import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import TCPServer
import threading
import time

PORT = 8080

class CallbackHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8'))

            print("\n" + "="*60)
            print("📬 收到 Callback 通知！")
            print("="*60)
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print("="*60 + "\n")

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

def start_server():
    server = TCPServer(("localhost", PORT), CallbackHandler)
    print(f"🚀 Callback Server 啟動在 http://localhost:{PORT}")
    print(f"📡 等待 Kie.ai 任務完成通知...")
    print(f"按 Ctrl+C 停止\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n⏹️ Server 已停止")
        sys.exit(0)

if __name__ == "__main__":
    start_server()
