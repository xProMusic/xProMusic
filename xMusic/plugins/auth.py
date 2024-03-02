from strings import get_command
from config import BANNED_USERS, adminlist

from pyrogram import filters
from pyrogram.types import Message

from xMusic import app
from xMusic.utils.formatters import int_to_alpha
from xMusic.utils.decorators import AdminActual, language
from xMusic.utils.database import delete_authuser, get_authuser, get_authuser_names, save_authuser


# Commands
AUTH_COMMAND = get_command("AUTH_COMMAND")
UNAUTH_COMMAND = get_command("UNAUTH_COMMAND")
AUTHUSERS_COMMAND = get_command("AUTHUSERS_COMMAND")


@app.on_message(filters.command(AUTH_COMMAND) & filters.group & ~BANNED_USERS)
@AdminActual
async def auth(client, message: Message, _):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        try:
            user = message.text.split(None, 1)[1]
            if "@" in user:
                user = user.replace("@", "")
            user = await app.get_users(user)
        except:
            await message.reply_text(_["general_1"])
            return

    _check = await get_authuser_names(message.chat.id)
    if len(_check) == 20:
        return await message.reply_text(_["auth_1"])

    token = await int_to_alpha(user.id)
    if token not in _check:
        assis = {
            "auth_user_id": user.id,
            "auth_name": user.first_name,
            "admin_id": message.from_user.id,
            "admin_name": message.from_user.first_name,
        }
        get = adminlist.get(message.chat.id)
        if get and (user.id not in get):
            get.append(user.id)
        await save_authuser(message.chat.id, token, assis)
        return await message.reply_text(_["auth_2"].format(user.mention))
    else:
        await message.reply_text(_["auth_3"].format(user.mention))


@app.on_message(filters.command(UNAUTH_COMMAND) & filters.group & ~BANNED_USERS)
@AdminActual
async def unauthusers(client, message: Message, _):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        try:
            user = message.text.split(None, 1)[1]
            if "@" in user:
                user = user.replace("@", "")
            user = await app.get_users(user)
        except:
            await message.reply_text(_["general_1"])
            return

    token = await int_to_alpha(user.id)
    deleted = await delete_authuser(message.chat.id, token)
    get = adminlist.get(message.chat.id)
    if get and (user.id in get):
        get.remove(user.id)
    if deleted:
        return await message.reply_text(_["auth_4"].format(user.mention))
    else:
        return await message.reply_text(_["auth_5"].format(user.mention))


@app.on_message(filters.command(AUTHUSERS_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def authusers(client, message: Message, _):
    _authusers = await get_authuser_names(message.chat.id)
    if _authusers:
        mystic = await message.reply_text(_["auth_6"])
        text = _["auth_7"]
        j = 1
        for note in _authusers:
            _note = await get_authuser(message.chat.id, note)
            user_id = _note["auth_user_id"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await app.get_users(user_id)
                text += f"{j}➤ {user.first_name}[`{user_id}`]\n   {_['auth_8']} {admin_name}[`{admin_id}`]\n\n"
                j += 1
            except:
                continue
        await mystic.edit_text(text)
    else:
        await message.reply_text(_["setting_4"])
