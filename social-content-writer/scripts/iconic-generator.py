#!/usr/bin/env python3
"""
Social Content Writer - Iconic Image Prompt Generator
標誌性圖片提示詞生成器（能識別和使用標誌性元素）
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List
import subprocess


# 標誌性元素識別模板
ICONIC_PATTERNS = {
    "moltbot": {
        "iconic_elements": {
            "primary_logo": {
                "name": "龍蝦（Lobster）",
                "description": "紅色卡通龍蝦，Moltbot 吉祥物",
                "visual_keywords": ["lobster", "crab", "red cartoon lobster", "cute mascot crab", "anime crab", "chibi lobster"],
                "color": "red"
            },
            "interface": {
                "name": "Chat 介面",
                "description": "WhatsApp/Telegram 聊天視窗",
                "visual_keywords": ["WhatsApp chat", "Telegram chat", "messaging app", "phone screen", "chat bubble", "conversation", "message interface"]
            },
            "platforms": {
                "name": "整合平台",
                "description": "Gmail、Calendar、Slack、GitHub 等整合",
                "visual_keywords": ["Gmail", "Google Calendar", "Slack", "GitHub", "Google Drive", "app icons", "platform integration"]
            },
            "concept": {
                "name": "24/7 工作",
                "description": "在你睡覺時幫你工作",
                "visual_keywords": ["sleeping person", "night work", "moon", "stars", "while you sleep", "overnight", "24/7"]
            }
        },
        "tagline": "AI助理在你睡覺時幫你工作"
    },
    "chatgpt": {
        "iconic_elements": {
            "primary_logo": {
                "name": "OpenAI Logo",
                "description": "OpenAI 的六角形 Logo",
                "visual_keywords": ["hexagon shape", "OpenAI logo", "orange spiral", "AI logo", "tech logo"]
            },
            "interface": {
                "name": "Chat 介面",
                "description": "ChatGPT 對話視窗",
                "visual_keywords": ["chat window", "typing interface", "conversation", "AI assistant", "text input"]
            },
            "concept": {
                "name": "AI 對話",
                "description": "AI 與人類對話",
                "visual_keywords": ["chatbot", "AI conversation", "asking questions", "AI helper"]
            }
        },
        "tagline": "ChatGPT：對話式 AI 先驅"
    },
    "github_copilot": {
        "iconic_elements": {
            "primary_logo": {
                "name": "GitHub Copilot Logo",
                "description": "GitHub Copilot 的六角形 Logo",
                "visual_keywords": ["GitHub Copilot logo", "hexagon", "spiral patterns", "AI coding assistant"]
            },
            "interface": {
                "name": "程式碼編輯器",
                "description": "IDE 程式碼編輯器視窗",
                "visual_keywords": ["code editor", "IDE", "typing code", "syntax highlighting", "code completion"]
            },
            "concept": {
                "name": "AI 編碼助手",
                "description": "AI 輔助程式設計",
                "visual_keywords": ["coding", "programming", "developer", "writing code", "autocomplete"]
            }
        },
        "tagline": "GitHub Copilot：AI 編碼夥伴"
    }
}


# 中二風格關鍵詞庫
CHUUNIBYOU_STYLES = {
    "visual_effects": [
        "glowing aura", "particle effects", "energy waves", "mystical symbols",
        "chromatic aberration", "lens flares", "bloom effect", "neon lights",
        "ethereal glow", "magical circles", "runes", "crystal shards"
    ],
    "atmosphere": [
        "apocalyptic", "cyberpunk", "steampunk", "dystopian", "futuristic",
        "mystical", "ethereal", "otherworldly", "dimensional", "transcendent"
    ],
    "color_schemes": [
        "neon blue and magenta", "crimson and obsidian", "electric purple",
        "golden and silver", "rainbow holographic", "bioluminescent green"
    ],
    "composition": [
        "dramatic low angle", "bird's eye view", "extreme close-up",
        "split screen", "multiple exposures", "double exposure"
    ]
}


class IconicPromptGenerator:
    """標誌性圖片提示詞生成器"""

    def __init__(self):
        self.patterns = ICONIC_PATTERNS
        self.chuunibyou_styles = CHUUNIBYOU_STYLES

    def analyze_from_article(self, article_content: str, article_title: str = "") -> Dict:
        """從文章內容中分析標誌性元素"""
        print("\n📖 從文章內容分析標誌性元素...")

        # 組合分析文本
        text_to_analyze = f"{article_title} {article_content}".lower()

        iconic_elements = {}

        # 1. 識別吉祥物/角色
        mascot_keywords = {
            "龍蝦": "lobster", "螃蟹": "crab", "熊": "bear", "貓": "cat",
            "鳥": "bird", "狗": "dog", "狐狸": "fox", "兔子": "rabbit",
            "dragon": "dragon", "phoenix": "phoenix", "robot": "robot",
            "lobster": "lobster", "crab": "crab", "mascot": "mascot",
            "吉祥物": "mascot", "角色": "character"
        }
        for zh, en in mascot_keywords.items():
            if zh in text_to_analyze or en in text_to_analyze:
                iconic_elements["primary_logo"] = {
                    "name": zh if zh in text_to_analyze else en,
                    "description": f"文章中提到的{zh}角色/吉祥物",
                    "visual_keywords": [en, f"cute {en}", f"anime {en}", f"chibi {en}", f"{en} mascot"]
                }
                print(f"   ✅ 識別出吉祥物: {zh}")
                break

        # 2. 識別界面/平台
        interface_keywords = {
            "WhatsApp": "WhatsApp chat interface",
            "Telegram": "Telegram chat interface",
            "聊天": "chat interface",
            "對話": "conversation interface",
            "訊息": "messaging app",
            "chat": "chat window",
            "AI助理": "AI assistant interface"
        }
        for keyword, desc in interface_keywords.items():
            if keyword in text_to_analyze:
                iconic_elements["interface"] = {
                    "name": keyword,
                    "description": desc,
                    "visual_keywords": [desc, "phone screen", "chat bubbles", "conversation"]
                }
                print(f"   ✅ 識別出界面: {keyword}")
                break

        # 3. 識別平台/工具
        platform_keywords = ["Gmail", "Google Calendar", "Slack", "GitHub", "Notion", "Excel"]
        found_platforms = [p for p in platform_keywords if p in article_content]
        if found_platforms:
            iconic_elements["platforms"] = {
                "name": "平台整合",
                "description": f"整合 {', '.join(found_platforms[:3])}",
                "visual_keywords": found_platforms + ["app icons", "platform integration", "workflow"]
            }
            print(f"   ✅ 識別出平台: {', '.join(found_platforms)}")

        # 4. 識別核心概念/價值
        concept_keywords = {
            "24/7": "全天候工作",
            "睡覺": "自動化工作",
            "省時間": "效率提升",
            "免費": "零成本",
            "開源": "open source",
            "AI": "artificial intelligence",
            "自動化": "automation"
        }
        for keyword, concept in concept_keywords.items():
            if keyword in text_to_analyze:
                iconic_elements["concept"] = {
                    "name": concept,
                    "description": f"文章核心概念：{concept}",
                    "visual_keywords": [concept, keyword, "innovation", "technology", "future"]
                }
                print(f"   ✅ 識別出概念: {concept}")
                break

        # 5. 如果沒有找到足夠元素，生成通用元素
        if len(iconic_elements) < 2:
            print("   🔧 生成通用標誌性元素")
            if "primary_logo" not in iconic_elements:
                iconic_elements["primary_logo"] = {
                    "name": article_title[:20] if article_title else "主題Logo",
                    "description": "文章主題的標誌性符號",
                    "visual_keywords": ["logo", "icon", "symbol", "tech logo", "modern design"]
                }
            if "concept" not in iconic_elements:
                iconic_elements["concept"] = {
                    "name": "核心價值",
                    "description": "文章傳達的核心價值",
                    "visual_keywords": ["innovation", "solution", "technology", "future", "automation"]
                }

        # 提取文章標語（第一句話或標題）
        tagline = article_title if article_title else article_content.split('\n')[0][:50]
        if len(tagline) > 50:
            tagline = tagline[:47] + "..."

        return {
            "topic": article_title[:50] if article_title else "文章主題",
            "iconic_elements": iconic_elements,
            "tagline": tagline,
            "match_type": "article_analysis"
        }

    def generate_chuunibyou_prompts(self, iconic_data: Dict, mode: str = "text_to_image") -> List[Dict]:
        """生成中二風格的標誌性圖片提示詞"""
        print(f"\n🔥 生成中二風格提示詞（{mode}）...")

        elements = iconic_data["iconic_elements"]
        prompts = []
        tagline = iconic_data.get("tagline", "")

        # 中二風格模板
        chuunibyou_templates = {
            "logo_showcase": {
                "style_prefix": "Epic legendary",
                "enhancements": "surrounded by glowing magical runes, particle effects emanating outward, divine aura",
                "lighting": "dramatic rim lighting, volumetric god rays, chromatic aberration",
                "background": "apocalyptic battlefield or celestial realm background"
            },
            "usage_demo": {
                "style_prefix": "Cinematic action movie",
                "enhancements": "screen holographically projected, data streams visible in air, matrix-like code rain",
                "lighting": "neon cyberpunk lighting, bioluminescent glow, electric sparks",
                "background": "futuristic cityscape or digital dimension"
            },
            "platform_integration": {
                "style_prefix": "Advanced technological singularity",
                "enhancements": "energy connections between platforms, glowing data streams, holographic interfaces",
                "lighting": "cold blue tech lighting, purple neon accents, lens flares",
                "background": "clean white space with floating particles, ethereal"
            },
            "concept_art": {
                "style_prefix": "Transcendent conceptual masterpiece",
                "enhancements": "reality breaking apart, dimensional portal opening, mystical energy swirling",
                "lighting": "divine golden light, ethereal glow, bloom effects",
                "background": "cosmic space with nebulae, otherworldly dimension"
            }
        }

        prompt_order = 1
        for elem_type, elem_data in elements.items():
            if prompt_order > 4:
                break

            # 確定場景類型
            if elem_type == "primary_logo":
                scenario_type = "logo_showcase"
                style_name = "Epic Anime"
            elif elem_type == "interface":
                scenario_type = "usage_demo"
                style_name = "Cyberpunk Cinematic"
            elif elem_type == "platforms":
                scenario_type = "platform_integration"
                style_name = "Tech Singularity"
            else:  # concept
                scenario_type = "concept_art"
                style_name = "Transcendent Art"

            template = chuunibyou_templates[scenario_type]
            keywords = elem_data.get("visual_keywords", elem_data.get("name", ""))

            # 生成中二風格英文提示詞
            main_prompt = self._build_chuunibyou_prompt(
                elem_data, template, tagline, mode
            )

            # 生成中文提示詞
            chinese_prompt = self._build_chuunibyou_prompt_chinese(
                elem_data, template, tagline, mode
            )

            # 圖生圖特殊處理
            if mode == "image_to_image":
                main_prompt = f"Transform this image into: {main_prompt}"
                chinese_prompt = f"將此圖片轉換為：{chinese_prompt}"

            prompts.append({
                "order": prompt_order,
                "scenario_type": scenario_type,
                "name": f"{elem_data['name']} - 中二風格",
                "description": elem_data.get("description", ""),
                "main_prompt": main_prompt,
                "chinese_prompt": chinese_prompt,
                "style": style_name,
                "aspect_ratio": "16:9" if scenario_type in ["platform_integration", "concept_art"] else "1:1",
                "purpose": "酷炫展示",
                "visual_keywords": elem_data.get("visual_keywords", []),
                "mode": mode,
                "suggested_platforms": ["instagram", "threads", "twitter"]
            })

            prompt_order += 1

        return prompts

    def _build_chuunibyou_prompt(self, elem_data: Dict, template: Dict, tagline: str, mode: str) -> str:
        """構建中二風格英文提示詞"""
        name = elem_data.get("name", "")
        keywords = elem_data.get("visual_keywords", [])

        # 基礎描述
        base = f"{template['style_prefix']} {name}"

        # 添加關鍵詞
        if isinstance(keywords, list) and keywords:
            base += f", {keywords[0]}"
            if len(keywords) > 1:
                base += f", {keywords[1]}"

        # 添加中二特效
        prompt = f"""{base},
{template['enhancements']},
{template['lighting']},
{template['background']},
masterpiece, ultra detailed, 8k resolution, trending on artstation,
digital art, concept art, character design, vibrant colors,
dramatic composition, professional artwork, {tagline}"""

        return prompt

    def _build_chuunibyou_prompt_chinese(self, elem_data: Dict, template: Dict, tagline: str, mode: str) -> str:
        """構建中二風格中文提示詞"""
        name = elem_data.get("name", "")
        description = elem_data.get("description", "")

        # 中二風格中文轉換
        style_map = {
            "Epic legendary": "史詩傳說級",
            "Cinematic action movie": "電影級動作場景",
            "Advanced technological singularity": "先進科技奇點",
            "Transcendent conceptual masterpiece": "超凡概念傑作"
        }

        style_prefix_cn = style_map.get(template["style_prefix"], "超酷炫風格")

        prompt = f"""{style_prefix_cn} {name}，
{description}，
史詩級光效，粒子特效，神聖光環，
戲劇性構圖，極致細節，8K 解析度，
數位藝術，概念藝術，角色設計，鮮豔色彩，
專業級作品，{tagline}"""

        return prompt

    def identify_iconic_elements(self, topic: str, research_data: Dict = None) -> Dict:
        """識別主題的標誌性元素"""
        print("\n🔍 識別標誌性元素中...")

        topic_lower = topic.lower()

        # 檢查是否為已知主題
        for pattern_key, pattern_data in self.patterns.items():
            if pattern_key in topic_lower:
                print(f"   ✅ 識別出已知主題: {pattern_key}")
                return {
                    "topic": pattern_key,
                    "iconic_elements": pattern_data["iconic_elements"],
                    "tagline": pattern_data["tagline"],
                    "match_type": "known"
                }

        # 如果是未知主題，分析研究資料
        if research_data:
            return self._extract_from_research(topic, research_data)

        # 都沒有，生成通用標誌性元素
        return self._generate_generic_iconic_elements(topic)

    def _extract_from_research(self, topic: str, research_data: Dict) -> Dict:
        """從研究資料中提取標誌性元素"""
        print("   🔎 從研究資料分析...")

        all_text = " ".join([item.get("summary", "") for item in research_data.get("data", [])])

        # 分析可能的標誌性元素
        possible_elements = {}

        # 檢查是否提到動物/吉祥物
        animals = ["龍蝦", "螃蟹", "lobster", "crab", "熊", "貓", "鳥"]
        found_animals = [a for a in animals if a in all_text]
        if found_animals:
            possible_elements["mascot"] = found_animals[0]

        # 檢查是否提到界面
        interfaces = ["WhatsApp", "Telegram", "chat", "對話", "訊息"]
        found_interfaces = [i for i in interfaces if i in all_text]
        if found_interfaces:
            possible_elements["interface"] = found_interfaces[0]

        return {
            "topic": topic,
            "iconic_elements": possible_elements,
            "tagline": f"關於{topic}",
            "match_type": "research_based"
        }

    def _generate_generic_iconic_elements(self, topic: str) -> Dict:
        """生成通用標誌性元素"""
        print("   🔧 生成通用標誌性元素")

        return {
            "topic": topic,
            "iconic_elements": {
                "primary_logo": {
                    "name": "抽象 Logo",
                    "description": f"{topic} 的標誌性符號",
                    "visual_keywords": [topic, "logo", "icon", "symbol"]
                },
                "interface": {
                    "name": "使用介面",
                    "description": f"{topic} 的使用方式",
                    "visual_keywords": ["interface", "app", "screen", "usage", "workflow"]
                },
                "concept": {
                    "name": "核心概念",
                    "description": f"{topic} 的核心價值",
                    "visual_keywords": [topic, "automation", "AI", "tool", "solution"]
                }
            },
            "tagline": f"關於{topic}",
            "match_type": "generic"
        }

    def generate_iconic_scenarios(self, iconic_data: Dict, num_prompts: int = 4) -> List[Dict]:
        """基於標誌性元素生成場景提示詞"""
        print(f"\n🎨 生成 {num_prompts} 種標誌性場景...")

        scenarios = []
        elements = iconic_data["iconic_elements"]

        # 場景 1: Logo 展示（最標誌性）
        if "primary_logo" in elements:
            logo = elements["primary_logo"]
            scenarios.append({
                "scenario_type": "logo_showcase",
                "name": f"{logo['name']} - Logo 展示",
                "description": f"{logo['description']}",
                "visual_keywords": logo["visual_keywords"],
                "style": "mascot" if "mascot" in logo.get("visual_keywords", "") else "logo",
                "purpose": "品牌識別",
                "suggested_platforms": ["instagram", "threads"]
            })

        # 場景 2: 使用介面（展示怎麼用）
        if "interface" in elements:
            interface = elements["interface"]
            scenarios.append({
                "scenario_type": "usage_demo",
                "name": f"{interface['name']} - 使用展示",
                "description": f"{interface['description']}",
                "visual_keywords": interface["visual_keywords"],
                "style": "lifestyle",
                "purpose": "教學示範",
                "suggested_platforms": ["instagram", "facebook"]
            })

        # 場景 3: 平台整合（展示功能）
        if "platforms" in elements:
            platforms = elements["platforms"]
            scenarios.append({
                "scenario_type": "platform_integration",
                "name": f"{platforms['name']} - 整合展示",
                "description": f"{platforms['description']}",
                "visual_keywords": platforms["visual_keywords"],
                "style": "infographic",
                "purpose": "能力展示",
                "suggested_platforms": ["linkedin", "facebook"]
            })

        # 場景 4: 概念圖（核心價值）
        if "concept" in elements:
            concept = elements["concept"]
            scenarios.append({
                "scenario_type": "concept_art",
                "name": f"{concept['name']} - 概念圖",
                "description": f"{concept['description']}",
                "visual_keywords": concept["visual_keywords"],
                "style": "conceptual",
                "purpose": "價值傳達",
                "suggested_platforms": ["facebook", "linkedin"]
            })

        # 為每個場景生成提示詞
        prompts = []
        for i, scenario in enumerate(scenarios[:num_prompts]):
            prompt = self._generate_scenario_prompt(scenario, iconic_data)

            # 推斷最佳寬高比
            if scenario["scenario_type"] == "logo_showcase":
                aspect_ratios = ["1:1", "4:5"]
            elif scenario["scenario_type"] == "usage_demo":
                aspect_ratios = ["9:16", "16:9"]
            elif scenario["scenario_type"] == "platform_integration":
                aspect_ratios = ["16:9"]
            else:  # concept_art
                aspect_ratios = ["16:9", "1:1"]

            prompts.append({
                "order": i + 1,
                "scenario_type": scenario["scenario_type"],
                "name": scenario["name"],
                "description": scenario["description"],
                "main_prompt": prompt["main"],
                "chinese_prompt": prompt["chinese"],
                "style": scenario["style"],
                "aspect_ratio": aspect_ratios[0],
                "purpose": scenario["purpose"],
                "visual_keywords": scenario["visual_keywords"],
                "suggested_platforms": scenario["suggested_platforms"]
            })

        return prompts

    def _generate_scenario_prompt(self, scenario: Dict, iconic_data: Dict) -> Dict:
        """為特定場景生成提示詞"""

        scenario_type = scenario["scenario_type"]

        if scenario_type == "logo_showcase":
            return self._generate_logo_prompt(scenario, iconic_data)

        elif scenario_type == "usage_demo":
            return self._generate_usage_prompt(scenario, iconic_data)

        elif scenario_type == "platform_integration":
            return self._generate_integration_prompt(scenario, iconic_data)

        else:  # concept_art
            return self._generate_concept_prompt(scenario, iconic_data)

    def _generate_logo_prompt(self, scenario: Dict, iconic_data: Dict) -> Dict:
        """生成 Logo 展示提示詞"""

        logo = scenario["visual_keywords"]
        tagline = iconic_data.get("tagline", "")

        # 檢查是否為龍蝦
        if "lobster" in " ".join(logo) or "crab" in " ".join(logo):
            # Moltbot 特殊處理
            main = f"""A cute red cartoon lobster character serving as an AI assistant mascot,
sitting in front of a computer screen, typing and organizing digital tasks,
friendly expression, red shell, big eyes, wearing a small name tag "Moltbot",
modern tech background, soft lighting, professional yet approachable style,
high quality, 4k, vibrant colors, character design, mascot style,
{tagline}"""

            chinese = f"""可愛的紅色卡通龍蝦角色，作為 AI 助理吉祥物，坐在電腦螢幕前打字和處理數位任務，
友好的表情，紅色外殼，大眼睛，戴著小名牌「Moltbot」，
現代科技背景，柔和光線，專業但親切風格，高品質，4K，鮮豔色彩，角色設計，吉祥物風格，
{tagline}"""

        else:
            # 通用 Logo
            main = f"""Professional logo design for {iconic_data['topic']},
minimalist style, modern and clean design, recognizable symbol or icon,
vector graphics style, bold colors, flat design,
simple yet memorable, tech company aesthetic, white background,
4k resolution, sharp lines, professional branding"""

            chinese = f"""{iconic_data['topic']}的專業 Logo 設計，
極簡主義風格，現代簡潔設計，易識別符號或圖標，
向量圖形風格，大膽色彩，平面設計，
簡單但易記，科技公司美學，白色背景，
4K 解析度，清晰線條，專業品牌設計"""

        return {
            "main": main,
            "chinese": chinese
        }

    def _generate_usage_prompt(self, scenario: Dict, iconic_data: Dict) -> Dict:
        """生成使用場景提示詞"""

        tagline = iconic_data.get("tagline", "")
        topic = iconic_data["topic"]

        main = f"""Smartphone screen displaying chat interface with {topic},
visible message bubbles showing the AI assistant helping with tasks,
hand holding phone in casual setting, cozy atmosphere, realistic lifestyle photography,
warm lighting, authentic scenario, modern smartphone,
chat application interface with message history, clean and organized,
friendly and approachable vibe, people connecting with technology,
showing the practical value and ease of use, {tagline}"""

        chinese = f"""智慧型手機螢幕顯示與 {topic} 的聊天介面，
可見訊息氣泡顯示 AI 助理幫忙處理任務，
手拿手機，休閒設定，溫馨氛圍，寫實生活攝影風格，溫暖光線，真實場景，
現代智慧型手機，聊天應用程式介面，訊息歷史，乾淨且有組織，
友善且親近的氛圍，人與科技的連接，展示實用價值和易用性，
{tagline}"""

        return {
            "main": main,
            "chinese": chinese
        }

    def _generate_integration_prompt(self, scenario: Dict, iconic_data: Dict) -> Dict:
        """生成平台整合提示詞"""

        tagline = iconic_data.get("tagline", "")
        topic = iconic_data["topic"]

        main = f"""Central {topic} mascot or logo in the center,
connected with sleek animated arrows to app icons surrounding it: Gmail, Google Calendar, Slack, GitHub, Google Drive,
floating in clean white space, minimalist isometric style,
3D rendered app icons with authentic brand colors,
dashed lines showing data flow and automation,
tech diagram style, professional infographic or explainer video,
clean background, subtle gradient, centered composition,
visualizing how {topic} connects different platforms and tools,
{tagline}"""

        chinese = f"""中央 {topic} 吉祥物或 Logo 在中心，
用簡潔的動畫箭頭連接周圍的應用程式圖標：
Gmail、Google 日曆、Slack、GitHub、Google Drive，
漂浮在潔白的空間中，極簡主義等距風格，
3D 渲染的應用程式圖標，真實的品牌色彩，
虛線顯示數據流動和自動化流程，
科技圖表風格，專業信息圖或解釋影片，
潔淨背景，微妙漸層，中心構圖，
視覺化展示 {topic} 如何連接不同平台和工具，
{tagline}"""

        return {
            "main": main,
            "chinese": chinese
        }

    def _generate_concept_prompt(self, scenario: Dict, iconic_data: Dict) -> Dict:
        """生成概念圖提示詞"""

        tagline = iconic_data.get("tagline", "")
        topic = iconic_data["topic"]

        main = f"""Conceptual art representing {topic},
modern digital art style, futuristic and inspiring,
visualizing the core value and benefit metaphorically,
tech-forward aesthetic with glowing elements, clean composition,
symbolic representation of innovation and automation,
bold colors, dynamic composition, professional yet accessible,
4k resolution, digital art, concept illustration,
{tagline}"""

        chinese = f"""{topic} 的概念藝術，
現代數位藝術風格，未來主義且啟發，
以隱喻方式視覺化核心價值和好處，
科技前沿美學，發光元素，簡潔構圖，
創新和自動化的象徵性表現，
大膽色彩，動態構圖，專業且親近，
4K 解析度，數位藝術，概念插圖，
{tagline}"""

        return {
            "main": main,
            "chinese": chinese
        }

    def generate(self, topic: str, research_file: str = None, num_prompts: int = 4) -> Dict:
        """生成標誌性圖片提示詞"""

        print("\n" + "="*60)
        print("🖼️ 標誌性圖片提示詞生成器")
        print("="*60)

        # 識別標誌性元素
        if research_file and os.path.exists(research_file):
            with open(research_file, 'r', encoding='utf-8') as f:
                research_data = json.load(f)
            iconic_data = self.identify_iconic_elements(topic, research_data)
        else:
            iconic_data = self.identify_iconic_elements(topic)

        # 生成場景提示詞
        prompts = self.generate_iconic_scenarios(iconic_data, num_prompts)

        print(f"\n✅ 生成了 {len(prompts)} 個標誌性場景")

        return {
            "topic": topic,
            "iconic_data": iconic_data,
            "scenarios": prompts,
            "total_prompts": len(prompts)
        }

    def print_iconic_prompts(self, result: Dict):
        """打印標誌性提示詞"""
        print("\n" + "="*60)
        print(f"🖼️ {result['topic']} - 標誌性圖片提示詞")
        print("="*60)

        print(f"\n🏷️ 標誌性元素:")
        for elem_name, elem_data in result["iconic_data"]["iconic_elements"].items():
            print(f"   • {elem_data['name']}: {elem_data['description']}")

        print(f"\n📌 標語: {result['iconic_data']['tagline']}")

        print(f"\n🎨 場景提示詞:")

        for scenario in result["scenarios"]:
            print(f"\n  [{scenario['order']}] {scenario['name']}")
            print(f"     類型: {scenario['scenario_type']}")
            print(f"     目的: {scenario['purpose']}")
            print(f"     風格: {scenario['style']}")
            print(f"     建議平台: {', '.join(scenario['suggested_platforms'])}")
            print(f"     寬高比: {scenario['aspect_ratio']}")

            print(f"     📝 英文提示詞:")
            print(f"     {scenario['main_prompt'][:100]}...")

            print(f"     🇨🇳 中文提示詞:")
            print(f"     {scenario['chinese_prompt'][:100]}...")

        print("="*60 + "\n")

    def save_to_file(self, result: Dict, filepath: str):
        """保存到文件"""
        output = {
            "generated_at": datetime.now().isoformat(),
            **result
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ 標誌性提示詞已保存到: {filepath}")

    def validate_story_consistency(self, article_content: str, prompt: str,
                                  article_key_elements: List[str]) -> Dict:
        """
        驗證圖片提示詞是否與文章內容一致

        核心原則：圖片就是要用視覺來展現你文章的內容

        Args:
            article_content: 文章內容
            prompt: 圖片提示詞
            article_key_elements: 文章中的關鍵元素列表

        Returns:
            驗證結果字典
        """
        print("\n" + "="*60)
        print("🔍 故事一致性驗證")
        print("="*60)
        print()

        validation_result = {
            "is_consistent": True,
            "missing_elements": [],
            "suggestions": [],
            "score": 0.0
        }

        # 檢查每個關鍵元素是否在提示詞中
        prompt_lower = prompt.lower()

        print("📋 關鍵元素檢查:")
        print("-"*60)

        found_elements = []
        missing_elements = []

        for element in article_key_elements:
            element_lower = element.lower()
            # 檢查是否在提示詞中（簡單匹配）
            if any(keyword in prompt_lower for keyword in element_lower.split()):
                found_elements.append(element)
                print(f"  ✅ {element}")
            else:
                missing_elements.append(element)
                print(f"  ❌ {element} (遺漏)")

        # 計算一致性分數
        if len(article_key_elements) > 0:
            validation_result["score"] = len(found_elements) / len(article_key_elements)

        # 如果有遺漏，生成建議
        if missing_elements:
            validation_result["is_consistent"] = False
            validation_result["missing_elements"] = missing_elements

            print()
            print("⚠️  發現遺漏元素:")
            for element in missing_elements:
                print(f"  • {element}")

            print()
            print("💡 建議修正:")

            # 根據遺漏的元素生成具體建議
            suggestions = []

            if any("衛星" in e or "starlink" in e.lower() for e in missing_elements):
                suggestions.append("在提示詞中添加：'Starlink satellite visible in sky with golden connection beam to phone'")

            if any("連接" in e or "connect" in e.lower() for e in missing_elements):
                suggestions.append("在提示詞中添加：'golden connection beam extending from satellite to iPhone'")

            if any("吉祥物" in e or "mascot" in e.lower() or "龍蝦" in e or "lobster" in e.lower() for e in missing_elements):
                suggestions.append("在提示詞中添加：'cute lobster mascot icon visible on screen'")

            if any("訊息" in e or "message" in e.lower() or "對話" in e or "chat" in e.lower() for e in missing_elements):
                suggestions.append("在提示詞中添加：'chat interface visible with message bubble showing specific text'")

            if any("對比" in e or "before" in e.lower() or "after" in e.lower() for e in missing_elements):
                suggestions.append("在提示詞中添加：'split screen showing before and after comparison'")

            # 如果沒有具體建議，給出通用建議
            if not suggestions:
                for element in missing_elements:
                    suggestions.append(f"在提示詞中明確包含：'{element}' 的視覺描述")

            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")

            validation_result["suggestions"] = suggestions

        else:
            print()
            print("✅ 所有关鍵元素都在提示詞中！")

        print()
        print("="*60)
        print(f"📊 一致性分數: {validation_result['score']*100:.1f}%")
        print("="*60)

        # 核心原則提醒
        print()
        print("🎯 核心原則:")
        print("   圖片就是要用視覺來展現你文章的內容")
        print()
        print("✓ 不能只展示結果（山裡有網路）")
        print("✓ 要展示關鍵元素（Starlink 衛星）")
        print("✓ 要展示技術實現（衛星連接光束）")
        print("✓ 讓觀眾看出「這是怎麼做到的」")

        return validation_result

    def enhance_prompt_with_consistency(self, original_prompt: str,
                                       missing_elements: List[str]) -> str:
        """
        根据遺漏元素增強提示詞

        Args:
            original_prompt: 原始提示詞
            missing_elements: 遺漏的元素列表

        Returns:
            增強後的提示詞
        """
        enhanced = original_prompt
        additions = []

        for element in missing_elements:
            element_lower = element.lower()

            # 根據元素類型添加視覺描述
            if "衛星" in element or "starlink" in element_lower:
                additions.append(", clearly visible Starlink satellite in the sky above")

            elif "連接" in element or "connect" in element_lower:
                additions.append(", golden connection beam extending from satellite to device")

            elif "吉祥物" in element_lower or "mascot" in element_lower:
                additions.append(", cute mascot icon visible on screen")

            elif "訊息" in element or "message" in element_lower:
                additions.append(", message bubble with specific text visible on screen")

            elif "龍蝦" in element or "lobster" in element_lower:
                additions.append(", red lobster mascot character visible")

            elif "對比" in element_lower or "before" in element_lower or "after" in element_lower:
                additions.append(", split screen composition showing comparison")

            else:
                additions.append(", showing " + element)

        if additions:
            enhanced = original_prompt + "".join(additions)

        return enhanced


def main():
    parser = argparse.ArgumentParser(
        description="生成標誌性圖片提示詞",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 為 Moltbot 生成標誌性提示詞
  python3 prompt-generator.py --content "Moltbot" --type iconic --num-prompts 4

  # 基於研究資料生成
  python3 prompt-generator.py --content "AI工具" --type iconic --research research.json
        """
    )

    # 注意：這是一個簡化版，實際應該整合到主 prompt-generator.py 中
    print("🔧 標誌性提示詞生成功能")
    print("⚠️  注意：這是展示概念，需要整合到主腳本中")
    print()
    print("📋 使用方式：")
    print("   python3 prompt-generator.py --content \"主題\" --type iconic")


if __name__ == "__main__":
    main()
