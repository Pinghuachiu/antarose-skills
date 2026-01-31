-- Social Content Writer - Database Setup
-- 資料庫設置腳本

-- 內容歷史表
CREATE TABLE IF NOT EXISTS content_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(255) NOT NULL COMMENT '內容主題',
    platform VARCHAR(50) NOT NULL COMMENT '發布平台',
    hook TEXT COMMENT '勾子',
    content TEXT NOT NULL COMMENT '完整內容',
    hashtags JSON COMMENT '標籤列表',
    metadata JSON COMMENT '元數據（框架、語調等）',
    status ENUM('draft', 'published', 'scheduled') DEFAULT 'draft' COMMENT '狀態',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '創建時間',
    published_at TIMESTAMP NULL COMMENT '發布時間',
    INDEX idx_topic (topic),
    INDEX idx_platform (platform),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='內容歷史記錄表';

-- 平台規則快取表
CREATE TABLE IF NOT EXISTS platform_rules_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    platform VARCHAR(50) NOT NULL UNIQUE COMMENT '平台名稱',
    rules JSON NOT NULL COMMENT '平台規則（JSON格式）',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新時間',
    INDEX idx_platform (platform)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='平台規則快取表';

-- 勾子模板庫
CREATE TABLE IF NOT EXISTS hook_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hook_type VARCHAR(50) NOT NULL COMMENT '勾子類型',
    template TEXT NOT NULL COMMENT '模板文字',
    example TEXT COMMENT '範例',
    effectiveness_score DECIMAL(3,2) DEFAULT 0.70 COMMENT '效果分數',
    tags JSON COMMENT '標籤',
    language VARCHAR(10) DEFAULT 'zh-TW' COMMENT '語言',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '創建時間',
    INDEX idx_hook_type (hook_type),
    INDEX idx_effectiveness (effectiveness_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='勾子模板庫';

-- 資料收集記錄
CREATE TABLE IF NOT EXISTS research_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(255) NOT NULL COMMENT '研究主題',
    source_url TEXT COMMENT '來源 URL',
    source_type VARCHAR(50) COMMENT '來源類型（web_search, youtube, database）',
    content TEXT COMMENT '內容摘要',
    quality_score DECIMAL(3,2) COMMENT '質量分數',
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '收集時間',
    INDEX idx_topic (topic),
    INDEX idx_source_type (source_type),
    INDEX idx_quality_score (quality_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='資料收集記錄表';

-- 發布記錄表
CREATE TABLE IF NOT EXISTS publish_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content_id INT COMMENT '內容 ID（關聯 content_history）',
    platform VARCHAR(50) NOT NULL COMMENT '平台',
    post_id VARCHAR(255) COMMENT '平台貼文 ID',
    status ENUM('success', 'failed', 'pending') DEFAULT 'pending' COMMENT '發布狀態',
    error_message TEXT COMMENT '錯誤訊息',
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '發布時間',
    FOREIGN KEY (content_id) REFERENCES content_history(id) ON DELETE SET NULL,
    INDEX idx_platform (platform),
    INDEX idx_status (status),
    INDEX idx_published_at (published_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='發布記錄表';

-- 提示詞生成記錄
CREATE TABLE IF NOT EXISTS prompt_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content_id INT COMMENT '內容 ID',
    prompt_type ENUM('image', 'video', 'thumbnail') NOT NULL COMMENT '提示詞類型',
    prompts JSON NOT NULL COMMENT '生成的提示詞',
    generated_images JSON COMMENT '生成的圖片路徑',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '生成時間',
    FOREIGN KEY (content_id) REFERENCES content_history(id) ON DELETE SET NULL,
    INDEX idx_content_id (content_id),
    INDEX idx_prompt_type (prompt_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='提示詞生成記錄表';

-- 內容分析記錄
CREATE TABLE IF NOT EXISTS analysis_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content_id INT COMMENT '內容 ID',
    platform VARCHAR(50) NOT NULL COMMENT '平台',
    overall_score DECIMAL(5,2) COMMENT '總體分數',
    metrics JSON COMMENT '詳細指標',
    suggestions JSON COMMENT '改進建議',
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '分析時間',
    FOREIGN KEY (content_id) REFERENCES content_history(id) ON DELETE SET NULL,
    INDEX idx_content_id (content_id),
    INDEX idx_overall_score (overall_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='內容分析記錄表';

-- 插入預設平台規則
INSERT INTO platform_rules_cache (platform, rules) VALUES
('facebook', JSON_OBJECT(
    'max_length', 60000,
    'optimal_length', 500,
    'max_hashtags', 5,
    'optimal_hashtags', 3,
    'supports_markdown', true,
    'supports_emojis', true,
    'content_type', 'long_form'
)),
('instagram', JSON_OBJECT(
    'max_length', 2200,
    'optimal_length', 150,
    'max_hashtags', 30,
    'optimal_hashtags', 20,
    'supports_markdown', false,
    'supports_emojis', true,
    'content_type', 'visual_first'
)),
('threads', JSON_OBJECT(
    'max_length', 500,
    'optimal_length', 150,
    'max_hashtags', 5,
    'optimal_hashtags', 3,
    'supports_markdown', false,
    'supports_emojis', true,
    'content_type', 'short_form'
)),
('linkedin', JSON_OBJECT(
    'max_length', 3000,
    'optimal_length', 1200,
    'max_hashtags', 5,
    'optimal_hashtags', 3,
    'supports_markdown', true,
    'supports_emojis', false,
    'content_type', 'professional'
))
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- 插入預設勾子模板
INSERT INTO hook_templates (hook_type, template, example, effectiveness_score, tags) VALUES
('question', '你是否曾經{pain_point}？', '你是否曾經發文後無人問津？', 0.85, JSON_ARRAY('engagement', 'relatable')),
('question', '你是否想知道{curiosity}？', '你是否想知道AI如何改變內容創作？', 0.82, JSON_ARRAY('curiosity', 'educational')),
('story', '當我{experience}時，我發現了{insight}', '當我嘗試100種方法後，我發現了秘密', 0.90, JSON_ARRAY('storytelling', 'personal')),
('story', '從{starting_point}到{achievement}，我的旅程', '從0粉絲到10萬粉絲，我的旅程', 0.88, JSON_ARRAY('inspiration', 'journey')),
('number', '{number}種{topic}方法', '5種讓內容爆火的方法', 0.82, JSON_ARRAY('listicle', 'practical')),
('number', '{number}個{benefit}技巧', '7個提升互動率的技巧', 0.80, JSON_ARRAY('tips', 'actionable')),
('curiosity', '為什麼{phenomenon}？真相是{truth}', '為什麼有些內容總能病毒傳播？真相是其實有科學依據', 0.88, JSON_ARRAY('curiosity', 'reveal')),
('curiosity', '秘密揭曉：{secret}', '秘密揭曉：內容創作的終極秘密', 0.85, JSON_ARRAY('secret', 'exclusive')),
('controversial', '我敢說：{controversial_statement}', '我敢說：SEO已死，內容才是王道', 0.75, JSON_ARRAY('controversial', 'opinion')),
('controversial', '{common_belief}已死，{new_method}才是王道', '社交媒體自動化已死，真實互動才是王道', 0.78, JSON_ARRAY('contrarian', 'trend'))
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- 創建視圖：內容統計
CREATE OR REPLACE VIEW content_stats AS
SELECT
    DATE(created_at) as date,
    platform,
    COUNT(*) as total_content,
    SUM(CASE WHEN status = 'published' THEN 1 ELSE 0 END) as published_count,
    SUM(CASE WHEN status = 'draft' THEN 1 ELSE 0 END) as draft_count,
    AVG(CHAR_LENGTH(content)) as avg_content_length
FROM content_history
GROUP BY DATE(created_at), platform;

-- 創建視圖：發布成功率
CREATE OR REPLACE VIEW publish_success_rate AS
SELECT
    platform,
    COUNT(*) as total_attempts,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count,
    ROUND(SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as success_rate
FROM publish_records
WHERE published_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY platform;
