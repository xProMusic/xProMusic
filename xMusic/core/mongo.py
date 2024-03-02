from config import MONGO_DB_URI, DB_NAME

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_


_mongo_async_ = _mongo_client_(MONGO_DB_URI)
_mongo_sync_ = MongoClient(MONGO_DB_URI)
mongodb = _mongo_async_[DB_NAME]
pymongodb = _mongo_sync_[DB_NAME]
