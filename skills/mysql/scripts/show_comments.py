#!/usr/bin/env python3
"""
MySQL Show Column Comments - Python 腳本
顯示資料表的欄位說明
"""

import os
import sys
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

def show_column_comments(table):
    """顯示資料表欄位說明"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = f"SHOW FULL COLUMNS FROM {table}"
        cursor.execute(sql)
        results = cursor.fetchall()

        print(f"\n{'='*80}")
        print(f"資料表: {table} 的欄位說明")
        print(f"{'='*80}\n")

        for row in results:
            field = row['Field']
            type_info = row['Type'].decode('utf-8') if isinstance(row['Type'], bytes) else row['Type']
            comment = row['Comment'].decode('utf-8') if isinstance(row['Comment'], bytes) else row['Comment']
            null = row['Null'].decode('utf-8') if isinstance(row['Null'], bytes) else row['Null']
            key = row['Key'].decode('utf-8') if isinstance(row['Key'], bytes) else row['Key']
            default = row['Default']

            print(f"欄位名稱: {field}")
            print(f"資料類型: {type_info}")
            print(f"可為空: {null}")
            print(f"鍵值: {key}")
            if default:
                default_str = default.decode('utf-8') if isinstance(default, bytes) else str(default)
                print(f"預設值: {default_str}")
            print(f"說明: {comment if comment else '(無)'}")
            print(f"{'-'*80}\n")
    except mysql.connector.Error as e:
        print(f"錯誤: {e}", file=sys.stderr)
    finally:
        cursor.close()
        conn.close()

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 show_comments.py <table>")
        print("範例:")
        print("  python3 show_comments.py channal_info")
        sys.exit(1)

    table = sys.argv[1]
    show_column_comments(table)

if __name__ == "__main__":
    main()
