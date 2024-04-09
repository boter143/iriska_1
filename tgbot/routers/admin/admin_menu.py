from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

from tgbot.keyboards.inline_main import admin_panel_finl
from tgbot.database.db_users import Userx

router = Router(name=__name__)


@router.message(Command(commands=['admin']))
async def admin_menu(message: Message):
    await message.answer(f'<b>👑 Админ-панель</b>\n\n'
                         f'Кол-во 👥: {Userx.get_all_count()}',
                         reply_markup=admin_panel_finl())
