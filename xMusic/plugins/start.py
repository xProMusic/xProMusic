import config
import asyncio

from youtubesearchpython.__future__ import VideosSearch

from strings import get_string
from config import BANNED_USERS

from pyrogram import filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from xMusic import app
from xMusic.utils.database import (
    add_served_chat, add_served_user, blacklisted_chats, get_assistant, get_lang
)
from xMusic.utils.inline import help_pannel, private_panel, start_pannel

loop = asyncio.get_running_loop()


@app.on_message(filters.command('start') & filters.private & ~BANNED_USERS)
async def start_comm(client, message: Message):
    try:
        _ = await get_lang(message.chat.id)
        _ = get_string(_)
    except:
        _ = get_string("en")
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                       photo=config.START_IMG_URL,
                       caption=_["help_1"].format(config.SUPPORT_GROUP), reply_markup=keyboard
            )
        elif name[0:3] == "inf":
            m = await message.reply_text(_["general_7"])
            query = name.replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
>> <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀɴᴀᴛɪᴏɴ</b>

📌 <b>ᴛɪᴛʟᴇ:</b> {title}

⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration} ᴍɪɴᴜᴛᴇs
👀 <b>ᴠɪᴇᴡs:</b> <code>{views}</code>
⏰ <b>ᴩᴜʙʟɪsʜᴇᴅ ᴏɴ:</b> {published}
🎥 <b>ᴄʜᴀɴɴᴇʟ:</b> {channel}
📎 <b>ᴄʜᴀɴɴᴇʟ ʟɪɴᴋ:</b> <a href="{channellink}">ᴠɪsɪᴛ ᴄʜᴀɴɴᴇʟ</a>
🔗 <b>ʟɪɴᴋ:</b> <a href="{link}">ᴡᴀᴛᴄʜ ᴏɴ ʏᴏᴜᴛᴜʙᴇ</a>

⚡ sᴇᴀʀᴄʜ ᴩᴏᴡᴇʀᴇᴅ ʙʏ {app.mention}"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʏᴏᴜᴛᴜʙᴇ •", url=link),
                        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode=ParseMode.HTML,
                reply_markup=key,
            )
    else:
        out = private_panel(app.username, _)
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(message.from_user.first_name, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )


@app.on_message(filters.command('start') & filters.group & ~BANNED_USERS)
async def testbot(client, message: Message):
    try:
        _ = await get_lang(message.chat.id)
        _ = get_string(_)
    except:
        _ = get_string("en")
    out = start_pannel(app.username, _)
    return await message.reply_text(
                _["start_1"].format(message.chat.title, app.mention),
                reply_markup=InlineKeyboardMarkup(out),
            )


@app.on_message(filters.new_chat_members, group=2)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.is_self:
                chat_type = message.chat.type
                if chat_type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(_["start_5"].format(f"https://t.me/{app.username}?start=sudolist"))
                    return await app.leave_chat(chat_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(app.username, _)
                await message.reply_text(
                    _["start_3"].format(app.mention, userbot.username, userbot.id),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                added_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
                text = f"**✫** <b><u>ɴᴇᴡ ɢʀᴏᴜᴘ</u></b> **:**\n\n**ᴄʜᴀᴛ ɪᴅ :** `{message.chat.id}`\n**ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :** @{message.chat.username}\n**ᴄʜᴀᴛ ᴛɪᴛʟᴇ :** {message.chat.title}\n\n**ᴀᴅᴅᴇᴅ ʙʏ :** {added_by}"
                reply_markup = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(message.from_user.first_name, user_id=message.from_user.id)
                    ]
                ])
                await client.send_message(config.LOG_GROUP_ID, text, reply_markup=reply_markup)
            return
        except:
            return


@app.on_message(filters.left_chat_member, group=2)
async def on_left_chat_member(client, message: Message):
    if message.left_chat_member.is_self:
        remove_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        text = f"**✫** <b><u>ʟᴇғᴛ ɢʀᴏᴜᴘ</u></b> **:**\n\n**ᴄʜᴀᴛ ɪᴅ :** `{message.chat.id}`\n**ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ** : @{message.chat.username}\n**ᴄʜᴀᴛ ᴛɪᴛʟᴇ :** {message.chat.title}\n\n**ʀᴇᴍᴏᴠᴇᴅ ʙʏ :** {remove_by}"
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(message.from_user.first_name, user_id=message.from_user.id)
            ]
        ])
        try:
            await client.send_message(config.LOG_GROUP_ID, text, reply_markup=reply_markup)
        except:
            await client.send_message(config.LOG_GROUP_ID, text)
