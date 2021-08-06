from config.payments import PAYMENT_TOKEN, SEND_POST_PRICE, \
    SEND_POST_IMAGE_WIDTH, SEND_POST_IMAGE_HEIGHT, SEND_POST_IMAGE_URL
from dispatcher import dp, bot
from aiogram.types import Message, ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config.messages import MESSAGES
from config.keyboards import KEYBOARDS
from states.send_post import SendPostStates
from keyboards.reply_keyboards import get_keyboard
from utils.check_post import send_post_to_mods


@dp.message_handler(Text(equals=KEYBOARDS['start']['post']), state=None)
async def confirm_sending_post(message: Message):
    approve_keyboard = get_keyboard('confirm_post')
    await message.answer(MESSAGES['send_post_terms'], reply_markup=approve_keyboard)
    await SendPostStates.waiting_for_confirm.set()


@dp.message_handler(Text(equals=KEYBOARDS['confirm_post']['yes']), state=SendPostStates.waiting_for_confirm)
async def sending_post_confirmed(message: Message):
    await message.answer(MESSAGES['send_post_confirmed'], reply_markup=get_keyboard('remove'))
    await SendPostStates.waiting_for_post_photo.set()


@dp.message_handler(state=SendPostStates.waiting_for_post_photo, content_types=ContentTypes.PHOTO)
async def get_post_photo_form_user(message: Message, state: FSMContext):
    if message.media_group_id:
        return

    async with state.proxy() as data:
        data['photo_id'] = str(message.photo[-1].file_id)
        data['sender_id'] = str(message.from_user.id)
        data['sender_name'] = str(message.from_user.full_name)

    await message.answer(MESSAGES['send_post_text'])

    await SendPostStates.waiting_for_post_text.set()


@dp.message_handler(state=SendPostStates.waiting_for_post_text, content_types=ContentTypes.TEXT)
async def get_post_text_form_user(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['post_text'] = message.text

    approve_keyboard = get_keyboard('approve_post')
    await message.answer(MESSAGES['send_post_approve'], reply_markup=approve_keyboard)
    await SendPostStates.waiting_for_approve.set()


@dp.message_handler(Text(equals=KEYBOARDS['approve_post']['yes']), state=SendPostStates.waiting_for_approve)
async def get_payment(message: Message):
    await SendPostStates.waiting_for_payment.set()

    if PAYMENT_TOKEN.split(":")[1] == "TEST":
        await message.answer(MESSAGES['test_payment'], reply_markup=get_keyboard('remove'))

    await bot.send_invoice(
        message.chat.id,
        title=MESSAGES['send_post_payment_title'],
        description=MESSAGES['send_post_description'],
        provider_token=PAYMENT_TOKEN,
        currency='rub',
        photo_url=SEND_POST_IMAGE_URL,
        photo_height=SEND_POST_IMAGE_HEIGHT,
        photo_width=SEND_POST_IMAGE_WIDTH,
        photo_size=512,
        is_flexible=False,
        prices=[SEND_POST_PRICE],
        start_parameter='channel-send-post',
        payload='send_post'
    )


@dp.message_handler(Text(equals=KEYBOARDS['approve_post']['edit']), state=SendPostStates.waiting_for_approve)
async def get_post_photo_form_user(message: Message):
    await message.answer(MESSAGES['send_post_confirmed'], reply_markup=get_keyboard('remove'))
    await SendPostStates.waiting_for_post_photo.set()


@dp.message_handler(Text(equals=KEYBOARDS['approve_post']['edit']), state=SendPostStates.waiting_for_edit_post_approve)
async def edited_post_re_edited(message: Message):
    await message.answer(MESSAGES['send_post_confirmed'], reply_markup=get_keyboard('remove'))
    await SendPostStates.waiting_for_edit_post_photo.set()


@dp.message_handler(state=SendPostStates.waiting_for_edit_post_photo, content_types=ContentTypes.PHOTO)
async def get_edited_post_photo_form_user(message: Message, state: FSMContext):
    if message.media_group_id:
        return

    async with state.proxy() as data:
        data['post_text'] = str(message.caption)
        data['photo_id'] = str(message.photo[-1].file_id)
        data['sender_id'] = str(message.from_user.id)
        data['sender_name'] = str(message.from_user.full_name)

    await message.answer(MESSAGES['send_post_text'])
    await SendPostStates.waiting_for_edit_post_text.set()


@dp.message_handler(state=SendPostStates.waiting_for_edit_post_text, content_types=ContentTypes.TEXT)
async def get_edited_post_text_form_user(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['post_text'] = str(message.caption)

    approve_keyboard = get_keyboard('approve_post')
    await message.answer(MESSAGES['send_post_approve'], reply_markup=approve_keyboard)

    await SendPostStates.waiting_for_edit_post_approve.set()


@dp.message_handler(Text(equals=KEYBOARDS['approve_post']['yes']), state=SendPostStates.waiting_for_edit_post_approve)
async def edited_post_approved(message: Message, state: FSMContext):
    await send_post_to_mods(state)
    remove_kb = get_keyboard('remove')
    await message.answer(MESSAGES['post_has_send_to_mods'], reply_markup=remove_kb)
    await SendPostStates.waiting_for_moderator.set()


@dp.message_handler(Text(equals=KEYBOARDS['approve_post']['no']), state=SendPostStates.waiting_for_edit_post_approve)
@dp.message_handler(Text(equals=KEYBOARDS['approve_post']['no']), state=SendPostStates.waiting_for_approve)
@dp.message_handler(Text(equals=KEYBOARDS['confirm_post']['no']), state=SendPostStates.waiting_for_confirm)
async def sending_post_denied(message: Message, state: FSMContext):
    await state.finish()
    start_keyboard = get_keyboard('start')
    await message.answer(MESSAGES['send_post_deny'], reply_markup=start_keyboard)
