#!/usr/bin/env python3
"""
Suno Batch Fetch Script
Fetch multiple Suno music generation tasks at once
"""

import os
import sys
import json
import argparse
import requests
from typing import List

# API Configuration
BASE_URL = os.environ.get("ALLAPI_BASE_URL", "https://allapi.store/")
API_KEY = os.environ.get("ALLAPI_KEY", "")

def check_api_key():
    """Check if API key is set"""
    if not API_KEY:
        print("Error: ALLAPI_KEY environment variable not set", file=sys.stderr)
        print("Please set it using: export ALLAPI_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)

def batch_fetch_tasks(task_ids: List[str]) -> List[dict]:
    """Fetch multiple tasks at once"""
    url = f"{BASE_URL}suno/fetch"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    params = {"ids": task_ids}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tasks: {e}", file=sys.stderr)
        sys.exit(1)

def format_output(tasks: List[dict]) -> str:
    """Format tasks output for display"""
    output = []
    for task in tasks:
        output.append({
            "task_id": task.get("task_id"),
            "status": task.get("status"),
            "action": task.get("action"),
            "submit_time": task.get("submitTime"),
            "start_time": task.get("startTime"),
            "finish_time": task.get("finishTime"),
            "fail_reason": task.get("failReason"),
            "data": task.get("data", [])
        })
    return json.dumps(output, indent=2, ensure_ascii=False)

def display_summary(tasks: List[dict]):
    """Display summary of fetched tasks"""
    total = len(tasks)
    success = sum(1 for t in tasks if t.get("status") == "SUCCESS")
    failed = sum(1 for t in tasks if t.get("status") == "FAILURE")
    in_progress = sum(1 for t in tasks if t.get("status") in ["NOT_START", "SUBMITTED", "QUEUED", "IN_PROGRESS"])

    print(f"\nSummary:", file=sys.stderr)
    print(f"  Total tasks: {total}", file=sys.stderr)
    print(f"  ✓ Success: {success}", file=sys.stderr)
    print(f"  ✗ Failed: {failed}", file=sys.stderr)
    print(f"  ⟳ In Progress: {in_progress}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Fetch multiple Suno music generation tasks",
        epilog="""
Examples:
  # Fetch multiple tasks
  %(prog)s task-id-1 task-id-2 task-id-3

  # Fetch from comma-separated string
  %(prog)s --ids "id1,id2,id3"

  # Fetch with summary only
  %(prog)s task-id-1 task-id-2 --summary

  # Output raw JSON
  %(prog)s task-id-1 task-id-2 --json
        """
    )

    parser.add_argument("task_ids", nargs="*", help="Task IDs to fetch")
    parser.add_argument("--ids", help="Comma-separated task IDs")
    parser.add_argument("--summary", action="store_true", help="Show summary only")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    # Parse task IDs
    task_ids = []

    if args.ids:
        task_ids = [tid.strip() for tid in args.ids.split(",") if tid.strip()]

    if args.task_ids:
        task_ids.extend(args.task_ids)

    if not task_ids:
        parser.error("No task IDs provided. Use: batch-fetch.py task-id-1 task-id-2 ... or --ids id1,id2,id3")

    # Check API key
    check_api_key()

    # Fetch tasks
    print(f"Fetching {len(task_ids)} task(s)...", file=sys.stderr)
    tasks = batch_fetch_tasks(task_ids)

    if not tasks:
        print("No tasks found", file=sys.stderr)
        sys.exit(1)

    # Display summary
    display_summary(tasks)

    # Output
    if args.summary:
        return

    if args.json:
        print(json.dumps(tasks, indent=2, ensure_ascii=False))
    else:
        print("\nTask Details:")
        print(format_output(tasks))

        # Display individual task info
        for i, task in enumerate(tasks, 1):
            status = task.get("status", "UNKNOWN")
            task_id = task.get("task_id", "unknown")
            print(f"\n[{i}] Task {task_id}: {status}", file=sys.stderr)

            if status == "SUCCESS":
                data = task.get("data", [])
                if data:
                    print(f"    Generated {len(data)} clip(s)", file=sys.stderr)

            elif status == "FAILURE":
                print(f"    Failed: {task.get('failReason', 'Unknown error')}", file=sys.stderr)

if __name__ == "__main__":
    main()
