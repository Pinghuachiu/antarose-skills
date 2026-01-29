#!/usr/bin/env node
/**
 * MySQL Show Column Comments - Node.js 腳本
 * 顯示資料表的欄位說明
 */

const mysql = require('mysql2/promise');

async function getConnection() {
  try {
    const conn = await mysql.createConnection({
      host: process.env.MYSQL_HOST || '192.168.1.159',
      port: parseInt(process.env.MYSQL_PORT) || 3306,
      user: process.env.MYSQL_USER || 'n8n',
      password: process.env.MYSQL_PASSWORD || '!!asshole!!asshole',
      database: process.env.MYSQL_DATABASE || 'infoCollection'
    });
    return conn;
  } catch (error) {
    console.error(`資料庫連線失敗: ${error.message}`);
    process.exit(1);
  }
}

async function showColumnComments(table) {
  const conn = await getConnection();

  try {
    const [rows] = await conn.execute('SHOW FULL COLUMNS FROM ?', [table]);

    console.log('\n' + '='.repeat(80));
    console.log(`資料表: ${table} 的欄位說明`);
    console.log('='.repeat(80) + '\n');

    for (const row of rows) {
      console.log(`欄位名稱: ${row.Field}`);
      console.log(`資料類型: ${row.Type}`);
      console.log(`可為空: ${row.Null}`);
      console.log(`鍵值: ${row.Key}`);
      if (row.Default) {
        console.log(`預設值: ${row.Default}`);
      }
      console.log(`說明: ${row.Comment || '(無)'}`);
      console.log('-'.repeat(80) + '\n');
    }
  } catch (error) {
    console.error(`錯誤: ${error.message}`);
  } finally {
    await conn.end();
  }
}

async function main() {
  if (process.argv.length < 3) {
    console.log('使用方法: node show_comments.js <table>');
    console.log('範例:');
    console.log('  node show_comments.js channal_info');
    process.exit(1);
  }

  const table = process.argv[2];
  await showColumnComments(table);
}

main().catch(error => {
  console.error('未預期的錯誤:', error);
  process.exit(1);
});
