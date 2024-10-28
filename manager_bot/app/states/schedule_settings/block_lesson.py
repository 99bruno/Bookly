from aiogram.fsm.state import StatesGroup, State


class BlockLesson(StatesGroup):
    dates = State()
    current_date = State()
    current_coach = State()

