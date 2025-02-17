from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

schedules_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="View full schedule for each couple")],
        [KeyboardButton(text="View full schedule for each coach")],
        [KeyboardButton(text="View full schedule in Excel")],
        [KeyboardButton(text="Back to the main menu")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose what you want to do",
)


async def create_schedule_keyboard(dates: list) -> InlineKeyboardMarkup:
    keyboard = []
    for i in range(0, len(dates), 2):
        row = [InlineKeyboardButton(text=dates[i].strftime("%d-%m-%Y"), callback_data=f"schedule_coach_for_{dates[i]}")]
        if i + 1 < len(dates):
            row.append(InlineKeyboardButton(text=dates[i + 1].strftime("%d-%m-%Y"), callback_data=f"schedule_coach_for_{dates[i + 1]}"))

        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
