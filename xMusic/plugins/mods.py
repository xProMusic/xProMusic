import os
import shutil
import urllib3

from strings import get_command
from config import OWNER_ID, LOG_FILE_NAME, UPSTREAM_BRANCH

from git import Repo
from asyncio import sleep
from pyrogram import filters
from datetime import datetime
from git.exc import GitCommandError, InvalidGitRepositoryError

from xMusic import app
from xMusic.misc import SUDOERS
from xMusic.utils.pastebin import Altbin
from xMusic.utils.decorators.language import language
from xMusic.utils.database import get_active_chats, remove_active_chat, remove_active_video_chat


# Commands
GETLOG_COMMAND = get_command("GETLOG_COMMAND")
UPDATE_COMMAND = get_command("UPDATE_COMMAND")
RESTART_COMMAND = get_command("RESTART_COMMAND")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@app.on_message(filters.command(GETLOG_COMMAND) & SUDOERS)
@language
async def log_(client, message, _):
    if os.path.exists(LOG_FILE_NAME):
        with open(LOG_FILE_NAME) as log:
            lines = log.readlines()
        data = ""
        try:
            NUMB = int(message.text.split(None, 1)[1])
        except:
            NUMB = 100
        for x in lines[-NUMB:]:
            data += x
        link = await Altbin(data)
        if link:
            return await message.reply_text(link)
        else:
            return await message.reply_document(LOG_FILE_NAME)
    else:
        return await message.reply_text(_["mods_1"].format(LOG_FILE_NAME))


@app.on_message(filters.command(UPDATE_COMMAND) & filters.user(OWNER_ID))
@language
async def update_(client, message, _):
    response = await message.reply_text(_["mods_4"])
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit_text(_["mods_2"])
    except InvalidGitRepositoryError:
        return await response.edit_text(_["mods_3"])

    os.system(f"git fetch origin {UPSTREAM_BRANCH} &> /dev/null")
    await sleep(7)
    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]  # main git repository

    for checks in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        verification = str(checks.count())
    if verification == "":
        return await response.edit_text("ʙᴏᴛ ɪs ᴜᴩ-ᴛᴏ-ᴅᴀᴛᴇ ᴡɪᴛʜ ᴜᴩsᴛʀᴇᴀᴍ ʀᴇᴩᴏ !")
    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[
            (format // 10 % 10 != 1)
            * (format % 10 < 4)
            * format
            % 10 :: 4
        ],
    )
    for info in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        updates += f"<b>➣ #{info.count()}: [{info.summary}](https://t.me/{app.username}) by -> {info.author}</b>\n\t\t\t\t<b>➥ ᴄᴏᴍᴍɪᴛᴇᴅ ᴏɴ:</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
    
    _update_response_ = "<b>ᴀ ɴᴇᴡ ᴜᴩᴅᴀᴛᴇ ɪs ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛʜᴇ ʙᴏᴛ !</b>\n\n➣ ᴩᴜsʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ɴᴏᴡ</code>\n\n**<u>ᴜᴩᴅᴀᴛᴇs:</u>**\n\n"
    _final_updates_ = _update_response_ + updates

    if len(_final_updates_) > 4096:
        url = await Altbin(_final_updates_)
        await response.edit_text(
            f"<b>ᴀ ɴᴇᴡ ᴜᴩᴅᴀᴛᴇ ɪs ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛʜᴇ ʙᴏᴛ !</b>\n\n➣ ᴩᴜsʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ɴᴏᴡ</code>\n\n**<u>ᴜᴩᴅᴀᴛᴇs:</u>** [ᴄʜᴇᴄᴋ ᴜᴩᴅᴀᴛᴇs]({url})", disable_web_page_preview=True
        )
    else:
        await response.edit_text(_final_updates_, disable_web_page_preview=True)

    os.system("git stash &> /dev/null && git pull")
    served_chats = await get_active_chats()
    for x in served_chats:
        await remove_active_chat(x)
        await remove_active_video_chat(x)
    await response.edit_text(f"{_final_updates_}ʙᴏᴛ ᴜᴩᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ! ɴᴏᴡ ᴡᴀɪᴛ ғᴏʀ ғᴇᴡ ᴍɪɴᴜᴛᴇs ᴜɴᴛɪʟ ᴛʜᴇ ʙᴏᴛ ʀᴇsᴛᴀʀᴛs ᴀɴᴅ ᴩᴜsʜ ᴄʜᴀɴɢᴇs !", disable_web_page_preview=True)

    os.system("pip3 install -r requirements.txt")
    os.system(f"kill -9 {os.getpid()} && bash start")
    exit()


@app.on_message(filters.command(RESTART_COMMAND) & filters.user(OWNER_ID))
async def reboot_(_, message):
    response = await message.reply_text("ʀᴇsᴛᴀʀᴛɪɴɢ...")
    served_chats = await get_active_chats()
    for x in served_chats:
        await remove_active_chat(x)
        await remove_active_video_chat(x)
    try:
        shutil.rmtree("downloads")
        shutil.rmtree("cache")
    except:
        pass
    await response.edit_text("ʀᴇsᴛᴀʀᴛ ᴩʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ, ᴡᴀɪᴛ ғᴏʀ ғᴇᴡ ᴍɪɴᴜᴛᴇs ᴜɴᴛɪʟ ᴛʜᴇ ʙᴏᴛ ʀᴇsᴛᴀʀᴛs.")
    os.system(f"kill -9 {os.getpid()} && bash start")
