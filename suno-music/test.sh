#!/bin/bash
# Quick test script for suno-music skill

echo "=== Suno Music Generation - Test ==="
echo ""
echo "API Configuration:"
echo "  BASE_URL: ${ALLAPI_BASE_URL:-https://allapi.store/}"
echo "  API_KEY: ${ALLAPI_KEY:+(configured)}"
echo ""

# Check if API key is set
if [ -z "$ALLAPI_KEY" ]; then
  echo "⚠️  Warning: ALLAPI_KEY not set"
  echo "  Setting it now..."
  export ALLAPI_KEY="sk-eJtw92E4YJZrdF6bv0bjiIU4DAwo8nHC3XPZeQFRxwZ5i6mM"
  echo "  ✓ API Key configured"
fi

export ALLAPI_BASE_URL="https://allapi.store/"

echo ""
echo "Testing connection to allapi.store..."
if curl -s --head "https://allapi.store/" | head -n 1 > /dev/null; then
  echo "✓ Connection successful"
else
  echo "✗ Connection failed - DNS or network issue"
  echo ""
  echo "Possible solutions:"
  echo "1. Check your internet connection"
  echo "2. Try using a VPN"
  echo "3. Check if allapi.store is accessible"
  exit 1
fi

echo ""
echo "Ready to generate music!"
echo ""
echo "To generate your song, run:"
echo ""
echo "  export ALLAPI_KEY=\"sk-eJtw92E4YJZrdF6bv0bjiIU4DAwo8nHC3XPZeQFRxwZ5i6mM\""
echo "  export ALLAPI_BASE_URL=\"https://allapi.store/\""
echo ""
echo "  python3 .claude/skills/suno-music/scripts/generate.py \\"
echo "    --mode custom \\"
echo "    --title \"糖果色電車\" \\"
echo "    --tags \"japanese city pop,acoustic R&B,sweet,breezy\" \\"
echo "    --vocal-gender m \\"
echo "    --model chirp-v4 \\"
echo "    \"你的歌詞內容...\""
