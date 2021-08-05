from glob import glob
from json import loads
from os.path import splitext, basename

from aiogram.utils.callback_data import CallbackData


mod_callback = CallbackData("mod_decision", "decision", "sender_id")

KEYBOARDS_TEXTS_DIR = r"data/keyboards/*?_keyboard.json"
KEYBOARDS = dict()

for keyboard_file_name in glob(KEYBOARDS_TEXTS_DIR):
    command_name_raw = splitext(basename(keyboard_file_name))[0]
    command_name = command_name_raw.replace("_keyboard", "")

    with open(keyboard_file_name, "r", encoding='utf-8') as file:
        command_keyboard = loads(file.read())

    KEYBOARDS[command_name] = command_keyboard
