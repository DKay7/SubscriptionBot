from aiogram.types import BotCommand
from aiogram import Dispatcher
from dispatcher import sched


async def on_startup(dp: Dispatcher):
    await dp.bot.set_my_commands([
        BotCommand("start", "🍓 Начать / Перезапустить"),
        BotCommand("help", "❓ Помощь (FAQ)"),
    ])


async def on_shutdown(dp: Dispatcher):
    sched.shutdown(wait=False)
    await dp.storage.close()
    await dp.storage.wait_closed()
