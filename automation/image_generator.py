"""
Image generator v3: Hybrid Rendering + OCR Safety Net + Chibi Characters.

Pipeline:
  1. Prompt Rewriter  – injects chibi characters + "no text" rules
  2. AI Visual Gen    – Gemini Flash Image generates text-free visual
  3. Text Compositor  – Pillow overlays all text (always correct)
  4. OCR Validator    – Gemini Vision checks for garbled AI text
  5. Logo Overlay     – brand logo at bottom-right

Text is NEVER rendered by the AI model. Pillow handles all typography
using Be Vietnam Pro fonts, guaranteeing perfect Vietnamese diacritics.
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
    LOGO_MAX_HEIGHT,
    FONT_REGULAR,
    FONT_BOLD,
    TEMPLATE_COLORS,
    POST_TYPE_LABELS,
    OUTPUT_DIR,
    COLORS,
    CHIBI_MASCOT,
    CHIBI_GUEST_CHARACTERS,
    OCR_MAX_RETRIES,
    OCR_VISION_MODEL,
)

logger = logging.getLogger(__name__)

_font_cache: dict[str, ImageFont.FreeTypeFont] = {}


# ── Font utilities ────────────────────────────────────────────────────

def _get_font(bold: bool = False, size: int = 40) -> ImageFont.FreeTypeFont:
    """Load font with caching. Falls back to default if custom font missing."""
    path = FONT_BOLD if bold else FONT_REGULAR
    cache_key = f"{path}_{size}"
    if cache_key in _font_cache:
        return _font_cache[cache_key]

    try:
        font = ImageFont.truetype(str(path), size)
    except (OSError, IOError):
        logger.warning("Font %s not found, using default.", path)
        try:
            font = ImageFont.truetype("arial.ttf", size)
        except (OSError, IOError):
            font = ImageFont.load_default()

    _font_cache[cache_key] = font
    return font


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


# ── Chibi Character Selection ────────────────────────────────────────

def pick_guest_character(
    post_type: str,
    last_character: str | None = None,
) -> tuple[str, str]:
    """Pick a guest chibi character based on post type, avoiding repeats.

    Returns:
        (character_name, character_description)
    """
    # Find characters that prefer this post type
    preferred = [
        (name, desc)
        for name, desc, types in CHIBI_GUEST_CHARACTERS
        if post_type in types and name != last_character
    ]

    # If no preferred match or all filtered out, use full list minus last
    if not preferred:
        preferred = [
            (name, desc)
            for name, desc, _ in CHIBI_GUEST_CHARACTERS
            if name != last_character
        ]

    # Safety fallback: if everything filtered, use full list
    if not preferred:
        preferred = [(name, desc) for name, desc, _ in CHIBI_GUEST_CHARACTERS]

    return random.choice(preferred)


# ── Step 1: Prompt Rewriter ──────────────────────────────────────────

def _rewrite_prompt_for_visual(
    image_prompt: str,
    post_type: str,
    guest_name: str,
    guest_desc: str,
) -> str:
    """Rewrite the content image_prompt into a text-free visual prompt.

    Adds chibi character instructions, brand colors, and strict no-text rules.
    The original image_prompt describes the chemistry content; we keep the
    visual/conceptual parts but strip any text-rendering instructions.
    """
    accent_color = TEMPLATE_COLORS.get(post_type, TEMPLATE_COLORS["review_question"])["accent"]

    prompt = (
        "STYLE: Cute chibi anime illustration, kawaii aesthetic, chemistry education theme. "
        "1080x1080 square image, no watermark. "
        "\n\n"
        f"BACKGROUND: Dark navy blue gradient from #213555 (top) to #172540 (bottom). "
        f"Accent color {accent_color} for decorative borders and highlight elements. "
        "Add subtle chalkboard or paper grain texture for organic feel. "
        "\n\n"
        "LAYOUT: Editorial magazine style, slightly asymmetric, hand-crafted feel. "
        "Leave the TOP 30% of the image mostly clear (dark background only) for text overlay. "
        "Leave the CENTER 40% with semi-transparent space for text overlay. "
        "Characters and decorations positioned around the edges and corners. "
        "\n\n"
        f"MAIN CHARACTER (bottom-right): {CHIBI_MASCOT} "
        "\n\n"
        f"GUEST CHARACTER (bottom-left or mid-left): {guest_desc} "
        "The guest character should be interacting with chemistry-related props. "
        "\n\n"
        f"CHEMISTRY VISUAL ELEMENTS (scattered as decoration): {image_prompt} "
        "Show these as visual diagrams, molecular models, beakers, periodic table cards, "
        "or floating chemical symbols. Use sketch-style arrows and rough borders. "
        "\n\n"
        "CRITICAL RULES: "
        "DO NOT render ANY text, words, letters, numbers, or characters in the image. "
        "NO titles, NO labels, NO captions, NO watermarks, NO text of any kind. "
        "The image must be COMPLETELY TEXT-FREE. "
        "All text will be added separately via overlay. "
        "Only visual elements: characters, chemistry props, decorations, backgrounds."
    )
    return prompt


# ── Step 2: AI Visual Generator ──────────────────────────────────────

def _generate_visual(prompt: str) -> Image.Image | None:
    """Generate a text-free visual using Gemini Flash Image.

    Returns a PIL Image or None on failure.
    """
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set, skipping AI visual generation.")
        return None

    try:
        from google import genai
    except ImportError:
        logger.warning("google-genai not installed, skipping AI visual gen.")
        return None

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-3.1-flash-image",
            contents=[prompt],
        )

        for part in response.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                logger.info(
                    "AI visual generated (%dx%d).", image.width, image.height
                )
                return image
            elif part.text is not None:
                logger.info("AI text response: %s", part.text[:200])

        logger.warning("No image data in Gemini response.")
        return None

    except Exception as exc:
        logger.error("AI visual generation failed: %s", exc, exc_info=True)
        return None


# ── Step 3: Text Compositor (Pillow) ─────────────────────────────────

def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = font.getbbox(test_line)
        line_width = bbox[2] - bbox[0]
        if line_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    return lines


def _draw_rounded_rect(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int, int],
) -> None:
    """Draw a rounded rectangle with alpha fill."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def _draw_text_block(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    y: int,
    color: tuple[int, int, int],
    max_width: int,
    center: bool = True,
) -> int:
    """Draw word-wrapped text. Returns the Y position after the last line."""
    lines = _wrap_text(text, font, max_width)

    for line in lines:
        bbox = font.getbbox(line)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        if center:
            x = (IMAGE_WIDTH - line_width) // 2
        else:
            x = (IMAGE_WIDTH - max_width) // 2
        draw.text((x, y), line, fill=color, font=font)
        y += line_height + 10

    return y


def _composite_text(
    bg_image: Image.Image,
    post_type: str,
    image_title: str,
    image_content: str,
    grade_label: str,
    quiz_data: dict | None = None,
) -> Image.Image:
    """Overlay all text onto the AI-generated visual background.

    Creates semi-transparent boxes for readability, then renders text
    using Pillow fonts (guaranteed correct Vietnamese).
    """
    # Ensure RGBA for alpha compositing
    if bg_image.mode != "RGBA":
        bg_image = bg_image.convert("RGBA")

    # Create transparent overlay for text boxes
    overlay = Image.new("RGBA", bg_image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    colors = TEMPLATE_COLORS.get(post_type, TEMPLATE_COLORS["review_question"])
    accent_rgb = _hex_to_rgb(colors["accent"])
    white = (255, 255, 255)
    gold_rgb = _hex_to_rgb(COLORS["gold"])

    type_label = POST_TYPE_LABELS.get(post_type, "LTH CHEMISTRY")
    padding_x = 50
    content_width = IMAGE_WIDTH - padding_x * 2

    # ── Top bar: post type label ──
    top_bar_h = 90
    _draw_rounded_rect(
        draw,
        (0, 0, IMAGE_WIDTH, top_bar_h),
        radius=0,
        fill=(17, 25, 40, 200),  # dark navy, ~78% opacity
    )
    # Accent line at bottom of top bar
    draw.rectangle(
        [0, top_bar_h - 3, IMAGE_WIDTH, top_bar_h],
        fill=(*accent_rgb, 220),
    )

    font_type = _get_font(bold=True, size=26)
    bbox = font_type.getbbox(type_label)
    lw = bbox[2] - bbox[0]
    draw.text(
        ((IMAGE_WIDTH - lw) // 2, 30),
        type_label,
        fill=gold_rgb,
        font=font_type,
    )

    # ── Grade label (below top bar) ──
    font_grade = _get_font(bold=False, size=22)
    bbox_g = font_grade.getbbox(grade_label)
    gw = bbox_g[2] - bbox_g[0]
    draw.text(
        ((IMAGE_WIDTH - gw) // 2, top_bar_h + 15),
        grade_label,
        fill=accent_rgb,
        font=font_grade,
    )

    # ── Main content box (semi-transparent) ──
    content_top = top_bar_h + 55
    content_bottom = IMAGE_HEIGHT - 160 if not quiz_data else IMAGE_HEIGHT - 130
    box_margin = 35
    _draw_rounded_rect(
        draw,
        (box_margin, content_top, IMAGE_WIDTH - box_margin, content_bottom),
        radius=18,
        fill=(17, 25, 40, 170),  # navy, ~67% opacity
    )

    # ── Title ──
    font_title = _get_font(bold=True, size=40)
    title_y = content_top + 25
    title_y = _draw_text_block(
        draw, image_title, font_title, title_y,
        gold_rgb, content_width - 30, center=True,
    )

    # Divider line
    div_y = title_y + 8
    div_x1 = IMAGE_WIDTH // 4
    div_x2 = 3 * IMAGE_WIDTH // 4
    draw.line([(div_x1, div_y), (div_x2, div_y)], fill=(*accent_rgb, 180), width=2)

    # ── Content text ──
    font_content = _get_font(bold=False, size=30)
    text_y = div_y + 18

    if quiz_data:
        # Quiz: show question + 4 options in 2x2 grid
        question = quiz_data.get("question", image_content)
        options = quiz_data.get("options", [])

        # Question text
        text_y = _draw_text_block(
            draw, question, font_content, text_y,
            white, content_width - 40, center=True,
        )
        text_y += 15

        # Options in 2x2 grid
        if len(options) >= 4:
            font_opt = _get_font(bold=False, size=26)
            opt_w = (content_width - 60) // 2
            opt_h = 55
            gap = 12
            grid_x = box_margin + 25

            for i, opt_text in enumerate(options[:4]):
                row = i // 2
                col = i % 2
                ox = grid_x + col * (opt_w + gap)
                oy = text_y + row * (opt_h + gap)

                # Option box
                _draw_rounded_rect(
                    draw,
                    (ox, oy, ox + opt_w, oy + opt_h),
                    radius=10,
                    fill=(*accent_rgb, 60),
                )
                # Option border
                draw.rounded_rectangle(
                    (ox, oy, ox + opt_w, oy + opt_h),
                    radius=10,
                    outline=(*accent_rgb, 140),
                    width=1,
                )
                # Option text
                draw.text(
                    (ox + 12, oy + 13),
                    opt_text,
                    fill=white,
                    font=font_opt,
                )
    else:
        # Normal post: just show content
        _draw_text_block(
            draw, image_content, font_content, text_y,
            white, content_width - 40, center=True,
        )

    # ── Bottom brand bar ──
    bar_h = 55
    bar_y = IMAGE_HEIGHT - bar_h
    _draw_rounded_rect(
        draw,
        (0, bar_y, IMAGE_WIDTH, IMAGE_HEIGHT),
        radius=0,
        fill=(17, 25, 40, 200),
    )
    # Top accent line
    draw.rectangle(
        [0, bar_y, IMAGE_WIDTH, bar_y + 3],
        fill=(*accent_rgb, 220),
    )
    font_brand = _get_font(bold=False, size=18)
    draw.text(
        (padding_x, bar_y + 18),
        "fb.com/LTHChemistry",
        fill=(200, 200, 200),
        font=font_brand,
    )

    # Composite overlay onto background
    result = Image.alpha_composite(bg_image, overlay)
    return result


# ── Step 4: OCR Validator ────────────────────────────────────────────

def _validate_no_garbled_text(image: Image.Image) -> bool:
    """Use Gemini Vision to check if the AI visual contains garbled text.

    Returns True if image is clean (no garbled text), False if problems found.
    """
    if not GEMINI_API_KEY:
        logger.info("No API key for OCR validation, skipping check.")
        return True

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        logger.info("google-genai not installed, skipping OCR validation.")
        return True

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Convert PIL image to bytes for the API
        buf = BytesIO()
        image.save(buf, format="PNG")
        image_bytes = buf.getvalue()

        response = client.models.generate_content(
            model=OCR_VISION_MODEL,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                (
                    "Examine this image carefully. Look for ANY text, words, letters, "
                    "or numbers rendered IN the image itself (not overlaid text boxes). "
                    "If you find text that is garbled, misspelled, broken, or nonsensical "
                    "(like random letter combinations that don't form real words), "
                    "respond with EXACTLY: GARBLED_TEXT_FOUND\n"
                    "If the image is clean (no text at all, or only correctly spelled text), "
                    "respond with EXACTLY: IMAGE_CLEAN\n"
                    "Respond with only one of those two phrases, nothing else."
                ),
            ],
        )

        result_text = response.text.strip().upper()
        if "GARBLED" in result_text:
            logger.warning("OCR validator found garbled text in AI visual.")
            return False

        logger.info("OCR validator: image is clean.")
        return True

    except Exception as exc:
        logger.warning("OCR validation failed (non-critical): %s", exc)
        return True  # don't block pipeline on OCR failure


# ── Step 5: Logo Overlay ─────────────────────────────────────────────

def _overlay_logo(img: Image.Image) -> Image.Image:
    """Place the LTH Chemistry logo at bottom-right corner."""
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
    except (FileNotFoundError, IOError):
        logger.warning("Logo not found at %s, skipping overlay.", LOGO_PATH)
        return img

    # Scale logo to fit max height while keeping aspect ratio
    aspect = logo.width / logo.height
    new_height = LOGO_MAX_HEIGHT
    new_width = int(new_height * aspect)
    logo = logo.resize((new_width, new_height), Image.LANCZOS)

    # Position: bottom-right, above the brand bar
    padding = 30
    x = img.width - new_width - padding
    y = img.height - new_height - padding - 55  # above brand bar

    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img.paste(logo, (x, y), logo)

    return img




# ── Constants ────────────────────────────────────────────────────────

AI_GEN_MAX_RETRIES = 3       # max retries when Nano Banana API fails
AI_GEN_RETRY_DELAY = 10      # seconds between retries


# ── Main entry point ─────────────────────────────────────────────────

def create_post_image(
    post_type: str,
    image_title: str,
    image_content: str,
    grade_label: str,
    image_prompt: str,
    filename: str,
    last_character: str | None = None,
    quiz_data: dict | None = None,
) -> tuple[Path | None, str | None]:
    """
    Create a post image using the Nano Banana pipeline (mandatory).

    Pipeline:
      1. Pick chibi guest character
      2. Rewrite prompt (no text + chibi)
      3. Generate AI visual via Nano Banana (text-free) — REQUIRED
      4. OCR validate (regen if garbled text detected)
      5. Overlay text via Pillow
      6. Overlay logo
      7. Save

    If Nano Banana fails after all retries, returns (None, None)
    and the post is skipped entirely. There is NO fallback.

    Args:
        post_type: One of the post types (quiz_mcq, review_question, etc.)
        image_title: Short title for the image header
        image_content: Main content text
        grade_label: Grade/subject label (e.g., "Hóa Học Lớp 10")
        image_prompt: English prompt for AI image generation
        filename: Output filename (without path)
        last_character: Name of the last used guest character (to avoid repeats)
        quiz_data: Optional dict with question/options/answer for quiz posts

    Returns:
        Tuple of (path_to_image, guest_character_name) or (None, None) on failure.
    """
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / filename

        # Step 1: Pick guest character
        guest_name, guest_desc = pick_guest_character(post_type, last_character)
        logger.info("Guest character: %s", guest_name)

        # Step 2: Rewrite prompt
        visual_prompt = _rewrite_prompt_for_visual(
            image_prompt, post_type, guest_name, guest_desc
        )

        # Step 3: Generate AI visual via Nano Banana (mandatory, with retries)
        bg_image = None

        for attempt in range(1, AI_GEN_MAX_RETRIES + 1):
            # Generate visual via Nano Banana
            ai_visual = _generate_visual(visual_prompt)

            if ai_visual is not None:
                # Resize to target dimensions
                ai_visual = ai_visual.resize(
                    (IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS
                )

                # Step 4: OCR validate the raw AI visual (before text overlay)
                if _validate_no_garbled_text(ai_visual):
                    bg_image = ai_visual
                    logger.info("Nano Banana visual accepted (attempt %d).", attempt)
                    break
                else:
                    logger.warning(
                        "Garbled text detected, regenerating (attempt %d/%d)...",
                        attempt, AI_GEN_MAX_RETRIES,
                    )
            else:
                logger.warning(
                    "Nano Banana returned None (attempt %d/%d).",
                    attempt, AI_GEN_MAX_RETRIES,
                )

            # Wait before retry (skip delay on last attempt)
            if attempt < AI_GEN_MAX_RETRIES:
                logger.info("Waiting %ds before retry...", AI_GEN_RETRY_DELAY)
                time.sleep(AI_GEN_RETRY_DELAY)

        # NO FALLBACK — Nano Banana is mandatory
        if bg_image is None:
            logger.error(
                "Nano Banana failed after %d attempts. "
                "Skipping post (no fallback).",
                AI_GEN_MAX_RETRIES,
            )
            return None, None

        # Step 5: Composite text overlay
        img = _composite_text(
            bg_image, post_type, image_title, image_content,
            grade_label, quiz_data=quiz_data,
        )

        # Step 6: Logo overlay
        img = _overlay_logo(img)

        # Save as PNG (flatten to RGB)
        final = Image.new("RGB", img.size, (255, 255, 255))
        final.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
        final.save(str(output_path), "PNG", quality=95)

        logger.info("Image created: %s (character: %s)", output_path, guest_name)
        return output_path, guest_name

    except Exception as exc:
        logger.error("Failed to create image: %s", exc, exc_info=True)
        return None, None
