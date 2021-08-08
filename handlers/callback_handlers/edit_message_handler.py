from aiogram.types import CallbackQuery


from dispatcher import dp
from config.messages import message_texts
from states.admin_edit_files import EditFiles
from config.keyboards import message_edit_callback


@dp.callback_query_handler(message_edit_callback.filter(), state=EditFiles.waiting_for_choose_message)
async def choose_message_for_edit_handler(callback_query: CallbackQuery, callback_data: dict):
    await callback_query.answer()
    filename = callback_data['filename']
    sender_id = int(callback_data['sender_id'])

    state = dp.current_state(user=sender_id, chat=sender_id)
    await state.update_data(filename=filename)

    await callback_query.message.answer(message_texts['edit_message_was_chosen'])
    await state.set_state(EditFiles.waiting_for_send_message)



