#!/bin/bash
# Rock Song Example - Suno Composer
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export ALLAPI_KEY="your-allapi-key"

echo "=== Creating an Empowering Rock Song ==="

python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "突破困境追夢" \
  --mood "激勵、力量、熱血" \
  --style "搖滾" \
  --tempo "快" \
  --instruments "電吉他、鼓、貝斯" \
  --vocal-gender m \
  --provider allapi

echo ""
echo "✅ Empowering rock song created!"
