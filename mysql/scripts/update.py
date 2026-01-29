#!/usr/bin/env python3
"""
MySQL Update - Python 腳本
更新 MySQL 資料表中的記錄
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

def update_record(table, record_id, data):
    """
    更新資料表中的記錄

    Args:
        table: 資料表名稱
        record_id: 記錄 ID
        data: 要更新的資料（字典格式）

    Returns:
        受影響的行數
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE id = %s"

        values = tuple(data.values()) + (record_id,)
        cursor.execute(sql, values)
        conn.commit()

        affected_rows = cursor.rowcount
        return affected_rows
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"更新失敗: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

def main():
    if len(sys.argv) < 4:
        print("使用方法: python3 update.py <table> <id> <data>")
        print("範例:")
        print('  python3 update.py users 5 \'{"name":"Updated Name","age":26}\'')
        print('  python3 update.py products 10 \'{"price":89.99}\'')
        sys.exit(1)

    table = sys.argv[1]
    try:
        record_id = int(sys.argv[2])
    except ValueError:
        print("錯誤: id 必須是整數", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(sys.argv[3])
    except json.JSONDecodeError as e:
        print(f"JSON 解析失敗: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print("錯誤: data 必須是 JSON 物件格式", file=sys.stderr)
        sys.exit(1)

    affected_rows = update_record(table, record_id, data)
    print(f"成功更新記錄，影響 {affected_rows} 行")

if __name__ == "__main__":
    main()
