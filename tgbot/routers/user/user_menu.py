import numbersystem

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from tgbot.database.db_users import Userx
from tgbot.keyboards.reply_main import menu_frep, send_video_frep
from tgbot.keyboards.inline_main import discord_link_finl, balance_add_finl, vip_tariffs
from tgbot.data.config import DISCORD_LINK, MINUTES_PER_VIDEO, MINUTES_PER_REFERRAL
from tgbot.utils.const_functions import convert_date, get_date, get_unix

router = Router(name=__name__)


##### [/START] #####
@router.message(Command(commands=['start']))
async def start(message: Message, bot: Bot, state: FSMContext):
    await state.clear()

    user = Userx.get(user_id=message.from_user.id)

    if user.user_referral == 0:
        first_start = True
    else:
        first_start = False

    # Проверка на реферала
    referral_id = message.text[7:]
    if referral_id != '':
        referral_id = numbersystem.octalToDecimal(int(message.text[7:]))
        try:
            if message.from_user.id != referral_id and Userx.user_check_ref(referral_id):
                if user.user_referral == 0:
                    Userx.user_add_ref(message.from_user.id, referral_id)
                    Userx.user_uptime(referral_id, MINUTES_PER_REFERRAL)
                    try:
                        await bot.send_message(referral_id, 'У Вас новый реферал!\n'
                                                            f'+ {MINUTES_PER_REFERRAL} минут к доступу')
                    except:
                        pass
            else:
                await message.answer('Нельзя использовать свою реферальную ссылку!')
        except:
            await message.answer('Нельзя использовать несуществующую реферальную ссылку!')
    else:
        Userx.user_without_ref(message.from_user.id)

    # Обработка команды в чате
    await message.answer(f'Discord (на случай блокировки)\n\n{DISCORD_LINK}', reply_markup=discord_link_finl())
    try:
        if referral_id != '' and message.from_user.id != referral_id and Userx.user_check_ref(referral_id):
            await bot.pin_chat_message(chat_id=message.from_user.id, message_id=message.message_id + 2)
        else:
            await bot.pin_chat_message(chat_id=message.from_user.id, message_id=message.message_id + 1)

    except:
        pass
    await message.answer(
        '👋 Приветствую тебя в самом лучшем боте по <u>анонимному</u> видео обмену.\n\n'
        '✨ Чтобы начать, попробуй отправить своё первое интимное видео',
        reply_markup=menu_frep())

    if first_start:
        await message.answer('🎁 Вам было выдано 10 минут PREMIUM за регистрацию!')
        Userx.user_uptime(user_id=message.from_user.id, minutes=10)


##### [👤 Профиль] #####
@router.message(F.text == '👤 Профиль')
async def profile(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    user = Userx.get(user_id=message.from_user.id)
    bot_tag = await bot.get_me()

    date = convert_date(user.user_unix, False)

    if user.user_unix < get_unix():
        response = '🚫 Доступа нет!'
    else:
        response = f'✅ Доступ до: {date}'

    await message.answer(f'<b>👤 Профиль</b>\n\n'
                         f'🆔: <code>{message.from_user.id}</code>\n\n'
                         f'💵: {user.user_balance} berrycoins\n\n'
                         f'🔗 Реферальная ссылка:\n'
                         f'<code>t.me/{bot_tag.username}?start={numbersystem.decimalToOctal(message.from_user.id)}</code>\n\n'
                         f'👥 Кол-во рефералов: {0}\n\n'
                         f'{response}', reply_markup=balance_add_finl())


##### [ℹ️ Информация] #####
@router.message(F.text == 'ℹ️ Информация')
async def profile(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'<b>ℹ️ Информация</b>\n\n'
                         f'Данный бот создан специально для <u>анонимного</u> обмена интимными видео 18+\n\n'
                         f'Чтобы отправить видео нужно нажать соответсвующую кнопку снизу\n\n'
                         f'1 реферал = {MINUTES_PER_REFERRAL} минутам доступа\n'
                         f'1 видео = {MINUTES_PER_VIDEO} минутам доступа\n\n'
                         f'<b>СТРОГО ЗАПРЕЩЕНО:</b>\n'
                         f'1. ЦП\n'
                         f'2. PeД0Filия\n'
                         f'3. СПАМ\n'
                         f'4. Присылать боту видео не соответствующего характера\n\n'
                         f'За те или иные действия предусмотрено наказание по усмотрению администратора или модератора')


##### [⚡️ VIP] #####
@router.message(F.text == '⚡️ VIP')
async def profile(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'💨 Успейте купить VIP по самой низкой цене!', reply_markup=vip_tariffs())


##### [ 3 дня vip ] #####
@router.callback_query(F.data == '3days_vip')
async def vip_buy(call: CallbackQuery, state: FSMContext):
    await state.clear()
    amount = 300
    minutes = 60 * 24 * 3

    user = Userx.get(user_id=call.from_user.id)

    if user.user_balance < amount:
        await call.answer('🚫 Недостаточно средств на балансе!')
    else:
        await call.message.answer('✅ Было добавлено 3 дня доступа!')
        Userx.user_change_balance(call.from_user.id, -amount)
        Userx.user_uptime(user_id=call.from_user.id, minutes=minutes)


##### [ 7 дней vip ] #####
@router.callback_query(F.data == '7days_vip')
async def vip_buy(call: CallbackQuery, state: FSMContext):
    await state.clear()
    amount = 600
    minutes = 60 * 24 * 7

    user = Userx.get(user_id=call.from_user.id)

    if user.user_balance < amount:
        await call.answer('🚫 Недостаточно средств на балансе!')
    else:
        await call.message.answer('✅ Было добавлено 3 дня доступа!')
        Userx.user_change_balance(call.from_user.id, -amount)
        Userx.user_uptime(user_id=call.from_user.id, minutes=minutes)


##### [ 14 дней vip ] #####
@router.callback_query(F.data == '14days_vip')
async def vip_buy(call: CallbackQuery, state: FSMContext):
    await state.clear()
    amount = 1000
    minutes = 60 * 24 * 14

    user = Userx.get(user_id=call.from_user.id)

    if user.user_balance < amount:
        await call.answer('🚫 Недостаточно средств на балансе!')
    else:
        await call.message.answer('✅ Было добавлено 3 дня доступа!')
        Userx.user_change_balance(call.from_user.id, -amount)
        Userx.user_uptime(user_id=call.from_user.id, minutes=minutes)
