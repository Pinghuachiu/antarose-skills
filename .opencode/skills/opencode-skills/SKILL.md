---
name: opencode-skills
description: 教導如何創建和使用 OpenCode Skills，包括目錄結構、frontmatter 規範、命名規則和完整範例
---

# OpenCode Skills 指南

OpenCode Skills 讓你可以定義可重用的行為，透過 SKILL.md 文件讓 OpenCode 發現和使用指令。

## 目錄結構

OpenCode 在以下位置搜尋 Skills：

### 項目層級
- `.opencode/skills/<name>/SKILL.md` - 項目特定技能
- `.claude/skills/<name>/SKILL.md` - Claude 相容的項目技能

### 全局層級
- `~/.config/opencode/skills/<name>/SKILL.md` - 全局 OpenCode 技能
- `~/.claude/skills/<name>/SKILL.md` - Claude 相容的全局技能

### 自動發現
對於項目本地路徑，OpenCode 會從當前工作目錄向上遍歷到 git worktree，沿途載入所有匹配的 `skills/*/SKILL.md`。

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
| `license` | 授權協議 |
| `compatibility` | 相容性標識（如 opencode, claude）|
| `metadata` | 額外的字符串到字符串映射 |

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

### 範例 1：Git Release 技能

創建 `.opencode/skills/git-release/SKILL.md`：

```yaml
---
name: git-release
description: 創建一致的版本發布和變更日誌
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

## 我做什麼

1. 根據合併的 PR 起草發布說明
2. 建議版本號升級
3. 提供可複製貼上的 `gh release create` 指令

## 什麼時候使用我

在準備標籤發布時使用此技能。如果目標版本方案不明確，請提出澄清問題。

## 使用方式

執行 `/git-release` 或 OpenCode 自動檢測到需要發布時使用。
```

### 範例 2：API 約定技能

創建 `.opencode/skills/api-conventions/SKILL.md`：

```yaml
---
name: api-conventions
description: 項目 API 設計約定和最佳實踐
metadata:
  category: conventions
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

4. **請求驗證**
   - 使用 Zod 進行 schema 驗證
   - 返回具體的驗證錯誤訊息
   - 記錄所有驗證失敗
```

### 範例 3：代碼審查技能

創建 `.opencode/skills/code-review/SKILL.md`：

```yaml
---
name: code-review
description: 執行深度代碼審查，檢查品質、安全性和最佳實踐
metadata:
  category: quality
  severity: high
---

## 代碼審查檢查清單

### 功能正確性
- [ ] 代碼符合需求規格
- [ ] 邊界條件已處理
- [ ] 錯誤處理完整

### 代碼品質
- [ ] 變量命名清晰且一致
- [ ] 函數職責單一
- [ ] 避免重複代碼
- [ ] 註解充分但非冗餘

### 安全性
- [ ] 輸入驗證
- [ ] SQL 注入防護
- [ ] XSS 防護
- [ ] 敏感資料保護

### 性能
- [ ] 資料庫查詢優化
- [ ] 避免不必要的計算
- [ ] 適當使用快取

### 可維護性
- [ ] 遵循項目編碼風格
- [ ] 測試覆蓋充分
- [ ] 文檔完整

## 審查流程

1. 理解變更的上下文和目的
2. 逐個檢查上述類別
3. 提供建設性的改進建議
4. 如果需要，要求澄清
5. 總結發現和優先級
```

## 工具描述

OpenCode 在 `skill` 工具描述中列出可用的 Skills。每個條目包含技能名稱和描述：

```xml
<available_skills>
  <skill>
    <name>git-release</name>
    <description>創建一致的版本發布和變更日誌</description>
  </skill>
  <skill>
    <name>code-review</name>
    <description>執行深度代碼審查，檢查品質、安全性和最佳實踐</description>
  </skill>
</available_skills>
```

Agent 透過調用工具載入技能：

```javascript
skill({ name: "git-release" })
```

## 權限配置

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

1. **保持專注**
   - 每個 Skill 應該有明確的目的
   - 避免過於寬泛的描述
   - 保持 `description` 簡潔明瞭

2. **提供上下文**
   - 在 `metadata` 中包含相關信息
   - 說明技能的適用場景
   - 指出不適用的情況

3. **測試 Skills**
   - 在多種場景下測試
   - 驗證 OpenCode 能正確識別
   - 收集反饋並持續改進

4. **文檔清晰**
   - 使用清晰的標題和分節
   - 提供具體範例
   - 記錄故障排除步驟
