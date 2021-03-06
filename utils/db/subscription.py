from datetime import datetime, timedelta

from utils.db.connection import COLLS


def upsert_user_subscription(telegram_user_id: int):
    sub = COLLS['subscriptions']

    old_date = get_sub_expired_date(telegram_user_id)

    new_expired_date = old_date if old_date > datetime.utcnow() else datetime.utcnow()

    new_expired_date += timedelta(days=7)

    sub.update_one(
        {"telegram_user_id": telegram_user_id},
        {"$set": {"expired_date": new_expired_date,
                  "subscribed": True}},

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

    users = sub.find({"expired_date": {"$lte": next_day, "$gte": today},
                      "subscribed": True},
                     {'telegram_user_id': True, '_id': False})
    users_list = list(map(lambda user: user['telegram_user_id'], users))

    return users_list


def get_users_with_ended_sub():
    sub = COLLS['subscriptions']
    current_day = datetime.utcnow()

    users = sub.find({"expired_date": {"$lte": current_day},
                      "subscribed": True},
                     {'telegram_user_id': True, '_id': False})
    users_list = list(map(lambda user: user['telegram_user_id'], users))

    return users_list


def get_users_with_active_sub():
    sub = COLLS['subscriptions']

    today = datetime.utcnow()

    users = sub.find({"expired_date": {"$gte": today},
                      "subscribed": True},
                     {'telegram_user_id': True, '_id': False})
    users_list = list(map(lambda user: user['telegram_user_id'], users))

    return users_list


def unsubscribe_user_from_db(user_id):
    sub = COLLS['subscriptions']

    sub.update_one(
        {"telegram_user_id": user_id},
        {"$set": {"subscribed": False}}
    )
