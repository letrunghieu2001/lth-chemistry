"""
Image generator v7: Two-Stage AI Pipeline for Study Cards.

Pipeline:
  1. Pick 2 chibi guest characters (weighted, history-aware)
  2. Build content brief from structured data
  3. ★ STAGE 1: Gemini Flash composes the EXACT image prompt
     - Decides layout, visual concept, decorations
     - Pre-bakes ALL Vietnamese text with correct spelling
     - Outputs a detailed image generation prompt
  4. ★ STAGE 2: Gemini Pro Image generates the image from that prompt
  5. OCR validates Vietnamese text quality
  6. If garbled → regenerate (up to N retries)
  7. Overlay logo → Save

Why two stages?
  - Text models spell Vietnamese perfectly
  - Image models often garble diacritics (ă, ơ, ư, ễ, ọ, etc.)
  - By pre-composing exact text in the prompt, the image model has a
    precise reference to copy, dramatically reducing spelling errors.
"""

import logging
import random
import time
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config import (
    GEMINI_API_KEY,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    LOGO_PATH,
    FONT_REGULAR,
    FONT_BOLD,
    OUTPUT_DIR,
    CHIBI_MASCOT,
    CHIBI_GUEST_CHARACTERS,
    CHARACTER_HISTORY_SIZE,
    OCR_MAX_RETRIES,
    OCR_VISION_MODEL,
    V3_LAYOUT_MAP,
)

logger = logging.getLogger(__name__)

AI_GEN_MAX_RETRIES = 5
AI_GEN_RETRY_DELAY = 8

# Models
PROMPT_COMPOSER_MODELS = None  # Will use FLASH_MODEL_CHAIN from config
IMAGE_GEN_MODEL = "gemini-3-pro-image"       # Stage 2: renders pixels

_font_cache: dict[str, ImageFont.FreeTypeFont] = {}


# ── Font Utilities (for logo overlay only) ───────────────────────────

def _get_font(bold: bool = False, size: int = 40) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold else FONT_REGULAR
    key = f"{path}_{size}"
    if key in _font_cache:
        return _font_cache[key]
    try:
        font = ImageFont.truetype(str(path), size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("arial.ttf", size)
        except (OSError, IOError):
            font = ImageFont.load_default()
    _font_cache[key] = font
    return font


# ── Character Selection ──────────────────────────────────────────────

def pick_guest_character(
    post_type: str, recent: list[str] | None = None,
) -> tuple[str, str]:
    """Pick a guest chibi, avoiding recent repeats. Returns (name, desc)."""
    recent = recent or []
    recent_set = set(recent[-CHARACTER_HISTORY_SIZE:])

    pool = [
        (n, d, wt)
        for n, d, types, wt in CHIBI_GUEST_CHARACTERS
        if post_type in types and n not in recent_set
    ]
    if not pool:
        pool = [
            (n, d, wt)
            for n, d, _, wt in CHIBI_GUEST_CHARACTERS
            if n not in recent_set
        ]
    if not pool:
        pool = [(n, d, wt) for n, d, _, wt in CHIBI_GUEST_CHARACTERS]

    idx = random.choices(range(len(pool)), weights=[p[2] for p in pool], k=1)[0]
    return pool[idx][0], pool[idx][1]


def _pick_two(post_type: str, recent: list[str] | None = None):
    """Pick 2 different guest characters."""
    n1, d1 = pick_guest_character(post_type, recent)
    n2, d2 = pick_guest_character(post_type, (recent or []) + [n1])
    return (n1, d1), (n2, d2)


# ── Stage 1: Prompt Composer (Text LLM) ─────────────────────────────

def _build_text_inventory(
    image_title: str,
    grade_label: str,
    layout_type: str,
    diagram_data: dict,
    quiz_data: dict | None = None,
) -> str:
    """
    Pre-build an exhaustive TEXT INVENTORY — a numbered list of EVERY text
    string that must appear in the generated image, verbatim.
    This is the core innovation: the image model copies these strings
    exactly instead of generating its own (error-prone) Vietnamese text.
    """
    lines: list[str] = []
    n = 1

    # Title & label
    lines.append(f'T{n}: "{image_title}"')
    n += 1
    lines.append(f'T{n}: "{grade_label}"')
    n += 1

    if layout_type == "mind_map":
        center = diagram_data.get("center", "")
        lines.append(f'T{n}: "{center}"')
        n += 1
        for br in diagram_data.get("branches", []):
            title = br.get("title", "")
            detail = br.get("detail", "")
            lines.append(f'T{n}: "{title}"')
            n += 1
            lines.append(f'T{n}: "{detail}"')
            n += 1

    elif layout_type == "flowchart":
        for st in diagram_data.get("steps", []):
            label = st.get("label", "")
            detail = st.get("detail", "")
            lines.append(f'T{n}: "{label}"')
            n += 1
            lines.append(f'T{n}: "{detail}"')
            n += 1

    elif layout_type == "info_grid":
        if quiz_data and quiz_data.get("question"):
            lines.append(f'T{n}: "{quiz_data["question"]}"')
            n += 1
            for i, cell in enumerate(diagram_data.get("cells", []), 1):
                letter = chr(64 + i)
                for bullet in cell.get("bullets", []):
                    lines.append(f'T{n}: "{letter}: {bullet}"')
                    n += 1
        else:
            for cell in diagram_data.get("cells", []):
                title = cell.get("title", "")
                lines.append(f'T{n}: "{title}"')
                n += 1
                for bullet in cell.get("bullets", []):
                    lines.append(f'T{n}: "{bullet}"')
                    n += 1

    return "\n".join(lines)


def _build_content_brief(
    post_type: str,
    image_title: str,
    layout_type: str,
    diagram_data: dict,
    grade_label: str,
    image_prompt: str,
    char1_desc: str,
    char2_desc: str,
    quiz_data: dict | None = None,
) -> str:
    """Build a content brief for the prompt composer LLM."""

    # Build the exhaustive text inventory
    text_inventory = _build_text_inventory(
        image_title, grade_label, layout_type, diagram_data, quiz_data,
    )

    # Describe layout type in Vietnamese for the LLM
    layout_desc_map = {
        "mind_map": "Sơ đồ tư duy (Mind Map): nút trung tâm + các nhánh tỏa ra",
        "flowchart": "Lưu đồ (Flowchart): các bước nối nhau bằng mũi tên, từ trên xuống",
        "info_grid": "Lưới thông tin (Info Grid): chia thành 2x2 ô thông tin",
    }
    layout_desc = layout_desc_map.get(layout_type, "Lưới thông tin")

    # Quiz-specific note
    quiz_note = ""
    if quiz_data and quiz_data.get("question"):
        layout_desc = "Thẻ trắc nghiệm (Quiz Card): câu hỏi lớn ở trên, 4 đáp án A/B/C/D bên dưới"
        quiz_note = "\n- Đây là Quiz Card: câu hỏi nổi bật trên nền navy, các đáp án là 4 ô riêng biệt."

    brief = f"""Bạn là chuyên gia thiết kế infographic giáo dục hóa học cho học sinh Việt Nam.

NHIỆM VỤ: Viết một prompt chi tiết bằng TIẾNG ANH để tạo ảnh infographic 1080x1080px.
Prompt này sẽ được gửi đến một AI image generator (Gemini Pro Image).

═══════════════════════════════════════════════════════════
DANH SÁCH TEXT BẮT BUỘC (TEXT INVENTORY)
Đây là TOÀN BỘ text phải xuất hiện trong ảnh. Sao chép NGUYÊN VĂN.
KHÔNG thêm, KHÔNG bớt, KHÔNG sửa, KHÔNG dịch bất kỳ chữ nào.
═══════════════════════════════════════════════════════════
{text_inventory}
═══════════════════════════════════════════════════════════

BỐ CỤC: {layout_desc}{quiz_note}
CHỦ ĐỀ HÌNH ẢNH: {image_prompt}

NHÂN VẬT CHIBI:
- Góc dưới bên trái: {char1_desc} (chibi sticker nhỏ ~15% chiều cao ảnh)
- Góc dưới bên phải: {char2_desc} (chibi sticker nhỏ ~15% chiều cao ảnh)

YÊU CẦU BẮT BUỘC cho prompt output:

1. PHẦN "TEXT PLACEMENT" — Bắt buộc trong prompt:
   Prompt PHẢI chứa một section "EXACT TEXT PLACEMENT" liệt kê TỪNG text item
   từ TEXT INVENTORY ở trên, kèm vị trí chính xác trong ảnh.
   Format: "Text string" → position in image (e.g., top center, branch 1, step 2).
   Sao chép NGUYÊN VĂN các text string, giữ ĐÚNG dấu tiếng Việt.

2. PHẦN "FORBIDDEN" — Bắt buộc trong prompt:
   Prompt PHẢI chứa dòng: "DO NOT generate any text that is not listed above.
   DO NOT modify, abbreviate, translate, or rephrase any text string.
   Copy each string character-by-character from the TEXT PLACEMENT list."

3. Giữ nguyên 100% dấu tiếng Việt (ă, â, ơ, ư, ễ, ọ, ứ, ờ, etc.)
4. Công thức hóa học giữ subscript: H₂O, CO₂, Fe₂O₃, Al₂O₃, etc.
5. Mô tả chi tiết: bố cục, kích thước, màu sắc, style cho từng element.

PALETTE MÀU BẮT BUỘC:
- Nền: kem ấm (#FDF8F0) với hoa văn chemistry nhạt
- Màu chính: teal (#0BA5A5) cho headers, connectors
- Màu phụ: navy đậm (#213555) cho borders, tiêu đề
- Text body: gần đen (#1A1A2E)
- Nền cards: trắng (#FFFFFF)
- Accent: vàng gold (#D4A017)

PHONG CÁCH:
- Modern, clean educational infographic — premium study flashcard
- Dày đặc thông tin, ít khoảng trắng (70-80% canvas là content)
- Text phải đọc rõ trên điện thoại

OUTPUT: Viết prompt bằng tiếng Anh, nhưng COPY-PASTE NGUYÊN VĂN tất cả
text tiếng Việt từ TEXT INVENTORY (trong ngoặc kép).
Chỉ output prompt, không giải thích gì thêm."""

    return brief


def _compose_image_prompt(content_brief: str) -> str | None:
    """
    Stage 1: Use Gemini Flash to compose the detailed image prompt.
    The text LLM ensures all Vietnamese text is perfectly spelled.
    Uses model fallback chain: 3.5 → 3.1 → 2.5
    """
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set.")
        return None
    try:
        from google import genai
        from config import FLASH_MODEL_CHAIN
        client = genai.Client(api_key=GEMINI_API_KEY)
        last_err = None
        for model_name in FLASH_MODEL_CHAIN:
            try:
                resp = client.models.generate_content(
                    model=model_name,
                    contents=[content_brief],
                )
                composed = resp.text.strip()
                logger.info(
                    "Stage 1 complete (model=%s): prompt composed (%d chars).",
                    model_name, len(composed),
                )
                return composed
            except Exception as exc:
                logger.warning("Prompt composer failed with %s: %s", model_name, exc)
                last_err = exc
        logger.error("All prompt composer models failed. Last error: %s", last_err)
        return None
    except Exception as exc:
        logger.error("Prompt composer setup failed: %s", exc)
        return None


# ── Stage 2: Image Generation ────────────────────────────────────────

def _gen_ai_image(prompt: str) -> Image.Image | None:
    """Stage 2: Generate image via Gemini Pro Image."""
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set.")
        return None
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        resp = client.models.generate_content(
            model=IMAGE_GEN_MODEL, contents=[prompt],
        )
        # Guard against None parts (safety filters, empty response)
        parts = getattr(resp, 'parts', None)
        if not parts:
            logger.warning("AI image gen returned no parts (possibly blocked by safety filter).")
            return None
        for part in parts:
            inline = getattr(part, 'inline_data', None)
            if inline is not None and hasattr(inline, 'data'):
                return Image.open(BytesIO(inline.data))
        logger.warning("AI image gen returned parts but no image data.")
        return None
    except Exception as exc:
        logger.error("AI image gen failed: %s", exc)
        return None


# ── OCR Validator ────────────────────────────────────────────────────

def _validate_image_quality(image: Image.Image, expected_title: str) -> bool:
    """
    Validate AI-generated image:
    1. Check for garbled/misspelled Vietnamese text
    2. Verify the title is present and readable
    Returns True if image passes quality checks.
    """
    if not GEMINI_API_KEY:
        return True
    try:
        from google import genai
        from google.genai import types
        from config import FLASH_MODEL_CHAIN
        client = genai.Client(api_key=GEMINI_API_KEY)
        buf = BytesIO()
        image.save(buf, format="PNG")
        image_part = types.Part.from_bytes(data=buf.getvalue(), mime_type="image/png")
        prompt_text = (
            f"Examine this Vietnamese educational infographic image carefully.\n"
            f"Expected title: \"{expected_title}\"\n\n"
            f"Check for these issues:\n"
            f"1. Any garbled, nonsensical, or badly misspelled Vietnamese text\n"
            f"2. Text that is unreadable or too blurry\n"
            f"3. Chemistry formulas that look wrong\n\n"
            f"If the image has CLEAR, READABLE Vietnamese text with no major "
            f"spelling errors, respond EXACTLY: IMAGE_CLEAN\n"
            f"If you find garbled or seriously misspelled text, respond EXACTLY: "
            f"GARBLED_TEXT_FOUND\n"
            f"Respond with only one of these two phrases."
        )
        for ocr_model in FLASH_MODEL_CHAIN:
            try:
                resp = client.models.generate_content(
                    model=ocr_model,
                    contents=[image_part, prompt_text],
                )
                result = resp.text.strip().upper()
                if "GARBLED" in result:
                    logger.warning("OCR (%s): garbled/misspelled text detected.", ocr_model)
                    return False
                logger.info("OCR (%s): image text quality OK.", ocr_model)
                return True
            except Exception as exc:
                logger.warning("OCR model %s failed: %s", ocr_model, exc)
        # All OCR models failed — don't block
        logger.warning("All OCR models failed. Passing image by default.")
        return True
    except Exception as exc:
        logger.warning("OCR validation error (non-critical): %s", exc)
        return True  # Don't block on OCR failure


# ── Logo Overlay ─────────────────────────────────────────────────────

def _overlay_logo(img: Image.Image) -> Image.Image:
    """Place logo in top-right corner (small, non-intrusive)."""
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
    except (FileNotFoundError, IOError):
        return img

    new_h = 45
    aspect = logo.width / logo.height
    new_w = int(new_h * aspect)
    logo = logo.resize((new_w, new_h), Image.LANCZOS)

    if img.mode != "RGBA":
        img = img.convert("RGBA")

    x = img.width - new_w - 16
    y = 12
    img.paste(logo, (x, y), logo)
    return img


# ── Main Entry Point ─────────────────────────────────────────────────

def create_post_image(
    post_type: str,
    image_title: str,
    layout_type: str,
    diagram_data: dict,
    grade_label: str,
    image_prompt: str,
    filename: str,
    recent_characters: list[str] | None = None,
    quiz_data: dict | None = None,
    # Backward compat — ignored
    image_bullets: list[str] | None = None,
) -> tuple[Path | None, list[str] | None]:
    """
    Create a FULL AI-generated Study Card image (two-stage pipeline).

    Stage 1: Gemini Flash composes the exact image prompt (perfect Vietnamese)
    Stage 2: Gemini Pro Image renders the infographic

    Returns (path_to_image, [char1_name, char2_name]) or (None, None).
    """
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / filename

        # Resolve layout type
        if not layout_type:
            layout_type = V3_LAYOUT_MAP.get(post_type, "info_grid")

        # Step 1: Pick 2 guest characters
        (c1_name, c1_desc), (c2_name, c2_desc) = _pick_two(
            post_type, recent_characters,
        )
        logger.info("Characters: %s (L), %s (R)", c1_name, c2_name)

        # Step 2 (Stage 1): Build content brief → LLM composes prompt
        content_brief = _build_content_brief(
            post_type, image_title, layout_type, diagram_data,
            grade_label, image_prompt, c1_desc, c2_desc, quiz_data,
        )
        logger.info("Content brief built (%d chars). Composing image prompt...", len(content_brief))

        composed_prompt = _compose_image_prompt(content_brief)
        if not composed_prompt:
            logger.error("Stage 1 failed: could not compose prompt.")
            return None, None

        # Step 3 (Stage 2): Generate image + OCR validate (with retries)
        # On OCR failure, re-compose prompt (Stage 1) every 2 failures
        # to get a fresh visual approach
        final_image = None
        for attempt in range(1, AI_GEN_MAX_RETRIES + 1):
            logger.info("Generation attempt %d/%d...", attempt, AI_GEN_MAX_RETRIES)

            # Re-compose prompt every 2 failures for fresh approach
            if attempt > 1 and (attempt - 1) % 2 == 0:
                logger.info("Re-composing prompt (fresh Stage 1)...")
                new_prompt = _compose_image_prompt(content_brief)
                if new_prompt:
                    composed_prompt = new_prompt

            raw_image = _gen_ai_image(composed_prompt)
            if raw_image is None:
                logger.warning("AI returned None (attempt %d).", attempt)
                if attempt < AI_GEN_MAX_RETRIES:
                    time.sleep(AI_GEN_RETRY_DELAY)
                continue

            # Resize to exact dimensions
            raw_image = raw_image.resize(
                (IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS,
            )

            # OCR quality check
            if _validate_image_quality(raw_image, image_title):
                final_image = raw_image
                logger.info("Image accepted (attempt %d).", attempt)
                break
            else:
                logger.warning(
                    "Image failed OCR check (attempt %d). Regenerating...",
                    attempt,
                )
                if attempt < AI_GEN_MAX_RETRIES:
                    time.sleep(AI_GEN_RETRY_DELAY)

        if final_image is None:
            logger.error("All %d generation attempts failed.", AI_GEN_MAX_RETRIES)
            return None, None

        # Step 4: Logo overlay
        final_image = _overlay_logo(final_image)

        # Step 5: Save as PNG
        if final_image.mode == "RGBA":
            save_img = Image.new("RGB", final_image.size, (255, 255, 255))
            save_img.paste(final_image, mask=final_image.split()[3])
        else:
            save_img = final_image.convert("RGB")
        save_img.save(str(output_path), "PNG", quality=95)

        logger.info("Image saved: %s", output_path)
        return output_path, [c1_name, c2_name]

    except Exception as exc:
        logger.error("Failed to create image: %s", exc, exc_info=True)
        return None, None
