from aiogram.dispatcher.filters.state import State, StatesGroup


class SendPostStates(StatesGroup):
    waiting_for_confirm = State()
    waiting_for_approve = State()
    waiting_for_post_photo = State()
    waiting_for_post_text = State()

    waiting_for_payment = State()
    waiting_for_moderator = State()

    waiting_for_edit_post_photo = State()
    waiting_for_edit_post_text = State()
    waiting_for_edit_post_approve = State()
