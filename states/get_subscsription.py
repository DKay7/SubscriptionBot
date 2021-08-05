from aiogram.dispatcher.filters.state import State, StatesGroup


class GetSubscriptionStates(StatesGroup):
    waiting_for_confirm = State()
    waiting_for_confirm_free = State()
    waiting_for_payment = State()
