#!/usr/bin/env python3
"""
Kie.ai Suno Generate Persona Script
Create a personalized music Persona from generated audio
"""

import os
import sys
import json
import argparse
import requests
from typing import Dict, Any

# API Configuration
BASE_URL = "https://api.kie.ai/api/v1"
API_KEY = os.environ.get("KIE_API_KEY", "")

def check_api_key():
    """Check if API key is set"""
    if not API_KEY:
        print("Error: KIE_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it using: export KIE_API_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)

def generate_persona(task_id: str, audio_id: str, name: str, description: str) -> Dict[str, Any]:
    """Generate a Persona from audio"""
    url = f"{BASE_URL}/generate-persona"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "taskId": task_id,
        "audioId": audio_id,
        "name": name,
        "description": description
    }

    try:
        print(f"Creating Persona: {name}")
        print(f"Task ID: {task_id}")
        print(f"Audio ID: {audio_id}")
        print()

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error generating persona: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a music Persona from generated audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a Persona from generated music
  %(prog)s --task-id "abc123" --audio-id "def456" --name "My Voice" --description "Pop singer style"

  # Create with detailed description
  %(prog)s --task-id "abc123" --audio-id "def456" \\
    --name "Classical Piano" \\
    --description "優雅的古典鋼琴風格，適合抒情歌曲，節奏溫和"

Workflow:
  1. Generate music using generate.py
  2. Note the taskId and audioId from the output
  3. Run this script to create a Persona
  4. Use the returned personaId in future generate.py calls
        """
    )

    parser.add_argument("--task-id", required=True, help="Music generation task ID")
    parser.add_argument("--audio-id", required=True, help="Audio ID from the task")
    parser.add_argument("--name", required=True, help="Persona name")
    parser.add_argument("--description", required=True, help="Detailed description of the Persona")
    parser.add_argument("--json", action="store_true", help="Output raw JSON only")

    args = parser.parse_args()

    # Check API key
    check_api_key()

    # Generate persona
    result = generate_persona(args.task_id, args.audio_id, args.name, args.description)

    # Check result
    if result.get("code") != 200:
        print(f"Error: {result.get('msg')}", file=sys.stderr)

        # Provide helpful error messages
        msg = result.get('msg', '')
        if 'Persona already exists' in msg:
            print("\n💡 Hint: Each audio ID can only generate one Persona.", file=sys.stderr)
            print("   Use a different audio ID or check existing Personas.", file=sys.stderr)
        elif 'not found' in msg.lower() or 'does not exist' in msg.lower():
            print("\n💡 Hint: Make sure the task has completed successfully.", file=sys.stderr)
            print("   Use fetch.py to check task status first.", file=sys.stderr)
        elif 'model' in msg.lower():
            print("\n💡 Hint: Persona generation only supports models above v3.5.", file=sys.stderr)
            print("   v3.5 itself is not supported.", file=sys.stderr)

        sys.exit(1)

    persona_id = result.get("data", {}).get("personaId")

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"✓ Persona created successfully!")
        print(f"\n   Persona ID: {persona_id}")
        print(f"   Name: {args.name}")
        print(f"\n   Use this personaId in generate.py:")
        print(f"   generate.py --prompt '...' --style 'pop' --title 'Song' --persona-id {persona_id}")

if __name__ == "__main__":
    main()
