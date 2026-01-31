#!/bin/bash
# Suno Download WAV Example
# Download high-quality audio files from completed tasks

echo "=== Suno Audio Download ==="
echo ""
echo "Download audio files from completed music generation tasks"
echo ""

echo "Example 1: Download all audio from a task"
echo "Command:"
echo "  python3 .claude/skills/suno-music/scripts/download-wav.py task-id-here"
echo ""

echo "Example 2: Download to specific directory"
echo "Command:"
echo "  python3 .claude/skills/suno-music/scripts/download-wav.py task-id-here --output ./my-music"
echo ""

echo "Example 3: List available files without downloading"
echo "Command:"
echo "  python3 .claude/skills/suno-music/scripts/download-wav.py task-id-here --list-only"
echo ""

echo "Example 4: Download only WAV format"
echo "Command:"
echo "  python3 .claude/skills/suno-music/scripts/download-wav.py task-id-here --wav-only"
echo ""

echo "Example 5: Download specific clip"
echo "Command:"
echo "  python3 .claude/skills/suno-music/scripts/download-wav.py task-id-here --clip-id clip-id-here"
echo ""

echo ""
echo "Notes:"
echo "  - Default output directory: ./suno-downloads"
echo "  - Supports both MP3 and WAV formats"
echo "  - Shows download progress"
echo "  - Automatically creates output directory"
