from aiogram.fsm.state import State, StatesGroup


class Dancers(StatesGroup):
    dancers_info = State()
    current__dancer = State()
    dancer_schedule = State()
    couples_info = State()
    lessons = State()

    available_lessons_to_pay = State()
    lessons_to_pay = State()

    available_lessons_to_cancel = State()
    lesson_to_cancel = State()

    select_lessons = State()
    cancel_select_lessons = State()

    reason = State()


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
