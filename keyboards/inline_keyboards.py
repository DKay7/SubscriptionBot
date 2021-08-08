from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.keyboards import mod_callback, message_edit_callback, accept_terms_callback


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


def get_message_edit_kb(filename, sender_id):
    callback = message_edit_callback.new(filename=filename, sender_id=sender_id)
    edit_button = InlineKeyboardButton('Редактировать это сообщение', callback_data=callback)

    message_edit_kb = InlineKeyboardMarkup()
    message_edit_kb.add(edit_button)

    return message_edit_kb


def get_accept_service_terms_kb(user_id):
    callback = accept_terms_callback.new(user_id=user_id)
    edit_button = InlineKeyboardButton('Принимаю правила сервиса', callback_data=callback)

    accept_terms_kb = InlineKeyboardMarkup()
    accept_terms_kb.add(edit_button)

    return accept_terms_kb
