#!/usr/bin/env python3
"""
Kie.ai Suno Fetch Task Script
Fetch task status and results
"""

import os
import sys
import time
import json
import argparse
import requests
from typing import Dict, Any

# API Configuration
BASE_URL = "https://api.kie.ai/api/v1"
API_KEY = os.environ.get("KIE_API_KEY", "")
CALLBACK_URL = os.environ.get("KIE_CALLBACK_URL", "http://localhost:8080/callback")

def check_api_key():
    """Check if API key is set"""
    if not API_KEY:
        print("Error: KIE_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it using: export KIE_API_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)

def fetch_task(task_id: str) -> Dict[str, Any]:
    """Fetch task status and results"""
    url = f"{BASE_URL}/generate"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "taskId": task_id,
        "customMode": True,
        "model": "V4",
        "callBackUrl": CALLBACK_URL,
        "instrumental": False
    }

    try:
        # Kie.ai requires POST method for fetch
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 200:
            return data.get("data", {})
        else:
            return {"error": data.get("msg", "Unknown error")}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def wait_for_completion(task_id: str, interval: int = 5, timeout: int = 300) -> Dict[str, Any]:
    """Wait for task completion with polling"""
    start_time = time.time()

    print(f"Waiting for task {task_id} to complete...")

    while True:
        if time.time() - start_time > timeout:
            print(f"\n✗ Timeout waiting for task", file=sys.stderr)
            return fetch_task(task_id)

        task = fetch_task(task_id)
        status = task.get("status", "unknown")

        print(f"Status: {status}...", end="\r", flush=True)

        if status == "complete":
            print(f"\n✓ Task completed!")
            return task
        elif status == "failed":
            print(f"\n✗ Task failed", file=sys.stderr)
            return task
        elif status in ["queued", "processing", "text_generated"]:
            time.sleep(interval)
        elif "error" in task:
            print(f"\n✗ Error: {task['error']}", file=sys.stderr)
            return task
        else:
            time.sleep(interval)

def format_task_output(task: Dict[str, Any], detailed: bool = False) -> str:
    """Format task output for display"""
    if "error" in task:
        return json.dumps({"error": task["error"]}, indent=2)

    output = {
        "task_id": task.get("taskId"),
        "status": task.get("status"),
    }

    if detailed:
        output.update({
            "audio_ids": task.get("audioIds", []),
            "clips": task.get("clips", []),
            "persona_id": task.get("personaId")
        })

    return json.dumps(output, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(
        description="Fetch task status from Kie.ai Suno API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch task status
  %(prog)s task-id-123

  # Fetch and wait for completion
  %(prog)s task-id-123 --wait

  # Fetch with detailed output
  %(prog)s task-id-123 --detailed

  # Wait with custom interval
  %(prog)s task-id-123 --wait --interval 10
        """
    )

    parser.add_argument("task_id", help="Task ID to fetch")
    parser.add_argument("--wait", action="store_true", help="Wait for task completion")
    parser.add_argument("--interval", type=int, default=5, help="Polling interval in seconds (default: 5)")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds (default: 300)")
    parser.add_argument("--detailed", action="store_true", help="Show detailed output including clips")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    # Check API key
    check_api_key()

    # Fetch or wait for task
    if args.wait:
        task = wait_for_completion(args.task_id, args.interval, args.timeout)
    else:
        task = fetch_task(args.task_id)

    # Format and output
    if args.json:
        print(json.dumps(task, indent=2, ensure_ascii=False))
    else:
        print(format_task_output(task, args.detailed))

        # Show additional info
        if task.get("status") == "complete":
            audio_ids = task.get("audioIds", [])
            if audio_ids:
                print(f"\n✓ Audio IDs: {', '.join(audio_ids)}")
                print(f"   Use these with generate-persona.py to create a Persona")

            clips = task.get("clips", [])
            if clips:
                print(f"\n✓ Generated {len(clips)} clip(s)")
                for i, clip in enumerate(clips, 1):
                    audio_url = clip.get("audio_url", "N/A")
                    print(f"   {i}. {audio_url}")

if __name__ == "__main__":
    main()
