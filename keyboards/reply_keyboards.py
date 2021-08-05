from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from config.keyboards import KEYBOARDS


def get_keyboard(kb_name):
    if kb_name == "remove":
        return ReplyKeyboardRemove()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard_data = KEYBOARDS[kb_name]
    for key, value in keyboard_data.items():
        button = KeyboardButton(value)
        keyboard.add(button)

    return keyboard
