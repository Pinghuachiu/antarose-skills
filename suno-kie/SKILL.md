---
name: suno-kie
description: 使用 Kie.ai Suno API 生成 AI 音樂，支援聲音角色（Persona）創建、上傳重新編曲、完整客製化功能
metadata:
  category: audio
  type: generation
  languages:
    - python
---

# Suno KIE - AI Music with Voice Persona

使用 Kie.ai Suno API 生成 AI 音樂，支援聲音角色（Persona）功能，可創建專屬聲音風格。

## 功能特性

- **Generate Persona** 🎭 - 從生成的音樂創建專屬聲音角色
- **Upload And Cover** 📤 - 上傳音訊並重新編曲（保留旋律）
- **Add Vocals** 🎤 - 為純音樂自動生成 AI 人聲和歌詞
- **完整音樂生成** 🎵 - 支援所有參數的客製化模式
- **聲音角色應用** ✨ - 在生成中使用 personaId 應用特定聲音風格
- **Callback 支援** 🔔 - 支援 webhook 回調
- **多模型支援** 🤖 - V5, V4.5+, V4.5, V4, V3.5

## Kie.ai vs AllAPI 差異

| 特性 | Kie.ai | AllAPI |
|------|--------|--------|
| 聲音角色（Persona） | ✅ 獨立端點 `/generate-persona` | ✅ `task=artist_consistency` |
| 上傳方式 | URL（需先上傳雲端） | 直接文件上傳 |
| Upload And Cover | ✅ 完整支援 | ✅ 完整支援 |
| Add Vocals | ✅ 專門端點 | ❌ 無專門端點 |
| 模型選擇 | V5, V4.5+, V4.5, V4, V3.5 | chirp-v5, v4.5, v4, v3.5 |
| Persona 跨帳號 | ❌ 不可跨帳號 | ✅ 可跨帳號 |

## 環境變數

```bash
export KIE_API_KEY="your-kie-api-key"
# 可選：設定 callback URL
export KIE_CALLBACK_URL="https://your-domain.com/callback"
```

## 使用方式

### Suno 歌詞格式指南 📝

#### 結構標籤（Structure Tags）

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

#### Meta Tags（語音/情緒控制）

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

#### 完整範例模板

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

#### 使用技巧

1. **Chorus 應該**：簡短、易記、可重複、情緒高點
2. **Verse 應該**：講述故事、鋪陳情節
3. **Bridge 應該**：轉折、對比、情感昇華
4. **保持簡潔**：每行不要太長，保持節奏感
5. **空格運用**：適當使用空格引導停頓感（Phrasing）

#### 範例文件

詳細範例和最佳實踐請參考：
```bash
# 查看完整歌詞範例
cat .claude/skills/suno-kie/examples/suno-lyrics-template.md

# 使用格式化工具
python3 .claude/skills/suno-kie/scripts/lyrics-formatter.py --show-tags
```

### 0. 使用 Ngrok 自動 Callback 🔥（推薦）

由於 Kie.ai 只支援 callback 模式（無法主動查詢任務狀態），推薦使用 Ngrok 快速建立臨時公網地址：

**優點：**
- ✅ 自動建立臨時公網 URL
- ✅ 自動接收任務完成通知
- ✅ 用完即關，無需長期 server
- ✅ 一次指令完成所有設定

**前置需求：**
```bash
# 安裝 ngrok (選擇其中一種方法)

# 方法 1: 使用 apt
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# 方法 2: 使用 snap
sudo snap install ngrok

# 設定 authtoken (從 https://dashboard.ngrok.com/get-started/your-authtoken 獲取)
ngrok config add-authtoken YOUR_TOKEN
```

**使用方式：**
```bash
# 自動建立 ngrok + callback + 生成音樂
python3 .claude/skills/suno-kie/scripts/generate-with-callback.py \
  --prompt "溫柔的舒眠音樂" \
  --style "Ambient,Relaxing" \
  --title "Sea Breeze" \
  --instrumental

# 使用 Persona
python3 .claude/skills/suno-kie/scripts/generate-with-callback.py \
  --prompt "新的歌詞" \
  --style "pop" \
  --title "我的歌" \
  --persona-id "persona_123"
```

**工作流程：**
1. 自動啟動 callback server (localhost:8080)
2. 自動啟動 ngrok tunnel
3. 自動獲取公網 URL (如: `https://abc123.ngrok-free.app/callback`)
4. 提交音樂生成任務
5. 等待 callback 接收完成通知
6. 按 Ctrl+C 清理所有背景程序

### 1. 生成音樂（支援 Persona）

```bash
# 基本生成
python3 .claude/skills/suno-kie/scripts/generate.py \
  --prompt "一首輕快的流行歌曲" \
  --style "pop,upbeat"

# 使用 Persona（聲音角色）
python3 .claude/skills/suno-kie/scripts/generate.py \
  --prompt "新的歌詞內容" \
  --style "pop" \
  --title "我的歌曲" \
  --persona-id "persona_123"

# 非客製模式（最簡單）
python3 .claude/skills/suno-kie/scripts/generate.py \
  --prompt "一首搖滾歌曲" \
  --custom-mode false
```

### 2. 創建聲音角色（Persona）🎭

**工作流程：**

```bash
# 步驟 1: 先生成一首音樂
python3 .claude/skills/suno-kie/scripts/generate.py \
  --prompt "悠揚的鋼琴演奏" \
  --style "Classical" \
  --title "Piano Test" \
  --instrumental

# 記下 taskId 和 audioId

# 步驟 2: 創建 Persona
python3 .claude/skills/suno-kie/scripts/generate-persona.py \
  --task-id "your-task-id" \
  --audio-id "your-audio-id" \
  --name "我的聲音角色" \
  --description "優雅的古典鋼琴風格，適合抒情歌曲"

# 步驟 3: 使用 Persona 生成新音樂
python3 .claude/skills/suno-kie/scripts/generate.py \
  --prompt "新的歌詞" \
  --style "pop" \
  --title "新歌" \
  --persona-id "your-persona-id"
```

**重要限制：**
- Persona 只支援 v3.5 以上的模型（v3.5 本身不支援）
- 每個 audioId 只能創建一個 Persona
- 音樂生成任務必須完全完成才能創建 Persona

### 3. 上傳並重新編曲（Upload And Cover）

首先需要將音訊上傳到雲端存儲（如 AWS S3、Google Cloud Storage），獲得 URL：

```bash
# 使用上傳的音訊重新編曲
python3 .claude/skills/suno-kie/scripts/upload-cover.py \
  --upload-url "https://storage.example.com/my-audio.mp3" \
  --prompt "將這首歌改為爵士風格" \
  --style "Jazz" \
  --title "Jazz Version" \
  --custom-mode true

# 非客製模式（最簡單）
python3 .claude/skills/suno-kie/scripts/upload-cover.py \
  --upload-url "https://storage.example.com/my-audio.mp3" \
  --prompt "改編成搖滾版本" \
  --custom-mode false
```

### 4. 加入人聲（Add Vocals）🎤

為現有的純音樂自動生成 AI 人聲和歌詞：

```bash
# 簡單模式 - 只描述你想要的歌詞主題
python3 .claude/skills/suno-kie/scripts/add-vocals.py \
  --upload-url "https://storage.example.com/piano-instrumental.mp3" \
  --prompt "創作關於夏天的快樂歌詞" \
  --custom-mode false

# 客製模式 - 完全控制
python3 .claude/skills/suno-kie/scripts/add-vocals.py \
  --upload-url "https://storage.example.com/beat.mp3" \
  --prompt "城市夜生活的嘻哈歌曲" \
  --style "Hip-Hop" \
  --title "Midnight City" \
  --vocal-gender m \
  --custom-mode true

# 指定人聲性別
python3 .claude/skills/suno-kie/scripts/add-vocals.py \
  --upload-url "https://storage.example.com/ballad.mp3" \
  --prompt "愛情抒情歌" \
  --style "Pop Ballad" \
  --title "My Heart" \
  --vocal-gender f \
  --custom-mode true
```

**使用場景：**
- 你有一首純音樂想加入人聲
- 快速測試不同歌詞主題在現有旋律上的效果
- 與編曲家合作（對方提供 Beat，你負責加歌詞）

**與其他功能的差別：**
| 功能 | 輸入 | 輸出 | 用途 |
|------|------|------|------|
| 普通生成 | 文字提示 | 完整歌曲 | 從零創作 |
| Persona | 歌詞 + 聲音模型 | 特定聲音的完整歌曲 | 聲音克隆 |
| **Add Vocals** | **純音樂** | **既有音樂 + AI 人聲** | **為現成音樂加歌詞** |
| Upload Cover | 你的聲音檔案 | 用你的聲音重新演唱 | 聲音克隆 |

**重要限制：**
- 人聲風格是 AI 自動生成的（不能用 Persona 指定特定聲音）
- 需要先有純音樂檔案
- 音訊不超過 2 分鐘
- URL 必須是公開可訪問的

### 5. 查詢任務狀態

```bash
# 查詢單個任務
python3 .claude/skills/suno-kie/scripts/fetch.py "task-id"

# 查詢並等待完成
python3 .claude/skills/suno-kie/scripts/fetch.py "task-id" --wait
```

## 參數說明

### Generate Music 參數

#### 通用參數
- `--prompt`: 歌詞或描述（必填）
- `--custom-mode`: 是否啟用客製模式（預設: true）
- `--model`: 模型版本（預設: V4_5）
  - `V5` - 最佳音樂表現，更快生成
  - `V4_5PLUS` - 更豐富聲音，最多 8 分鐘
  - `V4_5` - 更聰明提示，更快生成，最多 8 分鐘
  - `V4` - 改進人聲品質，最多 4 分鐘
  - `V3_5` - 更好歌曲結構，最多 4 分鐘

#### Custom Mode 參數（custom-mode=true）
- `--style`: 音樂風格（必填）
- `--title`: 歌曲標題（必填）
- `--instrumental`: 純音樂（預設: false）
- `--negative-tags`: 不想要的風格
- `--vocal-gender`: 人聲性別（m/f）
- `--style-weight`: 風格強度（0-1）
- `--weirdness`: 創意程度（0-1）
- `--audio-weight`: 音訊權重（0-1）
- `--persona-id`: **聲音角色 ID（Kie.ai 獨有）**

#### 字元限制
- **V5, V4.5+**: style 最多 1000 字元, title 100 字元, prompt 5000 字元
- **V3.5, V4**: style 最多 200 字元, title 80 字元, prompt 3000 字元
- **非客製模式**: prompt 最多 500 字元

### Generate Persona 參數
- `--task-id`: 音樂生成任務 ID（必填）
- `--audio-id`: 音訊 ID（必填）
- `--name`: Persona 名稱（必填）
- `--description`: 詳細描述（必填）

### Upload And Cover 參數
- `--upload-url`: 音訊文件 URL（必填，不超過 2 分鐘）
- `--prompt`: 描述或歌詞（必填）
- `--custom-mode`: 客製模式（預設: true）
- `--style`: 音樂風格（客製模式必填）
- `--title`: 歌曲標題（客製模式必填）
- `--instrumental`: 純音樂（預設: false）
- `--model`: 模型版本
- `--persona-id`: Persona ID（可選）

### Add Vocals 參數
- `--upload-url`: 純音樂文件 URL（必填，不超過 2 分鐘）
- `--prompt`: 歌詞主題或描述（必填）
- `--custom-mode`: 客製模式（預設: true）
- `--style`: 音樂風格（客製模式必填）
- `--title`: 歌曲標題（客製模式必填）
- `--vocal-gender`: 人聲性別 m/f（可選）
- `--model`: 模型版本
- `--negative-tags`: 不想要的風格（可選）
- `--style-weight`: 風格強度 0-1（可選）
- `--weirdness`: 創意程度 0-1（可選）

## 工作流程範例

### 完整工作流程：創建並使用 Persona

```bash
# 1. 生成初始音樂
python3 .claude/skills/suno-kie/scripts/generate.py \
  --prompt "溫柔的抒情歌，鋼琴伴奏" \
  --style "pop,ballad,piano" \
  --title "My Voice Sample" \
  --model V4_5

# 輸出會包含 taskId 和 audioId，記下來

# 2. 創建 Persona
python3 .claude/skills/suno-kie/scripts/generate-persona.py \
  --task-id "從步驟1獲得的taskId" \
  --audio-id "從步驟1獲得的audioId" \
  --name "我的聲音" \
  --description "溫柔的男聲，適合抒情歌曲，鋼琴伴奏風格"

# 輸出會包含 personaId

# 3. 使用 Persona 生成新歌曲
python3 .claude/skills/suno-kie/scripts/generate.py \
  --prompt "春天來了，花朵綻放，鳥兒歌唱" \
  --style "pop,upbeat,happy" \
  --title "春之歌" \
  --persona-id "從步驟2獲得的personaId" \
  --model V4_5

# 現在這首歌會使用你的聲音角色風格！
```

## 與 suno-allapi 技能的選擇

**使用 suno-kie 如果你需要：**
- ✅ 獨立的 `/generate-persona` 端點（更清晰的 Persona 創建流程）
- ✅ **Add Vocals** 功能（為純音樂加入 AI 人聲）
- ✅ 更新的模型支援（V5, V4.5+）
- ✅ 在同一帳號內保持聲音一致性
- ⚠️ **注意**: 只有 callback 模式，無主動查詢端點（推薦使用 `generate-with-callback.py` + ngrok）

**使用 suno-allapi 如果你需要：**
- ✅ 直接上傳音訊文件（不需 URL）
- ✅ Persona 可跨帳號使用
- ✅ **可主動查詢任務狀態**（有 fetch 端點）
- ✅ 更簡單的生成流程
- ✅ 歌曲拼接（Concat）功能

**兩者都支援 Persona，只是實現方式不同：**
- **Kie.ai**: 使用獨立的 `/generate-persona` 端點
- **AllAPI**: 使用 `task=artist_consistency` + `persona_id` 參數

## 注意事項

1. **API Key**: 需要从 [Kie.ai](https://kie.ai) 获取
2. **URL 上傳**: upload-cover 需要音訊已上傳到雲端存儲
3. **Persona 限制**: 只支援 v3.5 以上模型生成的音樂
4. **Callback**: 如使用 callback，需確保伺服器可接收 POST 請求
5. **文件保存**: 生成的文件會在 15 天後刪除
6. **手動查看任務**: 由於 Kie.ai 無查詢端點，可手動登入查看
   - 訪問 https://kie.ai/login 登入
   - 前往 https://kie.ai/logs 查看所有任務歷史和結果
7. **無法查詢進度**: Kie.ai 不提供主動查詢端點，只能使用 callback 或手動查看網站

## 相關文檔

- [Kie.ai Suno API Documentation](https://docs.kie.ai/suno-api)
- [Upload And Cover Audio](https://docs.kie.ai/suno-api/upload-and-cover-audio)
- [Generate Persona](https://docs.kie.ai/suno-api/generate-persona)
- [Add Vocals](https://kie.ai/suno-api?model=ai-music-api%2Fadd-vocals)
