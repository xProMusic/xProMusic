import config
import psutil
import platform

from strings import get_command
from config import BANNED_USERS

from sys import version as pyver
from pytgcalls.__version__ import __version__ as pytgver

from pyrogram import filters, __version__ as pyrover
from pyrogram.types import Message, CallbackQuery

from xMusic import app
from xMusic.plugins import ALL_MODULES
from xMusic.misc import SUDOERS, pymongodb
from xMusic.core.userbot import assistants
from xMusic.utils.decorators.language import language, languageCB
from xMusic.utils.inline.stats import back_stats_buttons, stats_buttons
from xMusic.utils.database import get_served_chats, get_served_users, get_sudoers


STATS_COMMAND = get_command("STATS_COMMAND")


@app.on_message(filters.command(STATS_COMMAND) & SUDOERS)
@language
async def stats_global(client, message: Message, _):
    upl = stats_buttons(_)
    await message.reply_photo(
        photo=config.STATS_IMG_URL,
        caption=_["stats_2"].format(app.mention),
        reply_markup=upl,
    )


@app.on_callback_query(filters.regex("TopOverall") & SUDOERS)
@languageCB
async def overall_stats(client, CallbackQuery: CallbackQuery, _):
    upl = back_stats_buttons(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    await CallbackQuery.edit_message_text(_["stats_1"])
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    blocked = len(BANNED_USERS)
    sudoers = len(SUDOERS)
    mod = len(ALL_MODULES)
    assistant = len(assistants)
    fetch_playlist = config.PLAYLIST_FETCH_LIMIT
    play_duration = config.DURATION_LIMIT_MIN
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        ass = "ʏᴇs"
    else:
        ass = "ɴᴏ"
    text = f"""**<u>ʙᴏᴛ's sᴛᴀᴛs ᴀɴᴅ ɪɴғᴏ:</u>**

**ᴍᴏᴅᴜʟᴇs:** {mod}
**ᴄʜᴀᴛs:** {served_chats} 
**ᴜsᴇʀs:** {served_users} 
**ʙʟᴏᴄᴋᴇᴅ:** {blocked} 
**sᴜᴅᴏᴇʀs:** {sudoers} 

**ᴀssɪsᴛᴀɴᴛs:** {assistant}
**ᴀss ᴀᴜᴛᴏ ʟᴇᴀᴠᴇ:** {ass}
**ᴅᴜʀᴀᴛɪᴏɴ ʟɪᴍɪᴛ:** {play_duration} ᴍɪɴᴜᴛᴇs
**ᴩʟᴀʏʟɪsᴛ ᴩʟᴀʏ ʟɪᴍɪᴛ:** {fetch_playlist}"""
    try:
        await CallbackQuery.edit_message_caption(text, reply_markup=upl)
    except:
        await CallbackQuery.message.reply_photo(photo=config.STATS_IMG_URL, caption=text, reply_markup=upl)


@app.on_callback_query(filters.regex("bot_stats_sudo") & SUDOERS)
@languageCB
async def overall_stats(client, CallbackQuery: CallbackQuery, _):
    upl = back_stats_buttons(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    await CallbackQuery.edit_message_text(_["stats_1"])
    sc = platform.system()
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = (
        str(round(psutil.virtual_memory().total / (1024.0**3)))
        + " ɢʙ"
    )
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = f"{round(cpu_freq / 1000, 2)}ɢʜᴢ"
        else:
            cpu_freq = f"{round(cpu_freq, 2)}ᴍʜᴢ"
    except:
        cpu_freq = "Unable to Fetch"
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    total = str(total)
    used = hdd.used / (1024.0**3)
    used = str(used)
    free = hdd.free / (1024.0**3)
    free = str(free)
    mod = len(ALL_MODULES)

    try:
        call = pymongodb.command("dbstats")
    except:
        await CallbackQuery.message.reply_text(_["general_8"])
        await CallbackQuery.message.delete()
        return

    datasize = call["dataSize"] / 1024
    datasize = str(datasize)
    storage = call["storageSize"] / 1024
    objects = call["objects"]
    collections = call["collections"]
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    blocked = len(BANNED_USERS)
    sudoers = len(await get_sudoers())
    text = f"""<u><b>ʙᴏᴛ's sᴛᴀᴛs ᴀɴᴅ ɪɴғᴏ:</b></u>

       <u><b>ʜᴀʀᴅᴡᴀʀᴇ</b></u>
**ᴍᴏᴅᴜʟᴇs:** {mod}
**ᴩʟᴀᴛғᴏʀᴍ:** {sc}
**ʀᴀᴍ:** {ram}
**ᴩʜʏsɪᴄᴀʟ ᴄᴏʀᴇs:** {p_core}
**ᴛᴏᴛᴀʟ ᴄᴏʀᴇs:** {t_core}
**ᴄᴩᴜ ғʀᴇǫᴜᴇɴᴄʏ:** {cpu_freq}

       <u><b>sᴏғᴛᴡᴀʀᴇ</b></u>
**ᴩʏᴛʜᴏɴ :** {pyver.split()[0]}
**ᴩʏʀᴏɢʀᴀᴍ :** {pyrover}
**ᴩʏ-ᴛɢᴄᴀʟʟs :** {pytgver}

        <u><b>sᴛᴏʀᴀɢᴇ</b></u>
**ᴀᴠᴀɪʟᴀʙʟᴇ:** {total[:4]} GiB
**ᴜsᴇᴅ:** {used[:4]} GiB
**ғʀᴇᴇ:** {free[:4]} GiB
        
      <u><b>ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛs</b></u>
**ᴄʜᴀᴛs:** {served_chats} 
**ᴜsᴇʀs:** {served_users} 
**ʙʟᴏᴄᴋᴇᴅ:** {blocked} 
**sᴜᴅᴏᴇʀs:** {sudoers} 

      <u><b>ᴍᴏɴɢᴏ ᴅᴀᴛᴀʙᴀsᴇ</b></u>
**sɪᴢᴇ:** {datasize[:6]} Mb
**sᴛᴏʀᴀɢᴇ:** {storage} Mb
**ᴄᴏʟʟᴇᴄᴛɪᴏɴs:** {collections}
**ᴋᴇʏs:** {objects}"""

    try:
        await CallbackQuery.edit_message_caption(text, reply_markup=upl)
    except:
        await CallbackQuery.message.reply_photo(photo=config.STATS_IMG_URL, caption=text, reply_markup=upl)


@app.on_callback_query(filters.regex("GETSTATS") & ~BANNED_USERS)
@languageCB
async def back_buttons(client, CallbackQuery: CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    upl = stats_buttons(_)
    try:
        await CallbackQuery.edit_message_caption(_["stats_2"].format(app.mention), reply_markup=upl)
    except:
        await CallbackQuery.message.reply_photo(
            photo=config.STATS_IMG_URL,
            caption=_["stats_2"].format(app.mention),
            reply_markup=upl,
        )
