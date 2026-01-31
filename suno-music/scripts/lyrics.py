#!/usr/bin/env python3
"""
Suno Lyrics Generation Script
Generate lyrics using AllAPI Suno API
"""

import os
import sys
import time
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

def submit_lyrics_task(prompt: str, model: str = "chirp-v4") -> dict:
    """Submit lyrics generation task to Suno API"""
    url = f"{BASE_URL}suno/submit/music"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    params = {
        "prompt": prompt,
        "generation_type": "TEXT",
        "mv": model,
        "metadata": {
            "create_mode": "lyrics"
        }
    }

    try:
        response = requests.post(url, json=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error submitting task: {e}", file=sys.stderr)
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}", file=sys.stderr)
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

def wait_for_completion(task_id: str, interval: int = 3, timeout: int = 120) -> dict:
    """Wait for lyrics generation to complete"""
    start_time = time.time()

    print(f"Generating lyrics for task {task_id}...")

    while True:
        if time.time() - start_time > timeout:
            print(f"\nTimeout waiting for task {task_id}", file=sys.stderr)
            sys.exit(1)

        task = fetch_task(task_id)
        status = task.get("status", "UNKNOWN")

        print(f"Status: {status}...", end="\r")

        if status == "SUCCESS":
            print(f"\n✓ Lyrics generated successfully!")
            return task
        elif status == "FAILURE":
            print(f"\n✗ Task failed: {task.get('failReason', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)
        elif status in ["NOT_START", "SUBMITTED", "QUEUED", "IN_PROGRESS"]:
            time.sleep(interval)
        else:
            print(f"\nUnknown status: {status}", file=sys.stderr)
            sys.exit(1)

def display_lyrics(task: dict):
    """Display generated lyrics"""
    data = task.get("data", [])

    if not data:
        print("No lyrics data in response", file=sys.stderr)
        return

    # Suno returns lyrics as a single item in data array
    lyrics_item = data[0] if isinstance(data, list) and len(data) > 0 else data
    lyrics = lyrics_item.get("lyrics") or lyrics_item.get("text", "")

    if lyrics:
        print("\n" + "=" * 60)
        print("Generated Lyrics:")
        print("=" * 60)
        print(lyrics)
        print("=" * 60)
    else:
        print("No lyrics content found", file=sys.stderr)

    # Also display as JSON
    print("\nJSON Output:")
    print(json.dumps(lyrics_item, indent=2, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(
        description="Generate lyrics using Suno API",
        epilog="""
Examples:
  %(prog)s "Generate lyrics about love and friendship"
  %(prog)s "Write a song about spring" --model chirp-v4 --no-wait
        """
    )

    parser.add_argument("prompt", help="Lyrics generation prompt")
    parser.add_argument("--model", default="chirp-v4",
                       choices=["chirp-v3-0", "chirp-v3-5", "chirp-v4", "chirp-auk", "chirp-v5"],
                       help="Model version (default: chirp-v4)")
    parser.add_argument("--no-wait", action="store_true",
                       help="Return immediately without waiting for completion")

    args = parser.parse_args()

    # Check API key
    check_api_key()

    # Submit task
    print("Submitting lyrics generation task...")
    result = submit_lyrics_task(args.prompt, args.model)
    task_id = result.get("task_id") or result.get("id")

    if not task_id:
        print("Error: No task ID in response", file=sys.stderr)
        print(f"Response: {result}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ Task submitted: {task_id}")

    # Wait for completion or return immediately
    if args.no_wait:
        output = json.dumps({"task_id": task_id, "status": "SUBMITTED"}, indent=2)
        print(output)
        return

    # Poll for completion
    task = wait_for_completion(task_id)

    # Display lyrics
    display_lyrics(task)

if __name__ == "__main__":
    main()
