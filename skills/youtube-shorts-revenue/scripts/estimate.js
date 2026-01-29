#!/usr/bin/env node
/**
 * YouTube Shorts Revenue Estimator - Node.js 腳本
 * 預估 YouTube Shorts 的收入
 */

const axios = require('axios');

// YouTube Shorts RPM 參考數據（每千次觀看收入）
const RPM_DATA = {
  'us': { min: 0.01, max: 0.06, avg: 0.03, name: '美國' },
  'tw': { min: 0.005, max: 0.03, avg: 0.015, name: '台灣' },
  'uk': { min: 0.01, max: 0.05, avg: 0.025, name: '英國' },
  'ca': { min: 0.01, max: 0.05, avg: 0.025, name: '加拿大' },
  'au': { min: 0.01, max: 0.05, avg: 0.025, name: '澳洲' },
  'jp': { min: 0.008, max: 0.04, avg: 0.02, name: '日本' },
  'de': { min: 0.01, max: 0.05, avg: 0.025, name: '德國' },
  'fr': { min: 0.01, max: 0.05, avg: 0.025, name: '法國' },
  'other': { min: 0.005, max: 0.03, avg: 0.015, name: '其他地區' }
};

/**
 * 預估收入
 * @param {number} views - 觀看次數
 * @param {string} region - 地區代碼
 * @param {string} use - 使用哪個 RPM 值（min, max, avg）
 * @returns {number} 預估收入
 */
function estimateRevenue(views, region = 'tw', use = 'avg') {
  if (!RPM_DATA[region]) {
    region = 'tw';
  }

  const rpm = RPM_DATA[region][use];
  const revenue = (views / 1000) * rpm;

  return revenue;
}

/**
 * 預估收入範圍
 * @param {number} views - 觀看次數
 * @param {string} region - 地區代碼
 * @returns {object} 包含最小、平均、最大收入
 */
function estimateRevenueRange(views, region = 'tw') {
  if (!RPM_DATA[region]) {
    region = 'tw';
  }

  const regionData = RPM_DATA[region];
  const minRevenue = (views / 1000) * regionData.min;
  const avgRevenue = (views / 1000) * regionData.avg;
  const maxRevenue = (views / 1000) * regionData.max;

  return {
    min: minRevenue,
    avg: avgRevenue,
    max: maxRevenue
  };
}

/**
 * 批量預估多個視頻
 * @param {array} videos - 視頻列表
 * @returns {array} 預估結果列表
 */
function batchEstimate(videos) {
  return videos.map(video => {
    const views = video.views || 0;
    const region = video.region || 'tw';

    const { min: minRevenue, avg: avgRevenue, max: maxRevenue } = estimateRevenueRange(views, region);

    return {
      views,
      region,
      regionName: RPM_DATA[region].name,
      minRevenue,
      avgRevenue,
      maxRevenue
    };
  });
}

/**
 * 使用 YouTube API 獲取頻道收入預估
 * @param {string} channelId - 頻道 ID
 * @param {number} periodDays - 統計週期（天數）
 * @returns {number} 總收入預估
 */
async function getChannelRevenue(channelId, periodDays = 30) {
  const apiKey = process.env.YOUTUBE_API_KEY;

  if (!apiKey) {
    console.error('錯誤: 請設定 YOUTUBE_API_KEY 環境變數');
    return null;
  }

  const baseUrl = 'https://www.googleapis.com/youtube/v3';

  try {
    // 獲取頻道的視頻列表
    const searchUrl = `${baseUrl}/search`;
    const searchParams = {
      key: apiKey,
      channelId,
      part: 'snippet',
      maxResults: 50,
      order: 'date',
      type: 'video'
    };

    const searchResponse = await axios.get(searchUrl, { params: searchParams });

    if (!searchResponse.data.items) {
      console.error('錯誤: 無法找到頻道視頻');
      return null;
    }

    const videoIds = searchResponse.data.items.map(item => item.id.videoId);

    // 獲取視頻統計數據
    const videosUrl = `${baseUrl}/videos`;
    const videosParams = {
      key: apiKey,
      id: videoIds.join(','),
      part: 'statistics'
    };

    const videosResponse = await axios.get(videosUrl, { params: videosParams });

    let totalViews = 0;
    if (videosResponse.data.items) {
      totalViews = videosResponse.data.items.reduce((sum, video) => {
        return sum + parseInt(video.statistics.viewCount || 0);
      }, 0);
    }

    // 使用平均 RPM 預估收入（假設為台灣）
    const totalRevenue = (totalViews / 1000) * RPM_DATA.tw.avg;

    return totalRevenue;

  } catch (error) {
    console.error(`API 請求失敗: ${error.message}`);
    return null;
  }
}

/**
 * 顯示幫助資訊
 */
function showHelp() {
  console.log('使用方法: node estimate.js [選項]\n');
  console.log('選項:');
  console.log('  --views <數字>         觀看次數');
  console.log('  --region <代碼>        地區代碼（us, tw, uk, ca, au, jp, de, fr, other）');
  console.log('  --channel <頻道ID>      頻道 ID（需要 YOUTUBE_API_KEY）');
  console.log('  --period <天數>          統計週期（預設 30）');
  console.log('  --batch <JSON>          批量預估（JSON 格式）\n');
  console.log('範例:');
  console.log('  node estimate.js --views 100000 --region tw');
  console.log('  node estimate.js --views 1000000 --region us');
  console.log('  node estimate.js --channel UCXXXXXXXXXXXXX --period 30');
  console.log('  node estimate.js --batch \'[{"views":50000,"region":"tw"},{"views":100000,"region":"us"}]\'');
}

/**
 * 主函數
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    showHelp();
    process.exit(1);
  }

  let views = null;
  let region = 'tw';
  let channelId = null;
  let periodDays = 30;
  let batchData = null;

  // 解析參數
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--views' && i + 1 < args.length) {
      views = parseInt(args[i + 1]);
      i++;
    } else if (arg === '--region' && i + 1 < args.length) {
      region = args[i + 1].toLowerCase();
      i++;
    } else if (arg === '--channel' && i + 1 < args.length) {
      channelId = args[i + 1];
      i++;
    } else if (arg === '--period' && i + 1 < args.length) {
      periodDays = parseInt(args[i + 1]);
      i++;
    } else if (arg === '--batch' && i + 1 < args.length) {
      try {
        batchData = JSON.parse(args[i + 1]);
      } catch (error) {
        console.error('錯誤: JSON 解析失敗');
        process.exit(1);
      }
      i++;
    }
  }

  // 執行預估
  if (batchData) {
    // 批量預估
    console.log(`\n批量預估 ${batchData.length} 個視頻:`);
    console.log('='.repeat(80));

    const results = batchEstimate(batchData);

    let totalMin = 0;
    let totalAvg = 0;
    let totalMax = 0;

    results.forEach(result => {
      console.log(`\n${result.views.toLocaleString()} 觀看 (${result.regionName})`);
      console.log(`  最小收入: $${result.minRevenue.toFixed(2)}`);
      console.log(`  平均收入: $${result.avgRevenue.toFixed(2)}`);
      console.log(`  最大收入: $${result.maxRevenue.toFixed(2)}`);

      totalMin += result.minRevenue;
      totalAvg += result.avgRevenue;
      totalMax += result.maxRevenue;
    });

    console.log('\n' + '='.repeat(80));
    console.log('總計:');
    console.log(`  最小收入: $${totalMin.toFixed(2)}`);
    console.log(`  平均收入: $${totalAvg.toFixed(2)}`);
    console.log(`  最大收入: $${totalMax.toFixed(2)}`);

  } else if (channelId) {
    // 頻道預估
    console.log(`\n獲取頻道 ${channelId} 的收入預估（過去 ${periodDays} 天）`);
    console.log('='.repeat(80));

    const totalRevenue = await getChannelRevenue(channelId, periodDays);

    if (totalRevenue !== null) {
      console.log(`預估總收入: $${totalRevenue.toFixed(2)}`);
    } else {
      console.log('無法獲取頻道收入預估');
    }

  } else if (views) {
    // 單一視頻預估
    const { min: minRev, avg: avgRev, max: maxRev } = estimateRevenueRange(views, region);

    console.log('\nYouTube Shorts 收入預估:');
    console.log('='.repeat(80));
    console.log(`觀看次數: ${views.toLocaleString()}`);
    console.log(`地區: ${RPM_DATA[region].name} (${region})`);
    console.log(`RPM 範圍: $${RPM_DATA[region].min.toFixed(3)} - $${RPM_DATA[region].max.toFixed(3)}`);
    console.log('\n預估收入:');
    console.log(`  最小收入: $${minRev.toFixed(2)}`);
    console.log(`  平均收入: $${avgRev.toFixed(2)}`);
    console.log(`  最大收入: $${maxRev.toFixed(2)}`);
    console.log('\n說明: 實際收入可能因觀眾年齡、內容類型等因素而有所不同');

  } else {
    console.error('錯誤: 請指定 --views 或 --channel');
    process.exit(1);
  }
}

main().catch(error => {
  console.error('未預期的錯誤:', error);
  process.exit(1);
});

// 導出函數供其他模組使用
module.exports = {
  estimateRevenue,
  estimateRevenueRange,
  batchEstimate,
  getChannelRevenue
};
