#!/usr/bin/env python3
"""
MySQL Query - Python 腳本
執行 MySQL SELECT 查詢並返回結果
"""

import os
import sys
import json
import mysql.connector

def get_connection():
    """建立資料庫連線"""
    try:
        conn = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST', '192.168.1.159'),
            port=int(os.environ.get('MYSQL_PORT', 3306)),
            user=os.environ.get('MYSQL_USER', 'n8n'),
            password=os.environ.get('MYSQL_PASSWORD', '!!asshole!!asshole'),
            database=os.environ.get('MYSQL_DATABASE', 'infoCollection')
        )
        return conn
    except mysql.connector.Error as e:
        print(f"資料庫連線失敗: {e}", file=sys.stderr)
        sys.exit(1)

def execute_query(sql, params=None):
    """
    執行查詢並返回結果

    Args:
        sql: SQL 查詢語句
        params: 查詢參數（可選）

    Returns:
        查詢結果列表
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        results = cursor.fetchall()
        return results
    except mysql.connector.Error as e:
        print(f"查詢執行失敗: {e}", file=sys.stderr)
        return []
    finally:
        cursor.close()
        conn.close()

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 query.py <sql> [params...]")
        print("範例:")
        print('  python3 query.py "SELECT * FROM users"')
        print('  python3 query.py "SELECT * FROM users WHERE age > ?" 18')
        sys.exit(1)

    sql = sys.argv[1]
    params = sys.argv[2:] if len(sys.argv) > 2 else None

    results = execute_query(sql, params)

    if results:
        print(json.dumps(results, indent=2, ensure_ascii=False, default=str))
    else:
        print("沒有找到符合的記錄")

if __name__ == "__main__":
    main()
