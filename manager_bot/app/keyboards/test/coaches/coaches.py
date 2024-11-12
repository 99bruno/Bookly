import ast

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

coach_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Add new coach")],
        [KeyboardButton(text="Go to the list of coaches")],
        [KeyboardButton(text="Back to menu")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)


def coaches_list_keyboard(coaches):
    keyboard = []
    for i in range(0, len(coaches), 2):
        row = [InlineKeyboardButton(text=f"Coach {i+1}", callback_data=f"coach_{i}")]
        if i + 1 < len(coaches):
            row.append(
                InlineKeyboardButton(text=f"Coach {i+2}", callback_data=f"coach_{i+1}")
            )
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(text="Return", callback_data="return_to_coaches_menu"),
            InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_keyboard_for_dates(dates_list):
    dates = ast.literal_eval(dates_list)
    keyboard = []
    for i in range(0, len(dates), 2):
        row = [InlineKeyboardButton(text=dates[i], callback_data=f"date_{dates[i]}")]
        if i + 1 < len(dates):
            row.append(
                InlineKeyboardButton(
                    text=dates[i + 1], callback_data=f"date_{dates[i + 1]}"
                )
            )
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(text="Return", callback_data="return_to_coach_info"),
            InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


coach_info_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="View schedule", callback_data="view_schedule")],
        [InlineKeyboardButton(text="Edit info", callback_data="edit_info")],
        [
            InlineKeyboardButton(text="Return", callback_data="return_to_coaches"),
            InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"),
        ],
    ]
)


coach_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Edit name", callback_data="edit_coach_name")],
        [InlineKeyboardButton(text="Edit surname", callback_data="edit_coach_surname")],
        [InlineKeyboardButton(text="Edit program", callback_data="edit_coach_program")],
        [
            InlineKeyboardButton(text="Edit price", callback_data="edit_coach_price"),
            InlineKeyboardButton(
                text="Edit currency", callback_data="edit_coach_currency"
            ),
        ],
        [InlineKeyboardButton(text="Delete coach", callback_data="delete_coach")],
        [
            InlineKeyboardButton(text="Return", callback_data="return_to_coach"),
            InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu"),
        ],
    ]
)


program_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Latin", callback_data="latin")],
        [InlineKeyboardButton(text="Ballroom", callback_data="ballroom")],
    ]
)


currency_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="EUR", callback_data="EUR")],
        [InlineKeyboardButton(text="USD", callback_data="USD")],
        [InlineKeyboardButton(text="UAH", callback_data="UAH")],
        [InlineKeyboardButton(text="GBP", callback_data="GBP")],
    ]
)
