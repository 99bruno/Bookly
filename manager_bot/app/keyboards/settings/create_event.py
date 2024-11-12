from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

confirm_create_event_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Create new event ")],
        [KeyboardButton(text="Decline")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose",
)

type_of_schedule_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Create a template for all days ", callback_data="single_template"
            )
        ],
        [
            InlineKeyboardButton(
                text="Enter a template for each day", callback_data="multiple_templates"
            )
        ],
    ]
)


single_template_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Start time", callback_data="single_event_start_time"
            )
        ],
        [InlineKeyboardButton(text="End time", callback_data="single_event_end_time")],
        [InlineKeyboardButton(text="Duration", callback_data="single_event_duration")],
        [InlineKeyboardButton(text="Breaks", callback_data="single_event_breaks")],
        [
            InlineKeyboardButton(
                text="Return", callback_data="return_to_template_type"
            ),
            InlineKeyboardButton(
                text="Confirm", callback_data="confirm_single_template"
            ),
        ],
    ]
)


single_event_breaks_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Add break", callback_data="add_break")],
        [InlineKeyboardButton(text="Return", callback_data="return_to_breaks")],
    ]
)
