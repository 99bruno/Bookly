from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Забронювати уроки 📅")],
        [KeyboardButton(text="Мої бронювання 🕒")],
        [KeyboardButton(text="Інформація про кемп 🪩")],
        [KeyboardButton(text="Потрібна допомога? 🆘")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)

back_to_main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Повернутись в головне меню")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)
