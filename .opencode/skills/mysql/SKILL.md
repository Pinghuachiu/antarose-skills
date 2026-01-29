---
name: mysql
description: 使用 Python 和 Node.js 腳本進行 MySQL 資料庫操作，包括連接、查詢、插入、更新和刪除操作
metadata:
  category: database
  type: mysql
  languages:
    - python
    - javascript
    - bash
  supports:
    - connect
    - query
    - insert
    - update
    - delete
    - batch-operations
---

# MySQL Database - 資料庫存取技能

使用 Python 和 Node.js 腳本進行 MySQL 資料庫操作，支援各種 CRUD 操作。

## 資料庫資訊

- **主機**: 192.168.1.159
- **端口**: 3306
- **資料庫**: infoCollection
- **Root 密碼**: !!asshole!!asshole
- **使用者帳號**: n8n
- **使用者密碼**: !!asshole!!asshole
- **連線字串**: `mysql://n8n:!!asshole!!asshole@192.168.1.159:3306/infoCollection`

## 環境變數

使用前請設定以下環境變數：

```bash
export MYSQL_HOST=165.154.226.78
export MYSQL_PORT=3306
export MYSQL_USER=n8n
export MYSQL_PASSWORD=!!asshole!!asshole
export MYSQL_DATABASE=infoCollection
```

請參考 [resource.md](../../../resource.md) 獲取完整的資料庫連線資訊。

## 快速開始

### Python 腳本

```bash
# 查詢資料
python3 skills/mysql/scripts/query.py "SELECT * FROM users"

# 插入資料
python3 skills/mysql/scripts/insert.py users '{"name":"John","email":"john@example.com"}'

# 更新資料
python3 skills/mysql/scripts/update.py users 1 '{"name":"John Updated"}'

# 刪除資料
python3 skills/mysql/scripts/delete.py users 1
```

### Node.js 腳本

```bash
# 查詢資料
node skills/mysql/scripts/query.js "SELECT * FROM users"

# 插入資料
node skills/mysql/scripts/insert.js users '{"name":"John","email":"john@example.com"}'

# 更新資料
node skills/mysql/scripts/update.js users 1 '{"name":"John Updated"}'

# 刪除資料
node skills/mysql/scripts/delete.js users 1
```

## 腳本說明

### 查看欄位說明腳本 (show_comments.py / show_comments.js)

顯示資料表的欄位結構和說明。

**參數**:
- `table`: 資料表名稱（必需）

**範例**:
```bash
python3 skills/mysql/scripts/show_comments.py channal_info
```

### 查詢腳本 (query.py / query.js)

### 查詢腳本 (query.py / query.js)

執行 SELECT 查詢並返回結果。

**參數**:
- `sql`: SQL 查詢語句（必需）

**範例**:
```bash
python3 skills/mysql/scripts/query.py "SELECT * FROM users WHERE age > 18"
node skills/mysql/scripts/query.js "SELECT COUNT(*) FROM orders"
```

### 插入腳本 (insert.py / insert.js)

插入新記錄到指定資料表。

**參數**:
- `table`: 資料表名稱（必需）
- `data`: JSON 格式的資料（必需）

**範例**:
```bash
python3 skills/mysql/scripts/insert.py users '{"name":"Alice","email":"alice@example.com","age":25}'
node skills/mysql/scripts/insert.js products '{"name":"Product A","price":99.99,"stock":100}'
```

### 更新腳本 (update.py / update.js)

更新指定記錄。

**參數**:
- `table`: 資料表名稱（必需）
- `id`: 記錄 ID（必需）
- `data`: JSON 格式的更新資料（必需）

**範例**:
```bash
python3 skills/mysql/scripts/update.py users 5 '{"name":"Updated Name","age":26}'
node skills/mysql/scripts/update.js products 10 '{"price":89.99}'
```

### 刪除腳本 (delete.py / delete.js)

刪除指定記錄。

**參數**:
- `table`: 資料表名稱（必需）
- `id`: 記錄 ID（必需）

**範例**:
```bash
python3 skills/mysql/scripts/delete.py users 5
node skills/mysql/scripts/delete.js products 10
```

## 查看資料表結構

### 查看欄位說明

使用 `SHOW FULL COLUMNS` 命令查看包含說明的欄位資訊：

```python
python3 skills/mysql/scripts/query.py "SHOW FULL COLUMNS FROM table_name"
```

### 添加欄位說明

為資料表欄位添加說明：

```sql
ALTER TABLE table_name
MODIFY COLUMN column_name VARCHAR(255) COMMENT '欄位說明文字';
```

## Python 程式碼範例

### 連線資料庫

```python
import os
import mysql.connector

conn = mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST', '165.154.226.78'),
    port=int(os.environ.get('MYSQL_PORT', 3306)),
    user=os.environ.get('MYSQL_USER', 'n8n'),
    password=os.environ.get('MYSQL_PASSWORD', '!!asshole!!asshole'),
    database=os.environ.get('MYSQL_DATABASE', 'infoCollection')
)

cursor = conn.cursor(dictionary=True)
```

### 查詢資料

```python
cursor.execute("SELECT * FROM users WHERE age > %s", (18,))
results = cursor.fetchall()
for row in results:
    print(row)
```

### 插入資料

```python
data = {'name': 'John', 'email': 'john@example.com', 'age': 25}
columns = ', '.join(data.keys())
placeholders = ', '.join(['%s'] * len(data))
sql = f"INSERT INTO users ({columns}) VALUES ({placeholders})"
cursor.execute(sql, tuple(data.values()))
conn.commit()
```

### 更新資料

```python
data = {'name': 'Updated Name', 'age': 26}
set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
sql = f"UPDATE users SET {set_clause} WHERE id = %s"
cursor.execute(sql, tuple(data.values()) + (user_id,))
conn.commit()
```

### 刪除資料

```python
sql = "DELETE FROM users WHERE id = %s"
cursor.execute(sql, (user_id,))
conn.commit()
```

## Node.js 程式碼範例

### 連線資料庫

```javascript
const mysql = require('mysql2/promise');

const conn = await mysql.createConnection({
  host: process.env.MYSQL_HOST || '165.154.226.78',
  port: parseInt(process.env.MYSQL_PORT) || 3306,
  user: process.env.MYSQL_USER || 'n8n',
  password: process.env.MYSQL_PASSWORD || '!!asshole!!asshole',
  database: process.env.MYSQL_DATABASE || 'infoCollection'
});
```

### 查詢資料

```javascript
const [rows] = await conn.execute('SELECT * FROM users WHERE age > ?', [18]);
console.log(rows);
```

### 插入資料

```javascript
const data = { name: 'John', email: 'john@example.com', age: 25 };
const columns = Object.keys(data).join(', ');
const placeholders = Object.keys(data).map(() => '?').join(', ');
const values = Object.values(data);

const sql = `INSERT INTO users (${columns}) VALUES (${placeholders})`;
await conn.execute(sql, values);
```

### 更新資料

```javascript
const data = { name: 'Updated Name', age: 26 };
const setClause = Object.keys(data).map(k => `${k} = ?`).join(', ');
const values = [...Object.values(data), userId];

const sql = `UPDATE users SET ${setClause} WHERE id = ?`;
await conn.execute(sql, values);
```

### 刪除資料

```javascript
const sql = 'DELETE FROM users WHERE id = ?';
await conn.execute(sql, [userId]);
```

## 常用 SQL 語句

### 查詢語句

```sql
-- 查詢所有記錄
SELECT * FROM table_name;

-- 帶條件查詢
SELECT * FROM table_name WHERE condition;

-- 排序
SELECT * FROM table_name ORDER BY column_name DESC;

-- 限制結果數量
SELECT * FROM table_name LIMIT 10;

-- 分組統計
SELECT column, COUNT(*) FROM table_name GROUP BY column;

-- 連線查詢
SELECT t1.*, t2.* FROM table1 t1 JOIN table2 t2 ON t1.id = t2.table1_id;
```

### 插入語句

```sql
-- 插入單條記錄
INSERT INTO table_name (col1, col2) VALUES (val1, val2);

-- 批量插入
INSERT INTO table_name (col1, col2) VALUES (val1, val2), (val3, val4);
```

### 更新語句

```sql
-- 更新單條記錄
UPDATE table_name SET col1 = val1, col2 = val2 WHERE id = 1;

-- 批量更新
UPDATE table_name SET col1 = val1 WHERE condition;
```

### 刪除語句

```sql
-- 刪除單條記錄
DELETE FROM table_name WHERE id = 1;

-- 批量刪除
DELETE FROM table_name WHERE condition;
```

### 資料表操作

```sql
-- 創建資料表
CREATE TABLE table_name (
    id INT AUTO_INCREMENT PRIMARY KEY,
    column1 VARCHAR(255),
    column2 INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 修改資料表結構
ALTER TABLE table_name ADD COLUMN new_column VARCHAR(255);

-- 刪除資料表
DROP TABLE table_name;
```

## 注意事項

1. **環境變數**: 使用前請設定 MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE 環境變數
2. **SQL 注入**: 始終使用參數化查詢，避免 SQL 注入風險
3. **連線管理**: 使用完畢後記得關閉資料庫連線
4. **錯誤處理**: 在程式碼中添加適當的錯誤處理機制
5. **備份**: 重要資料操作前請先備份資料庫
6. **權限**: 使用適當的使用者權限，避免使用 root 帳號進行日常操作
7. **清理 /tmp**: 腳本會自動清理 /tmp 目錄中的暫存檔案，任務結束後會清除本腳本創建的暫存檔案

## 錯誤處理

### 常見錯誤

1. **連線失敗**: 檢查主機地址、端口、使用者名稱和密碼是否正確
2. **資料表不存在**: 確認資料表名稱是否正確
3. **語法錯誤**: 檢查 SQL 語句是否符合 MySQL 語法
4. **權限不足**: 檢查使用者是否有足夠的權限執行相關操作

### 調試技巧

1. 啟用 SQL 日誌記錄
2. 使用 `EXPLAIN` 分析查詢性能
3. 檢查資料庫連線狀態
4. 驗證環境變數是否正確設定

## 依賴套件

### Python

```bash
pip install mysql-connector-python
```

### Node.js

```bash
npm install mysql2
```

## 最佳實踐

1. **使用連線池**: 在高併發場景下使用連線池提高性能
2. **事務管理**: 對於需要原子性的操作使用事務
3. **索引優化**: 為經常查詢的欄位創建索引
4. **分頁查詢**: 大量資料查詢時使用分頁
5. **定期備份**: 定期備份資料庫以防止資料丟失
