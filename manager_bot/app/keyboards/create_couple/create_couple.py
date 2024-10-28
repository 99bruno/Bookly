from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Coaches settings 🕺💃")],
        [KeyboardButton(text="Camp settings 🏕")],
        [KeyboardButton(text="Back to the main menu")],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)