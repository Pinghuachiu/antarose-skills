#!/bin/bash
# Suno Batch Fetch Example
# Fetch multiple tasks at once

echo "=== Suno Batch Task Query ==="
echo ""
echo "Fetching multiple tasks..."
echo ""

# Example 1: Fetch multiple tasks by space-separated IDs
echo "Example 1: Fetch multiple tasks"
echo "Command:"
echo "  python3 .claude/skills/suno-music/scripts/batch-fetch.py task-id-1 task-id-2 task-id-3"
echo ""

# Example 2: Fetch using comma-separated IDs
echo "Example 2: Fetch using comma-separated string"
echo "Command:"
echo '  python3 .claude/skills/suno-music/scripts/batch-fetch.py --ids "id1,id2,id3"'
echo ""

# Example 3: Summary only
echo "Example 3: Show summary only"
echo "Command:"
echo "  python3 .claude/skills/suno-music/scripts/batch-fetch.py task-id-1 task-id-2 --summary"
echo ""

# Example 4: JSON output
echo "Example 4: Raw JSON output"
echo "Command:"
echo "  python3 .claude/skills/suno-music/scripts/batch-fetch.py task-id-1 task-id-2 --json"
echo ""

echo "Usage:"
echo "  python3 .claude/skills/suno-music/scripts/batch-fetch.py <task-id-1> <task-id-2> ..."
echo "  python3 .claude/skills/suno-music/scripts/batch-fetch.py --ids \"id1,id2,id3\""
