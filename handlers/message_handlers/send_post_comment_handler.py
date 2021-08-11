from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from dispatcher import dp, bot
from states.add_comment_states import AddComment
from config.messages import message_texts


@dp.message_handler(state=AddComment.waiting_for_comment, content_types=ContentType.TEXT)
async def get_comment_from_mod_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    post_author_id = data['post_author_id']
    comment_text = message_texts['comment_pattern'].format(comment_text=message.text)

    await bot.send_message(chat_id=post_author_id, text=comment_text)
    await message.answer(message_texts['add_comment_success'])

    await state.finish()
