---
name: suno-allapi
description: 使用 AllAPI Suno API 生成 AI 音樂，支援所有官方功能：靈感、自定義、續寫、上傳、歌手風格、Persona 聲音角色、歌曲拼接
metadata:
  category: audio
  type: generation
  languages:
    - python
---

# Suno AllAPI - AI Music Generation

使用 AllAPI Suno API 生成 AI 音樂，支援多種創作模式和 **Persona 聲音角色**功能。

## 功能特性

- **靈感模式**：簡單描述即可生成完整歌曲
- **自定義模式**：完全控制標題、風格、歌詞等
- **續寫模式**：從指定時間點繼續創作
- **上傳音頻**：上傳自己的聲音用於聲音克隆
- **Cover 模式**：基於上傳的音頻重新創作
- **歌手風格模式**：使用特定歌手聲音風格
- **Persona 聲音角色** 🎭：創建並使用專屬聲音風格
- **歌曲拼接**：合併多首歌曲
- **歌詞生成**：純歌詞創作
- **批量查詢**：一次查詢多個任務
- **下載音頻**：下載 MP3/WAV 格式音頻

## 支援的模型

- `chirp-v3-0` (v3.0)
- `chirp-v3-5` (v3.5) - 用於 Persona
- `chirp-v3-5-tau` - **Persona 專用**
- `chirp-v4` (v4.0)
- `chirp-v4-tau` - **Persona 專用**
- `chirp-auk` (v4.5)
- `chirp-v5` (v5.0)

## 環境變量

```bash
export ALLAPI_BASE_URL="https://allapi.store/"
export ALLAPI_KEY="your-allapi-key"
```

## Suno 歌詞格式指南 📝

### 結構標籤（Structure Tags）

**必須標籤：**
- `[Verse]` - 主歌
- `[Chorus]` - 副歌（記憶點）

**建議標籤：**
- `[Intro]` - 開頭
- `[Pre-Chorus]` - 預副歌（過渡）
- `[Bridge]` - 橋段（轉折）
- `[Outro]` - 結尾
- `[Interlude]` - 間奏段落
- `[Guitar Solo]` / `[Instrumental]` - 純音樂段落

### Meta Tags（語音/情緒控制）

**聲音類：**
- `[Male vocals]` - 男聲
- `[Female vocals]` - 女聲
- `[Duet]` - 對唱
- `[Choir]` - 合唱

**情緒/風格類：**
- `[High Energy]` - 高能量
- `[Dreamy]` - 夢幻
- `[Nostalgic]` - 懷舊
- `[Emotional]` - 情感化
- `[Peaceful]` - 平靜
- `[Epic]` - 史詩

**特殊效果：**
- `[Instrumental break]` - 節奏性純音樂
- `[Tempo increase]` - 節奏加快
- `[Tempo decrease]` - 節奏減慢

### 完整範例模板

```
歌曲標題：銀色私語
建議風格 (Style): Soulful Pop, R&B, Dreamy, Atmospheric

[Verse 1]
當白晝的喧囂終於肯
閉上眼 城市的霓虹
也不再那麼刺眼

[Chorus]
Oh Moon, 妳是夜裡最溫柔的謳言
撒下銀色的網 捕捉我所有思念

[Verse 2]
古老的傳說 說妳藏著謎的容顏
我倒覺得 妳只是面巨大的鏡面

[Bridge]
月光穿透了窗櫃 落在掌心
像是一封沒署名的秘密信

[Chorus]
Oh Moon, 妳是夜裡最溫柔的謳言
撒下銀色的網 捕捉我所有思念

[Outro]
靜靜地守著... Silver whispers in the dark...
```

### 使用技巧

1. **Chorus 應該**：簡短、易記、可重複、情緒高點
2. **Verse 應該**：講述故事、鋪陳情節
3. **Bridge 應該**：轉折、對比、情感昇華
4. **保持簡潔**：每行不要太長，保持節奏感
5. **空格運用**：適當使用空格引導停頓感（Phrasing）

### 範例文件

詳細範例和最佳實踐請參考：
```bash
# 查看完整歌詞範例
cat .claude/skills/suno-allapi/examples/suno-lyrics-template.md

# 使用格式化工具
python3 .claude/skills/suno-allapi/scripts/lyrics-formatter.py --show-tags
```

## 使用方式

### 1. 靈感模式（最簡單）

```bash
python3 .claude/skills/suno-allapi/scripts/generate.py "快樂的歌曲"
```

### 2. 自定義模式

```bash
python3 .claude/skills/suno-allapi/scripts/generate.py \
  --mode custom \
  --title "我的歌曲" \
  --tags "pop,electronic,upbeat" \
  --prompt "歌詞內容或創作提示"
```

### 3. 續寫模式

```bash
python3 .claude/skills/suno-allapi/scripts/generate.py \
  --mode extend \
  --task-id "previous-task-id" \
  --continue-at 120.5 \
  --prompt "繼續創作"
```

### 4. 上傳音頻（用自己的聲音）

首先上傳你的音頻文件：

```bash
python3 .claude/skills/suno-allapi/scripts/upload.py my-voice.mp3

# 帶描述上傳
python3 .claude/skills/suno-allapi/scripts/upload.py my-voice.mp3 --description "我的演唱聲音"
```

上傳後會獲得 `clip_id`，然後用它來生成歌曲：

```bash
python3 .claude/skills/suno-allapi/scripts/generate.py \
  --mode cover \
  --cover-clip-id "your-clip-id" \
  --prompt "用我的聲音重新演唱這首歌"
```

### 5. 🎭 Persona 聲音角色（AllAPI 獨有）

**工作流程：**

```bash
# 步驟 1: 生成一首歌曲，獲取 clip_id
python3 .claude/skills/suno-allapi/scripts/generate.py \
  --mode custom \
  --title "我的聲音樣本" \
  --tags "pop,ballad" \
  --prompt "溫柔的抒情歌，鋼琴伴奏"

# 記下返回的 clip_id（類似：54834687-5e79-4f08-8e14-cf188f15b598）

# 步驟 2: 使用 clip_id 創建 Persona（系統會自動生成 persona_id）
# AllAPI 會自動為 clip_id 創建對應的 persona_id
# 這個 persona_id 可以在後續生成中使用

# 步驟 3: 使用 Persona 生成新歌曲
python3 .claude/skills/suno-allapi/scripts/generate.py \
  --mode singer-style \
  --title "新歌" \
  --tags "pop,happy" \
  --prompt "春天來了，花朵綻放" \
  --model chirp-v4-tau \
  --persona-id "auto-generated-persona-id" \
  --artist-clip-id "clip-id-from-step-1"
```

**重要說明：**
- AllAPI 的 Persona 是通過 `task=artist_consistency` 使用的
- 需要使用 `chirp-v3-5-tau` 或 `chirp-v4-tau` 模型
- `persona_id` 由系統自動生成（從 clip_id）
- `artist_clip_id` 是原始歌曲的 clip_id
- Persona 可跨帳號使用

### 6. 歌詞生成

```bash
python3 .claude/skills/suno-allapi/scripts/lyrics.py "生成關於春天的歌詞"
```

### 7. 查詢任務狀態

```bash
python3 .claude/skills/suno-allapi/scripts/fetch.py "task-id"
```

### 8. 歌手風格模式（基本）

```bash
python3 .claude/skills/suno-allapi/scripts/generate.py \
  --mode singer-style \
  --title "Jazz Night" \
  --tags "jazz,smooth,piano" \
  --prompt "Lyrics here..." \
  --vocal-gender f
```

### 9. 歌曲拼接模式

```bash
python3 .claude/skills/suno-allapi/scripts/generate.py \
  --mode concat \
  --concat-clips "clip-id-1,clip-id-2,clip-id-3" \
  --title "My Medley"
```

### 10. 批量查詢任務

```bash
python3 .claude/skills/suno-allapi/scripts/batch-fetch.py task-id-1 task-id-2 task-id-3

# 或使用逗號分隔
python3 .claude/skills/suno-allapi/scripts/batch-fetch.py --ids "id1,id2,id3"
```

### 11. 下載音頻文件

```bash
python3 .claude/skills/suno-allapi/scripts/download-wav.py "task-id"

# 下載到指定目錄
python3 .claude/skills/suno-allapi/scripts/download-wav.py "task-id" --output ./music

# 只下載 WAV 格式
python3 .claude/skills/suno-allapi/scripts/download-wav.py "task-id" --wav-only

# 列出可用文件（不下載）
python3 .claude/skills/suno-allapi/scripts/download-wav.py "task-id" --list-only
```

## 參數說明

### 通用參數

- `--mode`: 生成模式 (inspiration/custom/extend/cover/singer-style/concat)
- `--model`: 模型版本 (默認: chirp-v4)
  - Persona 需使用: `chirp-v3-5-tau` 或 `chirp-v4-tau`
- `--no-wait`: 立即返回不等待完成

### 自定義模式參數

- `--title`: 歌曲標題
- `--tags`: 音樂風格 (逗號分隔)
- `--prompt`: 創作提示詞或歌詞
- `--negative-tags`: 不希望出現的風格
- `--vocal-gender`: 歌手性別 (m/f)

### 續寫模式參數

- `--task-id`: 要續寫的任務 ID
- `--continue-at`: 續寫起始時間（秒）
- `--continue-clip-id`: 要續寫的歌曲 ID

### 上傳生成參數

- `--cover-clip-id`: 原曲或上傳音頻的 clip ID
- `--infill-start`: 填充開始時間（秒）
- `--infill-end`: 填充結束時間（秒）

### 歌手風格模式參數（含 Persona）

- `--title`: 歌曲標題
- `--tags`: 音樂風格 (逗號分隔)
- `--prompt`: 歌詞或創作提示
- `--vocal-gender`: 歌手性別 (m/f)
- `--persona-id`: **Persona ID**（用於 artist_consistency）
- `--artist-clip-id`: **原始歌曲 clip ID**（用於 artist_consistency）

### 歌曲拼接參數

- `--concat-clips`: 要拼接的 clip ID 列表 (逗號分隔，至少2個)
- `--title`: 拼接後的歌曲標題（可選）

### 批量查詢參數

- `task_ids`: 空格分隔的任務 ID 列表
- `--ids`: 逗號分隔的任務 ID 字符串
- `--summary`: 只顯示摘要
- `--json`: 輸出原始 JSON

### 下載音頻參數

- `task_id`: 任務 ID
- `--output`: 輸出目錄 (默認: ./suno-downloads)
- `--list-only`: 列出文件不下載
- `--wav-only`: 只下載 WAV 格式
- `--clip-id`: 只下載指定 clip

## 返回數據

成功生成後返回 JSON 數據：

```json
{
  "task_id": "uuid",
  "status": "SUCCESS",
  "data": [
    {
      "id": "clip-id",
      "title": "歌曲標題",
      "audio_url": "音頻鏈接",
      "image_url": "封面圖鏈接",
      "video_url": "視頻鏈接",
      "lyrics": "歌詞內容"
    }
  ]
}
```

## 任務狀態

- `NOT_START`: 未啟動
- `SUBMITTED`: 已提交
- `QUEUED`: 排隊中
- `IN_PROGRESS`: 生成中
- `SUCCESS`: 成功
- `FAILURE`: 失敗

## AllAPI vs Kie.ai 對比

| 特性 | AllAPI | Kie.ai |
|------|--------|--------|
| **Persona 創建** | 自動從 clip_id 生成 | 獨立端點 `/generate-persona` |
| **Persona 使用** | `task=artist_consistency` | `personaId` 參數 |
| **所需模型** | `chirp-v3-5-tau` 或 `chirp-v4-tau` | V3.5 以上（不含 V3.5） |
| **跨帳號** | ✅ 可跨帳號 | ❌ 不可跨帳號 |
| **上傳方式** | 直接文件上傳 | URL 上傳（需雲端存儲） |

## 注意事項

1. 生成時間通常需要 30-60 秒
2. 默認會自動輪詢直到任務完成
3. 使用 `--no-wait` 可以立即返回任務 ID
4. **Persona 使用時必須使用 `chirp-v3-5-tau` 或 `chirp-v4-tau` 模型**
5. Persona 可以跨帳號使用（與 Kie.ai 不同）
6. 歌曲會生成兩個版本（通常）

## 示例

更多示例請參考 `examples/` 目錄：
- `examples/inspiration.sh` - 靈感模式
- `examples/custom.sh` - 自定義模式
- `examples/extend.sh` - 續寫模式
- `examples/singer-style.sh` - 歌手風格模式
- `examples/persona.sh` - Persona 聲音角色模式
- `examples/concat.sh` - 歌曲拼接模式
- `examples/lyrics.sh` - 歌詞生成
- `examples/fetch.sh` - 查詢單個任務
- `examples/batch-fetch.sh` - 批量查詢任務
- `examples/download-wav.sh` - 下載音頻文件
