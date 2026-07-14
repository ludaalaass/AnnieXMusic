import functools
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message, CallbackQuery
from ANNIEMUSIC.utils.emoji_registry import (
    premiumize_emoji_html,
    is_emoji_send_error,
    strip_custom_emoji,
)

def _wrap(original):
    @functools.wraps(original)
    async def wrapper(self, *args, **kwargs):
        args = list(args)
        for key in ("text", "caption"):
            if isinstance(kwargs.get(key), str):
                kwargs[key] = premiumize_emoji_html(kwargs[key])
        if args and isinstance(args[0], str):
            args[0] = premiumize_emoji_html(args[0])
        kwargs.setdefault("parse_mode", ParseMode.HTML)
        try:
            return await original(self, *args, **kwargs)
        except Exception as e:
            if is_emoji_send_error(str(e)):
                if args and isinstance(args[0], str):
                    args[0] = strip_custom_emoji(args[0])
                for key in ("text", "caption"):
                    if isinstance(kwargs.get(key), str):
                        kwargs[key] = strip_custom_emoji(kwargs[key])
                return await original(self, *args, **kwargs)
            raise
    return wrapper

Message.reply_text = _wrap(Message.reply_text)
Message.edit_text = _wrap(Message.edit_text)
Message.reply_photo = _wrap(Message.reply_photo)
Message.reply_video = _wrap(Message.reply_video)
Message.reply_animation = _wrap(Message.reply_animation)
Message.reply_audio = _wrap(Message.reply_audio)
Message.edit_caption = _wrap(Message.edit_caption)

Client.send_message = _wrap(Client.send_message)
Client.edit_message_text = _wrap(Client.edit_message_text)
Client.send_photo = _wrap(Client.send_photo)
Client.send_video = _wrap(Client.send_video)
Client.edit_message_caption = _wrap(Client.edit_message_caption)

CallbackQuery.edit_message_text = _wrap(CallbackQuery.edit_message_text)
