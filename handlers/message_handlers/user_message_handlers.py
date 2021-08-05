from aiogram.dispatcher import FSMContext
from dispatcher import dp
from aiogram.types import Message

from config.messages import MESSAGES
from keyboards.reply_keyboards import get_keyboard


@dp.message_handler(commands='start', state='*')
async def start_command(message: Message, state: FSMContext):
    await state.finish()
    choose_action_keyboard = get_keyboard('start')
    await message.answer(MESSAGES['start'], reply_markup=choose_action_keyboard)


@dp.message_handler(commands='help', state='*')
async def help_command(message: Message):
    await message.answer(MESSAGES['help'])
