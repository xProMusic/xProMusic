from datetime import datetime

from strings import get_command

from pyrogram import filters
from pyrogram.types import Message

from xMusic import app
from xMusic.core.call import AltCall
from xMusic.utils import bot_sys_stats
from xMusic.utils.decorators.language import language


PING_COMMAND = get_command("PING_COMMAND")


@app.on_message(filters.command(PING_COMMAND) & filters.group)
@language
async def ping_com(client, message: Message, _):
    response = await message.reply_text(_["ping_1"])
    start = datetime.now()
    pytgping = await AltCall.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000

    await response.edit_text(
        _["ping_2"].format(resp, UP, DISK, RAM, CPU, pytgping)
    )
