from aiogram.dispatcher.filters.state import State, StatesGroup


class AddComment(StatesGroup):
    waiting_for_comment = State()
