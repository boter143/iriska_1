from aiogram import Dispatcher, F

from tgbot.routers.user import user_menu, user_video, user_pay
from tgbot.routers.admin import admin_menu, admin_time, admin_ban, admin_moderation
from tgbot.utils.misc.bot_filters import IsAdmin


def register_all_routers(dp: Dispatcher):
    # Подключение фильтров
    dp.message.filter(F.chat.type == "private")  # Работа бота только в личке - сообщения
    dp.callback_query.filter(F.message.chat.type == "private")  # Работа бота только в личке - колбэки

    admin_menu.router.message.filter(IsAdmin())
    admin_time.router.message.filter(IsAdmin())
    admin_time.router.callback_query.filter(IsAdmin())
    admin_ban.router.message.filter(IsAdmin())
    admin_ban.router.callback_query.filter(IsAdmin())
    admin_moderation.router.message.filter(IsAdmin())
    admin_moderation.router.callback_query.filter(IsAdmin())

    # Подключение роутеров
    dp.include_router(user_video.router)  # user
    dp.include_router(user_pay.router)  # user
    dp.include_router(admin_menu.router)  # admin
    dp.include_router(user_menu.router)  # user
    dp.include_router(admin_time.router)  # admin
    dp.include_router(admin_ban.router)  # admin
    dp.include_router(admin_moderation.router)  # admin
