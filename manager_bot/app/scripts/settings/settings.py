from aiogram import types
from aiogram.fsm.context import FSMContext
from app.database.requests.check_user import check_admin


def restricted(func):
    async def wrapper(message: [types.Message | FSMContext], state: FSMContext):
        if await check_admin(message.from_user.id):
            return await func(message, state)
        else:
            await message.answer("You are not an admin")

    return wrapper
