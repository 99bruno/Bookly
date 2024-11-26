from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

camp_settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Coaches settings 🕺💃")],
        [KeyboardButton(text="Camp settings 🏕")],
        [KeyboardButton(text="Schedule settings 📅")],
        [KeyboardButton(text="Make a announcement 📢")],
        [KeyboardButton(text="Back to the main menu")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)
