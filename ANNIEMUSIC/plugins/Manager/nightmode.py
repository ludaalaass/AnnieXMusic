import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters, enums
from pyrogram.enums import MessageEntityType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions, CallbackQuery, Message
from ANNIEMUSIC import app
from ANNIEMUSIC.plugins.Manager.nightmodedb import nightdb, nightmode_on, nightmode_off, get_nightchats
from datetime import datetime
import pytz
import builtins
from pytz import timezone

IST = pytz.timezone("Asia/Kolkata")

# --------------------------------------------------------
# 🌍 GLOBAL Scheduler Protection + GLOBAL Scheduler Storage
# --------------------------------------------------------
if not hasattr(builtins, "NIGHTMODE_SCHEDULER_STARTED"):
    builtins.NIGHTMODE_SCHEDULER_STARTED = False

GLOBAL_SCHEDULER = None


# --------------------------------------------------------
# 🛡 Chat Permission Sets
# --------------------------------------------------------
CLOSE_CHAT = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=False,
    can_send_polls=False,
    can_change_info=False,
    can_add_web_page_previews=False,
    can_pin_messages=False,
    can_invite_users=False,
)

OPEN_CHAT = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=True,
    can_add_web_page_previews=True,
    can_pin_messages=True,
    can_invite_users=True,
)

# --------------------------------------------------------
# 🔘 Buttons
# --------------------------------------------------------
buttons = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton("🌙 ᴇɴᴀʙʟᴇ ɴɪɢʜᴛᴍᴏᴅᴇ", callback_data="add_night"),
        InlineKeyboardButton("☀️ ᴅɪsᴀʙʟᴇ ɴɪɢʜᴛᴍᴏᴅᴇ", callback_data="rm_night")
    ]]
)

# --------------------------------------------------------
# 🌙 /nightmode Menu
# --------------------------------------------------------
@app.on_message(filters.command("nightmode") & filters.group)
async def _nightmode(_, message: Message):
    try:
        await message.reply_photo(
            photo="https://te.legra.ph/file/3e40a408286d4eda24191.jpg",
            caption=(
                "✨ **NɪɢʜᴛMᴏᴅᴇ Cᴏɴᴛʀᴏʟ Pᴀɴᴇʟ** ✨\n\n"
                "🌙 Enable/Disable NightMode for this group.\n"
                "🕙 10 PM → 7 AM IST\n"
                "🚫 Media/Links Restricted | ✏️ Text Allowed",
                has_spoiler=True
            ),
            reply_markup=buttons
        )
    except Exception as e:
        print(f"[nightmode_cmd_error] {e}")


# --------------------------------------------------------
# 🔧 Safe Caption Editor
# --------------------------------------------------------
async def safe_edit_caption(msg, caption):
    try:
        return await msg.edit_caption(caption)
    except:
        try:
            await msg.reply_text(caption)
        except:
            pass


# --------------------------------------------------------
# 🎛 Button Actions
# --------------------------------------------------------
@app.on_callback_query(filters.regex("^(add_night|rm_night)$"))
async def nightcb(_, query: CallbackQuery):
    data = query.data
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    admins = [m.user.id async for m in app.get_chat_members(
        chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    )]

    if user_id not in admins:
        return await query.answer("❌ Only admins can use this.", show_alert=True)

    check_night = await nightdb.find_one({"chat_id": chat_id})

    if data == "add_night":
        if check_night:
            return await safe_edit_caption(query.message, "🌙 **NightMode is already enabled!**")
        await nightmode_on(chat_id)
        return await safe_edit_caption(
            query.message,
            "🌌 **NightMode Activated!**\n🕙 10 PM → 7 AM\n🚫 Media Restricted"
        )

    if data == "rm_night":
        if not check_night:
            return await safe_edit_caption(query.message, "☀️ **NightMode is already disabled!**")
        await nightmode_off(chat_id)
        return await safe_edit_caption(
            query.message,
            "☀️ 𝐃ᴀʏMᴏᴅᴇ 𝐀ᴄᴛɪᴠᴇ!\n🎉 Aʟʟ ᴍᴇssᴀɢᴇ ᴛʏᴘᴇs ᴀʟʟᴏᴡᴇᴅ!"
        )


# --------------------------------------------------------
# 🚫 Delete During Night
# --------------------------------------------------------
@app.on_message(filters.group & (filters.media | filters.sticker | filters.text), group=99)
async def delete_night_messages(_, message: Message):

    try:
        chat_id = message.chat.id
        check_night = await nightdb.find_one({"chat_id": chat_id})
        if not check_night:
            return

        now = datetime.now(IST)
        hour = now.hour
        is_night = hour >= 22 or hour < 7
        if not is_night:
            return

        # allow commands
        if message.text and message.text.startswith("/"):
            return

        if message.entities:
            for ent in message.entities:
                if getattr(ent, "type", None) in ("bot_command", MessageEntityType.BOT_COMMAND):
                    if ent.offset == 0:
                        return

        # delete media
        if (
            message.sticker or message.photo or message.video or
            message.animation or message.audio or message.voice or
            message.video_note or (message.text and ("http" in message.text))
        ):
            await message.delete()
            warn = await message.reply_text(
                "⚠️ **NightMode Active (10PM – 7AM)**\n🚫 Media/Links Restricted"
            )
            await asyncio.sleep(4)
            await warn.delete()

    except Exception as e:
        print(f"[nightmode_delete_error] {e}")


# --------------------------------------------------------
# 🌙 Scheduled NightMode
# --------------------------------------------------------
async def start_nightmode():
    schats = await get_nightchats()
    chats = [int(x["chat_id"]) for x in schats] if schats else []
    for chat in chats:
        try:
            await app.send_photo(
                chat,
                photo="https://te.legra.ph/file/3e40a408286d4eda24191.jpg",
                caption="🌙 **NightMode Active:**\n🚫 Media Restricted\n✏️ Text Allowed",
                has_spoiler=True
            )
            await app.set_chat_permissions(chat, CLOSE_CHAT)
        except:
            pass


# --------------------------------------------------------
# 🌞 Scheduled DayMode
# --------------------------------------------------------
async def close_nightmode():
    schats = await get_nightchats()
    chats = [int(x["chat_id"]) for x in schats] if schats else []
    for chat in chats:
        try:
            await app.send_photo(
                chat,
                photo="https://i.ibb.co/Q3RtJqHs/x.jpg",
                caption="☀️ 𝐃ᴀʏMᴏᴅᴇ 𝐀ᴄᴛɪᴠᴇ!\n🎉 Aʟʟ ᴍᴇssᴀɢᴇ ᴛʏᴘᴇs ᴀʟʟᴏᴡᴇᴅ!",
                has_spoiler=True
            )
            await app.set_chat_permissions(chat, OPEN_CHAT)
        except:
            pass


# --------------------------------------------------------
# 🧠 SAFE Scheduler (NO DUPLICATION EVER)
# --------------------------------------------------------
async def _start_scheduler_task():
    global GLOBAL_SCHEDULER

    scheduler = AsyncIOScheduler(timezone=timezone("Asia/Kolkata"))
    scheduler.add_job(start_nightmode, "cron", hour=22, minute=0)
    scheduler.add_job(close_nightmode, "cron", hour=7, minute=0)
    scheduler.start()

    GLOBAL_SCHEDULER = scheduler
    print("🌙 NightMode Scheduler started (Asia/Kolkata)")


if not builtins.NIGHTMODE_SCHEDULER_STARTED:
    asyncio.create_task(_start_scheduler_task())
    builtins.NIGHTMODE_SCHEDULER_STARTED = True
    print("🛡 Scheduler Safe-Started")
else:
    print("⚠️ Scheduler already running — skipped")


# --------------------------------------------------------
# 📋 /jobs → list all jobs
# --------------------------------------------------------
@app.on_message(filters.command("jobs"))
async def jobs_cmd(_, message):
    try:
        global GLOBAL_SCHEDULER
        scheduler = GLOBAL_SCHEDULER

        if scheduler is None:
            return await message.reply("⚠️ Scheduler abhi start nahi hua!")

        jobs = scheduler.get_jobs()
        if not jobs:
            return await message.reply("📭 **No jobs found**")

        text = "🗂 **Active Scheduler Jobs:**\n\n"
        for j in jobs:
            text += f"• `{j.id}` → {j.next_run_time}\n"

        await message.reply(text)
    except Exception as e:
        await message.reply(f"❌ Error: {e}")


# --------------------------------------------------------
# 🧹 /clearjobs → remove all scheduler jobs
# --------------------------------------------------------
@app.on_message(filters.command("clearjobs"))
async def clearjobs_cmd(_, message):
    try:
        global GLOBAL_SCHEDULER
        scheduler = GLOBAL_SCHEDULER

        if scheduler is None:
            return await message.reply("⚠️ Scheduler abhi start nahi hua!")

        scheduler.remove_all_jobs()
        await message.reply("🧹 **All NightMode scheduler jobs removed!**")

    except Exception as e:
        await message.reply(f"❌ Error: {e}")
