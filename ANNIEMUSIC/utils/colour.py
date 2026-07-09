import json
import aiohttp
from typing import List, Optional, Union
import config
from pyrogram.types import InlineKeyboardButton

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
    """Create InlineKeyboardButton with style parameter"""
    button_kwargs = {
        "text": text,
    }
    
    if callback_data:
        button_kwargs["callback_data"] = callback_data
    elif url:
        button_kwargs["url"] = url
    
    return InlineKeyboardButton(**button_kwargs)

async def send_photo_colored(
    chat_id: Union[int, str],
    photo: str,
    caption: str = "",
    reply_markup: List[List[dict]] = None,
    parse_mode: str = "HTML",
) -> Optional[dict]:
    """Send photo via Bot API with colored buttons support"""
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
    """Edit message reply markup with colored buttons support"""
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
