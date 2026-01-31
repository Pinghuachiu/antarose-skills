#!/bin/bash
# Suno Custom Mode Example
# Full control over title, style, lyrics, and more

echo "=== Suno Music Generation - Custom Mode ==="
echo ""
echo "Generating music with custom parameters..."
echo ""

python3 .claude/skills/suno-music/scripts/generate.py \
  --mode custom \
  --title "Midnight City Dreams" \
  --tags "pop,synthwave,electronic,upbeat" \
  --prompt "Verse 1:
Walking through the neon lights
The city comes alive at night
Electric dreams in the air
Magic floating everywhere

Chorus:
Midnight city, calling my name
Dancing in the electric flame
Stars above, they shine so bright
We own the city tonight" \
  --model chirp-v4 \
  --vocal-gender f

echo ""
echo "Custom mode allows you to specify:"
echo "  --title        Song title"
echo "  --tags         Music styles (comma-separated)"
echo "  --prompt       Lyrics or creative direction"
echo "  --model        AI model version"
echo "  --vocal-gender m (male) or f (female)"
echo "  --negative-tags Styles to avoid"
