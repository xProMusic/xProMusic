from asyncio import sleep

from config import OWNER_ID
from strings import get_command

from pyrogram import filters
from pyrogram.errors import FloodWait

from xMusic import app
from xMusic.utils.decorators.language import language
from xMusic.utils.database import get_served_chats, get_served_users

BROADCAST_COMMAND = get_command("BROADCAST_COMMAND")
STOPBROADCAST_COMMAND = get_command("STOPBROADCAST_COMMAND")

IS_BROADCASTING = False


@app.on_message(filters.command(BROADCAST_COMMAND) & filters.user(OWNER_ID))
@language
async def braodcast_message(client, message, _):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        return await message.reply_text(_["broad_8"])

    copy = False
    if message.reply_to_message:
        if message.text.startswith("/gcastx"):
            copy = True
            markup = message.reply_to_message.reply_markup
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        try:
            query = message.text.split(" ", 1)[1]
        except:
            return await message.reply_text(_["broad_5"])
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await message.reply_text(_["broad_5"])

    IS_BROADCASTING = True

    # Bot broadcast inside chats
    if "-nobot" not in message.text:
        await message.reply_text(_["broad_9"])
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            if not IS_BROADCASTING:
                return
            if (sent % 300 == 0) and (sent > 0):
                await sleep(180)
            try:
                if copy:
                    await app.copy_message(i, y, x, reply_markup=markup)
                elif message.reply_to_message:
                    await app.forward_messages(i, y, x)
                else:
                    await app.send_message(i, text=query)
                sent += 1
                await sleep(1)
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await sleep(flood_time)
            except:
                continue
        try:
            await message.reply_text(_["broad_1"].format(sent))
        except:
            pass

    # Bot broadcasting to users
    if "-user" in message.text:
        await message.reply_text(_["broad_12"])
        susr = 0
        susers = await get_served_users()
        for user in susers:
            if not IS_BROADCASTING:
                return
            if (susr % 300 == 0) and (susr > 0):
                await sleep(180)
            try:
                if copy:
                    await app.copy_message(int(user["_id"]), y, x, reply_markup=markup)
                elif message.reply_to_message:
                    await app.forward_messages(int(user["_id"]), y, x)
                else:
                    await app.send_message(int(user["_id"]), text=query)
                susr += 1
                await sleep(1)
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await sleep(flood_time)
            except:
                pass
        try:
            await message.reply_text(_["broad_7"].format(susr))
        except:
            pass
    IS_BROADCASTING = False


@app.on_message(filters.command(STOPBROADCAST_COMMAND) & filters.user(OWNER_ID))
@language
async def stopbraodcast_message(client, message, _):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        IS_BROADCASTING = False
        await message.reply_text(_["broad_11"])
    else:
        await message.reply_text(_["broad_10"])
