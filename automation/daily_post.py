#!/usr/bin/env python3
"""
LTH Chemistry – Daily Facebook Post Automation

Main orchestrator that runs daily via GitHub Actions:
1. Check state (prevent double-posting)
2. Generate content via Gemini API (text + image prompts)
3. Create AI-generated images with logo overlay
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
    POST_TYPE_LABELS,
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


def run(dry_run: bool = False, force: bool = False) -> bool:
    """
    Execute the daily post pipeline.

    Args:
        dry_run: If True, generate content and images but don't post to Facebook.
        force: If True, skip the already-posted-today check.

    Returns:
        True if successful, False otherwise.
    """
    logger.info("=" * 60)
    logger.info("LTH Chemistry Daily Post – Starting (v2)")
    logger.info("=" * 60)

    # ── Step 0: Load state and check if we already posted today ───
    state = load_state()

    if not force and not should_post_today(state):
        return True  # Not an error, just already done

    # ── Step 0.5: Verify Facebook token ───────────────────────────
    if not dry_run:
        if not verify_token():
            logger.error("Facebook token invalid. Aborting.")
            return False

    # ── Step 1: Determine today's content parameters ──────────────
    today = get_today_info(state)
    thcs_label = POST_TYPE_LABELS.get(today["thcs_post_type"], today["thcs_post_type"])
    thpt_label = POST_TYPE_LABELS.get(today["thpt_post_type"], today["thpt_post_type"])

    logger.info(
        "Today: %s | THCS: Lớp %d Ch.%d [%s] | THPT: Lớp %d Ch.%d [%s]",
        today["date_display"],
        today["thcs_grade"],
        today["thcs_chapter"],
        thcs_label,
        today["thpt_grade"],
        today["thpt_chapter"],
        thpt_label,
    )

    # ── Step 2: Generate content via Gemini ───────────────────────
    logger.info("Generating content...")
    content = generate_content(today)

    if content is None:
        logger.error("Content generation failed. Skipping today.")
        return False

    thcs = content["thcs_post"]
    thpt = content["thpt_post"]

    logger.info("THCS status preview: %s...", thcs["status"][:80])
    logger.info("THPT status preview: %s...", thpt["status"][:80])

    # ── Step 3: Create images (AI-generated diagrams + chibi stickers) ──
    logger.info("Creating images...")

    recent_chars = today.get("recent_characters", [])

    # Build quiz_data if applicable
    thcs_quiz = None
    if today["thcs_post_type"] == "quiz_mcq":
        thcs_quiz = {
            "question": thcs.get("question", ""),
            "options": thcs.get("options", []),
            "answer": thcs.get("answer", ""),
        }

    thpt_quiz = None
    if today["thpt_post_type"] == "quiz_mcq":
        thpt_quiz = {
            "question": thpt.get("question", ""),
            "options": thpt.get("options", []),
            "answer": thpt.get("answer", ""),
        }

    thcs_image, thcs_chars = create_post_image(
        post_type=today["thcs_post_type"],
        image_title=thcs["image_title"],
        layout_type=thcs.get("layout_type", ""),
        diagram_data=thcs.get("diagram_data", {}),
        grade_label=thcs["grade_label"],
        image_prompt=thcs.get("image_prompt", ""),
        filename=f"{today['date']}_thcs.png",
        recent_characters=recent_chars,
        quiz_data=thcs_quiz,
    )

    # Add THCS chars to recent list for THPT selection
    thpt_recent = recent_chars + (thcs_chars if thcs_chars else [])

    thpt_image, thpt_chars = create_post_image(
        post_type=today["thpt_post_type"],
        image_title=thpt["image_title"],
        layout_type=thpt.get("layout_type", ""),
        diagram_data=thpt.get("diagram_data", {}),
        grade_label=thpt["grade_label"],
        image_prompt=thpt.get("image_prompt", ""),
        filename=f"{today['date']}_thpt.png",
        recent_characters=thpt_recent,
        quiz_data=thpt_quiz,
    )

    if thcs_image is None and thpt_image is None:
        logger.error("Both image generations failed. Skipping today.")
        return False

    if thcs_image is None:
        logger.warning("THCS image failed, will post THPT only.")
    if thpt_image is None:
        logger.warning("THPT image failed, will post THCS only.")

    logger.info(
        "Images created: THCS=%s (chars: %s), THPT=%s (chars: %s)",
        thcs_image.name if thcs_image else "FAILED", thcs_chars,
        thpt_image.name if thpt_image else "FAILED", thpt_chars,
    )

    # ── Step 4: Post to Facebook ──────────────────────────────────
    posted_count = 0

    if dry_run:
        if thcs_image:
            logger.info("[DRY RUN] Would post THCS at %02d:%02d", THCS_POST_HOUR, THCS_POST_MINUTE)
            logger.info("[DRY RUN] THCS type: %s | characters: %s", thcs_label, thcs_chars)
            logger.info("[DRY RUN] THCS status:\n%s\n%s", thcs["status"], thcs["hashtags"])
            posted_count += 1
        if thpt_image:
            logger.info("[DRY RUN] Would post THPT at %02d:%02d", THPT_POST_HOUR, THPT_POST_MINUTE)
            logger.info("[DRY RUN] THPT type: %s | characters: %s", thpt_label, thpt_chars)
            logger.info("[DRY RUN] THPT status:\n%s\n%s", thpt["status"], thpt["hashtags"])
            posted_count += 1
    else:
        # THCS post: schedule for morning
        if thcs_image:
            thcs_caption = f"{thcs['status']}\n\n{thcs['hashtags']}"
            thcs_result = schedule_photo(
                image_path=str(thcs_image),
                caption=thcs_caption,
                hour=THCS_POST_HOUR,
                minute=THCS_POST_MINUTE,
            )
            if thcs_result is None:
                logger.error("Failed to post THCS content.")
            else:
                posted_count += 1

        # THPT post: schedule for evening
        if thpt_image:
            thpt_caption = f"{thpt['status']}\n\n{thpt['hashtags']}"
            thpt_result = schedule_photo(
                image_path=str(thpt_image),
                caption=thpt_caption,
                hour=THPT_POST_HOUR,
                minute=THPT_POST_MINUTE,
            )
            if thpt_result is None:
                logger.error("Failed to post THPT content.")
            else:
                posted_count += 1

    if posted_count == 0 and not dry_run:
        logger.error("All Facebook posts failed.")
        return False

    # ── Step 5: Advance state ─────────────────────────────────────
    # Track all characters used today (each post uses 2)
    used_chars = (thcs_chars or []) + (thpt_chars or [])
    state = advance_state(
        state, today["thcs_post_type"], today["thpt_post_type"],
        used_characters=used_chars,
    )
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
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force run even if already posted today (for testing).",
    )
    args = parser.parse_args()

    success = run(dry_run=args.dry_run, force=args.force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
