from aiogram.fsm.state import State, StatesGroup


class Coach(StatesGroup):
    program = State()
    coach_info = State()
