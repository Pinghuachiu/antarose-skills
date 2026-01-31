#!/bin/bash
# Ballad Example - Suno Composer
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export ALLAPI_KEY="your-allapi-key"

echo "=== Creating an Emotional Ballad ==="

python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "深夜想起前任" \
  --mood "悲傷、懷念、孤單" \
  --style "抒情" \
  --tempo "慢" \
  --instruments "鋼琴、弦樂" \
  --vocal-gender f \
  --provider allapi

echo ""
echo "✅ Emotional ballad about lost love created!"
