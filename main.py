import handlers
from dispatcher import dp
from aiogram import executor
from utils.on_startup_and_shutdown import on_startup, on_shutdown


if __name__ == '__main__':
    executor.start_polling(dp,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)
