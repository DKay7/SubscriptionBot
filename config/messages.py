from glob import glob
from os.path import splitext, basename


def load_messages():
    messages = dict()

    for message_file_name in glob(MESSAGES_TEXTS_DIR, recursive=True):
        command_name_raw = splitext(basename(message_file_name))[0]
        command_name = command_name_raw.strip()

        with open(message_file_name, "r", encoding='utf-8') as file:
            command_message = file.read()

        messages[command_name] = command_message

    return messages


MESSAGES_TEXTS_DIR = r"data/messages/**/*?.txt"
MESSAGES_DIR = r"data/messages/"
MESSAGES_GROUP_PATTERN = r"data/messages/{group}/**/*?.txt"
MESSAGES_GROUP_PATH_PATTERN = r"data/messages/{group}/"

message_texts = load_messages()
