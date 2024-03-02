from config import BANNED_USERS
from strings import get_command

from pyrogram import filters
from pyrogram.types import Message

from xMusic import app
from xMusic.misc import SUDOERS
from xMusic.utils.decorators.language import language
from xMusic.utils.database import blacklist_chat, blacklisted_chats, whitelist_chat


# Commands

BLACKLISTCHAT_COMMAND = get_command("BLACKLISTCHAT_COMMAND")
WHITELISTCHAT_COMMAND = get_command("WHITELISTCHAT_COMMAND")
BLACKLISTEDCHAT_COMMAND = get_command("BLACKLISTEDCHAT_COMMAND")


@app.on_message(filters.command(BLACKLISTCHAT_COMMAND) & SUDOERS)
@language
async def blacklist_chat_func(client, message: Message, _):
    try:
        chat_id = int(message.text.strip().split()[1])
    except:
        return await message.reply_text(_["black_1"])

    if chat_id in await blacklisted_chats():
        return await message.reply_text(_["black_2"])

    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        await message.reply_text(_["black_3"])
    else:
        await message.reply_text(_["black_9"])
    try:
        await app.leave_chat(chat_id)
    except:
        pass


@app.on_message(filters.command(WHITELISTCHAT_COMMAND) & SUDOERS)
@language
async def white_funciton(client, message: Message, _):
    try:
        chat_id = int(message.text.strip().split()[1])
    except:
        return await message.reply_text(_["black_4"])

    if chat_id not in await blacklisted_chats():
        return await message.reply_text(_["black_5"])

    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(_["black_6"])
    await message.reply_text(_["black_9"])


@app.on_message(filters.command(BLACKLISTEDCHAT_COMMAND) & ~BANNED_USERS)
@language
async def all_chats(client, message: Message, _):
    text = _["black_7"]
    j = 0
    for chat_id in await blacklisted_chats():
        j += 1
        try:
            title = (await app.get_chat(chat_id)).title
        except:
            title = _["S_B_5"]
        text += f"**{j}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text(_["black_8"])
    else:
        await message.reply_text(text)
