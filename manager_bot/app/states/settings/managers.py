from aiogram.fsm.state import StatesGroup, State


class ManagerEdit(StatesGroup):

    add_manager = State()
    remove = State()
    add_admin = State()
