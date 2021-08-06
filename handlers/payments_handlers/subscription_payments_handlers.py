from aiogram.dispatcher import FSMContext
from aiogram.types import PreCheckoutQuery, Message
from aiogram.types import ContentType

from dispatcher import dp, bot
from keyboards.reply_keyboards import get_keyboard
from states.get_subscsription import GetSubscriptionStates
from utils.channel.telegram_channel import subscribe_user


@dp.pre_checkout_query_handler(lambda query: query.invoice_payload == 'subscription',
                               state=GetSubscriptionStates.waiting_for_payment)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state=GetSubscriptionStates.waiting_for_payment)
async def successful_payment(message: Message, state: FSMContext):
    invite_text = await subscribe_user(message.from_user.id)
    choose_action_keyboard = get_keyboard('start')
    await message.answer(invite_text, reply_markup=choose_action_keyboard)

    await state.finish()
