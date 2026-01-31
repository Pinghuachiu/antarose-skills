#!/bin/bash
# Suno Inspiration Mode Example
# Simple one-line prompt to generate complete music

echo "=== Suno Music Generation - Inspiration Mode ==="
echo ""
echo "Generating music with simple prompt..."
echo ""

python3 .claude/skills/suno-music/scripts/generate.py \
  "A happy upbeat pop song about summer adventures"

# Or try these other prompts:
# "A sad emotional piano ballad"
# "An energetic electronic dance track"
# "A relaxing lo-fi hip hop beat"
# "A dramatic orchestral cinematic piece"

echo ""
echo "To use your own prompt:"
echo "  python3 .claude/skills/suno-music/scripts/generate.py \"your prompt here\""
