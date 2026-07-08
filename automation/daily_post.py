#!/usr/bin/env python3
"""
LTH Chemistry – Daily Facebook Post Automation

Main orchestrator that runs daily via GitHub Actions:
1. Check state (prevent double-posting)
2. Generate content via Gemini API
3. Create branded images with logo
4. Post to Facebook Page (THCS morning, THPT evening)
5. Advance rotation state
"""

import argparse
import logging
import sys

from config import (
    THCS_POST_HOUR,
    THCS_POST_MINUTE,
    THPT_POST_HOUR,
    THPT_POST_MINUTE,
)
from state_manager import load_state, save_state, get_today_info, advance_state, should_post_today
from content_generator import generate_content
from image_generator import create_post_image
from facebook_poster import post_photo_now, schedule_photo, verify_token

# ── Logging ───────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("daily_post")


def run(dry_run: bool = False) -> bool:
    """
    Execute the daily post pipeline.

    Args:
        dry_run: If True, generate content and images but don't post to Facebook.

    Returns:
        True if successful, False otherwise.
    """
    logger.info("=" * 60)
    logger.info("LTH Chemistry Daily Post – Starting")
    logger.info("=" * 60)

    # ── Step 0: Load state and check if we already posted today ───
    state = load_state()

    if not should_post_today(state):
        return True  # Not an error, just already done

    # ── Step 0.5: Verify Facebook token ───────────────────────────
    if not dry_run:
        if not verify_token():
            logger.error("Facebook token invalid. Aborting.")
            return False

    # ── Step 1: Determine today's content parameters ──────────────
    today = get_today_info(state)
    logger.info(
        "Today: %s | Type: %s | THCS: Lớp %d Ch.%d | THPT: Lớp %d Ch.%d",
        today["date_display"],
        today["post_type"],
        today["thcs_grade"],
        today["thcs_chapter"],
        today["thpt_grade"],
        today["thpt_chapter"],
    )

    # ── Step 2: Generate content via Gemini ───────────────────────
    logger.info("Generating content...")
    content = generate_content(today)

    if content is None:
        logger.error("Content generation failed. Skipping today.")
        return False

    thcs = content["thcs_post"]
    thpt = content["thpt_post"]

    logger.info("THCS caption preview: %s...", thcs["caption"][:80])
    logger.info("THPT caption preview: %s...", thpt["caption"][:80])

    # ── Step 3: Create images ─────────────────────────────────────
    logger.info("Creating images...")

    thcs_image = create_post_image(
        post_type=today["post_type"],
        image_title=thcs["image_title"],
        image_content=thcs["image_content"],
        grade_label=thcs["grade_label"],
        filename=f"{today['date']}_thcs.png",
    )

    thpt_image = create_post_image(
        post_type=today["post_type"],
        image_title=thpt["image_title"],
        image_content=thpt["image_content"],
        grade_label=thpt["grade_label"],
        filename=f"{today['date']}_thpt.png",
    )

    if thcs_image is None or thpt_image is None:
        logger.error("Image generation failed. Skipping today.")
        return False

    logger.info("Images created: %s, %s", thcs_image.name, thpt_image.name)

    # ── Step 4: Post to Facebook ──────────────────────────────────
    if dry_run:
        logger.info("[DRY RUN] Would post THCS at %02d:%02d", THCS_POST_HOUR, THCS_POST_MINUTE)
        logger.info("[DRY RUN] Would post THPT at %02d:%02d", THPT_POST_HOUR, THPT_POST_MINUTE)
        logger.info("[DRY RUN] THCS caption:\n%s\n%s", thcs["caption"], thcs["hashtags"])
        logger.info("[DRY RUN] THPT caption:\n%s\n%s", thpt["caption"], thpt["hashtags"])
    else:
        # THCS post: schedule for morning
        thcs_caption = f"{thcs['caption']}\n\n{thcs['hashtags']}"
        thcs_result = schedule_photo(
            image_path=str(thcs_image),
            caption=thcs_caption,
            hour=THCS_POST_HOUR,
            minute=THCS_POST_MINUTE,
        )

        if thcs_result is None:
            logger.error("Failed to post THCS content.")
            return False

        # THPT post: schedule for evening
        thpt_caption = f"{thpt['caption']}\n\n{thpt['hashtags']}"
        thpt_result = schedule_photo(
            image_path=str(thpt_image),
            caption=thpt_caption,
            hour=THPT_POST_HOUR,
            minute=THPT_POST_MINUTE,
        )

        if thpt_result is None:
            logger.error("Failed to post THPT content.")
            return False

    # ── Step 5: Advance state ─────────────────────────────────────
    state = advance_state(state)
    save_state(state)

    logger.info("=" * 60)
    logger.info("Daily post complete. Total posts to date: %d", state["posts_count"])
    logger.info("=" * 60)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="LTH Chemistry Daily Facebook Post")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate content and images without posting to Facebook.",
    )
    args = parser.parse_args()

    success = run(dry_run=args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
