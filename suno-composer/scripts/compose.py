#!/usr/bin/env python3
"""
Suno Composer - AI Music Composer
Generate lyrics, recommend styles, and call Suno API to create songs
"""

import os
import sys
import time
import json
import argparse
import subprocess
from typing import Dict, Any, Optional, Tuple

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed", file=sys.stderr)
    print("Install it using: pip install anthropic", file=sys.stderr)
    sys.exit(1)

# API Keys
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ALLAPI_KEY = os.environ.get("ALLAPI_KEY", "")
KIE_API_KEY = os.environ.get("KIE_API_KEY", "")

def check_api_keys(provider: str):
    """Check if required API keys are set"""
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it using: export ANTHROPIC_API_KEY='your-key'", file=sys.stderr)
        sys.exit(1)

    if provider == "allapi" and not ALLAPI_KEY:
        print("Error: ALLAPI_KEY environment variable not set", file=sys.stderr)
        print("Please set it using: export ALLAPI_KEY='your-key'", file=sys.stderr)
        sys.exit(1)

    if provider == "kie" and not KIE_API_KEY:
        print("Error: KIE_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it using: export KIE_API_KEY='your-key'", file=sys.stderr)
        sys.exit(1)

def detect_language(text: str) -> str:
    """Detect if text is Chinese or English"""
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    if chinese_chars > len(text) * 0.3:
        return "chinese"
    return "english"

def generate_lyrics(theme: str, mood: str, style: str,
                    tempo: Optional[str] = None,
                    instruments: Optional[str] = None,
                    language: str = "auto") -> str:
    """Generate lyrics using Claude AI"""

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    # Detect language if auto
    if language == "auto":
        language = detect_language(theme + mood)

    # Build prompt
    if language == "chinese":
        prompt = f"""請為以下主題創作一首完整的歌曲歌詞：

主題：{theme}
情感：{mood}
風格：{style}"""
        if tempo:
            prompt += f"\n速度：{tempo}"
        if instruments:
            prompt += f"\n樂器：{instruments}"

        prompt += """

請按照以下結構創作：
[Verse 1]
（主歌第一段 - 設定場景和情境）

[Chorus]
（副歌 - 核心訊息和情感，需要朗朗上口）

[Verse 2]
（主歌第二段 - 發展故事或情感）

[Chorus]
（副歌 - 重複核心訊息）

[Bridge]
（橋段 - 情感轉折或高潮）

[Chorus]
（副歌 - 最後一次，更強烈）

[Outro]
（結尾 - 淡出或總結）

要求：
1. 歌詞要富有情感和畫面感
2. 副歌要容易記憶
3. 長度約 200-400 字
4. 只輸出歌詞內容，不要其他說明

請開始創作："""
    else:  # English
        prompt = f"""Create complete song lyrics for the following:

Theme: {theme}
Mood: {mood}
Style: {style}"""
        if tempo:
            prompt += f"\nTempo: {tempo}"
        if instruments:
            prompt += f"\nInstruments: {instruments}"

        prompt += """

Structure:
[Verse 1]
(Set the scene)

[Chorus]
(Core message - catchy and memorable)

[Verse 2]
(Develop the story)

[Chorus]
(Repeat core message)

[Bridge]
(Emotional turn or climax)

[Chorus]
(Final chorus - more intense)

[Outro]
(Fade out or conclusion)

Requirements:
1. Emotional and vivid lyrics
2. Catchy chorus
3. Length: 150-250 words
4. Output ONLY the lyrics, no explanations

Begin:"""

    try:
        print("🤖 Generating lyrics with AI...")
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        lyrics = response.content[0].text.strip()
        print("✓ Lyrics generated!")
        return lyrics

    except Exception as e:
        print(f"Error generating lyrics: {e}", file=sys.stderr)
        sys.exit(1)

def analyze_mood_and_style(mood: str, style: str,
                          theme: str) -> Tuple[str, str]:
    """Analyze mood and recommend Suno style tags"""

    # Mood to tags mapping
    mood_tags = {
        "快樂": ["upbeat", "happy", "energetic", "bright", "cheerful"],
        "悲傷": ["sad", "emotional", "melancholic", "slow", "ballad"],
        "激勵": ["empowering", "powerful", "energetic", "inspiring", "uplifting"],
        "浪漫": ["romantic", "warm", "love", "gentle", "sweet"],
        "神祕": ["mysterious", "dark", "atmospheric", "deep"],
        "輕鬆": ["relaxed", "peaceful", "calm", "chill", "acoustic"],
        "興奮": ["exciting", "high-energy", "fast", "intense"],
        "溫馨": ["warm", "cozy", "gentle", "comforting"],
        "孤單": ["lonely", "solitary", "quiet", "introspective"],
        "憤怒": ["angry", "aggressive", "intense", "powerful"],
    }

    # Style to tags mapping
    style_tags = {
        "流行": ["pop", "catchy", "radio-friendly"],
        "搖滾": ["rock", "guitar", "drums", "band"],
        "抒情": ["ballad", "piano", "slow", "emotional"],
        "民謠": ["folk", "acoustic", "guitar", "singer-songwriter"],
        "嘻哈": ["hip-hop", "rap", "beats", "rhythmic"],
        "R&B": ["r&b", "soul", "smooth", "groove"],
        "電子": ["electronic", "synth", "dance", "EDM"],
        "爵士": ["jazz", "smooth", "sophisticated", "improvisational"],
        "古典": ["classical", "orchestral", "elegant", "sophisticated"],
        "說唱": ["rap", "hip-hop", "flow", "rhythmic"],
        "鄉村": ["country", "acoustic", "guitar", "folk"],
        "金屬": ["metal", "heavy", "intense", "powerful"],
        "雷鬼": ["reggae", "island", "chill", "rhythmic"],
        "靈魂": ["soul", "gospel", "emotional", "powerful-vocals"],
    }

    # English equivalents
    style_tags_en = {
        "pop": ["pop", "catchy", "radio-friendly"],
        "rock": ["rock", "guitar", "drums", "band"],
        "ballad": ["ballad", "piano", "slow", "emotional"],
        "folk": ["folk", "acoustic", "guitar", "singer-songwriter"],
        "hip-hop": ["hip-hop", "rap", "beats", "rhythmic"],
        "r&b": ["r&b", "soul", "smooth", "groove"],
        "electronic": ["electronic", "synth", "dance", "EDM"],
        "jazz": ["jazz", "smooth", "sophisticated"],
        "classical": ["classical", "orchestral", "elegant"],
        "rap": ["rap", "hip-hop", "flow"],
        "country": ["country", "acoustic", "guitar"],
        "metal": ["metal", "heavy", "intense"],
        "reggae": ["reggae", "island", "chill"],
        "soul": ["soul", "gospel", "emotional"],
    }

    # Get style tags (support both Chinese and English)
    tags = style_tags.get(style, style_tags_en.get(style.lower(), [style]))

    # Add mood tags
    mood_lower = mood.lower()
    for mood_key, mood_values in mood_tags.items():
        if mood_key in mood or any(keyword in mood_lower for keyword in mood_values):
            tags.extend(mood_values)
            break

    # Add theme-based tags
    theme_lower = theme.lower()
    theme_keywords = {
        "愛": ["love", "romantic"],
        "愛情": ["love", "romantic"],
        "夏天": ["summer", "sunny", "beach"],
        "夜": ["night", "nocturnal", "late-night"],
        "城市": ["urban", "city"],
        "海灘": ["beach", "ocean", "summer"],
        "夢": ["dream", "ethereal", "floating"],
        "旅行": ["travel", "journey", "adventure"],
        "朋友": ["friendship", "together"],
        "舞": ["dance", "club", "party"],
    }

    for keyword, keyword_tags in theme_keywords.items():
        if keyword in theme_lower:
            tags.extend(keyword_tags)
            break

    # Remove duplicates and limit to 8 tags
    unique_tags = list(dict.fromkeys(tags))
    final_tags = unique_tags[:8]

    # Generate title
    title = generate_title(theme, mood, style)

    return ",".join(final_tags), title

def generate_title(theme: str, mood: str, style: str) -> str:
    """Generate a song title"""
    # Simple title generation
    titles = {
        "流行": ["夢想", "星光", "心跳", "時光", "約定"],
        "搖滾": ["覺醒", "突破", "狂野", "燃燒", "自由"],
        "抒情": ["回憶", "想念", "距離", "故事", "痕跡"],
        "民謠": ["旅途", "故鄉", "季節", "歲月", "足跡"],
        "嘻哈": ["實力", "態度", "節奏", "舞台", "玩家"],
        "R&B": ["專屬", "迷人的", "節奏", "夜晚", "靈魂"],
        "電子": ["脈搏", "電波", "幻覺", "飛翔", "未來"],
        "爵士": ["藍調", "夜晚", "情調", "搖擺", "氛圍"],
    }

    style_titles = titles.get(style, ["之歌", "回響", "旋律"])

    # Combine theme with style word
    if theme in ["失戀", "愛情", "夢想", "旅行"]:
        return theme
    else:
        import random
        return f"{theme} {random.choice(style_titles)}"

def call_suno_api(tags: str, title: str, lyrics: str,
                 provider: str, model: str,
                 vocal_gender: str,
                 persona_id: Optional[str] = None,
                 artist_clip_id: Optional[str] = None,
                 no_wait: bool = False) -> Dict[str, Any]:
    """Call Suno API to generate music"""

    print(f"\n🎵 Calling {provider.upper()} Suno API...")
    print(f"   Title: {title}")
    print(f"   Tags: {tags}")
    print(f"   Model: {model}")
    print()

    if provider == "allapi":
        return call_allapi(tags, title, lyrics, model, vocal_gender,
                          persona_id, artist_clip_id, no_wait)
    else:
        return call_kie(tags, title, lyrics, model, vocal_gender,
                       no_wait)

def call_allapi(tags: str, title: str, lyrics: str,
                model: str, vocal_gender: str,
                persona_id: Optional[str],
                artist_clip_id: Optional[str],
                no_wait: bool) -> Dict[str, Any]:
    """Call AllAPI Suno"""

    script_path = "/home/jackalchiu/claude/.claude/skills/suno-allapi/scripts/generate.py"

    # Build command
    cmd = [
        "python3", script_path,
        "--mode", "singer-style" if persona_id else "custom",
        "--title", title,
        "--tags", tags,
        "--prompt", lyrics,
        "--model", model,
        "--vocal-gender", vocal_gender
    ]

    if persona_id:
        cmd.extend(["--persona-id", persona_id])
    if artist_clip_id:
        cmd.extend(["--artist-clip-id", artist_clip_id])
    if no_wait:
        cmd.append("--no-wait")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        print(f"Error calling AllAPI: {e}", file=sys.stderr)
        print(f"Output: {e.output}", file=sys.stderr)
        return {"success": False, "error": str(e)}

def call_kie(tags: str, title: str, lyrics: str,
             model: str, vocal_gender: str,
             no_wait: bool) -> Dict[str, Any]:
    """Call Kie.ai Suno"""

    script_path = "/home/jackalchiu/claude/.claude/skills/suno-kie/scripts/generate.py"

    # Build command
    cmd = [
        "python3", script_path,
        "--prompt", lyrics,
        "--style", tags,
        "--title", title,
        "--custom-mode", "true",
        "--model", model
    ]

    if vocal_gender:
        cmd.extend(["--vocal-gender", vocal_gender])
    if no_wait:
        cmd.append("--no-wait")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        print(f"Error calling Kie.ai: {e}", file=sys.stderr)
        print(f"Output: {e.output}", file=sys.stderr)
        return {"success": False, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(
        description="AI Music Composer - Generate lyrics and create songs with Suno API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple pop song
  %(prog)s --theme "夏天海灘" --mood "快樂" --style "流行"

  # Emotional ballad
  %(prog)s --theme "失戀" --mood "悲傷" --style "抒情"

  # With Persona
  %(prog)s --theme "新歌" --mood "溫馨" --style "流行" \\
    --persona-id "xxx" --artist-clip-id "yyy"

  # English song
  %(prog)s --theme "love" --mood "romantic" --style "pop" --language english

  # Only generate lyrics (no API call)
  %(prog)s --theme "春天" --mood "溫暖" --style "民謠" --lyrics-only
        """
    )

    # Required parameters
    parser.add_argument("--theme", required=True, help="Song theme/topic")
    parser.add_argument("--mood", required=True, help="Emotional mood")
    parser.add_argument("--style", required=True, help="Music style/genre")

    # Optional parameters
    parser.add_argument("--tempo", help="Tempo description (slow/medium/fast)")
    parser.add_argument("--instruments", help="Instrument description")
    parser.add_argument("--vocal-gender", default="m", choices=["m", "f"],
                       help="Vocal gender (default: m)")
    parser.add_argument("--language", default="auto",
                       choices=["auto", "chinese", "english"],
                       help="Lyrics language (default: auto-detect)")
    parser.add_argument("--provider", default="allapi",
                       choices=["allapi", "kie"],
                       help="Suno API provider (default: allapi)")
    parser.add_argument("--model", default="chirp-v4",
                       help="Suno model (default: chirp-v4)")
    parser.add_argument("--lyrics-only", action="store_true",
                       help="Only generate lyrics, don't call Suno API")
    parser.add_argument("--no-wait", action="store_true",
                       help="Return immediately without waiting for completion")

    # Persona parameters
    parser.add_argument("--persona-id", help="Persona ID (AllAPI only)")
    parser.add_argument("--artist-clip-id", help="Artist Clip ID (AllAPI only)")

    args = parser.parse_args()

    # Check API keys
    check_api_keys(args.provider)

    print("=" * 60)
    print("🎵 Suno Composer - AI Music Composer")
    print("=" * 60)
    print(f"Theme: {args.theme}")
    print(f"Mood: {args.mood}")
    print(f"Style: {args.style}")
    print(f"Language: {args.language}")
    print(f"Provider: {args.provider.upper()}")
    print("=" * 60)
    print()

    # Step 1: Generate lyrics
    lyrics = generate_lyrics(
        args.theme, args.mood, args.style,
        args.tempo, args.instruments, args.language
    )

    # Step 2: Analyze and get tags/title
    tags, title = analyze_mood_and_style(args.mood, args.style, args.theme)

    print(f"\n📋 Generated Metadata:")
    print(f"   Title: {title}")
    print(f"   Tags: {tags}")
    print()

    if args.lyrics_only:
        print("=" * 60)
        print("📝 Generated Lyrics:")
        print("=" * 60)
        print(lyrics)
        print()
        print("=" * 60)
        print("JSON Output:")
        print("=" * 60)
        output = {
            "title": title,
            "tags": tags,
            "prompt": lyrics,
            "vocal_gender": args.vocal_gender
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    # Step 3: Call Suno API
    result = call_suno_api(
        tags, title, lyrics,
        args.provider, args.model,
        args.vocal_gender,
        args.persona_id, args.artist_clip_id,
        args.no_wait
    )

    if result.get("success"):
        print("\n🎉 Song creation process completed!")
    else:
        print(f"\n❌ Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
