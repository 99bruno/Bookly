from aiogram.fsm.state import StatesGroup, State


class NewCoach(StatesGroup):
    name = State()
    surname = State()
    price = State()
    currency = State()
    program = State()
    dates = State()
    full_schedule = State()
    selecting_numbers = State()
    waiting_for_numbers = State()