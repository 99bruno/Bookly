from aiogram import F, Router, types
from aiogram.client.bot import Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards.start.start import start_keyboard
from app.scripts.auxiliary_functions.delete_messages import (
    delete_previous_messages_bot,
    delete_previous_messages_user,
)
from app.templates.start.start import back_main_menu_message, start_message
from sentry_logging.sentry_setup import sentry_sdk

from app.states.camp_info.edit_camp_info import EditEvent
from sqlalchemy.sql.functions import current_date

router = Router()


def create_keyboard_for_time(dates: list):
    keyboard = []
    row = []
    for date in dates:
        button = InlineKeyboardButton(text=date, callback_data=f"test_dates_{date}")
        row.append(button)
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(text="Обрати", callback_data=f"book_lesson"),
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"return_to_dates"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)



@router.callback_query(Command("test"))
async def command_edit_handler(message: types.Message, state: FSMContext) -> None:

    await state.update_data(dates=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            coaches=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            current_date=1,
                            current_coach=1
                            )


    await state.set_state(EditEvent.name)


@router.callback_query(EditEvent.name)
async def process_number_selection(
    callback_query: types.CallbackQuery, state: FSMContext
):
    try:
        data = await state.get_data()

        dates = data.get("dates", [])
        coaches = data.get("coaches", [])

        if callback_query.data.startswith("test_dates_"):
            date_id = int(callback_query.data.split("_")[-1])
            date = available_dates[date_id]

            await state.update_data(current_date=date)

            await callback_query.message.edit_caption(
                caption="Тепер обери зручний для тебе час 🤩"
                "Ти можеш обрати одразу кілька занять,"
                " клікнувши на декілька кнопок.\n\n"
                "<b>ЗВЕРНИ УВАГУ</b> 👇\n\n"
                "❗Деякі тренери мають <b>обмеження по </b>"
                "<b>кількості занять</b>, "
                "перевищивши яке ти побачиш оповіщення."
            )

            await callback_query.message.edit_reply_markup(
                reply_markup=create_keyboard_for_time(list(all_dates[date].keys()))
            )

        if callback_query.data.startswith("time_"):
            if (
                lesson_restrictions
                and (len(choose_dates) + booked_lessons_count) >= lesson_restrictions
            ):
                await callback_query.answer(
                    "Ви не можете забронювати більше уроків, ніж дозволено тренером.",
                    show_alert=True,
                )
                return

            time_id = callback_query.data.split("_")[-1]
            choose_dates.append(all_dates[current_date][time_id])

            all_dates[current_date].pop(time_id)
            await state.update_data(all_dates=all_dates, choose_dates=choose_dates)
            keyboard = create_keyboard_for_time(all_dates[current_date])

            await callback_query.message.edit_reply_markup(reply_markup=keyboard)

        if callback_query.data == "return_to_dates":
            keyboard = create_keyboard_for_dates(available_dates)

            await callback_query.message.edit_caption(caption="Яка дата тебе цікавить?")
            await callback_query.message.edit_reply_markup(reply_markup=keyboard)

        if callback_query.data == "book_lesson":
            await state.update_data(selected_dates=choose_dates)
            data_of_lessons = await get_lessons_info(choose_dates)

            await callback_query.message.edit_caption(
                caption=format_lesson_info(
                    data_of_lessons, confirm_book_lessons_message
                )
            )
            await callback_query.message.edit_reply_markup(
                reply_markup=confirm_book_lessons_keyboard
            )

            await state.set_state(LessonRegistration.confirmation)

    except Exception as e:
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)