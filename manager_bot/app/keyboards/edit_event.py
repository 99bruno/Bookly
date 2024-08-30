from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

edit_event_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Add new coach")],
        [KeyboardButton(text="View full schedule")],
        [KeyboardButton(text="Edit camp info")],
        [KeyboardButton(text="Back to the main menu")]
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)

view_schedule_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Back to menu")],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)

edit_camp_info_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Change name of the camp")],
        [KeyboardButton(text="Change dates")],
        [KeyboardButton(text="Edit massage with full info")],
        [KeyboardButton(text="Back to menu")],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)

change_name_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Back to menu")],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)

change_date_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Back to menu")],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)

change_description_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Back to menu")],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)
