from aiogram.fsm.state import StatesGroup, State

class EditEvent(StatesGroup):
    name = State()
    date = State()
    description = State()