import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from tgbot.data.config import BOT_TOKEN, ADMIN_ID, PY_VERSION
from tgbot.routers import register_all_routers
from tgbot.utils.misc.bot_commands import set_commands
from tgbot.middlewares import register_all_middlewares
from tgbot.database.db_helper import create_dbx
from tgbot.database.db_users import Userx


async def on_startup(bot: Bot):
    await bot.send_message(ADMIN_ID, f'✔️ ➖ BerryBot ➖ ✔️\n'
                                     f'➖➖➖➖➖➖➖➖'
                                     f'\n\n'
                                     f'<b>Версия 🐍: {PY_VERSION}\n'
                                     f'Кол-во 👥: {Userx.get_all_count()}</b>'
                                     f'\n\n'
                                     f'➖➖➖➖➖➖➖➖\n')


def on_shutdown():
    print('Бот выключен')


async def mainS():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mWode='HTML'))  # Образ Бота
    dp = Dispatcher()  # Образ Диспетчера

    register_all_routers(dp)  # Подключение всех роутеров
    register_all_middlewares(dp)  # Подключение всех middlewares

    try:
        try:
            await on_startup(bot)  # Рассылка админам при запуске
        except:
            print('АДМИН НЕ ВОШЁЛ В БОТА')
        await set_commands(bot)  # Установка команд для users/admin

        await bot.delete_webhook()
        await bot.get_updates(offset=-1)

        await dp.start_polling(bot)
    except:
        pass


if __name__ == '__main__':
    create_dbx()  # Генерация БД + Таблиц

    try:
        asyncio.run(main())
    except:
        pass
