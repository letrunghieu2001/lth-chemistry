"""
Content generator v3: Study Card format with diagram data + history-hook status.

Calls Gemini API (direct or via OpenRouter) with the LTH Chemistry skill
prompt. Returns structured content for THCS & THPT posts.

v3 changes:
  - image_bullets → diagram_data (structured: mind_map / flowchart / info_grid)
  - Added layout_type field (mind_map | flowchart | info_grid)
  - Status MUST end with a CTA bridge linking to image content
  - Random caption style: story_hook or mini_trivia

Supports two backends:
  1. google-genai SDK (primary, requires GEMINI_API_KEY)
  2. OpenRouter API   (fallback, requires OPENROUTER_API_KEY)
"""

import json
import logging
import random
import re
import time

import requests as http_requests

from config import (
    GEMINI_API_KEY,
    OPENROUTER_API_KEY,
    SKILL_FILE,
    CURRICULUM_FILE,
    POST_TYPE_LABELS,
    CAPTION_STYLES,
    V3_LAYOUT_MAP,
)

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 10


def _repair_json(raw: str) -> str | None:
    """Attempt to repair truncated JSON from LLM output.
    
    Common failures:
    - Unterminated string (missing closing quote)
    - Missing closing braces/brackets
    - Trailing comma before closing brace
    """
    text = raw.strip()
    
    # Strip markdown code fences
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.startswith("json"):
            text = text[4:].strip()
    
    # Try parsing as-is first
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass
    
    # Fix unterminated string: find last unmatched quote, close it
    # Then close any open braces/brackets
    repaired = text
    
    # Close unterminated strings
    in_string = False
    escape = False
    for ch in repaired:
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
    if in_string:
        repaired += '"'
    
    # Remove trailing comma before we add closing braces
    repaired = re.sub(r',\s*$', '', repaired)
    
    # Count unmatched braces/brackets and close them
    opens = 0
    open_sq = 0
    in_str = False
    esc = False
    for ch in repaired:
        if esc:
            esc = False
            continue
        if ch == '\\':
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == '{':
            opens += 1
        elif ch == '}':
            opens -= 1
        elif ch == '[':
            open_sq += 1
        elif ch == ']':
            open_sq -= 1
    
    repaired += ']' * max(0, open_sq)
    repaired += '}' * max(0, opens)
    
    try:
        json.loads(repaired)
        logger.info("JSON repaired successfully (added %d closing tokens).",
                    max(0, open_sq) + max(0, opens) + (1 if in_string else 0))
        return repaired
    except json.JSONDecodeError:
        return None


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
    return f"""- Loại bài: TRẮC NGHIỆM HÓA HỌC
- YÊU CẦU ĐẶC BIỆT cho trắc nghiệm:
  + Tạo 1 câu hỏi trắc nghiệm 4 đáp án (A, B, C, D)
  + Câu hỏi phải rõ ràng, chính xác, phù hợp trình độ Lớp {grade} Chương {chapter}
  + Chỉ có DUY NHẤT 1 đáp án đúng
  + Trả về thêm fields: "question", "options" (list 4 string), "answer" (chỉ chữ A/B/C/D), "explanation"
  + Caption: hook hỏi, KHÔNG tiết lộ đáp án trong caption chính, đáp án để ở cuối sau dấu "---"
"""


def _build_normal_section(post_type: str, grade: int, chapter: int) -> str:
    post_label = POST_TYPE_LABELS.get(post_type, post_type)
    return f"""- Loại bài: {post_label}
"""


def _build_user_prompt(today_info: dict) -> str:
    """Build the user prompt with v3 schema: diagram_data + CTA bridge."""
    thcs_type = today_info["thcs_post_type"]
    thpt_type = today_info["thpt_post_type"]

    thcs_caption_style = random.choice(CAPTION_STYLES)
    thpt_caption_style = random.choice(CAPTION_STYLES)

    # Get default layout types
    thcs_layout = V3_LAYOUT_MAP.get(thcs_type, "info_grid")
    thpt_layout = V3_LAYOUT_MAP.get(thpt_type, "info_grid")

    if thcs_type == "quiz_mcq":
        thcs_section = _build_quiz_section("THCS", today_info["thcs_grade"], today_info["thcs_chapter"])
    else:
        thcs_section = _build_normal_section(thcs_type, today_info["thcs_grade"], today_info["thcs_chapter"])

    if thpt_type == "quiz_mcq":
        thpt_section = _build_quiz_section("THPT", today_info["thpt_grade"], today_info["thpt_chapter"])
    else:
        thpt_section = _build_normal_section(thpt_type, today_info["thpt_grade"], today_info["thpt_chapter"])

    quiz_fields_example = ""
    if thcs_type == "quiz_mcq" or thpt_type == "quiz_mcq":
        quiz_fields_example = """
    "question": "Câu hỏi trắc nghiệm (CHỈ có khi loại bài là TRẮC NGHIỆM)",
    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
    "answer": "B",
    "explanation": "Giải thích ngắn gọn tại sao đáp án đúng","""

    style_descriptions = {
        "story_hook": (
            "STORY HOOK — Kể 1 câu chuyện ngắn về lịch sử hóa học gắn với chủ đề bài viết. "
            "VD: 'Năm 1774, Lavoisier đốt kim cương và phát hiện nó chỉ là carbon...'"
        ),
        "mini_trivia": (
            "MINI TRIVIA — Đặt 1 câu hỏi/fact bất ngờ về lịch sử hóa học. "
            "VD: 'Bạn biết không? Cơ thể người có đủ carbon để làm 9000 chiếc bút chì.'"
        ),
    }

    thcs_style_desc = style_descriptions[thcs_caption_style]
    thpt_style_desc = style_descriptions[thpt_caption_style]

    # Diagram data examples per layout type
    diagram_examples = {
        "mind_map": '''"diagram_data": {{
      "center": "KHÁI NIỆM CHÍNH (tối đa 4 từ)",
      "branches": [
        {{"title": "Nhánh 1 (2-3 từ)", "detail": "Giải thích ngắn, max 15 từ"}},
        {{"title": "Nhánh 2", "detail": "Giải thích ngắn"}},
        {{"title": "Nhánh 3", "detail": "Giải thích ngắn"}}
      ]
    }}''',
        "flowchart": '''"diagram_data": {{
      "steps": [
        {{"label": "Bước/Chất 1 (2-4 từ)", "detail": "Mô tả ngắn, max 10 từ"}},
        {{"label": "Bước/Chất 2", "detail": "Mô tả ngắn"}},
        {{"label": "Bước/Chất 3", "detail": "Mô tả ngắn"}},
        {{"label": "KẾT QUẢ", "detail": "Kết luận cuối cùng"}}
      ]
    }}''',
        "info_grid": '''"diagram_data": {{
      "cells": [
        {{"title": "Ô 1 (2-3 từ)", "bullets": ["Điểm 1 (max 8 từ)", "Điểm 2"]}},
        {{"title": "Ô 2", "bullets": ["Điểm 1", "Điểm 2"]}},
        {{"title": "Ô 3", "bullets": ["Điểm 1", "Điểm 2"]}},
        {{"title": "Ô 4", "bullets": ["Điểm 1", "Điểm 2"]}}
      ]
    }}''',
    }

    thcs_diagram_ex = diagram_examples.get(thcs_layout, diagram_examples["info_grid"])
    thpt_diagram_ex = diagram_examples.get(thpt_layout, diagram_examples["info_grid"])

    return f"""Hôm nay là ngày {today_info['date_display']}.

Hãy tạo 2 bài đăng Facebook cho LTH Chemistry (Thầy Hiếu - gia sư Hóa học tại Hà Nội):

**Bài 1 - THCS:**
- Đối tượng: Lớp {today_info['thcs_grade']} (KHTN - Kết nối tri thức)
- Chương hiện tại: Chương {today_info['thcs_chapter']}
{thcs_section}
- CAPTION STYLE: {thcs_style_desc}
- LAYOUT TYPE: {thcs_layout}

**Bài 2 - THPT:**
- Đối tượng: Lớp {today_info['thpt_grade']} (Hóa học - Kết nối tri thức)
- Chương hiện tại: Chương {today_info['thpt_chapter']}
{thpt_section}
- CAPTION STYLE: {thpt_style_desc}
- LAYOUT TYPE: {thpt_layout}

## QUY TẮC BẮT BUỘC (PHẢI TUÂN THỦ):

### NGUYÊN TẮC #1: ẢNH LÀ NỘI DUNG CHÍNH — STUDY CARD FORMAT v3
- ẢNH chứa TOÀN BỘ kiến thức dưới dạng SƠ ĐỒ (diagram)
- Layout type quyết định cấu trúc diagram_data:
  + mind_map: center (khái niệm chính) + 3-4 branches (nhánh con)
  + flowchart: 3-5 steps (quy trình, chuỗi phản ứng)
  + info_grid: 2-4 cells (so sánh, liệt kê, quiz options)
- Mọi text trong diagram PHẢI NGẮN GỌN (title max 4 từ, detail max 15 từ)
- Nội dung phải là kiến thức cốt lõi: công thức, quy tắc, so sánh

### NGUYÊN TẮC #2: STATUS = HISTORY HOOK + CTA BRIDGE
- Status là 2-3 câu (40-60 từ):
  + Câu 1-2: FACT LỊCH SỬ HÓA HỌC CÓ THẬT gắn với chủ đề
  + Câu cuối: CTA BRIDGE dẫn người đọc xem ảnh, NÓI RÕ ảnh chứa gì
- VD CTA BRIDGE tốt:
  + "Xem sơ đồ 3 loại liên kết hóa học trong ảnh nhé! 👇"
  + "Thầy tổng hợp bảng so sánh axit-bazơ trong ảnh, check ngay! 🧪"
  + "Flowchart chuỗi phản ứng sắt ở ảnh dưới, lưu về ôn thi nha! 📚"
- CTA phải CỤ THỂ về nội dung ảnh (không chung chung kiểu "xem ảnh đi")
- TUYỆT ĐỐI KHÔNG viết công thức hóa học trong status

### Giọng văn status:
- Giọng Thầy Hiếu: mentor gần gũi, vui vẻ, đam mê hóa học
- Xưng "thầy"/"mình", gọi "em"/"các em"/"bạn"
- Emoji VỪA PHẢI (1-2 emoji), không spam

### Chính tả tiếng Việt:
- Kiểm tra kỹ chính tả trước khi trả về
- Không viết tắt vô nghĩa, không teencode

### image_title:
- Tiêu đề ngắn gọn, IN HOA, tối đa 6 từ

### image_prompt (mô tả visual cho AI gen ảnh nền):
- Mô tả bằng TIẾNG ANH
- KHÔNG yêu cầu text/chữ/số — text overlay riêng
- Yêu cầu: subtle chemistry doodles, molecular patterns, light decoration
- Luôn thêm: "1080x1080, no text, no words, no letters, light decoration only"

Trả về JSON (KHÔNG bọc trong markdown code block):
{{
  "thcs_post": {{
    "status": "History hook 40-60 từ + CTA bridge cụ thể dẫn vào ảnh",
    "caption_style": "{thcs_caption_style}",
    "hashtags": "#LTHChemistry #HoaHoc ... (cách nhau bằng dấu cách)",
    "image_title": "TIÊU ĐỀ NGẮN GỌN (max 6 từ, IN HOA)",
    "layout_type": "{thcs_layout}",
    {thcs_diagram_ex},{quiz_fields_example}
    "image_prompt": "English visual description for subtle background texture",
    "grade_label": "KHTN Lớp {today_info['thcs_grade']}"
  }},
  "thpt_post": {{
    "status": "History hook 40-60 từ + CTA bridge cụ thể dẫn vào ảnh",
    "caption_style": "{thpt_caption_style}",
    "hashtags": "#LTHChemistry #HoaHoc ... (cách nhau bằng dấu cách)",
    "image_title": "TIÊU ĐỀ NGẮN GỌN (max 6 từ, IN HOA)",
    "layout_type": "{thpt_layout}",
    {thpt_diagram_ex},{quiz_fields_example}
    "image_prompt": "English visual description for subtle background texture",
    "grade_label": "Hóa Học Lớp {today_info['thpt_grade']}"
  }}
}}"""


# ── Backend 1: Gemini Direct (google-genai SDK) ──────────────────────

def _call_gemini_direct(system_prompt: str, user_prompt: str) -> str | None:
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
        max_output_tokens=8192,
    )

    from config import FLASH_MODEL_CHAIN
    for model in FLASH_MODEL_CHAIN:
        try:
            logger.info("Trying model: %s", model)
            response = client.models.generate_content(
                model=model, contents=user_prompt, config=config,
            )
            return response.text.strip()
        except Exception as exc:
            if "503" in str(exc) or "UNAVAILABLE" in str(exc):
                logger.warning("Model %s unavailable, trying next...", model)
                continue
            raise
    raise RuntimeError("All text models unavailable (503).")


# ── Backend 2: OpenRouter API (HTTP) ─────────────────────────────────

def _call_openrouter(system_prompt: str, user_prompt: str) -> str | None:
    models_to_try = [
        "google/gemini-3.5-flash",
        "google/gemini-3.1-flash-lite",
        "google/gemini-2.5-flash",
        "openrouter/free",
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
    """Generate content for today's posts. Returns dict or None on failure."""
    backends = []
    if GEMINI_API_KEY:
        backends.append(("Gemini Direct", _call_gemini_direct))
    if OPENROUTER_API_KEY:
        backends.append(("OpenRouter", _call_openrouter))

    if not backends:
        logger.error("No API key configured.")
        return None

    system_prompt = _load_skill_prompt()
    user_prompt = _build_user_prompt(today_info)

    for backend_name, call_fn in backends:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info("[%s] Attempt %d/%d...", backend_name, attempt, MAX_RETRIES)
                raw_text = call_fn(system_prompt, user_prompt)
                if not raw_text:
                    raise ValueError("Empty response")

                # Try direct parse, then repair if truncated
                clean = raw_text
                if clean.startswith("```"):
                    clean = clean.strip("`").strip()
                    if clean.startswith("json"):
                        clean = clean[4:].strip()

                try:
                    content = json.loads(clean)
                except json.JSONDecodeError:
                    logger.warning("[%s] JSON parse failed, attempting repair...", backend_name)
                    repaired = _repair_json(raw_text)
                    if repaired is None:
                        raise
                    content = json.loads(repaired)

                if "thcs_post" not in content or "thpt_post" not in content:
                    logger.error("Response missing required keys.")
                    continue

                # Validate v3 structure
                for key in ["thcs_post", "thpt_post"]:
                    post = content[key]
                    required = ["status", "hashtags", "image_title",
                                "layout_type", "diagram_data",
                                "image_prompt", "grade_label"]
                    missing = [f for f in required if f not in post]
                    if missing:
                        logger.error("Post '%s' missing: %s", key, missing)
                        continue

                    if not isinstance(post.get("diagram_data"), dict):
                        logger.error("Post '%s' diagram_data must be dict", key)
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

        logger.warning("[%s] All attempts failed.", backend_name)

    logger.error("All backends failed. Skipping today.")
    return None
