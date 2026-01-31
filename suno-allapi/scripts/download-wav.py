#!/usr/bin/env python3
"""
Suno Download WAV Script
Download high-quality WAV audio files from Suno music generation tasks
"""

import os
import sys
import json
import argparse
import requests
from urllib.parse import urlparse
from pathlib import Path

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

def download_file(url: str, output_path: str) -> bool:
    """Download file from URL to local path"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Create parent directory if needed
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Download with progress
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    # Show progress
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\rDownloading: {progress:.1f}%", end='', file=sys.stderr)

        print(f"\r✓ Downloaded to: {output_path}", file=sys.stderr)
        return True

    except requests.exceptions.RequestException as e:
        print(f"\nError downloading file: {e}", file=sys.stderr)
        return False

def get_audio_urls(task_data: dict) -> list:
    """Extract all audio URLs from task data"""
    urls = []

    # Check if task has data
    if not task_data or "data" not in task_data:
        return urls

    data_list = task_data.get("data", [])

    for clip in data_list:
        if not isinstance(clip, dict):
            continue

        # Get audio URL (could be different keys)
        audio_url = (
            clip.get("audio_url") or
            clip.get("audioUrl") or
            clip.get("audio") or
            clip.get("wav_url") or
            clip.get("wavUrl") or
            clip.get("video_url") or
            clip.get("videoUrl")
        )

        if audio_url:
            clip_info = {
                "id": clip.get("id", "unknown"),
                "title": clip.get("title", "untitled"),
                "url": audio_url,
                "type": "wav" if ".wav" in audio_url.lower() else "mp3"
            }
            urls.append(clip_info)

    return urls

def generate_filename(clip_info: dict, output_dir: str, index: int) -> str:
    """Generate filename for downloaded audio"""
    title = clip_info.get("title", "untitled")
    clip_id = clip_info.get("id", "unknown")

    # Clean title for filename
    title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
    title = title[:50] if len(title) > 50 else title

    # Determine extension
    ext = "wav" if clip_info.get("type") == "wav" else "mp3"

    # Generate filename
    filename = f"{index:02d}-{title}-{clip_id[:8]}.{ext}"
    return os.path.join(output_dir, filename)

def main():
    parser = argparse.ArgumentParser(
        description="Download WAV/MP3 audio files from Suno music generation tasks",
        epilog="""
Examples:
  # Download all audio from a task
  %(prog)s task-id-here

  # Download to specific directory
  %(prog)s task-id-here --output ./music

  # List available audio files without downloading
  %(prog)s task-id-here --list-only

  # Download only WAV files
  %(prog)s task-id-here --wav-only
        """
    )

    parser.add_argument("task_id", help="Task ID to download from")
    parser.add_argument("--output", "-o", default="./suno-downloads",
                       help="Output directory (default: ./suno-downloads)")
    parser.add_argument("--list-only", action="store_true",
                       help="List available audio files without downloading")
    parser.add_argument("--wav-only", action="store_true",
                       help="Download only WAV format files")
    parser.add_argument("--clip-id", help="Download specific clip only")

    args = parser.parse_args()

    # Check API key
    check_api_key()

    # Fetch task
    print(f"Fetching task {args.task_id}...", file=sys.stderr)
    task = fetch_task(args.task_id)

    if not task:
        print(f"No task found with ID: {args.task_id}", file=sys.stderr)
        sys.exit(1)

    # Get status
    status = task.get("status", "UNKNOWN")

    if status != "SUCCESS":
        print(f"Task status: {status}", file=sys.stderr)
        print("Cannot download from incomplete or failed tasks", file=sys.stderr)
        if status == "FAILURE":
            print(f"Failure reason: {task.get('failReason', 'Unknown')}", file=sys.stderr)
        sys.exit(1)

    # Get audio URLs
    audio_list = get_audio_urls(task)

    if not audio_list:
        print("No audio files found in task", file=sys.stderr)
        sys.exit(1)

    # List available files
    print(f"\nFound {len(audio_list)} audio file(s):", file=sys.stderr)
    for i, clip_info in enumerate(audio_list, 1):
        print(f"  [{i}] {clip_info['title']} ({clip_info['type'].upper()})", file=sys.stderr)
        print(f"      ID: {clip_info['id']}", file=sys.stderr)
        print(f"      URL: {clip_info['url']}", file=sys.stderr)

    if args.list_only:
        sys.exit(0)

    # Filter by clip ID if specified
    if args.clip_id:
        audio_list = [c for c in audio_list if c["id"] == args.clip_id]
        if not audio_list:
            print(f"\nNo clip found with ID: {args.clip_id}", file=sys.stderr)
            sys.exit(1)

    # Filter by WAV only
    if args.wav_only:
        wav_count = len([c for c in audio_list if c["type"] == "wav"])
        if wav_count == 0:
            print("\nNo WAV files available", file=sys.stderr)
            sys.exit(1)
        audio_list = [c for c in audio_list if c["type"] == "wav"]
        print(f"\nDownloading {len(audio_list)} WAV file(s)...", file=sys.stderr)
    else:
        print(f"\nDownloading {len(audio_list)} file(s) to {args.output}/...", file=sys.stderr)

    # Download files
    success_count = 0
    for i, clip_info in enumerate(audio_list, 1):
        output_path = generate_filename(clip_info, args.output, i)

        print(f"\n[{i}/{len(audio_list)}] {clip_info['title']}", file=sys.stderr)
        if download_file(clip_info["url"], output_path):
            success_count += 1

    # Summary
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Download complete: {success_count}/{len(audio_list)} files", file=sys.stderr)
    print(f"Saved to: {os.path.abspath(args.output)}", file=sys.stderr)

if __name__ == "__main__":
    main()
