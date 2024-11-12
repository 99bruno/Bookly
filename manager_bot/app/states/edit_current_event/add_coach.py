from aiogram.fsm.state import State, StatesGroup


class NewCoach(StatesGroup):
    name = State()
    surname = State()
    price = State()
    program = State()
    dates = State()
    selecting_numbers = State()
    waiting_for_numbers = State()
