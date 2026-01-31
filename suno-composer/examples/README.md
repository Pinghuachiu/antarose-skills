# Suno Composer Examples

這個目錄包含了 `suno-composer` 技能的使用範例。

## 前置設置

在使用範例之前，請先設定環境變量：

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"  # 用於 AI 歌詞生成
export ALLAPI_KEY="your-allapi-key"                # 或使用 KIE_API_KEY
```

## 範例列表

### 1. `pop-song.sh` - 快樂流行歌曲
生成一首關於夏天海灘的快樂流行歌曲。
```bash
bash .claude/skills/suno-composer/examples/pop-song.sh
```

### 2. `ballad.sh` - 情感抒情歌
生成一首關於失戀的悲傷抒情歌。
```bash
bash .claude/skills/suno-composer/examples/ballad.sh
```

### 3. `rock.sh` - 励志搖滾
生成一首關於追夢的勵志搖滾歌曲。
```bash
bash .claude/skills/suno-composer/examples/rock.sh
```

### 4. `english.sh` - 英文歌曲
生成一首英文流行愛情歌曲。
```bash
bash .claude/skills/suno-composer/examples/english.sh
```

### 5. `with-persona.sh` - 使用聲音角色
使用特定的聲風格生成歌曲（需要先有 persona_id）。
```bash
bash .claude/skills/suno-composer/examples/with-persona.sh
```

## 自定義使用

直接使用腳本並自定義參數：

```bash
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "你的主題" \
  --mood "你的情感" \
  --style "風格" \
  --vocal-gender m \
  --provider allapi
```

## 進階選項

### 只生成歌詞（不調用 Suno API）
```bash
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "春天" \
  --mood "溫暖" \
  --style "民謠" \
  --lyrics-only
```

### 使用不同的 AI 模型
```bash
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "夢想" \
  --mood "激勵" \
  --style "流行" \
  --model chirp-v4-tau \
  --provider allapi
```

### 完整控制
```bash
python3 .claude/skills/suno-composer/scripts/compose.py \
  --theme "城市夜生活" \
  --mood "神秘、誘惑" \
  --style "R&B" \
  --tempo "中等" \
  --instruments "鋼琴、合成器、貝斯" \
  --vocal-gender f \
  --language chinese \
  --provider kie
```

## 支援的音樂風格

- **流行** (Pop)
- **搖滾** (Rock)
- **抒情** (Ballad)
- **民謠** (Folk)
- **嘻哈** (Hip-Hop)
- **R&B**
- **電子** (Electronic)
- **爵士** (Jazz)
- **古典** (Classical)

## 提示

1. **主題描述越具體越好**：例如 "夏天去海灘遇到喜歡的人" 比 "夏天" 更好
2. **情感描述可以是多個**：例如 "悲傷、懷念、帶點遺憾"
3. **語言會自動檢測**：中文主題會生成中文歌詞，英文主題會生成英文歌詞
4. **使用 Persona 可以保持聲音一致性**：參考 `with-persona.sh`

## 故障排除

### 缺少 API Key
```
Error: ANTHROPIC_API_KEY environment variable not set
```
解決方法：設定環境變量 `export ANTHROPIC_API_KEY="your-key"`

### Anthropic 套件未安裝
```
Error: anthropic package not installed
```
解決方法：`pip install anthropic`

### 歌詞生成失敗
檢查：
1. ANTHROPIC_API_KEY 是否正確
2. API 額度是否足夠
3. 網路連接是否正常

### Suno API 調用失敗
檢查：
1. ALLAPI_KEY 或 KIE_API_KEY 是否正確
2. API 提供商服務是否正常
