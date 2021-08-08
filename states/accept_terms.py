from aiogram.dispatcher.filters.state import State, StatesGroup


class AcceptTerms(StatesGroup):
    waiting_terms_accepted = State()
    terms_accepted = State()
