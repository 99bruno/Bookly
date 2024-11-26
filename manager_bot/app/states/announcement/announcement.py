from aiogram.fsm.state import State, StatesGroup


class Announcement(StatesGroup):
    msg = State()
    users_id = State()
