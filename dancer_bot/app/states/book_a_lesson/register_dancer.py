from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    name = State()
    surname = State()
    phone_number = State()


class Couple(StatesGroup):
    couples = State()
    current_couple = State()


class RegisterCouple(StatesGroup):
    name = State()
    surname = State()
    phone_number = State()
