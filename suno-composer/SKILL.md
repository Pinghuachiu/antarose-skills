---
name: suno-composer
description: AI 音樂作曲助手 - 自動生成歌詞、推薦風格、調用 Suno API 一條龍完成歌曲創作
metadata:
  category: audio
  type: generation
  languages:
    - python
---

# Suno Composer - AI 音樂作曲助手

智能音樂創作助手，自動完成歌詞創作、風格推薦、並調用 Suno API 生成完整歌曲。

## 功能特性

- **🤖 AI 歌詞生成** - 根據主題、情感自動創作結構化歌詞
- **🎨 智能風格推薦** - 分析歌詞情感並推薦最適合的音樂風格
- **🔄 格式轉換** - 自動轉換成 Suno API 格式
- **🎤 一鍵生成** - 自動調用 suno-allapi 或 suno-kie 生成歌曲
- **🌏 中英支援** - 支援中文和英文歌詞生成
- **🎭 Persona 支援** - 可選擇使用特定聲風格

## 環境變量

```bash
# Anthropic Claude API (用於 AI 歌詞生成)
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Suno API (選擇一個)
export ALLAPI_KEY="your-allapi-key"           # 使用 AllAPI
# 或
export KIE_API_KEY="your-kie-api-key"         # 使用 Kie.ai
```

## 使用方式

### 1. 基本使用 - 從主題開始

```bash
# 快樂流行歌曲
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "夏天去海灘" \
  --mood "快樂、充滿活力" \
  --style "流行"

# 悲傷抒情歌
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "失戀的夜晚" \
  --mood "悲傷、孤單" \
  --style "抒情"

# 搖滾勁歌
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "突破自我" \
  --mood "激勵、力量" \
  --style "搖滾"
```

### 2. 進階使用 - 完全控制

```bash
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "城市夜生活" \
  --mood "神秘、誘惑" \
  --style "R&B" \
  --tempo "中等" \
  --instruments "鋼琴、合成器" \
  --vocal-gender f \
  --language "中文" \
  --provider "allapi"
```

### 3. 使用 Persona

```bash
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "新的開始" \
  --mood "充滿希望" \
  --style "流行" \
  --persona-id "your-persona-id" \
  --artist-clip-id "your-clip-id" \
  --provider "allapi"
```

### 4. 只生成歌詞（不調用 Suno API）

```bash
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "春天" \
  --mood "溫暖" \
  --style "民謠" \
  --lyrics-only
```

### 5. 英文歌詞

```bash
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "love and heartbreak" \
  --mood "emotional" \
  --style "pop ballad" \
  --language "english"
```

## 參數說明

### 必要參數

| 參數 | 說明 | 範例 |
|------|------|------|
| `--theme` | 歌曲主題 | "夏天"、"愛情"、"夢想" |
| `--mood` | 情感描述 | "快樂"、"悲傷"、"激勵" |
| `--style` | 音樂風格 | "流行"、"搖滾"、"抒情" |

### 可選參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--tempo` | 速度描述 | "中等" |
| `--instruments` | 樂器描述 | 自動推薦 |
| `--vocal-gender` | 人聲性別 | m (男) |
| `--language` | 歌詞語言 | 中文 |
| `--provider` | API 提供商 | allapi |
| `--model` | Suno 模型 | chirp-v4 |
| `--lyrics-only` | 只生成歌詞 | false |
| `--persona-id` | Persona ID | - |
| `--artist-clip-id` | Artist Clip ID | - |
| `--no-wait` | 不等待完成 | false |

## 支援的音樂風格

### 中文風格
- **流行** (Pop)
- **搖滾** (Rock)
- **抒情** (Ballad)
- **民謠** (Folk)
- **嘻哈** (Hip-Hop)
- **R&B**
- **電子** (Electronic)
- **爵士** (Jazz)
- **古典** (Classical)
- **說唱** (Rap)

### 英文風格
- Pop, Rock, Ballad, Folk, Hip-Hop, R&B, Electronic, Jazz, Classical, Rap, Country, Reggae, Metal

## AI 歌詞生成邏輯

### 歌詞結構
```
[Verse 1]
主歌第一段 - 設定場景

[Chorus]
副歌 - 核心訊息（重複）

[Verse 2]
主歌第二段 - 發展故事

[Chorus]
副歌 - 核心訊息

[Bridge]
橋段 - 情感轉折

[Chorus]
副歌 - 最後一次

[Outro]
結尾 - 淡出
```

### 情感分析與風格推薦

| 歌詞情感 | 推薦風格 Tags |
|---------|--------------|
| 快樂/興奮 | pop,upbeat,happy,energetic,dance |
| 悲傷/孤單 | ballad,piano,sad,emotional,slow |
| 激勵/力量 | rock,empowering,powerful,energetic |
| 浪漫/溫馨 | romantic,ballad,warm,love |
| 神秘/暗黑 | dark,mysterious,electronic,atmospheric |
| 輕鬆/休閒 | folk,acoustic,relaxed,peaceful |

## 工作流程

```
┌─────────────────┐
│  1. 使用者輸入   │
│  (theme, mood)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. AI 生成歌詞   │
│  (Claude API)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. 情感分析     │
│  推薦風格 Tags  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. 格式轉換     │
│  (title, tags)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. 調用 Suno API│
│  (allapi/kie)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  6. 等待完成     │
│  返回歌曲連結    │
└─────────────────┘
```

## 輸出範例

### 只生成歌詞模式
```json
{
  "title": "海灘夏日",
  "tags": "pop,upbeat,happy,summer,beach,dance",
  "prompt": "[Verse 1]\n陽光灑在金色沙灘上...\n\n[Chorus]\n這個夏天最美好...",
  "lyrics": "[完整歌詞]"
}
```

### 完整生成模式
```bash
✓ AI 歌詞生成完成
✓ 風格推薦: pop,upbeat,happy,summer,beach
✓ 格式轉換完成
✓ 提交到 AllAPI Suno
✓ 任務 ID: abc123
✓ 生成完成！
🎵 歌曲: https://suno.com/song/abc123
```

## 與其他技能的配合

### 預設工作流程
```
suno-composer (生成歌詞+風格)
    ↓
suno-allapi/suno-kie (生成歌曲)
    ↓
使用 Persona 保持聲音一致性
```

### 進階工作流程
```bash
# 1. 使用 composer 生成歌曲
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "測試聲音" \
  --mood "溫和" \
  --style "流行"

# 2. 使用生成的 clip_id 創建 Persona (Kie.ai)
python3 .claude/skills/suno-kie/scripts/generate-persona.py \
  --task-id "xxx" --audio-id "yyy" \
  --name "我的聲音" --description "..."

# 3. 使用 composer + Persona 生成更多歌曲
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "新歌" \
  --mood "快樂" \
  --style "流行" \
  --persona-id "persona-id"
```

## 注意事項

1. **API Key**: 需要設定 ANTHROPIC_API_KEY（歌詞生成）和 Suno API Key
2. **歌詞語言**: 自動檢測主題語言，中文主題生成中文歌詞
3. **風格 Tags**: 根據情感分析自動推薦，也可手動指定
4. **生成時間**: 約 1-2 分鐘（包含歌詞生成 + Suno API）
5. **Tokens 使用**: 歌詞生成約使用 1000-2000 tokens

## 範例

更多範例請參考 `examples/` 目錄：
- `examples/pop-song.sh` - 流行歌曲
- `examples/ballad.sh` - 抒情歌曲
- `examples/rock.sh` - 搖滾歌曲
- `examples/with-persona.sh` - 使用 Persona
- `examples/english.sh` - 英文歌曲
