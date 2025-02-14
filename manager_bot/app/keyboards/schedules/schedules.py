from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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