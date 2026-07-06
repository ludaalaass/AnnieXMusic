import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# Load environment variables from .env file
load_dotenv()

# ── Core bot config ────────────────────────────────────────────────────────────
API_ID = int(getenv("API_ID", 37700))
API_HASH = getenv("API_HASH", "db7e06fe13be0c06e426e7906d7c6")
BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_ID = int(getenv("OWNER_ID", 6638833328))
OWNER_USERNAME = getenv("OWNER_USERNAME", "@sahilxalone")
BOT_USERNAME = getenv("BOT_USERNAME", "@NXMUSICroBOT")
BOT_NAME = getenv("BOT_NAME", "˹𝐍𝐱 ꭙ ᴍᴜ𝐬ɪᴄ˼ ♪")
ASSUSERNAME = getenv("ASSUSERNAME", "@NXMUSICroBOT")

# ── Database & logging ─────────────────────────────────────────────────────────
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOGGER_ID = int(getenv("LOGGER_ID", -1003842923746))

# ── Limits (durations in min/sec; sizes in bytes) ──────────────────────────────
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 600))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "1200"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "1800"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "157286400"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "1288490189"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "30"))
# 🔥 Added User Play Limit (Default = 10)
MAX_USER_PLAY_LIMIT = int(getenv("MAX_USER_PLAY_LIMIT", 10))

# ── External APIs ──────────────────────────────────────────────────────────────
COOKIE_URL = getenv("COOKIE_URL")  # required (paste link)
YOUTUBE_API_KEY = getenv("YOUTUBE_API_KEY")  # ✅ added for YouTube access
API_URL = getenv("API_URL")        # optional
API_KEY = getenv("API_KEY")        # optional
DEEP_API = getenv("DEEP_API")      # optional

# ── DeepAI (legacy) API config ────────────────────────────────────────────────
API_KEY = getenv("API_KEY", "PUT")
API_BASE_URL = getenv("API_BASE_URL", "http://34.208.39.84:8000")

# ── HuggingFace API config ─────────────────────────────────────────────────────
HF_API_KEY = getenv("HF_API_KEY")            # HuggingFace personal token
HF_API_URL = getenv("HF_API_URL")            # Model endpoint (e.g., stable-diffusion)

# ── Hosting / deployment ───────────────────────────────────────────────────────
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ── Git / updates ───────────────────────────────
API_URL = getenv("API_URL", 'https://pytdbotapi.thequickearn.xyz') #youtube song url
VIDEO_API_URL = getenv("VIDEO_API_URL", 'https://api.video.thequickearn.xyz')
API_KEY = getenv("API_KEY", None) # youtube song api key, generate free key or buy paid plan from panel.thequickearn.xyz

# -------------------------------------------------------------------
# (Fixed line — previously causing SyntaxError)
# -------------------------------------------------------------------

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://t.me/+3XobX_t--Bk4YmM1")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN")  # needed if repo is private

# ── Support links ──────────────────────────────────────────────────────────────
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/OSINTNXERA")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/+3XobX_t--Bk4YmM1")

# ── Assistant auto-leave ───────────────────────────────────────────────────────
AUTO_LEAVING_ASSISTANT = False
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "3600"))

# ── Debug ──────────────────────────────────────────────────────────────────────
DEBUG_IGNORE_LOG = True

# ── Spotify (optional) ─────────────────────────────────────────────────────────
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773")
# ── Session strings (optional) ─────────────────────────────────────────────────
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")

# ── Media assets ───────────────────────────────────────────────────────────────
START_VIDS = [
    "https://telegra.ph/file/9b7e1b820c72a14d90be7.mp4",
    "https://telegra.ph/file/72f349b1386d6d9374a38.mp4",
    "https://telegra.ph/file/a4d90b0cb759b67d68644.mp4",
]
STICKERS = [
    "CAACAgUAAx0Cd6nKUAACASBl_rnalOle6g7qS-ry-aZ1ZpVEnwACgg8AAizLEFfI5wfykoCR4h4E",
    "CAACAgUAAx0Cd6nKUAACATJl_rsEJOsaaPSYGhU7bo7iEwL8AAPMDgACu2PYV8Vb8aT4_HUPHgQ",
]
HELP_IMG_URL = "https://i.ibb.co/7x5WYR1v/x.jpg"
START_IMG_URL = "https://i.ibb.co/TBc7BQMm/x.jpg"
PING_VID_URL = "https://files.catbox.moe/2jv4js.mp4"
PLAYLIST_IMG_URL = "https://files.catbox.moe/yhaja5.jpg"
STATS_VID_URL = "https://telegra.ph/file/e2ab6106ace2e95862372.mp4"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/mlztag.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/tiss2b.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/1d3da7.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/zhymxl.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/veykzq.jpg"
SPOTIFY_ARTIST_IMG_URL = SPOTIFY_ALBUM_IMG_URL = SPOTIFY_PLAYLIST_IMG_URL = YOUTUBE_IMG_URL

# ── Helpers ────────────────────────────────────────────────────────────────────
def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

# ───── Bot Introduction Messages ───── #
AYU = [
    "ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ ᴠɪʙᴇ ɪs ʟᴏᴀᴅɪɴɢ… 🎧",
    "ꜰɪɴᴅɪɴɢ ʏᴏᴜʀ ᴛᴜɴᴇ, ʙᴀʙʏ... 💞",
    "🎧 ѕᴏɴɢ ʟᴏᴀᴅɪɴɢ ғᴏʀ ᴍʏ ʙᴀʙʏ 💋",
    "🌸 ғɪɴᴅɪɴɢ ʟᴏᴠᴇ ғᴏʀ ʏᴏᴜ, ʙᴀʙʏ 🎧",
    "🌷 ғɪɴᴅɪɴɢ ʏᴏᴜʀ ᴠɪʙᴇ, ᴍʏ ᴄᴜᴛɪᴇ 💘",
    "💓 ғɪɴᴅɪɴɢ ʏᴏᴜʀ ᴍᴜѕɪᴄ, ᴍʏ ᴅᴇᴀʀ 🌹",
    "💞 ʟᴏᴀᴅɪɴɢ ʜᴇᴀʀᴛғᴇʟᴛ ʙᴇᴀᴛѕ, ʙᴀʙʏ 🎶",
    "🎵 ᴍʏ ᴅᴊ ʜᴇᴀʀᴛ ɪѕ ᴍɪxɪɴɢ ʏᴏᴜʀ ᴍᴇʟᴏᴅʏ 💞",
    "🎶 ʙᴀʙʏ ʏᴏᴜʀ ʙᴇᴀᴛ ɪѕ ʟᴏᴀᴅɪɴɢ 💘",
    "💫 ᴛʜᴇ ʀʜʏᴛʜᴍ ᴏғ ʏᴏᴜʀ ʜᴇᴀʀᴛ ɪѕ ᴘʟᴀʏɪɴɢ 🎧",
    "💖 ʏᴏᴜʀ ᴠɪʙᴇ ɪѕ ɴᴏᴡ ᴄᴏɴɴᴇᴄᴛɪɴɢ... 🌸",
    "🎧 ʙᴀʙʏ, ʟᴏᴠᴇ ɪs ɪɴ ᴛʜᴇ ᴀɪʀ 💞",
    "🌹 ᴅᴊ ʜᴇᴀʀᴛ ɪs sʏɴᴄɪɴɢ ᴡɪᴛʜ ʏᴏᴜʀ ʙᴇᴀᴛ 💋",
    "💘 ʙᴀʙʏ, ᴛʜɪs ʙᴇᴀᴛ ɪs ᴍᴀᴅᴇ ғᴏʀ ʏᴏᴜ 🎵",
    "🎶 ʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ sᴍɪʟᴇ ɪɴ ᴍʏ ᴘʟᴀʏʟɪsᴛ 💞",
    "💞 ғɪɴᴅɪɴɢ ʏᴏᴜʀ ᴀɴɴɪᴇᴍᴜsɪᴄ ᴛᴜɴᴇ... 🎧",
    "🌸 ᴍʏ ʜᴇᴀʀᴛ ɪѕ ᴛᴜɴɪɴɢ ᴛᴏ ʏᴏᴜʀ ғʀᴇǫᴜᴇɴᴄʏ 💖",
    "🎧 ʟᴏᴠᴇ ᴍᴏᴅᴇ: ᴀᴄᴛɪᴠᴀᴛᴇᴅ 💞",
    "💓 ᴍʏ ᴍᴜѕɪᴄ ɴᴇᴇᴅѕ ʏᴏᴜʀ sᴍɪʟᴇ ᴛᴏ ᴘʟᴀʏ 🎧",
    "🎶 ᴍʏ ʜᴇᴀʀᴛ ɪѕ ɴᴏᴡ ᴘʟᴀʏɪɴɢ ʏᴏᴜʀ sᴏɴɢ 💘",
]
AYUV = [
    "ʜᴇʟʟᴏ {0}, 🥀\n\n ɪᴛ'ꜱ ᴍᴇ {1} !\n\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ◆ ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ : ʏᴏᴜᴛᴜʙᴇ, ꜱᴘᴏᴛɪꜰʏ,\n┠ ◆ ʀᴇꜱꜱᴏ, ᴀᴘᴘʟᴇᴍꜱᴜꜱɪᴄ , ꜱᴏᴜɴᴅᴄʟᴏᴜᴅ ᴇᴛᴄ.\n┗━━━━━━━━━━━━━━━━━⧫\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ➥ Uᴘᴛɪᴍᴇ : {2}\n┠ ➥ SᴇʀᴠᴇʀSᴛᴏʀᴀɢᴇ : {3}\n┠ ➥ CPU Lᴏᴀᴅ : {4}\n┠ ➥ RAM Cᴏɴsᴜᴘᴛɪᴏɴ : {5}\n┠ ➥ ᴜꜱᴇʀꜱ : {6}\n┠ ➥ ᴄʜᴀᴛꜱ : {7}\n┗━━━━━━━━━━━━━━━━━⧫\n\n🫧 ᴅᴇᴠᴇʟᴏᴩᴇʀ 🪽 ➪ [»»—— 𝐍𝖝 𝐒ᴀʜɪʟ](https://t.me/sahilxalone)",
]

# ── Runtime structures ─────────────────────────────────────────────────────────
BANNED_USERS = filters.user()
adminlist, lyrical, votemode, autoclean, confirmer = {}, {}, {}, [], {}

# ── Minimal validation ─────────────────────────────────────────────────────────
if SUPPORT_CHANNEL and not re.match(r"^https?://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHANNEL URL. Must start with https://")

if SUPPORT_CHAT and not re.match(r"^https?://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHAT URL. Must start with https://")

if not COOKIE_URL:
    raise SystemExit("[ERROR] - COOKIE_URL is required.")

# Only allow these cookie link formats
if not re.match(r"^https://(batbin\.me|pastebin\.com)/[A-Za-z0-9]+$", COOKIE_URL):
    raise SystemExit(
        "[ERROR] - Invalid COOKIE_URL. Use https://batbin.me/<id> or https://pastebin.com/<id>"
    )
