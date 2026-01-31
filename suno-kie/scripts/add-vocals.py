#!/usr/bin/env python3
"""
Kie.ai Suno Add Vocals Script
Add AI-generated vocals to instrumental tracks
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

def submit_add_vocals(params: Dict[str, Any]) -> Dict[str, Any]:
    """Submit add vocals task to Kie.ai"""
    url = f"{BASE_URL}/generate/add-vocals"
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
        "instrumental": False  # We want to ADD vocals, not make it instrumental
    }

    # Add callback URL if available
    if CALLBACK_URL:
        params["callBackUrl"] = CALLBACK_URL
    elif args.callback_url:
        params["callBackUrl"] = args.callback_url

    # Custom mode parameters
    if args.custom_mode:
        if not args.style or not args.title:
            print("Error: --style and --title are required in custom mode", file=sys.stderr)
            sys.exit(1)

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

    return params

def main():
    parser = argparse.ArgumentParser(
        description="Add AI-generated vocals to instrumental tracks using Kie.ai Suno API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple mode - just describe what you want
  %(prog)s --upload-url "https://storage.example.com/piano.mp3" \\
    --prompt "Create happy lyrics about summer" \\
    --custom-mode false

  # Custom mode - full control
  %(prog)s --upload-url "https://storage.example.com/beat.mp3" \\
    --prompt "Urban rap song about city life at night" \\
    --style "Hip-Hop" \\
    --title "Midnight City" \\
    --custom-mode true

  # With vocal gender control
  %(prog)s --upload-url "https://storage.example.com/instrumental.mp3" \\
    --prompt "Love song" \\
    --style "Pop Ballad" \\
    --title "My Heart" \\
    --vocal-gender f \\
    --custom-mode true

Workflow:
  1. Upload your instrumental to cloud storage (Dropbox, Google Drive, etc.)
  2. Get a publicly accessible URL
  3. Run this script to add AI vocals
  4. Wait for completion and download the result

Note:
  - The upload URL must be publicly accessible
  - Audio should not exceed 2 minutes
  - Vocals will be auto-generated to match your instrumental's mood and key
  - This is different from Persona - you cannot specify a particular voice
        """
    )

    parser.add_argument("--upload-url", required=True,
                       help="Publicly accessible URL of instrumental track")
    parser.add_argument("--prompt", required=True,
                       help="Description of lyrics or theme you want")
    parser.add_argument("--custom-mode", type=bool, default=True,
                       help="Enable custom mode for full control (default: true)")
    parser.add_argument("--model", default="V4_5",
                       choices=["V3_5", "V4", "V4_5", "V4_5PLUS", "V5"],
                       help="Model version (default: V4_5)")
    parser.add_argument("--callback-url", help="Callback URL for task completion")
    parser.add_argument("--no-wait", action="store_true",
                       help="Return immediately without waiting for completion")

    # Custom mode parameters
    parser.add_argument("--style", help="Music style (required in custom mode)")
    parser.add_argument("--title", help="Song title (required in custom mode)")
    parser.add_argument("--negative-tags", help="Unwanted styles (optional)")
    parser.add_argument("--vocal-gender", choices=["m", "f"],
                       help="Vocal gender: m/f (optional)")
    parser.add_argument("--style-weight", type=float,
                       help="Style adherence strength (0-1, optional)")
    parser.add_argument("--weirdness", type=float,
                       help="Creative deviation (0-1, optional)")

    args = parser.parse_args()

    # Check API key
    check_api_key()

    # Validate custom mode requirements
    if args.custom_mode:
        if not args.style or not args.title:
            parser.error("--style and --title are required when --custom-mode is true")

    # Build parameters
    params = build_params(args)

    # Submit task
    print("🎤 Submitting Add Vocals task...")
    print(f"📁 Instrumental URL: {args.upload_url}")
    print(f"💭 Prompt: {args.prompt}")
    if args.custom_mode:
        print(f"🎵 Style: {args.style}")
        print(f"📝 Title: {args.title}")
    print()

    result = submit_add_vocals(params)

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

    # Show clips if available
    clips = task.get("clips", [])
    if clips:
        print(f"\n✓ Generated {len(clips)} version(s):")
        for i, clip in enumerate(clips, 1):
            audio_url = clip.get("audio_url", "N/A")
            print(f"   {i}. {audio_url}")

    print(f"\n🎉 Vocals added successfully to your instrumental!")

if __name__ == "__main__":
    main()
