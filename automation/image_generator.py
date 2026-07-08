"""
Image generator: creates branded post images using Pillow.
Each post type has a distinct color scheme and layout.
Logo is always placed at bottom-right.
"""

import logging
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config import (
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    LOGO_PATH,
    LOGO_MAX_HEIGHT,
    FONT_REGULAR,
    FONT_BOLD,
    TEMPLATE_COLORS,
    POST_TYPE_LABELS,
    OUTPUT_DIR,
)

logger = logging.getLogger(__name__)

# Fallback font if custom font not available
_font_cache: dict[str, ImageFont.FreeTypeFont] = {}


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


def _draw_gradient(draw: ImageDraw.ImageDraw, width: int, height: int,
                   top_color: str, bottom_color: str) -> None:
    """Draw a vertical gradient background."""
    r1, g1, b1 = _hex_to_rgb(top_color)
    r2, g2, b2 = _hex_to_rgb(bottom_color)

    for y in range(height):
        ratio = y / height
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))


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


def _draw_centered_text(draw: ImageDraw.ImageDraw, text: str,
                        font: ImageFont.FreeTypeFont, y: int,
                        color: str, max_width: int) -> int:
    """Draw centered, word-wrapped text. Returns the Y position after text."""
    lines = _wrap_text(text, font, max_width)
    rgb = _hex_to_rgb(color)

    for line in lines:
        bbox = font.getbbox(line)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        x = (IMAGE_WIDTH - line_width) // 2
        draw.text((x, y), line, fill=rgb, font=font)
        y += line_height + 12

    return y


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

    # Position: bottom-right with padding
    padding = 30
    x = IMAGE_WIDTH - new_width - padding
    y = IMAGE_HEIGHT - new_height - padding

    # Composite onto image
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img.paste(logo, (x, y), logo)

    return img


def _draw_decorative_circles(draw: ImageDraw.ImageDraw, accent_color: str) -> None:
    """Add subtle decorative circles for visual interest."""
    rgb = _hex_to_rgb(accent_color)
    # Semi-transparent effect via lighter color
    light = tuple(min(255, c + 100) for c in rgb)

    # Top-left circle (partially off-screen)
    draw.ellipse([-60, -60, 120, 120], fill=(*light, 30), outline=None)
    # Bottom-left circle
    draw.ellipse([-40, IMAGE_HEIGHT - 160, 140, IMAGE_HEIGHT + 40],
                 fill=(*light, 25), outline=None)
    # Top-right small circle
    draw.ellipse([IMAGE_WIDTH - 100, 30, IMAGE_WIDTH - 20, 110],
                 fill=(*light, 20), outline=None)


def create_post_image(
    post_type: str,
    image_title: str,
    image_content: str,
    grade_label: str,
    filename: str,
) -> Path | None:
    """
    Create a branded post image.

    Args:
        post_type: One of the 7 post types (review_question, etc.)
        image_title: Short title for the image header
        image_content: Main content text
        grade_label: Grade/subject label (e.g., "Hóa Học Lớp 10")
        filename: Output filename (without path)

    Returns:
        Path to the created image, or None on failure.
    """
    try:
        colors = TEMPLATE_COLORS.get(post_type, TEMPLATE_COLORS["review_question"])
        type_label = POST_TYPE_LABELS.get(post_type, "LTH CHEMISTRY")

        # Create image with gradient background
        img = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT))
        draw = ImageDraw.Draw(img)

        _draw_gradient(draw, IMAGE_WIDTH, IMAGE_HEIGHT,
                       colors["bg_top"], colors["bg_bottom"])

        # Decorative elements
        _draw_decorative_circles(draw, colors["accent"])

        # ── Top bar: post type label ──────────────────────────────
        top_bar_height = 100
        accent_rgb = _hex_to_rgb(colors["accent"])
        draw.rectangle(
            [0, 0, IMAGE_WIDTH, top_bar_height],
            fill=(*accent_rgb, 60),
        )

        font_type_label = _get_font(bold=True, size=28)
        bbox = font_type_label.getbbox(type_label)
        lw = bbox[2] - bbox[0]
        draw.text(
            ((IMAGE_WIDTH - lw) // 2, 35),
            type_label,
            fill=_hex_to_rgb(colors["text"]),
            font=font_type_label,
        )

        # ── Grade label (below top bar) ───────────────────────────
        font_grade = _get_font(bold=False, size=24)
        bbox = font_grade.getbbox(grade_label)
        gw = bbox[2] - bbox[0]
        draw.text(
            ((IMAGE_WIDTH - gw) // 2, 120),
            grade_label,
            fill=(*_hex_to_rgb(colors["accent"]),),
            font=font_grade,
        )

        # ── Divider line ──────────────────────────────────────────
        div_y = 165
        draw.line(
            [(IMAGE_WIDTH // 4, div_y), (3 * IMAGE_WIDTH // 4, div_y)],
            fill=(*_hex_to_rgb(colors["accent"]),),
            width=2,
        )

        # ── Image title ──────────────────────────────────────────
        font_title = _get_font(bold=True, size=44)
        title_y = _draw_centered_text(
            draw, image_title, font_title, 200,
            colors["text"], IMAGE_WIDTH - 120,
        )

        # ── Main content ─────────────────────────────────────────
        font_content = _get_font(bold=False, size=34)
        content_y = max(title_y + 30, 340)
        _draw_centered_text(
            draw, image_content, font_content, content_y,
            colors["text"], IMAGE_WIDTH - 100,
        )

        # ── Bottom area: branding ─────────────────────────────────
        bottom_bar_y = IMAGE_HEIGHT - 120
        draw.rectangle(
            [0, bottom_bar_y, IMAGE_WIDTH, IMAGE_HEIGHT],
            fill=(*accent_rgb, 40),
        )

        font_brand = _get_font(bold=False, size=20)
        brand_text = "fb.com/LTHChemistry"
        bbox = font_brand.getbbox(brand_text)
        bw = bbox[2] - bbox[0]
        draw.text(
            (40, bottom_bar_y + 50),
            brand_text,
            fill=(*_hex_to_rgb(colors["text"]),),
            font=font_brand,
        )

        # ── Overlay logo ─────────────────────────────────────────
        img = _overlay_logo(img)

        # ── Save ──────────────────────────────────────────────────
        output_path = OUTPUT_DIR / filename
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Convert to RGB for JPEG/PNG compatibility
        final = Image.new("RGB", img.size, (255, 255, 255))
        final.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
        final.save(str(output_path), "PNG", quality=95)

        logger.info("Image created: %s", output_path)
        return output_path

    except Exception as exc:
        logger.error("Failed to create image: %s", exc, exc_info=True)
        return None
