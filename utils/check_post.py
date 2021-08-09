from aiogram.dispatcher import FSMContext

from config.messages import message_texts
from dispatcher import bot
from config.bot_config import BOT_MODERATOR_CHAT_ID
from keyboards.inline_keyboards import get_mod_decision_kb


async def send_post_to_mods(state: FSMContext):

    data = await state.get_data()
    inline_keyboard = get_mod_decision_kb(data['sender_id'])

    post_text = message_texts['for_moderator'].format(sender_id=data['sender_id'],
                                                      sender_real_name=data['sender_real_name'],
                                                      sender_location=data['sender_location'],
                                                      post_text=data['post_text'],
                                                      preferences=data['preferences'],
                                                      sender_nickname=data['sender_nickname'])

    await bot.send_photo(chat_id=BOT_MODERATOR_CHAT_ID, caption=post_text, photo=data['photo_id'],
                         reply_markup=inline_keyboard)
