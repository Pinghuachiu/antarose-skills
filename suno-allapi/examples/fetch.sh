#!/bin/bash
# Suno Fetch Task Example
# Check task status and retrieve results

echo "=== Suno Task Status Query ==="
echo ""
echo "Usage:"
echo "  python3 .claude/skills/suno-music/scripts/fetch.py <task-id>"
echo ""
echo "Example:"
echo "  python3 .claude/skills/suno-music/scripts/fetch.py f4a94d75-087b-4bb1-bd45-53ba293faf96"
echo ""
echo "Output JSON format:"
echo "  python3 .claude/skills/suno-music/scripts/fetch.py <task-id> --json"
echo ""

# Check if task ID is provided
if [ -z "$1" ]; then
  echo "Please provide a task ID:"
  echo "  $0 f4a94d75-087b-4bb1-bd45-53ba293faf96"
  exit 1
fi

# Execute fetch
python3 .claude/skills/suno-music/scripts/fetch.py "$1"
