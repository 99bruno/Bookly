from aiogram.fsm.state import State, StatesGroup


class BlockLesson(StatesGroup):
    dates = State()
    current_date = State()
    current_coach = State()
