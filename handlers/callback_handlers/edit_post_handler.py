from aiogram.types import CallbackQuery


from dispatcher import dp
from config.messages import message_texts
from keyboards.reply_keyboards import get_keyboard
from states.send_post import SendPostStates


@dp.callback_query_handler(state="*")
async def choose_message_for_edit_handler(callback_query: CallbackQuery):
    await callback_query.answer()

    state = dp.current_state(user=callback_query.from_user.id, chat=callback_query.from_user.id)

    await callback_query.message.answer(message_texts['send_post_confirmed'], reply_markup=get_keyboard('remove'))
    await state.set_state(SendPostStates.waiting_for_edit_name)
