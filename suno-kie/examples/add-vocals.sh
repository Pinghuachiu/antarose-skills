#!/bin/bash
# Add Vocals Examples for Kie.ai Suno API
# This script demonstrates how to add AI-generated vocals to instrumental tracks

# Make sure to set your API key first:
# export KIE_API_KEY="your-kie-api-key"

echo "=== Add Vocals Examples ==="
echo

# Example 1: Simple mode - just describe what you want
echo "Example 1: Simple mode - Add vocals to piano instrumental"
echo "----------------------------------------------------------------"
python3 .claude/skills/suno-kie/scripts/add-vocals.py \
  --upload-url "https://storage.example.com/piano-instrumental.mp3" \
  --prompt "創作關於夏天的快樂歌詞，海灘陽光" \
  --custom-mode false

echo
echo

# Example 2: Custom mode - Hip-Hop with male vocals
echo "Example 2: Custom mode - Add rap vocals to beat"
echo "----------------------------------------------------------------"
python3 .claude/skills/suno-kie/scripts/add-vocals.py \
  --upload-url "https://storage.example.com/hiphop-beat.mp3" \
  --prompt "城市夜生活，霓虹燈，街頭文化" \
  --style "Hip-Hop" \
  --title "Midnight City" \
  --vocal-gender m \
  --custom-mode true

echo
echo

# Example 3: Pop ballad with female vocals
echo "Example 3: Custom mode - Add female vocals to ballad"
echo "----------------------------------------------------------------"
python3 .claude/skills/suno-kie/scripts/add-vocals.py \
  --upload-url "https://storage.example.com/piano-ballad.mp3" \
  --prompt "愛情故事，溫柔感人的歌詞" \
  --style "Pop Ballad" \
  --title "My Heart" \
  --vocal-gender f \
  --custom-mode true

echo
echo

# Example 4: Rock song
echo "Example 4: Custom mode - Add vocals to rock instrumental"
echo "----------------------------------------------------------------"
python3 .claude/skills/suno-kie/scripts/add-vocals.py \
  --upload-url "https://storage.example.com/rock-instrumental.mp3" \
  --prompt "突破自我，追夢，永不放棄" \
  --style "Rock" \
  --title "Break Free" \
  --vocal-gender m \
  --weirdness 0.3 \
  --custom-mode true

echo
echo

# Example 5: No wait - submit and get task ID
echo "Example 5: No wait mode - Submit task and return immediately"
echo "----------------------------------------------------------------"
python3 .claude/skills/suno-kie/scripts/add-vocals.py \
  --upload-url "https://storage.example.com/instrumental.mp3" \
  --prompt "快樂的歌曲" \
  --custom-mode false \
  --no-wait

echo
echo "=== Tips ==="
echo "1. Upload your instrumental to cloud storage first (Google Drive, Dropbox, AWS S3)"
echo "2. Make sure the URL is publicly accessible"
echo "3. Audio should not exceed 2 minutes"
echo "4. Vocals will be auto-generated to match your instrumental's mood and key"
echo "5. Use --vocal-gender to specify male (m) or female (f) vocals"
echo "6. Use fetch.py to check task status later: fetch.py TASK_ID --wait"
