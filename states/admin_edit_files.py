from aiogram.dispatcher.filters.state import State, StatesGroup


class EditFiles(StatesGroup):
    waiting_for_choose_group = State()
    waiting_for_choose_message = State()
    waiting_for_send_message = State()
