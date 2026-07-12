"""
Generate a sample post image via Nano Banana and create
an HTML preview simulating a Facebook post.

Usage:
    $env:GEMINI_API_KEY="your-key"; python test_preview.py
"""

import base64
import logging
import os
import sys
from pathlib import Path

# ── Bootstrap ────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(name)s  %(message)s",
)
logger = logging.getLogger("test_preview")

# Ensure GEMINI_API_KEY is available
if not os.environ.get("GEMINI_API_KEY"):
    print("\n❌  GEMINI_API_KEY not set!")
    print("   Run:  $env:GEMINI_API_KEY=\"your-key\"; python test_preview.py\n")
    sys.exit(1)

from image_generator import create_post_image

# ── Sample content (Vietnamese chemistry) ────────────────────────────

SAMPLE_POSTS = [
    {
        "post_type": "quiz_mcq",
        "image_title": "NỒNG ĐỘ DUNG DỊCH",
        "image_content": "Hòa tan m gam NaCl vào 200g nước thu được dung dịch có nồng độ 10%",
        "grade_label": "KHTN Lớp 9",
        "image_prompt": (
            "Chemistry laboratory scene with a glass beaker containing salt dissolving "
            "in water, concentration percentage symbols floating around, a digital scale "
            "showing mass measurement, molecular models of NaCl (sodium chloride) crystal "
            "structure breaking apart in water"
        ),
        "filename": "preview_quiz.png",
        "quiz_data": {
            "question": "Hòa tan m gam NaCl vào 200g nước thu được dung dịch có nồng độ 10%. Giá trị của m là?",
            "options": [
                "A. 20,0 gam",
                "B. 22,2 gam",
                "C. 25,0 gam",
                "D. 18,5 gam",
            ],
            "answer": "B",
        },
    },
    {
        "post_type": "fun_facts",
        "image_title": "Bạn có biết: Nước là dung môi vạn năng?",
        "image_content": (
            "Nước có thể hòa tan nhiều chất nhất trong tự nhiên. "
            "Do phân tử nước có tính phân cực mạnh, nó có thể phá vỡ "
            "liên kết ion và hòa tan hầu hết các muối vô cơ."
        ),
        "grade_label": "Hóa Học Lớp 10",
        "image_prompt": (
            "A magical water molecule (H2O) shown as a cute character with "
            "two hydrogen atoms and one oxygen atom, dissolving colorful salt "
            "crystals, rainbow colors flowing in the water, molecular bonds "
            "breaking apart with sparkle effects"
        ),
        "filename": "preview_funfact.png",
        "quiz_data": None,
    },
]


def generate_facebook_html(posts_data: list[dict]) -> str:
    """Create an HTML page that simulates Facebook post previews."""

    cards_html = ""
    for post in posts_data:
        img_path = post.get("image_path")
        if not img_path or not Path(img_path).exists():
            continue

        # Read image and convert to base64 for embedding
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()

        caption = post.get("caption", "")
        character = post.get("character", "unknown")
        post_type = post.get("post_type", "")

        cards_html += f"""
        <div class="fb-post">
            <div class="fb-header">
                <div class="fb-avatar">LTH</div>
                <div class="fb-meta">
                    <div class="fb-page-name">LTH Chemistry</div>
                    <div class="fb-time">Vừa xong · <span class="globe">🌐</span></div>
                </div>
                <div class="fb-dots">···</div>
            </div>
            <div class="fb-caption">{caption}</div>
            <div class="fb-image-wrapper">
                <img src="data:image/png;base64,{img_b64}" alt="Post image" />
            </div>
            <div class="fb-stats">
                <span>❤️ 42</span>
                <span>💬 8 bình luận · 3 chia sẻ</span>
            </div>
            <div class="fb-actions">
                <button>👍 Thích</button>
                <button>💬 Bình luận</button>
                <button>↗️ Chia sẻ</button>
            </div>
            <div class="fb-debug">
                <span class="tag">🎨 Nano Banana</span>
                <span class="tag">🐱 {character}</span>
                <span class="tag">📝 {post_type}</span>
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LTH Chemistry - Facebook Post Preview</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap');

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #18191A;
            color: #E4E6EB;
            min-height: 100vh;
            padding: 20px;
        }}

        h1 {{
            text-align: center;
            font-size: 1.8rem;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #0BA5A5, #FFBF00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .subtitle {{
            text-align: center;
            color: #8a8d91;
            margin-bottom: 30px;
            font-size: 0.95rem;
        }}

        .container {{
            max-width: 580px;
            margin: 0 auto;
        }}

        .fb-post {{
            background: #242526;
            border-radius: 12px;
            margin-bottom: 24px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        }}

        .fb-header {{
            display: flex;
            align-items: center;
            padding: 14px 16px 8px;
            gap: 10px;
        }}

        .fb-avatar {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: linear-gradient(135deg, #213555, #0BA5A5);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
            color: #FFBF00;
            flex-shrink: 0;
        }}

        .fb-meta {{
            flex: 1;
        }}

        .fb-page-name {{
            font-weight: 700;
            font-size: 15px;
            color: #E4E6EB;
        }}

        .fb-time {{
            font-size: 13px;
            color: #8a8d91;
        }}

        .fb-dots {{
            color: #8a8d91;
            font-size: 20px;
            cursor: pointer;
            padding: 4px 8px;
        }}

        .fb-caption {{
            padding: 0 16px 12px;
            font-size: 15px;
            line-height: 1.5;
            white-space: pre-line;
        }}

        .fb-image-wrapper {{
            width: 100%;
            line-height: 0;
        }}

        .fb-image-wrapper img {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .fb-stats {{
            display: flex;
            justify-content: space-between;
            padding: 10px 16px;
            font-size: 14px;
            color: #8a8d91;
            border-bottom: 1px solid #3E4042;
        }}

        .fb-actions {{
            display: flex;
            padding: 6px 8px;
        }}

        .fb-actions button {{
            flex: 1;
            background: none;
            border: none;
            color: #8a8d91;
            font-size: 14px;
            font-weight: 600;
            padding: 8px;
            border-radius: 6px;
            cursor: pointer;
            font-family: inherit;
            transition: background 0.15s;
        }}

        .fb-actions button:hover {{
            background: #3A3B3C;
        }}

        .fb-debug {{
            display: flex;
            gap: 8px;
            padding: 8px 16px 12px;
            flex-wrap: wrap;
        }}

        .tag {{
            background: #3A3B3C;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            color: #0BA5A5;
        }}

        .status-bar {{
            text-align: center;
            padding: 16px;
            margin-bottom: 20px;
            background: #242526;
            border-radius: 12px;
            font-size: 14px;
        }}

        .status-bar .success {{ color: #33A06A; }}
        .status-bar .fail {{ color: #D94444; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 LTH Chemistry Preview</h1>
        <p class="subtitle">Facebook Post Preview — Nano Banana Pipeline</p>
        {cards_html}
    </div>
</body>
</html>"""


def main():
    results = []

    for i, sample in enumerate(SAMPLE_POSTS):
        logger.info("=" * 60)
        logger.info("Generating post %d/%d: %s", i + 1, len(SAMPLE_POSTS), sample["post_type"])
        logger.info("=" * 60)

        path, character = create_post_image(
            post_type=sample["post_type"],
            image_title=sample["image_title"],
            image_content=sample["image_content"],
            grade_label=sample["grade_label"],
            image_prompt=sample["image_prompt"],
            filename=sample["filename"],
            last_character=results[-1]["character"] if results else None,
            quiz_data=sample.get("quiz_data"),
        )

        if path is None:
            logger.error("❌ Post %d FAILED (Nano Banana unavailable)", i + 1)
            continue

        # Build Facebook-style caption
        label = {
            "quiz_mcq": "📝 TRẮC NGHIỆM HÓA HỌC",
            "fun_facts": "🔬 CÓ BIẾT KHÔNG?",
        }.get(sample["post_type"], "🧪 LTH CHEMISTRY")

        caption = (
            f"{label}\n\n"
            f"📌 {sample['image_title']}\n\n"
            f"{sample['image_content']}\n\n"
            f"👉 Comment đáp án bên dưới nhé!\n"
            f"#LTHChemistry #HoaHoc #{sample['grade_label'].replace(' ', '')}"
        )

        results.append({
            "image_path": str(path),
            "caption": caption,
            "character": character,
            "post_type": sample["post_type"],
        })
        logger.info("✅ Post %d done: %s (character: %s)", i + 1, path, character)

    if not results:
        logger.error("No posts generated. Check GEMINI_API_KEY and API status.")
        sys.exit(1)

    # Generate HTML preview
    html = generate_facebook_html(results)
    html_path = Path(__file__).parent / "output" / "facebook_preview.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")

    logger.info("=" * 60)
    logger.info("🎉 HTML preview saved: %s", html_path)
    logger.info("   Open in browser to see Facebook-style preview!")
    logger.info("=" * 60)

    print(f"\n✅ Preview ready: {html_path}")
    print(f"   Generated {len(results)} posts with Nano Banana")


if __name__ == "__main__":
    main()
