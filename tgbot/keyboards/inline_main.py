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


# Оплата
def balance_add_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("Пополнить баланс", data='balance_add')
    )

    return keyboard.as_markup()


# Способы оплаты
def pay_method_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💳 Карта (РФ, Украина, Казахстан)", data='pay_aaio')
    )

    keyboard.row(
        ikb("🪙 Крипта", data='pay_aaio')
    )

    return keyboard.as_markup()


# Ссылка на оплату
def pay_link_finl(link) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💵 Оплатить", url=link)
    )

    return keyboard.as_markup()


# Тарифы VIP
def vip_tariffs() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("3 дня - 300 berrycoins", data="3days_vip")
    )

    keyboard.row(
        ikb("7 дней - 600 berrycoins", data="7days_vip")
    )

    keyboard.row(
        ikb("14 дней - 1000 berrycoins", data="14days_vip")
    )

    return keyboard.as_markup()
