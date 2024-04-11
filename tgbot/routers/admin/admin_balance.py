from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from tgbot.database.db_users import Userx

router = Router(name=__name__)


class ChangeBalance(StatesGroup):
    choose_user = State()
    choose_balance = State()


# Указание id пользователя
@router.callback_query(F.data == 'admin_change_balance')
async def admin_add_time(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите id пользователя:')

    await state.set_state(ChangeBalance.choose_user)


# Указание количества berrycoins на добавление
@router.message(ChangeBalance.choose_user)
async def choose_user(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await message.answer('Введите количество 💵, которое хотите добавить:')

    await state.set_state(ChangeBalance.choose_balance)


# Проверка и добавление berrycoins
@router.message(ChangeBalance.choose_balance)
async def choose_user(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    try:
        user_id = int(user_data['user_id'])
        user_upbalance = int(message.text)
    except:
        await message.answer('⚠️ Был указан неверный тип дынных')
        await state.clear()
        return

    try:
        Userx.user_change_balance(user_id=user_id, count=user_upbalance)
        await message.answer(f"✅ Пользователю: {user_id} добавлено {user_upbalance} berrycoins")
        await bot.send_message(chat_id=user_id, text=f'✅ Админ начислил Вам на баланс {user_upbalance} berrycoins!')
    except:
        await message.answer('⚠️ Произошла ошибка, вероятно в введённых данных')
        await state.clear()
        return

    await state.clear()
