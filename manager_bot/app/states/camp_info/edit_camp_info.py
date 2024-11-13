from aiogram.fsm.state import State, StatesGroup


class EditEvent(StatesGroup):
    name = State()
    date = State()
    description = State()
