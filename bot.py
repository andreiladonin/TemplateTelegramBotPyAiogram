from aiogram.utils import executor
from config import bot, dp, env
from handlers.admin import *
from handlers.chat import *
from data.models import create_db

async def on_startup(_):
    print('The bot is running')
    await bot.send_message(int(env('ADMIN')), "Бот запущен")


if __name__ == "__main__":
    print('The bot is being launched')
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
