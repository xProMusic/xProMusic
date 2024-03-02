import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType

from datetime import datetime
from strings import get_command
from config import AUTO_LEAVING_ASSISTANT, AUTO_LEAVE_ASSISTANT_TIME, LOG_GROUP_ID

from xMusic import app
from xMusic.misc import SUDOERS
from xMusic.core.call import AltCall, autoend
from xMusic.utils.database import autoend_off, autoend_on
from xMusic.utils.database import get_client, is_active_chat, is_autoend


AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")


@app.on_message(filters.command(AUTOEND_COMMAND) & SUDOERS)
async def auto_end_stream(client, message):
    try:
        state = message.text.split(None, 1)[1].strip()
        state = state.lower()
    except:
        return await message.reply_text("**Usage:**\n/autoend [enable|disable]")

    if state == "enable":
        await autoend_on()
        await message.reply_text("**ᴀᴜᴛᴏ ᴇɴᴅ sᴛʀᴇᴀᴍ ᴇɴᴀʙʟᴇᴅ.**\n\nᴀssɪsᴛᴀɴᴛ ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʟᴇᴀᴠᴇ ᴛʜᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ ᴀғᴛᴇʀ ғᴇᴡ ᴍɪɴs ᴡʜᴇɴ ɴᴏ ᴏɴᴇ ɪs ʟɪsᴛᴇɴɪɴɢ.")
    elif state == "disable":
        await autoend_off()
        await message.reply_text("ᴀᴜᴛᴏ ᴇɴᴅ sᴛʀᴇᴀᴍ ᴅɪsᴀʙʟᴇᴅ.")
    else:
        await message.reply_text("**Usage:**\n/autoend [enable|disable]")


async def auto_end():
    while not await asyncio.sleep(5):
        if not await is_autoend():
            continue
        for chat_id in autoend:
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                autoend[chat_id] = {}
                if not await is_active_chat(chat_id):
                    continue
                try:
                    await AltCall.stop_stream(chat_id)
                    await app.send_message(chat_id, "» ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʟᴇғᴛ ᴠɪᴅᴇᴏᴄʜᴀᴛ ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴏɴᴇ ᴡᴀs ʟɪsᴛᴇɴɪɴɢ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.")
                except:
                    continue

asyncio.create_task(auto_end())


async def auto_leave():
    if AUTO_LEAVING_ASSISTANT == str(True):
        while not await asyncio.sleep(AUTO_LEAVE_ASSISTANT_TIME):
            from xMusic.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                left = 0
                try:
                    async for i in client.get_dialogs():
                        if i.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP, ChatType.CHANNEL]:
                            chat_id = i.chat.id
                            if (chat_id != LOG_GROUP_ID) and (chat_id != -1001859846702):
                                if left == 20:
                                    continue
                                if not await is_active_chat(chat_id):
                                    try:
                                        await client.leave_chat(chat_id)
                                        left += 1
                                        await asyncio.sleep(1)
                                    except:
                                        continue
                except:
                    pass

asyncio.create_task(auto_leave())
