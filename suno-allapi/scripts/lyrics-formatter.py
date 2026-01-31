#!/usr/bin/env python3
"""
Suno 格式化歌詞生成器
根據 Suno AI 最佳實踐創建結構化歌詞

功能：
- 自動添加結構標籤
- 標籤提示
- 格式優化

Sources:
- https://sunometatagcreator.com/metatags-guide
- https://jackrighteous.com/pages/suno-ai-meta-tags-guide
- https://learnprompting.org/blog/guide-suno
- https://suno.com/hub/how-to-make-a-song
"""

import sys
import argparse

def create_structure_template(title: str, style: str, mood: str = "") -> str:
    """創建 Suno 歌曲結構模板"""
    template = f"""Suno 量身打造的結構。我將這首歌設定為{style}風格。

歌曲標題：{title}
建議風格 (Style): {style}

{mood}

[Verse 1]
在此填入第一段主歌歌詞...

[Chorus]
在此填入副歌（記憶點）...

[Verse 2]
在此填入第二段主歌歌詞...

[Bridge]
在此填入橋段（過渡/轉折）...

[Chorus]
重複副歌...

[Outro]
結尾（淡出）...

Suno 使用小撇步：
- Style Description: 複製上面的 Style 標籤放入 Suno 的 "Style of Music" 欄位
- 結構標籤: [Verse], [Chorus], [Bridge], [Outro] 幫助 AI 識別段落
- 情感提示: 在歌詞中適當使用空格引導停頓感
- 保持簡潔: 每行不要太長，保持節奏感
"""
    return template

def format_lyrics(lyrics: str, add_tags: bool = True) -> str:
    """格式化現有歌詞，添加標籤"""
    if not add_tags:
        return lyrics

    lines = lyrics.strip().split('\n')
    formatted = []

    # 檢測是否已有標籤
    has_tags = any(line.strip().startswith('[') for line in lines)

    if has_tags:
        # 已有標籤，直接返回
        return lyrics

    # 自動添加標籤（簡單版本）
    formatted.append("[Verse 1]")
    formatted.append("")

    verse_count = 0
    chorus_count = 0
    in_verse = True

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 檢測副歌特徵（重複、簡短、情緒高漲）
        if len(line) < 50 and verse_count > 0 and '！' not in line and '。' not in line:
            if chorus_count == 0:
                formatted.append("")
                formatted.append("[Chorus]")
                formatted.append("")
                in_verse = False
                chorus_count += 1
            formatted.append(line)
        else:
            if not in_verse and verse_count == 0:
                formatted.append("")
                formatted.append("[Verse 2]")
                formatted.append("")
                in_verse = True
                verse_count += 1
            formatted.append(line)

    formatted.append("")
    formatted.append("[Outro]")

    return '\n'.join(formatted)

def add_meta_tags(lyrics: str, tags: list) -> str:
    """添加 Meta Tags 到歌詞"""
    if not tags:
        return lyrics

    lines = lyrics.split('\n')
    result = []

    for line in lines:
        # 在相關段落前添加 Meta Tags
        if '[Verse]' in line and '[Male vocals]' in tags:
            result.append("[Male vocals]")
            result.append(line)
        elif '[Verse]' in line and '[Female vocals]' in tags:
            result.append("[Female vocals]")
            result.append(line)
        elif '[Instrumental]' in line:
            result.append(line)
        elif '[Chorus]' in line and '[High Energy]' in tags:
            result.append("[High Energy]")
            result.append(line)
        elif '[Bridge]' in line and '[Emotional]' in tags:
            result.append("[Emotional]")
            result.append(line)
        else:
            result.append(line)

    return '\n'.join(result)

def show_available_tags():
    """顯示所有可用的 Meta Tags"""
    print("="*60)
    print("🏷️ Suno 可用的 Meta Tags")
    print("="*60)
    print("\n【結構標籤】")
    print("  [Intro]      - 開頭")
    print("  [Verse]     - 主歌")
    print("  [Chorus]    - 副歌（記憶點）")
    print("  [Bridge]    - 橋段（過渡/轉折）")
    print("  [Outro]     - 結尾")
    print("  [Interlude]  - 間奏段落")

    print("\n【Meta Tags - 聲音】")
    print("  [Male vocals]       - 男聲")
    print("  [Female vocals]     - 女聲")
    print("  [Duet]              - 對唱")
    print("  [Choir]             - 合唱")

    print("\n【Meta Tags - 情緒/風格】")
    print("  [High Energy]       - 高能量")
    print("  [Dreamy]            - 夢幻")
    print("  [Nostalgic]         - 懷舊")
    print("  [Emotional]        - 情感化")
    print("  [Peaceful]          - 平靜")
    print("  [Epic]              - 史詩")

    print("\n【Meta Tags - 特殊效果】")
    print("  [Instrumental]       - 純音樂段落")
    print("  [Instrumental break] - 樂奏性純音樂")
    print("  [Audience laughing] - 觀眾笑聲")
    print("  [Tempo increase]    - 節奏加快")
    print("  [Tempo decrease]    - 節奏減慢")

    print("\n【使用建議】")
    print("1. 保持歌詞簡潔，每行不要太長")
    print("2. Chorus 應該簡短、易記、可重複")
    print("3. Bridge 應該與 Verse/Chorus 形成對比")
    print("4. 適當使用空格引導停頓感")
    print("5. Meta Tags 放在相關段落標籤的下一行")

    print("="*60)

def main():
    parser = argparse.ArgumentParser(
        description="生成 Suno 格式化的結構化歌詞",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 顯示所有可用標籤
  %(prog)s --show-tags

  # 創建結構模板
  %(prog)s --title "銀色私語" --style "Soulful Pop,R&B" --mood "夢幻溫柔"

  # 格式化現有歌詞
  %(prog)s --format "我的歌詞內容..." --add-tags

  # 添加 Meta Tags
  %(prog)s --add-meta "我的歌詞..." --tags "Female vocals,Emotional"
        """
    )

    parser.add_argument("--show-tags", action="store_true", help="顯示所有可用的 Meta Tags")
    parser.add_argument("--format", help="格式化現有歌詞（添加結構標籤）")
    parser.add_argument("--title", help="歌曲標題")
    parser.add_argument("--style", help="音樂風格（逗號分隔）")
    parser.add_argument("--mood", default="", help="歌曲情緒/氛圍描述")
    parser.add_argument("--add-meta", help="添加 Meta Tags 到歌詞")
    parser.add_argument("--tags", help="Meta Tags（逗號分隔）")

    args = parser.parse_args()

    if args.show_tags:
        show_available_tags()
        return

    if args.title and args.style:
        template = create_structure_template(args.title, args.style, args.mood)
        print(template)
        print("\n" + "="*60)
        print("💡 提示：將上面的模板填入歌詞後，用於生成音樂")
        print("="*60)
    elif args.format:
        formatted = format_lyrics(args.format)
        print(formatted)
    elif args.add_meta:
        tags = args.tags.split(',') if args.tags else []
        result = add_meta_tags(args.add_meta, tags)
        print(result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
