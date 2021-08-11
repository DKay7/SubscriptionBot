from aiogram.dispatcher import FSMContext

from dispatcher import dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from dispatcher import bot
from config.messages import message_texts
from config.keyboards import keyboards_texts
from keyboards.reply_keyboards import get_keyboard
from states.accept_terms import AcceptTerms
from states.get_subscsription import GetSubscriptionStates
from config.payments import PAYMENT_TOKEN, SUBSCRIPTION_IMAGE_URL, SUBSCRIPTION_IMAGE_HEIGHT, SUBSCRIPTION_IMAGE_WIDTH,\
    SUBSCRIPTION_PHOTO_SIZE, SUBSCRIPTION_PRICE
from utils.db.subscription import has_free_month, get_sub_days_left
from utils.channel.telegram_channel import subscribe_user


@dp.message_handler(Text(equals=keyboards_texts['start']['subscription']), state=AcceptTerms.terms_accepted)
async def get_subscription_confirm(message: Message):

    if has_free_month(message.from_user.id):
        approve_kb_markup = get_keyboard('confirm_subscription')
        await message.answer(message_texts['free_period_info'], reply_markup=approve_kb_markup)
        await GetSubscriptionStates.waiting_for_confirm_free.set()

    else:
        if (days_left := get_sub_days_left(message.from_user.id)) > 0:
            left_days_notice = message_texts['days_left_notification'].format(days_left=days_left)
            await message.answer(left_days_notice)

        approve_kb_markup = get_keyboard('confirm_subscription')
        await message.answer(message_texts['subscription_terms'], reply_markup=approve_kb_markup)
        await GetSubscriptionStates.waiting_for_confirm.set()


@dp.message_handler(Text(equals=keyboards_texts['confirm_subscription']['yes']),
                    state=GetSubscriptionStates.waiting_for_confirm_free)
async def free_month_confirmed(message: Message, state: FSMContext):
    invite_text = await subscribe_user(message.from_user.id)
    choose_action_keyboard = get_keyboard('start')
    await message.answer(invite_text, reply_markup=choose_action_keyboard)

    await state.finish()
    await AcceptTerms.terms_accepted.set()


@dp.message_handler(Text(equals=keyboards_texts['confirm_subscription']['yes']),
                    state=GetSubscriptionStates.waiting_for_confirm)
async def subscription_confirmed(message: Message):
    await GetSubscriptionStates.waiting_for_payment.set()

    if PAYMENT_TOKEN.split(":")[1] == "TEST":
        await message.answer(message_texts['test_payment'], reply_markup=get_keyboard('remove'))

    await bot.send_invoice(
        message.chat.id,
        title=message_texts['subscription_payment_title'],
        description=message_texts['subscription_description'],
        provider_token=PAYMENT_TOKEN,
        currency='rub',
        photo_url=SUBSCRIPTION_IMAGE_URL,
        photo_height=SUBSCRIPTION_IMAGE_HEIGHT,
        photo_width=SUBSCRIPTION_IMAGE_WIDTH,
        photo_size=SUBSCRIPTION_PHOTO_SIZE,
        is_flexible=False,
        prices=[SUBSCRIPTION_PRICE],
        start_parameter='channel-subscription',
        payload='subscription'
    )


@dp.message_handler(Text(equals=keyboards_texts['confirm_subscription']['no']),
                    state=[GetSubscriptionStates.waiting_for_confirm,
                           GetSubscriptionStates.waiting_for_confirm_free])
async def subscription_deny(message: Message, state: FSMContext):
    await state.finish()
    await AcceptTerms.terms_accepted.set()
    choose_action_keyboard = get_keyboard('start')
    await message.answer(message_texts['subscription_deny'], reply_markup=choose_action_keyboard)
