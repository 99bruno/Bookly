from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def create_keyboard_for_dancers(dancers: list) -> InlineKeyboardMarkup:
    keyboard = []
    for i in range(0, len(dancers), 2):
        row = [InlineKeyboardButton(text=f"Dancer {i+1}", callback_data=f"dancer_{i}")]
        if i + 1 < len(dancers):
            row.append(
                InlineKeyboardButton(
                    text=f"Dancer {i+2}", callback_data=f"dancer_{i + 1}"
                )
            )
        keyboard.append(row)

    keyboard.append(
        [InlineKeyboardButton(text="Return 🔙", callback_data="back_to_main_menu")]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_keyboard_for_couples(couples: list) -> InlineKeyboardMarkup:
    keyboard = []
    for i in range(0, len(couples), 2):
        row = [InlineKeyboardButton(text=f"Couple {i+1}", callback_data=f"couple_{i}")]
        if i + 1 < len(couples):
            row.append(
                InlineKeyboardButton(
                    text=f"Couple {i+2}", callback_data=f"couple_{i + 1}"
                )
            )
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="return_to_dancers"),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_keyboard_for_lessons(lessons: list) -> InlineKeyboardMarkup:
    keyboard = []
    for lesson in lessons:
        row = [InlineKeyboardButton(text=f"{lesson}", callback_data=f"lesson_{lesson}")]
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="return_to_dancers"),
            InlineKeyboardButton(
                text="Confirm ✅", callback_data="confirm_payment_selected"
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


couple_schedule_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Pay all 🖇️️", callback_data="pay_all"),
            InlineKeyboardButton(text="Pay selected 🎯", callback_data="pay_selected"),
        ],
        [
            InlineKeyboardButton(text="Cancel selected payment ??️", callback_data="select_cancel"),
        ],
        [
            InlineKeyboardButton(
                text="Manage lessons 📚", callback_data="manage_lessons"
            ),
            InlineKeyboardButton(text="Manage couple 👫", callback_data="manage_couple"),
        ],
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="return_to_couple"),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ],
    ]
)

couple_schedule_paid_confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Confirm ✅", callback_data="confirm_payment")],
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="return_to_couple"),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ],
    ]
)

manage_lessons_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Book a lesson ➕", callback_data="book_lesson"),
            InlineKeyboardButton(text="Cancel lesson ➖", callback_data="cancel_lesson"),
        ],
        [
            InlineKeyboardButton(
                text="Reschedule lesson 🔄", callback_data="manager_reschedule_lesson"
            )
        ],
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="return_to_schedule"),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ],
    ]
)

choose_program_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Latin", callback_data="latin_book_lesson")],
        [InlineKeyboardButton(text="Ballroom", callback_data="ballroom_book_lesson")],
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="manage_lessons"),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ],
    ],
)


def create_keyboard_for_coaches(coaches: list, couple_id: int):
    keyboard = []
    for coach in coaches:
        button = InlineKeyboardButton(
            text=f"{coach['coach_firstname']} {coach['coach_lastname']}",
            callback_data=f"book_lesson_coach_{coach['coach_id']}",
        )
        keyboard.append([button])

    keyboard.append(
        [
            InlineKeyboardButton(text="Return 🔙", callback_data=f"book_lesson"),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_keyboard_for_dates(dates: list):
    import datetime

    keyboard = []
    for idx, date in enumerate(dates):
        button = InlineKeyboardButton(text=str(date), callback_data=f"date_{idx}")
        keyboard.append([button])

    keyboard.append(
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="book_lesson"),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_keyboard_for_time(dates: list):
    keyboard = []
    row = []
    for date in dates:
        button = InlineKeyboardButton(text=date, callback_data=f"time_{date}")
        row.append(button)
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(
                text="Choose 📅", callback_data=f"book_lesson_to_confirm"
            ),
            InlineKeyboardButton(text="Return 🔙", callback_data=f"return_to_dates"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


confirm_book_lessons_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Confirm booking ✅", callback_data="booking_confirmation"
            )
        ],
        [
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            )
        ],
    ]
)


def create_keyboard_for_cancel_lesson(lessons: list) -> InlineKeyboardMarkup:
    keyboard = []
    for lesson in lessons:
        row = [
            InlineKeyboardButton(
                text=f"{lesson}", callback_data=f"cancel_lesson_{lesson}"
            )
        ]
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="return_to_schedule"),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


return_to_schedule_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Return 🔙", callback_data="return_to_schedule")],
        [
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            )
        ],
    ]
)


def create_keyboard_for_reschedule_lesson(lessons: list) -> InlineKeyboardMarkup:
    keyboard = []
    for lesson in lessons:
        row = [
            InlineKeyboardButton(
                text=f"{lesson}", callback_data=f"reschedule_lesson_{lesson}"
            )
        ]
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="return_to_schedule"),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_keyboard_for_confirm_reschedule_lesson(
    lessons: list[dict],
) -> InlineKeyboardMarkup:
    keyboard = []
    for idx, lesson in enumerate(lessons):
        row = [
            InlineKeyboardButton(
                text=f'{lesson["start_time"].strftime("%d.%m  %H:%M")}',
                callback_data=f"reschedule_a_lesson_by_manager_{idx}",
            )
        ]
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(text="Return 🔙", callback_data="return_to_reschedule"),
            InlineKeyboardButton(
                text="Back to home 🏡", callback_data="back_to_main_menu"
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
