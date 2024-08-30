from aiogram.fsm.state import StatesGroup, State


class LessonRegistration(StatesGroup):
    couples = State()
    program = State()
    coach_id = State()
    couple_id = State()
    confirmation = State()
    all_dates = State()
    available_dates = State()
    current_date = State()
    selected_dates = State()
