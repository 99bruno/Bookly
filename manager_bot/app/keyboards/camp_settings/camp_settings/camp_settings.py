from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

camp_info_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Edit camp info")
        ],
        [
            KeyboardButton(text="Back to the main menu")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)
