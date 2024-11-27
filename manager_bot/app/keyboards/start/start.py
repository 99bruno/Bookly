from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="View and edit coaches")],
        [KeyboardButton(text="Search a dancer"), KeyboardButton(text="Create couple")],
        [KeyboardButton(text="View full schedule"), KeyboardButton(text="Analysis 🔬")],
        [KeyboardButton(text="Camp Settings")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose what you want to do",
)
