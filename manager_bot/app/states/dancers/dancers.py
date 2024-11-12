from aiogram.fsm.state import State, StatesGroup


class Dancers(StatesGroup):
    dancers_info = State()
    current__dancer = State()
    dancer_schedule = State()
    couples_info = State()
    lessons = State()

    available_lessons_to_pay = State()
    lessons_to_pay = State()

    select_lessons = State()
