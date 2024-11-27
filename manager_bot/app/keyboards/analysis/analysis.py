from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

add_coach_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Booked lessons", callback_data="analysis_booked_lessons")],
        [InlineKeyboardButton(text="Coaches booking rating", callback_data="analysis_coaches_booking_rating")],
        [InlineKeyboardButton(text="Coaches with available lessons",
                              callback_data="analysis_coaches_with_available_lessons")],
        [InlineKeyboardButton(text="Overall income", callback_data="analysis_overall_income")],
    ]
)