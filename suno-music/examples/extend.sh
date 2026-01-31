#!/bin/bash
# Suno Extend Mode Example
# Continue composing from a specific timestamp

echo "=== Suno Music Generation - Extend Mode ==="
echo ""
echo "This mode requires a previous task ID to continue from."
echo ""
echo "Example usage:"
echo ""

cat << 'EOF'
python3 .claude/skills/suno-music/scripts/generate.py \
  --mode extend \
  --task-id "previous-task-id-here" \
  --continue-clip-id "clip-id-from-previous-task" \
  --continue-at 120.5 \
  --prompt "Add an instrumental bridge with guitar solo"

Parameters:
  --task-id           The task ID of the original song
  --continue-clip-id  The clip ID to continue from
  --continue-at       Timestamp (in seconds) to start from
  --prompt            What to add in the extension
  --model             Model version (default: chirp-v4)

Workflow:
  1. Generate a song using inspiration or custom mode
  2. Get the task_id and clip_id from the output
  3. Use extend mode to continue from a specific point
  4. The AI will compose additional music seamlessly
EOF

echo ""
echo "Note: You need to run inspiration.sh or custom.sh first to get a task ID"
