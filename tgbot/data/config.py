from environs import Env
from platform import python_version

env = Env()
env.read_env()

# .env
BOT_TOKEN = env.str('BOT_TOKEN')
ADMIN_ID = env.int('ADMIN_ID')
DISCORD_LINK = env.str('DISCORD_LINK')
CHAT_ID = env.int('CHAT_ID')

# consts
PY_VERSION = python_version()
BOT_TIMEZONE = "Europe/Moscow"  # Временная зона бота

# PATHS
PATH_DATABASE = "tgbot/data/database.db"
