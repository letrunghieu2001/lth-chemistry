"""
Configuration for LTH Chemistry Facebook automation.
All secrets loaded from environment variables (GitHub Secrets).
"""

import os
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent
SKILLS_DIR = PROJECT_DIR / "skills" / "lth-facebook-content"
SKILL_FILE = SKILLS_DIR / "SKILL.md"
CURRICULUM_FILE = SKILLS_DIR / "curriculum-map.md"
STATE_FILE = BASE_DIR / "state.json"
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
OUTPUT_DIR = BASE_DIR / "output"
FONT_DIR = BASE_DIR / "fonts"
FONT_REGULAR = FONT_DIR / "BeVietnamPro-Regular.ttf"
FONT_BOLD = FONT_DIR / "BeVietnamPro-Bold.ttf"

# ── API Keys (from environment / GitHub Secrets) ──────────────────────
# Primary: Gemini API direct (aistudio.google.com)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
# Fallback: OpenRouter (openrouter.ai) — free tier available
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN", "")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID", "")

# ── Schedule (Vietnam time UTC+7) ────────────────────────────────────
THCS_POST_HOUR = 6   # 6:30 AM
THCS_POST_MINUTE = 30
THPT_POST_HOUR = 20  # 8:00 PM
THPT_POST_MINUTE = 0

# ── Image settings ────────────────────────────────────────────────────
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1080
LOGO_MAX_HEIGHT = 80

# ── Grade rotation ────────────────────────────────────────────────────
THCS_GRADES = [6, 7, 8, 9]
THPT_GRADES = [10, 11, 12]

# ── Post types with weights for random selection ──────────────────────
# Higher weight = more frequent. quiz_mcq gets 3x priority.
POST_TYPE_WEIGHTS = {
    "quiz_mcq": 3,
    "review_question": 1,
    "common_mistakes": 1,
    "chemistry_around_us": 1,
    "mnemonic_tips": 1,
    "fun_facts": 1,
    "exam_countdown": 1,
}

POST_TYPE_LABELS = {
    "quiz_mcq": "TRẮC NGHIỆM HÓA HỌC",
    "review_question": "CÂU HỎI ÔN TẬP",
    "common_mistakes": "SAI LẦM HAY GẶP",
    "chemistry_around_us": "HÓA HỌC QUANH TA",
    "mnemonic_tips": "MẸO GHI NHỚ",
    "fun_facts": "CÓ BIẾT KHÔNG?",
    "exam_countdown": "COUNTDOWN THI",
}

# ── Brand colors (from logo) ─────────────────────────────────────────
COLORS = {
    "teal": "#0d7377",
    "navy": "#1a1a4e",
    "sky_blue": "#7ec8e3",
    "yellow": "#f0c040",
    "white": "#ffffff",
    "light_gray": "#f5f7fa",
    "orange": "#e67e22",
    "red": "#e74c3c",
    "green": "#27ae60",
    "purple": "#6c3483",
    "dark_blue": "#1a2744",
    "gold": "#f1c40f",
}

# ── Template color schemes per post type (used by Pillow fallback) ────
TEMPLATE_COLORS = {
    "quiz_mcq": {
        "bg_top": "#6c3483",
        "bg_bottom": "#4a235a",
        "accent": "#d2b4de",
        "text": "#ffffff",
    },
    "review_question": {
        "bg_top": "#0d7377",
        "bg_bottom": "#0a5c5f",
        "accent": "#7ec8e3",
        "text": "#ffffff",
    },
    "common_mistakes": {
        "bg_top": "#e74c3c",
        "bg_bottom": "#c0392b",
        "accent": "#f5b041",
        "text": "#ffffff",
    },
    "chemistry_around_us": {
        "bg_top": "#27ae60",
        "bg_bottom": "#1e8449",
        "accent": "#a9dfbf",
        "text": "#ffffff",
    },
    "mnemonic_tips": {
        "bg_top": "#f39c12",
        "bg_bottom": "#d68910",
        "accent": "#fdebd0",
        "text": "#1a1a4e",
    },
    "fun_facts": {
        "bg_top": "#1a2744",
        "bg_bottom": "#0e1a30",
        "accent": "#f1c40f",
        "text": "#ffffff",
    },
    "exam_countdown": {
        "bg_top": "#e74c3c",
        "bg_bottom": "#922b21",
        "accent": "#f5b7b1",
        "text": "#ffffff",
    },
}
