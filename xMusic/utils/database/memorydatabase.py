from xMusic.core.mongo import mongodb

channeldb = mongodb.cplaymode
playmodedb = mongodb.playmode
playtypedb = mongodb.playtypedb
langdb = mongodb.language
authdb = mongodb.adminauth
onoffdb = mongodb.onoffper
autoenddb = mongodb.autoend

loop = {}
playtype = {}
playmode = {}
channelconnect = {}
langm = {}
pause = {}
active = []
activevideo = []
nonadmin = {}
maintenance = []
autoend = {}

# Auto End Stream

async def is_autoend() -> bool:
    chat_id = 1234
    return bool(await autoenddb.find_one({"chat_id": chat_id}))

async def autoend_on():
    chat_id = 1234
    await autoenddb.insert_one({"chat_id": chat_id})

async def autoend_off():
    chat_id = 1234
    await autoenddb.delete_one({"chat_id": chat_id})

# LOOP PLAY

async def get_loop(chat_id: int) -> int:
    lop = loop.get(chat_id)
    if lop:
        return lop
    return 0

async def set_loop(chat_id: int, mode: int):
    loop[chat_id] = mode

# Channel Play IDS

async def get_cmode(chat_id: int) -> int:
    mode = channelconnect.get(chat_id)
    if mode:
        return mode
    mode = await channeldb.find_one({"chat_id": chat_id})
    if mode:
        channelconnect[chat_id] = mode["mode"]
        return mode["mode"]
    return None

async def set_cmode(chat_id: int, mode: int):
    channelconnect[chat_id] = mode
    await channeldb.update_one({"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True)

# PLAY TYPE WHETHER ADMINS ONLY OR EVERYONE

async def get_playtype(chat_id: int) -> str:
    mode = playtype.get(chat_id)
    if mode:
        return mode
    mode = await playtypedb.find_one({"chat_id": chat_id})
    if mode:
        playtype[chat_id] = mode["mode"]
        return mode["mode"]
    playtype[chat_id] = "Everyone"
    return "Everyone"

async def set_playtype(chat_id: int, mode: str):
    playtype[chat_id] = mode
    await playtypedb.update_one({"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True)

# play mode whether inline or direct query

async def get_playmode(chat_id: int) -> str:
    mode = playmode.get(chat_id)
    if mode:
        return mode
    mode = await playmodedb.find_one({"chat_id": chat_id})
    if mode:
        playmode[chat_id] = mode["mode"]
        return mode["mode"]
    playmode[chat_id] = "Direct"
    return "Direct"

async def set_playmode(chat_id: int, mode: str):
    playmode[chat_id] = mode
    await playmodedb.update_one({"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True)

# language

async def get_lang(chat_id: int) -> str:
    mode = langm.get(chat_id)
    if mode:
        return mode
    lang = await langdb.find_one({"chat_id": chat_id})
    if lang:
        langm[chat_id] = lang["lang"]
        return lang["lang"]
    langm[chat_id] = "en"
    return "en"

async def set_lang(chat_id: int, lang: str):
    langm[chat_id] = lang
    await langdb.update_one({"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True)

# Pause-Skip

async def is_music_playing(chat_id: int) -> bool:
    mode = pause.get(chat_id)
    if mode:
        return mode
    return False

async def music_on(chat_id: int):
    pause[chat_id] = True

async def music_off(chat_id: int):
    pause[chat_id] = False

# Active Voice Chats

async def get_active_chats() -> list:
    return active

async def is_active_chat(chat_id: int) -> bool:
    if chat_id in active:
        return True
    else:
        return False

async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)

async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)

async def get_active_video_chats() -> list:
    return activevideo

async def add_active_video_chat(chat_id: int):
    if chat_id not in activevideo:
        activevideo.append(chat_id)

async def remove_active_video_chat(chat_id: int):
    if chat_id in activevideo:
        activevideo.remove(chat_id)


# Non Admin Chat

async def check_nonadmin_chat(chat_id: int) -> bool:
    user = await authdb.find_one({"chat_id": chat_id})
    if user:
        return True
    return False

async def is_nonadmin_chat(chat_id: int) -> bool:
    mode = nonadmin.get(chat_id)
    if mode:
        return mode
    user = await authdb.find_one({"chat_id": chat_id})
    if user:
        nonadmin[chat_id] = True
        return True
    nonadmin[chat_id] = False
    return False

async def add_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = True
    is_admin = await check_nonadmin_chat(chat_id)
    if is_admin:
        return
    return await authdb.insert_one({"chat_id": chat_id})

async def remove_nonadmin_chat(chat_id: int):
    nonadmin[chat_id] = False
    is_admin = await check_nonadmin_chat(chat_id)
    if is_admin:
        return await authdb.delete_one({"chat_id": chat_id})
    return


# On-Off

async def is_on_off(on_off: int) -> bool:
    onoff = await onoffdb.find_one({"on_off": on_off})
    if onoff:
        return True
    return False


# Maintenance

async def is_maintenance():
    if maintenance:
        if 1 in maintenance:
            return False
        else:
            return True
    else:
        get = await onoffdb.find_one({"on_off": 1})
        if get:
            maintenance.clear()
            maintenance.append(1)
            return False
        else:
            maintenance.clear()
            maintenance.append(2)
            return True

async def maintenance_off():
    maintenance.clear()
    maintenance.append(2)
    is_off = await is_on_off(1)
    if is_off:
        return await onoffdb.delete_one({"on_off": 1})
    return

async def maintenance_on():
    maintenance.clear()
    maintenance.append(1)
    is_on = await is_on_off(1)
    if is_on:
        return
    return await onoffdb.insert_one({"on_off": 1})
