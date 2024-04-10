from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils.const_functions import ikb
from tgbot.data.config import DISCORD_LINK


# Подписаться на discord
def discord_link_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Подписаться", url=DISCORD_LINK)
    )

    return keyboard.as_markup()


# Кнопки для админ панели
def admin_panel_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("⛔️ Забанить", data='admin_ban_unban_user')
    )
    keyboard.row(
        ikb("⏰ Время", data='admin_add_time')
    )

    return keyboard.as_markup()
