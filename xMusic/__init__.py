from xMusic.misc import sudo
from xMusic.core.git import git
from xMusic.core.dir import dirr
from xMusic.logging import LOGGER
from xMusic.core.bot import MusicBot
from xMusic.core.userbot import Userbot


dirr()

git()

sudo()

# Clients
app = MusicBot()
userbot = Userbot()

from xMusic.platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Telegram = TeleAPI()
