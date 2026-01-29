#!/usr/bin/env node
/**
 * MySQL Query - Node.js 腳本
 * 執行 MySQL SELECT 查詢並返回結果
 */

const mysql = require('mysql2/promise');

async function getConnection() {
  try {
    const conn = await mysql.createConnection({
      host: process.env.MYSQL_HOST || '165.154.226.78',
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

async function executeQuery(sql, params = []) {
  const conn = await getConnection();

  try {
    const [rows] = await conn.execute(sql, params);
    return rows;
  } catch (error) {
    console.error(`查詢執行失敗: ${error.message}`);
    return [];
  } finally {
    await conn.end();
  }
}

async function main() {
  if (process.argv.length < 3) {
    console.log('使用方法: node query.js <sql> [params...]');
    console.log('範例:');
    console.log('  node query.js "SELECT * FROM users"');
    console.log('  node query.js "SELECT * FROM users WHERE age > ?" 18');
    process.exit(1);
  }

  const sql = process.argv[2];
  const params = process.argv.slice(3);

  const results = await executeQuery(sql, params);

  if (results.length > 0) {
    console.log(JSON.stringify(results, null, 2));
  } else {
    console.log('沒有找到符合的記錄');
  }
}

main().catch(error => {
  console.error('未預期的錯誤:', error);
  process.exit(1);
});
