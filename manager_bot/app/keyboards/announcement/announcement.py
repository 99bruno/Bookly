from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

announcements_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Send a message to all users 📢")],
        [KeyboardButton(text="Send a message by coach booking 📢")],
        [KeyboardButton(text="Back to the main menu")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)


def announcements_choose_coach_kb(coaches: list[dict]) -> InlineKeyboardMarkup:
    keyboard = []
    for i in range(0, len(coaches), 2):
        row = [InlineKeyboardButton(text=f"{coaches[i]['name']}", callback_data=f"message_by_coach_{i}")]
        if i + 1 < len(coaches):
            row.append(
                InlineKeyboardButton(
                    text=f"{coaches[i+1]['name']}", callback_data=f"message_by_coach_{i + 1}"
                )
            )
        keyboard.append(row)

    keyboard.append(
        [InlineKeyboardButton(text="Return 🔙", callback_data="back_to_main_menu")]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)