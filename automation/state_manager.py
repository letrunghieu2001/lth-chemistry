"""
State manager: tracks grade rotation, chapter progression, post history,
and random post-type selection with quiz priority.
"""

import json
import logging
import random
from datetime import datetime, timezone, timedelta

from config import (
    STATE_FILE,
    THCS_GRADES,
    THPT_GRADES,
    POST_TYPE_WEIGHTS,
    CHARACTER_HISTORY_SIZE,
)

logger = logging.getLogger(__name__)

VN_TZ = timezone(timedelta(hours=7))


def load_state() -> dict:
    """Load state from JSON file, or return defaults if missing."""
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning("State file not found or corrupt, using defaults.")
        return _default_state()


def save_state(state: dict) -> None:
    """Write state back to JSON file."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    logger.info("State saved to %s", STATE_FILE)


def pick_random_type(recent_types: list[str]) -> str:
    """
    Pick a random post type using weighted selection.

    Avoids repeating the same type 3 days in a row by temporarily
    zeroing out the weight of any type that appeared in the last 2 picks.
    """
    types = list(POST_TYPE_WEIGHTS.keys())
    weights = list(POST_TYPE_WEIGHTS.values())

    # Check last 2 entries for streak prevention
    if len(recent_types) >= 2:
        last_two = recent_types[-2:]
        if last_two[0] == last_two[1]:
            # Same type 2 days in a row — zero its weight this round
            streak_type = last_two[0]
            weights = [
                0 if t == streak_type else w
                for t, w in zip(types, weights)
            ]
            # Safety: if all weights are 0, reset to uniform
            if sum(weights) == 0:
                weights = [1] * len(types)

    chosen = random.choices(types, weights=weights, k=1)[0]
    return chosen


def get_today_info(state: dict) -> dict:
    """
    Determine what to post today based on current state.

    Returns dict with:
        date, weekday,
        thcs_post_type, thpt_post_type (independently randomized),
        thcs_grade, thcs_chapter,
        thpt_grade, thpt_chapter,
    """
    now = datetime.now(VN_TZ)

    # Pick independent random types for THCS and THPT
    recent = state.get("recent_types", [])
    thcs_type = pick_random_type(recent)
    thpt_type = pick_random_type(recent)

    thcs_idx = state.get("thcs_grade_index", 0) % len(THCS_GRADES)
    thpt_idx = state.get("thpt_grade_index", 0) % len(THPT_GRADES)

    thcs_grade = THCS_GRADES[thcs_idx]
    thpt_grade = THPT_GRADES[thpt_idx]

    thcs_chapters = state.get("thcs_chapter", {})
    thpt_chapters = state.get("thpt_chapter", {})

    thcs_chapter = thcs_chapters.get(str(thcs_grade), 1)
    thpt_chapter = thpt_chapters.get(str(thpt_grade), 1)

    return {
        "date": now.strftime("%Y-%m-%d"),
        "date_display": now.strftime("%d/%m/%Y"),
        "weekday": now.weekday(),
        "thcs_post_type": thcs_type,
        "thpt_post_type": thpt_type,
        "thcs_grade": thcs_grade,
        "thcs_chapter": thcs_chapter,
        "thpt_grade": thpt_grade,
        "thpt_chapter": thpt_chapter,
        "recent_characters": state.get("recent_characters", []),
    }


def advance_state(
    state: dict,
    thcs_type: str,
    thpt_type: str,
    used_characters: list[str] | None = None,
) -> dict:
    """
    Advance the rotation after posting.
    - Rotate THCS grade index: 6 -> 7 -> 8 -> 9 -> 6 ...
    - Rotate THPT grade index: 10 -> 11 -> 12 -> 10 ...
    - Track recent post types for streak prevention.
    - Track recent chibi characters (last N) to avoid repeats.
    - Update post count and last date.
    """
    now = datetime.now(VN_TZ)

    state["thcs_grade_index"] = (state.get("thcs_grade_index", 0) + 1) % len(THCS_GRADES)
    state["thpt_grade_index"] = (state.get("thpt_grade_index", 0) + 1) % len(THPT_GRADES)
    state["last_post_date"] = now.strftime("%Y-%m-%d")
    state["posts_count"] = state.get("posts_count", 0) + 2  # 2 posts per day

    # Track recent types (keep last 6 for streak checking)
    recent = state.get("recent_types", [])
    recent.extend([thcs_type, thpt_type])
    state["recent_types"] = recent[-6:]

    # Track recent characters (keep last N for history-aware selection)
    recent_chars = state.get("recent_characters", [])
    if used_characters:
        recent_chars.extend(used_characters)
    state["recent_characters"] = recent_chars[-CHARACTER_HISTORY_SIZE:]

    return state


def should_post_today(state: dict) -> bool:
    """Check if we already posted today (prevent double-posting)."""
    now = datetime.now(VN_TZ)
    today = now.strftime("%Y-%m-%d")
    last = state.get("last_post_date")
    if last == today:
        logger.info("Already posted today (%s). Skipping.", today)
        return False
    return True


def _default_state() -> dict:
    return {
        "thcs_grade_index": 0,
        "thpt_grade_index": 0,
        "thcs_chapter": {"6": 1, "7": 1, "8": 1, "9": 1},
        "thpt_chapter": {"10": 1, "11": 1, "12": 1},
        "last_post_date": None,
        "posts_count": 0,
        "recent_types": [],
        "recent_characters": [],
    }
