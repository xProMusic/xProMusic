import asyncio
import config

from config import db
from strings import get_string

from typing import Union
from datetime import datetime, timedelta

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.errors import (
    ChatAdminRequired, UserAlreadyParticipant, UserNotParticipant, InviteRequestSent, UserDeactivatedBan
)

from pytgcalls import PyTgCalls
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types import (
    JoinedGroupCallParticipant, LeftGroupCallParticipant, AudioParameters,
    AudioQuality, VideoParameters, VideoQuality, Update
)
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall, TelegramServerError

from xMusic import LOGGER, YouTube, app
from xMusic.utils.thumbnails import gen_thumb
from xMusic.utils.exceptions import AssistantErr
from xMusic.utils.inline.play import stream_markup
from xMusic.utils.database import (
    add_active_chat, add_active_video_chat, get_lang, get_loop, group_assistant,
    is_autoend, music_on, set_loop, remove_active_chat, remove_active_video_chat
)
from xMusic.utils.stream.autoclear import auto_clean
from xMusic.utils.database.assistantdatabase import get_assistant


loop = asyncio.get_event_loop()

autoend = {}
counter = {}
AUTO_END_TIME = 1


async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="Assistant1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(
            self.userbot1,
            cache_duration=100,
        )
        self.userbot2 = Client(
            name="Assistant2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(
            self.userbot2,
            cache_duration=100,
        )
        self.userbot3 = Client(
            name="Assistant3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(
            self.userbot3,
            cache_duration=100,
        )
        self.userbot4 = Client(
            name="Assistant4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.four = PyTgCalls(
            self.userbot4,
            cache_duration=100,
        )
        self.userbot5 = Client(
            name="Assistant5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )
        self.five = PyTgCalls(
            self.userbot5,
            cache_duration=100,
        )

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            check = db.get(chat_id)
            check.pop(0)
        except:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def skip_stream(self, chat_id: int, link: str, video: Union[bool, str] = None):
        assistant = await group_assistant(self, chat_id)
        if video:
            stream = AudioVideoPiped(
                link,
                audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH),
                video_parameters=VideoParameters.from_quality(VideoQuality.SD_480p),
            )
        else:
            stream = AudioPiped(link, audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH))
        await assistant.change_stream(chat_id, stream)


    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await group_assistant(self, chat_id)
        stream = (
            AudioVideoPiped(
                file_path,
                audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH),
                video_parameters=VideoParameters.from_quality(VideoQuality.SD_480p),
                additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
            if mode == "video"
            else AudioPiped(
                file_path,
                audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH),
                additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
        )
        await assistant.change_stream(chat_id, stream)

    async def stream_call(self, link):
        assistant = await group_assistant(self, config.LOG_GROUP_ID)
        await assistant.join_group_call(config.LOG_GROUP_ID, AudioVideoPiped(link))
        await asyncio.sleep(0.5)
        await assistant.leave_group_call(config.LOG_GROUP_ID)

    async def join_assistant(self, original_chat_id, chat_id):
        language = await get_lang(original_chat_id)
        _ = get_string(language)
        userbot = await get_assistant(chat_id)
        try:
            get = await app.get_chat_member(chat_id, userbot.id)
            if get.status == ChatMemberStatus.BANNED:
                try:
                    await app.unban_chat_member(chat_id, userbot.id)
                    raise UserNotParticipant
                except ChatAdminRequired:
                    raise AssistantErr(_["call_2"].format(app.mention, userbot.name, userbot.id, userbot.username))
        except ChatAdminRequired:
            raise AssistantErr(_["call_1"])
        except UserNotParticipant:
            chat = await app.get_chat(chat_id)
            if chat.username:
                invitelink = chat.username
            else:
                try:
                    invitelink = chat.invite_link
                    if not invitelink:
                        invitelink = await app.export_chat_invite_link(chat_id)
                except ChatAdminRequired:
                    raise AssistantErr(_["call_1"])
                except Exception as e:
                    raise AssistantErr(e)
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
            try:
                m = await app.send_message(original_chat_id, _["call_4"].format(userbot.name, chat.title))
                await userbot.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(chat_id, userbot.id)
                except:
                    raise AssistantErr(_["call_10"].format(userbot.name))
            except UserDeactivatedBan:
                await app.send_message(config.LOG_GROUP_ID, _["call_8"].format(userbot.name, userbot.id, userbot.username))
                raise AssistantErr(_["call_3"].format(e))
            except Exception as e:
                raise AssistantErr(_["call_3"].format(e))
            await asyncio.sleep(2)
            await m.edit_text(_["call_5"].format(app.mention))

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        if video:
            stream = AudioVideoPiped(
                link,
                audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH),
                video_parameters=VideoParameters.from_quality(VideoQuality.SD_480p),
            )
        else:
            stream = AudioPiped(link, audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH))
        try:
            await assistant.join_group_call(chat_id, stream)
        except NoActiveGroupCall:
            await self.join_assistant(original_chat_id, chat_id)
            try:
                await assistant.join_group_call(chat_id, stream)
            except Exception:
                raise AssistantErr("**ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ғᴏᴜɴᴅ**\n\nᴩʟᴇᴀsᴇ ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ.")
        except AlreadyJoinedError:
            raise AssistantErr("**ᴀssɪsᴛᴀɴᴛ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ**\n\nᴍᴜsɪᴄ ʙᴏᴛ sʏsᴛᴇᴍs ᴅᴇᴛᴇᴄᴛᴇᴅ ᴛʜᴀᴛ ᴀssɪᴛᴀɴᴛ ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ, ɪғ ᴛʜɪs ᴩʀᴏʙʟᴇᴍ ᴄᴏɴᴛɪɴᴜᴇs ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.")
        except TelegramServerError:
            raise AssistantErr("**ᴛᴇʟᴇɢʀᴀᴍ sᴇʀᴠᴇʀ ᴇʀʀᴏʀ**\n\nᴩʟᴇᴀsᴇ ᴛᴜʀɴ ᴏғғ ᴀɴᴅ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ ᴀɢᴀɪɴ.")
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_autoend():
            counter[chat_id] = {}
            users = len(await assistant.get_participants(chat_id))
            if users == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)

    async def change_stream(self, client, chat_id):
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop = loop - 1
                await set_loop(chat_id, loop)
            if popped:
                if config.AUTO_DOWNLOADS_CLEAR == str(True):
                    await auto_clean(popped)
            if not check:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
        except:
            try:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
            except:
                return
        else:
            queued = check[0]["file"]
            language = await get_lang(chat_id)
            _ = get_string(language)
            title = (check[0]["title"]).title()
            user = check[0]["by"]
            original_chat_id = check[0]["chat_id"]
            streamtype = check[0]["streamtype"]
            videoid = check[0]["vidid"]
            check[0]["played"] = 0
            video = True if str(streamtype) == "video" else False
            if "live_" in queued:
                n, link = await YouTube.video(videoid, True)
                if n == 0:
                    return await app.send_message(original_chat_id, text=_["call_6"])
                if video:
                    stream = AudioVideoPiped(
                        link,
                        audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH),
                        video_parameters=VideoParameters.from_quality(VideoQuality.SD_480p),
                    )
                else:
                    stream = AudioPiped(link, audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH))
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(original_chat_id, text=_["call_6"])
                img = await gen_thumb(videoid)
                button = stream_markup(_, chat_id, app.username)
                await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        check[0]["dur"],
                        user[:31],
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
            elif "vid_" in queued:
                mystic = await app.send_message(original_chat_id, _["call_7"])
                try:
                    file_path, direct = await YouTube.download(
                        videoid,
                        mystic,
                        videoid=True,
                        video=True
                        if str(streamtype) == "video"
                        else False,
                    )
                except:
                    return await mystic.edit_text(_["call_6"], disable_web_page_preview=True)
                if video:
                    stream = AudioVideoPiped(
                        file_path,
                        audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH),
                        video_parameters=VideoParameters.from_quality(VideoQuality.SD_480p),
                    )
                else:
                    stream = AudioPiped(file_path, audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH))
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(original_chat_id, text=_["call_6"])
                img = await gen_thumb(videoid)
                button = stream_markup(_, chat_id, app.username)
                await mystic.delete()
                await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        check[0]["dur"],
                        user[:31],
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
            elif "index_" in queued:
                stream = (
                    AudioVideoPiped(
                        videoid,
                        audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH),
                        video_parameters=VideoParameters.from_quality(VideoQuality.SD_480p),
                    )
                    if str(streamtype) == "video"
                    else AudioPiped(videoid, audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH))
                )
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(original_chat_id, text=_["call_6"])
                button = stream_markup(_, chat_id, app.username)
                await app.send_photo(
                    original_chat_id,
                    photo=config.STREAM_IMG_URL,
                    caption=_["stream_2"].format(user[:31]),
                    reply_markup=InlineKeyboardMarkup(button),
                )
            else:
                if video:
                    stream = AudioVideoPiped(
                        queued,
                        audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH),
                        video_parameters=VideoParameters.from_quality(VideoQuality.SD_480p),
                    )
                else:
                    stream = AudioPiped(queued, audio_parameters=AudioParameters.from_quality(AudioQuality.HIGH))
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(original_chat_id, text=_["call_6"])
                if videoid == "telegram":
                    button = stream_markup(_, chat_id, app.username)
                    await app.send_photo(
                        original_chat_id,
                        photo=config.TELEGRAM_AUDIO_URL
                        if str(streamtype) == "audio"
                        else config.TELEGRAM_VIDEO_URL,
                        caption=_["stream_3"].format(title, check[0]["dur"], user[:31]),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                else:
                    img = await gen_thumb(videoid)
                    button = stream_markup(_, chat_id, app.username)
                    await app.send_photo(
                        original_chat_id,
                        photo=img,
                        caption=_["stream_1"].format(
                            title[:27],
                            f"https://t.me/{app.username}?start=info_{videoid}",
                            check[0]["dur"],
                            user[:31],
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )

    async def ping(self):
        pings = []
        if config.STRING1:
            pings.append(await self.one.ping)
        if config.STRING2:
            pings.append(await self.two.ping)
        if config.STRING3:
            pings.append(await self.three.ping)
        if config.STRING4:
            pings.append(await self.four.ping)
        if config.STRING5:
            pings.append(await self.five.ping)
        return str(round(sum(pings) / len(pings), 3))

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...\n")
        if config.STRING1:
            await self.one.start()
        if config.STRING2:
            await self.two.start()
        if config.STRING3:
            await self.three.start()
        if config.STRING4:
            await self.four.start()
        if config.STRING5:
            await self.five.start()

    async def decorators(self):
        @self.one.on_kicked()
        @self.two.on_kicked()
        @self.three.on_kicked()
        @self.four.on_kicked()
        @self.five.on_kicked()
        @self.one.on_closed_voice_chat()
        @self.two.on_closed_voice_chat()
        @self.three.on_closed_voice_chat()
        @self.four.on_closed_voice_chat()
        @self.five.on_closed_voice_chat()
        @self.one.on_left()
        @self.two.on_left()
        @self.three.on_left()
        @self.four.on_left()
        @self.five.on_left()
        async def stream_services_handler(_, chat_id: int):
            await self.stop_stream(chat_id)

        @self.one.on_stream_end()
        @self.two.on_stream_end()
        @self.three.on_stream_end()
        @self.four.on_stream_end()
        @self.five.on_stream_end()
        async def stream_end_handler1(client, update: Update):
            if not isinstance(update, StreamAudioEnded):
                return
            await self.change_stream(client, update.chat_id)

        @self.one.on_participants_change()
        @self.two.on_participants_change()
        @self.three.on_participants_change()
        @self.four.on_participants_change()
        @self.five.on_participants_change()
        async def participants_change_handler(client, update: Update):
            if not isinstance(update, JoinedGroupCallParticipant) and not isinstance(update, LeftGroupCallParticipant):
                return
            chat_id = update.chat_id
            users = counter.get(chat_id)
            if not users:
                try:
                    got = len(await client.get_participants(chat_id))
                except:
                    return
                counter[chat_id] = got
                if got == 1:
                    autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
                    return
                autoend[chat_id] = {}
            else:
                final = users + 1 if isinstance(update, JoinedGroupCallParticipant) else users - 1
                counter[chat_id] = final
                if final == 1:
                    autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
                    return
                autoend[chat_id] = {}


AltCall = Call()
