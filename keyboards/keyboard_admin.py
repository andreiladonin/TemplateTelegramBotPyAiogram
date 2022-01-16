from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_admin_1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

keyboard_1_buttons = ["Загрузить фото"]

keyboard_admin_1.add(*keyboard_1_buttons)