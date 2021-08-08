from aiogram.types import CallbackQuery


from dispatcher import dp
from config.messages import message_texts
from keyboards.reply_keyboards import get_keyboard
from states.accept_terms import AcceptTerms
from config.keyboards import accept_terms_callback


@dp.callback_query_handler(accept_terms_callback.filter(), state=AcceptTerms.waiting_terms_accepted)
async def choose_message_for_edit_handler(callback_query: CallbackQuery, callback_data: dict):
    user_id = int(callback_data['user_id'])

    state = dp.current_state(user=user_id, chat=user_id)

    await callback_query.answer("Вы приняли правила сервиса", show_alert=True)
    await state.set_state(AcceptTerms.terms_accepted)

    choose_action_keyboard = get_keyboard('start')
    await callback_query.message.answer(message_texts['start'], reply_markup=choose_action_keyboard)




