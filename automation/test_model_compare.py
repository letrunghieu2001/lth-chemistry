"""
Quick test: Compare image generation between gemini-3-pro-image (paid) and gemini-2.5-flash (free).
Generates one image with each model, saves to output/, and creates an HTML comparison page.
"""

import os, sys, base64, logging
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Simple test prompt (similar to what the pipeline generates)
TEST_PROMPT = """
Create a cute chibi-style educational chemistry infographic poster.

Theme: "Bảng tuần hoàn các nguyên tố" (Periodic Table of Elements)
Style: Anime/chibi art, vibrant colors, navy blue and teal background.
Characters: A cute chibi teacher character wearing a lab coat holding a beaker.
Layout: Clean, professional, with chemistry icons (atoms, molecules, beakers).
Size: 1080x1080 pixels, square format for social media.
Text: DO NOT include any text in the image. Leave blank spaces where text would go.
"""

MODELS_TO_TEST = [
    ("gemini-3.5-flash", "FREE tier text model + image output"),
]


def generate_image(model_name: str) -> bytes | None:
    """Generate an image using specified model."""
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)

        logger.info("Generating image with %s ...", model_name)
        resp = client.models.generate_content(
            model=model_name,
            contents=[TEST_PROMPT],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        parts = getattr(resp, "parts", None)
        if not parts:
            logger.warning("%s: No parts returned (safety filter?)", model_name)
            return None

        for part in parts:
            inline = getattr(part, "inline_data", None)
            if inline and hasattr(inline, "data"):
                logger.info("%s: Image generated successfully! (%d bytes)", model_name, len(inline.data))
                return inline.data

        logger.warning("%s: Response had parts but no image data.", model_name)
        # Log text response if any
        if hasattr(resp, 'text'):
            logger.info("%s text response: %s", model_name, resp.text[:200])
        return None

    except Exception as exc:
        logger.error("%s failed: %s", model_name, exc)
        return None


def create_html_preview(results: list[dict]):
    """Create an HTML comparison page."""
    cards_html = ""
    for r in results:
        if r["image_path"]:
            img_tag = f'<img src="{r["image_path"].name}" alt="{r["model"]}" style="max-width:100%; border-radius:12px;">'
        else:
            img_tag = '<div style="height:400px; display:flex; align-items:center; justify-content:center; background:#1a1a2e; border-radius:12px; color:#e94560;">❌ Generation Failed</div>'

        cards_html += f"""
        <div style="flex:1; min-width:300px; max-width:540px; background:#16213e; border-radius:16px; padding:20px; box-shadow:0 8px 32px rgba(0,0,0,0.3);">
            <h2 style="color:#e94560; margin:0 0 4px;">{r['model']}</h2>
            <p style="color:#a8a8b3; margin:0 0 16px; font-size:14px;">{r['tier']} | {r['size_kb']} KB</p>
            {img_tag}
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Image Model Comparison</title>
    <style>
        body {{ margin:0; padding:40px; background:#0f0f23; color:#fff; font-family:'Inter',sans-serif; }}
        h1 {{ text-align:center; color:#e94560; margin-bottom:8px; }}
        .subtitle {{ text-align:center; color:#a8a8b3; margin-bottom:32px; }}
        .grid {{ display:flex; gap:24px; justify-content:center; flex-wrap:wrap; }}
    </style>
</head>
<body>
    <h1>🧪 LTH Chemistry – Image Model Comparison</h1>
    <p class="subtitle">So sánh chất lượng ảnh giữa các model Gemini</p>
    <div class="grid">{cards_html}</div>
</body>
</html>"""

    preview_path = OUTPUT_DIR / "model_comparison.html"
    preview_path.write_text(html, encoding="utf-8")
    logger.info("Preview saved: %s", preview_path)
    return preview_path


def main():
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set in .env!")
        sys.exit(1)

    results = []
    for model_name, tier in MODELS_TO_TEST:
        img_data = generate_image(model_name)
        img_path = None
        size_kb = "0"

        if img_data:
            img_path = OUTPUT_DIR / f"test_{model_name.replace('-', '_')}.png"
            img_path.write_bytes(img_data)
            size_kb = f"{len(img_data) / 1024:.0f}"
            logger.info("Saved: %s", img_path)

        results.append({
            "model": model_name,
            "tier": tier,
            "image_path": img_path,
            "size_kb": size_kb,
        })

    preview = create_html_preview(results)
    print(f"\n✅ Done! Open: {preview}")


if __name__ == "__main__":
    main()
