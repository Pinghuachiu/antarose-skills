#!/bin/bash
# English Song Example - Suno Composer
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export ALLAPI_KEY="your-allapi-key"

echo "=== Creating an English Love Song ==="

python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "falling in love in the city" \
  --mood "romantic and dreamy" \
  --style "pop" \
  --language english \
  --vocal-gender f \
  --provider allapi

echo ""
echo "✅ English love song created!"
