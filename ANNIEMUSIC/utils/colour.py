# ═══════════════════════════════════════════════════════════
#        😎  VISHAL MUSIC BOT  😎
#   GitHub : github.com/ItsMeVishal0/VishalMusic
#   Developer : @ItsMeVishalBots | Telegram
#   Module : Colored Inline Buttons via Bot API HTTP
# ═══════════════════════════════════════════════════════════

"""
Kurigram/Pyrogram uses MTProto which doesn't support the 'style'
field on buttons yet. This module sends messages via Bot API HTTP
to enable colored inline keyboard buttons.

Styles: "primary" (blue), "success" (green), "danger" (red)
"""

import json
import aiohttp
from typing import List, Optional, Union

import config

BOT_API_URL = f"https://api.telegram.org/bot{config.BOT_TOKEN}"

_session: Optional[aiohttp.ClientSession] = None


async def _get_session() -> aiohttp.ClientSession:
    global _session
    if _session and not _session.closed:
        return _session
    _session = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30)
    )
    return _session


def styled_button(text: str, callback_data: str = None, url: str = None, style: str = None):
    btn = {"text": text}
    if callback_data:
        btn["callback_data"] = callback_data
    if url:
        btn["url"] = url
    if style:
        btn["style"] = style
    return btn


async def send_photo_colored(
    chat_id: Union[int, str],
    photo: str,
    caption: str = "",
    reply_markup: List[List[dict]] = None,
    parse_mode: str = "HTML",
) -> Optional[dict]:
    session = await _get_session()

    if reply_markup:
        markup_json = json.dumps({"inline_keyboard": reply_markup})
    else:
        markup_json = None

    import os
    if photo and os.path.exists(photo):
        try:
            data = aiohttp.FormData()
            data.add_field("chat_id", str(chat_id))
            data.add_field("caption", caption)
            data.add_field("parse_mode", parse_mode)
            if markup_json:
                data.add_field("reply_markup", markup_json)
            f = open(photo, "rb")
            data.add_field("photo", f, filename=os.path.basename(photo))

            try:
                async with session.post(f"{BOT_API_URL}/sendPhoto", data=data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result.get("result")
                    return None
            finally:
                f.close()
        except Exception:
            return None
    else:
        payload = {
            "chat_id": chat_id,
            "photo": photo,
            "caption": caption,
            "parse_mode": parse_mode,
        }
        if markup_json:
            payload["reply_markup"] = markup_json

        try:
            async with session.post(f"{BOT_API_URL}/sendPhoto", data=payload) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result.get("result")
                return None
        except Exception:
            return None


async def edit_reply_markup_colored(
    chat_id: Union[int, str],
    message_id: int,
    reply_markup: List[List[dict]] = None,
) -> Optional[dict]:
    session = await _get_session()
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps({"inline_keyboard": reply_markup})

    try:
        async with session.post(f"{BOT_API_URL}/editMessageReplyMarkup", data=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("result")
            return None
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════
#   HEART EFFECT - Send photo with message_effect_id via Bot API
# ═══════════════════════════════════════════════════════════

# Telegram Message Effect IDs (Bot API format - string)
EFFECT_HEART = "5159385139981059251"
EFFECT_FIRE = "5104841245755180586"
EFFECT_LIKE = "5107584321108051014"
EFFECT_DISLIKE = "5104858069142078462"
EFFECT_PARTY = "5046509860389126442"


async def send_photo_with_effect(
    chat_id,
    photo: str,
    caption: str = "",
    reply_markup=None,
    parse_mode: str = "HTML",
    effect_id: str = EFFECT_HEART,
) -> Optional[dict]:
    session = await _get_session()

    if reply_markup:
        markup_json = json.dumps({"inline_keyboard": reply_markup})
    else:
        markup_json = None

    import os
    if photo and os.path.exists(photo):
        try:
            data = aiohttp.FormData()
            data.add_field("chat_id", str(chat_id))
            data.add_field("caption", caption)
            data.add_field("parse_mode", parse_mode)
            data.add_field("message_effect_id", effect_id)
            if markup_json:
                data.add_field("reply_markup", markup_json)
            f = open(photo, "rb")
            data.add_field("photo", f, filename=os.path.basename(photo))

            try:
                async with session.post(f"{BOT_API_URL}/sendPhoto", data=data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result.get("result")
                    return None
            finally:
                f.close()
        except Exception:
            return None
    else:
        payload = {
            "chat_id": chat_id,
            "photo": photo,
            "caption": caption,
            "parse_mode": parse_mode,
            "message_effect_id": effect_id,
        }
        if markup_json:
            payload["reply_markup"] = markup_json

        try:
            async with session.post(f"{BOT_API_URL}/sendPhoto", data=payload) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result.get("result")
                return None
        except Exception:
            return None
