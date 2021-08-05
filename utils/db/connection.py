from pymongo import MongoClient
from config.db import DB_STORAGE_HOST, DB_STORAGE_PORT, DB_NAME, COLL_NAMES

client = MongoClient(DB_STORAGE_HOST, DB_STORAGE_PORT)
db = client[DB_NAME]
COLLS = {internal_name: db[coll_name] for internal_name, coll_name in COLL_NAMES.items()}
