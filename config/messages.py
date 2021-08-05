from glob import glob
from os.path import splitext, basename


MESSAGES_TEXTS_DIR = r"data/messages/**/*?_message_text.txt"
MESSAGES = dict()

for message_file_name in glob(MESSAGES_TEXTS_DIR, recursive=True):
    command_name_raw = splitext(basename(message_file_name))[0]
    command_name = command_name_raw.replace("_message_text", "")

    with open(message_file_name, "r", encoding='utf-8') as file:
        command_message = file.read()

    MESSAGES[command_name] = command_message
