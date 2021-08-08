import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from asyncio import get_event_loop

from config.bot_config import BOT_TOKEN
from config.db import DB_STORAGE_HOST, DB_STORAGE_PORT, STORAGE_NAME
from utils.channel.subscription_checker import setup_scheduler
from filters.admin_check_filter import AdminFilter

# initialize mongo database
mongo_storage = MongoStorage(host=DB_STORAGE_HOST, port=DB_STORAGE_PORT, db_name=STORAGE_NAME)


# initialize bot and FSM storage
loop = get_event_loop()
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=mongo_storage, loop=loop)


# Bind filters
dp.filters_factory.bind(AdminFilter)


# setup logging
logging.basicConfig(level=logging.INFO)

# setup scheduling
sched = setup_scheduler(bot)
sched.start()
