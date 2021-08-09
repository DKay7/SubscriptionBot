from config.payments import PAYMENT_TOKEN, SEND_POST_PRICE, \
    SEND_POST_IMAGE_WIDTH, SEND_POST_IMAGE_HEIGHT, SEND_POST_IMAGE_URL
from dispatcher import dp, bot
from aiogram.types import Message, ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config.messages import message_texts
from config.keyboards import keyboards_texts
from states.accept_terms import AcceptTerms
from states.send_post import SendPostStates
from keyboards.reply_keyboards import get_keyboard
from utils.check_post import send_post_to_mods


@dp.message_handler(Text(equals=keyboards_texts['start']['post']), state=AcceptTerms.terms_accepted)
async def confirm_sending_post(message: Message):
    approve_keyboard = get_keyboard('confirm_post')
    await message.answer(message_texts['send_post_terms'], reply_markup=approve_keyboard)
    await SendPostStates.waiting_for_confirm.set()


@dp.message_handler(Text(equals=keyboards_texts['confirm_post']['yes']), state=SendPostStates.waiting_for_confirm)
async def sending_post_confirmed(message: Message):
    await message.answer(message_texts['send_post_confirmed'], reply_markup=get_keyboard('remove'))
    await SendPostStates.waiting_for_send_name.set()


@dp.message_handler(state=SendPostStates.waiting_for_send_name, content_types=ContentTypes.TEXT)
async def get_name_form_user(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['sender_id'] = str(message.from_user.id)
        data['sender_nickname'] = str(message.from_user.mention)
        data['sender_real_name'] = message.text

    await message.answer(message_texts['got_real_name'])
    await SendPostStates.waiting_for_send_location.set()


@dp.message_handler(state=SendPostStates.waiting_for_edit_name, content_types=ContentTypes.TEXT)
async def get_edited_name_form_user(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['sender_id'] = str(message.from_user.id)
        data['sender_nickname'] = str(message.from_user.mention)
        data['sender_real_name'] = message.text

    await message.answer(message_texts['got_real_name'])
    await SendPostStates.waiting_for_edit_location.set()


@dp.message_handler(state=SendPostStates.waiting_for_send_location, content_types=ContentTypes.TEXT)
async def get_location_form_user(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['sender_location'] = message.text

    await message.answer(message_texts['got_location'])
    await SendPostStates.waiting_for_post_photo.set()


@dp.message_handler(state=SendPostStates.waiting_for_edit_location, content_types=ContentTypes.TEXT)
async def get_edited_location_form_user(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['sender_location'] = message.text

    await message.answer(message_texts['got_location'])
    await SendPostStates.waiting_for_edit_post_photo.set()


@dp.message_handler(state=SendPostStates.waiting_for_post_photo, content_types=ContentTypes.PHOTO)
async def get_post_photo_form_user(message: Message, state: FSMContext):
    if message.media_group_id:
        return

    async with state.proxy() as data:
        data['photo_id'] = str(message.photo[-1].file_id)

    await message.answer(message_texts['got_photo'])

    await SendPostStates.waiting_for_post_text.set()


@dp.message_handler(state=SendPostStates.waiting_for_edit_post_photo, content_types=ContentTypes.PHOTO)
async def get_edited_post_photo_form_user(message: Message, state: FSMContext):
    if message.media_group_id:
        return

    async with state.proxy() as data:
        data['photo_id'] = str(message.photo[-1].file_id)

    await message.answer(message_texts['got_photo'])
    await SendPostStates.waiting_for_edit_post_text.set()


@dp.message_handler(state=SendPostStates.waiting_for_post_text, content_types=ContentTypes.TEXT)
async def get_post_text_form_user(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['post_text'] = message.text

    await SendPostStates.waiting_for_preferences.set()
    await message.answer(message_texts['got_text'])


@dp.message_handler(state=SendPostStates.waiting_for_edit_post_text, content_types=ContentTypes.TEXT)
async def get_edited_post_text_form_user(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['post_text'] = message.text

    await SendPostStates.waiting_for_edit_preferences.set()
    await message.answer(message_texts['got_text'])


@dp.message_handler(state=SendPostStates.waiting_for_preferences, content_types=ContentTypes.TEXT)
async def get_user_preferences(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['preferences'] = message.text

    approve_keyboard = get_keyboard('approve_post')
    await message.answer(message_texts['send_post_approve'], reply_markup=approve_keyboard)
    await SendPostStates.waiting_for_approve.set()


@dp.message_handler(state=SendPostStates.waiting_for_edit_preferences, content_types=ContentTypes.TEXT)
async def get_edited_user_preferences(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['preferences'] = message.text

    approve_keyboard = get_keyboard('approve_post')
    await message.answer(message_texts['send_post_approve'], reply_markup=approve_keyboard)

    await SendPostStates.waiting_for_edit_post_approve.set()


@dp.message_handler(Text(equals=keyboards_texts['approve_post']['yes']), state=SendPostStates.waiting_for_approve)
async def get_payment(message: Message):
    await SendPostStates.waiting_for_payment.set()

    if PAYMENT_TOKEN.split(":")[1] == "TEST":
        await message.answer(message_texts['test_payment'], reply_markup=get_keyboard('remove'))

    await bot.send_invoice(
        message.chat.id,
        title=message_texts['send_post_payment_title'],
        description=message_texts['send_post_description'],
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


@dp.message_handler(Text(equals=keyboards_texts['approve_post']['yes']),
                    state=SendPostStates.waiting_for_edit_post_approve)
async def edited_post_approved(message: Message, state: FSMContext):
    await send_post_to_mods(state)
    remove_kb = get_keyboard('remove')
    await message.answer(message_texts['post_has_send_to_mods'], reply_markup=remove_kb)
    await SendPostStates.waiting_for_moderator.set()


@dp.message_handler(Text(equals=keyboards_texts['approve_post']['edit']), state=SendPostStates.waiting_for_approve)
async def get_post_photo_form_user(message: Message):
    await message.answer(message_texts['send_post_confirmed'], reply_markup=get_keyboard('remove'))
    await SendPostStates.waiting_for_send_name.set()


@dp.message_handler(Text(equals=keyboards_texts['approve_post']['edit']),
                    state=SendPostStates.waiting_for_edit_post_approve)
async def edited_post_re_edited(message: Message):
    await message.answer(message_texts['send_post_confirmed'], reply_markup=get_keyboard('remove'))
    await SendPostStates.waiting_for_edit_name.set()


@dp.message_handler(Text(equals=keyboards_texts['approve_post']['no']),
                    state=SendPostStates.waiting_for_edit_post_approve)
@dp.message_handler(Text(equals=keyboards_texts['approve_post']['no']), state=SendPostStates.waiting_for_approve)
@dp.message_handler(Text(equals=keyboards_texts['confirm_post']['no']), state=SendPostStates.waiting_for_confirm)
async def sending_post_denied(message: Message, state: FSMContext):
    await state.finish()
    await AcceptTerms.terms_accepted.set()
    start_keyboard = get_keyboard('start')
    await message.answer(message_texts['send_post_deny'], reply_markup=start_keyboard)
