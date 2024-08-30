from aiogram.fsm.state import StatesGroup, State


class Coach(StatesGroup):
    program = State()
    coach_info = State()
