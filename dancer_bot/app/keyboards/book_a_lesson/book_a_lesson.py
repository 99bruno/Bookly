from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


share_contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Поширити контакт",
                request_contact=True)
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажміть кнопку нижче, щоб поширити контакт"
)


def create_keyboard_for_choose_couple(couples: list):
    keyboard = []
    for i in range(0, len(couples), 2):
        row = [InlineKeyboardButton(text=f"Пара {i+1}", callback_data=f'couple_{i}')]
        if i + 1 < len(couples):
            row.append(InlineKeyboardButton(text=f"Пара {i+2}", callback_data=f'couple_{i + 1}'))
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(text="Змінити партнера", callback_data='change_couple')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


choose_program_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Latin", callback_data="latin_book_lesson")],
        [InlineKeyboardButton(text="Ballroom", callback_data="ballroom_book_lesson")],
             ],
)


change_partner_solo_or_couple_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Соло")],
        [KeyboardButton(text="В парі")],
             ],
    resize_keyboard=True,
    input_field_placeholder="Вибери"
)


def create_keyboard_for_coaches(coaches: list, couple_id: int):
    keyboard = []
    for coach in coaches:
        button = InlineKeyboardButton(
            text=f"{coach['coach_firstname']} {coach['coach_lastname']}",
            callback_data=f"coach_{coach['coach_id']}"
        )
        keyboard.append([button])

    keyboard.append([InlineKeyboardButton(text="Назад 🔙", callback_data=f"couple_{couple_id}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_keyboard_for_dates(dates: list):
    import datetime
    keyboard = []
    for idx, date in enumerate(dates):
        button = InlineKeyboardButton(
            text=str(date),
            callback_data=f"date_{idx}"
        )
        keyboard.append([button])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_keyboard_for_time(dates: list):
    keyboard = []
    row = []
    for date in dates:
        button = InlineKeyboardButton(
            text=date,
            callback_data=f"time_{date}"
        )
        row.append(button)
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(text="Обрати", callback_data=f"book_lesson"),
                    InlineKeyboardButton(text="Назад 🔙", callback_data=f"return_to_dates")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


confirm_book_lessons_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Підтвердити бронювання", callback_data="lesson_booking_confirmation")],
        [InlineKeyboardButton(text="Повернутись в головне меню", callback_data="back_to_main_menu")],
             ])
