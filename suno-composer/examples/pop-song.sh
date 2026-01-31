#!/bin/bash
# Pop Song Example - Suno Composer
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export ALLAPI_KEY="your-allapi-key"

echo "=== Creating a Happy Pop Song ==="

python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "夏天去海灘度假" \
  --mood "快樂、充滿活力、陽光" \
  --style "流行" \
  --tempo "輕快" \
  --vocal-gender m \
  --provider allapi

echo ""
echo "✅ Happy pop song about summer beach created!"
