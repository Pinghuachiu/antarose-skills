#!/usr/bin/env python3
"""
Pix2 Upload Script
Upload files to Pix2 image hosting service
Supports: PNG, JPEG, WebP, MP3, MP4
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

# API Configuration
API_KEY = os.environ.get("PIX2_API_KEY", "23df301b63a33587541a8680ef9472b9")
API_URL = "https://api.pix2.io/api/images"

# MIME type mapping
MIME_TYPES = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
    '.mp3': 'audio/mpeg',
    '.mp4': 'video/mp4'
}

def get_mime_type(file_path):
    """Get MIME type based on file extension"""
    ext = Path(file_path).suffix.lower()
    return MIME_TYPES.get(ext)

def upload_file(file_path, api_key=API_KEY):
    """Upload file to Pix2 API"""
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return None

    # Get MIME type
    mime_type = get_mime_type(file_path)
    if not mime_type:
        print(f"Error: Unsupported file type: {Path(file_path).suffix}", file=sys.stderr)
        print(f"Supported types: {', '.join(MIME_TYPES.keys())}", file=sys.stderr)
        return None

    # Check file size (max 50MB)
    file_size = os.path.getsize(file_path)
    max_size = 50 * 1024 * 1024  # 50MB
    if file_size > max_size:
        print(f"Error: File too large ({file_size / 1024 / 1024:.1f}MB, max 50MB)", file=sys.stderr)
        return None

    # Prepare upload
    url = API_URL
    headers = {
        'x-api-key': api_key
    }

    # Open file and prepare multipart form data
    # Key fix: For MP3/MP4, we need to specify the MIME type explicitly
    files = {
        'file': (os.path.basename(file_path), open(file_path, 'rb'), mime_type)
    }

    try:
        print(f"Uploading {os.path.basename(file_path)} ({file_size / 1024:.1f} KB)...")
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        data = response.json()

        if data.get('success'):
            return data
        else:
            print(f"Error: {data.get('error', 'Unknown error')}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Upload error: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}", file=sys.stderr)
        return None
    finally:
        files['file'][1].close()

def format_output(data, output_format='text'):
    """Format upload result output"""
    if not data:
        return ""

    if output_format == 'json':
        return json.dumps(data, indent=2, ensure_ascii=False)

    # Text format
    output = []
    output.append("✓ Upload successful!")
    output.append(f"  ID: {data['id']}")
    output.append(f"  Short URL: {data['url']}")
    output.append(f"  Direct URL: {data['directUrl']}")
    output.append(f"  Size: {data['size']:,} bytes ({data['size'] / 1024:.1f} KB)")
    output.append(f"  Type: {data['contentType']}")
    output.append(f"  Uploaded: {data['uploadTime']}")

    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(
        description="Upload files to Pix2 image hosting",
        epilog="""
Examples:
  # Upload image
  %(prog)s image.jpg

  # Upload MP3 audio
  %(prog)s song.mp3

  # Upload MP4 video
  %(prog)s video.mp4

  # Output JSON format
  %(prog)s image.png --json

  # Use custom API key
  %(prog)s file.jpg --api-key YOUR_API_KEY

Supported formats: PNG, JPG, JPEG, WebP, MP3, MP4
Max file size: 50MB
        """
    )

    parser.add_argument("file", help="File to upload")
    parser.add_argument("--json", action="store_true",
                       help="Output in JSON format")
    parser.add_argument("--api-key",
                       help="Pix2 API key (default: from PIX2_API_KEY env var)")

    args = parser.parse_args()

    # Use provided API key or default
    api_key = args.api_key or API_KEY

    if not api_key:
        print("Error: API key not set. Use --api-key or set PIX2_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    # Upload file
    result = upload_file(args.file, api_key)

    if result:
        print(format_output(result, 'json' if args.json else 'text'))
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
