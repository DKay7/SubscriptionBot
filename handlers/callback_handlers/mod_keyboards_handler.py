from aiogram.types import CallbackQuery

from config.messages import message_texts
from dispatcher import dp, bot
from config.keyboards import mod_callback
from states.send_post import SendPostStates
from config.bot_config import BOT_CHANNEL_ID


@dp.callback_query_handler(mod_callback.filter(decision="accepted"))
async def mod_accepted_handler(callback_query: CallbackQuery, callback_data: dict):
    sender_id = int(callback_data['sender_id'])
    state = dp.current_state(user=sender_id, chat=sender_id)
    data = await state.get_data()

    channel_post_caption = message_texts['post_for_channel'].format(sender_name=data['sender_name'],
                                                                    post_text=data['post_text'])
    await bot.send_photo(BOT_CHANNEL_ID, caption=channel_post_caption, photo=data['photo_id'])

    post_accepted_info = message_texts['post_sent_to_channel'].format(post_text=data['post_text'])
    await bot.send_photo(sender_id, caption=post_accepted_info, photo=data['photo_id'])

    await callback_query.answer("Пост был принят и отправлен в канал.", show_alert=True)
    new_caption = callback_query.message.caption + "\n------------------\nПРИНЯТО\n------------------\n"
    await bot.edit_message_caption(callback_query.message.chat.id, callback_query.message.message_id,
                                   caption=new_caption, reply_markup="")
    await state.finish()


@dp.callback_query_handler(mod_callback.filter(decision='denied'))
async def mod_denied_handler(callback_query: CallbackQuery, callback_data):
    sender_id = int(callback_data['sender_id'])
    state = dp.current_state(user=sender_id, chat=sender_id)
    data = await state.get_data()

    edit_request_text = message_texts['edit_post_request'].format(post_text=data['post_text'])
    await bot.send_photo(sender_id, caption=edit_request_text, photo=data['photo_id'])

    await callback_query.answer("Пост был возвращен на доработку", show_alert=True)
    new_caption = callback_query.message.caption + "\n------------------\nНА ДОРАБОТКУ\n------------------\n"
    await bot.edit_message_caption(callback_query.message.chat.id, callback_query.message.message_id,
                                   caption=new_caption, reply_markup="")

    await state.set_state(SendPostStates.waiting_for_edit_post_photo)
