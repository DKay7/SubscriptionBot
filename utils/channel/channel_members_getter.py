import logging

from aiogram import Bot
from telethon.sync import TelegramClient

from config.bot_config import TELEGRAM_API_ID, TELEGRAM_API_HASH, BOT_CHANNEL_ID, BOT_TOKEN
from utils.db.subscription import get_users_with_active_sub, get_users_with_ended_sub


async def get_all_channel_members(bot: Bot):
    client = TelegramClient("test", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH, loop=bot.loop)
    await client.start(bot_token=BOT_TOKEN)

    user_list = await client.get_participants(BOT_CHANNEL_ID, aggressive=True)

    user_list = list(map(lambda user: user.id, user_list))

    await client.log_out()

    return user_list


async def get_channel_admins(bot: Bot):
    admin_list = await bot.get_chat_administrators(BOT_CHANNEL_ID)
    admin_ids = list(map(lambda admin: admin.user.id, admin_list))

    return admin_ids


async def get_users_without_any_sub(bot: Bot):
    all_users = await get_all_channel_members(bot)
    with_sub_users = get_users_with_active_sub()
    with_ended_sub_users = get_users_with_ended_sub()
    admins = await get_channel_admins(bot)
    without_sub = set(all_users) - set(with_sub_users) - set(with_ended_sub_users) - set(admins) - {bot.id}

    log = logging.getLogger("Channel members checker")
    log.debug(f"ALL {all_users}")
    log.debug(f"WITH SUB: {with_sub_users}")
    log.debug(f"WITH ENDED SUB: {with_ended_sub_users}")
    log.debug(f"ADMINS {admins}")
    log.debug(f"TO KICK: {without_sub}")

    return list(without_sub)
