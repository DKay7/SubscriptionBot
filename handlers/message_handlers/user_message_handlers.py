from aiogram.dispatcher import FSMContext
from dispatcher import dp
from aiogram.types import Message

from config.messages import message_texts
from states.accept_terms import AcceptTerms
from keyboards.inline_keyboards import get_accept_service_terms_kb


@dp.message_handler(commands=['start', 'restart'], state='*')
async def accept_terms_command(message: Message, state: FSMContext):
    await state.finish()
    accept_service_terms_kb = get_accept_service_terms_kb(message.from_user.id)
    await message.answer(message_texts['service_terms'], reply_markup=accept_service_terms_kb)
    await AcceptTerms.waiting_terms_accepted.set()


@dp.message_handler(commands='help', state='*')
async def help_command(message: Message):
    await message.answer(message_texts['help'])
