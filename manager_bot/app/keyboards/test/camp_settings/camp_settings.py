from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


camp_settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Edit camp info")],
        [
           KeyboardButton(text="Back to the main menu"),
           KeyboardButton(text="Back to camp settings")
        ],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)