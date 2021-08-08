from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from config.bot_config import BOT_ADMINS_ID


class AdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: Message):
        return message.from_user.id in BOT_ADMINS_ID
