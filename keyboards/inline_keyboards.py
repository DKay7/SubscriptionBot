from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.keyboards import mod_callback


def get_mod_decision_kb(sender_id):
    accept_button = InlineKeyboardButton('Принять пост',
                                         callback_data=mod_callback.new(decision="accepted",
                                                                        sender_id=sender_id))

    deny_button = InlineKeyboardButton('Отклонить пост',
                                       callback_data=mod_callback.new(decision="denied",
                                                                      sender_id=sender_id))

    mod_decision_kb = InlineKeyboardMarkup()
    mod_decision_kb.add(accept_button)
    mod_decision_kb.add(deny_button)

    return mod_decision_kb
