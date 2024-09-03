from aiogram.fsm.state import StatesGroup, State


class ListOfCoaches(StatesGroup):
    coaches = State()
    current_coach = State()
    coach = State()
    edit = State()
    name = State()
    surname = State()
    program = State()
    price = State()
    currency = State()
    dates = State()

    current_date = State()