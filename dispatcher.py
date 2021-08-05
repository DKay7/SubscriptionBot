import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from config.bot_config import BOT_TOKEN
from config.db import DB_STORAGE_HOST, DB_STORAGE_PORT, STORAGE_NAME
from utils.subscription_checker import setup_scheduler


# initialize mongo database
mongo_storage = MongoStorage(host=DB_STORAGE_HOST, port=DB_STORAGE_PORT, db_name=STORAGE_NAME)


# initialize bot and FSM storage
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=mongo_storage)


# setup logging
logging.basicConfig(level=logging.INFO)

# setup scheduling
sched = setup_scheduler(bot)
sched.start()
