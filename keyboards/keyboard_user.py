from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

keyboard_1_buttons = ['Помощь 🔎', '📸 Отправить мемчик']

keyboard_1.add(*keyboard_1_buttons)