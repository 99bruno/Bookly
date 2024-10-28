import re

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from app.keyboards.search_dancer.search_dancer import *
from app.keyboards.start.start import start_keyboard

from app.scripts.search_dancer.search_dancer import *

from app.templates.search_dancer.search_dancer import *
from app.templates.start.start import back_main_menu_message

from app.database.requests.search_dancer.search_dancer import *

from app.states.search_dancer.search_dancer import *

from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.callback_query(lambda event: event.data == 'latin_book_lesson' or event.data == 'ballroom_book_lesson')
async def handle_program_selection(callback: types.CallbackQuery,
                                   state: FSMContext) -> None:
    try:
        program = callback.data.split('_')[0].title()

        await state.update_data(program=program)
        coaches = await get_coaches_by_program(program)
        await state.update_data(coaches=coaches)
        await state.set_state(LessonRegistration.coach_id)

        data = await state.get_data()

        await callback.message.edit_text(available_dates_message)
        await callback.message.edit_reply_markup(reply_markup=create_keyboard_for_coaches(coaches, data["couple_id"]))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback.from_user.id)
            scope.set_extra("username", callback.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data.startswith('book_lesson_coach_'))
async def handle_coach_selection(callback_query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    try:
        coach_id = int(callback_query.data.split('_')[-1])
        data = await state.get_data()

        dates = await get_lessons_by_coach(coach_id,
                                           data["couple_id"])

        for date in dates:
            if not bool(dates[date]):
                dates.pop(date)

        if not bool(dates):
            await callback_query.answer("Unfortunately, this trainer currently has no available hours for classes :(",
                                        show_alert=True)
            return

        await state.update_data(coach_id=coach_id)
        await state.update_data(all_dates=dates)
        await state.update_data(available_dates=list(dates.keys()))
        await state.set_state(LessonRegistration.selected_dates)

        await callback_query.message.edit_text("Which date are you interested in?")
        await callback_query.message.edit_reply_markup(reply_markup=create_keyboard_for_dates(list(dates.keys())))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(LessonRegistration.selected_dates)
async def process_number_selection(callback_query: types.CallbackQuery,
                                   state: FSMContext):
    try:
        data = await state.get_data()

        choose_dates = data.get('choose_dates', [])
        all_dates = data.get('all_dates', [])
        available_dates = data.get('available_dates', [])
        current_date = data.get('current_date', None)

        if callback_query.data.startswith('date_'):
            date_id = int(callback_query.data.split('_')[-1])
            date = available_dates[date_id]

            await state.update_data(current_date=date)

            await callback_query.message.edit_text("Now choose a convenient time for you 🤩"
                                                   "You can choose several classes at once,"
                                                   " by clicking on several buttons.\n\n")

            await callback_query.message.edit_reply_markup(reply_markup=create_keyboard_for_time(list(all_dates[date].keys())))

        if callback_query.data.startswith('time_'):

            time_id = callback_query.data.split('_')[-1]
            choose_dates.append(all_dates[current_date][time_id])

            all_dates[current_date].pop(time_id)
            await state.update_data(all_dates=all_dates, choose_dates=choose_dates)
            keyboard = create_keyboard_for_time(all_dates[current_date])

            await callback_query.message.edit_reply_markup(reply_markup=keyboard)

        if callback_query.data == 'return_to_dates':
            keyboard = create_keyboard_for_dates(available_dates)

            await callback_query.message.edit_text("What date are you interested in?")
            await callback_query.message.edit_reply_markup(reply_markup=keyboard)

        if callback_query.data == 'book_lesson_to_confirm':
            await state.update_data(selected_dates=choose_dates)
            data_of_lessons = await get_lessons_info(choose_dates)

            await callback_query.message.edit_text(format_lesson_info(data_of_lessons, confirm_book_lessons_message))
            await callback_query.message.edit_reply_markup(reply_markup=confirm_book_lessons_keyboard)

            await state.set_state(LessonRegistration.confirmation)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data == 'booking_confirmation')
async def command_book_lessons_handler(callback_query: types.CallbackQuery,
                                       state: FSMContext) -> None:
    try:
        data = await state.get_data()

        unavailable_lessons = await book_lessons(data["selected_dates"],
                                                 data["couple_id"],
                                                 data["coach_id"])

        await state.clear()

        if unavailable_lessons:
            await callback_query.answer(unavailable_lessons_message.format(", ".join(unavailable_lessons)),
                                        show_alert=True)

        await return_to_schedule(callback_query, data)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


async def return_to_schedule(callback_query: types.CallbackQuery,
                             data) -> None:

    try:

        schedule = await get_booked_lessons_for_couple(data["couple_id"])

        await callback_query.message.answer(await couple_info_message_unpack({"name": data["couples_info"][data["current_couple_id"]]["name"]},
                                                                             couple_info_message, schedule),
                                            reply_markup=start_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)