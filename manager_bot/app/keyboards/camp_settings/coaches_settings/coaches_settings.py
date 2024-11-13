from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

coaches_settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Add new coach")],
        [KeyboardButton(text="View and edit coaches")],
        [KeyboardButton(text="Back to the main menu")],
    ],
    resize_keyboard=True,
    selective=True,
)
