from aiogram.types.chat import Chat
from datetime import datetime, timedelta

from config.bot_config import BOT_CHANNEL_ID
from config.messages import message_texts
from utils.db.subscription import upsert_user_subscription
from dispatcher import bot


async def create_invite_link():
    expire_date = datetime.utcnow() + timedelta(days=1)
    link_object = await Chat(id=BOT_CHANNEL_ID).create_invite_link(member_limit=1,
                                                                   expire_date=expire_date)

    link = link_object.invite_link
    return link


async def subscribe_user(user_id: int):
    await bot.unban_chat_member(chat_id=BOT_CHANNEL_ID, user_id=user_id, only_if_banned=True)

    upsert_user_subscription(user_id)
    link = await create_invite_link()
    invite_text = message_texts["channel_invite"].format(link=link)

    return invite_text
