"""
Facebook poster: publishes photos with captions to a Facebook Page
via the Graph API.
"""

import logging
from datetime import datetime, timezone, timedelta

import requests

from config import FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID

logger = logging.getLogger(__name__)

GRAPH_API_BASE = "https://graph.facebook.com/v25.0"
VN_TZ = timezone(timedelta(hours=7))


def _validate_credentials() -> bool:
    """Check that Facebook credentials are configured."""
    if not FB_PAGE_ACCESS_TOKEN:
        logger.error("FB_PAGE_ACCESS_TOKEN not set.")
        return False
    if not FB_PAGE_ID:
        logger.error("FB_PAGE_ID not set.")
        return False
    return True


def post_photo_now(image_path: str, caption: str) -> dict | None:
    """
    Post a photo with caption to the Facebook Page immediately.

    Args:
        image_path: Local path to the image file.
        caption: The post caption text.

    Returns:
        API response dict with post_id, or None on failure.
    """
    if not _validate_credentials():
        return None

    # ── Strategy: 2-step upload (avoids pages_manage_metadata) ──
    # Step 1: Upload photo as unpublished
    # Step 2: Publish via /feed with attached_media
    upload_url = f"{GRAPH_API_BASE}/{FB_PAGE_ID}/photos"

    try:
        with open(image_path, "rb") as img_file:
            upload_resp = requests.post(
                upload_url,
                data={
                    "access_token": FB_PAGE_ACCESS_TOKEN,
                    "published": "false",
                },
                files={
                    "source": ("post_image.png", img_file, "image/png"),
                },
                timeout=60,
            )

        upload_result = upload_resp.json()
        logger.info(
            "FB photo upload response: status=%s body=%s",
            upload_resp.status_code, upload_result,
        )

        if "id" not in upload_result:
            logger.error("Failed to upload photo: %s", upload_result)
            return None

        photo_id = upload_result["id"]
        logger.info("Photo uploaded (unpublished). photo_id=%s", photo_id)

        # Step 2: Publish via /feed with attached_media
        feed_url = f"{GRAPH_API_BASE}/{FB_PAGE_ID}/feed"
        feed_resp = requests.post(
            feed_url,
            data={
                "message": caption,
                "access_token": FB_PAGE_ACCESS_TOKEN,
                "attached_media[0]": f'{{"media_fbid":"{photo_id}"}}',
            },
            timeout=60,
        )

        feed_result = feed_resp.json()
        logger.info(
            "FB feed publish response: status=%s body=%s",
            feed_resp.status_code, feed_result,
        )

        if "id" in feed_result:
            logger.info("Posted successfully via /feed. Post ID: %s", feed_result["id"])
            return feed_result
        else:
            logger.error("Facebook /feed publish error: %s", feed_result)
            return None

    except requests.RequestException as exc:
        logger.error("Network error posting to Facebook: %s", exc)
        return None
    except FileNotFoundError:
        logger.error("Image file not found: %s", image_path)
        return None


def schedule_photo(image_path: str, caption: str,
                   hour: int, minute: int = 0) -> dict | None:
    """
    Schedule a photo post for a specific time today (Vietnam time).

    Args:
        image_path: Local path to the image file.
        caption: The post caption text.
        hour: Hour in Vietnam time (0-23).
        minute: Minute (0-59).

    Returns:
        API response dict, or None on failure.
    """
    if not _validate_credentials():
        return None

    # Calculate scheduled Unix timestamp
    now_vn = datetime.now(VN_TZ)
    scheduled_time = now_vn.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # If the time has already passed today or is within 15 minutes,
    # post immediately instead (Facebook requires ≥10 min for scheduling)
    min_schedule_time = now_vn + timedelta(minutes=15)
    if scheduled_time <= min_schedule_time:
        logger.info(
            "Scheduled time %s too close or passed (now=%s). Posting immediately.",
            scheduled_time.strftime("%H:%M"), now_vn.strftime("%H:%M"),
        )
        return post_photo_now(image_path, caption)

    unix_timestamp = int(scheduled_time.timestamp())
    logger.info(
        "Scheduling post: page_id=%s, time=%s (unix=%d), image=%s",
        FB_PAGE_ID, scheduled_time.isoformat(), unix_timestamp, image_path,
    )

    url = f"{GRAPH_API_BASE}/{FB_PAGE_ID}/photos"

    try:
        with open(image_path, "rb") as img_file:
            response = requests.post(
                url,
                data={
                    "caption": caption,
                    "access_token": FB_PAGE_ACCESS_TOKEN,
                    "published": "false",
                    "scheduled_publish_time": str(unix_timestamp),
                },
                files={
                    "source": ("post_image.png", img_file, "image/png"),
                },
                timeout=60,
            )

        result = response.json()
        logger.info("FB API response (schedule): status=%s body=%s", response.status_code, result)

        if "id" in result:
            logger.info(
                "Scheduled post for %02d:%02d VN time. Post ID: %s",
                hour, minute, result["id"],
            )
            return result
        else:
            logger.error("Facebook API scheduling error: %s", result)
            return None

    except requests.RequestException as exc:
        logger.error("Network error scheduling post: %s", exc)
        return None
    except FileNotFoundError:
        logger.error("Image file not found: %s", image_path)
        return None


def verify_token() -> bool:
    """
    Verify the Page Access Token is still valid.
    Returns True if valid, False otherwise.
    """
    if not FB_PAGE_ACCESS_TOKEN:
        return False

    url = f"{GRAPH_API_BASE}/debug_token"
    try:
        response = requests.get(
            url,
            params={
                "input_token": FB_PAGE_ACCESS_TOKEN,
                "access_token": FB_PAGE_ACCESS_TOKEN,
            },
            timeout=15,
        )
        data = response.json().get("data", {})
        is_valid = data.get("is_valid", False)

        if not is_valid:
            logger.error(
                "Facebook token is INVALID or EXPIRED. "
                "Please generate a new token. Error: %s",
                data.get("error", {}).get("message", "Unknown"),
            )
        else:
            scopes = data.get("scopes", [])
            app_id = data.get("app_id", "unknown")
            token_type = data.get("type", "unknown")
            expires_at = data.get("expires_at", 0)
            logger.info(
                "Facebook token is valid. type=%s app_id=%s scopes=%s expires_at=%s",
                token_type, app_id, scopes, expires_at,
            )

        return is_valid

    except requests.RequestException as exc:
        logger.error("Failed to verify token: %s", exc)
        return False
