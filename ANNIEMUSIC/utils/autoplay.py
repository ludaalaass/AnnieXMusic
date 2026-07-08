from ANNIEMUSIC.core.mongo import mongodb
from ANNIEMUSIC.misc import db
from ANNIEMUSIC.platforms.Youtube import YouTubeAPI
from strings import get_string

import asyncio
import re
import time
import aiohttp
import hashlib
import random

yt = YouTubeAPI()
autoplay_db = mongodb.autoplay

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔥 PROTECTION SYSTEM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECENT = {}
AUTO_PLAYING = {}
ARTIST_HISTORY = {}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🇮🇳 ONLY INDIAN LANGUAGE TRENDING QUERIES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

INDIAN_TRENDING_QUERIES = {
    "hindi": [
        "bollywood songs 2024",
        "hindi hit songs 2024",
        "latest hindi songs",
        "top bollywood songs",
        "hindi romantic songs",
        "hindi sad songs",
        "bollywood party songs",
        "arijit singh songs",
        "atif aslam songs",
        "neha kakkar songs",
        "badshah songs",
        "honey singh songs",
        "shreya ghoshal songs",
        "jubin nautiyal songs",
    ],
    "punjabi": [
        "punjabi songs 2024",
        "sidhu moosewala songs",
        "diljit dosanjh songs",
        "karan aujla songs",
        "latest punjabi songs",
        "punjabi hit songs",
        "punjabi romantic songs",
        "punjabi sad songs",
    ],
    "bhojpuri": [
        "bhojpuri songs 2024",
        "bhojpuri hit songs",
        "pawan singh songs",
        "khesari lal songs",
    ],
    "marathi": [
        "marathi songs 2024",
        "marathi hit songs",
        "marathi romantic songs",
    ],
    "tamil": [
        "tamil songs 2024",
        "tamil hit songs",
        "tamil romantic songs",
    ],
    "telugu": [
        "telugu songs 2024",
        "telugu hit songs",
        "telugu romantic songs",
    ],
    "gujarati": [
        "gujarati songs 2024",
        "gujarati hit songs",
    ],
    "bengali": [
        "bengali songs 2024",
        "bengali hit songs",
    ],
}

# All Indian languages list for random selection
ALL_INDIAN_LANGS = ["hindi", "punjabi", "bhojpuri", "marathi", "tamil", "telugu", "gujarati", "bengali"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎤 INDIAN ARTIST DATABASE (ONLY SINGERS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

INDIAN_ARTIST_DB = {
    # Hindi
    "arijit singh": ["arijit singh", "arijit", "arijeet"],
    "atif aslam": ["atif aslam", "atif"],
    "jubin nautiyal": ["jubin nautiyal", "jubin"],
    "neha kakkar": ["neha kakkar", "neha"],
    "badshah": ["badshah"],
    "yo yo honey singh": ["honey singh", "yo yo"],
    "shreya ghoshal": ["shreya ghoshal", "shreya"],
    "sunidhi chauhan": ["sunidhi chauhan", "sunidhi"],
    "kishore kumar": ["kishore kumar", "kishore"],
    "lata mangeshkar": ["lata mangeshkar", "lata"],
    "alka yagnik": ["alka yagnik", "alka"],
    "udit narayan": ["udit narayan", "udit"],
    "sonu nigam": ["sonu nigam", "sonu"],
    "kumar sanu": ["kumar sanu", "sanu"],
    "kk": ["kk"],
    "mohit chauhan": ["mohit chauhan", "mohit"],
    "palak muchhal": ["palak muchhal", "palak"],
    "tulsi kumar": ["tulsi kumar", "tulsi"],
    "shaan": ["shaan"],
    # Punjabi
    "sidhu moosewala": ["sidhu moosewala", "sidhu"],
    "diljit dosanjh": ["diljit dosanjh", "diljit"],
    "karan aujla": ["karan aujla", "karan"],
    "ammy virk": ["ammy virk", "ammy"],
    "guru randhawa": ["guru randhawa", "guru"],
    "ap dhillon": ["ap dhillon", "ap"],
    "gurdas maan": ["gurdas maan", "gurdas"],
    # Bhojpuri
    "pawan singh": ["pawan singh", "pawan"],
    "khesari lal": ["khesari lal", "khesari"],
    # Marathi
    "ajay atul": ["ajay atul", "ajay"],
    "shreya ghoshal marathi": ["shreya ghoshal marathi"],
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🇮🇳 INDIAN LANGUAGE DETECTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

def detect_indian_lang(title):
    """सिर्फ इंडियन लैंग्वेज डिटेक्ट करेगा"""
    if not title:
        return random.choice(["hindi", "punjabi"])
    
    title = title.lower()
    
    # Hindi keywords
    hindi_keywords = ["arijit", "atif", "shreya", "bollywood", "hindi", "jubin", "neha", "badshah", "honey singh", "kk", "sonu nigam", "udit", "alka", "lata", "kishore"]
    
    # Punjabi keywords
    punjabi_keywords = ["sidhu", "diljit", "punjabi", "karan aujla", "ammy virk", "guru randhawa", "ap dhillon", "gurdas maan"]
    
    # Bhojpuri keywords
    bhojpuri_keywords = ["bhojpuri", "pawan singh", "khesari lal", "bhojpuriya"]
    
    # Marathi keywords
    marathi_keywords = ["marathi", "ajay atul", "marathi song"]
    
    # Tamil keywords
    tamil_keywords = ["tamil", "tamil song", "kollywood", "ar rahman tamil"]
    
    # Telugu keywords
    telugu_keywords = ["telugu", "tollywood", "telugu song"]
    
    # Gujarati keywords
    gujarati_keywords = ["gujarati", "gujarati song"]
    
    # Bengali keywords
    bengali_keywords = ["bengali", "bangla", "bengali song"]
    
    for word in hindi_keywords:
        if word in title:
            return "hindi"
    
    for word in punjabi_keywords:
        if word in title:
            return "punjabi"
    
    for word in bhojpuri_keywords:
        if word in title:
            return "bhojpuri"
    
    for word in marathi_keywords:
        if word in title:
            return "marathi"
    
    for word in tamil_keywords:
        if word in title:
            return "tamil"
    
    for word in telugu_keywords:
        if word in title:
            return "telugu"
    
    for word in gujarati_keywords:
        if word in title:
            return "gujarati"
    
    for word in bengali_keywords:
        if word in title:
            return "bengali"
    
    # Default to random Indian language
    return random.choice(ALL_INDIAN_LANGS)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 NORMALIZE SONG TITLE (IMPROVED)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

def normalize_song_title(title):
    """नॉर्मलाइज करता है गाने का टाइटल"""
    if not title:
        return ""
    
    title_lower = title.lower().strip()
    
    # Remove separators
    if " - " in title_lower:
        title_lower = title_lower.split(" - ")[0].strip()
    if " | " in title_lower:
        title_lower = title_lower.split(" | ")[0].strip()
    if " (" in title_lower:
        title_lower = title_lower.split(" (")[0].strip()
    if " [" in title_lower:
        title_lower = title_lower.split(" [")[0].strip()
    
    # Remove suffixes
    suffixes_to_remove = [
        "official video", "official music video", "official lyric video",
        "lyrics", "lyrical", "audio", "full song", "full video",
        "video song", "music video", "song", "track", "official",
        "video", "hd", "4k", "1080p", "hq"
    ]
    
    for suffix in suffixes_to_remove:
        if title_lower.endswith(f" {suffix}"):
            title_lower = title_lower[:-len(f" {suffix}")].strip()
        elif title_lower.startswith(f"{suffix} "):
            title_lower = title_lower[len(f"{suffix} "):].strip()
    
    # Remove featured artists
    import re
    patterns = [
        r"\s+feat\..*$",
        r"\s+featuring.*$",
        r"\s+ft\..*$",
        r"\s+present.*$",
        r"\s+by\s+\w+.*$",
        r"\s+x\s+\w+.*$",
        r"\s+&\s+\w+.*$",
    ]
    
    for pattern in patterns:
        title_lower = re.sub(pattern, "", title_lower, flags=re.IGNORECASE).strip()
    
    # Clean up
    title_lower = re.sub(r'\s+', ' ', title_lower).strip()
    title_lower = re.sub(r'[^\w\s]', '', title_lower)
    
    return title_lower

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔁 REPEAT CHECK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

def is_same_song(title1, title2):
    """दो गाने एक ही हैं या नहीं"""
    if not title1 or not title2:
        return False
    
    norm1 = normalize_song_title(title1)
    norm2 = normalize_song_title(title2)
    
    if norm1 == norm2:
        return True
    
    if len(norm1) > 5 and len(norm2) > 5:
        if norm1 in norm2 or norm2 in norm1:
            return True
    
    words1 = norm1.split()[:3]
    words2 = norm2.split()[:3]
    
    if words1 and words2:
        if words1[0] == words2[0]:
            if len(words1) > 1 and len(words2) > 1:
                if words1[1] == words2[1]:
                    return True
            else:
                return True
    
    return False

async def is_repeat(chat_id, vidid, title=None):
    if chat_id not in RECENT:
        RECENT[chat_id] = []
    current = time.time()
    
    RECENT[chat_id] = [(v, t, ti) for v, t, ti in RECENT[chat_id] if current - t < 7200]
    
    for stored_vidid, _, stored_title in RECENT[chat_id]:
        if stored_vidid == vidid:
            return True
    
    if title:
        for _, _, stored_title in RECENT[chat_id]:
            if is_same_song(stored_title, title):
                return True
    
    return False

async def add_recent(chat_id, vidid, title=""):
    if chat_id not in RECENT:
        RECENT[chat_id] = []
    RECENT[chat_id].append((vidid, time.time(), title))
    if len(RECENT[chat_id]) > 50:
        RECENT[chat_id] = RECENT[chat_id][-50:]

async def add_artist_song(chat_id, artist, vidid, title):
    if chat_id not in ARTIST_HISTORY:
        ARTIST_HISTORY[chat_id] = {}
    if artist not in ARTIST_HISTORY[chat_id]:
        ARTIST_HISTORY[chat_id][artist] = []
    current_time = time.time()
    
    ARTIST_HISTORY[chat_id][artist] = [(v, t, ti) for v, t, ti in ARTIST_HISTORY[chat_id][artist] if current_time - t < 10800]
    
    for stored_vidid, _, stored_title in ARTIST_HISTORY[chat_id][artist]:
        if stored_vidid == vidid or is_same_song(stored_title, title):
            return False
    
    ARTIST_HISTORY[chat_id][artist].append((vidid, current_time, title.lower()))
    if len(ARTIST_HISTORY[chat_id][artist]) > 20:
        ARTIST_HISTORY[chat_id][artist] = ARTIST_HISTORY[chat_id][artist][-20:]
    return True

async def is_artist_song_played(chat_id, artist, title):
    if chat_id not in ARTIST_HISTORY or artist not in ARTIST_HISTORY[chat_id]:
        return False
    
    current_time = time.time()
    for _, timestamp, played_title in ARTIST_HISTORY[chat_id][artist]:
        if current_time - timestamp < 10800:
            if is_same_song(played_title, title):
                return True
    return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎵 VALIDATE MUSIC (ONLY 5-7 MIN, NO MOVIES)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

def is_valid_music_video(title, duration_min):
    """ONLY 5-7 minute songs, NO movies/albums/live"""
    
    title_lower = title.lower()
    
    # ❌ REJECT - Movies/Albums/Live/Full concerts
    reject_keywords = [
        "movie", "film", "full movie", "full album", "juke box", "jukebox",
        "live concert", "live show", "full concert", "episode", "trailer",
        "interview", "documentary", "podcast", "speech", "news", "politics",
        "trump", "biden", "modi", "reaction", "vlog", "prank", "comedy",
        "gaming", "minecraft", "gta", "leaked", "call", "tutorial", "review"
    ]
    
    for word in reject_keywords:
        if word in title_lower:
            print(f"❌ Rejected movie/album: {title}")
            return False
    
    # ✅ ACCEPT - Only these
    accept_keywords = ["song", "music", "audio", "lyrics", "official video"]
    
    has_music_keyword = any(word in title_lower for word in accept_keywords)
    
    if not has_music_keyword:
        print(f"❌ Rejected (no music keyword): {title}")
        return False
    
    # 🔥 CRITICAL: Duration check - ONLY 5-7 MINUTES (300-420 seconds)
    try:
        if ":" in duration_min:
            parts = duration_min.split(":")
            mins = int(parts[0])
            secs = int(parts[1]) if len(parts) > 1 else 0
            
            total_seconds = (mins * 60) + secs
            
            # Strict 5-7 minutes range
            if total_seconds < 210:  # Less than 3.5 minutes - too short
                print(f"❌ Rejected (too short - {duration_min}): {title}")
                return False
            if total_seconds > 480:  # More than 8 minutes - too long
                print(f"❌ Rejected (too long - {duration_min}): {title}")
                return False
            if 210 <= total_seconds <= 480:
                print(f"✅ Duration OK: {duration_min} = {total_seconds} seconds")
            else:
                print(f"❌ Duration invalid: {duration_min}")
                return False
        else:
            return False
    except Exception as e:
        print(f"Duration parse error: {e}")
        return False
    
    return True

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎤 EXTRACT ARTIST
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

def extract_artist(title):
    if not title:
        return ""
    title_lower = title.lower()
    
    for artist, keys in INDIAN_ARTIST_DB.items():
        if any(x in title_lower for x in keys):
            return artist
    
    if " - " in title:
        parts = title.split(" - ")
        if len(parts) > 1 and len(parts[0]) > 2:
            return parts[0].strip()
    
    return ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔥 SMART QUERY BUILDER (ONLY INDIAN SONGS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_smart_queries(title, artist, lang):
    queries = []
    
    # Get normalized core title
    core_title = normalize_song_title(title) if title else ""
    
    # 🔥 ARTIST QUERIES
    if artist:
        queries.append(f"{artist} songs")
        queries.append(f"{artist} hit songs")
        queries.append(f"{artist} best song")
        queries.append(f"{artist} new song 2024")
    
    # 🔥 LANGUAGE SPECIFIC TRENDING
    if lang in INDIAN_TRENDING_QUERIES:
        queries.extend(INDIAN_TRENDING_QUERIES[lang][:5])
    
    # 🔥 CURRENT SONG
    if core_title and len(core_title) > 3 and core_title not in ["trending songs", "latest songs"]:
        queries.append(core_title)
    
    # 🔥 Add random Indian language trending for variety
    other_langs = [l for l in ALL_INDIAN_LANGS if l != lang]
    random.shuffle(other_langs)
    for other_lang in other_langs[:2]:
        if other_lang in INDIAN_TRENDING_QUERIES:
            queries.extend(INDIAN_TRENDING_QUERIES[other_lang][:2])
    
    # Remove duplicates
    queries = list(dict.fromkeys(queries))
    
    # Filter bad keywords
    final = []
    bad_words = ["slowed", "reverb", "lofi", "8d", "mix", "dj remix", "bass boosted", "instrumental", "karaoke"]
    
    for q in queries:
        if not any(x in q.lower() for x in bad_words):
            if len(q) > 5:
                final.append(q)
    
    return final[:15]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎵 BEST SONG FINDER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def get_best_song(chat_id, queries, last_title, artist, lang):
    candidates = []
    
    for q in queries:
        try:
            search_query = f"{q} song"
            
            details, vidid = await yt.track(search_query)
            
            if not vidid:
                continue
            
            title = details.get("title", "")
            duration = details.get("duration_min", "0:00")
            
            # 🔥 CRITICAL: Must pass duration check (5-7 min)
            if not is_valid_music_video(title, duration):
                print(f"❌ Failed validation: {title} | Duration: {duration}")
                continue
            
            # Duplicate check
            if await is_repeat(chat_id, vidid, title):
                print(f"⏭️ Duplicate: {title}")
                continue
            
            if last_title and is_same_song(title, last_title):
                print(f"⏭️ Same as current: {title}")
                continue
            
            # SCORING SYSTEM
            score = 0
            title_lower = title.lower()
            
            # Same artist = high score
            if artist and artist.lower() in title_lower:
                score += 200
                if not await is_artist_song_played(chat_id, artist, title):
                    score += 100
            
            # Same language = medium score
            if lang in title_lower:
                score += 50
            
            # Not recent = bonus
            if not await is_repeat(chat_id, vidid, title):
                score += 30
            
            candidates.append((score, vidid, details))
            print(f"✅ Candidate: {title[:40]} | Duration: {duration} | Score: {score}")
            
        except Exception as e:
            print(f"Search error: {e}")
            continue
        
        await asyncio.sleep(0.3)
    
    # Sort by score
    candidates.sort(key=lambda x: x[0], reverse=True)
    
    # Remove duplicates
    unique_candidates = []
    seen_titles = []
    for score, vidid, details in candidates:
        title = details.get("title", "")
        norm_title = normalize_song_title(title)
        if norm_title not in seen_titles:
            seen_titles.append(norm_title)
            unique_candidates.append((score, vidid, details))
    
    if unique_candidates:
        best_score, best_vidid, best_details = unique_candidates[0]
        print(f"🎯 Selected: {best_details.get('title')} | Score: {best_score}")
        return best_vidid, best_details
    
    return None, None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🖼 THUMBNAIL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def get_thumbnail_direct(video_id):
    urls = [
        f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    ]
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        return url
            except:
                continue
    return urls[-1]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 MAIN AUTOPLAY FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def auto_play_next(client, chat_id):
    from ANNIEMUSIC.utils.database import get_lang
    from ANNIEMUSIC.utils.stream.stream import stream
    from ANNIEMUSIC.core.call import JARVIS

    if AUTO_PLAYING.get(chat_id):
        return
    
    AUTO_PLAYING[chat_id] = True
    
    try:
        data = await autoplay_db.find_one({"chat_id": chat_id})
        if not data or not data.get("status"):
            AUTO_PLAYING[chat_id] = False
            return
        
        msg = await client.send_message(
            chat_id,
            "🔄🇮🇳 ᴀɴɴɪᴇᴍᴜꜱɪᴄ ᴀᴜᴛᴏᴘʟᴀʏ → ꜰɪɴᴅɪɴɢ ɪɴᴅɪᴀɴ ꜱᴏɴɢꜱ 💞"
        )
        
        queue = db.get(chat_id)
        last_title = None
        
        # Get last played song
        if queue and len(queue) > 0:
            last_title = queue[0].get("title", None)
        
        if not last_title and chat_id in RECENT and RECENT[chat_id]:
            for vidid, ts, title in reversed(RECENT[chat_id]):
                if title:
                    last_title = title
                    break
        
        # Default to random Indian language trending
        if not last_title:
            random_lang = random.choice(ALL_INDIAN_LANGS)
            last_title = random.choice(INDIAN_TRENDING_QUERIES[random_lang])
        
        lang = detect_indian_lang(last_title)
        current_artist = extract_artist(last_title)
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🇮🇳 LAST SONG → {last_title}")
        print(f"🎤 ARTIST → {current_artist if current_artist else 'Unknown'}")
        print(f"🌍 LANGUAGE → {lang.upper()}")
        print(f"📝 NORMALIZED → {normalize_song_title(last_title)}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        queries = build_smart_queries(last_title, current_artist, lang)
        print(f"🔍 Generated {len(queries)} search queries (Indian songs only)")
        
        vidid, details = await get_best_song(chat_id, queries, last_title, current_artist, lang)
        
        # FALLBACK: Try different Indian language
        if not vidid:
            print(f"⚠️ Trying different Indian languages...")
            other_langs = [l for l in ALL_INDIAN_LANGS if l != lang]
            random.shuffle(other_langs)
            
            for fallback_lang in other_langs[:3]:
                fallback_queries = INDIAN_TRENDING_QUERIES.get(fallback_lang, [])[:5]
                for q in fallback_queries:
                    details, vidid = await yt.track(f"{q} song")
                    if vidid:
                        title = details.get("title", "")
                        duration = details.get("duration_min", "0:00")
                        if is_valid_music_video(title, duration) and not await is_repeat(chat_id, vidid, title):
                            break
                if vidid:
                    lang = fallback_lang
                    break
        
        # FALLBACK 2: Random Indian artists
        if not vidid:
            print(f"⚠️ Trying random Indian artists...")
            random_artists = list(INDIAN_ARTIST_DB.keys())
            random.shuffle(random_artists)
            
            for artist in random_artists[:5]:
                details, vidid = await yt.track(f"{artist} songs")
                if vidid:
                    title = details.get("title", "")
                    duration = details.get("duration_min", "0:00")
                    if is_valid_music_video(title, duration) and not await is_repeat(chat_id, vidid, title):
                        current_artist = artist
                        break
        
        if not vidid:
            await msg.edit_text("❌ 🇮🇳 ɴᴏ ɪɴᴅɪᴀɴ ꜱᴏɴɢ ꜰᴏᴜɴᴅ. ᴛʀʏɪɴɢ ᴀɢᴀɪɴ...")
            AUTO_PLAYING[chat_id] = False
            return
        
        song_title = details.get("title", "Autoplay Song")
        song_duration = details.get("duration_min", "00:00")
        
        # Final duplicate check
        if await is_repeat(chat_id, vidid, song_title):
            print(f"❌ Duplicate at final stage!")
            AUTO_PLAYING[chat_id] = False
            return await auto_play_next(client, chat_id)
        
        await add_recent(chat_id, vidid, song_title)
        
        if current_artist:
            await add_artist_song(chat_id, current_artist, vidid, song_title)
        
        link = f"https://youtube.com/watch?v={vidid}"
        
        try:
            thumb = details.get("thumb", "")
            if not thumb.startswith("http"):
                thumb = await get_thumbnail_direct(vidid)
        except:
            thumb = await get_thumbnail_direct(vidid)
        
        print(f"⚡ NEXT SONG → {song_title}")
        print(f"⏱️ DURATION → {song_duration} (5-7 min approved)")
        print(f"🔗 LINK → {link}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        language = await get_lang(chat_id)
        _ = get_string(language)
        
        try:
            await JARVIS.stop_stream(chat_id, keep_vc=True)
            await asyncio.sleep(1)
        except:
            pass
        
        await stream(
            _, client, 0,
            {
                "link": link,
                "vidid": vidid,
                "title": song_title,
                "duration_min": song_duration,
                "thumb": thumb,
            },
            chat_id,
            f"{current_artist if current_artist else 'Indian Songs'}",
            chat_id,
            video=False,
            streamtype="youtube",
        )
        
        try:
            await msg.delete()
        except:
            pass
        
    except Exception as e:
        print(f"⚠️ Autoplay Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        AUTO_PLAYING[chat_id] = False
