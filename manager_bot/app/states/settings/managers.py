from aiogram.fsm.state import State, StatesGroup


class ManagerEdit(StatesGroup):
    add_manager = State()
    remove = State()
    add_admin = State()
