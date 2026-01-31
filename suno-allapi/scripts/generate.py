#!/usr/bin/env python3
"""
Suno AllAPI Music Generation Script
Generate AI music using AllAPI Suno API with Persona support
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
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)

def fetch_task(task_id: str) -> Dict[str, Any]:
    """Fetch task status and results"""
    url = f"{BASE_URL}suno/fetch"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {"ids": [task_id]}

    try:
        # AllAPI requires POST method for fetch
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        result = response.json()

        # Parse response format: {"code": "success", "data": [...]}
        if result.get("code") == "success":
            data_list = result.get("data", [])
            if data_list and len(data_list) > 0:
                return data_list[0]

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
        status = task.get("status", "")

        print(f"Status: {status}...", end="\r", flush=True)

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
    }

    # Build metadata
    metadata = {
        "create_mode": "custom"
    }

    # Add instrumental flag if specified
    if hasattr(args, 'instrumental') and args.instrumental:
        # AllAPI doesn't support instrumental param directly
        # Use empty vocal_gender instead
        metadata["vocal_gender"] = ""
        print(f"🎵 Instrumental mode: NO VOCALS (vocal_gender empty)")
    else:
        # Only add vocal_gender if NOT instrumental
        metadata["vocal_gender"] = getattr(args, 'vocal_gender', 'm')
        print(f"🎤 Vocal mode: gender={metadata['vocal_gender']}")

    params["metadata"] = metadata
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
        "tags": getattr(args, 'tags', ''),
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
    """Build parameters for singer style mode (with Persona support)"""
    params = {
        "prompt": args.prompt,
        "generation_type": "TEXT",
        "mv": args.model,
        "tags": args.tags,
        "title": args.title,
    }

    # Add negative_tags if provided
    if hasattr(args, 'negative_tags') and args.negative_tags:
        params["negative_tags"] = args.negative_tags

    # Add vocal_gender if provided
    if hasattr(args, 'vocal_gender') and args.vocal_gender:
        params["vocal_gender"] = args.vocal_gender
    else:
        params["vocal_gender"] = ""

    # Persona support (AllAPI exclusive)
    if hasattr(args, 'persona_id') and args.persona_id:
        # Using Persona - requires artist_consistency task
        params["task"] = "artist_consistency"
        params["persona_id"] = args.persona_id

        if hasattr(args, 'artist_clip_id') and args.artist_clip_id:
            params["artist_clip_id"] = args.artist_clip_id

        print(f"🎭 Using Persona: {args.persona_id}")
        if hasattr(args, 'artist_clip_id') and args.artist_clip_id:
            print(f"   Artist Clip ID: {args.artist_clip_id}")
    else:
        # Regular singer style mode
        params["metadata"] = {
            "create_mode": "singer_style",
            "vocal_gender": getattr(args, 'vocal_gender', 'm')
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
        description="Generate AI music using AllAPI Suno API with Persona support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Inspiration mode (simple)
  %(prog)s "快乐的歌曲"

  # Custom mode
  %(prog)s --mode custom --title "My Song" --tags "pop,electronic" --prompt "Lyrics here"

  # Singer style with Persona 🎭
  %(prog)s --mode singer-style --title "New Song" --tags "pop" --prompt "Lyrics" \\
    --model chirp-v4-tau --persona-id "xxx" --artist-clip-id "yyy"

  # Cover mode
  %(prog)s --mode cover --cover-clip-id "xxx" --prompt "Remix this song"

Persona Usage:
  1. Generate a song and get the clip_id
  2. Use singer-style mode with --persona-id and --artist-clip-id
  3. Model must be chirp-v3-5-tau or chirp-v4-tau for Persona
        """
    )

    parser.add_argument("prompt", nargs="?", help="Music prompt or lyrics")
    parser.add_argument("--mode", choices=["inspiration", "custom", "extend", "cover", "singer-style", "concat"],
                       default="inspiration", help="Generation mode (default: inspiration)")
    parser.add_argument("--model", default="chirp-v4",
                       choices=["chirp-v3-0", "chirp-v3-5", "chirp-v4", "chirp-auk", "chirp-v5",
                                "chirp-v3-5-tau", "chirp-v4-tau"],
                       help="Model version (default: chirp-v4). Use chirp-v3-5-tau or chirp-v4-tau for Persona")
    parser.add_argument("--no-wait", action="store_true",
                       help="Return immediately without waiting for completion")

    # Custom mode parameters
    parser.add_argument("--title", help="Song title (custom/singer-style mode)")
    parser.add_argument("--tags", help="Music styles, comma-separated (custom/cover/singer-style mode)")
    parser.add_argument("--negative-tags", help="Unwanted styles (custom/singer-style mode)")
    parser.add_argument("--vocal-gender", choices=["m", "f"], help="Vocal gender: m/f (custom/singer-style mode)")
    parser.add_argument("--instrumental", action="store_true", help="Generate instrumental music (no vocals)")

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

    # Persona parameters (singer-style mode)
    parser.add_argument("--persona-id", help="Persona ID for artist_consistency (singer-style mode)")
    parser.add_argument("--artist-clip-id", help="Original clip ID for Persona (singer-style mode)")

    args = parser.parse_args()

    # Check API key
    check_api_key()

    # Validate Persona parameters
    if hasattr(args, 'persona_id') and args.persona_id:
        if args.model not in ["chirp-v3-5-tau", "chirp-v4-tau"]:
            print("⚠️  Warning: Persona requires chirp-v3-5-tau or chirp-v4-tau model", file=sys.stderr)
            print(f"   Current model: {args.model}", file=sys.stderr)
        if not hasattr(args, 'artist_clip_id') or not args.artist_clip_id:
            print("⚠️  Warning: Persona usage works best with --artist-clip-id", file=sys.stderr)

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

    # Handle different response formats
    if isinstance(result, dict):
        if result.get("code") == "success":
            task_id = result.get("data")
        else:
            task_id = result.get("task_id") or result.get("id")
    else:
        task_id = result

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

    # Extract clip IDs from response
    data = task.get("data", [])
    if data and len(data) > 0:
        clip_ids = [clip.get("id") for clip in data if clip.get("id")]
        if clip_ids:
            print(f"\n✓ Clip IDs: {', '.join(clip_ids)}")
            print(f"   Use these clip_ids for Persona generation")

    print("\n" + format_output(task))

if __name__ == "__main__":
    main()
