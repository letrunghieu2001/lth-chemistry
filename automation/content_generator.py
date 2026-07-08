"""
Content generator: calls Gemini API (direct or via OpenRouter) with the
LTH Chemistry skill prompt.  Returns structured content for THCS & THPT posts.

Supports two backends:
  1. google-genai SDK (primary, requires GEMINI_API_KEY)
  2. OpenRouter API   (fallback, requires OPENROUTER_API_KEY)
"""

import json
import logging
import time

import requests as http_requests  # renamed to avoid collision

from config import (
    GEMINI_API_KEY,
    OPENROUTER_API_KEY,
    SKILL_FILE,
    CURRICULUM_FILE,
    POST_TYPE_LABELS,
)

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds


# ── Prompt builders ───────────────────────────────────────────────────

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


def _build_quiz_section(group: str, grade: int, chapter: int) -> str:
    """Build the quiz-specific prompt section for quiz_mcq post type."""
    return f"""- Loại bài: TRẮC NGHIỆM HÓA HỌC
- YÊU CẦU ĐẶC BIỆT cho trắc nghiệm:
  + Tạo 1 câu hỏi trắc nghiệm 4 đáp án (A, B, C, D)
  + Câu hỏi phải rõ ràng, chính xác, phù hợp trình độ Lớp {grade} Chương {chapter}
  + Chỉ có DUY NHẤT 1 đáp án đúng
  + Trả về thêm fields: "question", "options" (list 4 string), "answer" (chỉ chữ A/B/C/D), "explanation"
  + image_prompt phải mô tả ảnh quiz card hiện đại với câu hỏi + 4 đáp án hiển thị rõ
  + Caption: hook hỏi, KHÔNG tiết lộ đáp án trong caption chính, đáp án để ở cuối sau dấu "---"
"""


def _build_normal_section(post_type: str, grade: int, chapter: int) -> str:
    """Build the normal prompt section for non-quiz post types."""
    post_label = POST_TYPE_LABELS.get(post_type, post_type)
    return f"""- Loại bài: {post_label}
"""


def _build_user_prompt(today_info: dict) -> str:
    """Build the user prompt telling the AI what to generate today."""
    thcs_type = today_info["thcs_post_type"]
    thpt_type = today_info["thpt_post_type"]

    # Build type-specific sections
    if thcs_type == "quiz_mcq":
        thcs_section = _build_quiz_section("THCS", today_info["thcs_grade"], today_info["thcs_chapter"])
    else:
        thcs_section = _build_normal_section(thcs_type, today_info["thcs_grade"], today_info["thcs_chapter"])

    if thpt_type == "quiz_mcq":
        thpt_section = _build_quiz_section("THPT", today_info["thpt_grade"], today_info["thpt_chapter"])
    else:
        thpt_section = _build_normal_section(thpt_type, today_info["thpt_grade"], today_info["thpt_chapter"])

    # Quiz JSON fields
    quiz_fields_example = ""
    if thcs_type == "quiz_mcq" or thpt_type == "quiz_mcq":
        quiz_fields_example = """
    "question": "Câu hỏi trắc nghiệm (CHỈ có khi loại bài là TRẮC NGHIỆM)",
    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
    "answer": "B",
    "explanation": "Giải thích ngắn gọn tại sao đáp án đúng","""

    return f"""Hôm nay là ngày {today_info['date_display']}.

Hãy tạo 2 bài đăng Facebook cho LTH Chemistry (Thầy Hiếu - gia sư Hóa học tại Hà Nội):

**Bài 1 - THCS:**
- Đối tượng: Lớp {today_info['thcs_grade']} (KHTN - Kết nối tri thức)
- Chương hiện tại: Chương {today_info['thcs_chapter']}
{thcs_section}

**Bài 2 - THPT:**
- Đối tượng: Lớp {today_info['thpt_grade']} (Hóa học - Kết nối tri thức)
- Chương hiện tại: Chương {today_info['thpt_chapter']}
{thpt_section}

## QUY TẮC BẮT BUỘC (PHẢI TUÂN THỦ):

### Giọng văn:
- Viết bằng giọng Thầy Hiếu: mentor gần gũi, vui vẻ, đam mê hóa học
- Xưng "thầy" hoặc "mình", gọi học sinh là "em", "các em", "bạn"
- Dùng emoji VỪA PHẢI (3-5 emoji/bài), KHÔNG spam emoji
- Caption phải tự nhiên như người thật viết, TUYỆT ĐỐI KHÔNG giống AI

### Chính tả tiếng Việt (RẤT QUAN TRỌNG):
- Kiểm tra kỹ chính tả trước khi trả về
- Không viết tắt vô nghĩa, không dùng teencode
- Dấu câu đúng chuẩn tiếng Việt
- Công thức hóa học phải 100% chính xác (VD: H₂SO₄, NaOH, Fe₂O₃)

### Cấu trúc caption:
1. Hook mở đầu gây tò mò (1-2 dòng)
2. Nội dung chính: kiến thức / mẹo / câu hỏi (phần chính)
3. CTA kết thúc: khuyến khích comment, tag bạn, hoặc nhắn thầy

### Hashtags:
- 5-8 hashtags liên quan
- Luôn bao gồm: #LTHChemistry #HoaHoc #GiaSuHoaHoc

### image_prompt (BẮT BUỘC cho mỗi bài):
- Mô tả ảnh minh họa bằng TIẾNG ANH để AI gen ảnh
- Phong cách: modern, flat illustration, educational, vibrant colors
- Nếu là trắc nghiệm: mô tả quiz card với câu hỏi + 4 options A/B/C/D rendered trên ảnh
- Nếu là bài thường: mô tả hình minh họa liên quan đến chủ đề (ống nghiệm, phản ứng, nguyên tố...)
- KHÔNG yêu cầu text tiếng Việt trong ảnh (trừ công thức hóa học)
- Thêm "1080x1080, clean white or gradient background, no watermark" vào mỗi prompt

Trả về JSON (KHÔNG bọc trong markdown code block):
{{
  "thcs_post": {{
    "caption": "Nội dung caption đầy đủ, 150-280 từ",
    "hashtags": "#LTHChemistry #HoaHoc ... (cách nhau bằng dấu cách)",
    "image_title": "Tiêu đề trên ảnh (tối đa 8 từ)",
    "image_content": "Nội dung chính trên ảnh (tối đa 35 từ)",
    "image_prompt": "English description for AI image generation",{quiz_fields_example}
    "grade_label": "KHTN Lớp {today_info['thcs_grade']}"
  }},
  "thpt_post": {{
    "caption": "Nội dung caption đầy đủ, 150-280 từ",
    "hashtags": "#LTHChemistry #HoaHoc ... (cách nhau bằng dấu cách)",
    "image_title": "Tiêu đề trên ảnh (tối đa 8 từ)",
    "image_content": "Nội dung chính trên ảnh (tối đa 35 từ)",
    "image_prompt": "English description for AI image generation",{quiz_fields_example}
    "grade_label": "Hóa Học Lớp {today_info['thpt_grade']}"
  }}
}}"""


# ── Backend 1: Gemini Direct (google-genai SDK) ──────────────────────

def _call_gemini_direct(system_prompt: str, user_prompt: str) -> str | None:
    """Call Gemini via the official google-genai SDK."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        logger.warning("google-genai not installed, skipping direct Gemini.")
        return None

    client = genai.Client(api_key=GEMINI_API_KEY)

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json",
        temperature=0.8,
        max_output_tokens=4096,
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=user_prompt,
        config=config,
    )
    return response.text.strip()


# ── Backend 2: OpenRouter API (HTTP) ─────────────────────────────────

def _call_openrouter(system_prompt: str, user_prompt: str) -> str | None:
    """Call AI model via OpenRouter's REST API."""
    # Try models in order of quality (paid first, free fallback)
    models_to_try = [
        "google/gemini-3.5-flash",                   # best quality (paid, ~$0.001/req)
        "google/gemini-2.5-flash",                    # good quality (paid)
        "google/gemini-2.5-flash-preview-05-20",      # preview (might be free)
        "openrouter/free",                             # auto free router (fallback)
    ]

    last_error = None
    for model in models_to_try:
        try:
            resp = http_requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://lthchemistry.com",
                    "X-Title": "LTH Chemistry Auto Post",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.8,
                    "max_tokens": 4096,
                    "response_format": {"type": "json_object"},
                },
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            logger.warning("[OpenRouter] Model %s failed: %s", model, exc)
            last_error = exc

    if last_error:
        raise last_error
    return None


# ── Main entry point ─────────────────────────────────────────────────

def generate_content(today_info: dict) -> dict | None:
    """
    Generate content for today's posts using Gemini API.

    Tries direct Gemini first; if that fails, falls back to OpenRouter.
    Returns dict with 'thcs_post' and 'thpt_post' keys, or None on failure.
    """
    # Determine which backends are available
    backends = []
    if GEMINI_API_KEY:
        backends.append(("Gemini Direct", _call_gemini_direct))
    if OPENROUTER_API_KEY:
        backends.append(("OpenRouter", _call_openrouter))

    if not backends:
        logger.error(
            "No API key configured. Set GEMINI_API_KEY or OPENROUTER_API_KEY."
        )
        return None

    system_prompt = _load_skill_prompt()
    user_prompt = _build_user_prompt(today_info)

    for backend_name, call_fn in backends:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(
                    "[%s] Calling API (attempt %d/%d)...",
                    backend_name, attempt, MAX_RETRIES,
                )
                raw_text = call_fn(system_prompt, user_prompt)
                if not raw_text:
                    raise ValueError("Empty response from API")

                # Clean markdown fences if model wraps output
                if raw_text.startswith("```"):
                    raw_text = raw_text.strip("`").strip()
                    if raw_text.startswith("json"):
                        raw_text = raw_text[4:].strip()

                content = json.loads(raw_text)

                # Validate structure
                if "thcs_post" not in content or "thpt_post" not in content:
                    logger.error("Response missing required keys.")
                    continue

                for key in ["thcs_post", "thpt_post"]:
                    post = content[key]
                    required = ["caption", "hashtags", "image_title",
                                "image_content", "image_prompt", "grade_label"]
                    missing = [f for f in required if f not in post]
                    if missing:
                        logger.error("Post '%s' missing fields: %s", key, missing)
                        continue

                logger.info("[%s] Content generated successfully.", backend_name)
                return content

            except json.JSONDecodeError as exc:
                logger.error("[%s] JSON parse error: %s", backend_name, exc)
            except Exception as exc:
                logger.error("[%s] API error: %s", backend_name, exc)

            if attempt < MAX_RETRIES:
                wait = RETRY_DELAY * attempt
                logger.info("Retrying in %d seconds...", wait)
                time.sleep(wait)

        logger.warning("[%s] All attempts failed. Trying next backend...", backend_name)

    logger.error("All backends failed. Skipping today.")
    return None
