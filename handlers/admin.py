from bot import bot, dp, env
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.keyboard_admin import *
from .AdminState import AdminState
from data.models import UserBot, session
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
import os, random

get_user_callback = CallbackData('get_user_', 'tg_id')


@dp.message_handler(commands=['admin'])
@dp.message_handler(lambda message: message.text == "Загрузить фото", state=None)
async def auth_admin(message: types.Message, state:FSMContext):
    if message.from_user.id == int(env('ADMIN')):
        if message.text == "Загрузить фото":
            await AdminState.upload_image.set()
            await bot.send_message(message.from_user.id, "Выберите фото для загрузки: ")
        else:
            await bot.send_message(message.from_user.id, "Вы вошли в админскую часть\nВыберите действие:", reply_markup=keyboard_admin_1)
    else:
        await message.delete()


@dp.message_handler(content_types=["photo", "text"], state=AdminState.upload_image)
async def upload_to_photo(message: types.Message, state: FSMContext):
    if message.text == '/cancel':
        await state.finish()
        await message.answer("Вы вышли из загрузки фото")
        return
    if message.content_type != 'photo':
        await message.answer('Пожалуйста загрузи фото')
        return
    await message.photo[-1].download(f'handlers/images/{message.photo[-1].file_id}.jpg')
    await message.answer('Успешно!')
    await state.finish()


@dp.message_handler(commands=['get_users'])
async def get_users(message: types.Message):
    if message.from_user.id == int(env('ADMIN')):
        users = session.query(UserBot.telegram_id).all()
        inline_kb_users = InlineKeyboardMarkup(row_width=1)
        for user in users:
            inline_kb_users.insert(InlineKeyboardButton(text=str(user[0]), callback_data=get_user_callback.new(
                tg_id = user[0]
            )))

        await bot.send_message(message.from_user.id, "Список пользователей:", reply_markup=inline_kb_users)
    else:
        await message.delete()


@dp.callback_query_handler(Text(startswith="get_user_"))
async def get_user(call: types.CallbackQuery):
    tg_id = int(call.data.replace('get_user_:', ''))
    user = session.query(UserBot).filter(UserBot.telegram_id == tg_id).first()


    await call.message.answer(text=f"ID: {user.telegram_id}\nУровень: {user.level}\nКол-во сообщений: {user.message_count}")
