from config.load_env import env

BOT_TOKEN = env.str('TOKEN')
BOT_OWNER_ID = env.list('OWNER_ID')
BOT_MODERATOR_CHAT_ID = env.str('BOT_MODERATOR_CHAT_ID')
BOT_CHANNEL_ID = env.int('CHANNEL_ID')

