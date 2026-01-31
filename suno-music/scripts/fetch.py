#!/usr/bin/env python3
"""
Suno Task Fetch Script
Fetch Suno music generation task status and results
"""

import os
import sys
import json
import argparse
import requests

# API Configuration
BASE_URL = os.environ.get("ALLAPI_BASE_URL", "https://allapi.store/")
API_KEY = os.environ.get("ALLAPI_KEY", "")

def check_api_key():
    """Check if API key is set"""
    if not API_KEY:
        print("Error: ALLAPI_KEY environment variable not set", file=sys.stderr)
        print("Please set it using: export ALLAPI_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)

def fetch_task(task_id: str) -> dict:
    """Fetch task status and results"""
    url = f"{BASE_URL}suno/fetch"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    params = {"ids": [task_id]}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data and len(data) > 0:
            return data[0]
        return {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching task: {e}", file=sys.stderr)
        sys.exit(1)

def format_output(task: dict) -> str:
    """Format task output for display"""
    output = {
        "task_id": task.get("task_id"),
        "status": task.get("status"),
        "action": task.get("action"),
        "submit_time": task.get("submitTime"),
        "start_time": task.get("startTime"),
        "finish_time": task.get("finishTime"),
        "fail_reason": task.get("failReason"),
        "data": task.get("data", [])
    }
    return json.dumps(output, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(
        description="Fetch Suno music generation task status",
        epilog="""
Examples:
  %(prog)s f4a94d75-087b-4bb1-bd45-53ba293faf96
  %(prog)s --id f4a94d75-087b-4bb1-bd45-53ba293faf96 --json
        """
    )

    parser.add_argument("task_id", help="Task ID to fetch")
    parser.add_argument("--id", dest="task_id_alt", help="Task ID (alternative)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    # Use alternative argument if provided
    task_id = args.task_id_alt or args.task_id

    if not task_id:
        parser.error("task_id is required")

    # Check API key
    check_api_key()

    # Fetch task
    task = fetch_task(task_id)

    if not task:
        print(f"No task found with ID: {task_id}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.json:
        print(json.dumps(task, indent=2, ensure_ascii=False))
    else:
        print(format_output(task))

        # Display additional info
        status = task.get("status", "UNKNOWN")
        print(f"\nStatus: {status}", file=sys.stderr)

        if status == "SUCCESS":
            data = task.get("data", [])
            if data:
                print(f"Generated {len(data)} clip(s)", file=sys.stderr)
                for i, clip in enumerate(data, 1):
                    print(f"\nClip {i}:", file=sys.stderr)
                    print(f"  ID: {clip.get('id')}", file=sys.stderr)
                    print(f"  Title: {clip.get('title')}", file=sys.stderr)
                    print(f"  Audio: {clip.get('audio_url')}", file=sys.stderr)
                    print(f"  Video: {clip.get('video_url')}", file=sys.stderr)

        elif status == "FAILURE":
            print(f"Failed: {task.get('failReason', 'Unknown error')}", file=sys.stderr)

if __name__ == "__main__":
    main()
