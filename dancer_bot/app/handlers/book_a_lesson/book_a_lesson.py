from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from app.database.requests.book_a_lesson.book_a_lesson import *
from app.database.requests.book_a_lesson.check_dancer import check_user_registered, check_couple_registered

from app.keyboards.book_a_lesson.book_a_lesson import *
from app.keyboards.start.start import start_keyboard

from app.scripts.auxiliary_functions.format_strings import format_string
from app.scripts.book_a_lesson.book_a_lesson import concatenate_couples, format_couple, format_lesson_info

from app.states.book_a_lesson.book_a_lesson import LessonRegistration
from app.states.book_a_lesson.register_dancer import UserRegistration

from app.templates.book_a_lesson.book_a_lesson import *

from sentry_logging.sentry_setup import sentry_sdk

router = Router()


@router.callback_query(lambda c: c.data == 'book_lessons')
async def command_book_a_lesson_handler(callback: types.CallbackQuery, state: FSMContext) -> None:

    try:
        await state.clear()

        user_info = await check_user_registered(callback.from_user.id)
        if user_info:
            couple_info = await check_couple_registered(user_info)
            if couple_info:

                await state.set_state(LessonRegistration.couples)
                await state.update_data(couples=couple_info)

                couples = concatenate_couples(couple_info)

                await callback.message.answer(format_string(choose_couple_message, ["\n".join(format_couple(couples))]),
                                     reply_markup=create_keyboard_for_choose_couple(couples))
            else:
                await callback.message.answer(register_couple_message, reply_markup=change_partner_solo_or_couple_keyboard)
        else:
            await state.set_state(UserRegistration.phone_number)
            await callback.message.answer(enter_phone_number_message, reply_markup=share_contact_keyboard)
            await callback.message.answer_photo(photo=FSInputFile("app/database/Share_contact.jpeg"))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.message(F.text == "Забронювати уроки 📅")
async def command_book_a_lesson_handler(message: types.Message, state: FSMContext) -> None:

    try:
        await state.clear()

        user_info = await check_user_registered(message.from_user.id)
        if user_info:
            couple_info = await check_couple_registered(user_info)
            if couple_info:

                await state.set_state(LessonRegistration.couples)
                await state.update_data(couples=couple_info)

                couples = concatenate_couples(couple_info)

                await message.answer(format_string(choose_couple_message, ["\n".join(format_couple(couples))]),
                                     reply_markup=create_keyboard_for_choose_couple(couples))
            else:
                await message.answer(register_couple_message, reply_markup=change_partner_solo_or_couple_keyboard)
        else:
            await state.set_state(UserRegistration.phone_number)
            await message.answer(enter_phone_number_message, reply_markup=share_contact_keyboard)
            await message.answer_photo(photo=FSInputFile("app/database/Share_contact.jpeg"))

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", message.from_user.id)
            scope.set_extra("username", message.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda c: c.data == 'change_couple')
async def handle_change_couple(callback_query: types.CallbackQuery) -> None:
    try:
        await callback_query.message.answer(change_partner_solo_or_couple_message,
                                            reply_markup=change_partner_solo_or_couple_keyboard)
    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data.startswith('couple_'))
async def handle_couple_selection(callback_query: types.CallbackQuery,
                                  state: FSMContext) -> None:

    try:
        couple_id = callback_query.data.split('_')[-1]

        await state.set_state(LessonRegistration.couple_id)
        await state.update_data(couple_id=couple_id)
        data = await state.get_data()
        await state.set_state(LessonRegistration.program)

        await callback_query.message.edit_text(format_string(choose_program_message,
                                                          concatenate_couples([data["couples"][int(couple_id)]])))
        await callback_query.message.edit_reply_markup(reply_markup=choose_program_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


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


@router.callback_query(lambda event: event.data.startswith('coach_'))
async def handle_coach_selection(callback_query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    try:
        coach_id = int(callback_query.data.split('_')[-1])
        data = await state.get_data()

        dates, lesson_restrictions, booked_lessons_count = await get_lessons_by_coach(coach_id,
                                                                                      data["couples"][int(data["couple_id"])]["couple_id"])

        for date in dates:
            if not bool(dates[date]):
                dates.pop(date)

        if not bool(dates):
            await callback_query.answer("На жаль, наразі в цього тренера нема вільних годин для занять :(",
                                        show_alert=True)
            return

        await state.update_data(coach_id=coach_id)
        await state.update_data(all_dates=dates)
        await state.update_data(available_dates=list(dates.keys()))
        await state.update_data(lesson_restrictions=lesson_restrictions)
        await state.update_data(booked_lessons_count=booked_lessons_count)
        await state.set_state(LessonRegistration.selected_dates)

        await callback_query.message.answer_photo(photo=FSInputFile("app/database/Unknown.jpeg"),
                                                  reply_markup=create_keyboard_for_dates(list(dates.keys())),
                                                  caption="Яка дата тебе цікавить? "
                                                  )
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
        lesson_restrictions = data.get('lesson_restrictions', None)
        booked_lessons_count = data.get('booked_lessons_count', 0)

        if callback_query.data.startswith('date_'):
            date_id = int(callback_query.data.split('_')[-1])
            date = available_dates[date_id]

            await state.update_data(current_date=date)

            await callback_query.message.edit_caption(caption="Тепер обери зручний для тебе час 🤩"
                                                              "Ти можеш обрати одразу кілька занять,"
                                                              " клікнувши на декілька кнопок.\n\n"
                                                              "<b>ЗВЕРНИ УВАГУ</b> 👇\n\n"
                                                              "❗Деякі тренери мають <b>обмеження по </b>"
                                                              "<b>кількості занять</b>, "
                                                              "перевищивши яке ти побачиш оповіщення.")

            await callback_query.message.edit_reply_markup(
                reply_markup=create_keyboard_for_time(list(all_dates[date].keys())))

        if callback_query.data.startswith('time_'):
            if lesson_restrictions and (len(choose_dates) + booked_lessons_count) >= lesson_restrictions:
                await callback_query.answer("Ви не можете забронювати більше уроків, ніж дозволено тренером.",
                                            show_alert=True)
                return

            time_id = callback_query.data.split('_')[-1]
            choose_dates.append(all_dates[current_date][time_id])

            all_dates[current_date].pop(time_id)
            await state.update_data(all_dates=all_dates, choose_dates=choose_dates)
            keyboard = create_keyboard_for_time(all_dates[current_date])

            await callback_query.message.edit_reply_markup(reply_markup=keyboard)

        if callback_query.data == 'return_to_dates':
            keyboard = create_keyboard_for_dates(available_dates)

            await callback_query.message.edit_caption(caption="Яка дата тебе цікавить?")
            await callback_query.message.edit_reply_markup(reply_markup=keyboard)

        if callback_query.data == 'book_lesson':
            await state.update_data(selected_dates=choose_dates)
            data_of_lessons = await get_lessons_info(choose_dates)

            await callback_query.message.edit_caption(caption=format_lesson_info(data_of_lessons, confirm_book_lessons_message))
            await callback_query.message.edit_reply_markup(reply_markup=confirm_book_lessons_keyboard)

            await state.set_state(LessonRegistration.confirmation)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)


@router.callback_query(lambda event: event.data == 'lesson_booking_confirmation')
async def command_book_lessons_handler(callback_query: types.CallbackQuery,
                                       state: FSMContext) -> None:
    try:
        data = await state.get_data()

        unavailable_lessons = await book_lessons(data["selected_dates"],
                                                 data["couples"][int(data["couple_id"])]["couple_id"],
                                                 data["coach_id"])

        await state.clear()

        if unavailable_lessons:
            await callback_query.answer(unavailable_lessons_message.format(", ".join(unavailable_lessons)),
                                        show_alert=True)

        await callback_query.message.answer(confirmed_book_lessons_message, reply_markup=start_keyboard)

    except Exception as e:

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra("user_id", callback_query.from_user.id)
            scope.set_extra("username", callback_query.from_user.username)

        sentry_sdk.capture_exception(e)
