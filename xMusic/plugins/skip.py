from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message

from strings import get_command
from config import BANNED_USERS, AUTO_DOWNLOADS_CLEAR, STREAM_IMG_URL, TELEGRAM_VIDEO_URL, TELEGRAM_AUDIO_URL, db

from xMusic import YouTube, app
from xMusic.core.call import AltCall
from xMusic.utils.database import get_loop
from xMusic.utils.thumbnails import gen_thumb
from xMusic.utils.inline.play import stream_markup
from xMusic.utils.decorators import AdminRightsCheck
from xMusic.utils.stream.autoclear import auto_clean

SKIP_COMMAND = get_command("SKIP_COMMAND")


@app.on_message(filters.command(SKIP_COMMAND) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def skip(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        loop = await get_loop(chat_id)
        if loop != 0:
            return await message.reply_text(_["admin_8"])
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            check = db.get(chat_id)
            if check:
                count = len(check)
                if count > 2:
                    count = int(count - 1)
                    if 1 <= state <= count:
                        for x in range(state):
                            popped = None
                            try:
                                popped = check.pop(0)
                            except:
                                return await message.reply_text(_["admin_12"])
                            if popped:
                                if AUTO_DOWNLOADS_CLEAR == str(True):
                                    await auto_clean(popped)
                            if not check:
                                try:
                                    await message.reply_text(_["admin_6"].format(message.from_user.mention))
                                    await AltCall.stop_stream(chat_id)
                                except:
                                    return
                                break
                    else:
                        return await message.reply_text(_["admin_11"].format(count))
                else:
                    return await message.reply_text(_["admin_10"])
            else:
                return await message.reply_text(_["queue_2"])
        else:
            return await message.reply_text(_["admin_9"])
    else:
        check = db.get(chat_id)
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                if AUTO_DOWNLOADS_CLEAR == str(True):
                    await auto_clean(popped)
            if not check:
                try:
                    await message.reply_text(_["admin_6"].format(message.from_user.mention))
                    return await AltCall.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                await message.reply_text(_["admin_6"].format(message.from_user.mention))
                return await AltCall.stop_stream(chat_id)
            except:
                return

    queued = check[0]["file"]
    title = (check[0]["title"]).title()
    user = check[0]["by"]
    streamtype = check[0]["streamtype"]
    videoid = check[0]["vidid"]
    duration_min = check[0]["dur"]
    status = True if str(streamtype) == "video" else None

    if "live_" in queued:
        n, link = await YouTube.video(videoid, True)
        if n == 0:
            return await message.reply_text(_["admin_7"].format(title))
        try:
            await AltCall.skip_stream(chat_id, link, video=status)
        except:
            return await message.reply_text(_["call_6"])

        button = stream_markup(_, chat_id, app.username)
        img = await gen_thumb(videoid)
        await message.reply_photo(
            photo=img,
            caption=_["stream_1"].format(title[:31], f"https://t.me/{app.username}?start=info_{videoid}", duration_min, user[:31]),
            reply_markup=InlineKeyboardMarkup(button),
        )

    elif "vid_" in queued:
        mystic = await message.reply_text(_["call_7"], disable_web_page_preview=True)
        try:
            file_path, direct = await YouTube.download(videoid, mystic, videoid=True, video=status)
        except:
            return await mystic.edit_text(_["call_6"])
        try:
            await AltCall.skip_stream(chat_id, file_path, video=status)
        except:
            return await mystic.edit_text(_["call_6"])
        button = stream_markup(_, chat_id, app.username)
        img = await gen_thumb(videoid)
        await message.reply_photo(
            photo=img,
            caption=_["stream_1"].format(title[:27], f"https://t.me/{app.username}?start=info_{videoid}", duration_min, user[:31]),
            reply_markup=InlineKeyboardMarkup(button),
        )
        await mystic.delete()

    elif "index_" in queued:
        try:
            await AltCall.skip_stream(chat_id, videoid, video=status)
        except:
            return await message.reply_text(_["call_6"])
        button = stream_markup(_, chat_id, app.username)
        await message.reply_photo(
            photo=STREAM_IMG_URL,
            caption=_["stream_2"].format(user[:31]),
            reply_markup=InlineKeyboardMarkup(button),
        )

    else:
        try:
            await AltCall.skip_stream(chat_id, queued, video=status)
        except:
            return await message.reply_text(_["call_6"])
        if videoid == "telegram":
            button = stream_markup(_, chat_id, app.username)
            await message.reply_photo(
                photo=TELEGRAM_AUDIO_URL
                if str(streamtype) == "audio"
                else TELEGRAM_VIDEO_URL,
                caption=_["stream_3"].format(title[:31], check[0]["dur"], user[:31]),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            button = stream_markup(_, chat_id, app.username)
            img = await gen_thumb(videoid)
            await message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(title[:27], f"https://t.me/{app.username}?start=info_{videoid}", duration_min, user[:31]),
                reply_markup=InlineKeyboardMarkup(button),
            )
