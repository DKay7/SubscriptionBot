from aiogram import executor
from dispatcher import dp
import handlers
from utils.on_startup_and_shutdown import on_startup, on_shutdown

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)