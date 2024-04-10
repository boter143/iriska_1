from aiogram import Router, F, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.database.db_users import Userx

router = Router(name=__name__)


class BanUser(StatesGroup):
    choose_user = State()


# Запрос id пользователя
@router.callback_query(F.data == 'admin_ban_unban_user')
async def admin_ban_unban_user(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите id пользователя:')

    await state.set_state(BanUser.choose_user)


# Бан пользователя за видео
@router.message(BanUser.choose_user)
async def choose_user_to_ban(message: Message, bot: Bot, state: FSMContext):
    try:
        user_to_ban = int(message.text)
        answer = Userx.user_ban_unban(user_to_ban)
        if Userx.user_exist(user_to_ban):
            if answer:
                await message.answer(f'⛔ Пользователь {user_to_ban} был <b>забанен</b>')
                await bot.send_message(chat_id=user_to_ban, text='⛔ Вы были забанены администратором!\n'
                                                                 'Теперь Вы не сможете отправлять видео\n\n'
                                                                 '<b>Причина:</b> Без объяснения.')
            else:
                await message.answer(f'✅ Пользователь {user_to_ban} был <b>разбанен</b>')
                await bot.send_message(chat_id=user_to_ban, text='✅ Вы были разбанены администратором!\n'
                                                                 'Теперь Вы можете отправлять видео')
        else:
            await message.answer('⚠ Пользователя {user_id} не существует\n'
                                 'Попробуйте заново')
    except:
        await message.answer('⚠ Некорректный id пользователя!\n'
                             'Попробуйте заново')

    await state.clear()
