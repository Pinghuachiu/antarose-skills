#!/usr/bin/env python3
"""
Suno Audio Upload Script
Upload audio files to Suno for voice cloning or custom generation
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional, Dict, Any
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

def upload_audio(file_path: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Upload audio file to Suno"""
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Get file extension
    file_ext = Path(file_path).suffix.lower()
    supported_formats = ['.mp3', '.wav', '.m4a', '.mp4', '.mpeg']

    if file_ext not in supported_formats:
        print(f"Warning: File format {file_ext} may not be supported", file=sys.stderr)
        print(f"Supported formats: {', '.join(supported_formats)}", file=sys.stderr)

    url = f"{BASE_URL}suno/upload"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        with open(file_path, 'rb') as audio_file:
            files = {
                'file': (os.path.basename(file_path), audio_file, 'audio/mpeg')
            }

            data = {}
            if description:
                data['description'] = description

            print(f"Uploading {file_path}...")
            response = requests.post(url, files=files, data=data, headers=headers)
            response.raise_for_status()
            return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error uploading audio: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

def format_output(data: Dict[str, Any]) -> str:
    """Format upload output for display"""
    output = {
        "clip_id": data.get("id") or data.get("clip_id"),
        "filename": data.get("filename") or data.get("name"),
        "status": data.get("status", "uploaded"),
        "description": data.get("description", ""),
        "url": data.get("audio_url") or data.get("url")
    }
    return json.dumps(output, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(
        description="Upload audio to Suno for voice cloning or custom generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload audio file
  %(prog)s my-voice.mp3

  # Upload with description
  %(prog)s my-voice.mp3 --description "My singing voice"

  # Upload multiple files
  %(prog)s voice1.mp3 voice2.wav

Usage Workflow:
  1. Upload your audio: %(prog)s my-voice.mp3
  2. Get clip_id from output
  3. Use with cover mode: generate.py --mode cover --cover-clip-id CLIP_ID --prompt "Remix"
        """
    )

    parser.add_argument("files", nargs="+", help="Audio file(s) to upload")
    parser.add_argument("--description", "-d", help="Description for the audio (optional)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON only")

    args = parser.parse_args()

    # Check API key
    check_api_key()

    # Upload each file
    results = []
    for file_path in args.files:
        if not args.json:
            print(f"\n{'='*60}")
            print(f"Processing: {file_path}")
            print(f"{'='*60}")

        result = upload_audio(file_path, args.description)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n{format_output(result)}")

            clip_id = result.get("id") or result.get("clip_id")
            if clip_id:
                print(f"\n✓ Upload successful!")
                print(f"   Clip ID: {clip_id}")
                print(f"\n   Use this clip_id with:")
                print(f"   generate.py --mode cover --cover-clip-id {clip_id} --prompt 'your prompt'")

        results.append(result)

    if not args.json and len(results) > 1:
        print(f"\n{'='*60}")
        print(f"Uploaded {len(results)} file(s) successfully!")
        print(f"{'='*60}")

if __name__ == "__main__":
    main()
