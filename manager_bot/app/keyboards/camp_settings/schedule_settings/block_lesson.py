from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

schedule_settings_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Block lesson 🚫"),
            KeyboardButton(text="Unblock lesson ✅"),
        ],
        [
            KeyboardButton(text="Back to the main menu")
        ]
    ],
    resize_keyboard=True,
    selective=True)


async def dates_keyboard(dates: list) -> InlineKeyboardMarkup:
    keyboard = []
    row = []

    for i, date in enumerate(dates):
        row.append(InlineKeyboardButton(text=date, callback_data=f"block_date_choose_{date}"))
        if (i + 1) % 2 == 0 or i == len(dates) - 1:
            keyboard.append(row)
            row = []

    keyboard.append([
        InlineKeyboardButton(text="Back to home 🏡", callback_data='back_to_main_menu')
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def create_keyboard_for_coaches(coaches: dict) -> InlineKeyboardMarkup:
    keyboard = []
    row = []

    for i, (coach, coach_id) in enumerate(coaches.items()):
        row.append(InlineKeyboardButton(text=coach, callback_data=f"block_coach_choose_{coach_id}"))
        if (i + 1) % 2 == 0 or i == len(coaches) - 1:
            keyboard.append(row)
            row = []

    keyboard.append([
        InlineKeyboardButton(text="Return 🔙", callback_data='return_to_dates_of_blocking'),
        InlineKeyboardButton(text="Back to home 🏡", callback_data='back_to_main_menu')
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def create_keyboard_for_lessons(time: dict) -> InlineKeyboardMarkup:
    keyboard = []
    row = []

    for i, (time_, lesson_id) in enumerate(time.items()):
        row.append(InlineKeyboardButton(text=time_, callback_data=f"block_lesson_choose__{time_}_{lesson_id}"))
        if (i + 1) % 2 == 0 or i == len(time) - 1:
            keyboard.append(row)
            row = []

    keyboard.append([
        InlineKeyboardButton(text="Return 🔙", callback_data='return_to_coaches_of_blocking'),
        InlineKeyboardButton(text="Back to home 🏡", callback_data='back_to_main_menu')
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

