from aiogram.types import LabeledPrice

from config.load_env import env

PAYMENT_TOKEN = env.str("PAYMENT_TOKEN")

SUBSCRIPTION_PRICE = LabeledPrice(label='Неделя подписки на канал', amount=9900)
SUBSCRIPTION_IMAGE_URL = "https://www.uprankly.com/blog/wp-content/uploads/2018/11/Subscriber-768x432.jpg"
SUBSCRIPTION_IMAGE_HEIGHT = 432
SUBSCRIPTION_IMAGE_WIDTH = 768
SUBSCRIPTION_PHOTO_SIZE = 512


SEND_POST_PRICE = LabeledPrice(label='Опубликовать пост в закрытом канале', amount=14900)
SEND_POST_IMAGE_URL = "https://static10.tgstat.ru/channels/_0/d3/d35bf3a69b2230fc7a5b2ded1f668419.jpg"
SEND_POST_IMAGE_HEIGHT = 640
SEND_POST_IMAGE_WIDTH = 640
SEND_POST_PHOTO_SIZE = 512
