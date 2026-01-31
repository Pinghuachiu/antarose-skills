#!/usr/bin/env python3
"""
Suno Music Generation Script
Generate AI music using AllAPI Suno API
"""

import os
import sys
import time
import json
import argparse
import requests
from typing import Optional, Dict, Any

# API Configuration
BASE_URL = os.environ.get("ALLAPI_BASE_URL", "https://allapi.store/")
API_KEY = os.environ.get("ALLAPI_KEY", "")

def check_api_key():
    """Check if API key is set"""
    if not API_KEY:
        print("Error: ALLAPI_KEY environment variable not set", file=sys.stderr)
        print("Please set it using: export ALLAPI_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)

def submit_music_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Submit music generation task to Suno API"""
    url = f"{BASE_URL}suno/submit/music"
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
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)

def fetch_task(task_id: str) -> Dict[str, Any]:
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

def wait_for_completion(task_id: str, interval: int = 5, timeout: int = 300) -> Dict[str, Any]:
    """Wait for task completion with polling"""
    start_time = time.time()

    print(f"Waiting for task {task_id} to complete...")

    while True:
        if time.time() - start_time > timeout:
            print(f"Timeout waiting for task {task_id}", file=sys.stderr)
            sys.exit(1)

        task = fetch_task(task_id)
        status = task.get("status", "UNKNOWN")

        print(f"Status: {status}...", end="\r")

        if status == "SUCCESS":
            print(f"\n✓ Task completed successfully!")
            return task
        elif status == "FAILURE":
            print(f"\n✗ Task failed: {task.get('failReason', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)
        elif status in ["NOT_START", "SUBMITTED", "QUEUED", "IN_PROGRESS"]:
            time.sleep(interval)
        else:
            print(f"\nUnknown status: {status}", file=sys.stderr)
            sys.exit(1)

def format_output(task: Dict[str, Any]) -> str:
    """Format task output for display"""
    output = {
        "task_id": task.get("task_id"),
        "status": task.get("status"),
        "data": task.get("data", [])
    }
    return json.dumps(output, indent=2, ensure_ascii=False)

def build_inspiration_params(prompt: str, model: str) -> Dict[str, Any]:
    """Build parameters for inspiration mode"""
    return {
        "prompt": prompt,
        "generation_type": "TEXT",
        "mv": model,
        "metadata": {
            "create_mode": "inspiration"
        }
    }

def build_custom_params(args) -> Dict[str, Any]:
    """Build parameters for custom mode"""
    params = {
        "title": args.title,
        "tags": args.tags,
        "prompt": args.prompt,
        "generation_type": "TEXT",
        "mv": args.model,
        "negative_tags": getattr(args, 'negative_tags', ''),
        "metadata": {
            "create_mode": "custom",
            "vocal_gender": getattr(args, 'vocal_gender', 'm')
        }
    }
    return params

def build_extend_params(args) -> Dict[str, Any]:
    """Build parameters for extend mode"""
    params = {
        "prompt": args.prompt,
        "generation_type": "TEXT",
        "mv": args.model,
        "continue_at": args.continue_at,
        "continue_clip_id": args.continue_clip_id,
        "task": "extend",
        "metadata": {
            "create_mode": "extend"
        }
    }
    return params

def build_cover_params(args) -> Dict[str, Any]:
    """Build parameters for cover/upload mode"""
    params = {
        "prompt": args.prompt,
        "generation_type": "TEXT",
        "tags": args.tags,
        "mv": "chirp-v3-5-tau",
        "title": getattr(args, 'title', ''),
        "continue_clip_id": getattr(args, 'continue_clip_id', None),
        "continue_at": getattr(args, 'continue_at', None),
        "infill_start_s": getattr(args, 'infill_start', None),
        "infill_end_s": getattr(args, 'infill_end', None),
        "task": "cover",
        "cover_clip_id": args.cover_clip_id,
        "metadata": {
            "create_mode": "cover"
        }
    }
    return params

def build_singer_style_params(args) -> Dict[str, Any]:
    """Build parameters for singer style mode"""
    params = {
        "prompt": args.prompt,
        "generation_type": "TEXT",
        "mv": args.model,
        "tags": args.tags,
        "title": args.title,
        "metadata": {
            "create_mode": "singer_style",
            "vocal_gender": getattr(args, 'vocal_gender', 'm')
        }
    }
    return params

def build_concat_params(args) -> Dict[str, Any]:
    """Build parameters for song concatenation mode"""
    # Parse clip IDs from comma-separated string
    clip_ids = args.concat_clips.split(",") if args.concat_clips else []

    if len(clip_ids) < 2:
        raise ValueError("At least 2 clip IDs required for concatenation")

    params = {
        "generation_type": "TEXT",
        "mv": args.model,
        "task": "concat",
        "clip_ids": clip_ids,
        "metadata": {
            "create_mode": "concat"
        }
    }

    # Optional parameters
    if hasattr(args, 'title') and args.title:
        params["title"] = args.title
    if hasattr(args, 'prompt') and args.prompt:
        params["prompt"] = args.prompt

    return params

def main():
    parser = argparse.ArgumentParser(
        description="Generate AI music using Suno API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Inspiration mode (simple)
  %(prog)s "快乐的歌曲"

  # Custom mode
  %(prog)s --mode custom --title "My Song" --tags "pop,electronic" --prompt "Lyrics here"

  # Extend mode
  %(prog)s --mode extend --task-id "xxx" --continue-at 120.5 --prompt "Continue"

  # Cover mode
  %(prog)s --mode cover --cover-clip-id "xxx" --prompt "Remix this song"
        """
    )

    parser.add_argument("prompt", nargs="?", help="Music prompt or lyrics")
    parser.add_argument("--mode", choices=["inspiration", "custom", "extend", "cover", "singer-style", "concat"],
                       default="inspiration", help="Generation mode (default: inspiration)")
    parser.add_argument("--model", default="chirp-v4",
                       choices=["chirp-v3-0", "chirp-v3-5", "chirp-v4", "chirp-auk", "chirp-v5"],
                       help="Model version (default: chirp-v4)")
    parser.add_argument("--no-wait", action="store_true",
                       help="Return immediately without waiting for completion")

    # Custom mode parameters
    parser.add_argument("--title", help="Song title (custom mode)")
    parser.add_argument("--tags", help="Music styles, comma-separated (custom/cover mode)")
    parser.add_argument("--negative-tags", help="Unwanted styles (custom mode)")
    parser.add_argument("--vocal-gender", choices=["m", "f"], help="Vocal gender: m/f (custom mode)")

    # Extend mode parameters
    parser.add_argument("--task-id", help="Task ID to extend (extend mode)")
    parser.add_argument("--continue-at", type=float, help="Continue start time in seconds (extend mode)")
    parser.add_argument("--continue-clip-id", help="Clip ID to continue (extend/cover mode)")

    # Cover mode parameters
    parser.add_argument("--cover-clip-id", help="Original audio clip ID (cover mode)")
    parser.add_argument("--infill-start", type=float, help="Infill start time in seconds (cover mode)")
    parser.add_argument("--infill-end", type=float, help="Infill end time in seconds (cover mode)")

    # Concat mode parameters
    parser.add_argument("--concat-clips", help="Clip IDs to concatenate (comma-separated, at least 2)")

    # Singer style mode parameters (uses same as custom mode)
    # singer-style uses --title, --tags, --prompt, --vocal-gender

    args = parser.parse_args()

    # Check API key
    check_api_key()

    # Validate required parameters based on mode
    if args.mode == "inspiration":
        if not args.prompt:
            parser.error("prompt is required for inspiration mode")
        params = build_inspiration_params(args.prompt, args.model)

    elif args.mode == "custom":
        if not args.title or not args.tags or not args.prompt:
            parser.error("--title, --tags, and --prompt are required for custom mode")
        params = build_custom_params(args)

    elif args.mode == "extend":
        if not args.task_id or not args.continue_at or not args.continue_clip_id or not args.prompt:
            parser.error("--task-id, --continue-at, --continue-clip-id, and --prompt are required for extend mode")
        params = build_extend_params(args)

    elif args.mode == "cover":
        if not args.cover_clip_id or not args.prompt:
            parser.error("--cover-clip-id and --prompt are required for cover mode")
        params = build_cover_params(args)

    elif args.mode == "singer-style":
        if not args.title or not args.tags or not args.prompt:
            parser.error("--title, --tags, and --prompt are required for singer-style mode")
        params = build_singer_style_params(args)

    elif args.mode == "concat":
        if not args.concat_clips:
            parser.error("--concat-clips is required for concat mode (at least 2 clip IDs)")
        params = build_concat_params(args)

    # Submit task
    print(f"Submitting {args.mode} music generation task...")
    result = submit_music_task(params)
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
    print("\n" + format_output(task))

if __name__ == "__main__":
    main()
