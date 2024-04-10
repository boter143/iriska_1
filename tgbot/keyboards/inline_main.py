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
        ikb("⛔️ Бан / ✅ Разбан", data='admin_ban_unban_user'),
        ikb("⏰ Время", data='admin_add_time')
    )
    keyboard.row(
        ikb("🛠 Модерация видео", data='admin_moderation_video')
    )

    return keyboard.as_markup()


# Кнопки под видео-модерацию
def admin_moderation_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Принять", data='moderation_access'),
        ikb("⛔️ Забанить", data='moderation_ban')
    )

    return keyboard.as_markup()
