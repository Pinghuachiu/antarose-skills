---
name: agent-skills-guide
description: 教導如何創建和使用 Agent Skills，適用於所有支援技能的 AI Agent（包括 Claude Code、OpenCode 等），包含目錄結構、frontmatter 規範、命名規則和完整範例
metadata:
  category: guide
  audience: developers
  compatibility:
    - claude-code
    - opencode
    - any-agent
---

# Agent Skills 指南

Agent Skills 讓你可以定義可重用的行為，透過 SKILL.md 文件讓 AI Agent 發現和使用指令。

**適用平台**：
- ✅ Claude Code (Anthropic)
- ✅ OpenCode
- ✅ 其他支援技能系統的 AI Agent

## 目錄結構

不同的 AI Agent 在不同的位置搜尋 Skills：

### Claude Code (Anthropic)

**項目層級**：
- `.claude/skills/<name>/SKILL.md` - 項目特定技能

**全局層級**：
- `~/.claude/skills/<name>/SKILL.md` - 全局 Claude Code 技能

**自動發現**：
Claude Code 會從當前工作目錄向上搜尋 `.claude/skills/` 目錄。

### OpenCode

**項目層級**：
- `.opencode/skills/<name>/SKILL.md` - 項目特定技能
- `.claude/skills/<name>/SKILL.md` - Claude 相容的項目技能

**全局層級**：
- `~/.config/opencode/skills/<name>/SKILL.md` - 全局 OpenCode 技能
- `~/.claude/skills/<name>/SKILL.md` - Claude 相容的全局技能

**自動發現**：
對於項目本地路徑，OpenCode 會從當前工作目錄向上遍歷到 git worktree，沿途載入所有匹配的 `skills/*/SKILL.md`。

### 通用建議

為了讓技能在多個平台上都能使用，**建議同時創建兩個符號連結或複製**：

```bash
# 創建技能時，同時支持兩個平台
.claude/skills/my-skill/  # Claude Code 使用
.opencode/skills/my-skill/  # OpenCode 使用
```

或者使用符號連結：
```bash
ln -s .claude/skills/my-skill .opencode/skills/my-skill
```

## 創建 Skill 文件

### 基本結構

每個 Skill 必須包含 YAML frontmatter：

```yaml
---
name: skill-name
description: 技能描述（1-1024 字符）
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: utility
---

## 技能內容...
```

### 必填字段

| 字段 | 說明 |
|------|------|
| `name` | 技能名稱（1-64 字符）|
| `description` | 技能描述（1-1024 字符）|

### 可選字段

| 字段 | 說明 |
|------|------|
| `license` | 授權協議（如 MIT、Apache-2.0）|
| `compatibility` | 相容性標識（如 claude-code, opencode, any-agent）|
| `metadata` | 額外的元數據映射 |
| `metadata.category` | 技能分類（如 utility, development, content-creation）|
| `metadata.languages` | 支援的程式語言（如 python, javascript）|
| `metadata.type` | 技能類型（如 automation, guide, tool）|

## 命名規則

`name` 必須符合以下規則：
- 長度：1-64 字符
- 只能包含小寫字母、數字和單個連字符 `-`
- 不能以 `-` 開頭或結尾
- 不能包含連續的 `--`
- 必須與包含 `SKILL.md` 的目錄名稱匹配

**正則表達式**：
```regex
^[a-z0-9]+(-[a-z0-9]+)*$
```

**有效名稱範例**：
- ✅ `git-release`
- ✅ `image-generator`
- ✅ `pdf-parser`
- ✅ `code-reviewer`

**無效名稱範例**：
- ❌ `Git-Release`（大寫字母）
- ❌ `-git-release`（以連字符開頭）
- ❌ `git--release`（連續連字符）
- ❌ `git-release-`（以連字符結尾）
- ❌ `git_release`（使用下劃線）

## 完整範例

### 範例 1：Claude Code 專用 - MySQL 資料庫技能

創建 `.claude/skills/mysql/SKILL.md`：

```yaml
---
name: mysql
description: MySQL 資料庫操作技能，支援 Python、Node.js 和 Bash 腳本進行 CRUD 操作
metadata:
  category: database
  type: automation
  languages:
    - python
    - javascript
    - bash
---

# MySQL Database Skill

使用 Python 和 Node.js 腳本進行 MySQL 資料庫操作，支援各種 CRUD 操作。

## 快速開始

```bash
# 查詢資料
python3 scripts/query.py "SELECT * FROM users"

# 插入資料
python3 scripts/insert.py users '{"name":"John","email":"john@example.com"}'
```

## 連線資訊

從環境變數讀取：
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`
```

### 範例 2：通用 Agent - 圖片生成技能

創建 `.claude/skills/universal-image-gen/SKILL.md`：

```yaml
---
name: universal-image-gen
description: 智能圖片生成技能，優先使用 Antigravity API，失敗時自動降級到 NanoBanana。支援任意尺寸、多種品質和批次生成。
metadata:
  category: content-creation
  type: automation
  languages:
    - python
  compatibility:
    - claude-code
    - opencode
    - any-agent
---

# Universal Image Gen

智能圖片生成工具，具有自動備選機制。

## 功能特性

- **主要服務**：Antigravity API（高品質文生圖）
- **備選服務**：NanoBanana API（文生圖 + 圖生圖）
- **自動降級**：主服務失敗時自動切換
- **靈活尺寸**：支援任意 `WIDTHxHEIGHT` 格式
- **品質選項**：hd、medium、standard
- **批次生成**：1-10 張圖片

## 使用範例

```bash
# 基本使用
python3 scripts/generate.py "a beautiful sunset" --size 1920x1080 --quality hd

# 批次生成
python3 scripts/generate.py "mountain landscape" --batch 4

# 圖生圖
python3 scripts/generate.py "enhance this image" --input input.jpg --force-provider nanobanana
```
```

### 範例 3：多平台相容 - Git Release 技能

創建同時支援 Claude Code 和 OpenCode 的技能：

```yaml
---
name: git-release
description: 創建一致的版本發布和變更日誌（支援 Claude Code 和 OpenCode）
license: MIT
metadata:
  audience: maintainers
  workflow: github
  compatibility:
    - claude-code
    - opencode
---

# Git Release Skill

## 我做什麼

1. 根據合併的 PR 起草發布說明
2. 建議版本號升級
3. 提供可複製貼上的 `gh release create` 指令

## 什麼時候使用我

在準備標籤發布時使用此技能。如果目標版本方案不明確，請提出澄清問題。

## 使用方式

**Claude Code**：
```bash
# 使用 Skill 工具
/generate-release-notes
```

**OpenCode**：
```bash
# 執行 skill
/git-release
```

**或自動檢測**：
當 Agent 檢測到需要發布時自動使用。
```

### 範例 4：社交媒體內容創作

創建 `.claude/skills/social-content-writer/SKILL.md`：

```yaml
---
name: social-content-writer
description: 智能社交媒體內容創作技能，支持資料收集、勾子生成、內容創作、圖片/影片提示詞生成、平台適配和多平台發布。支援 Facebook、Instagram、LinkedIn、Threads 等平台，自動生成吸引人的勾子和高品質內容，並提供圖片和影片 AI 生成提示詞。
metadata:
  category: content-creation
  type: automation
  languages:
    - python
  platforms:
    - facebook
    - instagram
    - linkedin
    - threads
---

# Social Content Writer

智能的社交媒體內容創作技能。

## 核心功能

1. **📚 資料收集** - 從多個來源收集相關資料
2. **✨ 勾子生成** - 生成5種類型的吸引人開頭
3. **✍️ 內容創作** - 基於框架生成高品質內容
4. **🖼️ 圖片/影片提示詞生成** - 為內容生成專業精準的圖片和影片提示詞
5. **🎯 平台適配** - 自動調整內容以符合各平台規則
6. **🚀 多平台發布** - 一鍵發布到 Facebook、Instagram、LinkedIn 等

## 使用範例

```bash
# 生成內容
python3 scripts/write-content.py \
  --topic "AI內容創作趨勢" \
  --platform facebook \
  --framework aida

# 完整工作流
python3 scripts/write-content.py \
  --topic "2025年社交媒體趨勢" \
  --platforms facebook,instagram,linkedin \
  --generate-prompts \
  --auto-generate-images \
  --auto-publish
```
```

### 範例 5：API 約定技能

創建 `.claude/skills/api-conventions/SKILL.md`：

```yaml
---
name: api-conventions
description: 項目 API 設計約定和最佳實踐（適用於所有 Agent）
metadata:
  category: conventions
  type: guide
  language: typescript
---

## API 設計約定

編寫 API 端點時遵循以下約定：

1. **RESTful 命名**
   - 使用動詞 + 名詞的命名模式
   - 端點使用 kebab-case
   - 複數形式用於資源端點

2. **回應格式**
   ```json
   {
     "success": true,
     "data": {},
     "error": null,
     "meta": {}
   }
   ```

3. **錯誤處理**
   - 返回適當的 HTTP 狀態碼
   - 錯誤訊息使用統一格式
   - 包含錯誤代碼和描述
```

## 工具調用方式

不同的 AI Agent 有不同的技能調用方式：

### Claude Code (Anthropic)

Claude Code 使用 `Skill` 工具來執行技能：

```python
# 使用技能
Skill(skill="mysql", args="SELECT * FROM users")
```

或者在對話中使用：
```
請使用 mysql 技能查詢所有用戶
```

### OpenCode

OpenCode 在 `skill` 工具描述中列出可用的 Skills：

```xml
<available_skills>
  <skill>
    <name>mysql</name>
    <description>MySQL 資料庫操作技能</description>
  </skill>
  <skill>
    <name>git-release</name>
    <description>創建一致的版本發布和變更日誌</description>
  </skill>
</available_skills>
```

Agent 透過調用工具載入技能：

```javascript
skill({ name: "git-release" })
```

### 通用建議

為了讓技能在不同 Agent 中都能正常工作：

1. **提供清晰的描述**：讓 Agent 理解技能的功能
2. **包含使用範例**：展示如何正確使用
3. **說明輸入輸出**：明確參數格式和返回結果
4. **添加錯誤處理**：說明常見錯誤和解決方案

## 權限配置

### OpenCode 權限系統

使用 `opencode.json` 中基於模式的權限控制 Agent 可以訪問哪些 Skills：

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

| 權限 | 行為 |
|------|------|
| `allow` | 技能立即載入 |
| `deny` | 技能對 Agent 隱藏，訪問被拒絕 |
| `ask` | 在載入前提示用戶批准 |

模式支援通配符：`internal-*` 匹配 `internal-docs`, `internal-tools` 等。

### Claude Code 權限系統

Claude Code 通常不使用複雜的權限系統，而是：
- 自動發現 `.claude/skills/` 目錄中的所有技能
- 根據 `SKILL.md` 的 frontmatter 決定是否載入
- 用戶可以通過對話控制技能的使用

### 通用權限建議

為了保護敏感技能：

1. **命名敏感技能**：使用 `internal-` 或 `private-` 前綴
2. **在描述中說明**：在 frontmatter 中標記敏感度
3. **使用 metadata**：添加 `audience` 或 `access-level` 字段

```yaml
---
name: internal-deploy
description: 內部部署工具（僅限授權人員使用）
metadata:
  access-level: restricted
  allowed-users:
    - admin
    - devops
---
```

### 每個 Agent 覆蓋權限

**對於自定義 Agents**（在 agent frontmatter 中）：

```yaml
---
permission:
  skill:
    "documents-*": "allow"
---
```

**對於內建 Agents**（在 `opencode.json` 中）：

```json
{
  "agent": {
    "plan": {
      "permission": {
        "skill": {
          "internal-*": "allow"
        }
      }
    }
  }
}
```

## 禁用 Skill 工具

完全禁用不應該使用 Skills 的 Agents 的技能工具：

**對於自定義 Agents**：

```yaml
---
tools:
  skill: false
---
```

**對於內建 Agents**：

```json
{
  "agent": {
    "plan": {
      "tools": {
        "skill": false
      }
    }
  }
}
```

當禁用時，`<available_skills>` 部分將被完全省略。

## 故障排除

### Skill 沒有顯示出來

如果 Skill 沒有顯示：

1. 驗證 `SKILL.md` 是全大寫拼寫
2. 檢查 frontmatter 包含 `name` 和 `description`
3. 確保技能名稱在所有位置中唯一
4. 檢查權限 - `deny` 權限的技能對 Agent 隱藏

### Frontmatter 錯誤

確保 frontmatter 在文件開頭，用 `---` 包裹：

```yaml
---
name: my-skill
description: 技能描述
---

## 內容...
```

### 名稱不匹配

目錄名稱必須與 `name` 字段匹配：

```
✅ .opencode/skills/my-skill/SKILL.md
   ---
   name: my-skill
   ---

❌ .opencode/skills/my-skill/SKILL.md
   ---
   name: different-name
   ---
```

## 多文件 Skills

Skills 可以包含其他文件作為參考：

```
my-skill/
├── SKILL.md           # 主文件（必需）
├── examples.md        # 使用範例
├── reference.md       # 詳細參考文檔
└── scripts/
    └── helper.sh     # 輔助腳本
```

在 `SKILL.md` 中引用這些文件：

```markdown
## 參考資料

- 詳細 API 文檔參見 [reference.md](reference.md)
- 使用範例參見 [examples.md](examples.md)
- 輔助腳本位於 `scripts/helper.sh`
```

## 項目集成建議

1. **提交 Skills 到 Git**
   - Skills 應該提交到版本控制
   - 讓團隊成員可以共享和改進
   - 使用清晰的 Git 訊息

2. **版本控制**
   - 在 `metadata` 中添加版本信息
   - 在文件頂部記錄變更日誌
   - 使用語義化版本

3. **團隊協作**
   - 為不同團隊成員創建專門 Skills
   - 建立 Skills 審查流程
   - 維護中心化的 Skills 庫

## 最佳實踐

### 1. 保持專注
- 每個 Skill 應該有明確的目的
- 避免過於寬泛的描述
- 保持 `description` 簡潔明瞭（1-1024 字符）

### 2. 提供上下文
- 在 `metadata` 中包含相關信息
- 說明技能的適用場景
- 指出不適用的情況

### 3. 測試 Skills
- 在多種場景下測試
- 驗證多個 Agent 都能正確識別
- 收集反饋並持續改進

### 4. 文檔清晰
- 使用清晰的標題和分節
- 提供具體範例
- 記錄故障排除步驟

### 5. 跨平台兼容性
為了讓技能在多個平台上都能使用：

**✅ 推薦做法**：
- 使用 `.claude/skills/` 作為主要位置（Claude Code 原生支持）
- 在 frontmatter 中標明 `compatibility`
- 提供通用的使用範例
- 避免平台特定的功能

```yaml
---
name: my-skill
description: 通用技能描述
metadata:
  compatibility:
    - claude-code
    - opencode
    - any-agent
---
```

**❌ 避免的做法**：
- 只在 `.opencode/skills/` 創建（其他平台無法使用）
- 使用 OpenCode 特定的語法
- 依賴特定平台的工具或API

### 6. 目錄結構建議

完整的技能目錄結構：

```
my-skill/
├── SKILL.md              # 主文件（必需）
├── README.md             # 詳細說明（可選）
├── examples/             # 使用範例
│   ├── basic.md
│   └── advanced.md
├── scripts/              # 可執行腳本
│   ├── main.py
│   └── helper.sh
└── docs/                 # 額外文檔
    └── api-reference.md
```

### 7. 版本控制建議

1. **提交 Skills 到 Git**
   - Skills 應該提交到版本控制
   - 讓團隊成員可以共享和改進
   - 使用清晰的 Git 訊息

2. **版本管理**
   - 在 `metadata` 中添加版本信息
   - 在文件頂部記錄變更日誌
   - 使用語義化版本

```yaml
---
name: my-skill
description: 我的技能
version: 1.0.0
metadata:
  changelog:
    - "1.0.0: 初始版本"
    - "1.1.0: 添加新功能"
---
```

### 8. 命名最佳實踐

選擇清晰、描述性的名稱：

✅ **好的命名**：
- `mysql-database` - 明確指出是資料庫相關
- `image-generator` - 清楚說明功能
- `social-content-writer` - 具體且描述性

❌ **避免的命名**：
- `helper` - 太模糊
- `tool` - 不夠具體
- `stuff` - 完全沒有意義

### 9. 安全性考慮

對於涉及敏感操作的技能：

1. **明確標記敏感度**：
```yaml
---
name: production-deploy
description: 生產環境部署工具（需要特別權限）
metadata:
  access-level: restricted
  requires-approval: true
---
```

2. **添加安全檢查**：
- 在腳本中實施權限驗證
- 提供乾運行模式（dry-run）
- 記錄所有操作

3. **文檔化風險**：
- 在 SKILL.md 中說明風險
- 提供回滯步驟
- 列出先決條件

---

## 快速開始範例

### 5 分鐘創建你的第一個技能

**步驟 1**：創建目錄結構

```bash
mkdir -p .claude/skills/hello-world
cd .claude/skills/hello-world
```

**步驟 2**：創建 SKILL.md

```bash
cat > SKILL.md << 'EOF'
---
name: hello-world
description: 一個簡單的歡迎技能，示範如何創建 Agent Skills
metadata:
  category: example
  type: demonstration
  compatibility:
    - claude-code
    - opencode
    - any-agent
---

# Hello World Skill

這是一個示範技能，展示如何創建跨平台兼容的 Agent Skills。

## 功能

- 提供友好的歡迎訊息
- 展示當前時間和日期
- 列出可用的技能

## 使用方式

在 Claude Code 中：
```
請使用 hello-world 技能
```

或在 OpenCode 中：
```
/hello-world
```

## 範例輸出

```
👋 歡迎使用 Agent Skills！

當前時間：2026-01-30 12:00:00
可用技能數量：11

祝你使用愉快！
```
EOF
```

**步驟 3**：（可選）添加腳本

```bash
mkdir scripts
cat > scripts/hello.sh << 'EOF'
#!/bin/bash
echo "👋 Hello from $USER!"
echo "Current time: $(date)"
EOF
chmod +x scripts/hello.sh
```

**步驟 4**：測試技能

重啟你的 Agent，然後說：
```
請使用 hello-world 技能
```

---

## 總結

### 關鍵要點

1. ✅ **使用 `.claude/skills/`** - Claude Code 原生支持
2. ✅ **添加 `compatibility` metadata** - 標明支援的平台
3. ✅ **提供清晰描述** - 讓 Agent 理解技能功能
4. ✅ **包含使用範例** - 展示如何正確使用
5. ✅ **遵循命名規則** - 小寫字母、數字、連字符

### 常見平台比較

| 特性 | Claude Code | OpenCode |
|------|-------------|----------|
| 技能目錄 | `.claude/skills/` | `.opencode/skills/`, `.claude/skills/` |
| Frontmatter | YAML | YAML |
| 必填字段 | name, description | name, description |
| 可選字段 | metadata, compatibility | license, metadata |
| 權限系統 | 對話控制 | opencode.json 配置 |
| 調用方式 | Skill 工具或對話 | skill() 函數 |

### 相容性建議

**為了最大兼容性**：

```yaml
---
name: my-skill
description: 清晰的功能描述
metadata:
  compatibility:
    - claude-code
    - opencode
    - any-agent
  category: utility
  type: automation
  languages:
    - python
    - javascript
---
```

這樣的技能可以在：
- ✅ Claude Code (Anthropic)
- ✅ OpenCode
- ✅ 任何支援技能系統的 AI Agent
- ✅ 未來的新平台

中使用！
