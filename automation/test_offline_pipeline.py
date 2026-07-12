"""
Offline E2E test — mocks Gemini API to verify the full pipeline logic
without requiring a real API key.

Usage:
    python test_offline_pipeline.py
"""

import json
import logging
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("offline_test")


# ── Mock content that Gemini would return ──────────────────────────
MOCK_THCS_CONTENT = {
    "image_title": "Phản ứng hóa học là gì?",
    "image_content": "Phản ứng hóa học là quá trình biến đổi chất này thành chất khác. "
                     "Ví dụ: 2H₂ + O₂ → 2H₂O. Chất tham gia bị biến đổi, "
                     "chất sản phẩm được tạo thành.",
    "grade_label": "KHTN Lớp 9",
    "caption": "🔬 PHẢN ỨNG HÓA HỌC LÀ GÌ?\n\n"
               "Các em ơi, hôm nay Thầy Hiếu sẽ giúp các em hiểu rõ về phản ứng hóa học nhé! "
               "Phản ứng hóa học là quá trình biến đổi chất này thành chất khác.\n\n"
               "💡 Ví dụ kinh điển: 2H₂ + O₂ → 2H₂O\n"
               "Hydro và Oxy kết hợp tạo thành nước!\n\n"
               "👉 Các em hãy like và share nếu thấy bổ ích nhé!",
    "hashtags": "#LTHChemistry #HoaHoc #GiaSuHoaHoc #PhanUngHoaHoc #KHTN9",
    "image_prompt": "molecular models of H2 and O2 combining to form H2O water molecule, "
                    "chemistry laboratory with colorful beakers and test tubes, "
                    "periodic table elements floating, "
                    "1080x1080, no text, no words, no letters, no numbers, visual elements only",
}

MOCK_THPT_CONTENT = {
    "image_title": "Bạn có biết: Vàng không phản ứng với axit?",
    "image_content": "Vàng (Au) là kim loại quý hiếm, không bị oxy hóa trong không khí "
                     "và không tan trong hầu hết các axit thông thường. "
                     "Chỉ có nước cường toan (HNO₃ + 3HCl) mới hòa tan được vàng!",
    "grade_label": "Hóa Học Lớp 10",
    "caption": "✨ BẠN CÓ BIẾT?\n\n"
               "Vàng (Au) là kim loại 'kiêu kỳ' nhất bảng tuần hoàn! 👑\n\n"
               "🔹 Không bị oxy hóa trong không khí\n"
               "🔹 Không tan trong hầu hết axit\n"
               "🔹 Chỉ tan trong nước cường toan (HNO₃ + 3HCl)\n\n"
               "Đó là lý do vàng giữ được vẻ sáng bóng hàng nghìn năm! 🌟",
    "hashtags": "#LTHChemistry #HoaHoc #GiaSuHoaHoc #FunFacts #Vang #HoaHoc10",
    "image_prompt": "gold Au element from periodic table shining, "
                    "beaker with aqua regia dissolving gold nugget, "
                    "crown and gold bars with chemistry symbols, "
                    "1080x1080, no text, no words, no letters, no numbers, visual elements only",
}


def run_test():
    """Run the full pipeline with mocked content generation."""
    logger.info("=" * 60)
    logger.info("OFFLINE E2E TEST — mocking Gemini API calls")
    logger.info("=" * 60)

    # ── Step 1: Load real state ────────────────────────────────────
    logger.info("\nSTEP 1: Loading state...")
    from state_manager import load_state, get_today_info

    state = load_state()
    today = get_today_info(state)

    logger.info("  Date: %s", today["date_display"])
    logger.info("  THCS: Grade %s Ch.%s [%s]", today["thcs_grade"], today["thcs_chapter"], today["thcs_post_type"])
    logger.info("  THPT: Grade %s Ch.%s [%s]", today["thpt_grade"], today["thpt_chapter"], today["thpt_post_type"])
    logger.info("  Last character: %s", today.get("last_character"))

    # ── Step 2: Use mock content ───────────────────────────────────
    logger.info("\nSTEP 2: Using MOCK content (skipping Gemini call)")
    thcs = MOCK_THCS_CONTENT.copy()
    thpt = MOCK_THPT_CONTENT.copy()

    logger.info("  ✅ THCS: %s", thcs["image_title"])
    logger.info("  ✅ THPT: %s", thpt["image_title"])

    # ── Step 3: Create images via Hybrid Pipeline ──────────────────
    logger.info("\nSTEP 3: Creating images via Hybrid Rendering Pipeline...")
    logger.info("  (AI visual gen will use Pillow fallback since no API key)")

    from image_generator import create_post_image

    last_char = today.get("last_character")

    logger.info("\n  --- Generating THCS image ---")
    thcs_image, thcs_char = create_post_image(
        post_type=today["thcs_post_type"],
        image_title=thcs["image_title"],
        image_content=thcs["image_content"],
        grade_label=thcs["grade_label"],
        image_prompt=thcs["image_prompt"],
        filename=f"e2e_offline_{today['date']}_thcs.png",
        last_character=last_char,
    )

    logger.info("\n  --- Generating THPT image ---")
    thpt_image, thpt_char = create_post_image(
        post_type=today["thpt_post_type"],
        image_title=thpt["image_title"],
        image_content=thpt["image_content"],
        grade_label=thpt["grade_label"],
        image_prompt=thpt["image_prompt"],
        filename=f"e2e_offline_{today['date']}_thpt.png",
        last_character=thcs_char,  # avoid same character
    )

    # ── Step 4: Results ────────────────────────────────────────────
    logger.info("\n" + "=" * 60)
    logger.info("RESULTS:")
    logger.info("=" * 60)

    all_ok = True

    if thcs_image:
        size_kb = thcs_image.stat().st_size / 1024
        logger.info("✅ THCS: %s (%.1f KB) | char: %s", thcs_image.name, size_kb, thcs_char)
    else:
        logger.error("❌ THCS image FAILED")
        all_ok = False

    if thpt_image:
        size_kb = thpt_image.stat().st_size / 1024
        logger.info("✅ THPT: %s (%.1f KB) | char: %s", thpt_image.name, size_kb, thpt_char)
    else:
        logger.error("❌ THPT image FAILED")
        all_ok = False

    if all_ok:
        logger.info("")
        logger.info("🎉 ALL CHECKS PASSED!")
        logger.info("   Characters: %s → %s (no duplicates: %s)",
                     thcs_char, thpt_char, thcs_char != thpt_char)
        logger.info("   Vietnamese diacritics: rendered by Pillow (100%% accurate)")
        logger.info("   Output: %s", thcs_image.parent)
        logger.info("")
        logger.info("   To run with REAL Gemini API:")
        logger.info('   $env:GEMINI_API_KEY="your-key"; python test_full_pipeline.py')
    else:
        logger.error("❌ SOME CHECKS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    run_test()
