"""
Content generator: calls Gemini API with the LTH Chemistry skill prompt.
Returns structured content for both THCS and THPT posts.
"""

import json
import logging
import time

import google.generativeai as genai

from config import (
    GEMINI_API_KEY,
    SKILL_FILE,
    CURRICULUM_FILE,
    POST_TYPE_LABELS,
)

logger = logging.getLogger(__name__)

# Maximum retries for API calls
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def _load_skill_prompt() -> str:
    """Load the SKILL.md and curriculum-map.md as system instructions."""
    parts = []
    for path in [SKILL_FILE, CURRICULUM_FILE]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                parts.append(f.read())
        except FileNotFoundError:
            logger.warning("File not found: %s", path)
    return "\n\n---\n\n".join(parts)


def _build_user_prompt(today_info: dict) -> str:
    """Build the user prompt telling the AI what to generate today."""
    post_type = today_info["post_type"]
    post_label = POST_TYPE_LABELS.get(post_type, post_type)

    return f"""Hôm nay là ngày {today_info['date_display']}.

Hãy tạo 2 bài đăng Facebook cho LTH Chemistry:

**Bài 1 - THCS:**
- Đối tượng: Lớp {today_info['thcs_grade']} (KHTN - Kết nối tri thức)
- Chương hiện tại: Chương {today_info['thcs_chapter']}
- Loại bài: {post_label}

**Bài 2 - THPT:**
- Đối tượng: Lớp {today_info['thpt_grade']} (Hóa học - Kết nối tri thức)
- Chương hiện tại: Chương {today_info['thpt_chapter']}
- Loại bài: {post_label}

Trả về JSON với cấu trúc sau (KHÔNG bọc trong markdown code block):
{{
  "thcs_post": {{
    "caption": "Nội dung caption Facebook đầy đủ, dưới 280 từ, bao gồm hook, nội dung chính, CTA",
    "hashtags": "Danh sách hashtags cách nhau bằng dấu cách",
    "image_title": "Tiêu đề ngắn hiển thị trên ảnh (tối đa 8 từ)",
    "image_content": "Nội dung chính hiển thị trên ảnh (tối đa 40 từ, có thể là câu hỏi, công thức, fact...)",
    "grade_label": "KHTN Lớp {today_info['thcs_grade']}"
  }},
  "thpt_post": {{
    "caption": "Nội dung caption Facebook đầy đủ, dưới 280 từ, bao gồm hook, nội dung chính, CTA",
    "hashtags": "Danh sách hashtags cách nhau bằng dấu cách",
    "image_title": "Tiêu đề ngắn hiển thị trên ảnh (tối đa 8 từ)",
    "image_content": "Nội dung chính hiển thị trên ảnh (tối đa 40 từ)",
    "grade_label": "Hóa Học Lớp {today_info['thpt_grade']}"
  }}
}}

Nhớ:
- Viết bằng giọng Thầy Hiếu (mentor, gần gũi, dùng emoji vừa phải)
- Caption phải tự nhiên, KHÔNG giống AI viết
- Công thức hóa học phải chính xác
- Kết thúc bằng CTA rõ ràng (comment, share, tag bạn)
"""


def generate_content(today_info: dict) -> dict | None:
    """
    Generate content for today's posts using Gemini API.

    Returns dict with 'thcs_post' and 'thpt_post' keys, or None on failure.
    """
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set. Cannot generate content.")
        return None

    genai.configure(api_key=GEMINI_API_KEY)

    system_prompt = _load_skill_prompt()
    user_prompt = _build_user_prompt(today_info)

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=system_prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.8,
            max_output_tokens=4096,
        ),
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("Calling Gemini API (attempt %d/%d)...", attempt, MAX_RETRIES)
            response = model.generate_content(user_prompt)

            raw_text = response.text.strip()
            content = json.loads(raw_text)

            # Validate structure
            if "thcs_post" not in content or "thpt_post" not in content:
                logger.error("Response missing required keys. Raw: %s", raw_text[:500])
                continue

            for key in ["thcs_post", "thpt_post"]:
                post = content[key]
                required = ["caption", "hashtags", "image_title", "image_content", "grade_label"]
                missing = [f for f in required if f not in post]
                if missing:
                    logger.error("Post '%s' missing fields: %s", key, missing)
                    continue

            logger.info("Content generated successfully.")
            return content

        except json.JSONDecodeError as exc:
            logger.error("Failed to parse JSON response: %s", exc)
        except Exception as exc:
            logger.error("Gemini API error: %s", exc)

        if attempt < MAX_RETRIES:
            logger.info("Retrying in %d seconds...", RETRY_DELAY)
            time.sleep(RETRY_DELAY)

    logger.error("All %d attempts failed. Skipping today.", MAX_RETRIES)
    return None
