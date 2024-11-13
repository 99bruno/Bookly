from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

add_coach_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Add coach")],
        [KeyboardButton(text="Back to menu")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)


def create_keyboard_for_dates(dates):
    keyboard = []
    for i in range(0, len(dates), 2):
        row = [InlineKeyboardButton(text=dates[i], callback_data=f"num_{dates[i]}")]
        if i + 1 < len(dates):
            row.append(
                InlineKeyboardButton(
                    text=dates[i + 1], callback_data=f"num_{dates[i + 1]}"
                )
            )
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(text="Confirm", callback_data="confirm")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


add_coach_program_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Latin")],
        [KeyboardButton(text="Ballroom")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)

add_currency_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="EUR")],
        [KeyboardButton(text="USD")],
        [KeyboardButton(text="UAH")],
        [KeyboardButton(text="GBP")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)
