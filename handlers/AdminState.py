from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminState(StatesGroup):
    upload_image = State()