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

# ── Brand colors (Boped Design System) ───────────────────────────────
# All products share the same base palette for brand consistency.
# See: boped-design-system workflow
COLORS = {
    # Core brand
    "primary_teal": "#0BA5A5",    # hsl(185, 87%, 35%)
    "primary_dark": "#213555",     # Navy - primary dark
    "gold": "#FFBF00",             # hsl(45, 100%, 60%)
    # Extended palette
    "navy_deep": "#172540",        # Gradient bottom
    "teal_light": "#0DC5C5",       # Gradient top accent
    "white": "#ffffff",
    "off_white": "#F9FDFD",        # hsl(180, 20%, 99%)
    "muted": "#EFF5F5",            # hsl(180, 15%, 96%)
    # Status accents (for post-type differentiation)
    "safe_green": "#33A06A",       # hsl(152, 60%, 40%)
    "attempt_amber": "#F0A500",    # hsl(40, 95%, 52%)
    "dream_red": "#D94444",        # hsl(0, 72%, 55%)
    "purple": "#7C3AED",
}

# ── Template color schemes per post type (Pillow fallback) ───────────
# UNIFIED: All types share the same navy background for brand consistency.
# Only accent color differs to signal content type.
_NAVY_BG = {
    "bg_top": COLORS["primary_dark"],     # #213555
    "bg_bottom": COLORS["navy_deep"],      # #172540
    "text": COLORS["white"],
}

TEMPLATE_COLORS = {
    "quiz_mcq":            {**_NAVY_BG, "accent": COLORS["purple"]},
    "review_question":     {**_NAVY_BG, "accent": COLORS["primary_teal"]},
    "common_mistakes":     {**_NAVY_BG, "accent": COLORS["dream_red"]},
    "chemistry_around_us": {**_NAVY_BG, "accent": COLORS["safe_green"]},
    "mnemonic_tips":       {**_NAVY_BG, "accent": COLORS["gold"]},
    "fun_facts":           {**_NAVY_BG, "accent": COLORS["attempt_amber"]},
    "exam_countdown":      {**_NAVY_BG, "accent": COLORS["dream_red"]},
}

# ── Chibi Character System ───────────────────────────────────────────
# Fixed mascot description (appears in every image)
CHIBI_MASCOT = (
    "a cute chibi male Vietnamese teacher character with round face, "
    "wearing glasses and a white lab coat over casual clothes, "
    "holding a test tube with bubbling green liquid, friendly warm smile, "
    "positioned at bottom-right area of the image, small size (about 15% of image)"
)

# Guest characters: mapped to preferred post types for thematic matching.
# Each entry: (name, chibi_description, [preferred_post_types])
CHIBI_GUEST_CHARACTERS = [
    (
        "doraemon",
        "a cute chibi blue robot cat character (fan art style) pulling a chemistry "
        "beaker from its front pocket, big round eyes, red nose, no bell collar",
        ["fun_facts", "chemistry_around_us"],
    ),
    (
        "conan",
        "a cute chibi detective boy character (fan art style) with big glasses "
        "and bow tie, examining molecules with a magnifying glass, determined expression",
        ["quiz_mcq", "review_question"],
    ),
    (
        "naruto",
        "a cute chibi ninja boy character (fan art style) with spiky blonde hair "
        "and orange outfit, making hand signs with chemistry symbols floating around",
        ["mnemonic_tips"],
    ),
    (
        "luffy",
        "a cute chibi pirate boy character (fan art style) with straw hat, "
        "stretching rubber arm to grab a floating periodic table element card",
        ["common_mistakes"],
    ),
    (
        "nobita",
        "a cute chibi sleepy student boy character (fan art style) with round glasses, "
        "suddenly excited and alert while reading a chemistry textbook, sparkle eyes",
        ["exam_countdown"],
    ),
    (
        "pikachu",
        "a cute chibi yellow electric mouse creature (fan art style) with red cheeks, "
        "generating tiny lightning bolts between chemistry electrodes",
        ["review_question"],
    ),
    (
        "goku",
        "a cute chibi spiky-haired warrior boy character (fan art style) in orange gi, "
        "powering up with colorful chemical energy aura",
        ["fun_facts"],
    ),
    (
        "kiki",
        "a cute chibi young witch girl character (fan art style) with big red bow "
        "in hair, stirring a bubbling chemistry cauldron with a glass stirring rod",
        ["chemistry_around_us"],
    ),
]

# ── OCR Validation Settings ──────────────────────────────────────────
OCR_MAX_RETRIES = 2          # max regen attempts if garbled text detected
OCR_VISION_MODEL = "gemini-2.5-flash"  # model for OCR spell-checking
