"""
Configuration for LTH Chemistry Facebook automation.
Secrets loaded from environment variables (GitHub Secrets in CI,
.env file for local development).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env for local development (no-op if file doesn't exist)
load_dotenv(Path(__file__).parent / ".env")
load_dotenv(Path(__file__).parent.parent / ".env")

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
LOGO_MAX_HEIGHT = 60  # smaller logo for v2 compact header

# ── Study Card v2 Layout Constants ────────────────────────────────────
CARD_MARGIN = 20           # reduced from 35
HEADER_HEIGHT = 50         # compact header strip
FOOTER_HEIGHT = 35         # compact footer strip
TITLE_FONT_SIZE = 36       # reduced from 40
BULLET_FONT_SIZE = 26      # reduced from 30
GRADE_FONT_SIZE = 20       # reduced from 22
BULLET_SPACING = 8         # tight line spacing between bullets

# ── Caption Styles ────────────────────────────────────────────────────
CAPTION_STYLES = ["story_hook", "mini_trivia"]

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
COLORS = {
    # Core brand
    "primary_teal": "#0BA5A5",
    "primary_dark": "#213555",
    "gold": "#FFBF00",
    # Extended palette
    "navy_deep": "#172540",
    "teal_light": "#0DC5C5",
    "white": "#ffffff",
    "off_white": "#F9FDFD",
    "muted": "#EFF5F5",
    # Status accents
    "safe_green": "#33A06A",
    "attempt_amber": "#F0A500",
    "dream_red": "#D94444",
    "purple": "#7C3AED",
}

# ── Template color schemes per post type ──────────────────────────────
_NAVY_BG = {
    "bg_top": COLORS["primary_dark"],
    "bg_bottom": COLORS["navy_deep"],
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

# ── Chibi Character System (v2 — All-Stars Roster) ───────────────────
# Fixed mascot description (appears in every image)
CHIBI_MASCOT = (
    "a cute chibi male Vietnamese teacher character with round face, "
    "wearing glasses and a white lab coat over casual clothes, "
    "holding a test tube with bubbling green liquid, friendly warm smile, "
    "positioned at bottom-right area of the image, small size (about 15% of image)"
)

# Guest characters: (name, chibi_description, [preferred_post_types], weight)
# weight=1.0 is normal, 0.5 for rare "special guest" appearances
CHIBI_GUEST_CHARACTERS = [
    # ── Anime ──
    (
        "doraemon",
        "a cute chibi blue robot cat character (fan art style) pulling a chemistry "
        "beaker from its front pocket, big round eyes, red nose, no bell collar",
        ["fun_facts", "chemistry_around_us"], 1.0,
    ),
    (
        "conan",
        "a cute chibi detective boy character (fan art style) with big glasses "
        "and bow tie, examining molecules with a magnifying glass, determined expression",
        ["quiz_mcq", "review_question"], 1.0,
    ),
    (
        "naruto",
        "a cute chibi ninja boy character (fan art style) with spiky blonde hair "
        "and orange outfit, making hand signs with chemistry symbols floating around",
        ["mnemonic_tips"], 1.0,
    ),
    (
        "luffy",
        "a cute chibi pirate boy character (fan art style) with straw hat, "
        "stretching rubber arm to grab a floating periodic table element card",
        ["common_mistakes"], 1.0,
    ),
    (
        "nobita",
        "a cute chibi sleepy student boy character (fan art style) with round glasses, "
        "suddenly excited and alert while reading a chemistry textbook, sparkle eyes",
        ["exam_countdown"], 1.0,
    ),
    (
        "pikachu",
        "a cute chibi yellow electric mouse creature (fan art style) with red cheeks, "
        "generating tiny lightning bolts between chemistry electrodes",
        ["review_question"], 1.0,
    ),
    (
        "goku",
        "a cute chibi spiky-haired warrior boy character (fan art style) in orange gi, "
        "powering up with colorful chemical energy aura",
        ["fun_facts"], 1.0,
    ),
    # ── Marvel ──
    (
        "spider_man",
        "a cute chibi friendly red-blue web-slinging hero character (fan art style) "
        "connecting molecular bonds with webs between atoms",
        ["common_mistakes", "review_question"], 1.0,
    ),
    (
        "iron_man",
        "a cute chibi red-gold armored genius hero character (fan art style) "
        "projecting a holographic periodic table from palm repulsor",
        ["mnemonic_tips", "review_question"], 1.0,
    ),
    (
        "hulk",
        "a cute chibi giant green muscular hero character (fan art style) "
        "smashing atom models apart showing nuclear fission",
        ["fun_facts"], 1.0,
    ),
    (
        "dr_strange",
        "a cute chibi sorcerer hero character (fan art style) with red cape, "
        "opening glowing portals filled with chemistry symbols and equations",
        ["quiz_mcq"], 1.0,
    ),
    # ── Disney / Pixar ──
    (
        "elsa",
        "a cute chibi ice princess character (fan art style) with blonde braid, "
        "creating crystalline molecular structures from ice magic",
        ["chemistry_around_us"], 1.0,
    ),
    (
        "buzz",
        "a cute chibi space ranger astronaut character (fan art style) with green visor, "
        "scanning alien chemical compounds with a wrist laser",
        ["fun_facts"], 1.0,
    ),
    (
        "remy",
        "a cute chibi chef rat character (fan art style) with tiny chef hat, "
        "mixing colorful chemical solutions in laboratory beakers",
        ["chemistry_around_us"], 1.0,
    ),
    (
        "baymax",
        "a cute chibi white inflatable healthcare robot character (fan art style), "
        "analyzing molecular structure diagrams on a holographic screen",
        ["common_mistakes"], 1.0,
    ),
    # ── Football Stars ──
    (
        "messi",
        "a cute chibi short football star character (fan art style) with #10 jersey, "
        "juggling colorful atom models like footballs",
        ["exam_countdown"], 1.0,
    ),
    (
        "ronaldo",
        "a cute chibi athletic football star character (fan art style) with #7 jersey, "
        "doing a celebratory pose holding test tubes instead of trophies",
        ["mnemonic_tips"], 1.0,
    ),
    (
        "mbappe",
        "a cute chibi speedy football star character (fan art style) sprinting past "
        "flying periodic table element cards in a race",
        ["exam_countdown"], 1.0,
    ),
    # ── Music Stars ──
    (
        "kpop_idol",
        "a cute chibi stylish K-pop boy band member character (fan art style) "
        "singing into a microphone shaped like a molecular model",
        ["fun_facts"], 1.0,
    ),
    (
        "son_tung",
        "a cute chibi Vietnamese pop star character (fan art style) with stylish hair, "
        "performing on stage with chemistry-themed neon light effects",
        ["chemistry_around_us"], 1.0,
    ),
    (
        "taylor",
        "a cute chibi pop diva character (fan art style) with sparkly outfit, "
        "writing chemistry formulas in a glowing diary notebook",
        ["mnemonic_tips"], 1.0,
    ),
    # ── Science Legends (special guests — lower weight) ──
    (
        "einstein",
        "a cute chibi wild-haired genius professor character (fan art style), "
        "writing E=mc2 on a floating chalkboard with chalk dust flying",
        ["review_question"], 0.5,
    ),
    (
        "marie_curie",
        "a cute chibi determined female scientist character (fan art style) in old-style dress, "
        "holding glowing radium vials that illuminate her face",
        ["fun_facts"], 0.5,
    ),
    (
        "mendeleev",
        "a cute chibi bearded Russian chemist character (fan art style), "
        "arranging colorful periodic table cards on a large table",
        ["quiz_mcq"], 0.5,
    ),
]

# Number of recent characters to avoid repeating
CHARACTER_HISTORY_SIZE = 3

# ── Study Card v3 Layout Constants ────────────────────────────────────
# Zone heights (of 1080px total)
V3_MARGIN = 40
V3_HEADER_H = 65
V3_TITLE_TOP = 75
V3_CONTENT_TOP = 150
V3_FOOTER_H = 220
V3_CONTENT_H = IMAGE_HEIGHT - 150 - 220  # ~710px

# Light academic color palette
V3_PALETTE = {
    "bg": "#FDF8F0",           # Warm cream canvas
    "header_bg": "#213555",    # Navy header
    "title_text": "#1A1A2E",   # Near-black
    "body_text": "#2D3436",    # Dark gray
    "node_bg": "#FFFFFF",      # White nodes
    "node_border": "#213555",  # Navy border
    "accent": "#0BA5A5",       # Teal primary accent
    "accent2": "#D4A017",      # Gold secondary
    "accent_light": "#E8F6F6", # Light teal fill
    "connector": "#0BA5A5",    # Teal connectors
    "result_bg": "#213555",    # Navy for conclusions
    "result_text": "#FFFFFF",  # White on navy
    "footer_bg": "#213555",    # Navy footer
}

# Chibi sticker settings
V3_CHIBI_HEIGHT = 150    # px height for sticker
V3_CHIBI_MARGIN = 24     # px from edge

# Post type → default diagram layout
V3_LAYOUT_MAP = {
    "review_question": "mind_map",
    "common_mistakes": "mind_map",
    "fun_facts": "info_grid",
    "quiz_mcq": "info_grid",
    "quick_formula": "flowchart",
    "experiment_tip": "flowchart",
    "chemistry_around_us": "info_grid",
    "mnemonic_tips": "flowchart",
    "exam_countdown": "mind_map",
}

# ── Model Fallback Chain (high → low) ────────────────────────────────
FLASH_MODEL_CHAIN = ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-2.5-flash"]
OCR_VISION_MODEL = FLASH_MODEL_CHAIN[0]  # Best available for OCR
