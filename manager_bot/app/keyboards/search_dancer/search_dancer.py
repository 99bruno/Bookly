from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def create_keyboard_for_dancers(dancers: list) -> InlineKeyboardMarkup:
    keyboard = []
    for i in range(0, len(dancers), 2):
        row = [InlineKeyboardButton(text=f"Dancer {i+1}", callback_data=f'dancer_{i}')]
        if i + 1 < len(dancers):
            row.append(InlineKeyboardButton(text=f"Dancer {i+2}", callback_data=f'dancer_{i + 1}'))
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(text="Return 🔙", callback_data='back_to_main_menu')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_keyboard_for_couples(couples: list) -> InlineKeyboardMarkup:
    keyboard = []
    for i in range(0, len(couples), 2):
        row = [InlineKeyboardButton(text=f"Couple {i+1}", callback_data=f'couple_{i}')]
        if i + 1 < len(couples):
            row.append(InlineKeyboardButton(text=f"Couple {i+2}", callback_data=f'couple_{i + 1}'))
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(text="Return 🔙", callback_data='return_to_dancers'),
        InlineKeyboardButton(text="Back to home 🏡", callback_data='back_to_main_menu')
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_keyboard_for_lessons(lessons: list) -> InlineKeyboardMarkup:
    keyboard = []
    for lesson in lessons:
        row = [InlineKeyboardButton(text=f"{lesson}", callback_data=f'lesson_{lesson}')]
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(text="Return 🔙", callback_data='return_to_dancers'),
        InlineKeyboardButton(text="Confirm ✅", callback_data='confirm_payment_selected')
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


couple_schedule_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Pay all 🖇️️", callback_data="pay_all")],
        [InlineKeyboardButton(text="Pay selected 🎯", callback_data="pay_selected")],
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="return_to_couple"),
            InlineKeyboardButton(text="Back to home 🏡", callback_data="back_to_main_menu")
        ]
    ]
)

couple_schedule_paid_confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Confirm ✅", callback_data="confirm_payment")],
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="return_to_couple"),
            InlineKeyboardButton(text="Back to home 🏡", callback_data="back_to_main_menu")
        ]
    ]
)