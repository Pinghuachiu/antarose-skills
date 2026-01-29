#!/usr/bin/env node
/**
 * MySQL Update - Node.js 腳本
 * 更新 MySQL 資料表中的記錄
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

async function updateRecord(table, recordId, data) {
  const conn = await getConnection();

  try {
    const setClause = Object.keys(data).map(k => `${k} = ?`).join(', ');
    const values = [...Object.values(data), recordId];

    const sql = `UPDATE ${table} SET ${setClause} WHERE id = ?`;
    const [result] = await conn.execute(sql, values);

    return result.affectedRows;
  } catch (error) {
    console.error(`更新失敗: ${error.message}`);
    process.exit(1);
  } finally {
    await conn.end();
  }
}

async function main() {
  if (process.argv.length < 5) {
    console.log('使用方法: node update.js <table> <id> <data>');
    console.log('範例:');
    console.log('  node update.js users 5 \'{"name":"Updated Name","age":26}\'');
    console.log('  node update.js products 10 \'{"price":89.99}\'');
    process.exit(1);
  }

  const table = process.argv[2];
  const recordId = parseInt(process.argv[3], 10);

  if (isNaN(recordId)) {
    console.error('錯誤: id 必須是整數');
    process.exit(1);
  }

  let data;

  try {
    data = JSON.parse(process.argv[4]);
  } catch (error) {
    console.error(`JSON 解析失敗: ${error.message}`);
    process.exit(1);
  }

  if (typeof data !== 'object' || data === null || Array.isArray(data)) {
    console.error('錯誤: data 必須是 JSON 物件格式');
    process.exit(1);
  }

  const affectedRows = await updateRecord(table, recordId, data);
  console.log(`成功更新記錄，影響 ${affectedRows} 行`);
}

main().catch(error => {
  console.error('未預期的錯誤:', error);
  process.exit(1);
});
