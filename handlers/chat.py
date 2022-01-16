from bot import bot, dp, env
from aiogram import types
from keyboards.keyboard_user import *
from data.models import UserBot, session

import os, random

LEVELS = {
    5: "Младенц",
    15: "Мальчик",
    30: "Юноша",
    50: "Солдат",
    75: "Мужчина",
    100: "Пожилой",
    150: "Старик"
}


async def update_level(tg_id):
    user = session.query(UserBot).filter(UserBot.telegram_id == tg_id).first()
    user.message_count += 1
    if user.message_count in LEVELS.keys():
        user.level = LEVELS[user.message_count]
        await bot.send_message(tg_id, f"Ваш уровень повышен до '{LEVELS[user.message_count]}'")
    session.add(user)
    session.commit()


@dp.message_handler(commands=['start'])
async def start_chat(message: types.Message):
    try:
        user = UserBot(telegram_id=message.from_user.id)
        session.add(user)
        session.commit()
        await bot.send_message(message.from_user.id, f"Добро пожаловать к боту\n"
                                                f"Уровень: {user.level}\n"
                                                f"Дата создания: {user.date_created.strftime('%d/%m/%Y')}", reply_markup=keyboard_1)
    except:
        await bot.send_message(message.chat.id, "Отправьте команду или воспользуйтесь клаиатурой", reply_markup=keyboard_1)
        await update_level(message.from_user.id)


@dp.message_handler(commands=['help', 'info'])
@dp.message_handler(lambda message: message.text == "Помощь 🔎")
async def answer_message(message: types.Message):
    query_result = session.query(UserBot).filter(UserBot.telegram_id == message.from_user.id).count()
    if query_result == 0:
        await message.reply("Новым пользавтелям надо нажать /start")
        await message.delete()
    else:
        await bot.send_message(message.chat.id, "Описание комманд", reply_markup=keyboard_1)
        await update_level(message.from_user.id)

# @dp.message_handler(commands=['geo'])
# async def answer_message(message: types.Message):
#     await bot.send_message(message.from_user.id, "г.Самара\n"
#                                                  "ул.Ленина д.7")

@dp.message_handler(commands=['photo_random'])
@dp.message_handler(lambda message: message.text == "📸 Отправить мемчик")
async def send_mems_random(message:types.Message):
    query_result = session.query(UserBot).filter(UserBot.telegram_id == message.from_user.id).count()
    if query_result == 0:
        await message.reply("Новым пользавтелям надо нажать /start")
        await message.delete()
    else:
        path_img = env("IMAGES_FOLDER")
        image = random.choice(os.listdir(path_img))
        with open(path_img + "\\" + image, 'rb') as f:
            await bot.send_photo(message.chat.id, f, caption="Вот фото!")
            await update_level(message.from_user.id)


@dp.message_handler()
async def check_chat(message: types.Message):
    query_result = session.query(UserBot).filter(UserBot.telegram_id == message.from_user.id).count()
    if query_result == 0:
        await message.reply("Новым пользавтелям надо нажать /start")
        await message.delete()
    else:
        await update_level(message.from_user.id)