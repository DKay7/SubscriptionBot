import logging

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.channel.broadcasting import broadcaster
from config.messages import MESSAGES
from utils.channel.channel_members_getter import get_users_without_any_sub
from utils.db.subscription import get_users_with_ended_sub, get_users_with_expired_sub
from config.bot_config import BOT_CHANNEL_ID


async def send_expired_notification(bot):
    user_list = get_users_with_expired_sub()
    log = logging.getLogger("broadcast [Expired]")
    log.debug(user_list)

    await broadcaster(bot, user_list, message=MESSAGES['subscription_expired_in_day'],
                      broadcast_name="Notify members about expiring sub. broadcast")


async def kick_members_with_ended_sub(bot):
    user_list = get_users_with_ended_sub()
    log = logging.getLogger("broadcast [with ended sub]")
    log.debug(user_list)

    await broadcaster(bot, user_list, message=MESSAGES['subscription_kick'],
                      ban=True, chat_id=BOT_CHANNEL_ID,
                      broadcast_name="Ban members with ended sub. broadcast")


async def kick_members_without_sub(bot):
    user_list = await get_users_without_any_sub(bot)
    log = logging.getLogger("broadcast [without sub]")
    log.debug(user_list)

    await broadcaster(bot, user_list, send_message=False,
                      ban=True, chat_id=BOT_CHANNEL_ID,
                      broadcast_name="Ban members without sub. broadcast")


def setup_scheduler(bot):
    sched = AsyncIOScheduler()

    # Todo remove
    sched.add_job(send_expired_notification, CronTrigger(hour="*/2"), args=[bot])
    sched.add_job(kick_members_with_ended_sub, CronTrigger(hour="*/2"), args=[bot])
    sched.add_job(kick_members_without_sub, CronTrigger(hour="*/2"), args=[bot])

    return sched
