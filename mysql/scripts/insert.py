#!/usr/bin/env python3
"""
MySQL Insert - Python 腳本
插入新記錄到 MySQL 資料表
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

def insert_record(table, data):
    """
    插入記錄到資料表

    Args:
        table: 資料表名稱
        data: 要插入的資料（字典格式）

    Returns:
        插入的記錄 ID
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor.execute(sql, tuple(data.values()))
        conn.commit()

        insert_id = cursor.lastrowid
        return insert_id
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"插入失敗: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

def main():
    if len(sys.argv) < 3:
        print("使用方法: python3 insert.py <table> <data>")
        print("範例:")
        print('  python3 insert.py users \'{"name":"John","email":"john@example.com","age":25}\'')
        print('  python3 insert.py products \'{"name":"Product A","price":99.99}\'')
        sys.exit(1)

    table = sys.argv[1]
    try:
        data = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(f"JSON 解析失敗: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print("錯誤: data 必須是 JSON 物件格式", file=sys.stderr)
        sys.exit(1)

    insert_id = insert_record(table, data)
    print(f"成功插入記錄，ID: {insert_id}")

if __name__ == "__main__":
    main()
