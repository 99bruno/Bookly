from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

check_camp_info_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Переглянути список тренерів")
        ],
        [
            KeyboardButton(text="Вернутись в головне меню")
        ],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)


coaches_program_choose_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Latin", callback_data="coaches_program_choose_Latin")
        ],
        [
            InlineKeyboardButton(text="Ballroom", callback_data="coaches_program_choose_Ballroom")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="return_to_check_camp_info"),
            InlineKeyboardButton(text="В головне меню 🏡", callback_data="back_to_main_menu")
        ],
    ]
)


def create_keyboard_for_coaches_camp_info(coaches: list):
    keyboard = []

    for i in range(0, len(coaches), 2):
        row = [InlineKeyboardButton(text=f"Тренер {i+1}", callback_data=f'camp_info_coach_{coaches[i]["id"]}')]
        if i + 1 < len(coaches):
            row.append(InlineKeyboardButton(text=f"Тренер {i+2}", callback_data=f'camp_info_coach_{coaches[i+1]["id"]}'))
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(text="Назад 🔙", callback_data='return_to_program_choose'),
        InlineKeyboardButton(text="В головне меню 🏡", callback_data='back_to_main_menu'),

    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


coach_info_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Переглянути ціну", callback_data="view_price")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="return_to_coaches_list"),
            InlineKeyboardButton(text="В головне меню 🏡", callback_data="back_to_main_menu")
        ],
    ]
)


coach_view_price_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ціни всіх викладачів 💸", callback_data="compare_prices")
        ],
        [
            InlineKeyboardButton(text="В головне меню 🏡", callback_data="back_to_main_menu")
        ],
    ]
)

coach_compare_price_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Програми 🕺", callback_data="return_to_program_choose"),
            InlineKeyboardButton(text="В головне меню 🏡", callback_data="back_to_main_menu")
        ],
    ]
)
