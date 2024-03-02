import os

from config import (
    PLAYLIST_FETCH_LIMIT, STREAM_IMG_URL, TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL, DURATION_LIMIT, QUEUE_LIMIT, db
)

from typing import Union

from pyrogram.types import InlineKeyboardMarkup

from xMusic import Carbon, YouTube, app
from xMusic.core.call import AltCall
from xMusic.utils.pastebin import Altbin
from xMusic.utils.thumbnails import gen_thumb
from xMusic.utils.exceptions import AssistantErr
from xMusic.utils.inline.play import stream_markup
from xMusic.utils.stream.queue import put_queue, put_queue_index
from xMusic.utils.database import is_active_chat, add_active_video_chat


async def stream(
    _,
    mystic,
    result,
    chat_id,
    user_name,
    original_chat_id,
    video: Union[bool, str] = None,
    streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None,
    forceplay: Union[bool, str] = None,
):
    if not result:
        return
    if forceplay:
        await AltCall.force_stop_stream(chat_id)

    if streamtype == "playlist":
        msg = f"{_['playlist_2']}\n\n"
        count = 0
        for search in result:
            if count >= PLAYLIST_FETCH_LIMIT:
                break
            try:
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                    vidid,
                ) = await YouTube.details(
                    search, False if spotify else True
                )
            except:
                continue
            if str(duration_min) == "None":
                continue
            if duration_sec > DURATION_LIMIT:
                continue
            if await is_active_chat(chat_id):
                await put_queue(
                    chat_id,
                    original_chat_id,
                    f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    "video" if video else "audio",
                )
                position = len(db.get(chat_id)) - 1
                count += 1
                msg += f"{count}- {title[:70]}\n"
                msg += f"{_['playlist_3']} {position}\n\n"
            else:
                if not forceplay:
                    db[chat_id] = []
                status = True if video else None
                try:
                    file_path, direct = await YouTube.download(vidid, mystic, video=status, videoid=True)
                except:
                    raise AssistantErr(_["play_16"])
                await AltCall.join_call(chat_id, original_chat_id, file_path, video=status)
                await put_queue(
                    chat_id,
                    original_chat_id,
                    file_path if direct else f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    "video" if video else "audio",
                    forceplay=forceplay,
                )
                img = await gen_thumb(vidid)
                button = stream_markup(_, chat_id, app.username)
                await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(title[:27], f"https://t.me/{app.username}?start=info_{vidid}", duration_min, user_name[:31]),
                    reply_markup=InlineKeyboardMarkup(button),
                )
        if count == 0:
            return
        else:
            link = await Altbin(msg)
            lines = msg.count("\n")
            if lines >= 17:
                car = os.linesep.join(msg.split(os.linesep)[:17])
            else:
                car = msg
            carbon = await Carbon.generate(car, chat_id)
            return await app.send_photo(
                original_chat_id,
                photo=carbon,
                caption=_["playlist_4"].format(position, link)
            )

    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        status = True if video else None
        try:
            file_path, direct = await YouTube.download(vidid, mystic, videoid=True, video=status)
        except:
            raise AssistantErr(_["play_16"])
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            if position > QUEUE_LIMIT:
                raise AssistantErr(_["play_19"].format(QUEUE_LIMIT))
            await app.send_message(
                original_chat_id,
                _["queue_4"].format(position, title[:30], duration_min, user_name[:31]),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await AltCall.join_call(chat_id, original_chat_id, file_path, video=status)
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            img = await gen_thumb(vidid)
            button = stream_markup(_, chat_id, app.username)
            await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["stream_1"].format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    duration_min,
                    user_name[:31],
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )

    elif streamtype == "telegram":
        file_path = result["path"]
        link = result["link"]
        title = (result["title"]).title()
        duration_min = result["dur"]
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            if position > QUEUE_LIMIT:
                raise AssistantErr(_["play_19"].format(QUEUE_LIMIT))
            await app.send_message(
                original_chat_id,
                _["queue_4"].format(position, title[:30], duration_min, user_name[:31]),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await AltCall.join_call(chat_id, original_chat_id, file_path, video=status)
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            if video:
                await add_active_video_chat(chat_id)
            button = stream_markup(_, chat_id, app.username)
            await app.send_photo(
                original_chat_id,
                photo=TELEGRAM_VIDEO_URL if video else TELEGRAM_AUDIO_URL,
                caption=_["stream_4"].format(title, link, duration_min, user_name[:31]),
                reply_markup=InlineKeyboardMarkup(button),
            )

    elif streamtype == "live":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = "00:00"
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                f"live_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            if position > QUEUE_LIMIT:
                raise AssistantErr(_["play_19"].format(QUEUE_LIMIT))
            await app.send_message(
                original_chat_id,
                _["queue_4"].format(position, title[:30], duration_min, user_name[:31]),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            n, file_path = await YouTube.video(link)
            if n == 0:
                raise AssistantErr(_["str_3"])
            await AltCall.join_call(chat_id, original_chat_id, file_path, video=status)
            await put_queue(
                chat_id,
                original_chat_id,
                f"live_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            img = await gen_thumb(vidid)
            button = stream_markup(_, chat_id, app.username)
            await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["stream_1"].format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    duration_min,
                    user_name[:31],
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )

    elif streamtype == "index":
        link = result
        title = "Index or M3u8 Link"
        duration_min = "URL stream"
        if await is_active_chat(chat_id):
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            if position > QUEUE_LIMIT:
                raise AssistantErr(_["play_19"].format(QUEUE_LIMIT))
            await mystic.edit_text(
                _["queue_4"].format(position, title[:30], duration_min, user_name[:31])
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await AltCall.join_call(chat_id, original_chat_id, link, video=True if video else None,)
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = stream_markup(_, chat_id, app.username)
            await app.send_photo(
                original_chat_id,
                photo=STREAM_IMG_URL,
                caption=_["stream_2"].format(user_name[:31]),
                reply_markup=InlineKeyboardMarkup(button),
            )
            await mystic.delete()
