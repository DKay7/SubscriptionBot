import os
import sys
from glob import glob
from os import listdir
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from dispatcher import dp
from keyboards.inline_keyboards import get_message_edit_kb
from keyboards.reply_keyboards import get_keyboard
from states.admin_edit_files import EditFiles
from config.messages import MESSAGES_DIR, message_texts, MESSAGES_GROUP_PATTERN, MESSAGES_GROUP_PATH_PATTERN


@dp.message_handler(commands=['edit_messages'], is_admin=True, state="*")
async def choose_messages_group(message: Message):
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for messages_group_name in listdir(MESSAGES_DIR):
        button = KeyboardButton(messages_group_name)
        reply_keyboard.add(button)

    await message.answer(message_texts['edit_choose_group'], reply_markup=reply_keyboard)

    await EditFiles.waiting_for_choose_group.set()


@dp.message_handler(is_admin=True, state=EditFiles.waiting_for_choose_group)
async def choose_messages_group(message: Message, state: FSMContext):
    if message.text not in listdir(MESSAGES_DIR):
        await message.answer("Пожалуйста, используйте специальные кнопки")
        return

    group_glob_path = MESSAGES_GROUP_PATTERN.format(group=message.text)
    group_path = MESSAGES_GROUP_PATH_PATTERN.format(group=message.text)
    await state.update_data(group_path=group_path)

    for messages_file_name in glob(group_glob_path, recursive=True):
        with open(messages_file_name, "r", encoding="utf-8") as message_text_file:
            message_text = message_text_file.read()

        only_filename = os.path.split(messages_file_name)[-1]
        edit_kb = get_message_edit_kb(filename=only_filename, sender_id=message.from_user.id)
        text = message_texts['edit_message_pattern'].format(filename=messages_file_name,
                                                            message_text=message_text)

        await message.answer(text, reply_markup=edit_kb, parse_mode="")

    await message.answer(message_texts['edit_instruction'], parse_mode="",
                         reply_markup=get_keyboard("remove"))

    await EditFiles.waiting_for_choose_message.set()


@dp.message_handler(is_admin=True, state=EditFiles.waiting_for_send_message)
async def get_message_from_user(message: Message, state: FSMContext):
    data = await state.get_data()

    group_path = data['group_path']
    filename = data['filename']

    full_path = os.path.join(group_path, filename)

    with open(full_path, "w", encoding="utf-8") as message_text_file:
        message_text_file.write(message.text.strip())

    await message.answer(message_texts["edit_complete"])
    await state.finish()

    # TODO uncomment if run without self-reloaded daemon
    # os.system("python3 main.py")
    sys.exit()
