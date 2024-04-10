from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from tgbot.database.db_users import Userx
from tgbot.database.db_video import Videox
from tgbot.keyboards.inline_main import admin_moderation_finl
from tgbot.keyboards.reply_main import send_video_frep, menu_frep
from tgbot.data.config import CHAT_ID
from tgbot.utils.const_functions import convert_date, get_unix

router = Router(name=__name__)


class AdminModeration(StatesGroup):
    in_moderation = State()
    stop_moderation = State()


@router.callback_query(F.data == 'admin_moderation_video')
async def start_admin_moderation(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.answer('⚠ Если захочешь остановиться, нажми кнопку снизу!', reply_markup=send_video_frep())

    all_video_id = Videox.get_all_id()

    if not bool(len(all_video_id)):
        await call.message.answer('Нет видео для модерации!', reply_markup=menu_frep())
        return
    else:
        video_index = 0
        video = Videox.get(video_id=all_video_id[video_index][0])
        video_index += 1
        await state.update_data(video_index=video_index)

        try:
            await bot.copy_message(from_chat_id=CHAT_ID, chat_id=call.message.chat.id, message_id=video.video_id,
                                   reply_markup=admin_moderation_finl())
        except:
            pass

        print(video)


@router.callback_query(F.data == 'moderation_access')
async def start_admin_moderation(call: CallbackQuery, bot: Bot, state: FSMContext):
    state_data = await state.get_data()

    video_index = state_data['video_index']

    all_video_id = Videox.get_all_id()

    try:
        video = Videox.get(video_id=all_video_id[video_index][0])
        video_index += 1
    except:
        await call.message.answer('Нет видео для модерации!', reply_markup=menu_frep())
        await state.clear()
        return
    await state.update_data(video_index=video_index)

    try:
        await bot.copy_message(from_chat_id=CHAT_ID, chat_id=call.message.chat.id, message_id=video.video_id,
                               reply_markup=admin_moderation_finl())
    except:
        pass
