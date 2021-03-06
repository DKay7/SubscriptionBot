from config.load_env import env

BOT_TOKEN = env.str('TOKEN')
BOT_ADMINS_ID = list(map(int, env.list('ADMINS_ID')))
TELEGRAM_API_ID = env.int('TELEGRAM_API_ID')
TELEGRAM_API_HASH = env.str('TELEGRAM_API_HASH')

BOT_MODERATOR_CHAT_ID = env.int('BOT_MODERATOR_CHAT_ID')
BOT_CHANNEL_ID = env.int('CHANNEL_ID')

