from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.broadcasting import broadcaster
from config.messages import MESSAGES
from utils.db.subscription import get_users_without_sub, get_users_with_expired_sub
from config.bot_config import BOT_CHANNEL_ID


async def send_expired_notification(bot):
    user_list = get_users_with_expired_sub()

    await broadcaster(bot, user_list, MESSAGES['subscription_expired_in_day'],
                      broadcast_name="Notify members about expiring subscription")


async def kick_members_without_subscription(bot):
    user_list = get_users_without_sub()

    await broadcaster(bot, user_list, MESSAGES['subscription_kick'], ban=True, chat_id=BOT_CHANNEL_ID,
                      broadcast_name="Ban members messages")


def setup_scheduler(bot):
    sched = AsyncIOScheduler()

    # TODO remove test
    sched.add_job(send_expired_notification, CronTrigger(hour=18), args=[bot])
    sched.add_job(kick_members_without_subscription, CronTrigger(hour=18), args=[bot])

    return sched
