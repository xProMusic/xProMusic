import asyncio

from strings import get_command
from config import BANNED_USERS, adminlist, lyrical, db

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import CallbackQuery, Message

from xMusic import app
from xMusic.core.call import AltCall
from xMusic.utils.formatters import alpha_to_int
from xMusic.utils.database import get_authuser_names, get_cmode
from xMusic.utils.decorators import ActualAdminCB, AdminActual, language


RELOAD_COMMAND = get_command("RELOAD_COMMAND")
REBOOT_COMMAND = get_command("REBOOT_COMMAND")


@app.on_message(filters.command(RELOAD_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def reload_admin_cache(client, message: Message, _):
    try:
        chat_id = message.chat.id
        adminlist[chat_id] = []
        async for user in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
            if user.privileges.can_manage_video_chats:
                adminlist[chat_id].append(user.user.id)
        authusers = await get_authuser_names(chat_id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_15"])
    except:
        await message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇғʀᴇsʜ ᴀᴅᴍɪɴs ʟɪsᴛ, ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ᴩʀᴏᴍᴏᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.")


@app.on_message(filters.command(REBOOT_COMMAND) & filters.group & ~BANNED_USERS)
@AdminActual
async def restartbot(client, message: Message, _):
    mystic = await message.reply_text(f"ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ ʀᴇsᴛᴀʀᴛɪɴɢ {app.mention} ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ.")
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await AltCall.stop_stream(message.chat.id)
    except:
        pass
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            db[chat_id] = []
            await AltCall.stop_stream(chat_id)
        except:
            pass
    return await mystic.edit_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇsᴛᴀʀᴛᴇᴅ {app.mention} ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ, ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ sᴛᴀʀᴛ ᴩʟᴀʏɪɴɢ ᴀɢᴀɪɴ...")


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(filters.regex("stop_downloading") & ~BANNED_USERS)
@ActualAdminCB
async def stop_download(client, CallbackQuery: CallbackQuery, _):
    message_id = CallbackQuery.message.id
    task = lyrical.get(message_id)

    if not task:
        return await CallbackQuery.answer("ᴅᴏᴡɴʟᴏᴀᴅ ᴀʟʀᴇᴀᴅʏ ᴄᴏᴍᴩʟᴇᴛᴇᴅ.", show_alert=True)
    if task.done() or task.cancelled():
        return await CallbackQuery.answer("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀʟʀᴇᴀᴅʏ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ᴏʀ ᴄᴀɴᴄᴇʟʟᴇᴅ.", show_alert=True)
    
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await CallbackQuery.answer("ᴅᴏᴡɴʟᴏᴀᴅɪɢ ᴄᴀɴᴄᴇʟʟᴇᴅ.", show_alert=True)
            return await CallbackQuery.edit_message_text(f"ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴩʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ ʙʏ {CallbackQuery.from_user.mention}")
        except:
            return await CallbackQuery.answer("ғᴀɪʟᴇᴅ ᴛᴏ ᴄᴀɴᴄᴇʟ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...", show_alert=True)

    await CallbackQuery.answer("ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴏɢɴɪᴢᴇ ᴛʜᴇ ᴏɴɢᴏɪɴɢ ᴛᴀsᴋ.", show_alert=True)
