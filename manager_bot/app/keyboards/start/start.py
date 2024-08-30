from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Create a new event ")],
        [KeyboardButton(text="Edit the current event")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose what you want to do"
)
