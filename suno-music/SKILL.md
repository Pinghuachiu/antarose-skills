---
name: suno-music
description: 使用 AllAPI Suno API 生成 AI 音乐，支持所有官方功能：灵感、自定义、续写、上传、歌手风格、歌曲拼接
metadata:
  category: audio
  type: generation
  languages:
    - python
---

# Suno Music Generation

使用 AllAPI Suno API 生成 AI 音乐，支持多种创作模式。

## 功能特性

- **灵感模式**：简单描述即可生成完整歌曲
- **自定义模式**：完全控制标题、风格、歌词等
- **续写模式**：从指定时间点继续创作
- **上传生成**：基于上传的音频重新创作
- **歌手风格模式**：使用特定歌手声音风格
- **歌曲拼接**：合并多首歌曲
- **歌词生成**：纯歌词创作
- **批量查询**：一次查询多个任务
- **下载音频**：下载 MP3/WAV 格式音频

## 支持的模型

- `chirp-v3-0` (v3.0)
- `chirp-v3-5` (v3.5)
- `chirp-v4` (v4.0，默认)
- `chirp-auk` (v4.5)
- `chirp-v5` (v5.0)

## 环境变量

```bash
export ALLAPI_BASE_URL="https://allapi.store/"
export ALLAPI_KEY="sk-eJtw92E4YJZrdF6bv0bjiIU4DAwo8nHC3XPZeQFRxwZ5i6mM"
```

## 使用方式

### 1. 灵感模式（最简单）

```bash
python3 .claude/skills/suno-music/scripts/generate.py "快乐的歌曲"
```

### 2. 自定义模式

```bash
python3 .claude/skills/suno-music/scripts/generate.py \
  --mode custom \
  --title "我的歌曲" \
  --tags "pop,electronic,upbeat" \
  --prompt "歌词内容或创作提示"
```

### 3. 续写模式

```bash
python3 .claude/skills/suno-music/scripts/generate.py \
  --mode extend \
  --task-id "previous-task-id" \
  --continue-at 120.5 \
  --prompt "继续创作"
```

### 4. 上传生成

```bash
python3 .claude/skills/suno-music/scripts/generate.py \
  --mode cover \
  --cover-clip-id "audio-clip-id" \
  --prompt "重新编排这首歌曲"
```

### 5. 歌词生成

```bash
python3 .claude/skills/suno-music/scripts/lyrics.py "生成关于春天的歌词"
```

### 6. 查询任务状态

```bash
python3 .claude/skills/suno-music/scripts/fetch.py "task-id"
```

### 7. 歌手风格模式

```bash
python3 .claude/skills/suno-music/scripts/generate.py \
  --mode singer-style \
  --title "Jazz Night" \
  --tags "jazz,smooth,piano" \
  --prompt "Lyrics here..." \
  --vocal-gender f
```

### 8. 歌曲拼接模式

```bash
python3 .claude/skills/suno-music/scripts/generate.py \
  --mode concat \
  --concat-clips "clip-id-1,clip-id-2,clip-id-3" \
  --title "My Medley"
```

### 9. 批量查询任务

```bash
python3 .claude/skills/suno-music/scripts/batch-fetch.py task-id-1 task-id-2 task-id-3

# 或使用逗号分隔
python3 .claude/skills/suno-music/scripts/batch-fetch.py --ids "id1,id2,id3"
```

### 10. 下载音频文件

```bash
python3 .claude/skills/suno-music/scripts/download-wav.py "task-id"

# 下载到指定目录
python3 .claude/skills/suno-music/scripts/download-wav.py "task-id" --output ./music

# 只下载 WAV 格式
python3 .claude/skills/suno-music/scripts/download-wav.py "task-id" --wav-only

# 列出可用文件（不下载）
python3 .claude/skills/suno-music/scripts/download-wav.py "task-id" --list-only
```

## 参数说明

### 通用参数

- `--mode`: 生成模式 (inspiration/custom/extend/cover/singer-style/concat)
- `--model`: 模型版本 (默认: chirp-v4)
- `--no-wait`: 立即返回不等待完成

### 自定义模式参数

- `--title`: 歌曲标题
- `--tags`: 音乐风格 (逗号分隔)
- `--prompt`: 创作提示词或歌词
- `--negative-tags`: 不希望出现的风格
- `--vocal-gender`: 歌手性别 (m/f)

### 续写模式参数

- `--task-id`: 要续写的任务 ID
- `--continue-at`: 续写起始时间（秒）
- `--continue-clip-id`: 要续写的歌曲 ID

### 上传生成参数

- `--cover-clip-id`: 原曲或上传音频的 clip ID
- `--infill-start`: 填充开始时间（秒）
- `--infill-end`: 填充结束时间（秒）

### 歌手风格模式参数

- `--title`: 歌曲标题
- `--tags`: 音乐风格 (逗号分隔)
- `--prompt`: 歌词或创作提示
- `--vocal-gender`: 歌手性别 (m/f)

### 歌曲拼接参数

- `--concat-clips`: 要拼接的 clip ID 列表 (逗号分隔，至少2个)
- `--title`: 拼接后的歌曲标题（可选）

### 批量查询参数

- `task_ids`: 空格分隔的任务 ID 列表
- `--ids`: 逗号分隔的任务 ID 字符串
- `--summary`: 只显示摘要
- `--json`: 输出原始 JSON

### 下载音频参数

- `task_id`: 任务 ID
- `--output`: 输出目录 (默认: ./suno-downloads)
- `--list-only`: 列出文件不下载
- `--wav-only`: 只下载 WAV 格式
- `--clip-id`: 只下载指定 clip

## 返回数据

成功生成后返回 JSON 数据：

```json
{
  "task_id": "uuid",
  "status": "SUCCESS",
  "data": [
    {
      "id": "clip-id",
      "title": "歌曲标题",
      "audio_url": "音频链接",
      "image_url": "封面图链接",
      "video_url": "视频链接",
      "lyrics": "歌词内容"
    }
  ]
}
```

## 任务状态

- `NOT_START`: 未启动
- `SUBMITTED`: 已提交
- `QUEUED`: 排队中
- `IN_PROGRESS`: 生成中
- `SUCCESS`: 成功
- `FAILURE`: 失败

## 注意事项

1. 生成时间通常需要 30-60 秒
2. 默认会自动轮询直到任务完成
3. 使用 `--no-wait` 可以立即返回任务 ID
4. API Key 存储在 `resource.md` 中
5. 歌曲会生成两个版本（通常）

## 示例

更多示例请参考 `examples/` 目录：
- `examples/inspiration.sh` - 灵感模式
- `examples/custom.sh` - 自定义模式
- `examples/extend.sh` - 续写模式
- `examples/singer-style.sh` - 歌手风格模式
- `examples/concat.sh` - 歌曲拼接模式
- `examples/lyrics.sh` - 歌词生成
- `examples/fetch.sh` - 查询单个任务
- `examples/batch-fetch.sh` - 批量查询任务
- `examples/download-wav.sh` - 下载音频文件
