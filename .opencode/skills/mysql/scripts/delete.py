#!/usr/bin/env python3
"""
MySQL Delete - Python 腳本
刪除 MySQL 資料表中的記錄
"""

import os
import sys
import mysql.connector

def get_connection():
    """建立資料庫連線"""
    try:
        conn = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST', '165.154.226.78'),
            port=int(os.environ.get('MYSQL_PORT', 3306)),
            user=os.environ.get('MYSQL_USER', 'n8n'),
            password=os.environ.get('MYSQL_PASSWORD', '!!asshole!!asshole'),
            database=os.environ.get('MYSQL_DATABASE', 'infoCollection')
        )
        return conn
    except mysql.connector.Error as e:
        print(f"資料庫連線失敗: {e}", file=sys.stderr)
        sys.exit(1)

def delete_record(table, record_id):
    """
    刪除資料表中的記錄

    Args:
        table: 資料表名稱
        record_id: 記錄 ID

    Returns:
        受影響的行數
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = f"DELETE FROM {table} WHERE id = %s"
        cursor.execute(sql, (record_id,))
        conn.commit()

        affected_rows = cursor.rowcount
        return affected_rows
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"刪除失敗: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

def main():
    if len(sys.argv) < 3:
        print("使用方法: python3 delete.py <table> <id>")
        print("範例:")
        print("  python3 delete.py users 5")
        print("  python3 delete.py products 10")
        sys.exit(1)

    table = sys.argv[1]
    try:
        record_id = int(sys.argv[2])
    except ValueError:
        print("錯誤: id 必須是整數", file=sys.stderr)
        sys.exit(1)

    affected_rows = delete_record(table, record_id)
    print(f"成功刪除記錄，影響 {affected_rows} 行")

if __name__ == "__main__":
    main()
