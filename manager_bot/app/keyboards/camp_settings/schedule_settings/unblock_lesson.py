from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


async def dates_keyboard(dates: list) -> InlineKeyboardMarkup:
    keyboard = []
    row = []

    for i, date in enumerate(dates):
        row.append(
            InlineKeyboardButton(text=date, callback_data=f"date_choose_unblock_{date}")
        )
        if (i + 1) % 2 == 0 or i == len(dates) - 1:
            keyboard.append(row)
            row = []

    keyboard.append(
        [InlineKeyboardButton(text="Back to home 🏡", callback_data="back_to_main_menu")]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def create_keyboard_for_coaches(coaches: dict) -> InlineKeyboardMarkup:
    keyboard = []
    row = []

    for i, (coach, coach_id) in enumerate(coaches.items()):
        row.append(
            InlineKeyboardButton(
                text=coach, callback_data=f"choose_coach__unblock_{coach_id}"
            )
        )
        if (i + 1) % 2 == 0 or i == len(coaches) - 1:
            keyboard.append(row)
            row = []

    keyboard.append(
        [
            InlineKeyboardButton(
                text="Return 🔙", callback_data="return_to_dates_of_unblocking"
            ),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def create_keyboard_for_lessons(time: dict) -> InlineKeyboardMarkup:
    keyboard = []
    row = []

    for i, (time_, lesson_id) in enumerate(time.items()):
        row.append(
            InlineKeyboardButton(
                text=time_, callback_data=f"choose_lesson_unblock__{time_}_{lesson_id}"
            )
        )
        if (i + 1) % 2 == 0 or i == len(time) - 1:
            keyboard.append(row)
            row = []

    keyboard.append(
        [
            InlineKeyboardButton(
                text="Return 🔙", callback_data="return_to_coaches_of_unblocking"
            ),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
