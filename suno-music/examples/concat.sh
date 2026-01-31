#!/bin/bash
# Suno Concat Mode Example
# Concatenate/merge multiple songs together

echo "=== Suno Song Concatenation ==="
echo ""
echo "Merge multiple song clips into one"
echo ""

cat << 'EOF'
Usage:
  python3 .claude/skills/suno-music/scripts/generate.py \
    --mode concat \
    --concat-clips "clip-id-1,clip-id-2,clip-id-3" \
    --title "Merged Song"

Example:
  python3 .claude/skills/suno-music/scripts/generate.py \
    --mode concat \
    --concat-clips "abc123,def456,ghi789" \
    --title "My Medley"

Parameters:
  --concat-clips   Comma-separated list of clip IDs (at least 2)
  --title          Optional title for the merged song
  --prompt         Optional description
  --model          Model version (default: chirp-v4)

Workflow:
  1. Generate multiple songs using other modes
  2. Collect the clip IDs from each song
  3. Use concat mode to merge them together
  4. The result will be a seamless combination

Note: You need to have at least 2 existing clip IDs to use this mode
EOF
