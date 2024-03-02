from config import BANNED_USERS
from strings import get_command

from pyrogram import filters
from pyrogram.types import Message

from xMusic import app
from xMusic.misc import SUDOERS
from xMusic.utils.decorators.language import language
from xMusic.utils.database import add_banned_user, remove_banned_user

# Commands
BLOCK_COMMAND = get_command("BLOCK_COMMAND")
UNBLOCK_COMMAND = get_command("UNBLOCK_COMMAND")
BLOCKED_COMMAND = get_command("BLOCKED_COMMAND")


@app.on_message(filters.command(BLOCK_COMMAND) & SUDOERS)
@language
async def useradd(client, message: Message, _):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        try:
            user = message.text.split(None, 1)[1]
            if "@" in user:
                user = user.replace("@", "")
            user = await app.get_users(user)
        except:
            return await message.reply_text(_["general_1"])
    
    if user.id in BANNED_USERS:
        return await message.reply_text(_["block_1"].format(message.reply_to_message.from_user.mention))
    elif user.id in SUDOERS:
        return await message.reply_text(_["block_8"])

    await add_banned_user(user.id)
    BANNED_USERS.add(user.id)
    await message.reply_text(_["block_2"].format(user.mention))


@app.on_message(filters.command(UNBLOCK_COMMAND) & SUDOERS)
@language
async def userdel(client, message: Message, _):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        try:
            user = message.text.split(None, 1)[1]
            if "@" in user:
                user = user.replace("@", "")
            user = await app.get_users(user)
        except:
            return await message.reply_text(_["general_1"])

    if user.id not in BANNED_USERS:
        return await message.reply_text(_["block_3"])

    await remove_banned_user(user.id)
    BANNED_USERS.remove(user.id)
    await message.reply_text(_["block_4"].format(user.mention))


@app.on_message(filters.command(BLOCKED_COMMAND) & SUDOERS)
@language
async def blockedUsers_list(client, message: Message, _):
    if not BANNED_USERS:
        return await message.reply_text(_["block_5"])
    mystic = await message.reply_text(_["block_6"])
    msg = _["block_7"]
    count = 0
    for users in BANNED_USERS:
        count += 1
        try:
            user = await app.get_users(users)
            msg += f"{count}➤ {user.mention}\n"
        except Exception:
            msg += f"{count}➤ [ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ]{users}\n"
    if count == 0:
        return await mystic.edit_text(_["block_5"])
    else:
        return await mystic.edit_text(msg)
