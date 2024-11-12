from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def create_keyboard_for_choose_couple_for_schedule(
    couples: list,
) -> InlineKeyboardMarkup:
    keyboard = []

    for i in range(0, len(couples), 2):
        row = [
            InlineKeyboardButton(
                text=f"Пара {i + 1}", callback_data=f"schedules_couple_{i}"
            )
        ]
        if i + 1 < len(couples):
            row.append(
                InlineKeyboardButton(
                    text=f"Пара {i + 2}", callback_data=f"schedules_couple_{i + 1}"
                )
            )
        keyboard.append(row)

    keyboard.append(
        [InlineKeyboardButton(text=f"Назад 🔙", callback_data=f"back_to_main_menu")]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


check_schedules_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Скасувати запис", callback_data="cancel_lesson"),
            InlineKeyboardButton(
                text="Перенести урок", callback_data="reschedule_lesson"
            ),
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="back_to_couples"),
            InlineKeyboardButton(
                text="В головне меню 🏠", callback_data="back_to_main_menu"
            ),
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
            InlineKeyboardButton(text="Назад 🔙", callback_data="return_to_schedule"),
            InlineKeyboardButton(
                text="В головне меню 🏠", callback_data="back_to_main_menu"
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


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
            InlineKeyboardButton(text="Назад 🔙", callback_data="return_to_schedule"),
            InlineKeyboardButton(
                text="В головне меню 🏠", callback_data="back_to_main_menu"
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
                callback_data=f"lesson_reschedule{idx}",
            )
        ]
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="return_to_reschedule"),
            InlineKeyboardButton(
                text="В головне меню 🏠", callback_data="back_to_main_menu"
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# ----------------------------------------------------------------------------------------------------------------------


def create_keyboard_for_choose_schedule(lessons: list):
    keyboard = []

    for i in range(0, len(lessons), 2):
        row = [
            InlineKeyboardButton(
                text=f"Заняття {i + 1}", callback_data=f"schedules_{i}"
            )
        ]
        if i + 1 < len(lessons):
            row.append(
                InlineKeyboardButton(
                    text=f"Заняття {i + 2}", callback_data=f"schedules_{i + 1}"
                )
            )
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


confirm_lesson_cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Скасувати урок")],
        [KeyboardButton(text="Повернутись в головне меню")],
    ],
    resize_keyboard=True,
)


def create_keyboard_for_cancel_schedule(lessons: list) -> InlineKeyboardMarkup:
    keyboard = []

    for i in range(0, len(lessons), 2):
        row = [
            InlineKeyboardButton(
                text=f"Заняття {i + 1}", callback_data=f"schedules_{i}"
            )
        ]
        if i + 1 < len(lessons):
            row.append(
                InlineKeyboardButton(
                    text=f"Заняття {i + 2}", callback_data=f"schedules_{i + 1}"
                )
            )
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
