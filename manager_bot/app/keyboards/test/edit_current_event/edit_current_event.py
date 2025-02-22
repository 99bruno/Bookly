from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

edit_current_event_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Coaches")],
        [KeyboardButton(text="Camp info")],
        [KeyboardButton(text="Dancers info")],
        [KeyboardButton(text="Back to the main menu")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)
