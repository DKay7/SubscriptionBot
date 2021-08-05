import calendar
from datetime import datetime, timedelta

from utils.db.connection import COLLS


def upsert_user_subscription(telegram_user_id: int):
    sub = COLLS['subscriptions']

    old_date = get_sub_expired_date(telegram_user_id)

    new_expired_date = old_date if old_date > datetime.utcnow() else datetime.utcnow()

    days_in_month = calendar.monthrange(new_expired_date.year, new_expired_date.month)[1]
    new_expired_date += timedelta(days=days_in_month)

    sub.update_one(
        {"telegram_user_id": telegram_user_id},
        {"$set": {"expired_date": new_expired_date}},
        upsert=True)

    return new_expired_date


def get_sub_expired_date(telegram_user_id: int):
    sub = COLLS['subscriptions']

    result = sub.find_one({"telegram_user_id": telegram_user_id})
    if result:
        return result['expired_date']

    return datetime.utcnow()


def get_sub_days_left(telegram_user_id: int):
    expired_date = get_sub_expired_date(telegram_user_id)
    days_left = (expired_date - datetime.utcnow()).days

    return days_left


def has_free_month(telegram_user_id: int):
    sub = COLLS['subscriptions']

    result = sub.find_one({"telegram_user_id": telegram_user_id})
    if result:
        return False

    return True


def get_users_with_expired_sub():
    sub = COLLS['subscriptions']
    today = datetime.utcnow()
    next_day = datetime.utcnow() + timedelta(days=1)

    users = sub.find({"expired_date": {"$lte": next_day, "$gt": today}},
                     {'telegram_user_id': True, '_id': False})
    users_list = list(map(lambda user: user['telegram_user_id'], users))

    return users_list


def get_users_without_sub():
    sub = COLLS['subscriptions']
    current_day = datetime.utcnow()

    users = sub.find({"expired_date": {"$lte": current_day}},
                     {'telegram_user_id': True, '_id': False})
    users_list = list(map(lambda user: user['telegram_user_id'], users))

    return users_list
