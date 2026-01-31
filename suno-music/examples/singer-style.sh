#!/bin/bash
# Suno Singer Style Mode Example
# Generate music with specific vocal style

echo "=== Suno Singer Style Mode ==="
echo ""
echo "Generate music with specific singer vocal style"
echo ""

python3 .claude/skills/suno-music/scripts/generate.py \
  --mode singer-style \
  --title "Jazz Night" \
  --tags "jazz,smooth,relaxing,piano" \
  --prompt "Verse 1:
Late night in the city
Lights are fading low
I hear a melody
That makes me want to go

Chorus:
Take me to that jazz club
Where the music flows
Dancing in the moonlight
Where the trumpet blows" \
  --vocal-gender f \
  --model chirp-v4

echo ""
echo "Singer style mode allows:"
echo "  --title        Song title"
echo "  --tags         Musical style and mood"
echo "  --prompt       Lyrics or creative direction"
echo "  --vocal-gender m (male) or f (female) vocals"
echo "  --model        AI model version"
echo ""
echo "This mode emphasizes vocal styling and delivery"
