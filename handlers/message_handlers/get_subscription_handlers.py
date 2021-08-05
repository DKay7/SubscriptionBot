from aiogram.dispatcher import FSMContext

from dispatcher import dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from dispatcher import bot
from config.messages import MESSAGES
from config.keyboards import KEYBOARDS
from keyboards.reply_keyboards import get_keyboard
from states.get_subscsription import GetSubscriptionStates
from config.payments import PAYMENT_TOKEN, SUBSCRIPTION_PRICE, SUBSCRIPTION_IMAGE_URL, SUBSCRIPTION_IMAGE_WIDTH, \
    SUBSCRIPTION_IMAGE_HEIGHT
from utils.db.subscription import has_free_month, get_sub_days_left
from utils.telegram_channel import subscribe_user


@dp.message_handler(Text(equals=KEYBOARDS['start']['subscription']), state='*')
async def get_subscription_confirm(message: Message):

    if has_free_month(message.from_user.id):
        approve_kb_markup = get_keyboard('confirm_subscription')
        await message.answer(MESSAGES['free_month_info'], reply_markup=approve_kb_markup)
        await GetSubscriptionStates.waiting_for_confirm_free.set()

    else:
        if (days_left := get_sub_days_left(message.from_user.id)) > 0:
            left_days_notice = MESSAGES['days_left_notification'].format(days_left=days_left)
            await message.answer(left_days_notice)

        approve_kb_markup = get_keyboard('confirm_subscription')
        await message.answer(MESSAGES['subscription_terms'], reply_markup=approve_kb_markup)
        await GetSubscriptionStates.waiting_for_confirm.set()


@dp.message_handler(Text(equals=KEYBOARDS['confirm_subscription']['yes']),
                    state=GetSubscriptionStates.waiting_for_confirm_free)
async def free_month_confirmed(message: Message, state: FSMContext):
    invite_text = await subscribe_user(message.from_user.id)
    choose_action_keyboard = get_keyboard('start')
    await message.answer(invite_text, reply_markup=choose_action_keyboard)

    await state.finish()


@dp.message_handler(Text(equals=KEYBOARDS['confirm_subscription']['yes']),
                    state=GetSubscriptionStates.waiting_for_confirm)
async def subscription_confirmed(message: Message):
    await GetSubscriptionStates.waiting_for_payment.set()

    if PAYMENT_TOKEN.split(":")[1] == "TEST":
        await message.answer(MESSAGES['test_payment'], reply_markup=get_keyboard('remove'))

    await bot.send_invoice(
        message.chat.id,
        title=MESSAGES['subscription_payment_title'],
        description=MESSAGES['subscription_description'],
        provider_token=PAYMENT_TOKEN,
        currency='rub',
        photo_url=SUBSCRIPTION_IMAGE_URL,
        photo_height=SUBSCRIPTION_IMAGE_HEIGHT,
        photo_width=SUBSCRIPTION_IMAGE_WIDTH,
        photo_size=512,
        is_flexible=False,
        prices=[SUBSCRIPTION_PRICE],
        start_parameter='channel-subscription',
        payload='subscription'
    )


@dp.message_handler(Text(equals=KEYBOARDS['confirm_subscription']['no']),
                    state=[GetSubscriptionStates.waiting_for_confirm,
                           GetSubscriptionStates.waiting_for_confirm_free])
async def subscription_deny(message: Message, state: FSMContext):
    await state.finish()
    choose_action_keyboard = get_keyboard('start')
    await message.answer(MESSAGES['subscription_deny'], reply_markup=choose_action_keyboard)
