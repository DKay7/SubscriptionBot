from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.keyboards import mod_callback, message_edit_callback, accept_terms_callback, post_comment_callback


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


def get_add_comment_to_post_kb(sender_id):
    callback = post_comment_callback.new(sender_id=sender_id)
    add_comment_button = InlineKeyboardButton('Добавить комментарий к посту', callback_data=callback)

    add_comment_kb = InlineKeyboardMarkup()
    add_comment_kb.add(add_comment_button)

    return add_comment_kb


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


def get_user_ready_to_edit_post_kb():
    ready_to_edit_button = InlineKeyboardButton('Редактировать пост', callback_data="user_ready")

    ready_to_edit_kb = InlineKeyboardMarkup()
    ready_to_edit_kb.add(ready_to_edit_button)

    return ready_to_edit_kb
