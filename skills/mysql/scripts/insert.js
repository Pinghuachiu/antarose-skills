#!/usr/bin/env node
/**
 * MySQL Insert - Node.js 腳本
 * 插入新記錄到 MySQL 資料表
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

async function insertRecord(table, data) {
  const conn = await getConnection();

  try {
    const columns = Object.keys(data).join(', ');
    const placeholders = Object.keys(data).map(() => '?').join(', ');
    const values = Object.values(data);

    const sql = `INSERT INTO ${table} (${columns}) VALUES (${placeholders})`;
    const [result] = await conn.execute(sql, values);

    return result.insertId;
  } catch (error) {
    console.error(`插入失敗: ${error.message}`);
    process.exit(1);
  } finally {
    await conn.end();
  }
}

async function main() {
  if (process.argv.length < 4) {
    console.log('使用方法: node insert.js <table> <data>');
    console.log('範例:');
    console.log('  node insert.js users \'{"name":"John","email":"john@example.com","age":25}\'');
    console.log('  node insert.js products \'{"name":"Product A","price":99.99}\'');
    process.exit(1);
  }

  const table = process.argv[2];
  let data;

  try {
    data = JSON.parse(process.argv[3]);
  } catch (error) {
    console.error(`JSON 解析失敗: ${error.message}`);
    process.exit(1);
  }

  if (typeof data !== 'object' || data === null || Array.isArray(data)) {
    console.error('錯誤: data 必須是 JSON 物件格式');
    process.exit(1);
  }

  const insertId = await insertRecord(table, data);
  console.log(`成功插入記錄，ID: ${insertId}`);
}

main().catch(error => {
  console.error('未預期的錯誤:', error);
  process.exit(1);
});
