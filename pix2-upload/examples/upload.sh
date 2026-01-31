#!/bin/bash
# Pix2 Upload Examples
# Upload various file types to Pix2 hosting

echo "=== Pix2 Upload Examples ==="
echo ""

# Example 1: Upload image
echo "Example 1: Upload image"
echo "Command:"
echo "  python3 .claude/skills/pix2-upload/scripts/upload.py photo.jpg"
echo ""

# Example 2: Upload MP3
echo "Example 2: Upload MP3 audio"
echo "Command:"
echo "  python3 .claude/skills/pix2-upload/scripts/upload.py music.mp3"
echo ""

# Example 3: Upload MP4
echo "Example 3: Upload MP4 video"
echo "Command:"
echo "  python3 .claude/skills/pix2-upload/scripts/upload.py video.mp4"
echo ""

# Example 4: JSON output
echo "Example 4: Upload and get JSON output"
echo "Command:"
echo "  python3 .claude/skills/pix2-upload/scripts/upload.py file.png --json"
echo ""

# Example 5: Custom API key
echo "Example 5: Use custom API key"
echo "Command:"
echo "  python3 .claude/skills/pix2-upload/scripts/upload.py file.jpg --api-key YOUR_KEY"
echo ""

echo "Supported formats:"
echo "  - Images: PNG, JPG, JPEG, WebP"
echo "  - Audio: MP3"
echo "  - Video: MP4"
echo ""
echo "Max file size: 50MB"
echo ""
echo "Key fix for MP3/MP4:"
echo "  The script automatically adds the correct MIME type (audio/mpeg, video/mp4)"
echo "  This is required for Pix2 API to accept non-image files"
