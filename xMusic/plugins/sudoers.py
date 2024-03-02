from pyrogram import filters
from pyrogram.types import Message

from strings import get_command
from config import MONGO_DB_URI, OWNER_ID

from xMusic import app
from xMusic.misc import SUDOERS
from xMusic.utils.decorators.language import language
from xMusic.utils.database import add_sudo, remove_sudo

# Commands
ADDSUDO_COMMAND = get_command("ADDSUDO_COMMAND")
DELSUDO_COMMAND = get_command("DELSUDO_COMMAND")
SUDOUSERS_COMMAND = get_command("SUDOUSERS_COMMAND")


@app.on_message(filters.command(ADDSUDO_COMMAND) & filters.user(OWNER_ID))
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
            return await message.reply_text(_["sudo_8"])

    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text("ғᴀɪʟᴇᴅ.")


@app.on_message(filters.command(DELSUDO_COMMAND) & filters.user(OWNER_ID))
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
            return await message.reply_text(_["sudo_9"])

    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
        return
    await message.reply_text("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ!")


@app.on_message(filters.command(SUDOUSERS_COMMAND) & SUDOERS)
@language
async def sudoers_list(client, message: Message, _):
    text = _["sudo_5"]
    owner = await app.get_users(OWNER_ID)
    owner = owner.mention if owner.mention else owner.first_name
    text += f" ➤ {owner}\n"
    ind = 1
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.mention if user.mention else user.first_name
                if ind == 1:
                    text += _["sudo_6"]
                text += f"{ind}➤ {user}\n"
                ind += 1
            except Exception:
                continue
    if text:
        await message.reply_text(text)
    else:
        await message.reply_text(_["sudo_7"])
