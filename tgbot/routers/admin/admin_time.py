from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from tgbot.database.db_users import Userx

router = Router(name=__name__)


class AddTime(StatesGroup):
    choose_user = State()
    choose_time = State()


# Указание id пользователя
@router.callback_query(F.data == 'admin_add_time')
async def admin_add_time(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите id пользователя:')

    await state.set_state(AddTime.choose_user)


# Указание времени на добавление
@router.message(AddTime.choose_user)
async def choose_user(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await message.answer('Введите время, которое хотите добавить:')

    await state.set_state(AddTime.choose_time)


# Проверка и добавление времени
@router.message(AddTime.choose_time)
async def choose_user(message: Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        user_id = int(user_data['user_id'])
        user_uptime = int(message.text)
    except:
        await message.answer('⚠️ Был указан неверный тип дынных')
        await state.clear()
        return

    try:
        Userx.user_uptime(user_id=user_id, minutes=user_uptime)
        await message.answer(f"✅ Время добавлено пользователю: {user_data['user_id']}, кол-во минут - {user_uptime}")
    except:
        await message.answer('⚠️ Произошла ошибка, вероятно в введённых данных')
        await state.clear()
        return

    await state.clear()
