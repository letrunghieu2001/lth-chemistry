"""
Full E2E test: Generate content + image for one sample post.
Outputs caption + image for review.
"""
import os
import sys
import json
import logging

# Fix Windows terminal encoding for emoji/Vietnamese
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Ensure automation dir is on path
sys.path.insert(0, os.path.dirname(__file__))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("e2e_test")

from state_manager import load_state, get_today_info
from content_generator import generate_content
from image_generator import create_post_image


def main():
    logger.info("=" * 60)
    logger.info("  LTH Chemistry - Full Pipeline E2E Test")
    logger.info("=" * 60)

    # Step 1: Get today's info
    state = load_state()
    today_info = get_today_info(state)

    logger.info("Today: %s", today_info["date_display"])
    logger.info(
        "THCS: Lớp %d, Chương %d, Type: %s",
        today_info["thcs_grade"],
        today_info["thcs_chapter"],
        today_info["thcs_post_type"],
    )
    logger.info(
        "THPT: Lớp %d, Chương %d, Type: %s",
        today_info["thpt_grade"],
        today_info["thpt_chapter"],
        today_info["thpt_post_type"],
    )

    # Step 2: Generate content via Gemini 3.5 Flash
    logger.info("\n--- Step 2: Generating content (Gemini 3.5 Flash) ---")
    content = generate_content(today_info)

    if content is None:
        logger.error("Content generation FAILED. Aborting.")
        return

    logger.info("Content generated successfully!")

    # Step 3: Generate images for both posts
    for post_key in ["thcs_post", "thpt_post"]:
        post = content[post_key]
        label = "THCS" if "thcs" in post_key else "THPT"

        logger.info("\n--- Step 3: Generating image for %s ---", label)

        img_path = create_post_image(
            post_type=today_info[f"{post_key.replace('_post', '')}_post_type"],
            image_title=post.get("image_title", "LTH Chemistry"),
            image_content=post.get("image_content", ""),
            grade_label=post.get("grade_label", ""),
            image_prompt=post.get("image_prompt", ""),
            filename=f"test_{label.lower()}_post.png",
        )

        if img_path:
            logger.info("Image saved: %s", img_path)
        else:
            logger.warning("Image generation failed for %s", label)

        # Print the post content for review
        print(f"\n{'='*60}")
        print(f"📝 {label} POST PREVIEW")
        print(f"{'='*60}")
        print(f"\n📸 Caption:\n{post.get('caption', 'N/A')}")
        print(f"\n#️⃣  Hashtags:\n{post.get('hashtags', 'N/A')}")
        print(f"\n🖼️  Image Title: {post.get('image_title', 'N/A')}")
        print(f"📐 Image Content: {post.get('image_content', 'N/A')}")
        print(f"\n🎨 Image Prompt:\n{post.get('image_prompt', 'N/A')[:300]}...")
        if post.get("question"):
            print(f"\n❓ Quiz Question: {post['question']}")
            print(f"   Options: {post.get('options', [])}")
            print(f"   Answer: {post.get('answer', 'N/A')}")
        print(f"\n📁 Image file: {img_path or 'FAILED'}")

    logger.info("\n✅ E2E Test completed!")


if __name__ == "__main__":
    main()
