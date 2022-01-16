from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import environ

env = environ.Env()
environ.Env.read_env()
bot = Bot(token=env("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
