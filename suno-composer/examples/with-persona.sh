#!/bin/bash
# With Persona Example - Suno Composer
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export ALLAPI_KEY="your-allapi-key"

echo "=== Creating Song with Persona (Voice Cloning) ==="
echo ""
echo "Prerequisites:"
echo "1. You need to have a persona_id from suno-allapi"
echo "2. You need the original artist_clip_id"
echo ""

# Example with Persona
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "新的開始" \
  --mood "充滿希望、溫暖" \
  --style "流行" \
  --persona-id "your-persona-id" \
  --artist-clip-id "your-artist-clip-id" \
  --vocal-gender m \
  --provider allapi

echo ""
echo "✅ Song created with your custom voice persona!"
echo ""
echo "💡 Tip: Use suno-allapi's Persona feature to create consistent voice"
echo "   across multiple songs."
