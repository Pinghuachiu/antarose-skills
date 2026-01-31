#!/usr/bin/env python3
"""
Social Content Writer - Image/Video Prompt Generator
生成專業的 AI 圖片/影片生成提示詞
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# 圖片風格庫
IMAGE_STYLES = {
    "realistic": {
        "name": "寫實攝影",
        "description": "真實照片風格，專業攝影質量",
        "keywords": "photorealistic, professional photography, high detail, sharp focus"
    },
    "illustration": {
        "name": "數位插畫",
        "description": "現代數位插畫風格",
        "keywords": "digital illustration, modern art, clean lines, vibrant colors"
    },
    "3d-render": {
        "name": "3D 渲染",
        "description": "3D 軟件渲染的高質量圖像",
        "keywords": "3D render, octane render, blender, high quality, detailed"
    },
    "minimalist": {
        "name": "極簡主義",
        "description": "簡潔、乾淨的設計",
        "keywords": "minimalist, clean, simple, elegant, modern design"
    },
    "cyberpunk": {
        "name": "赛博朋克",
        "description": "科幻未來風格",
        "keywords": "cyberpunk, futuristic, neon, sci-fi, dark atmosphere"
    },
    "watercolor": {
        "name": "水彩畫",
        "description": "藝術水彩風格",
        "keywords": "watercolor painting, artistic, soft colors, hand-painted"
    },
    "pop-art": {
        "name": "波普藝術",
        "description": "大眾藝術風格",
        "keywords": "pop art, bold colors, comic style, artistic"
    },
    "isometric": {
        "name": "等距視圖",
        "description": "2.5D 等距視角",
        "keywords": "isometric, 2.5D, perspective, clean design"
    }
}

# 影片風格庫
VIDEO_STYLES = {
    "cinematic": {
        "name": "電影感",
        "description": "電影級質量，戲劇性光效",
        "keywords": "cinematic, dramatic lighting, film grain, professional"
    },
    "animation": {
        "name": "動畫風格",
        "description": "2D 或 3D 動畫",
        "keywords": "animation, 3D animation, smooth motion, colorful"
    },
    "documentary": {
        "name": "紀錄片風格",
        "description": "真實、客觀的視覺風格",
        "keywords": "documentary style, realistic, informative, clear"
    },
    "commercial": {
        "name": "商業廣告",
        "description": "高品質商業片風格",
        "keywords": "commercial, polished, professional, high production value"
    }
}

# 平台最佳實踐
PLATFORM_SPECS = {
    "instagram": {
        "image_ratios": ["1:1", "4:5"],
        "video_ratios": ["9:16", "1:1"],
        "recommended_image_styles": ["realistic", "3d-render", "minimalist"],
        "recommended_video_styles": ["cinematic", "animation"]
    },
    "facebook": {
        "image_ratios": ["16:9", "1:1"],
        "video_ratios": ["16:9"],
        "recommended_image_styles": ["realistic", "illustration"],
        "recommended_video_styles": ["cinematic", "documentary"]
    },
    "linkedin": {
        "image_ratios": ["16:9", "4:5"],
        "video_ratios": ["16:9"],
        "recommended_image_styles": ["minimalist", "realistic"],
        "recommended_video_styles": ["documentary", "commercial"]
    },
    "threads": {
        "image_ratios": ["16:9", "1:1"],
        "video_ratios": ["9:16", "16:9"],
        "recommended_image_styles": ["illustration", "minimalist"],
        "recommended_video_styles": ["animation", "cinematic"]
    },
    "youtube": {
        "image_ratios": ["16:9"],
        "video_ratios": ["16:9"],
        "recommended_image_styles": ["realistic", "3d-render", "pop-art"],
        "recommended_video_styles": ["cinematic", "commercial"]
    }
}


class PromptGenerator:
    """提示詞生成器"""

    def __init__(self, platform: str = "instagram"):
        self.platform = platform
        self.platform_specs = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["instagram"])

    def generate_image_prompts(self, content: Dict, styles: List[str],
                               num_prompts: int = 3) -> List[Dict]:
        """生成圖片提示詞"""
        print(f"🖼️  正在生成圖片提示詞（{num_prompts} 個）...")

        # 提取內容信息
        title = content.get("title", "")
        topic = content.get("metadata", {}).get("topic", "")
        content_text = content.get("content", "")[:500]

        prompts = []

        # 選擇風格
        available_styles = [s for s in styles if s in IMAGE_STYLES]
        if not available_styles:
            available_styles = self.platform_specs["recommended_image_styles"]

        for i in range(num_prompts):
            # 輪流使用風格
            style_name = available_styles[i % len(available_styles)]
            style = IMAGE_STYLES[style_name]

            # 生成提示詞
            prompt = self._create_image_prompt(title, topic, content_text, style)

            # 選擇寬高比
            ratio = self.platform_specs["image_ratios"][i % len(self.platform_specs["image_ratios"])]

            prompt_obj = {
                "order": i + 1,
                "main_prompt": prompt["main"],
                "chinese_prompt": prompt["chinese"],
                "style": style_name,
                "style_description": style["description"],
                "aspect_ratio": ratio,
                "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy, watermark, text",
                "enhancement_tips": [
                    f"使用 {style['name']} 風格獲得最佳效果",
                    f"推薦寬高比: {ratio}",
                    "高解析度建議: 1920x1080 或更高"
                ]
            }
            prompts.append(prompt_obj)

        return prompts

    def _create_image_prompt(self, title: str, topic: str, content: str, style: Dict) -> Dict[str, str]:
        """創建圖片提示詞"""

        # 基於內容生成主題
        subject = f"Professional visual representation of {topic or title}"

        # 英文提示詞
        main_prompt = (
            f"{subject}, "
            f"{style['keywords']}, "
            f"high quality, detailed, "
            f"professional composition, "
            f"perfect lighting, "
            f"8k resolution"
        )

        # 中文提示詞
        chinese_prompt = (
            f"{topic or title}的專業視覺呈現，"
            f"{style['name']}風格，"
            f"高品質，細節豐富，"
            f"專業構圖，完美光照"
        )

        return {
            "main": main_prompt,
            "chinese": chinese_prompt
        }

    def generate_video_prompts(self, content: Dict, duration: int = 30,
                               style: str = "cinematic") -> Dict:
        """生成影片提示詞"""
        print(f"🎬 正在生成影片提示詞（{duration}秒，{style}風格）...")

        # 提取內容信息
        title = content.get("title", "")
        topic = content.get("metadata", {}).get("topic", "")
        content_text = content.get("content", "")

        style_info = VIDEO_STYLES.get(style, VIDEO_STYLES["cinematic"])

        # 分解場景
        scenes = []

        # 開場場景（3秒）
        scenes.append({
            "order": 1,
            "duration": "3s",
            "visual_description": f"Opening shot featuring {topic or title} with dramatic entrance",
            "camera_movement": "Slow zoom in",
            "audio": "Background music starts building up"
        })

        # 主要場景
        main_duration = duration - 6
        if main_duration > 0:
            scenes.append({
                "order": 2,
                "duration": f"{main_duration}s",
                "visual_description": f"Main content showcasing key aspects of {topic or title}, dynamic transitions, engaging visuals",
                "camera_movement": "Mix of tracking shots and close-ups",
                "audio": "Upbeat background music with rhythmic cuts"
            })

        # 結尾場景（3秒）
        scenes.append({
            "order": len(scenes) + 1,
            "duration": "3s",
            "visual_description": "Call-to-action with branding or key message",
            "camera_movement": "Pull back to reveal full scene",
            "audio": "Music crescendo then fade out"
        })

        # 選擇寬高比
        ratio = self.platform_specs["video_ratios"][0]

        # 整體提示詞
        overall_prompt = (
            f"A {duration}-second {style_info['name']} video about {topic or title}, "
            f"{style_info['keywords']}, "
            f"professional quality, smooth transitions, "
            f"engaging visual storytelling"
        )

        chinese_prompt = (
            f"一部關於{topic or title}的{duration}秒{style_info['name']}影片，"
            f"專業品質，流暢轉場，引人入勝的視覺敘事"
        )

        result = {
            "video_type": style_info["name"],
            "duration": duration,
            "scenes": scenes,
            "technical_specs": {
                "resolution": "1080p",
                "aspect_ratio": ratio,
                "frame_rate": "30fps",
                "style": style_info["name"]
            },
            "overall_prompt": overall_prompt,
            "chinese_prompt": chinese_prompt,
            "enhancement_tips": [
                f"使用 {style_info['name']} 風格",
                f"推薦寬高比: {ratio}",
                "確保音樂與畫面節奏匹配"
            ]
        }

        return result

    def generate_with_ai(self, content: Dict, prompt_type: str,
                        styles: Optional[List[str]] = None,
                        num_prompts: int = 3) -> Dict:
        """使用 AI 生成高級提示詞"""
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            print("⚠️  未設置 OPENAI_API_KEY，使用模板生成")
            if prompt_type == "image":
                return {"prompts": self.generate_image_prompts(content, styles or ["realistic"], num_prompts)}
            else:
                return self.generate_video_prompts(content)

        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)

            if prompt_type == "image":
                return self._generate_image_prompts_ai(client, content, styles, num_prompts)
            else:
                return self._generate_video_prompts_ai(client, content)

        except Exception as e:
            print(f"⚠️  AI 生成失敗: {e}")
            print("使用模板生成作為備選方案")
            if prompt_type == "image":
                return {"prompts": self.generate_image_prompts(content, styles or ["realistic"], num_prompts)}
            else:
                return self.generate_video_prompts(content)

    def _generate_image_prompts_ai(self, client, content: Dict,
                                   styles: Optional[List[str]] = None,
                                   num_prompts: int = 3) -> Dict:
        """使用 AI 生成圖片提示詞"""
        title = content.get("title", "")
        topic = content.get("metadata", {}).get("topic", "")
        content_text = content.get("content", "")[:300]

        available_styles = styles or self.platform_specs["recommended_image_styles"]

        prompt = f"""基於以下文章內容，生成 {num_prompts} 個專業精準的 AI 圖片生成提示詞：

【文章資訊】
- 標題: {title}
- 主題: {topic}
- 內容摘要: {content_text}
- 目標平台: {self.platform}

【要求】
1. 每個提示詞必須包含：
   - 清晰的主體描述
   - 具體的藝術風格（從以下選擇：{', '.join(available_styles)}）
   - 詳細的環境和光照設定
   - 明確的構圖和視角
   - 色彩和氛圍描述

2. 技術參數建議：
   - 從以下寬高比選擇：{', '.join(self.platform_specs['image_ratios'])}
   - 解析度：建議 1920x1080 或更高

3. 返回 JSON 格式：
{{
  "prompts": [
    {{
      "order": 1,
      "main_prompt": "英文提示詞（詳細）",
      "chinese_prompt": "中文提示詞",
      "style": "風格名稱",
      "aspect_ratio": "寬高比",
      "negative_prompt": "負面提示詞"
    }}
  ]
}}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是專業的 AI 圖片生成提示詞工程師。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        content_text = response.choices[0].message.content
        import re
        json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        return {"prompts": []}

    def _generate_video_prompts_ai(self, client, content: Dict) -> Dict:
        """使用 AI 生成影片提示詞"""
        title = content.get("title", "")
        topic = content.get("metadata", {}).get("topic", "")
        content_text = content.get("content", "")[:300]

        prompt = f"""基於以下文章內容，生成專業精準的 AI 影片生成提示詞：

【文章資訊】
- 標題: {title}
- 主題: {topic}
- 內容摘要: {content_text}
- 目標平台: {self.platform}

【要求】
1. 分解為 3-5 個場景
2. 每個場景包含：
   - 視覺描述（主體、背景、動作）
   - 鏡頭運動
   - 時長分配
   - 音效建議

3. 返回 JSON 格式：
{{
  "video_type": "影片類型",
  "scenes": [
    {{
      "order": 1,
      "duration": "3s",
      "visual_description": "視覺描述",
      "camera_movement": "鏡頭運動",
      "audio": "音效建議"
    }}
  ],
  "overall_prompt": "整體影片提示詞（英文）",
  "chinese_prompt": "整體影片提示詞（中文）"
}}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是專業的 AI 影片生成提示詞工程師。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        content_text = response.choices[0].message.content
        import re
        json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        return {}

    def generate_images(self, prompts: List[Dict], provider: str = "nanobanana",
                        size: str = "1920x1080", quality: str = "hd",
                        upload_pix2: bool = False) -> List[str]:
        """使用 universal-image-gen 生成圖片"""
        print(f"\n🎨 正在生成圖片（{len(prompts)}張）...")

        script_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "universal-image-gen",
            "scripts",
            "generate.py"
        )

        generated_images = []

        for prompt_obj in prompts:
            try:
                prompt = prompt_obj["main_prompt"]
                print(f"  生成第 {prompt_obj['order']} 張圖片...")

                # 構建命令
                cmd = [
                    "python3", script_path,
                    prompt,
                    "--size", size,
                    "--quality", quality,
                    "--provider", provider
                ]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode == 0:
                    print(f"  ✅ 圖片 {prompt_obj['order']} 生成成功")
                    # 解析輸出獲取圖片路徑
                    output_lines = result.stdout.strip().split('\n')
                    if output_lines:
                        image_path = output_lines[-1].strip()
                        generated_images.append(image_path)

                        # 如果需要上傳到 Pix2
                        if upload_pix2:
                            print(f"  📤 正在上傳到 Pix2...")
                            self._upload_to_pix2(image_path)
                else:
                    print(f"  ❌ 圖片 {prompt_obj['order']} 生成失敗")

            except subprocess.TimeoutExpired:
                print(f"  ⏱️  圖片 {prompt_obj['order']} 生成超時")
            except Exception as e:
                print(f"  ❌ 圖片 {prompt_obj['order']} 生成錯誤: {e}")

        return generated_images

    def _upload_to_pix2(self, image_path: str) -> Optional[str]:
        """上傳圖片到 Pix2"""
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "pix2-upload",
            "scripts",
            "upload.py"
        )

        try:
            result = subprocess.run(
                ["python3", script_path, image_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # 解析輸出獲取 URL
                import re
                url_match = re.search(r'https?://[^\s]+', result.stdout)
                if url_match:
                    url = url_match.group()
                    print(f"  ✅ 上傳成功: {url}")
                    return url

        except Exception as e:
            print(f"  ⚠️  上傳失敗: {e}")

        return None

    def print_prompts(self, prompts_data: Dict):
        """打印生成的提示詞"""
        print("\n" + "="*60)
        print("✨ 提示詞生成成功")
        print("="*60)

        if "prompts" in prompts_data:
            prompts = prompts_data["prompts"]
            print(f"\n🖼️  圖片提示詞（{len(prompts)} 個）:\n")

            for prompt in prompts:
                print(f"  [{prompt['order']}] {prompt['style'].upper()} - {prompt['aspect_ratio']}")
                print(f"  英文: {prompt['main_prompt'][:100]}...")
                print(f"  中文: {prompt['chinese_prompt'][:80]}...")
                print()

        elif "scenes" in prompts_data:
            print(f"\n🎬 影片提示詞 ({prompts_data['duration']}秒, {prompts_data['video_type']}):\n")
            print(f"整體描述: {prompts_data['overall_prompt'][:100]}...")
            print(f"\n場景分解:")
            for scene in prompts_data["scenes"]:
                print(f"  場景 {scene['order']} ({scene['duration']}): {scene['visual_description'][:80]}...")

        print("="*60 + "\n")

    def save_to_file(self, prompts_data: Dict, filepath: str):
        """保存提示詞到文件"""
        output = {
            "generated_at": datetime.now().isoformat(),
            "platform": self.platform,
            **prompts_data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ 提示詞已保存到: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="生成 AI 圖片/影片生成提示詞",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 生成圖片提示詞
  python3 prompt-generator.py --content "AI內容創作" --type image

  # 生成圖片提示詞並自動生成圖片
  python3 prompt-generator.py --content "文章內容" --type image --auto-generate --upload-pix2

  # 生成影片提示詞
  python3 prompt-generator.py --content "文章內容" --type video --duration 30 --style cinematic
        """
    )
    parser.add_argument("--content", required=True, help="文章內容或 JSON 檔案路徑")
    parser.add_argument("--type", required=True,
                       choices=["image", "video", "thumbnail"],
                       help="提示詞類型")
    parser.add_argument("--platform", default="instagram",
                       choices=["instagram", "facebook", "linkedin", "threads", "youtube"],
                       help="目標平台")
    parser.add_argument("--styles", help="圖片風格（逗號分隔）")
    parser.add_argument("--num-prompts", type=int, default=3,
                       help="生成提示詞數量")
    parser.add_argument("--duration", type=int, default=30,
                       help="影片時長（秒）")
    parser.add_argument("--style", default="cinematic",
                       choices=["cinematic", "animation", "documentary", "commercial"],
                       help="影片風格")
    parser.add_argument("--use-ai", action="store_true",
                       help="使用 AI 生成高級提示詞")
    parser.add_argument("--auto-generate", action="store_true",
                       help="自動生成圖片（僅 image 類型）")
    parser.add_argument("--provider", default="nanobanana",
                       choices=["antigravity", "nanobanana"],
                       help="圖片生成服務")
    parser.add_argument("--size", default="1920x1080",
                       help="圖片尺寸")
    parser.add_argument("--quality", default="hd",
                       choices=["hd", "medium", "standard"],
                       help="圖片品質")
    parser.add_argument("--upload-pix2", action="store_true",
                       help="上傳到 Pix2 圖床")
    parser.add_argument("--output", default="prompts.json",
                       help="輸出檔案路徑")

    args = parser.parse_args()

    # 創建生成器
    generator = PromptGenerator(platform=args.platform)

    # 讀取內容
    content_input = args.content
    if os.path.exists(content_input):
        with open(content_input, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
    else:
        # 創建基本內容結構
        content_data = {
            "title": content_input[:50],
            "content": content_input,
            "metadata": {"topic": content_input[:30]}
        }

    # 解析風格
    styles = None
    if args.styles:
        styles = [s.strip() for s in args.styles.split(",")]

    # 生成提示詞
    if args.use_ai:
        prompts_data = generator.generate_with_ai(
            content_data,
            args.type,
            styles=styles,
            num_prompts=args.num_prompts
        )
    else:
        if args.type == "image":
            prompts_data = {
                "prompts": generator.generate_image_prompts(
                    content_data,
                    styles or generator.platform_specs["recommended_image_styles"],
                    args.num_prompts
                )
            }
        else:
            prompts_data = generator.generate_video_prompts(
                content_data,
                duration=args.duration,
                style=args.style
            )

    # 打印結果
    generator.print_prompts(prompts_data)

    # 自動生成圖片
    if args.auto_generate and args.type == "image":
        image_prompts = prompts_data.get("prompts", [])
        if image_prompts:
            generated = generator.generate_images(
                image_prompts,
                provider=args.provider,
                size=args.size,
                quality=args.quality,
                upload_pix2=args.upload_pix2
            )
            prompts_data["generated_images"] = generated

    # 保存到文件
    generator.save_to_file(prompts_data, args.output)


if __name__ == "__main__":
    main()
