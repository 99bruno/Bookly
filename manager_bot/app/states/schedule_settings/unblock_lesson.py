from aiogram.fsm.state import StatesGroup, State


class UnblockLesson(StatesGroup):
    dates = State()
    current_date = State()
    current_coach = State()