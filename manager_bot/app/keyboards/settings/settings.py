from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Create new event")],
        [KeyboardButton(text="Edit managers")],
        [KeyboardButton(text="Ban user")],
        [KeyboardButton(text="Back to the main menu")],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)
