from typing import Dict, List, Union

from xMusic.core.mongo import mongodb

authuserdb = mongodb.authuser
chatsdb = mongodb.chats
blacklist_chatdb = mongodb.blacklistChat
usersdb = mongodb.tgusersdb
blockeddb = mongodb.blockedusers
othersdb = mongodb.others


# Users

async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    is_served = await usersdb.find_one({"_id": user_id})
    if is_served:
        return
    return await usersdb.insert_one({"_id": user_id})


# Served Chats

async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if chat:
        return True
    return False

async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


# Blacklisted Chats

async def blacklisted_chats() -> list:
    chats_list = []
    async for chat in blacklist_chatdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat["chat_id"])
    return chats_list

async def blacklist_chat(chat_id: int) -> bool:
    if not await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.insert_one({"chat_id": chat_id})
        return True
    return False

async def whitelist_chat(chat_id: int) -> bool:
    if await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.delete_one({"chat_id": chat_id})
        return True
    return False


# Auth Users DB

async def _get_authusers(chat_id: int) -> Dict[str, int]:
    _notes = await authuserdb.find_one({"chat_id": chat_id})
    if _notes:
        return _notes["notes"]
    return {}

async def get_authuser_names(chat_id: int) -> List[str]:
    _notes = []
    for note in await _get_authusers(chat_id):
        _notes.append(note)
    return _notes

async def get_authuser(chat_id: int, name: str) -> Union[bool, dict]:
    _notes = await _get_authusers(chat_id)
    if name in _notes:
        return _notes[name]
    else:
        return False

async def save_authuser(chat_id: int, name: str, note: dict):
    _notes = await _get_authusers(chat_id)
    _notes[name] = note
    await authuserdb.update_one({"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True)

async def delete_authuser(chat_id: int, name: str) -> bool:
    notesd = await _get_authusers(chat_id)
    if name in notesd:
        del notesd[name]
        await authuserdb.update_one({"chat_id": chat_id}, {"$set": {"notes": notesd}}, upsert=True)
        return True
    return False


# Sudoers

async def get_sudoers() -> list:
    sudoers = await othersdb.find_one({"_id": "sudo"})
    if sudoers:
        return sudoers["sudoers"]
    return []

async def add_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.append(user_id)
    await othersdb.update_one({"_id": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True)
    return True

async def remove_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.remove(user_id)
    await othersdb.update_one({"_id": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True)
    return True


# Blocked Users

async def get_banned_users() -> list:
    results = []
    async for user in blockeddb.find({}):
        results.append(user["_id"])
    return results

async def add_banned_user(user_id: int):
    user = await blockeddb.find_one({"_id": user_id})
    if user:
        return
    return await blockeddb.insert_one({"_id": user_id})

async def remove_banned_user(user_id: int):
    user = await blockeddb.find_one({"_id": user_id})
    if user:
        return await blockeddb.delete_one({"_id": user_id})
    return
