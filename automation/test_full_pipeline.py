"""
Full end-to-end test of the Hybrid Rendering Pipeline.

Usage:
    $env:GEMINI_API_KEY="your-key-here"; python test_full_pipeline.py

This script:
1. Loads state & determines today's content params
2. Generates content via Gemini (content_generator)
3. Creates images via Hybrid Pipeline (image_generator)
4. Logs all outputs for verification
"""

import json
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("e2e_test")

# ── Step 0: Check API key ──────────────────────────────────────────
from config import GEMINI_API_KEY, OPENROUTER_API_KEY

if not GEMINI_API_KEY and not OPENROUTER_API_KEY:
    logger.error(
        "❌ No API key found!\n"
        "   Set one of:\n"
        '   $env:GEMINI_API_KEY="AIza..."\n'
        '   $env:OPENROUTER_API_KEY="sk-or-..."\n'
    )
    sys.exit(1)

key_source = "GEMINI" if GEMINI_API_KEY else "OPENROUTER"
logger.info("✅ Using %s API key (length: %d)", key_source, len(GEMINI_API_KEY or OPENROUTER_API_KEY))

# ── Step 1: Load state & determine today's params ──────────────────
logger.info("=" * 60)
logger.info("STEP 1: Loading state...")
from state_manager import load_state, get_today_info

state = load_state()
today = get_today_info(state)

logger.info("  Date: %s", today["date_display"])
logger.info("  THCS: Grade %s Ch.%s [%s]", today["thcs_grade"], today["thcs_chapter"], today["thcs_post_type"])
logger.info("  THPT: Grade %s Ch.%s [%s]", today["thpt_grade"], today["thpt_chapter"], today["thpt_post_type"])
logger.info("  Last character: %s", today.get("last_character"))

# ── Step 2: Generate content via Gemini ────────────────────────────
logger.info("=" * 60)
logger.info("STEP 2: Generating content via Gemini...")
from content_generator import generate_content

thcs, thpt = generate_content(today)

if thcs is None or thpt is None:
    logger.error("❌ Content generation failed!")
    sys.exit(1)

logger.info("✅ Content generated successfully!")
logger.info("  THCS title: %s", thcs.get("image_title", "N/A"))
logger.info("  THCS image_prompt: %.100s...", thcs.get("image_prompt", "N/A"))
logger.info("  THPT title: %s", thpt.get("image_title", "N/A"))
logger.info("  THPT image_prompt: %.100s...", thpt.get("image_prompt", "N/A"))

# Pretty-print full content for verification
logger.info("\n--- THCS Content JSON ---")
for key, val in thcs.items():
    if key == "image_prompt":
        logger.info("  %s: %s", key, val)
    else:
        text = str(val)[:200]
        logger.info("  %s: %s", key, text)

logger.info("\n--- THPT Content JSON ---")
for key, val in thpt.items():
    if key == "image_prompt":
        logger.info("  %s: %s", key, val)
    else:
        text = str(val)[:200]
        logger.info("  %s: %s", key, text)

# ── Step 3: Create images via Hybrid Pipeline ──────────────────────
logger.info("=" * 60)
logger.info("STEP 3: Creating images via Hybrid Rendering Pipeline...")
from image_generator import create_post_image

last_char = today.get("last_character")

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

logger.info("  Generating THCS image...")
thcs_image, thcs_char = create_post_image(
    post_type=today["thcs_post_type"],
    image_title=thcs["image_title"],
    image_content=thcs["image_content"],
    grade_label=thcs["grade_label"],
    image_prompt=thcs.get("image_prompt", ""),
    filename=f"e2e_{today['date']}_thcs.png",
    last_character=last_char,
    quiz_data=thcs_quiz,
)

logger.info("  Generating THPT image...")
thpt_image, thpt_char = create_post_image(
    post_type=today["thpt_post_type"],
    image_title=thpt["image_title"],
    image_content=thpt["image_content"],
    grade_label=thpt["grade_label"],
    image_prompt=thpt.get("image_prompt", ""),
    filename=f"e2e_{today['date']}_thpt.png",
    last_character=thcs_char,  # avoid same char in both posts
    quiz_data=thpt_quiz,
)

# ── Step 4: Report results ─────────────────────────────────────────
logger.info("=" * 60)
logger.info("RESULTS:")
logger.info("=" * 60)

if thcs_image:
    size_kb = thcs_image.stat().st_size / 1024
    logger.info("✅ THCS image: %s (%.1f KB) | character: %s", thcs_image.name, size_kb, thcs_char)
else:
    logger.error("❌ THCS image generation FAILED")

if thpt_image:
    size_kb = thpt_image.stat().st_size / 1024
    logger.info("✅ THPT image: %s (%.1f KB) | character: %s", thpt_image.name, size_kb, thpt_char)
else:
    logger.error("❌ THPT image generation FAILED")

if thcs_image and thpt_image:
    logger.info("")
    logger.info("🎉 FULL PIPELINE TEST PASSED!")
    logger.info("   Output directory: %s", thcs_image.parent)
    logger.info("   Characters used: %s, %s", thcs_char, thpt_char)
    logger.info("")
    logger.info("   Caption preview (THCS):")
    logger.info("   %s", thcs.get("caption", "")[:150])
    logger.info("")
    logger.info("   Caption preview (THPT):")
    logger.info("   %s", thpt.get("caption", "")[:150])
else:
    logger.error("❌ PIPELINE TEST FAILED — check logs above")
    sys.exit(1)
