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
        model="gemini-2.0-flash",
        contents=user_prompt,
        config=config,
    )
    return response.text.strip()


# ── Backend 2: OpenRouter API (HTTP) ─────────────────────────────────

def _call_openrouter(system_prompt: str, user_prompt: str) -> str | None:
    """Call a free model via OpenRouter's REST API."""
    # Try models in order: specific free model first, then free router
    models_to_try = [
        "google/gemini-2.5-flash-preview-05-20",  # often available free
        "openrouter/free",                          # auto-picks best free model
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
                                "image_content", "grade_label"]
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
