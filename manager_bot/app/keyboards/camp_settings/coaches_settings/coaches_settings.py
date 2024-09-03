from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

coaches_settings_kb = ReplyKeyboardMarkup(
    keyboard=[
            [
                KeyboardButton(text="Add new coach")
            ],
            [
                KeyboardButton(text="Delete coach")
            ],
            [
                KeyboardButton(text="View and edit coaches")
            ],
            [
                KeyboardButton(text="Back to the main menu")
            ],
    ],
    resize_keyboard=True,
    selective=True)
