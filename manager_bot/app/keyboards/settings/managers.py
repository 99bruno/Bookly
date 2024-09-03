from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


managers_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Add manager")],
        [KeyboardButton(text="Add admin")],
        [KeyboardButton(text="Remove manager")],
        [
            KeyboardButton(text="Back to settings"),
            KeyboardButton(text="Back to the main menu")],
        ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)


async def remove_manager_kb(managers: list):
    keyboard = []
    for idx, manager in enumerate(managers):
        row = [InlineKeyboardButton(text=f"Manager {idx+1}", callback_data=f'manager_{manager["id"]}')]
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)