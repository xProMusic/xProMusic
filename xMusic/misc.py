import time
import config

from pyrogram import filters
from xMusic.logging import LOGGER
from xMusic.core.mongo import pymongodb


SUDOERS = filters.user()

_boot_ = time.time()

def sudo():
    global SUDOERS
    OWNER = config.OWNER_ID
    othersdb = pymongodb.others
    sudoers = othersdb.find_one({"_id": "sudo"})
    sudoers = sudoers["sudoers"] if sudoers else []
    SUDOERS.add(OWNER)
    if OWNER not in sudoers:
        sudoers.append(OWNER)
        othersdb.update_one({"_id": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True)
    if sudoers:
        for x in sudoers:
            SUDOERS.add(x)
    LOGGER(__name__).info("Sudo Users Loaded Successfully.")
