async def check_access(message, message_answer, message_keyboard=None):
    from app.database.requests.check_user import check_user

    if await check_user(message.from_user.id):
        return await message.answer(message_answer, reply_markup=message_keyboard) if message_keyboard else await \
            message.answer(message_answer)
    else:
        return await message.answer(f"Sorry, you do not have access to this bot. "
                                    f"Please contact support for assistance.")
