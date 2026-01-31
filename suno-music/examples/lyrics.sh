#!/bin/bash
# Suno Lyrics Generation Example
# Generate lyrics only (without music)

echo "=== Suno Lyrics Generation ==="
echo ""
echo "Generating lyrics..."
echo ""

python3 .claude/skills/suno-music/scripts/lyrics.py \
  "Write a song about the beauty of nature and changing seasons" \
  --model chirp-v4

echo ""
echo "Try other prompts:"
echo "  python3 .claude/skills/suno-music/scripts/lyrics.py \"A love song about eternal devotion\""
echo "  python3 .claude/skills/suno-music/scripts/lyrics.py \"An energetic workout anthem\""
echo "  python3 .claude/skills/suno-music/scripts/lyrics.py \"A melancholic song about lost dreams\""
