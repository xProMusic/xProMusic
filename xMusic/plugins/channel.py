from config import BANNED_USERS
from strings import get_command

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus, ChatType

from xMusic import app
from xMusic.utils.database import set_cmode
from xMusic.utils.decorators.admins import AdminActual


CHANNELPLAY_COMMAND = get_command("CHANNELPLAY_COMMAND")


@app.on_message(filters.command(CHANNELPLAY_COMMAND) & filters.group & ~BANNED_USERS)
@AdminActual
async def playmode_(client, message: Message, _):
    try:
        query = message.text.split(None, 2)[1].lower().strip()
    except:
        return await message.reply_text(_["cplay_1"].format(message.chat.title, CHANNELPLAY_COMMAND[0]))

    if query == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text(_["cplay_7"].format(message.from_user.first_name, message.chat.title))

    elif query == "linked":
        chat = await app.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(_["cplay_3"].format(chat.linked_chat.title, chat.linked_chat.id))
        else:
            return await message.reply_text(_["cplay_2"])

    else:
        if query[0] == "@":
            query = query[1:]
        elif query.startswith("https://t.me/"):
            query = query.split("/")[-1]

        try:
            chat = await app.get_chat(query)
            if chat.type != ChatType.CHANNEL:
                return await message.reply_text(_["cplay_5"])
        except:
            return await message.reply_text(_["cplay_4"])

        try:
            cmember = await app.get_chat_member(chat.id, message.from_user.id)
            if cmember.status != ChatMemberStatus.OWNER:
                return await message.reply_text(_["cplay_6"].format(chat.title))
        except:
            return await message.reply_text(_["cplay_4"])

        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(_["cplay_3"].format(chat.title, chat.id))
