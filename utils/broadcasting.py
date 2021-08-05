from aiogram.utils import exceptions
from aiogram import Bot
import logging
import asyncio

from utils.db.subscription import unsubscribe_user_from_db


async def send_broadcast_message(bot: Bot, user_id: int, text: str, disable_notification: bool = False,
                                 ban: bool = False, chat_id: int = None):
    log = logging.getLogger('broadcast')

    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)

        if ban:
            result = await bot.ban_chat_member(chat_id=chat_id, user_id=user_id)

            if not result:
                log.error(f"User `tg://user?id={user_id}` was not banned!!")
            else:
                unsubscribe_user_from_db(user_id)

    except exceptions.CantRestrictChatOwner:
        log.error(f"Target tg://user?id={user_id} can't ban chat owner")

    except exceptions.BotBlocked:
        log.error(f"Target `tg://user?id={user_id}` blocked by user")

    except exceptions.ChatNotFound:
        log.error(f"Target `tg://user?id={user_id}` invalid user ID")

    except exceptions.RetryAfter as e:
        log.error(f"Target tg://user?id={user_id} Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_broadcast_message(bot, user_id, text)

    except exceptions.UserDeactivated:
        log.error(f"Target tg://user?id={user_id} user is deactivated")

    except exceptions.TelegramAPIError:
        log.exception(f"Target tg://user?id={user_id}: failed")

    else:
        log.info(f"Target tg://user?id={user_id}: success")
        return True

    return False


async def broadcaster(bot: Bot, user_list, message, ban=False, chat_id=None, broadcast_name="broadcast"):
    assert not ban or chat_id

    log = logging.getLogger('broadcast')
    count = 0
    try:
        for user_id in user_list:
            if await send_broadcast_message(bot, user_id, message, ban=ban, chat_id=chat_id):
                count += 1
            await asyncio.sleep(0.1)

    finally:
        log.info(f"{broadcast_name}: {count} messages successful sent.")

    return count
