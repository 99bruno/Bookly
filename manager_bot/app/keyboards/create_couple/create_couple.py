from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Coaches settings 🕺💃")],
        [KeyboardButton(text="Camp settings 🏕")],
        [KeyboardButton(text="Back to the main menu")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)
