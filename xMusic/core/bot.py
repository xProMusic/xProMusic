import sys

from config import API_ID, API_HASH, BOT_TOKEN, LOG_GROUP_ID

from xMusic.logging import LOGGER

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus


class MusicBot(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = get_me.first_name
        self.mention = get_me.mention

        m = await self.get_chat_member(LOG_GROUP_ID, self.id)
        if m.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error("Please promote Bot as Admin in Logger Group")
            sys.exit()
        LOGGER(__name__).info(f"MusicBot Started as {self.name}")
        try:
            await self.send_message(
                LOG_GROUP_ID, f"**» Mᴜsɪᴄ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :**\n\n❄ ɴᴀᴍᴇ : {self.name}\n✨ ɪᴅ : `{self.id}`\n💫 ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
            )
        except:
            LOGGER(__name__).error(
                "Bot has failed to access the log Group. Make sure that you have added your bot to your log channel and promoted as admin!"
            )
            sys.exit()
