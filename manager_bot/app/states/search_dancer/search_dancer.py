from aiogram.fsm.state import StatesGroup, State


class Dancers(StatesGroup):
    dancers_info = State()
    current__dancer = State()
    dancer_schedule = State()
    couples_info = State()
    lessons = State()

    available_lessons_to_pay = State()
    lessons_to_pay = State()

    select_lessons = State()

