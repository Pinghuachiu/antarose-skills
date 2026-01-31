#!/usr/bin/env python3
"""
Kie.ai Suno Upload And Cover Script
Upload audio and transform it into a new style while keeping the melody
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
CALLBACK_URL = os.environ.get("KIE_CALLBACK_URL", "")

def check_api_key():
    """Check if API key is set"""
    if not API_KEY:
        print("Error: KIE_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it using: export KIE_API_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)

def submit_upload_cover(params: Dict[str, Any]) -> Dict[str, Any]:
    """Submit upload and cover task to Kie.ai"""
    url = f"{BASE_URL}/generate/upload-cover"
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

def fetch_task(task_id: str) -> Dict[str, Any]:
    """Fetch task status and results"""
    url = f"{BASE_URL}/generate"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    params = {"taskId": task_id}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 200:
            return data.get("data", {})
        else:
            print(f"Error: {data.get('msg')}", file=sys.stderr)
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching task: {e}", file=sys.stderr)
        sys.exit(1)

def wait_for_completion(task_id: str, interval: int = 5, timeout: int = 300) -> Dict[str, Any]:
    """Wait for task completion with polling"""
    start_time = time.time()

    print(f"Waiting for task {task_id} to complete...")

    while True:
        if time.time() - start_time > timeout:
            print(f"\nTimeout waiting for task {task_id}", file=sys.stderr)
            print(f"Use fetch.py to check status later", file=sys.stderr)
            sys.exit(1)

        task = fetch_task(task_id)
        status = task.get("status", "")

        print(f"Status: {status}...", end="\r", flush=True)

        if status == "complete":
            print(f"\n✓ Task completed successfully!")
            return task
        elif status == "failed":
            print(f"\n✗ Task failed", file=sys.stderr)
            sys.exit(1)
        elif status in ["queued", "processing", "text_generated"]:
            time.sleep(interval)
        else:
            time.sleep(interval)

def build_params(args) -> Dict[str, Any]:
    """Build API parameters from arguments"""
    params = {
        "uploadUrl": args.upload_url,
        "prompt": args.prompt,
        "customMode": args.custom_mode,
        "model": args.model,
        "instrumental": args.instrumental
    }

    # Add callback URL if available
    if CALLBACK_URL:
        params["callBackUrl"] = CALLBACK_URL
    elif args.callback_url:
        params["callBackUrl"] = args.callback_url

    # Custom mode parameters
    if args.custom_mode:
        params["style"] = args.style
        params["title"] = args.title

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
    # Non-custom mode doesn't need style, title, etc.

    return params

def main():
    parser = argparse.ArgumentParser(
        description="Upload audio and transform it into a new style using Kie.ai Suno API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Custom mode - transform to jazz
  %(prog)s --upload-url "https://storage.example.com/song.mp3" \\
    --prompt "Convert to jazz style" \\
    --style "Jazz" \\
    --title "Jazz Version" \\
    --custom-mode true

  # Non-custom mode (simplest)
  %(prog)s --upload-url "https://storage.example.com/song.mp3" \\
    --prompt "Make it rock" \\
    --custom-mode false

  # With Persona
  %(prog)s --upload-url "https://storage.example.com/song.mp3" \\
    --prompt "New version" \\
    --style "pop" \\
    --title "Cover" \\
    --persona-id "persona_123"

Note:
  The upload URL must be publicly accessible.
  Audio should not exceed 2 minutes for upload-cover.
        """
    )

    parser.add_argument("--upload-url", required=True, help="URL of uploaded audio file")
    parser.add_argument("--prompt", required=True, help="Description or lyrics")
    parser.add_argument("--custom-mode", type=bool, default=True, help="Enable custom mode (default: true)")
    parser.add_argument("--model", default="V4_5",
                       choices=["V3_5", "V4", "V4_5", "V4_5PLUS", "V5"],
                       help="Model version (default: V4_5)")
    parser.add_argument("--instrumental", action="store_true", help="Instrumental only (no vocals)")
    parser.add_argument("--callback-url", help="Callback URL for task completion")
    parser.add_argument("--no-wait", action="store_true",
                       help="Return immediately without waiting for completion")

    # Custom mode parameters
    parser.add_argument("--style", help="Music style (required in custom mode)")
    parser.add_argument("--title", help="Song title (required in custom mode)")
    parser.add_argument("--negative-tags", help="Unwanted styles (optional)")
    parser.add_argument("--vocal-gender", choices=["m", "f"], help="Vocal gender: m/f (optional)")
    parser.add_argument("--style-weight", type=float, help="Style adherence strength (0-1)")
    parser.add_argument("--weirdness", type=float, help="Creative deviation (0-1)")
    parser.add_argument("--audio-weight", type=float, help="Audio feature weight (0-1)")
    parser.add_argument("--persona-id", help="Persona ID to apply (Kie.ai exclusive)")

    args = parser.parse_args()

    # Check API key
    check_api_key()

    # Validate custom mode requirements
    if args.custom_mode:
        if not args.style or not args.title:
            parser.error("--style and --title are required in custom mode")

    # Build parameters
    params = build_params(args)

    # Submit task
    print(f"Submitting upload and cover task...")
    print(f"Upload URL: {args.upload_url}")

    result = submit_upload_cover(params)

    if result.get("code") != 200:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    task_id = result.get("data", {}).get("taskId")

    if not task_id:
        print("Error: No task ID in response", file=sys.stderr)
        sys.exit(1)

    print(f"✓ Task submitted: {task_id}")

    # Wait for completion or return immediately
    if args.no_wait:
        output = json.dumps({"task_id": task_id, "status": "submitted"}, indent=2)
        print(output)
        return

    # Poll for completion
    task = wait_for_completion(task_id)

    # Extract important info
    audio_ids = task.get("audioIds", [])
    if audio_ids:
        print(f"\n✓ Audio IDs: {', '.join(audio_ids)}")

if __name__ == "__main__":
    main()
