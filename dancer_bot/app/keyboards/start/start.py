from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Забронювати уроки 📅")],
        [KeyboardButton(text="Мої бронювання 🕒")],
        [KeyboardButton(text="Інформація про кемп 🪩")],
        [KeyboardButton(text="Потрібна допомога? 🆘")],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)

back_to_main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Вернутись в головне меню")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)
