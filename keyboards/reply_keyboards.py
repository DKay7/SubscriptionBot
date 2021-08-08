from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from config.keyboards import keyboards_texts


def get_keyboard(kb_name):
    if kb_name == "remove":
        return ReplyKeyboardRemove()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard_data = keyboards_texts[kb_name]
    for key, value in keyboard_data.items():
        button = KeyboardButton(value)
        keyboard.add(button)

    return keyboard
