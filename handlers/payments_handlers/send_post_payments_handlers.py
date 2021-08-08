from aiogram.dispatcher import FSMContext
from aiogram.types import PreCheckoutQuery, Message
from aiogram.types import ContentType

from config.messages import message_texts
from dispatcher import dp, bot
from keyboards.reply_keyboards import get_keyboard
from states.send_post import SendPostStates
from utils.check_post import send_post_to_mods


@dp.pre_checkout_query_handler(lambda query: query.invoice_payload == 'send_post',
                               state=SendPostStates.waiting_for_payment)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state=SendPostStates.waiting_for_payment)
async def successful_payment(message: Message, state: FSMContext):
    await send_post_to_mods(state)

    remove_kb = get_keyboard('remove')
    await message.answer(message_texts['post_has_send_to_mods'], reply_markup=remove_kb)

    await SendPostStates.waiting_for_moderator.set()
