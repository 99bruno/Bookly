from aiogram.fsm.state import State, StatesGroup


class NewCouple(StatesGroup):
    phone_1 = State()
    phone_2 = State()

    name_1 = State()
    surname_1 = State()

    name_2 = State()
    surname_2 = State()

    dancer_id_1 = State()
    dancer_id_2 = State()
